# Outcome Builder Phase 1B Plan v2 — Outcome Store + Batch Contract

**Datum:** 2026-07-12
**Versie:** v2 — identity + record lifecycle hardening (patch 1-9)
**Status:** PLAN ONLY — geen implementatie, geen code
**Review:** Vereist Fable review vóór implementatie
**Aanleiding:** Phase 1A frozen (901a68e1), Noa review op v1 plan

---

## 1. Wat is Phase 1B?

Phase 1B bouwt verder op Phase 1A (read-only calculator) en voegt toe:

| Wat | Hoe |
|-----|-----|
| Outcome Store | Bewaart outcomes persistent |
| Batch processing | Draait outcomes over meerdere snapshots |
| Idempotentie | Multi-field outcome identity, niet alleen snapshot_id |
| Partial→complete lifecycle | Eerst partial, later compleet — append-only supersede |
| Record revision tracking | record_revision, active flag, record_hash chain |
| JSONL atomicity | Append-only, corruption detection |
| Archive fallback requirement | Gedocumenteerd als harde vereiste, nog niet gebouwd |

**Phase 1B blijft:**
- Descriptieve hindsight
- Geen interpretatie
- Geen strategie
- Geen trade-advies
- Geen scoring/labels

---

## 2. Architectuurpositie

```
L4 snapshot store (SQLite, mode=ro)
        │
        ▼
Outcome Builder Phase 1A calculator (reused)
        │
        ▼
  ┌─ OUTCOME STORE ─────────────────────┐
  │  JSONL per pair/maand              │
  │  Multi-field outcome identity      │
  │  Append-only + supersede lifecycle │
  │  record_hash chain voor audit      │
  └────────────────────────────────────┘
        │
        ▼ (later, NIET Phase 1B)
Strategy Harness — leest Outcome Store
```

**No-backflow (hard):**
Outcome Store wordt nooit gelezen door:
- Hermes-v03 chart reader
- L4 snapshot builder
- A0 readout
- ASOF lagen

Outcome Store wordt later WEL gelezen door:
- Strategy Harness
- A1+ (indien expliciet OUTCOME-mode)
- Audits in OUTCOME-mode

---

## 3. Outcome Store Format — JSONL (Besloten)

**Beslissing:** JSONL per pair/maand. Geen open vraag meer.

**Motivatie:**
- Append-only past bij audit trail + supersede lifecycle
- Shell-inspectable (`cat`, `tail`, `grep`, `jq`)
- Geen SQLite lock/WAL/SHM risico in eerste storefase
- Eenvoudig te migreren naar SQLite/Parquet later als queryability nodig wordt
- Diffbaar buiten git — handig voor handmatige audit

**Format:**
```jsonl
{"outcome_id":"abc123...","record_id":"def456...","active":true,"record_revision":1,...}
{"outcome_id":"abc123...","record_id":"ghi789...","active":false,"superseded":true,...}
```

Eén JSON object per regel. Newline-terminated. Geen top-level array.

**Pad (niet aanmaken — plan only):**
```
projects/hermes-v03-outcome/outcome_store/{PAIR}/{PAIR}_YYYY-MM_outcomes.jsonl
```

