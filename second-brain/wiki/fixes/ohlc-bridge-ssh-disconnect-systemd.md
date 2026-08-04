---
title: OHLC Bridge Writer — SSH disconnect fix + systemd service
type: fix
created: 2026-07-04
updated: 2026-07-04
status: resolved
related: [[crypto-data-pipeline]], [[crypto-tradebot]]
---

# OHLC Bridge Writer — SSH disconnect fix + systemd service

## Probleem

Op 4 juli 2026 stopte de `universe_ohlc_bridge.py` writer plots om 18:33 UTC.
Cache files (ETHEUR_1m t/m 1440m) werden niet meer geschreven.
Geen OOM kill, geen crashlog, geen reboot.

## Doodsoorzaak

Lexi's twee SSH sessies disconnecten tegelijk om 18:23:13 UTC:
```
Jul 04 18:23:13 lexi-server sshd[2802958]: pam_unix(sshd:session): session closed for user sjoe
Jul 04 18:23:13 lexi-server sshd[2803085]: pam_unix(sshd:session): session closed for user sjoe
```

De writer draaide in één van deze terminals (niet in tmux/screen/systemd).
Bij SSH disconnect → SIGHUP → proces sterft mee.

Datagat: 2u29min (18:33 UTC → 21:02 UTC).

## Oplossing

Systemd user service op `/home/sjoe/.config/systemd/user/ohlc-bridge.service`:

```
[Unit]
Description=NOA-Reign Universe OHLC Bridge
After=network-online.target

[Service]
Type=simple
WorkingDirectory=/mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/projects/crypto-data
ExecStart=/usr/bin/python3 .../universe_ohlc_bridge.py
Restart=always
RestartSec=10
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=default.target
```

- `systemctl --user enable ohlc-bridge.service`
- `loginctl enable-linger sjoe` (start bij boot, stond al op yes)
- `Restart=always` → herstart bij crash
- PID: 2950878, 26 pairs, 156 OK / 0 fail per cycle

## Clean store proof

L4 filler op schone database:
- Dry-run: 0 bestanden geschreven ✅
- Write: snapshots=1, raw_blobs=5, snapshot_timeframes=5 ✅
- Snapshot: `ETHEUR-1783200060-1m5m15m60m240m-c591b7e51f26`
- Alle TFs: candles_final=240, l1_valid=true

## TIMEFRAMES

Stonden al correct in het script:
```python
TIMEFRAMES = {
    1:    720,
    5:    300,
    15:   200,
    60:   150,
    240:  120,
    1440: 90,
}
```

## Lessons learned

1. Productieprocessen mogen NOOIT in een SSH terminal draaien — altijd systemd/tmux/screen
2. Zonder auto-recovery is elk datagat onopgemerkt
3. `systemctl --user` + `linger` = de simpelste veilige oplossing
4. Cache files alleen zeggen niet genoeg — heartbeat + journal check is nodig voor diagnose
