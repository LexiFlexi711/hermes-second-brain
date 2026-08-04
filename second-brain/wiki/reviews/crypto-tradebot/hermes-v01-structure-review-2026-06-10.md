---
title: Hermes v01 Structure Review
type: review
tags: [crypto, code-review, hermes-v01, market-structure, testplan, qwen3-coder]
status: draft
created: 2026-06-10
reviewer: OLLAMA_CLOUD_CODE_WORKER (qwen3-coder:480b-cloud)
related: [hermes-v01-py]
---

# Hermes v01 — Structure Review

## Audit Hypothese

Dit is een **audit-hypothese**, geen bewezen bugrapport. De review is uitgevoerd door
OLLAMA_CLOUD_CODE_WORKER (qwen3-coder:480b-cloud) op basis van statische code-analyse.
Alle bevindingen moeten handmatig geverifieerd worden voor ze als bugs behandeld worden.

## Bestand

| Veld | Waarde |
|------|--------|
| **Pad** | `/mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/projects/hermes-v01/layer2_structure/hermes_v01.py` |
| **Grootte** | 2030 lijnen, 86KB |
| **Review datum** | 2026-06-10 |
| **Reviewer** | OLLAMA_CLOUD_CODE_WORKER |
| **Model** | `qwen3-coder:480b-cloud` |
| **prompt_eval_count** | 24.749 |
| **eval_count** | 1.026 |
| **total_duration** | 19,672s |
| **Eindoordeel** | **VOORZICHTIG** |

## 10 Reviewpunten

### 1. Wat doet het bestand?
Marktstructuurlezer voor financiële charts. Detecteert fractalen, clustert ze in
support/resistance zones, bepaalt trendlijnen (diagonaal + horizontaal) en valideert
structuur met break-status.

### 2. Kernlogica (functies/classes)
- `vind_fractalen()` — fractal detectie op candlestick data
- `cluster_fractalen()` — groepeert fractalen in S/R zones
- `bepaal_trend()` — marktrichting bepaling
- `read_structure()` — centrale orchestrator (>200 lijnen)
- `_find_outer_envelope()` — outer-envelope tunnel detectie
- `find_best_swing_line()` — multi-factor swing scoring
- `Fractal`, `Zone`, `Structuur` — dataclasses

### 3. Risico's
- Geen inputvalidatie op `candles` → crash bij incomplete/null data
- Geen logging of exceptiehandling → moeilijk debuggen in productie
- `_range_atr()` kan 0 geven → deling door nul elders
- Magic numbers zonder documentatie of context
- Geen fallback voor `pair`-afhankelijke logica

### 4. Bugs / edge cases
- `lees_structuur()` kan crashen als `candles[-1]` niet bestaat
- `_range_atr()` kan 0 returnen
- `_bepaal_structure_type()` gebruikt hardcoded epsilon i.p.v. ATR-tolerantie
- `_build_tunnel()` wisselt lijnen om zonder slope-aanpassing
- `_detect_active_window()` gebruikt vaste horizontale threshold

### 5. Structuur: goed
- Duidelijke functiescheiding, herbruikbare dataclasses met type hints
- Modulaire opbouw: fractals → zones → structuur → validatie
- Logging-velden voor audit (source, score, reason)

### 6. Structuur: zwak
- `read_structure()` >200 lijnen
- Magic numbers (5 candles, 0.15 afstand, vaste epsilon)
- Geen consistente error handling
- Demo code in productiebestand

### 7. Code die niet zonder tests mag wijzigen
- `read_structure()` — centrale logica met vele afhankelijkheden
- `_find_outer_envelope()` — complexe scoring
- `_build_tunnel()` — lijn-omwissellogica
- `find_best_swing_line()` — multi-factor scoring
- `_is_line_broken()` — break detection

### 8. Concrete verbeteringen
- Inputvalidatie toevoegen aan `read_structure()` en `_range_atr()`
- Magic numbers vervangen door benoemde constanten
- `_build_tunnel()` refactoren naar kleinere functies
- ATR-afhankelijke thresholds in `_detect_active_window()`
- Demo code verplaatsen naar apart testbestand

### 9. Eerst nodige tests
Zie testplan sectie hieronder.

### 10. Eindoordeel
**VOORZICHTIG** — goed gestructureerd en modulair, maar edge cases met crashgevaar.
Geen inputvalidatie en hardcoded thresholds maken aanpassingen riskant zonder tests.

---

## Testplan: hermes_v01.py

### Prioriteit P0 (kritisch — eerst testen)

| ID | Test | Wat | Scenario's |
|----|------|-----|------------|
| T01 | inputvalidatie candles | `read_structure()` moet None/lege lijst/onvolledige data afvangen | `None`, `[]`, `[{}]`, ontbrekende 'high'/'low' keys |
| T02 | `_range_atr()` edge cases | ATR-berekening bij extreme data | constante prijs (ATR=0), 1 candle, 2 candles, NaN/Inf in data |
| T03 | `_is_line_broken()` | Break detection | candle ver boven lijn, ver onder, raakt exact, meerdere candles na break, valse break (wick only) |
| T04 | `_build_tunnel()` crossing/swap | Lijnen omwisselen zonder slope-aanpassing | parallelle lijnen die kruisen, slope verschil klein/groot |
| T05 | `read_structure()` integratietest | Volledige structuurscan met bekende dataset | vergelijk output met handmatig geëtiketteerde chart data |

### Prioriteit P1 (belangrijk — onderzoek voor aanpassingen)

| ID | Taak | Wat |
|----|------|-----|
| T06 | Magic numbers inventariseren | Alle hardcoded getallen (5, 0.15, epsilon, vaste thresholds) identificeren en documenteren |
| T07 | ATR-afhankelijke thresholds | Vervang vaste thresholds door ATR-afhankelijke varianten in `_detect_active_window()` en `_bepaal_structure_type()` |
| T08 | Demo-code lokaliseren | Demo/example code in productiebestand vinden en verplaatsen naar apart test/example bestand |

### Boundary conditions per functie

| Functie | Input | Expected behavior |
|---------|-------|-------------------|
| `vind_fractalen()` | 0-1 candles | graceful degrade of lege output |
| `cluster_fractalen()` | 0 zones | lege cluster output |
| `bepaal_trend()` | allemaal gelijke prijzen | neutraal / geen trend |
| `_find_outer_envelope()` | 1-2 swing lines | minimum 2 lijnen nodig |
| `find_best_swing_line()` | 0 kandidaten | graceful degrade |

### Testverbod
- **Geen tests schrijven** in deze fase
- **Geen code wijzigen**
- Dit testplan is een blauwdruk voor een volgende fase
