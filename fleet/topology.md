---
type: Reference
title: Fleet Topology
description: All RaapTech fleet nodes — hardware, roles, Tailscale IPs, status.
resource: C:/Users/Kyle/.openclaw/workspace/AGENTS.md
tags: [fleet, topology, proxmox, nodes]
timestamp: 2026-07-06T16:30:00Z
---

# Fleet Topology

**Source of truth:** Hermes memory + [AGENTS.md](C:/Users/Kyle/.openclaw/workspace/AGENTS.md) agent roster.

## Command Node

| Node | Hostname | OS | Hardware | Role |
|---|---|---|---|---|
| **Maxx** | Windows 10 | Win 10 | RTX 3080 10GB | Primary command node, Proxmox host, Hermes TUI |

## Proxmox Host

| Detail | Value |
|---|---|
| **Version** | PVE 9.2.3 |
| **Kernel** | 7.0.12-1-pve |
| **GPU** | RTX 3080 10GB (driver 610.43.02, NVIDIA debian13 CUDA repo) |

## Fleet Agents (Proxmox VMs)

| Agent | Role | Tailscale IP | Model | Status (2026-06-30) |
|---|---|---|---|---|
| **Maxx** (cmd) | COO / Orchestrator | 100.79.152.38 | GPT-5.5 (Codex) | Active |
| **Atlas** (worker) | Head of R&D | 100.88.61.120 | Qwen3.5-plus (DashScope) | Active, SSH `cbi` |
| **Falcon** (API) | API Gateway | 100.125.198.20 | — | OpenClaw 18789, SSH blocked |
| **Mac mobile** | Content & Intel | 100.123.255.56 | MiniMax M2.7 | SSH `timraap` |

## Containers

| CT | Name | IP | Service |
|---|---|---|---|
| 201 | ollama-gpu | 192.168.1.175 | Ollama with GPU passthrough |

## Key Rules

- **ALL lab access via Tailscale ONLY.** Ethernet unplugged on Maxx workstation.
- **Never use LAN IPs (10.0.0.x)** for SSH, API calls, or service access.
- **TrueNAS SSH:** `truenas_admin` + key `truenas_maxx`; password auth rejected.
- **SMW Cloud:** Bluehost cPanel `50.87.233.33` (pw-only SSH).

## PVE 8 Fixes (Historical)

- nvidia-uvm major 234→511
- OLLAMA_VULKAN=true blocks CUDA