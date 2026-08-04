---
title: Ollama Cloud Lanes
type: concept
tags: [ollama, model-routing, code-worker, lane-definitie, qwen3-coder]
status: draft
created: 2026-06-10
related: [model-routing-policy]
---

# Ollama Cloud Lanes

Twee lanes via Ollama op PC (192.168.1.215:11434) die via Ollama Cloud naar externe GPUs routen.

## Lane 1: OLLAMA_CLOUD_CODE_WORKER

| Veld | Waarde |
|------|--------|
| **Naam** | `OLLAMA_CLOUD_CODE_WORKER` |
| **Endpoint** | `http://192.168.1.215:11434` |
| **Model** | `qwen3-coder:480b-cloud` |
| **Bewezen test** | Server → PC Ollama → Ollama Cloud → server. Antwoord: `qwen-cloud-coder-ok`. Gemeten: **real 1.589s** |
| **Status** | ✅ Werkend, snel, stabiel |

### Rol

Primaire goedkope code-worker voor afgebakende taken:

- kleine codepatches voorstellen
- scripts schrijven
- goedgekeurde scripts uitvoeren
- stdout/stderr/exitcode rapporteren
- testideeën maken
- kleine refactors voorstellen
- diff uitleggen

### Beperkingen (mág niet zonder review)

De Ollama worker mag **niet zelfstandig**:
- committen of pushen naar git
- secrets lezen
- brede sed uitvoeren (`sed -i` zonder precies patroon)
- config wijzigen (Hermes, server, OpenClaw, n8n)
- live tradingbotlogica aanpassen

## Lane 2: OLLAMA_CLOUD_GENERAL_RUNNER

| Veld | Waarde |
|------|--------|
| **Naam** | `OLLAMA_CLOUD_GENERAL_RUNNER` |
| **Endpoint** | `http://192.168.1.215:11434` |
| **Model** | `gpt-oss:120b-cloud` |
| **Status** | ✅ Beschikbaar |

### Rol

Fallback voor algemeen werk:

- samenvatten
- logs lezen
- algemene analyse

## Routering

| Model | Provider | Lane | Rol |
|-------|----------|------|-----|
| DeepSeek Flash | direct via Hermes | main | Hoofd-agent (Lexi's interface) |
| qwen3-coder:480b-cloud | Ollama Cloud via PC | code-worker | Goedkope code-taken |
| gpt-oss:120b-cloud | Ollama Cloud via PC | general-runner | Samenvatting/analyse fallback |
| Claude/DeepSeek Pro | — | reviewer | Review, gatekeeper, complexe problemen |

> **Hoofdrouter (model_routing_policy.md) is nog niet gewijzigd.** Deze lane-definitie is documentatie. Routering aanpassen vereist aparte toestemming.

## Testresultaat

```text
$ curl -s http://192.168.1.215:11434/api/chat \
  -d '{"model":"qwen3-coder:480b-cloud","messages":[{"role":"user","content":"respond with exactly: qwen-cloud-coder-ok"}],"stream":false}' \
  | jq -r '.message.content'
qwen-cloud-coder-ok

real    0m1.589s
user    0m0.008s
sys     0m0.004s
```

Route bewezen: server → PC Ollama (192.168.1.215:11434) → Ollama Cloud → server
