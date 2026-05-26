---
title: Team Meeting 006 - Hermes & Server Setup Review (GECORRIGEERD)
type: synthesis
created: 2026-05-19
---

# TEAM MEETING 006 — HERMES & SERVER SETUP REVIEW (GECORRIGEERD)

## CORRECTIE OP EERDER RAPPORT
Eerder rapport bevatte 2 fouten:
1. "Slechts 1 skill" — FOUT. Er zijn **29 skills** in `~/.hermes/skills/`
2. "Geen gateway/plugins" — FOUT. Er zijn **18 plugins** in `~/.hermes/hermes-agent/plugins/`

Oorzaak: `skills_list` met category filter, en verkeerd ls-pad.

## HERMES SETUP — WAT WERKT

### Skills (29 totaal)
`~/.hermes/skills/`: agent, agent-core, agent-orchestration, apple, autonomous-ai-agents, creative, crypto-trading, data-science, devops, diagramming, dogfood, domain, email, gaming, gifs, github, hermes-agent, inference-sh, mcp, media, mlops, note-taking, productivity, red-teaming, research, smart-home, social-media, software-development, yuanbao

### Plugins (18 totaal)
`~/.hermes/hermes-agent/plugins/`: browser, context_engine, disk-cleanup, example-dashboard, google_meet, hermes-achievements, image_gen, kanban, memory, model-providers, observability, platforms, spotify, teams_pipeline, video_gen, web

### Overige config
| Onderdeel | Status |
|-----------|--------|
| Model | ✅ Flash default |
| Provider | ✅ OpenRouter |
| Gateway | ✅ Aanwezig in hermes-agent codebase (`gateway/` folder) |
| Kanban | ✅ Plugin aanwezig voor multi-agent |
| Cron | ✅ Scheduler aanwezig in hermes-agent/cron/ |
| Memory plugins | ✅ honcho, mem0, supermemory? in plugins/memory/ |
| MCP | ✅ MCP skill aanwezig |

## WAT NOG NIET ACTIEF/GEÏNTEGREERD IS

| Feature | Status | Wat nodig |
|---------|--------|-----------|
| Kanban board | Plugin aanwezig, niet actief | Configuratie + cron |
| Gateway platform | Code aanwezig, geen platform actief | Config per platform (telegram/discord/etc) |
| Cron jobs | Scheduler aanwezig, geen jobs | Hermes cron configureren |
| delegation tool | DISABLED in config | `disabled_toolsets` aanpassen |
| session_search | DISABLED in config | Idem |
| vision | DISABLED in config | Idem |

## SERVER — WAT WERKT

15 Docker containers draaien: caddy, n8n, plex, nextcloud, navidrome, qbittorrent, netdata, mail, redis, chromium, webdav, watchtower, talk-hpb, webssh, youtube-api.

## AANBEVOLEN VOLGORDE

| Prioriteit | Actie |
|-----------|-------|
| 1 | Eerst pullback script laten werken |
| 2 | Skills aanmaken voor pullback + meeting workflow |
| 3 | delegation + session_search inschakelen in config |
| 4 | Gateway configureren voor platform |
| 5 | Cron jobs voor pullback scan |

## BESLISSING
Focus eerst op pullback bot. Skills en config optimalisatie daarna.

---

## Zie ook
- [[hermes-openclaw-noa-agent]]
- [[secretary-agent]]
