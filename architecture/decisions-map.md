---
type: Reference
title: Architecture Decisions Map
description: Summary of all 27 ratified RaapTech OS architecture decisions with source links.
resource: C:/Users/Kyle/RaapTech_OS/docs/ARCHITECTURE_DECISIONS.md
tags: [architecture, decisions, raaptech-os]
timestamp: 2026-07-06T16:30:00Z
---

# Architecture Decisions Map

**Source of truth:** [ARCHITECTURE_DECISIONS.md](C:/Users/Kyle/RaapTech_OS/docs/ARCHITECTURE_DECISIONS.md) in RaapTech_OS repo.
**Status:** All 27 decisions ratified. Config aligned via PR #4. Implementation in progress via Session 13 sprint.

## Decision Groups

### G-ARCH: Architecture & Provider (4 decisions)
| ID | Decision | Status |
|---|---|---|
| G-ARCH-01 | OpenRouter / Multi-provider (not local-only Ollama) | ✅ Implemented in config/models.yaml |
| G-ARCH-02 | GLM-5.2:cloud as Primary Orchestrator | ✅ Active |
| G-ARCH-03 | DeepSeek V4 Flash as Executor Model | ✅ Active |
| G-ARCH-04 | Local FS + Git + Obsidian for knowledge layer | ✅ Active |

### G-SEC: Security (3 decisions)
| ID | Decision | Status |
|---|---|---|
| G-SEC-01 | Audit mutating actions only (not every call) | ✅ Implemented in config/mcp_servers.yaml |
| G-SEC-02 | Standard DLP patterns + configurable client-specific patterns | ✅ Implemented in config/dlp_patterns.yaml |
| G-SEC-03 | Independent kill switch per MCP server | ✅ Implemented |

### G-ARCH (continued): Engine Design
| ID | Decision | Status |
|---|---|---|
| G-ARCH-09 | JSONL write + SQLite query for audit logs | ✅ Implemented in raaptech/audit.py |
| G-ARCH-10 | Hard daily cap of $50/day | ✅ Implemented in raaptech/cost.py |

### G-ROT: Rotation & Maintenance
| ID | Decision | Status |
|---|---|---|
| G-ROT-01 | Adopt Mark Kashef's rot rates exactly | ✅ Implemented |

**Full 27/27 decisions:** See [source document](C:/Users/Kyle/RaapTech_OS/docs/ARCHITECTURE_DECISIONS.md).

## Implementation Status

- PR #3: Master Engine merged (audit, cost, DLP, killswitch, rot primitives)
- PR #4: Config sweep aligned to ratified decisions
- Session 13: First production workflow sprint (in queue)
- `raaptech doctor`: passes, detects 27+ ratified decisions
- Tests: 40 passing