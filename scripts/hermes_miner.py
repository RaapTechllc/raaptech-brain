#!/usr/bin/env python3
"""Hermes Miner — thin-proof Insight mining from Hermes memories only.

Reads allowlisted Hermes memory files, emits candidate Insights into
docs/mine/candidates.md. Never writes brain domain files or catalog.md.

Usage:
  python scripts/hermes_miner.py              # mine + write staging
  python scripts/hermes_miner.py --dry-run    # print candidates only
  python scripts/hermes_miner.py --max 20     # candidate cap (default 20)

Allowlist (thin proof):
  %LOCALAPPDATA%/hermes/memories/*.md   (skips *.lock and non-.md)
"""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

BUNDLE_ROOT = Path(__file__).resolve().parent.parent
STAGING_CANDIDATES = BUNDLE_ROOT / "docs" / "mine" / "candidates.md"
DEFAULT_HERMES_MEMORIES = Path(
    os.environ.get("HERMES_HOME", Path.home() / "AppData" / "Local" / "hermes")
) / "memories"
DEFAULT_MAX = 20

DOMAINS = (
    "architecture",
    "fleet",
    "business",
    "skills",
    "integrations",
    "research",
    "references",
    "sessions",
)

# Hard reject — Secrets never become candidates.
SECRET_PATTERNS = [
    re.compile(p, re.I)
    for p in (
        r"\b(api[_-]?key|secret[_-]?key|access[_-]?token|refresh[_-]?token)\b\s*[:=]",
        r"\bBearer\s+[A-Za-z0-9\-._~+/]+=*",
        r"\bsk-[A-Za-z0-9]{10,}\b",
        r"\bxai-[A-Za-z0-9]{10,}\b",
        r"\bghp_[A-Za-z0-9]{20,}\b",
        r"\bpassword\s*[:=]\s*\S+",
        r"\bpw\s*[:=]\s*\S+",
        r"-----BEGIN (RSA |OPENSSH |EC )?PRIVATE KEY-----",
        r"\bAKIA[0-9A-Z]{16}\b",
    )
]

# Soft skip — not operational Insights (personality / filler).
SKIP_SOFT = [
    re.compile(p, re.I)
    for p in (
        r"\bHormozi\b",
        r"\bhates filler\b",
        r"\bno-nonsense\b.*\bStyle:",
        r"^Style:\s*",
    )
]

DOMAIN_HINTS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\b(ollama|glm|nemotron|deepseek|grok|model routing|quota|cron)\b", re.I), "architecture"),
    (re.compile(r"\b(truenas|proxmox|tailscale|fleet|vm\s*\d+|ssh|rtx|pve)\b", re.I), "fleet"),
    (re.compile(r"\b(trading|tradingview|alpaca|council|smw|sheet metal|bluehost)\b", re.I), "business"),
    (re.compile(r"\b(morning brief|lab pulse|super brain|daily ops)\b", re.I), "business"),
    (re.compile(r"\b(hermes|oauth|auth\.json|secrets_index|mcp)\b", re.I), "integrations"),
    (re.compile(r"\b(delegation|subagent|swarm|agent)\b", re.I), "skills"),
]


@dataclass
class Candidate:
    claim: str
    source_path: str
    evidence: str
    proposed_domain: str
    miner: str = "hermes"
    gate_decision: str = "pending"
    gate_reason: str = ""


def configure_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")


def is_secret(text: str) -> bool:
    return any(p.search(text) for p in SECRET_PATTERNS)


def is_soft_skip(text: str) -> bool:
    return any(p.search(text) for p in SKIP_SOFT)


def propose_domain(text: str) -> str:
    scores: dict[str, int] = {d: 0 for d in DOMAINS}
    for pattern, domain in DOMAIN_HINTS:
        hits = pattern.findall(text)
        if hits:
            scores[domain] += len(hits)
    best = max(DOMAINS, key=lambda d: scores[d])
    return best if scores[best] > 0 else "references"


def claim_from_block(block: str) -> str:
    """One-sentence claim: first sentence, trimmed, capped."""
    cleaned = re.sub(r"\s+", " ", block.strip())
    # Prefer first sentence-ish chunk
    parts = re.split(r"(?<=[.!?])\s+", cleaned)
    claim = parts[0] if parts else cleaned
    if len(claim) > 220:
        claim = claim[:217].rstrip() + "..."
    return claim


def evidence_from_block(block: str) -> str:
    cleaned = re.sub(r"\s+", " ", block.strip())
    if len(cleaned) > 180:
        return cleaned[:177].rstrip() + "..."
    return cleaned


def allowlisted_sources(memories_dir: Path) -> list[Path]:
    """Only live .md files directly under hermes/memories — no archives."""
    if not memories_dir.is_dir():
        return []
    # Refuse paths that look like archives/backups even if mis-pointed.
    forbidden = ("archive", "backup", "_agent-md-backups", "openclaw-agents")
    parts_lower = {p.lower() for p in memories_dir.parts}
    if parts_lower & set(forbidden):
        return []
    out: list[Path] = []
    for md in sorted(memories_dir.glob("*.md")):
        if md.name.endswith(".lock") or md.suffix.lower() != ".md":
            continue
        if any(tok in md.name.lower() for tok in ("backup", "archive", "pre-")):
            continue
        out.append(md)
    return out


