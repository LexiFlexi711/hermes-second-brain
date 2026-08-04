# Outcome Builder Phase 0 Plan — Fable-Hardened v2

**Datum:** 2026-07-11
**Status:** Planning only — geen code, geen implementatie
**Review:** Fable Orange → 5 blockers verwerkt
**Aanleiding:** A0 Foundation Freeze op 4872eaa4 — Outcome Builder planning mag starten

---

## 1. Status

Planning only.
No code.
No implementation.
No directories.
No DB writes.

Dit document is het plan. Het bouwt niets.

---

## 2. Why This Layer Exists

Outcome Builder meet alleen wat na een snapshot gebeurde.

Het is **descriptieve hindsight**, niet strategisch.

| Outcome Builder doet WEL | Outcome Builder doet NIET |
|---------------------------|---------------------------|
| Prijsbeweging meten na asof | "Was dit een goede trade?" |
| High/low/close na venster | "Had je long moeten gaan?" |
| max_up / max_down berekenen | Entry/exit valideren |
| Compleetheid van toekomstdata checken | Setup score geven |
| Venster-gebaseerde metrics opslaan | Win/loss bepalen |

Outcome Builder is de brug tussen "wat zagen we" (A0) en "wat gebeurde er" (hindsight), zonder te interpreteren.

---

## 3. Inputs

### 3.1 L4 Snapshot Input

Uit L4 SQLite store (mode=ro):

| Veld | Bron | Gebruik |
|------|------|---------|
| `snapshot_id` | snapshots tabel | Outcome key |
| `pair` | snapshots tabel | Pair identificatie |
| `asof_ts` | snapshots tabel | Referentie-tijdstip |
| `stored_at` | snapshots tabel | Metadata |
| `snapshot_version` | snapshots tabel | Schema compatibiliteit |
| `timeframes_present` | snapshot_timeframes | Welke TFs beschikbaar |
| `price.current.close` | raw_blob → raw_json | Referentieprijs |

Geen A0-tekst. Geen A0-proza. Alleen ruwe snapshotvelden.

### 3.2 OHLC Future Source

#### Candle Timestamp Semantics — BEWEZEN

Read-only inspectie op 2026-07-11, live_cache ETHEUR + BTCEUR, alle 5 TFs:

| Pair | TF | Candles | Interval | Match? | Conclusie |
|------|-----|---------|----------|--------|-----------|
| ETHEUR | 1m | 720 | 60s | ✅ 719/719 | timestamp = candle_open |
| ETHEUR | 5m | 300 | 300s | ✅ 299/299 | timestamp = candle_open |
| ETHEUR | 15m | 200 | 900s | ✅ 199/199 | timestamp = candle_open |
| ETHEUR | 60m | 150 | 3600s | ✅ 149/149 | timestamp = candle_open |
| ETHEUR | 240m | 120 | 14400s | ✅ 119/119 | timestamp = candle_open |
| BTCEUR | Alle | — | — | ✅ alle | timestamp = candle_open |

**Bewijs:** Alle intervallen tussen opeenvolgende timestamps zijn exact gelijk aan de TF-interval. De `date`-string toont "HH:MM" wat overeenkomt met de candle-open tijd (bijv. timestamp 1783792080 → date "2026-07-11 17:48"). Dit is consistent met Kraken OHLC-conventie waarbij timestamp de candle-open time is.

**Conclusie: `candle.timestamp = candle open time` — bewezen.**

#### Cache Depth — GEMETEN

| Pair | TF | Candles | First TS | Last TS | Duration |
|------|-----|---------|----------|----------|----------|
| ETHEUR | 1m | 720 | 1783749180 | 1783792320 | ~12h |
| ETHEUR | 5m | 300 | 1783702500 | 1783792200 | ~25h |
| ETHEUR | 15m | 200 | 1783612800 | 1783791900 | ~50h |
| ETHEUR | 60m | 150 | 1783252800 | 1783789200 | ~6.2d |
| ETHEUR | 240m | 120 | 1782072000 | 1783785600 | ~20d |
| BTCEUR | Alle | ≈ zelfde | ≈ zelfde | ≈ zelfde | ≈ zelfde |

