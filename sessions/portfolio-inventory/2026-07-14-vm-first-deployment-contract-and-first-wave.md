# RaapTech Docker VM-First Deployment Contract and First-Wave Plan

**Status:** proposed standard — no deployment is authorized by this document.  
**Target:** `dockervm` / Proxmox VM 100 / Tailscale `100.97.87.28`  
**Evidence date:** 2026-07-14

## Decision

- **Wave one pilot:** `RaapTechllc/raaptech-rde` only.
- **Wave two candidate:** RaapTech website, only after Kyle makes a hosting/exposure decision and its private-edge contract is implemented.
- **Explicitly excluded:** Codex Project Factory (`BLOCKED WITH PREREQUISITES`); SMW Cloud (client data/Autodesk/Teams and Windows bridge); all trading systems; existing DVM stacks; MiniBench (Postgres state plus non-private published ports); consumer applications.

RDE is the correct proof vehicle: it is a small, stateless Python transform (`request JSON → HTML + data.json + sources.json + manifest.yaml + response JSON`), has a documented CLI and pytest entry point, has no customer data in the pilot fixture, and represents durable consulting-deliverable IP. It is **not deployable today**: it needs a pinned container/service contract and clean validation evidence.

## Non-negotiable operating model

| Plane | Authority | Must not do |
|---|---|---|
| Git/GitHub | Canonical source, branch, revision, PR | Become runtime state or secret storage |
| Docker VM | Durable builds, services, browser state, volumes, logs | Grant policy, approval, knowledge, merge, or deployment authority |
| Hermes | Operator conversation, approval, notification, exception surface | Become a hidden runtime host |
| RaapTech OS | Policy, budget, audit/DLP, kill switch, fleet health | Be replaced by a hosted application |
| RaapTech Brain | Curated verified operational knowledge | Store raw credentials or substitute for source authority |

## Standard deployment contract

Every new or remediated DVM service must meet every row before `docker compose up`.

| # | Required control | Required proof / implementation |
|---:|---|---|
| 1 | **Canonical source** | Repository URL, default branch, immutable commit SHA, deploy timestamp, and operator recorded in evidence bundle. Clone under a canonical VM root such as `/srv/raaptech/services/<name>/repo`; never deploy from an arbitrary home-directory copy. |
| 2 | **Pinned runtime and dependencies** | Docker base image pinned by version (digest preferred), language/runtime version declared, one lockfile and one package manager only. Build must use frozen/locked install (`uv sync --locked`, `npm ci`, or `pnpm --frozen-lockfile`). |
| 3 | **Deterministic preflight and validation** | Read-only preflight checks Git revision, required file names, environment-variable *names*, capacity, port conflict, and secret-file permissions. Then run the repository's deterministic lint/typecheck/test/build or a named equivalent before image build. Missing tools are blocked environment work, not a passing result. |
| 4 | **Versioned container contract** | Repository contains a reviewed Dockerfile and versioned Compose definition. It names services, images, networks, volumes, ports, restart behavior, health checks, limits, and only the exact files required at runtime. No parent-directory lockfiles, workstation paths, or untracked runtime inputs. |
| 5 | **Non-root execution** | Image uses an explicit unprivileged UID/GID. Persistent paths are created with matching ownership. No privileged mode, host networking, Docker socket, broad capability add, or root runtime without a separately approved exception. |
| 6 | **Secrets and configuration** | `.env.example` lists names/placeholders only. Real values stay in approved DVM secret injection with owner-only permissions; they must not enter Git, images, Compose output, logs, evidence, or chat. Document each required variable name, source owner, rotation impact, and whether absent is a safe fail. |
| 7 | **Private networking** | Bind only `127.0.0.1` or the DVM Tailscale address by default. Use internal Compose networks for databases and workers. No `0.0.0.0` binding, WAN firewall rule, reverse-proxy route, public DNS, or browser-debugging port without a separate Kyle approval. Verify listener and original-operator-path access after start. |
| 8 | **State and volume design** | Declare every persistent volume/bind mount, owner UID/GID, data class, growth expectation, retention, migration method, and backup inclusion. Stateless services declare `state: none` and still define artifact/log retention. Browser profiles, if needed, live in named documented private VM volumes. |
| 9 | **Health and readiness** | Define liveness and readiness separately where applicable. Compose health check is deterministic, bounded, and does not require public reachability. Document expected status, endpoint/command, timeout, and dependency ordering. |
| 10 | **Logs and observability** | Emit structured/redacted stdout/stderr; configure a bounded Docker log driver or rotation; name logs and retention. Evidence must include `docker compose ps`, health state, recent redacted logs, resource usage, and listener proof. No secrets in health output. |
| 11 | **Supervision and resources** | `restart: unless-stopped` only for approved durable services; finite jobs use `restart: "no"`. Define CPU, memory, PID, and disk expectations/limits. Deployment refuses when free root filesystem is below **30 GiB** or below **20%**, whichever is stricter, until an explicit capacity exception is approved. |
| 12 | **Backup and isolated restore** | Stateful services name backup schedule, retention, destination, encryption/credential owner, and an application-level restore command. Prove restore into an isolated temporary volume/container without touching production data, then record result and cleanup. VM/PBS backup existence is not sufficient. |
| 13 | **Rollback and retirement** | Retain the previous immutable image/revision until the new deployment passes. Define exact stop/down, rollback-to-prior-revision, schema compatibility, volume preservation, cleanup, and evidence-retention steps. `docker compose down -v` is prohibited unless the approved retirement plan explicitly permits data destruction. |
| 14 | **Evidence bundle** | Persist: source URL/branch/SHA; validation command and output; image digest; Compose config digest/path; environment-variable names only; bind/listener proof; health/restart test; resources; volume/backup/restore evidence; rollback result; unresolved risks; approver/time. Store under `raaptech-brain/assessments/<date>-<service>/` or approved operations repository. |

