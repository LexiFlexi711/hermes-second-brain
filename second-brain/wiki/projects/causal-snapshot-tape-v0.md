---
title: Causal Snapshot Tape V0.2 — Level/Event Tape + Tijdigheid (FROZEN)
type: project
status: FROZEN
date: 2026-09-10
tags: [noa-reign, snapshot-tape, causality, levels, pit-safety, freeze, level-provider-audit]
---

# Causal Snapshot Tape V0.2 — Level/Event Tape + Tijdigheid (FROZEN)

Pilot op exact 5 reviews (`REV_0003`, `REV_0024`, `REV_0030`, `REV_0054`, `REV_0056`).
Read-only; geen productiecode gewijzigd; alles onder
`/mnt/otherdrive1/dataLexi/LexiProjects/tmp/story_linker_v0/pilot_level_tape_v0/`.

Basiscommit: `413bbcbf` (projects/hermes-v03 tree `e5c03509`).

## Waarom deze pilot

De eerdere Story-run had `SYSTEMIC_LEVEL_PROVIDER_BIAS` (240m-levels genegeerd).
Daarna bleek de eerste snapshot-tape wel geometrisch correct maar **temporeel ongeldig**.
Deze pilot lost dat mechanisch op.

## Provider-inventaris (met bronregels)

| Rol | Providers |
|-----|-----------|
| LEVEL_PROVIDER | `P3_60m_swing` / `P4_240m_swing` (`L1_fractals/swing.py:24-136`), `P1_60m_cluster` / `P2_240m_cluster` (`L2_levels/cluster.py:8-119`) |
| LEVEL_TRANSFORMER | `L2_levels/classify.py:18-106`, `collect_structure_points` (`lines.py:11-47`), `build_lines` (`lines.py:50-65`), `L3_labels/__init__.py:9-49` |
| DEPENDENCY (geen level-provider) | `L1_fractals/fractal.py:19-47`, `_candle_window.py:76` (`load_window` = dataloader) |
| NORMALIZER (geen level-provider) | `L6_indicators/__init__.py:58` (`calculate_atr`) |

- **Geen bestaande break-definitie** in hermes-v03 (`grep` 0 hits) → `BREAK_PRIMITIVE_UNDEFINED = True`.
- Lookahead-test `projects/crypto-test-bot-v3/tests/integration/test_lookahead_poison.py`
  dekt de **tradebot**-pijplijn (Runner/V1), NIET de v03 level-pijplijn →
  `LOOKAHEAD_TEST_REUSE = NOT_AVAILABLE` (geen tweede framework gebouwd).

## Wat fout was (bewezen)

1. **HISTORICAL_WINDOW_TRUNCATION** — de eerste tape deed `final_window[:i+1]`, dus vroege
   snapshots kregen slechts 3/10/30 candles i.p.v. 240. Diagnostiek
   `rolling_window_audit_v02.csv`: old 3/10/30 candles en 0–5 levels vs new 240 candles en
   55–61 levels; `level_outputs_identical=false` in 9/9 controles.
2. **TEMPORAL_LEVEL_LEAKAGE** — de review_asof-levels werden tegen oudere candles getest:
   van 15.062 interacties waren 3.474 cluster-rijen pre-existentie-schendingen en 7.901
   swing-rijen pre-confirmation (75%). Cluster-level-identiteit over tijd is niet objectief
   afleidbaar → `CLUSTER_LEVEL_IDENTITY_UNDEFINED = True`.
3. **SAME-BAR SELF-REFERENCE** — candle T mocht niet bijdragen aan het level waartegen
   diezelfde candle getest wordt.

## V0.2-ontwerp (bewezen)

- **STATE_AFTER_T** = f(≤240 candles eindigend op T) — echte rolling replay per T via
  `load_window(pair, tf, source="archive", limit=240, start=None, end=T)`.
  2400 snapshots, allemaal 240 bars, 0 tekort door archiefstart.
- **LEVELS_BEFORE_T** = f(≤240 candles eindigend op PREV_T = T − tf).
- **INTERACTION_DURING_T = candle(T) × LEVELS_BEFORE_T** (nooit × AFTER).
- Geen level-lineage: `snapshot_level_id = review_id|timeframe|BEFORE|T|provider|ordinal`.
- Swings causaliteit (§9): geen verzonnen `confirmation_timestamp`; een swing geldt enkel
  als hij werkelijk in LEVELS_BEFORE_T zit. Gemeten provider-gedrag:
  `swing_first_visible_count = 1024`, `swing_later_disappeared_count = 581`,
  `swing_reappeared_count = 0` → **`SWING_PROVIDER_REPAINTS = True`** (mag de pilot niet laten falen).

## Freeze-gates (alle berekend, niets hardcoded)

| Gate | Waarde |
|------|--------|
| pilot_case_count / timeframe_count | 5 / 2 |
| rolling_snapshot_count / met 240 bars | 2400 / 2400 |
| interaction_rows | 8942 |
| future_after_review_asof_used | false |
| window_last_ts_after_snapshot_ts | 0 |
| interaction_level_missing_from_before_state | 0 |
| interaction_level_only_exists_after_t | 0 |
| invalid_geometric_touch / invalid_overlap | 0 / 0 |
| full_interaction_recompute_mismatches | 0 |
| same_bar_created_ALL / CLUSTER / SWING | 266 / 265 / 1 |
| levels_before_total / levels_after_total | 142863 / 142876 |
| total_added_after / total_removed_after / net | 2434 / 2421 / 13 = observed 13 |
| BOOKKEEPING_VALID | true |
| SWING_COUNTER_DISCREPANCY_RESOLVED | true |
| STORY_RUN_USED_TRUNCATED_WINDOW | FALSE (`data_source.py:59-61` gebruikt correct `end=T−tf`) |

**V0.2_FREEZE_READY = True** · **CAUSAL_SNAPSHOT_TAPE_V0.2 = FROZEN**

## Artefacten

`tmp/story_linker_v0/pilot_level_tape_v0/`:
`snapshot_levels_v0.csv`, `snapshot_interactions_v0.csv`, `level_tape.csv`, `interaction_tape.csv`,
`levels_before_t_v02.csv`, `levels_after_t_v02.csv`, `interactions_during_t_v02.csv`,
`same_bar_self_reference_cases_v02.csv`, `swing_revision_audit_v02.csv`,
`rolling_window_info_v02.csv`, `rolling_window_audit_v02.csv`, `before_after_accounting_v02.csv`,
`prefix_zones.json`.

Scripts: `build_snapshot_tape_v02.py`, `build_window_info_v02.py`, `build_window_audit_v02.py`,
`build_before_after_accounting_v02.py`, `rebuild_same_bar_cases_v02.py`,
`verify_snapshot_tape_v02.py` (canonieke gate; swing-teller gecorrigeerd).

## Les

Een geometrisch correcte tape is niet automatisch een causale tape. Voor élke interactie moet
bewezen zijn dat het level zelf al bestond op het moment van de candle-interactie — niet enkel
dat de candle vóór review_asof ligt.

## Gerelateerd

- [[trader-story-a1a2-story-linker-v0]] · [[market-situation-canonical-calendar-v0-predicates-v01]]
  · [[noa-reign-roadmap-v2]]
