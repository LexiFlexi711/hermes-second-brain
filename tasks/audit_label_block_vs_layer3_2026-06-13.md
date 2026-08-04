# Audit — label_block.py vs Layer 3 labels

**Datum:** 2026-06-13
**Status:** Geen code gewijzigd

---

## 1. Wat doet label_block.py?

- **Locatie:** `layer2_structure_v2/label_block.py` (121 lijnen)
- **Functie:** `draw_labels()` — tekent U/D/R labels op chart
- **Algoritme:** Structurele richting obv pivot-prijzen:
  - Stap 1: individuele segmenten labelen (U/D/R) op prijsverschil
  - Stap 2: major pivots vinden (> major_pct move)
  - Stap 3: R-segmenten overschrijven obv omliggende major pivot richting
  - Stap 4: counter-trend U's/D's corrigeren tussen major pivots
  - Stap 5: chop detectie op einde (kleine schommelingen = R)
- **Config:** Hardcoded per TF in de functie (`major_pct`, `cmax`)

## 2. Wat doet layer3_phase/layer3_label.py?

- **Locatie:** `layer3_phase/layer3_label.py` (487 lijnen)
- **Functies:** `label_phases()`, `draw_layer3_labels()`
- **Algoritme:** Box-based range detectie in 4 fasen:
  - Fase 1: raw slope labels (U/D/R)
  - Fase 2: compress opeenvolgendezelfde letters
  - Fase 3: horizontale box range detectie (min candles, pivots, drift)
  - Fase 4: chart labels
- **Config:** Aparte `layer3_config.py` — per TF aanpasbaar

## 3. Wie gebruikt label_block?

| File | Regel | Actief? |
|---|---|---|
| `chart_engine.py` | 296-297 | Alleen bij `show_labels=True` — **nooit True in dashboard routes** |

`show_labels` staat in `chart_engine.py` als `build_chart()` parameter (default `False`).  
Geen enkele dashboard route zet `show_labels=True`.

## 4. Wie gebruikt Layer 3 labels?

| File | Actief? |
|---|---|
| `structure_cockpit.py` (V5) | ✅ Ja — `draw_layer3_labels()` |
| `director/hermes_director.py` | ✅ Ja — `read_layer3()` |
| `chart_engine.py` (v2 mode) | ✅ Ja — `show_layer3_labels=True` in `/v2/major-trend/` routes |

## 5. Vergelijking

| Aspect | label_block (L2-v02) | Layer 3 |
|---|---|---|
| Aanpak | Pivot-richting + major pivot context | Box range + slope + compressie |
| Resistentie tegen ruis | Matig (enkel major pivot filter) | Hoog (4 fasen, range detectie) |
| Config | Hardcoded | Aparte config file |
| Testbaarheid | Geen tests | Baselines (b40c58f6) |
| Actief in dashboard | ❌ Nooit | ✅ Structureel |
| Output format | Enkel U/D/R per segment | U/D/R + range candidates + compressie |

## 6. Conclusie

**label_block.py is een legacy visual helper, geen actieve concurrent van Layer 3.**

- Actief? **Nee** — `show_labels` is nooit True in enige dashboard route
- Bereikbaar via route? **Nee**
- Duplicate met Layer 3? **Conceptueel ja** — beide doen U/D/R labeling, maar Layer 3 is complexer, beter, en actief
- Risico bij beide actief? **Geen** — label_block wordt nooit aangezet

**Advies:**
- Behouden op huidige plek voor nu (geen dode code verplaatsen zonder aparte opdracht)
- Label als `UNCLEAR_ACTIVE` — kan later naar dead_code
- Geen productierisico
- Layer 3 is de enige U/D/R bron voor testbot/tradebot
