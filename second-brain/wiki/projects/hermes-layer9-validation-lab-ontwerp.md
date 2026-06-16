# L9 PHASE 0 — VALIDATION LAB ONTWERP/AUDIT

**Datum:** 2026-06-16
**Status:** Read-only ontwerp/audit. L9 is nog niet gebouwd.
**Auteur:** Noa (Hermes Agent)

---

## 1. Scope

Gecontroleerd:
- `projects/hermes-v01/director/hermes_director.py` — alle director functies
- `projects/hermes-v01/layer2_structure/` — L2 fractals/swings
- `projects/hermes-v01/layer2_structure_v2/` — L2v2 swing points/S/R
- `projects/hermes-v01/layer3_phase/` — L3 D/U/R/range
- `projects/hermes-v01/layer4_trendline_lab/` — L4 trendlines
- `projects/hermes-v01/layer6_micro/` — L6 candle micro
- `projects/hermes-v01/layer7_indicator/` — L7 indicator context
- `projects/hermes-v01/layer8_market_context/` — L8 market context

Niet gecontroleerd (buiten scope):
- Layer 5 cockpit (visueel, geen data-laag)
- Layer 3 chart story (presentatie, geen analyse)
- Layer 6 recent trend (lege module)
- Layer 1 charts (data fetch, geen analyse)

---

## 2. Huidige beschikbare lagen

### Layers met director wrapper (read_layerX)

| Laag | Director functie | Outputtelt | Closed-candle? |
|------|-----------------|------------|----------------|
| L2 | `read_layer2(pair, tf)` | fractalen_count, swing_highs, swing_lows, pivot_count | ❌ Geen policy vermeld. Gebruikt `candles` direct. |
| L3 | `read_layer3(pair, tf)` | raw_segments, compressed_phases, final_phases, r_confirmed, r_candidates | ❌ Geen policy vermeld. Gebruikt pivot-index uit L2. |
| L4 | `read_layer4(pair, tf)` | swing_highs, swing_lows, high_labels, low_labels, high_sequence, low_sequence | ❌ Geen policy vermeld. Gebruikt wick-prijzen. |
| L4a | `read_layer4a(pair, tf)` | recent trendline output (alleen 5m/15m) | ❌ Alleen actief op lage TF. |
| L6 | `read_layer6(pair, tf)` | candle_micro output: patronen, body_trend | ✅ "excludes candles[-1] (open candle)" |
| L7 | `read_layer7(pair, tf)` | atr, ma_regime, ma_cross | ✅ "excludes candles[-1]" |
| L8 | `read_layer8(pair, tf)` | direction, alignment, relative behavior, market wind, audit window | ✅ "excludes candles[-1]" |

### Belangrijke vaststelling: L6/L7/L8 hebben gesloten-candle policy.

L2/L3/L4 hebben **geen** expliciete closed-candle policy in de director wrapper. Dit is een risico voor L9: als L2/L3/L4 een open candle gebruiken, is de snapshot niet reproduceerbaar.

---

## 3. Director/pure-function status

### Replay-safe (accepteert pre-fetched candles)

| Laag | Pure functie | Handtekening | Status |
|------|-------------|-------------|--------|
| L6 | `analyze_candle_micro(candles, lookback, pair, timeframe)` | `(candles: list, ...) -> dict` | ✅ Volledig zuiver |
| L8 | `read_market_context_from_candles(pair, tf, pair_c, btc_c, eth_c)` | `(pair, tf, candles, candles, candles) -> dict` | ✅ Volledig zuiver |

### Wrapper-only (moet refactoren voor L9)

| Laag | Huidige functie | Probleem |
|------|----------------|----------|
| L2 | `read_layer2(pair, tf)` | Roept `fetch_kraken` intern aan. Geen `_from_candles` variant. |
| L3 | `read_layer3(pair, tf)` | Roept `fetch_kraken` intern aan. Zelfde probleem. |
| L4 | `read_layer4(pair, tf)` | `fetch_and_prepare` haalt candles op. Interne helpers zijn wel zuiver. |
| L7 | `read_indicator_context(pair, tf)` | Roept `fetch_kraken` intern aan. Interne helpers (`_calc_atr`, `_calc_ema`, `_ma_regime`, `_ma_cross`) zijn wel zuiver. |

