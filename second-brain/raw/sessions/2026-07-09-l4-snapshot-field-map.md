# L4 SNAPSHOT FIELD MAP

**Datum:** 2026-07-09
**Commit:** `614fe0f2` — Snapshot Inspector
**Snapshots:** ETHEUR-1783530780, BTCEUR-1783530840

## 1. Snapshot top-level

| Veld | Type | Bron |
|---|---|---|
| `snapshot_id` | string | PK, format `{PAIR}-{asof_ts}-{tfs}-{hashprefix}` |
| `pair` | string | "ETHEUR" of "BTCEUR" |
| `asof_ts` | int | Unix timestamp van snapshot-moment |
| `stored_at` | int | Unix timestamp van opslag |
| `age_seconds` | int | `now - stored_at` |
| `timeframes_count` | int | 5 |
| `timeframes_present` | list | ["1m","5m","15m","60m","240m"] |
| `raw_blob_count` | int | 5 (één per TF) |
| `completeness` | bool | true als all_5_present |
| `all_5_present` | bool | true |

## 2. DB-relatie

```
snapshots (1)
  → snapshot_timeframes (5)
    → raw_blobs (5)
```

Per snapshot: 5 timeframe-links, 5 raw blobs, 1 blob per timeframe.
Deduplicatie op `raw_hash` dus identieke raw data wordt gedeeld over snapshots heen.

## 3. Timeframes — productie data

| Pair | TF | candle_count | candle_count_source | source_class | source_resolved | source_age_seconds | raw_size |
|---|---|---|---|---|---|---|---|
| ETHEUR | 1m | 240 | meta.candles_final | mixed | auto_archive_plus_cache | ~120s | 5.5 KB |
| ETHEUR | 5m | 240 | meta.candles_final | mixed | auto_archive_plus_cache | ~125s | 14.4 KB |
| ETHEUR | 15m | 240 | meta.candles_final | mixed | auto_archive_plus_cache | ~130s | 20.2 KB |
| ETHEUR | 60m | 240 | meta.candles_final | mixed | auto_archive_plus_cache | ~140s | 26.9 KB |
| ETHEUR | 240m | 240 | meta.candles_final | mixed | auto_archive_plus_cache | ~150s | 26.1 KB |
| BTCEUR | 1m | 240 | meta.candles_final | mixed | auto_archive_plus_cache | ~120s | 3.9 KB |
| BTCEUR | 5m | 240 | meta.candles_final | mixed | auto_archive_plus_cache | ~125s | 12.5 KB |
| BTCEUR | 15m | 240 | meta.candles_final | mixed | auto_archive_plus_cache | ~130s | 17.8 KB |
| BTCEUR | 60m | 240 | meta.candles_final | mixed | auto_archive_plus_cache | ~140s | 26.3 KB |
| BTCEUR | 240m | 240 | meta.candles_final | mixed | auto_archive_plus_cache | ~150s | 26.9 KB |

## 4. Source velden

Per timeframe in `meta`:

| Veld | Altijd aanwezig | Soms null | Betekenis |
|---|---|---|---|
| `source_class` | ✅ | — | "mixed" |
| `source_resolved` | ✅ | — | "auto_archive_plus_cache", "cache", "archive" |
| `source_age_seconds` | ✅ | ✅ | Kan null zijn voor archive-only |
| `source_generated_at` | ✅ | ✅ | Unix ts of null |
| `source_requested` | ✅ | — | "auto" |
| `source_paths` | ✅ | — | list van gebruikte bronpaden |

## 5. Meta velden (23 keys, alle TFs identiek)

| Veld | Type | Betrouwbaar voor audit |
|---|---|---|
| `schema_version` | int | ✅ |
| `pair` | string | ✅ |
| `tf` | string | ✅ |
| `candles_final` | int | ✅ primaire candle count bron |
| `candles_before_filter` | int | ✅ |
| `candles_after_filter` | int | ✅ |
| `effective_limit` | int | ✅ |
| `limit_requested` | int | ✅ |
| `first_ts` | int | ✅ |
| `last_ts` | int | ✅ |
| `first_date` | string | ✅ |
| `last_date` | string | ✅ |
| `candle_current_closed` | bool | ✅ |
| `candle_previous_closed` | bool | ✅ |
| `source_class` | string | ✅ |
| `source_resolved` | string | ✅ |
| `source_age_seconds` | int/null | ⚠️ null bij archive |
| `source_generated_at` | int/null | ⚠️ |
| `source_requested` | string | ✅ |
| `source_path` | string/null | ⚠️ |
| `source_paths` | list | ✅ |
| `start` | int | ✅ |
| `end` | int | ✅ |

