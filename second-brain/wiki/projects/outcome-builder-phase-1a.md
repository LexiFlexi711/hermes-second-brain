---
title: Outcome Builder Phase 1A
type: project
status: active
commit: 901a68e1
updated: 2026-07-11
---

# Outcome Builder Phase 1A

Read-only prototype. Meet wat er na een L4 snapshot gebeurde.
Descriptieve hindsight. Geen strategie. Geen trade.

## Status

🟢 **GROEN** — geïmplementeerd, getest, Fable-reviewed, gecommit.

## Commit

`901a68e1` — "Add Outcome Builder Phase 1A read-only prototype"

## Wat het doet

- Leest L4 snapshots (SQLite mode=ro)
- Leest live_cache 1m candles
- Berekent outcome windows: 5m, 15m, 60m, 240m
- JSON stdout only
- cache_for_recent_only policy
- fetched_at-based semantic sanity check
- Guardrails op JSON keys/values

## Wat het NIET doet

- Geen A0 parsing
- Geen strategie
- Geen trade-advies
- Geen entry/exit
- Geen win/loss
- Geen storage writes (Phase 1A)
- Geen A1/Strategy/Testbot/Trader

## Architectuur

```
L4 Snapshots + live_cache → Outcome Builder → JSON stdout
```

No-backflow regel: outcome data wordt nooit gelezen door ASOF lagen.

## Tests

- Outcome Builder: 48/48
- A0 (frozen): 68/68
- Inspector: 15/15
- Runner: 76/76
- Totaal: 207/207

## Bestanden

```
projects/hermes-v03-outcome/
  outcome_builder/
    __init__.py
    contracts.py
    l4_reader.py
    ohlc_cache.py
    calculator.py
    guardrails.py
    cli.py
  tests/
    test_outcome_builder.py
```

## CLI

```bash
python3 projects/hermes-v03-outcome/outcome_builder/cli.py \
  --pair ETHEUR --latest \
  --l4-base-dir projects/hermes-v03-interpreter/l4_store \
  --live-cache-dir projects/crypto-data/logs/live_cache \
  --windows 5m,15m,60m,240m --format json
```

## Gerelateerd

- [[a0-snapshot-readout]] — A0 Snapshot Readout (frozen foundation)
- [[hermes-v03-interpreter]] — L4 interpreter/data layer
- [[l4-runner-v2-production-active]] — L4 Runner V2 pair-isolated
- [[2026-07-11-a0-foundation-freeze-and-process-rules]] — A0 freeze + process rules
- [[2026-07-11-outcome-builder-phase-0-plan]] — Outcome Builder plan
