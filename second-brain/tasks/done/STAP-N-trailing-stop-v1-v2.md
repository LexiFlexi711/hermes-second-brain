# STAP N — Trailing stop implementatie V1 en V2

## Context

Simulatie (STAP-M) bewijst:
- V1 zonder trailing: -18.07% → met trailing: +36.88%
- V2 zonder trailing: -25.12% → met trailing: +9.58%
- Momentum: NIET aanpassen (wordt slechter)
- V3: NIET aanpassen (ander probleem)

## Regel die geïmplementeerd wordt

**Break-even bij +1%:** als floating PnL >= +1% → verplaats SL naar entry price.
**Trailing bij +2%:** als floating PnL >= +2% → trail SL op 1% afstand van beste koers.

Trail updaten elke cycle. Nooit SL verlagen.

## Bestand 1: `scripts/pullback_trader.py` (V1)

### Zoek de open trade loop

V1 beheert open trades via `pullback_state.json`. In de loop die open trades controleert:

```python
# Zoek naar iets als:
current_price = ...
entry_price = trade['entry_price']
stop_loss = trade['stop_loss']
take_profit = trade['take_profit']
direction = trade['direction']  # 'long' of 'short'
```

### Voeg toe VOOR de SL/TP check

```python
# ── Trail management ──────────────────────────────────────────
if direction == 'long':
    floating_pct = (current_price - entry_price) / entry_price * 100
    best_price = trade.get('trail_best', entry_price)
    if current_price > best_price:
        trade['trail_best'] = current_price
        best_price = current_price
    if floating_pct >= 2.0:
        new_trail_sl = round(best_price * 0.99, 8)
        if new_trail_sl > stop_loss:
            stop_loss = new_trail_sl
            trade['stop_loss'] = stop_loss
    elif floating_pct >= 1.0:
        be_sl = entry_price
        if be_sl > stop_loss:
            stop_loss = be_sl
            trade['stop_loss'] = stop_loss
else:  # short
    floating_pct = (entry_price - current_price) / entry_price * 100
    best_price = trade.get('trail_best', entry_price)
    if current_price < best_price:
        trade['trail_best'] = current_price
        best_price = current_price
    if floating_pct >= 2.0:
        new_trail_sl = round(best_price * 1.01, 8)
        if new_trail_sl < stop_loss:
            stop_loss = new_trail_sl
            trade['stop_loss'] = stop_loss
    elif floating_pct >= 1.0:
        be_sl = entry_price
        if be_sl < stop_loss:
            stop_loss = be_sl
            trade['stop_loss'] = stop_loss
# ─────────────────────────────────────────────────────────────
```

### State opslaan

`trail_best` moet mee opgeslagen worden in `pullback_state.json` zodat het overleeft bij herstart.
Als het veld nog niet bestaat in bestaande open trades: initialiseer op `entry_price`.

## Bestand 2: `scripts/pull_backtrader_2.py` (V2)

Zelfde logica. V2 gebruikt `v2_state.json`.

Zoek de open trade monitor loop en voeg identieke trail management toe.
Veldnamen kunnen licht verschillen — pas aan waar nodig maar logica blijft gelijk.

## Wat NIET aanraken

- `pull_backtrader_3.py` (V3) — niet aanpassen
- `momentum_trader.py` of equivalent — niet aanpassen
- `range_trader.py` — niet aanpassen
- Entry logica — niet aanpassen
- TP logica — niet aanpassen
- Bestaande SL checks — alleen uitbreiden, niet verwijderen

## Logging

Voeg een log toe wanneer trail/BE actief wordt:

```python
print(f"[TRAIL] {trade['pair']} {direction} floating={floating_pct:.2f}% → SL={stop_loss}")
```

## Verificatie door grote broer (Claude)

Na implementatie: geen herstart nodig van grote broer. Grote broer verifieert de code zelf.
Hermes hoeft de traders NIET te herstarten.

## Veiligheidsregels

- SL mag nooit verlaagd worden voor long (alleen verhogen)
- SL mag nooit verhoogd worden voor short (alleen verlagen)
- trail_best initialiseren op entry_price als veld ontbreekt
- Als current_price niet beschikbaar: geen trail update, geen fout

## Resultaat schrijven

```
/home/sjoe/system/hermes-second-brain/second-brain/tasks/done/STAP-N-result.md
```

Vermeld welke regels gewijzigd zijn in beide bestanden (bestandsnaam + regelnummer).
