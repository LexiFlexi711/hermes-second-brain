---
title: Crypto Tradebot — Volledig Onderzoeksoverzicht
type: project
created: 2026-05-30
author: Lexi (Noa write-back)
status: live
tags:
  - crypto-tradebot
  - crypto-data
  - research
  - architecture
  - exit-management
  - testbot
---

# Crypto Tradebot — Volledig Onderzoeksoverzicht

> **Bron:** Lexi's eigen architectuur- en onderzoeksdocument, opgeslagen door Noa op 30 Mei 2026.
> **Context:** Na STAP-O/P/Q/S — V3A multi-pair run afgerond, exit-analyse gestart.

---

## 0. Wat we écht bouwen

We bouwen een **complete test- en bewijsomgeving** rond crypto trading waarin drie dingen tegelijk moeten kloppen:

1. De data moet betrouwbaar zijn.
2. De bot moet beslissingen nemen die logisch verklaarbaar zijn.
3. Elke beslissing moet achteraf controleerbaar zijn via logs, charts en snapshots.

**Kernprincipe:** Niet gokken. Bewijzen.

---

## 1. De grote architectuur

```
EXTERNE DATA
    ↓
crypto-data pipeline
    ↓
data bridge / cache / freshness check
    ↓
candles per pair en timeframe
    ↓
strategy / testbot laag
    ↓
trade decision
    ↓
open trade monitor
    ↓
SL / TP / trailing / range-break / exit rules
    ↓
logs → charts → snapshots → audit → verbetering
```

**Belangrijk:** Die volgorde mag niet door elkaar lopen. Een strategie mag niet beslissen op halfgare data. Een chart mag niet iets anders tonen dan de log.

---

## 2. Crypto-data laag

De voeding van alles. Moet candles leveren voor pairs (ETHEUR, BTCEUR, BCHEUR, ICPEUR, INJEUR, LTCEUR, SOLEUR, DOGEEUR, PUMPEUR, GTCEUR, ...) en timeframes (15m, 1h, 4h, later daily).

Data moet geschikt zijn voor: live trading, testbot, backtests, charts, snapshot reconstructie, strategievergelijking, exit-analyse, foutdetectie.

Niet "ongeveer juist" — exact genoeg om te kunnen zeggen: op candle X, om timestamp Y, met prijs Z, had de bot deze beslissing.

---

## 3. Waarom de crypto-data pipeline zo belangrijk werd

**De bug van 29/5:** Oude traderprocessen draaiden nog met oude Python-imports. cache_freshness.py was gefixt, maar draaiende processen gebruikten nog oude `_CACHE_DIR` → `_read_cache()` gaf lege data → monitoring/TP/SL blocks overgeslagen → trades bleven hangen.

**Harde werkregel:** Na commits aan gedeelde modules/imports die live traders gebruiken:
1. Alle live traderprocessen stoppen
2. Opnieuw starten
3. Heartbeat controleren
4. Cache-path controleren
5. Bewijzen dat de nieuwe code effectief draait

---

## 4. Data bridge / cache laag

Tussenlaag tussen crypto-data en crypto-tradebot. Moet voorkomen dat elke strategie zelf data gaat ophalen, interpreteren of cachen.

**Eis:** Eén centrale data route, één cachelocatie, één freshness check, één duidelijke fout als data ontbreekt. Geen stille fallback. Geen lege lijst alsof dat normaal is.

---

## 5. Cache freshness

Moet controleren: is data vers? juiste pad? timestamp recent? genoeg candles? pair correct? timeframe correct? niet leeg? geen oude map?

**Probleem:** "Geen data" is soms gevaarlijker dan "foute data". Lege data moet behandeld worden als serieus signaal, niet als neutraal.

---

## 6. Snapshots

Een snapshot is een **bevroren momentopname** van de realiteit waarop de bot beslist. Niet gewoon "de bot gaf LONG" maar:

- timestamp, pair, timeframes
- exact welke candles beschikbaar waren
- exacte prijs, regime, signaal, confidence
- SL/TP/trail waarden

De snapshot is de **black box recorder** van de bot.

