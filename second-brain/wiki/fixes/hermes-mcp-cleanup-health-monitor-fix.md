---
title: "Hermes MCP Cleanup + Health-Monitor Fix"
date: 2026-07-07
type: fix
component: hermes-mcp
status: resolved
---

# Hermes MCP Cleanup + Health-Monitor Fix

**Datum:** 2026-07-07

## Probleem

- 12 MCP processen ipv 6 — 6 oude Jul06 zombies naast 6 actieve
- health-monitor MCP: config bug — `args` was dict ipv list → connection failed
- Status check toonde "1/3 alive" terwijl plex + filesystem wél draaiden

## Oplossing

### 1. Oude processen gekilled

| Server | Gekilde PIDs |
|--------|-------------|
| plex-mcp-server | 44638, 44675, 44676 |
| server-filesystem | 44651, 44683, 44684 |

Geverifieerd via `ps -fp` — alle 6 exact MCP processen van Jul06 (PPID 1841839).

### 2. health-monitor config fix

**FOUT:**
```yaml
args:
  '0': /home/sjoe/.hermes/mcp-local/...dist/index.js
```

**GOED:**
```yaml
args:
  - /home/sjoe/.hermes/mcp-local/...dist/index.js
```

Oorzaak: YAML dict (`'0': value`) ipv list (`- value`). Hermes verwacht `list_type`, kreeg `dict`.

### 3. Backup

```
~/.hermes/config.yaml.backup-mcp-health-20260707_162407
```

## Validatie

### `hermes mcp test`

| Server | Status | Tools | Connectie |
|--------|--------|-------|-----------|
| plex | ✅ | 45 | 1326ms |
| filesystem | ✅ | 14 | 1741ms |
| health-monitor | ✅ | 8 | 315ms |

### MCP reload
- 69 tools uit 3 MCP servers
- Agent updated: alle tools beschikbaar

## Regel voor toekomst

- `hermes mcp list` — bewijst alleen config-enabled, niet echte connectie
- `hermes mcp test` — de waarheid voor echte verbinding
- Bij MCP-processen: altijd `ps -fp` PID + command verifiëren vóór kill
