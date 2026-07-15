---
type: Reference
title: 01 CODEX PROJECT FACTORY ARCHITECTURE DECISION
description: "Assessment note: 01-CODEX-PROJECT-FACTORY-ARCHITECTURE-DECISION."

tags: [okf, auto-frontmatter]
timestamp: 2026-07-15T13:55:19Z
---

# Codex Project Factory — Architecture Decision

**Date:** 2026-07-14  
**Repository:** `https://github.com/RaapTechllc/codex-project-factory`  
**Inspected revision:** `master` / `7fbb782299c2100f8a14353631ae8fb43529e7ec`  
**Phase:** Read-only decision package

## Executive decision

# BLOCKED WITH PREREQUISITES

Factory is a credible bounded Product Delivery Factory, not a company-wide orchestrator. Its source implements the right project-delivery primitives and its complete repository validation passes. It is **not yet approved for a Docker VM pilot** because the repository has no deployment manifest or service health contract, the Docker VM has not demonstrated the required Node/Codex/Convex/GitHub runtime, and the local-only Convex persistence, backup, restore, upgrade, supervision, and exposure design has not been selected or proven.

This is a prerequisite block, not a rejection of the architecture.

## Proposed charter

> Codex Project Factory owns approved internal product milestones from durable goal/run state through isolated Codex execution, deterministic validation, independent review, and draft-PR evidence—never fleet orchestration, canonical knowledge, policy enforcement, merge, deployment, or production mutation.

## Actual current responsibilities

| Responsibility | Code evidence | Status |
|---|---|---|
| Project, idea, goal, run, thread, turn, artifact, event, command, workflow-node, and learning projections | `convex/schema.ts:9-78` | Implemented |
| Explainable idea scoring and ranked goal intake | `convex/lib/scoring.ts:1-10`; `convex/ideas.ts`; `convex/goals.ts` | Implemented; policy is simplistic |
| Approval-key and dispatch-key idempotency | `convex/goals.ts:5-12`; `convex/runs.ts:4-11` | Implemented |
| Command claim, four-hour lease, heartbeat, completion | `convex/commands.ts:13-25`; `apps/codex-bridge/src/worker.ts:47-95` | Implemented |
| Codex app-server JSON-RPC lifecycle | `apps/codex-bridge/src/json-rpc.ts:30-101`; `gateway.ts` | Implemented against an external Codex CLI |
| Distinct Codex thread/session/turn identity | `convex/schema.ts:38-48`; `apps/codex-bridge/src/types.ts:18-26,54-58` | Implemented |
| Fresh planning, architecture, implementation, verification, review, and repair threads | `.archon/workflows/milestone-to-pr.yaml:7-43`; `workflow.ts` | Implemented |
| Managed Git worktree and branch isolation | `workflow.ts:162-171` | Implemented |
| Deterministic validation with at most three repair cycles | `.archon/workflows/milestone-to-pr.yaml:3-5,25-33`; `workflow.ts:100-113` | Implemented |
| Sensitive-path refusal, validation-before-commit, protected-branch refusal, draft PR only | `workflow.ts:116-180` | Implemented |
| Minimal CLI and read-only dashboard | `apps/cli/src/index.ts`; `apps/web/app/page.tsx:9-27` | Implemented |

## Explicit non-responsibilities

Factory must not own:

- live fleet health, versions, reachability, Docker inventory, or infrastructure truth;
- Hermes conversations, approvals, fleet routing, or operator identity;
- RaapTech OS policy, budget enforcement, audit/DLP, or kill switches;
- Archon recipe governance beyond consuming versioned project-delivery recipes;
- Project Co-Pilot's guarded planning/specification product;
- Agentic Brain knowledge promotion or canonical operational context;
- Git/GitHub source authority, credentials, merge, release, deployment, or production state;
- the Codex runtime or Convex backend itself.

## Architectural strengths

1. **Bounded lifecycle matches adopted doctrine.** Code owns state, routing, isolation, retries, validation, and evidence; agents receive narrow roles (`raaptech-handoff-2026-07-14.md:18-39`).
2. **Safety is encoded, not merely documented.** Protected branches are refused, sensitive paths are blocked, validation is rerun before delivery commit, and only draft PRs are created (`workflow.ts:116-180`).
3. **Identity is recoverable.** Convex stores independent thread, session, turn, run, and workflow-node references; root creation is idempotent (`schema.ts:31-72`; `idempotency.ts:25-62`).
4. **Reasoning lanes are isolated.** Planning, architecture, verification, and review run in fresh child threads, reducing self-review contamination.
5. **Repository health is real.** `npm run validate` passed lint, typecheck, 25 tests, and all five package builds on 2026-07-14.

## Documented intent versus implemented behavior

