---
title: Data bridge migratie + git cleanup
type: fix
date: 2026-05-28
status: done
---

# Data bridge migratie + git cleanup

## Fixes van deze sessie

### 1. _BRIDGE_DIR migratie (alle traders)
Traders schreven `*_request.json` naar `crypto-tradebot/logs/bridge/`.
Bridge leest alleen uit `crypto-data/logs/bridge/`.
→ `_BRIDGE_DIR` gecorrigeerd in 8 trader-scripts.

### 2. cache_freshness.py
`_CACHE_DIR` wees naar `crypto-tradebot/logs/live_cache/` (niet meer bijgewerkt).
→ gecorrigeerd naar `crypto-data/logs/live_cache/`.
Resultaat: STALE-melding in webapp verdwenen.

### 3. Git history cleanup
`screen-0-bash.log` (171MB) en `pullback_v3_trades.jsonl` (101MB)
blokkeerden GitHub push.
→ `git-filter-repo` gebruikt om beide uit volledige history te verwijderen.
→ `.gitignore` uitgebreid met patronen voor runtime-only bestanden.
→ Force-with-lease push geslaagd.

Backup: `backup/pre-large-file-cleanup-20260528-230556`

### 4. Nightly OHLC backfill
Nieuw script `crypto-data/scripts/nightly_ohlc_backfill.py`.
Cron dagelijks 00:00. Vult OHLC-gaten via Kraken `since` parameter.

### 5. Waarschuwing nog open
`scan_events.jsonl` is 83MB — onder GitHub-grens maar risicovol.
Overweeg ook dat uit history verwijderen.
