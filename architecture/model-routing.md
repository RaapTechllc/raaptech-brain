---
type: Reference
title: Model Routing
description: Which model serves which role in RaapTech OS — orchestrator, executor, fallback chain.
resource: C:/Users/Kyle/RaapTech_OS/config/models.yaml
tags: [architecture, models, routing, openrouter]
timestamp: 2026-07-06T16:30:00Z
---

# Model Routing

**Source of truth:** [config/models.yaml](C:/Users/Kyle/RaapTech_OS/config/models.yaml)

## Active Routing (Post PR #4)

| Role | Model | Provider | Notes |
|---|---|---|---|
| **Orchestrator** | GLM-5.2 | OpenRouter (:cloud) | Primary decision-making, multi-step reasoning |
| **Executor** | DeepSeek V4 Flash | OpenRouter | Fast implementation, parsing, code generation |
| **Local fallback** | Gemma 4 12B QAT | Ollama (local) | Offline/air-gapped operation only |
| **Research** | Nemotron 3 Ultra | Ollama Cloud (:cloud) | Deep research, synthesis, analysis |
| **Budget/High-volume** | Various | MoA preset | Aggregator + reference model combos |

## Key Rules

- **No Anthropic on crons or heartbeats.** Use DashScope or Ollama.
- **Every cron sets model explicitly.** Never default to primary.
- **Fallback chain must NOT include Anthropic.** Rate-limit → fall to Grok/Codex.
- **Kyle conserves Ollama Cloud quota.** All 6 ollama crons paused when low (2026-06-30).

## MoA Presets

| Preset | Aggregator | References | Use Case |
|---|---|---|---|
| BUDGET | DeepSeek V4 Pro | Gemma 4 31B, DeepSeek V4 Flash, Nemotron 3 Ultra | General tasks |
| GROK_5.5 | GLM-5.2 | 3 xAI refs | Not a real model — MoA preset |

## Cost Policy

See [Cost Policy](/architecture/cost-policy.md). Hard cap: $50/day. Audit scope: mutating actions only.