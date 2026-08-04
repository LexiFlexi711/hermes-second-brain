---
title: NOA-Reign — Roadmap v2
type: project
date: 2026-07-12
status: Levend document
replaces: 2026-07-12-noa-reign-visie-en-roadmap.md (v1)
tags: [roadmap, noa-reign, outcome-builder, chartreader, evidence-lab]
---

# NOA-Reign — Roadmap v2 (samengevoegd: visie + Fable + Noa)

**Datum:** 2026-07-12
**Status:** Levend document — mag en zal bijgestuurd worden
**Vervangt:** 2026-07-12-noa-reign-visie-en-roadmap.md (v1)
**Nieuw in v2:** Noa's zeven punten verwerkt met triggers, tijdlijn rond 5/8 + 7 weken herstelvenster, eerste Hermes-opdracht gedefinieerd.

## 0. De tijdlijn die alles stuurt

| Periode | Situatie | Focus |
|---------|----------|-------|
| Nu → 5/8 (±3 weken) | Naast werk, beperkte avonduren | Bouwen: Phase 1B implementeren, L3 blockers sluiten, batch laten draaien |
| 5/8 → ±23/9 (7 weken) | Thuis, herstel na operatie | Testen: schermfase, human vs reader, journaal, data accumuleert vanzelf |
| Na 23/9 | Terug naar normaal ritme | Evidence Lab + blok 4 op basis van 7 weken observatie + verzamelde outcomes |

De hefboom: elke dag dat de 1B-batch vóór 5/8 draait, is een dag extra outcome-history tegen de tijd dat het herstelvenster start. De 7 weken zijn goud — maar alleen als er tegen dan iets op scherm staat én iets in de store zit. Daarom: bouwen gaat de komende 3 weken vóór alles, ook vóór nieuwe structuur.

**Prioriteit binnen de 3 weken:**

- Week 1–2: Phase 1B implementeren (store eerst — data-accumulatie start bij eerste batch-run, niet bij perfectie)
- Week 3: Layer 3 completeness-blockers (missing_local_upper, crossed/inverted lines) → schermwaarde
- Als er tijd over is: schermweergave-polish. Niks anders.

## 1. De kern van het idee

Alles wat nu bestaat, bestaat voor één ding: het juiste moment bepalen voor strategie-ingang en -uitgang, en het opsporen van grote moves ("olifanten") die we willen leren herkennen vóórdat ze gebeuren.

Aanpak omgekeerd aan 95% van de botbouwers: eerst het meetinstrument — een chartreader die marktstructuur machineleesbaar maakt en een outcome-store die eerlijk meet wat er ná elk moment werkelijk gebeurde. Pas daarna strategie, tester, trader.

Noa's formulering van wat we bouwen, overgenomen als noord-ster: een onderzoeksplatform dat over drie jaar nog weet waarom het iets gelooft — met Fable's voorwaarde erbij: over drie jaar iets geloven vereist dat er de komende drie maanden iets draait. Platform en pipeline houden elkaar in evenwicht; als ze botsen wint de pipeline.

## 2. Wat er staat (frozen / gebouwd)

- **Blok 1 — Data pipeline:** L4 snapshot store (SQLite, ro), cache freshness per timeframe bewaakt.
- **Blok 2 — Chartreader (Layer 3):** multi-TF structuurlezer. Calculation-verified. Twee open completeness-blockers. Layer 4 geblokkeerd tot L3 compleet.
- **Blok 3 — Interpreter + outcome opslag (A0–A1b):** A0 frozen (4872eaa). Phase 1A calculator frozen (901a68e). Phase 1B plan v6 GREEN na reviewcyclus v3→v6 — implementatie mag starten. Phase 1C (archive) gescoped, niet gepland.
- **Erfenis vorige generatie:** 5 strategieën event-driven gebacktest (no-lookahead). Momentum en V2 sterkst. Kernles: entries met "juiste cijfers" tegen resistance in late pullback = slechte trades — structurele context verslaat indicatorcijfers.

## 3. Roadmap-blokken (v2)

| Blok | Wat | Trigger / status |
|------|-----|------------------|
| 1 | Data pipeline | Staat |
| 2 | Chartreader (L3) | Blockers sluiten in week 3 |
| 3 | Interpreter + outcome opslag | NU — Phase 1B implementatie gestart |
| 3.5 | Evidence Lab (Noa) — geformaliseerde hypothese-toetsing: pre-registratie, baselines, negative controls, sample-minima, multiple-testing boekhouding | Trigger: blok 3 dicht + lijn A geformuleerd. Ontwerp mag in herstelvenster op papier |
| 4 | Strategie — conditionele regels op bestaande logica | Na 3.5 |
| 5 | Tester (Strategy Harness) — signal quality en portfolio quality apart gemeten (Noa punt 3) | Na 4; Harness ontwerpt de lat vóór de strategie hem mag claimen |
| 5b | Risk management — sizing, max exposure, correlatie, drawdown-limieten, killswitch | Eigen blok, eigen plan-review |
| 6 | Trader — papier, dan live | Na 5/5b; papier krijgt vooraf gepinde duur + go/no-go |
| 6b | Operations — monitoring, alerting, API-uitval, "flat bij twijfel"-protocol | Voorwaarde voor live |
| 7 | Sell the reader, keep the trader | Horizon; twee exits i.p.v. één |

**Doorlopende structuren (Noa, met Fable-triggers):**

