---
type: Specification
title: RaapTech Brain Next Steps Plan
description: Gap analysis and prioritized P0/P1/P2 plan for the final brain improvement push — Fable planning vs Cursor execution.
tags: [plan, brain, gaps, fable5, retrieval, okf]
timestamp: 2026-07-07T14:30:00Z
---

# RaapTech Brain — Next Steps Plan

**Date:** 2026-07-07 · **Status:** Draft for Fable review · **Repo:** `C:\Users\Kyle\CC\raaptech-brain`

## Executive summary

The brain bundle is **OKF-conformant** and **retrieval-ready** (10/10 bench, 177 catalogue lines, vault bridge OK). The remaining work is not greenfield — it is **hardening, gap-fill, and operational closure** before Fable description quota expires. This plan sequences a **Fable planning pass** (review + ordered execution spec) followed by **Cursor execution** of that spec in the same improvement window.

## Verified baseline (2026-07-07)

| Check | Command | Result |
|---|---|---|
| OKF conformance | `python scripts/okf-validate.py` | PASS — 48 `.md` files, 35 concepts, 11 indexes, 0 errors |
| Retrieval bench | `python scripts/brain.py bench` | 10/10 PASS — ~67% token savings vs naive reads |
| Vault bridge | `python scripts/vault-bridge.py --report` | PASS — 106 vault notes, domain mapping OK |
| Google Drive sync | `python scripts/sync-google-drive.py --status` | **FAIL** on Windows cp1252 (`UnicodeEncodeError` on emoji) |
| Git | `git status` | Clean vs `origin/main` except incidental `scripts/bench-results.json` churn |

**Domain coverage:** architecture (6), fleet (5), business (5), skills (5), integrations (4), sessions (3), references (2), research (1).

## Gap analysis (prioritized)

### P0 — Blocks agents or misroutes on this machine

| Gap | Rationale | Owner |
|---|---|---|
| **Windows console encoding in `sync-google-drive.py`** | `--status` crashes before any output; same class of bug already fixed in `okf-validate.py` / `vault-bridge.py` | Cursor |
| **Stale sessions domain vs brain reality** | Sprint tracker still points to Session 13/14 (RaapTech OS / Agent Arcade); brain retrieval work (2026-07-07) not reflected; bench Q9 hard-codes "Session 13" | Fable plan → Cursor |
| **Final Fable session not in catalog** | No session prompt for "brain final improvement"; quota is expiring — this session must be explicit in `sessions/` + fable5 | Fable plan → Cursor |

### P1 — Thin coverage, broken navigation, or drift risk

| Gap | Rationale | Owner |
|---|---|---|
| **Research domain (1 file)** | Only `fable5-prompting-patterns.md`; rich source material in `fable5/research/` and vault Market-Intel not synthesized | Fable scope → Cursor |
| **References domain (2 files)** | `memories.md` exists but is **not listed** in `references/index.md`; no local OKF spec extract | Cursor |
| **Root index overpromises** | `index.md` lists business "onboarding" — no concept file exists | Fable decide → Cursor |
| **`docs/` invisible in root nav** | `docs/plans/` and `docs/superpowers/specs/` not linked from bundle root; agents miss plans/specs | Cursor |
| **`brain save` domain list excludes `docs/`** | Plans/specs can't be written via atomic save path; encourages hand-edits | Fable decide → Cursor |
| **No script unit tests** | Only `brain bench` integration harness; regressions in okf-validate / vault-bridge / sync unguarded | Cursor |
| **Vault bridge display encoding** | `--report` runs but mojibake on Windows (`` in headers); cosmetic but erodes trust | Cursor |
| **Catalogue freshness after edits** | New files under `docs/` not in `DOMAINS` reindex scan; manual `brain reindex` easy to forget | Cursor (workflow + hook) |

### P2 — Nice-to-have / next sprint

