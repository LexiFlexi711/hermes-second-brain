---
type: fix
date: 2026-05-31
agent: Noa (Hermes)
title: V1 Backtest — Fee Analyse
---

# V1 Backtest — Fee Analyse

## Resultaat

V1 pullback trader is **niet winstbaar**, met of zonder fees.

| Metric | Waarde |
|--------|--------|
| Trades | 27 |
| Winrate | **14.8%** (4/27) |
| Totale PnL | **-25.08%** (-25.08 EUR) |
| Netto na Kraken (0.36%/trade) | **-34.80%** |
| Netto na Binance (0.075%/trade) | **-27.11%** |

Het probleem is niet de fee — het is de strategie. 17/27 trades raakten stop loss op exact -2.00%.

Bron: `tasks/done/v1-backtest-fee-analyse-resultaat.md`