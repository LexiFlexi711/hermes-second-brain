# Crypto Journal Visual

## Superpower 8 — Chart lezen als eerste validatie

Beschrijf in woorden wat de chart liet zien voor winnende vs verliezende trades.

## Wat deze skill doet

Read-only. Lees journal data en beschrijf de marktcontext in gewone taal.

Voor de meest recente journal entries in `logs/backtest_multirun_v2/`:
1. Selecteer 5 winners en 5 losers van een opgegeven pair+strategie
2. Per trade: beschrijf wat er op de chart stond VOOR de entry:
   - Wat was de 4H trend? (richting, sterkte)
   - Waar zat de prijs in de pullback? (fib niveau, hoog/laag in retracement)
   - Wat was de trigger candle? (rejection wick, engulfing, doji)
   - Was de pullback duidelijk afgelopen of nog lopend?
3. Vergelijk patronen: wat hadden winners gemeen? Wat hadden losers gemeen?

## Output formaat

```
JOURNAL VISUELE ANALYSE — V2/ADAEUR

WINNER #1 (2024-03-15, +8.1%):
  4H trend: duidelijke downtrend, 3 opvolgende LH+LL
  Pullback: 52% retracement, prijs stond 3 candles op weerstand
  Trigger:  bearish rejection wick, body klein, wick 2× body
  Patroon:  STERK — trend duidelijk, pullback volledig, trigger scherp

LOSER #1 (2024-04-02, -2.0%):
  4H trend: matige downtrend, 1 LH zichtbaar
  Pullback: 61% retracement, prijs bewoog nog steeds omhoog
  Trigger:  bearish candle maar geen duidelijke rejection
  Patroon:  ZWAK — trend onduidelijk, pullback nog niet klaar

CONCLUSIE: Winners hadden duidelijkere trend + volledig afgewerkte pullback.
```

## Paden

```
Journal:  projects/crypto-test-bot-v3/logs/backtest_multirun_v2/
```

## Regels

- Geen nieuwe backtests draaien
- Beschrijf altijd in gewone taal, geen technisch jargon
- Geen trade-advies
- Als checks ontbreken in journal: gebruik de beschikbare data
- **Rapporteer resultaat naar `second-brain/tasks/done/` als Lexi vraagt om een audit**