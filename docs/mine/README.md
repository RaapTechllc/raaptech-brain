---
type: Reference
title: Mine Staging Contract
description: Ephemeral candidate staging between source miners and the knowledge Gate.
tags: [mine-pass, staging, contract]
timestamp: 2026-07-19T00:00:00Z
---

# Mine Staging

Miners may propose knowledge here, but they never edit durable domain files or
`catalog.md`. The Gate accepts, rejects, or parks each candidate before any
durable save.

## Files

| File | Purpose | Git |
|---|---|---|
| `candidates.md` | Regenerated candidate queue | ignored |
| `conflicts.md` | Parked disagreements requiring audit | ignored |
| `pass-log.md` | Mine-pass outcomes | ignored |
| `README.md` | This contract | tracked |

## Candidate contract

Each candidate records a claim, source path, short evidence excerpt, proposed
domain, miner identity, Gate decision, and Gate reason. Blocks matching
credential assignments, connection strings, provider-token formats, private
keys, or JWTs are conservatively rejected before staging. A candidate is not
trusted knowledge.

## Boundaries

1. Hermes mining reads only the configured `HERMES_HOME/memories` root.
2. Symlinks and archive or backup paths are excluded.
3. A pass emits at most 20 candidates.
4. Miner output is restricted to `docs/mine/candidates.md`.
5. Only the Gate may promote accepted knowledge through `brain save`.
6. Conflicts never overwrite existing knowledge automatically.
