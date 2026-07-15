---
type: Reference
title: 03 CONTROL PLANE OWNERSHIP MAP
description: "Assessment note: 03-CONTROL-PLANE-OWNERSHIP-MAP."

tags: [okf, auto-frontmatter]
timestamp: 2026-07-15T13:55:19Z
---

# Control Plane Ownership Map

**Date:** 2026-07-14  
**Rule:** Every concern has exactly one primary owner. Factory is project-delivery scoped; it is not the fleet, policy, knowledge, credential, or deployment authority.

## Short diagram

```text
Live systems ──health facts──> RaapTech OS ──policy/budget permit──┐
Agentic Brain ─curated context─> Hermes ──Kyle approval reference──┤
Project Co-Pilot ─approved spec (optional one-way contract)────────┤
                                                                  v
Git/GitHub <──branch + draft PR── Codex Project Factory ──recipe──> Archon
   ^                                │ durable projection             │
   │ source authority               v                                │
   └──────────────────────────── Convex <── Codex app-server execution

Docker VM hosts approved services; hosting does not confer policy or knowledge authority.
```

## One-owner matrix

| Concern | Primary owner | Factory classification | Interface / non-owner boundary |
|---|---|---|---|
| intake / prioritization | Hermes + Kyle | INTEGRATE | Hermes captures intent/approval; Factory receives one approved bounded goal. Disable generic autonomous research intake for first pilot. |
| workflow routing | Codex Project Factory | REUSE | Factory instantiates the approved project-delivery recipe; Hermes routes fleet/operator work, not internal workflow nodes. |
| work-item and run state | Codex Project Factory | REUSE | Convex is the durable projection for Factory goals/runs only (`schema.ts:24-36`). |
| thread/session state | Codex app-server (conversation truth); Factory (references/projection) | INTEGRATE | Codex owns transcript/execution context; Factory stores IDs/status, never duplicate transcript storage. |
| worktree lifecycle | Codex Project Factory | REUSE | Factory creates named run worktrees; must add cleanup/retention. Git remains repository authority. |
| agent execution | Codex app-server | INTEGRATE | Factory dispatches bounded turns; Hermes/Atlas remain separate fleet workers. |
| deterministic validation | Target Git repository | INTEGRATE | Repo declares canonical command; Factory invokes and records it. Factory must not invent a weaker check. |
| evaluator/reviewer flow | Codex Project Factory | REUSE | Factory creates fresh verification/review threads; reviewer cannot merge/deploy. |
| approval records | Hermes + Kyle | INTEGRATE | Factory stores an immutable approval reference/key, not operator identity or policy authority. |
| cost budgets and enforcement | RaapTech OS | INTEGRATE | RaapTech OS grants a pre-dispatch ceiling; Factory records measured cost. `costUsd` storage alone is not enforcement. |
| audit/DLP/kill switches | RaapTech OS | KEEP SEPARATE | Factory exposes run/event/cancel interfaces; policy remains outside delivery execution. |
| secrets references | Approved credential store | INTEGRATE | Services receive references at runtime. Factory, Git, logs, and Agentic Brain never hold values. |
| notifications / operator experience | Hermes | INTEGRATE | Factory emits status/artifact events; Hermes presents them and asks for decisions. Dashboard is optional/read-only. |
| fleet health | Live systems + RaapTech OS | KEEP SEPARATE | Factory cannot assert host/service liveness from stored state. |
| knowledge evidence capture | Codex Project Factory | REUSE | Factory captures run-scoped artifacts/evidence only. |
| knowledge promotion | Agentic Brain controlled promotion | KEEP SEPARATE | Factory may propose a candidate learning; it cannot mutate canonical vault truth. |
| artifact retention | Codex Project Factory | REUSE | Factory owns run artifact index and retention contract; GitHub owns PR objects; backup system protects exported state. |
| backup / restore | Proxmox/PBS/TrueNAS backup plane | INTEGRATE | Factory defines consistency/export requirements; infrastructure performs and proves backup/restore. TrueNAS remains storage-only. |
| service deployment and lifecycle | Docker VM operations / RaapTech OS | KEEP SEPARATE | Versioned Compose/systemd plus operator change control; Factory cannot deploy itself. |

