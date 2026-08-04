---
title: "MOA unknown toolset — opgelost"
type: fix
created: 2026-06-26
fixed_by: Noa (Hermes)
severity: low
---

# Fix: "Warning: Unknown toolsets: moa"

## Symptoom
Hermes gaf bij elke startup de melding `Warning: Unknown toolsets: moa`.

## Oorzaak
In `~/.hermes/config.yaml` stond onder `platform_toolsets.cli` het item `- moa`. "moa" (Mixture of Agents) is een toolset die **off by default** staat en in deze Hermes build niet beschikbaar is als actieve toolset. Hermes kon het niet resolven, vandaar de warning.

## Fix
Lijn 654 (`  - moa`) verwijderd uit `platform_toolsets.cli` in `~/.hermes/config.yaml` met `sed -i '654d'`.

Config bleef geldig YAML na fix.

## Herkomst
"moa" stond in de config via een oude paste/meeting-samenvatting (paste_9_123516.txt, mei 2026) waar het als tool genoteerd stond. Later blijkbaar in de config blijven hangen.

## Impact
- ✅ Warning verdwijnt na restart (`/reset` of nieuwe hermes sessie)
- ✅ Geen functionele impact — toolset was toch niet beschikbaar
- ✅ Config blijft geldig
