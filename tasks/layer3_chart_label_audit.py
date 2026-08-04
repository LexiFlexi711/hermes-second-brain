"""Layer 3 Chart Label Audit — BTCEUR alle 4 TFs.
Leest JSON debug data, berekent audit metrics, genereert rapport."""
from __future__ import annotations
import sys, os, json
from datetime import datetime, timezone

OUTDIR = "/home/sjoe/system/hermes-second-brain/tasks"
TFS = ["240m", "60m", "15m", "5m"]

def load_json(tf):
    path = os.path.join(OUTDIR, f"layer3_debug_v2_BTCEUR_{tf}.json")
    with open(path) as f:
        return json.load(f)

def ts_to_str(ts):
    if ts is None:
        return "-"
    if isinstance(ts, (int, float)):
        return datetime.fromtimestamp(ts, tz=timezone.utc).strftime('%m-%d %H:%M')
    return str(ts)

def audit_phase(p, pts_dict):
    """Bereken audit metrics voor één final_phase."""
    start_price = p['start_price']
    end_price = p['end_price']
    price_low = p.get('price_low', min(start_price, end_price))
    price_high = p.get('price_high', max(start_price, end_price))
    
    net_delta = end_price - start_price
    net_delta_pct = net_delta / start_price * 100 if start_price > 0 else 0
    range_band_pct = (price_high - price_low) / start_price * 100 if start_price > 0 else 0
    
    # Gross move: sum of abs(delta) of raw segments
    seg_start = p.get('start_segment', 0)
    seg_end = p.get('end_segment', 0)
    gross = 0.0
    for si in range(seg_start, seg_end + 1):
        s = pts_dict.get(str(si))
        if s:
            gross += abs(s['delta'])
    
    efficiency = abs(net_delta) / gross if gross > 0 else 1.0
    
    return {
        'net_delta': net_delta,
        'net_delta_pct': net_delta_pct,
        'price_low': price_low,
        'price_high': price_high,
        'range_band_pct': range_band_pct,
        'gross_move': gross,
        'efficiency': efficiency,
        'seg_count': p.get('segments_count', p.get('segm', 0)),
        'raw_inside': p.get('raw_labels_inside', '?'),
        'reason': p.get('reason', ''),
    }

def verdict_u_d(p, metrics):
    """Geef verdict voor U of D label."""
    lbl = p['final_label']
    net = metrics['net_delta_pct']
    eff = metrics['efficiency']
    band = metrics['range_band_pct']
    seg = metrics['seg_count']
    raw = metrics['raw_inside']
    
    if lbl == 'U':
        if net <= 0:
            return "FOUT", f"U maar net_delta={net:.2f}% <= 0"
        if eff < 0.3 and seg >= 3:
            return "VERDACHT", f"U maar efficiency={eff:.2f} (veel U/D-wissels), net={net:.2f}%, band={band:.2f}%"
        if band > 15:
            return "VERDACHT", f"U maar band={band:.2f}% is erg breed"
        return "OK", f"U: net={net:+.2f}%, eff={eff:.2f}, band={band:.2f}%, segm={seg}"
    
    if lbl == 'D':
        if net >= 0:
            return "FOUT", f"D maar net_delta={net:.2f}% >= 0"
        if eff < 0.3 and seg >= 3:
            return "VERDACHT", f"D maar efficiency={eff:.2f} (veel U/D-wissels), net={net:.2f}%, band={band:.2f}%"
        return "OK", f"D: net={net:+.2f}%, eff={eff:.2f}, band={band:.2f}%, segm={seg}"
    
    return "FOUT", f"onbekend label {lbl}"

def verdict_r(p, metrics):
    """Geef verdict voor R label — strenge check."""
    net = metrics['net_delta_pct']
    eff = metrics['efficiency']
    band = metrics['range_band_pct']
    seg = metrics['seg_count']
    raw = metrics['raw_inside']
    
    reasons = []
    
    # Check 1: net_delta moet klein zijn
    if abs(net) > 1.5:
        reasons.append(f"net_delta={net:.2f}% is TE GROOT voor R")
    elif abs(net) > 0.8:
        reasons.append(f"⚠️ net_delta={net:.2f}% is aan de grote kant")
    
    # Check 2: band moet beperkt zijn
    if band > 4.0 and seg >= 4:
        reasons.append(f"band={band:.2f}% is breed maar door {seg} segmenten")
    elif band > 5.0:
        reasons.append(f"band={band:.2f}% is te breed voor R")
    
    # Check 3: efficiency moet laag zijn
    if eff > 0.5:
        reasons.append(f"efficiency={eff:.2f} is te hoog voor R")
    
    # Check 4: moet U/D-wissels hebben
    if 'R' in raw and all(c == 'R' for c in raw.split('→')):
        # Puur R (flat)
        if abs(net) < 0.05:
            return "OK", f"R (flat): net={net:.4f}%, band={band:.2f}%, segm={seg}"
        else:
            return "VERDACHT", f"R (flat) maar net={net:.4f}%"
    
    # Check 5: net_delta mag niet duidelijk U of D zijn
    if net > 1.0:
        reasons.append(f"EINDT HOGER dan start: net={net:+.2f}% — dit lijkt een U-fase")
    if net < -1.0:
        reasons.append(f"EINDT LAGER dan start: net={net:+.2f}% — dit lijkt een D-fase")
    
    if reasons:
        return "VERDACHT", "; ".join(reasons)
    
    return "OK", f"R: net={net:+.2f}%, band={band:.2f}%, eff={eff:.2f}, segm={seg}, raw={raw}"


