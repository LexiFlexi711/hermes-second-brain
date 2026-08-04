"""Generate structure label reports."""
import sys, os
sys.path.insert(0, '/mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/projects/hermes-v01')
from layer4_trendline_lab.trendline_lab import (
    fetch_and_prepare, calculate_median_range,
    classify_swing_high_structure, classify_swing_low_structure
)
from collections import Counter

tfs = [(240, '240m'), (60, '60m'), (15, '15m'), (5, '5m')]
for iv, tf in tfs:
    c, sh, sl, di = fetch_and_prepare('BTCEUR', tf, iv)
    mr = calculate_median_range(c)
    tol = mr * 0.5
    hc = classify_swing_high_structure(sh, c)
    lc = classify_swing_low_structure(sl, c)
    lines = []
    lines.append(f"Layer 4 Structure — BTCEUR {tf}")
    lines.append("=" * 60)
    lines.append(f"Candles: {di['candle_count']}  Swing highs: {di['swing_highs_count']}  Swing lows: {di['swing_lows_count']}")
    lines.append(f"Median range: {mr:.2f}  Tolerance (50%): {tol:.2f}")
    lines.append("")
    lines.append("── HIGH SEQUENCE ──")
    lines.append(f"{'idx':<5} {'wick':<12} {'delta':<12} {'label':<14}")
    lines.append("-" * 45)
    for h in hc:
        lines.append(f"{h['index']:<5} {h['wick_price']:<12.2f} {h['delta_from_prev']:<+11.2f} {h['display_label']:<14}")
    lines.append("")
    hcc = Counter(h['structure_label'] for h in hc)
    lines.append(f"Highs: {dict(hcc)}")
    lines.append("")
    lines.append("── LOW SEQUENCE ──")
    lines.append(f"{'idx':<5} {'wick':<12} {'delta':<12} {'label':<14}")
    lines.append("-" * 45)
    for lo in lc:
        lines.append(f"{lo['index']:<5} {lo['wick_price']:<12.2f} {lo['delta_from_prev']:<+11.2f} {lo['display_label']:<14}")
    lines.append("")
    lcc = Counter(lo['structure_label'] for lo in lc)
    lines.append(f"Lows: {dict(lcc)}")
    p = f"/home/sjoe/system/hermes-second-brain/tasks/layer4_structure_labels_BTCEUR_{tf}.txt"
    with open(p, 'w') as f:
        f.write('\n'.join(lines))
    print(f"✅ {p}")
    print(f"BTCEUR {tf}: highs={len(hc)} {dict(hcc)}  lows={len(lc)} {dict(lcc)}")
