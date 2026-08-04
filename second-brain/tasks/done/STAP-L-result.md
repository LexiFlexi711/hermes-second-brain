---
type: report
created: 2026-05-29
source: Hermes (STAP-L uitvoering)
status: done
---

# STAP L — MFE/MAE analyse crypto-tradebot

## Script
`/mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/projects/crypto-tradebot/scripts/mfe_mae_analyse.py`

## Output
- JSON: `logs/mfe_mae/mfe_mae_analyse.json`
- Markdown: `logs/mfe_mae/mfe_mae_rapport.md`

## Resultaten per strategie

| Strategie | Trades | MFE≥1% | MFE≥2% | MFE≥3% | Verliezers groen geweest | Gem. MFE win | Gem. MFE verlies | Giveback win | Giveback verlies |
|-----------|--------|--------|--------|--------|--------------------------|--------------|------------------|--------------|------------------|
| V1 | 17 | 59% | 47% | 29% | 50% | +8.04% | +2.90% | +4.73% | **+4.61%** |
| V2 | 31 | 52% | 35% | 16% | 41% | +2.31% | +1.33% | +1.49% | +2.71% |
| V3 | 8 | 38% | 12% | 12% | 17% | +2.43% | +0.34% | +1.43% | +1.73% |
| Momentum | 19 | 58% | 21% | 11% | 14% | +1.87% | +0.61% | -0.72% | +2.39% |
| Range | 14 | 64% | 7% | 0% | 38% | +1.83% | +0.85% | +0.68% | +2.27% |

## Opvallende inzichten
1. **V1 grootste giveback**: verliezers gingen gemiddeld +4.61% in winst voor ze verlies werden — exit management faalt hier
2. **Momentum beste verliescontrole**: maar 14% van verliezers was ooit groen
3. **Range safe maar beperkt**: 0% haalt 3% MFE, maar 64% haalt 1%
4. **V3 kleine sample**: slechts 8 closed trades, moeilijk conclusies trekken

## Technisch
- 89 trades geanalyseerd over 5 strategieën
- 40 trades overgeslagen (OPEN of onvolledig)
- Data uit 15m OHLC archive
- Enkel Python stdlib