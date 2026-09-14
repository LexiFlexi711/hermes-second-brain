---
title: BTCEUR CASE 1 — Trade-Moment Map (walk-forward) 2026-09-11
type: project
status: afgerond — momentenkaart gelockt + ge-unblinded; 1 open onderzoeksvraag
tags: [btceur, case1, trade-momenten, walk-forward, pit, price-first, hermes-v03, research]
created: 2026-09-11
updated: 2026-09-14
---

# BTCEUR CASE 1 — Trade-Moment Map

Gerelateerd: [[crypto-tradebot-research-overview]] · [[crypto-data-pipeline]] · [[hermes-v03-interpreter]]

## Doel van CASE 1

Niet: de perfecte strategie, classifier, indicator of threshold.
**Wel:** de volledige kaart van betekenisvolle trade-momenten op de chart — welke
momenten walk-forward redelijkerwijs tradebaar waren, in welke richting, en wat er op
dat moment al zichtbaar was.

Uitdrukkelijk onderscheid tussen:

- **ALERT MOMENT** — prijs verandert duidelijk van gedrag, maar een trade is nog niet
  noodzakelijk verantwoord.
- **TRADE MOMENT** — er is genoeg informatie om LONG of SHORT te overwegen.

## Periode

**2026-09-01 → 2026-09-10** (60m visible research period van deze case).
Bevestigd door Lexi op 2026-09-14: dit komt overeen met de oorspronkelijke chart-spec —
ongeveer 7 dagen vóór de study-day 2026-09-08, de study-day zelf, en ongeveer 2 dagen erna.

TF-rol: **60m = trade-chart · 240m = grotere context · 15m = interne context.**

## Price-first / PIT-methodiek

- **FASE A** (`include_indicators=False`): eerst prijsactie, candle/sequentie,
  locatie/structuur en multi-TF prijscontext.
- **FASE B** (daarna pas): volume-afgeleiden, ATR, EMA, VWAP, ADX, GC/DC en overige
  indicatorcontext. Indicatoren bevestigen of waarschuwen — ze bepalen NIET welke
  prijs-events gezien worden.
- **PIT-regel (uit de lock):** enkel gesloten candles; 24h-grenzen uit gesloten candles;
  entry = open van de eerstvolgende candle.
- **Event lock vóór unblinding:** alle alerts/trades/confirmations zijn vastgelegd
  vóórdat outcome-data werd geopend.

## Lock-artefact

- Bestand: `case1_trade_moments_lock.json`
- Locatie: `/mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/projects/hermes-project/charts/case1-trade-moments-20260911/`
- **SHA256:** `9f31e9bb6136eb8c49ba668f59fdb21ab454b8ba5ca1d95d9e09a87d6e1ba964`
- **LOCKED_AT_TIME:** 2026-09-11T13:06:44Z (13 momenten-types, 12 momenten)
- Rapport (documentatie achteraf, 2026-09-14): `case1_trade_moments_report.md` + `.json`
  in dezelfde map. De lock is daarbij **niet** gewijzigd (SHA identiek).

## De 12 gelockte momenten

| id | timestamp (UTC) | type | direction |
|---|---|---|---|
| A1 | 2026-09-01 07:00 | ALERT | NONE |
| A2 | 2026-09-01 10:00 | ALERT | NONE |
| A3 | 2026-09-02 11:00 | ALERT | NONE |
| A4 | 2026-09-03 11:00 | ALERT | NONE |
| A5 | 2026-09-06 14:00 | ALERT | NONE |
| A6 | 2026-09-09 10:00 | ALERT | NONE |
| T1 | 2026-09-02 12:00 | TRADE | LONG |
| T2 | 2026-09-03 12:00 | TRADE | LONG |
| T3 | 2026-09-03 13:00 | CONFIRMATION | LONG |
| T4 | 2026-09-04 14:00 | TRADE | SHORT |
| T5 | 2026-09-08 15:00 | TRADE | LONG |
| L1 | 2026-09-03 15:00 | LATE | LONG |

Totalen: 6 alerts · 4 trade-momenten · 1 confirmatie · 1 late · 3 longs · 1 short.

## Belangrijkste resultaten

