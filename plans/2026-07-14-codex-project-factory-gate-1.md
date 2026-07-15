---
type: Specification
title: Codex Project Factory Gate 1 Plan
description: Gate-1 execution plan for the Codex project factory.
tags: [okf, auto-frontmatter]
timestamp: 2026-07-15T13:55:19Z
---

# Codex Project Factory — Gate 1 Hardening Plan

> **For Hermes:** execute with Codex CLI in a clean isolated worktree. Each task is review-gated: deterministic tests first, then spec review, then standards review. No DVM service deployment, credential import, customer repository access, merge, or production mutation belongs to Gate 1.

**Goal:** Make `RaapTechllc/codex-project-factory` a reproducible, CI-enforced, singleton-safe, self-diagnosing Factory repository ready for a separately approved DVM service-plane proof.

**Baseline:** `master` at `7fbb782299c2100f8a14353631ae8fb43529e7ec`.

**Operating boundary:** Hermes owns approvals and stop gates. Codex CLI is an implementation worker. GitHub owns source/PR authority. The Factory remains the subject under construction—not the authority to merge, deploy, access customer repos, or expand scope.

**Excluded from Gate 1:** self-hosted Convex deployment, Codex/GitHub credentials on DVM, public dashboard, real target-repository write, live draft-PR dispatch, and any customer or production data.

---

## Acceptance gates

A Gate 1 PR is review-ready only when all of the following are command-backed:

1. `npm ci && npm run validate` from a clean checkout.
2. Root GitHub Actions runs the same validation contract on Node 22 and has a timeout.
3. Docker build/Compose configuration validates without secrets or a running live backend.
4. A structured, non-mutating preflight returns PASS/FAIL for required local configuration, repository state, worktree root safety, disk threshold, and optional dependency readiness.
5. Live Codex app-server contract test is opt-in and skips cleanly without a local authenticated Codex runtime; it proves initialize/close when explicitly enabled.
6. Worker cannot claim/process more than one execution command at a time in pilot mode.
7. Worktree and artifact retention/cleanup are explicit, bounded, dry-run capable, and covered by tests.
8. No service listens publicly; no secret values appear in source, fixtures, test output, images, or CI logs.

---

## Task 1 — Establish root CI and deterministic npm contract

**Files:**
- Create: `.github/workflows/ci.yml`
- Modify: `package.json`, `.gitignore`, `README.md`
- Test: repository validation command or focused CI/manifest contract tests

**Requirements:**
- npm is the only supported package manager; use the root `package-lock.json`.
- CI uses Node 22 with `npm ci`, runs `npm run validate`, has least-privilege read-only permissions and a bounded timeout.
- Document the one canonical local validation command.
- Ensure generated outputs, `.factory/`, worktrees, and environment files are ignored; do not delete user files.

**Verify:**
```bash
npm ci
npm run validate
```

---

## Task 2 — Add a non-root, private-by-default service contract

**Files:**
- Create: `Dockerfile`, `docker-compose.yml`, `.dockerignore`, `.env.example`
- Modify: `README.md`
- Test: structural manifest contract test

**Requirements:**
- Pin Node 22 image family; build only the bridge worker needed for first pilot.
- Create explicit non-root UID/GID.
- Compose has no `ports`, uses an internal network, read-only filesystem where compatible, bounded writable tmpfs/volumes, CPU/memory/PID limits, restart policy, and named documented volumes.
- `.env.example` contains names/placeholders only: `CONVEX_URL`, `FACTORY_PROJECTS_ROOT`, optional `FACTORY_ARTIFACTS_ROOT`, retention/threshold controls. No values or tokens.
- It must not claim a deployed Convex topology; that is Gate 2.

**Verify:**
```bash
docker build -t codex-project-factory:contract .
docker compose config
```

---

## Task 3 — Implement a structured no-write preflight / health contract

**Files:**
- Create: `apps/codex-bridge/src/preflight.ts`
- Modify: `apps/codex-bridge/src/index.ts` or CLI entrypoint, package scripts, README
- Test: `apps/codex-bridge/src/*.test.ts`

