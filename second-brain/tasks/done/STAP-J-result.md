---
type: report
created: 2026-05-29
source: Hermes (STAP-J uitvoering)
status: done
---

# STAP J — Per-candle HOLD logging in runner

## Wat is er gebeurd
Aanpassingen aan `src/crypto_test_bot_v3/runner.py` voor snapshot-based audit trail:

1. **open_pos creation** — MFE/MAE velden toegevoegd (`mfe_pct: 0.0`, `mae_pct: 0.0`)
2. **MFE/MAE update in monitor loop** — elke candle wordt best/worst case PnL berekend en MFE/MAE bijgewerkt
3. **HOLD logging** — na elke candle waarbij trade open blijft, wordt een HOLD event naar de journal geschreven met:
   - `type`, `ts`, `pair`, `entry_ts`, `entry_price`, `direction`
   - `current_close`, `current_high`, `current_low`
   - `sl`, `tp`, `trail_sl`
   - `pnl_pct`, `mfe_pct`, `mae_pct`

## Verificatie XBTEUR (2024 H1)

| Metric | Waarde |
|--------|--------|
| OPEN trades | 25 |
| HOLD events | 1.168 |
| Eerste HOLD mfe | +0.12% |
| Eerste HOLD mae | -0.45% |

## Tests
- 41/41 passed
- Geen breaking changes

## Bestanden
- Gewijzigd: `src/crypto_test_bot_v3/runner.py` (213 → 240 lijnen)
- Originele task: `tasks/done/STAP-J-hold-logging.md`
- Dit resultaat: `tasks/done/STAP-J-result.md`