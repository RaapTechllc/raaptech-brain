#!/usr/bin/env python3
"""Bridge raaptech-brain to the local RaapTech-Vault Obsidian workspace.

Verifies vault accessibility, maps brain domains to vault PARA folders,
and supports topic search for cross-checking knowledge.

Usage:
    python scripts/vault-bridge.py --status
    python scripts/vault-bridge.py --search <keyword>
    python scripts/vault-bridge.py --verify
    python scripts/vault-bridge.py --report
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

BUNDLE_ROOT = Path(__file__).resolve().parent.parent

# Override with VAULT_PATH env var if needed
DEFAULT_VAULT = Path.home() / ".openclaw" / "workspace" / "RaapTech-Vault"

DOMAIN_MAP: dict[str, list[str]] = {
    "architecture": [
        "20-Areas/Infrastructure",
        "30-Resources/Tech-Reference",
    ],
    "fleet": [
        "20-Areas/Fleet-Ops",
        "60-Fleet",
    ],
    "business": [
        "20-Areas/Business",
        "20-Areas/Trading",
    ],
    "integrations": [
        "20-Areas/Integrations",
    ],
    "skills": [
        "30-Resources/Brains",
        "30-Resources/Dynamous",
    ],
    "sessions": [
        "50-Daily",
    ],
    "research": [
        "30-Resources/Market-Intel",
        "00-Inbox",
    ],
    "references": [
        "30-Resources/Tech-Reference",
        "40-Archive",
    ],
}


@dataclass
class VaultStatus:
    path: Path
    exists: bool
    is_obsidian: bool
    markdown_count: int
    git_remote: str | None


def resolve_vault() -> Path:
    import os

    return Path(os.environ.get("VAULT_PATH", DEFAULT_VAULT)).expanduser()


def count_markdown(root: Path) -> int:
    if not root.exists():
        return 0
    return sum(1 for _ in root.rglob("*.md") if ".git" not in _.parts)


def get_git_remote(vault: Path) -> str | None:
    git_config = vault / ".git" / "config"
    if not git_config.exists():
        return None
    text = git_config.read_text(encoding="utf-8")
    match = re.search(r'url\s*=\s*(.+)', text)
    return match.group(1).strip() if match else None


def vault_status(vault: Path) -> VaultStatus:
    return VaultStatus(
        path=vault,
        exists=vault.exists(),
        is_obsidian=(vault / ".obsidian").exists(),
        markdown_count=count_markdown(vault),
        git_remote=get_git_remote(vault),
    )


def brain_concepts() -> list[Path]:
    reserved = {"index.md", "log.md", "README.md"}
    return sorted(
        f for f in BUNDLE_ROOT.rglob("*.md")
        if f.name not in reserved and f.relative_to(BUNDLE_ROOT).parts[0] != ".git"
    )


def parse_title(path: Path) -> str | None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return path.stem.replace("-", " ")
    parts = text.split("---", 2)
    if len(parts) < 3:
        return path.stem.replace("-", " ")
    import yaml

    try:
        fm = yaml.safe_load(parts[1]) or {}
    except Exception:
        return path.stem.replace("-", " ")
    return fm.get("title") or path.stem.replace("-", " ")


def search_vault(vault: Path, keyword: str) -> list[Path]:
    keyword_lower = keyword.lower()
    results: list[Path] = []
    for md in vault.rglob("*.md"):
        if ".git" in md.parts:
            continue
        rel = str(md.relative_to(vault)).lower()
        if keyword_lower in rel:
            results.append(md)
            continue
        try:
            if keyword_lower in md.read_text(encoding="utf-8").lower():
                results.append(md)
        except OSError:
            continue
    return sorted(results)


def verify_domains(vault: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    info: list[str] = []
    for domain, folders in DOMAIN_MAP.items():
        for folder in folders:
            full = vault / folder
            if full.exists():
                count = count_markdown(full)
                info.append(f"  OK  {domain:14} -> {folder} ({count} notes)")
            else:
                errors.append(f"  MISSING  {domain:14} -> {folder}")
    return errors, info


def verify_cross_refs(vault: Path) -> list[str]:
    """Warn when brain concept keywords have no obvious vault counterpart."""
    warnings: list[str] = []
    vault_names = {
        md.stem.lower().replace("-", " ")
        for md in vault.rglob("*.md")
        if ".git" not in md.parts
    }
    for concept in brain_concepts():
        title = (parse_title(concept) or "").lower()
        if not title or len(title) < 6:
            continue
        # Skip generic titles
        if title in {"raaptech brain readme"}:
            continue
        tokens = [t for t in re.split(r"[\s/&]+", title) if len(t) > 4]
        if not tokens:
            continue
        primary = tokens[0]
        if not any(primary in name for name in vault_names):
            rel = concept.relative_to(BUNDLE_ROOT)
            warnings.append(f"  NO VAULT MATCH  {rel} (searched: '{primary}')")
    return warnings


def cmd_status(vault: Path) -> int:
    status = vault_status(vault)
    print("RaapTech Vault Bridge — Status")
    print("=" * 40)
    print(f"Vault path:     {status.path}")
    print(f"Exists:         {'yes' if status.exists else 'NO'}")
    print(f"Obsidian vault: {'yes' if status.is_obsidian else 'no'}")
    print(f"Markdown notes: {status.markdown_count}")
    print(f"Git remote:     {status.git_remote or '(none)'}")
    print(f"Brain root:     {BUNDLE_ROOT}")
    if not status.exists:
        print("\nSet VAULT_PATH or open vault at default path.")
        return 1
    return 0


def cmd_search(vault: Path, keyword: str) -> int:
    if not vault.exists():
        print(f"Vault not found: {vault}")
        return 1
    hits = search_vault(vault, keyword)
    print(f"Search '{keyword}' in {vault}")
    print("=" * 40)
    if not hits:
        print("No matches.")
        return 0
    for md in hits[:50]:
        print(f"  {md.relative_to(vault)}")
    if len(hits) > 50:
        print(f"  ... and {len(hits) - 50} more")
    return 0


def cmd_verify(vault: Path) -> int:
    if not vault.exists():
        print(f"Vault not found: {vault}")
        return 1
    errors, info = verify_domains(vault)
    warnings = verify_cross_refs(vault)
    print("Domain mapping")
    print("=" * 40)
    for line in info:
        print(line)
    for line in errors:
        print(line)
    if warnings:
        print("\nBrain concepts without obvious vault notes (informational)")
        print("=" * 40)
        for line in warnings[:20]:
            print(line)
        if len(warnings) > 20:
            print(f"  ... and {len(warnings) - 20} more")
    return 1 if errors else 0


def cmd_report(vault: Path) -> int:
    rc = cmd_status(vault)
    print()
    cmd_verify(vault)
    return rc


def main() -> int:
    parser = argparse.ArgumentParser(description="Bridge raaptech-brain to RaapTech-Vault")
    parser.add_argument("--status", action="store_true", help="Show vault accessibility")
    parser.add_argument("--search", metavar="KEYWORD", help="Search vault notes by keyword")
    parser.add_argument("--verify", action="store_true", help="Verify domain mapping and cross-refs")
    parser.add_argument("--report", action="store_true", help="Full status + verify report")
    args = parser.parse_args()

    vault = resolve_vault()

    if args.report:
        return cmd_report(vault)
    if args.status:
        return cmd_status(vault)
    if args.search:
        return cmd_search(vault, args.search)
    if args.verify:
        return cmd_verify(vault)

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
