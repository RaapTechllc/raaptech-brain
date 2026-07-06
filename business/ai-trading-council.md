---
type: Reference
title: AI Trading Council
description: AI Trading Council modes, allocation rules, and strategy brief.
resource: C:/Users/Kyle/Documents/ai-trading-council-brief.md
tags: [business, trading, ai, crypto]
timestamp: 2026-07-06T16:30:00Z
---

# AI Trading Council

**Source of truth:** [ai-trading-council-brief.md](C:/Users/Kyle/Documents/ai-trading-council-brief.md)

## Modes

| Mode | Description | When |
|---|---|---|
| **Research** | Analysis only, no trades | Market uncertainty, new assets |
| **Ask** | Propose trades, human approves | Standard operation |
| **Full Autonomous** | Execute without approval | High-confidence signals only |

## Rules (June 2026)

- **Small gains:** Take profits early, don't hold for moonshots
- **Cut losers:** Hard stop-losses, no averaging down
- **Capital ladder:** Scale position sizes with account growth
- **Moon bags + trailing:** Keep small position with trailing stop after taking profit
- **Multi-agent verification:** Trades require consensus from multiple models
- **Allocation:** 60/30/10 (primary / secondary / speculative)

## Platforms

- **Primary:** HL (HyperLiquid)
- **Phase 2:** Alpaca (traditional markets)
- **Indicators:** Lorentzian Premium/Optimizer via TradingView MCP Jackson

## Integration

- TradingView MCP Jackson at `~/tradingview-mcp-jackson`
- TV Desktop CDP on port 9222
- Tools: `mcp_tradingview_*`