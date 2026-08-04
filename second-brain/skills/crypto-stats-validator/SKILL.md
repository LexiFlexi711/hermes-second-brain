# Crypto Stats Validator

## Superpower 5 — Statistische validatie

Valideer of backtest-resultaten statistisch betekenisvol zijn.

## Wat deze skill doet

Read-only. Lees backtest JSON output en beoordeel statistische kwaliteit.

Voor elk resultaat in `logs/research/`:
1. **Sample grootte**: zijn er minstens 30 trades? (minimum voor statistiek)
2. **Win rate betrouwbaarheid**: bereken 95% confidence interval op WR%
3. **Profit Factor**: total_wins / total_losses — moet > 1.0 zijn
4. **Max drawdown streak**: hoeveel opeenvolgende verliezen?
5. **Sharpe-achtige ratio**: gem_pnl / std_pnl (handmatig berekend)
6. **Overfitting gevaar**: zijn er te veel parameters t.o.v. het aantal trades?

## Output formaat

```
STATISTISCHE VALIDATIE — V2/ADAEUR (2 jaar)

Trades:           410  ✓ (>30)
WR%:             43.0% ± 4.8% (95% CI: 38.2%–47.8%)
Profit Factor:    1.24  ✓ (>1.0)
Max verliesreeks: 8     ⚠ (hoog)
Sharpe proxy:     0.31  (gem 0.24% / std 0.78%)
Overfitting:      OK — 5 params op 410 trades

OORDEEL: Statistisch valide maar grensgevallen aanwezig.
```

## Paden

```
Research results: projects/crypto-test-bot-v3/logs/research/
```

## Regels

- Geen resultaten aanpassen
- Geen nieuwe backtests draaien
- Als minder dan 30 trades: "onvoldoende data"
- Toon altijd confidence intervals bij WR%
- **Rapporteer resultaat naar `second-brain/tasks/done/` als Lexi vraagt om een audit**