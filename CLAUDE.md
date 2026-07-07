---
type: Reference
title: Claude Code Routing Note
description: How agents retrieve and save knowledge in this bundle — catalogue first, files second.
tags: [routing, brain, retrieval]
timestamp: 2026-07-07T12:00:00Z
---

# Routing note — read this before opening files

This bundle has a deterministic retrieval layer. Code before model:

1. **Check the catalogue first.** Answer questions with
   `python scripts/brain.py ask "your question"` (add `--json` for machine
   output). It scores `catalog.md` without opening files, then opens only the
   single winning section and prints an evidence block. Only open files by
   hand if `ask` reports no confident match — then start from the suggested
   domain `index.md`.
2. **Save durable facts with**
   `python scripts/brain.py save --domain <d> --title "..." "fact text"`.
   It writes the fact, the catalogue line, and the `log.md` entry in one
   atomic step. Valid domains: architecture, sessions, fleet, business,
   skills, integrations, research, references.
3. **Never hand-edit `catalog.md`.** It is generated. Rebuild with
   `python scripts/brain.py reindex`; regression-test retrieval with
   `python scripts/brain.py bench`.
