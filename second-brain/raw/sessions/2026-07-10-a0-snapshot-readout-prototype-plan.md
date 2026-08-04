# A0 SNAPSHOT READOUT PROTOTYPE PLAN

**Datum:** 2026-07-10
**Status:** Planning only — geen code, geen prototype
**Aanleiding:** ADR 2026-07-09 besliste: Snapshot Readout = Analyst A0
**24H Post-Freeze Health Check:** 🟢 GROEN — fundering gezond

---

## 1. Status

Planning only.
Geen code.
Geen prototype.
Geen directories aangemaakt.
Geen DB gewijzigd.

Dit document legt vast WAT A0 moet worden en HOE het later gebouwd en getest moet worden.
Het bouwt niets.

---

## 2. Doel

A0 Snapshot Readout wordt de eerste beschrijvende laag bovenop L4 snapshots.

A0 vertaalt snapshotvelden naar mensentaal, zonder tradebeslissing.

A0 is de poort tussen:
- **Interpreter** (data/geheugen/inspectie) — L4 snapshots, raw blobs, integrity
- **Analyst** (beschrijvende betekenis) — eerst A0 readout, later A1+ weging

Kernregel uit Readout Contract v2:
> Context is geen trigger. Support is geen buy. Resistance is geen short.
> Candle rejection is geen confirmed reversal. Compression is geen breakout.
> Local bounce is geen macro trend change.

---

## 3. Input

A0 gebruikt read-only:

- L4 SQLite snapshot store (`l4_store/{PAIR}/YYYY-MM.sqlite`)
- snapshot metadata (uit `snapshots` tabel)
- raw_blobs per timeframe (uit `raw_blobs` tabel)
- snapshot_timeframes (uit `snapshot_timeframes` tabel)
- bestaande inspectorlogica of inspector-output als basis

A0 mag **NIET**:
- OHLC opnieuw ophalen van exchange/bridge
- Indicators herberekenen uit raw candles
- Candles reconstrueren buiten wat in de snapshot staat
- Schrijven naar de database
- Nieuwe velden aan de snapshot toevoegen

### 3.1 Raw_blobs veld-whitelist

A0 mag raw_blobs alleen lezen via een expliciete veld-whitelist.

**Toegestane raw_json veldgroepen:**
- `meta`
- `price.current`
- `price.previous`
- `indicators`
- `candle_micro`
- `structure`
- `levels`
- `trendlines`
- `diagnostics`

**Niet toegestaan:**
- `candles`
- candle arrays
- originele OHLC-reeksen
- source payloads met volledige candle history
- reconstructie van historische candles
- indicator-herberekening vanuit raw candles

**Regel:**
Als een raw_blob ooit een volledige candle-array bevat onder keys zoals `candles`, `ohlc`, `history`, `series`, `source_payload` of vergelijkbaar, dan mag A0 die **niet** gebruiken voor readout.

A0 moet dan:
- die velden negeren of hard failen volgens guardrailbeleid
- expliciet rapporteren dat candle-array velden buiten A0-contract vallen

**Harde zin:** A0 leest snapshotvelden, geen OHLC-history.

### 3.2 SQLite read-only toegang — mode=ro

A0 moet SQLite **read-only** openen via URI:

```
file:<db_path>?mode=ro
```

Voor actieve WAL-databases:
- gebruik `mode=ro`
- **geen** gewone read/write connectie
- **geen** `PRAGMA wal_checkpoint`
- **geen** writes
- **geen** schema-wijziging
- **geen** journal side-effects
- bestaande WAL/SHM van de live writer **mogen** aanwezig zijn
- A0 **mag geen** nieuwe journal/WAL/SHM artefacten veroorzaken

**Immutable mode:**
- `immutable=1` mag **alleen** voor bevroren kopieën of offline restored archives
- **niet** standaard gebruiken op actieve live WAL-databases
- **niet** gebruiken als de L4 filler live schrijft

**Acceptatiecriteria voor DB-toegang:**
- A0 run veroorzaakt geen nieuwe SQLite artefacten
- A0 blokkeert de L4 writer niet
- A0 faalt netjes bij locked/corrupt/unreadable DB
- A0 heeft concurrency-test: lezen terwijl L4 runner schrijft

---

## 4. Harde datafeiten

