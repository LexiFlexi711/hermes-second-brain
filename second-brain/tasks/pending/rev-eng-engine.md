# Taak: Rev_Eng Engine — Reverse Engineer een strategie vanuit ideale trades

**Van:** Claude  
**Datum:** 2026-06-02  
**Prioriteit:** Hoog  
**Project:** `/mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/projects/crypto-test-bot-v3/`

---

## Het concept (van Lexi)

Niet starten vanuit een strategie en die backtesten.
Starten vanuit de **ideale trades** en ontdekken **welke strategie die vindt**.

**Generieke loop — werkt voor elke strategie (range, trend, pullback, ...):**

1. **Oracle scan** — vind alle ideale trades in hindsight voor een gegeven strategie-type
2. **Feature extractie** — wat was zichtbaar in de candles vóór elke goede trade?
3. **Patroon ontdekking** — welke features zijn consistent aanwezig bij goede trades?
4. **Rule synthese** — vertaal die patronen naar concrete filters en parameters
5. **Validatie** — werkt de gevonden rule set zonder lookahead?

De **oracle scanner** is het enige deel dat per strategie-type verschilt.
De rest van de pipeline is generiek en herbruikbaar voor range, trend, en alles daarna.

---

## Module structuur

```
scripts/rev_eng/
├── __init__.py
├── base.py                  # Abstracte base classes
├── oracle_range.py          # Oracle scanner voor range trades
├── oracle_trend.py          # Oracle scanner voor trend trades (later)
├── feature_extractor.py     # Generieke feature extractie (geen lookahead)
├── pattern_discovery.py     # Patroon ontdekking → rule set
├── rule_validator.py        # Validatie zonder lookahead
└── discover.py              # Hoofdscript — bind alles samen

tests/unit/
├── test_rev_eng_oracle_range.py
├── test_rev_eng_feature_extractor.py
└── test_rev_eng_pattern_discovery.py
```

---

## Base classes (`scripts/rev_eng/base.py`)

```python
from __future__ import annotations
from dataclasses import dataclass, field
from abc import ABC, abstractmethod

@dataclass
class OracleTrade:
    """Een ideale trade gevonden in hindsight."""
    pair: str
    strategy_type: str       # "range", "trend", "pullback"
    entry_ts: int
    entry_price: float
    tp_price: float
    sl_price: float
    tp_hit_ts: int
    hold_candles: int
    pnl_pct: float
    meta: dict = field(default_factory=dict)  # strategie-specifieke context

@dataclass
class PreTradeFeatures:
    """Features extraheerd uit candles vóór een trade. Geen lookahead."""
    trade: OracleTrade
    features: dict           # {"feature_naam": waarde}

@dataclass
class FeatureStat:
    name: str
    mean: float
    median: float
    std: float
    consistency: float       # 0-1: hoe consistent over alle trades

@dataclass
class DiscoveredRuleSet:
    strategy_type: str
    filters: dict            # {"feature_naam": {"min": x, "max": y}}
    confidence: float
    n_trades_basis: int
    top_features: list[FeatureStat]

@dataclass
class ValidationResult:
    precision: float
    recall: float
    f1: float
    true_positives: int
    false_positives: int
    false_negatives: int
    avg_pnl_pct: float

class OracleScanner(ABC):
    """Abstracte base — elke strategie implementeert zijn eigen scanner."""
    @abstractmethod
    def scan(self, candles: list[dict], pair: str) -> list[OracleTrade]:
        ...
```

---

## Oracle Range (`scripts/rev_eng/oracle_range.py`)

Vind alle momenten waar een range trade had gewerkt.

**Definitie ideale range trade:**
- Aaneengesloten periode van minstens `min_range_candles` (default: 20) candles
- Spread < `max_range_pct` (default: 8%), spread > `min_range_pct` (default: 2%)
- Entry mogelijk in onderste `entry_zone` (default: 20%) van de range
- TP = `range_low + tp_zone * range_width` (default: 65%)
- SL = `range_low * (1 - sl_buffer)` (default: 0.5%)
- TP geraakt binnen `max_hold_candles` (default: 96) zonder SL te raken

Vul `meta` in met: `range_high`, `range_low`, `range_pct`, `range_duration_candles`

---

## Feature Extractor (`scripts/rev_eng/feature_extractor.py`)

Generiek — werkt voor elke strategie. Extraheert features uit de `lookback` candles vóór `entry_ts`.

