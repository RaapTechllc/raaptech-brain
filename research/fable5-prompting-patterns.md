---
type: Reference
title: AI Developer Workflows and Fable Prompting Patterns
description: Fable 5 prompting practices reframed inside AI developer workflows: agents + deterministic code + human judgment.
resource: C:/Users/Kyle/CC/fable5/research/2026-07-02-last30days-fable5-synthesis.md
superseded_concept: "Loop engineering is a verification-repair pattern, not the operating model."
tags: [research, fable5, prompting, cost, patterns, ai-developer-workflows]
timestamp: 2026-07-13T00:00:00Z
---

# AI Developer Workflows and Fable Prompting Patterns

**Primary framing:** An **AI developer workflow (ADW)** is a reproducible end-to-end path for a class of work. It combines **engineers** (intent, judgment, approvals), **agents** (bounded reasoning/work), and **deterministic code** (routing, state, validation, evidence). A *loop* is one feedback edge—usually validator failure returning evidence to a builder—not the whole system.

**Reframing source:** [IndyDevDan — “FORGET Loop Engineering. Agentic Engineering is about THIS”](indydevdan-ai-developer-workflows.md).

## The 6 Habits

1. **Give the why** — agents perform better when they understand purpose and audience.
2. **Negative prompt / non-goals** — explicitly state what NOT to build; prevents over-engineering.
3. **Act when you have enough info** — do not ask permission for obvious, pre-authorized steps.
4. **Make it prove it** — verification loop: write → run → validate → fix.
5. **Don't request hidden reasoning** — extended thinking burns tokens without output-quality gains for routine work.
6. **Say less** — short prompts with clear constraints outperform verbose wishlists.

## The Correct Unit: AI Developer Workflow

A workflow must explicitly declare:

- **Trigger and work class:** chore, feature, bug, hotfix, research, ops check.
- **Input and output contracts:** what enters, required artifacts, evidence returned.
- **Actors and isolation:** which human/agent/code node acts, in which worktree/sandbox.
- **Deterministic gates:** tests, lint, typecheck, policy, CI, artifact checks.
- **Routing and retry policy:** who gets failures, maximum attempts, escalation rules.
- **Risk, budget, and approval:** model tier, token/compute cap, required human gate.
- **Measurement:** duration, cost, pass rate, rework, failure categories.

## Loop Engineering Is a Subroutine, Not Strategy

The previous useful pattern remains:

```
Build agent → deterministic validation → failure evidence → patch agent → revalidate
```

Use it **inside** a named workflow. It must have an explicit validator, bounded retry count, preserved evidence, and an escalation owner. Do not treat “keep prompting until it passes” as autonomous engineering.

## When to Use Fable / a High-Capability Build Agent

- Hard bounded outcomes—not generic “make it better.”
- Multi-file fixes where the exact change set is unknown.
- A workflow needs contextual reasoning before deterministic verification.
- Tasks where an agent must read significant local context to locate the change.

## When NOT to Use Fable / a High-Capability Build Agent

- Deterministic lint/format/typecheck/test execution.
- Copy polish.
- Whole-repo rewrites.
- Status checks and routine ops.
- Work that a cheaper specialized model can perform against a clear contract.

## Cost / Performance Rules

- The harness matters as much as the raw model.
- Use deterministic code for deterministic work: it is faster, repeatable, auditable, and token-free.
- Match model and workflow to risk: cheap/workhorse for chores; stronger scout/planner for ambiguity; parallel isolated candidates only where urgency justifies cost.
- Retrying an expensive model without new failure evidence is waste, not a workflow.

## Research-Backed Lessons

| Lesson | Source |
|---|---|
| Effort parameter matters—use it for hard tasks | Anthropic docs |
| Progress grounding reduces drift | Anthropic docs |
| Memory protocol (read pointer index) prevents context bloat | OpenClaw AGENTS.md |
| Sub-agent isolation improves reliability and parallelism | Anthropic docs + experience |
| Autonomy calibration—too much drifts, too little blocks | Anthropic docs |
| Validation loops are one component of a larger software factory | IndyDevDan video (2026-07-13 capture) |
