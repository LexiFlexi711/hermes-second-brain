# STAP I — V3A Parameter vergelijkingsscript (nieuwe runner)

## Wat al bestaat (niet aanraken)

- `config/strategy_profiles/v3a_profiles.json` ✓ — baseline/loose/strict/fib_strict/rr_strict
- `src/crypto_test_bot_v3/research/compare/v3a_param_compare.py` ✓ — maar gebruikt OUDE backtest_pair

## Wat gebouwd moet worden

Nieuw script dat dezelfde profielen gebruikt maar via de NIEUWE runner (`Runner.backtest()`).
Het oude script NIET aanpassen — nieuw bestand schrijven.

## Doel

Maak loose/strict config varianten voor V3A en een script dat baseline/loose/strict naast elkaar runt en vergelijkt.

## Project pad

```
/mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/projects/crypto-test-bot-v3/
```

## Bestand 1: `config/v3a_loose.json` (als nog niet bestaat)

Profielen staan al in `config/strategy_profiles/v3a_profiles.json`. Gebruik die als bron.
Loose/strict values overnemen van daaruit.

## Bestand (OVERGESLAGEN): `config/v3a_loose.json`

Loose = minder strenge eisen, meer trades verwacht.

```json
{
  "min_fib_pct": 30.0,
  "max_fib_pct": 85.0,
  "min_pullback_candles": 3,
  "counter_window": 15,
  "extreme_lookback": 25,
  "near_extreme_pct": 0.008,
  "wick_body_ratio": 1.2,
  "min_rr": 1.0,
  "max_sl_pct": 5.0
}
```

## Bestand 2: `config/v3a_strict.json`

Strict = hogere eisen, minder maar betere trades verwacht.

```json
{
  "min_fib_pct": 38.2,
  "max_fib_pct": 65.0,
  "min_pullback_candles": 6,
  "counter_window": 10,
  "extreme_lookback": 15,
  "near_extreme_pct": 0.003,
  "wick_body_ratio": 2.0,
  "min_rr": 2.0,
  "max_sl_pct": 3.0
}
```

## Bestand 3: `scripts/run_param_compare.py`

Script dat voor een gegeven pair alle 3 varianten draait en een vergelijkingstabel print.

### Interface

```bash
python3 scripts/run_param_compare.py --pair XBTEUR --from 2022-01-01 --to 2025-12-31
python3 scripts/run_param_compare.py --pair ADAEUR
```

### Vereiste imports (zijn beschikbaar via `sys.path.insert(0, 'src')`)

```python
from crypto_test_bot_v3.strategies.v3a.strategy import V3AStrategy
from crypto_test_bot_v3.runner import Runner
from pathlib import Path
import json, argparse
from datetime import datetime, timezone
```

### Logica

1. Laad params uit `config/v3a_baseline.json` (maak dit ook aan, kopie van huidige defaults)
2. Laad params uit `config/v3a_loose.json`
3. Laad params uit `config/v3a_strict.json`
4. Run `Runner.backtest(pair, V3AStrategy(params), variant=naam, ts_from=..., ts_to=...)` voor elk
5. Print vergelijkingstabel:

```
=== PARAM VERGELIJKING  XBTEUR  2022-2025 ===
variant    trades   WR      avg_win  avg_loss  PnL      PF     streak
baseline     102  17.6%    +3.97%   -0.45%  +33.42%  1.879      16
loose        ???  ???%     +?.??%   -?.??%  +??.??%  ?.???      ??
strict       ???  ???%     +?.??%   -?.??%  +??.??%  ?.???      ??
```

6. Sla resultaten op als `logs/param_compare/PAIR_compare.json`

### Bestand 4: `config/v3a_baseline.json`

De baseline defaults uit `src/crypto_test_bot_v3/strategies/v3a/config.py`:

```json
{
  "min_fib_pct": 38.2,
  "max_fib_pct": 78.6,
  "min_pullback_candles": 4,
  "counter_window": 12,
  "extreme_lookback": 20,
  "near_extreme_pct": 0.005,
  "wick_body_ratio": 1.5,
  "min_rr": 1.5,
  "max_sl_pct": 4.0
}
```

## Verificatie

```bash
cd /mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/projects/crypto-test-bot-v3
python3 scripts/run_param_compare.py --pair XBTEUR --from 2022-01-01 --to 2025-12-31
```

Verwacht: tabel met 3 rijen, geen errors, JSON opgeslagen.

## Resultaat schrijven

Schrijf resultaat naar:
`/home/sjoe/system/hermes-second-brain/second-brain/tasks/done/STAP-I-result.md`
