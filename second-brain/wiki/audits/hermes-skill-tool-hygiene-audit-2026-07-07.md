---
title: "Hermes Skill / Tool Hygiene Audit"
date: 2026-07-07
type: audit
source: HERMES AUDIT 07
status: partial-cleanup-later
---

# Hermes Skill / Tool Hygiene Audit — 2026-07-07

## Besluit

**Status: PARTIAL** — skill cleanup audit later nodig, maar niet urgent.

Hermes heeft veel skills/tools, maar er is vandaag geen bewijs dat dit acuut onveilig is.

**Cijfers:**
- totaal skills: 209
- categorieën: 36, waarvan 6 leeg
- curator actief bij sessie-start, trackt 85 skills
- curator markeerde 36 stale, reactivated 1
- LLC consolidation: OFF
- totaal tools: ~102
- MCP servers: 3 (plex 45, filesystem 14, health-monitor 8)

## Wat werkt goed

- Curator is actief en markeert stale skills.
- Boot summary voorkomt dat alle 209 skills volledig geladen worden.
- Nieuwe policies conflicteren niet hard met bestaande skills.
- Critical skills zijn identificeerbaar.
- MCP toolset is functioneel.
- AGENT_AUDIT blijft aanwezig.

## Critical skills — voorlopig houden

| Skill | Reden |
|-------|-------|
| context-compressie-check | voorkomt token-bloat |
| second-brain-maintenance | index/log discipline |
| hermes-agent | Hermes eigen config/docs |
| python-development | codewijzigingen |
| test-driven-development | testdiscipline |
| systematic-debugging | serverdebug protocol |
| server-administration | Docker/systemd/server |
| crypto-strategy-development | trading/chart logica |
| code-problemen-oplossen | stopregel bij debug |
| pro-routing | modelrouting discipline |

## Stale / duplicate candidates

Niet verwijderen. Alleen later beoordelen.

| Kandidaat | Reden | Advies |
|-----------|-------|--------|
| websites/* (37) | grotendeels geen actief Lexi-project | archive candidate |
| mlops/* (9) | HuggingFace/vLLM/AudioCraft ongebruikt | archive candidate |
| productivity/* (10) | Notion/Airtable/PowerPoint weinig gebruikt | archive candidate |
| creative/pixel-art | zelden/niet gebruikt | archive candidate |
| gaming/pokemon-player | geen serverproject | archive candidate |
| coaching/youth-cycling-coach | hoort bij Lennox, niet Hermes | keep |
| ollama-coding-executor | mogelijk nuttig, eerst review | review later |
| subagent-driven-development | overlapt met autonomie-policy | merge candidate |
| simplify-code | overlapt met code-quality | review later |
| spike | experiment-skill, lage kost | keep |

## Policy overlap

Geen harde conflicten gevonden.

| Policy | Overlap | Actie |
|--------|---------|-------|
| hermes-context-policy | context-compressie-check | beide houden |
| hermes-final-review-policy | code-problemen-oplossen/git skills | beide houden |
| hermes-health-monitor-policy | server-administration/devops | beide houden |
| hermes-autonomie-policy | anti_loop_protocol | beide houden |
| boot summary | hermes-constraint-manager | later reviewen |

## Tool-bloat conclusie

102 tools is veel, maar momenteel acceptabel. Niet uitschakelen.

Tool-bloat wordt beheerst via: boot summary, context-policy, autonomie-policy, on-demand policy loading.

## Risico's

| Risico | Ernst | Actie |
|--------|-------|-------|
| skill bloat door 209 skills | MED | later cleanup audit |
| stale chart/crypto skills | MED | alleen gebruiken bij exacte match |
| LLC consolidation OFF | LOW | niet wijzigen zonder aparte audit |
| lege categorieën | LOW | later opruimen |
| policy/skill overlap | LOW | boot summary wint |

## Geen actie vandaag

- geen skills verwijderen
- geen categories opruimen
- geen stale archive
- geen LLC consolidation
- geen configwijziging
- geen tool wijzigingen

## Later kandidaat

HERMES AUDIT 07B — SKILL CLEANUP PLAN:
1. critical skills pinnen
2. stale candidates één voor één beoordelen
3. lege categorieën controleren
4. LLC consolidation onderzoeken, niet blind aanzetten
5. crypto/chart skills extra voorzichtig behandelen

## Regel voor toekomst

Skills ouder dan 90 dagen alleen gebruiken bij exacte match.
Nieuwe policies winnen bij conflict, tenzij live bewijs anders toont.
Geen skill cleanup zonder aparte audit én expliciet akkoord van Lexi.
