---
type: result
task: STAP-P
created: 2026-05-30
status: completed
---

# STAP P — Paper vs Backtest: resultaat

## Wat getest

ETHEUR over 7 dagen en 30 dagen terug:
- Backtest: `backtest_pair()` op ohlc_archive
- Paper: `V3AStrategy` op LiveReader (live_cache)

## Resultaten

| Periode     | Backtest | Paper | Overlap | Conclusie |
|-------------|----------|-------|---------|-----------|
| 7 dagen     | 0        | 0     | n/a     | Geen signalen in beide |
| 30 dagen    | 8        | 0     | 0%      | Alleen backtest heeft data |

## Analyse

De live_cache (rolling cache) dekt **enkel de laatste paar uur** data. De backtest-signalen van 19-20 Mei liggen te ver terug om in de live_cache te zitten. Hierdoor is **directe signaalvergelijking niet mogelijk**.

## Conclusie

**Niet beoordeelbaar** — de live_cache heeft onvoldoende historische diepgang om een zinvolle paper-vs-backtest vergelijking te maken. De vergelijking zou kunnen werken als:

1. De live_cache langer bewaard wordt (dagen i.p.v. uren)
2. Of de paper-loop over dezelfde ohlc_archive data draait als de backtest (wat eigenlijk een backtest-in-backtest wordt)
3. Of we een paar nemen dat recent (laatste uren) een signaal gaf

**Aanbeveling:** Herontwerp de vergelijking zodra live_cache langer bewaard blijft, of voeg een modus toe die beide readers over dezelfde archief-data laat lopen.

JSON output: `logs/research/paper_vs_backtest_2026-05-30.json`