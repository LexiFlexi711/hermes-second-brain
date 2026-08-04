---
type: fix
date: 2026-06-07
status: DONE
title: "FASE 1C — outer-envelope tunnel scorer v1-v5 afgekeurd"
tags: [hermes-v01, outer-envelope, tunnel, structure-detection, compression, range]
---

# FASE 1C — outer-envelope tunnel scorer v1-v5

## Context

5 iteraties ontwikkeld om `_build_tunnel()` te laten werken met `_find_outer_envelope()` voor structuurdetectie (compression/range) op 60m candles.

## Wat er misliep

- **active/context structure mixing**: `active_structure` en `context_structure` logica werd door elkaar gebruikt in chart visualisatie
- **upper <= lower niet afgedwongen**: na swap kon width_atr negatief worden
- **inside_ratio over verkeerd venster**: gebruikte `recent_start` ipv vaste 36-bar window
- **Chart lijnen klopten niet**: upper/lower kleurconventie inconsistent
- Data plumbing bleef fouten geven na elke fix

## Fixes die wél werkten (v5)

1. **SOLEUR width_atr fixed**: na swap werd width_atr niet herberekend → opgelost
2. **inside_ratio 36-bar window**: in range- en compression-pad gefixt op vaste 36 bars
3. **BTCEUR 60m werd `valid=True`** voor het eerst — compression, 97% inside, price at upper_middle
4. **validate_v5.py** charts gegenereerd voor BTCEUR, ETHEUR, SOLEUR, ADAEUR

## Resultaat v5

| Pair | Type | Width | Inside | Valid |
|------|------|-------|--------|-------|
| BTCEUR | compression | 4.45 | 0.97 | ✅ True |
| ETHEUR | compression | 1.97 | 0.32 | ❌ inside_ratio te laag |
| SOLEUR | compression | 6.12 | 0.00 | ❌ inside_ratio te laag |
| ADAEUR | range | 9.15 | 1.00 | ❌ tunnel te breed |

## Lexi's verdict (7 juni)

**"sla je geheugen maar op, ik ben genoeg teleurgesteld"** — FASE 1C afgekeurd na v5.

## Volgende stap

Herstarten met schone `read_structure()` die:
- `active_structure` en `context_structure` strikt scheidt
- `upper > lower` garandeert
- enkel 36-bar inside_window gebruikt
- correcte kleurconventie: upper=blauw, lower=groen