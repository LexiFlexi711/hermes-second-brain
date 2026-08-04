# Taak: Strategy Audit V1 en V2

**Van:** Claude  
**Datum:** 2026-06-01  
**Prioriteit:** Hoog  

---

## Context

Lexi heeft vandaag V1 en V2 pullback traders geoptimaliseerd via grid search.
De nieuwe params (grid winners) zijn al live gezet:

- **V1:** SL=4%, TP=5%, max_lateness=40%, min_impulse=3%
- **V2:** SL=3%, TP=5%, max_lateness=0.40, min_impulse=3%

Maar voor we de params als definitief beschouwen, moet de **strategie-logica zelf** geauditeerd worden.
Bij de range trader vonden we twee bugs VOOR de grid (BTC macro filter blokkeert longs, SL/TP niet range-gebaseerd).
Hetzelfde risico bestaat voor V1 en V2.

---

## Taak

Doe een **diepte-audit** van de V1 en V2 strategie-implementatie.

Bestanden:
- V1 live: `/mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/projects/crypto-tradebot/scripts/pullback_trader.py`
- V1 strategy: `/mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/projects/crypto-tradebot/scripts/strategies/v1_strategy.py`
- V2 live: `/mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/projects/crypto-tradebot/scripts/pull_backtrader_2.py`
- V2 strategy: `/mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/projects/crypto-tradebot/scripts/strategies/v2_strategy.py`
- Testbot V1: `/mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/projects/crypto-test-bot-v3/src/crypto_test_bot_v3/strategies/v1/`
- Testbot V2: `/mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/projects/crypto-test-bot-v3/src/crypto_test_bot_v3/strategies/v2/`

---

## Wat te controleren

Voor **elke** van de volgende punten: bewijs tonen (coderegel + uitleg), niet alleen "lijkt ok".

### 1. Entry logica
- Klopt de fib-berekening (V1: fib_pct berekening, V2: pullback_fib)?
- Is de lateness-berekening correct? Blokkeert die de juiste entries?
- Zijn er filters die systematisch een richting (LONG of SHORT) blokkeren?
- Zijn direction (long/short) en de bijbehorende checks consistent?

### 2. SL/TP berekening
- Wordt SL_PCT correct toegepast per richting (long vs short)?
- Is er een discrepantie tussen wat de docstring zegt en wat de code doet?
- Klopt de TP berekening? (V2 gebruikt mogelijk SL_PCT × RR in plaats van TP_PCT)

### 3. Trailing stop
- Activeert de trailing stop op het juiste moment?
- Is er een race condition: kan trailing_sl slechter zijn dan stop_loss bij entry?
- Wordt TRAIL_DISTANCE_PCT consistent gebruikt?

### 4. State / persistentie
- Worden open trades correct geladen uit state file bij herstart?
- Kan een herstart leiden tot dubbele entries of verloren trades?

### 5. Live vs backtest discrepantie
- Zijn er logische verschillen tussen de live trader en de testbot strategy?
- Worden dezelfde params gebruikt (V2 importeert _calc_sl_tp uit v2_strategy.py)?

### 6. Bekende anomalie V2
- V2 live WR was 27% terwijl backtest 40% toonde. Is er een reden in de code?
- V2 TP_PCT=0.05 staat in v2_strategy.py maar TP lijkt berekend als SL_PCT × RR. Klopt dat?

---

## Output

Schrijf je bevindingen naar:
`/home/sjoe/system/hermes-second-brain/second-brain/tasks/done/strategy-audit-v1-v2-resultaat.md`

Gebruik dit formaat per bevinding:
```
## [V1|V2] — [Component] — [OK / BUG / RISICO / VRAAG]
Bestand: <pad>:<regel>
Bevinding: <wat je ziet>
Impact: <wat dit betekent voor live trading>
Aanbeveling: <wat er gedaan moet worden>
```

Wees concreet. Geen "mogelijk" zonder coderegel als bewijs.

---

## Niet doen

- Geen code aanpassen
- Geen nieuwe strategie voorstellen
- Geen parameters wijzigen
- Alleen lezen en rapporteren