#### Window Coverage Analyse

Voor latest snapshot (asof ~1783790700, 17:25 UTC):

| Venster | 1m candles nodig | Beschikbaar na asof | Status |
|---------|-----------------|--------------------|--------|
| 5m | 5 | ~27 | ✅ complete |
| 15m | 15 | ~27 | ✅ complete |
| 60m | 60 | ~27 | ⚠️ partial (27/60) |
| 240m | 240 | ~27 | ⚠️ partial (27/240) |

Voor hogere TFs direct (ipv 1m aggregatie):

| Venster | Hogere TF | Candles nodig | Beschikbaar na asof | Status |
|---------|-----------|---------------|--------------------|--------|
| 60m | 60m candles | 1 | 0 (next at 18:00) | ❌ not yet closed |
| 240m | 240m candles | 1 | 0 | ❌ not yet closed |

**Conclusie:** Voor recente snapshots kan live_cache alleen 5m en 15m vensters volledig dekken via 1m candles. 60m en 240m vensters vereisen ofwel diepere cache, ofwel wachten tot hogere-TF candles sluiten, ofwel archive fallback.

#### OHLC Source Policy — cache_for_recent_only

**Phase 1A beleid:**

```
cache_for_recent_only
```

Outcome Builder gebruikt uitsluitend `live_cache/{PAIR}_{TF}.json` als OHLC-bron.

Outcome Builder mag alleen complete windows meten als:
- `candles_found == candles_expected`
- timestamps contiguous zijn (geen gaten)
- window volledig gedekt is door beschikbare candles

Anders:
- `status = partial` (0 < candles_found < candles_expected)
- `status = missing` (candles_found == 0)

**Strikte statusdefinities:**
- `complete`: candles_found == candles_expected
- `partial`: 0 < candles_found < candles_expected
- `missing`: candles_found == 0

Geen "missing" gebruiken voor partial coverage. 27/240 is partial, niet missing.

**Geen reconstructie. Geen gok. Geen archive pretend.**

**Archive fallback — toekomstige vereiste (Phase 1B+):**

Archive fallback is **verplicht** vóór Phase 1B, bulk outcome, of historische outcome.

Niet als open vrijblijvende vraag — dit is een harde toekomstige requirement.

**Dekkingsgat documentatie:**
- `live_cache` is recent/rolling (~12h voor 1m)
- Kwartaal-CSV/archive (`historischedata/`) is historische fallback
- Tussen live_cache en archive kan tijdelijk een meetgat bestaan
- Dat meetgat moet expliciet `missing`/`partial` worden, niet opgevuld

---

## 4. Reference Price Rule

**Voorstel (ongewijzigd):**

```
reference_price = snapshot.raw_blob["1m"].price.current.close
reference_source = "snapshot.price.current.close"
reference_timeframe = "1m"
```

**Bewezen:**
- asof_ts % 60 = 0 — asof ligt exact op 1m candle boundary
- timestamp = candle_open (bewezen in §3.2)
- `price.current.close` is de close van de candle die **net opende** op asof
- Op boundary is dit praktisch de openingsprijs van de nieuw gestarte 1m candle

**Alternatief (niet gekozen voor Phase 1):**
- `snapshot.price.previous.close` — close van de net gesloten candle vóór asof
- Zou referentie zijn vóór asof, niet op asof

**Phase 1 keuze:** `price.current.close` — omdat dit de ASOF-prijs is volgens huidige runner/candle-open semantiek.

---

## 5. Outcome Windows

**Phase 1 vensters:**

| Venster | Candles (1m) | Beschrijving |
|---------|-------------|--------------|
| +5m | 5 | Directe micro-reactie |
| +15m | 15 | Korte-termijn beweging |
| +60m | 60 | Uurlijkse context (⚠️ vaak partial) |
| +240m | 240 | Sessie/halve dag (⚠️ vaak partial, zelden complete) |

