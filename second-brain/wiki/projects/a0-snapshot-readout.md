# A0 Snapshot Readout — Phase 1 Status

type: project
status: active
date: 2026-07-11
tags: [a0, hermes-v03-analyst, snapshot, rendering]

## Status

✅ Phase 1 LIVE — per-TF rendering gecommit en gepusht

## Architectuur

```
Hermes-v03 L8_synthesis → L4 SQLite raw_blobs → A0 readout
```

A0 leest read-only via `mode=ro` SQLite. Geen writes, geen berekeningen.

## Output secties

| Sectie | Rendering | Status |
|--------|-----------|--------|
| HEADER | enkel | ✅ |
| DATA QUALITY | enkel | ✅ |
| TIMEFRAMES | per TF | ✅ |
| PRICE CONTEXT | per TF | ✅ |
| STRUCTURE | **per TF** | ✅ nieuw |
| SUPPORT / RESISTANCE | **per TF** | ✅ nieuw |
| TRENDLINES | **per TF** | ✅ nieuw |
| CANDLE MICRO | single-TF fallback | ✅ |
| INDICATORS | single-TF fallback | ✅ |
| FIELD LIMITATIONS | enkel | ✅ |
| SCOPE NOTES | enkel | ✅ |

## Formaten

- Text (plain)
- Markdown (## headings)
- JSON (per-TF keys)

## Tests

61 tests — allemaal pass.

## Contract

- A0 berekent niets
- Toont per TF: stored_values of section_status
- Geen MTF-oordeel
- Geen "beste TF" selectie

## Commit

`735dd471` — Render A0 market context per timeframe
