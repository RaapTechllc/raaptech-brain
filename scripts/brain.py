#!/usr/bin/env python3
"""brain.py — deterministic retrieval CLI for the raaptech-brain bundle.

Zero third-party dependencies (stdlib only, Python 3.10+). Implements the
"code before model" retrieval ladder from the 2026-07-07 design spec:

  ask      question -> keywords -> score catalogue lines (no file opens) ->
           open ONLY the top file -> extract ONLY the winning section ->
           follow at most one pointer link -> print an evidence block.
  save     atomically write a dated fact into a domain file, append the
           catalogue line, and log the change (index can never drift).
  reindex  rebuild catalog.md from scratch by scanning every domain file.
  bench    run scripts/bench-questions.json through the ask pipeline and
           report hit/miss, latency, and evidence-vs-naive token counts.
  html     render dashboard.html from scripts/dashboard_template.html.

Usage:
  python scripts/brain.py ask "what is the daily cost cap?" [--json]
  python scripts/brain.py save --domain fleet --title "New NAS disk" "fact text"
  python scripts/brain.py reindex
  python scripts/brain.py bench
  python scripts/brain.py html
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG_PATH = ROOT / "catalog.md"
LOG_PATH = ROOT / "log.md"
BENCH_QUESTIONS = ROOT / "scripts" / "bench-questions.json"
BENCH_RESULTS = ROOT / "scripts" / "bench-results.json"
DASHBOARD_TEMPLATE = ROOT / "scripts" / "dashboard_template.html"
DASHBOARD_OUT = ROOT / "dashboard.html"

DOMAINS = [
    "architecture",
    "sessions",
    "fleet",
    "business",
    "skills",
    "integrations",
    "research",
    "references",
]

SKIP_FILES = {"index.md", "log.md"}

MAX_KEYWORDS = 8
MIN_CONFIDENT_SCORE = 4  # below this, `ask` refuses to guess
POINTER_BODY_LIMIT = 320  # section bodies shorter than this may be pointers

STOPWORDS = {
    "a", "about", "after", "all", "also", "an", "and", "any", "are", "as",
    "at", "be", "been", "before", "being", "between", "both", "but", "by",
    "can", "cannot", "could", "did", "do", "does", "doing", "down", "during",
    "each", "else", "every", "for", "from", "get", "got", "had", "has",
    "have", "having", "he", "her", "here", "him", "his", "how", "i", "if",
    "in", "into", "is", "it", "its", "just", "may", "me", "might", "more",
    "most", "must", "my", "no", "not", "now", "of", "off", "on", "one",
    "only", "or", "other", "our", "out", "over", "own", "per", "s", "same",
    "see", "shall", "she", "should", "so", "some", "such", "t", "than",
    "that", "the", "their", "them", "then", "there", "these", "they", "this",
    "those", "through", "to", "too", "under", "until", "up", "us", "use",
    "used", "uses", "using", "very", "via", "was", "we", "were", "what",
    "whats", "when", "where", "which", "while", "who", "whom", "whose",
    "why", "will", "with", "would", "you", "your",
}


# ---------------------------------------------------------------------------
# Text primitives
# ---------------------------------------------------------------------------

def slugify(heading: str) -> str:
    """GitHub-style anchor slug: lowercase, strip punctuation, spaces->hyphens."""
    text = heading.strip().lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"\s", "-", text)
    return text


def tokenize(text: str) -> list[str]:
    """Lowercase alphanumeric tokens (hyphens/slashes split into words)."""
    return re.findall(r"[a-z0-9]+", text.lower())


def keywords_of(text: str, limit: int | None = None) -> list[str]:
    """Stopword-stripped, deduped, order-preserving keywords of `text`."""
    out: list[str] = []
    seen: set[str] = set()
    for tok in tokenize(text):
        if tok in STOPWORDS or tok in seen:
            continue
        seen.add(tok)
        out.append(tok)
        if limit and len(out) >= limit:
            break
    return out


def tokens_match(query_tok: str, candidate: str) -> bool:
    """Exact match, or prefix match when both tokens are 4+ chars (backup~backups)."""
    if query_tok == candidate:
        return True
    if len(query_tok) >= 4 and len(candidate) >= 4:
        return candidate.startswith(query_tok) or query_tok.startswith(candidate)
    return False


def approx_tokens(text: str) -> int:
    """Cheap token estimate: len/4."""
    return max(1, len(text) // 4)


# ---------------------------------------------------------------------------
# Markdown parsing (no yaml dependency — simple line parsing)
# ---------------------------------------------------------------------------

def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Parse simple `key: value` YAML frontmatter. Returns (frontmatter, body).

    Handles quoted scalars and inline lists (`tags: [a, b]`). Anything more
    exotic degrades gracefully to the raw string value.
    """
    if not text.startswith("---"):
        return {}, text
    lines = text.splitlines()
    fm: dict = {}
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
        line = lines[i]
        if ":" not in line or line.startswith((" ", "\t", "#")):
            continue
        key, _, val = line.partition(":")
        val = val.strip()
        if val.startswith("[") and val.endswith("]"):
            fm[key.strip()] = [
                v.strip().strip("\"'") for v in val[1:-1].split(",") if v.strip()
            ]
        else:
            fm[key.strip()] = val.strip("\"'")
    if end is None:
        return {}, text
    return fm, "\n".join(lines[end + 1:])


