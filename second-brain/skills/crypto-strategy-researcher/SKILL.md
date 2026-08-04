# Crypto Strategy Researcher

## Superpower 10 — Continuous learning

Scan en vat samen welke nieuwe strategie-inzichten relevant zijn voor dit project.

## Wat deze skill doet

Combineert interne data met externe context om leeropportuniteiten te signaleren.

1. Lees de meest recente journal scanner rapporten (`logs/journal/daily_report_*.txt`)
2. Toon de actuele alarmen en patronen
3. Lees de Weekly AI Scout output als die beschikbaar is
4. Vergelijk actuele strategieresultaten met de 10-strategieën-lijst in second brain
5. Stel max. 3 concrete volgende onderzoeksvragen voor op basis van de data

## Output formaat

```
STRATEGIE RESEARCH UPDATE — 2026-05-31

INTERNE SIGNALEN (journal scanner):
  ⚠ V1/V2 WR < 25% — SL te krap (49% ruis-stops)
  ⚠ BILLEUR +26% buiten bridge gemist

ACTUELE STRATEGIE STATUS:
  V2: beste resultaat (+21% gem. PnL, 2 jaar data) → verder valideren
  Momentum: nog niet getest in testbot
  Failed breakout: nog niet geïmplementeerd

VOLGENDE ONDERZOEKSVRAGEN:
  1. Werkt V2 ook op BTCEUR en ETHEUR? (nu testen)
  2. Wat maakt een pullback "klaar" vs "te vroeg"? (journal analyse)
  3. Is er een momentum-equivalent dat werkt zoals de BTC 15M moves?

AANBEVELING: focus op V2-validatie voor nieuwe strategieën toe te voegen.
```

## Paden

```
Journal rapporten: projects/crypto-tradebot/logs/journal/
Second brain:      /home/sjoe/system/hermes-second-brain/second-brain/
Scout output:      projects/crypto-test-bot-v3/research/ (als beschikbaar)
```

## Regels

- Geen code schrijven
- Geen backtests draaien
- Max 3 onderzoeksvragen — focus, niet verstrooien
- Evidence first — baseer vragen op data, niet op gevoel
- **Rapporteer resultaat naar `second-brain/tasks/done/` als Lexi vraagt om een audit**