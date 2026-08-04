# L8A Build — 2026-06-16

**Status:** Gebouwd en getest.
**Tests:** 20 L8A specifiek, alle 233 bestaande tests blijven passen.

## Wat is gebouwd

1. `projects/hermes-v01/layer8_market_context/__init__.py` — leeg, markeert module
2. `projects/hermes-v01/layer8_market_context/market_context.py` — read_market_context()
3. `projects/hermes-v01/director/hermes_director.py` — read_layer8()
4. `projects/hermes-v01/tests/test_layer8_market_context.py` — 20 tests

## Wat L8A kan

- direction (up/down/sideways/unknown) voor pair, BTCEUR, ETHEUR
- return_pct voor pair, BTCEUR, ETHEUR (gesloten candles)
- relative_strength_vs_btc/eth (outperforming/underperforming/in_line)
- market_wind (supportive/hostile/neutral/mixed)
- coin_behavior (following_market/resilient/weak/decoupled)

## Wat L8A NIET is

- Geen route (/v8/)
- Geen dashboard
- Geen tradebot-consumptie
- Geen strategie/signaal
- Geen correlatie/beta
- Geen Layer 9

## Closed candle policy

`closed_candle_policy: "excludes candles[-1]"`
Returns berekend over `candles[:-1]`.

## Foutafhandeling

- pair_data_unavailable, btc_data_unavailable, eth_data_unavailable
- pair_too_few_closed_candles (< MIN_CANDLES=5)
- btc_too_few_closed_candles, eth_too_few_closed_candles
- quality: clean | limited_lookback | error