def iter_headings(body: str):
    """Yield (level, heading_text, line_index) for headings outside code fences."""
    in_fence = False
    for i, line in enumerate(body.splitlines()):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if m:
            yield len(m.group(1)), m.group(2), i


def slugged_headings(body: str) -> list[tuple[int, str, int, str]]:
    """iter_headings plus GitHub-style anchor dedup.

    Yields (level, heading, line_index, slug). Repeated heading slugs within
    one file get -1, -2, ... suffixes so every section stays addressable.
    """
    counts: dict[str, int] = {}
    out: list[tuple[int, str, int, str]] = []
    for lvl, heading, idx in iter_headings(body):
        base = slugify(heading)
        n = counts.get(base, 0)
        counts[base] = n + 1
        out.append((lvl, heading, idx, base if n == 0 else f"{base}-{n}"))
    return out


def first_sentence(text: str, limit: int = 160) -> str:
    """First prose sentence of `text`, markdown-stripped, capped at `limit` chars."""
    in_fence = False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        stripped = line.strip()
        if in_fence or not stripped or stripped.startswith(("#", "|", ">", "---")):
            continue
        # strip markdown emphasis, links, list bullets
        stripped = re.sub(r"^[*\-+\d.]+\s+", "", stripped)
        stripped = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", stripped)
        stripped = stripped.replace("**", "").replace("`", "").replace("|", "/")
        if not stripped:
            continue
        sentence = stripped.split(". ")[0].rstrip(".") + "."
        if len(sentence) > limit:
            sentence = sentence[:limit].rsplit(" ", 1)[0].rstrip(" ,;") + " ..."
        return sentence.strip()
    return ""


def extract_section(body: str, anchor: str) -> str | None:
    """Section for `anchor`: heading line through to next same-or-higher heading.

    Empty anchor means the whole body (file-level catalogue entry).
    Returns None when the anchor is not found.
    """
    if not anchor:
        return body.strip()
    lines = body.splitlines()
    start = None
    level = 0
    for lvl, _heading, idx, slug in slugged_headings(body):
        if start is None:
            if slug == anchor:
                start, level = idx, lvl
        elif lvl <= level:
            return "\n".join(lines[start:idx]).strip()
    if start is not None:
        return "\n".join(lines[start:]).strip()
    return None


# ---------------------------------------------------------------------------
# Catalogue model
# ---------------------------------------------------------------------------

@dataclass
class CatalogEntry:
    """One retrievable unit: a file or a file#anchor section."""

    path: str                     # bundle-relative posix path
    anchor: str                   # "" for file-level entries
    keywords: list[str]
    description: str
    path_tokens: list[str] = field(default_factory=list)
    desc_tokens: list[str] = field(default_factory=list)

    def __post_init__(self):
        self.path_tokens = keywords_of(f"{self.path} {self.anchor}")
        self.desc_tokens = keywords_of(self.description)

    @property
    def ref(self) -> str:
        return f"{self.path}#{self.anchor}" if self.anchor else self.path

    @property
    def domain(self) -> str:
        return self.path.split("/", 1)[0]

    def line(self) -> str:
        return f"{self.ref} | {' '.join(self.keywords)} | {self.description}"


