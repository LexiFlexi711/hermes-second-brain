---
title: "DE ARCHITECT — 5 Strategievoorstellen"
type: concept
created: 2026-06-17
status: draft
area: architectuur
tags: [hermes-lagen, lookahead, data-contracts, testbot, l9-validation]
---

# DE ARCHITECT — 5 Strategievoorstellen

## Context

Bestaande architectuur op `/home/sjoe`:

| Component | Pad | Status |
|-----------|-----|--------|
| **Hermes Agent** (v0.14) | `~/.hermes/` | ✅ Actief — skills, council, cron, plugins |
| **Noa-Hermes** | `~/Noa-Hermes/` | ✅ Actief — autonome protocollen, controller |
| **Hermes layers (L1-L4)** | `projects/hermes-v01/` | ✅ L1-L4 operationeel, L6-L8 bestaan |
| **Layer 9 (Validation Lab)** | `projects/hermes-v01/layer9/` | 🚧 L9A MVP (snapshot) gebouwd |
| **Crypto test-bot v3** | `src/crypto_test_bot_v3/` | ✅ V3A strategie, V1/V2 in migratie |
| **Crypto tradebot** | `/mnt/otherdrive1/.../crypto-tradebot/` | ✅ Live — V1/V2/V3/range traders |
| **Data pipeline** | `crypto-data/` (elders) | ✅ Universe → score → select → bridge → live_cache |
| **Second brain** | `~/system/hermes-second-brain/` | ✅ Wiki, scout, cron, scripts |
| **Governance protocol** | `Noa-Hermes/autonomous/protocols/` | ✅ Actielog, kosten, no-write zonder plan |

---

## Strategie 1: Hermes Laagcontracten — Strict Interface Per Layer

### Probleem

Elke Hermes laag (L1-L8) heeft een andere oproepstijl:
- L2/L3/L4 roepen `fetch_kraken()` intern aan — geen `_from_candles` variant
- L6/L7/L8 hebben wél closed-candle policy, maar inconsistente handtekeningen
- Orchestrator (`hermes_v02.py`) wrapt met `read_layerX(pair, tf)` — maar geeft geen garantie dat output reproduceerbaar is met historische data
- L9 kan daardoor **geen** laag isoleren en herhalen op historische snapshots

### Technische implementatie

**Fase 1 — Elke laag krijgt een `_from_candles(candles: list[dict], **kwargs) -> dict` variant**

```
Huidig:    read_layer2(pair, tf)  → fetch_kraken() intern
Nieuw:     read_layer2_from_candles(candles, tf, config=None) → dict
```

Implementatie per laag:

| Laag | Huidig probleem | Fix | Prioriteit |
|------|----------------|-----|-----------|
| L2 (`swing_points.py`) | Gebruikt `fetch_kraken` in `read_layer2()` | Refactor: extracteer swing-berekening naar `compute_swings(candles, **kw)` | 🔴 Hoog |
| L3 (`layer3_label.py`) | Gebruikt pivot-index uit L2, die `fetch_kraken` aanroept | Injecteer candles via L2_from_candles | 🔴 Hoog |
| L4 (`trendline_lab.py`) | `fetch_and_prepare` haalt candles op; interne helpers zijn zuiver | Wrap interne helpers in `read_layer4_from_candles()` | 🔴 Hoog |
| L7 (`indicator_context`) | `read_indicator_context` roept Kraken aan; `_calc_atr`, `_calc_ema` zijn zuiver | Maak `read_indicator_context_from_candles(candles, tf)` | 🟡 Medium |
| L6 | ✅ Al zuiver (`analyze_candle_micro(candles, ...)`) | Geen werk nodig | 🟢 Klaar |
| L8 | ✅ Al zuiver (`read_market_context_from_candles(...)`) | Geen werk nodig | 🟢 Klaar |

**Fase 2 — Gestandaardiseerd outputcontract per laag**

Elke `read_layerX_from_candles()` retourneert een `dict` met vaste velden:

