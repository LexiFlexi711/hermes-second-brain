# Taak: Strategy Audit Range Trader

**Van:** Claude  
**Datum:** 2026-06-01  
**Prioriteit:** Hoog  

---

## Context

De range trader is vandaag gefixed na een eerste audit door Claude:

**Bug #1 (gefixed):** BTC macro filter blokkeerde longs systematisch (`btc_trend == "bear" → skip long`). Filter verwijderd.

**Bug #2 (gefixed):** SL/TP was vast (2%/3%) terwijl docstring zei "SL 1% buiten range, TP 65% van range". Nu correct: `SL = range_low * 0.99`, `TP = range_low + range_width * 0.65`.

**Backtest na fix:** WR 71.4% (was 36.4%), LONG nu 71% WR (was 0%).

Maar de audit was snel gedaan. Hermes moet nu een **diepte-audit** doen zoals gedaan voor V1/V2.

---

## Bestanden

- Range live: `/mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/projects/crypto-tradebot/scripts/range_trader.py`
- Range strategy: `/mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/projects/crypto-tradebot/scripts/strategies/range_strategy.py`
- Range backtest: `/mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/projects/crypto-tradebot/scripts/range_backtest.py`
- Range selector: `/mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/projects/crypto-tradebot/scripts/range_selector.py`

---

## Wat te controleren

### 1. Range detectie logica
- Is `detect_range` correct? Gebruikt `max_high` en `min_low` van 20 candles — maar één spike bepaalt de range. Is dat wenselijk?
- Touch tolerance = `range_width * 0.03`. Is dat consistent voor kleine én grote ranges?
- `_has_trend` vergelijkt laatste 10 vs vorige 10 candles. Is dat een robuuste trendcheck?

### 2. Entry logica
- `ENTRY_ZONE = 0.25`: entry in bodem/top 25% van range. Klopt dat met de `position` berekening?
- `position = (current - range_low) / range_width` — is dit correct voor zowel LONG als SHORT?
- De 15M bevestiging (`_bullish_confirm`, `_bearish_confirm`): zijn deze robuust? Werken ze voor beide richtingen correct?

### 3. SL/TP (na fix)
- LONG: `SL = range_low * 0.99`, `TP = range_low + range_width * 0.65`
- SHORT: `SL = range_high * 1.01`, `TP = range_high - range_width * 0.65`
- Is de TP bij LONG correct richting het midden? `range_low + 0.65 * width` = 65% van de range. Klopt dat?
- Is de RR (1.5) consistent met de range-gebaseerde SL/TP? Of is RR nu een zinloze constante?

### 4. Trailing stop
- `rr1 = ep + sl_dist` (voor LONG) — trailing activeert op 1× SL-afstand. Met range-gebaseerde SL is SL-afstand nu variabel. Klopt de trailing activatie nog?
- Is er een race condition: kan `trailing_sl` slechter zijn dan `stop_loss` bij entry?

### 5. Range break check
- `_range_broken`: 0.5% buffer (`range_high * 1.005`). Is die buffer genoeg?
- Worden breakouts in BEIDE richtingen correct gecanceld voor zowel LONG als SHORT?
- Bug check: als een SHORT trade geopend is en prijs sloopt door range_low, wordt die dan ook gecanceld? (range break = slecht voor SHORT)

### 6. Backtest vs live discrepantie
- Backtest: 14 trades, WR 71%. Live (pre-fix): 8 trades, WR 75%.
- Zijn er filters in live die niet in de backtest zitten (of omgekeerd)?
- `range_backtest.py` gebruikt `pending_entry` patroon (entry op volgende 15M open). Klopt dit met live timing?

### 7. Universe coverage
- Range trader heeft maar 11 backtest-trades over 88 pairs in 1 jaar. Is dat realistisch, of filtert `detect_range` te streng?
- Wat % van pairs zit in range op een gemiddeld moment? Is de `range_quality` check ("weak", "ok", "strong") zinvol?

---

## Output

`/mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/second-brain/tasks/done/strategy-audit-range-resultaat.md`

Zelfde formaat als V1/V2 audit:
```
## [Component] — [OK / BUG / RISICO / VRAAG]
Bestand: <pad>:<regel>
Bevinding: <wat je ziet>
Impact: <effect op live trading>
Aanbeveling: <wat te doen>
```

---

## Niet doen

- Geen code aanpassen
- Geen nieuwe strategie voorstellen  
- Alleen lezen en rapporteren
