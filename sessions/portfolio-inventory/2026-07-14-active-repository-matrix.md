---
type: Reference
title: Active Repository Matrix
description: Decision matrix for RaapTechllc active repositories.
tags: [okf, auto-frontmatter]
timestamp: 2026-07-15T13:55:19Z
---

# RaapTech Active Repository Portfolio Matrix

**Evidence date:** 2026-07-14  
**Scope:** all 32 active, owned repositories in `RaapTechllc`; no remote lifecycle action was taken.  
**Canonical inventory:** `2026-07-14-raaptechllc-remote-inventory.json`  
**Technical manifest:** `2026-07-14-active-owned-repo-technical-manifest.json`  
**Bounded source evidence:** `2026-07-14-bounded-repo-source-evidence.json`

## Decision

Keep the forward portfolio deliberately small:

1. **SMW Cloud** — client-delivery system; the only direct client product in this review.
2. **RaapTech website** — revenue-facing offer and conversion surface.
3. **RaapTech OS** — internal governance/control-plane IP.
4. **RaapTech Brain** — curated operational knowledge plane.
5. **Fable5** — operating discipline for scarce high-leverage model runs.
6. **RDE** — smallest reusable research/ROI-deliverable primitive; needs proof before broader investment.

Everything else is either a separate portfolio, an internal experiment/demo, a bounded extraction candidate, or needs a specific evidence gap closed. This is **not** an archival authorization.

## Matrix

