# Hermes-v03 — Status 23-jun-2026

## Structuur

hermes-v03/ (projects/hermes-v03/), server op :5001, route /v03. v01 dashboard gekilled.

```
L0_data/           → candle loader (archive/cache/live/hist), volume meegeladen
L1_fractals/       → fractal + swing detectie, prominence filter gefixt
L2_levels/         → structuur → horizontale lijnen + clustering, is_extreme gefixt
L3_labels/         → HH/LH/HL/LL labels genummerd van rechts
L4a_trendlines_recent/ → recente actieve trendlines
L4_trendlines_macro/   → major trendline detectie
L5_chart/          → HTML chart assembler, fname v03_*, x-span-clamp voor trendlines
L6_indicators/     → EMA, MA regime, MA cross (GC/DC markers)
L7_candles/        → candle micro analyse
server.py          → Flask op :5003, debug=False
static/            → lightweight-charts.js v4.1.3
```

Alle layers standalone, enkel Python stdlib + Flask + LightweightCharts.

## Fixes vandaag (23-jun)

### L1_fractals/swing.py — prominence filter reparatie
- Bug: avg_neighbor operator-precedentie (r54-55) → avg≈helft, prom≈100%, filter dood
- Fix: correcte haakjes via l_highs/r_highs, % vs % vergelijking met MIN_SWING_PROMINENCE_PCT
- Unit: prom is % (×100), min_prominence was absoluut → nu % vs %
- Threshold: MIN_SWING_PROMINENCE_PCT = 0.10% (config.py)
- Effect 60m (500 candles): 54→48 highs, 49→47 lows (6+2 extra correct gefilterd)
- _estimate_price_range() verwijderd (ongebruikt)

### L0_data/__init__.py — volume meeladen
- _load_live, _load_cache, _load_hist, _load_archive: "volume" toegevoegd aan output dicts
- Auto-mode volume-conditie vuurt nu correct (was altijd False want volume=0)
- Range-check blijft als backup

### L5_chart/__init__.py — x-span-clamp voor trendlines
- Vervangt y-clamp (klemde y1/y2 los → platte lijn op framerand)
- _clip_tl() helper: behoudt echte slope, knip X-bereik waar lijn frame kruist
- Lijn volledig buiten frame → skip
- Toegepast op L4a en L4 trendlines

### server.py
- Port: 5001 → 5003 (consistent met docstring)
- debug=True → debug=False

### L5_chart — output fname
- l88_*.html → v03_*.html

### L2_levels/classify.py — O(n²) fix
- prev_wick lookup: next(... for p in sorted_pts ...) → direct candles[prev_idx]
- Zowel highs- als lows-functie

### L2_levels/cluster.py — is_extreme (al gefixt vorige sessie)
- groups[0] → groepsgemiddelden (max_avg, min_avg)

## Nog in todo
- ATR in apart chart paneel
- GC/DC testen als strategie
- L5_chart: historische date-ranges (hardcoded 2026 weg)
- L5_chart: window-caps ook bij start/end

## Nieuwe werkwijze
Elke fix eerst als bestand.fixXX, pas na testen+goedkeuring wordt .fix het nieuwe bestand. Oude code blijft levend tot v3test.
