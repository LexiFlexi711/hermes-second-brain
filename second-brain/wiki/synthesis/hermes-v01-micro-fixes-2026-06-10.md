---
title: Hermes v01 — micro-fixes sprint (juni 2026)
type: synthesis
tags: [hermes, v01, micro-fix, local-lines, wedge, horizontal-zone, falling-local-lower]
status: final
created: 2026-06-10
commits:
  - ecc8f56c: Fix Hermes lookback inference and recent range break status
  - a5eacfda: Prefer recent horizontal zones for Hermes local lines
  - 3f133665: Hide stale Hermes wedge labels
  - 5d853a9a: Reject bad falling Hermes local lower lines
---

# Hermes v01 micro-fixes

## Overzicht

Vier micro-fixes op main na `d4acaf44` (merge hermes line tuning candidate).
+596 / -31 lijnen over 3 bestanden. Tests: 51 → 74.

## 1. Lookback + recent_range break-status (`ecc8f56c`)

**Probleem:** `_infer_lookback_bars()` gebruikte totale tijdspanne i.p.v. gemiddelde candleduur. Recent_range in `_build_tunnel()` overschreef projected_now maar niet de break-status.

**Fix:**
- `_infer_lookback_bars()`: `candle_interval = total_seconds / (len(candles) - 1)` i.p.v. `total_seconds / 1`
- `_build_tunnel()`: `using_recent_range` flag + break-status gebruikt horizontale lijnen bij recente range

## 2. Horizontale zones voor local lines (`a5eacfda`)

**Probleem:** Hermes forceerde diagonale local upper/lower, zelfs als een horizontale zone beter paste.

**Nieuwe helpers:**
- `_find_recent_horizontal_zone(fractals, close, side, ...)` — clustert fractals op prijs, kiest cluster met meeste touches dicht bij close
- `_should_prefer_horizontal_zone(horizontal, diagonal, close)` — beslist of horizontale zone wint op basis van touches, afstand, en 4% guard

**Gedrag:**
- Horizontale zone wint bij meer touches, of gelijke touches + dichter bij close (≥0.25%punt), of diagonale >4% weg
- y1/y2 = avg_price, source = "recent_horizontal_zone"
- Side-role check: upper ≥ close×0.98, lower ≤ close×1.02

## 3. Wedge-label relevantie (`3f133665`)

**Probleem:** Oude/historische kruising van major lijnen kreeg wedge-label.

**Nieuwe helper:** `_should_show_wedge_label(x_cross, last_i, chart_span, min_fraction=0.25)`
- Wedge-label alleen in laatste 25% van chart
- Toekomstige kruising ≤8 bars
- Geen label diep in verleden

## 4. Local lower direction gate (`5d853a9a`)

**Probleem:** Dalende oranje local lower getekend zonder echt dalende bodems.

**Nieuwe helpers:**
- `_reject_bad_falling_local_lower(local_lower, bodems, close, last_index)` — verwerpt dalende lijn bij vlakke bodems, projected_now >2% weg, of touches <3
- `_select_local_lower(bodems, close, last_index)` — centrale selector: combineert active_lower + horizontale zone + falling gate

**Split-brain opgelost:** Zowel `structure_roles()` als `chart_engine.py` gebruiken `_select_local_lower()`.

## Architectuur

```
_select_local_lower()          # centrale local lower selector
├── active_lower()             # diagonale/local line
├── _find_recent_horizontal_zone()  # horizontale zone
├── _should_prefer_horizontal_zone()  # quality gate
└── _reject_bad_falling_local_lower()  # direction gate
    ├── bodems dalend check
    ├── distance_pct ≤ 2.0
    └── touches ≥ 3
```

## Tests

- `test_hermes_v01_structure_edges.py`: edge cases voor alle nieuwe helpers
- `test_structure_roles.py`: role-based integratietests
- Test count: 74 (was 51 bij merge)

## Open TODO

- `_direction` schaalbewustzijn (`eps=1e-9`)
- `body_cross_count` naam vs wick/range duplicatie
- `_bepaal_structure_type` / `_classify_tunnel_structure` duplicatie
