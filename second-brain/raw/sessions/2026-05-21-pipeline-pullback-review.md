---
title: Pipeline Design & Pullback Trader Review - 21 mei 2026
type: session_log
created: 2026-05-21
---

# Pipeline Design & Pullback Trader Review

**Aanwezige teamleden:** Noa (Hermes) + Data Scientist/DevOps/Trading Analyst subagents
**Opdrachtgever:** Lexi
**Status:** Bot stond stil sinds 06:20 — open trades in pullback_state.json

## Data gebruikt
- V2 trades: 66 trades (v2_trades.jsonl), waarvan 8 schema 2.2
- V3 scans: 8595 entries (pullback_v3_trades.jsonl)
- pullback_state.json: 6 open trades (SOLEUR, XRPEUR, POLEUR, PEPEEUR, AVAXEUR, DOTEUR)
- API candidate lijst: 607 coins met 36 ticker-velden
- Charts: enkel tot 19 mei op server, Lexi keek lokaal op TradingView

## V2 Trade Analyse (66 trades)
- Overall WR: 33.3% (17W/34L/15C)
- SHORT: 27.5% WR (11/40) — 78% van trades
- LONG: 54.5% WR (6/11) — 2x beter
- Schema 2.2: 7 trades, 6/7 WIN (enkel short LINKEUR verloor)
- SL krimping: WIN avg=0.68%, LOSS avg=0.43%, 16 trades <0.2%
- ETHEUR: 17% WR (2/12), alle shorts
- Chronologisch: 27% → 36% → 67% WR per dag

## Claude Code Team Analyse (via Lexi's Opus)
4 agenten (Trade Analyst, MIT Math Prof, Master Trader, Software Architect):
- V2 4/4 closed vannacht = +8.02R, maar correlatie ρ=0.85 → geen significantie
- V3 NEAR SL 13.4% = design bug
- Negatieve expectancy: -17.8% R per trade
- Geen kill switch in geen enkel script
- 28% code duplicatie

## Pipeline Ontwerp (nieuw)
- FASE 1: Ticker selector (elk uur) — 607 → 250 base candidates (enkel kill filters)
- FASE 2: Strategie scores op 250 → top 15-20 per strategie
- FASE 3: OHLC voor geselecteerde kandidaten
- FASE 4: V2/V3 executie

## Bestanden gecreëerd
- `/home/sjoe/Noa-Hermes/data-science/ticker_filter.py` — 393 regels, 4 score functies
- `/home/sjoe/Noa-Hermes/data-science/607-to-15-ticker-pipeline.md` — volledige pipeline doc
- `/home/sjoe/Noa-Hermes/data-science/devops-pipeline-advies.md` — DevOps advies
- `/home/sjoe/_pipeline_thresholds_conclusies.md` — data-gedreven drempels

## Beslissingen
- Pipeline: ticker elke 30-60 min → 250 base → scores → OHLC
- MIN_STOP 0.3% hard afdwingen
- ETHEUR SHORT blokkeren of sterk filteren
- LONG/SHORT bias corrigeren (50/50 doel)

## Open voor Lexi
- universe_selector.py herschrijven (kill filters → 250 base)
- V1 time-stop toevoegen
- V3 SL-engine fixen
- restart van V2 met open trades

## Model gebruikt
- deepseek/deepseek-v4-flash (HEAVY voor team subagents)