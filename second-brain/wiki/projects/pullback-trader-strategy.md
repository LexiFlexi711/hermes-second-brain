---
title: Pullback Trader Strategy
type: project
created: 2026-05-19
status: defined
---

# Pullback Trader Strategy

## Context
De huidige noa_trader.py bot haalt geen traden door MIN_RR=4.0, ontbrekende pullback-detectie, en fib filter 38.2-61.8% die te strict is in post-crash markt. Daarom een apart pullback-only script.

## Kernprincipe
Bij bearish context: 4H downtrend → bounce (pullback) → fib zone → 15M bearish → SHORT
Bij bullish context: omgekeerd

## Entry Conditions (SHORT)
1. 4H trend = DOWN — lower highs/lower lows, bearish impulse, broken support
2. Voorafgaande bearish move bestaat
3. Prijs maakt bounce omhoog = pullback tegen trend
4. pullback_start_low en pullback_high bekend
5. fib_pct = (current_price - pullback_start_low) / (pullback_high - pullback_start_low) * 100
6. 15M bearish bevestiging NA de pullback
7. entry_lateness_pct ≤ 50%

## Fib Zones (learning mode)
| Range | Label | Actie |
| <30% | pullback_forming | WAIT |
| 30-38.2% | early_pullback | WAIT |
| 38.2-61.8% | ideal_pullback_zone | KLAAR |
| 61.8-70% | deep_pullback_warning | WAIT/BLOCK |
| >70% | possible_trend_break | BLOCK |

## Entry Quality
- entry_lateness_pct = (pullback_high - entry_price) / (pullback_high - pullback_start_low) * 100. >50% = weak_entry
- candles_after_pullback_high: max 5 candles 15M
- rejection_wick: kwaliteitslabel, geen gate

## Status Labels
pullback_forming, early_pullback, ideal_pullback_zone, deep_pullback_warning, possible_trend_break, confirmed_ready, weak_entry, blocked_pullback_required

## Harde Regels
- RR minimum 2.0 (learning: 1.5), maximum 8.0
- "4H trend entry" als OPEN reden is VERBODEN
- Apart script (pullback_trader.py), nooit noa_trader.py aanpassen
- Geen fees/slippage/live ticker/extra indicatoren/AI-score

## Bestanden
- Script: `projects/crypto-tradebot/scripts/pullback_trader.py` (nog te schrijven door Claude Code)
- Agent persona: `autonomous/agents/trade-specialist.md`
- Meeting rapport: `autonomous/meetings/2026-05-19_pullback-strategy-meeting.md`

## Zie ook
- [[trade-specialist-agent]]
- [[crypto-tradebot]]
