# Outcome Builder Phase 1B Plan v6 — Outcome Store + Batch Contract

**Datum:** 2026-07-12
**Versie:** v6 — provenance-only record_id drift policy
**Status:** PLAN ONLY — geen implementatie, geen code
**Review:** Vereist Fable review vóór implementatie
**Aanleiding:** Fable ORANGE op v5:
- same completeness + same windows_data + different record_id was ongedefinieerd
- oorzaak: provenance/cache timing fields kunnen record_id wijzigen zonder dat outcome-data wijzigt

---

## 1. Wat is Phase 1B?

| Wat | Hoe |
|-----|-----|
| Outcome Store | Bewaart outcomes persistent, JSONL per pair/maand |
| Batch processing | dry-run verplicht, write-missing, update-partial |
| Idempotentie | Multi-field outcome_id, record_id semantic dedup |
| Partial→complete lifecycle | Append-only, completeness rank, resolver derived |
| Record revision chain | record_revision + supersedes_record_id + previous_record_hash |
| JSONL atomicity | True append-only, hard error op corruption |
| Archive fallback requirement | Phase 1C, niet in Phase 1B |
| No-backflow | outcome_store gitignored, path-isolated |

**Phase 1B is NIET:**
- Strategy Harness
- A1
- Testbot
- Trader
- signal generator
- scoring engine
- trade evaluator

---

## 2. Architectuurpositie

```
L4 snapshot store (SQLite, mode=ro)
        │
        ▼
Outcome Builder Phase 1A calculator (reused)
        │
        ▼
  ┌─ OUTCOME STORE ─────────────────────────┐
  │  JSONL per pair/maand (asof_ts month)  │
  │  True append-only — no record mutation │
  │  Resolver derives current/superseded   │
  │  record_id semantic, record_hash chain │
  └────────────────────────────────────────┘
        │
        ▼ (later, NIET Phase 1B)
Strategy Harness — leest Outcome Store
```

**No-backflow (hard):**
Outcome Store nooit gelezen door Hermes-v03, L4, A0, ASOF lagen.
`.gitignore`: `outcome_store/` — generated data, niet in git.

---

## 3. Canonical JSON Contract

`canonical_json(obj)` wordt gebruikt voor: outcome_id, windows_hash, record_id, record_hash.

**Definitie:**

1. Object keys alfabetisch gesorteerd.
2. `separators=(",", ":")` — compact, geen whitespace.
3. `ensure_ascii=False` — UTF-8 behouden.
4. UTF-8 bytes vóór SHA-256 hashing.
5. `allow_nan=False` — NaN/Infinity hard fail.
6. Dict key order mag nooit betekenis hebben.
7. List order blijft betekenisvol.
8. Timestamps: epoch int of ISO string, niet gemengd in hetzelfde object.
9. Identity fields mogen geen floats bevatten.
10. Hashes: lowercase hex strings.

**Python implementatie (later):**
```python
json.dumps(
    normalized_obj,
    sort_keys=True,
    separators=(",", ":"),
    ensure_ascii=False,
    allow_nan=False
).encode("utf-8")
```

**Numeric normalization (voor record/content hashes):**
- ints blijven ints
- floats → canonical decimal string via `Decimal(str(value))`
- geen exponentnotatie
- trailing zeros verwijderen
- "-0" → "0"
- NaN/Infinity → hard fail

---

## 4. Outcome Identity — Multi-Field

**snapshot_id is lookup key, NIET de primary outcome identity.**

```
outcome_identity_fields:
  - pair
  - snapshot_id
  - asof_ts
  - outcome_contract_version
  - store_schema_version
  - windows_hash
  - source_policy

outcome_id = SHA-256(canonical_json(outcome_identity_fields))
```

**windows_hash:**
```
windows_hash = SHA-256(canonical_json({name: seconds, ...}))
```
Niet alleen gesorteerde namen — de seconds mapping zit erin.

| Wijziging | Effect |
|-----------|--------|
| Andere windows / seconds | ✗ Nieuw outcome_id |
| Andere contract_version | ✗ Nieuw outcome_id |
| Andere store_schema_version | ✗ Nieuw outcome_id |
| Andere source_policy | ✗ Nieuw outcome_id |
| Zelfde snapshot, partial→complete | = Zelfde outcome_id |

