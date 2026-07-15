---
type: Reference
title: Mine Staging Contract
description: Shared candidate/conflict/pass-log contract for Hermes Miner, Vault Miner, Gate agent, and Hermes audit.
tags: [mine-pass, staging, contract]
timestamp: 2026-07-15T14:00:00Z
---

# Mine Staging

Ephemeral working files for an on-demand **mine pass**. Durable Insights enter domain files only via `brain save` after Gate (or Conflict resolution via Hermes audit).

## Files

| File | Role | Git |
|---|---|---|
| `candidates.md` | Miner output queue | gitignored |
| `conflicts.md` | Parked Conflicts for Hermes audit | gitignored |
| `pass-log.md` | Accept / reject / conflict / audit outcomes | gitignored |
| `README.md` (this file) | Contract documentation | tracked |

## Candidate contract

Each candidate is one H2 section:

```markdown
## C-001

- **claim:** <one-sentence Insight>
- **source_path:** <absolute or repo-relative path>
- **evidence:** <short quote or paraphrase>
- **proposed_domain:** architecture | fleet | business | skills | integrations | research | references | sessions
- **miner:** hermes | vault
- **gate_decision:** pending | accept | reject | conflict
- **gate_reason:** <filled by Gate agent>
```

## Conflict contract

```markdown
## X-001

- **brain_claim:** <current brain statement>
- **brain_ref:** <catalog path#anchor or file>
- **source_claim:** <contradicting statement>
- **source_path:** <allowlisted source path>
- **audit_status:** parked | confirmed_brain | corrected | left_parked
- **audit_notes:** <filled by Hermes audit>
```

## Pass-log contract

Append-only lines (or H2 per event):

```markdown
## 2026-07-15T14:00:00Z — accept C-001 → references
Reason: still true; operational; not covered; evidence-backed.
```

## Rules

1. Miners write candidates only — never domain files.
2. Gate alone accepts via `brain save`; unclear domain → `references`.
3. Secrets are never candidates.
4. Conflicts never auto-overwrite the brain.
5. Regenerate staging each pass; do not commit artifacts.