---

## 7. Waarom snapshots belangrijk zijn voor backtests

Backtesten op gewone historische candles is niet genoeg — snapshot-denken voorkomt **lookahead-bias**: de backtest gebruikt informatie die de live bot op dat moment nog niet had.

---

## 8. Charts naast logs

- Logs = tekstueel bewijs
- Charts = visueel bewijs

**Auditregel:** log zegt X, chart toont X, snapshot hoort bij X, bot-output formuleert X correct. Als één van die vier afwijkt, hebben we een auditpunt.

---

## 9. Logger

Moet per trade bewijsbaar maken bij **opening** (pair, strategie, richting, entry, timestamp, snapshot_id, timeframes, regime, signal, confidence, SL, TP, trail, reden), tijdens **monitoring** (huidige prijs, unrealized PnL, afstand tot SL/TP, trail actief, hoogste/laagste sinds entry, range geldig, data freshness), en bij **sluiting** (exit prijs, exit reden, WIN/LOSS, PnL%, MFE, MAE, of trailing/BE had kunnen redden).

---

## 10. Testbot

Het **experimenteerplatform** — niet de finale winstmachine. Moet strategieën kunnen draaien op historische en/of live data om exitvarianten te vergelijken (origineel, BE, trailing, combo, range-break).

---

## 11. Strategieën in beeld

V1, V2, V3, Momentum, Range, V3A pullback, Breakout, candle-battle/candle-first onderdelen.

**Nuance:** Niet alle strategieën zijn automatisch "goed" of "live-klaar". Ze zijn onderzoekskandidaten die door dezelfde poort moeten: data, logs, charts, entry, exit, confidence, regime, candlecontext, reproduceerbaarheid.

---

## 12. Recente harde ontdekking: exits zijn verdacht

Veel trades stonden groen maar eindigden rood of sloten te laat. Dat betekent: **entry kan goed genoeg zijn** (tijdelijke winst) maar exit/monitoring laat winst terug weglopen.

Diagnose: mogelijk wél een edge in entry/timing, maar probleem zit in te late exit, te ruime TP, geen trailing, BE ontbreekt, range-break te laat, monitor mist data, open trade manager reageert niet, oude process/cache bug, SL/TP-logica leest geen verse candles.

---

## 13. Exit-test resultaten (tot nu toe)

| Strategie | Origineel | BE (+1%) | Trail (+2%) | Combo A+B | Verliezers gered |
|-----------|-----------|----------|-------------|-----------|-----------------|
| **V1** | -18.07% | -4.07% | +36.88% | +36.88% | 7 |
| **V2** | -25.12% | -9.43% | +9.58% | +9.58% | 6 |
| **V3** | -11.37% | -8.61% | -7.04% | -7.04% | 1 |
| **Momentum** | +13.65% | +16.74% | +10.66% | +10.66% | 1 |
| **Range** | -4.44% | -0.30% | -0.32% | -0.32% | ? |

---

## 14. Belangrijk inzicht

Exitregels moeten **per strategie** onderzocht worden. Eén algemene exitregel voor alle strategieën zou dom zijn.
- V1: veel beter met trailing
- V2: beter met trailing
- V3: blijft zwak — entry/regime probleem?
- Momentum: beter met BE, slechter met trailing — heeft ruimte nodig
- Range: bijna break-even met bescherming

---

## 15-17. Exitmechanismen

- **Break-even stop:** SL naar entry na +1%. Redt trades die eerst groen waren. Risico: kan trades te vroeg stoppen in volatiele crypto.
- **Trailing stop:** Stop schuift mee met prijs. Laat winnaars lopen. Risico: te krap = te vroeg eruit, te ruim = geeft winst terug.
- **Combo A+B:** Eerst BE (+1%), dan trail (+2%). Logisch: fase 1 = verlies vermijden, fase 2 = winst beschermen.

---

## 18. Waarom we nu niet zomaar mogen optimaliseren

V1 + trailing = nog geen "geldprinter". We moeten eerst weten: is dataset representatief? fees/slippage mee? lookahead? live-uitvoerbaar? werkt in andere jaren/pairs? out-of-sample?