---

## 5. Hash Definities — record_id vs record_hash

### record_id — Semantic Deduplication Hash

```
content_fields = stored record MINUS exact record_id_excluded_fields

record_id = SHA-256(canonical_json(content_fields))
```

### record_id_excluded_fields — Gesloten Lijst (Closed List)

**Top-level uitgesloten (nooit in record_id):**
- `record_id`
- `record_hash`
- `created_at`
- `generated_at`
- `record_revision`
- `supersedes_record_id`
- `previous_record_hash`
- `run_metadata`

**Cache-status velden uitgesloten (nooit in record_id):**
- `cache_status.cache_staleness_seconds`
- `cache_status.staleness_seconds`
- `cache_status.checked_at`
- `cache_status.checked_at_ts`
- `cache_status.fetched_at`
- `cache_status.fetched_at_ts`
- `cache_status.generated_at`
- `cache_status.generated_at_ts`

**Regel:** Alles wat NIET expliciet in deze lijst staat, telt mee voor record_id.

**Deze cache_status velden tellen WEL mee:**
- `cache_status.source`
- `cache_status.semantic_check`
- `cache_status.staleness_status`
- `cache_status.has_gaps`
- `cache_status.gap_count` (indien aanwezig)
- `cache_status.source_policy` (indien aanwezig)

**Beleid:**
- created_at en runtime timing breken duplicate-detectie niet
- echte source/status verschillen blijven semantisch zichtbaar
- implementatie mag niet zelf kiezen wat volatile is
- de excluded field list is closed — nieuwe excluded fields vereisen contractwijziging of store_schema_version bump

**record_id is stabiel bij:** identieke rerun, andere created_at, andere revision, andere chain fields, andere cache_staleness_seconds (als outcome zelfde is).

**record_id verandert bij:** andere windows_data, andere completeness, andere reference, andere source_snapshot, andere outcome_id, andere source_policy, andere contract/schema version.

### record_hash — Integrity/Chain Hash

```
record_hash = SHA-256(canonical_json(full_stored_record MINUS record_hash))
```

Bevat: record_id, created_at, record_revision, supersedes_record_id, previous_record_hash — alle audit/provenance velden.

### previous_record_hash

`previous_record_hash` = record_hash van vorige current record in de chain.

**Regels:**
- record_hash mag nooit zichzelf bevatten
- record_id mag nooit zichzelf bevatten
- Geen circulaire hashdefinities

---

## 6. Record Revision Chain

### Stored Record Fields (Immutable)

| Veld | Beschrijving |
|------|-------------|
| `outcome_id` | SHA-256 van 7 identity fields |
| `record_id` | SHA-256 van content_fields (semantic dedup) |
| `record_revision` | 1, 2, 3... per outcome_id |
| `supersedes_record_id` | record_id van vorige record |
| `created_at` | ISO UTC timestamp |
| `record_hash` | SHA-256 van full record (chain integrity) |
| `previous_record_hash` | record_hash van vorige record |
| `outcome_contract_version` | 1 |
| `store_schema_version` | 1 |
| `source_policy` | "cache_for_recent_only" |
| `source_snapshot` | snapshot_id, pair, asof_ts |
| `windows_hash` | SHA-256 van windows + seconds |
| `completeness` | Per venster: missing/partial/complete |
| `windows_data` | Per venster metrics |
| `cache_status` | Source + staleness |
| `field_limitations` | Template zinnen |
| `scope_notes` | Template zinnen |

**Niet stored — derived door resolver:** current/superseded status.

---

## 7. Completeness Rank

| Status | Rank |
|--------|------|
| missing | 0 |
| partial | 1 |
| complete | 2 |

**Candidate is "more complete" dan current als:**
1. Voor elk window: candidate_rank >= current_rank
2. Voor minstens één window: candidate_rank > current_rank

