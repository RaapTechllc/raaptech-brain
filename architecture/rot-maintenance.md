---
type: Reference
title: Rot & Maintenance
description: Rot rates, credential rotation schedule, config freshness policy.
resource: C:/Users/Kyle/RaapTech_OS/raaptech/rot.py
tags: [architecture, maintenance, rot, credentials]
timestamp: 2026-07-06T16:30:00Z
---

# Rot & Maintenance

**Source of truth:** [raaptech/rot.py](C:/Users/Kyle/RaapTech_OS/raaptech/rot.py) — G-ROT-01

## Rot Rates

Adopted from Mark Kashef's rot rates exactly (G-ROT-01):

| Asset | Rot Period |
|---|---|
| API keys | 30 days |
| OAuth tokens | Auto-refresh |
| Config files | 30 days |
| MCP server configs | 30 days |
| Client patterns | 90 days |

## Credential Rotation

- OAuth tokens auto-refresh via provider SDKs
- API keys require manual rotation (human-in-loop)
- `raaptech doctor` checks credential freshness

## Config Freshness

- Config files stamped with `timestamp` in frontmatter
- Stale config (>30 days) flagged by doctor
- Rot module enforces freshness at engine level