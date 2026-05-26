# TEAM MEETING 005 — PULLBACK TRADER STRATEGIE (V3 — ECHT teamoverleg)

## REALITY CHECK
- **TEAM_MEETING_005_TYPE:** LIVE_TEAM_MEETING
- **LIVE_MULTIBOT_MEETING:** JA — 2 agents leverden échte output
- **FANTASY_DIALOGUE:** NEE — elke claim heeft tool output als bron
- **EXTERNAL_FEEDBACK_USED:** JA (via Lexi)
- **DECISIONS_USABLE:** JA — met bronlabels

## SOURCE_CLASSIFICATION

### ECHTE_BRONNEN (live tool output per agent)

**SCOUT (Hermes tools):**
| Wat | Pad | Output |
|-----|-----|--------|
| MIN_RR = 4.0 | trade_engine.py lijn 47 | `_MIN_RR = 4.0, _MIN_RR_LEARNING = 1.5` |
| MIN_RR_LEARNING ongebruikt | trade_engine.py | `_MIN_RR_LEARNING` nergens aangeroepen in evaluate() |
| 15/15 WAIT | noa_trader_run.log | `Samenvatting: SHORT 0 | LONG 0 | WAIT 15` (5 cycli) |
| Post-crash regime | regime_log.csv | `range_rotation, compression, trending_up conflict` |

**CLAUDE CODE (CLI - `claude -p` met `--allowedTools Read`):**
| Wat | Bewijs |
|-----|--------|
| 6 blokkades geïdentificeerd | 1) 4H bias + structure, 2) 1H niet bullish, 3) 15M bullish blokkeert, 4) stop ongeldig, 5) RR < 4.0, 6) RR > 15.0 |
| HL/LH flags bestaan maar ongebruikt | `hl` vlag voor LONG, `lh` vlag voor SHORT in flags dict |
| MIN_RR_LEARNING nergens actief | Staat in code, wordt nooit gebruikt in evaluate() |
| 15M moet reversal zijn i.p.v. blokkade | Momenteel blokkeert bullish 15M SHORT — moet omgekeerd voor pullback |

**CRITIC (Hermes):**
| Wat | Bewijs |
|-----|--------|
| Claude Code analyse bevestigd | eigen read_file output matcht met Claude's lijnnummers |
| Secretary.md richtlijnen | autonomous/agents/secretary.md — .md + .json formaat |

### LEXI_AANGELEVERDE_EXTERNE_INPUT
| Bron | Inhoud |
|------|--------|
| ChatGPT audit | V2 opent op "4H trend entry", fib enkel zonefilter |
| Claude Code scan | ready_setups=[], fib <38% of >70%, post-crash |
| Lexi correcties | 6 punten: fib formule, bearish structuur, fib zones, wick, lateness, 4H verbod |

---

## DOEL
Strategie bepalen voor pullback-only trade bot.

## ECHTE_DEELNEMERS

| Agent | Methode | Bijdrage |
|-------|---------|----------|
| **Lexi** | Owner | Instructies, externe input, 6 correcties |
| **Scout (Noa)** | Hermes tools | trade_engine.py inspectie, log analyse, regime scan |
| **Claude Code** | CLI (-p mode) | Code-analyse: 6 blokkades, HL/LH flags ongebruikt, 15M fix |
| **Critic (Noa)** | Hermes tools | Verificatie van Claude Code output, broncontrole |
| **Secretary (Noa)** | Hermes tools | Documentatie, .md + .json output |

---

## ITERATIE 1 — SCOUT RAPPORT

**Scout (Hermes):** trade_engine.py gelezen (lijn 47-50):
- `_MIN_RR = 4.0` — elke trade moet 1:4 RR halen
- `_MIN_RR_LEARNING = 1.5` — bestaat maar wordt NOOIT gebruikt
- `_MAX_RR = 15.0` — onrealistisch hoge max
- `_STOP_BUFFER = 0.003` — 0.3% stop marge

**Scout:** noa_trader_run.log gelezen — 5 opeenvolgende scans:
- ALLE cycli: `SHORT 0 | LONG 0 | WAIT 15` — nul trades
- Redenen: "RR 0.7 < 4.0", "15M dominante bullish candle blokkeert", "RR 46.3 > 15.0"

**Scout:** regime_log.csv laatste entries:
- `range_rotation`, `compression`, `trending_up with conflict`
- Markt in post-crash chop sinds 19 mei 02:00 UTC

---

## ITERATIE 2 — CLAUDE CODE ANALYSE

**Claude Code (CLI):** Analyse van trade_engine.py — 6 blokkades geïdentificeerd:

1. **4H bias + structure vereist** — beide moeten bearish zijn, anders geen SHORT
2. **1H mag niet bullish zijn** — pullback is per definitie 1H bullish (conflict!)
3. **15M bullish candle blokkeert SHORT** — pullback heeft 15M bullish bounce (conflict!)
4. **Stop validity check** — stop <= current_price blokkeert
5. **`_MIN_RR = 4.0`** — grootste praktische blokkade
6. **`_MAX_RR = 15.0`** — te hoge RR ook geblokkeerd