## System boundary decisions

### Hermes — INTEGRATE

- Owns conversation, Kyle approvals, notifications, exceptions, and operator surface.
- Sends a narrow approved goal/reference to Factory and receives status/evidence back.
- Does **not** store or replay Factory's run state and does not execute Factory workflow nodes.

### RaapTech OS — INTEGRATE / KEEP SEPARATE

- Owns policy, cost authorization, audit/DLP, kill switches, and fleet health.
- Provides allow/deny and ceilings before dispatch; can request cancellation.
- Must not become another implementation thread runner.

### Archon — INTEGRATE

- Owns reusable recipe format/mechanics where adopted.
- Factory consumes a pinned recipe and owns run instantiation/state.
- Current `.archon/*.yaml` files are local recipe declarations; naming does not prove a separate Archon runtime deployment.

### Project Co-Pilot — KEEP SEPARATE / UNKNOWN adapter

- Remains the guarded planning/specification product.
- Optional future interface: immutable approved spec + acceptance criteria into Factory.
- No shared database, bidirectional sync, or absorption without a separate ADR.

### Agentic Brain — KEEP SEPARATE

- Owns curated human-readable operational context after verification.
- Factory output enters only as candidate evidence through capture → verify → review → promote.
- Factory never writes the canonical vault during a run.

### Git / GitHub — INTEGRATE

- Git is source/reproducible-config authority; GitHub is remote branch/PR authority.
- Factory may create a run branch, validated commit, push, and draft PR.
- Human owns merge, release, and deployment.

### Docker VM — KEEP SEPARATE

- Hosts the service under an approved, versioned deployment contract.
- Does not become workflow policy, project state, or knowledge authority merely because it runs containers.

## Overlap classification and controls

| Overlap | Classification | Control |
|---|---|---|
| Factory idea research vs Hermes/Agentic Brain research intake | CONFLICT for pilot | Disable `research` commands; pilot starts from Kyle-approved internal work item. |
| Factory goal approval vs Hermes approval | INTEGRATE | Factory stores a reference/idempotency key; Hermes/Kyle remains human approval authority. |
| Factory candidate-goal lifecycle vs Project Co-Pilot planning/specification | CONFLICT until interface exists | Project Co-Pilot owns planning/specification and emits an immutable approved candidate goal plus acceptance criteria; Factory owns only approved-goal-to-run execution. No shared database, bidirectional lifecycle, or absorption without a separate Kyle-approved interface ADR. |
| Factory `costUsd` vs RaapTech OS budgets | CONFLICT if interpreted as enforcement | Treat as telemetry only until RaapTech OS issues and enforces caps. |
| Factory learnings vs Agentic Brain | INTEGRATE | Candidate evidence only; reviewed promotion remains external. |
| Factory workflow recipes vs Archon | INTEGRATE | Archon owns reusable recipe; Factory owns execution record. Avoid a second generic recipe engine. |
| Factory dashboard vs Hermes operator UI | KEEP SEPARATE | Dashboard is read-only diagnostics; Hermes remains operator/notification surface. Omit dashboard in first pilot. |
| Factory command worker vs Hermes/Atlas workers | KEEP SEPARATE | Factory worker processes product-delivery commands only; no fleet jobs or arbitrary mission queue. |
| Factory artifacts vs GitHub PR/source | INTEGRATE | Factory indexes URI/summary; GitHub/Git stores source/diff/PR truth. |

## Consistency result

Every required concern has one named primary authority. The architecture remains coherent only if autonomous research is disabled for the pilot, cost fields are not treated as enforcement, Factory cannot write the canonical vault, and deployment/merge remain external human-controlled operations.
