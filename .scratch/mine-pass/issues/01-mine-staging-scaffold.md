---
Status: ready-for-agent
Blocked by:
---

# Mine staging scaffold

## What to build

Agents can write and read a shared mine staging area under the brain repo — candidates, Conflicts, and pass log — with a documented contract and gitignored artifacts so pass noise never lands in git.

## Acceptance criteria

- [ ] `docs/mine/` exists with README describing the staging contract (claim, source path, evidence, proposed domain, gate decision + reason)
- [ ] Placeholder `candidates.md`, `conflicts.md`, and `pass-log.md` match that contract
- [ ] Staging artifacts are gitignored; README remains tracked
- [ ] `okf-validate` / existing brain bench still pass (or staging is correctly excluded)

## Blocked by

None — can start immediately.

## Comments