**Juiste formulering:** Trailing toont zeer sterk onderzoeksresultaat voor V1/V2, maar moet nog gevalideerd worden.

---

## 19. Backtestdata

361.327 candles, 15m, 2023-2024 — serieuzer dan twee weken testen, maar zelfs dan: crypto heeft regimewissels, survivorship bias, exchange-data gaten, fees/spread.

---

## 20. Wat "trainen" betekent

Parameters testen, regels vergelijken, exitgedrag meten. Gevaar: curve fitting bij 100 combinaties. Betere workflow: observeer probleem → formuleer hypothese → test kleine set logische parameters → controleer stabiliteit → valideer op andere periode.

---

## 21. Huidige onderzoeksvraag

**Zijn onze strategieën slecht, of zijn onze exits/monitoring slecht?**

Subvragen:
1. Welke trades stonden eerst groen?
2. Hoe groen stonden ze maximaal?
3. Hoeveel eindigden rood?
4. Waarom sloten ze niet vroeger?
5. Had BE ze gered?
6. Had trailing winst beschermd?
7. Mist de bot exit-signalen?
8. Of heeft de bot ze wel gezien maar genegeerd?
9. Of waren er data/cache problemen?
10. Of waren SL/TP/trail verkeerd berekend?

---

## 22. Open trades monitoring

Voor elke open trade moet de bot continu weten: pair, strategie, richting, entry, SL, TP, huidige prijs, unrealized PnL, hoogste/laagste sinds entry (voor trailing), of TP/BE/trail ooit gehit hebben, of range nog geldig is, of data vers is.

---

## 23. SL/TP-berekening

Moet **direction-aware** zijn:
- LONG: prijs omhoog = winst, SL onder entry, TP boven entry
- SHORT: prijs omlaag = winst, SL boven entry, TP onder entry

---

## 24. Candle-first refactor

Gewenste volgorde: candles → levels → context → patterns → signal → presentatie. Niet andersom. Candles zijn de ruwe waarheid.

---

## 25. Candlepatronen zijn geen tradebeslissingen

Een hammer ≠ koop. Een shooting star ≠ short. Patronen hebben context nodig: marktstructuur, S/R, trend, range, top-down timeframe analyse.

**Regel:** candle-label ≠ trade trigger. "Local rejection visible near support" is correct. "Bullish reversal confirmed" is te sterk zonder bevestiging.

---

## 26. Regime, bias, structure, signal context

De bot mag deze lagen niet verwarren:
- **Structure:** prijsstructuur (HH/HL, LH/LL, range, S/R)
- **Bias:** welke kant heeft voordeel (bulish/bearish/neutral)
- **Regime:** markttype (trend/range/compression/chop)
- **Signal context:** wat zegt de setup (possible long, weak signal, local bounce)
- **Trigger:** effectieve trade opening

**Voorbeeld:** 15m bounce binnen bearish 4h context ≠ confirmed reversal.

---

## 27. Confidence

Moet verklaarbaar zijn, niet zomaar een percentage. Confidence moet lager bij conflicterende timeframes, range midden, compressie, onduidelijke candle-confirmatie, ontbrekende data, mixed signals, stale data. Hoger bij duidelijke structuur, alignment, heldere key levels, verse data, consistente logs/charts.

---

## 28. "Lexi :)" laag

Indicator research probe met 13 indicatoren: LONG/SHORT/HOLD met gewicht 0-100. Belangrijke nuance: HOLD met bijna perfecte balans (6L/7S) kan hoog scoren — het gewicht meet signaalspanning/consensus/conflictsterkte, niet automatisch tradebaarheid.

---

## 29. Live dashboard

`indicator_research_probe.py --live --dashboard --live-pairs ETHEUR,BTCEUR --live-interval 5 --loop --loop-interval 60` — nuttig voor live consistentie maar observatie, niet automatisch strategie.

---

## 30. Snapshot_id verbetering

