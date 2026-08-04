---
title: "Hermes Context Policy"
date: 2026-07-07
type: policy
source: HERMES AUDIT 02
status: active
---

# Hermes Context Policy

**Status:** actief
**Datum:** 2026-07-07
**Bron:** HERMES AUDIT 02 — Context-hygiëne / Second-brain discipline

## Besluit

Context-hygiëne is goed genoeg.

Hermes gebruikt de second brain meestal gericht:
- index eerst
- maximaal 5 relevante notities bij second-brain lookup
- write-back met bewijs
- geen recente brede JSONL dumps
- geen volledige wiki-dumps
- AGENT_AUDIT bij taken

Wel blijven er aandachtspunten:
- raw inbox bevat veel oude bestanden
- memory zit rond 85%
- contextregels zijn vooral tekstueel en niet overal hard afgedwongen
- er ontbreken taak-specifieke harde limieten in runtime

Geen onmiddellijke cleanup nodig.

## Harde werkregel

Hermes leest nooit breed "voor de zekerheid".

Volgorde:
1. Eerst index of live status.
2. Daarna alleen relevante bestanden/logregels.
3. Eerst samenvatten.
4. Dan pas handelen.
5. Bij twijfel stoppen en Lexi vragen.

## Context-policy per taaktype

### Simpele vraag / chat
- Geen second brain tenzij expliciet gevraagd.
- Max 1 relevant bestand.
- Max 20 regels context.
- Geen logs.
- Geen oude fixnotes.

### Serverdebug
- Eerst live status/diagnose: docker ps, systemctl status, journalctl -n, ss -tuln, relevante health checks.
- Max 100 relevante logregels.
- Alleen recente logs, bij voorkeur <24u.
- Geen oude fixnotes tenzij exact dezelfde fout terugkomt.
- Geen volledige logbestanden lezen.

### Repo-wijziging
- Eerst README, projectindex of relevante documentatie.
- Max 3 relevante bronbestanden.
- Geen brede codebase-scan zonder reden.
- Voor commit/push altijd final review.

### Second-brain lookup
- Eerst wiki/index.md.
- Daarna maximaal 5 relevante notities.
- Samenvatten in max 20 regels vóór verdere actie.
- Geen volledige wiki dump.
- Geen raw JSONL dump.

### Architectuurkeuze
- Relevante huidige config.
- Laatste relevante fixnotes.
- Oude context alleen gebruiken als aantoonbaar nog geldig.
- Bij tegenstrijdigheid wint live bewijs boven oude notitie.

## Harde limieten per taak

| Type         | Max files | Max logregels | Max wiki pages |
|--------------|-----------|---------------|----------------|
| Chat         | 1         | 0             | 0              |
| Debug        | 3         | 100           | 1              |
| Repo         | 3         | 0             | 1              |
| Audit        | 5         | 120           | 5              |
| Architectuur | 5         | 50            | 3              |

## Stale-context regels

- Fixnotes ouder dan 90 dagen alleen gebruiken bij exacte match.
- Logs ouder dan 14 dagen niet lezen tenzij expliciet nodig.
- Raw inbox ouder dan 30 dagen beschouwen als stale.
- Oude context mag nooit live bewijs overschrijven.
- Bij twijfel: noteer onzekerheid en vraag toestemming voor extra context.

## Acceptatietests

| Vraag                               | Verwacht gedrag                                    |
|--------------------------------------|---------------------------------------------------|
| "waarom crasht docker X?"           | live logs/status, max 100 regels, geen wiki dump   |
| "wat was die Hermes MCP fix?"       | index → specifieke fixnote, max 1 wiki page        |
| "check repo issue"                  | README/index + max 3 files, geen hele repo         |
| "zoek in second brain naar API fix" | index → max 5 notities, max 20 regels samenvatting |
| "debug oude chart bug"              | oude fixnote alleen bij exacte match               |
| "geef laatste 3 dagen context"      | geen JSONL dump, alleen gerichte samenvatting      |
| "hey hoe gaat het?"                 | geen second brain, geen files, geen logs           |

## Do-not-change

Deze policy wijzigt niets aan:
- model default
- MCP config
- tools
- skills
- raw inbox
- memory
- runtime config

## Regel voor toekomst

Context is geen vuilnisbak.
Hermes moet minder lezen, maar beter kiezen.
