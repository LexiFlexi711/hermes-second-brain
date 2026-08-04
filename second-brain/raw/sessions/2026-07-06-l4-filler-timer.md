---
date: 2026-07-06
session: l4-filler-timer-deployment
---

# L4 Filler Systemd Timer — Deployment

## Context
Na succesvolle bouw van de L4 filler runner werd een systemd user timer opgezet om automatisch elke 5 minuten de productie L4 store te vullen met ETHEUR data.

## Wat gebeurd is

### Commits in scope
- `e01dfa3e` — Add safe one-shot L4 filler runner
- `8cc8504f` — Add 1m and 5m to OHLC bridge timeframes
- `9faaff15` — Add source-aware L4 snapshot filler

### Systemd files (buiten repo)
- `~/.config/systemd/user/l4-filler.service` — oneshot runner
- `~/.config/systemd/user/l4-filler.timer` — 5min cadence, OnBootSec=2min

### Service config
- Type: oneshot
- ExecStart: python3 run_l4_filler_once.py --pairs ETHEUR --base-dir .../l4_store --source auto --json
- SuccessExitStatus=75 (lock collision = geen failure)
- After/Wants: ohlc-bridge.service

### Timer config
- OnUnitActiveSec=5min
- OnBootSec=2min
- Persistent=true
- AccuracySec=30s

### Bewezen
- Preflight no-write: mtime diff leeg — geen DB write
- Handmatige run: snapshots 2→3, raw_blobs 10→15
- Timer-run automatisch: snapshots 3→5, status=0/SUCCESS
- Laatste log: status=success, write_passed=true, exit_code=0
- Productie DB: l4_store/ETHEUR/2026-07.sqlite — 5 snapshots, 25 raw_blobs, 25 snapshot_timeframes

### Runner exit codes
- 0 = success
- 1 = exception
- 2 = dry_run_failed
- 3 = write_failed
- 75 = locked (geen failure)

### Data flow
OHLC bridge (systemd, 60s) → live_cache (1m/5m/15m/60m/240m) → Hermes-v03 auto_archive_plus_cache → run_l4_filler_once.py (elke 5min) → L4 SQLite store

## Status
Alles groen. Timer enabled + active. DB vult automatisch.
