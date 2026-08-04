# Outcome Builder Phase 1A Freeze

**Datum:** 2026-07-12
**Status:** Frozen — Fable green review passed
**Aanleiding:** Commit 901a68e1 — Outcome Builder Phase 1A read-only prototype

---

## 1. Commit

| Veld | Waarde |
|------|--------|
| SHA | `901a68e16cb9052297fc7821e495ebe1de827b22` |
| Message | Add Outcome Builder Phase 1A read-only prototype |
| Branch | main |
| Remote | origin/main |
| A0 frozen commit | `4872eaa4525bcfb8ff53f290b5b7100cfa810ae4` |

---

## 2. Doel van Outcome Builder Phase 1A

Outcome Builder meet wat er na een L4 snapshot gebeurde.

- **Read-only** — geen writes naar L4, A0, of storage
- **JSON stdout only** — geen bestandsopslag in Phase 1A
- **cache_for_recent_only** — uitsluitend live_cache als OHLC-bron
- **1m live_cache candles** als canonical future source
- **Descriptieve hindsight** — geen interpretatie, geen strategie

---

## 3. Architectuurpositie

```
┌──────────────────────────────────────────┐
│              HERMES / L4                  │
│  ASOF snapshot/context                    │
│  (data — wat zagen we?)                   │
├──────────────────────────────────────────┤
│              ANALYST A0                   │
│  (presentatie — FROZEN)                   │
│  Wordt NIET geparset door andere lagen    │
├──────────────────────────────────────────┤
│           OUTCOME BUILDER                 │
│  (DIT — wat gebeurde er?)                 │
│  Meet prijsbeweging na asof               │
│  Descriptief, geen strategie              │
├──────────────────────────────────────────┤
│         STRATEGY HARNESS (later)          │
├──────────────────────────────────────────┤
│              A1+ (later)                  │
├──────────────────────────────────────────┤
│           TESTBOT (later)                 │
├──────────────────────────────────────────┤
│           TRADER (veel later)             │
└──────────────────────────────────────────┘
```

---

## 4. Contractregels

| Regel | Waarde |
|-------|--------|
| OUTCOME_CONTRACT_VERSION | 1 |
| ALLOWED_SCHEMA_VERSIONS | {1} |
| source_policy | cache_for_recent_only |
| reference | snapshot.price.current.close uit 1m raw_json |
| generated_at | ISO UTC string |
| Exit code 0 | success |
| Exit code 2 | read error / missing data |
| Exit code 3 | schema/contract/semantic error |
| Exit code 5 | guardrail violation |
| A0 parsing | verboden — outcome leest nooit A0 output |
| No-backflow | outcome data wordt nooit gelezen door ASOF lagen |

---

## 5. Windowregels

| Venster | Candles (1m) | Beschrijving |
|---------|-------------|--------------|
| +5m | 5 | Directe micro-reactie |
| +15m | 15 | Korte-termijn beweging |
| +60m | 60 | Uurlijkse context |
| +240m | 240 | Sessie/halve dag |

**Candle inclusie:**
- timestamp = candle_open (bewezen via interval-analyse)
- include: timestamp >= asof_ts
- exclude: timestamp >= window_end_ts

**Completeness statussen:**
- `complete` — found == expected
- `partial` — 0 < found < expected
- `missing` — found == 0

Partial/missing is geen failure — het is een meetresultaat.

---

## 6. Metricregels

| Metriek | Formule | Type |
|---------|---------|------|
| close_delta_abs | final_close - reference_price | float (signed) |
| close_delta_pct | close_delta_abs / reference_price * 100 | float (signed) |
| max_up_abs | high - reference_price | float |
| max_up_pct | max_up_abs / reference_price * 100 | float |
| max_down_abs | max(0, reference_price - low) | float (positief) |
| max_down_pct | max_down_abs / reference_price * 100 | float (positief) |

**Naamgeving:**
- `max_up` — niet "gain" of "profit"
- `max_down` — niet "loss" of "drawdown"
- `close_delta` — niet "return" of "PnL"
- Geen win/loss
- Geen trade-resultaat

