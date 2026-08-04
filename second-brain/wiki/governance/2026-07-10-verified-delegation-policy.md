---
title: Verified Delegation Policy — No Synthetic Agents
type: governance
date: 2026-07-10
status: actief
binding: ja
evidence: REAL DELEGATION SMOKE TEST — deleg_98159754
---

# Verified Delegation Policy — No Synthetic Agents

**Datum:** 2026-07-10
**Status:** Actief en bindend
**Bewijs:** Smoke test `deleg_98159754` — echte child-run op `deepseek-v4-flash` (52.94s, 4 API calls, 0 files touched)

---

## 1. Definities

| Term | Definitie | Voorbeeld |
|------|-----------|-----------|
| **Simulated role** | Hermes speelt een rol binnen de eigen context, zonder aparte LLM-call of runtime | "Als Reviewer zou ik zeggen..." |
| **Council simulation** | Meerdere gesimuleerde perspectieven in één sessie, gelabeld als SIMULATED_COUNCIL | "De Baas: ... De Criticus: ..." |
| **Real child-run** | delegate_task met aparte LLM-call, model, context, output path, delegation_id | deleg_98159754 |
| **Worker** | Extern proces (cron script, n8n workflow, systemd service) met eigen logs | Weekly Scout (scout.py + cron) |
| **Real multi-agent** | 2+ echte child-runs OF 1+ echte child-run + 1+ echte worker | delegate_task + Weekly Scout |

---

## 2. Waarheidsregel

**Hermes mag de woorden "agent", "subagent", "Reviewer child", "DevOps child", "Researcher child" of "Code-review child" ALLEEN gebruiken als aan ALLE volgende voorwaarden voldaan is:**

1. `delegation_id` bestaat (bv. `deleg_98159754`)
2. Child model is bekend en gerapporteerd
3. Child output path bestaat en is verifieerbaar
4. `AGENT_AUDIT_V2` blok is ingevuld
5. `files_touched_by_children` is gerapporteerd

**Als NIET aan deze voorwaarden voldaan is, moet Hermes zeggen:**

> "Gesimuleerde rolreview, geen echte subagent gebruikt."

**Geen uitzonderingen.** Ook niet bij haast, korte taken, of "ik weet het antwoord al".

---

## 3. Wanneer delegate_task verplicht is

| Situatie | Child type | Reden |
|----------|-----------|-------|
| Core config wijzigingen (config.yaml, .env) | DevOps-review child | Configfouten = Hermes offline |
| MCP server wijzigingen (add/remove/config) | DevOps-review child | MCP = tool-toegang, veiligheidsgrens |
| Server/devops risico (Docker, services, disk) | DevOps-review child | Destructieve acties mogelijk |
| Codepatch > 50 regels | Code-review child | Complexiteit vereist tweede paar ogen |
| Skills wijzigen (SKILL.md patchen) | Reviewer child | Skills = Hermes gedrag, impact op alle sessies |
| Approval/governance wijzigingen | Reviewer child | Governance = vertrouwensgrens |
| Architectuurkeuzes met langetermijnimpact | Reviewer child | Beslissingen met blijvende gevolgen |

---

## 4. Wanneer delegate_task niet nodig is

| Situatie | Reden |
|----------|-------|
| Simpele read-only statuschecks | Geen wijzigingsrisico |
| Kleine teksttaken | Geen technische impact |
| Gewone uitleg | Geen beslissing |
| Kleine todo/index updates | Administratief, geen code |
| Chatten/emotionele babbel | Geen technische context |

---

## 5. Standaard child-profielen

### Reviewer child
- **Doel:** Read-only review — risico's en blinde vlekken vinden
- **Model:** deepseek-v4-flash
- **Tools:** read_file (geen writes, geen terminal)
- **Output:** Max 5 risico's + 5 aanbevelingen
- **Regel:** Mag geen files wijzigen

### Research child
- **Doel:** Read-only research — docs, web, context vergelijken
- **Model:** deepseek-v4-flash
- **Tools:** web_search, web_extract, read_file
- **Output:** Gestructureerde vergelijking met bronnen
- **Regel:** Alleen lezen, geen writes

