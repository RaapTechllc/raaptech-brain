---
type: Reference
title: Tailscale Network Map
description: All Tailscale IPs, hostnames, roles, and connectivity notes.
tags: [fleet, tailscale, network, ips, topology]
timestamp: 2026-07-07T12:00:00Z
---

# Tailscale Network Map

**Rule:** ALL lab access via Tailscale ONLY. Never use LAN IPs (10.0.0.x).

## IP Map

| IP | Hostname | Role | Connection |
|---|---|---|---|
| 100.97.87.28 | Docker VM | Container runtime | SSH |
| 100.72.235.14 | TrueNAS | NAS / backups | SSH (key: truenas_maxx) |
| 100.108.110.114 | Maxx workstation | Primary Hermes desktop | Local/RDP |
| 100.79.152.38 | Maxx (cmd) | Fleet cmd endpoint | SSH |
| 100.88.61.120 | Atlas worker | Head of R&D (Hermes + OpenClaw) | SSH (cbi) |
| 100.125.198.20 | Falcon API | OpenClaw 18789 | HTTP (SSH blocked) |
| 100.123.255.56 | Mac mobile | Axel content/intel | SSH (timraap) |
| 100.79.231.98 | Damien | CTO (execution) | SSH |
| 100.96.218.109 | Remi | Head of Growth | SSH |
| 100.102.207.14 | TopG | CRO (risk/security) | SSH |

## Connectivity Rules

- If Tailscale is down → fix Tailscale, don't work around with LAN IPs
- Ethernet unplugged on Maxx workstation — always wireless via TS
- Fleet agents: use Tailscale IPs from this table
- TrueNAS: `truenas_admin` user + key `truenas_maxx`, pw auth rejected
- SMW Cloud: not on Tailscale — Bluehost cPanel at `50.87.233.33` (pw-only SSH)

## Fleet Agent ↔ Tailscale

| Agent | IP | Model | Provider |
|---|---|---|---|
| Damien (CTO) | 100.79.231.98 | qwen3.5:397b | Ollama Pro |
| Atlas (R&D) | 100.88.61.120 | qwen3.5-plus | DashScope |
| Remi (Growth) | 100.96.218.109 | gpt-5.4 | OpenAI |
| TopG (Risk) | 100.102.207.14 | glm-5.1 | Ollama Pro |
| Axel (Content) | 100.123.255.56 | minimax-m2.7 | Ollama Pro |

## Network Diagram

```
Maxx Workstation (100.108.110.114)
    |
    +-- Hermes GUI (primary agent brain)
    +-- OpenClaw MC gateway (A2A)
    |
    +-[Tailscale Mesh]--+
    |                    |
    Docker VM (100.97.87.28)     TrueNAS (100.72.235.14)
    Proxmox PVE (LAN only)       
    Fleet VMs (100.79.x, 100.88.x, 100.96.x, 100.102.x, 100.125.x)
    Mac mobile (100.123.255.56)
```
