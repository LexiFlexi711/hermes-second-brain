---
type: fix
date: 2026-07-01
project: hermes-v03-interpreter
tags: [audit, l4, sqlite, integrity, tests]
status: verified
---

# L4 Audit Tools Hardening

## Wat er gebeurde

Commit `5f05dfe7` (direct na `b6f3c343`) hardent de audit checks in `audit_l4_store_integrity.py`. Mismatches die eerder warnings waren, zijn errors geworden — exit code is nu 1 ipv 0 bij integriteitsproblemen.

## Wat er veranderde — `audit_l4_store_integrity.py`

**Fix 1 — Integriteitsmismatches van warning → error:**

| Check | Vorige status | Nieuwe status |
|-------|--------------|---------------|
| `raw_blobs.last_ts` != `raw.meta.last_ts` | warning | error: `last_ts_mismatch` |
| `snapshot_timeframes.last_ts` != `meta.last_ts` | warning | error: `last_ts_mismatch` |
| `snapshot_timeframes.source_requested` != `meta.source_requested` | warning | error: `source_requested_mismatch` |
| `snapshot_timeframes.candles_final` != `meta.candles_final` | warning | error: `candles_final_mismatch` |
| `raw.meta.*` != `snapshot_timeframes.meta.*` (6 velden) | warning | error: `meta_consistency_*` |

Enige overblijvende `add_warning`: diagnostics_json parsefout (niet-kritiek).

**Fix 2 — raw_hash canonical herberekening:**

- Hash wordt berekend op `_sha256_obj(raw_obj)` — canonical JSON object, niet op opslagstring
- Nieuwe check: als `raw_json_str != canonical_raw_json` → error `raw_json_not_canonical`
- Bewijst dat L4 canonical opslaat zoals contract vereist

## Tests toegevoegd — `test_tools_audit_integrity.py`

| Test | Scenario | Resultaat |
|------|----------|-----------|
| 8 | raw_blobs last_ts mismatch | FAIL + `last_ts_mismatch` |
| 9 | snapshot_timeframes source_requested mismatch | FAIL + `source_requested_mismatch` |
| 10 | raw vs snapshot_timeframe meta consistency | FAIL + `meta_consistency_*` |
| 11 | noncanonical raw_json (indent/unsorted) | FAIL + `raw_json_not_canonical`, hash nog correct |
| 12 | canonical DB als controle | PASS |

## Testresultaten

- **Audit tools:** 59 ✅ / 0 ❌
- **L4 snapshot store:** 162 ✅ / 0 ❌

## Geraakte files

Enkel:
- `tools/audit_l4_store_integrity.py` (+43/-18)
- `tools/test_tools_audit_integrity.py` (+142)

Geen L5, geen price events, geen analyst, geen trader, geen interpreter layer, geen storage redesign.

## Context

De tools zitten in `projects/hermes-v03-interpreter/tools/`, niet in `crypto-data/`. Bevestigd met `b6f3c343` (Add interpreter audit tools for L4 store verification).
