# Layer 2 v02 & Layer 3 — Status en Architectuur

## Datum: 12 juni 2026
## Project: NOA-Reign / hermes-v01

## Architectuur Overzicht

### Layer 2 v02 Blokken (layer2_structure_v2/)

| Block | Bestand | Functie | Parameter |
|-------|---------|---------|-----------|
| 🟣 Trendline | `trendline_block.py` | `draw_trendline()` | `show_major_trend` |
| ➖ S/R | `sr_block.py` | `draw_sr_zones()` | `show_sr_zones` |
| 🟡 Pivot rays | `zone_block.py` | `draw_pivot_rays()` | `show_pivot_rays` |
| 🟢 Markers | `marker_block.py` | `draw_markers()` | `show_swings` |
| 🏷️ Labels (Layer 3) | `layer3_label.py` | `draw_layer3_labels()` | `show_layer3_labels` |
| 🧰 Shared | `pivot_utils.py` | `compute_pivots()` | — |

### Swing Detectie
- `swing_highs.py` — fractal top detectie
- `swing_points.py` — unified SwingPoint dataclass + detectie
- `config.py` — per-TF lookback/parameters

### Opgeruimde Dode Code (verwijderd 12/06)
- `major_upper.py` — vervangen door lexi_trend → blocks
- `scoring.py` — was enkel voor major_upper
- `trendline.py` — placeholder
- `lexi_trend.py` — vervangen door individuele blocks
- `debug/` — oude debug outputs

## Layer 3 — D/U/R Labels

### Huidige Status (12/06 16:45)
- Labels worden NIET getoond op chart (show_labels=False)
- Layer 3 `layer3_label.py` klaar maar met foute tolerance
- De tolerance-waarden zijn te hoog:
  - 240m: 1.8% → zou 0.5% moeten zijn
  - 60m: 1.0% → zou 0.3% moeten zijn
  - 15m: 0.55% → zou 0.12% moeten zijn
  - 5m: 0.25% → zou 0.06% moeten zijn

### Problems
- Huidige tolerance zorgt dat 63-82% van segmenten als R gelabeld wordt
- Echte U/D bewegingen worden gemaskeerd als R
- Layer 3 gebruikt enkel purper line punten (geen S/R, zones, touches) — dat is correct
- Fix: tolerance verlagen per TF

## Layer 2 v02 — Rendering

### Routes
- `/v2/sr/<pair>` — S/R cockpit (alle blocks aan)
- `/v2/sr-debug/<pair>` — S/R debug (toont candidate levels)
- `/v2/major-trend/<pair>` — Major trend cockpit
- `/v2/swings/<pair>` — Alleen swing markers
- `/v2/<pair>` — Blank v02
- `/v2/all-pairs` — Alle 4 paren × 4 timeframes

### S/R Selectie Regels
- **240m:** max 5 levels, bundel binnen 0.5%
- **60m:** max 6 levels, bundel binnen 0.5%
- **15m:** max 8 levels, geen bundeling
- **5m:** max 15 levels, geen bundeling
- Pivot levels (waar purper lijn draait) ALTIJD behouden
- Andere levels via touch_density, strong_score

## Lexi Trend Line Definitie
- Paarse lijn door body-average van fractals
- Lijnen ALTIJD op body (max/min open/close), NOOIT wicks
- Apart aan/uit per block
- S/R zones in grijs, dikte via score/touches
- Pivot rays in paars, vanuit purper draaipunten, doorlopend rechts
- U/D/R labels (Layer 3) met per-TF tolerance — NOG TE FIXEN