def parse_blocks(text: str) -> list[str]:
    """Hermes memories use § as entry separators; also accept blank-line paragraphs."""
    if "§" in text:
        raw = [b.strip() for b in text.split("§")]
    else:
        raw = [b.strip() for b in re.split(r"\n\s*\n", text)]
    return [b for b in raw if len(b) >= 40]


def mine_file(path: Path) -> list[Candidate]:
    text = path.read_text(encoding="utf-8")
    candidates: list[Candidate] = []
    for block in parse_blocks(text):
        if is_secret(block):
            continue
        if is_soft_skip(block):
            continue
        claim = claim_from_block(block)
        if is_secret(claim):
            continue
        candidates.append(
            Candidate(
                claim=claim,
                source_path=str(path),
                evidence=evidence_from_block(block),
                proposed_domain=propose_domain(block),
            )
        )
    return candidates


def render_candidates(candidates: list[Candidate]) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    lines = [
        "---",
        "type: Reference",
        "title: Mine Candidates Staging",
        "description: Hermes Miner thin-proof candidate queue. Regenerated each pass; gitignored.",
        "tags: [mine-pass, staging, hermes-miner]",
        f"timestamp: {now}",
        "---",
        "",
        "# Candidates",
        "",
        f"Generated by Hermes Miner at {now}. Cap applied. Gate decisions are pending.",
        "",
    ]
    if not candidates:
        lines.append("No candidates emitted.")
        lines.append("")
        return "\n".join(lines)

    for i, c in enumerate(candidates, 1):
        cid = f"C-{i:03d}"
        lines.extend(
            [
                f"## {cid}",
                "",
                f"- **claim:** {c.claim}",
                f"- **source_path:** `{c.source_path}`",
                f"- **evidence:** {c.evidence}",
                f"- **proposed_domain:** {c.proposed_domain}",
                f"- **miner:** {c.miner}",
                f"- **gate_decision:** {c.gate_decision}",
                f"- **gate_reason:** {c.gate_reason}",
                "",
            ]
        )
    return "\n".join(lines)


def fingerprint_brain() -> str:
    """Hash domain markdown + catalog so we can prove Miner did not write them."""
    h = hashlib.sha256()
    catalog = BUNDLE_ROOT / "catalog.md"
    if catalog.exists():
        h.update(catalog.read_bytes())
    for domain in DOMAINS:
        ddir = BUNDLE_ROOT / domain
        if not ddir.is_dir():
            continue
        for md in sorted(ddir.rglob("*.md")):
            h.update(md.relative_to(BUNDLE_ROOT).as_posix().encode())
            h.update(md.read_bytes())
    return h.hexdigest()


def main() -> int:
    configure_stdio()
    parser = argparse.ArgumentParser(description="Hermes Miner — thin-proof candidate emitter")
    parser.add_argument(
        "--memories",
        type=Path,
        default=DEFAULT_HERMES_MEMORIES,
        help="Allowlisted Hermes memories directory",
    )
    parser.add_argument("--max", type=int, default=DEFAULT_MAX, help="Max candidates (default 20)")
    parser.add_argument("--dry-run", action="store_true", help="Print candidates; do not write staging")
    parser.add_argument(
        "--out",
        type=Path,
        default=STAGING_CANDIDATES,
        help="Staging candidates path (default docs/mine/candidates.md)",
    )
    args = parser.parse_args()

    memories_dir = args.memories.resolve()
    # Thin-proof path rule: must be .../hermes/memories (or HERMES_HOME/memories)
    if memories_dir.name.lower() != "memories":
        print(f"Refusing path — allowlist requires a 'memories' directory: {memories_dir}",
              file=sys.stderr)
        return 2
    if "archive" in {p.lower() for p in memories_dir.parts}:
        print(f"Refusing archive path: {memories_dir}", file=sys.stderr)
        return 2

    sources = allowlisted_sources(memories_dir)
    if not sources:
        print(f"No allowlisted .md files under {memories_dir}", file=sys.stderr)
        return 1

    before = fingerprint_brain()
    all_cands: list[Candidate] = []
    skipped_secret = 0
    for src in sources:
        raw_blocks = parse_blocks(src.read_text(encoding="utf-8"))
        for block in raw_blocks:
            if is_secret(block):
                skipped_secret += 1
        mined = mine_file(src)
        all_cands.extend(mined)

    # Dedupe by claim text
    seen: set[str] = set()
    unique: list[Candidate] = []
    for c in all_cands:
        key = c.claim.lower()
        if key in seen:
            continue
        seen.add(key)
        unique.append(c)

    capped = unique[: max(0, args.max)]
    body = render_candidates(capped)

    print(f"Hermes Miner — thin proof")
    print(f"  memories: {memories_dir}")
    print(f"  sources:  {len(sources)} file(s)")
    for s in sources:
        print(f"            - {s.name}")
    print(f"  mined:    {len(unique)} unique (secret blocks skipped: {skipped_secret})")
    print(f"  emitted:  {len(capped)} (cap {args.max})")

    if args.dry_run:
        print()
        print(body)
    else:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(body, encoding="utf-8")
        print(f"  wrote:    {args.out}")

    after = fingerprint_brain()
    if before != after:
        print("ERROR: domain files or catalog.md changed during mine — aborting integrity check",
              file=sys.stderr)
        return 3
    print("  integrity: domain files + catalog.md unchanged")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
