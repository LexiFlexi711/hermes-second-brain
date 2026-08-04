---
type: project
status: draft
created: 2026-05-29
tags: [crypto-test-bot, architectuur, modulair, event-driven]
---

# Crypto Test-Bot — Architectuur

## Relatie met crypto-data

```
crypto-data/                      crypto-test-bot/
─────────────────                 ─────────────────
Pipeline (top 100)                Strategieën (modulair)
universe → filter → score         Strategy classes (OOP)
↓ watchlist                       DataProvider ← crypto-data/live_cache
↓ bridge (OHLC)                   Signal → ExecutionEngine → Paper/Live Router
↓ live_cache + ohlc_archive       Logging → analyse → bijsturen
```

- **crypto-data** = de bestaande pipeline die coins selecteert en filtert tot top 100
- **crypto-test-bot** = nieuw modulair systeem dat strategieën ontwikkelt met parameters (geen harde code), test, backtest, bijstelt tot feilloos, en signalen doorgeeft aan traders

## Kernprincipes

1. **Modulair** — elke laag eigen verantwoordelijkheid, communiceert via events/queues
2. **Config-driven** — alle parameters in JSON/YAML, niks hardcoded
3. **Herbruikbaar** — OOP base classes (Strategy, Trader, DataProvider)
4. **Gescheiden** — Data → Strategie → Trader → Logging, strikte interfaces
5. **Testbaar** — zelfde Strategy classes voor backtest, paper en live

## Architectuurlagen

### Data Layer (MarketData / CandlesReader)
- Leest uit `crypto-data/logs/live_cache/` en `crypto-data/logs/ohlc_archive/`
- Centrale DataProvider met Observer-patroon (geen dubbele API-calls)
- WebSocket optioneel voor realtime
- Publiceert events per stream (bv. `BTC/EUR-15m-update`)

### Strategy Layer (StrategyLab)
- Base class `Strategy` met `compute_signal(marketdata) -> Signal`
- Elke strategie krijgt eigen JSON-config met symbolen, intervals, drempels
- Strategie beheert enkel *eigen interne state* (window, tracking) — nooit gedeelde state
- Retourneert enkel signalen — geen execution logica

### Execution Layer (ExecutionEngine / OrderRouter)
- Luistert naar signalen van alle strategieën
- `OrderRouter` interface: `PaperRouter` (simulatie) en `LiveRouter` (echte API)
- Positiebeheer, risk management (max exposure, stop-loss), order lifecycle
- Strikte scheiding: strategie beslist WANNEER, trader doet WAT

### Logging & Monitoring
- Trade logs in `*_trades.jsonl`, state in `*_state.json` per strategie
- Events (SignalGegeven, TradeUitgevoerd) voor transparantie
- Heartbeats, web dashboard

### Analysis Layer
- Hergebruikt exact dezelfde Strategy classes
- `BacktestProvider` injecteert historische data in DataProvider interface
- Backtest, paper, live = zelfde code, andere DataProvider + OrderRouter

## Configuratie

```json
{
  "strategies": [
    {"name": "Momentum", "symbol": "BTC/EUR", "lookback": 50, "threshold": 0.01},
    {"name": "MeanReversion", "symbol": "ETH/EUR", "window": 20}
  ]
}
```

- Aparte config per strategie in `config/*.json`
- Geen hardcoded constanten in code

## Workflows

| Fase | Data | Router | Doel |
|------|------|--------|------|
| Backtest | Historisch (ohlc_archive) | Simulation | Parameters valideren |
| Paper | Live (live_cache) | PaperRouter | Gedrag testen |
| Live | Live (live_cache) | LiveRouter | Echte trades |

## Review-opmerkingen (Claude review + Hermes review, 2026-05-29)

### 3 punten uit Claude review
1. **OrderRouter interface** — cruciaal: abstractie tussen PaperRouter en LiveRouter voorkomt `if paper_mode:` checks
2. **State-disclaimer** — strategie is niet "stateless", maar beheert enkel *eigen interne state* (window, tracking)
3. **Analyse ↔ Runtime koppeling** — backtest moet zelfde Strategy classes gebruiken via BacktestProvider

### 3 punten uit Hermes agentscan
4. **`class DataReader(ABC)`** — nu beslissen, niet later. LiveReader (live_cache) en BacktestReader (ohlc_archive) implementeren zelfde interface.
5. **Position sizing** — ontbreekt in document. Welke grootte per trade? Hoeveel EUR? Dit hoort in ExecutionEngine.
6. **Portfolio-level limieten** — bij 10 parallelle strategieën: wie beheert gecombineerde exposure?

### DataProvider keuze
Voor crypto-test-bot: **Polling via JSON-cache** (huidige crypto-data aanpak). WebSocket is later toevoegbaar. Polling = laag complex, genoeg voor strategie-testing elke 60s.

## Status

- **crypto-data** — ✅ operationeel (pipeline, bridge, live_cache)
- **crypto-test-bot** — 📝 in ontwerpfase, architectuur gedefinieerd, nog te bouwen

## Team & Rolverdeling

```
Lexi (Owner) — beslist eindverantwoordelijk
├── Claude Code — Fullstack Software Engineer (MIT, cum laude)
│   └── complexe architectuur, refactors, core systemen
└── Noa (Hermes) — Makkelijke taken
    └── configs, documentatie, tests, simpele scripts, monitoring
```

- **Claude Code** is de fullstack software engineer, opgeleid op MIT, cum laude afgestudeerd
- **Noa/Hermes** doet de makkelijke taken: configs aanpassen, documentatie schrijven, tests draaien, simpele scripts, monitoring
- **Lexi** beslist altijd eindverantwoordelijk
- Noa schrijft nooit core strategielogica of ExecutionEngine zonder Claude Code's leiding