### Code-review child
- **Doel:** Diff en testplan beoordelen
- **Model:** deepseek-v4-flash
- **Tools:** read_file, terminal (alleen `git diff`, `grep`, `pytest --collect-only`)
- **Output:** PASS/REQUEST_CHANGES + specifieke issues
- **Regel:** Geen code wijzigen, geen git commit

### DevOps-review child
- **Doel:** Backup/rollback/risico controleren voor deployment
- **Model:** deepseek-v4-flash
- **Tools:** read_file, terminal (alleen read-only: `ls`, `stat`, `docker ps`)
- **Output:** Risico-assessment + rollbackplan
- **Regel:** Geen containers herstarten, geen services aanraken

---

## 6. Verboden voor ALLE children

| Actie | Reden |
|-------|-------|
| Files wijzigen (write_file, patch, terminal writes) | Child heeft geen toestemming van Lexi |
| Approvals accepteren | Alleen Lexi of parent approve't |
| Secrets lezen/loggen | Gevoelige data blijft in parent context |
| Services restart (Docker, systemd, cron) | Destructief zonder Lexi |
| rm/chmod uitvoeren | Permanent dataverlies mogelijk |
| delegate_task zelf aanroepen | Geen nested delegation (max_spawn_depth=1) |
| MCP servers toevoegen/wijzigen | Infrastructuurwijziging zonder audit |
| Config schrijven | Configfouten = Hermes offline |

---

## 7. Verplicht eindblok — AGENT_AUDIT_V2

Elke taak waarin delegation gebruikt wordt, moet eindigen met:

```yaml
AGENT_AUDIT_V2:
  real_delegation_used: yes | no
  delegation_method: delegate_task | delegate_with_model | delegate_parallel | none
  real_child_count: 0 | 1 | N
  child_session_ids: [lijst] | none
  child_output_paths: [lijst] | none
  simulated_roles_used: [lijst] | none
  simulated_role_count: 0 | N
  worker_logs: [paden] | none
  evidence_paths: [paden naar bewijsbestanden]
  models_used:
    parent: modelnaam
    children: [modelnaam, ...]
  files_touched_by_children: [lijst] | none
  status: completed | failed | partial
```

**Als `real_delegation_used: no`:**
- `simulated_roles_used` moet exact benoemen welke rollen gesimuleerd werden
- `simulated_role_count` moet > 0 zijn als er rollen gespeeld werden
- Geen woorden als "agent", "subagent", "reviewer" gebruiken zonder "gesimuleerd" ervoor

---

## 8. Bewijsreferentie

Deze policy is gebaseerd op de **REAL DELEGATION SMOKE TEST** van 2026-07-10:

| Parameter | Waarde |
|-----------|--------|
| delegation_id | deleg_98159754 |
| parent model | deepseek-v4-pro |
| child model | deepseek-v4-flash |
| child duration | 52.94s |
| child API calls | 4 |
| files touched | 0 |
| child output | /home/sjoe/.hermes/cache/delegation/subagent-summary-0-20260710_141545_818548.txt |
| bewijs van echte run | Kind citeerde regelnummers uit code, vond risico's die parent miste |

**Conclusie:** delegate_task werkt. Het is geen simulatie. Maar vanwege de kosten (apart model, aparte context) moet het doelbewust ingezet worden — niet voor elke kleine taak.

---

## 9. Papieren agenten — status

De 20 bestanden in `/home/sjoe/Noa-Hermes/autonomous/agents/*.md` zijn **papieren rolbeschrijvingen** uit mei 2026. Ze hebben:
- ❌ Geen runbewijs
- ❌ Geen output logs
- ❌ Geen actieve status
- ❌ Geen delegation_id's

Ze mogen gebruikt worden als **inspiratie voor child-profielen** maar niet als bewijs van actieve agents.

---

*Governance policy — bindend vanaf 2026-07-10. Elke afwijking moet expliciet gemeld worden aan Lexi.*
