# QA Plan — RaapTech Brain (full platform) — 2026-07-15

**Environment:** local CLI · branch `cursor/brain-next-steps-plan` · commit `5d89505` · workspace `C:\Users\Kyle\CC\raaptech-brain`
**Agent mode:** local
**Evidence:** CLI output (saved under `docs/qa-evidence/`)

| Suite # | Surface / flow | Tests (count) | Priority |
|--:|---|--:|---|
| 1 | OKF conformance | 2 | P0 |
| 2 | Brain retrieval CLI (`ask` / `bench` / `html`) | 5 | P0 |
| 3 | Vault bridge | 3 | P0 |
| 4 | Google Drive sync | 1 | P0 |
| 5 | Mine-pass pipeline (spec → scaffold → run) | 4 | P0 |
| 6 | Glossary / spec / tickets presence | 3 | P1 |

## Suites detail

### Suite 1 — OKF conformance
- [ ] It should report OKF v0.1 conformant with 0 errors
- [ ] It should resolve catalogue lines without unresolved entries

### Suite 2 — Brain retrieval CLI
- [ ] It should answer a known cost-cap question via `brain ask` with an evidence block
- [ ] It should pass `brain bench` 10/10
- [ ] It should report token savings vs naive reads in the bench summary
- [ ] It should generate `dashboard.html` via `brain html` without error
- [ ] It should refuse or no-op harmlessly when asked a nonsense question (still returns a best-effort match or clear miss — assert non-crash)

### Suite 3 — Vault bridge
- [ ] It should find the RaapTech-Vault path and report Exists: yes
- [ ] It should map brain domains to vault PARA folders with OK status
- [ ] It should search vault notes for a known topic (e.g. fleet) and return matches or an empty-but-successful result

### Suite 4 — Google Drive sync
- [ ] It should complete `sync-google-drive.py --status` without UnicodeEncodeError and print auth/status output

### Suite 5 — Mine-pass pipeline
- [ ] It should have mine-pass spec + ADR + tickets on disk
- [ ] It should have `docs/mine/` staging scaffold (README + candidates/conflicts/pass-log)
- [ ] It should have a mine-pass skill/entrypoint runnable on demand
- [ ] It should run a Hermes thin-proof mine pass end-to-end (Miner → Gate → staging) without writing Secrets

### Suite 6 — Glossary / design artifacts
- [ ] It should have root `CONTEXT.md` with Insight / Miner / Gate vocabulary
- [ ] It should list mine-pass in `docs/superpowers/specs/index.md`
- [ ] It should have `tickets.md` frontier ticket unblocked (Mine staging scaffold)

## Kill criteria
Stop the whole run and escalate if: brain.py missing / Python cannot import scripts / vault path deleted mid-run / destructive write attempted outside QA fixtures.

## Skipped (with reason)
- Browser/UI Playwright suites — brain is CLI + markdown; no product UI beyond static dashboard file generation (covered in Suite 2).
- ChatGPT/Claude export mining — out of scope per mine-pass spec.
- Cron mine passes — out of scope (on-demand only).
