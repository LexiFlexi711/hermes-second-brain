---
title: Pullback Trader Review - 21 mei 2026
type: session_log
created: 2026-05-21
---

# Pullback Trader Review - 21 mei 2026

**Aanwezige teamleden:** Noa (Hermes) + Master Trader subagent
**Opdrachtgever:** Lexi
**Status:** Bot gestopt sinds 20 mei 20:58 — geen actieve processen

## Reality check

- V1 + V2 heartbeats gestopt 2026-05-20 20:58
- pullback_state.json = leeg {}
- Geen actieve Python trading processen
- Data consistent tot 20 mei 22:58 (candle battles, live cache)
- Charts laatste 19 mei

## V2 Trade Stats (62 trades, 51 actief)

- **WR: 33.3%** (17W/34L)
- SHORT: 27.5% (11/40) — slecht
- LONG: 54.5% (6/11) — 2x beter
- Short bias: 78%
- SL krimping: avg 0.515%, 16 trades <0.2%, WIN SL=0.679% vs LOSS SL=0.434%
- ETHEUR: 17% WR (2/12) — grootste verliesbron
- Simulated P&L: exact break-even (+68%/-68%)
- Chronologische trend stijgt: 27% → 36% → 67%
- MIN_STOP vloer NIET toegepast (fix uit Meeting 006 gemist)

## V3 State Machine

- Zuivere observer — opent geen echte trades
- Entry trigger: PULLBACK_FAILED — FUNDAMENTEEL FOUT (omgekeerd van strategie)
- Geen fib zone berekening, geen entry_lateness
- Markt: meeste pairs in chop, geen duidelijke 4H trend

## Beslissingen

- Geen actieve beslissingen — Lexi volgt meeting en beslist

## Aanbevelingen

1. Restart volgorde: cache_watchdog → V2 (niet V3)
2. MIN_STOP harde vloer toevoegen (0.3%)
3. ETHEUR short filteren
4. Meer long trades
5. V3's state machine logica samensmelten met V2's entry logic

## Bestanden gewijzigd

- Geen bestanden gewijzigd — enkel data-analyse

## Model gebruikt

- deepseek/deepseek-v4-flash (HEAVY voor Master Trader)