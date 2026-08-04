# STAP L — MFE/MAE analyse crypto-tradebot

## Doel

Analyseer alle gesloten trades per strategie en bereken per trade:
- MFE (max favorable excursion) — hoogste floating winst ooit
- MAE (max adverse excursion) — diepste dip ooit
- Wanneer de trade +1%, +2%, +3% groen stond
- Hoeveel winst teruggegeven na MFE
- Of de trade zijn MFE ooit bijna TP raakte

Dit is een analyse-only script. Geen strategie aanpassen, geen nieuwe logica.

## Project pad

```
/mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/projects/crypto-tradebot/
```

## Script pad

```
scripts/mfe_mae_analyse.py
```

## Databronnen

### Trade logs (input)

| Strategie | Bestand | Entry veld | Exit veld | Tijd velden |
|-----------|---------|-----------|-----------|-------------|
| V1 | `logs/pullback_trades.jsonl` | `entry_price` | `exit_price` | `entry_timestamp`, `close_time` |
| V2 | `logs/v2_trades.jsonl` | `entry_price` | `exit_price` | `entry_timestamp`, `close_time` |
| V3 | `logs/v3_trades.jsonl` | `entry` | `exit_price` | `entry_ts`, `close_time` |
| Momentum | `logs/momentum_trades.jsonl` | `entry` | `exit_price` | `entry_ts`, `close_time` |
| Range | `logs/range_trades.jsonl` | `entry_price` | `exit_price` | `entry_timestamp`, `close_time` |

Sla trades over waarbij `outcome == "OPEN"` (nog niet gesloten) of `exit_price` ontbreekt.

### OHLC data (voor reconstructie floating PnL)

```
/mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/projects/crypto-data/logs/ohlc_archive/{PAIR}_15m.jsonl
```

Velden per candle: `timestamp`, `open`, `high`, `low`, `close`

## Logica per trade

```python
def analyse_trade(trade: dict, candles_15m: list[dict]) -> dict:
    """
    Bereken MFE/MAE voor één trade op basis van 15m candles.
    
    candles_15m: alleen candles waar entry_ts <= timestamp <= exit_ts
    """
    entry     = trade['entry_price']  # of trade['entry']
    direction = trade['direction']    # 'long' of 'short'
    exit_price = trade['exit_price']
    sl        = trade.get('stop_loss') or trade.get('sl')
    tp        = trade.get('take_profit') or trade.get('tp')
    
    mfe_pct = 0.0   # hoogste floating winst (positief)
    mae_pct = 0.0   # diepste dip (negatief)
    reached_1pct = reached_2pct = reached_3pct = False
    mfe_ts  = None
    
    for c in candles_15m:
        if direction == 'long':
            best  = (c['high'] - entry) / entry * 100
            worst = (c['low']  - entry) / entry * 100
        else:
            best  = (entry - c['low'])  / entry * 100
            worst = (entry - c['high']) / entry * 100
        
        if best > mfe_pct:
            mfe_pct = best
            mfe_ts  = c['timestamp']
        if worst < mae_pct:
            mae_pct = worst
        
        if not reached_1pct and best >= 1.0: reached_1pct = True
        if not reached_2pct and best >= 2.0: reached_2pct = True
        if not reached_3pct and best >= 3.0: reached_3pct = True
    
    # Gerealiseerde PnL
    if direction == 'long':
        pnl_pct = (exit_price - entry) / entry * 100
    else:
        pnl_pct = (entry - exit_price) / entry * 100
    
    # TP afstand
    tp_dist_pct = None
    if tp:
        if direction == 'long':
            tp_dist_pct = (tp - entry) / entry * 100
        else:
            tp_dist_pct = (entry - tp) / entry * 100
    
    # Giveback = MFE - realized PnL (hoeveel winst teruggegeven)
    giveback_pct = mfe_pct - pnl_pct if mfe_pct > 0 else 0.0
    
    # Hoe dicht bij TP?
    pct_of_tp = (mfe_pct / tp_dist_pct * 100) if tp_dist_pct and tp_dist_pct > 0 else None
    
    return {
        'pair':          trade.get('pair'),
        'direction':     direction,
        'outcome':       trade.get('outcome'),
        'entry_price':   entry,
        'exit_price':    exit_price,
        'pnl_pct':       round(pnl_pct, 3),
        'mfe_pct':       round(mfe_pct, 3),
        'mae_pct':       round(mae_pct, 3),
        'giveback_pct':  round(giveback_pct, 3),
        'reached_1pct':  reached_1pct,
        'reached_2pct':  reached_2pct,
        'reached_3pct':  reached_3pct,
        'mfe_ts':        mfe_ts,
        'pct_of_tp':     round(pct_of_tp, 1) if pct_of_tp else None,
        'candles_in_trade': len(candles_15m),
    }
```

## Hoe OHLC candles ophalen per trade

```python
import json
from pathlib import Path

ARCHIVE = Path('/mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/projects/crypto-data/logs/ohlc_archive')

def get_candles_for_trade(pair: str, entry_ts: int, exit_ts: int) -> list[dict]:
    path = ARCHIVE / f'{pair}_15m.jsonl'
    if not path.exists():
        return []
    candles = []
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        c = json.loads(line)
        ts = int(c['timestamp'])
        if entry_ts <= ts <= exit_ts:
            candles.append(c)
    return sorted(candles, key=lambda x: x['timestamp'])
```

Let op: als `close_time` een string is (bv "2026-05-29 14:50:18"), converteer naar Unix timestamp:
```python
from datetime import datetime, timezone
exit_ts = int(datetime.strptime(close_time, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc).timestamp())
```

## Output

### 1. Console samenvatting per strategie

```
=== V3 (26 trades, 18 gesloten) ===
Trades waar MFE >= 1%:   12/18  (67%)
Trades waar MFE >= 2%:    7/18  (39%)
Trades waar MFE >= 3%:    3/18  (17%)
Gem. giveback (verliezers): 2.1%
Gem. giveback (winners):    0.8%
Verliezers die >= 1% groen stonden: 8/12 (67%)
Gem. MFE verliezers: 1.8%  |  Gem. MAE verliezers: -1.6%
```

### 2. JSON output per trade

```
logs/mfe_mae/mfe_mae_analyse.json
```

Formaat:
```json
{
  "generated_at": "2026-05-29 ...",
  "strategies": {
    "V1": { "trades": [...], "summary": {...} },
    "V2": { "trades": [...], "summary": {...} },
    ...
  }
}
```

### 3. Overzichtsbestand (markdown)

```
logs/mfe_mae/mfe_mae_rapport.md
```

Met tabel per strategie: pair, direction, outcome, MFE%, MAE%, giveback%, pnl%, reached_1/2/3pct, pct_of_tp.

## Gebruik

```bash
cd /mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/projects/crypto-tradebot
python3 scripts/mfe_mae_analyse.py
```

## Verificatie

- Minimaal 1 strategie met trades geanalyseerd
- JSON en markdown aangemaakt
- Geen errors voor trades met ontbrekende OHLC data (gewoon overslaan met warning)
- Console toont samenvatting per strategie

## Geen dependencies

Alleen Python stdlib: `json`, `pathlib`, `datetime`, `collections`.

## Resultaat schrijven

```
/home/sjoe/system/hermes-second-brain/second-brain/tasks/done/STAP-L-result.md
```
