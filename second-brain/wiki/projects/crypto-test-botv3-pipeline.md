---
title: Crypto Test Bot V3 — Scripts en Pipeline
type: project
created: 2026-05-30
updated: 2026-05-30
status: active
---

# Crypto Test Bot V3 — Scripts en Pipeline

Project: `crypto-test-bot-v3` — modulair systeem om strategieën te testen via backtest.
Pad: `/mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/projects/crypto-test-bot-v3/`
Opstarten: via `run.py` in de projectroot.

---

## Centrale launcher

```
python run.py                    toont het menu met alle commando's

python run.py tests              alle unit + integratietests
python run.py tests-unit         alleen unit tests
python run.py tests-integ        alleen integratietests

python run.py multi              multi-pair backtest: 7 pairs × 3 varianten
python run.py multi --pairs ADAEUR LINKEUR
python run.py multi --verbose

python run.py grid               grid search: alle parametercombo's, gerankt op WR%
python run.py grid --pairs ADAEUR LINKEUR --top 20
python run.py grid --grid config/grid_v3a.json

python run.py rapport            kandidaatbeoordeling op basis van laatste multi-pair run

python run.py signal-pre         reverse signaalanalyse: welke checks waren actief
python run.py signal-pre --pairs ADAEUR     VOOR een WIN-trade (leading indicators)
python run.py signal-pre --lookback 10
```

---

## Data-stroom

```
HISTORISCHE DATA (crypto-data project)
    │
    ├── logs/historical_csv/PAIREUR_NNm.csv   2015 → maart 2026 (29.4M candles)
    └── ohlc_archive/PAIREUR_NNm.jsonl        recente candles (rolling)
    │
    ▼
BacktestReader                               leest beide bronnen, mergt op timestamp
    │                                        geen lookahead — filtert op ts_to
    ▼
Runner.backtest()                            event-driven loop over 15M candles
    │  - voor elke candle: check signaal via strategy
    │  - fill op open van volgende candle
    │  - bewaakt SL/TP/trailing stop
    │  - logt elke beslissing naar journal
    ▼
Journal (logs/journal_PAIR_variant.jsonl)    elke OPEN + REJECT + HOLD met checks + context
    │
    ▼
compute_report()                             WR%, PnL%, avg win/loss, max streak, open
```

---

## Scripts — wat doet wat

### Research (analyse)

| Script | Commando | Wat |
|---|---|---|
| `research/compare/v3a_multi_pair.py` | `run.py multi` | 7 pairs × 3 varianten, stabiliteitsmatrix |
| `research/compare/v3a_grid_search.py` | `run.py grid` | alle parametercombo's via itertools.product |
| `research/v3a_kandidaat_rapport.py` | `run.py rapport` | kandidaatbeoordeling op 4 criteria |
| `research/signal_pre_analysis.py` | `run.py signal-pre` | welke checks rijpen VOOR een WIN-trade |
| `research/compare/paper_vs_backtest.py` | — | vergelijkt paper vs backtest signalen |

### Strategie

| Bestand | Wat |
|---|---|
| `strategies/v3a/logic.py` | pure functies: trend, pullback, fib, trigger, SL/TP |
| `strategies/v3a/strategy.py` | V3AStrategy — compute_checks() + build_signal() |
| `strategies/v3a/config.py` | alle defaults als constanten |
| `strategies/aggregator.py` | gate/score/mixed mode via config |

### Config (parameters)

| Bestand | Wat |
|---|---|
| `config/v3a_baseline.json` | exacte defaults |
| `config/v3a_loose.json` | ruimere parameters, meer trades |
| `config/v3a_strict.json` | strengere parameters, minder maar betere trades |
| `config/grid_v3a.json` | grid spec voor grid search (zelf aanmaken) |

Alle parameters zijn meegegeven als args/kwargs — niets is hardcoded.
Volledige lijst: fib_min/max, min_pullback, counter_window, extreme_lookback,
near_extreme_pct, wick_body_ratio, min_rr, max_sl_pct, trail_pct,
pivot_n, pivot_lookback, sma_fast, sma_slow, sma_long_window, sma_threshold,
sl_buffer_pct, tp_buffer_pct, n_4h, n_15m.

### Infrastructure

| Bestand | Wat |
|---|---|
| `infrastructure/reader.py` | BacktestReader + LiveReader (DataReader ABC) |
| `infrastructure/paths.py` | padresolutie: zoekt ohlc_archive + historical_csv |
| `runner.py` | Runner.backtest() + Runner.paper() |
| `trader/journal.py` | schrijft OPEN/REJECT/HOLD/CANCEL naar JSONL |
| `trader/trader.py` | accept/reject beslissing + positiebeheer |
| `reporting/metrics.py` | compute_report() |

---

## Output bestanden

| Bestand | Wat |
|---|---|
| `logs/journal_PAIR_VARIANT_backtest.jsonl` | elke trade + alle checks + candle context |
| `logs/backtest_multirun_v2/` | journals van eerdere multi-pair runs |
| `logs/research/v3a_multi_pair_DATUM.json` | ruwe resultaten multi-pair |
| `logs/research/v3a_grid_search_DATUM.json` | grid search resultaten |

---

## Status (2026-05-30)

**V3A — NIET KLAAR** (STAP S resultaat)
- 0/7 pairs haalt ≥ 40% WR (beste: ADAEUR 34.5%)
- Parameterstabiliteit: gem. spread 13.5% — stabiel
- Beste pairs: ADAEUR (+25.3% PnL), LINKEUR (+27.1% PnL)

**Volgende stappen:**
1. Grid search draaien → parameters vinden die WR over 40% tillen
2. signal-pre uitbreiden → leading indicators identificeren
3. V3A kandidaat maken op basis van grid search resultaten

---

## Kern-interfaces (VAST — niet wijzigen zonder review)

```python
CheckResult(name, ok, value, why)
Signal(direction, entry, sl, tp, checks, context)
DataReader.get_candles(pair, interval, n) → list[dict]
Strategy.compute_checks(data) → dict[str, CheckResult]
Aggregator(config).should_signal(checks) → (bool, str)
Journal.log_open / log_reject / fill_outcome
Runner.backtest() / Runner.paper()
```

---

## Zie ook

- [[crypto-data-pipeline]] — bron van historische en live candles
- [[crypto-tradebot]] — productie-bot, V3A wordt hier uiteindelijk ingezet
- [[pullback-trader-strategy]] — V3A logica achtergrond
