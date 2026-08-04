# Layer 3 Label Audit — 12 Juni 2026

## Probleem
D/U/R labels tonen te veel R (63-82% van segmenten) omdat de tolerance te hoog is.

## Oorzaak
Enkel de tolerance-waarden in `layer3_label.py` → `label_segments()`. De logica gebruikt alleen purper line punten — geen S/R, zones, touches. Dat is correct, maar de drempel is te hoog.

## Huidige vs Voorgestelde Tolerance

| TF | Huidig | Voorgesteld | Huidige R% |
|----|--------|-------------|------------|
| 240m | 1.8% | 0.5% | 63% |
| 60m | 1.0% | 0.3% | 70% |
| 15m | 0.55% | 0.12% | 82% |
| 5m | 0.25% | 0.06% | 71% |

## Voorbeelden van Foute R's
- 240m: +823pt stijging (1.25%) = R ipv U
- 60m: +518pt stijging (0.97%) = R ipv U  
- 5m: -161pt daling (0.29%) = R ipv D

## Actie
Tolerance verlagen per TF. Eerst basis correct, dan range/chop detectie toevoegen.
