---
title: Strategy Harness Evaluation Phase 1B Primitives
type: project
status: frozen
updated: 2026-08-26
tags: [strategy-harness, evaluation, phase1b, freeze, signal-quality]
---

# Strategy Harness Evaluation Phase 1B Primitives

Signal-quality primitieven bovenop de frozen Phase1A join (`45109f2e`).
Gefrozen op 2026-08-26.

## Status

🟢 **FROZEN** — PASS_FROZEN.

## Lineage

Phase3B `213d77db` → Phase0 `1225cd8e` → Phase1A `45109f2e` →
RC1 `a30fce5e` → RC2 `ea7e0467` → RC3 `1c824599` →
review `45e8f1ca` → freeze `ca1bfd2a`.

## Review

- RC1 `a30fce5e` → ORANGE 0 Critical / 0 High / 2 Medium / 3 Low
- RC2 `ea7e0467` → ORANGE 0/0/2/3
- RC3 `1c824599` → GREEN 0/0/0/3

## Wat het NIET is

Geen PnL, geen scoring, geen ranking, geen optimizer, geen baseline,
geen statistical confidence, geen composite. Enkel signal-quality primitieven.

## Accepted semantics

- signal quality, NOT PnL
- NO_SIGNAL coverage-only
- LONG/SHORT directional semantics separate
- selected horizons explicit; complete horizons only for quality metrics
- partial/missing horizons excluded with reason
- coverage/directional zero denominator = NOT_APPLICABLE/null
- FLAT excluded from HIT+MISS denominator
- favorable/adverse normalization
- COUNT/MEAN/MEDIAN only; finite values only; canonical aggregation order
- evidence status DESCRIPTIVE_ONLY
- geen min-sample threshold, geen onafhankelijkheidsclaim, geen percentielen extra

## Evidence binding

- exact Phase1A Outcome reference (record_id + record_revision)
- exact historical revision dereference, geen current/latest fallback
- prefix chain validation through referenced revision (latere corrupte revisie
  kan oudere geldige frozen evidence niet ongeldig maken)
- content projection bound back to frozen record_id/source_record
- tampered materialized content rejected (MATERIALIZED_SAMPLE_MISMATCH)
- Outcome revision transitively bound into evaluation_result_id

## Consistent read

manifest before → materialize once → manifest after; max 2 retries /
max 3 attempts; geen per-sample disk reread; HARD_FAIL op unstable store.

## Frozen implementation files

```
strategy_harness/evaluation_result_contracts.py
strategy_harness/evaluation_outcome_materialization.py
strategy_harness/evaluation_metrics.py
```

## Test resultaten (final acceptance)

- Phase1B: 123 passed / 0 failed
- Phase1A: 52 passed
- Phase3B: 68 passed / 9 skipped
- Outcome: 186 passed
- Guardrail: 70 passed / 12 skipped
- Full core: 462 passed / 17 inherited failures / 21 skipped
- Candidate new failures: 0

## Real pipeline acceptance

REAL_PIPELINE_TEMP, pair ETHEUR, echte L4 + echte OHLC, values niet gewijzigd,
availability cutoff only. Writer-genereerde revision 1 + revision 2 (zelfde
Outcome chain). Supersedes + previous-hash links PASS. Old/new revision
dereference PASS. Real content-tamper rejected. Canonical stores niet gemuteerd.

## LOW findings (NON_BLOCKING, NOT_FIXED_DURING_FREEZE)

1. `_is_actionable` dead code — cosmetisch
2. Claude real-acceptance verificatie tooling boundary
3. temp-store / housekeeping residu

## Deferred items

MIN_SAMPLE_THRESHOLD=TBD, CORRELATED_SAMPLE_POLICY=NEEDS_EVIDENCE,
ADDITIONAL_PERCENTILE_SET=NEEDS_DEFINITION, REWARD_RISK_ASYMMETRY=DEFERRED,
STATISTICAL_UNCERTAINTY=DEFERRED, BASELINES=DEFERRED, MULTIPLE_TESTING=DEFERRED,
COMPOSITE=DEFERRED, PNL/EXECUTION=DEFERRED.

## Freeze record

`projects/hermes-v03-strategy-harness/evaluation/PHASE1B_PRIMITIVES_FREEZE_RECORD.md`

## Gerelateerd

- [[strategy-harness-evaluation-pipeline]] — volledige lineage
- [[outcome-builder-phase-1a]] — Outcome Builder
- [[noa-reign-roadmap-v2]] — roadmap
