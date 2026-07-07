---
type: Reference
title: Fable 5 Prompting Patterns
description: Synthesis of Fable 5 prompting best practices — habits, routing, loop engineering, cost lessons.
resource: C:/Users/Kyle/CC/fable5/research/2026-07-02-last30days-fable5-synthesis.md
tags: [research, fable5, prompting, cost, patterns]
timestamp: 2026-07-07T12:00:00Z
---

# Fable 5 Prompting Patterns

**Source:** Research synthesis from Anthropic docs, creator videos, and user testing (2026-07-02).

## The 6 Habits

1. **Give the why** — agents perform better when they understand purpose and audience
2. **Negative prompt / non-goals** — explicitly state what NOT to build (kills 70% of over-engineering)
3. **Act when you have enough info** — don't ask permission for obvious steps
4. **Make it prove it** — verification loop: write → run → validate → fix
5. **Don't request hidden reasoning** — extended thinking burns tokens without output quality gains for routine work
6. **Say less** — shorter prompts with clear constraints outperform verbose wishlists

## When to Use Fable

- Hard bounded outcomes (not generic "make it better")
- Multi-file fixes where you don't know the exact change set
- Anything that needs a verification loop (build → test → validate → repeat)
- Tasks that need the model to read a lot of context to find the one thing

## When NOT to Use Fable

- Lint fixes
- Copy polish
- Whole-repo rewrites
- Status checks and routine ops
- Anything a cheaper model can do with a clear brief

## Loop Engineering (BoxminingAI / Superbash Pattern)

Instead of prompt → hope → manual review:

```
One-shot prompt → Validation harness → Patch-until-pass
```

- First prompt produces full implementation
- Headless browser checks UI artifacts
- Test suite validates API contracts
- Only patch failures, don't rewrite
- Cost warning: looping on expensive models gets expensive fast

## Cost/Performance Framing (AsapGuide / Tech With Tim)

- Fable outperformed Opus on complex UI/visual/code tasks
- But Opus was "good enough" for routine app reconstruction
- The coding harness matters as much as the raw model
- Cheaper specialized models beat expensive generalists on focused work

## Research-Backed Lessons

| Lesson | Source |
|---|---|
| Effort parameter matters — use it for hard tasks | Anthropic docs |
| Progress grounding reduces drift | Anthropic docs |
| Memory protocol (read pointer index) prevents context bloat | OpenClaw AGENTS.md |
| Sub-agent isolation = better results | Anthropic docs + experience |
| Autonomy calibration — too much = drift, too little = blocks | Anthropic docs |