- Alle 4 genomen trades waren **GOOD** (MFE +1.03% tot +5.41%; MAE max 0.61%).
- **Beste read = T2 (2026-09-03 12:00, LONG, entry 67114.0):** compressie + kruipende
  closes + krimpende afstand tot de 24h-high, een vol uur vóór de break-candle en drie
  uur vóór de expansie. MFE +5.41%, MAE +0.09%. Dat moment was een **ALERT-niveau** punt
  (A4) dat een uur later tradebaar werd.
- T1 (09-02 12:00, LONG, entry 66317.5) — close-loc 100% op de niveausamenloop met de
  240m LL8; MFE +1.52%, MAE +0.34%.
- T5 (09-08 15:00, LONG, entry 67539.5) — close-loc 94%, body 80% na 4 lagere closes;
  MFE +1.49%, MAE +0.26%.
- T4 (09-04 14:00, SHORT, entry 68377.8) — displacement -2.03% met close-loc 11%;
  MFE +1.03%, MAE +0.61% → **GOOD maar LATE entry**: de candle was al -2% toen er werd
  ingestapt.
- Alerts A2, A3, A4 en A6 waren correcte reads van een gedragsverandering.

## Gemiste major moves

Drie grote dalingen werden niet getrad:

| window | move | alert vooraf | trade moment vooraf | MISS |
|---|---|---|---|---|
| 09-01 06:00 → 09-02 11:00 | −2.26% (67100 → 65902) | JA (A2) | NEE | YES |
| 09-06 18:00 → 09-08 07:00 | −2.06% (69200 → 67383, diepste 66782) | NEE | NEE | YES |
| 09-09 10:00 → 09-10 | −3.32% (68516 → 66087) | JA (A6) | NEE | YES |

**Patroon:** de alerts voor de neerwaartse bewegingen waren er (2 van 3 keer), maar er
volgde geen short-beslissing. Alleen T4 is genomen, en die kwam ná de eerste −2%-candle.

FALSE_ALERTS: A1 (nadering van de 24h-high 68236, grens brak niet) en A5 (compressie
zonder richting — terecht geen trade).

## Eindantwoord op de kernvraag

**Kan Hermes deze chart walk-forward lezen en de belangrijke trade-momenten zelfstandig
duiden? — GEDEELTELIJK.**

Wat wel kan: opwaartse momenten en rejections herkennen en er een richting aan hangen.
Wat niet kan: de **down-continuation** vertalen naar een tradebeslissing. De kaart is
asymmetrisch (3 longs + 1 late short tegenover 3 gepasseerde dalingen). Dat is geen
informatiegat — de alerts waren er — maar een **beslissingsgat**: bij een neerwaartse
richting bleef de read steken op "alert" zonder door te schuiven naar "trade".

## Open onderzoeksvraag (NIET onderzocht)

> **Waarom leiden correcte downside alerts niet tot een shortbeslissing?**

**Status: OPEN — nog niet onderzocht.** Binnen deze kaart blijft dit een open vraag;
er is geen analyse voor uitgevoerd en er is geen conclusie over getrokken.

## Wat niet is vastgelegd

De momenten zijn gelockt met `price_action`, `location` en `why|note`. De velden
`sequence`, `context_240m`, `context_60m`, `context_15m`, `indicator_confirmation` en
`invalidation` zijn in de oorspronkelijke run **niet per moment vastgelegd** en in het
rapport gemarkeerd als **NOT_RECORDED** (niet gereconstrueerd, niet ingevuld).
De unblinding (MFE/MAE en +1h…+24h) dekte uitsluitend de TRADE-momenten.

## Bronnen

- Lock: `projects/hermes-project/charts/case1-trade-moments-20260911/case1_trade_moments_lock.json`
- Rapport achteraf: `case1_trade_moments_report.md` / `.json` (zelfde map)
- Sessietranscript 2026-09-11: `raw/sessions/20260911_072042_443ae5-session.md`
  (lock-generatie ~regel 12372; eindrapport ~regel 12442-12530)

## Hard stop

Geen strategie gebouwd, geen classifier, geen thresholds getuned, geen nieuwe features,
geen L8-wijzigingen, geen merge naar main.
