# Startup Cleanup & Filesystem MCP Hardening — 2026-07-09

## Samenvatting

Volledige startup-context opgeschoond: crypto naar OPTIONAL/LEGACY, Pro als default,
filesystem MCP allowlist verkleind van `/home/sjoe` naar 4 specifieke directories.

---

## 1. Startup Cleanup

### Crypto-infra → OPTIONAL / LEGACY
- Crypto-infra check verplaatst naar OPTIONAL / LEGACY sectie
- Tradebot/backtest uit normale STATUS-output verwijderd
- Alleen getoond bij `CRYPTO_MODULE_ENABLED=true` of expliciete "check crypto"

### Model Policy
- **Pro is default** (`deepseek-v4-pro`)
- **Flash is available** (cheap/low-risk)
- **OpenRouter** reachable, manual fallback (geen auto-failover)
- personality=kawaii is cosmetisch, SOUL.md=Noa actief

### TODO Cleanup
- L3_snapshot_build fysiek verwijderd uit todo.md
- V2 grid search fysiek verwijderd uit todo.md
- News Scraper terug in normale TODO (zonder crypto-keywords)
- Crypto-edge scraping blijft legacy
- TODO-filter toegevoegd aan .hermes.md voor crypto-keywords

---

## 2. Bestanden Gewijzigd

| Bestand | Wijziging |
|---|---|
| `/home/sjoe/.hermes.md` | TODO crypto-filterregel toegevoegd |
| `/home/sjoe/scripts/model-startup-check.sh` | DeepSeek Pro check toegevoegd, labels gecorrigeerd |
| `/home/sjoe/scripts/status_overview.py` | Tradebot/backtest naar LEGACY_MODULES, MCP detectie fix |
| `/home/sjoe/system/hermes-second-brain/todo.md` | L3_snapshot_build en V2 grid search verwijderd, News Scraper label aangepast |

---

## 3. Backups

| Backup | Datum |
|---|---|
| `/home/sjoe/scripts/model-startup-check.sh.bak-20260709` | 2026-07-09 |
| `/home/sjoe/scripts/status_overview.py.bak-20260709` | 2026-07-09 |
| `/home/sjoe/scripts/status_overview.py.bak-20260709-mcpfix` | 2026-07-09 |
| `/home/sjoe/scripts/model-startup-check.sh.bak.20260615_074949` | 2026-06-15 |

---

## 4. Filesystem MCP Hardening

### Oude allowlist
```
/home/sjoe  ← veel te breed, .ssh/.gnupg/.docker allemaal bereikbaar
```

### Nieuwe allowlist
```
/home/sjoe/system/hermes-second-brain
/home/sjoe/Noa-Hermes
/home/sjoe/scripts
/home/sjoe/.hermes/skills
```

### Uitgesloten paden (NIET bereikbaar)
- `/home/sjoe/.ssh` ✅
- `/home/sjoe/.gnupg` ✅
- `/home/sjoe/.docker` ✅
- `/home/sjoe/.hermes/` (volledig) ✅
- `/home/sjoe/.hermes/state.db` ✅

### MCP Status
- Health: ✅ healthy, 228ms, 14 tools
- Runtime: npx → node (stdio)
- Server: `@modelcontextprotocol/server-filesystem`

### Commando gebruikt voor hardening
```bash
hermes mcp remove filesystem
hermes mcp add filesystem --command npx \
  --args -y \
  --args @modelcontextprotocol/server-filesystem \
  --args /home/sjoe/system/hermes-second-brain \
  --args /home/sjoe/Noa-Hermes \
  --args /home/sjoe/scripts \
  --args /home/sjoe/.hermes/skills
```

---

## 5. Resterende Waarschuwingen

- **"Self-improvement review: Patched SKILL.md"** verscheen tijdens audit — Noa heeft GEEN SKILL.md gepatcht. Mogelijk parallelle Hermes-sessie of curator-run. Onderzoek nodig.
- **Langfuse stack** staat down (5 containers), maar is optioneel
- **20 pending updates** op de server
- **NeuroAPI MCP tools** nog niet geaudit: https://neuroapi.me/blog/best-mcp-tools-for-hermes
- **filesystem MCP `list_allowed_directories`** toont nog `/home/sjoe` in huidige sessie (cached tool reference), werkt correct na `/new`

---

## 6. Volgende Aanbevolen Volgorde

1. `/new` → bevestig dat filesystem MCP hardened is (list_allowed_directories)
2. Audit "Self-improvement review" incident
3. NeuroAPI MCP-tools audit
4. Daarna pas eventueel tools installeren
