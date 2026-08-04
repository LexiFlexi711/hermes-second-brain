---
title: Crypto Test Bot V3
type: project
created: 2026-05-29
updated: 2026-05-30
status: in-ontwikkeling
---

# Crypto Test Bot V3

Nieuw modulair test-bot systeem. Doel: strategieën grondig testen via backtest + paper + live, met een rijke journal die elke beslissing (ook afgewezen signalen) vastlegt voor latere analyse.

Aparte repo van crypto-tradebot. Hergebruikt componenten uit bestaande codebase waar zinvol.

## Rolverdeling

| Wie | Rol |
|-----|-----|
| Claude | Architectuurbewaker, second brain, interfaces bewaken, integratie |
| Hermes/DeepSeek | Implementatie van afgebakende modules (één taak = één bestand) |
| ChatGPT | Spot review op verzoek |

## Projectstructuur

```
crypto-test-botv3/
├── config/
│   ├── v3a.json          ← parameters per strategie-variant (baseline/loose/strict)
│   ├── breakout.json
│   └── momentum.json
├── src/
│   ├── data/
│   │   └── reader.py     ← DataReader ABC → LiveReader / BacktestReader
│   ├── market/
│   │   ├── levels.py     ← overgenomen van market_levels.py
│   │   ├── structure.py  ← overgenomen van market_structure_reader.py
│   │   └── regime.py     ← NIEUW: get_regime() centrale interface
│   ├── strategy/
│   │   ├── base.py       ← CheckResult + Signal dataclasses + Strategy ABC
│   │   ├── aggregator.py ← mode A (gate) / B (score) / C (mixed) via config
│   │   └── v3a.py        ← V3A checks (hergebruikt pull_backtrader_3a functies)
│   ├── trader/
│   │   ├── trader.py     ← accept/reject + alles loggen
│   │   └── journal.py    ← schrijft trade_journal.jsonl + CSV export
│   └── backtest/
│       ├── runner.py     ← event-driven, geen lookahead, BacktestReader
│       └── report.py     ← overgenomen van backtest_report.py
├── tests/
└── main.py               ← orchestrator: laadt config, koppelt lagen
```

## 20-lagen model

Lexi's analyse van het systeem van onder naar boven:

| Laag | Wat | Status bestaande code |
|------|-----|----------------------|
| 1 | Exchange API, pair universe, fetchers | ✓ crypto-data klaar |
| 2 | Kopers/verkopers, sentiment | ⚠ deels (market_structure_reader.py) |
| 3 | Spread, volume, tradebaarheidsfilter | ✓ crypto-data klaar |
| 4 | Ruwe OHLCV, archive, live_cache | ✓ klaar |
| 5 | Candle metrics, patronen | ✓ candle_reader.py, candle_patterns.py |
| 6 | Timeframes 15M/1H/4H/1D | ✓ trade_engine.py |
| 7 | Marktstructuur: pivots, HH/HL, structure break | ✓ market_levels.py |
| 8 | Trend: detect_trend_direction | ⚠ duplicaat — V3A-versie wint |
| 9 | Support/resistance | ✓ market_levels.py (centrale owner) |
| 10 | Regime: trending/range/compression/pullback_zone | ⚠ geen centrale get_regime() |
| 11 | Indicatoren als bevestiging | ✓ indicator_research_probe.py (research) |
| 12 | Setup: markt is interessant | ✓ v3a_backtest, breakout, momentum |
| 13 | Trigger: concreet signaal | ✓ detect_pullback_failed_v3a(), signal_detector.py |
| 14 | Strategie/script | ✓ v3a, breakout, momentum apart |
| 15 | Strategieparameters | ⚠ hardcoded → moet naar config/ |
| 16 | Testwaarden, param-varianten | ✓ v3a_param_compare.py |
| 17 | Backtestregels: event-driven, geen lookahead | ✓ v3a_backtest.py |
| 18 | Resultaatmetingen | ✓ backtest_report.py |
| 19 | Paper/live validatie | ✓ logs, jsonl, heartbeat, dashboard |
| 20 | Kandidaatstrategie-criteria | ✓ beschreven, nog niet als code |

## Kern-interfaces (VAST — niet wijzigen zonder review)

