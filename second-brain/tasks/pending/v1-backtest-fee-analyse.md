---
task_id: v1-backtest-fee-analyse
aangemaakt: 2026-05-31
aangevraagd_door: Claude
prioriteit: hoog
---

# Taak: V1 backtest — winstbaar na fees?

## Context

V1 trader (pullback_trader.py) draait live op de server (paper trading).
Lexi wil weten of V1 winstbaar is na fees, voor ze live gaat.

Fee drempel:
- Kraken: 0.72% round-trip → min. 0.36% winst per trade nodig
- Binance: 0.15% round-trip → min. 0.075% winst per trade nodig

## Wat Hermes moet doen

1. Lees `logs/pullback_trades.jsonl` in:
   `/mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/projects/crypto-tradebot/logs/pullback_trades.jsonl`

2. Bereken per trade:
   - pnl_pct
   - outcome (WIN/LOSS)

3. Bereken totaal:
   - Aantal trades
   - Winrate %
   - Gemiddelde pnl_pct per trade
   - Totale pnl_pct
   - Aantal trades boven 0.36% (Kraken drempel)
   - Aantal trades boven 0.075% (Binance drempel)

4. Conclusie: is V1 winstbaar na fees op Kraken? Op Binance?

## Output

Sla resultaat op in:
`/mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/second-brain/tasks/done/v1-backtest-fee-analyse-resultaat.md`

Kort rapport, feiten alleen, geen strategie-advies.
