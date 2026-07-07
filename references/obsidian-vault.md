---
type: Reference
title: Obsidian Vault Bridge
description: Maps raaptech-brain domains to the local RaapTech-Vault Obsidian workspace for capture, verification, and deeper context.
resource: C:/Users/Kyle/.openclaw/workspace/RaapTech-Vault
tags: [obsidian, vault, knowledge-layer, para, verification]
timestamp: 2026-07-07T04:45:00Z
---

# Obsidian Vault Bridge

**Decision:** G-ARCH-04 — Local FS + Git + Obsidian for knowledge layer.

The brain **synthesizes and links**. The vault **captures, expands, and holds working notes**. Neither replaces the other.

| Layer | Repo / path | Role |
|---|---|---|
| **Brain (OKF)** | `C:/Users/Kyle/CC/raaptech-brain` | Traversable bundle for agents — decisions, topology, integrations |
| **Vault (PARA)** | `C:/Users/Kyle/.openclaw/workspace/RaapTech-Vault` | Kyle + fleet workspace — projects, runbooks, daily notes, mentor brains |
| **Engine code** | `C:/Users/Kyle/RaapTech_OS` | Implementation source of truth |
| **Operating repo** | `C:/Users/Kyle/CC/fable5` | Session prompts, sprint queue, run ledger |

## Open the vault on this station

### Obsidian (recommended)

1. Open Obsidian → **Open folder as vault**
2. Select: `C:\Users\Kyle\.openclaw\workspace\RaapTech-Vault`
3. Vault name in Obsidian: **RaapTech-Vault**

Or use the URI (after vault is registered once in Obsidian):

```
obsidian://open?vault=RaapTech-Vault
```

### Explorer / terminal

```powershell
# Open in File Explorer
explorer "C:\Users\Kyle\.openclaw\workspace\RaapTech-Vault"

# Open in VS Code / Cursor
code "C:\Users\Kyle\.openclaw\workspace\RaapTech-Vault"
```

### GitHub (private)

- **Repo:** [RaapTechllc/raaptech-vault](https://github.com/RaapTechllc/raaptech-vault)
- **Local clone:** same path as above (`.openclaw/workspace/RaapTech-Vault`)

## Domain mapping — brain ↔ vault

Use this table when building out brain structure or verifying that vault notes still align with brain concepts.

| Brain domain | Vault PARA folder(s) | What lives in vault vs brain |
|---|---|---|
| [Architecture](/architecture/) | `20-Areas/Infrastructure/`, `30-Resources/Tech-Reference/` | Vault: network topology, docker services, rollout notes. Brain: ratified decisions, model routing, cost/DLP policy |
| [Fleet](/fleet/) | `20-Areas/Fleet-Ops/`, `60-Fleet/` | Vault: per-agent profiles, blockers, recovery runbooks. Brain: topology summary, service registry |
| [Business](/business/) | `20-Areas/Business/`, `20-Areas/Trading/` | Vault: playbooks, client context, trading MOCs. Brain: morning ops stack, council decisions |
| [Integrations](/integrations/) | `20-Areas/Integrations/`, `20-Areas/Infrastructure/n8n-workflows.md` | Vault: setup notes, workflow specs. Brain: OAuth bridge, MCP wiring |
| [Skills](/skills/) | `30-Resources/Brains/`, `30-Resources/Dynamous/` | Vault: mentor brain entries, course extracts. Brain: Cole Medin patterns, AGENTS conventions |
| [Sessions](/sessions/) | `50-Daily/`, `60-Fleet/*/daily/` | Vault: daily agent logs. Brain: sprint tracker, run ledger (links to fable5) |
| [Research](/research/) | `30-Resources/Market-Intel/`, `00-Inbox/` | Vault: raw research, competitor notes. Brain: archived synthesis (when populated) |

## Key vault entry points

| Topic | Vault path |
|---|---|
| Vault architecture spec | [obsidian-vault-architecture.md](file:///C:/Users/Kyle/.openclaw/workspace/RaapTech-Vault/20-Areas/Infrastructure/obsidian-vault-architecture.md) |
| Fleet registry | [fleet-registry.md](file:///C:/Users/Kyle/.openclaw/workspace/RaapTech-Vault/20-Areas/Fleet-Ops/fleet-registry.md) |
| Network topology | [network-topology.md](file:///C:/Users/Kyle/.openclaw/workspace/RaapTech-Vault/20-Areas/Infrastructure/network-topology.md) |
| Mission Control status | [STATUS-2026-03-09.md](file:///C:/Users/Kyle/.openclaw/workspace/RaapTech-Vault/10-Projects/Mission-Control/STATUS-2026-03-09.md) |
| Trading MOC | [MOC-Trading.md](file:///C:/Users/Kyle/.openclaw/workspace/RaapTech-Vault/20-Areas/Trading/MOC-Trading.md) |
| Vault README | [README.md](file:///C:/Users/Kyle/.openclaw/workspace/RaapTech-Vault/README.md) |

## Verification workflow

Run from the brain repo root:

```bash
# Check vault is reachable + domain mapping health
python scripts/vault-bridge.py --status

# List vault notes that match a brain topic (e.g. fleet, trading, mcp)
python scripts/vault-bridge.py --search fleet

# Compare brain frontmatter titles against vault note filenames (warn on gaps)
python scripts/vault-bridge.py --verify

# Full report
python scripts/vault-bridge.py --report
```

Pair with OKF validation:

```bash
python scripts/okf-validate.py
python scripts/vault-bridge.py --verify
```

## When to add to brain vs vault

| Add to **vault** when… | Add to **brain** when… |
|---|---|
| Note is in flux, daily, or agent-generated | Concept is stable and agent-traversable |
| Full spec, runbook, or project folder | Summary + link to source repo or vault path |
| Personal / fleet working notes | Ratified decision or cross-domain navigation |
| Mentor brain chunks, research inbox | Synthesized pattern or integration map |

## Stale path note

Older docs referenced `E:\openclaw\Openclaw`. The active vault on this station is **`C:\Users\Kyle\.openclaw\workspace\RaapTech-Vault`**. Morning Brief and Super Brain should target this path.
