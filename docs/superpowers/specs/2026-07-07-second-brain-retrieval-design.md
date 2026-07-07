---
type: Specification
title: Deterministic Retrieval System (Design)
description: Approved design for the brain.py retrieval CLI, catalogue, benchmark, and dashboard.
tags: [spec, retrieval, brain]
timestamp: 2026-07-07T00:00:00Z
---

# RaapTech Brain — Deterministic Retrieval System (Design)

Date: 2026-07-07 · Status: Approved by Kyle

## Goal

Add the retrieval machinery the knowledge bundle lacks: a deterministic, zero-dependency
lookup path (code before model), an always-true one-line-per-fact catalogue, an atomic
memory-save command, a rerunnable benchmark, and a human dashboard. Follows the
RoboNuggets 5-principle guide.

## Decisions (from interview)

- **Primary consumer:** Claude Code sessions (fleet agents adopt later).
- **Write path:** this repo only — `brain save` is the single write entry; vault untouched.
- **Scoring:** pure-stdlib keyword index; no embeddings, no SQLite, no deps.
- **Scope:** core retrieval + save + catalogue, benchmark harness, housekeeping fixes,
  plus a human-facing static dashboard. Prior-art study pass skipped.

## Components

### 1. `catalog.md` (repo root)
One line per retrievable section: `path#anchor | keywords | one-sentence description`.
Bootstrapped by scanning every domain file's headings + frontmatter descriptions.
Maintained by `brain save` (append) and `brain reindex` (full rebuild).
`okf-validate.py` gains a catalogue-consistency check (every line resolves; every
domain heading is catalogued) so it can never silently drift.

### 2. `scripts/brain.py` — single CLI, stdlib only
- `brain ask "question"` — the ladder: keywords (stopword strip) → score every
  catalogue line WITHOUT opening files (weighted: title > keywords > description) →
  open only the single top file → extract only the winning section → follow at most
  one pointer link if the section defers elsewhere → print an evidence block.
- `brain save --domain <d> --title "..." "fact"` — writes fact into the right domain
  file (dated section) or new OKF-frontmattered file, appends catalogue line, touches
  `log.md`. One step, atomic — index can't drift.
- `brain reindex` — rebuild catalogue from scratch.
- `brain bench` — run `scripts/bench-questions.json` (~10 real questions with
  expected-answer substrings); report hit/miss, latency, evidence-block token count
  vs naive whole-file read, as a table.
- `brain html` — generate self-contained `dashboard.html`: client-side search over
  embedded catalogue JSON, domain map, latest bench results. Template in
  `scripts/dashboard_template.html`. No external requests (CSP-safe).

### 3. Routing note
Create `CLAUDE.md` in repo root: check catalogue first via `brain ask`, open files
second; save durable facts with `brain save`; never edit `catalog.md` by hand.

### 4. Housekeeping
Strip `sessions/index.md` frontmatter; add `scripts/index.md`; rewrite
`scripts/README.md` to match reality (drop never-built bash scripts, document brain.py);
add `requirements.txt` (deps for sync/vault scripts only; brain.py needs none);
add `references` to vault-bridge DOMAIN_MAP.

## Error handling
Unknown domain → list valid ones. No hit above threshold → say so, suggest nearest
domain index; never guess. Malformed catalogue lines → skip with warning.

## Testing
`brain bench` is the regression suite; okf-validate catalogue check guards drift.
Acceptance: all bench questions retrieve the correct file/section; evidence block is
clearly smaller than naive reads; okf-validate passes clean.