`snapshot_id` uit `fetch_all_timeframes()` wordt doorgestuurd naar result vóór `log_entry()`. `format_decision()` toont `snap=<timestamp>`. Alle timeframes delen dezelfde snapshot timestamp — cruciaal voor auditbaarheid.

---

## 31. Strategieonderzoek versus productie

Strikt onderscheid:
- **Research mode:** backtests, parameters vergelijken, hypothesen testen
- **Testbot/live paper mode:** bot draait alsof live, monitoring/exits/logs controleren
- **Production/live mode:** echte posities, geen experimenten zonder audit

---

## 32-33. Backtest runner & DataReader concept

Ideaal:zelfde strategy core, andere data reader (LiveReader vs BacktestReader). Strategie weet niet of data live of historisch is. Minder dubbele logica, makkelijker testen, betere auditbaarheid.

---

## 34. OpenClaw / Hermes / Claude rolverdeling

- **Lexi** = eigenaar / beslisser
- **Noa** = audit, architectuur, scherpe lijn, prompts, controle
- **Hermes/Claude** = implementatie/uitvoering in repo
- **OpenClaw** = koerier/regisseur tussen processen (taak ophalen, naar Hermes brengen, wachten, resultaat terugbrengen)

OpenClaw moet niet "denken" of strategie bepalen.

---

## 35. Second brain / write-back

Elke meeting/audit/strategie-update moet naar second brain met exact pad en bewijs. Second brain is projectgeheugen — essentieel voor tradebot met zoveel bewegende delen.

---

## 36-37. Focus

**NIET:** nieuwe indicatoren, strategieën, AI-lagen, dashboards, filters, integraties, portfolio optimalisatie, live geld, ML-training.
**WEL:** data betrouwbaarheid, open trade monitoring, exit-analyse, backtest-validatie, logs/charts/snapshots matchen.

---

## 38. Concrete onderzoeksboom

```
Probleem: Groene trades eindigen rood of sluiten te laat.
  ├── Hypothese 1: Exitlogica te zwak (BE, trailing, combo, time stop)
  ├── Hypothese 2: Monitoring mist data (cache freshness, heartbeat, log)
  ├── Hypothese 3: SL/TP/trail fout berekend (direction-aware, unit tests)
  ├── Hypothese 4: Strategie stapt te laat in (MFE/MAE, entry candle analyse)
  └── Hypothese 5: Strategie gewoon zwak (out-of-sample, fees/slippage)
```

We zijn nu bezig met hypothese 1 en 2.

---

## 39. MFE en MAE

- **MFE (Maximum Favorable Excursion):** Hoeveel stond trade maximaal in winst?
- **MAE (Maximum Adverse Excursion):** Hoeveel stond trade maximaal tegen?

Een trade die eindigt op -2% maar ooit +4% stond = exit failure. Een trade die nooit groen stond = entry failure.

---

## 40. Trade classificatie

- **Type A — direct fout:** nooit groen, direct naar SL → entry/signaal probleem
- **Type B — groen maar terug rood:** MFE positief, final negatief → exit/trailing probleem
- **Type C — goed:** MFE positief, final positief, exit logisch
- **Type D — groen maar te weinig gepakt:** MFE veel groter dan final → trailing/TP optimalisatie
- **Type E — dataprobleem:** monitor mist candles, snapshot ontbreekt, cache stale

---

## 41. Waarom "groene trades rood" zo belangrijk is

Objectief meetbaar: max winst, eindwinst, weggegeven winst. Bijv. MFE +4.2%, final -1.1% = 5.3 procentpunt weggegeven. Dat is strategie-DNA.

---

## 42. Wat "geldprinter" pas betekent

10 voorwaarden: positief op train, validation, out-of-sample, fees/slippage inbegrepen, geen lookahead, live/testbot gelijk, open trade monitor mist niets, exits correct, drawdown aanvaardbaar, niet afhankelijk van één coin/periode.

Nu: "exit-testresultaten zijn veelbelovend en verdienen prioriteit" — saai maar eerlijk.

---

## 43. Wat we aan Hermes/Claude moeten laten doen