**Requirements:**
- `factory-preflight --no-write` emits machine-readable JSON with version/revision and PASS/FAIL checks.
- Checks must not write to a project or make GitHub mutations.
- Validate: required env names are present (values never printed); target/worktree roots resolve under declared allowed roots; source checkout is a Git worktree; disk floor; `git` present; optional `gh`, Codex, Convex reachability reported as explicit readiness states.
- Return non-zero on a required failed check; redact all values.
- Make the implementation dependency-injectable so tests do not need actual Codex/GitHub/Convex services.

**Verify:**
```bash
npm test --workspace @factory/codex-bridge
npm run bridge:preflight -- --no-write
```

---

## Task 4 — Add opt-in live Codex app-server protocol contract test

**Files:**
- Create/modify: `apps/codex-bridge/src/json-rpc.live.test.ts`, JSON-RPC test helpers, README

**Requirements:**
- Default CI/unit test suite never requires Codex credentials.
- When `FACTORY_LIVE_CODEX_CONTRACT=1`, start `codex app-server --stdio`, issue only the minimum safe initialize/close protocol exchange, enforce a short timeout, and cleanly terminate the child process.
- No target repository task, code generation, or external mutation.
- Fail with a clear diagnostic when the live flag is set and Codex is unavailable/unauthed.

**Verify:**
```bash
npm test --workspace @factory/codex-bridge
FACTORY_LIVE_CODEX_CONTRACT=1 npm test --workspace @factory/codex-bridge -- --run json-rpc.live
```

---

## Task 5 — Enforce singleton command processing and safe lease ownership

**Files:**
- Modify: `apps/codex-bridge/src/worker.ts`, `convex/commands.ts`, workflow types if needed
- Test: worker/command behavior tests

**Requirements:**
- Pilot default is exactly one active execution command. `cycle()` must not launch a second command while a prior command is active.
- Interrupt commands may be handled only in a way that cannot start a second milestone run; document the behavior.
- Event attribution is deterministic for the one active run.
- Claim/heartbeat/finish must retain worker ownership semantics; no change may allow another worker to finish a command it did not own.
- The YAML `max_parallel_implementers` field must either be rejected/not-supported with clear validation or be enforced. Do not retain a misleading unenforced value.

**Verify:**
```bash
npm test --workspace @factory/codex-bridge
```

---

## Task 6 — Add bounded retention and cleanup controls

**Files:**
- Create: `apps/codex-bridge/src/retention.ts`
- Modify: bridge CLI, `workflow.ts`, README, `.env.example`
- Test: retention tests using temporary directories/repositories

**Requirements:**
- Explicit roots only; reject paths outside configured Factory roots.
- `factory-retain --dry-run` reports candidate worktrees/artifacts by age and size without mutation.
- Actual cleanup requires an explicit confirmation flag, refuses active run/worktree paths, uses Git worktree-aware removal/prune, and records structured evidence.
- Default retention/size limits are conservative and configurable via names-only environment variables.
- No deletion is exercised against non-test paths in CI.

**Verify:**
```bash
npm test --workspace @factory/codex-bridge
factory-retain --dry-run
```

---

## Task 7 — Add deployment-contract tests and close documentation drift

**Files:**
- Create: manifest/preflight/retention contract tests
- Modify: `README.md`, `.archon/workflows/milestone-to-pr.yaml`

**Requirements:**
- Tests parse Compose/Dockerfile/CI definitions and assert non-root, no published port, internal network, resource limits, canonical Node/npm versions, CI validation, and no secret values.
- Reconcile workflow contract vocabulary and remove or enforce misleading parallelism metadata.
- State exactly what remains Gate 2: pinned self-hosted Convex compatibility, DVM credentials, backup/restore, private service runtime, restart/cancellation proof, and single real internal draft-PR proof.

**Verify:**
```bash
npm run validate
docker compose config
```

---

## Required review package

For each Codex implementation commit:

1. command output for focused tests and full `npm run validate`;
2. CI run URL and final check state;
3. two independent reviews: spec compliance first, standards second;
4. diff/stat and secret-pattern scan;
5. draft PR only; no merge until Kyle approval.

## Gate 2 entry criteria (not authorization)

Gate 2 begins only after Gate 1 merges and Kyle separately approves an isolated DVM change window plus:

- self-hosted Convex topology/image compatibility decision;
- approved DVM credential references for dedicated Codex/GitHub service identity;
- documented persistent volumes, backup destination, and isolated restore proof;
- one internal synthetic target repository and hard time/token/spend ceiling;
- dashboard omitted unless explicitly approved for authenticated Tailscale-only access.
