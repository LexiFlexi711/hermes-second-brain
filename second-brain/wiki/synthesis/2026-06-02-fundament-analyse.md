---
type: synthesis
id: fundament-analyse-2026-06-02
tags: [candle-battle, test-bot, strategie, herbouw]
---

# Fundament Analyse — Wat is er fout en hoe lossen we het op

**Datum:** 2026-06-02
**Status:** Concept

---

## 1. De Candle Battle Reader — wat het is en waarom het niet gebruikt wordt

De **candle battle reader** (`candle_battle_reader.py` in de oude tradebot) is
een **narratieve analyse-laag** die per candle beschrijft wat er gebeurt:

- Wie probeerde wat (buyer attempt / seller attempt)
- Hoe reageerde de markt op extremen (high/low reaction)
- Wie won de close (close result)
- Hoe beslissend was de win (dominance)
- Wat bewijst deze candle (proof)
- Wat moet de volgende candle bevestigen (not yet proven)

**Filosofie:** "Candles are the primary truth. No indicators. No patterns.
No scores. No trades."

**Waarom is het nooit geïntegreerd?** Omdat de bot van dag 1 gebouwd is op
aannames over wat "trend", "pullback" en "range" betekenen, in plaats van op
wat de candles werkelijk tonen. De candle battle reader was een apart project
dat nooit gekoppeld is aan de handelslogica.

---

## 2. Wat is er fout in de test-bot strategieën

### V2 logic — find_pullback_leg (lijn 136-170)

**Wat het doet:** Zoekt swing highs/lows met `find_swings(c4h, n=2)` en meet
of de afstand tussen high en low groter is dan `min_impulse_pct`.

**Waarom het fout is:**
- `n=2` betekent: een swing high is een candle met 2 lagere highs links en
  rechts. Dat is **geen fractaal**. Een fractaal heeft minstens 2 lagere highs
  aan elke kant, wat betekent dat `n` ≥ 2. Maar met `n=2` en `range(2, len-2)`
  krijg je swings die te klein zijn om betekenisvol te zijn.
- De impuls wordt gemeten als `(high - low) / high`. Dat is de **totale
  beweging** tussen twee swings, niet de **impuls** die de pullback definieert.
- Er wordt geen onderscheid gemaakt tussen een impuls (snelle move) en een
  correctie (langzame terugkeer).

### V2 logic — detect_trend (lijn 56-77)

**Wat het doet:** Vergelijkt de laatste 2 swing highs/lows.

**Waarom het fout is:**
- Twee swings zijn genoeg om "up" of "down" te zeggen. Dat is **te weinig**
  voor een trend. Een trend heeft meerdere HH/HL nodig, niet 2.
- `clearly_higher(a, b) = (a-b)/b > 0.002` — de tolerance is 0.2%. Dat is
  kleiner dan de spread op sommige coins. Structurele bewegingen van <0.2%
  worden als "signaal" beschouwd.

### V2 logic — check_setup (lijn 225-276)

**Wat het doet:** Combineert trend + leg + fib + volume + confirm.

**Waarom het fout is:**
- `fib_label` splitst de retracement in zones (forming, early, ideal, deep,
  trend_break). Maar de zones zijn **arbitrair** (30%, 38.2%, 61.8%, 70%).
  Deze getallen komen uit de klassieke fib, maar zonder context (vorige
  impuls lengte, volatiliteit) zijn het slechts aannames.
- `lateness` wordt berekend uit fib: hoe dieper de pullback, hoe later.
  Maar "later" betekent niet "slechter" — sommige van de beste trades komen
  uit diepe pullbacks.
- `volume_ok_for_leg` checkt of het gemiddelde volume in de bounce niet meer
  dan 1.5x het impuls volume is. Deze drempel is willekeurig.

### Range logic — detect_range (lijn 26-76)

**Wat het doet:** Neemt de laatste N 4H candles, berekent min/max, checkt
of de range tussen 2-12% ligt, en of er minstens 2 touches aan elke kant.

