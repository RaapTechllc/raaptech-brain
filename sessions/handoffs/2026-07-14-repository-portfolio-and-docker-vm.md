---
type: Reference
title: Repository Portfolio and Docker VM Handoff
description: Session handoff for portfolio inventory and VM-first work.
tags: [okf, auto-frontmatter]
timestamp: 2026-07-15T13:55:19Z
---

# Handoff — RaapTech Repository Portfolio and Docker VM Operating Model

**Date:** 2026-07-14  
**For:** Fresh Hermes session, preferably continued from Telegram  
**Status:** Ready to begin repository portfolio triage; no repository archival or Docker VM deployment is authorized by this handoff.

## Immediate objective

Today, review the RaapTech GitHub repository portfolio and decide which repositories will continue moving forward. For the selected repositories:

1. determine actual technical and business viability;
2. classify deployment readiness;
3. close repository-specific deployment gaps;
4. deploy only approved, proven repositories to the Proxmox Docker VM;
5. establish a VM-first operating workflow so source execution, builds, services, browser automation, and durable runtime state live on the Linux workflow plane rather than being scattered across local workstations.

The next session must start with remote GitHub inventory and classification. Do not start by copying local folders or deploying Codex Project Factory.

## Completed work — do not repeat

Codex Project Factory received a three-lane, read-only assessment covering code/runtime truth, RaapTech authority fit, and Docker VM deployment/pilot feasibility.

Final decision: **`BLOCKED WITH PREREQUISITES`**.

Repository validation passed lint, typecheck, 25 tests, and all five builds. The final decision package passed 52/52 structural, consistency, boundary, contradiction, and credential-pattern checks.

Reference the existing artifacts rather than reproducing their contents:

1. `C:\Users\Kyle\CC\raaptech-brain\assessments\2026-07-14-codex-project-factory\01-CODEX-PROJECT-FACTORY-ARCHITECTURE-DECISION.md`
2. `C:\Users\Kyle\CC\raaptech-brain\assessments\2026-07-14-codex-project-factory\02-CODEX-PROJECT-FACTORY-DEPLOYMENT-READINESS.md`
3. `C:\Users\Kyle\CC\raaptech-brain\assessments\2026-07-14-codex-project-factory\03-CONTROL-PLANE-OWNERSHIP-MAP.md`
4. `C:\Users\Kyle\CC\raaptech-brain\assessments\2026-07-14-codex-project-factory\04-CODEX-PROJECT-FACTORY-PROOF-RUN-PLAN.md`
5. `C:\Users\Kyle\CC\raaptech-brain\assessments\2026-07-14-codex-project-factory\05-EVIDENCE-INDEX.md`

The Factory blockers include the absence of a reproducible service deployment contract, no live Codex app-server protocol contract test, unproven self-hosted Convex persistence/backup/restore, package-manager root ambiguity, unenforced recipe parallelism, no active top-level CI, no health contract, and missing cleanup/retention controls.

Do not deploy Factory until its `BLOCKED` readiness rows have command-backed closure.

## Accepted operating boundaries

- **Hermes:** Kyle's conversational operator, approval, notification, and exception surface.
- **Docker VM:** durable Linux workflow and service plane.
- **Git/GitHub:** source, branch, commit, and PR authority.
- **RaapTech OS:** policy, budget authorization, audit/DLP, kill switches, and fleet health.
- **Agentic Brain:** curated operational knowledge after capture → verify → review → promote.
- **Codex Project Factory:** bounded approved-goal-to-draft-PR product delivery only.
- **Project Co-Pilot:** guarded planning/specification; keep separate until an explicit interface contract exists.
- **Archon:** reusable workflow recipe ownership/mechanics where adopted.

Hosting a service on Docker VM does not grant it policy, knowledge, approval, merge, or deployment authority.

## Infrastructure context

- Proxmox Docker VM is the accepted durable Linux workflow plane.
- Accepted evidence from 2026-07-14 says Docker VM and the lab/WAN safety baseline were healthy.
- Historical capacity and service inventory must be treated as stale until re-probed live before deployment.
- Existing backup infrastructure includes Proxmox/PBS/TrueNAS, but VM-level restore proof does not automatically prove application-level state consistency or restore.
- Access must remain private. Use SSH and Tailscale/private networking. Do not publish dashboards or service ports to the WAN without a separate explicit approval.
- No credential values are included in this handoff. Resolve credentials from the approved credential store only in the shell or service that needs them.