| Repository | Lifecycle | Business reason / durable asset | Technical health evidence | Deployment class | Runtime / state | Risk / exposure | Next action | Confidence |
|---|---|---|---|---|---|---|---|---|
| [project-copilot](https://github.com/RaapTechllc/project-copilot) | DEMO/FREEZE | Guarded planning/specification; must remain distinct from Factory and OS. | Recent 7b71c30; CI has format/lint/mypy/pytest/Postgres + pnpm checks; two Dockerfiles but no root compose contract found. | NEEDS CONTAINERIZATION | Next.js, FastAPI, Postgres, Clerk/xAI configuration. | Multi-service auth/state/control-plane overlap. | Finish explicit interface/authority contract; do not deploy in wave one. | High |
| [codex-project-factory](https://github.com/RaapTechllc/codex-project-factory) | DEMO/FREEZE | Bounded draft-PR delivery concept only. | Existing independent assessment: lint, typecheck, 25 tests, five builds pass; deployment blockers remain. | KEEP OFF VM | Node/Turbo/Convex/Codex protocol; persistence unresolved. | Blocked service contract, Convex durability, cleanup/retention, health and CI gaps. | **BLOCKED WITH PREREQUISITES**; no re-assessment or deployment. | High |
| [codex-project-factory-e2e-20260713](https://github.com/RaapTechllc/codex-project-factory-e2e-20260713) | EXTRACT-THEN-ARCHIVE | Disposable Factory verification fixture. | 11 files, CI, package lock; explicitly described as disposable. | ARCHIVE PATH | Node fixture only. | Could be CI dependency; no gate review yet. | Verify Factory CI/references, preserve reproducible fixture instructions, then propose archive. | High |
| [trading-platform](https://github.com/RaapTechllc/trading-platform) | SEPARATE-PORTFOLIO | Paper/live trading system, not RaapTech consulting core. | Recent 1dc3ef2; Dockerfile/Compose/.env.example/CI; CI runs pytest and bounded live-config smoke; already running on DVM. | NEEDS STATE/SECURITY WORK | Python, exchange credentials, runtime/db bind mounts. | Financial-loss and credential risk; current host port 3045 is all-interface. | Keep separate; only paper/replay until separate trading approval and restore/security proof. | High |
| [RaapTech-OS](https://github.com/RaapTechllc/RaapTech-OS) | INTERNAL-CORE | Governance, policy, local-first construction/fabrication OS. | Recent 8e3d0e1; pyproject, .env.example, CI; README defines Hermes profile model. No Docker/Compose marker. | KEEP OFF VM | Hermes/runtime and policy artifacts; no service contract. | Must not become a duplicate control plane or unmanaged daemon. | Define bounded service candidates separately; retain as source/policy authority. | High |
| [minibench](https://github.com/RaapTechllc/minibench) | DEMO/FREEZE | Hardware benchmark proof/learning asset, not current consulting offer. | Docker Compose, frontend/backend Dockerfiles, .env example, CI with pytest/npm test/build; already running on DVM. | NEEDS STATE/SECURITY WORK | FastAPI, React, Postgres volume. | Public-facing product; Compose uses published API/UI/DB ports and placeholder DB password. | Use as **contract remediation pilot only** after approval: private binds, non-root/resource/log/backup/restore proof. | High |
| [cerebro](https://github.com/RaapTechllc/cerebro) | EXTRACT-THEN-ARCHIVE | Citation-first retrieval/evaluation ideas. | 52 files, npm lock; README calls it a narrow-V1 spike/pivot and Convex extension; no Docker/CI marker. | ARCHIVE PATH | Browser extension, Convex, local profile/state. | Consumer/product overlap with Brain; unproven deployment. | Extract citation/eval patterns into Brain or a future retrieval component, then propose archive. | High |
| [raaptech-brain](https://github.com/RaapTechllc/raaptech-brain) | INTERNAL-CORE | Curated knowledge and evidence index for all operating planes. | Recent d5fb9e1; deterministic `scripts/brain.py`; requirements; OKF validation fixes; no service need. | KEEP OFF VM | Git knowledge bundle, Python retrieval script. | Public repo requires deliberate redaction; source-of-truth links must not duplicate secrets. | Continue as durable evidence destination; use its save/reindex workflow. | High |
| [the-pit](https://github.com/RaapTechllc/the-pit) | SEPARATE-PORTFOLIO | Crypto paper-trading research/design IP. | Recent e4bb835; pyproject/.env.example/pytest CI; README says paper mode default, SQLite/FastAPI dashboard. | NEEDS CONTAINERIZATION | Python, SQLite, market APIs, Telegram. | Trading/data/alert risk; no Docker contract found. | Keep separate; preserve paper-mode safety; do not add to VM wave. | High |
| [RaapTech](https://github.com/RaapTechllc/RaapTech) | REVENUE-NOW | Consulting offer and conversion surface for fabrication/AI onboarding. | Recent 65ac1e2; Node 22 documented; Dockerfile/Compose/npm lock; lint/test/build scripts. | NEEDS STATE/SECURITY WORK | Next.js static/app runtime; no durable application state expected. | Currently DVM website uses all-interface 3035 mapping; needs private-edge policy and health/resource/log proof. | Candidate second contract-remediation pilot, after public/private hosting decision. | High |
| [RaapTech-PDF](https://github.com/RaapTechllc/RaapTech-PDF) | SEPARATE-PORTFOLIO | Personal Windows PDF/capture product; valuable product exploration but outside present offer. | Recent 6831e42; Phase 0 GO, personal build; docs-only/Windows-oriented; no runtime marker. | KEEP OFF VM | Windows desktop application. | Wrong operating plane; personal-product scope. | Continue only as separate personal portfolio. | High |
| [fable5](https://github.com/RaapTechllc/fable5) | INTERNAL-CORE | Prompt/run discipline and high-value model-use controls. | Recent 4813dbc; documentation/OKF operating repository, no application runtime. | KEEP OFF VM | Git documents/artifacts. | Misuse/cost rather than service risk. | Keep as source-managed operating repository; no containerization. | High |
| [RaapTech-Jarvis](https://github.com/RaapTechllc/RaapTech-Jarvis) | DEMO/FREEZE | Voice-first desktop-operator concept; potential UX/IP, not a current offer. | Recent 84b9125; Electron/Vite, lint/typecheck/test/smoke/UI scripts and CI; .env example. | KEEP OFF VM | Windows/macOS desktop, WebRTC and provider credentials. | Computer-control and voice-auth risk; headed desktop required. | Freeze product expansion pending a named buyer/use case; preserve audit/approval patterns. | High |
| [raaptech-rde](https://github.com/RaapTechllc/raaptech-rde) | VERTICAL-IP | Deterministic request-to-ROI calculator deliverable for consulting discovery and sales. | 8-file P0; README documents CLI and pytest; pyproject. No Docker/CI marker. | NEEDS CONTAINERIZATION | Python, JSON inputs, generated HTML/JSON/YAML artifacts; likely stateless. | Source/provenance quality and output correctness; minimal attack surface. | Run clean fixture proof; add CI, Dockerfile/Compose, health/no-op job contract before selecting it as an internal worker pilot. | Medium |
| [smw-cloud](https://github.com/RaapTechllc/smw-cloud) | REVENUE-NOW | Active Sheet Metal Werks operational command layer; directly reduces client delivery friction. | Recent 7cf37d0; pnpm lock, Docker Compose, .env example, CI; canonical `validate` runs typecheck/lint/test/build; docs say several product epics remain placeholders. | NEEDS STATE/SECURITY WORK | Next.js, Postgres, Redis/BullMQ, Windows-only FabOps/Autodesk bridge. | Client data, Autodesk, Teams, QR/workflow mutation. Existing unverified VM artifact/volumes are stale. | Retain and advance only client-approved value slices; define private deployment and backup/restore contract before any redeploy. | High |
| [agent-arcade](https://github.com/RaapTechllc/agent-arcade) | DEMO/FREEZE | Agent evaluation/scorecard experiment. | Recent 02ddeae; pnpm lock, CI, no Docker contract identified. | KEEP OFF VM | Node application/evaluation state unknown. | Commodity wrapper risk. | Preserve any useful scoring schema; no service investment. | Medium |
| [openclaw-agents](https://github.com/RaapTechllc/openclaw-agents) | CONSOLIDATE | Historical fleet workspaces and useful protocols. | 3,824 files; many embedded projects/Dockerfiles; CI; README identifies workstation-centred legacy fleet. | KEEP OFF VM | Multiple agents/services/state paths. | Monorepo contains overlapping control planes and high accidental-deploy risk. | Extract approved reusable protocols into OS/Brain; inventory dependencies before any archive/consolidation batch. | Medium |
| [SEO-Health-Report-System](https://github.com/RaapTechllc/SEO-Health-Report-System) | DEMO/FREEZE | Potential diagnostic/report methodology, but no named client/demand in evidence. | Dockerfile/Compose/.env examples, multiple CI/deploy/rollback workflows, Python; README claims MVP hardening. | NEEDS STATE/SECURITY WORK | FastAPI/job worker, likely Postgres/AI/provider keys. | External crawling/provider secrets, report data, unverified customer value. | Perform deterministic clean validation and data-flow review; only then consider internal diagnostic pilot—not wave one by default. | Medium |
| [dontbuyjunktech](https://github.com/RaapTechllc/dontbuyjunktech) | SEPARATE-PORTFOLIO | Consumer technology project. | Recent ab344db1; npm lock and CI; no Compose/Docker marker. | KEEP OFF VM | Node/consumer app. | Outside current consulting scope. | Separate portfolio; no current RaapTech deployment work. | High |
| [DealForge](https://github.com/RaapTechllc/DealForge) | DEMO/FREEZE | Outbound/integration experiment; could inform sales operations. | Recent 9ef56ea; .env example, CI, npm lock; 10 outbound integrations. | NEEDS STATE/SECURITY WORK | Node and broad third-party service credentials. | High credential/outbound automation risk; unclear buyer/workflow. | Freeze; extract only reusable integration governance if a sales workflow demands it. | Medium |
| [raaptech-trading-stack](https://github.com/RaapTechllc/raaptech-trading-stack) | SEPARATE-PORTFOLIO | Trading intelligence/paper-trading suite. | Recent d273eb5; pyproject, CI, Hermes cron architecture; README says paper-trading. | KEEP OFF VM | Hermes cron jobs, SQLite/data feeds. | Financial decision risk and separate governance. | Continue as isolated trading portfolio; no general DVM migration. | High |
| [hourly-opus-ultracode](https://github.com/RaapTechllc/hourly-opus-ultracode) | CONSOLIDATE | Historical model/run-loop artifacts. | Recent 099bba9; CI/README, no deploy markers. | ARCHIVE PATH | Docs/scripts; runtime unclear. | Overlaps Fable5/Hermes operating discipline. | Compare unique prompts/gates with Fable5; extract distinct material then propose archive. | Medium |
| [raaptech-vault](https://github.com/RaapTechllc/raaptech-vault) | CONSOLIDATE | Prior Obsidian knowledge base. | 1,638 files, README; last update June 22. | KEEP OFF VM | Knowledge documents. | Duplicate/possibly stale authority relative to Brain. | Establish canonical ownership and migration/extraction manifest into Brain; no deletion yet. | Medium |
| [SMW-EMERGENT](https://github.com/RaapTechllc/SMW-EMERGENT) | EXTRACT-THEN-ARCHIVE | Historical SMW experiments only if unique client logic remains. | 87 files; README; last meaningful signal is auto-generated change; no runtime contract. | ARCHIVE PATH | Unknown. | Could contain client-specific IP/data. | Inspect unique docs/code and redaction needs; extract named useful artifacts before archive proposal. | Low |
| [nbarunner](https://github.com/RaapTechllc/nbarunner) | SEPARATE-PORTFOLIO | Hardware/controller project. | 40 files, README; no service markers. | KEEP OFF VM | Hardware/Windows dependencies. | Outside consulting scope. | Separate portfolio. | High |
| [n8n-integration](https://github.com/RaapTechllc/n8n-integration) | CONSOLIDATE | Integration experiments that may overlap active DVM n8n. | 123 files, shell-language repo, no root runtime/deploy marker in manifest. | NEEDS STATE/SECURITY WORK | n8n workflows/credentials. | Active n8n service has credentials and workflow mutation risk. | Compare workflows with deployed canonical n8n export; extract verified flows, then propose consolidation. | Medium |
| [openclaw-agent-backup](https://github.com/RaapTechllc/openclaw-agent-backup) | VERTICAL-IP | Sanitized backup/restore approach for agent state. | 393 files; README identifies sanitized backup snapshots; last update Apr 12. | KEEP OFF VM | Shell/config snapshots. | Must avoid credential and stale-config restoration. | Retain as reference until its functions are deliberately folded into OS/Brain backup standard. | Medium |
| [funding-rate-monitor](https://github.com/RaapTechllc/funding-rate-monitor) | SEPARATE-PORTFOLIO | Tiny trading data utility. | 3 files, requirements; old. | ARCHIVE PATH | Python/API URL env vars. | Trading scope, unknown operational use. | Verify no active cron/repo references; then propose archive or fold into trading stack. | High |
| [mc-sync](https://github.com/RaapTechllc/mc-sync) | CONSOLIDATE | Mission Control health/repository sync script. | 2 files; old; no standard manifest. | ARCHIVE PATH | Python/script environment. | May overlap Lab Pulse/Brain/fleet tooling. | Compare output/consumers with Lab Pulse; extract if unique, otherwise propose archive. | Medium |
| [trading-research-swarm](https://github.com/RaapTechllc/trading-research-swarm) | SEPARATE-PORTFOLIO | Historical trading research swarm. | 305 files, agent guidance; old. | ARCHIVE PATH | Agent prompts/scripts; dependencies not reviewed. | Separate trading scope and possible reusable prompts. | Extract unique research-method material into trading stack, then propose archive. | Medium |
| [beanzneez](https://github.com/RaapTechllc/beanzneez) | SEPARATE-PORTFOLIO | Consumer coffee-deal application. | Dockerfile/.env/CI/npm lock; March activity. | KEEP OFF VM | Node/Convex-style application state. | Consumer scope; duplicate successor exists. | Hold while deciding canonical consumer repo; no RaapTech core investment. | High |
| [beanzneez-v2](https://github.com/RaapTechllc/beanzneez-v2) | SEPARATE-PORTFOLIO | Newer consumer coffee-deal application. | Dockerfile/Compose/.env; already running on DVM, but no CI marker. | NEEDS STATE/SECURITY WORK | Next.js/Postgres volume. | Current Compose has published all-interface app and DB ports and embedded secrets; non-compliant with target contract. | Separate portfolio; remediate or retire its DVM stack in a dedicated approval window. | High |

## Proposed continue-moving shortlist

| Priority | Repository | Why now | Approval boundary |
|---|---|---|---|
| 1 | SMW Cloud | Direct active-client leverage; has canonical validation and CI. | No VM deployment or client-data change without Kyle/client-approved scope. |
| 2 | RaapTech website | Direct revenue conversion and low application state. | Hosting/public exposure decision required before any service change. |
| 3 | RaapTech OS | Keeps policy and control-plane boundaries explicit. | Do not turn into a DVM service without a bounded authority decision. |
| 4 | RaapTech Brain | Durable evidence/operating knowledge. | No separate deployment required. |
| 5 | Fable5 | Preserves disciplined high-value execution. | No separate deployment required. |
| 6 | RDE | Smallest sales-deliverable primitive worth proving. | Containerization/validation changes require repository approval path. |

## Proposed cleanup batches — approval required

No archive, transfer, visibility change, deletion, or repo mutation has occurred.

| Batch | Candidates | Action after gates | Required gates |
|---|---|---|---|
| A — disposable fixtures | `codex-project-factory-e2e-20260713` | Extract reproducibility instructions; archive. | Search Factory CI/docs, branches/tags, and remote dependency references. |
| B — duplicate operating artifacts | `cerebro`, `hourly-opus-ultracode`, `raaptech-vault`, `mc-sync`, `n8n-integration`, `openclaw-agents` | Extract named durable components into Brain/OS/Fable5 or deployed canonical n8n; consolidate/archive sources. | Extraction manifest, destination verification, CI/dependency, branch/tag and unpushed-work checks. |
| C — stale separate projects | `SMW-EMERGENT`, `funding-rate-monitor`, `trading-research-swarm` | Extract vertical/trading/client IP then archive as appropriate. | Client-data review and explicit Kyle approval. |

**Excluded from cleanup:** all 39 already-archived repositories, active fork(s), current client assets, and all consumer/trading projects until their own portfolio decisions. They were counted but not mutated.

## Evidence limits

This is a remote metadata/source-manifest classification, not a claim that every candidate builds today. The next proof step for any `NEEDS …` row is its repository-specific clean checkout and deterministic validation. Missing local tooling is not a code-health failure.
