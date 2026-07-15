---
type: Reference
title: 02 CODEX PROJECT FACTORY DEPLOYMENT READINESS
description: "Assessment note: 02-CODEX-PROJECT-FACTORY-DEPLOYMENT-READINESS."

tags: [okf, auto-frontmatter]
timestamp: 2026-07-15T13:55:19Z
---

# Codex Project Factory — Deployment Readiness

**Date:** 2026-07-14  
**Decision:** `BLOCKED WITH PREREQUISITES`  
**Scope:** Phase A source evidence only; no deployment occurred.

## Readiness matrix

| Requirement | Status | Evidence / current truth | Proof required before pilot |
|---|---|---|---|
| Docker VM designated as Linux workflow plane | DEMONSTRATED | `Infrastructure-Post-Repair-Verification-2026-07-14.md:14-17`; fleet audit `:43,56` | Recheck live immediately before change window |
| Docker VM current capacity/headroom | ASSUMED | Historical audit reports Ubuntu 24.04, 46 GiB RAM, 122 GiB free (`fleet-workflow-audit.md:26,43`) | Live `free`, `df`, `docker system df`, load, service inventory |
| Factory repository health | DEMONSTRATED | Clean `master` at `7fbb782...`; `npm run validate` passed lint, typecheck, 25 tests, five builds | Repeat on Docker VM at the pinned revision |
| Node runtime | CONFIGURABLE | Factory declares Node `>=22` (`package.json:28-30`) | `node --version`; pin exact supported major/minor |
| npm runtime | CONFIGURABLE | Factory declares `npm@11.11.0` (`package.json:5`) | `npm --version`; use `npm ci` |
| Deterministic package-manager root / lockfile strategy | BLOCKED | Next.js build succeeded but inferred `C:\Users\Kyle\pnpm-lock.yaml` as the workspace root while also detecting the Factory `package-lock.json` | Normalize to one package-manager/lockfile strategy and explicitly set Next.js `outputFileTracingRoot`; prove a clean build from an isolated Docker context |
| Codex CLI / app-server | BLOCKED | Bridge spawns `codex app-server --stdio` (`json-rpc.ts:30-43`); gateway tests use a fake transport and do not launch the real app-server; only Maxx login was demonstrated | Dedicated VM service account; `codex --version`, non-secret auth status, and live initialize/thread/turn/interrupt protocol contract smoke |
| Git and Git worktree | CONFIGURABLE | Workflow invokes `git worktree add` (`workflow.ts:162-171`) | Git version, writable target roots, clean scratch worktree add/remove test |
| GitHub CLI and authorization | BLOCKED | Workflow invokes `gh repo view`, push, PR list/create (`workflow.ts:145-159`) | Dedicated least-privilege credential; repo-scoped branch push + draft-PR permission proof |
| Convex control plane | BLOCKED | Factory requires `CONVEX_URL`; README's `npx convex dev` path is a development bootstrap, not an approved durable service contract, and no Factory deployment manifest exists | Select self-hosted topology; start pinned backend; push schema/functions; query health |
| Convex local-only persistence | CONFIGURABLE | Official Convex self-host guide supports backend/dashboard/frontend and persistent SQLite via Docker volume; the repository's local-development path does not define production persistence, backup, or restore | Pin image/digest, persistent volume, local URLs, admin-key reference, export/restore test |
| Convex/client compatibility | BLOCKED | Factory pins `convex ^1.25.0`; self-host guide says latest CLI | Test exact client against exact backend; record compatibility |
| Factory container/service definition | BLOCKED | No Factory Dockerfile, Compose, devcontainer, systemd unit, or active top-level CI workflow; the only CI workflow is nested in the generated-project template | Versioned service definition with non-root UID, restart policy, resources, health check |
| Required environment names | DEMONSTRATED | Source-only scan: `CONVEX_URL`, `FACTORY_PROJECTS_ROOT`, `NEXT_PUBLIC_CONVEX_URL` | Supply references only; dashboard variable omitted if dashboard omitted |
| Secrets storage | BLOCKED | No source secret values; no deployment secret-reference contract | Approved credential store/file permissions; never bake keys into image, repo, logs, or vault |
| Ports and bind addresses | BLOCKED | Factory defines none; official self-hosted Convex defaults: 3210 backend, 3211 actions, 6791 dashboard | Loopback/container-network binding; no WAN/NAT; Tailscale-only operator access if UI enabled |
| Reverse proxy | NOT REQUIRED FOR PILOT | Dashboard can be omitted; bridge/CLI can use internal Convex URL | If UI enabled later, authenticated Tailscale-only proxy |
| Factory health/readiness | BLOCKED | No endpoint or health command exists | Script checks process, Convex query, Codex initialize, Git/GH read-only access, disk thresholds |
| Logging and audit evidence | CONFIGURABLE | Worker stderr plus Convex events/artifacts exist (`worker.ts:38-44,86-90`; schema `:50-77`) | Structured service logs, run ID correlation, rotation, redaction, retained proof bundle |
| Process supervision/restart | BLOCKED | Worker is an infinite one-second poll loop (`worker.ts:138-163`); no supervisor config | Docker/systemd restart test; interrupt/restart/reconcile test |
| Command leases/retry | DEMONSTRATED | Claim/heartbeat/four-hour lease (`commands.ts:13-25`; `worker.ts:47-95`) | Pilot one command; kill/restart without duplicate PR |
| Concurrency safety | BLOCKED | Events are assigned only when exactly one run is active (`worker.ts:42-44`). Recipe metadata declares `max_parallel_implementers: 2`, but the executor is sequential and does not enforce the field (`milestone-to-pr.yaml:3-5`; `workflow.ts:66-80`) | Enforce concurrency=1 outside recipe metadata for pilot; later implement explicit run correlation and tested concurrency controls |
| Cancellation | CONFIGURABLE | Cancellation queues interrupts and marks run cancelled (`runs.ts:13-20`) | Live dummy cancellation proves turn interruption and terminal state |
| Repair cap | DEMONSTRATED | Maximum three repairs (`milestone-to-pr.yaml:3-5`; `workflow.ts:100-113`) | Verify failed check reaches blocked state after cap |
| Worktree retention/cleanup | BLOCKED | Creation is implemented; automatic cleanup is absent | Retention policy, disk quota/alert, explicit `git worktree remove/prune`, stale branch procedure |
| Artifact/event retention | BLOCKED | Tables have timestamps but no TTL/deletion policy (`schema.ts:50-77`) | Retention duration, export path, deletion/redaction procedure |
| Backup of Convex state | BLOCKED | Official default is SQLite in Docker volume; no RaapTech backup job exists | Snapshot/export volume into protected backup path and record successful job |
| Restore of Convex state | BLOCKED | General VM/PBS restore is proven, not Factory logical state | Isolated restore; start backend; query known run/thread/artifact; destroy scratch restore |
| Upgrade/migration path | BLOCKED | No pinned image or tested schema/backend upgrade | Document pin, backup-first upgrade, rollback image, compatibility test |
| CPU/RAM/disk controls | BLOCKED | No resource limits or worktree capacity limit | Compose limits/reservations; thresholds; stop gate |
| Local GPU/Ollama | NOT REQUIRED FOR PILOT | Factory uses Codex app-server; infrastructure explicitly forbids depending on CT 201 | None |
| Windows VM/QGA | NOT REQUIRED FOR PILOT | Pilot is Linux and internal code only | None |
| Dummy/internal data only | CONFIGURABLE | Workflow is repository-scoped and draft-PR-only | Select internal low-risk repo; synthetic fixture; deny customer/canonical-vault paths |
| Rollback/retirement | CONFIGURABLE | Services can be isolated; no deployed state exists yet | Tested stop/export/remove sequence below |

