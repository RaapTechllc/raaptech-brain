---
okf_version: "0.1"
type: Bundle
title: RaapTech Brain
description: Consolidated knowledge bundle for RaapTech LLC — architecture, fleet, sessions, business ops, skills, and integrations. Any AI agent can traverse this without special tooling.
tags: [raaptech, brain, okf, knowledge-bundle]
timestamp: 2026-07-06T16:30:00Z
---

# RaapTech Brain

This is the single traversable knowledge bundle for RaapTech LLC. Start here, follow links, drill into domains.

**Design principle:** This bundle synthesizes and links — it does not duplicate. Source-of-truth files live in their respective repos. Concepts here explain the *what* and *why*; follow `resource` links for the *how* (code, config, run logs).

## Domains

* [Architecture](/architecture/) — 27 ratified decisions, model routing, cost policy, DLP, MCP servers, kill switches
* [Sessions](/sessions/) — Fable 5 sprint queue, run ledger, session catalog, quota tracking
* [Fleet](/fleet/) — Topology, services, backups, monitoring, Tailscale map
* [Business](/business/) — Morning ops, TOC analysis, revenue, onboarding, client work
* [Skills & Standards](/skills/) — Cole Medin patterns, AGENTS.md conventions, build process, sub-agent rules
* [Integrations](/integrations/) — Google OAuth bridge, GitHub, TradingView, messaging gateways
* [Research](/research/) — Archived research synthesis, market data, paper trails
* [References](/references/) — Obsidian vault bridge, OKF spec, external extracts

## Quick nav

| From | To | Clicks |
|---|---|---|
| "What's the current sprint?" | [Sessions → Sprint Tracker](/sessions/sprint-tracker.md) | 2 |
| "What model serves what role?" | [Architecture → Model Routing](/architecture/model-routing.md) | 2 |
| "Which fleet nodes are up?" | [Fleet → Topology](/fleet/topology.md) | 2 |
| "How do I use Google OAuth?" | [Integrations → Google OAuth Bridge](/integrations/google-oauth-bridge.md) | 2 |
| "What are Cole's top patterns?" | [Skills → Cole Medin Patterns](/skills/cole-medin-patterns.md) | 2 |

## Conformance

This bundle targets OKF v0.1. Every `.md` file has YAML frontmatter with a non-empty `type` field. `index.md` files provide progressive disclosure. `log.md` tracks change history.