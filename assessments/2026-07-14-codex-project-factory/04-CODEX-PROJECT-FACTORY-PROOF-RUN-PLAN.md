---
type: Reference
title: 04 CODEX PROJECT FACTORY PROOF RUN PLAN
description: "Assessment note: 04-CODEX-PROJECT-FACTORY-PROOF-RUN-PLAN."

tags: [okf, auto-frontmatter]
timestamp: 2026-07-15T13:55:19Z
---

# Codex Project Factory — Proof-Run Plan

**Date:** 2026-07-14  
**Execution:** Not authorized in this session.  
**Purpose:** One recurring, internal, reversible proof after deployment prerequisites pass.

## Selected proof milestone

> **Weekly documentation-drift check for one low-risk internal TypeScript repository:** update one generated/maintained repository inventory section when source paths or npm scripts have drifted, producing an isolated worktree, deterministic validation evidence, independent verification, independent review, and an unmerged draft PR.

This is narrow, recurring, measurable, and reversible. It exercises discovery, editing, validation, review, Git worktrees, Codex identity, Factory state, and draft-PR delivery without customer data or production mutation.

## Target repository selection criteria

The repository must:

- be owned by RaapTech and explicitly approved by Kyle;
- be internal/non-customer and contain no production/customer datasets;
- not be the canonical Obsidian vault, infrastructure-as-code for a live host, secrets repo, trading execution system, or deployment repo;
- have a clean default branch and a disposable branch policy;
- have Node `>=22` compatibility and a deterministic `npm run validate` command that passes at baseline;
- contain a clearly delimited generated/maintained documentation inventory whose expected output can be checked mechanically;
- permit the dedicated GitHub identity to push a `codex/<run>` branch and create a draft PR, but not merge or administer the repository.

## Exact work-item input contract

```json
{
  "source": "hermes-kyle-approval",
  "approvalRef": "immutable operator decision reference",
  "repository": "approved RaapTech internal GitHub URL",
  "defaultBranch": "verified remote default branch",
  "baseRevision": "full commit SHA",
  "outcome": "Synchronize the delimited repository inventory section with current tracked source paths and package scripts; no other prose or code changes.",
  "allowedPaths": ["docs/repository-inventory.md"],
  "forbiddenPaths": [".env*", ".github/workflows/**", "infra/**", "deploy/**", "secrets/**"],
  "validation": [
    "npm ci --ignore-scripts",
    "npm run validate",
    "npm run docs:inventory:check",
    "git diff --check",
    "git diff --name-only <baseRevision>...HEAD"
  ],
  "riskTier": "LOW / INTERNAL / REVERSIBLE",
  "maxConcurrentRuns": 1,
  "maxRepairCycles": 3,
  "delivery": "draft-pr-only",
  "expiresAt": "approved dispatch deadline"
}
```

The target repository must implement `docs:inventory:check` before selection. It must deterministically regenerate the inventory to a temporary location and fail on drift. If no repository already has that check, adding it is a separate human-approved prerequisite, not part of this proof.

## Risk tier and approval points

| Gate | Owner | Required evidence / action |
|---|---|---|
| P0 deployment prerequisite gate | Kyle / Docker VM ops | All `BLOCKED` readiness rows closed, backup/restore and health contract passed |
| P1 work-item approval | Kyle in Hermes | Exact repo, base SHA, allowed path, checks, cap, and deadline approved |
| P2 dispatch permit | RaapTech OS or manual equivalent | One run only; budget/time cap; no active run; kill switch available |
| P3 draft PR review | Kyle | Inspect diff and evidence; Factory cannot merge |
| P4 cleanup/retention | Factory operator | Worktree removed/pruned; evidence retained; credentials unchanged/revoked per policy |

## Required Factory configuration/state

- Pinned Factory revision and pinned Node/npm/Codex/Convex versions.
- Self-hosted Convex local-only endpoint and persistent volume.
- Dedicated service account with repo-scoped GitHub and Codex credential references.
- `CONVEX_URL` and `FACTORY_PROJECTS_ROOT`; `NEXT_PUBLIC_CONVEX_URL` omitted because UI is omitted.
- Project record with exact repository/root/base revision.
- Goal containing the input contract and approval reference.
- Singleton worker enforcement, three-repair maximum, time/spend stop, worktree/artifact roots, and retention policy.
- Baseline `npm run validate` and `npm run docs:inventory:check` passing before dispatch.

## Exact lifecycle

