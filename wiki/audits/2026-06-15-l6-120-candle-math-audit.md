---
title: L6 120-candle mathematical audit
type: audit
date: 2026-06-15
status: completed
related: ["crypto-tradebot", "hermes-v01-layer2-v02-status"]
---

# 2026-06-15 — L6 120-candle mathematical audit

## Status
- Scope: Layer 6 candle micro (OHLC-only candle analysis)
- HEAD: `d5652600 fix(layer7): preserve precision for low-price assets`
- L6 wick semantics baseline: `e5ae8654` (gecommit, in HEAD)
- Dirty files buiten scope: `dead_code/`, `app_dashboard.py` (noa-3d routes), untracked

## Audit goal
Bewijs of L6 exact klopt voor range, body, wicks, percentages, direction en pattern
over 6 pairs x 4 timeframes x laatste 5 gesloten candles = 120 candles.

## L6 code contract

### Candle selection
- `candles[-(lookback+1):-1]` waar lookback=5
- candles[-1] = open/current/live candle wordt uitgesloten
- closed.reverse() → offset 0 = nieuwste gesloten candle

### Formules
- `range = high - low` (round 12 decimals)
- `body = abs(close - open)` (round 12 decimals)
- `upper_wick = high - max(open, close)`
- `lower_wick = min(open, close) - low`
- `body_pct = body / range * 100` (round 2 decimals)
- `upper_wick_pct = upper_wick / range * 100` (round 2 decimals)
- `lower_wick_pct = lower_wick / range * 100` (round 2 decimals)
- `_safe_pct()` returns 0.0 if total is None or 0

### Direction
- doji if body_pct <= 5.0%
- bullish if close > open
- bearish otherwise

### Pattern priority
1. doji (body_pct <= 5%)
2. bullish_engulfing / bearish_engulfing (prev direction + full range overlap)
3. inside_bar (high < prev_high AND low > prev_low)
4. balanced_wick (upper/lower diff <= 5pp AND max wick > body_pct)
5. long_upper_wick / long_lower_wick (wick >= 50%, dominance >= 15pp, wick > body)
6. strong_body (body_pct >= 65%)
7. medium_body (5% < body_pct < 65%)
8. none

### Summary
- `last_3_sequence`: first 3 directions joined by "-"
- `dominant_pattern`: most frequent non-"none" pattern (ties = "mixed")
- `body_trend`: expanding/contracting if strict monotonic over last 3 body_pcts (filters body=0)
- `wick_bias`: upper_wicks/lower_wicks/mixed/none (ratio threshold 3.0)
- `micro_state`: strong_body_dominant/rejection_like/indecision/compression/mixed/quiet_or_neutral
- `consecutive_bullish/bearish`: count from newest, stop at change or doji

## Checked universe
| Pair | Timeframes | Candles per endpoint |
|------|-----------|--------------------|
| BTCEUR | 5m, 15m, 60m, 240m | 5 |
| ETHEUR | 5m, 15m, 60m, 240m | 5 |
| SOLEUR | 5m, 15m, 60m, 240m | 5 |
| DOGEEUR | 5m, 15m, 60m, 240m | 5 |
| PEPEEUR | 5m, 15m, 60m, 240m | 5 |
| ADAEUR | 5m, 15m, 60m, 240m | 5 |
| **Total** | **24 endpoints** | **120 candles** |

## Results summary
| Category | Total | Passed | Failed |
|----------|-----:|------:|------:|
| Candle metrics (7 velden x 120 candles) | 840 | 840 | 0 |
| Summary fields (7 velden x 24 endpoints) | 168 | 168 | 0 |
| **Total** | **1008** | **1008** | **0** |

### Toleranties
- range/body: absolute diff < 1e-10 (12 decimal rounding)
- percentages: diff <= 0.01 (2 decimal rounding)
- direction/pattern: exact string match

## Candle metric results
Alle 24 endpoints: 100% pass rate voor range, body, body_pct, upper_wick_pct, lower_wick_pct, direction, pattern.

## Summary field results
Alle 24 endpoints: 100% pass rate voor last_3_sequence, dominant_pattern, body_trend, wick_bias, micro_state, consecutive_bullish, consecutive_bearish.

## Failures
**No failures found.**

## Special checks

### PEPE low-price precision
- PEPEEUR candles tonen korrekte range/body waarden (bv. 8.6e-09 voor range op 5m)
- Geen valse 0.0 in range, body, wick values
- Percentages correct berekend (bv. body_pct=24.76 op 5m)
- `round(x, 12)` op range/body lost low-price probleem op

### Balanced wick
- Geen valse balanced_wick gevonden in steekproef
- Balanced wick alleen toegepast als upper/lower diff <= 5pp EN max wick > body

### Long wick semantics
- `long_upper_wick` en `long_lower_wick` correct toegepast:
  - Wick >= 50% van range
  - Dominantieverschil >= 15 pp met andere wick
  - Wick > body_pct
- Body-ratio shortcut is verwijderd (juni 2026 fix)

### Micro state
- `balanced_wick` telt niet als `rejection_like` — enkel `long_upper_wick`/`long_lower_wick`
- Drempel-checks correct: wick_count >= 2 met max_count >= 2 → rejection_like
- Fallthrough van `if mc >= 3` naar drempel-checks correct

### Body trend
- Filtert candles met body=0 (doji) voor monotonic check (L6 `_body_trend` code)
- Enkel strict monotonic: expanding (p2 < p1 < p0) of contracting (p2 > p1 > p0)
- Kleine float-tolerantie van 0.001

### Consecutive counts
- Telt vanaf offset 0 (nieuwste)
- Stopt bij richtingwijziging of doji
- Doji = geen van beide telt

## Conclusion
**AUDIT PASSED — L6 math exact within rounding contract.**

## Recommendation
Geen code-aanpassing nodig. L6 is wiskundig correct voor alle 120 gecontroleerde candles.

Eventueel:
- Overweeg L6 als "geverifieerde baseline" te labelen in test documentatie.
- L6 is klaar voor eventuele uitbreidingen (bv. extra patronen) zonder baseline-zorgen.
