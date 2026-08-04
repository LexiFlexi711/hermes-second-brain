---
type: result
task: STAP-T
created: 2026-05-31
status: completed
---

# STAP T — V1 en V2 strategie in testbot

## Wat gebouwd is

| Map | Bestanden | Lijnen | 
|-----|-----------|--------|
| `strategies/v1/config.py` | Constanten (SL/TP, fib zones, aggregator) | 44 |
| `strategies/v1/logic.py` | Pure functies (structuur, swings, pullback, reversals, SL/TP) | 283 |
| `strategies/v1/strategy.py` | V1Strategy — compute_checks + build_signal, 5 checks (trend,impulse,fib,trigger,btc_macro) | 187 |
| `strategies/v2/config.py` | Constanten (SL/TP, swing, structuur_tol) | 28 |
| `strategies/v2/logic.py` | Pure functies (trend, swings, pullback_leg, fib, confirm, volume, SL/TP) | 283 |
| `strategies/v2/strategy.py` | V2Strategy — compute_checks + build_signal, 5 checks (trend,pullback,confirm,lateness,volume) | 155 |

## Tests

| Testbestand | Aantal tests |
|-------------|-------------|
| `tests/unit/test_v1_strategy.py` | 31 |
| `tests/unit/test_v2_strategy.py` | 21 |
| **Totaal nieuwe** | **52** |
| **Volledige unit suite** | **101/101 ✅** |

## Verificatie

- ✅ V1Strategy en V2Strategy importeren zonder errors
- ✅ Beide strategieën instantieerbaar met `Strategy({})`
- ✅ V1 fib_label: forming (0.1), early_pullback (0.35), ideal (0.5), deep_warning (0.65), trend_break (0.8)
- ✅ V1 SL/TP: LONG entry=100 → SL=98.0, TP=103.0 (exact 2%/3%)
- ✅ V1 SL/TP: SHORT entry=100 → SL=102.0, TP=97.0
- ✅ V2 SL/TP identiek aan V1 bij zelfde constanten
- ✅ Alle bestaande 49 unit tests nog groen (geen regressie)

## Bronbestanden (LEES ONLY, geen aanpassingen)

- `/mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/projects/crypto-tradebot/scripts/strategies/v1_strategy.py`
- `/mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/projects/crypto-tradebot/scripts/strategies/v2_strategy.py`

## Testbot pad

`/mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/projects/crypto-test-bot-v3/`

## Volgende stappen (STAP U)

- [ ] Backtest draaien op ADAEUR + LINKEUR (2 jaar data) voor V1/V2 resultaten
- [ ] V1/V2 resultaten vergelijken met live tradebot historiek
- [ ] Paper trading starten voor alignment data
