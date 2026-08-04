---
type: decision
title: structure_roles horizontal zone substitution is non-production known debt
status: parked
created: 2026-06-11
tags: [hermes-v01, structure-roles, horizontal-zone, truth-split, known-debt]
related:
  - fix/layer2-major-upper-pre-anchor-fix
  - fix/layer2-active-upper-full-candidate-comparison
  - fix/layer2-body-extremes-for-fractal-prices
  - fix/layer1-sr-level-neutral-gray
---

# structure_roles horizontal zone substitution is non-production known debt

## Probleem

`structure_roles()` in `layer2_structure/hermes_v01.py` bevat een horizontale
zone substitutie (`_should_prefer_horizontal_zone()`) die de diagonale
`local_upper` van `active_upper()` kan vervangen door een vlakke horizontale
zone uit `_find_recent_horizontal_zone()`.

Dit creëert een potentiële truth split:
- chart toont diagonale `active_upper()` (via `chart_engine.py`)
- `structure_roles()` kan horizontale zone teruggeven in `local_upper`

## Consumer-audit resultaat

| Component | Gebruikt `structure_roles()`? | Gebruikt `active_upper()` direct? |
|-----------|-------------------------------|-----------------------------------|
| chart_engine (chart PNG) | Nee | Ja — lijn 241 |
| app_dashboard (HTTP) | Nee (importeert niet) | Ja — via chart_engine |
| read_structure() / build_tunnel | Nee | Ja — aparte cascade (lijn 1335) |
| tradebot scripts | Nee (0 refs) | — |
| tradebot agents | Nee (0 refs) | — |
| crypto-data | Nee (0 refs) | — |
| Layer 3 sidecar | Bestaat niet meer | — |
| experimenten | Nee | Ja (2 experimenten) |
| test suite | Ja — 2 calls | Ja — 2 calls |

**Conclusie:** `structure_roles()` wordt enkel in de test suite geconsumeerd
(2 test calls in `test_hermes_v01_structure_edges.py`). Geen enkele
productiecomponent gebruikt de `structure_roles()` output.

## Huidige productie truth

```
chart_engine.py → active_upper() direct → diagonale local_upper (blauw)
                 ↓
            chart PNG op dashboard
```

`structure_roles()` output heeft géén effect op chart, dashboard, tradebot,
of Layer 3. Vandaag geen actieve truth split.

## Waarschuwing

**Do not use `structure_roles().local_upper` as production truth without
resolving horizontal-zone substitution vs chart `active_upper()` semantics.**

Als `structure_roles()` in de toekomst een productie-consumer krijgt (bv.
tradebot, Layer 3 sidecar, of een nieuwe API), moet de horizontale zone
substitutie opnieuw beoordeeld worden:
- verwijderen (enkel diagonale local_upper gebruiken)
- of expliciet harmoniseren met chart-engine semantiek
- of een apart veld toevoegen voor "best horizontal zone" naast local_upper

## Bewijs

Consumer-audit uitgevoerd via `git grep` en bestandsinspectie op 2026-06-11.

Relevante bestanden en regelnummers:
- `layer2_structure/hermes_v01.py` lijn 536-564: `_should_prefer_horizontal_zone()`
- `layer2_structure/hermes_v01.py` lijn 662-665: substitutie in `structure_roles()`
- `layer2_structure/hermes_v01.py` lijn 700: `local_upper` in return dict
- `layer1_charts/chart_engine.py` lijn 241: `active_upper()` direct
- `tests/test_hermes_v01_structure_edges.py` lijn 366, 570: `structure_roles()` tests

Relevante commits in deze sessie:
- `3456e460` — major_upper pre-anchor touches excluded (Mechanism 1)
- `8dd0cd06` — S/R level color to neutral gray
- `d98ada13` — active_upper full candidate comparison
- `dfa9626f` — body extremes for structure fractal prices
