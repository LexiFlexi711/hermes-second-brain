---
title: "24U L4 AUTOFILL STATUS — ETHEUR + BTCEUR STABIEL"
date: 2026-07-07
type: project
project: hermes-v03-interpreter
component: l4-autofill
status: stable
pairs: [ETHEUR, BTCEUR]
---

# 24U L4 AUTOFILL STATUS — ETHEUR + BTCEUR STABIEL

**Datum/tijd:** 2026-07-07

**Kernstatus:** De L4 autofill draait stabiel voor ETHEUR en BTCEUR.

## Bewezen

- OHLC bridge active/running, 2+ dagen uptime
- 26 pairs, cycles met 156 OK / 0 fail
- L4 filler timer active, elke 5 minuten
- Geen echte journal errors/exceptions
- Geen lock collisions
- DB groeit automatisch voor ETHEUR en BTCEUR
- Beide pairs hebben perfecte ratios:
  - raw_blobs / snapshots = 5.0
  - snapshot_timeframes / snapshots = 5.0
- Laatste stored_at < 6 minuten oud

## DB status

### ETHEUR
- snapshots: 281
- raw_blobs: 1405
- timeframe links: 1405
- raw/snap: 5.0
- tf/snap: 5.0
- laatste stored_at: 14:38:45, 323 sec oud

### BTCEUR
- snapshots: 198
- raw_blobs: 990
- timeframe links: 990
- raw/snap: 5.0
- tf/snap: 5.0
- laatste stored_at: 14:38:46, 322 sec oud

## Runner logs 24u

- totaal geanalyseerd: 297
- success: 283
- dry_run_passed_no_write: 5
- dry_run_failed: 4
- write_failed: 5
- failures totaal: 9
- failures zijn ETHEUR transient 1m timeframe_alignment_failed:
  lag=120s > max 60s
- BTCEUR failures: 0

## Audit-correctie

Success rate = 283 / 297 ≈ 95.3% (niet 95.6%).

## Interpretatie

De 9 ETHEUR failures zijn geen datacorruptie.
De filler heeft stale/misaligned 1m data correct geweigerd.
De volgende timer-run herstelde vanzelf.
Dit bewijst dat de guards werken.

## Conclusie

**Stabiel genoeg voor L4 Runner V2.**

## Volgende stap

Bouw L4 Runner V2 — pair-isolated multi-pair mode.

### Doel van V2
- meerdere pairs in één runner/timer kunnen draaien
- elke pair apart preflighten en schrijven
- falende pair overslaan zonder gezonde pairs te blokkeren
- per-pair status in log: success / dry_run_failed / write_failed
- geen Analyst/L5/Trader
- geen DB schema wijziging
- geen strategie/event/outcome/backtest logic

### Belangrijke open observatie

De huidige gecombineerde service kan bij een ETHEUR dry-run failure
ook BTCEUR blokkeren in die run. Daarom is pair-isolated V2 de juiste
volgende bouwstap.
