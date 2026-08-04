---
title: "Sessie 31 Mei 2026 — STAP T + strategie research"
type: source_summary
created: 2026-05-31
source: Hermes sessie
status: inbox
---

# Sessie 31 Mei 2026

## Wat gebeurd is

### 1. Research 10 crypto-bot strategieën
Op vraag van Lexi: "gaat dit eesn bekjken op het net" — 10 strategieën online onderzocht met bronnen.
- **Opgeslagen:** `raw/inbox/31mei26-claude-10-strategieen.md`
- Momentum/trend-following ✅ hard gemaakt (arXiv paper, Sharpe 2.41)
- Failed breakout exit 🏆 quick win
- Market making ❌ kill, Pairs trading ❌ kill

### 2. STAP T — V1 en V2 strategie in testbot
- V1 strategie overgezet van `crypto-tradebot/scripts/strategies/v1_strategy.py` naar testbot
- V2 strategie overgezet van `crypto-tradebot/scripts/strategies/v2_strategy.py` naar testbot
- Beide met config.py + logic.py + strategy.py (Strategy ABC patroon)
- 52 nieuwe unit tests — 101/101 totaal ✅
- Resultaat: `tasks/done/STAP-T-result.md`
- Pending task verplaatst naar `tasks/done/`

### 3. Startup-check
- Server OK (8 weken uptime, 25/25 docker)
- 20 pending updates ⚠️
- Backtest data beschikbaar (V1: 40%, V2: 40%, V3: 29%, Momentum: 52%)
- Crypto-data bridge: status.json niet gevonden
