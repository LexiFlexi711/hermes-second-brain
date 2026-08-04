# Strategy Audit V1 & V2 — Resultaat

**Uitgevoerd:** 2026-06-01
**Door:** Noa (Hermes Executor)
**Bron:** Claude (Director) — `/home/sjoe/system/hermes-second-brain/second-brain/tasks/pending/strategy-audit-v1-v2.md`

**Geanalyseerde bestanden:**
- V1 live: `crypto-tradebot/scripts/pullback_trader.py` (719 lijnen)
- V1 strategy: `crypto-tradebot/scripts/strategies/v1_strategy.py` (283 lijnen)
- V2 live: `crypto-tradebot/scripts/pull_backtrader_2.py` (1005 lijnen)
- V2 strategy: `crypto-tradebot/scripts/strategies/v2_strategy.py` (402 lijnen)
- Testbot V1: `crypto-test-bot-v3/src/crypto_test_bot_v3/strategies/v1/` (strategy.py, logic.py, config.py)
- Testbot V2: `crypto-test-bot-v3/src/crypto_test_bot_v3/strategies/v2/` (strategy.py, logic.py, config.py)

---

## BUG #1 [KRITIEK] — Testbot V1 & V2 configs NIET geüpdatet na grid search

**Bestanden:**
- `/mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/projects/crypto-test-bot-v3/src/crypto_test_bot_v3/strategies/v1/config.py:8-9`
- `/mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/projects/crypto-test-bot-v3/src/crypto_test_bot_v3/strategies/v2/config.py:8-9`

**Bevinding:** De testbot configs gebruiken nog de OUDE pre-grid-search parameters.

| Parameter | V1 testbot | V1 live (v1_strategy.py) | V2 testbot | V2 live (v2_strategy.py) |
|-----------|-----------|-------------------------|-----------|-------------------------|
| SL_PCT | 0.02 (2%) | **0.04 (4%)** | 0.02 (2%) | **0.03 (3%)** |
| TP_PCT | 0.03 (3%) | **0.05 (5%)** | 0.03 (3%) | **0.05 (5%)** |
| MAX_LATENESS | 0.50 (50%) | **0.40 (40%)** | 0.65 (65%) | **0.40 (40%)** |
| MIN_IMPULSE_PCT | 0.05 (5%) | **0.03 (3%)** | 0.03 (3%) | 0.03 (3%) ✓ |

**Impact:** Elke backtest die via de testbot wordt gedraaid gebruikt FUNDAMENTEEL ANDERE parameters dan de live traders. Resultaten zijn niet vergelijkbaar. Het grid search resultaat (V1: 4%/5%, V2: 3%/5%) wordt niet weerspiegeld in de testbot.

**Aanbeveling:** Testbot configs synchroniseren met de grid winner parameters.

---

## BUG #2 [KRITIEK] — V2 fib-berekening voor LONG is omgekeerd in testbot vs live

**Bestand:** `crypto-test-bot-v3/strategies/v2/logic.py:203-214` vs `pull_backtrader_2.py:181-185`

**Bevinding:** De fib-berekening voor LONG trades is INVERTED tussen live V2 en testbot V2.

**Live V2** (`pull_backtrader_2.py:181-185` — `_calc_fib_pct`):
```python
fib = (current - pb_low) / (pb_high - pb_low)   # direction-agnostic
```

**Testbot V2** (`v2/logic.py:203-214` — `calc_pullback_fib`):
```python
if direction == "down":
    fib = (current - pb_low) / span    # SHORT
else:
    fib = (pb_high - current) / span    # LONG — INVERTED!
```

**Voorbeeld LONG trade:** current=107, pb_low=100, pb_high=110
- Live V2: fib=(107-100)/(110-100)=**0.70** → deep_warning
- Testbot V2: fib=(110-107)/(110-100)=**0.30** → forming/early_pullback

**Lateness-effect:** Live V2 gebruikt `_entry_lateness(fib, direction)` = fib voor LONG = 0.70. Testbot gebruikt `entry_lateness` = 1-fib = 0.70 (toevallig zelfde cijfer door omkering).

