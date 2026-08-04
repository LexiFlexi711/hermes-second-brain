# Crypto Risk Manager

## Superpower 4 — Position sizing & risicobeheer

Bereken optimale positiegrootte en portfolio-risico voor de actieve trades.

## Wat deze skill doet

Read-only. Geen trade-advies, geen orders.

1. Lees open trades uit alle state files (V1, V2, V3, Range, Momentum)
2. Bereken per trade: risicobedrag = positie × SL%
3. Bereken totaal portfolio-risico (som van alle SL-risico's)
4. Detecteer correlatie-gevaar: meerdere trades in zelfde richting op zelfde pair?
5. Stel voor: hoeveel mag maximaal per trade bij SL van X% (vaste €2 risico methode)
6. Toon: als alle SL's geraakt worden, hoeveel verlies dan totaal?

## Output formaat

```
PORTFOLIO RISICO OVERZICHT
Open trades: 8

Per trade:
  V1 ADAEUR LONG  €100  SL 1.96%  → risico €1.96
  V2 TAOEUR LONG  €100  SL 3.96%  → risico €3.96
  ...

Totaal SL-risico: €18.40 (als alles geraakt wordt)
Correlatie gevaar: V1 TAOEUR SHORT + V2 TAOEUR LONG → tegengesteld!

Aanbevolen positiegrootte bij €2 risico/trade:
  SL 2% → positie €100
  SL 4% → positie €50
  SL 8% → positie €25
```

## Paden

```
State files:
  logs/pullback_state.json   (V1)
  logs/v2_state.json         (V2)
  logs/v3_state.json         (V3)
  logs/range_state.json      (Range)
  logs/momentum_state.json   (Momentum)
```

## Regels

- Geen live prijzen opvragen via API
- Gebruik cache-prijs als beschikbaar voor floating P&L
- Geen advies om trades te sluiten
- Geen claims over winstgevendheid
- **Rapporteer resultaat naar `second-brain/tasks/done/` als Lexi vraagt om een audit**