**Per venster opslaan:**

| Veld | Type | Beschrijving |
|------|------|-------------|
| `window_start_ts` | int | asof_ts (inclusive start) |
| `window_end_ts` | int | asof_ts + window_seconds (exclusive end) |
| `candles_expected` | int | Theoretisch aantal candles |
| `candles_found` | int | Werkelijk gevonden |
| `completeness_status` | string | `complete` / `partial` / `missing` |
| `final_close` | float | Close van laatste candle in venster |
| `high` | float | Hoogste high in venster |
| `high_ts` | int | Timestamp van high |
| `low` | float | Laagste low in venster |
| `low_ts` | int | Timestamp van low |
| `close_delta_abs` | float | final_close - reference_price |
| `close_delta_pct` | float | (final_close - reference_price) / reference_price * 100 |
| `max_up_abs` | float | high - reference_price |
| `max_up_pct` | float | (high - reference_price) / reference_price * 100 |
| `max_down_abs` | float | reference_price - low (positief getal) |
| `max_down_pct` | float | (reference_price - low) / reference_price * 100 |

**Neutrale naamgeving:**
- `max_up` — niet "gain" of "profit"
- `max_down` — niet "loss" of "drawdown"
- `close_delta` — niet "return" of "PnL"

---

## 6. Candle Inclusion Rule

**Bewezen:** timestamp = candle_open. asof % 60 = 0.

**Keuze Phase 1A:**

```
INCLUDE candle met timestamp == asof_ts in outcome.
```

**Reden:**
- candle opent op asof_ts — zijn high/low/close ontstaan allemaal NA asof
- Reference price (= price.current.close) komt uit snapshot op asof
- De candle op asof representeert de eerste minuut prijsbeweging na het snapshot
- Uitsluiten zou max_up/max_down in de eerste minuut missen

**Regel:**
- Eerste outcome candle: timestamp >= asof_ts
- Laatste outcome candle: timestamp < asof_ts + window_seconds
- Aantal verwacht: window_seconds / 60 (voor 1m candles)

**Concreet voorbeeld 5m window (asof = 1783790700):**
- Included candles: asof+0, asof+60, asof+120, asof+180, asof+240 (=5 candles)
- Excluded: asof+300 (open_ts == window_end_ts)

---

## 7. Output Contract Draft — Fable-Hardened

```json
{
  "outcome_contract_version": 1,
  "source_snapshot": {
    "snapshot_id": "ETHEUR-1783790700-1m5m15m60m240m-0d3e83c83b07",
    "pair": "ETHEUR",
    "asof_ts": 1783790700,
    "snapshot_version": 1
  },
  "generated_at": "2026-07-11T17:30:00+00:00",
  "reference": {
    "price": 1595.13,
    "source": "snapshot.price.current.close",
    "timeframe": "1m",
    "boundary_status": {
      "asof_on_1m_boundary": true,
      "asof_mod_60": 0,
      "timestamp_semantics": "candle_open",
      "reference_meaning": "close of newly opened 1m candle at asof boundary"
    }
  },
  "windows": {
    "5m": {
      "status": "complete",
      "window_start_ts": 1783790700,
      "window_end_ts": 1783791000,
      "candles_expected": 5,
      "candles_found": 5,
      "final_close": 1596.06,
      "high": 1596.06,
      "high_ts": 1783790820,
      "low": 1594.91,
      "low_ts": 1783790760,
      "close_delta_abs": 0.93,
      "close_delta_pct": 0.0583,
      "max_up_abs": 0.93,
      "max_up_pct": 0.0583,
      "max_down_abs": 0.22,
      "max_down_pct": 0.0138
    }
  },
  "field_limitations": [
    "Outcome is descriptive hindsight, not a trade decision.",
    "max_up/max_down are measurements, not profit/loss.",
    "close_delta is a measurement, not a return."
  ],
  "scope_notes": [
    "Outcome is descriptive hindsight.",
    "Outcome is not a trade decision.",
    "Outcome is not an entry or exit.",
    "Outcome is not a strategy result."
  ]
}
```

