---
type: fix
date: 2026-05-31
agent: Noa (Hermes)
title: Watchdog reboot om 16:14 (hoge load)
---

# Watchdog reboot — 31 Mei 2026

## Wat gebeurde

- **16:13:11** — watchdog begint te klagen: loadavg 21/16/13 boven drempel 24/18/12
- **16:13:11 → 16:14:23** — ~72 seconden load boven 15-min drempel (12)
- **16:14:23** — watchdog stuurt SIGTERM naar systemd (PID 1) → reboot
- **16:15:16** — server terug online, propere shutdown

## Vorige uptime: 59 dagen 18u (van 1 Apr tot 31 Mei)

## Oorzaak

**Direct:** watchdog daemon (`/etc/watchdog.conf`) met `max-load-1 = 24`, 5-min default 18, 15-min default **12**. De 15-min load van 13 overschreed de drempel.

**Onderliggend:** loadspike naar 18-21 werd waarschijnlijk veroorzaakt door combinatie van:
- Chromium renderers (kunnen 50%+ CPU per core pakken)
- ClickHouse (Langfuse analytics, ~12% CPU)
- Selkies websocket streaming
- Claude Code + Hermes agent
- Mogelijk n8n workflow uitvoering

## Waarom dit een probleem is

- Server heeft **8 cores, 16GB RAM** met 25 Docker containers
- Normale load kan tijdens routine-operaties boven 12 pieken
- Watchdog heeft geen fysiek `/dev/watchdog` — het is pure software
- De 15-min drempel van 12 is te laag voor deze workload

## Hoe voorkomen

Opties:
1. **Watchdog uitschakelen** — geen fysiek watchdog device, dus enkel software reboot
2. **Thresholds verhogen** bv. max-load-1=36, max-load-5=28, max-load-15=20
3. **Realtime monitoring** via netdata (loopt al) — veel beter dan watchdog

## Huidige status

Alle 25 containers up ✅, proper opgestart. Geen dataverlies. Geen corruptie.
