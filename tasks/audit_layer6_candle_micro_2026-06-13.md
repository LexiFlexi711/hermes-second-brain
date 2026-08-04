# Audit — Layer 6 Candle Micro voorbereiding

**Datum:** 2026-06-13
**Status:** Geen code gewijzigd

---

## 1. Bestaande Layer 6 placeholder

Ja — `layer6_recent_trend/` met `__init__.py` en `README.md`.

README zegt al:
> *"Layer 6 will handle near-term active movement (micro structure)"*

De placeholder is klaar voor gebruik. Kan hernoemd of direct gebruikt worden.

## 2. Bestaande candle-pattern code

**In actieve Hermes code:** ❌ Geen.

**Enkel in experiments:**
- `stable_baseline.py` — doji detectie (body < 5% range), inline
- `validate_visual_v2.py` — doji detectie, inline
- Geen propere functies, geen herbruikbare helpers

Body ratio logica bestaat wel in `swing_points.py` (voor swing strength berekening), maar dat is voor swing detectie, niet voor candle micro.

## 3. Candle source — gesloten/open candle policy

`fetch_kraken()` in `chart_engine.py` haalt 200 candles op via Kraken API.

**Belangrijk:** de **laatste candle (`candles[-1]`) is CURRENT (nog open/niet gesloten)**.
- `candles[-2]` = de laatste gesloten candle
- `candles[-3]` = de 2de laatste gesloten candle, etc.

Huidige Hermes layers gebruiken `candles[-1]` voor close/current prijs. Dat is correct voor L1-L5.

**Voor L6:** de huidige open candle is niet bruikbaar voor micro-analyse. L6 moet enkel gesloten candles gebruiken.

## 4. Minimale toekomstige files

```
projects/hermes-v01/layer6_micro/__init__.py     (placeholder)
projects/hermes-v01/layer6_micro/candle_micro.py  (hoofdmodule)
```

L6 later:
- `director/hermes_director.py` — `read_layer6(pair, tf)`
- `app_dashboard.py` — `/v6/micro/<pair>/<tf>` route

## 5. Voorstel output contract

```python
{
  "pair": "BTCEUR",
  "timeframe": "5m",
  "lookback": 5,
  "candles": [
    {
      "index": 195,
      "direction": "bearish",          # "bullish" | "bearish" | "doji"
      "body_pct": 35,                  # body% van totale range
      "upper_wick_pct": 10,            # upper wick% van totale range
      "lower_wick_pct": 55,            # lower wick% van totale range
      "pattern": "long_lower_wick",    # "doji" | "inside_bar" | "engulfing_bullish"
                                        # "engulfing_bearish" | "long_lower_wick"
                                        # "long_upper_wick" | "strong_body" | none
      "range": 145.0,                  # high - low
      "close": 54950.0
    },
    ...
  ],
  "summary": {
    "consecutive_bearish": 2,
    "consecutive_bullish": 0,
    "dominant_pattern": "long_lower_wick",
    "buyer_pressure": 0.65,
    "seller_pressure": 0.35,
    "momentum": "bearish_fading",
    "volatility_expanding": false,
    "inside_bar_count": 1
  }
}
```

## 6. Voorstel patronen (eerste versie)

| Patroon | Regel |
|---|---|
| `doji` | body ≤ 5% van range |
| `bullish` | close > open |
| `bearish` | close < open |
| `long_lower_wick` | lower wick ≥ 60% van range |
| `long_upper_wick` | upper wick ≥ 60% van range |
| `strong_body` | body ≥ 70% van range |
| `small_body` | body ≤ 20% van range |
| `inside_bar` | high < prev_high AND low > prev_low |
| `engulfing_bullish` | close > prev_high AND open < prev_close AND prev_bearish |
| `engulfing_bearish` | close < prev_low AND open > prev_close AND prev_bullish |

Alle patronen werken met OHLC-only. Geen indicatoren nodig.

## 7. Risico's

| Risico | Mitigatie |
|---|---|
| Huidige open candle meenemen | Enkel `candles[:-1]` of `candles[-lookback-1:-1]` gebruiken |
| Pattern overlap (bv doji + small body) | Prioriteit: doji > engulfing > inside_bar > wick > body |
| Te veel patronen op 5m | Beperk tot 5 candles lookback |
| Geen L2-L5 context | L6 is pure candle micro — geen context nodig. Later in L8 assessment |

## 8. Advies

**L6 is klaar om gebouwd te worden.** De architectuur staat:
- Placeholder: `layer6_recent_trend/` kan hernoemd worden naar `layer6_micro/`
- Data: `fetch_kraken()` via L1
- Gesloten candle policy: duidelijk (`candles[-1]` skippen)
- Patronen: eenvoudig, OHLC-only, geen dependencies
- Output: compact, testbaar, geen interpretatie