Deze feiten moeten expliciet in A0's documentatie en guardrails:

| Feit | Bron |
|------|------|
| De volledige 240-candle-array zit **NIET** in de L4 snapshot | Readout Contract v2 §3 |
| `meta.candles_final=240` betekent: Hermes berekende op basis van 240 candles | Readout Contract v2 §3 |
| Het betekent **NIET**: 240 candles opgeslagen in snapshot | Readout Contract v2 §3 |
| Snapshot bevat alleen `price.current` en `price.previous` (dicts, geen arrays) | Readout Contract v2 §3 |
| Analyst kan later indicators **niet** herberekenen uit snapshot alleen | Readout Contract v2 §3 |
| HH/HL/LH/LL labels mogen alleen genoemd worden als ze letterlijk in `structure.recent_structure` of `structure.structure_points` staan | Readout Contract v2 §3 |
| `source_age_seconds` per TF toont hoe vers de onderliggende OHLC was | Inspector output |
| `raw_hash` is uniek per raw_blob, 0% dedup is verwacht door volatile source-velden | Archive Contract v2 §3 |

---

## 5. Output van A0

**Architectuurbesluit — template-rendering als basis:**

A0 gebruikt **geen vrije tekstgeneratie** als primaire outputmethode.

A0-output wordt **template-based** opgebouwd:
- vaste secties
- vaste veld-slots
- vaste zinnen
- vaste waarschuwingen
- **geen** creatieve formulering
- **geen** interpretatieve parafrase buiten whitelist

**Reden:** Template-rendering voorkomt hallucinaties beter dan achteraf scannen.
De forbidden-language scanner blijft **tweede verdedigingslaag**, niet de primaire beveiliging.

Prototype moet later maximaal deze secties genereren:

### 5.1 Header
```
PAIR:        ETHEUR
SNAPSHOT:    ETHEUR-1783692120-1m5m15m60m240m-66c5e8a8de53
ASOF:        2026-07-10T14:02:00+00:00
STORED_AT:   2026-07-10T14:02:46+00:00
AGE:         94s
COMPLETENESS: YES — 5/5 timeframes
```

### 5.2 Data Quality
- 5/5 TFs aanwezig: ja/nee
- `candles_final` per TF (altijd 240 indien compleet)
- `source_age_seconds` per TF
- warnings of missing velden
- hashes en provenance indien relevant voor audit

### 5.3 Timeframe Overview
Per timeframe (1m → 5m → 15m → 60m → 240m):
- laatste candle timestamp en close
- source type (bridge/cache/mixed)
- source age
- opgeslagen velden per TF naast elkaar tonen

**A0/A1 grens — harde regel:**
A0 mag per timeframe de opgeslagen velden naast elkaar tonen.

A0 mag **NIET** zelf concluderen:
- dat timeframes conflicteren
- dat iets opvallend is
- dat er MTF alignment of misalignment is
- dat de markt bullish/bearish is
- dat context gunstig/ongunstig is

**Voorbeeld toegestane A0-zin:**
"1m veld X heeft waarde A. 240m veld X heeft waarde B."

**Voorbeeld verboden A0-zin:**
"1m en 240m conflicteren."

**Besluit:** MTF-conflict, MTF-alignment en contextweging horen bij Analyst A1+, niet bij A0.

### 5.4 Price Context
- `price.current`: open, high, low, close, volume
- `price.previous`: open, high, low, close, volume
- Richting van laatste candle: afleidbaar uit current vs previous close
- **Niet**: historische candle-array claim ("de laatste 240 candles tonen...")

### 5.5 Structure
- Swing highs en swing lows (indien aanwezig)
- HH/HL/LH/LL labels — alleen als ze letterlijk in de data staan
- `recent_structure` met `last_high_label` en `last_low_label`
- `structure_points` indien aanwezig

### 5.6 Support / Resistance
- `levels.nearest_support`
- `levels.nearest_resistance`
- `levels.below_price` (support candidates)
- `levels.above_price` (resistance candidates)
- `levels.clusters_raw` (alle S/R)
- `trendlines.recent.lower` en `trendlines.recent.upper` (dynamische S/R)

### 5.7 Candle Micro
- `patterns`
- `body_trend`
- `wick_bias`
- `micro_state`
- **Zonder** reversal/breakout-confirmatie te claimen

