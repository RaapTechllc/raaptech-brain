---
type: Reference
title: TradingView MCP Integration
description: TradingView MCP Jackson bridge — CDP connection, Lorentzian indicators, morning brief.
resource: C:/Users/Kyle/tradingview-mcp-jackson
tags: [integrations, tradingview, mcp, trading]
timestamp: 2026-07-06T16:30:00Z
---

# TradingView MCP Integration

**Bridge:** Jackson at `~/tradingview-mcp-jackson`
**Connection:** TV Desktop CDP on port 9222
**Tools:** `mcp_tradingview_*`

## Key Capabilities

| Tool | Purpose |
|---|---|
| `mcp_tradingview_tv_launch` | Launch TradingView Desktop with CDP |
| `mcp_tradingview_chart_set_symbol` | Change chart symbol |
| `mcp_tradingview_chart_set_timeframe` | Change timeframe |
| `mcp_tradingview_data_get_ohlcv` | Get OHLCV bar data |
| `mcp_tradingview_data_get_study_values` | Get indicator values |
| `mcp_tradingview_morning_brief` | Scan watchlist, read indicators, generate brief |
| `mcp_tradingview_pine_compile` | Compile Pine Script |
| `mcp_tradingview_replay_start` | Start bar replay mode |

## Indicators

- **Lorentzian Premium** — Primary AI Edge indicator
- **Lorentzian Optimizer** — Parameter optimization
- Use `tradingview-indicator-optimization` skill for tuning

## Morning Brief Flow

1. `mcp_tradingview_tv_launch` — Start TV Desktop
2. `mcp_tradingview_morning_brief` — Scan watchlist + indicators
3. `mcp_tradingview_session_save` — Save brief to `~/.tradingview-mcp/sessions/`
4. Feed into Morning Ops stack

## Integration with AI Trading Council

See [AI Trading Council](/business/ai-trading-council.md) for strategy rules and allocation.