### CheckResult
```python
@dataclass
class CheckResult:
    name: str
    ok: bool
    value: Any    # gemeten waarde: 0.52, "long", "chop", ...
    why: str      # leesbare reden
```

### Signal
```python
@dataclass
class Signal:
    direction: str             # "long" | "short"
    entry: float
    sl: float
    tp: float
    checks: dict[str, CheckResult]
    context: dict              # volledige candle context op moment van signaal
```

### Aggregator config
```json
{
  "mode": "gate",
  "required": ["trend", "structure"],
  "optional": ["regime", "indicator"],
  "threshold": 0.6
}
```

Modes:
- **gate (A)**: alle required checks ok → signaal. Één fail = geen signaal.
- **score (B)**: gewogen score per check, totaal > threshold → signaal.
- **mixed (C)**: required checks + optionele score-bonus.

### Journal entry (trade_journal.jsonl)
```json
{
  "id": "uuid",
  "ts": 1780037100,
  "pair": "INJEUR",
  "strategy": "v3a",
  "params_variant": "baseline",
  "decision": "OPEN",
  "reject_reason": null,
  "signal": {"direction": "long", "entry": 5.0, "sl": 4.90, "tp": 5.15},
  "checks": {
    "trend":     {"ok": true,  "value": "long",   "why": "HH+HL op 4H"},
    "fib":       {"ok": true,  "value": 0.52,     "why": "in 38-78% zone"},
    "structure": {"ok": true,  "value": "intact", "why": "geen break"},
    "regime":    {"ok": false, "value": "chop",   "why": "geen richting"}
  },
  "context": {
    "4H": {"close": 5.0, "body_pct": 0.6, "trend": "long"},
    "1H": {"close": 5.0, "body_pct": 0.4},
    "15M": {"close": 5.0, "body_pct": 0.3, "wick_upper": 0.1}
  },
  "candle_window": {
    "ref": {"pair": "INJEUR", "interval": 15, "ts_signal": 1780037100},
    "lookback": [
      {"offset": -3, "ts": 1780034400, "body_pct": 0.3, "wick_upper": 0.5, "wick_lower": 0.1, "pattern": null, "direction": 1},
      {"offset": -2, "ts": 1780035300, "body_pct": 0.6, "wick_upper": 0.1, "wick_lower": 0.2, "pattern": null, "direction": -1},
      {"offset": -1, "ts": 1780036200, "body_pct": 0.8, "wick_upper": 0.05,"wick_lower": 0.1, "pattern": "bearish_engulfing", "direction": -1}
    ],
    "signal_candle": {"offset": 0, "ts": 1780037100, "body_pct": 0.7, "wick_upper": 0.05, "wick_lower": 0.6, "pattern": "hammer", "direction": 1},
    "lookahead": null
  },
  "outcome": "WIN",
  "exit_price": 5.15,
  "exit_ts": 1780040000,
  "pnl_pct": 3.0
}
```

**Afgewezen signalen worden ook gelogd** (`decision: "REJECT"`) — voor analyse van gemiste setups.

## Status (2026-05-30)

### STAP T — Parameters als args/kwargs + grid search

Alle hardcoded waarden in logic.py en strategy.py zijn blootgesteld als kwargs.
Nieuwe params: `pivot_n`, `pivot_lookback`, `sma_fast`, `sma_slow`, `sma_long_window`, `sma_threshold`, `sl_buffer_pct`, `tp_buffer_pct`, `trail_pct`, `n_4h`, `n_15m`.
Alle JSON configs uitgebreid. Runner leest trail_pct/n_4h/n_15m uit strategy.params.

Nieuw script: `research/compare/v3a_grid_search.py` — draait alle parametercombo's via itertools.product, rankt op gemiddelde WR%.

48/49 unit tests groen (1 pre-existente fout in test_kandidaat_rapport.py).

### STAP S — Volledige 7-pair run (2026-05-30)

EINDOORDEEL: **NIET KLAAR** (2/4 criteria slaagt)
- Consistentie: 0/7 pairs ≥ 40% WR (beste: ADAEUR 34.5%) ❌
- Parameterstabiliteit: gem. spread 13.5% ✅
- Paper/backtest alignment: niet werkend ❌
- Exit potentieel: sterk (MFE data bewezen) ✅

