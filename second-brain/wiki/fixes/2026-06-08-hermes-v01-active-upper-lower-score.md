---
title: Hermes v01 — active_upper/lower score-based rewrite
type: fix
date: 2026-06-08
status: UNCOMMITTED
---

# Hermes v01 — active_upper / active_lower score-based (2026-06-08)

## Status

**Niet gecommit.** Wijziging staat als unstaged in `projects/hermes-v01/hermes_v01.py`.

## Wat er veranderd is

`active_upper()` en `active_lower()` in `hermes_v01.py`:

**Oud:** eerste dalende top-paar dat voldoet aan condities wordt teruggegeven ("eerste gevonden").  
**Nieuw:** alle kandidaten scoren, beste wint ("score-based selectie").

## Score-formule

```
score = touches * 100.0 - dp * 10.0 + slope_bonus + recency_bonus
```

| Component | Waarde | Reden |
|-----------|--------|-------|
| `touches * 100` | dominant | meer fractalen op lijn = sterkere zone |
| `dp * 10` | straf | ver van huidige prijs = minder relevant |
| `slope_bonus` | +25.0 als slope < 0 | dalende lijn = betere weerstand |
| `recency_bonus` | max(0, 20 - recency × 0.05) | recenter paar scoort beter |

Nieuwe parameter: `touch_pct: float = 0.45` — tolerantie voor "op de lijn" bij touch-telling.

## Aanleiding

Structuur-audit (zie [[hermes-v01-structuur-audit]]) wees uit dat de eerste-gevonden aanpak
willekeurig de verkeerde lijn kon teruggeven. Score-based geeft de meest valide S/R-lijn.

## Volgende stap

Visueel valideren op referentie-charts (BTCEUR/ETHEUR/SOLEUR/ADAEUR) en committen als output klopt.
