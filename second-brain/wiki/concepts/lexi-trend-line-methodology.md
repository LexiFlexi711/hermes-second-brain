# Lexi Trend Line Methodology

## Definities
- **Lexi Trend Line:** paarse lijn (#9C27B0) door gemiddelde van body high/low van ALLE fractal candles
- **Body prices gebruiken** — NOOIT wicks voor trendlijnen
- **Wicks** mogen gebruikt worden voor swing markers (^ / v)

### Lijnen
1. 🟣 **Paarse lijn** — trend line (body average van fractals)
2. ➖ **Grijze lijnen** — S/R zones (dikker bij meer touches/score)
3. 🟢 **Fluro groene lijnen** — trend pivot punten (kort, gestippeld)
4. 🟣 **Paarse stippellijnen** — pivot rays vanuit purper draaipunten (doorlopend rechts)

### Labels (Layer 3 — NOG TE CORRIGEREN)
- **U** = up/stijgend segment (purper lijn stijgt)
- **D** = down/dalend segment (purper lijn daalt)
- **R** = range (purper lijn blijft vlak)
- Tolerance per TF moet lager:
  - 240m: ~0.5%
  - 60m: ~0.3%
  - 15m: ~0.12%
  - 5m: ~0.06%

## Regels
1. Van LINKS naar RECHTS lezen
2. Lijn volgt de dominante prijsrichting via belangrijke draaipunten
3. Bij daling: lijn omlaag (D)
4. Bij herstel: lijn omhoog (U)  
5. Bij range: lijn horizontaal/zijwaarts (R)
6. Bij nieuwe draai: lijn knikt naar de nieuwe richting
7. Forceer NOOIT — None is ok

## Referentie Voorbeelden
- `verify-charts-human/btc-10h28.jpg` — Lexi's handmatige trendlijnen
- `verify-charts-human/btc-11h23.jpg` — Paarse correcties

## Layer 2 v02 Blokken
- `trendline_block.py` — enkel paarse lijn
- `sr_block.py` — horizontale S/R levels
- `zone_block.py` — paarse pivot rays
- `marker_block.py` — swing markers
- `pivot_utils.py` — gedeelde pivot detectie
- `layer3_label.py` — U/D/R labels (NOG TE FIXEN)
