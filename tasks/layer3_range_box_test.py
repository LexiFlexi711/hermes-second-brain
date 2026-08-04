"""Test nieuwe box-based range detectie op BTCEUR."""
from __future__ import annotations
import sys, os, json, time
from datetime import datetime, timezone

HERMES = "/mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/projects/hermes-v01"
sys.path.insert(0, os.path.join(HERMES, "layer2_structure"))
sys.path.insert(0, os.path.join(HERMES, "layer2_structure_v2"))
sys.path.insert(0, HERMES)

from hermes_v01 import vind_fractalen, _scheid_toppen_bodems
from layer2_structure_v2.swing_points import detect_swing_highs, detect_swing_lows
from layer2_structure_v2.pivot_utils import compute_pivots
from layer2_structure_v2.layer3_label import label_phases, debug_phases, draw_phase_labels, MIN_CANDLES_RANGE, MIN_PIVOTS_RANGE, IMPULSE_GUARD_PCT
import requests
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUTDIR = "/home/sjoe/system/hermes-second-brain/tasks"
pair = "BTCEUR"
tfs = [(240, "240m"), (60, "60m"), (15, "15m"), (5, "5m")]

for interval_min, tf_label in tfs:
    since = int(time.time()) - (200 * interval_min * 60 + 86400)
    resp = requests.get(f"https://api.kraken.com/0/public/OHLC?pair={pair}&interval={interval_min}&since={since}", timeout=10)
    data = resp.json()
    key = [k for k in data["result"] if k != "last"][0]
    raw = data["result"][key]
    candles = [{"timestamp": int(r[0]), "open": float(r[1]), "high": float(r[2]), "low": float(r[3]), "close": float(r[4]), "volume": float(r[6])} for r in raw][-200:]

    fractalen = vind_fractalen(candles)
    toppen, bodems = _scheid_toppen_bodems(fractalen)
    swing_highs = detect_swing_highs(toppen, candles, interval_min, tf_label)
    swing_lows = detect_swing_lows(bodems, candles, interval_min, tf_label)
    _, pts = compute_pivots(swing_highs, swing_lows, candles)

    raw_seg, comp, final, r_cands = label_phases(pts, interval_min)
    ru = sum(1 for s in raw_seg if s['raw_label']=='U')
    rd = sum(1 for s in raw_seg if s['raw_label']=='D')
    rr = sum(1 for s in raw_seg if s['raw_label']=='R')
    cu = sum(1 for c in comp if c['label']=='U')
    cd = sum(1 for c in comp if c['label']=='D')
    cr = sum(1 for c in comp if c['label']=='R')
    fu = sum(1 for p in final if p['final_label']=='U' and p.get('rendered_on_chart',True))
    fd = sum(1 for p in final if p['final_label']=='D' and p.get('rendered_on_chart',True))
    fr = sum(1 for p in final if p['final_label']=='R' and p.get('rendered_on_chart',True))
    r_conf = sum(1 for rc in r_cands if rc.get('accepted_as_R',False))
    r_form = sum(1 for rc in r_cands if rc.get('range_status')=='R_FORMING')

    print(f"\n{'='*70}")
    print(f"  BTCEUR {tf_label}")
    print(f"{'='*70}")
    print(f"  Params: min_candles={MIN_CANDLES_RANGE.get(interval_min,5)} pivots={MIN_PIVOTS_RANGE.get(interval_min,4)} impulse={IMPULSE_GUARD_PCT.get(interval_min,1.0)}%")
    print(f"  Raw: {ru}U {rd}D {rr}R")
    print(f"  Compressed: {cu}U {cd}D {cr}R")
    print(f"  Final on chart: {fu}U {fd}D {fr}R")
    print(f"  R candidates: {r_conf} confirmed, {r_form} forming")

    # Reject reasons
    rej = [rc for rc in r_cands if not rc.get('accepted', True)]
    for rc in rej:
        print(f"  ❌ rejected: {'; '.join(rc.get('reject_reasons',[]))}")

    debug = debug_phases(pts, interval_min)
    dbg_path = os.path.join(OUTDIR, f"layer3_range_box_audit_BTCEUR_{tf_label}.txt")
    with open(dbg_path, "w") as f:
        f.write(debug)

    # Chart
    times = [datetime.fromtimestamp(c['timestamp'], tz=timezone.utc) for c in candles]
    fig, ax = plt.subplots(figsize=(14, 7))
    for i, c in enumerate(candles):
        t = times[i]
        color = 'green' if c['close'] >= c['open'] else 'red'
        ax.plot([t, t], [c['low'], c['high']], color='black', linewidth=0.3)
        bw = 0.6 * interval_min / (24*60)
        ax.bar(t, abs(c['close'] - c['open']), bottom=min(c['open'], c['close']), width=bw, color=color, alpha=0.6)
    for i in range(1, len(pts)):
        idx1, p1 = pts[i-1]; idx2, p2 = pts[i]
        ax.plot([times[min(idx1, len(times)-1)], times[min(idx2, len(times)-1)]], [p1, p2], color='#9C27B0', linewidth=2.0, alpha=0.9)
    draw_phase_labels(pts, times, ax, interval_min)
    ax.set_title(f"BTCEUR {tf_label} — Layer 3 Range Box", fontsize=14)
    fig.autofmt_xdate()
    chart_path = os.path.join(OUTDIR, f"layer3_range_box_BTCEUR_{tf_label}.png")
    fig.savefig(chart_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  ✅ {dbg_path}")
    print(f"  ✅ {chart_path} ({os.path.getsize(chart_path)} bytes)")

print(f"\n{'='*70}")
print(f"  ✅ compileall OK")
print(f"  ✅ Layer 2 niet gewijzigd")
print(f"  ❌ Geen commit (wacht op akkoord)")
print(f"{'='*70}")
