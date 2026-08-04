# A0 SNAPSHOT READOUT

## HEADER

pair: ETHEUR
snapshot_id: ETHEUR-1783755060-1m5m15m60m240m-03efcd474fea
asof: 2026-07-11T07:31:00+00:00
stored_at: 2026-07-11T07:32:16+00:00
snapshot_version: 1
contract_version: snapshot_contract_version: missing

## DATA QUALITY

timeframes_present: 5/5
completeness: YES
  1m: candles_final=240, source_age=13s
  5m: candles_final=240, source_age=21s
  15m: candles_final=240, source_age=23s
  60m: candles_final=240, source_age=23s
  240m: candles_final=240, source_age=23s

## TIMEFRAMES

[1m]
  stored_value meta.candles_final: 240
  stored_value meta.source_age_seconds: 13
  stored_value meta.source_resolved: auto_archive_plus_cache
  stored_value meta.source_class: mixed
  stored_value price.current.close: 1577.41
  stored_value price.current.open: 1577.41
  stored_value price.current.high: 1577.41
  stored_value price.current.low: 1577.41
  stored_value price.previous.close: 1577.07

[5m]
  stored_value meta.candles_final: 240
  stored_value meta.source_age_seconds: 21
  stored_value meta.source_resolved: auto_archive_plus_cache
  stored_value meta.source_class: mixed
  stored_value price.current.close: 1577.41
  stored_value price.current.open: 1576.77
  stored_value price.current.high: 1577.41
  stored_value price.current.low: 1576.64
  stored_value price.previous.close: 1576.74

[15m]
  stored_value meta.candles_final: 240
  stored_value meta.source_age_seconds: 23
  stored_value meta.source_resolved: auto_archive_plus_cache
  stored_value meta.source_class: mixed
  stored_value price.current.close: 1577.41
  stored_value price.current.open: 1576.77
  stored_value price.current.high: 1577.41
  stored_value price.current.low: 1576.64
  stored_value price.previous.close: 1576.74

[60m]
  stored_value meta.candles_final: 240
  stored_value meta.source_age_seconds: 23
  stored_value meta.source_resolved: auto_archive_plus_cache
  stored_value meta.source_class: mixed
  stored_value price.current.close: 1577.41
  stored_value price.current.open: 1575.24
  stored_value price.current.high: 1577.62
  stored_value price.current.low: 1574.0
  stored_value price.previous.close: 1575.29

[240m]
  stored_value meta.candles_final: 240
  stored_value meta.source_age_seconds: 23
  stored_value meta.source_resolved: auto_archive_plus_cache
  stored_value meta.source_class: mixed
  stored_value price.current.close: 1577.41
  stored_value price.current.open: 1573.44
  stored_value price.current.high: 1578.39
  stored_value price.current.low: 1571.76
  stored_value price.previous.close: 1573.67

## PRICE CONTEXT

  1m: o=1577.41 h=1577.41 l=1577.41 c=1577.41
  5m: o=1576.77 h=1577.41 l=1576.64 c=1577.41
  15m: o=1576.77 h=1577.41 l=1576.64 c=1577.41
  60m: o=1575.24 h=1577.62 l=1574.0 c=1577.41
  240m: o=1573.44 h=1578.39 l=1571.76 c=1577.41

## STRUCTURE

  timeframe: 1m
  stored_value structure.recent_structure.last_high_label: START
  stored_value structure.recent_structure.last_high_price: 1578.34
  stored_value structure.recent_structure.last_low_label: START
  stored_value structure.recent_structure.last_low_price: 1571.76

## SUPPORT / RESISTANCE


## TRENDLINES


## CANDLE MICRO

  timeframe: 1m
  stored_value candle_micro.body_trend: mixed
  stored_value candle_micro.micro_state: strong_body_dominant
  stored_value candle_micro.wick_bias: lower_wicks
  stored_value candle_micro.patterns[0].pattern: strong_body
  stored_value candle_micro.patterns[0].direction: bearish
  stored_value candle_micro.patterns[1].pattern: bullish_engulfing
  stored_value candle_micro.patterns[1].direction: bullish
  stored_value candle_micro.patterns[2].pattern: bearish_engulfing
  stored_value candle_micro.patterns[2].direction: bearish

## INDICATORS

  timeframe: 1m
  stored_value indicators.adx.adx: 50.74
  stored_value indicators.adx.di_bias: bullish
  stored_value indicators.adx.minus_di: 12.09
  stored_value indicators.adx.plus_di: 44.45
  stored_value indicators.adx.trend_strength: strong
  stored_value indicators.atr.atr_pct: 0.0245
  stored_value indicators.atr.value: 0.3857
  stored_value indicators.atr.volatility_state: low
  stored_value indicators.ema.fast_last: 1576.74
  stored_value indicators.ema.slow_last: 1576.29
  stored_value indicators.volume.avg_volume: 1.546
  stored_value indicators.volume.current_volume: 0.0249
  stored_value indicators.volume.spike: False
  stored_value indicators.volume.strong_spike: False
  stored_value indicators.volume.volume_empty: False
  stored_value indicators.volume.volume_ratio: 0.02
  stored_value indicators.volume.volume_trend: falling
  stored_value indicators.vwap.bars_used: 240
  stored_value indicators.vwap.lower_band: 1574.1857
  stored_value indicators.vwap.std_dev: 1.4425
  stored_value indicators.vwap.upper_band: 1577.0707
  stored_value indicators.vwap.value: 1575.6282
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
