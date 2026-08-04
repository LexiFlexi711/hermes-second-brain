---
title: Stuck trades door stale cache_freshness in-memory bug
type: fix
date: 2026-05-29
status: done
related:
  - "[[2026-05-28-data-bridge-migratie-git-cleanup]]"
  - "[[crypto-tradebot]]"
---

# Stuck trades door stale cache_freshness in-memory bug

## Symptoom

4 V1-trades en 3 Range-trades bleven open in dashboard terwijl current_price al voorbij SL of TP lag:

| Pair | Richting | Entry | SL/TP | Current | Status |
|------|----------|-------|--------|---------|--------|
| INJEUR | LONG | 4.798 | TP 4.942 | 5.155 | TP geraakt, stuck |
| ICPEUR | LONG | 2.295 | TP 2.364 | 2.391 | TP geraakt, stuck |
| ETHEUR | LONG | 1797.87 | SL 1761.91 | 1728 | SL geraakt, stuck |
| BCHEUR | SHORT | 300.87 | TP 291.84 | 261.98 | TP geraakt, stuck |
| LTCEUR | LONG | 44.92 | SL 44.02 | 44.45 | Range open, stuck |
| SOLEUR | LONG | 71.76 | SL 70.32 | 70.53 | Range open, stuck |
| DOGEEUR | LONG | 0.0865 | SL 0.0848 | 0.0854 | Range open, stuck |

## Root cause

Volgorde van commits op 2026-05-28:

| Tijd (UTC) | Commit | Wijziging |
|-----------|--------|-----------|
| 20:36 | `5d339613` | `pullback_trader.py` `_CACHE_DIR` → `crypto-data/` |
| **20:43** | — | **V1, V2, Range processen gestart** |
| 20:59 | `2ed54922` | `cache_freshness.py` `_CACHE_DIR` → `crypto-data/` |

V1/V2/Range laadden `cache_freshness.py` **vóór** de fix-commit. De in-memory `_CACHE_DIR` wees nog naar `crypto-tradebot/logs/live_cache/` — een map die al ~50 uur niet bijgewerkt was (laatste candle: 2026-05-27 04:30).

Gevolg:
1. `_cache_is_fresh(pair, 15)` → age ≈ 3000 min > max 30 min → `False`
2. `_read_cache()` returnt `[]`
3. Monitoring-block: `if not c15m: continue` → exit-check overgeslagen
4. Trades nooit gesloten, state file ongewijzigd

Bewijs in screen-output (06:46 UTC):
```
[STALE] ICPEUR_15m  stale_data  last=2026-05-27 04:30  age=3016.6min  (max=30min)
ICPEUR  LONG  2.2950  2.2950  ...  +0.0%  0x15m
```

De exit-logica zelf (`_check_outcome`) was **correct** — simulatie bevestigde dat LOSS/WIN juist gedetecteerd werd met verse data.

## Welke processen getroffen

| Trader | PID | Gestart (UTC) | Vóór fix? |
|--------|-----|---------------|-----------|
| V1 | 2306061 | 20:43:40 | ja |
| V2 | 2306064 | 20:43:40 | ja |
| Range | 2306070 | 20:43:40 | ja |
| V3 | 2375074 | 21:18:32 | nee ✓ |
| Momentum | 2375071 | 21:18:32 | nee ✓ |

## Fix

```bash
kill -INT 2306061 2306064 2306070
sleep 4

TRADEBOT="/mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/projects/crypto-tradebot"
screen -dmS v1    bash -c "cd $TRADEBOT && python scripts/pullback_trader.py --loop"
screen -dmS v2    bash -c "cd $TRADEBOT && python scripts/pull_backtrader_2.py --scan"
screen -dmS range bash -c "cd $TRADEBOT && python scripts/range_trader.py --loop"
```

## Resultaat

Na herstart binnen 60 seconden (eerste scan-cyclus):

| Pair | Outcome | Exit prijs | Close time |
|------|---------|------------|------------|
| BCHEUR | WIN (trailing) | 282.5778 | 07:03 UTC |
| ETHEUR | LOSS | 1761.9126 | 07:03 UTC |
| ICPEUR | LOSS | 2.2491 | 07:03 UTC |
| INJEUR | LOSS | 4.70204 | 07:03 UTC |
| LTCEUR | RANGE_BREAK | 44.43 | 07:03 UTC |
| SOLEUR | RANGE_BREAK | 70.55 | 07:03 UTC |
| DOGEEUR | RANGE_BREAK | 0.08537 | 07:03 UTC |

## Les

> **Na een code-wijziging aan een gedeelde module (zoals `cache_freshness.py`), moeten alle lopende processen die die module importeren herstart worden.**

Python laadt modules eenmalig in memory. Een update van het `.py`-bestand heeft geen effect op draaiende processen totdat ze herstarten.

Risicovolle commits: wijzigingen aan `cache_freshness.py`, `universe_candidates.py`, `live_data_cache.py`, of andere gedeelde imports.
