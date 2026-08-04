# Research Status: downtrend + near_resistance

**Status:** PROMISING_ENTRY_ARCHETYPE (niet PROVEN)
**Datum:** 2026-06-18

## Bewijs

| Metriek | Waarde |
|---------|--------|
| OOS trades | 18 |
| Hit rate 10 candles | 72% |
| MFE (gem) | +1.23% |
| MAE (gem) | -0.45% |
| MFE/MAE ratio | 2.73 |

## Probleem

Legacy exit logica vernietigt de edge:

| Metriek | Waarde |
|---------|--------|
| Exit WR (legacy) | 11.1% |
| Payoff ratio | 0.15 |
| trailing_stop | 39% (te vroeg) |
| stop_loss | 28% (verliezen te groot) |

De setup heeft 10-20 candles nodig om zich te ontwikkelen. Elke exit binnen 5 candles kapt de edge af.

## Volgende stappen (geen prioriteit)

Nog geen live/paper. Eerst:
- Visuele chart audit van de 18 OOS trades
- Exit-hypotheses ontwerpen:
  - time-based exit 10/20 candles
  - delayed trailing (pas na grotere move)
  - partial take profit
  - tighter invalidation boven resistance
  - BE pas na voldoende move
  - exit op L2/L4 break of reclaim

## Uitsluitsels

- Momentum op 1 jaar: **REJECT** (53% WR, neg PnL)
- high_volume + near_resistance: **INCONCLUSIVE** (herhaalt niet in OOS)
- downtrend + BTC flat: **INCONCLUSIVE** (zwakke edge)
