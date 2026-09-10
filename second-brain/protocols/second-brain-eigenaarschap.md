---
title: Second Brain eigenaarschap — wie schrijft wat
type: protocol
created: 2026-05-29
updated: 2026-05-29
---

# Second Brain eigenaarschap

Afspraak om dubbele schrijfacties en conflicterende waarheid te vermijden tussen Noa/ChatGPT, Claude en Hermes. `SECOND_BRAIN.md` is bovenliggend wanneer deze oudere tabel ermee botst.

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

1. **Noa/ChatGPT, Claude en Hermes mogen duurzame kennis terugschrijven** wanneer hun opdracht dat vereist en het bewijs duidelijk is.
2. **Claude schrijft reviewer-output primair naar `wiki/reviews/` of `wiki/audits/`** en niet naar `tasks/done/`.
3. **Hermes schrijft uitvoeringsresultaten primair naar `tasks/done/`**, maar mag relevante project/fix/status-wiki bijwerken wanneer dat onderdeel is van de opdracht.
4. **Noa/ChatGPT bewaakt cross-project architectuur, beslissingen en consistentie** en schrijft die terug naar de passende wiki/decision/protocol-pagina.
5. **Bij twijfel of onvolledig bewijs:** schrijf eerst naar `raw/inbox/`; promoveer pas naar `wiki/` na verificatie.

## Periodieke cleanup

Claude en Lexi checken samen af en toe:
- Dubbele entries in wiki bestanden
- Verouderde pending taken
- Done taken ouder dan 30 dagen (archiveren of verwijderen)

## Doel

Eén bron van waarheid per onderwerp. Geen conflicterende versies.
