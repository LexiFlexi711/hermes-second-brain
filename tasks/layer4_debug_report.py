"""Generate debug reports for Layer 4 Trendline Lab."""
import sys, os, json
HERMES = "/mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/projects/hermes-v01"
for p in [os.path.join(HERMES, "layer1_charts"), os.path.join(HERMES, "layer2_structure"), os.path.join(HERMES, "layer2_structure_v2"), HERMES]:
    sys.path.insert(0, p)
from chart_engine import fetch_kraken
from hermes_v01 import vind_fractalen, _scheid_toppen_bodems
from layer2_structure_v2.swing_points import detect_swing_highs
from layer4_trendline_lab.trendline_lab import (
    fetch_and_prepare, inspect_swing_strengths, select_upper_points,
    generate_upper_candidates, validate_upper_candidate, pick_top_upper_candidates
)

pair = "BTCEUR"
tfs = [(240, "240m"), (60, "60m"), (15, "15m"), (5, "5m")]

for interval_min, tf_label in tfs:
    candles, swing_highs, debug_info = fetch_and_prepare(pair, tf_label, interval_min)
    strength_info = inspect_swing_strengths(swing_highs)
    points = select_upper_points(swing_highs, candles)
    candidates = generate_upper_candidates(points)
    validated = [{**c, **validate_upper_candidate(c, candles)} for c in candidates]
    top = pick_top_upper_candidates(validated)

    report = []
    report.append(f"Layer 4 Trendline Lab — {pair} {tf_label}")
    report.append(f"{'='*60}")
    report.append(f"")
    report.append(f"Candles: {debug_info['candle_count']}")
    report.append(f"Fractalen: {debug_info['fractalen_count']}")
    report.append(f"Toppen: {debug_info['toppen_count']}")
    report.append(f"Swing highs: {debug_info['swing_highs_count']}")
    report.append(f"")
    report.append(f"Strength inspectie:")
    for k, v in strength_info.items():
        report.append(f"  {k}: {v}")
    report.append(f"")
    report.append(f"Geselecteerde upper points ({len(points)}):")
    for p in points:
        report.append(f"  idx={p['index']:3d}  strength={p['strength']:.3f}  wick={p['wick_price']:.1f}  body={p['body_price']:.1f}")
    report.append(f"")
    report.append(f"Upper candidates: {len(candidates)}")
    valid_cnt = sum(1 for c in validated if c.get('valid', False))
    report.append(f"Valid candidates: {valid_cnt}/{len(validated)}")
    report.append(f"")
    report.append(f"Top candidates:")
    for i, t in enumerate(top):
        report.append(f"  #{i+1}: p1={t['p1_index']} p2={t['p2_index']} slope={t['slope']:.6f} touches={t['touch_count']} breaches={t['breaches_above']} cuts={t['cuts_through_bodies']} conf={t['confidence']} valid={t.get('valid','?')}")
    report.append(f"")
    if valid_cnt == 0:
        report.append(f"WAARSCHUWING: Geen valide upper kandidaten")
        for c in validated:
            report.append(f"  rejected: p1={c['p1_index']} p2={c['p2_index']} touches={c['touch_count']} breaches={c['breaches_above']}")

    path = f"/home/sjoe/system/hermes-second-brain/tasks/layer4_trendline_lab_{pair}_{tf_label}.txt"
    with open(path, "w") as f:
        f.write("\n".join(report))
    print(f"✅ {path}")
    print("\n".join(report))
    print()
