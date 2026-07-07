# RaapTech Brain catalogue — one line per retrievable section.
# Format: path#anchor | keywords | one-sentence description
# GENERATED — never hand-edit. Update via `python scripts/brain.py save`
# (append) or `python scripts/brain.py reindex` (full rebuild).

architecture/cost-policy.md | cost policy architecture budget audit raaptech os 50 | RaapTech OS cost policy — $50/day hard cap, per-model pricing, audit scope.
architecture/cost-policy.md#hard-cap | hard cap cost policy 50 day across providers | $50/day across all providers.
architecture/cost-policy.md#per-model-pricing | model pricing cost policy routing serves role | See Model Routing for which model serves which role.
architecture/cost-policy.md#audit-scope | audit scope cost policy mutating actions g sec | Mutating actions only (G-SEC-01).
architecture/cost-policy.md#quota-conservation | quota conservation cost policy 6 ollama crons paused | All 6 Ollama crons paused as of 2026-06-30 (quota low).
architecture/decisions-map.md | architecture decisions map raaptech os summary 27 ratified | Summary of all 27 ratified RaapTech OS architecture decisions with source links.
architecture/decisions-map.md#decision-groups | decision groups architecture decisions map full 27 source | Full 27/27 decisions: See source document.
architecture/decisions-map.md#g-arch-architecture--provider-4-decisions | g arch architecture provider 4 decisions map | G-ARCH: Architecture & Provider (4 decisions) — see Architecture Decisions Map.
architecture/decisions-map.md#g-sec-security-3-decisions | g sec security 3 decisions architecture map | G-SEC: Security (3 decisions) — see Architecture Decisions Map.
architecture/decisions-map.md#g-arch-continued-engine-design | g arch continued engine design architecture decisions map | G-ARCH (continued): Engine Design — see Architecture Decisions Map.
architecture/decisions-map.md#g-rot-rotation--maintenance | g rot rotation maintenance architecture decisions map full | Full 27/27 decisions: See source document.
architecture/decisions-map.md#implementation-status | implementation status architecture decisions map pr 3 master | PR #3: Master Engine merged (audit, cost, DLP, killswitch, rot primitives).
architecture/dlp-security.md | dlp security architecture kill switch data loss prevention | Data loss prevention patterns, kill switches, per-client DLP configuration.
architecture/dlp-security.md#decisions | decisions dlp security | Decisions — see DLP & Security.
architecture/dlp-security.md#dlp-scanner | dlp scanner security dlpscanner client scanning | DLPScanner(client=...) for per-client scanning.
architecture/dlp-security.md#kill-switches | kill switches dlp security mcp server switch config | Per MCP server kill switch in config/mcp_servers.yaml.
architecture/mcp-servers.md | mcp servers architecture integration connected transport audit scope | Connected MCP servers — transport, audit scope, kill switches.
architecture/mcp-servers.md#defaults | defaults mcp servers | Defaults — see MCP Servers.
architecture/mcp-servers.md#connected-servers | connected servers mcp | Connected Servers — see MCP Servers.
architecture/mcp-servers.md#rules | rules mcp servers server independent kill switch g | Each server has independent kill switch (G-SEC-03).
architecture/model-routing.md | model routing architecture models openrouter serves role raaptech | Which model serves which role in RaapTech OS — orchestrator, executor, fallback chain.
architecture/model-routing.md#active-routing-post-pr-4 | active routing post pr 4 model | Active Routing (Post PR #4) — see Model Routing.
architecture/model-routing.md#key-rules | key rules model routing anthropic crons heartbeats | No Anthropic on crons or heartbeats.
architecture/model-routing.md#moa-presets | moa presets model routing | MoA Presets — see Model Routing.
architecture/model-routing.md#cost-policy | cost policy model routing | See Cost Policy.
architecture/rot-maintenance.md | rot maintenance architecture credentials rates credential rotation schedule | Rot rates, credential rotation schedule, config freshness policy.
architecture/rot-maintenance.md#rot-rates | rot rates maintenance adopted mark kashef exactly g | Adopted from Mark Kashef's rot rates exactly (G-ROT-01):.
architecture/rot-maintenance.md#credential-rotation | credential rotation rot maintenance oauth tokens auto refresh | OAuth tokens auto-refresh via provider SDKs.
architecture/rot-maintenance.md#config-freshness | config freshness rot maintenance files stamped timestamp frontmatter | Config files stamped with timestamp in frontmatter.
sessions/run-ledger.md | run ledger sessions fable5 cost fable 5 usage | Fable 5 usage ledger — cost, duration, worth-it verdicts, routing lessons.
sessions/run-ledger.md#runs | runs run ledger | Runs — see Run Ledger.
sessions/run-ledger.md#routing-lessons | routing lessons run ledger dry prompt validation claude | Dry-run prompt validation → Claude CLI, not Fable.
sessions/session-catalog.md | session catalog sessions fable5 fable 5 prompts descriptions | All Fable 5 session prompts with descriptions and target repos.
sessions/sprint-tracker.md | sprint tracker sessions current state fable 5 status | Current state of all Fable 5 sessions — status, next action, blockers.
sessions/sprint-tracker.md#next-action | next action sprint tracker implementation first fable reset | Implementation-first while Fable reset is available:.
sessions/sprint-tracker.md#sprint-status-summary | sprint status summary tracker | Sprint Status Summary — see Sprint Tracker.
fleet/backups.md | backups disaster recovery fleet proxmox truenas docker vm | Proxmox, TrueNAS, Docker VM backup strategy and schedules.
fleet/backups.md#architecture | architecture backups disaster recovery | Architecture — see Backups & Disaster Recovery.
fleet/backups.md#backup-targets | backup targets backups disaster recovery | Backup Targets — see Backups & Disaster Recovery.
fleet/backups.md#key-vms-backed-up | key vms backed backups disaster recovery | Key VMs Backed Up — see Backups & Disaster Recovery.
fleet/backups.md#recovery-order | recovery order backups disaster proxmox hypervisor | Proxmox hypervisor.
fleet/backups.md#notes | notes backups disaster recovery truenas 100 72 235 | TrueNAS at 100.72.235.14 (Tailscale) — SSH key: truenas_admin + key truenas_maxx.
fleet/monitoring.md | monitoring health checks fleet crons heartbeats service monitored | How each service is monitored — crons, heartbeats, alerts, dashboards.
fleet/monitoring.md#dashboard-lab-pulse | dashboard lab pulse monitoring health checks primary projects | Primary: ~/projects/lab-pulse/run-pulse.bat — checks 7 DVM services + 7 TS hosts.
fleet/monitoring.md#hermes-cron-monitoring | hermes cron monitoring health checks rule set model | Rule: Every cron MUST set --model explicitly.
fleet/monitoring.md#health-check-matrix | health check matrix monitoring checks | Health Check Matrix — see Monitoring & Health Checks.
fleet/monitoring.md#proxmox-monitoring | proxmox monitoring health checks web ui https 10 | Web UI: https://10.0.0.20:8006 (LAN) or via Tailscale.
fleet/monitoring.md#alert-flow | alert flow monitoring health checks | Alert Flow — see Monitoring & Health Checks.
fleet/monitoring.md#daily-ops-stack | daily ops stack monitoring health checks run pulse | run-pulse.bat — Lab Pulse (service check).
fleet/services.md | fleet services ollama openclaw hermes runs across raaptech | What runs where across the RaapTech fleet — Ollama, OpenClaw, Hermes, n8n, Postgres, TradingView.
fleet/services.md#core-services | core services fleet | Core Services — see Fleet Services.
fleet/services.md#daily-ops-stack | daily ops stack fleet services | Daily Ops Stack — see Fleet Services.
fleet/services.md#model-serving | model serving fleet services | Model Serving — see Fleet Services.
fleet/services.md#storage | storage fleet services | Storage — see Fleet Services.
fleet/tailscale-map.md | tailscale network map fleet ips topology hostnames roles | All Tailscale IPs, hostnames, roles, and connectivity notes.
fleet/tailscale-map.md#ip-map | ip map tailscale network | IP Map — see Tailscale Network Map.
fleet/tailscale-map.md#connectivity-rules | connectivity rules tailscale network map fix don work | If Tailscale is down → fix Tailscale, don't work around with LAN IPs.
fleet/tailscale-map.md#fleet-agent--tailscale | fleet agent tailscale network map | Fleet Agent ↔ Tailscale — see Tailscale Network Map.
fleet/tailscale-map.md#network-diagram | network diagram tailscale map | Network Diagram — see Tailscale Network Map.
fleet/topology.md | fleet topology proxmox nodes raaptech hardware roles tailscale | All RaapTech fleet nodes — hardware, roles, Tailscale IPs, status.
fleet/topology.md#command-node | command node fleet topology | Command Node — see Fleet Topology.
fleet/topology.md#proxmox-host | proxmox host fleet topology | Proxmox Host — see Fleet Topology.
fleet/topology.md#fleet-agents-proxmox-vms | fleet agents proxmox vms topology | Fleet Agents (Proxmox VMs) — see Fleet Topology.
fleet/topology.md#containers | containers fleet topology | Containers — see Fleet Topology.
fleet/topology.md#key-rules | key rules fleet topology lab access tailscale | ALL lab access via Tailscale ONLY.
fleet/topology.md#pve-8-fixes-historical | pve 8 fixes historical fleet topology nvidia uvm | nvidia-uvm major 234→511.
business/ai-trading-council.md | ai trading council business crypto modes allocation rules | AI Trading Council modes, allocation rules, and strategy brief.
business/ai-trading-council.md#modes | modes ai trading council | Modes — see AI Trading Council.
business/ai-trading-council.md#rules-june-2026 | rules june 2026 ai trading council small gains | Small gains: Take profits early, don't hold for moonshots.
business/ai-trading-council.md#platforms | platforms ai trading council primary hl hyperliquid | Primary: HL (HyperLiquid).
business/ai-trading-council.md#integration | integration ai trading council tradingview mcp jackson | TradingView MCP Jackson at ~/tradingview-mcp-jackson.
business/client-work.md | client work business clients smw sheet metal werks | Active client engagements — Sheet Metal Werks, SMW Cloud, and pipeline.
business/client-work.md#primary-client-sheet-metal-werks-inc-smw | primary client sheet metal werks inc smw work | Main web platform (smw-cloud-main).
business/client-work.md#smw-cloud-components | smw cloud components client work main web platform | Main web platform (smw-cloud-main).
business/client-work.md#smw-sessions | smw sessions client work session 1 ready ship | Session 1: ready_to_ship summary path — done.
business/client-work.md#pipeline | pipeline client work | Pipeline — see Client Work.
business/client-work.md#client-rules | client rules work smw deliverable goes github | Every SMW deliverable goes through GitHub.
business/morning-ops.md | morning operations business daily ops stack lab pulse | Daily ops stack — Lab Pulse, Morning Brief, Super Brain dashboard.
business/morning-ops.md#daily-stack-run-order | daily stack run order morning operations command projects | Command: ~/projects/lab-pulse/run-pulse.bat.
business/morning-ops.md#1-lab-pulse | 1 lab pulse morning operations command projects run | Command: ~/projects/lab-pulse/run-pulse.bat.
business/morning-ops.md#2-morning-brief | 2 morning brief operations command projects ops run | Command: ~/projects/morning-ops-brief/run-brief.bat.
business/morning-ops.md#3-super-brain | 3 super brain morning operations command projects dashboard | Command: ~/projects/super-brain-dashboard/run-brain.bat.
business/morning-ops.md#integration-points | integration points morning operations three tools feed obsidian | All three tools feed into the Obsidian vault at C:\Users\Kyle\.openclaw\workspace\RaapTech-Vault (see Obsidian Vault Bridge).
business/morning-ops.md#cron-status | cron status morning operations 6 ollama crons paused | All 6 Ollama crons paused as of 2026-06-30 (quota conservation).
business/revenue-pricing.md | revenue pricing business services raaptech service model client | RaapTech service model, pricing, client engagement structure.
business/revenue-pricing.md#business-model | business model revenue pricing raaptech llc solo ai | RaapTech LLC = solo AI/automation consultancy (Kyle Raap).
business/revenue-pricing.md#primary-revenue-sheet-metal-werks-inc-smw | primary revenue sheet metal werks inc smw pricing | Project/retainer mix.
business/revenue-pricing.md#secondary-revenue-pipeline | secondary revenue pipeline pricing agent arcade skill marketplace | Agent Arcade — Agent-skill marketplace MVP (prototype stage).
business/revenue-pricing.md#internal-cost-centers-not-revenue | internal cost centers revenue pricing raaptech os operating | RaapTech OS — Operating system for the consultancy itself.
business/revenue-pricing.md#pricing-principles | pricing principles revenue convert project work retainer recurring | Convert project work to retainer → recurring revenue without per-project attention overhead.
business/revenue-pricing.md#revenue-path-status | revenue path status pricing | Revenue Path Status — see Revenue & Pricing.
business/toc-analysis.md | theory constraints analysis business strategy toc bottleneck raaptech | RaapTech bottleneck analysis — attention is the constraint, 5-step action plan.
business/toc-analysis.md#the-constraint | constraint theory constraints analysis attention time revenue pipeline | Attention — not time, not revenue, not pipeline.
business/toc-analysis.md#5-whys-root-cause | 5 whys root cause theory constraints analysis side | Side projects stall at 60% → Context switching costs eat delivery.
business/toc-analysis.md#constraint-chain | constraint chain theory constraints analysis attention context switching | Attention → Context switching → Delivery stalls → Revenue delayed → Cash flow depends on SMW retainer → Vulnerable to single-client concentration.
business/toc-analysis.md#action-plan | action plan theory constraints analysis | Action Plan — see Theory of Constraints Analysis.
business/toc-analysis.md#next-constraint-after-relief | next constraint relief theory constraints analysis converting agent | Converting Agent Arcade from prototype to revenue-generating product — requires shipping and selling, not building.
skills/agents-conventions.md | agent conventions roster skills agents fleet roles output | Fleet agent roles, output styles, model assignments, and operating conventions.
skills/agents-conventions.md#roster | roster agent conventions | Roster — see Agent Conventions & Roster.
skills/agents-conventions.md#memory-protocol | memory protocol agent conventions roster read soul md | Read SOUL.md — who you are.
skills/agents-conventions.md#blocker-hygiene-every-session | blocker hygiene session agent conventions roster check blockers | Check BLOCKERS for items older than 7 days.
skills/agents-conventions.md#change-governance | change governance agent conventions roster | Change Governance — see Agent Conventions & Roster.
skills/agents-conventions.md#output-style | output style agent conventions roster write mental notes | Write it down — "mental notes" don't survive sessions.
skills/anti-patterns.md | anti patterns skills error recovery failures known failure | Known failure modes, what NOT to do, and error recovery protocol.
skills/anti-patterns.md#communication-anti-patterns | communication anti patterns | Communication Anti-Patterns — see Anti-Patterns.
skills/anti-patterns.md#build-anti-patterns | build anti patterns | Build Anti-Patterns — see Anti-Patterns.
skills/anti-patterns.md#sub-agent-anti-patterns | sub agent anti patterns | Sub-Agent Anti-Patterns — see Anti-Patterns.
skills/anti-patterns.md#cost-anti-patterns | cost anti patterns | Cost Anti-Patterns — see Anti-Patterns.
skills/anti-patterns.md#error-recovery-protocol | error recovery protocol anti patterns read full | Read the FULL error.
skills/build-process.md | build process skills gate standards gated feature request | The gated build process every feature request must pass through. Stack → Scope → Audience → Overlap → Handoff.
skills/build-process.md#gate-every-build-request | gate build request process goes 5 checks writing | Every build request goes through 5 checks before writing code:.
skills/build-process.md#rule-standards-override-defaults | rule standards override defaults build process check first | Check standards/ FIRST.
skills/build-process.md#8-phase-build-loop-autonomous-builds | 8 phase build loop autonomous builds process context | Context — Read task brief, understand requirements.
skills/build-process.md#definition-of-done | definition done build process marking task complete | Before marking ANY task complete:.
skills/build-process.md#frontend-standards | frontend standards build process library discipline ui lib | Library discipline: If a UI lib exists in the project, USE IT.
skills/build-process.md#fable-5-build-rules | fable 5 build rules process fable5 repo specifically | In the fable5 repo specifically:.
skills/cole-medin-patterns.md | cole medin patterns skills agents highest signal content | Highest-signal patterns from Cole Medin's content — progressive disclosure, PRD-first, contract-first spawning, system evolution.
skills/cole-medin-patterns.md#tier-1--directly-applicable | tier 1 directly applicable cole medin patterns description | Description loaded at all times (~50-100 words, 5% of context).
skills/cole-medin-patterns.md#1-progressive-disclosure-skills | 1 progressive disclosure skills cole medin patterns description | Description loaded at all times (~50-100 words, 5% of context).
skills/cole-medin-patterns.md#2-the-5-techniques-top-agentic-engineers | 2 5 techniques top agentic engineers cole medin | PRD-First Development — comprehensive PRD as north star, not optional docs.
skills/cole-medin-patterns.md#3-agent-harness-architecture-24-hour-agent | 3 agent harness architecture 24 hour cole medin | 54% test pass rate in 24 hours, 54 coding sessions.
skills/cole-medin-patterns.md#4-agent-teams-vs-sub-agents | 4 agent teams vs sub agents cole medin | 4. Agent Teams vs Sub-Agents — see Cole Medin Patterns.
skills/cole-medin-patterns.md#5-contract-first-spawning | 5 contract first spawning cole medin patterns don | Don't launch all agents in parallel.
skills/cole-medin-patterns.md#6-harness-reliability-math | 6 harness reliability math cole medin patterns single | Single agent reliability: ~95%.
skills/cole-medin-patterns.md#7-second-brain-architecture-obsidian--claude-code | 7 second brain architecture obsidian claude code cole | Obsidian = canvas (markdown = LLM-native).
skills/cole-medin-patterns.md#8-system-evolution-pattern | 8 system evolution pattern cole medin patterns bug | After every bug fix:.
skills/cole-medin-patterns.md#mapping-to-raaptech | mapping raaptech cole medin patterns | Mapping to RaapTech — see Cole Medin Patterns.
skills/sub-agent-rules.md | sub agent rules skills agents spawning delegation contracts | How to spawn, constrain, and validate sub-agents — contract-first, fresh context, write-first.
skills/sub-agent-rules.md#core-principles | core principles sub agent rules write first research | Write-first, research-second.
skills/sub-agent-rules.md#contract-first-pattern | contract first pattern sub agent rules prevents cascading | Prevents cascading failures from missing dependencies.
skills/sub-agent-rules.md#hermes-sub-agent-rules-delegate_task | hermes sub agent rules delegate task leaf agents | Leaf agents cannot call: delegate_task, clarify, send_message, execute_code.
skills/sub-agent-rules.md#when-to-use-sub-agents-vs-direct | sub agents vs direct agent rules | When to Use Sub-Agents (vs Direct) — see Sub-Agent Rules.
skills/sub-agent-rules.md#patterns-that-work | patterns work sub agent rules research report subagent | Research → Report: Subagent researches, returns structured summary.
skills/sub-agent-rules.md#patterns-that-fail | patterns fail sub agent rules subagent starts web | Subagent starts with web search → timeouts, zero output.
integrations/github-integration.md | github integration integrations git pr gh cli auth | gh CLI auth status, repo map, PR workflow conventions.
integrations/github-integration.md#raaptech-repos | raaptech repos github integration | RaapTech Repos — see GitHub Integration.
integrations/github-integration.md#pr-workflow | pr workflow github integration branch feature description fix | Branch: feature/description or fix/description.
integrations/github-integration.md#git-rules-from-agentsmd | git rules agents md github integration line code | Every line of code MUST reach GitHub.
integrations/google-oauth-bridge.md | google oauth bridge integrations sync credentials knowledge workspace | How to use Google OAuth credentials for knowledge sync, Google Workspace, and cloud operations.
integrations/google-oauth-bridge.md#scopes-available | scopes available google oauth bridge | Scopes Available — see Google OAuth Bridge.
integrations/google-oauth-bridge.md#what-this-unlocks | unlocks google oauth bridge cloud platform scope agents | With cloud-platform scope, agents can:.
integrations/google-oauth-bridge.md#usage-pattern | usage pattern google oauth bridge | Usage Pattern — see Google OAuth Bridge.
integrations/google-oauth-bridge.md#python-recommended | python recommended google oauth bridge | Python (recommended) — see Google OAuth Bridge.
integrations/google-oauth-bridge.md#hermes-cli | hermes cli google oauth bridge | Hermes CLI — see Google OAuth Bridge.
integrations/google-oauth-bridge.md#sync-protocol | sync protocol google oauth bridge agent reads concept | Agent reads concept from brain.
integrations/google-oauth-bridge.md#brain--google-drive-push | brain google drive push oauth bridge agent reads | Agent reads concept from brain.
integrations/google-oauth-bridge.md#google-drive--brain-pull | google drive brain pull oauth bridge agent lists | Agent lists files in designated Drive folder.
integrations/google-oauth-bridge.md#security-rules | security rules google oauth bridge never print access | Never print the access token or refresh token.
integrations/messaging-gateways.md | messaging gateways integrations telegram discord hermes platform signal | Hermes messaging platform integrations — Telegram, Discord, Signal, WhatsApp, and routing rules.
integrations/messaging-gateways.md#overview | overview messaging gateways hermes connects platforms gateway system | Hermes connects to messaging platforms via the gateway system.
integrations/messaging-gateways.md#active-platforms | active platforms messaging gateways | Active Platforms — see Messaging Gateways.
integrations/messaging-gateways.md#cron-delivery | cron delivery messaging gateways jobs run user present | Cron jobs run with no user present.
integrations/messaging-gateways.md#gateway-troubleshooting | gateway troubleshooting messaging gateways common issues | See messaging-gateway-troubleshooting for common issues:.
integrations/tradingview-mcp.md | tradingview mcp integration integrations trading jackson bridge cdp | TradingView MCP Jackson bridge — CDP connection, Lorentzian indicators, morning brief.
integrations/tradingview-mcp.md#key-capabilities | key capabilities tradingview mcp integration | Key Capabilities — see TradingView MCP Integration.
integrations/tradingview-mcp.md#indicators | indicators tradingview mcp integration lorentzian premium primary ai | Lorentzian Premium — Primary AI Edge indicator.
integrations/tradingview-mcp.md#morning-brief-flow | morning brief flow tradingview mcp integration tv launch | mcp_tradingview_tv_launch — Start TV Desktop.
integrations/tradingview-mcp.md#integration-with-ai-trading-council | integration ai trading council tradingview mcp strategy rules | See AI Trading Council for strategy rules and allocation.
research/fable5-prompting-patterns.md | fable 5 prompting patterns research fable5 cost synthesis | Synthesis of Fable 5 prompting best practices — habits, routing, loop engineering, cost lessons.
research/fable5-prompting-patterns.md#the-6-habits | 6 habits fable 5 prompting patterns give agents | Give the why — agents perform better when they understand purpose and audience.
research/fable5-prompting-patterns.md#when-to-use-fable | fable 5 prompting patterns hard bounded outcomes generic | Hard bounded outcomes (not generic "make it better").
research/fable5-prompting-patterns.md#when-not-to-use-fable | fable 5 prompting patterns lint fixes | Lint fixes.
research/fable5-prompting-patterns.md#loop-engineering-boxminingai--superbash-pattern | loop engineering boxminingai superbash pattern fable 5 prompting | Instead of prompt → hope → manual review:.
research/fable5-prompting-patterns.md#costperformance-framing-asapguide--tech-with-tim | cost performance framing asapguide tech tim fable 5 | Fable outperformed Opus on complex UI/visual/code tasks.
research/fable5-prompting-patterns.md#research-backed-lessons | research backed lessons fable 5 prompting patterns | Research-Backed Lessons — see Fable 5 Prompting Patterns.
references/memories.md | references memories brain save durable facts saved domain | Durable facts saved into the references domain via brain save.
references/memories.md#brain-retrieval-cli-2026-07-07 | brain retrieval cli 2026 07 references memories bundle | The brain bundle has a deterministic retrieval CLI at scripts/brain.py — use 'python scripts/brain.py ask' before opening files, 'brain save' to store durable ...
references/obsidian-vault.md | obsidian vault bridge knowledge layer para verification maps | Maps raaptech-brain domains to the local RaapTech-Vault Obsidian workspace for capture, verification, and deeper context.
references/obsidian-vault.md#open-the-vault-on-this-station | open vault station obsidian bridge folder | Open Obsidian → Open folder as vault.
references/obsidian-vault.md#obsidian-recommended | obsidian recommended vault bridge open folder | Open Obsidian → Open folder as vault.
references/obsidian-vault.md#explorer--terminal | explorer terminal obsidian vault bridge | Explorer / terminal — see Obsidian Vault Bridge.
references/obsidian-vault.md#github-private | github private obsidian vault bridge repo raaptechllc raaptech | Repo: RaapTechllc/raaptech-vault.
references/obsidian-vault.md#domain-mapping--brain--vault | domain mapping brain vault obsidian bridge table building | Use this table when building out brain structure or verifying that vault notes still align with brain concepts.
references/obsidian-vault.md#key-vault-entry-points | key vault entry points obsidian bridge | Key vault entry points — see Obsidian Vault Bridge.
references/obsidian-vault.md#verification-workflow | verification workflow obsidian vault bridge run brain repo | Run from the brain repo root:.
references/obsidian-vault.md#when-to-add-to-brain-vs-vault | add brain vs vault obsidian bridge | When to add to brain vs vault — see Obsidian Vault Bridge.
references/obsidian-vault.md#stale-path-note | stale path note obsidian vault bridge older docs | Older docs referenced E:\openclaw\Openclaw.
