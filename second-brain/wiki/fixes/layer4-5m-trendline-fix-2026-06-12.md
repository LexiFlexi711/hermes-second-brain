# Layer 4 — 5m trendline fix (2026-06-12)

## Wat er gebeurd is
De 5m upper trendline op BTCEUR toonde een stijgende lijn (idx=78→158) terwijl de logische structuur een dalende lijn van HH4 naar LH11 vereiste.

## Oorzaak
- LH11→HH4 combinatie (p1=idx136, p2=idx194) stond op positie 36 in span-sortering
- Max candidates was 20 → combinatie werd niet gegenereerd
- Zelfs als die gegenereerd werd: body_violation threshold (0.25) was te strict

## Oplossing (commit 59b4dffa)
Drie aanpassingen in `trendline_lab.py`:

1. **Max candidates verhoogd**: 20 → 40
   - `_generate_candidates(points, max_cand=40)`
   - Zodat verder-gespreide paren (span=58) ook overwogen worden

2. **Body violation thresholds versoepeld**:
   - body_violation_ratio: 0.25 → 0.35
   - price_side_ratio: 0.20 → 0.30
   - body_cut_ratio: 0.25 → 0.35
   - Reden: 5m prijs zigzagt sterk, lijnen snijden door bodies

3. **Score bonus voor logische structuur**:
   - Upper: +15 punten als p1 prijs > p2 prijs (dalend)
   - Lower: +15 punten als p2 prijs > p1 prijs (stijgend)
   - Vervangt generieke `_pick_top()`

## Resultaat 5m
- **Winner**: p1=idx136(HH4, 55594) → p2=idx194(LH11, 55041)
- **Score**: 100 + 15 bonus = 115
- **Touches**: 7 (+5 extra)
- **Body violations**: 0/64 (0%)

## Impact andere TFs
- 240m, 60m, 15m: ongewijzigd (eigen punten, eigen candidates)
- V4 route: zelfde logica, zelfde resultaat
- V2/SR: aparte Layer 2 code, niet beïnvloed

## Revert opties
- Volledige revert: `git revert 59b4dffa`
- Alleen thresholds: herstel naar 0.25/0.20/0.25
- Alleen candidates: herstel `max_cand=20`
- Alleen bonus: herstel `_pick_top()`