```python
# Gestandaardiseerde output (PEP 8, type hints)
{
    "layer": "L2",
    "snapshot_time": "2026-06-17T12:00:00Z",  # time of last closed candle
    "candle_count": 180,
    "closed_candle_policy": True,               # werd candles[-1] uitgesloten?
    "data": { ... },                            # laag-specifieke output
    "errors": [],                                # runtime errors (geen crash)
    "warnings": ["L2: minder dan 50 candles — resultaten onbetrouwbaar"]
}
```

**Fase 3 — Contractvalidatie in CI**

```python
# tests/contracts/test_layer_contracts.py
@pytest.mark.parametrize("layer_fn", [
    L2_from_candles, L3_from_candles, L4_from_candles,
    L6_from_candles, L7_from_candles, L8_from_candles,
])
def test_layer_contract_returns_required_keys(layer_fn):
    result = layer_fn(mock_candles, tf="60m")
    assert "layer" in result
    assert "snapshot_time" in result
    assert "closed_candle_policy" in result
    assert "data" in result
    assert isinstance(result["data"], dict)
```

### Integratie in testbot

De laagcontracten worden een `HermesLayer` ABC in de testbot:

```python
# src/crypto_test_bot_v3/analysis/hermes_layer_base.py
from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class LayerSnapshot:
    layer: str
    snapshot_time: str
    candle_count: int
    closed_candle_policy: bool
    data: dict
    errors: list
    warnings: list

class HermesLayer(ABC):
    @abstractmethod
    def compute(self, candles: list[dict], **kwargs) -> LayerSnapshot:
        ...
```

Hierdoor kan de testbot elke Hermes laag aanroepen in backtest, paper en live — zelfde code, andere data.

---

## Strategie 2: Lookahead Preventie — Twee Niveaus

### Probleem

Lookahead (data leakage) komt voor op **twee niveaus** in de huidige architectuur:

1. **Backtest lookahead** — toekomstige candles lekken in signaalberekening omdat L2/L3/L4 geen closed-candle policy hebben. L9-audit toonde: L2/L3/L4 gebruiken open candles.
2. **Agent execution lookahead** — Hermes/Claude Code ziet in één sessie data van "nu" terwijl het een historisch backtest beoordeelt. Bestaande anti-loop protocol detecteert loops maar voorkomt geen lookahead.

### Technische implementatie — Niveau 1: Backtest lookahead

**Candles immutability policy**: candle data krijgt een `closed`-flag zodra de candle gesloten is.

```python
# src/crypto_test_bot_v3/data/candle_utils.py
from datetime import datetime, timezone
from typing import Any

def seal_candles(candles: list[dict]) -> list[dict]:
    """Markeer candles als 'closed'. candles[-1] is ALTIJD closed."""
    now = datetime.now(timezone.utc).timestamp()
    for c in candles:
        c["__sealed"] = True
        c["__closed"] = c["timestamp"] + c.get("interval", 3600) <= now
    return candles

def assert_no_open_candle(candles: list[dict], layer_name: str) -> None:
    """Raise als laatste candle open is — vangt lookahead."""
    if candles and not candles[-1].get("__closed", True):
        raise LookaheadError(
            f"{layer_name}: laatste candle is open — lookahead risico. "
            f"Timestamp: {candles[-1]['timestamp']}"
        )
```

**L9 snapshot protocol**: elke snapshot gebruikt een `visible_window` en `future_window`:

```
Snapshot T = 179:
  visible: candles[0..179]  (alleen closed)
  future:  candles[180..199] (alleen voor uitkomstmeting)
  Laagberekening: ALLEEN zichtbaar op candles[0..179]
  Uitkomst: future_return op candles[180..199]
```

**CI check** — pytest fixture die lookahead detecteert:

```python
@pytest.fixture
def lookahead_safe_candles():
    candles = load_test_candles("BTC/EUR", "60m", count=200)
    return seal_candles(candles[:180])  # visible = 180 closed

def test_strategy_no_lookahead(lookahead_safe_candles):
    signal = my_strategy.compute_signal(lookahead_safe_candles)
    # Als er future data in zit: LookaheadError
```

### Technische implementatie — Niveau 2: Agent execution lookahead

**Hermes tool-level guard**: een `pre_action_hook` in Hermes agent die checkt of de actie historische data betreft en of de agent "nu" als referentie gebruikt.