| Gap | Rationale | Owner |
|---|---|---|
| **Brain ↔ vault is one-directional** | `vault-bridge.py` verifies reads; `brain save` never pushes to vault; no promotion workflow for synthesized research | Fable design → later |
| **Google Drive sync scope** | Push/pull all `*.md` — unclear conflict rules vs git + catalogue; never validated end-to-end in ledger | Fable design → later |
| **`dashboard.html` lifecycle** | Generated artifact at repo root; not in `.gitignore`, not in README quick start | Cursor |
| **Pre-commit / CI** | No automated `okf-validate` + `brain bench` on commit | Cursor |
| **Expand bench questions** | 10 questions don't cover plans, vault bridge, sync, or docs specs | Cursor |
| **fable5 STATUS.md reconciliation** | Brain sessions summarize fable5; two-way sync manual | Fable + Kyle |

## Phased execution plan

### Phase 0 — Fable planning session (this session)

**Goal:** Produce a checkable execution spec Cursor will implement without re-discovery.

| Step | Fable | Cursor |
|---|---|---|
| 0.1 | Re-run validators/bench; confirm baseline | — |
| 0.2 | Critique this gap list; add missed gaps | — |
| 0.3 | Decide: onboarding concept vs remove from root index | — |
| 0.4 | Decide: research synthesis scope (which fable5/vault sources to distill) | — |
| 0.5 | Decide: sessions 13/14 vs brain-final priority for Kyle | — |
| 0.6 | Output ordered checklist with file paths, acceptance commands, est. size (S/M/L) | — |

**Exit criteria:** Written execution plan with P0 items fully specified; P1 items either in scope or explicitly deferred with reason.

### Phase 1 — Cursor execution (P0, same day)

| Item | Acceptance |
|---|---|
| Fix `sync-google-drive.py` UTF-8 stdout (mirror `okf-validate.py` pattern) | `python scripts/sync-google-drive.py --status` exits 0 on Windows |
| Update `sessions/sprint-tracker.md` + `run-ledger.md` | Reflect brain-final session; note quota context |
| Add brain-final entry to `sessions/session-catalog.md` | Links to `docs/plans/fable-final-session-prompt.md` |
| Run `brain save` or edit + `brain reindex` | Catalogue includes new session/plan sections |
| `python scripts/okf-validate.py` + `python scripts/brain.py bench` | Both PASS |

### Phase 2 — Cursor execution (P1, scoped by Fable)

| Item | Acceptance |
|---|---|
| Fix `references/index.md` (add `memories.md`) | No dangling index links |
| Link `docs/plans/` from root `index.md` (and optionally `docs/superpowers/specs/`) | 2-click nav from root |
| Resolve onboarding gap per Fable decision | Index and domain agree |
| Research synthesis (if in scope) | ≥1 new research concept with `resource:` links to source |
| Encoding cleanup in `vault-bridge.py` | Clean `--report` on cp1252 |
| Minimal tests: `unittest` for catalogue parse + frontmatter validator | `python -m unittest` passes |
| Update `log.md` via `brain save` or manual dated entry | Change history current |

### Phase 3 — Deferred (P2, post-quota or follow-up)

- Vault → brain promotion workflow
- Drive sync conflict policy + dry-run mode
- CI/pre-commit wiring
- Bench expansion + dashboard.html policy

## Work split summary

| Role | Responsibility |
|---|---|
| **Fable** | Critical review, scope decisions, ordered execution spec, session prompt refinement |
| **Cursor** | Implement spec, run validators, reindex catalogue, no hand-editing `catalog.md` |
| **Kyle** | Approve scope tradeoffs (sessions 13/14 vs brain), commit/push when satisfied |

## Acceptance for "final improvement done"

1. `python scripts/okf-validate.py` — 0 errors
2. `python scripts/brain.py bench` — 10/10 (or expanded set if bench grows)
3. `python scripts/sync-google-drive.py --status` — no crash on Windows
4. `python scripts/vault-bridge.py --report` — vault reachable
5. Sessions domain documents the final Fable session and updated next action
6. Gap items marked **in scope** in Phase 2 are closed or explicitly deferred in this file

## Related

* [Fable Final Session Prompt](/docs/plans/fable-final-session-prompt.md)
* [Deterministic Retrieval Design](/docs/superpowers/specs/2026-07-07-second-brain-retrieval-design.md)
* [Sprint Tracker](/sessions/sprint-tracker.md)
