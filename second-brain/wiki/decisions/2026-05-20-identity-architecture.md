---
title: Identity Architecture — SOUL.md = primaire identiteit
type: decision
created: 2026-05-20
source: meeting-010
status: actief
---

# Identity Architecture

**Beslissing:** SOUL.md is de enige bron voor Noa's identiteit. Skills zijn operationeel en dupliceren geen identiteit.

**Waarom:** Voorkomt stale duplicates en authority ambiguity. Als SOUL.md wijzigt, moet de skill niet apart gepatcht worden.

**Consequenties:**
- Skills mogen GEEN `## Identiteit`, `## Persona` of `## Startup bericht` secties bevatten
- Skills verwijzen naar `~/.hermes/SOUL.md` via path, niet via copy-paste
- `hermes-agent-skill-authoring` skill heeft `## Content Scope` sectie die dit afdwingt
- Zie ook: `protocols/skill_creation_policy.md`

**Referenties:**
- `~/.hermes/SOUL.md`
- `~/.hermes/skills/software-development/hermes-agent-skill-authoring/SKILL.md` → Content Scope
- `~/Noa-Hermes/protocols/skill_creation_policy.md`

Verwant: [[2026-05-20-noa-identity-skill-verworpen]], [[2026-05-20-hermes-md-startup-owner]], [[skill-creation-policy]], [[hermes-openclaw-noa-agent]], [[meeting-010]]
