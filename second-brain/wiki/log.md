---
title: Wiki Change Log
type: log
created: 2026-04-22
updated: 2026-05-20
---

# Change Log

## 2026-04-22
- System initialized

## 2026-05-17

- Aangemaakt: `wiki/fixes/2026-05-17-hermes-yaml-prefix-fix.md`
- Bron toegevoegd: `raw/inbox/2026-05-17-hermes-yaml-fix.md`
- Reden: eerste gecureerde herinnering voor Noa Second Brain.

- Aangemaakt: `wiki/projects/hermes-openclaw-noa-agent.md`
- Reden: projectpagina gemaakt zodat `[[Hermes OpenClaw Noa Agent]]` geen lege link blijft.

## 2026-05-19

- Aangemaakt: `wiki/projects/pullback-trader-strategy.md`
- Aangemaakt: `wiki/entities/trade-specialist-agent.md`
- Aangemaakt: `wiki/projects/crypto-tradebot.md`
- Aangemaakt: `wiki/synthesis/team_meeting_005_pullback_strategy.md` (V3 — ECHT teamoverleg)
- Aangemaakt: `wiki/synthesis/team_meeting_005_pullback_strategy.json` (V3 — ECHT teamoverleg)
- Bestaande meetings (002-004) gekopieerd naar wiki/synthesis/
- Reden: LIVE_TEAM_MEETING — Scout + Claude Code CLI + Critic + Secretary leverden échte output met tool bewijs. Claude Code identificeerde 6 blokkades, HL/LH flags ongebruikt, 15M moet reversal worden.

## 2026-05-20

- Aangemaakt: `wiki/synthesis/meeting_008.md`
- Gekopieerd: `~/Noa-Hermes/autonomous/meetings/meeting_008.md` → `wiki/synthesis/`
- Reden: TEAM MEETING 008 — Dringende Tradebot Audit. V1: 0 trades in laatste 24u+ (3 totaal, macro fib structuren te breed). V2: 61 trades, 30% WR, -54.84 EUR (77% SHORTS, ETHEUR 17% WR). Beide screens dood sinds 19/05 19:14. 2 open posities verloren (INJEUR LONG, RENDEREUR SHORT). Geen auto-restart.

- Aangemaakt: `wiki/synthesis/team_meeting_006.md`
- Gekopieerd: `~/Noa-Hermes/autonomous/meetings/team_meeting_006.md` → `wiki/synthesis/`
- Reden: TEAM MEETING 006 — Tradebot V1/V2 audit + Claude Code prompt. Nieuwe code (Lexi's update 11:24) heeft al richting-bewuste pullback, 15M confirm, entry_lateness, MIN_RR=2.0, MIN_STOP_DIST. Nog te fixen: calc_sl harde afstandsgrens, heartbeat, V1 macro-paralysis.
