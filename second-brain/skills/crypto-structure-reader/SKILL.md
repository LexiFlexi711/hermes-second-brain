# Crypto Structure Reader

## Superpower 3 — Marktstructuur lezen

Lees de marktstructuur van een pair: pivots, swing levels, HH/HL/LH/LL patroon.

## Wat deze skill doet

Read-only. Vraag: welk pair?

1. Lees 4H candles (laatste 60) uit live_cache
2. Detecteer pivot highs en lows (venster n=2)
3. Toon de laatste 4 pivots chronologisch
4. Label: HH/HL (uptrend) | LH/LL (downtrend) | gemengd (geen trend)
5. Toon waar prijs nu staat t.o.v. de structuur:
   - Boven laatste pivot high → at_top / potential breakout
   - Tussen pivots → pullback_zone
   - Onder laatste pivot low → at_bottom / potential breakdown
6. Geef ook: is structuur intact of gebroken?

## Output formaat

```
ADAEUR — 4H Marktstructuur
Pivot 1: HIGH 0.2340  (2026-05-28)
Pivot 2: LOW  0.1980  (2026-05-29)  ← lager low = downtrend bevestigd
Pivot 3: HIGH 0.2180  (2026-05-30)  ← lager high = downtrend bevestigd
Pivot 4: LOW  0.1950  (2026-05-31)  ← lager low

Label: LH+LL → SHORT TREND
Huidige prijs: 0.2040 → IN PULLBACK (tussen pivot 3 en 4)
Structuur: INTACT (geen close boven 0.2180)
```

## Paden

```
Live cache: projects/crypto-data/logs/live_cache/
```

## Regels

- Geen signaal genereren — alleen structuur beschrijven
- Als minder dan 20 4H candles: "te weinig data"
- Altijd exact de candle timestamps tonen
- **Rapporteer resultaat naar `second-brain/tasks/done/` als Lexi vraagt om een audit**