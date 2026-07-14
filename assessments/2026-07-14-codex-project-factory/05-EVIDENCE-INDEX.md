# Codex Project Factory — Evidence Index

**Assessment timestamp:** 2026-07-14  
**Repository revision:** `7fbb782299c2100f8a14353631ae8fb43529e7ec`  
**Precedence:** live/repository evidence → post-repair report → current handoff → curated Agentic Brain → historical audit/research.

## Repository identity and validation

| Claim | Source type | Exact source | Line / command | Timestamp | Confidence |
|---|---|---|---|---|---|
| Inspected the intended private repository | Git command | `C:\Users\Kyle\AppData\Local\Temp\codex-project-factory-inspection-2026-07-14` | `git remote get-url origin` → `https://github.com/RaapTechllc/codex-project-factory.git` | 2026-07-14 | High |
| Default/active branch is `master` | Git/GitHub command | same clone | `git branch --show-current`; `gh repo view ...defaultBranchRef` | 2026-07-14 | High |
| Inspected revision | Git command | same clone | `git rev-parse HEAD` → `7fbb782299c2100f8a14353631ae8fb43529e7ec` | 2026-07-14 | High |
| Inspection tree remained clean | Git command | same clone | `git status --porcelain` before/after validation → empty | 2026-07-14 | High |
| Full validation passed | Executed command | same clone | `npm run validate`: lint/typecheck/test/build; 25 tests; five package builds. A second explicit `npm run lint && npm run typecheck && npm test && npm run build` also exited 0 and left `master...origin/master` clean. | 2026-07-14 | High |
| Successful Next.js build exposed package-root ambiguity | Executed command | same clone | Build warned that Next.js inferred `C:\Users\Kyle\pnpm-lock.yaml` as workspace root while also detecting the Factory `package-lock.json`; correctness passed, deployment reproducibility is not normalized | 2026-07-14 | High |
| First standalone test attempt was malformed, not a product failure | Executed command | same clone | `npm test -- --run` rejected Turbo argument; canonical `npm test` inside validate passed | 2026-07-14 | High |
| Dependency audit reported two moderate vulnerabilities | Executed command | same clone | `npm install --ignore-scripts` audit summary | 2026-07-14 | Medium; package audit details not expanded |

## Code and runtime truth

