---
title: Hermes API Key Env Fix
type: fix
date: 2026-06-15
status: applied
---

# Hermes API Key Env Fix

## Probleem

`config.yaml` had lege `api_key: ''` velden bij alle auxiliary providers en delegation.
`env_passthrough` miste `DEEPSEEK_API_KEY` en `OPENROUTER_API_KEY`.
`model-startup-check.sh` controleerde shell env vars die niet geëxporteerd waren.

Hierdoor rapporteerde de health check "key niet gezet" terwijl de keys wel in
`~/.hermes/.env` stonden.

## Oorzaak

Hermes laadt `.env` intern en werkt daarmee. Maar:
- config.yaml verwees nergens expliciet naar `${DEEPSEEK_API_KEY}` voor de model/api keys
- 13 plekken hadden `api_key: ''` in plaats van `${DEEPSEEK_API_KEY}`
- `env_passthrough` enkel `FIRECRAWL_API_KEY`, dus subagents misten de LLM keys
- `model-startup-check.sh` controleerde `$DEEPSEEK_API_KEY` uit shell env (leeg), niet uit `.env`

## Wijziging

### config.yaml

| Locatie | Van | Naar |
|---------|-----|------|
| `model.api_key` | (bestaand niet) | `${DEEPSEEK_API_KEY}` |
| `auxiliary.*.api_key` (11x) | `''` | `${DEEPSEEK_API_KEY}` |
| `delegation.api_key` | `''` | `${DEEPSEEK_API_KEY}` |
| `terminal.env_passthrough` | `[FIRECRAWL_API_KEY]` | `[FIRECRAWL_API_KEY, DEEPSEEK_API_KEY, OPENROUTER_API_KEY]` |

### model-startup-check.sh

Toegevoegd bovenaan (na shebang):

```bash
ENV_FILE="/home/sjoe/.hermes/.env"
if [ -f "$ENV_FILE" ]; then
  set -a
  source "$ENV_FILE" 2>/dev/null
  set +a
fi
```

## Bewijs

- `bash -n /home/sjoe/scripts/model-startup-check.sh` → ✅ Syntax OK
- `grep -n "api_key:" config.yaml | sed 's/api_key: .*/<redacted>/'` → 15 occurrences, allemaal `${VARIABELE}` referenties, geen raw secrets
- `bash model-startup-check.sh`:
  - [OK] DeepSeek Flash — HTTP 200
  - [OK] OpenRouter fallback — HTTP 200
  - [OK] Ollama qwen3-coder — online (qwen3-coder:480b-cloud, gpt-oss:120b-cloud, qwen3-coder:30b)

## Backups

- `/home/sjoe/.hermes/config.yaml.bak.20260615_065817_envfix`
- `/home/sjoe/scripts/model-startup-check.sh.bak.20260615_074949`

## Risico / Regel

- Nooit `.env` printen of raw keys in logs tonen
- Nooit raw API keys in `config.yaml` hardcoden — altijd `${VARIABELE}` gebruiken
- Na configwijziging altijd `bash ~/scripts/model-startup-check.sh` draaien voor validatie
- Bij nieuwe auxiliary tools: `api_key: ${DEEPSEEK_API_KEY}` ipv `''`
- Bij nieuwe env vars die naar subagents moeten: toevoegen aan `env_passthrough`
