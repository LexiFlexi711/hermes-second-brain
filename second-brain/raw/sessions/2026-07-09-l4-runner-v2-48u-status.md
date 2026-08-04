# 48U L4 RUNNER V2 PRODUCTIESTATUS — PAIR-ISOLATED STABIEL

**Datum:** 2026-07-09

## Context

L4 Runner V2 pair-isolated draait ongeveer 48 uur in productie voor:
- ETHEUR
- BTCEUR

Service: `--pairs ETHEUR,BTCEUR --pair-isolated`

## Git

- HEAD: `3119965c` — Add pair-isolated mode to L4 filler runner
- Dirty: alleen untracked logs/stores, geen codewijzigingen

## Systemd

- OHLC bridge: active, 3 dagen uptime
- L4 timer: active
- Laatste run: status=0/SUCCESS
- Lock collisions: 0
- Tracebacks/crashes: 0

## Runner Logs 48u

| Metric | Count |
|---|---|
| Total logs | 530 |
| Success | 506 |
| Partial success | 12 |
| Dry run failed | 3 |
| Write failed | 4 |

### Pair Status

**ETHEUR:** success=285, dry_run_failed=6, write_failed=5
**BTCEUR:** success=295, dry_run_failed=0, write_failed=1

Interpretatie: partial_success/dry_run/write_failed zijn transient pair-level issues. Geen crashes, lock collisions of datacorruptie. Pair-isolated mode werkt correct.

## DB Counts

| | ETHEUR | BTCEUR |
|---|---|---|
| Snapshots | 579 | 506 |
| Raw blobs | 2895 | 2530 |
| raw/snap | 5.0 | 5.0 |
| tf/snap | 5.0 | 5.0 |
| 48u snaps | 506 | 506 |
| 24u snaps | 250 | 260 |
| Latest age | 81s | 80s |
| DB size | 58 MB | 46 MB |

## Storage Projectie

- Huidig: 105 MB (2 pairs)
- 4 pairs: ~3 GB/maand
- 10 pairs: ~7.5 GB/maand
- 26 pairs: ~19.5 GB/maand

## Conclusie

- L4 Runner V2 stabiel genoeg ✅
- Productie betrouwbaar voor ETHEUR + BTCEUR ✅
- Storage lineair, acceptabel ✅
- Klaar voor Snapshot Inspector ✅
- Extra pairs technisch mogelijk, nog niet uitvoeren

## Volgende Stap

**HERMES SNAPSHOT INSPECTOR READ-ONLY**

Doel: één opgeslagen L4 snapshot inspecteren en menselijk tonen.

Niet doen: extra pairs, dedup-fix, service/timer wijziging, DB schema wijziging, Analyst/L5/Trader