**Contractwijzigingen t.o.v. v1:**
- ✅ `boundary_status` verplicht aanwezig — altijd, niet alleen bij afwijking
- ✅ `timestamp_semantics` expliciet: "candle_open"
- ✅ `reference_meaning` gedocumenteerd
- ✅ Scope notes exact — geen vrije formulering

---

## 8. Storage Proposal

**Aanbevolen locatie:**

```
projects/hermes-v03-outcome/outcome_store/{PAIR}/
```

**Opslagformaat (voorstel):**
- JSONL per pair per maand: `{PAIR}_2026-07_outcomes.jsonl`
- Eén regel per outcome = één snapshot
- Pair-isolated zoals L4 store
- Snapshot_id als primary key

**Recompute/dedup beleid (Phase 1C):**
- Phase 1A: stdout-only, geen storage
- Phase 1C storage moet kiezen:
  - `latest-line-wins` — eenvoudig, laatste run overschrijft
  - `only-write-complete` — alleen complete windows schrijven
  - `upsert` via SQLite — later te overwegen
- Nog geen implementatie in Phase 1A

---

## 9. CLI Proposal

**Voorstel (later, niet nu bouwen):**

```bash
python3 projects/hermes-v03-outcome/cli.py \
  --pair ETHEUR \
  --snapshot-id ETHEUR-1783790700-1m5m15m60m240m-0d3e83c83b07 \
  --base-dir projects/hermes-v03-interpreter/l4_store \
  --ohlc-source projects/crypto-data/logs/live_cache \
  --windows 5m,15m,60m,240m \
  --format json
```

---

## 10. Guardrail Mechanism — Fable-Hardened

Outcome Builder hergebruikt A0 guardrail-principe:

1. **Template-first output** — geen vrije tekstgeneratie
2. **Exact allowed sentence whitelist** — alleen deze zinnen met verboden woorden:
   **Scope notes:**
   - "Outcome is not an entry or exit."
   - "Outcome is not a strategy result."
   - "Outcome is not a trade decision."
   - "Outcome is descriptive hindsight, not a trade decision."
   **Field limitations:**
   - "max_up/max_down are measurements, not profit/loss."
   - "close_delta is a measurement, not a return."
   - "Outcome is descriptive hindsight, not a trade decision."
3. **JSON value scanning** — alle JSON keys en values gescand
4. **Forbidden words blocked** — buiten exacte whitelist-zinnen
5. **CLI subprocess tests verplicht** — exit codes geverifieerd
6. **Guardrail failure krijgt expliciete exit code**

**Verboden in output (buiten scope-note whitelist):**
- buy, sell, long, short, entry, exit, koop, verkoop
- setup, signal, signaal, confirmed
- good trade, bad trade, win, loss, profit, PnL
- target, stoploss, take profit, TP, SL
- confidence, prediction, probability, verwacht

---

## 11. Tests Plan — Expanded

