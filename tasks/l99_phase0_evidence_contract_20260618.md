# L99 Phase 0 — Evidence/Export Contract (2026-06-18)

## Status
- L5/V5 frozen ✅
- L98 contract ready ✅
- Oude L99 evidence_layer.py is legacy/experiment (niet gebruiken)
- Nieuwe official L99 contract bestaat in `layer99_evidence_export/`

## Contract
- L99 is evidence/export only
- L99 mag NIET renderen
- L99 mag GEEN entries/candidates kiezen
- L99 mag GEEN V5/L5 gebruiken
- L99 mag geen matplotlib gebruiken

## Bestanden
- `layer99_evidence_export/evidence_contract.py` — contractdefinitie
- `layer99_evidence_export/evidence_models.py` — 3 dataclasses
- `layer99_evidence_export/evidence_writer.py` — 3 veilige writer-functies
- `tests/test_layer99_evidence_export_contract.py` — 11 tests

## Tests
- 11/11 L99 tests passed
- 497/497 total passed
- Geen verboden imports in official L99
- Writer verandert data niet

## Verdict
`L99_PHASE0_EVIDENCE_CONTRACT_READY`
