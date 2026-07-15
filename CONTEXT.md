---
type: Reference
title: RaapTech Brain Domain Glossary
description: Ubiquitous language for Insights, Miners, Gate agent, and mine passes.
tags: [okf, auto-frontmatter]
timestamp: 2026-07-15T13:55:19Z
---

# RaapTech Brain

Agent-traversable knowledge bundle for RaapTech. Synthesizes durable operational truth from workstation sources; does not mirror raw chat or vault dumps.

## Language

**Insight**:
A durable, still-true operational fact or pattern worth keeping in the brain (decisions, topology, runbooks, conventions, current blockers).
_Avoid_: Memory dump, transcript, note copy, archive

**Stale residue**:
Old session chatter, superseded facts, personal asides, and one-off debugging that should stay in the source platform and never enter the brain.
_Avoid_: Legacy memory, junk, noise (too vague — name the class)

**Source platform**:
An external store agents may read for mining (Obsidian vault, Hermes/OpenClaw MEMORY files, ChatGPT/Claude exports) but that is not itself the brain.
_Avoid_: Second brain (reserved for this OKF bundle), vault-as-brain

**Miner**:
An agent that only reads source platforms and emits candidate Insights; it never writes brain domain files.
_Avoid_: Importer, syncer, crawler

**Gate**:
The accept/reject step that turns a candidate Insight into a `brain save` — or discards it as stale residue. In v1 the Gate is a **Gate agent** (not a human checklist), scored for impact vs outdated/flopped claims.
_Avoid_: Review, approval (too generic), auto-commit

**Gate agent**:
An agent whose only job is to judge Miner candidates: keep high-impact still-true Insights, reject stale residue and low-value noise, then invoke `brain save` only for accepts.
_Avoid_: Miner (proposes only), curator (vague), reviewer

**Accept rule**:
A candidate Insight is accepted only if it is still true, operationally useful, not already covered by `brain ask`, and evidence-backed from an allowlisted source. Fail any one → reject with a logged reason.
_Avoid_: Interesting, maybe useful, vibes

**Conflict**:
A parked disagreement between a brain claim and an allowlisted source (or between sources). Mining never auto-overwrites the brain on Conflict; the claim is set aside for audit.
_Avoid_: Error, bug, mismatch (too vague)

**Hermes audit**:
An end-of-pass validation run (local agent via Hermes) that checks parked Conflicts and brain claims against live sources, then confirms or corrects what is true before any overwrite. Audit may write only Conflict resolutions; routine accepts stay with the Gate agent.
_Avoid_: Sync, reindex, bench (those are different tools)

**Allowlisted source (v1)**:
Hermes memories (`AppData\Local\hermes\memories`) and RaapTech-Vault (Areas/Fleet/Resources; not Inbox/dailies by default). OpenClaw MEMORY files and ChatGPT/Claude exports are out of scope until a later pass.
_Avoid_: Full workstation crawl, archive folders, `_agent-md-backups`

**Mine pass**:
An on-demand run of Hermes Miner + Vault Miner → Gate agent → park Conflicts → Hermes audit. Not scheduled by cron in v1.
_Avoid_: Sync job, continuous crawl, nightly import

**Hermes Miner**:
Miner specialized on `AppData\Local\hermes\memories`; emits candidate Insights only.
_Avoid_: Hermes audit (validates; does not mine)

**Vault Miner**:
Miner specialized on RaapTech-Vault allowlisted folders; emits candidate Insights only.
_Avoid_: Vault bridge (verify/search tool; not a Miner)

**Mine staging**:
Ephemeral pass files under `docs/mine/` in the brain repo — `candidates.md`, `conflicts.md`, `pass-log.md`. Regenerated each mine pass; gitignored except a README that documents the layout. Only accepted Insights enter domain files via `brain save`.
_Avoid_: Vault inbox dump, committing raw transcripts into domains

**Mine-pass skill**:
Brain-repo entrypoint that runs Hermes Miner + Vault Miner + Gate agent against allowlisted sources and writes mine staging. Hermes audit is a separate Hermes-side step after Conflicts are parked.
_Avoid_: OpenClaw MEMORY-hosted pipeline, always-on crawler

**Secret**:
Credentials or key material (API keys, tokens, passwords, private keys). Always rejected by Miners and Gate; never enters the brain — point at the secret store instead. Non-secret ops facts (Tailscale IPs, service names) remain allowed.
_Avoid_: Sensitive (too vague), PII dump

**Domain routing**:
Miner proposes a brain domain for each candidate; Gate confirms or overrides. If unclear, save under **references**. v1 never invents new domains.
_Avoid_: Dump-everything-in-research, new ad-hoc folders

**Thin proof**:
The first mine pass uses Hermes memories only (`AppData\Local\hermes\memories`), caps candidates (~20), runs Gate + Hermes audit end-to-end, then widens to vault. Same pipeline; smaller input.
_Avoid_: Big-bang import, full vault crawl on day one