**Geen git tracking van outcome_store/** — gegenereerde data, `.gitignore` entry nodig.

---

## 4. Outcome Identity — Multi-Field (PATCH 1)

**snapshot_id is lookup key, NIET de primary outcome identity.**

Eén snapshot kan meerdere geldige outcome records hebben:
- andere windows
- andere contractversie
- andere store schema version
- andere source_policy (cache vs archive)
- partial state versus later complete upgrade

### Identity Fields

```
outcome_identity_fields:
  - pair
  - snapshot_id
  - asof_ts
  - outcome_contract_version
  - store_schema_version
  - windows_hash
  - source_policy
```

### Outcome ID

```
outcome_id = SHA-256(canonical_json(outcome_identity_fields))
```

Waarbij:
- `pair` / `snapshot_id` / `asof_ts` = uit source_snapshot
- `outcome_contract_version` = 1 (wijzigt bij contractbreuk)
- `store_schema_version` = 1 (wijzigt bij schema upgrade)
- `windows_hash` = SHA-256 van gesorteerde window namen (bijv. "5m,15m,60m,240m")
- `source_policy` = "cache_for_recent_only" (of later "archive_fallback")

### Regels

| Wijziging | Effect op outcome_id |
|-----------|---------------------|
| Andere windows | ✗ Nieuw outcome_id |
| Andere contract_version | ✗ Nieuw outcome_id |
| Andere store_schema_version | ✗ Nieuw outcome_id |
| Andere source_policy | ✗ Nieuw outcome_id |
| Zelfde snapshot, partial→complete | = Zelfde outcome_id (record revision update) |

---

## 5. Record Revision / Active State (PATCH 2)

Omdat JSONL append-only is, moet elk record zijn eigen plaats in de ketting kennen.

### Record Fields

| Veld | Type | Beschrijving |
|------|------|-------------|
| `outcome_id` | string | SHA-256 van identity fields |
| `record_id` | string | SHA-256 van full record (minus record_hash) |
| `record_revision` | int | Oplopend: 1, 2, 3... per outcome_id |
| `active` | boolean | Exact één record per outcome_id is active=true |
| `superseded` | boolean | Oude record na upgrade |
| `supersedes_record_id` | string\|null | record_id van vorige actieve record |
| `created_at` | string | ISO UTC timestamp |
| `record_hash` | string | SHA-256 van full record (minus record_hash) |
| `previous_record_hash` | string\|null | record_hash van vorige record in de ketting |

### Active Resolver

Voor één `outcome_id` is exact één record `active=true` geldig.

```
Scan alle records met zelfde outcome_id:
  → Vind record met active=true en hoogste record_revision
  → Dat is het geldige record
```

### Record ID vs Record Hash

```
record_id    = SHA-256(canonical_json(full_record - record_hash - record_id))
record_hash  = SHA-256(canonical_json(full_record - record_hash))

record_id    → identificeert de inhoud van dit record
record_hash  → verifieert dat de inhoud niet corrupt is
```

`record_id` is de echte inhoudelijke vingerafdruk. `record_hash` is alleen voor ketting-integriteit (want `record_hash` hangt af van `previous_record_hash`).

---

## 6. Idempotency + Duplicate Prevention (PATCH 1+2)

### Write Flow

```
1. Bouw outcome
2. Bereken outcome_id uit identity fields
3. Bereken record_id uit full content
4. Check store voor bestaande records met dezelfde outcome_id
5. Als geen bestaand record → WRITE als active=true, revision=1
6. Als wel bestaand:
   a. Vind huidige active record → vergelijk record_id
   b. Als record_id matcht → SKIP (exact duplicate)
   c. Als partial → meer complete state upgrade → WRITE met:
      - active=true
      - superseded=false
      - supersedes_record_id = oude record_id
      - previous_record_hash = oude record_hash
      - record_revision = oud.revision + 1
      - oud record updaten: active=false, superseded=true
   d. Als complete EN record_id verschilt → CONFLICT → exit 3
```

---

## 7. Complete Immutability (PATCH 3)

**Harde regel: complete outcome records zijn immutable.**

Als een outcome eenmaal `complete` is voor alle vensters:
- Rerun met zelfde identity fields moet exact dezelfde record_id opleveren
- Als record_id matcht → SKIP (idempotent)
- Als record_id verschilt → CONFLICT ERROR (exit 3)
- **Nooit automatisch overschrijven**
- Conflict wordt gerapporteerd in batch summary

Partial records mogen evolueren naar completer via append-only supersede:
- partial → meer compleet (meer candles, nog steeds partial voor sommige vensters)
- partial → complete (alle vensters nu complete)

Maar complete → complete met ander resultaat = CONFLICT.

---

## 8. Partial → Complete Lifecycle (PATCH 2 refinement)

### Scenario

Voor een recente snapshot (asof = nu - 5 minuten):
- 5m venster: complete
- 15m venster: complete
- 60m venster: partial (27/60)
- 240m venster: partial (27/240)

Later (60 minuten na asof): 60m nu complete, 240m nog partial.

### Record Chain

```
Run 1: outcome_id="abc", record_id="r1", revision=1, active=true,  superseded=false
  completeness: {5m:complete, 15m:complete, 60m:partial, 240m:partial}

Run 2: zelfde outcome_id, meer candles beschikbaar
  → Oud record (r1): active=false, superseded=true
  → Nieuw record (r2): revision=2, active=true, superseded=false,
    supersedes_record_id="r1", previous_record_hash="hash_r1"
  completeness: {5m:complete, 15m:complete, 60m:complete, 240m:partial}

Run 3: nu 240m ook complete
  → r2: active=false, superseded=true
  → r3: revision=3, active=true, supersedes_record_id="r2"
  completeness: {5m:complete, 15m:complete, 60m:complete, 240m:complete}

Run 4: complete rerun — zelfde record_id als r3 → SKIP
```

---

## 9. JSONL Atomicity / Corruption (PATCH 4)

### Schrijfregels (later implementeren)

- Append-only — nooit regels overschrijven of middenin schrijven
- Eén JSON object per regel, newline-terminated
- Schrijf via temp/staging: schrijf nieuwe regel naar `.tmp`, rename naar `.jsonl`, of gebruik file-lock
- `flush`/`fsync` na append voor crash safety
- Detecteer malformed JSONL lines bij lezen
- Malformed line = store corruption error — niet stil negeren
- `record_hash` verplicht — verifieert content integriteit
- Active resolver moet corruption/conflict detecteren

### Crash Scenario's

| Scenario | Gevolg | Herstel |
|----------|--------|---------|
| Crash tijdens append | Half-geschreven laatste regel | Laatste regel negeren (malformed) |
| Crash na append, vóór supersede mark | Nieuwe regel actief, oude nog active=true | Active resolver: hoogste revision wint |
| Crash vóór append | Geen wijziging | Geen herstel nodig |
| Disk full tijdens write | Partial write | Laatste regel malformed → negeren |

---

## 10. Source Policy (PATCH 6 — phasing verduidelijkt)

### Phase 1B Source Regels

| Bron | Gebruik | Status |
|------|---------|--------|
| live_cache 1m candles | Primaire bron | ✅ Phase 1A bewezen |
| archive (historischedata/) | Fallback voor historisch | ⬜ Vereist, nog niet gebouwd |

### Phase 1B Mag (zonder archive)

- Latest snapshot outcomes (zolang live_cache diep genoeg is)
- Complete windows tot ~15m (live_cache dekt dit)
- Partial outcomes voor grotere vensters (eerlijk gelabeld)
- `source_policy = "cache_for_recent_only"` in outcome_id

### Phase 1B Mag NIET (zonder archive)

- Claimen dat historische 60m/240m outcomes "complete" zijn
- `source_policy = "archive_fallback"` gebruiken zonder archive implementatie
- Nep-complete resultaten door reconstructie of extrapolatie

### Archive Fallback — Vereiste voor Later

Archive fallback is verplicht vóór:
- Bulk historical outcomes
- Outcomes met source_policy="archive_fallback"
- Strategy Harness die historische outcomes nodig heeft

Archive source requirements:
- 1m candles met candle_open semantics (bewezen)
- Gap detection
- Dezelfde inclusion rule: timestamp >= asof_ts, timestamp < window_end_ts
- `source_policy` opgenomen in outcome_id

---

## 11. Batch Contract (PATCH 7 — expanded)

### Input (toekomstige CLI)

| Parameter | Beschrijving |
|-----------|-------------|
| --pair | Pair (ETHEUR, BTCEUR) |
| --since | Start asof_ts of ISO datetime |
| --until | Eind asof_ts of ISO datetime |
| --count | Max aantal snapshots |
| --mode | write-missing, update-partial, dry-run |
| --windows | 5m,15m,60m,240m |
| --include-partial | Ook partial windows schrijven |

### Output Statistieken (uitgebreid)

| Veld | Beschrijving |
|------|-------------|
| `processed` | Totaal bekeken snapshots |
| `skipped_existing` | Bestaand, overgeslagen (exact duplicate) |
| `written` | Nieuw geschreven |
| `updated_partial_to_complete` | Partial → complete upgrades |
| `updated_partial_to_more_complete` | Partial → meer compleet (nog niet volledig) |
| `failed` | Errors (missing snapshot, corrupt data) |
| `conflicts` | Complete met afwijkend resultaat (exit 3 per stuk) |
| `guardrail_failed` | Guardrail violations (exit 5, niet geschreven) |
| `read_errors` | Snapshot of cache niet leesbaar |
| `schema_errors` | Onbekende schema/contract versie |
| `store_corruption_errors` | Malformed JSONL in store |
| `partial` | Aantal outcomes met minstens één partial venster |
| `complete` | Aantal outcomes met alle vensters complete |
| `missing` | Aantal outcomes met minstens één missing venster |
| `window_stats` | Per venster: complete/partial/missing counts |

---

## 12. No-Backflow Enforcement

### Technische Bescherming

| Regel | Hoe afdwingen |
|-------|---------------|
| Outcome Store apart pad | `projects/hermes-v03-outcome/outcome_store/` — gescheiden van L4/A0/Hermes |
| A0 importeert nooit outcome | Test: `grep -r "outcome_store" projects/hermes-v03-analyst/` moet leeg zijn |
| L4 importeert nooit outcome | Test: `grep -r "outcome_store" projects/hermes-v03-interpreter/` moet leeg zijn |
| Hermes-v03 importeert nooit outcome | Test: `grep -r "outcome_store" projects/hermes-v03/` moet leeg zijn |
| ASOF lagen lezen geen outcome | Test in CI/review gate |
| Outcome Builder schrijft alleen naar eigen store | Geen writes naar L4 of A0 paden |

---

## 13. Guardrails Blijven Gelden

Opgeslagen outcome records moeten voldoen aan dezelfde guardrails als Phase 1A stdout:

- JSON keys en values gescand op verboden termen
- Scope notes en field_limitations alleen via exacte whitelist
- Guardrail failure = exit 5 — outcome wordt NIET opgeslagen
- Scan gebeurt vóór write, niet erna

---

## 14. Schema / Versioning (PATCH 1 updated)

### Outcome Store Schema

```json
{
  "outcome_id": "sha256...",
  "record_id": "sha256...",
  "record_revision": 1,
  "active": true,
  "superseded": false,
  "supersedes_record_id": null,
  "created_at": "2026-07-12T10:00:00+00:00",
  "record_hash": "sha256...",
  "previous_record_hash": null,
  "outcome_contract_version": 1,
  "store_schema_version": 1,
  "source_policy": "cache_for_recent_only",
  "pair": "ETHEUR",
  "snapshot_id": "ETHEUR-1783790700-...",
  "asof_ts": 1783790700,
  "generated_at": "2026-07-12T10:00:00+00:00",
  "windows_hash": "sha256...",
  "windows": ["5m", "15m", "60m", "240m"],
  "reference": {"price": 1595.13, "source": "snapshot.price.current.close", "timeframe": "1m"},
  "boundary_status": {"asof_on_1m_boundary": true, "asof_mod_60": 0, "timestamp_semantics": "candle_open"},
  "completeness": {"5m": "complete", "15m": "complete", "60m": "partial", "240m": "missing"},
  "windows_data": {...},
  "cache_status": {"source": "live_cache", "fetched_at_ts": 1783791000, "staleness_seconds": 300, "has_gaps": false},
  "field_limitations": [...],
  "scope_notes": [...]
}
```

### Version Policy

| Versie | Betekenis |
|--------|-----------|
| outcome_contract_version 1 | Huidige contract — Phase 1A metrics |
| store_schema_version 1 | Huidig JSONL schema met record revision chain |

---

## 15. Data Integrity Checks

| Check | Type | Actie bij falen |
|-------|------|-----------------|
| snapshot_id match | Pre-write | Exit 2 |
| pair match | Pre-write | Exit 2 |
| asof_ts consistent | Pre-write | Exit 2 |
| reference price aanwezig | Pre-write | Exit 2 |
| outcome_id duplicate — same record_id | Pre-write | Skip (idempotent) |
| partial → upgrade (record_id verschilt) | Pre-write | Write + supersede oud |
| complete — same record_id | Pre-write | Skip |
| complete — andere record_id | Pre-write | Exit 3 (conflict) |
| guardrail scan | Pre-write | Exit 5 |
| windows_hash mismatch | Pre-write | Exit 3 |
| cache staleness > drempel | Warning | Status warning, geen failure |
| negative staleness (clock skew) | Pre-write | Exit 3 |
| JSON parse error in store file | Bij read | Exit 2 |
| malformed JSONL line | Bij read | Exit 2 (corruption) |
| record_hash mismatch | Bij read | Exit 2 (corruption) |

---

## 16. Tests voor Phase 1B Implementatie (PATCH 8 — 28 tests)

| # | Test | Beschrijving |
|---|------|-------------|
| 1 | test_outcome_id_stable | Zelfde identity fields → zelfde outcome_id |
| 2 | test_outcome_id_changes_windows_hash | Andere windows → ander outcome_id |
| 3 | test_outcome_id_changes_contract_version | Andere contract_version → ander outcome_id |
| 4 | test_outcome_id_changes_store_schema | Andere store_schema_version → ander outcome_id |
| 5 | test_outcome_id_changes_source_policy | Andere source_policy → ander outcome_id |
| 6 | test_snapshot_id_not_primary_identity | snapshot_id-only is geen primary key |
| 7 | test_first_partial_write_active_revision_1 | Eerste write: active=true, revision=1 |
| 8 | test_duplicate_partial_skip | Zelfde record_id → skip |
| 9 | test_partial_with_more_candles_appends_revision | Meer candles → nieuwe revision |
| 10 | test_partial_to_complete_supersedes | Complete upgrade → oud partial superseded |
| 11 | test_complete_unchanged_rerun_skip | Complete + zelfde record_id → skip |
| 12 | test_complete_changed_rerun_conflict | Complete + ander record_id → exit 3 |
| 13 | test_exactly_one_active_per_outcome_id | Active resolver: 1 active per outcome_id |
| 14 | test_previous_record_hash_linked | Supersede koppelt record_hash chain |
| 15 | test_record_hash_validates_content | Corrupt record → record_hash mismatch |
| 16 | test_malformed_jsonl_line_detected | Geen geldige JSON → exit 2 |
| 17 | test_atomic_append_no_partial_corruption | Crash → geen corrupt record |
| 18 | test_batch_summary_written_skipped_updated_conflicts | Counts kloppen |
| 19 | test_guardrail_before_storage | Verboden termen → exit 5, geen write |
| 20 | test_guardrail_failure_not_written | Exit 5 schrijft niets |
| 21 | test_no_a0_import | Outcome Builder importeert nooit A0 |
| 22 | test_no_l4_write | Outcome Builder schrijft nooit L4 |
| 23 | test_no_backflow_path | Geen outcome_store imports in ASOF lagen |
| 24 | test_invalid_store_schema_fails | Onbekende versie → exit 3 |
| 25 | test_live_cache_insufficient_marks_partial | Te weinig candles → partial |
| 26 | test_historical_complete_blocked_without_archive | Geen archive → geen historisch complete |
| 27 | test_active_latest_resolver_works | Hoogste revision + active=true wint |
| 28 | test_store_corruption_blocks_or_errors | Corrupt bestand → harde error |

---

## 17. CLI Ontwerp (Later, Niet Nu Bouwen)

```bash
# Store write — enkele snapshot
python3 outcome_builder/store_cli.py \
  --pair ETHEUR --latest \
  --store-dir outcome_store \
  --mode write

# Batch — alle missing outcomes sinds datum
python3 outcome_builder/store_cli.py \
  --pair ETHEUR \
  --since 2026-07-12T00:00:00+00:00 \
  --mode write-missing \
  --store-dir outcome_store

# Batch — update partials
python3 outcome_builder/store_cli.py \
  --pair ETHEUR \
  --mode update-partial \
  --store-dir outcome_store

# Dry-run
python3 outcome_builder/store_cli.py \
  --pair ETHEUR --since 2026-07-12T00:00:00+00:00 \
  --mode dry-run --format json
```

---

## 18. Open Questions (PATCH 9 — gereduceerd van 8 naar 6)

| # | Vraag | Status |
|---|-------|--------|
| 1 | Exacte file lock techniek (flock, temp+rename, .lock file)? | ⬜ Beslissen tijdens implementatie |
| 2 | fsync verplicht of configurable? | ⬜ Aanbevolen: verplicht voor crash safety |
| 3 | Wanneer archive fallback bouwen? | ⬜ Phase 1C — vereist vóór historische outcomes |
| 4 | Max bestandsgrootte per JSONL? | ✅ Maandrotatie voldoende (~86MB/maand/pair) |
| 5 | Automatische batch of handmatig? | ✅ Handmatig voor Phase 1B |
| 6 | Retention/archive policy voor outcome_store? | ⬜ Later bepalen — voor nu oneindig bewaren |

**Beslissingen die dicht zijn (geen open vragen meer):**
- Storage format = JSONL per pair/maand ✅
- snapshot_id = lookup only, niet primary ✅
- outcome_id = SHA-256 van alle identity fields ✅
- partial→complete via append-only supersede ✅
- complete immutable ✅
- historical complete blocked zonder archive fallback ✅
- JSONL atomic/corruption regels ✅
- Testplan op 28 tests ✅

---

## 19. Aanbeveling

### Veiligste Minimale Phase 1B

1. **JSONL store** — `outcome_store/{PAIR}/{PAIR}_YYYY-MM_outcomes.jsonl`
2. **Multi-field outcome_id** — SHA-256 van pair+snapshot_id+asof_ts+contract+schema+windows+source_policy
3. **Record revision chain** — record_id, record_revision, active flag, record_hash, previous_record_hash
4. **Append-only supersede** — partial→complete via nieuwe regel, oude superseded
5. **Complete immutability** — complete rerun met afwijkend resultaat = conflict
6. **Guardrail scan vóór write** — exit 5 zonder bestandswijziging
7. **28 tests** — identity, revision, lifecycle, corruption, backflow, guardrails
8. **Geen archive fallback nog** — partial/missing zijn eerlijk, source_policy = cache_for_recent_only

### Wat Fable Moet Reviewen (Vóór Code)

- Multi-field outcome_id contract
- Record revision chain (active, superseded, record_hash)
- Complete immutability regel
- JSONL atomicity/corruption regels
- No-backflow tests (path-isolatie)
- 28-test plan

### Wat Pas Phase 1C Mag Zijn

- Archive fallback implementatie
- Bulk historische outcomes
- Automatische batch scheduling
- SQLite/Parquet migratie
- Strategy Harness integratie

---

## RAPPORTAGE

| # | Check | Status |
|---|-------|--------|
| 1 | Document patched | ✅ Ja — v1 → v2 |
| 2 | Path | `raw/sessions/2026-07-12-outcome-builder-phase-1b-plan.md` |
| 3 | Old line count | 532 |
| 4 | New line count | ~500 |
| 5 | snapshot_id-only primary removed | ✅ Ja — vervangen door multi-field outcome_id |
| 6 | outcome_id identity fields defined | ✅ Ja — 7 velden |
| 7 | windows_hash included | ✅ Ja |
| 8 | source_policy included | ✅ Ja |
| 9 | store_schema_version included | ✅ Ja |
| 10 | record_revision/supersede policy defined | ✅ Ja — record_id, revision, active, superseded, hash chain |
| 11 | complete immutability defined | ✅ Ja — harde regel, conflict bij afwijkend resultaat |
| 12 | JSONL atomic/corruption rules added | ✅ Ja — temp+rename, flush, malformed detectie |
| 13 | storage format decision closed | ✅ Ja — JSONL per pair/maand, geen open vraag |
| 14 | archive fallback phasing clarified | ✅ Ja — Phase 1C, verplicht vóór historical |
| 15 | batch summary contract expanded | ✅ Ja — 15 velden |
| 16 | testplan old count | 20 |
| 17 | testplan new count | 28 |
| 18 | open questions old count | 8 |
| 19 | open questions new count | 6 |
| 20 | no code changes | ✅ Ja |
| 21 | no tests changed | ✅ Ja |
| 22 | no DB/store files created | ✅ Ja |
| 23 | no service/timer changes | ✅ Ja |
| 24 | no commit | ✅ Ja |
| 25 | git status --short | ✅ Geen tracked diffs |
