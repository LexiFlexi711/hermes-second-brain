---
title: "L4 RAW_BLOBS DEDUP AUDIT — 0% DEDUP VERKLAARD"
date: 2026-07-07
type: project
project: hermes-v03-interpreter
component: l4-autofill
status: audited
related: ["l4-autofill-24u-status"]
---

# L4 RAW_BLOBS DEDUP AUDIT — 0% DEDUP VERKLAARD

**Datum:** 2026-07-07

**Context:** Na 24u L4 autofill stabiliteit en Runner V2 pair-isolated commit werd onderzocht waarom raw_blobs 0% hergebruik tonen.

**Belangrijkste resultaat:** 0% raw_blob dedup is verwacht gedrag en geen bug.

## DB stats

### BTCEUR
- snapshots: 210
- raw_blobs: 1050
- distinct_raw_hashes: 1050
- dedup: 0%

### ETHEUR
- snapshots: 293
- raw_blobs: 1465
- distinct_raw_hashes: 1465
- dedup: 0%

## Raw hash definitie

`raw_hash` = SHA-256 van volledige `raw_json`:
- candles
- meta
- source_paths
- indicators
- candle_micro
- price/current
- price/previous

**Code:** `L3_snapshot_build/__init__.py`
```python
raw_hash = _sha256_obj(raw)
```

**Canonical JSON:** `json.dumps(obj, sort_keys=True, separators=(",",":"), ensure_ascii=False)`

Er worden **geen** volatile velden uitgesloten.

## Deep diff conclusie

Alle timeframes tonen veranderende raw inhoud tussen opeenvolgende snapshots.

| TF | Oorzaak |
|----|---------|
| 1m | Nieuwe candle, candle_micro changes, patterns/direction veranderen |
| 5m/15m | Huidige/open candle verandert, EMA/ATR/ADX en patterns herberekenen |
| 60m/240m | Minder candle changes, maar indicators/patterns/candle_micro herberekenen, meta verandert |

**Volatile velden:**
- `source_age_seconds` verandert
- `source_generated_at` kan veranderen
- `last_ts` kan veranderen
- current/open candle drift kan veranderen

**Nuance:** `source_age_seconds` is op zichzelf al voldoende om raw_hash te wijzigen. Maar in de praktijk veranderen ook candles, indicators en candle_micro mee. 0% dedup is niet alleen door metadata veroorzaakt.

## Conclusie

- 0% raw_blob hergebruik op alle pairs en TFs
- Geen datacorruptie
- Content-addressable storage werkt correct
- Elke raw_hash verwijst naar de exacte volledige Hermes-output van dat moment
- Het systeem bewaart snapshots eerlijk en reproduceerbaar

## Advies

**Nu niets wijzigen.**

Niet doen:
- raw_hash niet aanpassen
- volatile metadata nu niet uitsluiten
- geen stable_raw_hash toevoegen
- geen raw/candles architectuurwijziging
- geen DB schema wijziging

**Reden:** Voor 2 pairs is opslaggroei acceptabel. Bij opschaling naar veel pairs moet opslagcapaciteit opnieuw gemeten worden met echte DB-groei.

## Open follow-up (later)

Voor uitbreiding naar veel pairs:
- meet echte DB-groei per 24u
- bereken projectie voor 4/10/26 pairs
- pas daarna beslissen over retentie, compression, archive of stable hash ontwerp

## Projectstatus na deze audit

- L4 autofill stabiel
- Runner V2 pair-isolated gecommit (3119965c)
- Dedup verklaard
- Geen dedup-fix nodig vóór productie switch naar `--pair-isolated`