Beste pairs: ADAEUR (+25.3% PnL), LINKEUR (+27.1% PnL) — stabiel en positief.

Volgende: grid search op alle params → V3A naar ≥ 40% WR brengen.

## Status (2026-05-29)

Fasen A t/m H volledig afgerond. 41/41 tests slagen.
Commit: `7ac02d36` gepusht naar `LexiFlexi711/NOA-reign`.
Auto-commit Stop hook actief in `.claude/settings.json` (git add src/+tests/ → commit → push bij sessie-einde).

### Sessie 2026-05-29 — data + bugfixes

**Historische data geïmporteerd:**
- `Kraken_OHLCVT.zip` (7.4GB) + `Kraken_OHLCVT_Q1_2026.zip` (521MB)
- Import script: `crypto-data/scripts/import_historical.py`
- Output: `crypto-data/logs/historical_csv/` — 2526 bestanden, 29.4M candles
- ETHEUR_15m: 361.327 candles (2015-08-07 → 2026-03-31)
- BacktestReader leest nu historical_csv (primair) + ohlc_archive (recent), mergt op timestamp
- Eind juni Q2 2026 beschikbaar → sluit gat naar live archive (april-mei 2026)

**Bugs gevonden en gefixed:**
1. `journal.py log_open`: `"ts": _now_ts()` → `"ts": ts` (candle timestamp uit signal.context)
2. `journal.py log_reject`: `"ts": _now_ts()` → `"ts": context.get("entry_candle_ts", _now_ts())`
3. `strategy.py build_signal`: SL-validatie toegevoegd — long: sl >= entry → None, short: sl <= entry → None
   - Oorzaak: `detect_trend_direction` geeft soms pivot_high/low terug dat aan de verkeerde kant van entry ligt
   - Gevolg zonder fix: LOSS met positieve pnl, avg_loss_pct positief (onzinnig)

**Smoke run resultaten (gecorrigeerd, ETHEUR 2023-10-01 → 2024-03-31):**
- 6 trades, 1 win / 5 losses, winrate 16.7%
- avg_win: +5.96% | avg_loss: -1.93% | total_pnl: -3.68%
- Timestamps correct (candle ts), SL correct (long < entry, short > entry)

**Overige fixes deze sessie:**
- `universe_ohlc_bridge.py`: incomplete (lopende) candle wordt niet meer naar archive geschreven
  - Filter in `archive_new`: `timestamp + interval * 60 <= time.time()`
  - `_cleanup_incomplete_candles()` bij startup (verwijderde 282 slechte candles)

**Runner performance fix:** bisect.bisect_right + pre-index all_4h_ts → O(n log n).
8 pairs × 3 jaar in ~14 minuten totaal (was >15 min per pair).

### Multi-pair backtest V3A/baseline  2022-01-01 → 2025-12-31

Journals opgeslagen in `crypto-test-bot-v3/logs/backtest_multirun/journal_PAIR_baseline.jsonl`.

| Coin | Pair | Trades | WR | Avg win | Avg loss | PnL | PF | Max streak |
|------|------|--------|----|---------|----------|-----|----|------------|
| DOGE | DOGEUR | 9 | 55.6% | +8.77% | -4.00% | +27.85% | 2.74 | 2 |
| XRP | XRPEUR | 101 | 33.7% | +6.55% | -2.87% | +29.98% | 1.16 | 10 |
| BTC | XBTEUR | 97 | 17.5% | +3.81% | -0.51% | +23.63% | 1.58 | 16 |
| ADA | ADAEUR | 110 | 31.8% | +6.48% | -3.18% | -11.41% | 0.95 | 9 |
| BNB | BNBEUR | 17 | 29.4% | +3.21% | -1.41% | -0.84% | 0.95 | 4 |
| SOL | SOLEUR | 103 | 30.1% | +6.22% | -3.24% | -40.24% | 0.83 | 10 |
| ETH | ETHEUR | 71 | 23.9% | +5.32% | -2.59% | -49.42% | 0.65 | 11 |
| TRX | TRXEUR | 84 | 8.3% | +2.31% | -0.75% | -41.34% | 0.28 | 38 |

