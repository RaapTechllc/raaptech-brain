---
type: Reference
title: Messaging Gateways
description: Hermes messaging platform integrations — Telegram, Discord, Signal, WhatsApp, and routing rules.
tags: [integrations, messaging, gateways, telegram, discord]
timestamp: 2026-07-07T12:00:00Z
---

# Messaging Gateways

## Overview

Hermes connects to messaging platforms via the gateway system. Each platform is a separate channel with its own routing, delivery rules, and thread support.

## Active Platforms

| Platform | Purpose | Delivery Target |
|---|---|---|
| Telegram | Primary human-in-loop channel | `telegram:<chat_id>[:<thread_id>]` |
| Discord | Developer/community channels | `discord:#channel` |
| Signal | Private/encrypted comms | `signal:+<phone>` |
| WhatsApp | Client comms | Direct via gateway |

## Cron Delivery

Cron jobs run with no user present. Output must be delivered to a platform:

| Delivery Value | Behavior |
|---|---|
| `origin` / omitted | Back to the chat that created the job |
| `local` | No delivery — saved only (viewable via `cronjob action=list`) |
| `all` | Fan out to every connected home channel |
| `telegram:<chat_id>:<thread_id>` | Specific Telegram topic |
| `discord:#channel` | Specific Discord channel |

**TUI sessions:** Cron output is LOCAL-ONLY from the TUI. Use `deliver='telegram'` or other platform for real notification.

## Gateway Troubleshooting

See [messaging-gateway-troubleshooting](/skills/messaging-gateway-troubleshooting) for common issues:
- Platform auth failures
- Message delivery not arriving
- Thread/topic routing errors
- Gateway process crashes
