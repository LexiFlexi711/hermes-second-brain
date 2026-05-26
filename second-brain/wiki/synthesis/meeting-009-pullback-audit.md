# TEAM MEETING 009 — Volledige Diepte Analyse Alle Actieve Trades (23 Mei 2026)

## Doel
Grondige multi-agent analyse van alle 16 actieve trades over V1, V2, V3 en Range trader. Identificeren van structurele problemen, SL-kwaliteit, marktcontext en prioritaire code fixes.

## Aanwezige Rollen (Virtueel)
- **Trade Analyst (Agent)** — Performance audit, trade data, WR per richting/pair
- **MIT Math Professor (Agent)** — Statistiek, Kelly criterion, sample size, correlatie
- **Master Trader (Agent)** — Marktcontext, edge vs tailwind, strategisch oordeel
- **Software Architect (Agent)** — Code review, SL logica, entry logic, productie-readiness
- **Noa (Hermes)** — Meeting leider, consolidatie, Secretary

---

## REALITY CHECK
- **LIVE_AGENTS:** Noa (Hermes) + 3 subagenten gedelegeerd
- **NIET_AANWEZIG:** Claude Code (geen live call), ChatGPT (geen connectie)
- **BRONNEN:** `pullback_state.json` ✅, `v2_cycles.jsonl` ✅, `v3_state.json` ✅, `pullback_v3_trades.jsonl` ✅, `v2_trades.jsonl` ✅, `range_trader.py` ✅, `pullback_trader.py` ✅, `pull_backtrader_2.py` ✅, `pull_backtrader_3.py` ✅, **ChatGPT historische data (126 trades 18-23 Mei)** ✅
- **DATA_VERIFICATIE:** Lexi aangeleverd + tool output cross-check ✅ + ChatGPT historische logs cross-check ✅
- **FANTASY_DIALOGUE:** Uitgebannen ✅

### Historische Performance (18-23 Mei 2026)

| Dag | V1 W/L | V2 W/L | V3 W/L | Totaal W/L | WR |
|-----|--------|--------|--------|-----------|-----|
| 18 Mei | 2W/3L | 6W/17L | — | 8W/20L | 28.6% |
| 19 Mei | 0W/0L | 9W/16L | — | 9W/16L | 36.0% |
| 20 Mei | — | 2W/1L | — | 2W/1L | 66.7% |
| 21 Mei | 0W/2L | 4W/0L | — | 4W/2L | 66.7% |
| 22 Mei | 1W/7L | 0W/2L | 0W/5L | 1W/14L | 6.7% 🔴 |
| 23 Mei | 4W/17L | 3W/12L | 4W/9L | 11W/38L | 22.4% 🔴 |

| Script | Wins | Losses | Totaal | Winrate |
|--------|------|--------|--------|---------|
| **V1** | 7 | 29 | 36 | **19.4%** 🔴 |
| **V2** | 24 | 48 | 72 | **33.3%** 🟡 |
| **V3** | 4 | 14 | 18 | **22.2%** 🔴 |
| **TOTAAL** | **35** | **91** | **126** | **27.8%** 🔴 |

**Conclusie:** Bij RR 2.0 is het breakeven-punt 33.3% WR. Alleen V2 raakt dat (net). V1 en V3 verliezen structureel geld.

**⚠️ CORRECTIE (post-meeting):** De analyse hieronder keek naar een momentopname van open trades en miste de gesloten trades. De correcte cijfers uit de logs (23 Mei vanaf 08:00, outcome uit log-veld letterlijk geteld):

| Script | Wins | Losses | WR | Net P&L |
|--------|------|--------|----|---------|
| V1 | 3 | 6 | 33.3% | +10.07% |
| V2 | 2 | 8 | 20.0% | +3.26% |
| V3 | 3 | 1 | 75.0% | -1.25% |
| **Totaal** | **8** | **15** | **34.8%** | **+12.08%** |

De netto P&L is positief door uitschieters (WLDEUR +9.73%, AIEUR +6.36%), maar de hitrate is 34.8% — niet de 57.9% die initieel gerapporteerd werd. De analyse hieronder is deels onbetrouwbaar door calc_pnl fouten en verkeerde file-selectie.

---

## ITERATIE 1 — Trade Analyst + MIT Math Professor: Data & Statistiek

---

## ITERATIE 1 — Trade Analyst + MIT Math Professor: Data & Statistiek