| # | Test | Beschrijving |
|---|------|-------------|
| 1 | `test_reads_snapshot_not_a0` | Leest L4 snapshotvelden, niet A0-tekst |
| 2 | `test_rejects_missing_snapshot` | Nette fout bij ontbrekende snapshot |
| 3 | `test_rejects_missing_future_ohlc` | Nette fout bij ontbrekende OHLC data |
| 4 | `test_marks_partial_window` | Venster met te weinig candles → status partial |
| 5 | `test_marks_complete_window` | Venster met exact genoeg candles → status complete |
| 6 | `test_boundary_exact_12_utc` | Candle met timestamp == asof hoort WEL in outcome |
| 7 | `test_includes_candle_at_asof` | Eerste outcome candle timestamp >= asof_ts |
| 8 | `test_computes_max_up_from_candles` | high - reference_price klopt |
| 9 | `test_computes_max_down_from_candles` | reference_price - low klopt |
| 10 | `test_no_win_loss_language` | Output bevat geen win/loss/entry/exit |
| 11 | `test_no_db_write_default` | Schrijft niet tenzij --output pad gegeven |
| 12 | `test_pair_isolated` | Outcome voor ETHEUR leest geen BTCEUR data |
| 13 | `test_snapshot_id_keyed` | Outcome is keyed op snapshot_id |
| 14 | `test_no_a0_parsing` | Leest nooit A0-output bestanden |
| 15 | `test_missing_ohlc_file` | Nette fout bij ontbrekend live_cache bestand |
| 16 | `test_candle_timestamp_semantics` | Bewijst dat timestamp = candle_open in fixture |
| 17 | `test_guardrail_whitelist_self` | Scope-note én field_limitations whitelist triggert scanner niet |
| 18 | `test_guardrail_json_values_scanned` | JSON values met buy/sell/entry worden gedetecteerd |
| 19 | `test_cli_exit_codes` | CLI exit codes: 0 success, 2 read error, 5 guardrail |
| 20 | `test_no_wal_artifacts` | Read-only reader maakt geen WAL/SHM artefacten |
| 21 | `test_cache_depth_missing_window` | Venster buiten cache → status missing/partial |
| 22 | `test_boundary_status_present` | boundary_status altijd in output |

**Toekomstige runtime invariant (optioneel, niet Phase 1A):**

Voor candle_open semantics, als sanity check bij elke outcome run:
```
latest_candle.timestamp <= now < latest_candle.timestamp + interval
```
Dit verifieert dat de laatste candle in live_cache nog open/in-progress is.
Niet verplicht voor Phase 1A, wel aanbevolen als future invariant.

---

## 12. Relation to Later Layers

```
┌──────────────────────────────────────────┐
│              L4 SNAPSHOT                  │
│  (data/geheugen — wat zagen we?)          │
├──────────────────────────────────────────┤
│              ANALYST A0                   │
│  (presentatie — FROZEN)                   │
│  Beschrijft context in mensentaal         │
│  Wordt NIET geparset door andere lagen    │
├──────────────────────────────────────────┤
│           OUTCOME BUILDER                 │
│  (DIT PLAN — wat gebeurde er?)            │
│  Meet prijsbeweging na asof               │
│  Descriptief, geen strategie              │
│  Leest snapshots + live_cache OHLC        │
├──────────────────────────────────────────┤
│         STRATEGY TEST HARNESS             │
│  (later — wat als we regel X hadden?)     │
│  Test hypothetische regels historisch     │
│  Leest snapshots + outcomes               │
├──────────────────────────────────────────┤
│              ANALYST A1+                  │
│  (later — contextweging)                  │
│  MTF alignment, candidate/scoring         │
│  Leest snapshots + gestructureerde data   │
├──────────────────────────────────────────┤
│              TESTBOT                      │
│  (later — paper simulatie)                │
├──────────────────────────────────────────┤
│              TRADER                       │
│  (veel later — live executie)             │
└──────────────────────────────────────────┘
```

---

## 13. No-Backflow Rule — HARD ARCHITECTUURREGEL

**Harde regel:**

Geen enkele laag die ASOF snapshots produceert of presenteert mag outcome_store lezen.

Concreet:
- A0 leest **nooit** outcome data
- L4 snapshot builder leest **nooit** outcome data
- Hermes-v03 chart reader leest **nooit** outcome data tijdens ASOF snapshot generation
- Outcome Builder schrijft **nooit** terug naar L4 raw snapshot
- Outcome data blijft **fysiek en logisch gescheiden** van ASOF data

Outcome mag later alleen gelezen worden door:
- Strategy Harness
- A1+
- Audits die expliciet OUTCOME-mode zijn

**ASOF-mode en OUTCOME-mode blijven gescheiden.**

Open vraag voor later: "hoe technisch afdwingen via tests/paths?"

---

## 14. Open Questions

