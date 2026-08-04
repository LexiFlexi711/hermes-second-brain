# Strategy Test Harness Phase 0 — Final

**Date:** 2026-07-30
**Status:** GREEN

## SHAs

- Foundation SHA: 798dde1d51f183abfa29a3a35555f870359732a4
- Incomplete candidate SHA: af9c6e1e (referenced in spec)
- Completion SHA: c4fe2654251197c14c5b991695c0c80e5773df8a
- Final SHA: 835c077fb0e380348bbfdb18e7b736c018af7e44

## Branches

- Final candidate branch: candidate/strategy-test-harness-phase0-final-20260728

## Content Hash Fix

### Problem
- `a0_adapter.py`: `content_hash = meta.get("snapshot_id")` — snapshot_id werd gebruikt als content_hash
- `strategy_runtime.py`: `"content_hash": content_hash or ""` — lege string als default
- `outcome_adapter.py`: content_hash vergeleken met rec.get("snapshot_id") — foute vergelijking, en mismatch werd genegeerd met `pass`

### Fix
- content_hash key wordt NIET gereturnd door extract_source_snapshot
- Frozen L4 reader levert GEEN content_hash — status: NOT_PROVIDED_BY_FROZEN_SOURCE
- build_strategy_input voegt alleen content_hash toe als het een niet-lege string is
- outcome_adapter: foute vergelijking verwijderd; correcte content_hash check via source_snapshot.content_hash blijft bestaan

### Canonical koppeling
- pair/snapshot_id/asof_ts is de canonical koppeling voor Phase 0

## Bewijs

- BTCEUR single: processed=1, written=1, rerun idempotent (skipped_existing=1)
- ETHEUR single: processed=1, written=1, rerun idempotent (skipped_existing=1)
- ETHEUR batch: 2 snapshots, all_ok=true, rerun idempotent
- Real asof_ts: BTCEUR=1785396060, ETHEUR=1785396000
- NO_SIGNAL, NOT_APPLICABLE voor alle runs

## Test Totalen

- Harness tests: 91 collected, 91 passed, 0 failed, exit code 0
- Foundation gate: 14/14 suites green, 951 passed, 0 failed, GATE_RC=0

## Foundation Gate

- 14/14 suites green
- Real-data all_green=True, production_safe=True
- Frozen A0 green
- Frozen Phase 1A green
- Backflow green
- Index green
- Decision: FOUNDATION GREEN — READY FOR STRATEGY TEST HARNESS

## Source Manifests

- Production L4: 2 SQLite files, unchanged
- Live cache: 854 files, unchanged
- pre- en post- manifests identiek

## Production Data

- Niet gewijzigd

## Diff Scope

Alle wijzigingen uitsluitend onder `projects/hermes-v03-strategy-harness/`:
- a0_adapter.py
- outcome_adapter.py
- strategy_runtime.py
- tests/test_content_hash_regression.py (nieuw)

## Definitief Oordeel

STRATEGY TEST HARNESS PHASE 0 GREEN — READY FOR FIRST STRATEGY ADAPTER