| Claim | Source type | Exact source | Line / section | Timestamp | Confidence |
|---|---|---|---|---|---|
| Factory is a project-delivery control plane, with Codex owning execution context and Convex projections | Repository docs/code | `README.md` | `1-29` | revision above | High |
| Node `>=22`, npm `11.11.0`, workspaces, and canonical validate command | Manifest | `package.json` | `5-19,28-30` | revision above | High |
| Convex stores projects, ideas, goals, runs, thread/turn refs, artifacts, events, commands, nodes, learnings | Schema | `convex/schema.ts` | `9-78` | revision above | High |
| Thread and session IDs are distinct | Schema/types | `convex/schema.ts`; `apps/codex-bridge/src/types.ts` | `38-48`; `18-26,54-58` | revision above | High |
| Goal/run dispatch is idempotent and approval-gated | Code | `convex/goals.ts`; `convex/runs.ts` | `5-12`; `4-11` | revision above | High |
| Commands use claim, heartbeat, lease, and completion | Code | `convex/commands.ts`; `worker.ts` | `13-25`; `47-95` | revision above | High |
| Worker spawns external `codex app-server` via JSON-RPC stdio | Code | `apps/codex-bridge/src/json-rpc.ts` | `30-43` | revision above | High |
| Root creation has restart-oriented local idempotency store | Code | `apps/codex-bridge/src/idempotency.ts`; `worker.ts` | `25-62`; `38-40` | revision above | High |
| Workflow uses fresh role-specific threads and deterministic bash node | Recipe/code | `.archon/workflows/milestone-to-pr.yaml`; `workflow.ts` | `7-43`; `80-113` | revision above | High |
| Repair is capped at three cycles | Recipe/code | same | YAML `3-5`; TS `100-113` | revision above | High |
| Declared implementer parallelism is not enforced | Recipe/code mismatch | `.archon/workflows/milestone-to-pr.yaml`; `apps/codex-bridge/src/workflow.ts` | YAML `3-5` declares `max_parallel_implementers: 2`; executor `66-80` is sequential and does not consume the field | revision above | High |
| README's app-server contract-test instruction is not backed by a live contract test | Documentation/test-code mismatch | `README.md`; `apps/codex-bridge/src/gateway.test.ts` | README `44`; gateway tests instantiate `FakeTransport` and never launch real `codex app-server` | revision above | High |
| README references Convex MCP integration, but no implementation was found | Documentation/negative source search | `README.md`; entire source clone excluding generated/vendor output | README `60-62`; no MCP client/server/config integration found | revision above | Medium-high; absence is scoped to inspected source |
| Factory itself has no active repository CI workflow | File inventory | entire clone | only workflow found is nested under `packages/project-template/template/.github/workflows/ci.yml` for generated projects | revision above | High |
| Factory creates managed worktree/branch | Code | `apps/codex-bridge/src/workflow.ts` | `162-171` | revision above | High |
| Delivery refuses protected branch, sensitive paths, validation drift, and creates draft PR only | Code/tests | `workflow.ts`; `workflow.test.ts` | `116-180`; tests `48-135` | revision above | High |
| Dashboard is minimal/read-only view of run/thread projections | Code | `apps/web/app/page.tsx` | `9-27` | revision above | High |
| Cost is recorded but not enforced | Schema/code | `convex/schema.ts`; `convex/runs.ts` | `31-36`; `15-20` | revision above | High |
| Worktree creation exists; cleanup/TTL is absent from inspected source | Negative repository search | entire clone excluding generated/vendor dirs | searched worktree/cleanup/retention surfaces | 2026-07-14 | Medium-high |
| No Factory Dockerfile, Compose, devcontainer, or GitHub CI workflow exists | File inventory | entire clone | filename searches and 76-file source inventory | 2026-07-14 | High |
| Environment names only are `CONVEX_URL`, `FACTORY_PROJECTS_ROOT`, `NEXT_PUBLIC_CONVEX_URL` | Source-only regex scan | apps source | `cli/index.ts:50`; `worker.ts:15,75`; `web/app/providers.tsx:6` | 2026-07-14 | High |
| No secret values were inspected | Method constraint | assessment procedure | source-only env-name scan; generated/vendor and secret files excluded | 2026-07-14 | High |
| Concurrent event attribution is ambiguous unless one run is active | Code | `apps/codex-bridge/src/worker.ts` | `34-44` | revision above | High |
| Contract run-phase vocabulary differs from Convex schema | Code | `packages/contracts/src/schemas.ts`; `convex/schema.ts` | contracts `59-70`; schema `4-7` | revision above | High |

## Authority and system fit

| Claim | Source type | Exact source | Line / section | Timestamp | Confidence |
|---|---|---|---|---|---|
| Code/agents/humans doctrine and draft-PR-only boundary are adopted | Current handoff | `C:\Users\Kyle\AppData\Local\Temp\raaptech-handoff-2026-07-14.md` | `18-39` | 2026-07-14 | High |
| Hermes is operator/approval surface, not durable delivery state machine | Current handoff | same | `75-87` | 2026-07-14 | High |
| Factory candidate owns product goals/runs/thread refs/artifacts/draft-PR delivery | Goal/current handoff | goal `:77-89`; handoff `:75-87` | cited lines | 2026-07-14 | High |
| Agentic Brain is curated operational authority; Git/live systems/credential stores retain their authority | Curated source | `Agentic Brain/vaults.md` | `15-40` | verified 2026-07-13 | High |
| Knowledge promotion is capture → verify → review → promote | Curated source | `vaults.md`; `operating-model.md` | `35-41`; `21-27` | verified 2026-07-13 | High |
| Infrastructure truth precedes workflow design | Curated decision | `Agentic Brain/decisions.md`; `infrastructure-agent-workflows-goal.md` | decisions `5-10`; goal `25-30,113-124` | 2026-07-13 | High |
| Hermes-first fleet model is adopted; stale OpenClaw details are historical | Current runbook + goal precedence | `hermes-fleet-team-runbook.md`; goal document | runbook `5-24`; goal `56-73` | 2026-07-11/14 | Medium-high |
| Research/master-prompt material is not adopted policy | Goal/current handoff/index | goal `47-73`; handoff `89-110`; `_index.md:6-10` | cited | 2026-07-14 | High |

