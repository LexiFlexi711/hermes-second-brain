# Hermes Vervolg — Chartlezer naar Trade Assessment

**Datum:** 2026-06-13
**Context:** Hermes heeft nu alle layers op hun plaats. Tijd voor de volgende stap.

---

## Huidige Hermes — Wat we hebben

```
Layer 1: Data (fetch_kraken, 200 candles, OHLC)
Layer 2: Fractals + Major trendlines (upper/lower, active local)
Layer 2v2: Swings + S/R zones + pivot blocks
Layer 3: D/U/R fase-detectie (range labeling)
Layer 4: Major structuur labels (HH/HL/LH/LL/EH/EL)
Layer 4a: Recent active trendlines (laatste swing + 5 vorige)
Layer 5: Visuele cockpit (combineert L2/L3/L4/L4a)
Layer 6: Placeholder
```

**Wat Hermes NU al kan zeggen:**
- Major trend: bearish/bullish channel, compression, expansion, wedge
- Recente trend: up/down/squeeze/unclear (L4a)
- Structuur: HH/HL/LH/LL sequentie
- Fase: D (down), U (up), R (range)
- S/R zones: waar zit weerstand/support
- Lijnkwaliteit: touches, scores, body violations

**Wat ontbreekt:**
- Synthese: combineert deze nog niet tot 1 coherent marktbeeld
- Micro: wat doen de laatste 3-5 candles?
- Verwachting: wat is de meest waarschijnlijke volgende move?
- Kwaliteit: hoe betrouwbaar is de structuur vandaag?
- Conflictdetectie: L4 zegt channel, L4a zegt squeeze — wat weegt door?

---

## Mijn idee: Synthesis Layer (informeel "Layer 7")

Geen nieuwe logica. Geen nieuwe detectie. Enkel een laag die ALLE bestaande layers uitleest en combineert tot een assessment.

### Outputcontract (concept)

```json
{
  "pair": "BTCEUR",
  "timeframe": "5m",
  "timestamp": "...",

  "major": {
    "trend": "bearish_channel",
    "valid": true,
    "quality": 0.72,
    "upper": {...}, "lower": {...}
  },

  "recent": {
    "trend": "squeeze",
    "status": "active",
    "upper": {...}, "lower": {...}
  },

  "phase": {
    "label": "D3",
    "compressed": "D",
    "range_active": false
  },

  "micro": {
    "last_3_candles": "lower_wick_rejection_at_support",
    "last_5_candles": "consolidating_near_lower",
    "buyer_pressure": 0.65,
    "seller_pressure": 0.35,
    "inside_bar": false
  },

  "structure": {
    "last_high": {"label": "LH5", "price": 54963, "age_bars": 15},
    "last_low": {"label": "HL9", "price": 54936, "age_bars": 6},
    "sequence": "LH:LH:LH:HH:LH:EH",
    "momentum": "bearish"
  },

  "expectation": {
    "direction": "bounce_to_upper_range",
    "confidence": 0.55,
    "reason": "price at lower channel, recent lower wick rejection, L4a squeeze converging"
  },

  "tradeable": true,
  "reason": "structure is clean, major lower holds, L4a active — wacht op bevestiging bij upper"
}
```

### Hoe bouwen

Niet als nieuwe laag met complexe logica.
Eerst als **tekstuele read-only output**, bijvoorbeeld:

```
Hermes Assessment — BTCEUR 5m

Structuur: Bearish channel, valid, prijs in onderste helft.
Recent: Squeeze — upper en lower convergeren.
Fase: D3 (range compression).
Micro: Laatste 3 candles long lower wicks op lower channel support.
Verwachting: Bounce naar upper zone (~55050).
Kwaliteit: 72% — redelijk clean, maar upper heeft body violations.
Tradeable: Ja — structuur staat, wacht op bevestiging van de bounce.
```

### Wie gebruikt dit

Deze assessment is wat we geven aan:
- **Testbot**: "Hé testbot, hier is wat Hermes ziet op de chart. Jij mag beslissen of jouw strategie hier een trade van wil maken."
- **Tradebot**: "Hé tradebot, hier is de chartlezing. Als jouw strategie akkoord is, mag je traden."

**Hermes zegt nooit "trade nu".** Hermes zegt enkel:
```
Ik zie: bearish channel, prijs aan lower, bounce verwacht.
Status: tradeable — structuur is clean.
Jij beslist of je traded.
```

---

## Voorstel — Volgende stappen

### Stap 1: Hermes Assessment tekstuele output
Maak een functie `read_assessment(pair, tf)` die alle layers uitleest en een dict + tekst teruggeeft.
- Gebruikt bestaande L1/L2/L3/L4/L4a output
- Voegt micro-analyse toe (laatste 3-5 candles: patronen, wicks, bodies)
- Berekent kwaliteitsscore obv touches, violations, span
- Bepaalt verwachting obv structuur + micro

### Stap 2: Hermes API endpoint
`/v7/assessment/<pair>/<tf>` — geeft JSON + optioneel tekst.

### Stap 3: Integratie met testbot/tradebot
Testbot en tradebot krijgen Hermes assessment als input.
Zij beslissen of ze traden — Hermes niet.

---

## Waarom dit werkt

1. **Alles is er al** — L1 t/m L4a produceren alle data die we nodig hebben
2. **Geen nieuwe detectie** — enkel combinatie + interpretatie
3. **Clean separation** — Hermes leest charts, strategieën traden
4. **Testbaar** — assessment kan vergeleken worden met wat er écht gebeurde
5. **Uitbreidbaar** — nieuwe inzichten = nieuwe velden in assessment, geen nieuwe detectie

---

## Risico's

| Risico | Mitigatie |
|---|---|
| Assessment wordt te vaag | Harde regels: elk statement moet uit layer-data komen |
| Kwaliteitsscore is subjectief | Gebruik bestaande metrics: touches, body_violations, span |
| Micro-analyse wordt te complex | Beperk tot laatste 5 candles, simpele patronen |
| Verwachting is altijd fout | Geef confidence mee, documenteer waarom |
| Tradeable flag wordt verkeerd gebruikt | Hermes zegt nooit "trade", enkel "tradeable structuur" |

---

## Voorstel volgende prompt

```
BUILD — Layer 7 Hermes Assessment module

Maak:
projects/hermes-v01/layer7_assessment/hermes_assessment.py

Functie:
read_assessment(pair, tf) → dict met major, recent, phase, micro, expectation, tradeable

Gebruik:
- read_structure() uit director (L1/L2/L3/L4)
- read_recent_trendlines() uit L4a
- micro-analyse: laatste 5 candles (wicks, bodies, inside/outside, consecutieve closes)
- quality score obv touches/violations/span

Endpoint:
/v7/assessment/<pair>/<tf> → JSON

Geen trade signals. Enkel assessment.
```

**STOP.** Wat denk je, Sjoe? Zin om deze richting uit te gaan?
