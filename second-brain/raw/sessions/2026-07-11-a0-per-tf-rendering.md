# A0 Phase 1 — Per-TF Rendering & Empty Section Fixes

type: synthesis
date: 2026-07-11
tags: [a0, hermes-v03-analyst, snapshot, rendering, per-tf, audit]

## Samenvatting

A0 Snapshot Readout Phase 1 is in één sessie van "toont lege secties" naar "toont alle data per timeframe" gegaan. Drie iteraties:

### Iteratie 1 — Empty Sections Explicit

Probleem: SUPPORT/RESISTANCE en TRENDLINES waren leeg bij BTCEUR. Auditmatig ambigu.

Fix: `section_status: no_whitelisted_values_present` toegevoegd aan `_build_structure`, `_build_support_resistance`, `_build_trendlines` in templates.py. Ook JSON builders toegevoegd.

Status: ✅ gecommit in 735dd471

### Iteratie 2 — Meaningful TF Fallback

Probleem: A0 toonde `section_status` terwijl data wél bestond op hogere TFs. `_first_tf_with_data()` pakte blind 1m, die vaak leeg is.

Fix: `_find_structure_tf()`, `_find_levels_tf()`, `_find_trendlines_tf()` — selectors die eerste TF met echte data (non-empty dict/lists) pakken.

Status: ✅ gewerkt, maar superseded door Iteratie 3

### Iteratie 3 — Per-TF Rendering (FINAL)

Probleem: Lexi wou ALLE TFs zien, niet "de beste TF". Contract: Hermes-v03 genereert per TF, L4 slaat per TF op, A0 moet per TF tonen.

Hard audit bewees:
- Hermes-v03 L8_synthesis: `synthesize(pair, tf)` — per TF ✅
- L4 raw_blobs: 5 unieke hashes, per TF data ✅
- A0: toonde maar 1 TF — BUG ❌

Fix: Alle drie builders herschreven om over `REQUIRED_TIMEFRAMES` te itereren. Per TF: stored_values als data, anders section_status.

Commit: `735dd471` — "Render A0 market context per timeframe"

## Hard Audit Bevindingen

### Per-TF Data Audit (ETHEUR + BTCEUR)

| TF | structure | levels | trendlines |
|----|-----------|--------|------------|
| 1m | leeg/None | ns=None, nr=None | lower/upper None |
| 5m | ✅ data | ✅ dict data | ✅ bij ETHEUR, leeg bij BTCEUR |
| 15m | ✅ data | ✅ dict data | ✅ bij ETHEUR, upper bij BTCEUR |
| 60m | ✅ data | ✅ 14-16 levels | ✅ 4 lijnen |
| 240m | ✅ data | ✅ 11-14 levels | ✅ 4 lijnen |

1m leeg is verwacht — te weinig swing points op 1-minuut candles.

### OHLC Boundary Condition

BTCEUR 12:00 UTC snapshot toonde identieke OHLC voor alle TFs. Geen bug — round-hour grens waar alle candles tegelijk rollen. Snapshot om 11:49 toont wél verschillende current candles per TF.

## Bestanden

- `projects/hermes-v03-analyst/a0_snapshot_readout/templates.py` — per-TF builders
- `projects/hermes-v03-analyst/tests/test_a0_snapshot_readout.py` — 61 tests

## Contract

- A0 berekent niets — toont alleen wat in L4 raw_blobs zit
- Per TF: stored_values of section_status
- Geen MTF-oordeel, geen "beste TF", geen interpretatie
- CANDLE MICRO en INDICATORS blijven single-TF fallback
