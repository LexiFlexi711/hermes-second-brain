# L4 SNAPSHOT READOUT CONTRACT v2

**Datum:** 2026-07-09
**Status:** Contract — geen prototype, geen code, geen Analyst

## 1. Doel

Een L4 snapshot is een bevroren as-of marktbeeld. Het bevat wat Hermes op dat moment kon zien — geen voorspelling, geen trade.

Kernregel:

Context is geen trigger. Support is geen buy. Resistance is geen short.
Candle rejection is geen confirmed reversal. Compression is geen breakout.
Local bounce is geen macro trend change.

## 2. Scope

Dit contract geldt voor read-only uitleg op basis van één L4 snapshot.

**Toegestaan:**
- snapshot samenvatten
- data kwaliteit beschrijven
- timeframe-aanwezigheid beschrijven
- support/resistance tonen
- candle-context beschrijven
- indicatorvelden benoemen
- structurevelden benoemen
- onzekerheden benoemen
- conflicten tussen timeframes benoemen

**Verboden:**
- tradeadvies, entry, exit, long, short, buy, sell
- take profit, stop loss
- trade confidence, win probability
- strategie-aanbeveling, voorspelling als feit

## 3. Beschikbare inputvelden

### Snapshot top-level
- snapshot_id, pair, asof_ts, stored_at
- timeframes_present, completeness / all_5_present

Precisie: snapshot-level age_seconds is afgeleid door inspector uit stored_at. Timeframe freshness zit per timeframe/meta (source_age_seconds, tf_age_seconds indien aanwezig).

### Source / provenance
- source_class, source_resolved, source_age_seconds
- source_generated_at, source_requested
- raw_hash, raw_size_bytes
- warnings / diagnostics

### Candles / price

Bewezen: meta.candles_final=240, price.current en price.previous bestaan.

**Hard feit:** De volledige 240-candle-array zit NIET in de L4 snapshot.

Betekenis:
- meta.candles_final=240 betekent dat Hermes berekende op basis van 240 candles
- Niet dat 240 candles opgeslagen zijn
- price.current en price.previous zijn dicts (laatste/voorlaatste candle-context)
- price.current en price.previous zijn GEEN candle-array

Consequentie:
- Readout mag alleen current/previous price/candle-context citeren
- Readout mag geen historische candle-array tonen
- Analyst kan indicators niet herberekenen uit snapshot alleen
- Analyst kan alleen opgeslagen indicatorvelden lezen, tenzij externe OHLC heropgehaald

### Indicators
EMA, ATR, ADX, VWAP, Volume

Indicators mogen gelezen/beschreven als bestaande velden. Niet herberekend.

### Candle micro
body_trend, patterns, micro_state, wick_bias, etc.

Candle_micro is context, geen trigger.

### Structure

**Bevestigd aanwezig:**
- structure_points met HH/HL/LH/LL labels
- recent_structure met last_high_label, last_low_label
- swing_highs, swing_lows
- fractals, labels

Regel: HH/HL/LH/LL-labels alleen noemen wanneer letterlijk aanwezig in de data.

### Support / resistance

**Expliciet aanwezig:**
- levels.nearest_support
- levels.nearest_resistance
- levels.below_price → support candidates
- levels.above_price → resistance candidates
- levels.clusters_raw → alle S/R
- structure.swing_lows → structurele support
- structure.swing_highs → structurele resistance
- trendlines.recent.lower/upper → dynamische S/R

### Trendlines
trendlines.recent.lower, trendlines.recent.upper, trendlines.major

## 4. Wat Hermes WEL mag zeggen

### Source / data quality
"Snapshot is compleet: 5/5 timeframes, meta.candles_final=240 per TF, source_age_seconds aanwezig."

### Timeframe-overzicht
"1m/5m geven lokale context; 60m/240m geven hogere structuurcontext. TFs mogen elkaar tegenspreken."

### Price / candles
- Laatste open/high/low/close uit price.current
- Vorige open/high/low/close uit price.previous
- Candle richting, body/wick-context indien in candle_micro
- meta.candles_final als bewijs van berekeningsbasis

**Niet:** "De 240 candles in de snapshot tonen..." want die array zit er niet in.

### Structure
- Swing highs/lows, structure_points aanwezig
- HH/HL/LH/LL indien letterlijk aanwezig
- recent_structure met labels

### Support / resistance
"Prijs bevindt zich tussen nearest_support en nearest_resistance."

### Indicators
Welke indicatorgroepen beschikbaar zijn, indicatorstaat beschrijven.