### 5.8 Indicators
- Alleen opgeslagen indicatorvelden benoemen: EMA, ATR, ADX, VWAP, Volume
- Geen herberekening
- Geen signaalinterpretatie als trade
- Formulering: "ADX staat op X" — niet "ADX bevestigt trend"

### 5.9 Missing / Uncertainty
- Ontbrekende velden
- Stale data (source_age > drempel)
- Incomplete data (minder dan 5 TFs)
- Afstand tot S/R ontbreekt indien niet berekend in snapshot

**A0/A1 grens — geen MTF-conflict claims:**
A0 rapporteert per TF de aanwezige/ontbrekende velden.
A0 concludeert **niet** dat TFs conflicteren, aligneren of elkaar tegenspreken.
Die weging hoort bij Analyst A1+.

### 5.10 What This Does NOT Say
Verplichte afsluiter:
```
WHAT THIS DOES NOT SAY:
- Geen entry/exit/long/short/buy/sell
- Geen tradebeslissing of voorspelling
- Geen bewezen strategie
- Geen historische candle-array in snapshot
- Geen setup-score of candidate-beslissing
```

---

## 6. Verboden taal

A0-output mag deze woorden/zinnen **nooit** gebruiken als beslissing.

### 6.1 Nederlands

| Categorie | Verboden woorden |
|-----------|-----------------|
| Trade acties | buy, sell, koop, verkoop, kopen, verkopen, long gaan, short gaan |
| Positie | instappen, uitstappen, positie nemen, positie openen, positie sluiten, bijkopen, afbouwen |
| Order types | entry, exit, TP, SL, stop loss, take profit |
| Signalen | signal, confirmed trade, setup confirmed, setup, signaal, koopmoment, verkoopmoment |
| Kwaliteit | mooi moment, goed moment, kansrijke trade |
| Confidence | trade confidence, win probability, high probability setup |
| Voorspelling | gaat stijgen, gaat dalen, stijgt waarschijnlijk, daalt waarschijnlijk, will go up, will go down, target price, expected move |
| Oordelen | this is a good trade, breakout confirmed, reversal confirmed |

### 6.2 Engels

| Categorie | Verboden woorden |
|-----------|-----------------|
| Positie | position, open position, close position, add to position, reduce position |
| Strategie | DCA, dollar cost average, risk reward, R:R, position size, sizing, leverage |
| Bias | bullish as trade reason, bearish as trade reason, oversold as buy reason, overbought as sell reason |
| Voorspelling | likely to rise, likely to fall, good trade, high probability |

### 6.3 Scannerregels

- gebruik **word-boundary matching** (`\b`)
- voorkom false positives zoals `belong` bevat `long`
- voorkom false positives zoals `selloff` bevat `sell`
- voorkom false positives zoals `buyout` bevat `buy`
- scan niet alleen tekst, maar ook:
  - markdown output
  - JSON values
  - JSON keys
  - section titles
  - metadata keys

### 6.4 Negatiebeleid — whitelist-only

**Geen** algemene negatie-parser bouwen.

Alleen **letterlijke whitelist-zinnen** zijn toegestaan als negatie:

- "Dit is geen entry."
- "Dit is geen buy/sell-signaal."
- "Dit is geen long/short-advies."
- "Dit is geen tradebeslissing."
- "Deze context rechtvaardigt geen trade."
- "Support betekent niet 'kopen'."

Alles buiten die letterlijke whitelist moet **hard failen** als verboden trade-taal voorkomt.

---

## 7. Confidence-regel

| Toegestane confidence-types | Verboden confidence-types |
|-----------------------------|--------------------------|
| `data_quality_confidence` | `trade_confidence` |
| `source_confidence` | `entry_confidence` |
| `completeness_confidence` | `signal_confidence` |
| | `setup_confidence` |
| | `win_probability` |
| | `readout_confidence` |

**`readout_confidence` is geschrapt** als losstaand veld. Het concept is te vaag en leent zich voor interpretatie als trade-relevantie.

De resterende toegestane confidence-velden gaan **uitsluitend** over datakwaliteit:
- `data_quality_confidence` — hoe compleet en consistent de snapshot is
- `source_confidence` — hoe betrouwbaar de OHLC-bron was op moment van snapshot
- `completeness_confidence` — of alle verwachte velden en TFs aanwezig zijn

