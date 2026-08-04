---
stap: G
naam: backtest-paper-koppeling
status: done
uitgevoerd-door: Hermes
datum: 2026-05-29
---

## Wat gedaan

Runner class aangemaakt in `runner.py` — draait backtest én paper via dezelfde Strategy code.

- `Runner.backtest()` factory met BacktestReader
- `Runner.paper()` factory met LiveReader  
- Event-driven loop: chronologisch door 15M candles, 4H slice zonder lookahead
- TP/SL monitoring met trailing SL
- Open positie aan einde wordt geforceerd gesloten
- `compute_report()` uit reporting.metrics voor samenvatting
- Journal logt OPEN + REJECT beslissingen

## Fix in strategy.py (STAP-E spec was foutief)

`calc_sl_tp()` in logic.py heeft een andere signature dan de STAP-E spec:
- Heeft 6 verplichte args: `(entry, direction, swing_high, swing_low, pivot_high, pivot_low)`
- Retourneert 4 waarden: `(sl, tp, sl_pct, tp_pct)`

`find_pivots()` geïmporteerd en gebruikt om `swing_high`/`swing_low` te halen.

## Testresultaat

```bash
Backtest OK — 3 trades, 2 gesloten
Rapport keys OK
Journal OK — 640 entries: OPEN=3 REJECT=637
Paper runner OK — source=LiveReader
Alle Runner tests OK
```

Bestaande tests: 9 passed in 0.93s ✅

## Aangeraakte bestanden
- NIEUW: `runner.py` ✅
- GEPATCHT: `strategies/v3a/strategy.py` — calc_sl_tp signature gefixt + find_pivots toegevoegd ✅
- GEEN andere bestaande bestanden gewijzigd ✅