---
title: Hermes Opstart 15 — Second brain scan, todo updates, SL/TP audit taak
type: raw_session
created: 2026-05-29
status: saved_before_reboot
---

# Sessie 2026-05-29 — Noa & Lexi

## Wat gedaan

### 1. Startup-check versie 15
- `.hermes.md` aangepast: second brain scan toegevoegd bij opstart
- Bij opstart: lees wiki/log.md voor laatste 2-3 dagen, meld relevante wijzigingen
- Versie opgehoogd: opstart 14 → opstart 15

### 2. Todo.md bijgewerkt
- **Nieuw open item:** Tradebot SL/TP audit — controleer live/open-trade output SL/TP-berekening en labels.
  - LONG en SHORT apart controleren
  - Onderscheid: SL-risk vanaf entry, TP-target vanaf entry, afstand vanaf huidige prijs
  - Geen code aanpassingen — alleen audit + labelcorrectie voorstel
- Datum notatie toegevoegd met context

### 3. Claude Code samenwerking
- Lexi werkt met Claude Code aan STAP-H (tests uitbreiden)
- Claude Code is tevreden over werk
- Pending folder is leeg — taken zijn opgepikt en afgerond

### 4. MCP server voor second brain — besproken
- Huidige setup werkt (search_files, read_file, scripts)
- Geen dringende nood aan MCP server
- Skills die nog gewenst zijn: auto-writeback, session-summary, wiki-template
- Besluit: huidige setup is goed genoeg, focus eerst op taken

### 5. Continu online
- Lexi heeft aangegeven dat Hermes vanaf nu continu online blijft
- Cronjobs draaien al (status/30min, lint+nacht/4u, backtest/5:30, OHLC/0:00)

## Openstaande taken (todo.md)

**Bezig:**
- Second Brain optimalisatie

**Open:**
- Crypto-data pipeline — stale/oude paden checken
- MCP servers 0/3 alive — uitzoeken (plex, health-monitor, filesystem)
- 20 pending updates — nakijken
- Tradebot stale candles — 568 stale 15m
- Radarr + Sonarr configureren — in compose-media
- Langfuse URL mismatch — 127.0.0.1:3010 vs 192.168.1.205:3010
- Tradebot SL/TP audit — nieuwe taak (zie boven)

## Beslissingen
- Geen MCP server voor second brain nodig — huidige setup volstaat
- Second brain scan bij startup — toegevoegd aan .hermes.md