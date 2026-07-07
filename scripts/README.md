---
type: Reference
title: Scripts
description: Maintenance and operational scripts for the brain repository.
tags: [scripts, maintenance, validation, links]
timestamp: 2026-07-07T12:00:00Z
---

# Scripts

## validate-links.sh

**Status:** Planned (referenced in architecture index)

Validates internal wiki-style links across all markdown files in the brain.
Ensures no broken references after reorganization.

**Location:** TBD — will be created at `C:\Users\Kyle\CC\raaptech-brain\scripts\validate-links.sh`

## Planned Scripts

| Script | Purpose | Status |
|---|---|---|
| `validate-links.sh` | Check all internal links resolve | Planned |
| `sync-from-vault.sh` | Pull latest vault notes as brain references | Planned |
| `sync-from-fable5.sh` | Pull latest fable5 status/runs as brain summaries | Planned |
| `generate-index.sh` | Auto-generate table-of-contents for each domain index | Planned |

## Usage

All scripts should:
- Run from repo root: `bash scripts/<script>.sh`
- Be bash-compatible (git-bash on Windows)
- Report exit code 0 on success, non-zero on failure
- Print validation errors with file paths and line numbers