**Observaties:**
- BTC + XRP: positief PnL, profit factor > 1 → interessant voor verdere analyse
- DOGE: hoge WR + PF maar slechts 9 trades (data pas jun 2025, te weinig)
- TRX: problematisch — 8.3% WR, max streak 38 verlies → niet geschikt voor V3A
- ETH: negatief ondanks redelijke WR — avg_loss te hoog
- Dit is ruw baseline zonder parameteroptimalisatie

**Bug gevonden en gefixed na eerste run:** 4H lookahead bias.
`bisect_right(all_4h_ts, ts)` includeerde lopende 4H candle → gefixed naar `bisect_right(all_4h_ts, ts - interval_4h * 60)`.

### Multi-pair backtest V2 (gecorrigeerd, zonder lookahead) — 2022-01-01 → 2025-12-31

Journals in `crypto-test-bot-v3/logs/backtest_multirun_v2/`, snapshots in `.../snapshots/`.

| Coin | Pair | Trades | WR | Avg win | Avg loss | PnL | PF | Streak | Status |
|------|------|--------|----|---------|----------|-----|----|--------|--------|
| BTC | XBTEUR | 102 | 17.6% | +3.97% | -0.45% | +33.42% | 1.879 | 16 | **KANDIDAAT** |
| ADA | ADAEUR | 98 | 34.7% | +6.58% | -3.13% | +23.37% | 1.117 | 7 | **KANDIDAAT** |
| DOGE | DOGEUR | 8 | 50.0% | +8.33% | -3.99% | +17.33% | 2.085 | 2 | te weinig data |
| BNB | BNBEUR | 23 | 26.1% | +3.28% | -1.19% | -0.48% | 0.976 | 6 | neutraal |
| XRP | XRPEUR | 91 | 27.5% | +6.67% | -2.66% | -9.13% | 0.948 | 12 | afgewezen |
| ETH | ETHEUR | 79 | 27.8% | +4.36% | -2.38% | -39.91% | 0.706 | 7 | afgewezen |
| TRX | TRXEUR | 95 | 9.5% | +3.14% | -0.67% | -29.79% | 0.487 | 15 | afgewezen |
| SOL | SOLEUR | 98 | 25.5% | +6.85% | -3.11% | -55.92% | 0.754 | 13 | afgewezen |

**Kandidaten (PF > 1, trades >= 20):** BTC + ADA
**Afgewezen:** XRP (was lookahead-geflatterd), TRX (WR 9.5%), SOL, ETH

**Volgende stappen Fase 8:**
- Parameterstabiliteitscheck (loose/strict) op BTC + ADA
- Paper vs backtest vergelijking
- Snapshot-based audit (HOLD-logging, MFE/MAE per candle) — architectuur beschreven

## Werkelijke structuur (Hermes build)

Package: `src/crypto_test_bot_v3/` + `pyproject.toml` (pip-installable)

Statusoverzicht:
- domain/ — Candle, Trade, enums ✓  |  CheckResult + Signal ✗
- infrastructure/ — paths.py, ohlc_archive.py, jsonl_store.py ✓  |  DataReader ABC + LiveReader ✗
- market/ — mappen bestaan maar zijn 0-byte stubs ✗
- strategies/v3a/ — logic.py, config.py, spec.py ✓  |  Strategy ABC + Aggregator ✗
- backtesting/v3a_backtest.py ✓  |  9/9 tests slagen
- reporting/ — metrics.py, text_report.py, json_report.py ✓
- research/v3a_param_compare.py ✓  |  v3a_profiles.json baseline/loose/strict ✓
- trader/ — leeg ✗

Architectureel probleem: backtest omzeilt DataReader ABC, importeert direct ohlc_archive.
Oplossing: DataReader ABC toevoegen, BacktestReader wraps ohlc_archive, LiveReader nieuw.
Backtest blijft werken zoals nu — uitbreiden, niet refactoren.

## Stappenplan

### Fase 0 — Fundament
- 0.1 Repo aanmaken (git init, .gitignore)
- 0.2 Mappenstructuur (src/, config/, tests/)
- 0.3 Lege __init__.py per module
- 0.4 requirements.txt

