---
Status: ready-for-agent
Blocked by: 02
---

# Gate agent

## What to build

A Gate agent judges staging candidates with the Accept rule, rejects Secrets and stale residue with logged reasons, parks Conflicts without overwriting the brain, and `brain save`s only accepts with confirmed domain routing (unclear → references).

## Acceptance criteria

- [ ] Accept requires still true + operationally useful + not already covered (`brain ask`) + evidence-backed
- [ ] Secrets always rejected
- [ ] Accepts go only through `brain save`; Miners still cannot write domains
- [ ] Conflicts are parked in staging; brain claim unchanged
- [ ] Pass log records accept / reject / conflict with reasons
- [ ] Unclear domain → references; no new domains invented

## Blocked by

- 02 — Hermes Miner (thin proof)

## Comments
