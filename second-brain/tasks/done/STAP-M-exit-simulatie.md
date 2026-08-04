# STAP M — Exit management simulatie op bestaande MFE/MAE data

## Doel

Simuleer twee exit-regels op de bestaande trade data en bereken wat het resultaat geweest zou zijn.
Geen live code aanpassen. Alleen simuleren op historische trades.

## Input bestand

```
/mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/projects/crypto-tradebot/logs/mfe_mae/mfe_mae_analyse.json
```

Per trade zijn beschikbaar:
- `mfe_pct` — hoogste floating winst ooit
- `mae_pct` — diepste dip ooit
- `pnl_pct` — gerealiseerde PnL
- `reached_1pct` / `reached_2pct` / `reached_3pct` — booleans
- `outcome` — WIN / LOSS
- `candles_in_trade`

## Script pad

```
/mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/projects/crypto-tradebot/scripts/exit_sim.py
```

## Te simuleren regels

### Regel A — Break-even stop

> Als trade +1% bereikt: SL naar entry (0% PnL).

Simuleer voor elke trade:
```
als reached_1pct == True:
    gesimuleerde_pnl = max(0.0, pnl_pct)   # minimaal break-even
    gesimuleerd_outcome = "WIN" als gesimuleerde_pnl > 0 else "BREAK_EVEN"
anders:
    gesimuleerde_pnl = pnl_pct              # ongewijzigd
    gesimuleerd_outcome = outcome
```

### Regel B — Trailing stop na +2%

> Als trade +2% bereikt: exit op (MFE - 1%).

Simuleer voor elke trade:
```
als reached_2pct == True:
    gesimuleerde_pnl = mfe_pct - 1.0        # trail op 1% afstand van MFE
    gesimuleerd_outcome = "WIN" als gesimuleerde_pnl > 0 else "LOSS"
anders als reached_1pct == True:
    gesimuleerde_pnl = max(0.0, pnl_pct)   # break-even bescherming
    gesimuleerd_outcome = "WIN" als gesimuleerde_pnl > 0 else "BREAK_EVEN"
anders:
    gesimuleerde_pnl = pnl_pct
    gesimuleerd_outcome = outcome
```

### Combinatie A+B

Pas beide regels samen toe (dat is wat we eigenlijk willen implementeren).

## Output per strategie

Voor elke strategie (V1, V2, V3, Momentum, Range):

```
=== V1 ===
                   Trades   WR%    Total PnL   Avg trade
Origineel:           17    17.6%    -21.3%      -1.25%
Regel A (BE):        17    47.1%     -8.4%      -0.49%
Regel B (trail):     17    52.9%    +12.7%      +0.75%
Combinatie A+B:      17    52.9%    +14.2%      +0.83%

Verliezers gered door BE stop:     7
Verliezers verbeterd door trail:   5
```

## Output bestanden

```
logs/mfe_mae/exit_sim_resultaten.json
logs/mfe_mae/exit_sim_rapport.md
```

## Gebruik

```bash
cd /mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/projects/crypto-tradebot
python3 scripts/exit_sim.py
```

## Verificatie

- Alle 5 strategieën verwerkt
- Origineel vs A vs B vs A+B naast elkaar
- Geen externe dependencies (alleen stdlib)
- JSON + markdown aangemaakt

## Geen live aanpassingen

Dit script leest alleen — het schrijft niets naar traders, state files of trade logs.

## Resultaat schrijven

```
/home/sjoe/system/hermes-second-brain/second-brain/tasks/done/STAP-M-result.md
```
