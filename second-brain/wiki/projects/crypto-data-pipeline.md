---
title: Crypto Data Pipeline
type: project
created: 2026-05-30
updated: 2026-05-30
status: active
---

# Crypto Data Pipeline

Project: `crypto-data` — eigenaar van alle marktdata, universe selectie, OHLC archief en live cache.
Pad: `/mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/projects/crypto-data/`

Traders in `crypto-tradebot` consumeren de output van dit project. Ze schrijven nooit zelf naar de exchange API.

---

## Stroom: universe selectie

```
KRAKEN API
    │
    ▼
universe_selector.py              Stap 1 — haalt ALLE Kraken EUR pairs op
    │                             output: logs/universe_selector.json
    ▼
universe_selector_normalisatie.py Stap 2 — normaliseert pairnamen
    │                             output: logs/universe_selector_normalisatie.json
    ▼
universe_liquidity_filter.py      Stap 3 — gooit illiquide pairs weg
    │                             output: logs/universe_liquidity_filter.json
    ▼
universe_scorer.py                Stap 4 — scoort resterende pairs op bruikbaarheid
    │                             output: logs/universe_scorer.json
    ▼
universe_watchlist.py             Stap 5 — curated lijst voor de traders
                                  output: logs/universe_watchlist.json
```

`universe_pipeline.py` — draait stap 1–4 in één keer (`--loop` = elke 60s)
`universe_delta.py` — bewaakt wat er verandert in de watchlist

---

## Stroom: OHLC data

```
WATCHLIST
    │
    ▼
universe_ohlc_bridge.py           draait continu, elke 60s
    │  - leest candidate-verzoeken van traders (logs/bridge/vN_request.json)
    │  - bepaalt welke pairs gevolgd worden (met grace period van 35 min)
    │  - doet 1 Kraken OHLC call per pair (geen duplicaten)
    │  - schrijft naar:
    │      logs/live_cache/PAIREUR_NNm.json      rolling, traders lezen live
    │      ohlc_archive/PAIREUR_NNm.jsonl        groeiend, backtest leest dit
    │
live_data_cache.py                geen standalone script — module die traders importeren
                                  shared OHLCV cache, één Kraken call per pair/interval per TTL
```

---

## Stroom: historische data

```
import_historical.py              eenmalig — importeer Kraken CSV dumps (zip)
                                  output: logs/historical_csv/
                                  29.4M candles, 2015 → maart 2026
                                  Q2 2026 volgt eind juni

nightly_ohlc_backfill.py          nachtelijk — vult gaten in ohlc_archive
                                  leest pairs uit universe_watchlist.json
                                  pagineert automatisch (max 720 candles per request)
                                  output: ohlc_archive/ aangevuld
                                  auditlog: logs/backfill/
```

---

## Kandidaten (parallel)

```
candidate_universe.py             twee lagen:
                                  CANDIDATE_UNIVERSE     — breed, 7 bronnen:
                                    1. CORE_WATCH_UNIVERSE  (vaste top 10)
                                    2. LEXI_TOP_COINS       (persoonlijke watchlist)
                                    3. TOP_NEW_LISTINGS     (research-only)
                                    4. TOP_VOLATILE
                                    5. TOP_GAINERS
                                    6. TOP_LOSERS
                                    7. TOP_LIQUIDITY
                                  ACTIVE_TRADE_UNIVERSE  — effectieve scanlijst per 15 min

market_universe_scanner.py        scoort pairs op volatiliteit + liquiditeit
                                  scorecomponenten: volatility_pct, avg_range_pct,
                                  movement_score, liquidity_score, noise_penalty,
                                  data_completeness
                                  output: logs/market_universe/
```

---

## Wat loopt er continu

| Script | Wat | Frequentie |
|---|---|---|
| `universe_pipeline.py --loop` | universe stap 1–4 | elke 60s |
| `universe_ohlc_bridge.py` | candles fetchen + archiveren | elke 60s |
| `nightly_ohlc_backfill.py` | gaten dichten in archief | elke nacht |

---

## Wat lezen de traders

| Bestand | Wat |
|---|---|
| `logs/universe_watchlist.json` | welke pairs scannen |
| `logs/live_cache/PAIREUR_NNm.json` | live candles (rolling) |
| `ohlc_archive/PAIREUR_NNm.jsonl` | historische candles (backtest) |
| `logs/bridge/vN_request.json` | trader schrijft hier zijn gewenste pairs |

---

## Zie ook

- [[crypto-tradebot]] — traders die deze data consumeren
- [[crypto-test-botv3]] — test-bot die ohlc_archive + historical_csv gebruikt via BacktestReader
