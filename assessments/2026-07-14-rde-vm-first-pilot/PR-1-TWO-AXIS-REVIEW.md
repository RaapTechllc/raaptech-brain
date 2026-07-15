---
type: Reference
title: RDE Pilot PR-1 Two-Axis Review
description: Standards and spec review receipt for RDE VM-first pilot.
tags: [okf, auto-frontmatter]
timestamp: 2026-07-15T13:55:19Z
---

# PR #1 Two-Axis Review — RDE VM-First Contract

**PR:** https://github.com/RaapTechllc/raaptech-rde/pull/1  
**Reviewed revision:** `4000bbb36231487a42d9149383fe93ee8c149a27`  
**Base:** `4df2bc33062aea3f6d784716e5a27bf93ada53c6`  
**CI at reviewed revision:** `fixture-contract` SUCCESS, Actions run `29356273474`

## Specification compliance

**PASS.** The stated pilot requirements are implemented and proven:

- pinned Python 3.11 slim runtime;
- explicit non-root RDE user;
- finite Compose job and no published ports;
- private internal network in Compose and `--network none` in the real pilot;
- read-only root, bounded tmpfs, CPU/memory/PID limits;
- evidence-only output and exact five-artifact acceptance test;
- deterministic pytest, image build, isolated execution, and acceptance in CI;
- no runtime secrets or customer data.

## Standards / code quality

**MERGE HOLD — one material operational defect.**

`docker-compose.yml` mounts `${RDE_EVIDENCE_DIR:-./out-container}` directly into `/evidence` while running the job as UID/GID `10001`. On a fresh Docker host, Docker may create the default bind-source directory as root-owned. The non-root job then cannot write its artifacts. The successful DVM proof deliberately used an initialized Docker volume rather than this Compose bind path, so it proves the container contract but not the default Compose invocation.

**Required correction before merge:** make the standard Compose invocation deterministic by either:

1. shipping an explicit preflight/deploy script that creates `RDE_EVIDENCE_DIR` with UID/GID `10001` and restrictive permissions before Compose runs; or
2. replacing the default bind mount with a named initialized volume and adding a documented/exported evidence path; or
3. running a narrowly scoped, documented one-time init step that owns only the RDE evidence directory.

Then run the exact `docker compose` job on DVM using the documented command, record the artifact receipt, and clean up.

## Findings that do not block merge

- The CI root-capable Alpine `chown` helper initializes a disposable Docker volume. It does **not** make the RDE workload root; the workload itself runs as `10001:10001`. This is acceptable for a scoped volume-init operation, though it should be documented.
- Adding a BuildKit cache is an optimization, not a correctness/security or reproducibility gate. Do not add registry/cache complexity until CI duration justifies it.
- CI repeats runtime limits rather than invoking Compose because it validates an equivalent lower-level Docker command. This is acceptable but should eventually share a single tested runner/preflight script to avoid drift.
- Test overlap is minor; both current tests protect distinct seams: emitted artifact shape and persisted response integrity.

## Decision

**Do not merge PR #1 yet.** Fix the default Compose evidence-directory ownership/preflight and prove that documented Compose path on the DVM. The completed direct-Docker pilot remains valid evidence of container isolation and artifact correctness; it is not a proof that the Compose contract is turnkey.
