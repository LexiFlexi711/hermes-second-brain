---
title: Pullback Strategy Team Meeting - 19 mei 2026
type: synthesis
created: 2026-05-19
---

# Pullback Strategy Team Meeting

**Team:** Noa Hermes + ChatGPT audit + Claude Code schrijver
**Opdrachtgever:** Lexi
**Status:** Strategie vastgelegd

## Diagnose

**Probleem A: MIN_RR = 4.0 blokkeert alles**
- trade_engine.py hanteert `_MIN_RR = 4.0` 1:4 risk/reward
- Logs: 15/15 pairs altijd WAIT, geen enkele trade

**Probleem B: 15M blokkeert SHORT in pullback-situatie**
- 4H bearish + 15M bullish = gemiste pullback opportuniteiten

**Probleem C: Geen pullback-detectie**
- Geen fib retracement, geen bounce-herkenning, geen entry_lateness check

## Vastgestelde Strategie

Pullback-only: 4H downtrend -> bounce -> fib zone -> 15M bearish -> SHORT

fib_pct = current_price - pullback_start_low / pullback_high - pullback_start_low * 100

**Fib zones:**
- <30%: pullback_forming
- 30-38.2%: early_pullback
- 38.2-61.8%: ideal_pullback_zone
- 61.8-70%: deep_pullback_warning
- >70%: possible_trend_break

entry_lateness_pct = pullback_high - entry_price / pullback_high - pullback_start_low * 100
>50% = weak_entry

## Correcties na Lexi
1. Fib formule gecorrigeerd
2. Bearish structuur: lower highs/lower lows i.p.v. HH/HL broken
3. Fib zones verfijnd met 5 labels
4. rejection_wick = kwaliteitslabel, geen gate
5. entry_lateness_pct toegevoegd
6. 4H trend entry verboden als OPEN reden

## Deliverables
- pullback_trader.py nog te schrijven door Claude Code
- autonomous/agents/trade-specialist.md trade specialist persona

## Zie ook
- [[crypto-tradebot]]
- [[pullback-trader-strategy]]
- [[trade-specialist-agent]]
- [[secretary-agent]]
- [[meeting-002]]
- [[meeting-008]]
- [[team-meeting-005-pullback-strategy]]
- [[team-meeting-006]]