Deze velden mogen in output verschijnen maar alleen over datakwaliteit gaan — **nooit** over trade-uitkomst, setupkwaliteit, marktcontext, S/R-nabijheid, trendrichting, indicatorstatus, candle_micro, tradekans, of expected move.

---

## 8. Prototypevorm later

### 8.1 Conceptuele locatie

```
projects/hermes-v03-analyst/a0_snapshot_readout/
```

Nog niet aanmaken. Dit is de geplande locatie conform ADR 2026-07-09.

### 8.2 Mogelijke bestanden (later)

| Bestand | Functie |
|---------|---------|
| `__init__.py` | Package init |
| `read_snapshot.py` | Leest snapshot + raw_blobs + timeframes uit SQLite |
| `map_fields.py` | Vertaalt ruwe snapshotvelden naar leesbare secties |
| `render_readout.py` | Genereert output in text/json/markdown formaat |
| `guardrails.py` | Scant output op verboden taal, hard fail bij overtreding |
| `cli.py` | CLI entry point |
| `test_a0_snapshot_readout.py` | Volledige testsuite |
| `fixtures/` | Test snapshots in verschillende staten |

### 8.3 CLI interface (later)

```bash
# Lees laatste snapshot voor een pair
python3 projects/hermes-v03-analyst/a0_snapshot_readout/cli.py \
  --pair ETHEUR \
  --snapshot latest \
  --base-dir projects/hermes-v03-interpreter/l4_store \
  --format text

# Lees specifieke snapshot
python3 projects/hermes-v03-analyst/a0_snapshot_readout/cli.py \
  --pair BTCEUR \
  --snapshot BTCEUR-1783692120-1m5m15m60m240m-ba92c9370a97 \
  --base-dir projects/hermes-v03-interpreter/l4_store \
  --format json

# Output formaten: text, json, markdown
```

**Nu niets aanmaken.** Dit is alleen specificatie.

---

## 9. Guardrails later

Prototype moet later **hard falen** (exit code ≠ 0) als output verboden trade-taal bevat.

### 9.1 Guardrail checks

De guardrails-module moet output scannen op:

1. **Verboden woorden**: exact match op buy/sell/long/short/entry/exit/TP/SL etc.
2. **Candle-array hallucination**: zinnen als "de 240 candles tonen", "in de snapshot zie je 240 candles dat..."
3. **Trade-claims**: "support houdt dus kopen", "resistance breekt dus long"
4. **Reversal/breakout confirmatie**: "breakout confirmed", "reversal confirmed"
5. **Voorspellingen**: "zal stijgen", "target is", "verwacht wordt"

### 9.2 Guardrail acties

Bij overtreding:
- Log de exacte overtreding met regelnummer
- Exit code 1
- Geen output naar stdout (alleen stderr)
- Melding: "A0 GUARDRAIL VIOLATION: [type] in sectie [X]: [tekst]"

### 9.3 Tests voor guardrails

```python
# Test 1: output zonder trade-taal → exit 0
# Test 2: output met "buy" → exit 1
# Test 3: output met "long setup confirmed" → exit 1
# Test 4: output met "240 candles in snapshot tonen" → exit 1
# Test 5: output met "support houdt dus kopen" → exit 1
# Test 6: output met "breakout confirmed" → exit 1
# Test 7: output met "Dit is geen entry" → exit 0 (negatie toegestaan)
# Test 8: lege output → exit 0
```

---

## 10. Testplan later

Minimale testsuite vóór implementatie gereed:

### 10.1 Fixture snapshots

| Fixture | Beschrijving |
|---------|-------------|
| Fixture 1 | Volledige snapshot: 5 TFs, alle velden aanwezig, S/R, structure, indicators |
| Fixture 2 | Ontbrekende TF: 4/5 TFs (bijv. 240m missing) |
| Fixture 3 | Stale source age: source_age > 300s op 1m |
| Fixture 4 | S/R aanwezig: nearest_support + nearest_resistance gevuld |
| Fixture 5 | Geen S/R: levels leeg of None |
| Fixture 6 | HH/HL labels aanwezig in structure_points |
| Fixture 7 | Geen labels: structure_points leeg |
| Fixture 8 | Corrupte snapshot: raw_json ontbreekt of is beschadigd |

