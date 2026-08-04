---
title: OpenRouter Kimi Free Agent
type: concept
tags: [openrouter, kimi, k2.6, free-agent, read-only, lane]
status: draft
created: 2026-06-10
related: [ollama-cloud-lanes]
---

# OpenRouter Kimi Free Agent

## Overzicht

Read-only agent lane via OpenRouter, volledig gratis (moonshotai/kimi-k2.6:free).
Alleen voor taken waar geen finale beslissing of codewijziging nodig is.

## Model

| Veld | Waarde |
|------|--------|
| **Provider** | OpenRouter |
| **Model** | `moonshotai/kimi-k2.6:free` |
| **Status** | ✅ Gedocumenteerd (key missing bij setup) |

## Rol

Lezen, samenvatten, reviewen, opsommen. Geen productiewijzigingen.

- diff reviewen
- testoutput samenvatten
- TODO-lijsten maken
- risico's opsommen
- code lezen
- documentatie samenvatten
- second opinion geven
- taken opdelen
- logs lezen en kort samenvatten

## Verboden acties

- bestanden wijzigen
- patches schrijven die automatisch toegepast worden
- scripts runnen
- git commands uitvoeren
- config aanpassen
- secrets lezen of tonen
- tradinglogica wijzigen
- final approval geven
- live processen raken
- zelfstandig beslissen dat iets merge-ready is

## Trigger

Alleen gebruiken wanneer Lexi of reviewer expliciet zegt:

> "gebruik OPENROUTER_KIMI_FREE_AGENT"

**Nooit automatisch. Nooit als main model. Nooit als fallback zonder toestemming.**

## Task Packet Formaat

```
TASK:
FILES_ALLOWED:
READ_ALLOWED: yes/no
WRITE_ALLOWED: no
RUN_ALLOWED: no
COMMANDS_ALLOWED:
EXPECTED_OUTPUT:
STOP_CONDITION:
```

## Beperkingen

- Geen `WRITE_ALLOWED: yes` — dit is een read-only lane
- Geen `RUN_ALLOWED: yes` — geen scriptexecutie
- Alleen `READ_ALLOWED: yes` voor code/documentatie lezen

## Veiligheid

- Nooit `OPENROUTER_API_KEY` printen
- Alleen controleren of key bestaat, zonder waarde te tonen
- Als geen OpenRouter key beschikbaar is: STOP en rapporteer "OpenRouter key missing"
- Geen secrets meesturen naar free modellen
- Geen privédata tenzij Lexi expliciet akkoord geeft

## Technische uitvoering

```
POST https://openrouter.ai/api/v1/chat/completions
Authorization: Bearer $OPENROUTER_API_KEY
Content-Type: application/json

{
  "model": "moonshotai/kimi-k2.6:free",
  "messages": [{"role": "user", "content": "..."}],
  "stream": false
}
```

## Smoke Test Status

| Check | Status |
|-------|--------|
| OpenRouter API key | ✅ Werkt (geen 401) |
| Laatste test | 🔴 HTTP 429 Too Many Requests |
| Auth | ✅ Correct (sk-or-v1-... key) |
| Status | **Prepared but rate-limited** |
| Volgende test | Prompt `"Antwoord exact met: kimi-free-agent-ok"` |
| Routing | ❌ Niet opnemen — alleen op expliciet verzoek |

Rate limit op free model (`moonshotai/kimi-k2.6:free`) is tijdelijk.
Later opnieuw testen zodra rate limit voorbij is.