### Conclusie voor L9 MVP:
- **L6 en L8** zijn direct bruikbaar met historische candles
- **L7** interne functies zijn zuiver maar hebben geen `_from_candles` wrapper
- **L2/L3/L4** hebben refactoring nodig voor L9 — of L9 slaat ze over in MVP

---

## 4. Closed-candle/replay-risico's

| Risico | Ernst | Toelichting |
|--------|-------|-------------|
| L2/L3/L4 open candle | **HOOG** | Deze lagen hebben geen expliciete closed-candle policy. L9 kan ze niet veilig herhalen zonder refactor. |
| L7 wrapper fetch | **HOOG** | `read_indicator_context(pair, tf)` haalt via Kraken. L9 kan geen historische candles injecteren. |
| L6 offset-logica | **MEDIUM** | L6 gebruikt offset 0 = recentste gesloten candle. Bij 1 candle terugspoelen moet dit consistent zijn. |
| L8 BTC/ETH data | **MEDIUM** | L8 heeft BTC/ETH candles nodig naast pair candles. L9 moet 3 datasets leveren. |
| Timestamp drift | **LAAG** | Bij backtest/backfill moeten timestamps exact matchen tussen snapshot en future window. |

---

## 5. Voorgesteld L9 snapshot contract

```json
{
  "pair": "SOLEUR",
  "timeframe": 60,
  "snapshot_timestamp": 1781589600,
  "closed_candle_policy": "excludes candles[-1]",
  "layers": {
    "l6_micro": {
      "enabled": true,
      "patterns": [...],
      "body_trend": "...",
      "closed_candle_policy": "excludes candles[-1]"
    },
    "l8_market_context": {
      "enabled": true,
      "pair_direction": "up",
      "btc_direction": "up",
      "eth_direction": "up",
      "relative_strength_vs_btc": "outperforming",
      "relative_strength_vs_eth": "outperforming",
      "direction_alignment": "aligned_with_benchmark",
      "relative_behavior": "stronger_than_benchmarks",
      "market_wind": "benchmark_up",
      "benchmark_mode": "both",
      "self_benchmark": "none",
      "audit_window": {
        "candles_used": 100,
        "window_start": 1780142400,
        "window_end": 1781589600
      }
    }
  }
}
```

**Regels:**
- Elke layer rapporteert `enabled: bool` + `closed_candle_policy`
- L9 slaat geen data op die het zelf kan herberekenen (geen ruwe candles)
- L9 slaat enkel laaguitvoer op als geneste dicts

---

## 6. Voorgesteld future-outcome contract

```json
{
  "pair": "SOLEUR",
  "timeframe": 60,
  "snapshot_timestamp": 1781589600,
  "future_windows": {
    "next_3_candles": {
      "candle_count": 3,
      "return_pct": 1.23,
      "max_up_pct": 2.10,
      "max_down_pct": -0.45,
      "range_pct": 2.55,
      "direction_after_window": "up",
      "volatility_after_window": 0.82,
      "did_continue_direction": true,
      "did_reverse_direction": false,
      "did_expand_range": true,
      "did_compress": false
    },
    "next_5_candles": { ... },
    "next_10_candles": { ... },
    "next_20_candles": { ... }
  }
}
```

**Verboden woorden in outcome:**
profit, loss, win, trade, entry, exit, stop loss, take profit, long, short, buy, sell, setup, signaal, signal

**Toegestane termen:**
return_pct, max_up_pct, max_down_pct, range_pct, direction, volatility, did_continue, did_reverse, did_expand, did_compress

---

## 7. Minimale MVP voor L9 Phase A

### Wat L9 Phase A minimaal moet doen:

