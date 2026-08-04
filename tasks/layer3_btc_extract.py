"""Extract purper line pivot segmenten voor BTCEUR — exact zoals ADAEUR tabellen."""
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
from layer2_structure_v2.layer3_label import label_segments

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
    return [{"timestamp": int(r[0]), "open": float(r[1]), "high": float(r[2]), "low": float(r[3]), "close": float(r[4]), "volume": float(r[6])} for r in raw][-candles:]

def ts_to_dt(ts):
    return datetime.fromtimestamp(ts, tz=timezone.utc)

TOLERANCE_MAP = {240: 1.8, 60: 1.0, 15: 0.55, 5: 0.25}

pair = "BTCEUR"
tfs = [(240, "240m"), (60, "60m"), (15, "15m"), (5, "5m")]

for interval_min, tf_label in tfs:
    print(f"\n=== {pair} {tf_label} ===")
    candles = fetch_kraken(pair, interval_min)
    if len(candles) < 10:
        print(f"  ❌ Te weinig candles")
        continue

    fractalen = vind_fractalen(candles)
    toppen, bodems = _scheid_toppen_bodems(fractalen)
    swing_highs = detect_swing_highs(toppen, candles, interval_min, tf_label)
    swing_lows = detect_swing_lows(bodems, candles, interval_min, tf_label)
    pivot_indices, pts = compute_pivots(swing_highs, swing_lows, candles)
    print(f"  Purper line punten (pts): {len(pts)}")
    if len(pts) < 2:
        print("  ❌ Te weinig pivots")
        continue

    for i, (idx, price) in enumerate(pts):
        ts = candles[idx]["timestamp"] if idx < len(candles) else 0
        dt_str = ts_to_dt(ts).strftime('%Y-%m-%d %H:%M')
        print(f"    X{i}: idx={idx}, ts={dt_str}, price={price:.1f}")

    segs = label_segments(pts, interval_min)
    print(f"  Segmenten: {len(segs)}")
    # toon de nieuw pipeline segmenten (raw slope, geen tolerance)
    r_u = sum(1 for s in segs if s['raw_label']=='U')
    r_d = sum(1 for s in segs if s['raw_label']=='D')
    r_r = sum(1 for s in segs if s['raw_label']=='R')
    print(f"    U={r_u} D={r_d} R={r_r}")

    tolerance = TOLERANCE_MAP[interval_min]
    rows = []
    for i in range(len(pts) - 1):
        idx1, p1 = pts[i]
        idx2, p2 = pts[i+1]
        x_minus_1_price = None; x_minus_1_ts = None
        x_minus_2_price = None; x_minus_2_ts = None
        if i >= 1:
            xm1_idx, xm1_p = pts[i-1]
            x_minus_1_ts = candles[xm1_idx]["timestamp"] if xm1_idx < len(candles) else 0
            x_minus_1_price = xm1_p
        if i >= 2:
            xm2_idx, xm2_p = pts[i-2]
            x_minus_2_ts = candles[xm2_idx]["timestamp"] if xm2_idx < len(candles) else 0
            x_minus_2_price = xm2_p
        X_ts = candles[idx1]["timestamp"] if idx1 < len(candles) else 0
        Xplus1_ts = candles[idx2]["timestamp"] if idx2 < len(candles) else 0
        delta_price = p2 - p1
        delta_pct = delta_price / p1 * 100 if p1 > 0 else 0
        if delta_price > 0: direction_raw = "HOGER"
        elif delta_price < 0: direction_raw = "LAGER"
        else: direction_raw = "GELIJK"
        if delta_pct > tolerance: raw_label_tol = "U"
        elif delta_pct < -tolerance: raw_label_tol = "D"
        else: raw_label_tol = "R"
        if delta_price > 0: raw_label_strict = "U"
        elif delta_price < 0: raw_label_strict = "D"
        else: raw_label_strict = "R"
        candles_between = idx2 - idx1
        hours_between = (Xplus1_ts - X_ts) / 3600 if Xplus1_ts and X_ts else 0
        slope_pts_per_candle = delta_price / candles_between if candles_between > 0 else 0
        slope_pct_per_candle = delta_pct / candles_between if candles_between > 0 else 0
        slope_pts_per_hour = delta_price / hours_between if hours_between > 0 else 0
        prev_seg = None; prev_2_seg = None; ctx = None
        if i >= 1:
            prev_seg = "U" if (pts[i][1] - pts[i-1][1]) > 0 else ("D" if (pts[i][1] - pts[i-1][1]) < 0 else "R")
        if i >= 2:
            prev_2_seg = "U" if (pts[i-1][1] - pts[i-2][1]) > 0 else ("D" if (pts[i-1][1] - pts[i-2][1]) < 0 else "R")
            ctx = f"{prev_2_seg}→{prev_seg}"
        rows.append({
            "timeframe": tf_label, "segment_index": i,
            "X_index": idx1, "X_timestamp": X_ts, "X_avg_price": round(p1, 2),
            "X_minus_1_timestamp": x_minus_1_ts, "X_minus_1_avg_price": round(x_minus_1_price, 2) if x_minus_1_price else None,
            "X_minus_2_timestamp": x_minus_2_ts, "X_minus_2_avg_price": round(x_minus_2_price, 2) if x_minus_2_price else None,
            "X_plus_1_index": idx2, "X_plus_1_timestamp": Xplus1_ts, "X_plus_1_avg_price": round(p2, 2),
            "delta_price": round(delta_price, 2), "delta_pct": round(delta_pct, 4),
            "direction_raw": direction_raw, "current_tolerance_pct": tolerance,
            "raw_label_met_tolerance": raw_label_tol, "raw_label_strict_slope": raw_label_strict,
            "candles_between": candles_between, "hours_between": round(hours_between, 2),
            "slope_points_per_candle": round(slope_pts_per_candle, 2),
            "slope_pct_per_candle": round(slope_pct_per_candle, 4),
            "slope_points_per_hour": round(slope_pts_per_hour, 2),
            "previous_segment_label": prev_seg, "previous_2_segment_label": prev_2_seg,
            "context_previous_2_segments": ctx, "note": ""
        })

    md_lines = []
    md_lines.append(f"# Layer 3 Purper Line Pivot Segmenten — {pair} {tf_label}")
    md_lines.append(f"")
    md_lines.append(f"Extractie: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    md_lines.append(f"Tolerantie: {tolerance}%")
    md_lines.append(f"Aantal segmenten: {len(rows)}")
    md_lines.append(f"Aantal purper line punten (X): {len(pts)}")
    md_lines.append(f"")
    md_lines.append("## Segmenten (volledige tabel)")
    md_lines.append("")
    md_lines.append("| # | X_idx | X_dt | X_price | X-1_dt | X-1_price | X-2_dt | X-2_price | X+1_idx | X+1_dt | X+1_price | delta_price | delta_pct | dir | tol | label_tol | label_strict | candles | hours | slp_pt/c | slp_pct/c | slp_pt/h | prev | prev2 | ctx |")
    md_lines.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for r in rows:
        x_dt = ts_to_dt(r["X_timestamp"]).strftime('%m-%d %H:%M') if r["X_timestamp"] else "?"
        x1_dt = ts_to_dt(r["X_plus_1_timestamp"]).strftime('%m-%d %H:%M') if r["X_plus_1_timestamp"] else "?"
        xm1_dt = ts_to_dt(r["X_minus_1_timestamp"]).strftime('%m-%d %H:%M') if r["X_minus_1_timestamp"] else "-"
        xm2_dt = ts_to_dt(r["X_minus_2_timestamp"]).strftime('%m-%d %H:%M') if r["X_minus_2_timestamp"] else "-"
        xm1_p = f"{r['X_minus_1_avg_price']:.1f}" if r['X_minus_1_avg_price'] is not None else "-"
        xm2_p = f"{r['X_minus_2_avg_price']:.1f}" if r['X_minus_2_avg_price'] is not None else "-"
        ctx = r["context_previous_2_segments"] or "-"
        prev = r["previous_segment_label"] or "-"
        prev2 = r["previous_2_segment_label"] or "-"
        md_lines.append(
            f"| {r['segment_index']} "
            f"| {r['X_index']} "
            f"| {x_dt} "
            f"| {r['X_avg_price']:.1f} "
            f"| {xm1_dt} "
            f"| {xm1_p} "
            f"| {xm2_dt} "
            f"| {xm2_p} "
            f"| {r['X_plus_1_index']} "
            f"| {x1_dt} "
            f"| {r['X_plus_1_avg_price']:.1f} "
            f"| {r['delta_price']:+.1f} "
            f"| {r['delta_pct']:+.2f}% "
            f"| {r['direction_raw']:<6} "
            f"| {r['current_tolerance_pct']}% "
            f"| {r['raw_label_met_tolerance']} "
            f"| {r['raw_label_strict_slope']} "
            f"| {r['candles_between']} "
            f"| {r['hours_between']:.1f} "
            f"| {r['slope_points_per_candle']:.1f} "
            f"| {r['slope_pct_per_candle']:.2f}% "
            f"| {r['slope_points_per_hour']:.1f} "
            f"| {prev} "
            f"| {prev2} "
            f"| {ctx} |"
        )
    md_lines.append("")
    md_lines.append("## Samenvatting")
    md_lines.append("")
    labels_tol = [r["raw_label_met_tolerance"] for r in rows]
    labels_strict = [r["raw_label_strict_slope"] for r in rows]
    md_lines.append(f"- Huidige tolerance: {tolerance}%")
    md_lines.append(f"- Labels met tolerance: {labels_tol.count('U')}x U, {labels_tol.count('D')}x D, {labels_tol.count('R')}x R")
    md_lines.append(f"- Labels strikte slope: {labels_strict.count('U')}x U, {labels_strict.count('D')}x D, {labels_strict.count('R')}x R")
    diffs = []
    for r in rows:
        if r["raw_label_met_tolerance"] != r["raw_label_strict_slope"]:
            diffs.append(r["segment_index"])
    if diffs:
        md_lines.append(f"- Verschillen tolerance vs strict: segmenten {', '.join(str(d) for d in diffs)}")
    else:
        md_lines.append("- Geen verschillen")
    md_lines.append("")

    md_path = os.path.join(OUTDIR, f"layer3_debug_pivot_segments_BTCEUR_{tf_label}.md")
    with open(md_path, "w") as f:
        f.write("\n".join(md_lines))
    json_path = os.path.join(OUTDIR, f"layer3_debug_pivot_segments_BTCEUR_{tf_label}.json")
    with open(json_path, "w") as f:
        json.dump({
            "pair": pair, "timeframe": tf_label, "interval_minutes": interval_min,
            "tolerance": tolerance, "segment_count": len(rows), "point_count": len(pts),
            "extracted_utc": datetime.now(timezone.utc).isoformat(),
            "segments": rows,
            "points": [{"idx": p[0], "price": p[1]} for p in pts],
        }, f, indent=2, default=str)
    print(f"\n  ✅ {md_path} — {len(rows)} segmenten")
    print(f"  ✅ {json_path}")

print(f"\n✅ BTCEUR tabellen klaar in {OUTDIR}")
