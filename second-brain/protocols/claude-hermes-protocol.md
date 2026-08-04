---
title: Claude ↔ Hermes Taakprotocol
type: protocol
status: active
created: 2026-05-29
---

# Claude ↔ Hermes Taakprotocol

Claude leidt de architectuur. Hermes voert afgebakende taken uit.
Communicatie verloopt via de second brain task queue.

## Mappenstructuur

```
second-brain/tasks/
├── pending/   ← Claude schrijft hier taakspecs
└── done/      ← Hermes schrijft hier resultaten
```

## Workflow

1. Claude schrijft taak naar `tasks/pending/STAP-X-naam.md`
2. Lexi zegt tegen Hermes: **"Volgende taak in second brain"**
3. Hermes leest `tasks/pending/`, voert de eerste taak uit
4. Hermes schrijft resultaat naar `tasks/done/STAP-X-naam.md`
5. Hermes verwijdert het bestand uit `tasks/pending/`
6. Lexi zegt tegen Claude: **"Hermes klaar"**
7. Claude leest `tasks/done/`, besluit volgende stap

## Taakspec formaat (pending/)

```markdown
---
stap: A
naam: kort-beschrijvend
project: crypto-test-botv3
prioriteit: hoog
status: pending
geschreven-door: Claude
---

## Doel
Één zin wat er gebouwd moet worden.

## Bestand
Exact pad van het aan te passen of aan te maken bestand.

## Huidige staat
Wat er al staat (of: bestand bestaat nog niet).

## Te bouwen
Exacte code of interface die toegevoegd moet worden.

## Imports beschikbaar
Welke modules mag Hermes importeren.

## Test
Exacte commando's om te verifiëren dat het werkt.
Verwachte output erbij.

## Mag NIET
Wat Hermes niet mag aanraken.
```

## Resultaatformaat (done/)

```markdown
---
stap: A
naam: kort-beschrijvend
status: done | failed | partial
uitgevoerd-door: Hermes
---

## Wat gedaan
Concrete beschrijving van wat uitgevoerd is.

## Testresultaat
Exacte output van de test.

## Afwijkingen
Wat anders liep dan de spec beschreef (of: geen).

## Volgende stap aanbeveling
Optioneel: wat Hermes aanraadt als volgende.
```

## Regels

- Hermes voert ALLEEN uit wat in de taakspec staat
- Hermes raakt geen bestanden aan die niet in de spec staan
- Hermes schrijft altijd een resultaatbestand, ook bij fouten
- Claude leest het resultaat vóór de volgende taak te schrijven
- Eén taak tegelijk in pending/ (tenzij expliciet parallel)
