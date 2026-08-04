# MODEL ROUTING POLICY

## Doel

Hermes moet goedkoper draaien zonder veiligheid, controle of kwaliteit te verliezen.

## Strategie

- Hermes default draait op **DeepSeek V4 Flash**.
- Zware, riskante of beslissende taken moeten naar **DeepSeek V4 Pro**.
- Ultralichte, niet-gevoelige taken mogen eventueel naar een **free/ultra-cheap model**.
- **Gemini Flash-Lite** blijft fallback, niet standaard.

## Waarom deze keuzes

- **DeepSeek V4 Flash** is goedkoper dan DeepSeek V4 Pro en geschikt voor snelle agent/chat/coding-assistant taken.
- **DeepSeek V4 Pro** is sterker voor zware redenering, codebase-analyse, governance en lange agent-workflows.
- **Gemini 2.5 Flash-Lite** is snel en goedkoop, maar voor Hermes is DeepSeek Flash de betere standaard-light keuze.

**Kostenbesparing mag nooit veiligheid vervangen.**

---

## 1. DEFAULT MODEL

**`deepseek/deepseek-v4-flash`**

Gebruik als standaard voor:

- gewone chat
- eenvoudige uitleg
- lezen
- samenvatten
- notulen
- simpele analyse
- brainstorm
- Scout
- Secretary
- Producer
- lichte Memory-taken
- eenvoudige Researcher-taken
- eenvoudige Market/Monetization inventaris
- title_generation
- triage_specifier
- session_search
- compression (na test)

---

## 2. HEAVY MODEL

**`deepseek/deepseek-v4-pro`**

Gebruik VERPLICHT voor:

- Agent Controller
- QA Agent
- Critic / Strategist
- Skills Agent
- Hermes Updater
- RUN_STATE beslissingen
- anti-loop beslissingen
- scope-overgangen
- git add / commit / push
- config-wijzigingen
- provider/model-wijzigingen
- agents/ files
- protocols/ files
- autonomous/ files
- workflows/ files
- systeemfiles
- shell/terminal met wijzigingsrisico
- secrets / env / API keys
- install / delete / apt / pip / docker / systemctl
- DevOps met write/shell/service-risico
- Finance bij echte providerkeuze, abonnement, recurring cost of betaalimpact
- alles waar Lexi expliciete goedkeuring voor moet geven

---

## 3. FREE / ULTRA-CHEAP MODEL

**`deepseek/deepseek-v4-flash:free`**

Alleen voor:

- titelvarianten
- losse brainstorm zonder repo-context
- publieke tekst herschrijven
- niet-persoonlijke, niet-gevoelige tekst

FREE mag NOOIT voor:

- repo-inhoud
- persoonlijke context
- systeemconfig
- secrets
- git
- agents / protocols / workflows
- RUN_STATE
- governance
- beslissingen
- juridische/financiële/veiligheidsinhoud

---

## 4. FALLBACK MODEL

**`google/gemini-2.5-flash-lite`**

Alleen als fallback voor:

- DeepSeek Flash failure
- specifieke Gemini-sterktes
- eventueel multimodal/extractie-taken

Niet als standaard voor governance.

---

## 5. ROUTINGREGELS

```
IF task is simple / read-only / non-sensitive:
  → deepseek/deepseek-v4-flash

IF task touches git/config/agents/protocols/workflows/autonomous/systemfiles/secrets:
  → deepseek/deepseek-v4-pro

IF task requires approval, QA, critic judgement, controller decision or risk judgement:
  → deepseek/deepseek-v4-pro

IF task is public brainstorm or title generation without private context:
  → deepseek/deepseek-v4-flash:free may be used

IF task phase == WAITING_FOR_LEXI:
  → STOP. Geen enkel model gaat verder.

IF task has loop risk:
  → STOP or escalate to deepseek/deepseek-v4-pro.

IF unsure:
  → deepseek/deepseek-v4-pro or ask Lexi.
```

---

## 6. FINANCE GUARD

Finance Guard moet bij modelrouting bewaken:

- gekozen model
- reden van keuze
- kostklasse: free / low / medium / high / unknown
- of Lexi approval nodig is
- of recurring cost ontstaat
- of gevoelige data naar light/free zou gaan

Finance Guard mag adviseren en waarschuwen.

Finance Guard mag NOOIT zelf:

- provider wijzigen
- model wijzigen
- config aanpassen
- commit/push doen
- beslissen namens Lexi

---

## 7. CONFIGBELEID

Gewenste basisconfig:

```yaml
model:
  default: deepseek/deepseek-v4-flash
  provider: openrouter
  base_url: https://openrouter.ai/api/v1
```

Heavy model wordt via policy afgedwongen (geen apart config-slot in Hermes):

```
HEAVY_MODEL = deepseek/deepseek-v4-pro
```

### Auxiliary kandidaten voor light

Deze mogen naar v4-flash:

- triage_specifier
- title_generation
- session_search
- compression

### Niet zomaar light zetten

Deze moeten HEAVY blijven tot aparte toestemming van Lexi:

- approval
- skills_hub
- curator
- kanban_decomposer
- mcp

---

## 8. TESTPLAN

Na elke modelwijziging:

1. Read-only taak testen.
2. Lichte samenvatting testen.
3. Fake heavy taak testen: Hermes moet herkennen dat dit Pro vereist of stoppen.
4. Controleren dat geen writes/git gebeuren zonder Lexi.
5. Controleren dat anti_loop_protocol actief blijft.
6. Bij fout: rollback naar DeepSeek V4 Pro.

---

## 9. ROLLBACK

Bij instabiliteit of fouten:

```bash
hermes config set model.default deepseek/deepseek-v4-pro
```

Of `config.yaml` manueel herstellen vanaf backup.

---

## 10. IMPLEMENTATIEVOLGORDE

1. Create/update: `autonomous/protocols/model_routing_policy.md`
2. Update Controller to reference `model_routing_policy.md`
3. Hermes default model zetten op `deepseek/deepseek-v4-flash`
4. Heavy override documenteren als `deepseek/deepseek-v4-pro`
5. Test: read-only → light summary → fake heavy (refuse/escalate)
6. Na tests: auxiliary slots instellen (triage, title, session_search, compression)
7. Niet instellen zonder aparte toestemming: approval, skills_hub, curator, kanban_decomposer, mcp

---

## 11. MODELREFERENTIES

| Tier | Model ID | Prijs input /M | Prijs output /M | Context |
|------|----------|----------------|-----------------|---------|
| HEAVY | deepseek/deepseek-v4-pro | $0.435 | $0.87 | 1M |
| LIGHT | deepseek/deepseek-v4-flash | $0.112 | $0.224 | 1M |
| FREE | deepseek/deepseek-v4-flash:free | $0 | $0 | 1M |
| FALLBACK | google/gemini-2.5-flash-lite | $0.10 | $0.40 | 1M |

---

## 12. HARDE REGEL

Cost saving is not allowed to reduce safety.

If unsure whether LIGHT or HEAVY: choose HEAVY or ask Lexi.

Harde regel in gewone taal:
- Flash mag werken.
- Pro moet beslissen.
- Free mag alleen rommel zonder risico.
- Lexi beslist bij twijfel.
