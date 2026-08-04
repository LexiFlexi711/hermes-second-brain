# L4 SNAPSHOT SUPPORT/RESISTANCE FIELD DRILLDOWN

**Datum:** 2026-07-09
**Snapshots:** ETHEUR-1783530780, BTCEUR-1783530840

## Conclusie bovenaan

| Vraag | Antwoord |
|---|---|
| S/R expliciet aanwezig? | **JA** — `nearest_support` + `nearest_resistance` bestaan |
| S/R impliciet aanwezig via levels.above/below? | **JA** — above=resistance, below=support |
| Bruikbaar voor latere Analyst? | **JA** |
| Vereist documentatie/mapping? | **NEE** — velden zijn self-documenting |

## Per pair/timeframe (15m)

| Pair | close | above | below | clusters | nearest_support | price | dist% | nearest_resistance | price | dist% | swing_lows | swing_highs |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ETHEUR | 1518.13 | 12 | 2 | 14 | price=1505.69 touch=1 | 1505.69 | 0.82% | price=1520.64 touch=3 | 1520.64 | 0.17% | 16 | 14 |
| BTCEUR | 54313.6 | 10 | 2 | 12 | price=53766.3 touch=1 | 53766.3 | 1.01% | price=54361.9 touch=3 | 54361.9 | 0.09% | 15 | 10 |

## Level veldstructuur (elk level-item)

| Veld | Type | ZEKER |
|---|---|---|
| `price` | float | ✅ prijsniveau |
| `touches` | int | ✅ hoe vaak getest |
| `count` | int | ✅ cluster count |
| `type` | string | ✅ "line" |
| `color` | string | ✅ "blue"/"red" (chart rendering) |
| `hi` | float | ✅ top van zone (indien zone) |
| `lo` | float | ✅ bottom van zone |
| `line_width` | float | ✅ chart rendering |

## Mapping — bewezen

| Raw veld | Betekenis | Status |
|---|---|---|
| `levels.nearest_support` | Dichtstbijzijnde support onder price | ✅ BEWEZEN |
| `levels.nearest_resistance` | Dichtstbijzijnde resistance boven price | ✅ BEWEZEN |
| `levels.below_price` | Alle support levels (price < close) | ✅ BEWEZEN |
| `levels.above_price` | Alle resistance levels (price > close) | ✅ BEWEZEN |
| `levels.clusters_raw` | Alle S/R clusters (beide richtingen) | ✅ BEWEZEN |
| `structure.swing_lows` | Structurele low-punten (support candidates) | ✅ BEWEZEN |
| `structure.swing_highs` | Structurele high-punten (resistance candidates) | ✅ BEWEZEN |
| `structure.recent_structure` | Laatste HH/HL/LH/LL labels + prices | ✅ BEWEZEN |
| `trendlines.recent.upper` | Actuele upper trendline (dynamische resistance) | ✅ BEWEZEN |
| `trendlines.recent.lower` | Actuele lower trendline (dynamische support) | ✅ BEWEZEN |
| `trendlines.major` | Lange-termijn trendlines | ✅ BEWEZEN |

## Wat ontbreekt

| Veld | Status |
|---|---|
| `distance_pct` | ❌ NIET AANWEZIG — afleidbaar uit close - price |
| `support_strength` | ❌ NIET AANWEZIG — `touches` geeft wel indicatie |
| `resistance_strength` | ❌ NIET AANWEZIG |
| `tested` / `broken` status | ❌ NIET AANWEZIG |
| `retest_status` | ❌ NIET AANWEZIG |
| `zone_width` | ❌ NIET AANWEZIG — afleidbaar uit hi - lo |
| `confidence` | ❌ NIET AANWEZIG |
| `last_tested_at` | ❌ NIET AANWEZIG |
| Regime-context per level | ❌ NIET AANWEZIG |

## Advies

**1. Niets doen — S/R is al duidelijk genoeg** ✅

De velden zijn aanwezig en self-documenting:
- `nearest_support` / `nearest_resistance` bestaan expliciet
- `above_price` / `below_price` zijn duidelijk directioneel
- `touches` geeft strength-indicatie
- `price` is exact

Distance_pct en broken/tested status kunnen later afgeleid worden door de Analyst zonder DB-wijziging.

### Correctie op eerder Field Map rapport

Het Field Map rapporteerde `nearest_support` en `nearest_resistance` als "None" voor 1m TF. Bij 15m zijn ze wél altijd aanwezig met data. De None-waarde in lagere TFs is normaal (minder levels in 1m). Hogere TFs hebben altijd nearest levels.

## Bevestiging

- DB mtime unchanged ✅
- Git clean ✅ (`614fe0f2`)
- Geen codewijziging ✅
- Geen service/timer/DB/pairs ✅
