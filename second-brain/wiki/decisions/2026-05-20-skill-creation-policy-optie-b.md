---
title: Skill Creation Policy — apart protocol (Optie B)
type: decision
created: 2026-05-20
source: meeting-010
status: actief
---

# Skill Creation Policy — Optie B

**Beslissing:** Skill creatie beleid wordt een apart protocolbestand, geen sectie in een skill.

**Waarom:** Clean separation — identity skill = gedrag, protocols = beleid. Makkelijker te patchen.

**Consequenties:**
- `~/Noa-Hermes/protocols/skill_creation_policy.md` is de source of truth
- `hermes-agent-skill-authoring` skill verwijst ernaar in `## When to Use` → Drempelwaardes
- Drempels: zware fout / ≥2x herhaling / ≥3 stappen complex / ≥2x patroon
- Geen skills voor: eenmalige fout, prutsprobleem, duplicatie

**Referenties:**
- `~/Noa-Hermes/protocols/skill_creation_policy.md`
- `~/.hermes/skills/software-development/hermes-agent-skill-authoring/SKILL.md` → Drempelwaardes
- `~/system/second-brain/wiki/concepts/skill-creation-policy.md`

Verwant: [[skill-creation-policy]], [[2026-05-20-identity-architecture]], [[meeting-010]]
