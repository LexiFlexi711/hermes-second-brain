---
type: synthesis
date: 2026-05-26
title: "Sessie 26 Mei — Model routing optimalisatie + Governance + Langfuse setup"
status: completed
---

# Sessie Samenvatting — 26 Mei 2026

## Wat er gebeurd is

### 1. Model Routing Optimalisatie (Fase 1)
- 10 auxiliary modellen naar `deepseek/deepseek-v4-flash:free` gezet
- delegation.model expliciet op paid Flash
- Besparing: ~$10.80/maand, 0% kwaliteitsimpact
- Backup: `config.yaml.backup_20260526_075147`

### 2. Governance Protocol (5 regels)
- Bestand: `autonomous/protocols/governance_protocol.md`
- Actielog verplicht → `~/.hermes/actielog.md`
- Kostenrapport per model/tool
- No-write zonder plan bij infra
- Healthcheck vóór+na elke wijziging
- Rollback-pad bij elke infra-aanpassing

### 3. Langfuse Self-Hosted (Fase 2)
- 6 containers in compose-media stack (postgres, clickhouse, minio, redis, web, worker)
- Alle poorten enkel op 127.0.0.1
- Langfuse web op poort 3010 (ipv 3000 — chromium conflict)
- Plugin `observability/langfuse` enabled
- API keys gezet in `~/.hermes/.env`
- Nog 1 herstart nodig voor eerste trace!

## Openstaand (todo)
- Fase 3: Budget bijstellen ($6→$3?)
- Fase 4: Gemini key activeren
- Radarr + Sonarr configureren

## Belangrijke changes
- `config.yaml` — aux modellen naar :free
- `docker-compose.yml` — +6 langfuse services
- `langfuse/.env` — secrets (postgres, minio, nextauth)
- `~/.hermes/.env` — Langfuse API keys
- `protocols/governance_protocol.md` — nieuw
