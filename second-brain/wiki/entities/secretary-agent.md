---
title: Secretary Agent
type: entity
created: 2026-05-18
---

# Secretary Agent

## Rol
Meeting Secretary / Notulist / Vergaderleider. Leidt vergaderingen, bewaakt de agenda en noteert alle gesprekken, beslissingen, twijfels, conflicten en actiepunten.

## Verantwoordelijkheden
- Start en sluit vergaderingen
- Bewaakt agenda
- Noteert per agent wat gezegd werd
- Noteert conflicten, open vragen, beslissingen, actiepunten
- Maakt leesbaar MD verslag + machineleesbare JSON notulen
- Verifieert dat beide bestanden op disk staan

## Locatie
`~/Noa-Hermes/autonomous/agents/secretary.md`

## Output
- `.md` verslag naar `~/Noa-Hermes/autonomous/meetings/meeting_{id}.md`
- `.json` notulen naar `~/Noa-Hermes/autonomous/meetings/meeting_{id}.json`

## Gedocumenteerde meetings
- [[meeting-002]]
- [[meeting-008]]
- [[team-meeting-005-pullback-strategy]]
- [[team-meeting-006]]
- [[2026-05-19-pullback-strategy-meeting]]

## Zie ook
- [[hermes-openclaw-noa-agent]]