def scan_file(path: Path) -> list[CatalogEntry]:
    """Catalogue entries for one markdown file: file-level + one per H2/H3."""
    rel = path.relative_to(ROOT).as_posix()
    fm, body = parse_frontmatter(path.read_text(encoding="utf-8"))
    title = str(fm.get("title", path.stem))
    description = str(fm.get("description", "")) or first_sentence(body)
    tags = fm.get("tags", [])
    tag_text = " ".join(tags) if isinstance(tags, list) else str(tags)

    entries = [CatalogEntry(
        path=rel,
        anchor="",
        keywords=keywords_of(f"{title} {tag_text} {description}", MAX_KEYWORDS),
        description=description.replace("|", "/"),
    )]

    lines = body.splitlines()
    headings = slugged_headings(body)
    for pos, (level, heading, idx, slug) in enumerate(headings):
        if level not in (2, 3) or not slug:
            continue  # empty slug (punctuation-only heading) is unaddressable
        end = next((j for lvl, _, j, _ in headings[pos + 1:] if lvl <= level),
                   len(lines))
        section_body = "\n".join(lines[idx + 1:end])
        desc = first_sentence(section_body) or f"{heading} — see {title}."
        entries.append(CatalogEntry(
            path=rel,
            anchor=slug,
            keywords=keywords_of(f"{heading} {title} {desc}", MAX_KEYWORDS),
            description=desc.replace("|", "/"),
        ))
    return entries


def build_catalog() -> list[CatalogEntry]:
    """Scan every domain dir and produce the full catalogue."""
    entries: list[CatalogEntry] = []
    for domain in DOMAINS:
        ddir = ROOT / domain
        if not ddir.is_dir():
            continue
        for md in sorted(ddir.rglob("*.md")):
            if md.name in SKIP_FILES:
                continue
            entries.extend(scan_file(md))
    return entries


