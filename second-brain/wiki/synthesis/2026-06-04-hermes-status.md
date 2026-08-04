---
type: synthesis
id: 2026-06-04-hermes-status
tags: [hermes, v02, pipeline, channel-down, indicators]
---

# Hermes Status — 2026-06-04

## Wat afgerond is

### hermes_v02.py (laatste versie)
- `channel_down()`: dalend kanaal detectie via laatste 2 pivot highs + parallelle lower door laagste bodem ertussen. Zoekt van achter naar voor, minimum 10 bars afstand.
- `indicators()`: MACD (12,26,9), RSI(14), MA(9)/MA(21) met cross detectie
- `read_market()`: gebruikt channel_down() voor upper/lower trendlijnen + confidence scoring via fuzzy AND van richtingsscores
- `move_atr` berekend over HELE lookback (500 bars) zoals PineScript v02 validatie

### Tests
- v01 tests: 32/32 groen
- v02 tests: 4/4 groen (channel_down synthetisch, indicators vlak)
- Veel tijd verloren aan PineScript syntax fouten — LESSON: StackOverflow/GitHub eerst na 2 mislukte pogingen

### Data pipeline
- crypto-data ohlc_archive liep 9 uur achter op tradebot
- Fix: cp -ru van tradebot/logs/ naar crypto-data/logs/ voor ohlc_archive, live_cache, bridge
- Root cause: cache_updater.py schrijft naar tradebot path, BacktestReader checkt crypto-data eerst
- ADAEUR 1H nu up-to-date tot 4/6 10:00

### SOUL.md geupdate
- CODE-PROBLEMEN REGEL toegevoegd
- AANWEZIGHEID VAN TOOLS EN CONTEXT
- LOYALITEIT AAN LEXI
- BRONNENREGEL

### Skill: code-problemen-oplossen
- Na 2 mislukte pogingen: STOP → StackOverflow/GitHub → lezen → schrijven

## Nog open

- strategy_channel_down_v1.py (v1: enkel short op trending_down, -160% PnL)
- strategy_channel_down_v2.py (MTF 4H+1H, 61 trades, 45.9% WR, -30.94% PnL)
- strategy_channel_down_v4.py (15M, 2632 trades, 29.86% WR, -840% PnL)
- Data pipeline root cause nog niet opgelost (cache updater schrijft naar verkeerde path)
- PineScript v4.4 is de werkende referentie (Lexi schreef die)