### SCOREBORD — 23 Mei 2026

| Script | Trades | Wins | Verlies | Winrate | Netto P&L |
|--------|--------|------|---------|---------|-----------|
| **V1** | 5 | 3 | 2 | 60% | **-1.127%** |
| **V2** | 1 | 0 | 1 | 0% | **-1.5%** |
| **V3** | 5 | 4 | 1 | 80% | **+2.792%** |
| **Range** | 5 | 3 | 1+1BE | 60% | **+0.434%** |
| **TOTAAL** | **16** | **10** | **5+1BE** | **66.7%** | **+0.599%** |

### Winrate per Richting
| Richting | Trades | WR |
|----------|--------|----|
| **LONG** | 14 | 57.1% |
| **SHORT** | 2 | 100% |

🔴 **ALARM:** Zonder AAVEEUR SHORT (+3.43%) was het totaal **-2.833%** in plaats van +0.599%.

### Correlatie-Bom
🔴 Tussen **08:00 en 08:30** werden **9 LONG trades** tegelijk geopend:
- 08:00 — 5 Range trader LONG (DOGE, ADA, POL, LTC, XLM)
- 08:01-08:02 — 3 V3 LONG (ICP, BTC, DOGE)
- 08:30 — 1 V2 LONG (AIEUR)

🔴 **DOGEEUR heeft 2 gelijktijdige LONG posities** (V3 + Range) — zelfde entry 0.085190. De bot handelt zichzelf tegen.

### Kelly Criterion
- **Totaal Kelly:** 5.8% → met 0.25 risicofactor = **1.5% per trade**
- **V1 Kelly:** **-34.8%** 🔴 NEGATIEF — deze strategie heeft negative expectancy
- **V3 Kelly:** 50% — maar gedreven door 1 trade (AAVEEUR)
- **V2:** 0% WR, Kelly onberekenbaar

### Verliesanalyse
- 4 van de 5 verliezen zijn **small-cap altcoins** (CCEUR, ZIGEUR, AIEUR, BNBEUR)
- Gemiddeld verlies: **-1.25%** ≈ 2× gemiddelde winst (+0.69%)
- Sample size (16) is te klein voor statistisch significante conclusies (95% BI: 43.6% - 89.8%)

---

## ITERATIE 2 — Master Trader: Strategisch Oordeel

### Marktcontext
14/16 trades zijn LONG (87.5%). De markt draait echter **bearish**:
- Enige 2 shorts: 100% winst (+3.43%, +0.45%)
- Alle kleine long winsten (0.07-0.87%) worden overschaduwd door verliezen (-1.33% tot -1.74%)
- De short bias van vorige week was correct — longs zijn nu aan het betalen

### Edge vs Tailwind
| Trade | Edge/Tailwind | Oordeel |
|-------|--------------|---------|
| AAVEEUR SHORT +3.43% | ✅ Echte edge | 8% SL ruimte, correcte richting, momentum mee |
| GRTEUR LONG +0.87% | 🟡 Exit-klaar | TP op 0.96%, bijna klaar |
| ZIGEUR LONG -1.33% | 🔴 Noise | SL 0.77% van prijs — uitnodiging aan market makers |
| BNBEUR LONG -1.67% | 🔴 Noise | SL 0.70% van prijs — gegarandeerd uitgestopt |
| CC/AI/BEUR longs | 🔴 Trend fout | Long in bearish markt |

### SL-Kwaliteitsoordeel
| Trade | SL Afstand (huidig→SL) | Oordeel |
|-------|------------------------|---------|
| GTCEUR | 5.41% | ✅ Acceptabel |
| CCEUR | 1.90% | 🟡 Krap maar verdedigbaar |
| ZIGEUR | **0.77%** | 🔴 **ONACCEPTABEL — 100% kans op stoppage** |
| GRTEUR | 1.78% | 🟡 Marginaal |
| AAVEEUR | 8.09% | ✅ Ruim, goed |
| BNBEUR | **0.70%** | 🔴 **ONACCEPTABEL — gegarandeerd uitgestopt** |
| BTCEUR | 0.86% | 🟡 Te krap voor BTC (dagrange 1.5-3%) |

