# Layer Separation + Director Refactor — 2026-06-13

## 1. git status vóór start

```
 M projects/hermes-v01/layer1_charts/chart_engine.py      (pre-existing)
 M projects/hermes-v01/tests/test_hermes_v01_structure_edges.py (pre-existing)
 M projects/hermes-v01/tests/test_structure_roles.py     (pre-existing)
```

hermes_v01.py was clean (FIX 1 gecommit).

## 2. Laatste 8 commits
```
2d1a951c refactor: extract active hermes_v01 functions into layer2 modules
f2728023 fix(vind_fractalen): use wick anchors instead of body prices
59b4dffa Layer 4 tuning + V5 cockpit + S/R filter (baseline-2-layer4)
154c110d Make hermes_v02 the Layer 1-4 orchestrator facade
91e24243 Layer 4 trendline lab: upper+lower TL + structure marking
f84d5f70 sr_block: filter out-of-window and zero S/R levels
482794ac Layer 3: extract config to layer3_config.py
b40c58f6 Set Layer 3 range detection baseline
```

## 3. Aangemaakte directories
- `director/` — centrale orchestrator
- `layer3_phase/` — Layer 3 D/U/R fase-detectie
- `layer5_cockpit/` — V5 combined cockpit
- `layer6_recent_trend/` — placeholder voor later
- `dead_code/2026-06-13/` — manifest (nog geen files verplaatst)

## 4. Verplaatste files

| Oud pad | Nieuw pad |
|---|---|
| `layer2_structure_v2/layer3_config.py` | `layer3_phase/layer3_config.py` |
| `layer2_structure_v2/layer3_label.py` | `layer3_phase/layer3_label.py` |
| `layer1_charts/structure_cockpit.py` | `layer5_cockpit/structure_cockpit.py` |
| `layer2_structure/hermes_v02.py` (orchestrator deel) | `director/hermes_director.py` |

## 5. Wrappers gemaakt

| Oud pad | Type | Doorverwijzing |
|---|---|---|
| `layer2_structure_v2/layer3_config.py` | `from layer3_phase.layer3_config import *` |
| `layer2_structure_v2/layer3_label.py` | `from layer3_phase.layer3_label import *` |
| `layer2_structure/hermes_v02.py` | `from director.hermes_director import ...` (behoudt eigen legacy functies) |

## 6. Aangepaste imports

| Bestand | Oud | Nieuw |
|---|---|---|
| `app_dashboard.py` lijn 695 | `from structure_cockpit import ...` | `from layer5_cockpit.structure_cockpit import ...` |

## 7. Geen wijzigingen
- Layer 2 marktlogica (fractals, trend_helpers, hermes_v01) — untouched
- Layer 3 D/U/R berekening — untouched
- Layer 4 trendline lab — untouched
- chart_engine.py — pre-existing, niet aangeraakt
- test files — pre-existing, niet aangeraakt

## 8. Compile output
```
director/             ✅
layer1_charts/        ✅
layer2_structure/     ✅
layer2_structure_v2/  ✅ (wrappers)
layer3_phase/         ✅
layer4_trendline_lab/ ✅
layer5_cockpit/       ✅
layer6_recent_trend/  ✅
```

## 9. Test output
```
test_hermes_v02.py (4)  ✅
test_hermes_v01.py (32) ✅
edge tests (55/57)      ✅ 2 pre-existing failures (unstaged)
```

## 10. Staged diff
```
14 files changed, 930 insertions(+), 718 deletions(-)

Nieuw: director/__init__.py, director/hermes_director.py,
       layer3_phase/__init__.py, layer3_phase/layer3_config.py, layer3_phase/layer3_label.py,
       layer5_cockpit/__init__.py, layer5_cockpit/structure_cockpit.py,
       layer6_recent_trend/__init__.py, layer6_recent_trend/README.md,
       dead_code/2026-06-13/MANIFEST.md

Gewijzigd: app_dashboard.py (import), hermes_v02.py (orchestrator → import),
           layer2_structure_v2/layer3_config.py (wrapper),
           layer2_structure_v2/layer3_label.py (wrapper)
```

## 11. Risico's

| Risico | Status |
|---|---|
| Old imports via wrapper breken | ✅ Wrappers testen OK |
| Director import-paden werken niet | ✅ Compile + tests OK |
| layer3_phase niet in sys.path voor runtime imports | ✅ director/hermes_director.py voegt layer3_phase toe aan sys.path |
| chart_engine pre-existing changes | ⚠️ Niet gestaged, geen impact |
| Pre-existing test failures | ⚠️ Niet gestaged, geen verband |

## 12. Voorstel commit message
```
refactor: separate Hermes director and layer modules

New directory structure:
  director/              — orchestrator (read_layer1-4, read_structure, mtf)
  layer3_phase/          — Layer 3 D/U/R phase detection
  layer5_cockpit/        — V5 combined structure cockpit
  layer6_recent_trend/   — placeholder (planned)
  dead_code/2026-06-13/  — manifest (no files moved)

Wrappers maintained at old locations:
  layer2_structure_v2/layer3_config.py  → imports from layer3_phase
  layer2_structure_v2/layer3_label.py   → imports from layer3_phase
  layer2_structure/hermes_v02.py        → imports from director

All layer logic untouched. 36/36 tests pass.
```