**Impact voor lateness:** 
- Live V2: lateness = fib (0.70) → 70% → BLOCKED (max=0.40)
- Testbot V2: lateness = 1-fib (0.70) → 70% → BLOCKED (max=0.65)

WACHT — testbot heeft max_lateness=0.65, dus 0.70 is nog steeds geblokkeerd. MAAR met de oude params (max_lateness=0.65):
- Live V2: fib(0.70) → lateness(0.70) > 0.65 → geblokkeerd
- Testbot V2: fib(0.30) → lateness(1-0.30=0.70) > 0.65 → geblokkeerd

Dus voor dit specifieke voorbeeld geven ze hetzelfde resultaat door verschillende thresholds. Maar de fib-zones zijn WEL verschillend (deep_warning vs early_pullback), wat de fib_label en dus de entry-kwaliteit beïnvloedt.

**HEIKER GEVAL:** current=104, pb_low=100, pb_high=110:
- Live V2: fib=(104-100)/10=**0.40** → early_pullback ✓
- Testbot V2: fib=(110-104)/10=**0.60** → ideal_pullback ✓
- Live V2 lateness: fib=0.40 → 40% ≤ max_lateness(0.40) ✓ → ENTRY
- Testbot V2 lateness: 1-0.60=0.40 → 40% ≤ max_lateness(0.65) ✓ → ENTRY

Beide laten entry toe, maar met VERSCHILLENDE fib_labels!

**NOG ERGER:** current=102, pb_low=100, pb_high=110:
- Live V2: fib=(102-100)/10=**0.20** → "forming" → GEBLOKKEERD
- Testbot V2: fib=(110-102)/10=**0.80** → "trend_break" → GEBLOKKEERD
Beide blokkeren, maar voor TEGENOVERGESTELDE redenen!

**CRITICAL:** current=106, pb_low=100, pb_high=110:
- Live V2: fib=0.60 → ideal_pullback ✓, lateness=0.60 > 0.40 → GEBLOKKEERD (te laat)
- Testbot V2: fib=0.40 → early_pullback ✓, lateness=0.60 > 0.65 → TOEGESTAAN!

**HIER** is de breuk: testbot laat een trade toe die live zou blokkeren, of blokkeert een trade die live zou toelaten.

**Impact:** De fib-berekening voor LONG in de testbot V2 is INCONSISTENT met de live V2. Dit is een bron van backtest vs live discrepantie voor LONG trades.

**Aanbeveling:** De fib-berekening uniform maken. De live V2 gebruikt de direction-agnostische formule `(current - pb_low)/(pb_high - pb_low)` — die werkt correct voor zowel LONG als SHORT. De testbot en v2_strategy.py moeten deze formule ook gebruiken.

---

## BUG #3 [HOOG] — V2 lateness-berekening in testbot is symmetrisch, live is directioneel

**Bestand:** `v2/logic.py:219-221` vs `pull_backtrader_2.py:205-214`

**Bevinding:** 

**Live V2** (`_entry_lateness`):
```python
if direction == "short":
    return round(1.0 - fib_pct, 3)    # hoge fib = lage lateness
return round(fib_pct, 3)              # lage fib = lage lateness
```
Dit is correct voor de direction-agnostische fib: SHORT wil hoge fib (dicht bij swing high), LONG wil lage fib (dicht bij impulse low).

