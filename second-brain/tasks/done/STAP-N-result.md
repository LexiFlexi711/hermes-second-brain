---
type: report
created: 2026-05-29
source: Hermes (STAP-N uitvoering)
status: done
---

# STAP N — Trailing stop implementatie V1 en V2

## Gewijzigde bestanden

### 1. `scripts/pullback_trader.py` (V1)
- **`_check_outcome`** (regel 356): floating PnL trail toegevoegd vóór bestaande SL/TP check
  - BE bij +1%: `stop_loss` naar entry price
  - Trail bij +2%: trailing SL op 1% afstand van beste koers
  - Updates `trailing_sl`, `trail_best` en `stop_loss` in trade dict
  - Logging: `[TRAIL]` bij trail update, `[BE]` bij break-even
- **monitoring loop** (regel 492): detecteert ook `stop_loss` wijzigingen voor state save

### 2. `scripts/pull_backtrader_2.py` (V2)
- **`check_outcome`** (regel 350): identieke floating PnL trail logica toegevoegd
- **monitoring loop** (regel 839): detecteert ook `stop_loss` wijzigingen voor state save

## Implementatie details
- `trail_best` wordt geïnitialiseerd bij eerste trail-activatie en opgeslagen in state
- SL mag nooit verslechteren: alleen verhogen voor long, alleen verlagen voor short
- Bestaande trailing na TP-hit blijft intact
- V3, Momentum, Range: niet aangeraakt

## Veiligheidsregels
- SL wordt nooit verlaagd voor long (alleen verhoogd via trail)
- SL wordt nooit verhoogd voor short (alleen verlaagd via trail)
- `trail_best` wordt opgeslagen in state JSON (overleeft herstart)
- Als candle data ontbreekt: geen trail update, geen fout