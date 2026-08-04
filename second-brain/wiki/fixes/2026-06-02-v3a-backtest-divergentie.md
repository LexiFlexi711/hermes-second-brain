# V3A Divergentie: backtest_pair vs Runner+V3AStrategy

**Datum:** 2026-06-02
**Tijd:** ~10:00 UTC
**Auteur:** Claude (Director) + Hermes (executie opslag)

## Bevinding

`backtest_pair` (inline logica in v3a_backtest.py) en `Runner + V3AStrategy` (canonieke engine)
zijn **niet equivalent** — ze geven compleet verschillende resultaten op exact dezelfde data.

## Divergentiemeting (ETHEUR, 17 mei - 1 juni 2026)

| Aspect | backtest_pair | Runner + V3AStrategy |
|--------|--------------|---------------------|
| 15m candles | 1445 | 1445 |
| 4H candles | 765 | 765 |
| Trades | **9** | **0** |
| total_pnl | +5.10% | 0.00% |

## Oorzaak

`backtest_pair` detecteert signalen via directe aanroepen van
`detect_pullback_failed_v3a`, `detect_trend_direction` etc. **inline** in zijn loop.

`V3AStrategy` is een **separate herimplementatie** met een andere aggregator-flow —
trigger en fib slagen nooit gelijktijdig bij dit pair/periode.

Structureel andere engines, geen numerieke afrondingsverschillen.

## Actie

`v3a_backtest.py` is **gedepreceerd** en gemarkeerd met:

```python
"""DEPRECATED — Runner.run is de canonieke engine. Niet gebruiken voor nieuwe tooling.
Behouden voor referentie.
"""
```

## Impact

- V3A-beoordeling via `v3a_param_compare.py` draaide op `backtest_pair`
- V3A grid search draaide op `Runner`
- Resultaten zijn **niet vergelijkbaar** geweest
- Alle nieuwe V3A tooling moet op `Runner` draaien

## Bestanden die backtest_pair gebruiken

| Bestand | Gebruik |
|---------|---------|
| `cli/v3a_backtest_cli.py` | `from ... import backtest_pair` |
| `research/compare/paper_vs_backtest.py` | `from ... import backtest_pair` |
| `research/compare/v3a_param_compare.py` | `from ... import backtest_pair` |
| `tests/integration/test_v3a_compare_smoke.py` | `from ... import backtest_pair` |

## Bestandslocatie

- Depot notificatie: `src/crypto_test_bot_v3/backtesting/v3a_backtest.py`
