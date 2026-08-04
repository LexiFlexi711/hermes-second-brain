---
title: L7 ma_cross alignment + low-price precision fixes
type: fix
date: 2026-06-15
status: applied
related: ["hermes-v01-layer2-v02-status", "crypto-tradebot"]
---

# 2026-06-15 — L7 ma_cross alignment + low-price precision fixes

## Status
- Current L7 baseline commits:
  - `a6e353b2 fix(layer7): align EMA series in ma_cross`
  - `d5652600 fix(layer7): preserve precision for low-price assets`
  - `79b188a7 feat(layer7): add indicator audit core`
- Scope: Layer 7 indicator context only.
- Purpose: neutral indicator context, not strategy/timing/trade logic.

## Fix 1 — ma_cross EMA alignment

### Symptom
- `ma_cross.direction` fout voor 21/24 endpoints.
- `ma_cross.bars_since` fout voor 24/24 endpoints.
- Bullish regime (fast_ema > slow_ema) combineerde met bearish cross direction.

### Root cause
- `fast_series` (EMA12, start bij candle 12) en `slow_series` (EMA26, start bij candle 26) werden als aparte lijsten opgebouwd.
- `_ma_cross(fast_series, slow_series)` vergeleek `fast_series[i]` (candle 12+i) met `slow_series[i]` (candle 26+i).
- Structurele offset van 14 candles tussen de series.

### Fix
- EMA-series aligned vóór `_ma_cross`:
  ```python
  ema_offset = SLOW_EMA_PERIOD - FAST_EMA_PERIOD  # = 14
  aligned_fast = fast_series[ema_offset:]  # candles 26..199
  aligned_slow = slow_series               # candles 26..199
  ```
- Beide series starten nu op candle 26.

### Evidence
- **BTCEUR 240m**: bullish, bars_since 21, recent false ✅
- **ETHEUR 240m**: bullish, bars_since 13, recent false ✅
- **ADAEUR 60m**: bullish, bars_since 10, recent true ✅
- Alle 24 endpoints coherent: direction matcht regime.
- 5 nieuwe `TestMACrossAlignment` tests (27/27 L7 tests pass).

### Lesson / rule
EMA series with different periods do not share the same candle index unless explicitly aligned.
Always align EMA series to the same candle basis before detecting crosses.

## Fix 2 — low-price precision output

### Symptom
- Low-price assets zoals PEPEEUR (~2.5e-06) toonden `0.0` voor prijswaarden.
- `atr.value: 0.0` (terwijl atr_pct wel correct was).
- `fast_ema: 0.0`, `slow_ema: 0.0` (terwijl spread_pct wel correct was en regime bullish).
- Interne math correct, maar `round(value, 4)` drukte kleine waarden naar nul.

### Root cause
- `round(value, 4)` op 3 outputvelden:
  - `"value": round(atr_val, 4)` — line 73
  - `"fast_ema": round(fast_ema, 4)` — line 96
  - `"slow_ema": round(slow_ema, 4)` — line 97

### Fix
- Nieuwe helper `_round_price_value()` met dynamische precisie:
  - `< 0.0001` → 12 decimalen
  - `< 0.01` → 8 decimalen
  - `< 1.0` → 6 decimalen
  - `>= 1.0` → 4 decimalen
- PEPEEUR toont nu `2.566e-06` ipv `0.0`.
- BTC/ETH blijven 4 decimalen (`56647.2896`).

### Evidence
- **PEPEEUR 15m**: atr.value=`1.464e-08`, fast_ema=`2.555e-06`, slow_ema=`2.537e-06`, atr_pct=`0.5702` ✅
- **PEPEEUR 240m**: atr.value=`4.079e-08`, fast_ema=`2.492e-06`, slow_ema=`2.463e-06` ✅
- Alle 36 L7 tests pass (27 oud + 9 nieuwe precision tests).
- 24 endpoints live bevestigd via HTTP.

### Lesson / rule
Never round price-like values to fixed 4 decimals when low-price assets are supported.
Use dynamic numeric precision for price values and keep percentages compact.

