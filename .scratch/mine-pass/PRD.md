---
Status: ready-for-agent
---

# Mine Pass — Insight Mining from Hermes and Vault

Canonical copy also at `docs/superpowers/specs/2026-07-09-mine-pass-design.md`. Glossary: `CONTEXT.md`. ADR: `docs/adr/0001-mine-pass-gate-and-audit.md`.

## Problem Statement

The brain is retrieval-ready but only partially filled from curated synthesis. Workstation source platforms hold operational truth mixed with stale residue. Bulk import would pollute the catalogue; doing nothing leaves agents blind to live ops facts. Kyle needs agents that mine Insights only, gate them for impact and freshness, park Conflicts, and validate truth via Hermes audit — without mirroring dumps.

## Solution

An on-demand mine pass: specialized Miners read allowlisted sources and emit candidates; a Gate agent accepts or rejects under a hard Accept rule and secrets ban; Conflicts are parked; a Hermes audit validates and may write only Conflict resolutions. Staging lives under gitignored `docs/mine/`. First run is a Hermes-only thin proof; vault widens later.

## User Stories

1. As Kyle, I want to run a mine pass on demand, so that Insights land when I choose — not on a cron that floods the brain.
2. As Kyle, I want Miners to never write domain files, so that stale residue cannot sneak in without a Gate.
3. As a Hermes Miner, I want to read only Hermes memories, so that I emit candidates from a small, live source.
4. As a Vault Miner, I want to read only allowlisted vault folders, so that Inbox and dailies stay out by default.
5. As a Gate agent, I want a four-part Accept rule, so that I keep still-true, useful, novel, evidence-backed Insights only.
6. As a Gate agent, I want to reject Secrets always, so that credentials never enter the brain.
7. As a Gate agent, I want to call `brain ask` before accept, so that I do not duplicate covered Insights.
8. As a Gate agent, I want to `brain save` only accepts, so that the catalogue and log stay consistent.
9. As Kyle, I want Conflicts parked instead of auto-overwrite, so that flopped source claims cannot clobber brain truth.
10. As a Hermes audit, I want to resolve parked Conflicts against live sources, so that the brain stays true-to-source when it must change.
11. As a Hermes audit, I want write authority only for Conflict resolutions, so that routine accepts stay with the Gate.
12. As Kyle, I want mine staging under `docs/mine/`, so that candidates and Conflicts are inspectable during a pass.
13. As Kyle, I want staging artifacts gitignored, so that pass noise and source snippets are not committed.
14. As Kyle, I want a mine-pass skill in the brain repo, so that Cursor/Claude Code can orchestrate Miners + Gate without burying the pipeline in OpenClaw MEMORY.
15. As Kyle, I want the first pass to be Hermes-only with a ~20 candidate cap, so that the Gate + audit loop is proven before vault widen.
16. As Kyle, I want unclear domain routing to fall back to references, so that Miners do not invent domains.
17. As Kyle, I want OpenClaw MEMORY and ChatGPT/Claude exports deferred, so that v1 stays focused.
18. As Kyle, I want reject reasons logged in the pass log, so that I can tune Gate false positives.
19. As an agent consuming the brain, I want only Insights in domains, so that `brain ask` stays high-signal.
20. As Kyle, I want vault widen after thin proof, so that the same pipeline scales without redesign.

## Implementation Decisions

- Seam 1 — Mine staging contract (shared candidate/conflict/pass-log shape).
- Seam 2 — Existing `brain ask` / `brain save` as only brain read/write.
- Seam 3 — Mine-pass skill orchestrates Hermes Miner → Gate (thin proof); later Vault Miner.
- Seam 4 — Hermes audit handoff for Conflicts only.
- Allowlist, thin proof, domain routing, secrets ban, gitignore staging — as in the repo spec copy.
- ADR `0001-mine-pass-gate-and-audit.md`.

## Testing Decisions

- External behaviour at staging + brain CLI seams.
- Fixture-based Accept-rule cases; thin-proof dry run; do not break `brain bench` 10/10.

## Out of Scope

Cron; OpenClaw/ChatGPT/Claude mining; brain→vault write; auto-overwrite Conflicts; full crawl; Drive sync; new domains.

## Further Notes

Pass 2 adds Vault Miner after thin proof. Work tickets will live in repo-root `tickets.md` and optionally `.scratch/mine-pass/issues/`.
