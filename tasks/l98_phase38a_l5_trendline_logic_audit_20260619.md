# L98 Phase 3.8A — L5 Trendline Logic Audit (2026-06-19)

## Vermoeden bevestigd
L98 gebruikt een compleet andere, simplistische trendline-logica dan L5/V5.
L4 wordt gereduceerd tot een boolean `l4_present=True`. Geen enkele L4 trendline-functie wordt aangeroepen.

## L5 pipeline
swings → select_upper_points (best 15) → generate_candidates (alle paren) → validate (score, touches, violations) → pick_top (sort + bonus) → _render_line (diamond anchors)

## L98 pipeline
swings → neem laatste 3 → rechte lijn first→last (geen selectie, geen validatie, geen scoring)

## L4 functies die L98 negeert
select_upper_points, generate_upper_candidates, validate_upper_candidate, pick_top_upper_candidates, _render_line, read_recent_trendlines

## Fix-plan (niet uitgevoerd)
6 stappen: roep echte L4 functies aan ipv eigen simplistische logica.

## Tests
555/555 passed. Geen code gewijzigd.

## Verdict
`L98_PHASE38A_L5_TRENDLINE_DIFFERENCE_FOUND`