## 6. Price velden

**price.current** (6 keys, DICT — géén candle-array):
- `open`, `high`, `low`, `close`, `timestamp`, `volume`

**price.previous** (6 keys, DICT):
- `open`, `high`, `low`, `close`, `timestamp`, `volume`

**LET OP:** Dit zijn de laatste 2 candles (huidige + vorige). De volledige candle-array (240 candles) zit elders in de raw structuur.

## 7. Indicator velden

| Groep | Keys | ZEKER/ONZEKER |
|---|---|---|
| **EMA** | `fast_last`, `slow_last`, `regime` (aligned/compressing/crossing), `cross` (direction/aligned/warning) | ✅ ZEKER |
| **ATR** | `value`, `atr_pct`, `volatility_state` | ✅ ZEKER |
| **ADX** | `adx`, `plus_di`, `minus_di`, `di_bias`, `trend_strength` | ✅ ZEKER |
| **VWAP** | `value`, `std_dev`, `upper_band`, `lower_band`, `bars_used`, `volume_empty` | ✅ ZEKER |
| **Volume** | `current_volume`, `avg_volume`, `volume_ratio`, `spike`, `strong_spike`, `volume_trend`, `volume_empty` | ✅ ZEKER |

Alle 5 indicatorgroepen aanwezig in alle TFs, beide pairs.

## 8. Candle_micro velden

| Veld | Type | ZEKER/ONZEKER |
|---|---|---|
| `body_trend` | string | "expanding"/"contracting"/"mixed" |
| `candle_count` | int | 5 (laatste N candles geanalyseerd) |
| `direction_summary` | dict | bullish/bearish/doji counts |
| `last` | dict | body_pct, direction, lower_wick_pct, pattern, upper_wick_pct |
| `micro_state` | string | "mixed"/"rejection_like" etc. |
| `patterns` | list | patterns van laatste candles |
| `wick_bias` | string | "lower_wicks"/"upper_wicks"/"mixed" |

## 9. Structure velden

Per TF aanwezig:
- `swing_highs`: list (groeit met TF)
- `swing_lows`: list (groeit met TF)
- `classified_highs`: list
- `classified_lows`: list
- `fractal_count`: int
- `labels`: list
- `recent_structure`: dict (`last_high_label`, `last_high_price`, `last_low_label`, `last_low_price`)

Hogere TFs hebben meer structure points (1m: ~2, 240m: ~35).

## 10. Levels velden

Per TF:
- `above_price`: list (resistance levels)
- `below_price`: list (support levels)
- `clusters_raw`: list (S/R clusters)
- `nearest_resistance`: dict of None
- `nearest_support`: dict of None
- `structure_points`: list (alle structure points)

## 11. Trendlines velden

- `recent`: dict — `enabled`, `lower`, `upper`, `reason`, `status`, `trend`
- `major`: dict — `both_present`, `lower`, `upper`

## 12. Diagnostics + Summary

- `diagnostics`: `warnings` (list), `missing` (list), `no_trade_decision` (bool)
- `summary`: `enabled` (bool), `reason` (string)

## 13. Wat Hermes hiermee later kan

- ✅ As-of replay met 240 candles per TF
- ✅ Multi-timeframe snapshot audit
- ✅ Indicator-staat inspecteerbaar
- ✅ Bronkwaliteit controleerbaar (source class/age/resolved)
- ✅ Structure/levels/trendlines aanwezig voor charting
- ✅ Candle_micro voor prijsactie-analyse
- ✅ Latere Analyst/L5 kan hieruit putten

## 14. Wat ontbreekt / onzeker

| Item | Status |
|---|---|
| Volledige candle-array (niet alleen laatste 2) | ⚠️ ONZEKER — wel 240 candles in meta maar array pad onbekend |
| Regime-detectie veld | ❌ NIET AANWEZIG — losse indicatorwaarden wel, geen geaggregeerd regime |
| Bias/sentiment veld | ❌ NIET AANWEZIG |
| MTF alignment veld | ❌ NIET AANWEZIG — moet later uit meerdere TFs afgeleid |
| S/R levels numeriek | ✅ ZEKER (structure_points, clusters, above/below) |
| Trendline numeriek | ✅ ZEKER (recent/major upper/lower) |

## 15. Bevestiging

- DB mtime unchanged ✅
- Geen codewijziging ✅
- Geen service/timer wijziging ✅
- Geen DB schema wijziging ✅
- Geen dedup-fix ✅
- Geen extra pairs ✅
- Geen Analyst/L5/Trader ✅
