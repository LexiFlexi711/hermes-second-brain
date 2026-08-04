# Session Log — 2026-05-24: Zelf-audit & Upgrade

## Overzicht
Grote audit van Noa's skills, plugins en mogelijkheden. 19 overbodige skills verwijderd, 3 nieuwe tools geïnstalleerd.

## Opkuis
- **Verwijderd:** godmode, minecraft-modpack-server, openhue, apple/* (5), baoyu-* (3), manim-video, p5js, arxiv, research-paper-writing, llm-wiki, pretext, design-md, touchdesigner-mcp
- **Memory plugins:** enkel mem0 behouden (rest uitgesteld)

## Toegevoegd

### Plex MCP
- Config toegevoegd aan `~/.hermes/config.yaml`
- 45 tools beschikbaar (search, recently added, on deck, etc.)
- Plex token opgehaald uit Docker container
- Werkt via `npx plex-mcp-server`

### Navidrome Music (Subsonic API)
- Skill `navidrome-music` aangemaakt
- Server: Navidrome 0.61.2 op localhost:4533
- Auth: u=sjoe, p=sjoeke
- Endpoints: getArtists, getAlbumList2, getRandomSongs, search3, getGenres

### hermes-plugins (42-evey)
- 34 plugins gekopieerd naar `~/.hermes/hermes-agent/plugins/`
- Meest relevant: evey-cost-guard, evey-goals, evey-learner, evey-habits, evey-autonomy, evey-status

## Harde regels
- Docker stack is off-limits (kijken mag, veranderen niet zonder akkoord)
- n8n: Lexi gebruikt het niet zelf maar wil wél Hermes → n8n webhook skill

## Research gedaan
- awesome-hermes-agent list op GitHub
- MCP server directories
- 42-evey plugins (hermes-plugins)
- Hermes v0.14.0 — 276 commits achter op main
