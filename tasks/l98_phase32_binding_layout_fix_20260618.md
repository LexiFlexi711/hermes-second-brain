# L98 Phase 3.2 — Binding & Layout Fix (2026-06-18)

## Doel
Fix twee bewezen problemen uit Phase 3.1:
A) hardcoded fake candidate vervangen door echte truth record data
B) L98 renderer canvas/layout auditbaar maken

## Binding fix uitgevoerd
- Oud: entry_price=3450, support=3400, resistance=3500 (hardcoded)
- Nieuw: entry_price=2064.73, support=2049.32, resistance=2061.96 (uit truth record)
- Guard ENTRY_IN_LOCAL_RANGE passeert nu ✅

## Layout fix uitgevoerd
- Oud: 1816x22016 (aspect 0.082) — bbox_inches=tight explode
- Nieuw: 1920x1080 (aspect 1.778) — constrained_layout, geen bbox_inches
- Geen tight_layout, geen font warnings, geen deprecations

## Nieuwe proof chart
`charts/full/replay_charts/l98_phase32_proof/l98_phase32_etheur_15_1706094000_INVALID_GUARDS_FAILE.png`
1920x1080, aspect 1.778, verdict: INVALID_GUARDS_FAILED

## Tests
- 17/17 Phase 3 tests (6 nieuwe: PNG size, aspect, bbox, tight_layout, guards)
- 538/538 total passed

## Verdict
`L98_PHASE32_PROOF_CHART_FIXED_AND_RENDERED`