## Portfolio decision rule

A repository earns continued active status only if it does at least one of the following:

- generates outreach, onboarding, delivery, or revenue now;
- materially reduces client-delivery time;
- supports an active client or internal operating capability;
- contains durable vertical/domain IP, governance, diagnostics, or integration logic worth preserving;
- is necessary infrastructure for an approved active product or workflow.

A polished UI, a better model, a runnable demo, or recent activity is not sufficient by itself.

Use these lifecycle classes:

- `REVENUE-NOW`
- `INTERNAL-CORE`
- `VERTICAL-IP`
- `DEMO/FREEZE`
- `SEPARATE-PORTFOLIO`
- `CONSOLIDATE`
- `EXTRACT-THEN-ARCHIVE`
- `ARCHIVE-CANDIDATE`

Do not archive, transfer, delete, or mutate repositories during evidence gathering. Present cleanup batches to Kyle for explicit approval.

## First-session execution plan

### Stage 1 — establish remote portfolio truth

1. Verify GitHub authentication without printing credential values.
2. Enumerate the authoritative `RaapTechllc` GitHub portfolio.
3. Separate active owned repositories, active forks, and archived repositories.
4. Capture repository name, URL, visibility, archived/fork state, default branch, last update, language, and description.
5. Bound the first review to active owned repositories relevant to RaapTech operations, client delivery, internal automation, and deployable services.

Do not perform broad local filesystem archaeology before the remote inventory is complete.

### Stage 2 — classify business and technical viability

For each bounded candidate, inspect read-only evidence:

- README, architecture/decision documents, and agent instructions;
- package/project manifests and lockfiles;
- canonical test, lint, typecheck, build, and run commands;
- Dockerfile, Compose, active CI, deployment scripts, health checks, and rollback support;
- environment-variable names only and secret-injection strategy;
- state, database, volumes, migrations, retention, backup, and restore needs;
- authentication, port/bind, browser/headed/headless requirements;
- git identity, branch, revision, status, and last commit;
- unique reusable IP and dependencies on other repositories.

Run deterministic non-mutating checks where feasible. Separate code viability from missing local tooling.

### Stage 3 — produce today's decision matrix

Create a durable matrix with one row per active owned candidate:

- lifecycle class;
- business reason;
- technical health;
- deployment class: `DEPLOYABLE NOW`, `NEEDS CONTAINERIZATION`, `NEEDS STATE/SECURITY WORK`, `KEEP OFF VM`, or `ARCHIVE PATH`;
- required runtime and state;
- risk and exposure;
- canonical repository/check-out;
- next action;
- confidence and evidence.

Limit the first deployment wave to one or two low-risk services. Do not attempt to migrate the entire portfolio today.

### Stage 4 — define the reusable VM-first contract

Create one standard deployment contract, then adapt it per repository. Minimum expected components:

- pinned runtime and dependency versions;
- one canonical lockfile/package-manager strategy;
- non-root container/service identity;
- Dockerfile and versioned Compose definition where appropriate;
- `.env.example` containing names/placeholders only, never values;
- private bindings and Tailscale/SSH operator access;
- persistent volume declarations and ownership;
- read-only preflight;
- deterministic validation before build/start;
- health/readiness contract;
- structured/redacted logs and rotation;
- restart/supervision policy;
- resource limits and disk thresholds;
- backup and isolated application-level restore procedure;
- rollback/retirement procedure;
- deployment evidence bundle.

Recommended workflow:

`Hermes approval → SSH to Docker VM → isolated Git checkout/worktree → validate → container build → Compose deploy → health/smoke → evidence → rollback if failed`

No service should depend on an arbitrary local workstation checkout or parent-directory lockfile. Local workstations should remain operator surfaces, not durable runtime planes.

### Stage 5 — select and prove one pilot

Choose the simplest approved repository that already has deterministic validation, externalized configuration, no customer data, and minimal state. Prove:

