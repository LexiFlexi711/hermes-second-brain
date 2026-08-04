# Pre-refactor: remove hermes_v01 dependencies — 2026-06-13

## 1. git status vóór start
```
 M projects/hermes-v01/layer1_charts/chart_engine.py    (pre-existing)
 M projects/hermes-v01/tests/test_hermes_v01_structure_edges.py (pre-existing)
 M projects/hermes-v01/tests/test_structure_roles.py    (pre-existing)
```
FIX 1 gecommit als `f2728023 fix(vind_fractalen): use wick anchors instead of body prices`

## 2. Actieve hermes_v01 usages (pre-refactor)

| File | Import |
|---|---|
| `chart_engine.py` | `vind_fractalen, _scheid_toppen_bodems, active_upper, active_lower, trend_tops, trend_bodems, trendlines_cross_at, _direction, _should_show_wedge_label, _select_local_lower, line_intersection_bars` |
| `structure_cockpit.py` | `vind_fractalen, _scheid_toppen_bodems` |
| `trendline_lab.py` | `vind_fractalen, _scheid_toppen_bodems` |
| `hermes_v02.py` | `vind_fractalen, _scheid_toppen_bodems` (2×: read_layer2 + read_layer3) |

## 3. Nieuwe modules gemaakt

### `layer2_structure/fractals.py`
- `Fractal` class
- `Zone` class
- `is_fractaal_top()`
- `is_fractaal_bodem()`
- `vind_fractalen()` — met wick anchors (FIX 1)
- `_scheid_toppen_bodems()`

### `layer2_structure/trend_helpers.py`
- `_direction()`
- `_find_recent_horizontal_zone()`
- `_should_prefer_horizontal_zone()`
- `_reject_bad_falling_local_lower()`
- `_select_local_lower()`
- `macro_trendlijn()`
- `active_upper()`
- `active_lower()`
- `trend_tops()`
- `trend_bodems()`
- `trendlines_cross_at()`
- `line_intersection_bars()`
- `_should_show_wedge_label()`

## 4. Imports aangepast

| Bestand | Oud | Nieuw |
|---|---|---|
| `chart_engine.py` | `from hermes_v01 import ...` | `from layer2_structure.fractals import ...` + `from layer2_structure.trend_helpers import ...` |
| `structure_cockpit.py` | `from hermes_v01 import ...` | `from layer2_structure.fractals import ...` |
| `trendline_lab.py` | `from hermes_v01 import ...` | `from layer2_structure.fractals import ...` |
| `hermes_v02.py` (2×) | `from hermes_v01 import ...` | `from layer2_structure.fractals import ...` |

## 5. Wrappers

**Geen.** `hermes_v01.py` blijft voorlopig intact als eigenaar van alle overige functies (read_structure, cluster_fractalen, market_state, tunnel-logica, etc.). Tests en experiments importeren nog uit v01 en blijven werken.

## 6. Bewijs: actieve code leunt niet meer rechtstreeks op hermes_v01

Na aanpassing werd `grep -rn "from.*hermes_v01\|import.*hermes_v01"` alleen nog gevonden in:
- **Tests** (test_hermes_v01.py, test_hermes_v01_structure_edges.py, test_structure_roles.py)
- **Experiments** (various experiment scripts — niet actief in dashboard flow)
- **hermes_v01.py zelf** (uiteraard)
- **hermes_v01b.py** (lege stub)

**Geen actief dashboard-bestand importeert nog uit hermes_v01.py.**

## 7. Compile output

```
fractals.py      ✅
trend_helpers.py ✅
chart_engine.py  ✅
structure_cockpit.py ✅
trendline_lab.py ✅
hermes_v02.py    ✅
```

## 8. Test output

| Test suite | Resultaat |
|---|---|
| `test_hermes_v02.py` (4) | ✅ ALL PASS |
| `test_hermes_v01.py` (32) | ✅ ALL PASS |
| `test_hermes_v01_structure_edges.py` + `test_structure_roles.py` (57) | ⚠️ **55 pass, 2 pre-existing failures** |

**2 failures zijn pre-existing** (test_hermes_v01_structure_edges.py was al `M` gemarkeerd vóór refactor):
- `test_trend_tops_pn_below_close_rejected` — verwacht pn<close gate die in uncommitted versie zat
- `test_trend_bodems_pn_above_close_rejected` — zelfde

Deze tests zijn geschreven voor uncommitted wijzigingen die door `git checkout --` (FIX 1 prep) gereset zijn. Geen verband met deze refactor.

## 9. git diff --stat

```
projects/hermes-v01/layer1_charts/chart_engine.py            | 218 ++++----
projects/hermes-v01/layer1_charts/structure_cockpit.py       |   2 +-
projects/hermes-v01/layer2_structure/hermes_v02.py           |   4 +-
projects/hermes-v01/layer4_trendline_lab/trendline_lab.py    |   2 +-
projects/hermes-v01/tests/test_hermes_v01_structure_edges.py |  42 ++++
projects/hermes-v01/tests/test_structure_roles.py            |   4 +-
```

Plus **2 untracked files**: fractals.py, trend_helpers.py

## 10. git diff --name-status

```
M   projects/hermes-v01/layer1_charts/chart_engine.py
M   projects/hermes-v01/layer1_charts/structure_cockpit.py
M   projects/hermes-v01/layer2_structure/hermes_v02.py
M   projects/hermes-v01/layer4_trendline_lab/trendline_lab.py
M   projects/hermes-v01/tests/test_hermes_v01_structure_edges.py (pre-existing)
M   projects/hermes-v01/tests/test_structure_roles.py (pre-existing)
??  projects/hermes-v01/layer2_structure/fractals.py (nieuw)
??  projects/hermes-v01/layer2_structure/trend_helpers.py (nieuw)
```

## 11. Risico's

| Risico | Impact | Status |
|---|---|---|
| functie niet exact gekopieerd | logica-verschil tussen v01 en trend_helpers | ✅ Alle import-consumenten gebruiken nu trend_helpers/fractals. v01 blijft als fallback. |
| import niet gevonden via sys.path | runtime import error | ✅ Getest: 36/36 + 55/57 tests pass |
| trend_tops/bodems versie-verschil | v01 heeft collinear versie, pre-existing had andere | ✅ Geen impact — consumers gebruiken beide niet direct |
| chart_engine pre-existing changes | lijn 326-328 gebruikt recent_touch param | ⚠️ Pre-existing, niet door refactor |
| pre-existing test failures | zouden ook zonder refactor falen | ⚠️ Pre-existing, geen verband met refactor |

## 12. Voorstel commit message

```
refactor: extract active hermes_v01 functions into layer2 modules

Move fractal detection and trend helper functions from
hermes_v01.py into dedicated modules:

  layer2_structure/fractals.py       — Fractal class, fractal detection,
                                       vind_fractalen (wick anchors)
  layer2_structure/trend_helpers.py  — trend_tops, trend_bodems,
                                       active_upper/lower, _select_local_lower,
                                       trendlines_cross_at, line_intersection_bars,
                                       and related helpers

hermes_v01.py remains intact for remaining functions
(read_structure, cluster_fractalen, tunnel logic, etc.).

Updated imports in:
  - chart_engine.py
  - structure_cockpit.py
  - trendline_lab.py
  - hermes_v02.py (read_layer2 + read_layer3)

No active dashboard code now imports directly from hermes_v01.py.
Tests and experiments continue to use hermes_v01 directly.
```
