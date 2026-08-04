---
title: MCP Tools Audit — Beslissing
type: decision
date: 2026-07-10
status: beslist
audit_scope: NeuroAPI + Toloka + Postproxy + n8n MCP
---

# 2026-07-10 — MCP Tools Audit Beslissing

## Conclusie

Geen nieuwe MCP tools installeren. Huidige setup is compleet en dekkend.
Nieuwe tools alleen toevoegen bij concrete use case + security audit + rollbackplan.

## Wat bestaat al

- **Weekly Scout**: `/home/sjoe/system/hermes-second-brain/scout/scout.py` — draait wekelijks via cron (maandag 07:00). Drie profielen: Noa (Tech/Hermes), Claude (Tech), Lexi (Opportunity/inkomsten). Output naar `raw/inbox/scout/`.
- **n8n integratie**: `n8n-webhook-trigger` + `n8n-integration` skills — curl-gebaseerde webhook en REST API calls.
- **Filesystem MCP**: Gehardened met beperkte allowlist.
- **Firecrawl**: `web_search` + `web_extract` tools.

## Per tool beslissing

| Tool | Besluit | Reden |
|------|---------|-------|
| **NeuroAPI** | LATER | Alleen evalueren als Firecrawl/browser faalt op 3 concrete News Scraper targets |
| **n8n MCP** | LATER | Interessantste kandidaat — nettere interface bovenop webhooks. Eerst security-audit nodig. |
| **GitHub MCP** | LATER | Read-only evalueren voor repo/issues/PR's. `gh` CLI dekt nu de basis. |
| **SQLite MCP** | LATER | Alleen voor aparte Opportunity Scout database — niet voor second brain. |
| **Composio** | NIET DOEN | 200+ integraties = gigantisch risico. `gh` CLI + `n8n` dekken alles af. |
| **Memory MCP** | NIET DOEN | Confliceert met bestaand `memory` tool + second brain systeem. |
| **Brave Search** | NIET DOEN | Firecrawl search is voldoende. Extra tool voegt alleen complexiteit toe. |
| **Code Execution MCP** | NIET DOEN | `execute_code` + `terminal` volstaan. |
| **Docker MCP** | NIET DOEN | Terminal + docker commands zijn genoeg. Docker socket = root-toegang = te risicovol. |
| **Cloudflare MCP** | LATER | Alleen als tunnel opnieuw problemen geeft. |
| **Playwright MCP** | NIET DOEN | Camofox `browser_*` werkt prima. |
| **Zapier MCP** | NIET DOEN | Overlapt met n8n — overbodig. |

## Regel

Geen nieuwe MCP tools zonder:
1. Concrete use case (niet "ooit handig")
2. Security audit (read-only eerst, whitelist van tools)
3. Rollbackplan (verwijderen uit config + `/new`)

## Vervolgacties (in todo.md)

- [ ] n8n MCP gerichte security-audit
- [ ] GitHub MCP read-only audit
- [ ] NeuroAPI evalueren bij 3+ Firecrawl/browser failures