## Required layout on the Docker VM

This is the target convention for new services; it is not a retroactive change to existing DVM stacks.

```text
/srv/raaptech/services/<service>/
  repo/                     # clean pinned Git checkout or detached worktree
  deploy/compose.yaml       # reviewed generated/adapted deployment definition
  secrets/                  # owner-only, never committed; referenced read-only
  data/                     # only when stateful, explicit UID/GID ownership
  evidence/<deploy-id>/     # redacted deployment receipts
  backups/                  # only when an app backup belongs locally before replication
```

## Live DVM preflight — decision-grade evidence

| Area | Live evidence | Verdict |
|---|---|---|
| Reachability | SSH to `dvm` and Tailscale `100.97.87.28` succeeded; DVM Tailscale reports online/direct. | PASS |
| Host/runtime | Ubuntu 24.04.3, kernel 6.8.0-134; Docker 29.1.5; Compose v5.0.2; Docker enabled and active. | PASS |
| Capacity | 8 vCPU; 46 GiB RAM with ~44 GiB available; root 194 GiB total / 121 GiB free (35% used); inode 9% used. | PASS for one small stateless pilot |
| Existing load | 29/29 containers running, 27 images, 12 Compose projects. | CAUTION — do not disturb existing stacks |
| Existing ports | Many containers bind all interfaces: 80, 81, 443, 8898, 3001, 3034–3036, 3045, 3050, 3055, 3070–3071, 5434, 5437–5438, 5678, 8055; RustDesk also listens broadly. | HIGH — target standard is not yet fleet-wide |
| Firewall | UFW default deny incoming; Tailscale interface allowed; multiple explicit Tailscale rules. Docker-published all-interface ports still need a service-by-service exposure audit. | CAUTION |
| Private storage/backup | `/mnt/truenas` exists but preflight did not prove it is mounted; no application-level backup/restore proof was found. Existing config/Supabase/DB-related crons exist but are not proof for candidate services. | BLOCKED for stateful pilots |
| Conventions | Existing projects are scattered across `/home/dvm`, `/opt`, and `/srv`; no consistent service/evidence root exists. | GAP — new contract establishes one |
| Secrets | Existing running Compose examples include embedded/default-looking credentials. Values are not copied here. | HIGH — do not reuse their patterns |

### DVM blockers to remediate before scaling beyond RDE

1. **Do not assume UFW alone makes Docker-published ports private.** Inventory and explicitly decide each existing all-interface listener; no broad port changes are authorized in this work.
2. **Existing workloads are unproven against the new contract.** They need per-stack source/revision, health, resource, secret, data, backup/restore, and rollback evidence before being called compliant.
3. **No DVM-wide app-level restore evidence was observed.** Stateful workloads cannot enter a new deployment wave until isolated restore is demonstrated.
4. **No canonical DVM deployment root exists.** Create it only within the approved RDE deployment change.
5. **Live inventory and configuration contain legacy weak patterns.** Examples include `latest` tags, published database ports, and inline/default-looking configuration. They are remediation targets, not templates.