- `.archon/workflows/milestone-to-pr.yaml:3-5` declares `max_parallel_implementers: 2`, but `executeWorkflow` iterates nodes sequentially (`workflow.ts:66-80`) and never reads or enforces that limit. Pilot concurrency must therefore be enforced externally at one run; the YAML field is not a runtime control.
- `README.md:44` instructs operators to run app-server contract tests before unattended use, but the inspected gateway tests use `FakeTransport`; no test launches the real `codex app-server` or proves live protocol compatibility. The 25 passing tests establish unit behavior, not an app-server integration contract.
- `README.md:62` describes a Convex MCP integration safety boundary, but no MCP integration was found in the inspected source. Treat this as stale or prospective documentation, not an implemented capability or control.
- The repository contains a CI workflow only inside the generated project template (`packages/project-template/template/.github/workflows/ci.yml`); Factory itself has no active repository CI workflow.

## Failure modes and missing invariants

| Gap | Consequence | Required invariant before pilot |
|---|---|---|
| No Dockerfile, Compose file, systemd unit, or CI workflow in Factory repo | No reproducible service deployment or restart contract | Versioned deployment bundle outside or inside repo, reviewed before use |
| Convex topology is unspecified | Hosted Convex would violate an unexamined local-only boundary; self-hosted persistence is unproven | Explicit self-hosted Convex decision, loopback/Tailscale binding, persistent volume, backup/restore test |
| No `/health` or worker readiness endpoint | Process existence cannot prove Codex/Convex/Git/GitHub readiness | Health contract that checks dependencies without mutating a target repo |
| `costUsd` is stored but no limit is enforced | Factory cannot own budget enforcement | RaapTech OS pre-dispatch budget gate; Factory records usage only |
| Approval is a Convex mutation/key, not authenticated operator evidence | Approval provenance is weak | Hermes/Kyle approval reference supplied one-way; no anonymous web mutation |
| Worktree creation exists but cleanup/retention does not | Disk growth and stale branches/worktrees | Capped TTL/retention and explicit cleanup command with evidence |
| Worker can process multiple commands while app-server events are attributed only when one run is active | Concurrent event attribution can be lost | Pilot concurrency fixed at one; later add explicit run correlation |
| Four-hour command lease is static | Duplicate work possible after long/stalled jobs | Pilot jobs below lease or renewable lease proven; reconcile before retry |
| Runtime versions are incompletely pinned | Drift across Node, npm, Codex CLI, Convex backend/client | Compatibility matrix and immutable versions/images |
| Repository contracts and Convex schema disagree on some run-phase vocabulary (`ready/failed` versus `completed`) | Cross-layer validation drift | Reconcile contract schema before relying on external consumers |
| Artifact URIs include local paths and summaries, but retention/redaction policy is absent | Evidence loss or leakage | Approved artifact root, redaction, retention, and backup policy |

## Facts

- Origin, branch, revision, and clean state were verified before inspection.
- Node `>=22` and npm `11.11.0` are declared (`package.json:5,28-30`).
- Source references only `CONVEX_URL`, `FACTORY_PROJECTS_ROOT`, and `NEXT_PUBLIC_CONVEX_URL`; values were not opened.
- The local Codex CLI on Maxx is authenticated, and `codex app-server` is present; that does not prove Docker VM readiness.
- Docker VM is the accepted durable Linux workflow plane and current infrastructure health is green, but adding Factory is a new workload requiring its own service contract.

## Assumptions

- The Docker VM can install a compatible Codex CLI and authenticate it under a dedicated service account.
- Self-hosted Convex can satisfy the local-only requirement using its official Docker deployment, but Factory has never been tested against it.
- A low-risk internal repository can expose a stable deterministic validation command and permit a draft PR.

## Risks

- External Codex or GitHub authentication can fail mid-run despite healthy Factory code.
- Self-hosted Convex SQLite and Factory artifact/worktree data may be lost without explicit volume backups and restore proof.
- Unbounded worktrees, artifacts, events, and learnings can grow disk usage.
- The dashboard has no demonstrated authentication boundary; it must not be exposed broadly.
- Generic research intake overlaps with Agentic Brain/Project Co-Pilot and should be disabled for the first pilot.

## Required Kyle decisions

1. Approve **self-hosted Convex on Docker VM** for the pilot; hosted Convex is not the default.
2. Approve one dedicated internal target repository and allow Factory to push a branch and create a **draft PR only**.
3. Set pilot ceilings: **singleton concurrency** (exactly one concurrent run), three repair cycles maximum, time/token/spend cap enforced before dispatch, and retention period.
4. Decide whether the Factory dashboard is omitted initially (recommended) or bound to Tailscale with authentication.

## Decision exit criteria

Change this decision to `APPROVE FOR DOCKER VM PILOT` only after every `BLOCKED` row in the deployment-readiness document has command-backed proof and a dry preflight shows no customer, production, or canonical-vault mutation.
