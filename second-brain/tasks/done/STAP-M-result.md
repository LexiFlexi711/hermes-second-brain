---
type: report
created: 2026-05-29
source: Hermes (STAP-M uitvoering)
status: done
---

# STAP M — Exit management simulatie

## Script
`/mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/projects/crypto-tradebot/scripts/exit_sim.py`

## Resultaten per strategie

| Strategie | Origineel | BE stop (+1%) | Trail (+2%) | Combo A+B | Verliezers gered |
|-----------|-----------|---------------|-------------|-----------|------------------|
| **V1** | -18.07% | -4.07% | +36.88% | **+36.88%** | 7 |
| **V2** | -25.12% | -9.43% | +9.58% | **+9.58%** | 6 |
| **V3** | -11.37% | -8.61% | -7.04% | -7.04% | 1 |
| **Momentum** | +13.65% | +16.74% | +10.66% | +10.66% | 1 |
| **Range** | -4.44% | -0.30% | -0.32% | -0.32% | 0 |

## Conclusie
- **V1** heeft het meest te winnen: trailing zou historisch +36.88% hebben opgeleverd ipv -18.07%
- **V2** ook sterke verbetering: van -25% naar +9.58%
- **Momentum** presteert al OK origineel (+13.65%), trailing maakt het iets minder
- **V3 + Range** kleine samples, moeilijk conclusies
- Break-even stop alleen is al winst: V1 van -18% naar -4%

## Output
- `logs/mfe_mae/exit_sim_resultaten.json`
- `logs/mfe_mae/exit_sim_rapport.md`