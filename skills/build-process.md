---
type: Reference
title: Build Process
description: The gated build process every feature request must pass through. Stack → Scope → Audience → Overlap → Handoff.
resource: C:/Users/Kyle/.openclaw/workspace/standards/BUILD-PROCESS.md
tags: [skills, build, process, gate, standards]
timestamp: 2026-07-07T12:00:00Z
---

# Build Process

## Gate (Every Build Request)

Every build request goes through 5 checks before writing code:

1. **Stack check** — Does the project already have a library/framework for this?
2. **Scope check** — Is this in scope for the current session/task?
3. **Audience check** — Who is this for? User, developer, admin?
4. **Overlap check** — Does something similar already exist?
5. **Handoff check** — Can this be delegated to a sub-agent safely?

## Rule: Standards Override Defaults

Check `standards/` FIRST. If a standard exists, follow it — don't invent alternatives.

## 8-Phase Build Loop (Autonomous Builds)

1. **Context** — Read task brief, understand requirements
2. **Plan** — Break into subtasks, identify dependencies
3. **Task** — Pick the next subtask
4. **Build** — Write the code/config
5. **Validate** — Run it, test it, check output
6. **Heal** — If broken, diagnose and fix (max 3 attempts)
7. **Retest** — Confirm the fix worked
8. **Close** — Commit, push, update memory, move to next task

## Definition of Done

Before marking ANY task complete:
1. Code compiles/runs without errors
2. You tested it yourself — visited the URL, ran the command, checked the output
3. If it's a web app: it's deployed and accessible, not just committed
4. Git: committed AND pushed
5. Documented in `memory/YYYY-MM-DD.md`

## Frontend Standards

- **Library discipline:** If a UI lib exists in the project, USE IT. Never build custom components when the lib provides them.
- **No dead elements:** Every UI element must have a calculated purpose
- **Anti-template:** Reject generic bootstrap layouts
- **Anti-AI-Slop:** See `standards/ANTI-SLOP.md`

## Fable 5 Build Rules

In the fable5 repo specifically:
- One Fable prompt = one measurable outcome
- Code changes belong in the target repo, not in fable5
- Every run passes PRE-FLIGHT check before paste
- Close the loop after: run summary in `runs/` + STATUS update