## First-wave plan — approval-gated RDE pilot

### Scope and stop conditions

**Purpose:** prove the standard, not create a customer-facing service.  
**Data:** repository-provided `roi-fixture.json` only; no customer data and no external secret values.  
**Network:** no published application port; execute as a finite internal Compose job or localhost-only diagnostic endpoint if a service mode is explicitly added.  
**State:** generated artifacts are written to a named, documented volume or a dated evidence directory; no database.  
**Stop immediately if:** clean validation fails; image build is non-reproducible; any secret value is needed or appears in output; an unexpected listener appears; DVM capacity crosses threshold; output differs from accepted fixture contract; or any action would touch unrelated stack state.

### Phase A — repository contract work (no DVM deployment)

1. Create a branch/PR in `raaptech-rde`; do not work in an ambiguous local copy.
2. On a clean checkout, run and record:
   ```bash
   python3 -m pytest -q
   python3 -m raaptech_rde.cli requests/roi-fixture.json
   ```
3. Add and validate: pinned Python container base, non-root user, Dockerfile, Compose job definition, `.env.example` names-only if configuration is needed, `.dockerignore`, reproducible `uv`/pip contract, health/acceptance command, resource limits, and artifact retention/cleanup instructions.
4. Add CI that exercises the exact container build and fixture acceptance check.
5. Review changes, create PR; no merge without Kyle direction/normal PR authority.

### Phase B — approved DVM proof run

Only after Kyle explicitly approves deployment and the PR/revision is accepted:

1. Capture DVM preflight: `git rev-parse`, `docker version`, `docker compose version`, `df -h`, `docker ps`, listener/port-conflict check, and current resource baseline.
2. Make clean detached checkout at `/srv/raaptech/services/rde/repo` pinned to approved SHA.
3. Inject **no runtime secret values**. Verify only expected environment variable names/placeholders.
4. Run repository validation, build image, record image digest.
5. Run the finite RDE fixture job on an internal network with no published ports; write output and redacted logs to the evidence path.
6. Compare produced artifact manifest/response against expected fixture contract.
7. Verify no unexpected host listener, restart behavior is `restart: "no"`, and resource footprint is bounded.
8. Demonstrate rollback as removal of the new job/container/image reference while preserving the evidence artifact; no persistent service data exists to restore.
9. Save a deployment receipt to Brain and report PASS/BLOCKED with raw evidence locations.

### Success criteria

- Clean pinned checkout and deterministic pytest/fixture execution pass.
- Reproducible non-root image builds.
- No all-interface listener or public exposure is introduced.
- No client data, secrets, customer systems, or existing DVM stacks are touched.
- Artifact set matches the accepted RDE fixture contract.
- Logs/evidence are redacted and durable.
- Rollback/retirement completes without impacting unrelated containers/volumes.

### Candidate wave two — RaapTech website

The website already has Dockerfile, Compose, a non-root `nextjs` user, healthcheck, Node 22 base, lockfile, lint/test/build scripts, and no expected durable app state. It is **not approved for wave one/two deployment** until Kyle decides whether it is private-only or intentionally public. Its current Compose mapping `3000:3000` is all-interface and does not meet this contract. Any deployment must use an explicit private binding/approved edge, resource/log contract, image digest, and rollback proof.

## Approval gate

Kyle must explicitly approve each separately:

1. **RDE repository contract work** (branch/PR and deterministic validation).
2. **RDE DVM proof run** (creates checkout/build/job/evidence on DVM; no service exposure).
3. Any second-wave deployment or any remediation of existing DVM listeners/stacks.

No approval was requested or granted through this document; no DVM state has been changed.

## Evidence locations

- Remote inventory: `sessions/portfolio-inventory/2026-07-14-raaptechllc-remote-inventory.json`
- Technical manifest: `sessions/portfolio-inventory/2026-07-14-active-owned-repo-technical-manifest.json`
- Bounded source evidence: `sessions/portfolio-inventory/2026-07-14-bounded-repo-source-evidence.json`
- Raw DVM preflight: `sessions/portfolio-inventory/2026-07-14-dvm-preflight.txt`
- Portfolio decision matrix: `sessions/portfolio-inventory/2026-07-14-active-repository-matrix.md`
