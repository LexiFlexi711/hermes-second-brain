---
title: Hermes OpenClaw Noa Agent
type: project
status: active
created: 2026-05-17
updated: 2026-05-17
related: "[[2026-05-17-hermes-yaml-prefix-fix]]"
---

# Hermes OpenClaw Noa Agent

## Doel

Een persoonlijke AI-agent bouwen voor Lexi/Noa die kan helpen met serverbeheer, coding support, n8n, projectstatus, logging, research en automatisering.

## Huidige basis

- Hermes draait op de server.
- Hermes versie: v0.14.0.
- Noa Second Brain staat in `~/system/hermes-second-brain/second-brain/`.
- Hermes gebruikt eigen memory-bestanden in `~/.hermes/`.
- Het second brain gebruikt `raw/` voor ruwe bronnen en `wiki/` voor gecureerde kennis.

## Geheugenlagen

- `~/.hermes/SOUL.md`: persoonlijkheid en gedragsregels.
- `~/.hermes/memories/USER.md`: stabiele info over Lexi.
- `~/.hermes/memories/MEMORY.md`: korte actieve kernstatus.
- `~/system/hermes-second-brain/second-brain/wiki/`: gecureerd projectbrein.
- `~/system/hermes-second-brain/second-brain/raw/`: ruwe input, nooit aanpassen.

## Harde regels

- Eerst diagnose, dan fix.
- Geen riskante shell-acties zonder expliciete toestemming.
- Geen kosten maken zonder toestemming.
- Geen projectstatus verzinnen.
- Kleine stappen.
- Belangrijke fixes en beslissingen worden gelogd.

## Belangrijke fixes

- [[2026-05-17-hermes-yaml-prefix-fix]]

## Volgende stappen

- Skills inspecteren vóór kopiëren.
- `wiki/index.md` actueel houden.
- Projectpagina’s maken voor crypto-tradebot, server, n8n en Python leerpad.
- Later eventueel Graphify of vector search toevoegen.
