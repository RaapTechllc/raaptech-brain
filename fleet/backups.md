---
type: Reference
title: Backups & Disaster Recovery
description: Proxmox, TrueNAS, Docker VM backup strategy and schedules.
tags: [fleet, backups, disaster-recovery, proxmox, truenas]
timestamp: 2026-07-07T12:00:00Z
---

# Backups & Disaster Recovery

## Architecture

```
Proxmox PVE (10.0.0.20) -- PBS --> TrueNAS (10.0.0.30)
                                    |
                                    +-- VM snapshots
                                    +-- CT snapshots
                                    +-- Config backups
                                    +-- Critical data replication
```

## Backup Targets

| What | Where | Schedule | Retention |
|---|---|---|---|
| Proxmox VMs | TrueNAS PBS | Daily | 7 rolling + 4 weekly |
| Proxmox CTs | TrueNAS PBS | Daily | 7 rolling + 4 weekly |
| TrueNAS datasets | Offsite (future) | — | Not yet configured |
| Hermes config | `C:\Users\Kyle\AppData\Local\hermes\` | Git-tracked | — |
| Obsidian vault | Git-synced | On commit | Full history |
| Fable5 runs | `C:\Users\Kyle\CC\fable5\runs\` | Git-tracked | — |

## Key VMs Backed Up

| VMID | Name | Role | Backup Priority |
|---|---|---|---|
| 201 | ollama-gpu | LLM inference (RTX 3080) | High |
| 111 | atlas-hermes | Atlas agent (Hermes + OpenClaw) | High |
| All | Other fleet VMs | Various agents | Medium |

## Recovery Order

1. Proxmox hypervisor
2. TrueNAS (restore access)
3. Tailscale (restore connectivity)
4. ollama-gpu CT (restore LLM capability)
5. atlas-hermes VM (restore primary agent)
6. Other VMs as needed

## Notes

- TrueNAS at `100.72.235.14` (Tailscale) — SSH key: `truenas_admin` + key `truenas_maxx`
- No offsite backup currently configured — single point of failure risk
- PBS (Proxmox Backup Server) integration with TrueNAS pending
