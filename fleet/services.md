---
type: Reference
title: Fleet Services
description: What runs where across the RaapTech fleet — Ollama, OpenClaw, Hermes, n8n, Postgres, TradingView.
tags: [fleet, services, ollama, openclaw, hermes]
timestamp: 2026-07-06T16:30:00Z
---

# Fleet Services

## Core Services

| Service | Node | Port | Notes |
|---|---|---|---|
| **Ollama (GPU)** | CT 201 (192.168.1.175) | 11434 | RTX 3080 passthrough; `:cloud` tags for remote models |
| **Ollama (local)** | Maxx (Windows) | 11434 | Gemma 4 12B QAT fallback |
| **OpenClaw Gateway** | Falcon (100.125.198.20) | 18789 | SSH blocked as of 2026-06-30 |
| **Hermes TUI** | Maxx (Windows) | — | Primary interaction surface |
| **n8n** | Maxx (Windows) | 5678 | Workflow automation |
| **TradingView MCP** | Maxx (Windows) | CDP 9222 | Jackson bridge, Lorentzian indicators |

## Daily Ops Stack

| Tool | Path | Purpose |
|---|---|---|
| **Lab Pulse** | `~/projects/lab-pulse/run-pulse.bat` | 7 DVM services + 7 TS hosts health check |
| **Morning Brief** | `~/projects/morning-ops-brief/run-brief.bat` | Pulse + vault → HTML report |
| **Super Brain** | `~/projects/super-brain-dashboard/run-brain.bat` | YouTube RSS + vault prompts + daily master prompt |

## Model Serving

| Provider | Location | Models |
|---|---|---|
| **Ollama Cloud** | CT 201 | GLM-5.2, Nemotron 3 Ultra, DeepSeek V4 Flash |
| **Ollama Local** | Maxx | Gemma 4 12B QAT |
| **OpenRouter** | API | Multi-provider fallback |
| **DashScope** | API | Qwen3.5-plus (cron/heartbeat) |
| **OpenAI Codex** | OAuth | GPT-5.5 (orchestrator) |

## Storage

| System | IP | Role |
|---|---|---|
| **TrueNAS** | Tailscale | Backups, media, ISO storage |
| **SMW Cloud** | 50.87.233.33 | Bluehost cPanel, client hosting |