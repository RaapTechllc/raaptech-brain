---
type: Reference
title: Sub-Agent Rules
description: How to spawn, constrain, and validate sub-agents — contract-first, fresh context, write-first.
resource: C:/Users/Kyle/.openclaw/workspace/standards/SUB-AGENT-RULES.md
tags: [skills, sub-agents, spawning, delegation, contracts]
timestamp: 2026-07-07T12:00:00Z
---

# Sub-Agent Rules

## Core Principles

1. **Write-first, research-second.** Sub-agents that start with web searches timeout with ZERO output.
2. **Fresh context only.** Don't dump session history. Write a brief to a file, point the agent at it.
3. **Contract-first spawning.** DB → Backend → Frontend. Never all parallel.
4. **15 min timeout max.** Most good work finishes in 5-10 min.
5. **Sub-agents get AGENTS.md + TOOLS.md ONLY.** No soul, no identity, no user context, no memory. If they need something, encode it in the task prompt.

## Contract-First Pattern

```
Database agent runs FIRST → produces schema contract
     ↓
Backend agent gets DB contract → produces API contract
     ↓
Frontend agent gets API contract → builds UI
```

Prevents cascading failures from missing dependencies. Never launch all agents in parallel.

## Hermes Sub-Agent Rules (delegate_task)

- **Leaf agents** cannot call: delegate_task, clarify, send_message, execute_code
- **Orchestrator agents** can spawn their own workers (max_spawn_depth=1)
- **Isolation:** Each subagent gets its own terminal session
- **Results:** Only final summary returns — intermediate tool output is discarded
- **Self-reports are not verified** — verify side-effects yourself

## When to Use Sub-Agents (vs Direct)

| Use Sub-Agents When | Use Direct When |
|---|---|
| Reasoning-heavy subtasks (debug, review) | Single tool call |
| Tasks would flood your context | Mechanical multi-step work |
| Parallel independent workstreams | Tasks needing user input |

## Patterns That Work

- **Research → Report:** Subagent researches, returns structured summary
- **Parallel audit:** 3 subagents audit different aspects simultaneously
- **Build + Test:** Subagent builds artifact, parent verifies with tests

## Patterns That Fail

- Subagent starts with web search → timeouts, zero output
- Subagent asked to "implement feature X" with no context → hallucination
- All 3 subagents building same module → merge conflicts
- Subagent modifies shared state → race conditions
