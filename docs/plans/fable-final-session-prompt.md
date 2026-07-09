---
type: Reference
title: Fable 5 Final Session Starter Prompt
description: Ready-to-paste marching orders for the last Fable 5 planning session — review gaps, produce execution plan for Cursor.
tags: [fable5, prompt, sessions, brain, planning]
timestamp: 2026-07-07T14:30:00Z
---

# Fable 5 Final Session — Starter Prompt

Copy **everything inside the fenced block below** into Fable as the session description / starter prompt. Cursor executes the plan Fable produces.

---

```
You are running the FINAL Fable 5 session for RaapTech LLC before description/quota usage expires. This session is PLANNING ONLY — your deliverable is a concrete, ordered execution plan that Cursor will implement immediately after. Do not implement code yourself unless a 2-minute verification command is needed to confirm baseline.

## Repo

C:\Users\Kyle\CC\raaptech-brain

RaapTech Brain — OKF v0.1 markdown knowledge bundle. Deterministic retrieval via scripts/brain.py. Never hand-edit catalog.md.

## Verified baseline (confirm first)

Run from repo root:

  python scripts/okf-validate.py
  python scripts/brain.py bench
  python scripts/vault-bridge.py --report

Expected: OKF PASS (48 md files, 35 concepts, 0 errors), bench 10/10, vault 106 notes mapping OK.

Known failure:

  python scripts/sync-google-drive.py --status
  → UnicodeEncodeError on Windows cp1252 (emoji in print at line 149). Display bug only; fix pattern exists in okf-validate.py (stdout.reconfigure utf-8).

## Routing rules for this repo

1. python scripts/brain.py ask "question" — catalogue first, one evidence block
2. python scripts/brain.py save --domain <d> --title "..." "fact" — atomic write (domains: architecture, sessions, fleet, business, skills, integrations, research, references)
3. python scripts/brain.py reindex — rebuild catalog.md
4. Never hand-edit catalog.md

Read before planning:
- docs/plans/next-steps-plan.md (draft gap analysis — critique it)
- docs/superpowers/specs/2026-07-07-second-brain-retrieval-design.md
- sessions/sprint-tracker.md, sessions/run-ledger.md, sessions/session-catalog.md
- CLAUDE.md, index.md, log.md
- references/obsidian-vault.md

Vault (cross-context, read-only): C:\Users\Kyle\.openclaw\workspace\RaapTech-Vault (106 notes, GitHub RaapTechllc/raaptech-vault)

## Your mission

1. REVIEW the repo and the draft gap list in docs/plans/next-steps-plan.md.
2. CRITICALLY ASSESS what is missing, weak, stale, or misrouted. Find gaps WE MISSED — do not treat the draft list as complete.
3. PRODUCE a concrete, ordered EXECUTION PLAN for Cursor with checkable steps.

## Starting hypotheses (validate or overturn)

P0:
- sync-google-drive.py Windows encoding crash blocks --status
- sessions/sprint-tracker.md stale (still Session 13/14; brain 2026-07-07 retrieval work not reflected; bench Q9 expects "Session 13")
- No catalogued "brain final improvement" Fable session while quota expires

P1:
- research/ has only 1 concept; fable5/research/ and vault Market-Intel under-synthesized
- references/memories.md missing from references/index.md
- Root index.md promises business "onboarding" — no concept file
- docs/plans/ and docs/superpowers/specs/ not linked from root index.md
- brain save domains exclude docs/ — plans can't use atomic save path
- No unit tests for scripts (only brain bench)
- vault-bridge.py mojibake on Windows console
- Catalogue drift risk for files outside DOMAINS folders

P2:
- brain↔vault is verify-only, no promotion workflow
- Google Drive sync conflict policy untested
- dashboard.html untracked policy unclear
- No CI/pre-commit for validate+bench

## Decisions you must make in the plan

- Sessions 13/14 (RaapTech OS / Agent Arcade) vs brain-final: what is Kyle's next action after this session?
- Onboarding: create business/onboarding.md stub, fold into morning-ops, or remove from root index?
- Research synthesis scope: which 1–3 source files to distill this sprint (max)?
- Whether to extend brain.py DOMAINS or keep docs/ as spec-only with manual reindex

## Required output format

Produce a single markdown document (paste back to Kyle) titled:

  # Brain Final Improvement — Cursor Execution Plan

Structure:

### Baseline snapshot
- Command outputs summary (pass/fail)

### Gaps confirmed / gaps added / gaps rejected
- Table: Priority | Gap | Action | Owner (Cursor/Fable/Kyle/defer)

### Phase 1 — P0 (must ship today)
- [ ] Step N: <imperative> — Files: <paths> — Acceptance: <exact command + expected result> — Size: S/M/L

### Phase 2 — P1 (ship if time)
- Same checkbox format

### Phase 3 — Explicitly deferred
- Item + reason + suggested follow-up

### Session housekeeping
- Exact edits for sessions/sprint-tracker.md (next action, status row for this session)
- session-catalog.md row for this session
- Whether bench-questions.json Q9 answer should change

### Handoff to Cursor
- One-paragraph summary Kyle can paste to Cursor: "Execute Phase 1 and Phase 2 items through step X"

## Constraints

- OKF v0.1: concept files need YAML frontmatter with type; index.md files NO frontmatter (except bundle root)
- Do not hand-edit catalog.md — use brain reindex after content changes
- Minimize scope — final session must count; no whole-repo rewrites
- Fable for planning and hard calls; Cursor for implementation
- Do not commit or push — Kyle reviews git

## Anti-patterns (from research/fable5-prompting-patterns.md)

- No generic "make it better"
- State non-goals
- Every step needs verification command
- Shorter plan beats verbose wishlist

Begin by running the three PASS validators, then read docs/plans/next-steps-plan.md, then produce the execution plan.
```

---

## After Fable completes

Paste Fable's **Cursor Execution Plan** into Cursor with:

> Execute the Brain Final Improvement plan from Fable. Start with Phase 1 P0 items. Run okf-validate and brain bench after each phase.