## Fix 3 — L7 audit core Phase A

### Commit
`79b188a7 feat(layer7): add indicator audit core`

### Purpose
Layer 7 is now auditable through `audit_indicator_context()`.

This does not add strategy, timing, setup logic, or trade signals.
It adds a verification layer around the existing neutral L7 indicator context.

### Files
- `projects/hermes-v01/layer7_indicator/indicator_audit.py`
- `projects/hermes-v01/tests/test_layer7_indicator_audit.py`
- `projects/hermes-v01/layer7_indicator/__init__.py`

### What it verifies
- closed candle selection
- ATR true ranges / ATR value / ATR pct
- EMA12 and EMA26 series
- EMA series alignment (fast start 12, slow start 26, offset 14)
- MA regime
- latest MA cross direction
- bars_since
- recent
- low-price precision compatibility
- L7 output versus independent audit calculation

### Evidence
- 12/12 audit tests passed
- 36/36 L7 regression passed
- 29/29 L6 regression passed
- 5/5 director L6 passed
- 4/4 hermes_v02 passed
- compile clean
- forbidden words clean
- 24 endpoint live smoke passed
- no dashboard route added
- no app_dashboard.py changes
- no L6/L8/V5/strategy/tradebot changes

### Lesson / rule
Every analytical layer that may later feed strategy/testbot/tradebot must have a local audit core before it is consumed downstream.

Auditability comes before interpretation.

Layer 7 is now a technical baseline for neutral indicator context, not a timing or strategy layer.

## Current L7 contract
- ATR:
  - `atr.value`: dynamic numeric precision
  - `atr.atr_pct`: compact percentage precision (4 decimals)
  - `volatility_state`: unchanged (low/normal/high/extreme)
- MA regime:
  - `fast_ema`: dynamic numeric precision
  - `slow_ema`: dynamic numeric precision
  - `spread_pct`: compact percentage precision (4 decimals)
  - `regime`: neutral context only (bullish/bearish/mixed/unknown)
- MA cross:
  - aligned EMA12/EMA26 series (same candle basis)
  - `direction`: latest true cross direction
  - `bars_since`: candles since latest cross
  - `recent`: `bars_since <= CROSS_LOOKBACK` (10)
- Quality:
  - `clean` if ATR and MA available
  - `weak` if one unavailable
  - `invalid` if fetch failed or insufficient data
- Closed candle policy: `candles[-(lookback+1):-1]`, excludes candles[-1]
- Audit:
  - `audit_indicator_context()`: independent re-calculation vs L7 output
  - 11 checks per endpoint
  - status: pass/fail
  - full failure list

## Not changed
- L6, L8, V5
- dashboard/app_dashboard.py
- strategy/tradebot
- ATR-formule (simple mean, geen Wilder smoothing)
- EMA-formule (SMA init + EMA iteratie)
- ma_regime-semantiek
- ma_cross-semantiek na alignment

## Parked / next
- `projects/hermes-v01/layer1_charts/app_dashboard.py` blijft dirty door noa-3d avatar routes.
- `dead_code/` en untracked bestanden blijven buiten scope.
- L6 120-candle mathematical audit completed (1008/1008 checks pass).
- L7 audit-view (HTML/cockpit) later wenselijk.
- L8 nog niet bouwen (geen assessment/synthesis laag).
- `_build_tunnel()` break-status verifiëren.
- Dubbele `structure_cockpit.py` audit.
- `layer6_recent_trend/` beslissen: roadmap-slot of archiveren.
- Legacy label-bestanden beoordelen.
- Director end-to-end tests.

## Verification summary
- 48 L7 tests pass (22 baseline + 5 alignment + 9 precision + 12 audit core).
- 29 L6 regression tests pass — 0 regressie.
- 5 director L6 tests pass.
- 4 hermes_v02 tests pass.
- 24 live HTTP endpoints bevestigd (6 pairs x 4 TFs).
- 24 live audit endpoints pass (11/11 checks each).
- Dashboard HTTP op poort 5001 (geen SSL, geen auth).
