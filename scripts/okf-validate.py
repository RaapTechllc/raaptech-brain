#!/usr/bin/env python3
"""OKF v0.1 conformance validator for raaptech-brain.

Checks:
1. Every non-reserved .md file has parseable YAML frontmatter.
2. Every frontmatter block contains a non-empty `type` field.
3. index.md and log.md follow reserved-filename conventions.
4. Cross-links are checked for existence (warn only — broken links are OK per spec).

Usage: python scripts/okf-validate.py [--strict]
"""

import sys
import yaml
from pathlib import Path

RESERVED = {"index.md", "log.md"}
BUNDLE_ROOT = Path(__file__).resolve().parent.parent


def parse_frontmatter(path: Path) -> dict | None:
    """Extract YAML frontmatter from a markdown file. Returns None if missing/malformed."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None
    try:
        return yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        return None


def validate_bundle(strict: bool = False) -> tuple[list[str], list[str], list[str]]:
    """Validate the bundle. Returns (errors, warnings, info)."""
    errors: list[str] = []
    warnings: list[str] = []
    info: list[str] = []

    md_files = sorted(BUNDLE_ROOT.rglob("*.md"))
    concept_files = [f for f in md_files if f.name not in RESERVED]
    index_files = [f for f in md_files if f.name == "index.md"]
    log_files = [f for f in md_files if f.name == "log.md"]

    info.append(f"Found {len(md_files)} .md files ({len(concept_files)} concepts, {len(index_files)} indexes, {len(log_files)} logs)")

    # Check 1: Every concept has parseable frontmatter with non-empty type
    for f in concept_files:
        fm = parse_frontmatter(f)
        if fm is None:
            errors.append(f"  MISSING FRONTMATTER: {f.relative_to(BUNDLE_ROOT)}")
            continue
        if not fm.get("type"):
            errors.append(f"  MISSING TYPE: {f.relative_to(BUNDLE_ROOT)}")
        else:
            info.append(f"  OK: {f.relative_to(BUNDLE_ROOT)} (type={fm['type']})")

    # Check 2: index.md files should NOT have frontmatter (per spec §6)
    for f in index_files:
        fm = parse_frontmatter(f)
        if fm is not None:
            warnings.append(f"  INDEX HAS FRONTMATTER: {f.relative_to(BUNDLE_ROOT)} — spec §6 says index.md has no frontmatter (except bundle-root for okf_version)")

    # Check 3: log.md should follow date-grouped structure
    for f in log_files:
        text = f.read_text(encoding="utf-8")
        if "## 20" not in text:
            warnings.append(f"  LOG MISSING DATE HEADINGS: {f.relative_to(BUNDLE_ROOT)} — spec §7 recommends YYYY-MM-DD headings")

    # Check 4: Cross-links (warn only — spec says consumers MUST tolerate broken links)
    if strict:
        all_paths = {f.relative_to(BUNDLE_ROOT).as_posix() for f in md_files}
        for f in concept_files:
            text = f.read_text(encoding="utf-8")
            for line in text.splitlines():
                if "](" in line and ".md)" in line:
                    # Extract markdown links
                    import re
                    for match in re.finditer(r"\]\(([^)]+\.md)\)", line):
                        target = match.group(1)
                        if target.startswith("/"):
                            target = target.lstrip("/")
                        if target not in all_paths and not target.startswith("http"):
                            warnings.append(f"  BROKEN LINK in {f.relative_to(BUNDLE_ROOT)}: -> {target}")

    return errors, warnings, info


def main():
    strict = "--strict" in sys.argv
    errors, warnings, info = validate_bundle(strict=strict)

    print("=" * 60)
    print("OKF v0.1 Conformance Check")
    print("=" * 60)

    for line in info:
        print(line)

    if warnings:
        print(f"\n⚠ Warnings ({len(warnings)}):")
        for w in warnings:
            print(w)

    if errors:
        print(f"\n❌ Errors ({len(errors)}):")
        for e in errors:
            print(e)
        print(f"\nBundle is NOT conformant. Fix {len(errors)} error(s).")
        sys.exit(1)
    else:
        print(f"\n✅ Bundle is OKF v0.1 conformant ({len(concept_files := [f for f in BUNDLE_ROOT.rglob('*.md') if f.name not in RESERVED])} concepts, 0 errors)")
        if warnings:
            print(f"   ({len(warnings)} non-blocking warnings)")

    # Summary
    dirs_with_index = {f.parent for f in BUNDLE_ROOT.rglob("index.md")}
    dirs_with_md = {f.parent for f in BUNDLE_ROOT.rglob("*.md") if f.name not in RESERVED}
    missing_index = dirs_with_md - dirs_with_index
    if missing_index:
        print(f"\n📁 Directories missing index.md ({len(missing_index)}):")
        for d in sorted(missing_index):
            print(f"   {d.relative_to(BUNDLE_ROOT)}/")


if __name__ == "__main__":
    main()