### 10.2 Functionele tests

| Test | Beschrijving |
|------|-------------|
| read_latest | Leest laatste snapshot voor pair → retourneert alle secties |
| read_by_id | Leest specifieke snapshot_id → zelfde output als inspector |
| completeness_yes | 5/5 TFs → COMPLETENESS: YES |
| completeness_no | 4/5 TFs → COMPLETENESS: NO, met missing TF |
| source_age_reporting | Toont source_age_seconds per TF |
| no_candle_array_claim | Output bevat nooit "240 candles in de snapshot" |
| verboden_taal_scan | Alle output passeert guardrails |
| read_only_check | Geen writes naar DB (controleer via sqlite3 total_changes) |

### 10.3 Guardrail-specifieke tests

| Test | Beschrijving |
|------|-------------|
| false_positive_scanner | `belong`, `longer`, `selloff`, `buyout` mogen **niet** triggeren als `long`/`sell`/`buy` |
| json_markdown_guardrail | Verboden termen in JSON keys, JSON values, markdown headings en tekst moeten gedetecteerd worden |
| whitelist_negatie | "Dit is geen entry." → exit 0; "Dit is misschien geen entry." → exit 1 (buiten whitelist) |
| sqlite_artefact | A0 veroorzaakt geen nieuwe `-journal`, `-wal`, `-shm` artefacten; bestaande WAL/SHM van writer mogen blijven |
| unknown_pair_empty_db | Onbekende pair / lege DB / geen snapshots → faalt netjes zonder traceback |
| concurrency | A0 leest terwijl L4 writer/timer actief is; A0 blokkeert writer niet; A0 crasht niet |
| schema_contract_version | Onbekende snapshot `schema_version` of `contract_version` → hard fail |
| raw_blob_ohlc_backdoor | Als raw_json een `candles`/`history`/`ohlc` array bevat, gebruikt A0 die niet |
| template_only_output | Output komt uit vaste templates/slots, niet uit vrije generatie |

### 10.4 Integratietest

```bash
# End-to-end: lees ETHEUR latest → text output → scan op guardrails
python3 -m pytest projects/hermes-v03-analyst/a0_snapshot_readout/test_a0_snapshot_readout.py -v
```

---

## 11. Acceptatiecriteria later

A0 prototype is pas acceptabel als:

| # | Criterium | Verificatie |
|---|-----------|-------------|
| 1 | **Read-only**: schrijft nooit naar DB | `sqlite3_total_changes` = 0 na run |
| 2 | **SQLite mode=ro**: opent DB via `file:...?mode=ro` | Code audit + strace verificatie |
| 3 | **Geen DB artefacten**: geen nieuwe -journal/-wal/-shm | `ls -la` voor/na run |
| 4 | **Geen writer-blokkering**: L4 filler draait door tijdens A0-run | Concurrency test |
| 5 | **Geen OHLC fetch**: geen netwerk calls naar exchange/bridge | Mock of network audit |
| 6 | **Geen indicator herberekening**: leest alleen opgeslagen velden | Code audit |
| 7 | **Geen tradebeslissing**: output bevat geen verboden taal | Guardrail scan |
| 8 | **Geen candle-array hallucinatie**: claimt nooit 240 candles te tonen | Guardrail scan |
| 9 | **Raw_blob whitelist**: candle/ohlc/history arrays worden niet gelezen | Code audit + raw_blob backdoor test |
| 10 | **Template-based output**: output komt uit vaste templates, niet vrije generatie | Code audit |
| 11 | **Forbidden-language scan**: scant text/markdown/JSON/keys | Guardrail test suite |
| 12 | **Onbekende schema/contract versie**: hard fail | Schema version test |
| 13 | **Contractregels afgedwongen**: volgt Readout Contract v2 | Handmatige review |
| 14 | **Tests groen**: alle fixtures + functionele + guardrail tests pass | `pytest -v` |
| 15 | **Menselijk leesbaar**: output is begrijpelijk zonder tradingkennis | Fable/Claude review |
| 16 | **Onafhankelijk reviewbaar**: Fable of Claude kan output beoordelen | Externe audit |
| 17 | **CLI werkt**: `--pair ETHEUR --snapshot latest --format text` geeft output | Manuele test |
| 18 | **Latere lagen parsen A0-output niet**: A0 is presentatie, geen datalaag | Architectuuraudit |