| # | Vraag | Status |
|---|-------|--------|
| 1 | Welke OHLC-bron is canonical? | ✅ Beantwoord: `live_cache/{PAIR}_{TF}.json` |
| 2 | Welke reference price? | ✅ Beantwoord: `price.current.close` (1m) |
| 3 | Welke outcome windows Phase 1? | ✅ 5m, 15m, 60m, 240m |
| 4 | JSONL of SQLite voor outcome store? | ⬜ Voorgesteld: JSONL |
| 5 | Automatisch of handmatig draaien? | ⬜ Handmatig voor Phase 1 |
| 6 | Hoe teruglek naar ASOF voorkomen? | ✅ Harde no-backflow regel (§13) |
| 7 | Fable review verplicht vóór implementatie? | ⬜ Aanbevolen: ja |
| 8 | Hoe technisch afdwingen no-backflow? | ⬜ Open — via tests/paths in Phase 1 |
| 9 | Archive fallback implementatiepad? | ✅ Verplicht vóór Phase 1B |

---

## 15. Recommended Phase 1 Implementation Path

### Phase 1A — Read-only prototype
- Eén pair (ETHEUR)
- Laatste snapshot (latest)
- Leest L4 (mode=ro) + live_cache
- JSON stdout only
- boundary_status verplicht in output
- Guardrail scanner actief
- Tests 1-11, 16-22
- **cache_for_recent_only** — alleen complete vensters

### Phase 1B — Multi-window + robustness
- Alle vensters: 5m, 15m, 60m, 240m
- ETHEUR + BTCEUR smoke
- Missing/partial detectie voor grotere vensters
- Archive fallback voor historische snapshots
- Tests 1-22

### Phase 1C — Optional storage
- `--output` flag voor JSONL write
- latest-line-wins of only-write-complete
- Pair-isolated bestanden
- Nog steeds geen strategie

---

## RAPPORTAGE — Fable-Hardened v2

| # | Check | Status |
|---|-------|--------|
| 1 | Plan patched | ✅ Ja — 5 blockers + 4 non-blockers verwerkt |
| 2 | Path | `/home/sjoe/system/hermes-second-brain/second-brain/raw/sessions/2026-07-11-outcome-builder-phase-0-plan.md` |
| 3 | New line count | ~490 |
| 4 | Candle timestamp semantics bewezen | ✅ Ja — alle 5 TFs, beide pairs, 100% interval match |
| 5 | Timestamp = candle_open | ✅ Bewezen: Kraken-conventie, interval-consistentie, date-veld |
| 6 | Cache depth measured | ✅ Ja |
| 7 | ETHEUR cache depth: 1m=720(12h), 5m=300(25h), 15m=200(50h), 60m=150(6.2d), 240m=120(20d) | ✅ |
| 8 | BTCEUR cache depth: ≈ zelfde | ✅ |
| 9 | Source policy: cache_for_recent_only | ✅ Ja — alleen complete vensters, geen reconstructie |
| 10 | Archive fallback: promoted to future requirement | ✅ Ja — verplicht vóór Phase 1B |
| 11 | boundary_status added to contract | ✅ Ja — altijd aanwezig, timestamp_semantics expliciet |
| 12 | Guardrail mechanism added | ✅ Ja — template-first, whitelist scope notes, JSON scan |
| 13 | No-backflow promoted to architecture rule | ✅ Ja — harde regel in §13 |
| 14 | Candle inclusion rule clarified | ✅ Ja — INCLUDE candle op asof (open = asof, beweging erna) |
| 15 | Testplan expanded | ✅ Ja — 22 tests (was 15), incl. timestamp, guardrail, boundary |
| 16 | Remaining open questions | 4 (storage formaat, automation, Fable review, technisch afdwingen) |
| 17 | No code changes | ✅ Ja |
| 18 | No tests changed | ✅ Ja |
| 19 | No DB/service/timer changes | ✅ Ja |
| 20 | No commit | ✅ Ja |
| 21 | git status --short | ✅ Ongewijzigd |