1. **Approve:** Hermes records Kyle's exact work item and sends only the immutable approval reference + bounded contract.
2. **Preflight:** Verify target origin/default branch/base SHA/clean state, health contract, free space, backup freshness, singleton status, credentials, and baseline checks.
3. **Create state:** Factory upserts project, creates candidate goal, records approval key, and dispatches one idempotent run.
4. **Create root:** Worker claims command, starts Codex app-server root task, and reconciles distinct thread/session IDs.
5. **Plan:** Fresh planning thread produces a file-scoped plan and check mapping in `.factory/artifacts/<run>/`.
6. **Architecture critique:** Fresh architecture thread rejects scope expansion, nondeterminism, or forbidden-path access.
7. **Isolate:** Factory creates `.factory-worktrees/<repo>-<run>` and branch `codex/<run>` from the approved base SHA.
8. **Implement:** Fresh implementation thread changes only `docs/repository-inventory.md` and leaves evidence.
9. **Deterministic validation:** Run exact commands in order. Any failure permits at most three fresh repair threads; then block.
10. **Verify:** Fresh verifier confirms acceptance criteria from repository state and captured command output; it does not trust the implementer summary.
11. **Review:** Fresh reviewer checks correctness, security, maintainability, scope, and exact changed-path allowlist.
12. **Deliver:** Factory refuses protected/default branch, blocks sensitive files, reruns validation, creates/reuses one branch, and creates one **draft PR only**.
13. **Synthesize:** Root thread returns structured `ready`, summary, and remaining risks. Any unmet criterion blocks completion.
14. **Notify:** Factory emits run/evidence/PR status to Hermes; Kyle decides manually.
15. **Clean up:** After evidence capture, remove/prune the worktree; preserve the branch/draft PR until Kyle closes or accepts it; apply retention policy.

## Worktree isolation and cleanup

- Worktree root is dedicated to Factory and outside the canonical checkout.
- Base SHA is recorded before creation; branch name includes run ID.
- Only one run is active.
- Before delivery, assert changed paths equal the allowlist and the worktree is based on the approved SHA.
- On cancel/failure, interrupt active turn, mark run terminal, retain diagnostics, then remove the worktree after confirming no uncommitted evidence is required.
- Cleanup commands are operator-reviewed for the proof:

```bash
git -C <canonical-repo> worktree list --porcelain
git -C <canonical-repo> worktree remove <factory-worktree>
git -C <canonical-repo> worktree prune
git -C <canonical-repo> branch --list 'codex/*'
```

No branch deletion or draft PR closure without Kyle approval.

## Deterministic checks

All must exit zero:

```bash
npm ci --ignore-scripts
npm run validate
npm run docs:inventory:check
git diff --check
test "$(git diff --name-only "$BASE_SHA"...HEAD)" = "docs/repository-inventory.md"
git status --porcelain
```

For the final line, expected state is clean after the verified delivery commit. Capture exit code, duration, revision, and bounded stdout/stderr for each check.

## Verifier versus reviewer

- **Verifier:** maps each acceptance criterion to observed files, diff, commit, and deterministic command output. It answers only whether the contract was met.
- **Reviewer:** independently evaluates unnecessary scope, unsafe paths, secret risk, architectural fit, maintainability, and whether the PR should remain blocked. It cannot waive a failed check.

Both use fresh Codex threads and neither is the implementation thread.

## Draft-PR-only output

Allowed external mutation is exactly one approved branch push and one draft PR. The Factory must not mark ready for review, merge, rebase default branch, release, deploy, invoke repository workflows intentionally, or touch production/customer/canonical-vault state.

## Cancel and rollback behavior

- Kyle/RaapTech OS may cancel before draft PR creation; Factory interrupts active turns and records terminal state.
- If a draft PR exists, cancellation leaves it draft, adds no further commits, and alerts Kyle.
- Revoke/disable dispatch, preserve evidence, clean worktree, and close/delete branch only after Kyle's decision.
- If Convex/worker fails, restore from the pre-pilot backup or retire the disposable proof state; GitHub draft PR and Git history remain the external evidence.

## Measurable success criteria

- Exactly one run, one managed worktree, one run branch, and one draft PR.
- No changed path outside `docs/repository-inventory.md`.
- All five deterministic checks pass on the exact delivered commit.
- Separate planning, architecture, implementation, verification, and review thread references are recorded with distinct IDs.
- Cancellation and worker restart are tested on a disposable pre-run or rehearsal without duplicate root, branch, or PR.
- Repair count is `0` for the qualifying proof; any repair may be informative but does not qualify the first run for promotion.
- No secrets in diff, logs, artifacts, Convex records, or PR.
- No merge/deploy/customer/canonical-vault mutation.
- Worktree cleanup succeeds and disk usage returns within the agreed threshold.
- Backup and isolated restore can read back the completed run and artifacts.

## Failure criteria and stop conditions

Stop and mark the pilot failed on:

- any prerequisite health failure or stale backup/restore evidence;
- target origin/base SHA mismatch, dirty baseline, or baseline check failure;
- any forbidden/unapproved path change;
- secret-like path/content detection;
- more than one active run or ambiguous event attribution;
- any attempt to merge, deploy, change infrastructure, or access customer data;
- budget/time ceiling reached;
- third repair failure—the pilot allows three repair cycles maximum, then blocks;
- non-draft PR, duplicate branch/PR, or protected-branch operation;
- inability to cancel, restart safely, clean the worktree, or restore state.

## Evidence required to qualify for Docker VM pilot acceptance

- Pinned component/version manifest and deployment revision.
- Preflight and health report with listener/bind evidence.
- Baseline and delivered validation outputs with checksums/revisions.
- Convex run/goal/thread/session/turn/workflow-node/artifact records.
- Worktree/branch/base-SHA and changed-path evidence.
- Draft PR URL and proof it remains open/draft/unmerged.
- Service restart/idempotency and cancellation evidence.
- Disk before/after and cleanup output.
- Backup identifier and isolated restore readback.
- Hermes approval reference and final Kyle accept/reject decision.

Only a clean success against all criteria supports changing the architecture decision to `APPROVE FOR DOCKER VM PILOT`.
