---
title: "Hermes Interpreter -> Outcome Codereview 2026-07-27"
date: 2026-07-27
type: audit
source: Claude Code read-only audit (3 parallel agents + manual verificatie)
status: open — bevindingen nog niet gefixt
---

# Hermes Interpreter -> Outcome Codereview — 2026-07-27

## Scope

Read-only codereview van alle 42 tracked `.py`-bestanden in:
- `projects/hermes-v03-interpreter/`
- `projects/hermes-v03-analyst/`
- `projects/hermes-v03-outcome/`

(repo: NOA-Reign). Volledig rapport gepusht naar branch
`review/hermes-interpreter-outcome-codereview-20260727`,
bestand `CODE_REVIEW.md`, commit `966c786c`.

Methode: 3 parallelle read-only agents (één per project), daarna
handmatige verificatie van de meest ernstige bevindingen door de
bronbestanden zelf te lezen. Geen wijzigingen aan productiecode.

## 🔴 hermes-v03-analyst — guardrail-bypasses (meest ernstig)

1. `a0_snapshot_readout/guardrails.py:376-377` — `_scan_stored_values`
   geeft blanket immuniteit aan élke string onder `stored_values`,
   ongeacht path. Zelf geverifieerd: geen whitelist-check, comment zegt
   letterlijk "stored_values are always immune". `_is_json_stored_value_path`
   (regel 170) is dead code — nergens aangeroepen (bevestigd via grep).
   Voorbeeld: `{'stored_values': {'price.current.note': 'buy signal now'}}`
   → 0 violations.
2. `a0_snapshot_readout/field_whitelist.py:38` — `scan_for_forbidden_ohlc_keys`
   checkt alleen top-level keys; verboden key één niveau dieper
   (bv. `structure.candle_history`) lekt ongefilterd door.
3. `a0_snapshot_readout/guardrails.py:344` — JSON-stringwaarden worden niet
   tegen `FORBIDDEN_A0A1_LEAK` gecheckt (breakout/reversal/gunstig/etc.),
   terwijl keys en tekstoutput dat wel doen.
4. `a0_snapshot_readout/cli.py:95` — schema/contract-versie alleen
   gevalideerd voor de eerste timeframe, niet voor elke aanwezige timeframe.

## 🟠 hermes-v03-interpreter — resource leaks

1. `L4_snapshot_store/__init__.py:1281-1309` (herhaald op 1208-1219,
   1348-1359, 1372-1383) — sqlite3-connectie niet gesloten bij een falende
   `conn.execute`/`cursor.fetchone` op een corrupte DB. Bestaande test
   (`test_l4_snapshot_store.py` Test F) triggert dit pad al.
2. `tools/audit_real_data_e2e.py:57` vs `:78-79` — geïmporteerde
   `_sha256_obj` wordt lokaal overschreven; audit-tool gebruikt stilzwijgend
   zijn eigen kopie i.p.v. de echte hashfunctie die hij hoort te verifiëren.

## 🟡 hermes-v03-outcome — kleiner, deels niet-bereikbaar

1. `outcome_builder/guardrails.py:65-73` — `continue` staat buiten de
   `isinstance(value, list)`-check; scope_notes/field_limitations die geen
   list zijn slaan de scan volledig over. Nu niet bereikbaar via de CLI
   (upstream valideert al als list).

Overige latente/onzekere punten (dode variabele in calculator.py, stale-read
race in store_cli.py run_batch, ontbrekende zero-guard reference_price,
geen try/except om JSONL-append) staan in het volledige rapport — geen
bewezen live bugs.

## Niet gevonden

Geen bare excepts, geen mutable-default-argument bugs, geen aantoonbare
datacorruptie in de store/load-roundtrip. Hash/canonicalisatie-logica
(`canonical_json.py`, `outcome_identity.py`) klopte met eigen contracten.

## Actie

Nog niets gefixt. Wacht op keuze van Lexi welke bevindingen (indien enige)
opgepakt worden. Prioriteit bij keuze: analyst guardrail-bypass #1 (meest
ernstig — kan verboden trading-taal doorlaten via stored_values).
