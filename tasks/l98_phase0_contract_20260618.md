# L98 Phase 0 — Contract Definition (2026-06-18)

## Status
- L5/V5 frozen ✅
- Oude L98 scripts zijn legacy/temp (niet gebruiken)
- Nieuwe official L98 contract bestaat in `layer98_historical_audit/`

## Contract
- L98 is aparte historical audit renderer
- L98 mag GEEN V5 wrapper zijn
- L98 mag L2/L3/L4/L9 read-only gebruiken
- L98 mag NIET V5 importeren

## Bestanden
- `layer98_historical_audit/audit_contract.py` — contractdefinitie
- `layer98_historical_audit/audit_models.py` — dataclasses
- `layer98_historical_audit/audit_guards.py` — 5 guardfuncties
- `tests/test_layer98_historical_audit_contract.py` — 9 tests

## Tests
- 9/9 L98 tests passed
- 486/486 total passed
- Geen verboden imports in official L98

## Verdict
`L98_PHASE0_CONTRACT_READY`
