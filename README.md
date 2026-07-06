# RaapTech Brain

Consolidated OKF v0.1 knowledge bundle for RaapTech LLC. Any AI agent can traverse this without special tooling.

## What this is

The single traversable knowledge layer that links all RaapTech repos, fleet nodes, business ops, and integrations. It synthesizes and links — it does not duplicate. Source-of-truth files live in their respective repos. Concepts here explain the *what* and *why*; follow `resource` links for the *how*.

## What this is NOT

- A replacement for `fable5/` (that's the Fable 5 operating repo — session prompts, run logs, sprint queue)
- A replacement for `RaapTech_OS/` (that's the engine code)
- A replacement for `.openclaw/workspace/` (that's agent memory and daily notes)
- A duplicate of any source repo

## Relationship to other repos

| Repo | Relationship |
|---|---|
| `RaapTech_OS/` | Brain links to architecture decisions, model routing, config |
| `fable5/` | Brain links to session catalog, sprint tracker; fable5 is the *operating* repo, brain is the *knowledge* layer |
| `.openclaw/workspace/` | Brain links to AGENTS.md, fleet roster, Cole Medin extract |
| `raaptech-rde/` | Brain links to deliverable engine (when cloned) |
| `smw-cloud-main/` | Brain links to Agent Arcade, SMW ops |

## Quick start

```bash
# Traverse the brain
cd C:/Users/Kyle/CC/raaptech-brain
cat index.md

# Sync with Google Drive
python scripts/sync-google-drive.py --pull

# Validate OKF conformance
python scripts/okf-validate.py
```

## Structure

```
raaptech-brain/
├── index.md              # Root entry point
├── log.md                # Change history
├── README.md             # This file
├── .gitignore
├── scripts/              # Automation scripts
│   ├── sync-google-drive.py
│   └── okf-validate.py
├── architecture/         # 27 decisions, model routing, cost, DLP, MCP
├── sessions/             # Sprint queue, run ledger, session catalog
├── fleet/                # Topology, services, backups, monitoring
├── business/             # Morning ops, TOC, revenue, trading
├── skills/               # Cole Medin patterns, AGENTS.md conventions
├── integrations/         # Google OAuth, GitHub, TradingView, messaging
├── research/             # Archived research synthesis
└── references/           # External specs, brain extracts
```