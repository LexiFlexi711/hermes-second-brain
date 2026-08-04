# L98 Phase 3.5 — Bottom Info Layout (2026-06-18)

## Probleem
Info rechts of overlay versmalde of bedekte steeds de candle-zone. Geen enkele eerdere "fix" loste dit op.

## Oplossing
Rechterpaneel verwijderd. Overlay verwijderd. Info in compact bottom panel (9% hoogte). Main chart full-width (92%).

## Proof chart
`charts/full/replay_charts/l98_phase35_proof/l98_phase35_etheur_15_1706094000_INVALID_GUARDS_FAILE.png`
2560x1440, main chart 92% width, info bottom 9% height

## Checks
- right_panel_removed: true ✅
- info_panel_position: bottom ✅
- info_panel_fraction_height: 0.09 ≤ 0.10 ✅
- main_axes_fraction_width: 0.92 ≥ 0.90 ✅
- overlay_used: false ✅

## Tests
- 22/22 Phase 3 tests
- 543/543 total
- 0 forbidden imports

## Verdict
`L98_PHASE35_BOTTOM_INFO_FULL_WIDTH_FIXED`