Niet "bouw een nieuwe strategie" maar "controleer en bewijs de bestaande pipeline":
1. Crypto-data pipeline werkt?
2. Testbot gebruikt crypto-data versie?
3. Open trades correct gemonitord?
4. Bewijslogs waar data leeg/stale is
5. SL/TP/trailing direction-aware
6. Backtest 2023-2024 15m
7. MFE/MAE per trade exporteren
8. Origineel vs BE vs trail vs combo vergelijken
9. Resultaten wegschrijven
10. Geen nieuwe strategieën

---

## 44. Minimale testbot output

**Per run:** run_id, strategie, periode, pairs, timeframe, candles, trades, winrate, total return, avg win/loss, profit factor, max drawdown, fees, exit variant.

**Per trade:** trade_id, pair, strategie, direction, entry/exit time/price/reason, final PnL%, MFE, MAE, bars_held, BE/trail/triggered, TP/SL touched, would_be_saved_by, snapshot_entry/exit.

---

## 45. Chart-audit

Niet om trades te nemen. Wel om te controleren: bot zegt X, chart toont X of niet, log ondersteunt X of niet, snapshot matcht X of niet.

---

## 46. Candle-first concreet

Eerst candle-feiten (body, wicks, range, close, engulfing, doji). Dan context (near S/R? in range? after pullback?). Dan interpretatie (local rejection, possible exhaustion). Dan strategie.

Niet: hammer = buy. Wel: hammer-like candle near support after decline, higher timeframe not aligned → possible local reaction, not confirmed reversal.

---

## 47. Ideale trading bot documenten

Referentie, geen directe implementatie. Trend following en momentum zijn historisch sterker. Ondersteunt onze keuze om op exitregels en risk control te focussen.

---

## 48. Crypto is anders

24/7, weekendgedrag, volume spikes, lage liquiditeit, spread variatie, exchange API issues, wick spikes, noise op lage TF. Exitregels moeten rekening houden met volatiliteit per coin, gemiddelde candle range, wick gedrag, timeframe, spread.

---

## 49. Huidige projectfase

**FASE:** Bestaande bot betrouwbaar krijgen + exitgedrag bewijzen.
**NIET:** Nieuwe strategieën, AI optimalisatie, live geld opschalen.

---

## 50. Eerstvolgende logische stappen

1. Pipeline smoke test — bewijs dat testbot crypto-data gebruikt
2. Open trade monitor audit — monitor ziet trades, candles, PnL, SL/TP
3. Exit replay — historische trades met origineel/BE/trail/combo
4. Per-strategie beoordeling — V1, V2, V3, Momentum, Range apart
5. Out-of-sample check
6. Live paper check

---

## 51. Goede eindtoestand

Voor elke beslissing moet de bot kunnen antwoorden: waarom LONG/SHORT/HOLD? Welke candles/timeframes ondersteunen/spreken tegen? Regime? Structureel of lokaal? Setup of trigger? Hoe confidence? SL/TP/trail? Welke snapshot? Wat toont chart en log?

---

## 52. Project in één werkdefinitie

We bouwen een **evidence-first crypto trading research en testbot systeem**: crypto-data pipeline, data bridge, cache freshness, data readers, strategy runners, open trade monitor, SL/TP/trailing, backtest engine, trade journal, charts, snapshots, audit prompts, second brain write-back.

**Hoofdmissie:** Bewijzen of strategieën verliezen door slechte exits/monitoring of door slechte entries/signalen.

**Sterkste aanwijzing:** V1 en V2 verbeteren door trailing. Momentum baat bij BE. V3 blijft verdacht. Range break-even.

**Grootste risico's:** Oude processen, stale cache, lookahead, overfitting, niet-matchende logs/charts, confidence zonder bewijs.

---

## 53. De bot die we willen

Niet "LONG 72%". Wel: "Ik zie op snapshot X: 4H bearish, 1H range rotation, 15M local support reaction, candle toont rejection maar geen confirmed reversal, confidence beperkt door timeframe conflict, strategie V1 geeft setup maar trigger is zwak. Alle waarden gelogd, chart staat klaar."

Dat is het verschil tussen AI-bullshit en een echte tradingmachine.
