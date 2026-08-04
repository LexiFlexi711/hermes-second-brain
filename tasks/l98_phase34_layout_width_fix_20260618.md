# L98 Phase 3.4 — Layout Width Fix (2026-06-18)

## Probleem
Infopaneel rechts stal breedte van de main chart. Main chart was maar 1440px breed bij 1920px canvas.

## Oplossing
Canvas verbreed naar 24x9 (2880x1080). Main chart krijgt vaste 1920px (16 inch). Info gebruikt extra 960px rechts.

## Proof chart
`charts/full/replay_charts/l98_phase34_proof/l98_phase34_etheur_15_1706094000_INVALID_GUARDS_FAILE.png`
2880x1080, main chart 1920px, info_panel_affects_chart_width=false

## Tests
- 21/21 Phase 3 tests (4 nieuwe layout tests)
- 542/542 total
- 0 forbidden imports

## Verdict
`L98_PHASE34_MAIN_CHART_WIDTH_FIXED`
