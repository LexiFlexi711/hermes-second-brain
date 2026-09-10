---
title: Strategy Harness Evaluation Pipeline
type: project
status: active
updated: 2026-08-26
tags: [strategy-harness, evaluation, freeze, noa-reign]
---

# Strategy Harness Evaluation Pipeline

Deterministische signal-quality evaluatie bovenop de NOA-Reign strategy-harness.
Fase-gewijze freeze: elke fase wordt candidate → onafhankelijke Claude review
(ORANGE/GREEN) → commit review → freeze record + tag. Nooit pushen.

## Lineage (frozen, 19–26 aug 2026)

| Fase | Commit | Review | Verdict | Freeze-tag |
|------|--------|--------|---------|-----------|
| Phase3B batch v2 | `213d77db` | `5977456f` | GREEN | (eerder gefrozen) |
| Evaluation Phase0 contract | `1225cd8e` | `2d06134d` | GREEN | `strategy-harness-evaluation-contract-phase0-frozen-20260819` |
| Phase1A join | `45109f2e` | `4d996d26` | GREEN 0/0/0/2 | `strategy-harness-evaluation-phase1a-join-frozen-20260825` |
| Phase1B primitives | `ca1bfd2a` | `45e8f1ca` | GREEN 0/0/0/3 | `strategy-harness-evaluation-phase1b-primitives-frozen-20260826` |

## Commit-keten

```
213d77db (Phase3B freeze)
  → b2fa2f3e → a9994dc0 → fe93ba20 (Phase0 contract draft→finalize)
  → 2d06134d (Phase0 review) → 1225cd8e (Phase0 freeze)
  → 8e5a5661 (Phase1A join) → 4d996d26 (Phase1A review) → 45109f2e (Phase1A freeze)
  → a30fce5e (RC1) → ea7e0467 (RC2) → 1c824599 (RC3)
  → 45e8f1ca (RC3 review) → ca1bfd2a (Phase1B freeze)
```

## Frozen branches

- `frozen/strategy-harness-evaluation-contract-phase0-20260819`
- `frozen/strategy-harness-evaluation-phase1a-join-20260825`
- `frozen/strategy-harness-evaluation-phase1b-primitives-20260826`

## Wat elke fase doet

- **Phase3B** — Batch v2 historical replay (runner).
- **Phase0** — evaluatiecontract: roles, verboden sources, dereference-key
  (record_id + record_revision), consistent-read model.
- **Phase1A** — deterministische read-only Batch-v2 ↔ Outcome join. Populatie/
  volgorde behouden, NO_SIGNAL joined, MISSING_OUTCOME excluded, geen fallback/
  latest, geen scoring.
- **Phase1B** — signal-quality primitieven (geen PnL): directional HIT/MISS/FLAT,
  coverage, favorable/adverse, COUNT/MEAN/MEDIAN. Zie [[strategy-harness-evaluation-phase1b-primitives]].

## Review-cyclus (RC)

Elke fase doorloopt RC's: implementatie → Claude review → delta-fix tot GREEN.

- Phase1B RC1 `a30fce5e` → ORANGE 0/0/2/3 (chain-semantiek + positional alignment)
- Phase1B RC2 `ea7e0467` → ORANGE 0/0/2/3 (full-chain te streng + content-tamper)
- Phase1B RC3 `1c824599` → GREEN 0/0/0/3

## Gerelateerd

- [[strategy-harness-evaluation-phase1b-primitives]] — Phase1B detail
- [[outcome-builder-phase-1a]] — Outcome Builder (outcome store, andere lijn)
- [[noa-reign-roadmap-v2]] — roadmap
- [[2026-08-25-hermes-update-mcp-repair]] — Hermes/MCP fix parallel aan dit werk
