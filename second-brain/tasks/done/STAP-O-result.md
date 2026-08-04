---
type: result
task: STAP-O
created: 2026-05-30
status: completed
---

# STAP O — Multi-pair backtest: resultaat

## Wat getest

7 pairs (ETHEUR, BTCEUR, SOLEUR, ADAEUR, XRPEUR, LINKEUR, INJEUR) × 3 varianten (baseline/loose/strict) op TF=15m.

## Resultaten per pair (baseline)

| Pair     | Trades | WR%   | PnL%   | MaxStreak | Open |
|----------|--------|-------|--------|-----------|------|
| ETHEUR   | 8      | 12.5% | +2.86% | 5         | 0    |
| BTCEUR   | 4      | 0.0%  | -0.88% | 4         | 0    |
| SOLEUR   | 4      | 0.0%  | +0.45% | 2         | 1    |
| ADAEUR   | 2      | 0.0%  | -1.91% | 2         | 0    |
| XRPEUR   | 2      | 50.0% | +4.77% | 0         | 0    |
| LINKEUR  | 2      | 0.0%  | -3.43% | 2         | 0    |
| INJEUR   | 3      | 33.3% | +6.01% | 2         | 0    |

## Stabiliteitsmatrix (WR% per variant)

| Pair     | baseline | loose  | strict |
|----------|----------|--------|--------|
| ETHEUR   | 12.5%   | 0.0%   | 0.0%   |
| BTCEUR   | 0.0%    | 14.3%  | 0.0%   |
| SOLEUR   | 0.0%    | 0.0%   | 0.0%   |
| ADAEUR   | 0.0%    | 0.0%   | 0.0%   |
| XRPEUR   | 50.0%   | 50.0%  | 50.0%  |
| LINKEUR  | 0.0%    | 0.0%   | 0.0%   |
| INJEUR   | 33.3%   | 40.0%  | 100.0% |

## Stabiliteitsanalyse

- Gemiddelde WR spread: 13.4%
- Maximale WR spread: 66.7% (INJEUR — 1 trade in strict)
- **Conclusie: Stabiel?** De gemiddelde spread is ≤15%, maar dit komt vooral doordat de meeste pairs **0 trades of 0% WR** hebben. Het is geen echte stabiliteit — het is een gebrek aan signalen.

## Eindoordeel

De multi-pair test toont aan dat V3A **weinig signalen genereert op de meeste pairs**. Enkel ETHEUR heeft een redelijk aantal trades (8), de rest 2-4. Dit maakt parameterstabiliteit moeilijk te beoordelen — de samples zijn te klein voor statistische conclusies.

**Vraag voor STAP-Q:** Is dit een probleem met de data-periode (enkel de laatste archief-data), of is V3A inherent selectief? De backtest gebruikt de volledige ohlc_archive, dus de lage aantallen kunnen betekenen dat V3A enkel op bepaalde marktcondities reageert.

JSON output: `logs/research/v3a_multi_pair_2026-05-30.json`
