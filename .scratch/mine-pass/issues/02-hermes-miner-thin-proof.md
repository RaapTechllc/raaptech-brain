---
Status: ready-for-agent
Blocked by: 01
---

# Hermes Miner (thin proof)

## What to build

An on-demand Hermes Miner reads only Hermes memories, emits at most ~20 candidate Insights into mine staging, and never writes brain domain files.

## Acceptance criteria

- [ ] Miner allowlist is Hermes memories only for thin proof
- [ ] Candidates land in staging in the shared contract shape (including proposed domain)
- [ ] Secrets are never proposed as candidates
- [ ] Archives/backups paths are not read
- [ ] Domain files and catalogue are unchanged by the Miner alone

## Blocked by

- 01 — Mine staging scaffold

## Comments
