# Crypto Cost Analyzer

## Superpower 6 — Slippage, spread & fees begrijpen

Bereken de echte kostprijs van een strategie na spread, fees en slippage.

## Wat deze skill doet

Read-only. Berekent impact van handelskosten op backtest-resultaten.

1. Lees spread% per pair uit de universe watchlist
2. Schat Kraken taker fee (0.26% per kant = 0.52% round-trip)
3. Schat slippage (0.1% per kant als conservatieve schatting voor Kraken spot)
4. Bereken totale kostprijs per round-trip trade:
   - Spread impact: spread% / 2 in + spread% / 2 out
   - Fees: 0.26% in + 0.26% out
   - Slippage: 0.1% in + 0.1% out
5. Vergelijk met gem. PnL per trade uit backtest
6. Toon: hoeveel trades zijn winstgevend na kosten?

## Output formaat

```
KOSTPRIJSANALYSE — V2/ADAEUR

Spread ADAEUR:       0.003% (Kraken live)
Kraken taker fee:    0.260% per kant
Geschatte slippage:  0.100% per kant
──────────────────────────────────────
Totaal round-trip:   0.726%

Backtest gem. PnL:   +0.59% per trade
Na kosten:           +0.59% - 0.73% = -0.14% per trade ⚠

CONCLUSIE: Strategie is marginaal negatief na kosten.
Breakeven PnL nodig: minstens +0.73% per trade.
```

## Paden

```
Watchlist (spread): projects/crypto-data/logs/universe_watchlist.json
Research results:   projects/crypto-test-bot-v3/logs/research/
```

## Regels

- Geen echte orders plaatsen
- Gebruik live spread uit watchlist, niet geschatte waarden
- Toon altijd de aannames expliciet
- Geen claims over winstgevendheid
- **Rapporteer resultaat naar `second-brain/tasks/done/` als Lexi vraagt om een audit**