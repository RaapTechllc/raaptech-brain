---
Status: ready-for-agent
Blocked by: 04
---

# Hermes audit handoff

## What to build

A Hermes-side audit step consumes parked Conflicts, validates against live sources, writes only Conflict resolutions (via `brain save` when correcting), and closes the pass log — without becoming a general writer for routine accepts.

## Acceptance criteria

- [ ] Audit prompt/runbook exists and points at staging Conflicts
- [ ] Audit may write Conflict resolutions only
- [ ] Routine accepts remain Gate-owned
- [ ] Pass log records audit outcomes (confirm / correct / leave parked)
- [ ] Brain bench still passes after a resolution write

## Blocked by

- 04 — Mine-pass skill (Hermes path)

## Comments