def load_catalog() -> list[CatalogEntry]:
    """Parse catalog.md; malformed lines are skipped with a stderr warning."""
    if not CATALOG_PATH.exists():
        sys.stderr.write(
            "warning: catalog.md missing — run `python scripts/brain.py reindex`\n")
        return []
    entries: list[CatalogEntry] = []
    for lineno, raw in enumerate(
            CATALOG_PATH.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = [p.strip() for p in line.split("|", 2)]
        if len(parts) != 3 or not parts[0]:
            sys.stderr.write(f"warning: catalog.md:{lineno}: malformed line skipped\n")
            continue
        ref, kws, desc = parts
        path, _, anchor = ref.partition("#")
        entries.append(CatalogEntry(
            path=path.strip(), anchor=anchor.strip(),
            keywords=kws.split(), description=desc))
    return entries


# ---------------------------------------------------------------------------
# ask — the retrieval ladder
# ---------------------------------------------------------------------------

def score_entry(entry: CatalogEntry, qtokens: list[str]) -> int:
    """Weighted keyword score: path/title 3, keywords 2, description 1."""
    score = 0
    for q in qtokens:
        if any(tokens_match(q, t) for t in entry.path_tokens):
            score += 3
        if any(tokens_match(q, t) for t in entry.keywords):
            score += 2
        if any(tokens_match(q, t) for t in entry.desc_tokens):
            score += 1
    return score


def find_pointer(section: str, source: Path) -> tuple[Path, str] | None:
    """If `section` is mostly a pointer, resolve its first in-bundle .md link.

    A pointer is a short body (under POINTER_BODY_LIMIT chars, excluding the
    heading line) containing a relative or bundle-absolute markdown link.
    Absolute filesystem/URL links are never followed.
    """
    body_lines = section.splitlines()[1:]  # drop the heading line
    body = "\n".join(body_lines).strip()
    if len(body) > POINTER_BODY_LIMIT:
        return None
    for m in re.finditer(r"\[[^\]]*\]\(([^)#\s]+\.md)(#([^)]+))?\)", body):
        target, anchor = m.group(1), m.group(3) or ""
        if target.startswith("http") or re.match(r"^[A-Za-z]:", target):
            continue  # external URL or absolute Windows path — out of bundle
        if target.startswith("/"):
            resolved = (ROOT / target.lstrip("/")).resolve()
        else:
            resolved = (source.parent / target).resolve()
        if resolved.is_file() and ROOT in resolved.parents:
            return resolved, anchor
    return None


def run_ask(question: str) -> dict:
    """Full ask pipeline. Returns a machine-readable result dict."""
    qtokens = keywords_of(question)
    catalog = load_catalog()
    if not catalog:
        return {"query": question, "keywords": qtokens, "matched": False,
                "reason": "empty catalogue", "suggestion": "index.md"}

    scored = [(score_entry(e, qtokens), e) for e in catalog]
    # Prefer anchored (section-level) entries on ties: tighter evidence.
    best_score, best = max(scored, key=lambda se: (se[0], bool(se[1].anchor)))

    if best_score < MIN_CONFIDENT_SCORE:
        domain_totals: dict[str, int] = {}
        for s, e in scored:
            domain_totals[e.domain] = domain_totals.get(e.domain, 0) + s
        nearest = max(domain_totals, key=domain_totals.get) if domain_totals else ""
        return {
            "query": question, "keywords": qtokens, "matched": False,
            "best_score": best_score,
            "reason": f"best score {best_score} below threshold {MIN_CONFIDENT_SCORE}",
            "suggestion": f"{nearest}/index.md" if nearest else "index.md",
        }

    source = ROOT / best.path
    if not source.is_file():
        return {"query": question, "keywords": qtokens, "matched": False,
                "reason": f"catalogue points to missing file {best.path}",
                "suggestion": f"{best.domain}/index.md"}

    _, body = parse_frontmatter(source.read_text(encoding="utf-8"))
    section = extract_section(body, best.anchor)
    if section is None:
        sys.stderr.write(
            f"warning: anchor #{best.anchor} not found in {best.path}; "
            "using whole file (run reindex)\n")
        section = body.strip()

    pointer_ref = None
    pointer = find_pointer(section, source)
    if pointer:
        ptarget, panchor = pointer
        _, pbody = parse_frontmatter(ptarget.read_text(encoding="utf-8"))
        psection = extract_section(pbody, panchor) if panchor else pbody.strip()
        if psection:
            prel = ptarget.relative_to(ROOT).as_posix()
            pointer_ref = f"{prel}#{panchor}" if panchor else prel
            section = f"{section}\n\n--- pointer -> {pointer_ref} ---\n\n{psection}"

    return {
        "query": question, "keywords": qtokens, "matched": True,
        "source": best.ref, "file": best.path, "anchor": best.anchor,
        "score": best_score, "tokens": approx_tokens(section),
        "pointer": pointer_ref, "evidence": section,
    }


def cmd_ask(args) -> int:
    result = run_ask(args.question)
    if args.json:
        print(json.dumps(result, indent=2))
        return 0 if result["matched"] else 1
    if not result["matched"]:
        print(f"No confident match ({result.get('reason', 'low score')}).")
        print(f"Try browsing: {result['suggestion']}")
        return 1
    print(f"SOURCE: {result['source']}")
    print(f"SCORE: {result['score']} | TOKENS: ~{result['tokens']}")
    if result["pointer"]:
        print(f"POINTER FOLLOWED: {result['pointer']}")
    print("-" * 60)
    print(result["evidence"])
    print("-" * 60)
    return 0


# ---------------------------------------------------------------------------
# reindex
# ---------------------------------------------------------------------------

CATALOG_HEADER = """\
# RaapTech Brain catalogue — one line per retrievable section.
# Format: path#anchor | keywords | one-sentence description
# GENERATED — never hand-edit. Update via `python scripts/brain.py save`
# (append) or `python scripts/brain.py reindex` (full rebuild).
"""


def cmd_reindex(_args) -> int:
    entries = build_catalog()
    lines = [CATALOG_HEADER] + [e.line() for e in entries]
    CATALOG_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"catalog.md rebuilt: {len(entries)} entries "
          f"({sum(1 for e in entries if not e.anchor)} files, "
          f"{sum(1 for e in entries if e.anchor)} sections)")
    return 0


# ---------------------------------------------------------------------------
# save — atomic fact write
# ---------------------------------------------------------------------------

