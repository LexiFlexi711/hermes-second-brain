---
type: session
date: 2026-05-28
model: deepseek/deepseek-v4-flash
provider: openrouter
commits:
  - 5ff4af3 (protocols: add governance protocol, gepusht naar GitHub)
---

# Sessie 2026-05-28 — Model Routing Fix

## Wat gebeurde

1. **Startup check** — alle systemen OK. 20 pending updates, 365 stale 15m candles in tradebot, V3 backtest zwak (26% WR).

2. **MODEL_ROUTING.md onderzoek** — ontdekt dat `memory/MODEL_ROUTING.md` bewust verwijderd werd in commit `325dbb5`. De `memory/` directory in Noa-Hermes is een symlink naar `~/system/hermes-second-brain/`. Git ignoreert de hele directory sinds die commit.

3. **Per ongeluk MODEL_ROUTING.md aangemaakt** in de second brain root via de symlink. Later verwijderd na Lexi's correctie.

4. **3 bestanden gepatcht** — alle referenties van `memory/MODEL_ROUTING.md` → `autonomous/protocols/model_routing_policy.md`:
   - `/home/sjoe/.hermes.md` lijn 6
   - `/home/sjoe/.hermes/.hermes.md` lijn 6
   - `governance_protocol.md` lijn 66

5. **Format-only cleanup** van governance_protocol.md (trailing newline toegevoegd). model_routing_policy.md was al proper.

6. **Backups** verplaatst naar `~/system/hermes-second-brain/backups/noa-hermes-protocols/20260528_model_routing_fix/`.

7. **Commit + push** — `governance_protocol.md` (184 lijnen) gecommit als `5ff4af3` en gepusht naar GitHub.

## Leerpunten

- Lexi wil rauwe data in de chat, geen samenvattingen.
- Als ze vraagt om bestanden te tonen: `read_file` gebruiken en letterlijk plakken.
- Geen eigen zinnen verzinnen en presenteren als bestandsinhoud.
- Bij format-cleanup: backup eerst, dan pas patchen.