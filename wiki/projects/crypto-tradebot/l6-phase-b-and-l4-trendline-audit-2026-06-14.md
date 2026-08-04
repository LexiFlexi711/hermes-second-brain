# L6 Phase B baseline + L4 trendline audits — 2026-06-14

## 1. Repo/head

- **Huidige HEAD:** `5d059db5 fix(layer6): body_trend uses last 3 candles strict monotonic check`
- **Laatste relevante commits:**
  - `cb356826 Add Layer 6 micro director route`
  - `5d059db5 fix(layer6): body_trend uses last 3 candles strict monotonic check`
- **Git status:** enkel pre-existing `dead_code/` modified + untracked experiments/pngs/backups — buiten scope

## 2. L6 Phase B baseline

- `director.read_layer6(pair, timeframe)` toegevoegd aan `director/hermes_director.py`
- `/v6/micro/<pair>/<tf>` JSON route toegevoegd aan `app_dashboard.py`
- 5 mocked director tests in `tests/test_director_layer6.py`
- `candle_micro.py` bleef onaangeraakt tijdens Phase B
- Baseline gepusht als commit `cb356826`
- **Geen** V5/L8/cockpit/HTML/PNG-integratie
- **Geen** trade-taal in output

## 3. L6 validatie A (route/output check)

- Routes getest: BTCEUR 5m/15m/60m, ETHEUR 5m, SOLEUR 15m, PEPEEUR 60m
- Alle routes ✅ 200 JSON met keys: candles, closed_candle_policy, enabled, lookback, pair, reason, summary, timeframe
- `closed_candle_policy` aanwezig op alle routes
- `summary` aanwezig (last_3_sequence, consecutive, dominant, body_trend, wick_bias, micro_state)
- Invalid timeframe (999m) → 400 JSON error
- Fake pair → 500 JSON error (Kraken error), geen HTML stacktrace
- Enkel `"long"` in pattern namen `long_lower_wick`/`long_upper_wick` (toegestaan)

## 4. L6 validatie B (numerieke metric check)

- Samples: BTCEUR 5m, ETHEUR 5m, PEPEEUR 60m
- 15 candles gecontroleerd, **120 metric checks correct**:
  - range, body, direction, body_pct, upper_wick_pct, lower_wick_pct
- Alle patterns verklaarbaar via code-logica (doji, strong_body, medium_body, long_*, inside_bar, engulfing)
- PEPE low-price precision initieel aandachtspunt → later gefixt

## 5. L6 summary bugs gevonden

- `consecutive_bullish` / `consecutive_bearish` telden fout vanaf oudste kant in plaats van nieuwste
- `body_trend` keek fout/te simpel (second_half/first_half verkeerd om + averaging te grof)
- `dominant_pattern` behandelde ties/unique patterns misleidend (max() kiest arbitrair)
- `micro_state` was te grof: 1 enkele long_wick triggerde meteen `rejection_like`
- low-price rounding: `round(body, 8)` gaf `0.0` voor PEPE-achtige micro-prijzen
- **L6 raw metrics waren OK** — probleem zat enkel in summary/serialisatie

## 6. L6 summary fix

- **Commit:** `5d059db5 fix(layer6): body_trend uses last 3 candles strict monotonic check`
- **Scope:**
  - `projects/hermes-v01/layer6_micro/candle_micro.py` — logica fixes
  - `projects/hermes-v01/tests/test_layer6_candle_micro.py` — nieuwe tests
