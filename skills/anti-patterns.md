---
type: Reference
title: Anti-Patterns
description: Known failure modes, what NOT to do, and error recovery protocol.
tags: [skills, anti-patterns, error-recovery, failures]
timestamp: 2026-07-07T12:00:00Z
---

# Anti-Patterns

## Communication Anti-Patterns

| Anti-Pattern | Why It Fails | Do Instead |
|---|---|---|
| No async promises | "I'll get back to you" wastes time | Give 60% now, flag the 40% gap |
| Silent failures | Blocks go unnoticed | Always surface blockers immediately |
| Same-command retries | Same input → same error | Diagnose → adapt → try differently (max 3) |
| Idea without capture | Worth saying = worth writing | Capture in IDEAS.md or memory |
| Theory > execution | "Here's how you could..." | Execute it, show the result |
| Filler/hedging | "I think maybe perhaps..." | Lead with the answer, then explain |

## Build Anti-Patterns

| Anti-Pattern | Why It Fails | Do Instead |
|---|---|---|
| Custom when lib exists | Reimplementing Shadcn modals | Wrap/style lib primitives |
| No dead elements | UI with unclear purpose = noise | Every element must have calculated purpose |
| Template look | Generic = rejected | Custom layout reasoning |
| No verification | "It should work" | Run it, visit the URL, check output |
| Local-only commits | Code doesn't count if not on GitHub | Push immediately after every phase |
| Skipping the gate | Building before checking standards | Stack → Scope → Audience → Overlap → Handoff |

## Sub-Agent Anti-Patterns

| Anti-Pattern | Why It Fails | Do Instead |
|---|---|---|
| Research-first start | Web search timeouts = zero output | Write brief, embed all context in task |
| Session dump | History = noise for fresh agent | Write to file, point agent at it |
| All parallel | Missing dependencies cascade | Contract-first: DB → Backend → Frontend |
| No timeout | Agents drift indefinitely | 15 min max, most work in 5-10 |
| Identity bleed | Giving soul/memory to sub-agents | Just AGENTS.md + TOOLS.md + task prompt |

## Cost Anti-Patterns

| Anti-Pattern | Why It Fails | Do Instead |
|---|---|---|
| Anthropic on crons | Rate limits + cost explosion | DashScope/Ollama for all 24/7 tasks |
| Fable on lint fixes | Expensive model on trivial work | Route to cheaper model |
| Default model everywhere | Burns quota on status checks | Explicit `--model` on every cron |
| Thinking mode for routine | Wasted tokens on simple tasks | Thinking OFF for routine work |
| Google on research | Hallucinates, won't follow directions | Use Ollama Cloud for subagents |

## Error Recovery Protocol

1. Read the FULL error. Classify: syntax, permission, logic, timeout.
2. Change approach based on diagnosis.
3. Retry with variation (max 3). Same error twice = wrong approach, not retry problem.
4. After 3 fails: document in `failures.md`, escalate, ship what you CAN.
5. After every fix: ask "what rule/process would prevent this?" Update the system.