def pick_target_file(domain: str, title: str, fact: str) -> Path:
    """Most relevant existing file in `domain`, else <domain>/memories.md.

    Relevance = number of distinct save-keywords found in the candidate's
    frontmatter title/description/tags. Needs >= 2 hits to piggyback on an
    existing file; otherwise the fact goes to memories.md.
    """
    save_kws = keywords_of(f"{title} {fact}")
    best_path, best_hits = None, 0
    ddir = ROOT / domain
    for md in sorted(ddir.glob("*.md")) if ddir.is_dir() else []:
        if md.name in SKIP_FILES:
            continue
        fm, _ = parse_frontmatter(md.read_text(encoding="utf-8"))
        tags = fm.get("tags", [])
        tag_text = " ".join(tags) if isinstance(tags, list) else str(tags)
        cand = set(keywords_of(
            f"{fm.get('title', '')} {fm.get('description', '')} {tag_text}"))
        hits = sum(1 for k in save_kws if any(tokens_match(k, c) for c in cand))
        if hits > best_hits:
            best_path, best_hits = md, hits
    if best_path is not None and best_hits >= 2:
        return best_path
    return ddir / "memories.md"


def cmd_save(args) -> int:
    domain, title, fact = args.domain, args.title, args.fact
    if domain not in DOMAINS:
        print(f"Unknown domain '{domain}'. Valid domains: {', '.join(DOMAINS)}",
              file=sys.stderr)
        return 2

    now = datetime.now(timezone.utc)
    date = now.strftime("%Y-%m-%d")
    stamp = now.strftime("%Y-%m-%dT%H:%M:%SZ")

    target = pick_target_file(domain, title, fact)
    rel = target.relative_to(ROOT).as_posix()
    heading = f"{title} ({date})"
    target_text = target.read_text(encoding="utf-8") if target.exists() else None
    # GitHub-style dedup: saving the same title twice in one day must not
    # collide — the new section gets a -1/-2 suffixed anchor.
    base = slugify(heading)
    if target_text is not None:
        _, tbody = parse_frontmatter(target_text)
        existing = sum(1 for _, h, _ in iter_headings(tbody)
                       if slugify(h) == base)
        anchor = base if existing == 0 else f"{base}-{existing}"
    else:
        anchor = base
    desc = first_sentence(fact) or f"{title}."
    entry = CatalogEntry(
        path=rel, anchor=anchor,
        keywords=keywords_of(f"{title} {desc}", MAX_KEYWORDS),
        description=desc.replace("|", "/"))
    section_md = f"\n## {heading}\n\n{fact.strip()}\n"

    # --- prepare every write up front (all-or-nothing ordering) -------------
    if target_text is not None:
        new_target_text = target_text.rstrip("\n") + "\n" + section_md
    else:
        new_target_text = (
            "---\n"
            "type: Concept\n"
            f"title: {domain.capitalize()} Memories\n"
            f"description: Durable facts saved into the {domain} domain via brain save.\n"
            f"tags: [{domain}, memories, brain-save]\n"
            f"timestamp: {stamp}\n"
            "---\n"
            f"\n# {domain.capitalize()} Memories\n"
            f"{section_md}")

    catalog_text = CATALOG_PATH.read_text(encoding="utf-8") \
        if CATALOG_PATH.exists() else CATALOG_HEADER + "\n"
    new_catalog_text = catalog_text.rstrip("\n") + "\n" + entry.line() + "\n"

    log_text = LOG_PATH.read_text(encoding="utf-8") if LOG_PATH.exists() \
        else "# Bundle Update Log\n"
    log_line = f"* **Memory**: brain save — {domain}: {title} -> {entry.ref}"
    if f"## {date}" in log_text:
        new_log_text = log_text.rstrip("\n") + "\n" + log_line + "\n"
    else:
        new_log_text = log_text.rstrip("\n") + f"\n\n## {date}\n{log_line}\n"

    # --- commit: fact file, then catalogue, then log; roll back on failure --
    originals = {
        target: target_text,
        CATALOG_PATH: catalog_text if CATALOG_PATH.exists() else None,
        LOG_PATH: log_text if LOG_PATH.exists() else None,
    }
    written: list[Path] = []
    try:
        for path, text in ((target, new_target_text),
                           (CATALOG_PATH, new_catalog_text),
                           (LOG_PATH, new_log_text)):
            path.write_text(text, encoding="utf-8")
            written.append(path)
    except OSError as exc:
        for path in written:
            orig = originals[path]
            if orig is None:
                path.unlink(missing_ok=True)
            else:
                path.write_text(orig, encoding="utf-8")
        print(f"save failed, rolled back: {exc}", file=sys.stderr)
        return 1

    print(f"saved: {entry.ref}")
    print(f"catalogued: {entry.line()}")
    return 0


# ---------------------------------------------------------------------------
# bench
# ---------------------------------------------------------------------------

