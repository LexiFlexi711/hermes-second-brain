---
title: Hermes v01 — Live Flask Dashboard
type: fix
date: 2026-06-08
status: DONE
commit: 92850414
---

# Hermes v01 — Live Flask Dashboard (2026-06-08)

## Wat er gebouwd is

Flask webserver op poort 5001 met live Kraken-data en zone/S/R-detectie.

**Commit:** `92850414` — "hermes-v01: live Flask dashboard met 5m Kraken data en S/R extensie"  
**Datum:** 2026-06-08 20:47

## Bestanden

| Pad | Inhoud |
|-----|--------|
| `projects/hermes-v01/dashboard/app.py` | Flask server, routes per pair, auto-refresh |
| `projects/hermes-v01/dashboard/chart_engine.py` | Zone-detectie + S/R op live Kraken data |

## Design beslissingen

- **Data source:** Kraken public API, 5m candles → 60m aggregaat
- **Pairs:** BTCEUR, ETHEUR, SOLEUR, ADAEUR
- **Refresh:** elke 5 minuten (nieuwe gesloten 5m candle)
- **Chart-logica:** identiek aan `stable_baseline.py` — geen nieuwe detectie
- **S/R extensie:** lijnen verlengd met 25 candles als stippellijn
- **Poort:** 5001

## Voorgeschiedenis

Stap 1 (test Kraken API): 200 candles BTCEUR 60m ontvangen — structuur bevestigd.  
Stap 2 (chart_engine.py): data-input laag vervangen van lokale files naar live API.  
Stap 3 (app.py): Flask wrapper met 4 pair routes.

**Baseline:** `stable_baseline.py` (commit `002bd6c1`, 2026-06-08 19:48) is de vaste referentie.
Vaste parameters:
- ATR-band factor: dynamisch per pair `(ATR_14 / avg_close) × 100`
- Min candles per zone: 8
- Merge threshold: 1% prijsverschil, ≤3 candle gaps
- Slope threshold: 1.2% (na merging, trending zones uitgesloten)
