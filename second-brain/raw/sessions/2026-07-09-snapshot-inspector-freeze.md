# L4 SNAPSHOT INSPECTOR READ-ONLY GECOMMIT

**Datum:** 2026-07-09

**Commit:** `614fe0f2` — Add read-only L4 snapshot inspector

## Files

- `projects/hermes-v03-interpreter/tools/inspect_l4_snapshot.py`
- `projects/hermes-v03-interpreter/tools/test_inspect_l4_snapshot.py`

## Doel

Read-only tool om één opgeslagen L4 snapshot te inspecteren en menselijk/JSON te tonen wat Hermes daarin ziet.

## Bug gevonden vóór commit

- Eerste versie telde foutief 6 candles door dict keys van `price.current` te tellen
- Correctie: `candle_count` gebruikt nu `meta.candles_final` als primaire bron
- Defensieve fallback toegevoegd voor ontbrekende meta

## Real productie bewijs

- ETHEUR: 240 candles per TF (1m/5m/15m/60m/240m)
- BTCEUR: 240 candles per TF
- `candle_count_source = meta.candles_final`
- DB mtime unchanged

## Tests groen

- `test_inspect_l4_snapshot.py`: 14/14
- `test_run_l4_filler_once.py`: 76/76
- `test_fill_l4_snapshot_store.py`: 61/61

## Bevestiging

- Geen service/timer wijziging
- Geen DB schema wijziging
- Geen dedup-fix
- Geen extra pairs
- Geen Analyst/L5/Trader
- Geen entry/exit/long/short/buy/sell logic

## Conclusie

Snapshot Inspector is veilig bevroren. Volgende stap: L4 Snapshot Field Map maken — wat zit er werkelijk in een snapshot, per timeframe.
