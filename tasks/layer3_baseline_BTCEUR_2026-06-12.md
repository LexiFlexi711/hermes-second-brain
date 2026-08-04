# Layer 3 baseline — BTCEUR — 2026-06-12

Status: approved baseline

## Scope

* file: projects/hermes-v01/layer2_structure_v2/layer3_label.py
* Layer 2 unchanged
* S/R unchanged
* purple middle line unchanged
* chart_engine.py unchanged

## Approved behavior

* strict slope for raw U/D (delta_price > 0 = U, < 0 = D, mini_flat = R)
* no label_tol for chartlabels
* same-direction compression (U+U = 1 U label on chart)
* range requires horizontal box validation
* 240m/60m range minimum 5 closed candles
* 15m/5m range minimum 7 closed candles
* range min 4 pivots, upper/lower drift check, netto/box ratio check
* rising/falling channel rejected as range
* staircase rejected as range (netto_box_ratio > 2.0)
* flat_raw single R debug-only, not on chart
* clean cockpit preferred

## BTCEUR visual approval

* 240m: OK — no fake R, clean U/D
* 60m: OK — no fake R
* 15m: OK — 1 confirmed horizontal box R, U segment #26 (+1.01%) preserved
* 5m: OK — staircase down rejected, last spike U preserved

## Known next validation

* ETH/EUR
* SOL/EUR
* ADA/EUR

## Rule

Do not change Layer 3 logic unless another pair proves a real failure.