**Write-regels:**
- candidate more complete → APPEND new revision
- candidate exact same record_id → SKIP
- candidate minder compleet → SKIP (skipped_less_complete)
- candidate zelfde completeness_vector, andere windows_data → CONFLICT exit 3
- candidate hogere rank maar gelijke-rank windows andere values → CONFLICT exit 3
- complete (alle windows rank 2) + zelfde record_id → SKIP
- complete + ander record_id → CONFLICT exit 3

---

## 8. Incomparable Completeness

**Definitie:** candidate is incomparable met current als:
- minstens één window candidate_rank > current_rank
EN
- minstens één window candidate_rank < current_rank

**Voorbeeld:**
```
current:   {5m:2, 15m:2, 60m:1, 240m:1}
candidate: {5m:2, 15m:2, 60m:2, 240m:0}
```
→ 60m beter, 240m slechter → incomparable

**Regel:**
- incomparable candidate = SKIP
- geen write
- geen revision
- batch counter: `skipped_incomparable += 1`

**Extra conflictregel (equal-rank value drift):**
Als candidate en current voor een gelijke-rank window verschillende windows_data hebben:
- CONFLICT exit 3
- geen write

**Dus:**
- incomparable zonder equal-rank value drift → skip_incomparable
- incomparable met equal-rank value drift → conflict exit 3

---

## 9. Write Flow

```
1. Als chain corrupt:
   store corruption error exit 2, geen write

2. Als candidate record_id == current record_id:
   skip duplicate

3. Als current complete:
   - candidate same record_id: skip
   - candidate different record_id: conflict exit 3

4. Vergelijk completeness_vector:
   - more complete: append new revision
   - less complete: skip_less_complete
   - same completeness:
       * same record_id: skip duplicate
       * different record_id, same windows_data: provenance-only drift → skip (skipped_provenance_only += 1)
       * different windows_data: conflict exit 3
   - incomparable:
       * if equal-rank windows_data differs: conflict exit 3
       * else skip_incomparable

5. Geen enkele stap herschrijft oude JSONL regels.
```

---

## 10. Partial → Complete Lifecycle

```
JSONL (alleen appends):

{"outcome_id":"abc","record_id":"r1","record_revision":1,"supersedes_record_id":null,...}
// completeness: {5m:2, 15m:2, 60m:1, 240m:1}

{"outcome_id":"abc","record_id":"r2","record_revision":2,"supersedes_record_id":"r1","previous_record_hash":"h1",...}
// completeness: {5m:2, 15m:2, 60m:2, 240m:1}

{"outcome_id":"abc","record_id":"r3","record_revision":3,"supersedes_record_id":"r2","previous_record_hash":"h2",...}
// completeness: {5m:2, 15m:2, 60m:2, 240m:2}
```

Resolver: current=r3, revision=3, superseded=[r1,r2].

---

## 11. JSONL Atomicity / File Rotation

**True append-only** — bestaande regels nooit herschreven.
File lock (flock), flush/fsync, malformed = hard error.

**Phase 1B:** fsync is altijd aan na append — niet configureerbaar in Phase 1B. Configureerbaarheid is een latere optimalisatie (niet Phase 1B).

**File month = asof_ts month (UTC):**
```
outcome_store/{PAIR}/{PAIR}_YYYY-MM_outcomes.jsonl
```
Alle revisions van hetzelfde outcome_id blijven in het asof_ts month file — ook als revision later in een andere maand geschreven wordt.

---

## 12. Source Policy / Archive Fallback

**Phase 1B:** `source_policy = "cache_for_recent_only"`

- Recente outcomes uit live_cache toegestaan
- Partial/missing eerlijk opslaan
- Zonder archive: NOOIT historische complete outcomes claimen
- Historical bulk complete → Phase 1C

**Archive fallback requirements (Phase 1C):**
- 1m candles, candle_open semantics, gap detection
- Zelfde inclusion rule: timestamp >= asof, timestamp < window_end
- Eigen source_status/cache_status equivalent
- source_policy opgenomen in outcome_id

**Historical complete block — emergent, niet separaat:** Het blokkeren van historical complete outcomes is emergent:
- completeness wordt uitsluitend afgeleid uit werkelijk beschikbare 1m candles
- completeness wordt nooit aangenomen op basis van datum, verwachting of windowlengte
- zonder archive source kan een historical complete claim alleen ontstaan als alle vereiste 1m candles werkelijk beschikbaar zijn
- er is geen aparte datumdrempel
- geen fake completeness

