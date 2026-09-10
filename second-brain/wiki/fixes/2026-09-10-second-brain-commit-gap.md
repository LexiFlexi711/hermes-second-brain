---
title: Second Brain — commit-gap 2026-08-04 → 2026-09-10
type: fix
status: opgelost
date: 2026-09-10
tags: [second-brain, git, maintenance, incident, commit-gap]
---

# Second Brain — commit-gap 2026-08-04 → 2026-09-10

## Datum + impact

- **Datum vastgesteld:** 2026-09-10
- **Impact:** MIDDEN (geen dataverlies, wel zichtbaarheids- en vertrouwensverlies)
- Lexi kreeg van Claude te horen dat er "niks nieuw" in de second brain stond sinds eind augustus.

## Symptoom

Claude (en iedere lezer van de GitHub-repo) zag geen nieuwe inhoud, terwijl er dagelijks
nieuwe bestanden gegenereerd werden.

## Oorzaak

Twee losse dingen, beide aangetroffen:

1. **Git is blijven steken.** Laatste commit = `09015e5` van **2026-08-04 13:09**.
   Daarna 147 gewijzigde/untracked bestanden, waarvan 137 untracked — ruim 5 weken
   niets gecommit en dus ook niets gepusht naar
   `github.com/LexiFlexi711/hermes-second-brain`. Wie de repo leest, ziet niets nieuws.
2. **Wiki-curatie liep achter.** De wiki-inhoud liep t/m **2026-08-26**; de periode
   27-08 → 10-09 was volledig ongeregistreerd. `wiki/index.md` vermeldde zelfs
   "Laatst bijgewerkt: 2026-07-10".

De automatische onderdelen werkten wél: `sync-sessions.py` en `sync-bot-commits.py`
rapporteerden "0 nieuwe" (state bijgewerkt 2026-09-10 05:40), en de scout/morning-analyst
schreven dagelijks (`raw/inbox/opportunity-2026-09-10.md`,
`wiki/scout/2026-09-10-morning-top5.md`). Het probleem was dus niet de generatie maar
**de curatie + het committen/pushen**.

## Omvang

| Item | Waarde |
|------|--------|
| Laatste commit | `09015e5` — 2026-08-04 13:09 |
| Gewijzigde/untracked bestanden | 147 (10 modified, 137 untracked) |
| Wiki-inhoud liep t/m | 2026-08-26 |
| Ontbrekende periode | 2026-08-27 → 2026-09-10 (~2 weken) |
| Dataverlies | geen |

## Herstel

1. `sync-sessions.py` + `sync-bot-commits.py` gedraaid (0 nieuw — al actueel).
2. Drie projectpagina's geschreven voor de onopgeslagen arcs:
   - `wiki/projects/market-situation-canonical-calendar-v0-predicates-v01.md`
   - `wiki/projects/trader-story-a1a2-story-linker-v0.md`
   - `wiki/projects/causal-snapshot-tape-v0.md`
3. `wiki/log.md` aangevuld met entries voor 2026-08-31 … 2026-09-10.
4. Index + lint + graaf opnieuw gedraaid.
5. Alles gecommit en gepusht naar `origin/main`.

## Preventie

- **Regel:** na elke significante sessie/arc → wiki-curatie + `git commit` + `git push`
  (niet enkel bestanden laten staan).
- **Check:** `git -C ~/system/hermes-second-brain log -1 --format=%ci` mag nooit meer dan
  enkele dagen oud zijn; anders is de backupketen stilgevallen.
- De bestaande 6-uurs sync dekt enkel `raw/` (sessies/bot-commits). De **wiki-curatie +
  commit** blijft een handmatige, bewuste stap — die mag niet vergeten worden.

## Bewijs

Zie de commit en `git log` in `hermes-second-brain`; wiki-entry
`wiki/log.md` → "2026-09-10 — Causal Snapshot Tape V0.2 FROZEN + second-brain commit-gap hersteld".
