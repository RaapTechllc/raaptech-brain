---
type: Reference
title: QA Report 2026-07-15
description: Evidence-driven QA results for the RaapTech Brain platform.
tags: [okf, auto-frontmatter]
timestamp: 2026-07-15T13:55:19Z
---

# QA Report — RaapTech Brain (full platform) — 2026-07-15

**Commit / branch / URL:** `5d89505` · `cursor/brain-next-steps-plan` · local `C:\Users\Kyle\CC\raaptech-brain`
**Plan:** `docs/qa-plan.md`
**Totals:** 13 passed · 5 failed · 0 partial · 0 blocked · 3 skipped

| # | Suite | Test | Result | Evidence |
|--:|---|---|---|---|
| 1.1 | OKF conformance | It should report OKF v0.1 conformant with 0 errors | failed | `docs/qa-evidence/01-okf-validate.txt` |
| 1.2 | OKF conformance | It should resolve catalogue lines without unresolved entries | passed | same (0 unresolved; 43 uncatalogued warnings) |
| 2.1 | Brain retrieval | It should answer cost-cap via `brain ask` with evidence | passed | `docs/qa-evidence/02-brain-ask-cost-cap.txt` |
| 2.2 | Brain retrieval | It should pass `brain bench` 10/10 | passed | `docs/qa-evidence/02-brain-bench.txt` |
| 2.3 | Brain retrieval | It should report token savings in bench summary | passed | same (67% saved) |
| 2.4 | Brain retrieval | It should generate `dashboard.html` via `brain html` | passed | `docs/qa-evidence/02-brain-html.txt` (70,031 bytes) |
| 2.5 | Brain retrieval | Nonsense ask should not crash (clear miss) | passed | `docs/qa-evidence/02-brain-ask-nonsense.txt` |
| 3.1 | Vault bridge | It should find vault Exists: yes | passed | `docs/qa-evidence/03-vault-report.txt` |
| 3.2 | Vault bridge | Domain mapping OK for PARA folders | passed | same |
| 3.3 | Vault bridge | Search `fleet` returns matches | passed | `docs/qa-evidence/03-vault-search-fleet.txt` |
| 4.1 | Google Drive sync | `--status` without UnicodeEncodeError | failed | `docs/qa-evidence/04-gdrive-status.txt` |
| 5.1 | Mine-pass | Spec + ADR + tickets on disk | passed | `docs/qa-evidence/05-mine-pass-inventory.txt` |
| 5.2 | Mine-pass | `docs/mine/` staging scaffold exists | failed | same (all MISSING) |
| 5.3 | Mine-pass | Mine-pass skill/entrypoint runnable | failed | same (only tickets/spec; no skill) |
| 5.4 | Mine-pass | Hermes thin-proof E2E Miner→Gate | failed | blocked by missing scaffold/skill — classified **failed** (feature absent) |
| 6.1 | Glossary | `CONTEXT.md` has Insight/Miner/Gate vocab | passed | `docs/qa-evidence/06-glossary-tickets.txt` |
| 6.2 | Glossary | Specs index lists Mine Pass | passed | same |
| 6.3 | Glossary | `tickets.md` frontier is Mine staging scaffold | passed | `tickets.md` (Blocked by: None) |

## Skipped
- Browser/UI Playwright — no product UI beyond static dashboard generation (Suite 2.4).
- ChatGPT/Claude export mining — out of scope per mine-pass spec.
- Cron mine passes — out of scope (on-demand only).

## Failures (fix-first order)

1. **1.1 OKF non-conformant (27 errors)** — severity **high**  
   Bundle fails validate. Errors: `.scratch/mine-pass/*` MISSING TYPE; many new `assessments/`, `CONTEXT.md`, `docs/adr/`, `tickets.md`, portfolio/fleet audit docs MISSING FRONTMATTER. Also 43 uncatalogued headings under sessions/portfolio and fleet/audits.  
   **Repro:** `cd C:\Users\Kyle\CC\raaptech-brain` → `python scripts/okf-validate.py` → exit 1.

2. **5.2–5.4 Mine-pass not implemented** — severity **high** (for the Insight-mining goal)  
   Spec/tickets exist; `docs/mine/` scaffold, gitignore rule, skill, and thin-proof run are absent. Frontier ticket never started.  
   **Repro:** check `Test-Path docs/mine/README.md` → False; see inventory evidence.

3. **4.1 Google Drive sync status crash** — severity **med** (known P0)  
   `UnicodeEncodeError` printing emoji lock on Windows cp1252 before any status output.  
   **Repro:** `python scripts/sync-google-drive.py --status`.

## Blocked (owner action)
- None this run (Python, vault path, and brain CLI all available).

## Recommended next
1. Fix failure **1.1** — exclude `.scratch/` from OKF scan and/or add OKF frontmatter / catalogue refresh for new markdown so validate is green again.
2. Implement frontier ticket **Mine staging scaffold** via `/implement` (unblocks 5.2–5.4).
3. Fix failure **4.1** — strip/replace emoji prints in `sync-google-drive.py` (same pattern as vault-bridge/okf-validate).

Highest-severity failure: **OKF validate red (27 errors)** — core retrieval still works (bench 10/10), but the bundle is not conformant and mine-pass E2E is not built.
