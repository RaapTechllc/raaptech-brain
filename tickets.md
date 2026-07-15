# Tickets: Mine Pass

On-demand Insight mining from Hermes (then vault) via Miners → Gate agent → parked Conflicts → Hermes audit. Spec: `docs/superpowers/specs/2026-07-09-mine-pass-design.md`. Glossary: `CONTEXT.md`. ADR: `docs/adr/0001-mine-pass-gate-and-audit.md`.

Work the **frontier**: any ticket whose blockers are all done. For this chain that means top to bottom. Use `/implement` one ticket at a time with a fresh context window.

## Mine staging scaffold

**What to build:** Agents can write and read a shared mine staging area under the brain repo — candidates, Conflicts, and pass log — with a documented contract and gitignored artifacts so pass noise never lands in git.

**Blocked by:** None — can start immediately.

- [ ] `docs/mine/` exists with README describing the staging contract (claim, source path, evidence, proposed domain, gate decision + reason)
- [ ] Placeholder `candidates.md`, `conflicts.md`, and `pass-log.md` match that contract
- [ ] Staging artifacts are gitignored; README remains tracked
- [ ] `okf-validate` / existing brain bench still pass (or staging is correctly excluded)

## Hermes Miner (thin proof)

**What to build:** An on-demand Hermes Miner reads only Hermes memories, emits at most ~20 candidate Insights into mine staging, and never writes brain domain files.

**Blocked by:** Mine staging scaffold

- [ ] Miner allowlist is Hermes memories only for thin proof
- [ ] Candidates land in staging in the shared contract shape (including proposed domain)
- [ ] Secrets are never proposed as candidates
- [ ] Archives/backups paths are not read
- [ ] Domain files and catalogue are unchanged by the Miner alone

## Gate agent

**What to build:** A Gate agent judges staging candidates with the Accept rule, rejects Secrets and stale residue with logged reasons, parks Conflicts without overwriting the brain, and `brain save`s only accepts with confirmed domain routing (unclear → references).

**Blocked by:** Hermes Miner (thin proof)

- [ ] Accept requires still true + operationally useful + not already covered (`brain ask`) + evidence-backed
- [ ] Secrets always rejected
- [ ] Accepts go only through `brain save`; Miners still cannot write domains
- [ ] Conflicts are parked in staging; brain claim unchanged
- [ ] Pass log records accept / reject / conflict with reasons
- [ ] Unclear domain → references; no new domains invented

## Mine-pass skill (Hermes path)

**What to build:** A brain-repo mine-pass skill runs Hermes Miner → Gate on demand and leaves staging ready for Hermes audit — without cron and without hosting the pipeline in OpenClaw MEMORY.

**Blocked by:** Gate agent

- [ ] Single on-demand entrypoint documents how to run the Hermes thin-proof pass
- [ ] Running it produces candidates + gate decisions + pass log in staging
- [ ] Skill does not schedule cron or touch vault yet
- [ ] Thin-proof dry run completes against live Hermes memories (or fixtures if offline)

## Hermes audit handoff

**What to build:** A Hermes-side audit step consumes parked Conflicts, validates against live sources, writes only Conflict resolutions (via `brain save` when correcting), and closes the pass log — without becoming a general writer for routine accepts.

**Blocked by:** Mine-pass skill (Hermes path)

- [ ] Audit prompt/runbook exists and points at staging Conflicts
- [ ] Audit may write Conflict resolutions only
- [ ] Routine accepts remain Gate-owned
- [ ] Pass log records audit outcomes (confirm / correct / leave parked)
- [ ] Brain bench still passes after a resolution write

## Vault Miner widen

**What to build:** After thin proof works, a Vault Miner mines allowlisted RaapTech-Vault folders (Areas/Fleet/Resources; not Inbox/dailies), and the mine-pass skill includes it in the same Gate → audit pipeline.

**Blocked by:** Hermes audit handoff

- [ ] Vault Miner allowlist excludes Inbox, dailies, archives
- [ ] Candidates use the same staging contract
- [ ] Mine-pass skill can run Hermes + Vault Miners into one Gate queue
- [ ] OpenClaw MEMORY and ChatGPT/Claude exports remain out of scope
