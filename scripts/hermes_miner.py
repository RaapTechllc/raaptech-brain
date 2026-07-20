#!/usr/bin/env python3
"""Emit bounded candidate Insights from the configured Hermes memory root.

The miner is deliberately read-only with respect to durable brain content. It
may write only ``docs/mine/candidates.md``; a later Gate decides what becomes
durable knowledge.
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

SECRET_PATTERNS = tuple(
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r'''(?<![A-Za-z0-9])["']?[A-Za-z0-9_-]*(api[_-]?key|secret(?:[_-]?key)?|token|client[_-]?secret|private[_-]?key|password|passwd|pwd|connection[_-]?string|database[_-]?url)["']?\s*[:=]\s*["']?\S+''',
        r"\b(postgres(?:ql)?|mysql|mongodb(?:\+srv)?|redis|amqps?)://[^\s:/]+:[^\s@]+@",
        r"\bBearer\s+[A-Za-z0-9\-._~+/]+=*",
        r"\bsk-[A-Za-z0-9]{10,}\b",
        r"\bsk-(?:proj|svcacct|admin|ant-api\d+|ant-admin\d+)-[A-Za-z0-9_-]{10,}\b",
        r"\b(?:xox[a-z]-|xapp-)[A-Za-z0-9-]{10,}\b",
        r"(?<!\d)\d{6,12}:[A-Za-z0-9_-]{30,}\b",
        r"\bxai-[A-Za-z0-9]{10,}\b",
        r"\bgh[pousr]_[A-Za-z0-9]{20,}\b",
        r"\bgithub_pat_[A-Za-z0-9_]{20,}\b",
        r"\bAIza[0-9A-Za-z_-]{20,}\b",
        r"-----BEGIN (RSA |OPENSSH |EC )?PRIVATE KEY-----",
        r"\bAKIA[0-9A-Z]{16}\b",
        r"\beyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b",
    )
)

DOMAIN_HINTS = (
    (re.compile(r"\b(ollama|model routing|quota|cron)\b", re.I), "architecture"),
    (re.compile(r"\b(truenas|proxmox|tailscale|fleet|vm\s*\d+|ssh|pve)\b", re.I), "fleet"),
    (re.compile(r"\b(trading|tradingview|smw|sheet metal|bluehost)\b", re.I), "business"),
    (re.compile(r"\b(morning brief|lab pulse|super brain|daily ops)\b", re.I), "business"),
    (re.compile(r"\b(hermes|oauth|auth\.json|mcp)\b", re.I), "integrations"),
    (re.compile(r"\b(delegation|subagent|swarm|agent)\b", re.I), "skills"),
)


@dataclass(frozen=True)
class Candidate:
    claim: str
    source_path: str
    evidence: str
    proposed_domain: str


def configure_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")


def configured_memories_root() -> Path:
    configured_home = os.environ.get("HERMES_HOME")
    if configured_home:
        hermes_home = Path(configured_home)
    else:
        local_app_data = os.environ.get("LOCALAPPDATA")
        hermes_home = (
            Path(local_app_data) / "hermes"
            if local_app_data
            else Path.home() / "AppData" / "Local" / "hermes"
        )
    return Path(os.path.abspath(hermes_home / "memories"))


def same_path(left: Path, right: Path) -> bool:
    return os.path.normcase(str(left.resolve())) == os.path.normcase(str(right.resolve()))


def path_has_symlink(path: Path) -> bool:
    current = Path(path.anchor)
    start = 1 if path.anchor else 0
    for part in path.parts[start:]:
        current /= part
        if current.is_symlink():
            return True
    return False


def candidate_limit(raw: str) -> int:
    try:
        value = int(raw)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("candidate limit must be an integer") from exc
    if not 1 <= value <= DEFAULT_MAX:
        raise argparse.ArgumentTypeError(f"candidate limit must be between 1 and {DEFAULT_MAX}")
    return value


def is_secret(text: str) -> bool:
    return any(pattern.search(text) for pattern in SECRET_PATTERNS)


def parse_blocks(text: str) -> list[str]:
    separator = "§" if "§" in text else None
    raw_blocks = text.split(separator) if separator else re.split(r"\n\s*\n", text)
    return [block.strip() for block in raw_blocks if len(block.strip()) >= 40]


def normalized_excerpt(text: str, limit: int) -> str:
    cleaned = re.sub(r"\s+", " ", text.strip())
    if len(cleaned) <= limit:
        return cleaned
    return cleaned[: limit - 3].rstrip() + "..."


def claim_from_block(block: str) -> str:
    cleaned = re.sub(r"\s+", " ", block.strip())
    first_sentence = re.split(r"(?<=[.!?])\s+", cleaned, maxsplit=1)[0]
    return normalized_excerpt(first_sentence, 220)


def propose_domain(text: str) -> str:
    scores = {domain: 0 for domain in DOMAINS}
    for pattern, domain in DOMAIN_HINTS:
        scores[domain] += len(pattern.findall(text))
    best = max(DOMAINS, key=lambda domain: scores[domain])
    return best if scores[best] else "references"


def allowlisted_sources(memories_root: Path) -> list[Path]:
    if path_has_symlink(memories_root):
        return []
    if not memories_root.is_dir():
        return []
    resolved_root = memories_root.resolve()
    path_parts = {
        part.lower() for part in (*memories_root.parts, *resolved_root.parts)
    }
    if any(
        "archive" in part
        or "backup" in part
        or part in {"_agent-md-backups", "openclaw-agents"}
        for part in path_parts
    ):
        return []

    sources: list[Path] = []
    for source in sorted(memories_root.glob("*.md")):
        if source.is_symlink():
            continue
        resolved = source.resolve()
        if resolved.parent != resolved_root or not resolved.is_file():
            continue
        lowered = source.name.lower()
        if any(token in lowered for token in ("backup", "archive", "pre-")):
            continue
        sources.append(resolved)
    return sources


def mine_source(path: Path) -> tuple[list[Candidate], int]:
    candidates: list[Candidate] = []
    secret_blocks = 0
    for block in parse_blocks(path.read_text(encoding="utf-8")):
        if is_secret(block):
            secret_blocks += 1
            continue
        candidates.append(
            Candidate(
                claim=claim_from_block(block),
                source_path=str(path),
                evidence=normalized_excerpt(block, 180),
                proposed_domain=propose_domain(block),
            )
        )
    return candidates, secret_blocks


def render_candidates(candidates: list[Candidate]) -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    lines = [
        "---",
        "type: Reference",
        "title: Mine Candidates Staging",
        "description: Ephemeral Hermes Miner candidate queue.",
        "tags: [mine-pass, staging, hermes-miner]",
        f"timestamp: {timestamp}",
        "---",
        "",
        "# Candidates",
        "",
        f"Generated at {timestamp}. Gate decisions are pending.",
        "",
    ]
    if not candidates:
        return "\n".join([*lines, "No candidates emitted.", ""])

    for index, candidate in enumerate(candidates, 1):
        lines.extend(
            [
                f"## C-{index:03d}",
                "",
                f"- **claim:** {candidate.claim}",
                f"- **source_path:** `{candidate.source_path}`",
                f"- **evidence:** {candidate.evidence}",
                f"- **proposed_domain:** {candidate.proposed_domain}",
                "- **miner:** hermes",
                "- **gate_decision:** pending",
                "- **gate_reason:**",
                "",
            ]
        )
    return "\n".join(lines)


def durable_brain_fingerprint() -> str:
    digest = hashlib.sha256()
    paths = [BUNDLE_ROOT / "catalog.md"]
    for domain in DOMAINS:
        paths.extend(sorted((BUNDLE_ROOT / domain).rglob("*.md")))
    for path in paths:
        digest.update(path.relative_to(BUNDLE_ROOT).as_posix().encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()


def atomic_write(path: Path, content: str) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary.write_text(content, encoding="utf-8")
    temporary.replace(path)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Emit candidate Insights from Hermes memories")
    parser.add_argument(
        "--memories",
        type=Path,
        help="Hermes memories path; must equal the configured HERMES_HOME memory root",
    )
    parser.add_argument("--max", type=candidate_limit, default=DEFAULT_MAX)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--out",
        type=Path,
        help="Output path; only docs/mine/candidates.md is permitted",
    )
    return parser


def main() -> int:
    configure_stdio()
    args = build_parser().parse_args()

    configured_root = configured_memories_root()
    requested_root = (args.memories or configured_root).resolve()
    if not same_path(requested_root, configured_root):
        print(
            f"Refusing source: expected configured Hermes memory root {configured_root}",
            file=sys.stderr,
        )
        return 2

    requested_output = (args.out or STAGING_CANDIDATES).resolve()
    if not same_path(requested_output, STAGING_CANDIDATES):
        print(f"Refusing output: output must be {STAGING_CANDIDATES}", file=sys.stderr)
        return 2

    sources = allowlisted_sources(configured_root)
    if not sources:
        print(f"No allowlisted .md files under {configured_root}", file=sys.stderr)
        return 1

    before = durable_brain_fingerprint()
    candidates: list[Candidate] = []
    secret_blocks = 0
    for source in sources:
        mined, secrets = mine_source(source)
        candidates.extend(mined)
        secret_blocks += secrets

    unique: list[Candidate] = []
    seen: set[str] = set()
    for candidate in candidates:
        key = candidate.claim.casefold()
        if key not in seen:
            seen.add(key)
            unique.append(candidate)
    emitted = unique[: args.max]
    rendered = render_candidates(emitted)

    print("Hermes Miner")
    print(f"  memories: {configured_root}")
    print(f"  sources:  {len(sources)} file(s)")
    print(f"  mined:    {len(unique)} unique (secret blocks skipped: {secret_blocks})")
    print(f"  emitted:  {len(emitted)} (cap {args.max})")

    if args.dry_run:
        print()
        print(rendered)
    else:
        atomic_write(STAGING_CANDIDATES, rendered)
        print(f"  wrote:    {STAGING_CANDIDATES}")

    if before != durable_brain_fingerprint():
        print("ERROR: durable brain content changed during mining", file=sys.stderr)
        return 3
    print("  integrity: durable brain content unchanged")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