def cmd_bench(_args) -> int:
    if not BENCH_QUESTIONS.exists():
        print(f"missing {BENCH_QUESTIONS.relative_to(ROOT).as_posix()}",
              file=sys.stderr)
        return 2
    questions = json.loads(BENCH_QUESTIONS.read_text(encoding="utf-8"))

    results = []
    for item in questions:
        question, expect = item["question"], item["expect"]
        t0 = time.perf_counter()
        res = run_ask(question)
        latency_ms = round((time.perf_counter() - t0) * 1000, 1)
        evidence = res.get("evidence", "")
        hit = res["matched"] and expect.lower() in evidence.lower()
        naive_tokens = 0
        if res.get("file"):
            fpath = ROOT / res["file"]
            if fpath.is_file():
                naive_tokens = approx_tokens(fpath.read_text(encoding="utf-8"))
        results.append({
            "question": question,
            "hit": hit,
            "file": res.get("source", "-"),
            "latency_ms": latency_ms,
            "evidence_tokens": res.get("tokens", 0) if res["matched"] else 0,
            "naive_tokens": naive_tokens,
        })

    print("| question | hit | file | latency ms | evidence tokens | naive tokens |")
    print("|---|---|---|---|---|---|")
    for r in results:
        mark = "PASS" if r["hit"] else "MISS"
        print(f"| {r['question']} | {mark} | {r['file']} | {r['latency_ms']} "
              f"| {r['evidence_tokens']} | {r['naive_tokens']} |")

    hits = sum(1 for r in results if r["hit"])
    ev = sum(r["evidence_tokens"] for r in results)
    nv = sum(r["naive_tokens"] for r in results)
    print(f"\n{hits}/{len(results)} hit — evidence {ev} tokens vs naive {nv} tokens "
          f"({(100 * (1 - ev / nv)):.0f}% saved)" if nv else f"\n{hits}/{len(results)} hit")

    BENCH_RESULTS.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    return 0 if hits == len(results) else 1


# ---------------------------------------------------------------------------
# html
# ---------------------------------------------------------------------------

def cmd_html(_args) -> int:
    if not DASHBOARD_TEMPLATE.exists():
        print("missing scripts/dashboard_template.html — cannot render dashboard",
              file=sys.stderr)
        return 2
    catalog_json = json.dumps([
        {"path": e.path, "anchor": e.anchor, "keywords": e.keywords,
         "description": e.description, "domain": e.domain}
        for e in load_catalog()
    ]).replace("</", "<\\/")  # raw "</script>" in content would end the JSON block
    bench_json = (BENCH_RESULTS.read_text(encoding="utf-8").strip()
                  if BENCH_RESULTS.exists() else "[]").replace("</", "<\\/")
    html = DASHBOARD_TEMPLATE.read_text(encoding="utf-8")
    html = html.replace("__CATALOG_JSON__", catalog_json)
    html = html.replace("__BENCH_JSON__", bench_json)
    html = html.replace("__GENERATED_AT__",
                        datetime.now(timezone.utc).isoformat(timespec="seconds"))
    DASHBOARD_OUT.write_text(html, encoding="utf-8")
    print(f"wrote {DASHBOARD_OUT.relative_to(ROOT).as_posix()}")
    return 0


# ---------------------------------------------------------------------------
# entry point
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    # Windows consoles default to cp1252; bundle content is UTF-8.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(
        prog="brain", description="Deterministic retrieval for raaptech-brain.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_ask = sub.add_parser("ask", help="answer a question from the catalogue")
    p_ask.add_argument("question")
    p_ask.add_argument("--json", action="store_true", help="machine output")
    p_ask.set_defaults(func=cmd_ask)

    p_save = sub.add_parser("save", help="save a durable fact atomically")
    p_save.add_argument("--domain", required=True)
    p_save.add_argument("--title", required=True)
    p_save.add_argument("fact")
    p_save.set_defaults(func=cmd_save)

    p_re = sub.add_parser("reindex", help="rebuild catalog.md from scratch")
    p_re.set_defaults(func=cmd_reindex)

    p_bench = sub.add_parser("bench", help="run the retrieval benchmark")
    p_bench.set_defaults(func=cmd_bench)

    p_html = sub.add_parser("html", help="render dashboard.html")
    p_html.set_defaults(func=cmd_html)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
