"""Generate test chart with new Layer 3 phase labels."""
import sys, os
hermes = "/mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/projects/hermes-v01"
sys.path.insert(0, os.path.join(hermes, "layer2_structure"))
sys.path.insert(0, os.path.join(hermes, "layer2_structure_v2"))
sys.path.insert(0, hermes)

from layer2_structure_v2.layer3_label import draw_phase_labels
from layer2_structure_v2.pivot_utils import compute_pivots
from hermes_v01 import vind_fractalen, _scheid_toppen_bodems
from layer2_structure_v2.swing_points import detect_swing_highs, detect_swing_lows
import requests, time
from datetime import datetime, timezone

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def fetch(pair, interval):
    since = int(time.time()) - (200 * interval * 60 + 86400)
    resp = requests.get(f"https://api.kraken.com/0/public/OHLC?pair={pair}&interval={interval}&since={since}", timeout=10)
    data = resp.json()
    key = [k for k in data["result"] if k != "last"][0]
    raw = data["result"][key]
    return [{"timestamp": int(r[0]), "open": float(r[1]), "high": float(r[2]), "low": float(r[3]), "close": float(r[4]), "volume": float(r[6])} for r in raw][-200:]

outdir = "/home/sjoe/system/hermes-second-brain/tasks"

pairs_tfs = [
    ("ADAEUR", 240, "240m"),
    ("ADAEUR", 60, "60m"),
    ("ADAEUR", 15, "15m"),
    ("ADAEUR", 5, "5m"),
    ("BTCEUR", 240, "240m"),
    ("BTCEUR", 60, "60m"),
]

for pair, interval, tf_label in pairs_tfs:
    print(f"\n=== {pair} {tf_label} ===")
    candles = fetch(pair, interval)
    
    fractalen = vind_fractalen(candles)
    toppen, bodems = _scheid_toppen_bodems(fractalen)
    swing_highs = detect_swing_highs(toppen, candles, interval, tf_label)
    swing_lows = detect_swing_lows(bodems, candles, interval, tf_label)
    _, pts = compute_pivots(swing_highs, swing_lows, candles)
    
    if len(pts) < 2:
        print("  ❌ Te weinig punten")
        continue
    
    times = [datetime.fromtimestamp(c['timestamp'], tz=timezone.utc) for c in candles]
    
    fig, ax = plt.subplots(figsize=(14, 7))
    
    # Candlesticks
    for i, c in enumerate(candles):
        t = times[i]
        color = 'green' if c['close'] >= c['open'] else 'red'
        ax.plot([t, t], [c['low'], c['high']], color='black', linewidth=0.3)
        bar_width = 0.6 * interval / (24*60) if interval >= 60 else 0.6 * interval / (24*60)
        ax.bar(t, abs(c['close'] - c['open']), bottom=min(c['open'], c['close']), 
               width=bar_width, color=color, alpha=0.6)
    
    # Purper line
    for i in range(1, len(pts)):
        idx1, p1 = pts[i-1]
        idx2, p2 = pts[i]
        ax.plot([times[min(idx1, len(times)-1)], times[min(idx2, len(times)-1)]], 
                [p1, p2], color='#9C27B0', linewidth=2.0, alpha=0.9)
    
    # Phase labels (NEW)
    draw_phase_labels(pts, times, ax, interval)
    
    ax.set_title(f"{pair} {tf_label} — Layer 3 fase-labels", fontsize=14)
    fig.autofmt_xdate()
    
    outpath = os.path.join(outdir, f"test_labels_{pair}_{tf_label}.png")
    fig.savefig(outpath, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  ✅ {outpath} ({os.path.getsize(outpath)} bytes)")

print("\n✅ Done")