## Infrastructure and deployment

| Claim | Source type | Exact source | Line / section / URL | Timestamp | Confidence |
|---|---|---|---|---|---|
| Docker VM health and lab/WAN safety checks passed post-repair | Live-probe report | `C:\Users\Kyle\Documents\Reference\Infrastructure-Post-Repair-Verification-2026-07-14.md` | `3-18` | 2026-07-14 | High |
| Docker VM is designated durable Linux workflow plane | Curated goal/historical audit | `infrastructure-agent-workflows-goal.md`; fleet audit | goal `84-96,187-199`; audit `36-62` | 2026-07-13/14 | High for role; capacity needs re-probe |
| PBS and NFS backup plus isolated VM restore are proven | Post-repair report / audit | post-repair `7-18`; fleet audit `133-191` | cited | 2026-07-13/14 | High |
| General infrastructure restore does not prove Factory logical restore | Analysis from boundaries | deployment readiness artifact | backup target differs from undeployed Convex/Factory state | 2026-07-14 | High |
| CT 201/GPU and Windows QGA are not pilot dependencies | Goal / post-repair report | goal `91-99`; post-repair `20-29` | cited | 2026-07-14 | High |
| Convex officially supports self-hosting | Primary external docs | `https://docs.convex.dev/self-hosting` | Self Hosting page | fetched 2026-07-14 | High |
| Repository local-development Convex instructions do not define a durable production contract | Repository documentation/negative deployment inventory | `README.md`; entire clone | README local `npx convex dev` setup; no persistence, backup, restore, or service manifest in Factory repo | revision above | High |
| Official self-host topology uses backend, dashboard, and frontend; default backend state is SQLite in Docker volume | Primary upstream repo | `https://github.com/get-convex/convex-backend/blob/main/self-hosted/README.md` | Self-hosting / Docker configuration | fetched 2026-07-14 | High |
| Official default endpoints are backend 3210, actions 3211, dashboard 6791 | Primary upstream repo | same URL | Docker configuration | fetched 2026-07-14 | High |
| Official self-host config uses `CONVEX_SELF_HOSTED_URL` and admin-key reference | Primary upstream repo | same URL | Docker configuration | fetched 2026-07-14 | High; these are backend deployment vars, not Factory source vars |
| Docker VM has not demonstrated Node/Codex/Convex/GH prerequisites for Factory | Absence of Phase B proof | current accepted sources + no deployment | no Factory deployment or live VM prerequisite probe performed | 2026-07-14 | High |

## Decision trace

| Decision statement | Evidence basis | Confidence |
|---|---|---|
| Factory is a strong bounded Product Delivery Factory candidate | Implemented state/identity/workflow/worktree/validation/draft-PR controls plus green validation | High |
| Factory must not become fleet, policy, canonical knowledge, credential, merge, or deployment authority | Accepted authority model and explicit non-responsibilities | High |
| Docker VM pilot is blocked, not rejected | Source is healthy and topology is feasible, but deployment/runtime/persistence/health/backup prerequisites are not proven | High |
| First pilot must be singleton, internal, local-only, dashboard-omitted, and draft-PR-only | Concurrency attribution code, safety doctrine, network boundary, and minimal-risk objective | High |
| Autonomous Factory research should be disabled for first pilot | It overlaps intake/knowledge boundaries and is unnecessary to prove delivery | Medium-high |

## Artifact cross-check

- Decision-bearing artifacts 01 and 02 use exactly `BLOCKED WITH PREREQUISITES`; artifact 04 uses `APPROVE FOR DOCKER VM PILOT` only as the future promotion exit condition.
- All five artifacts assign Factory project-delivery scope only.
- All require self-hosted/local-only Convex proof rather than asserting readiness.
- All set singleton concurrency, three repairs maximum, no merge/deploy/customer/canonical-vault mutation.
- All use the same internal documentation-drift proof milestone.
- Every system/concern in the ownership map has one primary owner.
- No credential value appears in this package.
