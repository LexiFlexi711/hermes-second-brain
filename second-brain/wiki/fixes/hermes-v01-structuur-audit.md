# Hermes v01 — Structuur Audit (2026-06-06)

## Aanleiding
Entry-scan over 10 pairs (28 dagen) gaf tegenstrijdige output: tegelijk LONG en SHORT op dezelfde candle, dagelijkse entries om 04:00, ranges alleen op laatste dag. Opdracht: enkel code lezen en exact aantonen wat fout zit.

## Relevante bestanden

| Pad | Regels | Inhoud |
|-----|--------|--------|
| `projects/hermes-v01/hermes_v01.py` | 430 | Fractalen, zones, trend (diepte=4), consolidatie (20 bars), trendlijnen, market_state, location |
| `projects/hermes-v01/hermes_v02.py` | 483 | ATR, channel_down (parallel upper+lower), indicators, read_market, richtingsscores |
| `research/channel_candidate_eval.py` | 313 | 3 kandidaten (down/up/range) met score-based selectie |
| `research/detector_validation.py` | 272 | Validatie: draait read_market over 500 windows per coin |

## Waarom de output fout wordt

### 1. LONG en SHORT tegelijk op dezelfde candle
- Entry-script evalueert `bearish_upper_close` EN `bullish_lower_close` als aparte condities
- Geen `mutual_exclusivity` check: als beide True zijn, worden BEIDE gerapporteerd
- `macro_trendlijn()` kan een dalende lijn vinden (bv projectie 54068, close 53574) EN `lower_trendlijn()` kan een stijgende lijn vinden (bv projectie 50600, close 53574). Beide binnen 2% = LONG+SHORT.

### 2. Bijna elke dag entry om 04:00
- Scan stapgrootte: 24 bars (1 dag op 1H)
- In dalende markt liggen veel fractale toppen dicht bij een dalende lijn
- Touch tolerantie 0.45% = 270 punten op BTC 60K — te ruim
- "close binnen 2% van lijn" = 1.070 punten op BTC 60K — geen entry-bewijs

### 3. "close binnen 2% van lijn" is geen entry
- `macro_trendlijn()` projecteert een lijn naar huidige bar
- Als lijn BOVEN de prijs staat maar binnen 2%, is het kanaal GEBROKEN — geen weerstand
- SHORT logisch bij NET RAKEN van lijn, niet bij ver onder de lijn staan

### 4. Range vs consolidation niet gescheiden
- `is_consoliderend()` gebruikt 20 bars (minder dan 1 dag)
- Check: range_n < 0.75 × 20 × gem ATR. In rustige markt bijna altijd True
- Geen boven- + ondergrens concept voor range

### 5. Zones te los/breed
- `cluster_fractalen()` in v01: 0.5% tolerantie = 300 punten op BTC 60K
- Zone_type bepaald door meerderheid — 3 toppen + 2 bodems wordt "resistance", maar gemiddelde vervormt
- V02: ATR × 0.5 clustering = 400 punten op BTC met ATR=800

### 6. XBTEUR = BTCEUR
- BacktestReader alias/logica: XBTEUR en BTCEUR geven identieke data

## Wat ontbreekt in de code

| Concept | Status |
|---------|--------|
| Swing points (gefilterde fractalen) | ONTBREEKT |
| Tijdsdimensie in zone-clustering | ONTBREEKT |
| Aparte bovenlijn + onderlijn in v01 | ONTBREEKT (wel in v02) |
| Paralleliteitscheck slopes | ONTBREEKT |
| Kanaaltype (range/bullish/bearish) | ONTBREEKT |
| Wedge/compressie detectie | ONTBREEKT |
| Prijspositie (boven/midden/onder) | ONTBREEKT (location() is te simpel) |
| Mutual exclusivity LONG/SHORT | ONTBREEKT |
| "Geen entry" bij middenpositie | ONTBREEKT |

## Wat moet veranderen

| Functie | Beslissing |
|---------|-----------|
| `macro_trendlijn()` | Aanpassen — enkel lijn, geen entry |
| `lower_trendlijn()` | Aanpassen — idem |
| `bepaal_trend()` | Herschrijven — diepte=4 te klein |
| `cluster_fractalen()` | Herschrijven — te brede clustering |
| `is_consoliderend()` | Herschrijven — 20 bars te kort |
| `location()` | Herschrijven — procentuele positie nodig |
| `channel_down()` (v02) | Behouden — parallel concept correct |
| `channel_candidate_eval.py` | Behouden — 3 kandidaten correct |

## Minimaal nieuw ontwerp

1. Candles → swing points (fractalen, filter op ≥ 1× ATR)
2. Swing points → swing zones (cluster op 0.3× ATR)
3. Zones → S/R (dichtste R/S, check binnen/buiten)
4. Bovenlijn + onderlijn → slopes → structuurtype (parallel, convergent, divergent)
5. Prijspositie = % tussen lower en upper (0-20% onder, 20-80% midden, 80-100% boven)
6. Entry: SHORT enkel bearish + boven, LONG enkel bullish + onder, GEEN entry midden

## Eindoordeel

- `macro_trendlijn()` en `lower_trendlijn()`: volledig onbetrouwbaar als entry-detector
- `bepaal_trend()` met diepte=4: onbetrouwbaar
- `is_consoliderend()` met 20 bars: onbetrouwbaar
- LONG+SHORT opzelfde candle: mag niet meer gebruikt worden
- Entry_price uit gebroken lijn: mag niet meer gebruikt worden
- Eerste fix: `prijspositie_binnen_kanaal()` + `mutual_exclusivity_check()` toevoegen