---
title: "L4 RUNNER V2 PRODUCTIE ACTIEF — PAIR-ISOLATED MODE"
date: 2026-07-07
type: project
project: hermes-v03-interpreter
component: l4-autofill
status: production-active
related: ["l4-autofill-24u-status", "l4-raw-blobs-dedup-audit"]
commit: 3119965c
---

# L4 RUNNER V2 PRODUCTIE ACTIEF — PAIR-ISOLATED MODE

**Datum:** 2026-07-07

**Commit:** `3119965c` Add pair-isolated mode to L4 filler runner

## Wijziging

De bestaande productie `l4-filler.service` is aangepast.

**Oud:**
```
--pairs ETHEUR,BTCEUR
```

**Nieuw:**
```
--pairs ETHEUR,BTCEUR --pair-isolated
```

**Niet gewijzigd:**
- Geen extra pairs toegevoegd
- Geen code gewijzigd
- Geen commit uitgevoerd
- Geen DB schema wijziging
- Geen OHLC bridge wijziging
- Geen dedup-fix uitgevoerd
- Geen Analyst/L5/Trader toegevoegd

## Dedup-status

Dedup is eerder onderzocht en verklaard in [[l4-raw-blobs-dedup-audit]].
0% raw_blob dedup is verwacht gedrag. Dedup is niet aangepast.

## Bewijs preflight

- `--pair-isolated --no-write` exit code 0
- `pair_isolated`: true
- DB mtime ongewijzigd
- ETHEUR: dry_run_passed_no_write
- BTCEUR: dry_run_passed_no_write

## Service backup

```
/home/sjoe/.config/systemd/user/l4-filler.service.bak_20260707_155607
```

## Service diff

Alleen `--pair-isolated` toegevoegd aan ExecStart.

## Handmatige productie-run

| Pair | Vóór | Na | Delta | Status |
|------|------|----|-------|--------|
| BTCEUR | 212 snapshots | 213 snapshots | +1/+5/+5 | success |
| ETHEUR | 295 snapshots | 296 snapshots | +1/+5/+5 | success |

## Timer-run

| Veld | Waarde |
|------|--------|
| pair_isolated | true |
| status | success |
| exit_code | 0 |
| pairs_success | 2 |
| pairs_failed | 0 |
| successful_pairs | [ETHEUR, BTCEUR] |
| failed_pairs | [] |

| Pair | Final count | Laatste data |
|------|-------------|-------------|
| BTCEUR | 214 snapshots | <40 sec oud |
| ETHEUR | 297 snapshots | <40 sec oud |

## Conclusie

L4 Runner V2 is succesvol actief in productie.
De bestaande twee pairs ETHEUR en BTCEUR groeien automatisch verder.
Pair-isolated mode werkt in productie.
Gezonde pairs kunnen nu los van falende pairs verwerkt worden.

## Volgende stap

Laat dit minstens enkele uren tot 24u draaien.
Daarna pas gecontroleerd uitbreiden naar SOLEUR en XRPEUR via preflight.
