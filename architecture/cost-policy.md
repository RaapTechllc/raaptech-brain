---
type: Reference
title: Cost Policy
description: RaapTech OS cost policy — $50/day hard cap, per-model pricing, audit scope.
resource: C:/Users/Kyle/RaapTech_OS/raaptech/cost.py
tags: [architecture, cost, budget, audit]
timestamp: 2026-07-06T16:30:00Z
---

# Cost Policy

**Source of truth:** [raaptech/cost.py](C:/Users/Kyle/RaapTech_OS/raaptech/cost.py) — G-ARCH-10

## Hard Cap

- **$50/day** across all providers
- Enforced at the engine level (not advisory)
- Kill switch triggers when cap is reached

## Per-Model Pricing

See [Model Routing](/architecture/model-routing.md) for which model serves which role. Pricing is tracked per-call via OpenRouter API.

## Audit Scope

- **Mutating actions only** (G-SEC-01)
- Reads are not logged unless elevated
- JSONL write + SQLite query for audit logs (G-ARCH-09)

## Quota Conservation

- All 6 Ollama crons paused as of 2026-06-30 (quota low)
- Restore when Ollama Cloud quota replenishes
- No Anthropic models on crons or heartbeats