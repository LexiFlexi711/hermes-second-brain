# Strategy MA Cross V1 — Sessie 4 juni 2026

## Wat gedaan
- `strategy_ma_cross_v1.py` gebouwd op EMA9/EMA21 cross, ADAEUR 15M, IS 2022-01-14 t/m 2024-12-05
- Backtest draait in `/mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/projects/hermes-v01/research/`

## Wijzigingen aan hermes_v02.py
1. **Confidence saturation fix** — `_richting_scores()`: `s = min(g, 1.0)` → `s = g / (1.0 + g)` — nooit meer 1.0, echte gradient
2. **3+ touches guard** — `channel_down()`: `if upper_touches < 3: return None` — minder valse channels

## Strategy filters (in volgorde)
1. trending_down + confidence ≥ 0.50
2. RSI: SHORT > 60, LONG < 40
3. S/R proximity: SHORT r1 binnen 1.5×ATR, LONG s1 binnen 1.5×ATR

## Huidige status
RSI filter is te restrictief — EMA crosses gebeuren in neutrale RSI (40-60). 0 entries in eerste 2000 IS-bars. Moet RSI drempels verruimen of filter verwijderen.

## Bestand
`/mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/projects/hermes-v01/research/strategy_ma_cross_v1.py`