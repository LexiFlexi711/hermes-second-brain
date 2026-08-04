---
title: Crypto Tradebot
type: project
created: 2026-04-29
updated: 2026-05-28
status: active
---

# Crypto Tradebot

Multi-pair crypto trading bot op Kraken exchange. Twee projecten samenwerken:
- `crypto-data` — eigenaar van API, universe, bridge, live_cache, ohlc_archive
- `crypto-tradebot` — consumer van data; traders, selectors, webapp

## Architectuur (mei 2026)

6-staps pipeline in `crypto-data`:
1. Universe scanner → kandidaatpairs
2. Scorer → gescoorde shortlist
3. Selector → gefilterde tradeable pairs
4. OHLC bridge → live_cache opslaan per pair/timeframe
5. Bridge → verwerkt request-files van traders
6. Nightly backfill → vult OHLC-gaten aan

## Traders (crypto-tradebot)

| Script | Strategie | Screen |
|--------|-----------|--------|
| `pullback_trader.py` | V1 pullback | v1 |
| `pull_backtrader_2.py` | V2 pullback + trailing SL | v2 |
| `pull_backtrader_3.py` | V3 pullback | v3 |
| `range_trader.py` | Range | range |
| `momentum_trader.py` | Momentum | momentum |

## Selectors

V1/V2/V3/range selectors draaien als screen-sessies (v1sel, v2sel, v3sel, rangesel).
Schrijven request-files naar `crypto-data/logs/bridge/`.

## Kritieke paden

| Variabele | Pad |
|-----------|-----|
| `_CACHE_DIR` / `_LIVE` | `crypto-data/logs/live_cache/` |
| `_BRIDGE_DIR` | `crypto-data/logs/bridge/` |
| `_SCORED_PATH` | `crypto-data/logs/scored_pairs.json` |

## Webapp

`noa_webapp.py` draait op screen `webapp`, port 5000.
Gebruikt `cache_freshness.py` → leest van `crypto-data/logs/live_cache/`.

## Bekende valkuil: module-reload na code-wijziging

Python laadt gedeelde modules eenmalig in memory. Na een commit die `cache_freshness.py`, `universe_candidates.py` of andere imports wijzigt, moeten draaiende traders **herstart** worden — anders gebruiken ze de oude versie.

Symptoom: traders tonen STALE-warnings en sluiten geen trades.
Fix: `kill -INT <pid>` + nieuwe screen sessie.

Zie [[2026-05-29-stuck-trades-cache-freshness-in-memory-bug]] voor volledig incident.

## Sessie 2026-05-29 — trailing stop + MFE/MAE analyse

### Bridge fix: incomplete candles
`universe_ohlc_bridge.py` schreef lopende (niet-gesloten) candles naar het archief.
Fix: `archive_new` filtert candles waar `timestamp + interval * 60 > now`.
`_cleanup_incomplete_candles()` draait bij bridge-startup (verwijderde 282 slechte candles).

### MFE/MAE analyse (STAP-L)
Script: `scripts/mfe_mae_analyse.py`
Output: `logs/mfe_mae/mfe_mae_analyse.json` + `mfe_mae_rapport.md`

Bevinding: V1-verliezers stonden gem. +4.61% in winst voor ze verlies werden.
7/14 V1-verliezers stonden minstens +1% groen.

### Exit simulatie (STAP-M)
Script: `scripts/exit_sim.py`
Output: `logs/mfe_mae/exit_sim_resultaten.json` + `exit_sim_rapport.md`

| Strategie | Origineel | Met trailing | Verbetering |
|-----------|-----------|--------------|-------------|
| V1 | -18.07% | +36.88% | +54.95% |
| V2 | -25.12% | +9.58% | +34.70% |
| Momentum | +13.65% | +10.66% | -2.99% → NIET aanpassen |

### Trailing stop geïmplementeerd (STAP-N)
`pullback_trader.py` (V1) en `pull_backtrader_2.py` (V2) uitgebreid:
- Break-even bij +1% floating PnL → SL naar entry
- Trailing stop bij +2% → trail 1% achter beste koers
- `trailing_sl` en `trail_best` opgeslagen in state JSON
- Logging: `[BE]` en `[TRAIL]` in console

V3, Momentum en Range: **niet aangepast**.
Herstart: 2026-05-29 22:09 UTC — geen open trades op moment van herstart.

## Zie ook

- [[pullback-trader-strategy]]
- [[2026-05-28-data-bridge-migratie-git-cleanup]]
- [[2026-05-29-stuck-trades-cache-freshness-in-memory-bug]]
- [[crypto-test-bot-architectuur]] — nieuwe modulaire test-bot (in ontwerp)