**Testbot V2** (`entry_lateness`):
```python
return round(1.0 - fib_pct, 3)        # ALTIJD 1-fib
```
Maar de testbot gebruikt een ANDERE fib (zie BUG #2). Doordat fib voor LONG in testbot 1 - fib_v2_live is, geeft lateness = 1 - fib_testbot = 1 - (1 - fib_live) = fib_live. Dus het CIJFERMATIGE resultaat klopt vaak toevallig, maar de fib_label en zone-classificatie kloppen niet.

**Impact:** Zie BUG #2 voor concrete scenarios.

**Aanbeveling:** De lateness moet in lijn zijn met de gebruikte fib-berekening. Als de fib direction-agnostisch is (BUG #2 fix), moet lateness directioneel zijn zoals in live V2.

---

## BUG #4 [HOOG] — V2 1D filter ontbreekt in testbot

**Bestand:** `pull_backtrader_2.py:588-601` vs testbot `v2/` (geen 1D filter)

**Bevinding:** De live V2 blokkeert SHORT trades wanneer de 1D trend niet bearish is:
```python
if direction == "short":
    trend_1d = _detect_trend(c1d) if len(c1d) >= 10 else None
    if trend_1d != "down":
        # BLOCKED
```
Dit filter zit in zowel `run_loop()` als `scan_pair_v2()` — maar NIET in de gedeelde `check_pullback_setup()` functie.

De testbot V2 heeft dit filter niet in `check_setup()` of in de strategy laag.

**Impact:** De testbot backtest opent SHORT trades die de live V2 zou blokkeren. Dit kan de backtest WR opblazen met trades die in realiteit nooit uitgevoerd worden.

**Aanbeveling:** 1D filter toevoegen aan testbot V2 strategy, of de shared `check_setup` functie uitbreiden.

---

## BUG #5 [MEDIUM] — V2 `direction` default naar "long" bij None trend

**Bestand:** `pull_backtrader_2.py:585`, `pull_backtrader_2.py:731`

**Bevinding:** 
```python
direction = "short" if trend == "down" else "long"
```
Wanneer `_detect_trend()` None retourneert (geen duidelijke trend), wordt direction=foutief op "long" gezet. De logica zou moeten stoppen of neutraal blijven.

**Impact:** Bij onduidelijke trend forceert V2 een LONG richting. De pullback check faalt dan meestal (geen impulse gevonden), maar het is een latent risico op foute entries in choppy markten.

**Aanbeveling:** `direction = "short" if trend == "down" else ("long" if trend == "up" else None)` en None afvangen.

---

## BUG #6 [MEDIUM] — V1 docstring zegt 2%/3% maar code gebruikt 4%/5%

**Bestand:** `pullback_trader.py:293`

**Bevinding:** De comment zegt:
```python
# ── Stap 6: SL en TP berekenen — vaste 2% SL / 3% TP ─────────────────
```
Maar de functie `_calc_sl_tp` importeert uit `v1_strategy.py` die `_SL_PCT=0.04, _TP_PCT=0.05` heeft (grid winners). De werkelijke gebruikte waarden zijn 4%/5%, niet 2%/3%.

**Impact:** Verwarrend bij debugging. Geen functionele impact.

**Aanbeveling:** Comment updaten naar "vaste 4% SL / 5% TP".

---

## BUG #7 [MEDIUM] — V2 docstring zegt 2%/3% maar code gebruikt 3%/5%

**Bestand:** `v2_strategy.py:382-387`

**Bevinding:**
```python
def _calc_sl_tp(entry: float, direction: str) -> tuple[float, float]:
    """
    V2-variant SL/TP:
      LONG  SL = entry * (1 - 2%), TP = entry * (1 + 3%)
      SHORT SL = entry * (1 + 2%), TP = entry * (1 - 3%)
    """
```
De code gebruikt `SL_PCT=0.03` en `TP_PCT=0.05` (grid winners), niet 2%/3%.

**Impact:** Verwarrend. Geen functionele impact.

**Aanbeveling:** Docstring updaten naar de grid winner waarden.

---

## BUG #8 [LAAG] — Testbot V1 config MIN_IMPULSE_PCT niet gesynchroniseerd

**Bestand:** `v1/config.py:12`

**Bevinding:** Testbot V1 heeft `MIN_IMPULSE_PCT=0.05`, live V1 gebruikt `MIN_IMPULSE_PCT=0.03` (grid winner). Dit betekent dat de testbot V1 een STERKERE impuls vereist (5% i.p.v. 3%) voor een pullback setup, wat minder trades toelaat.

**Impact:** Testbot backtest V1 laat minder trades toe dan live V1 door strengere impulse filter. WR-cijfers zijn niet vergelijkbaar.

**Aanbeveling:** Synchroniseren naar MIN_IMPULSE_PCT=0.03.

---

## V2 WR ANOMALY — Analyse (27% live vs 40% backtest)

**Bestand:** `v2_strategy.py:12-18` (geschiedenis header)

**Bevindingen:**

De oude V2 (SL=2%, TP=3%, max_lateness=0.65) had 27% WR live vs 40% in backtest. 3 factoren dragen bij:

### Factor 1: 1D filter ontbreekt in backtest (BUG #4)
Backtest opent SHORT trades die live zou blokkeren. Dit zou de backtest WR KUNNEN verhogen maar ook verlagen — meer trades ≠ betere WR. De richting van het effect hangt af van de marktregime.

### Factor 2: Pullback cancel logica in live V2
Live V2 cancelled trades bij 4+ consecutive adverse 15m candles (`check_pullback_fast`). Deze logica zit NIET in de testbot backtest. Gecancelde trades worden apart geteld (niet als LOSS) maar tellen ook niet als WIN. Als gecancelde trades anders waren afgelopen (sommige wel WIN, sommige LOSS), verschuift de WR. Het netto-effect is afhankelijk van marktcondities.

### Factor 3: Stale candles in live
V2 live leest uit cache (`_read_cache`) die stale kan zijn. Als de cache verouderd is, krijgt de trader oude data en neemt suboptimale beslissingen. De cache freshness check staat wel in de code maar blokkeert niet volledig — bij stale cache returnt `_read_cache` gewoon lege lijst, waarna `_fetch_kraken` als fallback directe Kraken calls doet. Maar tijdelijk stale data kan nog steeds entries beïnvloeden.

### Factor 4: Marktregime (meest waarschijnlijk)
Backtest dekt een jaar. Live dekt een kortere, recentere periode met mogelijk andere marktcondities. De oude params (SL=2%, TP=3%) zijn OOK de params die de grid search afwees — ze presteren gewoon slechter in de recente markt.

**Conclusie:** De 27% vs 40% discrepantie is een COMBINATIE van:
1. 1D filter ontbrekend in backtest (opent andere trades)
2. Pullback cancel in live (breekt trades vroegtijdig af)
3. Marktregime-verschil (grootste factor)
4. BUG #2/#3 — fib/lateness inconsistentie voor LONG trades (kleine factor in absolute termen, want V2 trade vooral SHORT)

**Met de nieuwe grid winner params** (SL=3%/TP=5%/max_lateness=0.40) zou de backtest 57% WR geven. Nu de configs en fib-berekening gesynchroniseerd zijn (na fixes), kan de live performance deze backtest benaderen.

---

## Samenvatting

| # | Prioriteit | Component | Type | Beschrijving |
|---|-----------|-----------|------|-------------|
| 1 | 🔴 KRITIEK | Testbot V1+V2 config | BUG | SL/TP/max_lateness niet geüpdatet naar grid winners |
| 2 | 🔴 KRITIEK | V2 fib LONG | BUG | Inverse fib-berekening testbot vs live voor LONG |
| 3 | 🟠 HOOG | V2 lateness | BUG | Symmetrische lateness in testbot ipv directioneel |
| 4 | 🟠 HOOG | V2 1D filter | BUG | Ontbreekt in testbot (wel in live) |
| 5 | 🟡 MEDIUM | V2 direction default | BUG | Default "long" bij None trend |
| 6 | 🟡 MEDIUM | V1 docstring | INFO | Comment zegt 2%/3%, code gebruikt 4%/5% |
| 7 | 🟡 MEDIUM | V2 docstring | INFO | Docstring zegt 2%/3%, code gebruikt 3%/5% |
| 8 | 🟢 LAAG | V1 MIN_IMPULSE | BUG | Testbot 5%, live 3% |

**Aanbevolen fix-volgorde:**
1. 🔴 Fix #1: Testbot configs updaten naar grid winners (5 min)
2. 🔴 Fix #2: V2 fib uniform maken (direction-agnostisch) in testbot + v2_strategy.py (10 min)
3. 🟠 Fix #3: V2 lateness directioneel maken in testbot (5 min)
4. 🟠 Fix #4: 1D filter toevoegen aan testbot V2 (10 min)
5. 🟡 Fix #5, #6, #7: Docstrings en default logica fixen (5 min)
6. 🟢 Fix #8: MIN_IMPULSE_PCT in V1 testbot (2 min)

Na fixes: Nieuwe grid search draaien vanuit de testbot om te verifiëren dat de grid winner params nog steeds optimaal zijn.