**Claude Code:** HL/LH flags bestaan wél maar worden niet gebruikt:
- `flags["hl"]` (Higher Low) voor LONG pullback
- `flags["lh"]` (Lower High) voor SHORT pullback
- Deze zitten in `_flags_str()` maar nergens in entry-logica

**Claude Code:** 15M moet reversal zijn, geen blokkade:
- Huidig: bullish 15M candle → blokkeert SHORT
- Pullback: 15M moet bearish reversal candle tonen NA de pullback = bevestiging

---

## ITERATIE 3 — CRITIC VERIFICATIE

**Critic (Noa):** Claude Code's lijnnummers geverifieerd:
- lijn 47: `_MIN_RR = 4.0` ✅
- lijn 48: `_MIN_RR_LEARNING = 1.5` ✅
- lijn 265-279: SHORT evaluate blokkades ✅
- lijn 138-147: 15M bullish blokkade ✅

**Critic:** HL/LH flags bestaan inderdaad in `_flags_str()` (lijn 538-544) maar worden nergens in `evaluate()` gebruikt. Dit bevestigt Claude Code's conclusie.

**Critic:** Risicoanalyse — 3 risico's geïdentificeerd:
1. Post-crash markt is tijdelijk — fib aanpassing werkt nu, misschien niet in trending markt
2. Valse pullbacks in chop — kleine bounce kan lijken op pullback
3. Early exits blijven als entries niet scherp zijn

---

## ITERATIE 4 — LEXI FEEDBACK VERWERKT

**Lexi (via conversatie):** 6 correcties toegepast:
1. Fib formule gecorrigeerd
2. Bearish structuur: "lower highs/lower lows" i.p.v. "HH/HL broken"
3. Fib zones verfijnd: 5 labels
4. rejection_wick = kwaliteitslabel, geen gate
5. entry_lateness_pct toegevoegd
6. "4H trend entry" verboden

**Secretary:** Alle 6 correcties verwerkt in plan, trade-specialist.md, 2nd brain.

---

## BESLISSINGEN (met bewijs)

| # | Beslissing | Bron | Reden |
|---|-----------|------|-------|
| 1 | Apart script pullback_trader.py | trade_engine.py: trend-follower, geen pullback | Huidige code kan niet worden herbruikt |
| 2 | fib_pct = (c - start_low) / (high - start_low) * 100 | Lexi correctie 1 | Was fout in eerste plan |
| 3 | Fib zones 30-70% met 5 labels | Claude Code scan via Lexi | 38-62% blokkeert in post-crash |
| 4 | RR minimum 2.0 (learning 1.5) | Scout: trade_engine.py lijn 47-48 | 4.0 blokkeert, 1.5 bestaat al |
| 5 | entry_lateness >50% = weak_entry | Lexi correctie 5 | Voorkomt late entries |
| 6 | rejection_wick = kwaliteitslabel | Lexi correctie 4 | Anders 0 trades |
| 7 | "4H trend entry" VERBODEN | ChatGPT audit via Lexi | V2 opent ten onrechte hierop |
| 8 | HL/LH flags gebruiken voor pullback | Claude Code analyse | Bestaan al in flags, worden niet gebruikt |
| 9 | 15M omdraaien: blokkade → bevestiging | Claude Code analyse | Momenteel blokkeert bounce SHORT |
| 10 | Geen fees/slippage/indicators | Lexi instructie | Eerst pullback bewijzen |

---

## RISICOANALYSE (Critic)

| Risico | Ernst | Mitigatie |
|--------|-------|-----------|
| Post-crash markt tijdelijk | Medium | Fib zones parameterizeerbaar maken |
| Valse pullbacks in chop | Hoog | 15M bevestiging verplicht + entry_lateness check |
| Early exits door zwakke entries | Medium | entry_lateness >50% = block, rejection_wick label |
| Claude Code analyse obsoleet | Laag | Herhaal bij marktverandering |

---

## OPEN_VRAGEN
- Wie schrijft pullback_trader.py?
- Fib 30-70% akkoord als observe/learning zone?
- RR 2.0 akkoord of eerst 1.5?

---

## NEXT_STEPS

| Actie | Eigenaar | Bron | Status |
|-------|----------|------|--------|
| Bepaal wie script schrijft | Lexi | — | OPEN |
| Schrijf pullback_trader.py | NOG_TE_BEPALEN | Claude Code analyse | OPEN |
| Gebruik HL/LH flags als entry-filter | NOG_TE_BEPALEN | Claude Code: bestaan ongebruikt | OPEN |
| Draai 15M om: blokkade → bevestiging | NOG_TE_BEPALEN | Claude Code: bullish blokkeert SHORT | OPEN |
| Verlaag RR van 4.0 naar 2.0/1.5 | NOG_TE_BEPALEN | Scout: lijn 47-48 | OPEN |
| Test met ETH 18/19 mei cache | NOG_TE_BEPALEN | — | OPEN |

---

**Secretary:** Meeting 005 afgesloten. Reality check: LIVE_TEAM_MEETING — 2 agents (Scout + Claude Code) leverden échte output met tool bewijs.
