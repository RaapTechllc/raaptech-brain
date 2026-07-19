---
type: Reference
title: ADR 0001 Mine Pass Boundaries
description: Miners stage bounded candidates; only a Gate promotes durable knowledge.
tags: [mine-pass, adr, safety]
timestamp: 2026-07-19T00:00:00Z
---

# Mine Pass Boundaries

Operational source platforms contain useful facts mixed with stale material
and secrets. Bulk import would make the deterministic catalogue less reliable.

Miners therefore read one explicitly configured source root and write only an
ephemeral candidate queue. They never edit domain files or `catalog.md`. A Gate
must independently accept a candidate before `brain save` promotes it. Conflicts
are parked for audit and never overwrite existing knowledge automatically.

Rejected alternatives were unrestricted workstation crawling, automatically
trusting the newest source, and writing miner output directly into domains.