1. **Eén snapshot per pair/tf** opslaan op een gegeven timestamp
2. **Twee lagen lezen:** L6 (candle micro) + L8 (market context)
3. **Future outcome meten** over next_3, next_5, next_10, next_20 candles
4. **Geen database** — enkel JSON-bestand per snapshot
5. **Geen dashboard** — enkel CLI-output of file dump

### Voorgestelde repo-structuur:

```text
projects/hermes-v01/layer9_validation/
  __init__.py
  validation_lab.py          — orchestrator: snap + measure + save
  snapshot_builder.py        — bouwt snapshot uit L6 + L8 met pre-fetched candles
  future_measure.py          — meet future outcome uit volgende candles
  config.py                  — windows, lookback, thresholds
  tests/
    test_validation_lab.py
```

### Data-functies voor L9 MVP:

```python
# Snapshot: bouw laag-uitvoer uit historische candles
def build_snapshot(pair, timeframe, pair_candles, btc_candles, eth_candles):
    l6 = analyze_candle_micro(pair_candles, pair=pair, timeframe=timeframe)
    l8 = read_market_context_from_candles(pair, timeframe, pair_candles, btc_candles, eth_candles)
    return { "pair": pair, "timeframe": timeframe, "layers": { "l6": l6, "l8": l8 } }

# Future: meet wat de volgende N candles deden
def measure_future(pair_candles, snapshot_index, windows=[3,5,10,20]):
    # snapshot_index = index van de laatste gesloten candle in de snapshot
    # future candles = pair_candles[snapshot_index+1 : snapshot_index+1+window]
    ...
```

---

## 8. Niet doen

- **Geen L2/L3/L4 in L9 MVP** — deze hebben geen pure functie en geen closed-candle garantie
- **Geen L7 in L9 MVP** — wrapper fetch, interne functies hebben geen `_from_candles` sig
- **Geen database** — MVP is bestand-gebaseerd
- **Geen dashboard/route** — MVP is CLI-only
- **Geen tradebot-koppeling** — L9 is validatie, geen productie
- **Geen AI/voorspelling** — L9 meet alleen achteraf
- **Geen koop/verkoop/long/short/entry/exit/setup/signaal** in output
- **Geen herschrijving van bestaande lagen** zonder apart akkoord

---

## 9. Risico's

| Risico | Ernst | Mitigatie |
|--------|-------|-----------|
| L2/L3/L4 niet replay-safe | **HOOG** | L9 MVP slaat deze over. Aparte refactor nodig voor L9B. |
| L7 niet replay-safe | **HOOG** | L7 interne functies zijn zuiver. Maak `_from_candles` wrapper indien nodig voor L9B. |
| Candles-index bij snapshot | **MEDIUM** | `snapshot_index` moet exact wijzen naar laatste gesloten candle. Eén-offs veroorzaken verschoven resultaten. |
| BTC/ETH data mismatch | **MEDIUM** | L9 moet 3 candlereeksen synchroniseren op timestamp. Niet op index. |
| Lookback-venster overlap | **LAAG** | Bij aaneengesloten snapshots overlappen windows. L9 moet schuivend of per timestamp werken. |
| JSON-bestand groeit | **LAAG** | Elke snapshot ~5KB. 1000 snapshots = 5MB. Acceptabel voor MVP. |

---

## 10. Conclusie

```text
Klaar voor L9 Phase A: ✅ JA
```

**Waarom:**
- L6 en L8 hebben pure functies die historische candles accepteren
- Beide lagen hebben closed-candle policy
- Future outcome meting is rekenwerk op volgende candles (geen AI)
- MVP is klein: 1 orchestrator + 2 helpers + config
- Geen bestaande code hoeft gewijzigd te worden

**Voorwaarden:**
- L9 Phase A gebruikt enkel L6 + L8 (geen L2/L3/L4/L7)
- L9 Phase A is bestand-gebaseerd, geen database
- L9 Phase A heeft geen route, dashboard of tradebot-koppeling
- L9 Phase A output bevat geen trade-taal
- L7/L2/L3/L4 pure-functie refactors zijn aparte taken (L9B of later)