---

## 12. Relatie tot latere lagen

```
┌─────────────────────────────────────────────────────────┐
│                     INTERPRETER                          │
│  (data/geheugen — bestaat al)                            │
│  OHLC bridge → L4 snapshots → raw blobs → inspector     │
│  Read-only. Geen analyse.                                │
├─────────────────────────────────────────────────────────┤
│                     ANALYST A0                           │
│  (beschrijvende betekenis — DIT PLAN)                     │
│  Snapshot Readout: feitelijke context in mensentaal      │
│  Geen trade. Geen candidate. Geen score.                 │
├─────────────────────────────────────────────────────────┤
│                     OUTCOME BUILDER                      │
│  (meet wat daarna gebeurde — later)                       │
│  Historische uitkomst per snapshot.                      │
│  Basis voor backtest.                                    │
├─────────────────────────────────────────────────────────┤
│                  STRATEGY TEST HARNESS                   │
│  (test regels historisch — later)                         │
│  Punt-in-tijd simulatie zonder lookahead.                │
├─────────────────────────────────────────────────────────┤
│                     ANALYST A1+                          │
│  (contextweging — later)                                  │
│  MTF alignment, setup/no_setup, candidate/no_candidate   │
│  Pas na outcome/backtest basis.                          │
├─────────────────────────────────────────────────────────┤
│                      TESTBOT                             │
│  (simuleert regels — later)                               │
│  Paper trading met neporders.                            │
├─────────────────────────────────────────────────────────┤
│                    PAPER TRADER                          │
│  (live markt, neporders — later)                          │
│  Real-time data, geen echt geld.                         │
├─────────────────────────────────────────────────────────┤
│                     LIVE TRADER                          │
│  (echte orders — veel later)                              │
│  Pas na bewezen paper record + aparte contracten.        │
└─────────────────────────────────────────────────────────┘
```

A0 is de **eerste stap bovenop pure data**. Zonder A0 is er geen gedeelde taal over wat een snapshot bevat. Zonder die taal is Analyst A1+ niet veilig te bouwen.

### 12.1 Harde architectuurregel — A0 is presentatie, geen datalaag

A0-output is **presentatie**, geen datalaag.

Latere lagen mogen A0-output **NIET** parsen of gebruiken als input:
- **Outcome Builder** leest snapshots, niet A0-tekst
- **Strategy Test Harness** leest snapshots/outcomes, niet A0-tekst
- **Analyst A1+** leest snapshots/gestructureerde data, niet A0-proza
- **Testbot** leest regels/snapshots/outcomes, niet A0-proza
- **Trader** leest **nooit** A0-proza als beslissingsbron

**Reden:** Geen proza-gebaseerde pipeline. A0 is voor mensen, niet voor machines.

---

## 13. Open vragen

| # | Vraag | Status |
|---|-------|--------|
| 1 | Exacte outputvorm: plain text, JSON, markdown, of alle drie? | Open |
| 2 | Gebruiken we `inspect_l4_snapshot.py` output als input, of lezen we direct SQLite? | Open |
| 3 | Moet A0 per pair/latest werken of ook per snapshot_id? Beide? | Open |
| 4 | Moet A0 meerdere TFs samenvatten in vaste volgorde (1m→240m)? | Open |
| 5 | Hoe hard moet de forbidden-language scanner zijn? Hard fail of warning-mode? | ✅ **Beslist: hard fail** — exit code ≠ 0, geen output naar stdout, alleen stderr |
| 6 | Waar bewaren we voorbeeldreadouts ter review? | Open |
| 7 | Moet Fable eerst een readout-review rubric maken vóór implementatie? | Open |
| 8 | Moet A0 distance_pct tot S/R zelf berekenen of alleen tonen als al aanwezig? | ✅ **Beslist: whitelist rekenkunde** — zie §13.1 |
| 9 | Moet A0 de output van meerdere pairs kunnen vergelijken? | Open |
| 10 | Hoe integreren we A0-output later in second brain / meeting notes? | Open |

### 13.1 Toegestane afgeleide rekenkunde (whitelist)

A0 mag alleen eenvoudige afgeleide rekenkunde doen via expliciete whitelist.

