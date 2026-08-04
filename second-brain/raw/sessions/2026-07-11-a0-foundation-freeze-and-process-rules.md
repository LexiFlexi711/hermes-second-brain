# A0 Foundation Freeze and Process Rules

**Datum:** 2026-07-11
**Status:** Frozen foundation — Fable green review passed
**Aanleiding:** Commit 4872eaa4 herstelt volledige A0 testsuite na procesfouten in eerdere commits

---

## 1. Status

Frozen foundation after Fable green review.

A0 Snapshot Readout Phase 1 is inhoudelijk compleet.
Geen verdere A0-wijzigingen zonder expliciete Lexi-opdracht + Fable review.

---

## 2. Frozen Commit

```
4872eaa4525bcfb8ff53f290b5b7100cfa810ae4
```

Branch: main (remote verified)
Remote: origin/main @ 4872eaa4

---

## 3. What Is Frozen

A0 Snapshot Readout Phase 1:

**Architectuurregels (blijvend):**
- A0 output is presentation, not data
- Latere lagen mogen A0-output niet parsen als input
- Geen interpretatie
- Geen tradeadvies
- Geen signalen
- Geen entry/exit
- Geen confidence (behalve data_quality/source/completeness)
- Geen A1-taal (conflict, alignment, opvallend, bullish, bearish, gunstig, breakout, reversal)
- Template-rendering als basis — geen vrije tekstgeneratie
- Stored-value exception policy voor Interpreter-output
- SQLite mode=ro — geen writes, geen WAL side-effects
- Raw_blob veld-whitelist — OHLC-backdoor gesloten

**A0 mag groeien in:**
- Meer stored fields tonen (nieuwe velden uit whitelist)
- Per-TF rendering (reeds geïmplementeerd)

**A0 mag NIET groeien in:**
- Interpretatievere taal
- Rijkere zinnen
- Contextweging
- MTF-alignment/conflict
- Setup/candidate/scoring

Rijkere taal hoort bij Analyst A1+, niet bij A0.

---

## 4. Verified by Fable

| Check | Resultaat |
|-------|-----------|
| A0 tests | 68/68 groen |
| Verdwenen regressietests | Alle terug (waren dropped in b3ddf032) |
| Orange-fix tests | 7 aanwezig |
| Per-TF STRUCTURE rendering | ✅ Werkt |
| Per-TF SUPPORT / RESISTANCE rendering | ✅ Werkt |
| Per-TF TRENDLINES rendering | ✅ Werkt |
| Real trendline details | ✅ Geen "present" masking meer |
| Real S/R level details | ✅ Geen list[n] masking meer |
| Numeric support/resistance edge case | ✅ Gedekt |
| CANDLE MICRO single-TF render | ✅ Gedocumenteerd als A0 Phase 1 |
| INDICATORS single-TF render | ✅ Gedocumenteerd als A0 Phase 1 |

---

## 5. Process Failure Discovered

Tijdens A0-ontwikkeling traden procesfouten op:

| Commit | Probleem |
|--------|----------|
| `735dd471` | Gecommit vóór green Fable review |
| `b3ddf032` | Gecommit vóór green Fable review |
| `b3ddf032` | Liet per ongeluk regressietests vallen |
| `4872eaa4` | Herstelde de volledige testsuite correct |

**Root cause:** Commits werden gemaakt zonder dat Fable groen licht had gegeven.
Tests werden herschreven in plaats van gepatcht, waardoor regressiedekking verdween.

---

## 6. New Mandatory Process Rules

### Rule 1 — Review Gate Before Commit

Voor foundation layers (A0, interpreter, L4, contracts, ADRs):

**Geen commit of push vóór green Fable review**, tenzij Lexi expliciet anders zegt.

Workflow:
1. Code schrijven
2. Tests runnen — alles groen
3. Fable review vragen
4. Pas na Fable ✅ → commit

---

### Rule 2 — Testcount Delta Required

Elk rapport dat tests aanraakt moet bevatten:

| Veld | Verplicht |
|------|-----------|
| Previous test count | Ja |
| New test count | Ja |
| Added tests (aantal + namen) | Ja |
| Removed tests (aantal + namen) | Ja |
| Reason for every removed test | Ja |

Geen delta = geen commit.

---

### Rule 3 — Removing a Test Is an Architecture Decision

Een test mag **niet** stilzwijgend verwijderd worden.

Een regressietest verwijderen vereist:
- Expliciete goedkeuring van Lexi OF Fable
- Documentatie van de reden in commit message
- Delta-rapportage in de bijbehorende prompt

**Default:** tests blijven staan tenzij actief geschrapt met akkoord.

---

### Rule 4 — Patch, Do Not Rewrite

Bij het fixen van gereviewde code:

- **Patch** het kleinst noodzakelijke gebied
- **Niet** volledige testbestanden herschrijven
- **Niet** historische regressiedekking vervangen

Uitzondering: alleen bij grootschalige architectuurwijziging met expliciet akkoord.

---

### Rule 5 — A0 Grows in Fields, Not in Sentences

A0 mag meer stored fields tonen.
A0 mag **niet** interpretatiever worden.

| Toegestane A0-groei | Verboden A0-groei |
|---------------------|-------------------|
| Nieuw veld uit whitelist tonen | "De markt is bullish" |
| Per-TF rendering uitbreiden | "1m en 240m conflicteren" |
| Nieuwe stored_value paths whitelisten | "Dit is een setup" |
| Template-sectie toevoegen voor nieuw veldtype | "Support houdt dus kopen" |

Rijkere taal hoort bij Analyst A1+, niet bij A0.

---

## 7. Next Allowed Phase

Outcome Builder planning mag starten na dit document.

**Outcome Builder moet:**
- L4/raw snapshot data lezen (of dedicated contracts)
- **Niet** A0-proza parsen
- **Niet** A0 wijzigen
- **Niet** strategielogica creëren
- **Niet** entries/exits creëren
- **Niet** Testbot/Trader-gedrag implementeren

**Outcome Builder is:**
- Wat gebeurde er na deze snapshot?
- Punt-in-tijd meting zonder lookahead
- Basis voor latere backtest

---

## 8. Open Next Step

1. ✅ A0 Foundation Freeze document — dit document
2. ⬜ Outcome Builder Phase 0 plan — volgende stap
3. ⬜ Geen code tot plan is gereviewed

---

## RAPPORTAGE

| # | Check | Status |
|---|-------|--------|
| 1 | Document created | ✅ Ja |
| 2 | Path | `/home/sjoe/system/hermes-second-brain/second-brain/raw/sessions/2026-07-11-a0-foundation-freeze-and-process-rules.md` |
| 3 | Line count | 199 |
| 4 | No code changes | ✅ Ja |
| 5 | No tests changed | ✅ Ja |
| 6 | No commit | ✅ Ja |
| 7 | Git status | ✅ Ongewijzigd — 0 tracked diffs |
