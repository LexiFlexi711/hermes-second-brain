---
title: Hermes update v0.20.5 + MCP reparaties (20 aug 2026)
type: fix
created: 2026-08-25
tags: [hermes, mcp, update, gateway, node]
---

# Hermes update v0.20.5 + MCP reparaties

Parallel aan het strategy-harness werk (20 aug 2026) drie problemen opgelost.

## 1. Gateway auto-restart faalde na update

`cannot import name 'line_input' from 'hermes_cli.cli_output'` bij gateway
auto-restart na update.

**Fix:** `hermes gateway restart` → PID 956674, v0.20.5 actief.
**Verificatie:** `hermes --version` → exit 0.

## 2. filesystem MCP — `--args` flag

`npm error Unknown cli flag: --args` — 5× foute `--args` in config.yaml.

**Fix:** via `hermes config set` (niet `hermes mcp add`, die annuleerde de
interactieve prompt). MCP-beveiligingsregel: filesystem allowlist max
`/home/sjoe/.hermes/skills`, nooit volledige `.hermes`.

## 3. health-monitor better-sqlite3 ABI-mismatch

Geneste better-sqlite3 binary was voor Node 24 (ABI 137) gebouwd, maar de
Hermes-node is v22 (ABI 127).

**Fix:** health-monitor command op `/usr/bin/node` v24 (ABI 137) gezet i.p.v.
Hermes-node. `npm install-scripts approve better-sqlite3` faalde (exit 1), dus
systeem-node-aanpak gebruikt. Bij systeem-node upgrade naar v25+: opnieuw
compileren.

## Node versies (belangrijk voor MCP native modules)

- `/usr/bin/node` = v24 (ABI 137)
- Hermes bundled `~/.hermes/node/bin/node` = v22 (ABI 127)

## Gerelateerd

- [[strategy-harness-evaluation-pipeline]] — werk dat hier parallel mee liep
- [[hermes-mcp-cleanup-health-monitor-fix]] — eerdere MCP/health-monitor fix
