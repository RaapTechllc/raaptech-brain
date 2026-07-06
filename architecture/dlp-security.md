---
type: Reference
title: DLP & Security
description: Data loss prevention patterns, kill switches, per-client DLP configuration.
resource: C:/Users/Kyle/RaapTech_OS/raaptech/dlp.py
tags: [architecture, security, dlp, kill-switch]
timestamp: 2026-07-06T16:30:00Z
---

# DLP & Security

**Source of truth:** [raaptech/dlp.py](C:/Users/Kyle/RaapTech_OS/raaptech/dlp.py), [config/dlp_patterns.yaml](C:/Users/Kyle/RaapTech_OS/config/dlp_patterns.yaml)

## Decisions

| ID | Decision | Status |
|---|---|---|
| G-SEC-01 | Audit mutating actions only | ✅ Implemented |
| G-SEC-02 | Standard patterns + configurable client-specific patterns | ✅ Implemented |
| G-SEC-03 | Independent kill switch per MCP server | ✅ Implemented |

## DLP Scanner

- `DLPScanner(client=...)` for per-client scanning
- Client-specific patterns in `config/clients/<client-key>/patterns.yaml`
- Standard patterns baked into `raaptech/dlp.py`

## Kill Switches

- Per MCP server kill switch in `config/mcp_servers.yaml`
- Global kill switch via `raaptech killswitch` CLI command
- Rot: 30 days (G-ROT-01)