- **Feature Contract Registry + feature_version** — versioneert de betekenis van features (semantische drift is onzichtbare corruptie die de hash-chain niet vangt). Goedkope eerste stap NU: feature_version: 1 als veld in het 1B-schema meebakken via micro-delta v6→v7 (één veld, included in record_id, ALLOWED_FEATURE_VERSIONS={1}; Fable delta-check volstaat). Volledige registry start bij eerste draaiende batch.
- **Canonical Audit Corpus** — vaste examenset charts waar de reader blijvend op getoetst wordt; regressietesten voor betekenis. Start bij het sluiten van de L3-blockers: die twee bugs zijn letterlijk corpus-case 1 en 2.
- **Tradejournaal** — licht (Fable-afzwakking van Noa punt 6): drie regels per moment — reader zei / ik besloot / wat gebeurde. Doel is hypothese-generatie, geen bewijs. Promoveert pas tot formeel human-vs-reader experiment als het na weken nog wordt ingevuld én er iets in zit. Het perfecte journaal dat na drie weken stopt verliest van het simpele dat zeven weken volgehouden wordt.

## 4. Het herstelvenster (5/8 → ±23/9) — human vs bot

Zeven weken thuis is het eerste echte human-vs-reader onderzoek, in lichte vorm:

- Schermfase: blok 1+2+3 live op scherm, dagelijks meekijken op eigen tempo (herstel gaat voor — dit is observeren, geen verplichting).
- Licht journaal vanaf dag 1 (formaat hierboven).
- Batch draait op de achtergrond — outcomes accumuleren zonder werktijd.
- Hypotheses vastleggen: lijn A (timing/pullback-resistance) en lijn B (olifanten) als gedateerde documenten, in meetbare L3-termen, vóór outcome-data bekeken wordt.
- Evidence Lab op papier ontwerpen (geen code): spelregels, baseline-definities, negative-control-recepten.
- Einde venster: journaal + verzamelde outcomes = de input voor blok 3.5/4.

## 5. Onderzoekslijnen

**Lijn A — Conditionele activatie / timing** (kan op 1B-data):
Strategieën zijn de basis; de vraag is onder welke omstandigheden ze beter werken. Kiemhypothese: pullback-entries laat in de pullback, vlak onder resistance = structureel slecht (weinig ruimte boven, veel eronder). Toets: verbetert het outcome-profiel meetbaar als L3 ruimte tot de volgende resistance toont?

**Lijn B — Olifanten** (vereist Phase 1C — multi-day windows; formeel behandeld als event-study tot prospectieve uplift bewezen is, Noa punt 7):
Moves gestratificeerd per klasse (2–4%, 4–7%, 7%+; mechanisch per window). Wat zagen we 1u / 24u / dagen vooraf, en overleven tendensen forward, backward én over regimes?

**Spelregels (Evidence Lab-kern — Fable + Noa punt 2 samengevoegd):**

- Hypotheses vooraf, gedateerd, vóór de data.
- Conditie-vocabulaire gesloten; alleen features met economische rationale.
- Voorwaarts meten vanaf de conditie — alle gevallen, ook de duizend keer niks.
- Elke hypothese krijgt een baseline én een negative control (geschudde labels moeten níks vinden; de tendens moet de domme baseline verslaan).
- Zoeken/valideren gescheiden in tijd; validatieperiode wordt één keer aangeraakt.
- Minimum sample per bucket, na fees.
- Multiple-testing boekhouding: bijhouden hoeveel combinaties geprobeerd zijn.
- "Niks gevonden" is een toegestane, waardevolle uitkomst. Het instrument mag nee zeggen.

## 6. Succes- en kill-criteria (pinnen vóór blok 5 — in getallen)

- Papierfase: minimaal ___ maanden, max drawdown < ___%, rendement na fees > ___% → anders geen live.
- Live start met bedrag dat volledig verloren mag gaan; eerste live-jaar = collegegeld.
- Kill live: drawdown ___% of ___ opeenvolgende verliesweken → automatisch flat + review.
- Vastgelegd vóór de eerste papierrun; daarna nooit versoepeld.

## 7. Procesregels (verworven, niet onderhandelbaar)

- Plan → onafhankelijke review → GREEN → implementatieprompt. Zelfrapportage is geen bewijs.
- Eén taak per sessie; geen scope-creep; freeze-docs bij afronding.
- Guardrails: meetlagen bevatten nooit trade-vocabulaire.
- Gegenereerde data (outcome_store) nooit in git.
- Elke fase korter dan de vorige. Verzonden infrastructuur verzamelt data; perfecte plannen niet.
- Nieuwe structuur (registry, corpus, lab) start pas op zijn trigger — nooit als voorwerk.

## 8. Eerstvolgende stappen (volgorde = prioriteit)

1. Micro-delta v6→v7: feature_version veld toevoegen aan 1B-schema → Fable delta-check.
2. Hermes-opdracht 1B-01: canonical_json + hashing module (staat klaar, zie apart document) — schema-onafhankelijk, kan parallel aan stap 1.
3. Phase 1B verder implementeren in sessies van één module: store writer/resolver → batch → boundary/guardrail-tests (48 totaal).
4. Batch periodiek laten draaien op de server → accumulatie start.
5. Week 3: L3 blockers sluiten → corpus-case 1 en 2 vastleggen → Layer 4 deblokkeren.
6. 5/8: schermfase + licht journaal starten.
7. In herstelvenster: hypotheses A/B vastleggen, Evidence Lab op papier.
8. Na venster: Phase 1C scopen op wat lijn A/B werkelijk nodig hebben.
