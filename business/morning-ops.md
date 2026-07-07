---
type: Reference
title: Morning Operations
description: Daily ops stack — Lab Pulse, Morning Brief, Super Brain dashboard.
resource: C:/Users/Kyle/projects/lab-pulse/run-pulse.bat
tags: [business, operations, morning, daily]
timestamp: 2026-07-06T16:30:00Z
---

# Morning Operations

**Source of truth:** `~/projects/lab-pulse/`, `~/projects/morning-ops-brief/`, `~/projects/super-brain-dashboard/`

## Daily Stack (Run Order)

### 1. Lab Pulse
**Command:** `~/projects/lab-pulse/run-pulse.bat`
**Scope:** 7 DVM services + 7 TS hosts
**Output:** Health status for all fleet nodes and services

### 2. Morning Brief
**Command:** `~/projects/morning-ops-brief/run-brief.bat`
**Scope:** Pulse results + Obsidian vault
**Output:** HTML report with fleet health + daily context

### 3. Super Brain
**Command:** `~/projects/super-brain-dashboard/run-brain.bat`
**Scope:** YouTube RSS feeds + vault prompts + daily master prompt
**Output:** Consolidated daily intelligence brief

## Integration Points

- All three tools feed into the Obsidian vault at `C:\Users\Kyle\.openclaw\workspace\RaapTech-Vault` (see [Obsidian Vault Bridge](/references/obsidian-vault.md))
- Morning Brief HTML is the primary human-facing dashboard
- Super Brain generates the daily master prompt for Hermes/Fable sessions

## Cron Status

All 6 Ollama crons paused as of 2026-06-30 (quota conservation). Restore when Ollama Cloud quota replenishes.