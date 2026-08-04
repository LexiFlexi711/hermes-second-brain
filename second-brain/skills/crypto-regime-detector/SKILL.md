# Crypto Regime Detector

## Superpower 2 — Regime detectie

Bepaal voor de actieve pairs of de markt trending, ranging of choppy is.

## Wat deze skill doet

Read-only. Gebruikt live_cache data.

Voor elk pair in de bridge watchlist:
1. Lees 4H candles uit `crypto-data/logs/live_cache/PAIREUR_240m.json`
2. Bereken ATR(14) op 4H
3. Bereken swing amplitude (laatste pivot high - laatste pivot low)
4. Vergelijk: swing amplitude > 2.5× ATR → trending | anders → ranging/choppy
5. Bepaal richting (HH+HL = long trend | LH+LL = short trend | anders = geen)
6. Toon resultaat per pair

## Output formaat

```
Pair        Regime      Richting  Swing    ATR     Ratio
BTCEUR      trending    long      2100     820     2.56×
ETHEUR      ranging     -          45      38      1.18×
ADAEUR      trending    short      0.018   0.006   3.00×
```

## Paden

```
Live cache: projects/crypto-data/logs/live_cache/
Bridge:     projects/crypto-data/logs/bridge/bridge_watchlist.json
```

## Regels

- Alleen live_cache lezen, geen API calls
- Als data stale is (>30 min): meld dit bij het pair
- Geen trade-advies — alleen regime-label
- **Rapporteer resultaat naar `second-brain/tasks/done/` als Lexi vraagt om een audit**