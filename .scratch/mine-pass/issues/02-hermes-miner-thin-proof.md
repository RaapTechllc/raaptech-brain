---
Status: resolved
Blocked by: 01
---

# Hermes Miner (thin proof)

## What to build

An on-demand Hermes Miner reads only Hermes memories, emits at most ~20 candidate Insights into mine staging, and never writes brain domain files.

## Acceptance criteria

- [x] Miner allowlist is Hermes memories only for thin proof
- [x] Candidates land in staging in the shared contract shape (including proposed domain)
- [x] Secrets are never proposed as candidates
- [x] Archives/backups paths are not read
- [x] Domain files and catalogue are unchanged by the Miner alone

## Blocked by

- 01 — Mine staging scaffold

## Answer

Added `scripts/hermes_miner.py` (stdlib). Allowlists `%LOCALAPPDATA%/hermes/memories/*.md` only; refuses archive paths; secret-regex hard reject; writes `docs/mine/candidates.md` (≤20) in staging contract; fingerprints domain files + catalog.md before/after to prove no writes. Live thin-proof run: 13 candidates from MEMORY.md + USER.md.

## Comments