---

## 13. Version Policy

| Constant | Value |
|----------|-------|
| STORE_SCHEMA_VERSION | 1 |
| ALLOWED_STORE_SCHEMA_VERSIONS | {1} |
| ALLOWED_OUTCOME_CONTRACT_VERSIONS | {1} |

- Unknown version → hard fail exit 3
- Missing version field → hard fail exit 3
- Writer schrijft alleen current version
- Geen stille migratie, geen best-effort parse

**Exit codes:**
- 0 = success
- 2 = read/store corruption error
- 3 = schema/contract/conflict error
- 5 = guardrail error

---

## 14. Batch Contract

**Modes:** dry-run (verplicht vóór write), write-missing, update-partial.

**Input:** pair, since, until, count, windows, include_partial.

**Summary velden:**
processed, skipped_existing, skipped_less_complete, skipped_incomparable, skipped_provenance_only, written, updated_partial_to_complete, updated_partial_to_more_complete, failed, conflicts, guardrail_failed, read_errors, schema_errors, store_corruption_errors, partial, complete, missing, window_stats (per window: complete/partial/missing).

**write-missing:**
- schrijft uitsluitend nieuwe outcome_ids
- schrijft nooit nieuwe revisions voor bestaande outcome_ids
- partial upgrades worden overgeslagen

**update-partial:**
- mag bestaande partial outcome_ids upgraden naar more-complete revisions
- mag geen complete conflicts overschrijven
- mag geen less-complete of incomparable candidates schrijven

**dry-run:**
- schrijft nooit bytes
- moet dezelfde summary produceren alsof write zou gebeuren

---

## 15. Guardrails — Vóór Append

Voor elke JSONL append: full candidate stored record gescand met Phase 1A guardrail. JSON keys/values gescand; exact scope_notes/field_limitations whitelists toegestaan. Guardrail failure → exit 5, geen bytes geschreven.

Verboden: buy, sell, long, short, entry, exit, TP, SL, take profit, stop loss, win, loss, profit, PnL, trade_confidence, setup, signal, target, stop, koop, verkoop.

---

## 16. No-Backflow + .gitignore

`.gitignore`: `outcome_store/` — generated data.

A0, L4, Hermes-v03 lezen/schrijven nooit outcome_store. Alleen Outcome Builder store code schrijft ernaar.

---

## 17. Schema

```json
{
  "outcome_id": "sha256...",
  "record_id": "sha256...",
  "record_revision": 1,
  "supersedes_record_id": null,
  "created_at": "...",
  "record_hash": "sha256...",
  "previous_record_hash": null,
  "outcome_contract_version": 1,
  "store_schema_version": 1,
  "source_policy": "cache_for_recent_only",
  "pair": "ETHEUR",
  "snapshot_id": "...",
  "asof_ts": 1783790700,
  "windows_hash": "sha256...",
  "windows": {"5m":300,"15m":900,"60m":3600,"240m":14400},
  "reference": {"price":1595.13,"source":"snapshot.price.current.close","timeframe":"1m"},
  "completeness": {"5m":"complete","15m":"complete","60m":"partial","240m":"missing"},
  "windows_data": {...},
  "cache_status": {...},
  "field_limitations": [...],
  "scope_notes": [...]
}
```

---

## 18. Tests — 48