```yaml
# In ~/.hermes/config.yaml aanpassing
agent:
  lookahead_guard: true
  lookahead_rules:
    - pattern: "backtest.*result"
      require_snapshot_time: true
    - pattern: "evaluate.*strategy"
      forbid_current_time_ref: true
```

**Anti-loop protocol uitbreiding** — nieuwe check:

```
LOOKAHEAD_CHECK:
  conditie: agent gebruikt "current price" / "today" / "now" in combinatie
            met historische backtest-evaluatie
  detectie: prompt-parsing op tijdsreferenties
  actie:    STOP + "LOOKAHEAD DETECTED — gebruik snapshot_time i.p.v. now"
```

**Second-brain rule**: bij elke L9-snapshot wordt `snapshot_time` opgeslagen. Agent mag geen conclusies trekken over snapshots zonder `snapshot_time` te respecteren.

### Integratie in testbot

Testbot krijgt een `LookaheadGuard` die in de `BacktestProvider` zit:

```python
class LookaheadGuard:
    def __init__(self, snapshot_time: datetime):
        self._snapshot_time = snapshot_time

    def verify(self, data: dict) -> bool:
        """Controleer of data geen future info bevat."""
        for key, value in data.items():
            if isinstance(value, datetime) and value > self._snapshot_time:
                raise LookaheadError(f"Future timestamp in field '{key}': {value}")
        return True
```

---

## Strategie 3: Data Contracts — SLA Tussen Alle Componenten

### Probleem

Data stroomt tussen 4 systemen zonder formele contracten:

```
crypto-data (pipeline) → live_cache/ (JSON-bestanden)
live_cache/ → crypto-test-bot (DataProvider)
crypto-test-bot → crypto-tradebot (signalen via bestanden)
Hermes layers → Layer 9 (dict-output zonder schema)
```

Elke interface is impliciet. Wijzigingen in één systeem breken stilletjes andere systemen. Bewijs: de `stale_cache` bug (26u oude data werd als `pullback_required` gelabeld).

### Technische implementatie

**Fase 1 — Pydantic/Schema modellen voor elke interface**

```python
# src/crypto_test_bot_v3/contracts/candle_contract.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class CandleRecord(BaseModel):
    timestamp: int
    open: float
    high: float
    low: float
    close: float
    volume: float
    interval: int = Field(ge=60, description="interval in seconds")
    closed: bool = Field(default=True)
    pair: str

class LiveCacheContract(BaseModel):
    pair: str
    timeframe: str
    candles: list[CandleRecord]
    generated_at: datetime
    freshness_seconds: int = Field(ge=0)
    stale_warning: Optional[str] = None  # "data is 26h oud"
```

**Fase 2 — Bridge-output contract**

Huidige bridge schrijft JSON zonder schema. Nieuw contract:

```json
{
  "$schema": "https://noa-hermes/bridge/v1/candle-response.json",
  "pair": "BTC/EUR",
  "timeframe": "60m",
  "candles": [
    {
      "timestamp": 1718600000,
      "o": 65000.0,
      "h": 65200.0,
      "l": 64800.0,
      "c": 65100.0,
      "v": 1234.5,
      "closed": true
    }
  ],
  "status": "fresh",
  "generated_at": "2026-06-17T12:00:00Z"
}
```

Implementatie in bridge:

```python
# In universe_ohlc_bridge.py — structuur output
def build_bridge_response(pair, tf, candles) -> dict:
    return {
        "$schema": "bridge/v1",
        "pair": pair,
        "timeframe": tf,
        "candles": [candle_to_record(c) for c in candles],
        "status": "fresh" if is_fresh(candles) else "stale",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "freshness_seconds": freshness(candles),
    }
```

**Fase 3 — Testbot DataProvider interface contract**

```python
# src/crypto_test_bot_v3/data/dataprovider_base.py
from abc import ABC, abstractmethod
from ..contracts.candle_contract import LiveCacheContract

class DataProvider(ABC):
    @abstractmethod
    def get_candles(self, pair: str, tf: str, count: int) -> LiveCacheContract:
        """Haal candles op. Garandeert dat closed=True voor candles[-1]."""
        ...

    @abstractmethod
    def get_freshness(self, pair: str, tf: str) -> int:
        """Return seconds since last update. -1 als pair niet gevolgd wordt."""
        ...
```

