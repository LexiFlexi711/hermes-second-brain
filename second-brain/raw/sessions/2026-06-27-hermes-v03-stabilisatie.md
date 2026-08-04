# Sessie 27 juni 2026 — Hermes v03 stabilisatie

## Wat gebouwd/gefixt

- **L8_synthesis**: Nieuwe laag die alle bestaande layers (L0-L7) assembleert in 1 JSON-object. Serveert via `/v03/data?pair=ETHEUR&tf=15m`. Eigen directory, standalone imports, geen wrapper van L5_chart.
- **MA-cross alignment**: `calculate_ma_cross()` in L6_indicators herschreven met auto-detect input type. Timestamp-aligned mode (set intersection op timestamps) ipv index-based (14 candles offset bug). Backward compat voor float input.
- **Candle-window afknijping verwijderd**: `effective_limit()` geeft altijd `limit_requested` terug. Geen verborgen 60m→80 / 240m→30 meer. De gebruiker bepaalt hoeveel candles.
- **L7_candles stabilisatie**: `micro_state()` deterministisch zonder `[0]` tie-break, bij gelijkstand expliciet `"mixed"`. `wick_bias()` gebruikt EPS + WICK_DOMINANCE ipv magic 99.0 fallback.
- **L3_labels**: `.index()` op dicts vervangen door `enumerate()` — geen duplicate numbering bij identieke dicts.
- **`_parse_dt()` multi-format**: Ondersteunt nu ISO (`2026-06-20 00:00`), ISO compact (`2026-06-20T00:00`), Europees met jaar (`20/06/2026 00:00`), en legacy `dd/mm HH:MM` (huidig UTC jaar). Geen hardcoded 2026 meer.
- **`_candle_window.py`**: Gedeelde helper voor L5_chart en L8_synthesis. `load_window()` regelt effective_limit, data laden, date filter, slicing, window-info.

## Structuur

```
projects/hermes-v03/
  _candle_window.py        # gedeelde candle window loading
  L0_data/                 # data laag
  L1_fractals/             # fractal/swing detectie
  L2_levels/               # structuur → levels → clusters
  L3_labels/               # HH/LH/HL/LL labels (van rechts genummerd)
  L4a_trendlines_recent/   # recente actieve trendlines
  L4_trendlines_macro/     # major trendlines
  L5_chart/                # HTML chart rendering
  L6_indicators/           # EMA, ATR, ADX, VWAP, Volume
  L7_candles/              # candle micro analyse
  L8_synthesis/            # JSON data API (nieuw)
  tools/
    verify_ma_cross_alignment.py
  server.py                # Flask op :5001
```

## Nog open

- L9_strategy: multi-timeframe combinatie (15m + 1H + 4H → 1 beslissing)
- VWAP naar subchart verhuizen (Lexi wil)
- calculation/display window split (design audit gedaan, nog niet gebouwd)
- 240m met default 240 candles is veel voor chart, maar analyse is beter

## Server

- Draait op UTC, Lexi is CEST (UTC+2)
- Local: `http://192.168.1.205:5001/v03?pair=ETHEUR&tf=15m`
- Data JSON: `http://192.168.1.205:5001/v03/data?pair=ETHEUR&tf=15m`
