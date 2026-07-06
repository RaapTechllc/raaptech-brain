---
type: Reference
title: MCP Servers
description: Connected MCP servers — transport, audit scope, kill switches.
resource: C:/Users/Kyle/RaapTech_OS/config/mcp_servers.yaml
tags: [architecture, mcp, servers, integration]
timestamp: 2026-07-06T16:30:00Z
---

# MCP Servers

**Source of truth:** [config/mcp_servers.yaml](C:/Users/Kyle/RaapTech_OS/config/mcp_servers.yaml)

## Defaults

| Setting | Value |
|---|---|
| Transport | stdio |
| Timeout | 30s |
| Audit scope | mutating_actions only |

## Connected Servers

| Server | Status | Notes |
|---|---|---|
| TradingView MCP Jackson | Active | CDP 9222, Lorentzian indicators |
| GitHub | Active | gh CLI auth |
| File system | Active | Local FS access |

## Rules

- Each server has independent kill switch (G-SEC-03)
- Servers marked `enabled: false` are stubs awaiting real infra/secrets
- Rot: 30 days