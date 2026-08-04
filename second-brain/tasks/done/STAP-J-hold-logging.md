# STAP J — Per-candle HOLD logging in runner (snapshot audit trail)

## Doel

Uitbreiden van de runner zodat elke candle terwijl een trade open staat wordt gelogd als HOLD-event met MFE/MAE bijgehouden. Dit maakt snapshot-based audit mogelijk.

## Project pad

```
/mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/projects/crypto-test-bot-v3/
```

## Aan te passen bestand: `src/crypto_test_bot_v3/runner.py`

### Huidige situatie

De runner logt alleen bij OPEN en CLOSE. Terwijl een trade open staat wordt niets gelogd.

### Gewenste toevoeging

In de runner-loop, na het monitoren van de open positie maar vóór het signaal evalueren:
als een positie OPEN is EN er geen exit plaatsvindt op deze candle → log een HOLD event.

### HOLD event structuur (toe te voegen aan journal)

```python
hold_event = {
    "type":        "HOLD",
    "ts":          ts,                    # candle timestamp
    "pair":        self.pair,
    "entry_ts":    open_pos["ts"],
    "entry_price": open_pos["entry"],
    "direction":   open_pos["direction"],
    "current_close": candle["close"],
    "current_high":  candle["high"],
    "current_low":   candle["low"],
    "sl":          open_pos["sl"],
    "tp":          open_pos["tp"],
    "trail_sl":    open_pos.get("trail_sl"),
    "pnl_pct":     pnl_now,              # zie berekening hieronder
    "mfe_pct":     open_pos["mfe_pct"],  # max favorable excursion
    "mae_pct":     open_pos["mae_pct"],  # max adverse excursion
}
```

### MFE/MAE bijhouden in open_pos

Bij het aanmaken van open_pos toevoegen:
```python
open_pos = {
    ...bestaande velden...,
    "mfe_pct": 0.0,
    "mae_pct": 0.0,
}
```

Bij elke candle update (in het monitor-blok):
```python
# pnl van dit moment
if d == "long":
    pnl_now = (candle["high"] - entry) / entry * 100   # best case this candle
    pnl_low = (candle["low"]  - entry) / entry * 100   # worst case this candle
else:
    pnl_now = (entry - candle["low"])  / entry * 100
    pnl_low = (entry - candle["high"]) / entry * 100

open_pos["mfe_pct"] = max(open_pos["mfe_pct"], pnl_now)
open_pos["mae_pct"] = min(open_pos["mae_pct"], pnl_low)
```

### Waar HOLD te loggen

In runner.py, na het monitor-blok (na de `if outcome:` check) en vóór het signaal-blok:

```python
# Log HOLD als positie nog open is na deze candle
if open_pos is not None:
    self._log_hold(open_pos, candle, ts)
```

Nieuwe methode in Runner class:
```python
def _log_hold(self, open_pos: dict, candle: dict, ts: int) -> None:
    d = open_pos["direction"]
    entry = open_pos["entry"]
    close = candle["close"]
    pnl_now = (close - entry)/entry*100 if d == "long" else (entry - close)/entry*100
    self.journal._append({
        "type":          "HOLD",
        "ts":            ts,
        "pair":          self.pair,
        "entry_ts":      open_pos["ts"],
        "entry_price":   entry,
        "direction":     d,
        "current_close": close,
        "current_high":  candle["high"],
        "current_low":   candle["low"],
        "sl":            open_pos["sl"],
        "tp":            open_pos["tp"],
        "trail_sl":      open_pos.get("trail_sl"),
        "pnl_pct":       round(pnl_now, 4),
        "mfe_pct":       round(open_pos["mfe_pct"], 4),
        "mae_pct":       round(open_pos["mae_pct"], 4),
    })
```

## Journal aanpassing

`src/crypto_test_bot_v3/trader/journal.py` — `_append` is al een publieke methode? Controleer dit.
Als `_append` private is (underscore), mag de runner hem direct aanroepen (zelfde package).

## Verificatie

```bash
cd /mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/projects/crypto-test-bot-v3
python3 -c "
import sys; sys.path.insert(0, 'src')
from crypto_test_bot_v3.strategies.v3a.strategy import V3AStrategy
from crypto_test_bot_v3.strategies.v3a.config import *
from crypto_test_bot_v3.runner import Runner
from pathlib import Path
from datetime import datetime, timezone
import json

params = {
    'min_fib_pct': MIN_FIB_PCT, 'max_fib_pct': MAX_FIB_PCT,
    'min_pullback_candles': MIN_PULLBACK_CANDLES,
    'counter_window': DEFAULT_COUNTER_WINDOW, 'extreme_lookback': DEFAULT_EXTREME_LOOKBACK,
    'near_extreme_pct': DEFAULT_NEAR_EXTREME_PCT, 'wick_body_ratio': DEFAULT_WICK_BODY_RATIO,
    'min_rr': DEFAULT_MIN_RR, 'max_sl_pct': MAX_SL_PCT,
}
ts_from = int(datetime(2024, 1, 1, tzinfo=timezone.utc).timestamp())
ts_to   = int(datetime(2024, 6, 30, tzinfo=timezone.utc).timestamp())
journal_path = Path('/tmp/test_hold.jsonl')
runner = Runner.backtest('XBTEUR', V3AStrategy(params), variant='baseline',
                          ts_from=ts_from, ts_to=ts_to, journal_path=journal_path)
runner.run()
lines = journal_path.read_text().splitlines()
holds = [l for l in lines if '\"HOLD\"' in l]
opens = [l for l in lines if '\"OPEN\"' in l]
print(f'OPEN: {len(opens)}, HOLD events: {len(holds)}')
if holds:
    h = json.loads(holds[0])
    print(f'Eerste HOLD: mfe={h[\"mfe_pct\"]}% mae={h[\"mae_pct\"]}%')
"
```

Verwacht: HOLD events aanwezig, mfe/mae ingevuld.

## Tests

Bestaande tests mogen NIET breken. Controleer:
```bash
python3 -m pytest tests/ -q
```

Verwacht: 41 passed.

## Resultaat schrijven

Schrijf resultaat naar:
`/home/sjoe/system/hermes-second-brain/second-brain/tasks/done/STAP-J-result.md`
