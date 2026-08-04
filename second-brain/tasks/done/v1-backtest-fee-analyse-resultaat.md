---
type: synthesis
task_id: v1-backtest-fee-analyse
aangemaakt: 2026-05-31
uitgevoerd: 2026-05-31
agent: Noa (Hermes)
bron: pullback_trades.jsonl (27 trades)
---

# V1 Backtest — Fee Analyse

## Resultaten

| Metric | Waarde |
|--------|--------|
| Trades | 27 |
| Winrate | **14.8%** (4/27) |
| Totale PnL | **-25.08%** (-25.08 EUR) |
| Gem. PnL per trade | -0.93% |
| Gem. win | +2.74% |
| Gem. loss | -1.57% |
| Beste trade | BCHEUR short +6.08% |
| Slechtste trade | -2.00% (meerdere) |

## Fee Impact

| Exchange | Round-trip fee | Netto PnL | Oordeel |
|----------|---------------|-----------|---------|
| **Kraken** | 0.36%/trade | **-34.80%** | ❌ Niet winstbaar |
| **Binance** | 0.075%/trade | **-27.11%** | ❌ Niet winstbaar |

## Per Pair

| Pair | Trades | WR | PnL |
|------|--------|----|-----|
| BCHEUR | 2 | 50% | +6.08% |
| ZECEUR | 1 | 100% | +1.00% |
| UAIEUR | 3 | 33% | -1.16% |
| XRPEUR | 4 | 25% | -0.96% |
| SOLEUR | 1 | 0% | -1.01% |
| ETHEUR | 2 | 0% | -3.03% |
| Overige (11 pairs) | 1-2 elk | 0% | -2.00% elk |

## Conclusie

**V1 is niet winstbaar, met of zonder fees.** De winrate van 14.8% is te laag om break-even te draaien. Zelfs op Binance met 0.075% fees blijft V1 -27% in het rood. Het probleem is niet de fee — het is de strategie.

Bron data: `/mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/projects/crypto-tradebot/logs/pullback_trades.jsonl`