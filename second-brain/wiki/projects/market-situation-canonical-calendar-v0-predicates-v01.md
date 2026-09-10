---
title: Market Situation V0 — Canonical Calendar Replication + Nieuwe Predicates V0.1
type: project
status: afgerond
date: 2026-09-08
tags: [noa-reign, market-situation, canonical-calendar, predicates, replication, pit-safety]
---

# Market Situation V0 — Canonical Calendar Replication + Predicates V0.1

Twee afgeronde studies op de gefrozen Market Situation V0-basis
(`8ba1a8da`), Study Runner V0 (`dd7ff37a`), Foundation RC2 (`e513700c`),
historical-synthesis fix (`34dc263f`).

## Deel 1 — Canonical Calendar Replication V0

**FINAL STATUS: CANONICAL_CALENDAR_REPLICATION_V0_COMPLETE**

Uniforme, vooraf geregistreerde 9-weekse kalenderreplicatie (2026-07-04 → 2026-09-05 UTC),
15m cadans, 672 canonical_T per week.

| Week | Venster | Resultaat |
|------|---------|-----------|
| CAL_01 | 07-04 → 07-11 | 672/672 |
| CAL_02 | 07-11 → 07-18 | 672/672 |
| CAL_03 | 07-18 → 07-25 | 672/672 |
| CAL_04 | 07-25 → 08-01 | 672/672 |
| CAL_05_DISCOVERY | 08-01 → 08-08 | 672/672 |
| CAL_06 | 08-08 → 08-15 | 672/672 |
| CAL_07 | 08-15 → 08-22 | 672/672 |
| CAL_08 | 08-22 → 08-29 | 672/672 |
| CAL_09 | 08-29 → 09-05 | 672/672 |

- GOLDEN CHECK PASS: CAL_05 = 672 records, 5975 situations,
  hash `8a2cf8f44373a70fdce183163a927936ed66f7a8c9df397d68b57ac2c86012c1`
  → `DISCOVERY_GOLDEN_IDENTICAL = YES`.
- CAL_06..CAL_09 byte-identiek aan eerdere replicatie-weken.
- Watch-list sign-consistentie (8 vergelijkingsweken, 240m close_delta):
  - A `CONTINUATION_STATE@240m`: 6 neg / 2 pos → bevestigd negatief
  - B `STRUCTURE_TRANSITION@240m`: 6 pos / 2 neg → bevestigd positief
  - C `STRUCTURE_TRANSITION@60m`: 5 pos / 3 neg → instabiel
  - D `EMA_STATE|SHORT`: 6 pos / 2 neg → bevestigd (kleine magnitude)
  - E `MTF_DIRECTION_CONFLICT`: 4 pos / 4 neg → **niet bevestigd** (correctie t.o.v. eerdere observatie)
- `TREND_STATE` en `EMA_STATE` (overall) zijn tautologisch (n=672/week, mediaan == baseline exact).

## Deel 2 — Nieuwe Market Situation Predicates V0.1

**FINAL STATUS: NEW_MARKET_SITUATION_PREDICATES_V01_VALIDATED**

Drie zuiver additieve, PIT-safe types bovenop de bestaande zes:

| Type | Hergebruikte reader-fields | Richting |
|------|---------------------------|----------|
| `LEVEL_PROXIMITY_STATE` | `levels.nearest_resistance/support` (price/lo/hi/count/touches), `indicators.atr.value`, `price.current.close` | near support = LONG, near resistance = SHORT |
| `WICK_BIAS_STATE` | `candle_micro.wick_bias` | upper_wicks = SHORT, lower_wicks = LONG |
| `HIGH_VOLATILITY_STATE` | `indicators.atr.volatility_state` | NEUTRAL |

- FROZEN threshold: `1.0 × ATR.value`, zone-aware afstand (niet blind mid-price).
- Zone-regel: high < zone_low of low > zone_high ⇒ geen test (geen proximity-marge).
- Tests: 27/27 pass (zone-aware 7 cases, wick, vola, PIT source-audit, future-invariance,
  no-outcome-dependency, determinism, golden comparison, no-implicit-move-selection).
- 9-weekse run: alle weken `golden_match=True`; 672/672, 0 dup, 0 guard/outcome failures.
- `EXISTING_SIX_CHANGED = NO` — bewezen op twee manieren: code-diff (enkel docstring +
  3 functies + 3 calls) én runtime (hash van de zes types byte-identiek in alle 9 weken).
- `RUNNER_CHANGED = NO` (enkel `evaluate_situations` gemonkeypatcht).
- Sign-consistentie nieuwe types (8 niet-discovery weken, 240m):
  - `LEVEL_PROXIMITY_STATE`: 5 pos / 2 neg / 1 zero (kleine deltas)
  - `WICK_BIAS_STATE`: 2 pos / 6 neg (magnitude verwaarloosbaar 0.0006–0.0073)
  - `HIGH_VOLATILITY_STATE`: 3 pos / 3 neg / 1 zero
  - Subgroep `LEVEL_PROXIMITY|LONG` (near support): 7/1 pos — naïeve referentie, geen significantieclaim.
- ATR-eerlijkheidsnoot (verbatim in rapport): ATR/volatility_state is PIT-safe
  backward-looking context en dus gecorreleerd met recente candle-ranges — geen future leak,
  maar ook NIET volledig onafhankelijk van recente prijsactie.
- Geen tuning, geen code-commit, geen push, geen nieuwe periodes.

## Artefacten

- `/mnt/otherdrive1/dataLexi/LexiProjects/tmp/study_runner_v0/canonical_calendar_v0/`
  (`canonical_calendar_report.txt`, `calendar_accounting.json`, CAL_01..CAL_09)
- `/mnt/otherdrive1/dataLexi/LexiProjects/tmp/study_runner_v0/new_predicates_v01/`
  (`market_situations/__init__.py`, `tests/test_new_predicates.py`, `run/`)

## Gerelateerd

- [[crypto-predictor-evaluation]] · [[crypto-evaluation-protocol]] · [[noa-reign-roadmap-v2]]