**Verplichte features (altijd berekend):**
```python
# Prijs positie
price_vs_recent_high_pct     # prijs t.o.v. hoogste punt lookback
price_vs_recent_low_pct      # prijs t.o.v. laagste punt lookback
price_position_in_range      # 0.0=bodem, 1.0=top van lookback range

# Volume
volume_vs_avg                # gem. laatste 5 candles / gem. lookback
volume_trend                 # "dalend" / "stijgend" / "neutraal"

# Momentum
consecutive_same_direction   # hoeveel opeenvolgende candles zelfde richting
body_size_trend              # "krimpend" / "stabiel" / "groeiend"
candles_since_extreme        # candles sinds laagste punt in lookback

# Structuur
rejection_wick_present       # wick die richting entry afwijst (bool)
higher_low_formed            # hogere bodem gevormd in lookback (bool)
```

**Interface:**
```python
class FeatureExtractor:
    def extract(self, trade: OracleTrade, 
                all_candles: list[dict], 
                lookback: int = 40) -> PreTradeFeatures:
        """Gebruik enkel candles met timestamp < trade.entry_ts."""
```

---

## Pattern Discovery (`scripts/rev_eng/pattern_discovery.py`)

Gegeven lijst van `PreTradeFeatures`: vind wat consistent aanwezig is.

**Aanpak:**
- Numerieke features: bereken mean, median, std → consistency = 1 - (std / (mean + ε))
- Bool features: frequency → consistency = max(freq, 1-freq)
- Categorische features: meest voorkomende waarde → consistency = freq van die waarde
- Filter: behoud alleen features met consistency >= `min_consistency` (default: 0.65)
- Output: `DiscoveredRuleSet` met drempelwaarden afgeleid van mediaan ± 0.5*std

**Interface:**
```python
class PatternDiscovery:
    def discover(self, features: list[PreTradeFeatures],
                 min_consistency: float = 0.65) -> DiscoveredRuleSet:
        ...
```

---

## Rule Validator (`scripts/rev_eng/rule_validator.py`)

Test de gevonden rules op echte candles zonder lookahead.

- Genereer signalen op elk candle waar rules gelden
- Vergelijk met oracle trades (match op timestamp nabijheid ± 4 candles)
- Bereken precision, recall, F1

```python
class RuleValidator:
    def validate(self, rules: DiscoveredRuleSet,
                 candles: list[dict],
                 oracle_trades: list[OracleTrade],
                 feature_extractor: FeatureExtractor) -> ValidationResult:
        ...
```

---

## Hoofdscript (`scripts/rev_eng/discover.py`)

```
Gebruik:
    python scripts/rev_eng/discover.py --pair XBTEUR --strategy range --years 1
    python scripts/rev_eng/discover.py --pair XBTEUR --strategy trend --years 1
    python scripts/rev_eng/discover.py --pairs XBTEUR ETHEUR SOLEUR --strategy range
```

**Output:**
```
XBTEUR — range — 1 jaar
────────────────────────────────────────────
Oracle trades gevonden:  47
Lookback features:       12

Top filters (consistency):
  pre_range_duration     mediaan=24  min≥15      consistency=0.82
  volume_vs_avg          mediaan=0.6 max≤0.85    consistency=0.74
  rejection_wick         True        freq=71%    consistency=0.71

Validatie (geen lookahead):
  Precision  68%   Recall  91%   F1  0.78
  Gem. PnL gevonden trades: +1.34%
────────────────────────────────────────────
```

---

## Tests

**test_rev_eng_oracle_range.py:**
```python
def test_vindt_ideale_range()       # range aanwezig, TP geraakt → gevonden
def test_slaat_sl_hit_over()        # SL geraakt voor TP → niet opgenomen  
def test_range_te_breed_skip()      # spread > 8% → geen trade
def test_range_te_smal_skip()       # spread < 2% → geen trade
def test_geen_entry_aan_bodem()     # prijs niet in entry_zone → geen trade
```

**test_rev_eng_feature_extractor.py:**
```python
def test_geen_lookahead()           # features gebruiken enkel ts < entry_ts
def test_volume_dalend()            # dalend volume → volume_vs_avg < 1.0
def test_rejection_wick()           # wick aanwezig → rejection_wick_present=True
```

---

## Constraints

- **Enkel stdlib** — geen sklearn, numpy, pandas
- **Geen lookahead** — feature extractor mag entry_ts niet overschrijden
- **Generiek** — oracle_range en oracle_trend zijn uitwisselbaar in dezelfde pipeline
- **Single pair eerst** — geen parallellisatie, eerst correct dan snel

---

## Bewijs dat je levert

1. `python -m pytest tests/unit/test_rev_eng_*.py -v` — alle tests groen
2. `python scripts/rev_eng/discover.py --pair XBTEUR --strategy range --years 1` — draait, geeft output
3. Vermeld: hoeveel oracle trades op XBTEUR, top 3 features met consistency score
