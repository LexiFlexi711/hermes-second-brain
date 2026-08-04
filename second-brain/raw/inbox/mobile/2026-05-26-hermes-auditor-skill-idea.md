---
datum: 2026-05-26
status: raw
type: idea
project: hermes-core
backlink: [[audits/2026-05-26-hermes-brain-access-test.md]]
---

# Skill: Hermes Second Brain Auditor

## Idee
Hermes kan autonoom read-only audits uitvoeren op het volledige Noa-Hermes ecosysteem.
Scopes: naming chaos, duplicate content, git hygiene, recursion risico's, memory governance.

## Eerste test
26 mei 2026 — volledige audit uitgevoerd (11 findings, waarvan 3 KRITISCH).
Bewijs in `audits/2026-05-26-hermes-brain-access-test.md`.

## Risico
- Read-only moet gegarandeerd blijven — geen `rm`, `mv`, `git add`
- Context window kan overvol raken bij grote audits (3,077 files in recursion)
- Geen automatische cleanups — enkel rapporteren

## Volgende stap
- Skill aanmaken in Hermes skills
- Trigger definiëren (wekelijkse cron audit?)
- Meeting protocol voor audit resultaten