- **Geen** director/route/V5/L8/dashboard geraakt
- **Fixes:**
  - `_body_trend()`: gebruikt nu alleen **laatste 3 gesloten candles** (offset 2→1→0), strict monotonic check:
    - `p2 < p1 < p0` → expanding
    - `p2 > p1 > p0` → contracting
    - anders → mixed
    - Geen gemiddelden, geen 5-candle trends
  - `consecutive_*`: telt vanaf `directions[0]` (offset 0 = nieuwste), stopt bij richtingswissel of doji
  - `dominant_pattern`: gebruikt `Counter()` met check op ties → `mixed` bij gelijke telling
  - `wick_bias`: percentage-gebaseerd (som van upper/lower_wick_pct, ratio >3.0 of <0.33)
  - `micro_state`: eerst dominantie check (≥3), dan drempel-chefs. `strong_body_dominant` toegevoegd. `quiet_or_neutral` bij geen patronen.
  - low-price precision: `round(x, 12)` ipv `round(x, 8)` voor range en body
- **Tests:**
  - `test_layer6_candle_micro.py` ✅ 23/23 passed (10 nieuwe summary tests)
  - `test_director_layer6.py` ✅ 5/5 passed
  - `test_hermes_v02.py` ✅ 4/4 passed
  - compile OK

## 7. L4a 240m audit (recent local trendline)

- **Conclusie:** L4a/recent trendlines **bestaan en werken** op 240m via `/v4a/recent-trendline/<pair>/240m`
- **Resultaten:**
  - BTCEUR 240m: ✅ upper + lower valid, trend=up
  - SOLEUR 240m: ✅ upper valid, geen lower, trend=unclear
  - ETHEUR 240m: ✅ upper + lower valid, trend=squeeze
  - ADAEUR 240m: ✅ upper + lower valid, trend=squeeze
  - PEPEEUR 240m: ✅ upper + lower valid, trend=squeeze
- **Schijnbaar ontbreken in V5** komt door V5 render-policy: commit `3b7a1e6b` beperkt L4a in V5 tot 5m/15m
- **Geen** L4a detectiebug — het is een V5 rendering policy/debt

## 8. L4 major lower 240m audit (structurele lower/bottom trendline)

- **Conclusie:** ontbreken van lower op BTCEUR/SOLEUR/PEPEEUR 240m is **correct validatiegedrag**
- **L4 standalone en V5 consistent** — geen renderbug
- **Details per pair:**
  - **BTCEUR:** 19 swing lows, **0/40 valid lower candidates**, hoofdoorzaak: `too_old_no_recent_touch:24>20` — laatste extra touch 24+ candles terug (limiet is 20)
  - **SOLEUR:** 20 swing lows, **0/40 valid**, hoofdoorzaak: `too_old_no_recent_touch:21>20`
  - **PEPEEUR:** 23 swing lows, **0/40 valid**, `too_old_no_recent_touch:21>20` + body violations `0.388 > 0.35`
  - **ETHEUR:** **4/40 valid**, beste `idx=44→131`, 5 touches
  - **ADAEUR:** **2/40 valid**, beste `idx=47→188`, 5 touches
- **Validatiecriteria 240m:** min_span=8, body_violations≤0.35, price_side≤0.30, cuts≤0.35, extra_touch≥1, `candles_since_last_touch≤20`

## 9. Parked debts / later

- L6 mag als aparte inspectielaag baseline blijven
- L6 nog **niet automatisch in V5 integreren** zonder Phase C audit/design
- L4a op 60m/240m is local en bewust uit in V5 — policy later beslissen
- `too_old_no_recent_touch=20` op 240m is mogelijk streng maar geen bug
- Valid candidate met **score=0** bij ETH/ADA is verwarrend (score penalties trekken naar 0)
- `read_layer4` mist expliciete `lower_found`/candidate-status voor testbot/tradebot
- Upper trendline audit is later nog mogelijk apart
- Geen nieuwe lagen/filters/strategie nu

## 10. Current baseline

Current baseline: L6 Phase B + L6 summary fix are pushed. L4a 240m is not a detection bug. L4 major lower absence on BTCEUR/SOLEUR/PEPEEUR 240m is currently correct validation behavior. Next step should be Phase C audit/design for optional L6 display in V5, or a separate V5 render-policy design — not direct building.