**Niet:** "Indicator geeft entry/bevestigt trade/voorspelt richting."

## 5. Wat Hermes NIET mag zeggen

**Verboden woorden:** buy, sell, long, short, entry, exit, TP, SL, stop loss, take profit,
trade now, confirmed trade, guaranteed, win probability, high confidence trade,
profitable setup, strategy says enter, live signal.

**Verboden claims:**
- "support houdt dus kopen"
- "resistance breekt dus long"
- "bullish reversal confirmed"
- "breakout confirmed"
- "trend change confirmed"
- "high confidence"
- "setup is bewezen" zonder outcome/backtest
- "de laatste 240 candles in de snapshot tonen..."

## 6. Verplichte nuance

- Structure is geen bias
- Bias is geen trigger
- Regime is geen trade
- Support is geen buy
- Resistance is geen short
- Candle rejection is geen reversal-confirmatie
- Compression is geen breakout
- Local bounce is geen trendomkeer
- Timeframe-conflict is normaal
- 240 candles berekend ≠ 240 candles opgeslagen

## 7. Confidence-regel

**Geen trade-confidence.**

Toegestaan: data_quality_confidence, source_confidence, completeness_confidence, readout_confidence.

Niet: trade_confidence, entry_confidence, win_probability, setup_confidence, signal_confidence.

## 8. Toegestane formuleringen

Goed:
- "De snapshot is compleet en auditbaar."
- "Prijs bevindt zich tussen nearest_support en nearest_resistance."
- "1m toont lokale candle-context; hogere TF-context moet apart gelezen worden."
- "S/R-context is aanwezig, maar L4 neemt geen tradebesluit."
- "Candle_micro toont wick-reactie; dit is context, geen trigger."
- "Timeframes zijn niet automatisch aligned."
- "meta.candles_final toont berekening op 240 candles; de array zelf zit niet in de snapshot."

Fout:
- "Long setup confirmed." / "Short setup confirmed."
- "Support houdt, dus kopen." / "Resistance rejection, dus short."
- "Bullish reversal confirmed." / "Breakout confirmed."
- "High confidence trade." / "Dit is een goede entry."
- "De 240 candles in de snapshot tonen..."

## 9. Readout outputvorm (toekomstig)

```
PAIR:
SNAPSHOT:
ASOF:
SOURCE:
DATA QUALITY:
TIMEFRAMES:
PRICE CURRENT/PREVIOUS:
STRUCTURE:
SUPPORT / RESISTANCE:
TRENDLINES:
CANDLES / CANDLE_MICRO:
INDICATORS:
CONFLICTS / UNCERTAINTY:
WHAT THIS DOES NOT SAY:
```

"WHAT THIS DOES NOT SAY" altijd:
- Geen entry/exit/long/short/buy/sell
- Geen tradebeslissing/voorspelling
- Geen bewezen strategie
- Geen historische candle-array in snapshot

## 10. Onzekerheden / ontbrekende velden

**NIET AANWEZIG:**
- Volledige 240-candle-array
- Regime, bias, MTF alignment
- Outcome Builder, Strategy Test Harness, Analyst, Trader

**Nog niet standaard in readout:**
- distance_pct, tested/broken/retest status
- zone_width, explicit MTF alignment view

Consequentie ontbrekende candle-array:
- Readout citeert current/previous price/candle-context
- Readout leest opgeslagen indicatoren, herberekent niet
- Analyst kan niet claimen volledige candlehistoriek uit snapshot te lezen

## 11. Relatie met latere Analyst

Snapshot Readout is de poort vóór Analyst.

- Snapshot Readout: beschrijft wat in de snapshot staat, geen trade-oordeel
- Analyst later: weegt context pas na aparte contractfase
- Trader nog later: pas na paper trading + bewezen audit

**Architectuurgrens beslist:** De ADR `raw/sessions/2026-07-09-snapshot-readout-location-adr.md` is leidend.

Die ADR kiest Optie B: Snapshot Readout wordt Analyst A0 / poortlaag.

Interpreter blijft data/geheugen/inspectie. Er wordt nog geen prototype gebouwd.

## 12. Conclusie

L4 bevat genoeg voor betrouwbare context-readout: current/previous price, indicators, candle_micro, structure met HH/HL, explicit S/R, trendlines, source/provenance.

L4 bevat NIET: 240-candle-array, regime, bias, MTF alignment, outcome, tradebeslissing.

L4 geeft geen toestemming voor: entry, exit, long, short, buy, sell, trade confidence, live trading.

Volgende stap: architectuurbeslissing over prototype-locatie — maar nog niet bouwen.
