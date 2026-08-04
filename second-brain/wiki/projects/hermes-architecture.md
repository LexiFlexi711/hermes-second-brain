# Hermes Architectuur — 2026-06-12

## Overzicht
Hermes is een chart/structure-engine voor crypto marktanalyse, opgedeeld in aparte layers.

```
projects/hermes-v01/
├── layer1_charts/           # Dashboard + chart rendering + data fetch
│   ├── app_dashboard.py     # Flask app, alle routes
│   └── chart_engine.py      # build_chart(), fetch_kraken()
├── layer2_structure/        # Legacy layer (hermes_v01) + orchestrator
│   ├── hermes_v01.py        # Layer 1: fractals, trendlines, zones (legacy)
│   ├── hermes_v02.py        # ORCHESTRATOR / FACADE — roept alle layers aan
│   └── hermes_v01_backup_20260610.py
├── layer2_structure_v2/     # Layer 2: swing points, S/R, purper lijn, D/U/R
│   ├── swing_points.py      # swing high/low detectie (SwingPoint dataclass)
│   ├── pivot_utils.py       # compute_pivots()
│   ├── label_block.py       # draw_labels()
│   ├── trendline_block.py   # draw_trendline() (purper middle lijn)
│   ├── sr_block.py          # draw_sr_zones() (S/R levels)
│   ├── zone_block.py        # draw_pivot_rays()
│   ├── marker_block.py      # draw_markers()
│   ├── layer3_label.py      # Layer 3: D/U/R + range detectie
│   └── layer3_config.py     # Config per timeframe
├── layer3_chart_story/      # Chart story reader + export
│   ├── story_reader.py      # read_chart_story()
│   ├── story_models.py      # ChartSnapshot, ChartStory, LineSnapshot
│   ├── story_repository.py  # read_pair_story()
│   ├── story_presenter.py   # present_story_payload()
│   └── ...
├── layer4_trendline_lab/    # Layer 4: structure marking + trendlines
│   └── trendline_lab.py     # Upper/lower TL + HH/HL/LH/LL/EH/EL labels
├── tests/
└── experiments/
```

## Layer verantwoordelijkheden
- **Layer 1**: Data ophalen, chart renderen, dashboard routes
- **Layer 2**: Fractals, swing points, S/R, purper middle lijn
- **Layer 3**: D/U/R labels, range detectie (box-based), compressie
- **Layer 4**: Trendline lab (upper/lower), structuur labels (HH/HL/LH/LL/EH/EL)
- **Orchestrator** (hermes_v02.py): Roept alle layers aan via read_layer1/2/3/4(), read_structure(), read_mtf_structure()

## Belangrijke commits
- b40c58f6 — Layer 3 range detection baseline
- 482794ac — Layer 3 config extract (layer3_config.py)
- f84d5f70 — sr_block: filter out-of-window S/R levels
- 91e24243 — Layer 4 trendline lab + structure marking

## Bekende dode bestanden (niemand importeert ze)
- hermes_v01b.py (1.3KB)
- app.py (1.6KB — vervangen door app_dashboard.py)
- swing_highs.py (5KB — vervangen door swing_points.py)
- hermes_v02.py is GEEN dode code — het is de orchestrator

## Dashboard routes
- /v2/sr/<pair> — MTF cockpit met S/R, Layer 3 labels, paarse lijn
- /v4/trendline-lab/<pair>/<tf> — Layer 4 trendlines + structuur labels
- /v2/<pair> — lege MTF cockpit
- /v2/swings/<pair> — swing points
- /v2/major-trend/<pair> — major trend
