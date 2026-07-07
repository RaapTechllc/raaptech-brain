---
type: Reference
title: Monitoring & Health Checks
description: How each service is monitored — crons, heartbeats, alerts, dashboards.
tags: [fleet, monitoring, health, crons, heartbeats]
timestamp: 2026-07-07T12:00:00Z
---

# Monitoring & Health Checks

## Dashboard: Lab Pulse

**Primary:** `~/projects/lab-pulse/run-pulse.bat` — checks 7 DVM services + 7 TS hosts.
**Part of:** Morning Brief (`~/projects/morning-ops-brief/run-brief.bat`).

## Hermes Cron Monitoring

| Cron | Purpose | Model | Schedule |
|---|---|---|---|
| Fleet hourly check | Agent heartbeat, disk/memory alerts | dashscope/qwen3.5-plus | Every hour |
| Morning brief | Lab pulse + Obsidian vault → HTML | Current main | Daily 9am |
| Super brain | YouTube RSS + vault prompts | Current main | Daily |

**Rule:** Every cron MUST set `--model` explicitly. No Anthropic on crons. DashScope/Ollama only.

## Health Check Matrix

| Service | Check Method | Alert if Missing |
|---|---|---|
| Hermes GUI | Process running | — |
| OpenClaw MC gateway | `mc-gateway-*` process | Fleet agent unreachable |
| Tailscale | `tailscale status` | All fleet agents unreachable |
| ollama-gpu CT | `curl :11434/api/tags` | LLM inference down |
| Each fleet agent | Heartbeat via cron | Agent not responding |
| TrueNAS | SSH reachability | Backups at risk |
| SMW Cloud (Bluehost) | HTTPS check | Client site at risk |

## Proxmox Monitoring

- Web UI: `https://10.0.0.20:8006` (LAN) or via Tailscale
- Key metric: GPU availability (RTX 3080 passthrough to CT 201)
- Key metric: Disk usage on VMs/CTs

## Alert Flow

```
Health check failure → Hermes cron detects → Telegram alert to Kyle
                                          → Logged to ~/projects/lab-pulse/
```

## Daily Ops Stack

1. `run-pulse.bat` — Lab Pulse (service check)
2. `run-brief.bat` — Morning Brief (pulse + vault → HTML dashboard)
3. `run-brain.bat` — Super Brain (YouTube RSS + vault + daily master prompt)

All at `~/projects/`.