**Toegestaan:**
- verschil tussen `price.current.close` en opgeslagen `levels.nearest_support` / `levels.nearest_resistance`
- `distance_pct` vanaf `price.current.close` naar opgeslagen levels
- candle direction uit `price.current.open` vs `price.current.close`
- age seconds vanaf `stored_at` / source timestamps

**Niet toegestaan:**
- indicator herberekenen
- trend bepalen
- MTF alignment bepalen
- setupkwaliteit bepalen
- support/resistance opnieuw berekenen
- candles reconstrueren
- outcome voorspellen

---

## 14. Conclusie

A0 Snapshot Readout mag gepland worden.

Dit document is het plan. Het bouwt niets.

**Wat dit plan toestaat:**
- A0 Snapshot Readout als concept vastleggen
- Input/output contract definiëren
- Guardrails en tests specificeren
- Relatie tot Outcome/Strategy/Analyst/Testbot/Trader vastleggen

**Wat dit plan verbiedt:**
- Code schrijven
- Prototype bouwen
- Directories aanmaken
- DB wijzigen
- Services/timers wijzigen
- Analyst A1 bouwen
- Strategy Test bouwen
- Outcome Builder bouwen
- Trader bouwen

**Volgende stap na dit plan:**
Lexi beslist wanneer A0 gebouwd mag worden.
Pas als dit plan en de open vragen besproken zijn, start implementatie.

---

## RAPPORTAGE — HARDENED V2

| # | Check | Status |
|---|-------|--------|
| 1 | Plan gepatcht | ✅ Ja — 10 patches toegepast |
| 2 | Raw_blobs whitelist toegevoegd | ✅ Ja (§3.1) |
| 3 | OHLC-backdoor gesloten | ✅ Ja — candles/ohlc/history arrays expliciet verboden |
| 4 | SQLite mode=ro regel toegevoegd | ✅ Ja (§3.2) |
| 5 | Immutable nuance toegevoegd | ✅ Ja — alleen voor bevroren kopieën/archives |
| 6 | Concurrency/writer-blokkering toegevoegd | ✅ Ja (§3.2 + §10.3) |
| 7 | Template-rendering als basis toegevoegd | ✅ Ja (§5) |
| 8 | A0/A1 grens rond TF-conflict/opvallend aangescherpt | ✅ Ja (§5.3 + §5.9) |
| 9 | Forbidden-language lijst uitgebreid | ✅ Ja — NL + EN, positie/strategie/bias categorieën (§6) |
| 10 | Word-boundary + whitelist-negatie toegevoegd | ✅ Ja (§6.3 + §6.4) |
| 11 | JSON-key scan toegevoegd | ✅ Ja (§6.3) |
| 12 | readout_confidence geschrapt | ✅ Ja — uit tabel verwijderd, vervangen door strikte datakwaliteit-definitie (§7) |
| 13 | Testplan uitgebreid | ✅ Ja — 9 guardrail-specifieke tests toegevoegd (§10.3) |
| 14 | Latere lagen mogen A0-output niet parsen | ✅ Ja — harde architectuurregel (§12.1) |
| 15 | Schema/contract version hard fail toegevoegd | ✅ Ja (§10.3 + §11) |
| 16 | Open vragen gesloten | ✅ Ja — #5 hard fail, #8 whitelist rekenkunde (§13) |
| 17 | Geen codewijziging | ✅ Geen code aangeraakt |
| 18 | Geen DB wijziging | ✅ Geen SQLite geopend |
| 19 | Geen prototype | ✅ Alleen plan-document |
| 20 | Geen commit | ✅ Geen git acties |
| 21 | Git status | ✅ Ongewijzigd |

**Fable-eindoordeel na hardening:** 🟢 GROEN — plan is nu implementatieklaar.

De vijf contractgaten zijn gedicht:
1. ✅ Read-only DB-toegang: `mode=ro`, concurrency-test, geen WAL-artefacten
2. ✅ A0/A1 grens: TF-conflict/opvallende context verhuisd naar A1+
3. ✅ Forbidden-language scanner: word-boundary, NL+EN, JSON/MD scan, whitelist-negaties
4. ✅ Raw_blobs OHLC-achterdeur: expliciete veld-whitelist, candle arrays verboden
5. ✅ Vrije tekstgeneratie: template-rendering als primaire output, scanner als tweede laag