**Waarom het fout is:**
- Een range is **geen** "max - min over 20 candles". Een range is een zone
  waar de prijs **blijft hangen** tussen twee niveaus die elkaar afwisselen
  als support/resistance.
- `_has_trend()` filtert alles weg wat een trend lijkt. Maar tijdens een
  trend kunnen ook ranges ontstaan (consolidatie). Die worden gemist.
- Twee touches is te weinig voor een betrouwbare range.

### V1 logic — is_bearish_structure / is_bullish_structure

**Wat het doet:** Vergelijkt de max high / min low van twee windows van 10
candles.

**Waarom het fout is:**
- Dit detecteert of het **maximum** van de laatste 10 candles lager is dan
  het maximum van de 10 daarvoor. Dat is **geen** bearish structuur — het
  zegt enkel dat de hoogste high van de recente periode lager is.
- Een echte bearish structuur heeft **lagere highs EN lagere lows** (LL/LH).
  Deze check mist de helft van het plaatje.

---

## 3. De rode draad: aannames in plaats van metingen

| Wat de bot denkt | Wat het werkelijk is |
|-----------------|---------------------|
| "Swing high" | Een candle met n lagere buren |
| "Trend" | Twee swings in dezelfde richting |
| "Range" | Min/max over N candles met 2 touches |
| "Pullback" | Een fib retracement naar een willekeurige impuls |
| "Support" | De laagste prijs in N candles |
| "Resistance" | De hoogste prijs in N candles |

---

## 4. Oplossingsvoorstel: herbouw op candle-filosofie

### Fase 1 — Fractaal-structuur (week 1)

Vervang `find_swings` door echte fractaal-detectie:

- Fractale top = high met minstens 2 lagere highs links en 2 lagere highs rechts
- Fractale bodem = low met minstens 2 hogere lows links en 2 hogere lows rechts

Dit is de **Bill Williams fractaal**. Het is simpel, robuust, en werkt al
decennia.

**Waarom fractals beter zijn:**
- Ze filteren ruis — kleine prijsbewegingen worden genegeerd
- Ze geven betekenisvolle swing punten
- Ze zijn tijdonafhankelijk — werken op 15M, 4H, 1D

### Fase 2 — Support/Resistance (week 2)

S/R niveaus op basis van fractals:

- **Sterke S/R**: meerdere fractals op hetzelfde niveau (cluster)
- **Matige S/R**: een enkele fractal met duidelijke impuls
- **Trendlijnen**: verbind fractals voor dynamische S/R

Dit is wat `candle_battle_reader._detect_higher_lows` al probeert, maar dan
structureel.

### Fase 3 — Range detectie op basis van consolidatie (week 2-3)

Een range is geen min/max, maar:

- Minstens 2 fractale bodems op ongeveer hetzelfde niveau
- Minstens 2 fractale toppen op ongeveer hetzelfde niveau
- De prijs blijft tussen deze niveaus
- Het volume neemt af (consolidatie)

### Fase 4 — Strategieën herbouwen op fractalen (week 3-4)

- **Pullback**: trend (HH/HL) → impuls (snelle fractaal) → retracement (fib naar vorige fractaal)
- **Range**: consolidation (fractale S/R) → entry aan de rand → TP naar de andere kant
- **Breakout**: consolidatie → doorbraak van fractale S/R met volume

---

## 5. Conclusie

De test-bot is structureel gezond (pipeline, reader, runner, reporting), maar
de **marktdefinities** zijn fout. De strategieën vertrouwen op willekeurige
drempels en te kleine samples.

De **candle battle reader** toont de juiste filosofie: candles zijn de
primaire waarheid. Die filosofie moet de basis worden van de herbouw.

**Niet doen:**
- Verder tunen van parameters op de huidige logica
- Grid search draaien zonder fundament

**Wel doen:**
- Fractaal-detectie bouwen
- S/R op fractalen
- Strategieën herbouwen
- Valideren op TradingView (Pine Script) voor implementatie in Python
