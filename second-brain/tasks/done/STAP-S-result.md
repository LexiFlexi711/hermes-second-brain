---
type: result
task: STAP-S
created: 2026-05-30
status: completed
---

# STAP S — Volledige 7-pair run + herbeoordeling V3A

## Resultaten multi-pair run (BacktestReader — historische CSV + archive)

| Pair | Trades | WR% | PnL% | AvgPnL | MaxStr | Open |
|------|--------|-----|------|--------|--------|------|
| ETHEUR | 89 | 28.1% | -44.42% | -0.50% | 7 | 0 |
| BTCEUR | 7 | 16.7% | +4.73% | +0.79% | 4 | 1 |
| SOLEUR | 115 | 26.1% | -43.25% | -0.38% | 13 | 0 |
| ADAEUR | 110 | 34.5% | +25.26% | +0.23% | 7 | 0 |
| XRPEUR | 102 | 25.5% | -22.17% | -0.22% | 12 | 0 |
| LINKEUR | 102 | 32.4% | +27.08% | +0.27% | 8 | 0 |
| INJEUR | 80 | 21.2% | -36.23% | -0.45% | 12 | 0 |

## Stabiliteitsmatrix (WR spread per pair)

| Pair | baseline | loose | strict | spread |
|------|----------|-------|--------|--------|
| ETHEUR | 28.1% | 39.6% | 20.0% | 19.6% ❌ |
| BTCEUR | 16.7% | 25.0% | 50.0% | 33.3% ❌ |
| SOLEUR | 26.1% | 32.7% | 28.0% | 6.6% ✅ |
| ADAEUR | 34.5% | 34.0% | 28.0% | 6.5% ✅ |
| XRPEUR | 25.5% | 30.2% | 20.0% | 10.2% ✅ |
| LINKEUR | 32.4% | 35.9% | 30.3% | 5.6% ✅ |
| INJEUR | 21.2% | 29.8% | 17.4% | 12.4% ✅ |

Gem. spread: **13.5%** (≤ 15% → ✅ stabiel)

## Herbeoordeling

| Criterium | Status | Detail |
|-----------|--------|--------|
| 1. Consistentie over pairs | **SLAAGT NIET** | 0/7 pairs ≥ 40% WR (beste: ADAEUR 34.5%) |
| 2. Parameterstabiliteit | **SLAAGT** | Gem. spread 13.5%, max 33.3% (BTCEUR) |
| 3. Paper/backtest alignment | **SLAAGT NIET** | 0% overlap — live_cache dekt niet |
| 4. Exit potentieel (MFE/L) | **SLAAGT** | V1 MFE verliezers +2.90%, exit verb. +304% |

**EINDOORDEEL: NIET KLAAR** (2/4 slaagt, 2/4 faalt)

## Wat er moet gebeuren

1. **Consistentie verbeteren** — V3A haalt nergens 40% WR. Zelfs ADAEUR (beste, 34.5%) is ondermaats.
2. **Alignment fixen** — paper-vs-backtest data-brug moet werken voor validatie.
3. **Exit potentieel is de sterkte** — trailing stops kunnen V3 mogelijk redden, maar de entry-logica faalt eerst.

## Output

- `tasks/done/STAP-S-multi-pair-output.txt` — terminal output
- `logs/research/v3a_multi_pair_2026-05-30.json` — volledige JSON
- `logs/research/v3a_kandidaat_rapport_2026-05-30.json` — rapport JSON