---

## 7. Cache Sanity

- Sanity check gebruikt `fetched_at`, niet wall-clock `now`
- `cache_staleness_seconds` wordt gerapporteerd
- Stale cache is status/warning, geen failure
- Semantic sanity failure = exit 3
- Negative staleness = clock_skew → exit 3
- `cache_status.has_gaps` aanwezig in output

---

## 8. Guardrails

**Verboden woorden/keys in output:**
- buy, sell, long, short, entry, exit
- TP, SL, take profit, stop loss
- win, loss, profit, PnL
- setup, signal, signaal, confirmed
- confidence, prediction, probability

**Toegestaan met exacte whitelist:**
- Scope notes: "Outcome is descriptive hindsight.", "Outcome is not a trade decision.", "Outcome is not an entry or exit.", "Outcome is not a strategy result."
- Field limitations: "max_up/max_down are measurements, not profit/loss.", "close_delta is a measurement, not a return.", "Outcome is descriptive hindsight, not a trade decision."

Guardrail failure = exit 5.

---

## 9. Tests

| Fase | Count | Delta |
|------|-------|-------|
| Previous | 0 | — |
| Initial Phase 1A | 39 | +39 |
| After Fable fixes | 48 | +9 |
| Removed | 0 | — |
| Skipped | 0 | — |

| Suite | Tests | Status |
|-------|-------|--------|
| Outcome Builder | 48/48 | ✅ |
| A0 (frozen) | 68/68 | ✅ |
| Inspector | 15/15 | ✅ |
| Runner | 76/76 | ✅ |
| **Totaal** | **207/207** | ✅ |

---

## 10. Review Gate

| Fase | Resultaat |
|------|-----------|
| Fable initial | 🟠 ORANGE |
| Blocker a | max_down teken (was negatief, moest positief zijn) |
| Blocker b | TP/SL guardrail (verboden termen niet geblokkeerd) |
| Fixes applied | ✅ |
| Fable final | 🟢 GREEN |
| Commit | Pas na review gate ✅ |

---

## 11. Wat Phase 1A NIET doet

- Geen opslag (stdout only)
- Geen batch processing
- Geen historical archive fallback
- Geen scoring (geen good/bad labels)
- Geen entry/exit
- Geen strategy result
- Geen Testbot
- Geen Trader
- Geen A0 parsing
- Geen backflow naar ASOF lagen

---

## 12. Volgende Toegestane Stap

Phase 1B mag alleen een **plan** zijn voor:

- Outcome Store contract
- Idempotente opslag (JSONL of SQLite)
- Batch/bulk outcomes
- Archive fallback requirement (verplicht vóór Phase 1B)
- No-backflow enforcement
- Review gate vóór code

**Geen Phase 1B code zonder:**
1. Plan
2. Fable review
3. Expliciet akkoord

---

## 13. Bestanden

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

---

## 14. Gerelateerd

- [[a0-snapshot-readout]] — A0 Snapshot Readout (frozen foundation)
- [[2026-07-11-a0-foundation-freeze-and-process-rules]] — A0 freeze + process rules
- [[2026-07-11-outcome-builder-phase-0-plan]] — Outcome Builder plan
- [[outcome-builder-phase-1a]] — Outcome Builder Phase 1A project page
- [[hermes-v03-interpreter]] — L4 interpreter/data layer

---

## RAPPORTAGE

| # | Check | Status |
|---|-------|--------|
| 1 | Document created | ✅ Ja |
| 2 | Path | `/home/sjoe/system/hermes-second-brain/second-brain/raw/sessions/2026-07-12-outcome-builder-phase-1a-freeze.md` |
| 3 | Line count | 252 |
| 4 | No code changes | ✅ Ja |
| 5 | No tests changed | ✅ Ja |
| 6 | No DB/service/timer changes | ✅ Ja |
| 7 | No commit | ✅ Ja |
| 8 | Git status | ✅ Geen tracked diffs |