## Minimum supported topology

```text
Kyle approval in Hermes
        │ one-way approved goal reference
        v
Docker VM private service network
  ├─ Factory bridge worker (Node >=22, npm, Codex CLI, git, gh)
  ├─ self-hosted Convex backend (persistent SQLite volume for pilot)
  └─ optional web dashboard — OMIT in first pilot
        │
        ├─ target internal Git repo in managed worktree root
        └─ GitHub outbound HTTPS for branch push + draft PR only
```

The Factory bridge and Convex backend bind only to loopback/private Docker networking. No WAN publication, router change, or public reverse proxy is permitted. Operator access, if later required, is Tailscale-only and authenticated. Outbound access is limited to Codex/OpenAI authentication, npm installation during controlled build, and GitHub operations required by the approved repository.

## Required-but-unknown inputs

- Exact Docker VM OS/package state, capacity, and current container ownership at pilot time.
- Exact Codex CLI version and app-server protocol version supported on Linux.
- Dedicated service account and approved Codex/GitHub credential references.
- Exact self-hosted Convex backend image/digest compatible with Factory's client.
- Persistent volume path, backup target, retention, export, and restore commands.
- Approved internal target repository and deterministic validation command.
- Pilot time/token/spend ceiling and stop owner.

## Phase A preflight command list