**Fase 4 — Monitoring/Alerting**

Cron check in second-brain:

```python
# ~/system/hermes-second-brain/scripts/check_data_contracts.py
def check_bridge_contract():
    """Valideer dat alle bridge outputs voldoen aan het contract."""
    errors = []
    for pair_file in Path(LIVE_CACHE).glob("*.json"):
        try:
            data = json.loads(pair_file.read_text())
            LiveCacheContract(**data)  # pydantic validate
        except Exception as e:
            errors.append(f"{pair_file.name}: {e}")
    return errors
```

### Data Contract Register

Permanent bewaard in second brain:

```yaml
# /mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/second-brain/wiki/concepts/data-contracts.md
contracts:
  bridge_v1:
    location: "crypto-data/logs/bridge/"
    schema: "LiveCacheContract"
    validator: "pydantic"
    staleness_threshold: 3600  # 1h = stale
    owners: ["crypto-data", "crypto-test-bot"]

  signal_v1:
    location: "crypto-tradebot/logs/signals/"
    schema: "TradeSignalContract"
    validator: "pydantic"
    owners: ["crypto-test-bot", "crypto-tradebot"]

  layer_snapshot_v1:
    location: "hermes-v01/layer9/snapshots/"
    schema: "LayerSnapshot"
    validator: "dataclass + pytest"
    owners: ["hermes-v01", "layer9"]
```

---

## Strategie 4: Hermes Layers in Testbot — Unified Analysis Pipeline

### Probleem

Testbot en Hermes layers leven nu in aparte werelden:
- Testbot heeft eigen `Strategy` classes (V3A, migratie V1/V2)
- Hermes layers (L1-L8) zitten in `projects/hermes-v01/`
- L9 (Validation Lab) is een aparte pipeline
- Geen gedeelde infrastructuur — dubbel werk, inconsistente resultaten

### Technische implementatie

**Fase 1 — `HermesSignalStrategy` wrapper**

Elke Hermes laag wordt een Strategy implementatie:

```python
# src/crypto_test_bot_v3/strategies/hermes/layer2_sr_strategy.py
from ...strategies.base import Strategy, Signal
from ...analysis.hermes_layer_base import HermesLayer
from ...data.dataprovider_base import DataProvider

class Layer2SRStrategy(Strategy):
    """Wrap L2 S/R zone detectie als testbot strategy."""

    def __init__(self, config: dict, data_provider: DataProvider):
        super().__init__(config)
        self._dp = data_provider
        self._layer = L2Layer()  # imports ge-refactorde L2_from_candles

    def compute_signal(self, pair: str, tf: str = "60m") -> Signal | None:
        candles = self._dp.get_candles(pair, tf, count=180)
        snapshot = self._layer.compute(candles.candles, tf=tf)
        zones = snapshot.data.get("sr_zones", [])

        # Signaal als prijs dichtbij S/R zone zit
        for zone in zones:
            if zone["distance_pct"] < 0.5:  # <0.5% van zone
                return Signal(
                    pair=pair,
                    strategy="L2_SR",
                    direction=zone["bounce_direction"],
                    confidence=zone["quality"],
                    meta={"zone": zone}
                )
        return None
```

Standaardstrategieën uit Hermes layers:

| Strategie | Hermes laag | Signaal | Prioriteit |
|-----------|------------|---------|-----------|
| `L2_Bounce` | L2 (S/R zones) | Bounce van S/R niveau | 🟡 Medium |
| `L3_TrendFollow` | L3 (D/U/R) | Meebewegen met fase | 🔴 Hoog |
| `L4_TrendlineBreak` | L4 (trendlines) | Break van trendline | 🔴 Hoog |
| `L6_CandlePattern` | L6 (candle micro) | Engulfing/doji bij S/R | 🟡 Medium |
| `L7_RegimeShift` | L7 (MA cross, ATR) | MA-cross + volatility shift | 🔴 Hoog |

**Fase 2 — L9 als meta-strategy evaluator**

