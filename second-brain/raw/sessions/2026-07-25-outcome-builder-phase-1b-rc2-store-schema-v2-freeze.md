# Outcome Builder Phase 1B — RC2 Store Schema v2 Freeze

- **Titel:** RC2 Store Schema Version 2 — Canonical Hash Freeze
- **Datum:** 2026-07-25
- **Status:** frozen architecture decision
- **Repo:** /mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign

## Branches en Commits

| Label | Branch | Commit |
|-------|--------|--------|
| RC1 | candidate/phase1b-rc1-20260723 | 7671b52f53a9eaee06fa7126c3abd0fe4152ee71 |
| RC2 | candidate/phase1b-rc2-20260723 | b31cb8420bec169a08e0d4508a343bf3e73bdb72 |
| Base (main) | main | b07daaf83558e832f5b72d31474f2f7256788b32 |
| Main status at RC2 | — | b07daaf8 (onveranderd) |

RC2 bouwt rechtstreeks op main (merge-base = b07daaf8). Candidate staat 3 commits vóór main: RC1 → RC2 → auto-sync (b5f5b9a, enkel .bak bestand).

## Waarom STORE_SCHEMA_VERSION van 1 naar 2

De canonical JSON in v1 produceerde `1.0` voor integer floats. Dit gaf andere JSON-bytes dan `1` (integer), terwijl de numerieke waarde identiek is. Hashes gebaseerd op deze JSON waren dus instabiel: dezelfde rekenkundige data kon verschillende hashes krijgen afhankelijk van Python's interne float-representatie.

RC2 lost dit op door exponentvrije numeric tokens in canonical JSON:
- `1` en `1.0` → beide `1` in canonical JSON (identieke bytes)
- `1.5` → blijft `1.5`
- `-0.0` → wordt `0`
- Kleine floats zonder decimalen → integer representatie

## Exacte canonical JSON-wijziging

Bestand: `outcome_builder/canonical_json.py`

Kernfunctie: `_canonical_float_value(value: float) -> int | float`

```python
def _canonical_float_value(value):
    if value == int(value) and value != 0:
        return int(value)
    if value == 0:
        return 0  # -0.0 → 0
    return value
```

## String-collisie

`"1"` (string) blijft een string en collidet niet met `1` (integer/float). JSON onderscheidt strings van numbers op token-niveau — canonical JSON behoudt dit onderscheid.

## Gevolg voor hashes en outcome_id

- Alle hashes (outcome_id, record_id, record_hash, windows_hash) zijn deterministisch voor identieke numerieke data
- v1 en v2 produceren verschillende outcome_id's voor dezelfde snapshot+windows combinatie
- Daarom: stille compatibiliteit met v1 is verboden

## v1 Candidates Hard Geweigerd

- v1 records worden niet geaccepteerd in v2 store
- stored v1 records worden behandeld als corruption
- store_schema_version == 2 is verplicht in alle nieuwe records
- v2 golden identities: outcome_id, record_id, record_hash herbouwd met v2 canonical

## RC2 Gewijzigde Bestanden

```
M  outcome_builder/canonical_json.py       (+163/-? regels)
M  outcome_builder/outcome_store.py         (+654/-? regels)
A  outcome_builder/phase1a_adapter.py       (+120 regels)
M  outcome_builder/store_cli.py             (+412/-? regels)
M  outcome_builder/store_contracts.py       (+86/-? regels)
M  tests/test_outcome_store.py              (+1596/-404 regels, +1192 netto)
```

## Test Counts

| Fase | Tests | Delta |
|------|-------|-------|
| RC1 (7671b52f) | 118 (pytest --collect-only) | — |
| RC2 (b31cb842) | 138 (pytest --collect-only) | +20 |
| RC2 candidate (na AST-patch) | 138 | — |

De +20 tests in RC2 omvatten o.a.:
- TestV2CanonicalRegression (8 tests)
- TestV2OutcomeIdDiffersFromV1 (2 tests)
- TestV2DeterministicHashes (3 tests)
- Extra backflow/existing tests (7 tests)

## Testcommando's

```bash
# Phase 1A
python3 -m pytest projects/hermes-v03-outcome/tests/test_outcome_builder.py -q

# Phase 1B
python3 -m pytest projects/hermes-v03-outcome/tests/test_outcome_store.py -q

# A0
python3 -m pytest projects/hermes-v03-analyst/tests/test_a0_snapshot_readout.py -q

# Inspector
python3 -m pytest projects/hermes-v03-interpreter/tools/test_inspect_l4_snapshot.py -q

# Runner
python3 -m pytest projects/hermes-v03-interpreter/tools/test_run_l4_filler_once.py -q
```

## Bekende Resterende Risico's

1. **Interpreter index mismatch**: `idx_snapshots_pair_asof` indexeert op kolom `pair`, maar `query_snapshots` filtert op `WHERE pair_id = ?`. Hoewel `pair` en `pair_id` identiek zijn voor canonical pairs, is de index mismatch een latent risico — de database kan de index niet gebruiken voor de query. (Bestand: L4_snapshot_store/__init__.py, regels 130-131 vs 1285)

2. **Resolver JSONL formaat**: `read_jsonl_lines()` verwacht newline-delimited JSON, maar de store schrijft pretty-printed JSON (enkel-regelig via canonical_json maar met newlines door json.dumps indent). De resolver faalt op pretty-printed output.

## Productie-Outcome Store

Geen productie Outcome Store aangemaakt tijdens RC2-ontwikkeling. Geen merge naar main zonder review.

## 2026-07-25 Corrections

In de worktree `work/phase1b-final-corrections-20260725` (HEAD: b31cb842):
- Phase 1A backflowtest vervangen: `TestNoBackflow.test_no_a0_import` → echte AST importaudit
- Phase 1B backflowtest vervangen: `TestNoBackflow.test_no_a0_import` → echte AST importaudit
- Frozen Phase 1A unchanged: confirmed (diff vs 901a68e exitcode 0)
- Alle 298 tests pass (48+138+68+15+29)
- Smoke test: BTCEUR write-missing → 3571 bytes, SHA 9051c78a..., idempotent rerun confirmed
- Smoke test: ETHEUR dry-run → processed 1