1. clean pinned checkout;
2. validation success;
3. reproducible image build;
4. private service startup;
5. health check from the original operator path;
6. restart behavior;
7. logs and resource visibility;
8. backup/restore when stateful;
9. rollback;
10. no unexpected listeners, secrets, or local-workstation dependencies.

Only after this contract works should it become the template for subsequent repositories.

## Browser and interactive-work policy

- Prefer headless browser automation on Docker VM for repeatable service tasks.
- Use a headed browser only when authentication, visual QA, or human interaction requires it.
- Keep browser profiles and session state on a documented private VM volume, not scattered on workstations.
- Access headed sessions through a private mechanism such as Tailscale-protected remote desktop/browser tooling; do not expose browser-debugging ports publicly.
- SSH commands must operate in canonical VM repository roots or disposable worktrees, never ambiguous user-home folders.

## Required durable outputs from the next session

1. Active repository portfolio matrix.
2. Continue-moving shortlist, capped to the highest-leverage repositories.
3. Proposed archive/extract/consolidate batch requiring Kyle approval.
4. VM-first deployment standard/template.
5. First-wave deployment plan for one or two repositories.
6. Live Docker VM preflight evidence and blockers.
7. A new handoff if deployment cannot be completed in the same session.

Save durable outputs outside `%TEMP%`, preferably in the RaapTech Brain or an approved version-controlled operations repository. Before relying on the Factory assessment long term, copy its five artifacts from `%TEMP%` into the chosen durable evidence location without altering their contents.

## Stop conditions

Stop and ask Kyle before:

- archiving, deleting, transferring, or changing repository visibility;
- deploying a service or changing Docker VM state;
- exposing any port outside the approved private network;
- moving or importing credentials;
- changing DNS, router, firewall, Proxmox, PBS, TrueNAS, or production infrastructure;
- merging PRs or modifying customer/production data;
- choosing between materially different product directions.

Read-only GitHub inventory, source inspection, non-mutating validation, and live read-only VM preflight may proceed without another approval.

## Suggested skills

Load and follow:

- `repository-portfolio-governance`
- `github-repo-management`
- `codebase-inspection`
- `infrastructure-audit`
- `network-service-debugging`

For deeper selected-repository work, also consider:

- `repo-e2e-validation`
- `codebase-design`
- `writing-plans`
- `github-pr-workflow`
- `secrets-handling`

## Telegram starter prompt

```text
Continue the RaapTech repository portfolio and Proxmox Docker VM initiative using this handoff as the controlling context:

C:\Users\Kyle\CC\raaptech-brain\sessions\handoffs\2026-07-14-repository-portfolio-and-docker-vm.md

Start now with remote GitHub truth. Load repository-portfolio-governance, github-repo-management, codebase-inspection, infrastructure-audit, and network-service-debugging. Enumerate the RaapTechllc portfolio, separate active owned repos/forks/archived repos, then bound the review to active owned repositories relevant to revenue, client delivery, internal operations, and deployable services.

For each bounded repository, gather read-only business-fit and technical/deployment evidence. Classify lifecycle and deployment readiness. Produce a durable active-repository matrix, a capped continue-moving shortlist, and proposed extract/consolidate/archive batches. Do not archive, delete, transfer, change visibility, or deploy anything without explicit Kyle approval.

Then read-only probe the Proxmox Docker VM to establish current capacity, containers, runtime versions, listeners, private access, volume/storage, and backup state. Design one reusable VM-first deployment contract: pinned checkout, deterministic validation, non-root Docker/Compose service, externalized secrets, private bindings, health checks, logs, resource limits, backup/restore, rollback, and evidence. Select only one or two low-risk first-wave repositories. Local workstations are operator surfaces, not durable runtime planes.

Codex Project Factory has already been assessed and remains BLOCKED WITH PREREQUISITES. Do not repeat that assessment or deploy it. Reference its five artifacts under C:\Users\Kyle\CC\raaptech-brain\assessments\2026-07-14-codex-project-factory\ when needed.

Lead with decisions and evidence. Keep the portfolio audit bounded and return attention to revenue/client delivery once the active set is sufficient.
```
