# Render Architecture Sanering — Task Summary
**Datum:** 2026-06-18
**Project:** hermes-v01
**Verdict:** RENDER_ARCHITECTURE_SANERING_ABORTED_L5_DIRTY

## Wat gebeurd is
Volledige render-architectuur audit uitgevoerd van L1 tot L99. 
13 renderbestanden geanalyseerd op imports, routes, tests, V5-gebruik en output.

## Belangrijkste bevindingen
- **4 render approaches** geïdentificeerd, 43 bestanden met matplotlib/plotting
- L5/V5 is **DIRTY** — structure_cockpit.py heeft uncommitted `candles_override` changes
- Geen enkel render script buiten L98 wordt geïmporteerd, getest of gerouteerd
- `render_mtf.py` hangt op data loading
- `render_rescaled.py` is de enige loose render die geen V5 gebruikt

## Beslissingen vastgelegd
- L1 = KEEP (data chart engine)
- L5 = KEEP_FROZEN (na cleanup dirty state)
- full_context_v5.py = TEMP_DO_NOT_PROMOTE
- Loose render scripts = LEGACY_CANDIDATE
- L98 = FUTURE_OFFICIAL historical audit renderer (geen V5 wrapper)
- L99 = OFFICIAL evidence/export only

## Output bestanden
- `charts/full/files/render_architecture_sanering_audit.md`
- `charts/full/files/render_architecture_sanering_audit.json`
- `charts/full/files/render_file_inventory.csv`
- `charts/full/files/render_file_inventory.json`
- `charts/full/files/render_ownership_matrix.csv`
- `charts/full/files/render_ownership_matrix.json`

## Blokker
Sanering kan pas afgerond worden als L5/V5 dirty state opgelost is.
Opties: commit candles_override of revert.
