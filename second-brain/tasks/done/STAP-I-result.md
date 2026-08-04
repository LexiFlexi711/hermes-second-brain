---
type: report
created: 2026-05-29
source: Hermes (STAP-I uitvoering)
status: done
---

# STAP I — V3A Parameter Varianten + Vergelijkingsscript

## Uitgevoerd door
Hermes (Noa) — op aanwijzing van Lexi, taak uit `tasks/pending/STAP-I-param-varianten.md`

## Gemaakt

| Bestand | Pad |
|---------|-----|
| Config baseline | `config/v3a_baseline.json` |
| Config loose | `config/v3a_loose.json` |
| Config strict | `config/v3a_strict.json` |
| Compare script (Runner) | `scripts/run_param_compare.py` |

## Parameter keys
Gebruikte keys komen overeen met wat V3AStrategy verwacht:
`fib_min`, `fib_max`, `min_pullback`, `counter_window`, `extreme_lookback`,
`near_extreme_pct`, `wick_body_ratio`, `min_rr`, `max_sl_pct`

(Anders dan de task spec die `min_fib_pct`/`max_fib_pct`/`min_pullback_candles` vermeldde — die keys bestaan niet in de strategy.)

## Verificatie ETHEUR (Mei 2025)

| Variant | Trades | WR% | Total% | AvgTr% | MaxL |
|---------|--------|-----|--------|--------|------|
| loose   | 8      | 57.1| +1.49% | +0.21% | 3    |
| baseline| 4      | 50.0| +0.10% | +0.03% | 2    |
| strict  | 2      | 0.0 | -6.00% | -3.00% | 2    |

## Conclusie
- **Loose** presteert best op deze korte periode (mei 2025): 8 trades, +1.49%
- **Strict** is te streng: maar 2 trades, allebei verlies
- Script werkt met `Runner.backtest()` + `V3AStrategy(params)` zoals bedoeld
- Output JSON staat in `logs/param_compare/PAIR_compare_runner.json`

## Nota
Er bestaat ook een **oude** `v3a-compare` CLI (in scripts/ en cli/v3a_compare_cli.py) die een andere backtest gebruikt (backtesting/v3a_backtest.py) met hardcoded varianten. Die is blijven staan — niet vervangen.