# PULLBACK_BOUNCE_V0 Backtest — 6 Juni 2026
**Resultaat: NIET tradebaar** — negatieve expectancy op alle 3 pairs.

## Setup
PULLBACK_BOUNCE_V0 = best_geometry("down") + price_position ≤ 0.40 + last50_net_move < 0
TF: 1H, fees 0.30% round-trip, 4 exit varianten (3%/1%/12b, 3%/1.5%/24b, 4%/1.5%/24b, 3%/ATR/24b)

## Resultaten per pair
- ADAEUR (66k candles, 2018-2026): 12,678 trades, expectancy -0.30% tot -0.36%, 0/9 jaar +.
- ETHEUR (93k candles, 2015-2026): 14,672 trades, expectancy -0.27% tot -0.35%, 1/12 jaar + (2015: +15%).
- XBTEUR (100k candles, 2015-2026): 13,920 trades, expectancy -0.30% tot -0.33%, 0/12 jaar +.

## Conclusie
Setup detecteert wel pullbacks, maar bounce-kwaliteit onvoldoende. Median MAE > median MFE in alle varianten — downside domineert. Geen regime edge. Hypothese verworpen.

## Rapport
Zie /mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/projects/hermes-v01/research/pullback_bounce_backtest.py