L9 draait als een `ValidationStrategy` die andere strategieën evalueert:

```python
class Layer9ValidationStrategy(Strategy):
    """Meta-strategy: meet of een andere strategy correct voorspelde."""

    def __init__(self, target_strategy: Strategy, lookback: int = 100):
        self._target = target_strategy
        self._lookback = lookback
        self._results: list[ValidationResult] = []

    def evaluate(self, historical_candles: list[dict]) -> dict:
        """Draai target op elk snapshot, meet uitkomst."""
        for i in range(self._lookback, len(historical_candles) - 20):
            snapshot = historical_candles[:i]
            future = historical_candles[i:i+20]
            signal = self._target.compute_signal(snapshot)
            if signal:
                result = self._measure_outcome(signal, future)
                self._results.append(result)
        return self._summary()
```

**Fase 3 — Unified runner: testbot + Hermes layers**

`run.py` krijgt nieuwe commando's:

```bash
# Bestaand
python run.py backtest v3a --pair BTC/EUR
python run.py paper v3a --pair BTC/EUR

# Nieuw — Hermes layers
python run.py backtest hermes/l2_sr --pair BTC/EUR
python run.py backtest hermes/l3_trend --pair ETH/EUR
python run.py validate l3_trend --pair SOL/EUR --snapshots 100
python run.py compare l3_trend vs v3a --pair BTC/EUR
```

**Fase 4 — Resultaten naar second brain**

Na elke `validate`-run schrijft de runner JSON naar second brain:

```
/mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/second-brain/raw/validation/
├── 2026-06-17_l3_trend_BTC-EUR.json
├── 2026-06-17_l2_sr_ETH-EUR.json
└── 2026-06-17_comparison_v3a-vs-l3_trend.json
```

---

## Strategie 5: L9 Validation Lab in CI/CD — Automatische Kwaliteitspoort

### Probleem

L9 (Validation Lab) is nu een handmatige analyse — architect draait één snapshot, leest output, rapporteert. Er is geen geautomatiseerde feedbackloop die:
- Elke code-wijziging aan een laag test tegen historische data
- Regressie detecteert (L4 werkte gisteren, vandaag niet meer)
- Rapport genereert per commit

### Technische implementatie

**Fase 1 — L9 test suite in pytest**

```python
# tests/layer9/test_validation_snapshots.py
import pytest
from layer9.validation_runner import run_validation

SNAPSHOT_PAIRS = ["BTC/EUR", "ETH/EUR", "SOL/EUR"]
SNAPSHOT_TFS = ["15m", "60m", "240m"]
SNAPSHOT_COUNT = 200
FUTURE_WINDOW = 20

@pytest.mark.parametrize("pair", SNAPSHOT_PAIRS)
@pytest.mark.parametrize("tf", SNAPSHOT_TFS)
@pytest.mark.parametrize("layer", ["L2", "L3", "L4", "L6", "L7", "L8"])
def test_layer_snapshot_replayable(pair, tf, layer):
    """Elke laag moet een snapshot reproduceren zonder errors."""
    result = run_validation(layer, pair, tf, count=SNAPSHOT_COUNT)
    assert result["status"] == "ok", f"{layer} faalde op {pair} {tf}"
    assert result["snapshot_count"] >= 100
    assert len(result["errors"]) == 0

@pytest.mark.validation
def test_regression_vs_baseline():
    """Nieuwe code mag accuracy niet verlagen tov baseline."""
    current = run_validation_batch()
    baseline = load_baseline("2026-06-01")
    for layer, metrics in current.items():
        assert metrics["f1"] >= baseline[layer]["f1"] * 0.95, \
            f"{layer}: F1 gedaald van {baseline[layer]['f1']} naar {metrics['f1']}"
```

**Fase 2 — GitHub Actions workflow**

