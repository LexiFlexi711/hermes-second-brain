---
title: Hermes Line Tuning Candidate — Merge Nota
type: synthesis
tags: [hermes-v01, merge-candidate, review, build-tunnel, input-validatie, trend-tops]
status: draft
created: 2026-06-10
related: [hermes-v01-structure-review-2026-06-10]
---

# Hermes Line Tuning Candidate — Merge Nota

## Branch

| Veld | Waarde |
|------|--------|
| **Branch** | `hermes-line-tuning-candidate` |
| **Remote** | `origin/hermes-line-tuning-candidate` |
| **Upstream** | ✅ set |
| **Status** | ✅ clean — 0 modified files |

## Commits (3 op deze branch)

| Commit | Omschrijving |
|--------|-------------|
| `7756f053` | WIP hermes line tuning candidate (Claude) |
| `cda97ba7` | fix(build_tunnel): width initialiseren bij single-envelope + regressietests |
| `66997a76` | fix(hermes): candle input validation — OHLC keys verplicht, _range_atr robuust |

## Testbaseline

**51 passed, 0 xfailed, 0 failed** — volledige testset.

## Opgeloste reviewpunten

| Punt | Omschrijving | Status |
|------|-------------|--------|
| #1 | `_build_tunnel` width-crash (UnboundLocalError bij single envelope) | ✅ Fix + regressietests |
| #3 | `_build_tunnel` recent_range break-status consistentie | ✅ Opgelost in Claude's tuning |
| #4 | `trend_tops`/`trend_bodems` slope/anchor consistentie | ✅ Opgelost + regressietests |
| KeyError | Candle inputvalidatie ontbrekende OHLC keys | ✅ Fix + xfail → pass |

## Open TODO's (niet aangepakt)

| Punt | Omschrijving |
|------|-------------|
| #2 | `read_structure` lookback/timeframe-bug (`candle_span`) |
| #5 | `_direction` schaalbewustzijn (`eps=1e-9`) |
| #6 | `body_cross_count` naam vs wick/range logica |
| #7 | Duplicatie `_bepaal_structure_type` / `_classify_tunnel_structure` |

## Gewijzigde bestanden (sinds main)

| Bestand | Wijziging |
|---------|-----------|
| `layer2_structure/hermes_v01.py` | Claude's tuning + width fix + candle validatie |
| `layer1_charts/chart_engine.py` | Legenda rolgebaseerd + richtingpijlen |
| `CLAUDE.md` | Second brain protocol verduidelijking |
| `tests/test_hermes_v01_structure_edges.py` | Nieuw: edge case tests (6 tests) |

## Eindoordeel

**Merge-ready.** Alle opgeloste punten hebben tests. Open TODO's zijn gedocumenteerd en apart te behandelen. Geen regressie in bestaande tests.