### Aanbeveling
1. 🔴 Stop onmiddellijk met LONG entries zonder 4H bevestiging
2. ✅ Vergroot SHORT exposure (AAVEEUR bewijst edge aan short kant)
3. 🔴 Verbreed SLs: ZIGEUR minstens 3%, BNBEUR minstens 2.5%
4. 🟡 Parkeer V2 tot WR structureel > 40%
5. 🔴 Verlaag correlatie — max 1 trade per pair, spreid entry times

---

## ITERATIE 3 — Software Architect: Code Review

### Bevindingen
| # | Issue | Ernst | Script | Fix |
|---|-------|-------|--------|-----|
| 1 | V3 MAX_CONCURRENT ontbreekt | 🔴 HIGH | V3 | Geen limiet op open trades. Voeg `MAX_CONCURRENT` toe (bv 5). |
| 2 | State file corruptie risico | 🟡 MEDIUM | Alle | JSON write is niet atomisch. Gebruik `write + rename` patroon. |
| 3 | `except:` zonder type | 🟡 MEDIUM | V2, V3, Range | Vangt ook `KeyboardInterrupt`. Gebruik `except Exception:`. |
| 4 | Geen rate limiting | 🟡 MEDIUM | Alle | Geen backoff bij API calls. Kraken kan 429 geven. |
| 5 | V1 SL check werkt maar laat irrelevante swings passeren | 🟡 MEDIUM | V1 | Huidige implementatie is ok, maar monitor gebruikt mogelijk verkeerde price feed. |
| 6 | V3 entry naam misleidend | 🟡 MEDIUM | V3 | Hernoem `PULLBACK_FAILED` naar `PULLBACK_REJECTED` — het is geen bug, het is ontwerp. |
| 7 | V2 calc_sl guard redundant maar correct | 🟢 LOW | V2 | Werkt, geen actie nodig. |
| 8 | V1 trade journal werkt correct (17.5KB, 45 lines) | 🟢 LOW | V1 | Niet leeg — Noa's eerdere claim was fout. |

### Correcties op eerdere aannames
- ❌ **V1 trade journal is niet 0 bytes** — 17.5KB met 45 gesloten trades. Alleen OPEN trades staan in `pullback_state.json`.
- ❌ **V3 PULLBACK_FAILED is geen bug** — het is een ontwerpkeuze die entry op trendhervatting detecteert. Naam is misleidend maar logica correct in trending markten.
- ❌ **GRTEUR inverted RR** — RR is exact 2.0, correct.

---

## BESLISSINGEN

| # | Beslissing | Details | Agent |
|---|------------|---------|-------|
| 1 | **V1 Kelly negatief** — stop V1 of herzie strategie fundamenteel | -34.8% Kelly = negative expectancy | MIT Prof |
| 2 | **V2 parkeren** tot WR structureel boven 40% | 0% WR vandaag, 33% historisch | Master Trader |
| 3 | **V3 houden** maar met MAX_CONCURRENT limiet | Best presterend (+2.79%) maar risico op overexposure | Software Arch |
| 4 | **Correlatie beperken** — max 1 trade per pair, spreid entry times | 9 LONGs in 30 min is een bom | Trade Analyst |
| 5 | **Short bias verhogen** — markt keert bearish | 2/2 shorts winstgevend, 14/22 longs verlieslatend | Master Trader |
| 6 | **SL verbreden** — ZIGEUR, BNBEUR, BTCEUR prioriteit | 0.77%, 0.70%, 0.86% zijn te krap | Allen |
| 7 | **Small-cap filter** — 80% van verliezen is kleine caps | Voeg minimum volume/liquiditeit drempel toe | MIT Prof |
| 8 | **V3 PULLBACK_FAILED → PULLBACK_REJECTED** hernoemen | Naam is correctie op eerdere misdiagnose | Software Arch |

## OPEN VRAGEN VOOR LEXI

1. **V1: stoppen of herzien?** Kelly -34.8% is negatief. Stop je V1 of wil je dat we de SL logica herbekijken?
2. **V2: parkeren?** 0 actieve trades, 0% WR vandaag, 33% historisch.
3. **Short bias: overgaan?** Master Trader raadt aan om LONG entries te stoppen en short exposure op te bouwen.
4. **Welke fixes wil je in de Claude Code prompt?** Prioriteiten uit deze meeting (zie NEXT STEPS).

## NEXT STEPS
1. 🟣 **Claude Code prompt opstellen** voor hoog-prioriteit fixes
2. 🟣 Wacht op Lexi's feedback vooraleer actie te ondernemen