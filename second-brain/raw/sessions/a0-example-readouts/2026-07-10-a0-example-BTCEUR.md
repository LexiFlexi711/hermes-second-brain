# A0 SNAPSHOT READOUT

## HEADER

pair: BTCEUR
snapshot_id: BTCEUR-1783755060-1m5m15m60m240m-0adbeece8251
asof: 2026-07-11T07:31:00+00:00
stored_at: 2026-07-11T07:32:19+00:00
snapshot_version: 1
contract_version: snapshot_contract_version: missing

## DATA QUALITY

timeframes_present: 5/5
completeness: YES
  1m: candles_final=240, source_age=30s
  5m: candles_final=240, source_age=30s
  15m: candles_final=240, source_age=30s
  60m: candles_final=240, source_age=30s
  240m: candles_final=240, source_age=30s

## TIMEFRAMES

[1m]
  stored_value meta.candles_final: 240
  stored_value meta.source_age_seconds: 30
  stored_value meta.source_resolved: auto_archive_plus_cache
  stored_value meta.source_class: mixed
  stored_value price.current.close: 56236.1
  stored_value price.current.open: 56232.1
  stored_value price.current.high: 56236.1
  stored_value price.current.low: 56232.0
  stored_value price.previous.close: 56237.9

[5m]
  stored_value meta.candles_final: 240
  stored_value meta.source_age_seconds: 30
  stored_value meta.source_resolved: auto_archive_plus_cache
  stored_value meta.source_class: mixed
  stored_value price.current.close: 56236.1
  stored_value price.current.open: 56228.8
  stored_value price.current.high: 56237.9
  stored_value price.current.low: 56228.7
  stored_value price.previous.close: 56228.8

[15m]
  stored_value meta.candles_final: 240
  stored_value meta.source_age_seconds: 30
  stored_value meta.source_resolved: auto_archive_plus_cache
  stored_value meta.source_class: mixed
  stored_value price.current.close: 56236.1
  stored_value price.current.open: 56228.8
  stored_value price.current.high: 56237.9
  stored_value price.current.low: 56228.7
  stored_value price.previous.close: 56228.8

[60m]
  stored_value meta.candles_final: 240
  stored_value meta.source_age_seconds: 30
  stored_value meta.source_resolved: auto_archive_plus_cache
  stored_value meta.source_class: mixed
  stored_value price.current.close: 56236.1
  stored_value price.current.open: 56225.2
  stored_value price.current.high: 56240.0
  stored_value price.current.low: 56186.5
  stored_value price.previous.close: 56221.1

[240m]
  stored_value meta.candles_final: 240
  stored_value meta.source_age_seconds: 30
  stored_value meta.source_resolved: auto_archive_plus_cache
  stored_value meta.source_class: mixed
  stored_value price.current.close: 56236.1
  stored_value price.current.open: 56184.7
  stored_value price.current.high: 56290.2
  stored_value price.current.low: 56125.3
  stored_value price.previous.close: 56185.3

## PRICE CONTEXT

  1m: o=56232.1 h=56236.1 l=56232.0 c=56236.1
  5m: o=56228.8 h=56237.9 l=56228.7 c=56236.1
  15m: o=56228.8 h=56237.9 l=56228.7 c=56236.1
  60m: o=56225.2 h=56240.0 l=56186.5 c=56236.1
  240m: o=56184.7 h=56290.2 l=56125.3 c=56236.1

## STRUCTURE


## SUPPORT / RESISTANCE


## TRENDLINES


## CANDLE MICRO

  timeframe: 1m
  stored_value candle_micro.body_trend: contracting
  stored_value candle_micro.micro_state: strong_body_dominant
  stored_value candle_micro.wick_bias: lower_wicks
  stored_value candle_micro.patterns[0].pattern: strong_body
  stored_value candle_micro.patterns[0].direction: bearish
  stored_value candle_micro.patterns[1].pattern: strong_body
  stored_value candle_micro.patterns[1].direction: bullish
  stored_value candle_micro.patterns[2].pattern: strong_body
  stored_value candle_micro.patterns[2].direction: bearish

## INDICATORS

  timeframe: 1m
  stored_value indicators.adx.adx: 23.01
  stored_value indicators.adx.di_bias: bullish
  stored_value indicators.adx.minus_di: 15.54
  stored_value indicators.adx.plus_di: 21.44
  stored_value indicators.adx.trend_strength: weak
  stored_value indicators.atr.atr_pct: 0.0157
  stored_value indicators.atr.value: 8.8143
  stored_value indicators.atr.volatility_state: low
  stored_value indicators.ema.fast_last: 56231.26
  stored_value indicators.ema.slow_last: 56227.62
  stored_value indicators.volume.avg_volume: 0.0542
  stored_value indicators.volume.current_volume: 0.0224
  stored_value indicators.volume.spike: False
  stored_value indicators.volume.strong_spike: False
  stored_value indicators.volume.volume_empty: False
  stored_value indicators.volume.volume_ratio: 0.41
  stored_value indicators.volume.volume_trend: rising
  stored_value indicators.vwap.bars_used: 240
  stored_value indicators.vwap.lower_band: 56175.4174
  stored_value indicators.vwap.std_dev: 29.1078
  stored_value indicators.vwap.upper_band: 56233.6331
  stored_value indicators.vwap.value: 56204.5253
  stored_value indicators.vwap.volume_empty: False

## FIELD LIMITATIONS

De volledige 240-candle-array zit NIET in de snapshot.
meta.candles_final=240 betekent: berekend op basis van 240 candles.
Het betekent NIET: 240 candles opgeslagen in snapshot.
A0 toont alleen opgeslagen velden uit de whitelist.
Geen indicatoren herberekend. Geen candles gereconstrueerd.

## SCOPE NOTES

Dit is geen entry.
Dit is geen buy/sell-signaal.
Dit is geen long/short-advies.
Dit is geen tradebeslissing.
Dit is geen voorspelling.
Support betekent niet 'kopen'.
Resistance betekent niet 'verkopen'.
Deze context rechtvaardigt geen trade.
