"""Test de nieuwe Layer 3 pipeline — raw slope → merge → chop detectie."""
from __future__ import annotations
import sys, os, json, time
from datetime import datetime, timezone

HERMES_ROOT = "/mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/projects/hermes-v01"
sys.path.insert(0, os.path.join(HERMES_ROOT, "layer2_structure"))
sys.path.insert(0, os.path.join(HERMES_ROOT, "layer2_structure_v2"))
sys.path.insert(0, HERMES_ROOT)

from hermes_v01 import vind_fractalen, _scheid_toppen_bodems
from layer2_structure_v2.swing_points import detect_swing_highs, detect_swing_lows
from layer2_structure_v2.pivot_utils import compute_pivots
from layer2_structure_v2.layer3_label import label_phases, debug_phases, MINI_FLAT_PCT, CHOP_BAND_PCT, CHOP_MIN_SWITCHES, CHOP_MAX_NETTO_PCT

import requests

OUTDIR = "/home/sjoe/system/hermes-second-brain/tasks"

def fetch_kraken(pair, interval, candles=200):
    since = int(time.time()) - (candles * interval * 60 + 86400)
    url = f"https://api.kraken.com/0/public/OHLC?pair={pair}&interval={interval}&since={since}"
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    if data.get("error"):
        raise ValueError(f"Kraken: {data['error']}")
    key = [k for k in data["result"] if k != "last"][0]
    raw = data["result"][key]
    result = [
        {"timestamp": int(r[0]), "open": float(r[1]), "high": float(r[2]),
         "low": float(r[3]), "close": float(r[4]), "volume": float(r[6])}
        for r in raw
    ]
    return result[-candles:]

pair = "ADAEUR"
tfs = [(240, "240m"), (60, "60m"), (15, "15m"), (5, "5m")]
results = {}

for interval_min, tf_label in tfs:
    print(f"\n{'='*60}")
    print(f"  {pair} {tf_label}")
    print(f"{'='*60}")
    
    candles = fetch_kraken(pair, interval_min)
    if len(candles) < 10:
        print(f"  ❌ Te weinig candles")
        continue
    
    fractalen = vind_fractalen(candles)
    toppen, bodems = _scheid_toppen_bodems(fractalen)
    swing_highs = detect_swing_highs(toppen, candles, interval_min, tf_label)
    swing_lows = detect_swing_lows(bodems, candles, interval_min, tf_label)
    pivot_indices, pts = compute_pivots(swing_highs, swing_lows, candles)
    
    if len(pts) < 2:
        print(f"  ❌ Te weinig purper punten")
        continue
    
    # Nieuwe pipeline
    raw, merged, final = label_phases(pts, interval_min)
    
    print(f"  Purper punten: {len(pts)}")
    print(f"  Raw segmenten: {len(raw)}")
    r_u = sum(1 for s in raw if s['raw_label']=='U')
    r_d = sum(1 for s in raw if s['raw_label']=='D')
    r_r = sum(1 for s in raw if s['raw_label']=='R')
    print(f"    Raw: {r_u}x U, {r_d}x D, {r_r}x R")
    print(f"  Merged phases: {len(merged)}")
    m_u = sum(1 for p in merged if p['label']=='U')
    m_d = sum(1 for p in merged if p['label']=='D')
    m_r = sum(1 for p in merged if p['label']=='R')
    print(f"    Merged: {m_u}x U, {m_d}x D, {m_r}x R")
    print(f"  Final phases: {len(final)}")
    f_u = sum(1 for p in final if p['final_label']=='U')
    f_d = sum(1 for p in final if p['final_label']=='D')
    f_r = sum(1 for p in final if p['final_label']=='R')
    print(f"    Final: {f_u}x U, {f_d}x D, {f_r}x R")
    
    # Debug output
    debug = debug_phases(pts, interval_min)
    print(f"\n{debug}")
    
    # Sla debug output op
    debug_path = os.path.join(OUTDIR, f"layer3_debug_v2_{tf_label}.txt")
    with open(debug_path, "w") as f:
        f.write(debug)
    
    # Sla alle data op
    data = {
        "pair": pair,
        "timeframe": tf_label,
        "interval_minutes": interval_min,
        "mini_flat_pct": MINI_FLAT_PCT.get(interval_min, 0.03),
        "chop_band_pct": CHOP_BAND_PCT.get(interval_min, 2.0),
        "chop_min_switches": CHOP_MIN_SWITCHES.get(interval_min, 3),
        "chop_max_netto_pct": CHOP_MAX_NETTO_PCT.get(interval_min, 0.8),
        "points": [{"idx": p[0], "price": p[1]} for p in pts],
        "raw_segments": raw,
        "merged_phases": merged,
        "final_phases": final,
    }
    json_path = os.path.join(OUTDIR, f"layer3_debug_v2_{tf_label}.json")
    with open(json_path, "w") as f:
        json.dump(data, f, indent=2, default=str)
    
    results[tf_label] = {
        "pts": len(pts),
        "raw": (r_u, r_d, r_r),
        "merged": (m_u, m_d, m_r),
        "final": (f_u, f_d, f_r),
        "debug_path": debug_path,
        "json_path": json_path,
    }

print("\n\n" + "="*60)
print("  EINDRAPPORT — NIEUWE PIPELINE")
print("="*60)
print(f"  Pair: {pair}")
for tf_label in ["240m", "60m", "15m", "5m"]:
    r = results.get(tf_label)
    if not r:
        continue
    print(f"\n  ── {tf_label} ──")
    print(f"  Debug: {r['debug_path']}")
    print(f"  JSON:  {r['json_path']}")
    print(f"  Purper punten: {r['pts']}")
    print(f"  Raw segments:   U={r['raw'][0]}  D={r['raw'][1]}  R={r['raw'][2]}")
    print(f"  Merged phases:  U={r['merged'][0]}  D={r['merged'][1]}  R={r['merged'][2]}")
    print(f"  Final phases:   U={r['final'][0]}  D={r['final'][1]}  R={r['final'][2]}")

print()
print("✅ Alleen layer3_label.py gewijzigd. Layer 2 onaangeroerd. Geen commit.")
