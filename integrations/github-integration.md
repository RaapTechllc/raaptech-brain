---
type: Reference
title: GitHub Integration
description: gh CLI auth status, repo map, PR workflow conventions.
tags: [integrations, github, git, pr]
timestamp: 2026-07-06T16:30:00Z
---

# GitHub Integration

**Auth:** `gh` CLI authenticated (verified 2026-07-06)

## RaapTech Repos

| Repo | URL | Role |
|---|---|---|
| **RaapTech_OS** | [github.com/RaapTechllc/RaapTech-OS](https://github.com/RaapTechllc/RaapTech-OS) | Core OS engine |
| **fable5** | [github.com/RaapTechllc/fable5](https://github.com/RaapTechllc/fable5) | Fable 5 operating repo |
| **raaptech-rde** | [github.com/RaapTechllc/raaptech-rde](https://github.com/RaapTechllc/raaptech-rde) | Research deliverable engine |
| **raaptech-brain** | [github.com/RaapTechllc/raaptech-brain](https://github.com/RaapTechllc/raaptech-brain) | Consolidated OKF knowledge bundle |

## PR Workflow

1. Branch: `feature/description` or `fix/description`
2. Commit: conventional commits (`feat:`, `fix:`, `docs:`, `chore:`)
3. Push: `git push -u origin <branch>`
4. PR: `gh pr create --base main --head <branch>`
5. Merge: squash merge, delete branch
6. Verify: `gh pr checks <N> --watch`

## Git Rules (from AGENTS.md)

- Every line of code MUST reach GitHub
- Commit after every phase, push immediately
- Never leave uncommitted work at end of session
- Verify push succeeded before declaring done