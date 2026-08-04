---
type: task
created: 2026-05-31
assignee: Hermes
priority: high
status: pending
depends_on: STAP-T
---

# STAP U — Multi-strategy vergelijking over alle pairs

## Context

V2 backtest op ADAEUR + LINKEUR (2 jaar data) geeft als enige strategie positieve PnL:
- V2/ADAEUR: 43.0% WR, +24.09% PnL ✓
- V2/LINKEUR: 41.7% WR, +18.79% PnL ✓

Nu willen we ALLE strategieën (V1, V2, V3A, V4) vergelijken over de top 10 pairs uit de watchlist.

## Taak: nieuw bestand

**Pad:** `src/crypto_test_bot_v3/research/compare/multi_strategy_compare.py`

## Wat het script doet

1. Draait 4 strategieën × 10 pairs via Runner + BacktestReader (2 jaar data)
2. Print een vergelijkingstabel per strategie:

```
=== STRATEGIE VERGELIJKING — 2026-05-31 (2 jaar data) ===

Strategie    Pair       Trades   WR%    PnL%    MaxStreak
---------------------------------------------------------
V1           ADAEUR       662   40.1%  -53.71%     12
V1           BTCEUR         ?      ?%      ?%       ?
...
V2           ADAEUR       410   43.0%  +24.09%      8
V2           BTCEUR         ?      ?%      ?%       ?
...
```

3. Print een samenvatting per strategie (gem. WR, gem. PnL over alle pairs):

```
=== SAMENVATTING ===
V2:   gem WR 42.3%  gem PnL +18.4%  → KANDIDAAT
V1:   gem WR 39.5%  gem PnL -72.5%  → AFGEWEZEN
V3A:  gem WR 28.1%  gem PnL -44.4%  → AFGEWEZEN
V4:   gem WR 30.4%  gem PnL -69.2%  → AFGEWEZEN
```

4. Schrijft JSON naar `logs/research/multi_strategy_compare_YYYY-MM-DD.json`

## Pairs (top 10 watchlist)

```python
PAIRS = [
    "XRPEUR", "ADAEUR", "BTCEUR", "ETHEUR", "SOLEUR",
    "LTCEUR", "HYPEEUR", "DOTEUR", "SUIEUR", "DOGEEUR",
]
```

## Strategieën

```python
from crypto_test_bot_v3.strategies.v1.strategy import V1Strategy
from crypto_test_bot_v3.strategies.v2.strategy import V2Strategy
from crypto_test_bot_v3.strategies.v3a.strategy import V3AStrategy
from crypto_test_bot_v3.strategies.v4.strategy import V4Strategy

STRATEGIES = [
    ("V1",  V1Strategy,  {}),
    ("V2",  V2Strategy,  {}),
    ("V3A", V3AStrategy, {}),
    ("V4",  V4Strategy,  {}),
]
```

## Data

```python
from datetime import datetime, timezone, timedelta
ts_from = int((datetime.now(timezone.utc) - timedelta(days=730)).timestamp())
reader = BacktestReader(ts_from=ts_from)
```

## Parallelisme

Gebruik `ProcessPoolExecutor(max_workers=4)` — één worker per strategie×pair combinatie.

## Tests vereist

`tests/integration/test_multi_strategy_compare.py`

```python
def test_multi_strategy_compare_runs():
    # 2 strategies, 2 pairs, controleer output dict
    ...

def test_output_has_required_keys():
    # elke rij heeft strategy, pair, total_trades, winrate_pct, total_pnl_pct
    ...
```

## Verificatie

```bash
python -m pytest tests/ -q  # alle tests groen
python -m crypto_test_bot_v3.research.compare.multi_strategy_compare --pairs ADAEUR LINKEUR
```

## Resultaat wegschrijven

`tasks/done/STAP-U-result.md`

Vermeld: winnende strategie per pair, gem. WR en PnL per strategie, aanbeveling.
