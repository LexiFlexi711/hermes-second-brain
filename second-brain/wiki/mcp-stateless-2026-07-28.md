# MCP Stateless — 2026-07-28 Spec

**Bron:** mcp-use v2 blog (Manufact, 29 juli 2026) + MCP spec announcement
**Datum gescout:** 2026-08-07
**Score:** 10/10 — grootste MCP-wijziging sinds launch

## Wat veranderde

De MCP-specificatie `2026-07-28` maakte het protocol **stateless**:

- **Geen `initialize` handshake meer** — elke request is self-contained
- **Geen `Mcp-Session-Id`** — geen sticky sessions naar één server-instantie
- **Geen session state** in het transport — state is nu expliciet onderdeel van de applicatie
- **`server/discover`** voor capability discovery (optioneel)
- **Multi Round-Trip Requests** vervangen de oude aanname van open connecties

Praktisch: een load balancer kan elk request naar elke instance sturen zonder iets van sessies te weten.

## Impact op onze stack

| Component | Huidig | Na migratie |
|-----------|--------|-------------|
| filesystem MCP | stateful | stateless — geen sessie per client |
| Plex MCP | stateful | idem |
| health-monitor MCP | stateful | idem |
| Hermes Agent | v2026.8.3 (oude spec?) | checken bij release notes |

## mcp-use v2 (referentie-implementatie)

- **Package split:** `mcp-use` (server), `@mcp-use/client`, `@mcp-use/agent`, `@mcp-use/inspector`
- **Footprint:** 405 MiB → 74 MiB (-83%)
- **Snelheid:** 25% sneller dan v1
- **Auto-negotiatie:** client probeert stateless, valt terug op oude flow
- **React integratie:** `McpClientProvider`, `useMcpClient`, `useMcpServer`, `ViewRenderer`

## Actie

- [ ] Checken of Hermes v2026.8.3 de nieuwe spec ondersteunt
- [ ] Bij volgende Hermes release: MCP spec versie verifiëren
- [ ] Niet zelf migreren — wachten op Hermes-adoptie

## Gerelateerd

- [[MCP authorization server]] — FusionAuth MCP auth (2026-08-11)
- [[HoneyMCP]] — Deception layer voor MCP (2026-08-12)
- [[mcpvessel]] — Untrusted MCP servers caged (2026-08-06)
