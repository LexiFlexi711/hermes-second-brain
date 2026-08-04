---
title: "Hermes Health-Monitor Policy"
date: 2026-07-07
type: policy
source: HERMES AUDIT 04
status: active
---

# Hermes Health-Monitor Policy

**Status:** actief
**Datum:** 2026-07-07
**Bron:** HERMES AUDIT 04 — Health-monitor benutten

## Besluit

Health-monitor is bruikbaar, maar alleen als MCP meta-monitor.

Belangrijkste regel:

**Health-monitor bewaakt MCP servers, niet de volledige server.**

Het mag dus nooit gebruikt worden als bewijs dat CPU, RAM, disk, Docker, systemd of netwerkpoorten gezond zijn.

## Wat health-monitor WEL bewaakt

Health-monitor ziet:
- MCP servers alive/offline
- MCP latency
- MCP tool count
- MCP degraded status
- MCP tool schema drift
- MCP historiek/latency trends

Voor huidige setup: plex MCP, filesystem MCP, health-monitor MCP.

## Wat health-monitor NIET bewaakt

Health-monitor ziet niet:
- CPU load
- RAM-gebruik
- diskgebruik
- swap
- Docker container status
- Docker logs
- systemd services
- netwerkpoorten
- mountproblemen
- zombie/duplicate processen
- Plex scan-load
- algemene servergezondheid

Voor die zaken blijft shellbewijs verplicht.

## Beschikbare tools

| Tool | Gebruik |
|------|---------|
| `health_check_all` | Snelle check of MCP servers alive zijn |
| `get_server_status` | Status van één specifieke MCP server |
| `list_degraded` | MCP servers vinden die offline of traag zijn |
| `check_updates` | Tool schema drift controleren na wijzigingen/upgrades |
| `get_history` | Historiek/latency trends bekijken |
| `export_dashboard` | Visueel MCP-dashboard maken |
| `configure_server` | MCP server toevoegen — niet zonder expliciete opdracht |
| `remove_server` | MCP server verwijderen — niet zonder expliciete opdracht |

## Wanneer health-monitor eerst gebruiken

- "MCP doet raar" of "MCP tools zijn weg"
- "zijn de MCP servers alive?"
- na MCP wijziging of Hermes upgrade
- bij vermoeden van MCP latency
- bij tool schema drift
- bij intermitterende MCP problemen

## Wanneer shell verplicht blijft

Shell blijft verplicht bij:
- "server is traag", "disk bijna vol", "RAM bijna op", "CPU/load hoog"
- Docker container crasht, Plex doet raar
- poort luistert niet, service start niet
- vóór kill/restart/configwijziging/deployment
- vóór conclusies met risico

Voorbeelden shellbewijs: `uptime`, `free -h`, `df -h`, `docker ps`, `docker logs`, `systemctl status`, `journalctl`, `ss -tuln`, `ps`.

## Overlapregels

| Diagnosevraag | Eerste stap |
|---------------|-------------|
| "server traag" | shell: uptime/free/top |
| "docker container crasht" | shell: docker ps + docker logs |
| "disk vol?" | shell: df -h |
| "poort luistert niet" | shell: ss -tuln |
| "MCP doet raar" | health-monitor + hermes mcp test |
| "MCP tools verdwenen?" | check_updates + hermes mcp test |
| "MCP latency hoog?" | get_history + hermes mcp test |
| "alles ok?" | korte gecombineerde check: MCP + shell |

## Drempels

| Metriek | Warning | Critical |
|---------|---------|----------|
| MCP latency | >1000ms | >3000ms |
| MCP tools changed | altijd melden | — |
| MCP error count | >0 in 24u | >5 in 24u |
| degraded servers | 1 | >1 |

Deze waarden zijn praktische richtlijnen, geen absolute waarheid.

## Korte "alles ok?" check

Bij algemene statusvraag maximaal 5 checks:
1. `health_check_all` — MCP alive?
2. `list_degraded` — MCP traag/offline?
3. `docker ps` — containers ok?
4. `df -h` — disk ok?
5. `uptime` / `free -h` — load en RAM ok?

Geen diepe debug tenzij één van deze checks afwijkend is.

## Harde regel

Health-monitor output mag nooit shellbewijs vervangen voor acties met risico.

Bij twijfel: **shell wint.**

- Niet killen op basis van health-monitor.
- Niet herstarten op basis van health-monitor alleen.
- Niet concluderen dat "de server gezond is" omdat MCP gezond is.
- Niet concluderen dat Docker/Plex/systemd ok zijn zonder shellbewijs.

## Acceptatietests

| Vraag | Verwacht gedrag |
|-------|----------------|
| "server is traag" | shell eerst: uptime/free/top, niet health-monitor |
| "Plex doet raar" | docker/logs eerst, health-monitor alleen voor MCP-connectie |
| "MCP tools weg?" | check_updates + hermes mcp test |
| "disk bijna vol?" | df -h, want health-monitor ziet geen disk |
| "mag ik proces killen?" | nooit zonder ps/live bewijs |
| "alles ok?" | korte gecombineerde check, geen diepe debug |
| "container crasht" | docker ps + docker logs blijft leidend |
| "MCP latency hoog?" | get_history voor trend, hermes mcp test voor bevestiging |

## Do-not-change

Deze policy wijzigt niets aan: MCP config, startup-check, services, processen, model default, repo code, git hooks, systemd, Docker.

## Regel voor toekomst

Health-monitor is geen dokter voor de server. Het is een thermometer voor MCP.