```yaml
# .github/workflows/layer9-validation.yml
name: Layer 9 Validation
on: [push, pull_request]

jobs:
  validate:
    runs-on: self-hosted  # homelab
    steps:
      - uses: actions/checkout@v4
      - name: Run L9 validation
        run: |
          python -m pytest tests/layer9/ -q --validation \
            --html=report.html --self-contained-html
      - name: Compare with baseline
        run: |
          python layer9/compare_baseline.py \
            --current results.json \
            --baseline layer9/baselines/latest.json \
            --output comparison.md
      - name: Upload report
        uses: actions/upload-artifact@v4
        with:
          name: layer9-report
          path: report.html
      - name: Update baseline if main branch
        if: github.ref == 'refs/heads/main'
        run: |
          cp results.json layer9/baselines/$(date +%Y-%m-%d).json
```

**Fase 3 — Baseline management in second brain**

Baselines bewaard in:

```
/mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/second-brain/wiki/projects/layer9-baselines/
├── 2026-06-01.json    # eerste baseline (L2-L8)
├── 2026-06-10.json    # na L4 trendline fix
├── 2026-06-15.json    # na L7 ma-cross fix
└── latest.json        # symlink → laatste baseline
```

Elke baseline bevat per laag:

```json
{
  "L3": {
    "f1": 0.72,
    "precision": 0.74,
    "recall": 0.70,
    "sample_count": 3420,
    "confusion_matrix": {"U": [120, 30, 15], "D": [25, 140, 10], "R": [20, 15, 130]},
    "commit": "91e24243",
    "date": "2026-06-12"
  }
}
```

**Fase 4 — Hermes cron voor weekly L9 scan**

```bash
# ~/.hermes/cron/layer9-weekly-scan.sh
#!/bin/bash
# Draait elke zondag 08:00 via Hermes cron
cd /home/sjoe/projects/hermes-v01
python -m layer9.validation_runner \
  --pairs BTC/EUR,ETH/EUR,SOL/EUR \
  --tfs 15m,60m,240m \
  --count 500 \
  --output /mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/second-brain/raw/validation/
python -m layer9.compare_baseline \
  --current results.json \
  --baseline layer9/baselines/latest.json \
  --output /mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/second-brain/raw/validation/comparison.md
```

Output wordt automatisch naar second brain geschreven en beschikbaar voor volgende Hermes sessie.

### Integratie in testbot

L9 CI-runner wordt een `run.py` commando:

```bash
python run.py validate-all \
  --pairs BTC/EUR,ETH/EUR,SOL/EUR \
  --tfs 15m,60m,240m \
  --layers L2,L3,L4,L6,L7,L8 \
  --snapshots 200 \
  --baseline layer9/baselines/latest.json \
  --html report.html
```

---

## Implementatieprioriteit

| # | Strategie | Afhankelijk van | Tijd | Risico | Impact |
|---|-----------|----------------|------|--------|--------|
| 1 | Laagcontracten | Niets | 2-3 dagen | 🟡 Medium (bestaande code aanpassen) | 🔴 Hoog — basis voor L9 |
| 2 | Lookahead preventie | Strategie 1 | 1-2 dagen | 🟢 Laag (toevoegingen, geen refactors) | 🔴 Hoog — voorkomt data leakage |
| 3 | Data contracts | Niets | 2-3 dagen | 🟢 Laag (nieuwe code, geen bestaande aanpassingen) | 🟡 Medium — stabiliteit |
| 4 | Layers in testbot | Strategie 1, 3 | 3-5 dagen | 🟡 Medium — moet laagcontracten afwachten | 🔴 Hoog — unified pipeline |
| 5 | L9 in CI/CD | Strategie 1, 2, 4 | 2-3 dagen | 🟢 Laag (Git Actions + cron) | 🟡 Medium — kwaliteitsborging |

### Aanbevolen volgorde

```
Week 1:  Strategie 1 (laagcontracten) + Strategie 2 (lookahead)
          → L2/L3/L4 _from_candles refactor
          → Anti-loop protocol uitbreiding
          → LookaheadGuard in testbot

Week 2:  Strategie 3 (data contracts)
          → Pydantic modellen
          → Bridge-output contract
          → Data Contract Register in second brain

Week 3:  Strategie 4 (layers in testbot)
          → HermesSignalStrategy wrappers
          → L9 als meta-strategy
          → run.py uitbreiding

Week 4:  Strategie 5 (L9 in CI/CD)
          → pytest validatiesuite
          → GitHub Actions workflow
          → Baseline management
          → Cron wekelijkse scan
```
