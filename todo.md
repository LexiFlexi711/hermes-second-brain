# TODO — Noa & Lexi

> Automatisch beheerd via Hermes startup-check.
> Bron: `~/system/hermes-second-brain/todo.md`
> Laatste update: 2026-07-10 (Hermes sessie — rootdisk cleanup + torrentz migratie)

---

## ✅ Vandaag afgerond

- [x] **Rootdisk cleanup — Torrentz SSD leftovers** — 48G vrijgemaakt, 10 films naar SATA, qBittorrent paden geverifieerd
- [x] **.hermes state-snapshot archive** — 557M snapshot naar SATA, secret-files uit archive verwijderd
- [x] **.hermes state.db audit** — 557M, 54K messages, dubbele FTS-indexering, geen VACUUM nodig
- [x] **Hermes-v03-interpreter project opgestart** — aparte directory, contract.md, L1_validate
- [x] **schema_version toegevoegd** aan Hermes-v03 L8_synthesis (versie 1)
- [x] **L1_validate geschreven en getest** — 5/5 tests geslaagd
- [x] **Pro-routing skill v2.0** — Flash voor simpele code, Noa routeert autonoom
- [x] **Pro-routing updated** — Noa zegt vooraf als ze naar Pro gaat
- [x] **MCP Tools Audit (NeuroAPI + Toloka + Postproxy + n8n)** — 12 tools beoordeeld, beslisnota in wiki/decisions, geen installaties
- [x] **n8n MCP gerichte audit** — security-analyse: instance-level MCP read-only, MCP Server Trigger per workflow, Bearer auth. Advies: LATER
- [x] **Weekly Scout uitbreiding (optic A)** — hermes_releases.py, crypto-filter (alleen Lexi), n8n/MCP termen, Hermes release sectie. 59 items testrun, cron ongemoeid
- [x] **Hermes release audit v2026.7.7.2** — we draaien er al op (v0.18.2), WhatsApp fix, geen impact
- [x] **Real multi-agent capability audit** — delegate_task = echt (ThreadPoolExecutor), kanban = leeg, 20 papieren agenten, 1 echte worker (Weekly Scout)
- [x] **Real delegation smoke test** — deleg_98159754, child deepseek-v4-flash, 52.94s, 4 API calls, vond risico's die parent miste. Delegation werkt.
- [x] **Verified delegation policy vastgelegd** — wiki/governance/2026-07-10-verified-delegation-policy.md, AGENT_AUDIT_V2 verplicht, geen synthetic agents
- [x] **Self-improvement review incident audit** — approval gates actief (memory + skills), 3 pending proposals veilig gestaged
- [x] **Filesystem MCP hardening geverifieerd** — allowlist correct, 3 paden, geen .hermes volledig
- [x] **3 pending skill proposals geaccepteerd** — 77a87232 (hermes-self-audit), dd458b38 (self-improvement-review), 9d220ce5 (server-administration)

## 🔄 Bezig

- [x] **Opportunity Scout bouwen** — derde profiel toegevoegd aan weekly scout (Lexi/Opportunity). Google News RSS + Reddit opportunity. Draait wekelijks. ✅
- [x] **News Scraper maken** — beslist: géén apart script. Weekly Scout uitgebreid met Hermes releases + n8n/MCP termen + crypto-filter. ✅

## ⏳ Open

- [ ] **Website ontwerpen voor website business** — ontwerp + landing page voor eigen website/bureau
- [ ] **Turbo Express BE website herontwikkelen** — herontwerp/ rebuild van turboexpress.be
- [ ] **Vakantie-aanvraag automail** — script dat automatisch mail naar werk stuurt om 00:00:30 om vakantie aan te vragen (voor juli 2026)
- [ ] **Second Brain optimalisatie** — gebruik, opslaan en bijhouden verbeteren
- [ ] **Pending updates server nakijken** — 76 stuks (Docker 29.5.3→29.6.2, NVIDIA security, Brave, systeem). ⚠️ Thuis doen — Docker herstart = 2-3 min downtime.
- [ ] **Radarr + Sonarr configureren** — in compose-media
- [ ] **NeuroAPI evalueren** — pas bij 3+ Firecrawl/browser failures op concrete News Scraper targets. Nu geen actie.
- [x] **"Self-improvement review" incident audit** — SKILL.md patch tijdens read-only audit ✅ 2026-07-10: approval gates actief, background review geblokkeerd, 3 pending proposals veilig gestaged
- [x] **Filesystem MCP hardening controleren** — na /new, allowlist beperken tot skills/ en tweede brein ✅ 2026-07-10: allowlist correct, 3 paden, geen .hermes volledig