# ── Hoofdloop ──

for tf in TFS:
    data = load_json(tf)
    pts = data.get('points', [])
    raw_segs = data.get('raw_segments', [])
    final_phases = data.get('final_phases', [])
    
    # Bouw pts_dict voor gross move lookup
    pts_dict = {}
    for i, seg in enumerate(raw_segs):
        pts_dict[str(i)] = seg
    
    print(f"\n{'='*80}")
    print(f"  CHART LABEL AUDIT — BTCEUR {tf}")
    print(f"{'='*80}")
    print(f"  Data timestamp: {data.get('extracted_utc', '?')}")
    print(f"  Purper punten: {len(pts)}")
    print(f"  Raw segmenten: {len(raw_segs)}")
    print(f"  Final phases:  {len(final_phases)}")
    
    # ── A. RAW SEGMENTS (verkort) ──
    print(f"\n  ── A. RAW SEGMENTS ({len(raw_segs)} segs) ──")
    
    # ── B. FINAL PHASES met audit metrics ──
    print(f"\n  ── B. FINAL PHASES MET AUDIT METRICS ──")
    hdr = f"  {'#':<3} {'label':<6} {'start_p':<10} {'end_p':<10} {'net%':<8} {'band%':<8} {'gross':<10} {'eff':<7} {'segm':<5} {'reason':<16}"
    print(hdr)
    print("  " + "-" * (len(hdr) - 2))
    
    for p in final_phases:
        metrics = audit_phase(p, pts_dict)
        print(f"  {p['phase_index']:<3} {p['final_label']:<6} {p['start_price']:<10.1f} {p['end_price']:<10.1f} "
              f"{metrics['net_delta_pct']:<+7.2f}% {metrics['range_band_pct']:<7.2f}% "
              f"{metrics['gross_move']:<10.1f} {metrics['efficiency']:<6.2f} "
              f"{metrics['seg_count']:<5} {metrics['reason']:<16}")
    
    # ── C. CHART LABEL AUDIT ──
    print(f"\n  ── C. CHART LABEL AUDIT — per phase verdict ──")
    hdr2 = f"  {'#':<3} {'label':<6} {'net%':<9} {'band%':<8} {'eff':<6} {'segm':<5} {'verdict':<12} {'comment'}"
    print(hdr2)
    print("  " + "-" * (len(hdr2) - 2))
    
    ok_count = 0
    verdacht_count = 0
    fout_count = 0
    
    for p in final_phases:
        metrics = audit_phase(p, pts_dict)
        lbl = p['final_label']
        
        if lbl in ('U', 'D'):
            v, c = verdict_u_d(p, metrics)
        elif lbl == 'R':
            v, c = verdict_r(p, metrics)
        else:
            v, c = "FOUT", f"onbekend label {lbl}"
        
        if v == "OK": ok_count += 1
        elif v == "VERDACHT": verdacht_count += 1
        elif v == "FOUT": fout_count += 1
        
        net_s = f"{metrics['net_delta_pct']:+.2f}%"
        print(f"  {p['phase_index']:<3} {lbl:<6} {net_s:<9} {metrics['range_band_pct']:<7.2f}% "
              f"{metrics['efficiency']:<5.2f} {metrics['seg_count']:<5} {v:<12} {c[:40]}")
        
        # Extra check voor R
        if lbl == 'R' and v in ('VERDACHT', 'FOUT'):
            print(f"    └─ raw: {metrics['raw_inside']} | gross={metrics['gross_move']:.1f} | "
                  f"prices: {p['start_price']:.1f}→{p['end_price']:.1f} "
                  f"(low={metrics['price_low']:.1f} high={metrics['price_high']:.1f})")
    
    print(f"\n  RESULT: {ok_count}x OK, {verdacht_count}x VERDACHT, {fout_count}x FOUT")
    
    # ── R-label extra analyse ──
    r_phases = [p for p in final_phases if p['final_label'] == 'R']
    if r_phases:
        print(f"\n  ── R-LABEL EXTRA CHECK ({len(r_phases)} R-fases) ──")
        for p in r_phases:
            metrics = audit_phase(p, pts_dict)
            net = metrics['net_delta_pct']
            band = metrics['range_band_pct']
            eff = metrics['efficiency']
            
            print(f"  Phase {p['phase_index']}: R")
            print(f"    1. Waarom geen U?  net_delta={net:+.2f}% — {'klein genoeg' if abs(net) < 1.5 else 'TE GROOT'}")
            print(f"    2. Waarom geen D?  net_delta={net:+.2f}% — {'klein genoeg' if abs(net) < 1.5 else 'TE GROOT'}")
            print(f"    3. net_delta_pct: {net:+.2f}%")
            print(f"    4. range_band_pct: {band:.2f}%")
            print(f"    5. efficiency: {eff:.2f}")
            print(f"    6. raw labels: {metrics['raw_inside']}")
            print(f"    7. prijsband: {metrics['price_low']:.1f} - {metrics['price_high']:.1f} "
                  f"(range={metrics['price_high']-metrics['price_low']:.1f})")

print(f"\n{'='*80}")
print("  AUDIT VOLTOOID — Geen code gewijzigd. Geen commit.")
print(f"{'='*80}")
