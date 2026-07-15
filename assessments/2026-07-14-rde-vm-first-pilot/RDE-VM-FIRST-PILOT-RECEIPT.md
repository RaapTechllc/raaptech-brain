---
type: Reference
title: RDE VM-First Pilot Receipt
description: Evidence receipt for the RDE VM-first pilot.
tags: [okf, auto-frontmatter]
timestamp: 2026-07-15T13:55:19Z
---

# RDE VM-First Isolated Pilot Receipt

**Decision:** PASS — isolated RDE fixture pilot completed and retired cleanly.  
**Date:** 2026-07-14  
**Pilot scope:** deterministic repository fixture only; no customer data, no runtime secrets, no published service, and no change to an existing DVM stack.

## Source and CI evidence

| Item | Verified value |
|---|---|
| Canonical remote | `https://github.com/RaapTechllc/raaptech-rde.git` |
| PR | [#1 — VM-first RDE fixture contract](https://github.com/RaapTechllc/raaptech-rde/pull/1) — **open**, not merged |
| Pinned pilot revision | `4000bbb36231487a42d9149383fe93ee8c149a27` |
| CI workflow | `RDE VM-first contract` → `fixture-contract` **SUCCESS** |
| Successful Actions run | `29356273474` / job `87164612108` |
| CI evidence | pytest, non-root Docker build, isolated no-network fixture job, and artifact-contract check all passed |

## Contract implemented on the PR branch

- Python `3.11.11-slim-bookworm` image.
- Explicit non-root `rde` user/group, UID/GID `10001`.
- Finite job with `restart: "no"`; no published ports.
- Compose internal-only network; direct pilot command used `--network none`.
- Read-only root filesystem; `/tmp` is a bounded tmpfs.
- Limits: `0.50` CPU, `512 MiB` memory, 64 PIDs.
- Evidence is isolated in a temporary Docker volume, copied to the durable evidence directory, then the volume is deleted.
- `.env.example` contains names/comments only; the pilot required no secret values.
- Tests lock the exact artifact set and accepted ROI result (`2.291x`, approved).

## DVM proof

| Gate | Result |
|---|---|
| DVM preflight | PASS — Docker 29.1.5, Compose v5.0.2, 121 GiB root free, ~44 GiB RAM available before pilot |
| Pinned detached checkout | PASS — DVM checkout is at `4000bbb36231487a42d9149383fe93ee8c149a27` |
| Repository tests | PASS — `2 passed in 0.02s` |
| Image build | PASS — `raaptech-rde:4000bbb36231` built from the pinned checkout |
| Image identity | `sha256:ab0eb3f9b0d1a9843f5a12a9b587a9445e35bbc7434e4a9bec4c79d2bded9fd9` |
| Job execution | PASS — non-root, read-only, no-network finite container ran fixture successfully |
| Artifact contract | PASS — exactly `deliverable.html`, `data.json`, `sources.json`, `manifest.yaml`, `rde-response.json` |
| Business gate | PASS — ROI `2.291`, `approved_by_roi_gate=true` |
| Existing services | PASS — no existing DVM service/container was stopped, restarted, changed, or credentialed |
| Pilot cleanup | PASS — no RDE container remained, temporary `rde-pilot-*` volume was deleted, and image was removed after evidence capture |

## Pilot evidence locations

**DVM durable evidence directory**

```text
/srv/raaptech/services/rde/evidence/pilot-20260714T181154Z-resume/
  preflight.txt
  pytest.txt
  build.txt
  image.txt
  job-output.json
  acceptance.txt
  postflight.txt
  artifacts/20260714-181202-model-subscription-roi-calculator/
```

`acceptance.txt` records:

```text
DVM_PILOT_ACCEPTANCE_PASS .../artifacts/20260714-181202-model-subscription-roi-calculator
```

The VM retains the **pinned source checkout** at:

```text
/srv/raaptech/services/rde/repo
```

That checkout is source/build evidence only. No service is running from it.

## Deviations and recovered blockers

1. The DVM did not have `pytest`; installed Ubuntu package `python3-pytest` (plus `python3-iniconfig` and `python3-pluggy`) solely to run the approved deterministic preflight. No containers were restarted by package installation.
2. The initial pilot checkout was incomplete because a bundle-transfer attempt did not contain the commit data expected by the clone. The incomplete repository had **no commit**, no source files, no service, and no volume. It was inspected, proven partial, and removed before the successful pilot resumed.
3. The DVM lacks GitHub CLI credentials. The final pilot used a local Git bundle made from the already CI-verified commit; the DVM checkout remote was set to the canonical GitHub URL after clone. No token was stored on the DVM.

## Compose contract proof — final revision

The original direct-Docker proof established container isolation. The final proof below establishes that the **documented Compose path** also works on the DVM.

| Item | Verified value |
|---|---|
| Final PR revision | `4ed8db6dae9c9a1cc2904411d0ab40685ce8b409` |
| Merged main revision | `200fd19df027b832ad16739fe6afce902cfd00fd` — PR #1 merged 2026-07-14T19:54:24Z |
| Green CI | Actions run `29357816372`, `fixture-contract` **SUCCESS** |
| Documented runner | `scripts/run-fixture-compose.sh`, Git mode `100755` / DVM mode `755` |
| Ownership preflight | Runner creates the selected bind-mounted evidence directory as `10001:10001`, mode `0750` |
| Operator access | Runner applies `chmod -R a+rX` only after the finite non-root job completes |
| Final Compose evidence | `/srv/raaptech/services/rde/evidence/compose-final-20260714T182818Z/` |
| DVM repository revision | Exact final PR revision above |
| Tests before Compose run | `2 passed in 0.02s` |
| Artifact validation | **PASS** — exactly the required five artifact files, readable by the DVM operator |
| Business result | `published`; ROI `2.291`; `approved_by_roi_gate=true` |
| Cleanup | no RDE container, Compose network, or RDE image remained after the proof |

The final artifact set is:

```text
data.json
deliverable.html
manifest.yaml
rde-response.json
sources.json
```

The successful final Compose proof supersedes the earlier incomplete Compose attempts. Those attempts created only partial evidence directories; no service, long-lived container, or runtime volume was retained.

## Review status

Two-axis review is complete:

- **Specification compliance:** PASS.
- **Standards hold:** the bind-mounted evidence ownership/readability defect was fixed by the documented Compose runner and the exact Compose flow was proven on the DVM.

The review record is `PR-1-TWO-AXIS-REVIEW.md` in this same assessment directory.

## Operational disposition

- **Pilot contract:** proven, including the exact documented Compose route.
- **PR #1:** open, green, merge-ready. Merge authority remains separate and was not exercised.
- **Production service:** not created.
- **DVM source checkout:** retained solely as pinned source/build evidence; it is not a service.
- **Wave-two decision:** separate approval is required. After merge, RDE should run only as an explicitly requested finite job—not a resident service.
- **Stateful/client systems:** remain blocked until application-level backup/restore and private exposure requirements are proven.