| # | Test |
|---|------|
| 1 | test_canonical_json_sorts_keys |
| 2 | test_canonical_json_uses_compact_separators |
| 3 | test_canonical_json_rejects_nan_inf |
| 4 | test_canonical_json_normalizes_float_for_hashing |
| 5 | test_windows_hash_includes_window_seconds |
| 6 | test_outcome_id_stable_same_identity |
| 7 | test_outcome_id_changes_when_windows_hash_changes |
| 8 | test_outcome_id_changes_when_outcome_contract_version_changes |
| 9 | test_outcome_id_changes_when_store_schema_version_changes |
| 10 | test_outcome_id_changes_when_source_policy_changes |
| 11 | test_snapshot_id_is_lookup_not_primary_identity |
| 12 | test_record_id_excludes_created_at |
| 13 | test_record_id_excludes_revision_and_chain_fields |
| 14 | test_duplicate_rerun_same_content_different_created_at_skips |
| 15 | test_record_hash_includes_chain_fields |
| 16 | test_record_hash_mismatch_is_corruption |
| 17 | test_first_partial_write_revision_1 |
| 18 | test_partial_more_complete_appends_revision |
| 19 | test_partial_to_complete_appends_revision |
| 20 | test_less_complete_rerun_skips |
| 21 | test_same_completeness_different_values_conflict |
| 22 | test_complete_unchanged_rerun_skips |
| 23 | test_complete_changed_rerun_conflict |
| 24 | test_current_status_derived_by_resolver |
| 25 | test_superseded_status_derived_by_chain |
| 26 | test_old_record_not_mutated_on_upgrade |
| 27 | test_append_only_never_rewrites_old_record |
| 28 | test_previous_record_hash_linked |
| 29 | test_duplicate_revision_conflict |
| 30 | test_chain_break_detected |
| 31 | test_malformed_jsonl_line_hard_error |
| 32 | test_malformed_last_line_hard_error |
| 33 | test_cross_month_revision_uses_asof_month_file |
| 34 | test_batch_summary_counts_all_categories |
| 35 | test_dry_run_writes_nothing |
| 36 | test_guardrail_before_storage |
| 37 | test_guardrail_failure_not_written |
| 38 | test_no_a0_import |
| 39 | test_no_l4_write |
| 40 | test_no_backflow_path |
| 41 | test_outcome_store_gitignored |
| 42 | test_invalid_store_schema_version_fails |
| 43 | test_invalid_outcome_contract_version_fails |
| 44 | test_live_cache_insufficient_marks_partial |
| 45 | test_historical_complete_blocked_without_archive |
| 46 | test_incomparable_completeness_skips |
| 47 | test_corrupt_chain_blocks_new_write_exit_2 |
| 48 | test_provenance_only_difference_skips_not_conflicts |

---

## 19. Open Questions

**Beslissingen dicht:**
- JSONL per pair/maand, file month = asof_ts month ✅
- Multi-field outcome_id ✅
- canonical_json contract vast ✅
- record_id/record_hash split ✅
- record_id excluded fields closed list ✅
- Completeness rank defined ✅
- Incomparable completeness policy ✅
- Provenance-only record_id drift policy ✅
- Complete immutable ✅
- No historical complete zonder archive ✅
- Dry-run verplicht vóór batch write ✅
- Guardrail vóór append ✅
- outcome_store gitignored ✅
- fsync altijd aan na append in Phase 1B ✅
- write-missing/update-partial semantics gescheiden ✅

**Open (implementatiedetails):**
- Exacte Python file-lock implementatie (flock, .lock file)
- Wanneer archive fallback Phase 1C
- Later recovery/repair tool voor corrupte JSONL
- Later SQLite/Parquet migratie
- Batch default count/size

---

## RAPPORTAGE

| # | Check | Status |
|---|-------|--------|
| 1 | Document patched | ✅ v5 → v6 |
| 2 | Path | `raw/sessions/2026-07-12-outcome-builder-phase-1b-plan.md` |
| 3 | Old version | v5 |
| 4 | New version | v6 |
| 5 | Old line count | 575 |
| 6 | New line count | 572 |
| 7 | fetched_at moved to record_id excluded list | ✅ |
| 8 | fetched_at_ts moved to record_id excluded list | ✅ |
| 9 | provenance-only branch added | ✅ |
| 10 | same completeness + same windows_data + different record_id policy = skip | ✅ |
| 11 | skipped_provenance_only counter added | ✅ |
| 12 | test 48 added | ✅ |
| 13 | testplan old count | 47 |
| 14 | testplan new count | 48 |
| 15 | no code changes | ✅ |
| 16 | no tests changed | ✅ |
| 17 | no DB/store files created | ✅ |
| 18 | no service/timer changes | ✅ |
| 19 | no commit | ✅ |
| 20 | git status --short | M second-brain/raw/sessions/2026-07-12-outcome-builder-phase-1b-plan.md |
