# L98 Phase 3.1 — Binding & Layout Audit (2026-06-18)

## Doel
Audit waarom Phase 3 proof chart een INVALID_DEBUG_CHART was en waarom de PNG layout onleesbaar was.

## Binding mismatch
- **Oorzaak:** Smoke test gebruikte hardcoded entry_price=3450/support=3400/resistance=3500
- **Realiteit:** Echte ETH prijs in Jan 2024 (ts=1706094000) was ~$2050-2100
- **Candle range:** correct [2023.58, 2077.85]
- **Guards werkten perfect:** ENTRY_OUTSIDE_LOCAL_RANGE correct gedetecteerd
- **Echte truth record #0** heeft S/R rond 2050, géén entry_price veld

## Layout mismatch
- **Oorzaak:** `bbox_inches="tight"` + gridspec text boxes = canvas 22016px hoog
- `tight_layout` werkt slecht met gridspec + text-only axes
- Width 1816 px OK, height 22016 px absurd (aspect 0.082)

## Besluit
L98 renderer weigerde CORRECT een valse entry-chart. Beide oorzaken zijn gevonden.

## Verdict
`L98_PHASE31_BINDING_AND_LAYOUT_CAUSE_FOUND`
