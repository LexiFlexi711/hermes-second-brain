# OHLC Bridge Dedup Hardening — RC2 Claude ORANGE Review → RC3 Resolution

**Datum:** 2026-08-05
**Type:** review-resolutie
**Repo:** NOA-Reign
**Branch:** candidate/crypto-data-ohlc-bridge-dedup-hardening-rc3-20260805
**Commit:** 5fbba6a854f22523388ea28fd33a147949525bd2
**Worktree:** /mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign-worktrees/crypto-data-ohlc-bridge-dedup-hardening-rc3-20260805

## Context

Claude deed een onafhankelijke ORANGE-review van RC2 (commit 06ce7bac). Drie findings moesten opgelost worden voor RC3.

## Opgeloste findings

### MEDIUM — pairs_failed telt ArchiveReadError niet mee

- **Probleem:** `backfill_pair_tf()` vangt `ArchiveReadError` intern en zet `stat["error"]`, maar `run_backfill()` keek alleen naar excepties die propageren. `pair_errored` werd nooit True.
- **Fix:** Na `results.append(stat)` checkt `run_backfill()` nu `if stat.get("error"): pair_errored = True`
- **Bestand:** `nightly_ohlc_backfill.py`

### LOW — count_archive_lines ambigu bij leesfout

- **Probleem:** Retourneerde 0 bij zowel geldig leeg bestand als bij leesfouten.
- **Fix:** Raise `ArchiveReadError` bij `OSError`/`UnicodeDecodeError` i.p.v. `return 0`
- **Bestand:** `nightly_ohlc_backfill.py`

### LOW — Unicode/decode-fout op file-niveau ongetest

- **Probleem:** `path.read_text()` stond buiten try/except, `UnicodeDecodeError` propageerde rauw.
- **Fix:** `path.read_text()` in `archive_new()` en `append_to_archive()` gewrapt: `UnicodeDecodeError` → `ArchiveReadError`
- **Tests:** 13 nieuwe tests (5 pairs_failed, 4 count_archive_lines, 4 unicode decode)
- **Bestanden:** `universe_ohlc_bridge.py`, `nightly_ohlc_backfill.py`, `test_archive_dedup.py`

### LOW — _is_complete_candle mist in backfill

- **Status:** ACCEPTED_OUT_OF_SCOPE — niet verslechterd

## Testresultaten

- **40/40 PASS**
- **py_compile:** PASS
- **diff --check:** PASS
- **Live archive:** filecount 710 ongewijzigd

## Status

- **Pushed:** no
- **Safe to deploy:** no