### Fase 1 — Data-laag
- 1.1 DataReader ABC — get_candles(pair, interval, n) → list[dict]
- 1.2 BacktestReader — leest ohlc_archive, filtert op timestamp
- 1.3 LiveReader — leest live_cache, zelfde interface
- 1.4 Test: candles correct in beide modes

### Fase 2 — Markt-laag
- 2.1 src/market/levels.py — kopieer market_levels.py
- 2.2 src/market/structure.py — kopieer market_structure_reader.py
- 2.3 src/market/candles.py — kopieer candle_reader.py + candle_patterns.py
- 2.4 src/market/regime.py — NIEUW: get_regime(c4h, c1h, c15m) → str
- 2.5 Test: bekende candle-reeks → verwacht regime-label

### Fase 3 — Strategie-laag
- 3.1 src/strategy/base.py — CheckResult, Signal, Strategy ABC
- 3.2 config/v3a.json — alle V3A parameters uit code halen
- 3.3 src/strategy/aggregator.py — gate/score/mixed via config
- 3.4 src/strategy/v3a.py — check_X(data, params) → CheckResult per check
- 3.5 Test: candles + config → Signal of None, alle checks zichtbaar

### Fase 4 — Backtest
- 4.1 src/backtest/report.py — kopieer backtest_report.py
- 4.2 src/backtest/runner.py — event-driven, geen lookahead, entry volgende candle
- 4.3 Verbind runner met V3A strategy
- 4.4 Test: output vergelijken met bestaand v3a_backtest.py

### Fase 5 — Journal
- 5.1 src/trader/journal.py — JSONL writer, vult lookahead bij sluiting
- 5.2 src/trader/trader.py — accept/reject, roept journal aan in beide gevallen
- 5.3 candle_window invullen (lookback + lookahead als metrics, ref naar archive)
- 5.4 Test: OPEN + REJECT entries aanwezig, candle_window ingevuld

### Fase 6 — Paper-validatie
- 6.1 LiveReader koppelen aan strategy-loop
- 6.2 Heartbeat + scan-log
- 6.3 Dashboard-feed vanuit journal
- 6.4 Vergelijking: ziet V3A live dezelfde setups als backtest?

### Fase 7 — Parameter-varianten
- 7.1 config/v3a_loose.json + config/v3a_strict.json
- 7.2 CLI-flag --variant laadt juiste config
- 7.3 Rapport per variant naast elkaar

### Fase 8 — Kandidaatbeoordeling
- 8.1 Multi-pair backtest (min. 5 pairs)
- 8.2 Parameterstabiliteitscheck
- 8.3 Paper vs backtest vergelijking
- 8.4 Kandidaat ja/nee met bewijs in second brain

Breakout + Momentum: apart plan na V3A-validatie.
Live trading: pas na paper-validatie.

## Gaps die gebouwd moeten worden

1. `src/market/regime.py` — `get_regime(c4h, c1h, c15m) → str`
2. `src/data/reader.py` — `DataReader` ABC + `LiveReader` + `BacktestReader`
3. `src/strategy/base.py` — `CheckResult`, `Signal`, `Strategy` ABC
4. `src/strategy/aggregator.py` — mode A/B/C via config
5. `config/v3a.json` — V3A parameters uit code halen

## Herbruikbaar uit bestaande code

| Bestand (bron) | Naar (test-botv3) |
|---|---|
| market_levels.py | src/market/levels.py (direct) |
| market_structure_reader.py | src/market/structure.py (direct) |
| pull_backtrader_3a.py functies | src/strategy/v3a.py (als checks) |
| backtest_report.py | src/backtest/report.py (direct) |
| candle_reader.py | src/market/ (candle metrics) |
| candle_patterns.py | src/market/ (patronen) |
| live_data_cache.py (crypto-data) | src/data/reader.py LiveReader basis |

## Werkwijze Hermes-taken

Elke Hermes-taak moet bevatten:
- Welk bestand aanmaken
- Exacte interface (signatuur, input, output)
- Welke imports beschikbaar zijn
- Hoe te testen (simpele assert)

Hermes heeft geen projectcontext nodig — alleen de taakspec.

## Zie ook

- [[crypto-tradebot]] — bestaande bot, bron van herbruikbare componenten
- [[pullback-trader-strategy]] — V3A logica
