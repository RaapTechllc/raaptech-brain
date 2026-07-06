---
type: Reference
title: Cole Medin Patterns
description: Highest-signal patterns from Cole Medin's content — progressive disclosure, PRD-first, contract-first spawning, system evolution.
resource: C:/Users/Kyle/.openclaw/workspace/research/cole-medin-brain-extract.md
tags: [skills, cole-medin, patterns, agents]
timestamp: 2026-07-06T16:30:00Z
---

# Cole Medin Patterns

**Source:** [cole-medin-brain-extract.md](C:/Users/Kyle/.openclaw/workspace/research/cole-medin-brain-extract.md) — 25 videos, 143+ chunks extracted 2026-03-16.

## Tier 1 — Directly Applicable

### 1. Progressive Disclosure (Skills)
- **Description** loaded at all times (~50-100 words, 5% of context)
- **SKILL.md** loaded on-demand (~300-500 lines, 30% of context)
- **Reference docs** loaded only if SKILL.md points to them
- "Drop a skill in a folder" = instant capability
- Works with ANY framework, not just Claude Code

### 2. The 5 Techniques (Top Agentic Engineers)
1. **PRD-First Development** — comprehensive PRD as north star, not optional docs
2. **Modular Rules Architecture** — global rules <200 lines, task-specific rules in reference/ folder
3. **Commandify Everything** — any prompt used 2+ times becomes a reusable command
4. **Context Reset** — plan in one session, output structured plan doc, execute in FRESH session
5. **System Evolution** — after fixing bugs, ask "what rules would prevent this?" Update system

### 3. Agent Harness Architecture (24-Hour Agent)
```
PRD → Initializer Agent → feature_list.json + scaffold + git init + progress.md
     → Coding Agent Loop (fresh context each iteration):
        1. Read progress.md + feature_list.json
        2. Analyze codebase
        3. Run regression tests
        4. Implement NEXT feature
        5. Validate (tests + visual)
        6. Commit to git
        7. Update progress.md
        8. Update feature_list.json
```
- 54% test pass rate in 24 hours, 54 coding sessions
- Uses Claude Agent SDK (programmatic, not CLI)

### 4. Agent Teams vs Sub-Agents

| Factor | Sub-Agents | Agent Teams |
|---|---|---|
| **Best for** | Research, analysis, web search | Implementation requiring coordination |
| **Communication** | None (isolated, summaries only) | Shared task list, peer-to-peer |
| **Token cost** | Lower (1x) | Higher (2-4x overhead) |
| **Context isolation** | Full | Shared |
| **Reliability** | Higher (isolated failures) | Lower (hallucinations, misconfigs) |

### 5. Contract-First Spawning
- Don't launch all agents in parallel
- Database agent runs FIRST → produces schema contract
- Backend agent waits for DB contract → then runs
- Frontend agent waits for backend API contract
- Prevents cascading failures from missing dependencies

### 6. Harness Reliability Math
- Single agent reliability: ~95%
- 20-step harness: 0.95^20 = 36% overall
- Need 99.9%+ per-step for complex builds
- Solution: self-validation + rollbacks + human checkpoints

### 7. Second Brain Architecture (Obsidian + Claude Code)
- Obsidian = canvas (markdown = LLM-native)
- Claude Code = engine (file access, web search, terminal)
- Skills = capabilities (PowerPoint, research, diagrams)
- MCP bridge skill: converts MCP servers into skills
- Brand voice generator: personalizes all output

### 8. System Evolution Pattern
After every bug fix:
1. Ask: "What in our rules/processes would have prevented this?"
2. Agent analyzes execution vs planned rules
3. Identifies systemic weakness (not just symptom)
4. Updates: global rules, reference docs, commands/workflows
5. Never just patch — always strengthen the system

## Mapping to RaapTech

| Cole's Concept | RaapTech Equivalent | Status |
|---|---|---|
| PRD-first | write-prd skill | ✅ Done |
| Modular rules | skills/ + AGENTS.md | ✅ Done |
| Commandify | Hermes crons + commands | ⚠️ Could be more structured |
| Context reset | Sub-agent fresh context rule | ✅ Done |
| System evolution | Error recovery protocol | ⚠️ Need post-fix "strengthen system" step |
| Agent harness | AutoLab experiment loop | ⚠️ Could apply to all builds |
| Contract-first spawning | Not implemented | ❌ New pattern to adopt |
| Human injection points | Kyle Telegram approval gate | ⚠️ Not generalized |