Run read-only first; installation/deployment requires a later approved change session.

```bash
uname -a
cat /etc/os-release
free -h
df -h
docker version
docker compose version
docker system df
node --version
npm --version
codex --version
codex login status
git --version
gh --version
gh auth status
git ls-remote --exit-code <approved-internal-repo-url> HEAD
```

After an approved isolated checkout, but before dispatch:

```bash
npm ci
npm run validate
git status --porcelain
git branch --show-current
npx convex --version
# query Factory health contract once implemented
factory-preflight --no-write --repo <approved-internal-repo>
```

No command should print token values. Authentication commands must report status only.

## Health-check contract

A pilot is healthy only when one command returns structured PASS/FAIL for:

1. Factory process alive and revision/version reported.
2. Convex backend reachable; schema/functions revision matches Factory.
3. A read-only Convex query succeeds.
4. Codex app-server initializes and closes cleanly under the service account.
5. Approved target repository exists, is clean, has expected origin/default branch, and permits a disposable worktree in a designated root.
6. GitHub identity is known and has only the required repository scope.
7. Worktree/artifact/Convex volumes have at least the approved free-space threshold.
8. No listener is bound to `0.0.0.0` unless explicitly approved; no WAN exposure exists.
9. Last backup and last isolated restore evidence are within the accepted freshness window.
10. No active run exists before a singleton pilot dispatch.

Process-alive alone is not healthy.

## Backup and restore gate

Before promotion beyond a disposable proof:

- persist Convex SQLite and Factory local state (`.factory/thread-idempotency.json`, artifact root, worktree metadata where needed) on named, documented volumes;
- stop or quiesce writes before snapshot/export;
- back up to the existing protected infrastructure chain without making TrueNAS a worker;
- restore into an isolated scratch location with networking constrained;
- start the restored Convex backend and read back a known project, run, thread reference, artifact, and workflow-node state;
- record version, timestamps, checksums/IDs, and cleanup evidence.

The existing PBS/VM restore proof establishes infrastructure recovery capability, **not** Factory application recovery.

## Rollback / retirement

1. Cancel or block new dispatch; wait for/interrupt the singleton run.
2. Preserve the final run ledger, validation evidence, and draft-PR URL; do not merge.
3. Stop Factory bridge and optional UI, then Convex after a final export/snapshot.
4. Revoke the dedicated Codex/GitHub credentials.
5. Remove managed worktrees with `git worktree remove` and `git worktree prune`; delete only Factory-created branches after Kyle approval.
6. Remove service definitions and containers; retain the final encrypted backup until retention expires.
7. Verify no listeners, scheduled jobs, containers, orphan worktrees, or credential references remain.
8. Mark the pilot retired in Hermes/Agentic Brain through the normal reviewed promotion path.

## Phase distinction

- **Phase A source evidence (complete):** code inspection, repository validation, source-only environment scan, architecture/ownership analysis, and official self-hosting feasibility.
- **Phase B live deployment proof (not started):** Docker VM prerequisites, pinned topology, service installation, health checks, backup/restore, cancellation/restart, and one internal draft-PR proof run.

No Phase A claim should be read as Phase B proof.
