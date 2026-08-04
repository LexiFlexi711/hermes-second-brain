---
title: .hermes.md = eigenaar van startup regels
type: decision
created: 2026-05-20
source: meeting-010
status: actief
---

# .hermes.md Startup Ownership

**Beslissing:** `.hermes.md` is de source of truth voor startup berichten, checks en boot regels. Skills volgen, niet leiden.

**Waarom:** Voorkomt conflicten tussen `agent-grounding` skill en `.hermes.md` (beiden wilden eigen startup bericht).

**Consequenties:**
- `agent-grounding` skill: Trigger sectie heeft ⚠️ voorrangswaarschuwing, Startup Messages verwijzen naar `.hermes.md`
- De ketting bij startup: `.hermes.md` → SOUL.md → memory → skills → config
- Geen enkele skill mag startup berichten of boot logic embedden

**Referenties:**
- `~/.hermes/.hermes.md` — Startup-check sectie
- `~/.hermes/skills/agent-core/agent-grounding/SKILL.md` — Trigger + Required Startup Messages

Verwant: [[2026-05-20-identity-architecture]], [[hermes-openclaw-noa-agent]], [[meeting-010]]
