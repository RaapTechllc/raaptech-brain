---
Status: ready-for-agent
Blocked by: 03
---

# Mine-pass skill (Hermes path)

## What to build

A brain-repo mine-pass skill runs Hermes Miner → Gate on demand and leaves staging ready for Hermes audit — without cron and without hosting the pipeline in OpenClaw MEMORY.

## Acceptance criteria

- [ ] Single on-demand entrypoint documents how to run the Hermes thin-proof pass
- [ ] Running it produces candidates + gate decisions + pass log in staging
- [ ] Skill does not schedule cron or touch vault yet
- [ ] Thin-proof dry run completes against live Hermes memories (or fixtures if offline)

## Blocked by

- 03 — Gate agent

## Comments
