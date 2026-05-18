---
title: Hermes YAML prefix fix
type: fix
project: Hermes / Noa-agent
date: 2026-05-17
sources: raw/inbox/2026-05-17-hermes-yaml-fix.md
related: "[[hermes-openclaw-noa-agent]]"
---

# Hermes YAML prefix fix

## Probleem

Hermes startte met een YAML parse warning:

Failed to parse /home/sjoe/.hermes/config.yaml

Daardoor viel Hermes terug op de default config en werden eigen overrides zoals providers, fallback chain en modelinstellingen genegeerd.

## Oorzaak

~/.hermes/config.yaml bevatte per ongeluk gekopieerde lijnprefixes zoals:

- 1|model:
- 10|- hermes-cli

Die prefixes maakten de YAML ongeldig.

## Fix

De prefixes zijn verwijderd uit ~/.hermes/config.yaml.

Daarna gaf de Python YAML-test:

YAML OK

## Status

- Hermes versie: v0.14.0
- Config YAML: geldig
- Aandachtspunt: shell environment toonde geen zichtbare OpenRouter/API-key variabelen

## Les

Bij YAML-fouten altijd eerst met lijnnummers en yaml.safe_load() valideren voor er aan Hermes zelf wordt gesleuteld.
