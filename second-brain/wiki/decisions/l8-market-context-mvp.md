# Besluit: L8 Market Context MVP (L8A)

**Datum:** 2026-06-16
**Status:** Goedgekeurd door Lexi

## Scope

L8A = direction + relative returns + market wind + coin behavior.
Enkel Hermes interne laag. Geen route, dashboard, tradebot-consumptie, Layer 9.

## Niet in scope

- correlatie / beta
- nieuws / catalysts
- Layer 9 Validation Lab
- /v8/ route in app_dashboard.py
- dashboard-visualisatie
- tradebot-consumptie
- extra indicatoren

## Architectuur

- Map: `projects/hermes-v01/layer8_market_context/`
- Module: `market_context.py` met `read_market_context(pair, timeframe) -> dict`
- Director: `read_layer8(pair, timeframe) -> dict`
- Tests: `tests/test_layer8_market_context.py`

## Data

- BTC/ETH candles via `fetch_kraken("BTCEUR", timeframe)` en `fetch_kraken("ETHEUR", timeframe)`
- Fallback naar live_cache JSON indien API faalt
- Closed candle policy: candles[-1] uitsluiten voor return berekeningen

## Output velden L8A

- pair_direction: "up|down|sideways|unknown"
- btc_direction: "up|down|sideways|unknown"
- eth_direction: "up|down|sideways|unknown"
- pair_return_pct: float
- btc_return_pct: float
- eth_return_pct: float
- relative_strength_vs_btc: "outperforming|underperforming|in_line|unknown"
- relative_strength_vs_eth: "outperforming|underperforming|in_line|unknown"
- market_wind: "supportive|hostile|neutral|mixed|unknown"
- coin_behavior: "following_market|resilient|weak|decoupled|unknown"

## Verboden output

buy, sell, long, short, entry, exit, signal, setup, take profit, stop loss, trade
(ook Nederlandse varianten: koop, verkoop, instap, uitstap, signaal, trade)
