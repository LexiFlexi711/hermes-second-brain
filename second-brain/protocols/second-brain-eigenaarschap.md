---
title: Second Brain eigenaarschap — wie schrijft wat
type: protocol
created: 2026-05-29
updated: 2026-05-29
---

# Second Brain eigenaarschap

Afspraak om dubbele schrijfacties te vermijden tussen Claude (grote broer) en Hermes.

## Eigenaarschap per sectie

| Sectie | Eigenaar | Opmerkingen |
|--------|----------|-------------|
| `wiki/projects/crypto-test-botv3.md` | **Claude** | Architectuur, status, bugs, backtest resultaten |
| `wiki/projects/crypto-tradebot.md` | **Claude** | Architectuur, traders, bugs, implementaties |
| `wiki/projects/weekly-scout.md` | **Hermes** | Scout configuratie en resultaten |
| `tasks/pending/STAP-*.md` | **Claude** schrijft specs | Hermes leest en voert uit |
| `tasks/done/STAP-*.md` | **Hermes** schrijft resultaten | Claude leest en verifieert |
| `protocols/` | **Claude** | Architectuur-afspraken |
| `raw/inbox/scout/` | **Hermes** | Weekly scout output |

## Regels

1. **Hermes schrijft nooit naar wiki/projects/** tenzij Claude dat expliciet vraagt.
2. **Claude schrijft nooit naar tasks/done/** — dat is Hermes haar werkgebied.
3. **Tasks/pending/** schrijft Claude, Hermes leest alleen.
4. **Bij twijfel:** Hermes schrijft naar `raw/inbox/` en Claude verwerkt naar de juiste plek.

## Periodieke cleanup

Claude en Lexi checken samen af en toe:
- Dubbele entries in wiki bestanden
- Verouderde pending taken
- Done taken ouder dan 30 dagen (archiveren of verwijderen)

## Doel

Eén bron van waarheid per onderwerp. Geen conflicterende versies.
