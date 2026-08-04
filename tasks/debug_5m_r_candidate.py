"""Debug 5m R_KANDIDAAT #0 — exacte pivot data."""
from __future__ import annotations
import sys, os
sys.path.insert(0, "/mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/projects/hermes-v01/layer2_structure")
sys.path.insert(0, "/mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/projects/hermes-v01/layer2_structure_v2")
sys.path.insert(0, "/mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/projects/hermes-v01")
from hermes_v01 import vind_fractalen, _scheid_toppen_bodems
from layer2_structure_v2.swing_points import detect_swing_highs, detect_swing_lows
from layer2_structure_v2.pivot_utils import compute_pivots
from layer2_structure_v2.layer3_label import label_phases
import requests, time, json

since = int(time.time()) - (200 * 5 * 60 + 86400)
resp = requests.get(f"https://api.kraken.com/0/public/OHLC?pair=BTCEUR&interval=5&since={since}", timeout=10)
data = resp.json()
key = [k for k in data["result"] if k != "last"][0]
raw = data["result"][key]
candles = [{"timestamp": int(r[0]), "open": float(r[1]), "high": float(r[2]), "low": float(r[3]), "close": float(r[4]), "volume": float(r[6])} for r in raw][-200:]
fractalen = vind_fractalen(candles)
toppen, bodems = _scheid_toppen_bodems(fractalen)
swing_highs = detect_swing_highs(toppen, candles, 5, "5m")
swing_lows = detect_swing_lows(bodems, candles, 5, "5m")
_, pts = compute_pivots(swing_highs, swing_lows, candles)

raw_seg, comp, final, r_cands = label_phases(pts, 5)

# Zoek de R-kandidaat
for rc in r_cands:
    if not rc.get('accepted', False):
        continue
    print(f"=== R_KANDIDAAT #{rc['candidate_index']} ===")
    print(f"  start_price: {rc.get('start_price', '?'):.2f}")
    print(f"  end_price:   {rc.get('end_price', '?'):.2f}")
    print(f"  price_low:   {rc.get('price_low', '?'):.2f}")
    print(f"  price_high:  {rc.get('price_high', '?'):.2f}")
    print(f"  net_delta_pct: {rc.get('net_delta_pct', 0):.4f}%")
    print(f"  box_height_pct: {rc.get('box_height_pct', 0):.4f}%")
    print(f"  upper_mean:  {rc.get('upper_mean', '?'):.2f}")
    print(f"  lower_mean:  {rc.get('lower_mean', '?'):.2f}")
    print(f"  pivots: {rc.get('pivot_count', 0)}")
    print(f"  raw_indices: {rc.get('raw_indices_inside', [])}")
    print(f"  compressed_indices: {rc.get('compressed_indices_inside', [])}")
    
    # Print pivot prices
    ri = rc.get('raw_indices_inside', [])
    pivot_prices = [raw_seg[r]['p1'] for r in ri if r < len(raw_seg)]
    if ri and ri[-1] < len(raw_seg):
        pivot_prices.append(raw_seg[ri[-1]]['p2'])
    print(f"  pivot_prices: {[f'{p:.2f}' for p in pivot_prices]}")
    
    # Local extremes
    prices = pivot_prices
    highs = []
    lows = []
    for i in range(1, len(prices) - 1):
        if prices[i] > prices[i-1] and prices[i] > prices[i+1]:
            highs.append(prices[i])
        if prices[i] < prices[i-1] and prices[i] < prices[i+1]:
            lows.append(prices[i])
    print(f"  local_highs: {[f'{h:.2f}' for h in highs]}")
    print(f"  local_lows:  {[f'{l:.2f}' for l in lows]}")
    
    # Netto vs box check
    net = rc.get('net_delta_pct', 0)
    box = rc.get('box_height_pct', 0.0001)
    print(f"  net/box ratio: {net/box:.2f}")
    print(f"  Dit is een staircase-down van {net:.2f}% met kleine zigzag amplitude van {box:.2f}%")
    print(f"  → GEEN RANGE, dit moet D zijn")
