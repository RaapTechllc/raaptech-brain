---
Status: resolved
Blocked by:
---

# Mine staging scaffold

## What to build

Agents can write and read a shared mine staging area under the brain repo — candidates, Conflicts, and pass log — with a documented contract and gitignored artifacts so pass noise never lands in git.

## Acceptance criteria

- [x] `docs/mine/` exists with README describing the staging contract (claim, source path, evidence, proposed domain, gate decision + reason)
- [x] Placeholder `candidates.md`, `conflicts.md`, and `pass-log.md` match that contract
- [x] Staging artifacts are gitignored; README remains tracked
- [x] `okf-validate` / existing brain bench still pass (or staging is correctly excluded)

## Blocked by

None — can start immediately.

## Answer

Implemented `docs/mine/README.md` contract plus placeholder candidates/conflicts/pass-log; gitignored artifacts; OKF validate skips `docs/mine` and `.scratch`; bench 10/10.

## Comments
