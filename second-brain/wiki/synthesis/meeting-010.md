# TEAM MEETING 010 — Noa Super Bot: Skills, Patches & Upgrades

## Doel
Bepalen welke skills, patches, upgrades en tools Noa nodig heeft om van assistent naar super bot te gaan.

## Aanwezige Rollen (Virtueel)
- **Scout (Hermes)** — inventarisatie
- **Skills Agent (Hermes)** — skill-analyse
- **QA Agent (Hermes)** — kwaliteitscontrole
- **Controller (Hermes)** — synthese en prioriteiten
- **Strategist (Hermes)** — roadmap
- **Secretary (Hermes)** — documentatie
- **Lexi** — Owner, live meevolgend

---

## ITERATIE 1 — Scout: Huidige staat

| Component | Status |
|-----------|--------|
| 98 skills beschikbaar | ✅ Groot arsenaal |
| Subagents / delegate_task | ✅ Max 3 concurrent |
| Second brain | ✅ wiki/raw/synthesis |
| Model routing (Flash/Pro/Free) | ✅ actief |
| Anti-loop protocol | ✅ actief |
| Memory (persistent) | ✅ 5K chars |
| GitHub integratie | ✅ PR, review, issues |

**Bevindingen:** Geen Noa-specifieke skill-set, geen automatische startup-routine, geen systematische skill-patch workflow, geen MCP servers, geen actieve cron jobs.

### Skill Cluster Analyse
- **Sterk:** agent-orch (4), autonomous-ai (5), creative (16), devops (7), github (6), mlops (9), software-dev (12)
- **Zwak:** hermes-agent (2), MCP (1), crypto-trading (2), data-science (1)

### QA Bevindingen
- agent-grounding conflict met .hermes.md — startup bericht inconsistent
- document-maintenance vereist handmatige flow

---

## ITERATIE 2 — Controller: 4 lagen verbetering

### LAAG 1 — Core Identity
1. ~~Noa-specifieke SKILL.md~~ → **Herzien:** SOUL.md = identiteit, skill = operationele verwijzer
2. agent-grounding patch (conflict met .hermes.md oplossen)
3. controller.md verduidelijking (Noa's rol)

### LAAG 2 — Skills Uitbreiden
4. hermes-cron-management skill
5. hermes-config-management skill
6. hermes-plugin-management skill

### LAAG 3 — Tools & Integraties
7. Second brain auto-sync
8. MCP server setup
9. n8n koppeling

### LAAG 4 — Power User
10. Self-healing skills
11. Multi-agent orchestration
12. Autonome beslissingsboom

---

## ITERATIE 3 — Uitvoering (in meeting)

| Actie | Status |
|-------|--------|
| Punt 2 — agent-grounding patch (2 edits) | ✅ Uitgevoerd |
| Punt 3 — controller.md verduidelijking (1 edit) | ✅ Uitgevoerd |
| Punt 1 — noa-identity skill (v2) | ⏳ Voorstel goedgekeurd, wacht op uitvoering in volgende sessie |

---

## BESLISSINGEN

| # | Beslissing | Details |
|---|-----------|---------|
| 1 | SOUL.md = primaire identiteit | Skills dupliceren geen identiteit |
| 2 | noa-identity skill = operationeel | Verwijst naar SOUL.md en .hermes.md, geen duplicatie |
| 3 | .hermes.md = startup regels | Boot checks, startup bericht |
| 4 | Grounding bij startup | .hermes.md leest → SOUL.md → memory → skills → config |

## OPEN VRAGEN
- Wanneer noa-identity skill uitvoeren?
- Fase 2 skills (cron/config/plugin) prioriteit geven?

## NEXT STEPS
1. noa-identity skill aanmaken (operationeel, geen identiteit)
2. Meeting files syncen naar 2nd brain
3. Fase 2 voorbereiden