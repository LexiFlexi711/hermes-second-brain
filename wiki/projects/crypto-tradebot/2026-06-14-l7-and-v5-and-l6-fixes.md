# L7 Indicator Context + V5 Cockpit Fix + L6 Body Trend Fix — 2026-06-14

## 1. Repo/head

- **Huidige HEAD:** `9a462a19 feat(layer7): add neutral indicator context MVP`
- **Laatste 10 commits vandaag (chronologisch):**

| Commit | Omschrijving |
|---|---|
| `cb356826` | Add Layer 6 micro director route |
| `5d059db5` | fix(layer6): body_trend uses last 3 candles strict monotonic check |
| `2aa7834c` | feat(v5): add HTML cockpit with 4 panels + L6 per timeframe |
| `db592a92` | fix(v5): server-side chart cache + sequential render for reliable cockpit load |
| `9a462a19` | feat(layer7): add neutral indicator context MVP |

- **Git status:** enkel pre-existing dead_code + untracked experiments/pngs

## 2. L6 Phase B — Baseline

- `director.read_layer6(pair, timeframe)` toegevoegd
- `/v6/micro/<pair>/<tf>` JSON route toegevoegd
- 5 mocked director tests
- `candle_micro.py` bleef onaangeraakt tijdens Phase B
- **Geen** V5/L8/cockpit/HTML/PNG-integratie
- Route geverifieerd voor BTCEUR/ETHEUR/SOLEUR/PEPEEUR 5m-240m

## 3. L6 Validatie A + B

- **Validatie A:** Alle routes 200 JSON, closed_candle_policy aanwezig, summary aanwezig, 400 bij invalid TF, nette JSON error bij fake pair
- **Validatie B:** 15 candles uit 3 samples (BTCEUR/ETHEUR/PEPEEUR) — 120 metric checks correct (range, body, direction, body_pct, wick percentages)

## 4. L6 Summary Bugs + Fix (commit `5d059db5`)

**5 bugs gevonden en gefixt:**

| Bug | Oorzaak | Fix |
|---|---|---|
| `consecutive_*` telt verkeerd | Telde vanaf oudste in plaats van nieuwste | Start bij offset 0, stop bij change/doji |
| `body_trend` leest richting fout | second_half/first_half ratio verkeerd om + averaging te grof | Enkel laatste 3 candles, strict monotonic check |
| `dominant_pattern` tie misleidend | `max(set(...))` kiest arbitrair bij tie | Counter + check op unique max → `mixed` |
| `micro_state` te grof | 1 long_wick triggerde meteen `rejection_like` | Eerst dominantie (≥3), dan drempel-checks |
| Low-price precision | `round(x, 8)` gaf 0.0 voor PEPE body | `round(x, 12)` voor range en body |

**Testresultaten:** test_layer6 23/23, test_director 5/5, hermes_v02 4/4

## 5. V5 HTML Cockpit (commits `2aa7834c` + `db592a92`)

**Nieuwe route:** `/v5/cockpit/<pair>` — HTML pagina met 4 losse panels

**Wat er is:**
- 4 panels: 240m / 60m / 15m / 5m
- Elke chart als `<img>` image (gebaseerd op `/v5/cockpit-img/` cache)
- Klik op chart → opent full-size PNG in nieuw tabblad
- L6 compact blok onder elke chart: direction chips + dominant/trend/micro/wick/cb info
- "Open Xm full chart" fallback knop per paneel

**Fix voor betrouwbaar laden:**
- Server-side chart cache in RAM (dict `_cockpit_chart_cache`)
- Cockpit route genereert 4 charts 1 voor 1 met 1.5s pauze
- `/v5/cockpit-img/<pair>/<tf>` serveert uit cache (~1ms, geen Kraken calls)
- Images hebben `loading="lazy"`, `decoding="async"`, `aspect-ratio` zodat layout niet instort

**Bestaande routes behouden:** `/v5/structure-cockpit/<pair>` (PNG), `/v5/structure-cockpit/<pair>/<tf>` (single PNG)

## 6. L4a 240m Audit

- L4a/recent trendlines bestaan en werken op 240m
- Apparent ontbreken in V5 komt door V5 render-policy (enkel 5m/15m)
- **Geen** L4a detectiebug

## 7. L4 Major Lower 240m Audit

- BTCEUR/SOLEUR/PEPEEUR 240m missen lower **terecht**:
  - `too_old_no_recent_touch` — laatste touch > 20 candles terug
  - Prijs is van lower zone weggelopen (bullish)
- ETHEUR/ADAEUR 240m: lower bestaat en is valid
- **Geen** renderbug, **geen** detectiebug. Correct validatiegedrag.

## 8. L7 Indicator Context MVP (commit `9a462a19`)

**Nieuwe module:** `projects/hermes-v01/layer7_indicator/`

**Inhoud:** neutrale indicator-contextlaag — meet-only, geen trade-signalen

**Features:**
- ATR 14 (simple mean) met `atr_pct` en `volatility_state` (low/normal/high/extreme)
- EMA 12/26 met `ma_regime` (bullish/bearish/mixed)
- MA crossover detectie met `bars_since`, `direction`, `recent` flag
- Closed candle policy: gebruikt enkel gesloten candles
- Lookback: 200 candles (Kraken max)

**Output (JSON via `/v7/indicator/<pair>/<tf>`):**

```json
{
  "pair": "BTCEUR",
  "timeframe": "15m",
  "enabled": true,
  "atr": {"value": 109.39, "atr_pct": 0.19, "volatility_state": "low"},
  "ma_regime": {"fast_ema": 55492, "slow_ema": 55591, "regime": "bearish", "spread_pct": 0.18},
  "ma_cross": {"direction": "bullish", "bars_since": 10, "recent": true},
  "quality": "clean"
}
```

**Verboden woorden:** buy/sell/entry/exit/long/short/setup/trigger/ready/forecast/prediction/tradeable — **none found** in 20 live JSON outputs

**Files (5, 524 inserties):**
- `layer7_indicator/__init__.py` — package init
- `layer7_indicator/indicator_context.py` — core module (224 regels)
- `tests/test_layer7_indicator.py` — 22 unit tests
- `director/hermes_director.py` — `read_layer7()` toegevoegd (+11)
- `layer1_charts/app_dashboard.py` — `/v7/indicator/` route (+20)

**Route:** `/v7/indicator/<pair>/<tf>` (5m/15m/60m/240m) — JSON, 400 bij invalid TF

**Tests:** 22/22 L7 + 54/54 totaal ✅

## 9. Parked Debts

- L6 mag als aparte inspectielaag baseline blijven
- L6 nog niet automatisch in V5 integreren zonder Phase C audit/design
- L4a op 60m/240m is bewust uit in V5 — policy later beslissen
- `too_old_no_recent_touch=20` op 240m is streng maar geen bug
- `read_layer4` mist expliciete `lower_found`/candidate-status voor testbot/tradebot
- L7 MVP bevat ATR + MA. RSI/MACD/Volume later in Phase 2
- L8 timing context nog niet gebouwd (combineert L2-L7)
- V5 cockpit cache (`_cockpit_chart_cache`) is RAM-only, vervalt bij restart. Later eventueel disk/file cache.

## 10. Huidige Baseline

L6 Phase B + L6 summary fix + V5 HTML cockpit + V5 chart cache + L7 indicator MVP zijn allemaal gepusht. L7 is live en geverifieerd op 20 routes. Geen trade-taal in L6 of L7. Volgende stap: L7 Phase 2 (RSI/MACD) of L8 timing context of V5 cockpit verfijning.
