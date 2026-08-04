---
type: task
created: 2026-05-31
assignee: Hermes
priority: high
status: pending
---

# STAP T — V1 en V2 strategie in testbot

## Doel

V1 en V2 live-strategie logica overzetten naar de testbot als Strategy-implementaties.
Daarna kunnen we alle strategieën eerlijk vergelijken via dezelfde backtest-rails.

## Bronbestanden (live tradebot — LEES ONLY, geen aanpassingen)

```
/mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/projects/crypto-tradebot/scripts/strategies/v1_strategy.py
/mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/projects/crypto-tradebot/scripts/strategies/v2_strategy.py
```

## Referentie implementatie (hoe het moet)

Kijk naar V3A als template:
```
src/crypto_test_bot_v3/strategies/v3a/config.py    ← parameters
src/crypto_test_bot_v3/strategies/v3a/logic.py     ← pure logica
src/crypto_test_bot_v3/strategies/v3a/strategy.py  ← Strategy ABC implementatie
```

## Taak: twee nieuwe strategy mappen

### V1 — `src/crypto_test_bot_v3/strategies/v1/`

**Logica (uit v1_strategy.py):**
- `_is_bearish_structure(c4h)` / `_is_bullish_structure(c4h)` — 4H trend
- `_has_bearish_move(c4h)` / `_has_bullish_move(c4h)` — impulse aanwezig
- `_find_swings` + `_detect_pullback` — fib zone detectie
- `_fib_label` — welke zone (forming/early/ideal/deep/trend_break)
- `_has_bearish_reversal` / `_has_bullish_reversal` — 15M trigger
- `_calc_sl_tp` — SL 2%, TP 3%, max_lateness 50%
- BTC macro filter (bull/bear threshold)

**Checks voor Strategy ABC:**
1. `trend` — 4H bearish/bullish structure + impulse
2. `fib` — fib label in allowed zone (ideal_pullback, early_pullback)
3. `lateness` — entry_lateness_pct <= 50%
4. `trigger` — bearish/bullish reversal op 15M
5. `btc_macro` (optioneel) — BTC niet in tegengestelde richting

**SL/TP:** vast 2% SL, 3% TP (uit v1_strategy.py constanten)

---

### V2 — `src/crypto_test_bot_v3/strategies/v2/`

**Logica (uit v2_strategy.py):**
- Richting-bewuste pullback — apart voor long en short
- Confirm type detectie (bullish_engulfing, bearish_body, etc.)
- Entry lateness check
- SL/TP berekening

**Checks voor Strategy ABC:**
1. `trend` — 4H richting
2. `pullback` — pullback aanwezig + fib zone
3. `confirm` — confirm type (engulfing, body, etc.)
4. `lateness` — entry_lateness_pct <= 50%

**SL/TP:** conform v2_strategy.py logica

---

## Wat Hermes NIET mag doen

- Geen aanpassingen aan de live strategy bestanden
- Geen nieuwe logica uitvinden — kopieer en wrap de bestaande functies
- Geen aanpassingen aan runner.py, reader.py of domain/models.py

## Tests vereist

`tests/unit/test_v1_strategy.py` en `tests/unit/test_v2_strategy.py`

Per strategie minimaal:
```python
def test_v1_compute_checks_returns_all_keys():
    # met mock candle data — checks dict heeft trend, fib, lateness, trigger

def test_v1_no_signal_without_trend():
    # als trend check faalt → geen signal

def test_v2_compute_checks_returns_all_keys():
    ...
```

## Verificatie

```bash
python -m pytest tests/ -q   # alle bestaande tests + nieuwe groen

# Smoke test
python3 -c "
from crypto_test_bot_v3.strategies.v1.strategy import V1Strategy
from crypto_test_bot_v3.strategies.v2.strategy import V2Strategy
from crypto_test_bot_v3.infrastructure.reader import BacktestReader
from crypto_test_bot_v3.runner import Runner
import tempfile
from pathlib import Path

for StratCls, name in [(V1Strategy, 'v1'), (V2Strategy, 'v2')]:
    reader = BacktestReader()
    strategy = StratCls({})
    with tempfile.NamedTemporaryFile(suffix='.jsonl', delete=False) as tf:
        jp = Path(tf.name)
    runner = Runner('ADAEUR', strategy, name, reader, jp)
    report = runner.run()
    print(f'{name}: {report[\"total_trades\"]} trades, WR {report[\"winrate_pct\"]}%')
    jp.unlink(missing_ok=True)
"
```

## Resultaat wegschrijven

`tasks/done/STAP-T-result.md`

Vermeld per strategie: trades, WR%, PnL% op ADAEUR en LINKEUR (2 jaar data).
