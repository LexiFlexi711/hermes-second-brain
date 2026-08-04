# L5 Freeze Revert — 2026-06-18

## Waarom revert nodig was
`candles_override` zat in L5 structure_cockpit.py als dirty change. L5/V5 moet frozen blijven — geen replay-features in de Hermes cockpit.

## Welk bestand gerevert
`layer5_cockpit/structure_cockpit.py` — `git checkout --` naar HEAD

## L5/V5 is nu FROZEN
- Geen dirty L5/V5 files
- `candles_override` verwijderd uit L5 source
- V5 functies (`_render_single_tf`, `build_structure_cockpit`) bestaan nog
- V5 route (`/v5/cockpit-img/`) werkt nog
- Geen replay-feature in L5

## L98 later apart
Historical audit renderer wordt later apart gebouwd, zonder V5 wrapper.

## L99 later evidence/export only
Wordt later ingevuld.

## Testresultaat
477 passed ✅ — compileall OK ✅

## Final verdict
`L5_FREEZE_REVERT_DONE`
