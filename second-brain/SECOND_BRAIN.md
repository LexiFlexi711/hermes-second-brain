---
title: Second Brain — gedeeld contract
type: protocol
status: active
updated: 2026-09-10
---

# Second Brain — gedeeld contract

Dit is de gedeelde, duurzame kennisbron voor Lexi, Noa/ChatGPT, Claude en Hermes.

## Rollen
- **Lexi** — eigenaar en eindbeslisser.
- **Noa / ChatGPT** — architect, sparringpartner en finale technische beslisser binnen opdrachten van Lexi; leest én onderhoudt de second brain.
- **Claude** — onafhankelijke reviewer; verifieert, falsificeert, auditeert en schrijft eigen bevindingen terug.
- **Hermes** — executor/coder; voert afgebakend werk uit, verzamelt bewijs en schrijft uitvoeringsresultaten terug.

## Harde werkregel
**Read before work. Update after meaningful work.**

Bij bestaand projectwerk:
1. Lees eerst `00_HOME.md`, de relevante projectpagina en relevante protocolpagina.
2. Zoek gericht; laad nooit blind het volledige brain in context.
3. Voer het werk uit op basis van broncode, data en bewijs — niet op verouderde samenvattingen alleen.
4. Schrijf duurzame nieuwe kennis terug na betekenisvol werk.
5. Werk `wiki/log.md` en waar nodig `wiki/index.md` bij.
6. Niet gecommit/gepusht is geen betrouwbare backup. De uitvoerende agent meldt expliciet wanneer commit/push nog ontbreekt.

## Wat hoort erin
- architectuur- en ontwerpbeslissingen
- projectstatus die met bewijs is vastgesteld
- fixes, incidenten en bekende technische schuld
- audit- en reviewbevindingen
- runbooks en terugkerende procedures
- relevante open loops en volgende stappen

## Wat hoort er niet in
- wachtwoorden, API keys, tokens of andere secrets
- tijdelijke console-output zonder blijvende waarde
- ongefilterde logdumps als gecureerde wiki-kennis
- aannames die als feiten worden gepresenteerd

## Bronnenhiërarchie bij conflict
1. Lexi's expliciete actuele beslissing
2. actuele broncode/data/config + reproduceerbaar bewijs
3. dit contract en actieve protocols
4. actuele gecureerde wiki-pagina
5. raw/sessiehistoriek

Bij conflict wordt de oudere gecureerde tekst niet stil overschreven: corrigeer haar met datum, bewijs en reden.

## Schrijfgebieden
- `raw/` = bronmateriaal; na opname niet muteren.
- `wiki/` = gecureerde kennis.
- `wiki/reviews/` en `wiki/audits/` = Claude-review/audit-output.
- `wiki/projects/`, `wiki/fixes/`, `wiki/decisions/`, `wiki/concepts/` = gedeelde gecureerde kennis; Noa en Hermes mogen deze bijwerken wanneer hun opdracht dit vereist en het bewijs duidelijk is.
- `tasks/pending/` = afgebakende taakspecificaties.
- `tasks/done/` = uitvoeringsresultaten.

## Toegang
Desktop Commander op `lexi-server` is beperkt tot:
`/mnt/otherdrive1/dataLexi/LexiProjects`

De second brain die binnen deze toegestane projectroot wordt gebruikt staat hier:
`/mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/second-brain`

Als documentatie een ander historisch pad noemt, mag niet worden aangenomen dat dit dezelfde fysieke kopie is zonder verificatie. Vermijd split-brain.
