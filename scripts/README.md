---
type: Reference
title: Scripts
description: Operational scripts for the brain repository — retrieval CLI, validation, and sync bridges.
tags: [scripts, retrieval, validation, sync, vault]
timestamp: 2026-07-07T12:00:00Z
---

# Scripts

All scripts run from the repo root with `python scripts/<script>.py`. Only
`sync-google-drive.py`, `okf-validate.py`, and `vault-bridge.py` need
third-party packages (see `requirements.txt` at repo root); `brain.py` and
`hermes_miner.py` are stdlib-only.

## brain.py

Deterministic retrieval CLI over the brain's markdown knowledge base.

```bash
python scripts/brain.py ask "what is the cost policy?"   # Retrieve answers
python scripts/brain.py save "note text"                 # Save new knowledge
python scripts/brain.py reindex                          # Rebuild the index
python scripts/brain.py bench                            # Run bench-questions.json benchmark
python scripts/brain.py html                             # Render HTML dashboard
```

Stdlib-only — no pip install required.

## okf-validate.py

Validates OKF bundle conformance: YAML frontmatter, required fields, and
bundle structure across all markdown files. Requires PyYAML.

```bash
python scripts/okf-validate.py
```

## sync-google-drive.py

Push/pull knowledge documents between the brain and a `raaptech-brain`
folder in Google Drive, using OAuth credentials at `~/.gemini/oauth_creds.json`.
Requires the Google API client libraries.

```bash
python scripts/sync-google-drive.py --status   # Check auth status
python scripts/sync-google-drive.py --list     # List files in Drive brain folder
python scripts/sync-google-drive.py --pull     # Download from Drive → brain
python scripts/sync-google-drive.py --push     # Upload brain → Drive
```

## vault-bridge.py

Bridge to the local RaapTech-Vault Obsidian workspace: verifies vault
accessibility, maps brain domains to vault PARA folders, and searches vault
notes. Override the vault location with the `VAULT_PATH` env var. Requires
PyYAML (frontmatter parsing).

```bash
python scripts/vault-bridge.py --status
python scripts/vault-bridge.py --search <keyword>
python scripts/vault-bridge.py --verify
python scripts/vault-bridge.py --report
```

## hermes_miner.py

Thin-proof Hermes Miner: reads only `%LOCALAPPDATA%/hermes/memories/*.md`,
emits ≤20 candidate Insights into `docs/mine/candidates.md`. Never writes
domain files or `catalog.md`. Secrets are hard-rejected.

```bash
python scripts/hermes_miner.py              # mine + write staging
python scripts/hermes_miner.py --dry-run    # print only
python scripts/hermes_miner.py --max 20     # candidate cap
```

Override memories root via `HERMES_HOME` or `--memories`.

## bench-questions.json

Benchmark question set consumed by `python scripts/brain.py bench` to score
retrieval quality.

## Conventions

- Run from repo root: `python scripts/<script>.py`
- Exit code 0 on success, non-zero on failure
- Print errors with file paths where applicable
