---
title: "Model routing — Noa routeert autonoom tussen Flash en Pro"
type: decision
date: 2026-06-29
status: active
tags: [routing, model, flash, pro, autonomie]
---

## Beslissing

Lexi heeft beslist dat Noa **autonoom** mag routen tussen Flash en Pro.

## Wat er veranderde

**Oude situatie:**
- Noa moest vragen: "type /model deepseek-v4-pro"
- Lexi switchte manueel
- Noa zei: "type /model deepseek-v4-flash" om terug te gaan

**Nieuwe situatie:**
- Noa beslist zelf of een taak Flash of Pro nodig heeft
- Geen /model commando meer van Lexi nodig
- Na elke Pro-taak switcht Noa zelf terug naar Flash

## Routing regels

| Wat | Model |
|---|---|
| Chatten, onnozel doen | Flash |
| Second brain lezen/schrijven | Flash |
| Memory checks | Flash |
| Simpele code / kleine fixes | Flash |
| Complex denkwerk / architectuur | Pro |
| Serverdebug met risico | Pro |
| Repo-wijziging / code review | Pro |
| Final review vóór commit/push | Pro |
| Autonome beslissing | Pro |
| Debuggen complexe fouten | Pro |

## Bestanden gewijzigd

1. `~/.hermes/skills/developer/pro-routing/SKILL.md` → v2.0, autonome routing
2. `Noa-Hermes/autonomous/protocols/model_routing_policy.md` → Pro toegevoegd + routing tabel
3. `~/.hermes/SOUL.md` → routing sectie toegevoegd met verwijzingen

## Bronnen

- `skill_view('pro-routing')`
- `read_file('/home/sjoe/Noa-Hermes/autonomous/protocols/model_routing_policy.md')`
- `read_file('/home/sjoe/.hermes/SOUL.md')`
