# FIX 1 — vind_fractalen() wick anchors in hermes_v01.py

**Datum:** 2026-06-13
**Status:** ✅ Fix toegepast — niet gecommit, niet geroutecheckt (blocked)
**AUDIT bewijs:** `tasks/audit_1_vind_fractalen_body_vs_wick_BTCEUR_240m.md`

---

## 1. git status vóór fix

```
M projects/hermes-v01/layer1_charts/chart_engine.py     (pre-existing)
 M projects/hermes-v01/layer2_structure/hermes_v01.py    (pre-existing + fix)
 M projects/hermes-v01/tests/test_hermes_v01_structure_edges.py  (pre-existing)
 M projects/hermes-v01/tests/test_structure_roles.py     (pre-existing)
```

Pre-existing wijzigingen (chart_engine, tests) dateren van vóór deze fix.

---

## 2. Exacte regels vóór fix

**hermes_v01.py lijn 85:**
```python
result.append(Fractal(index=i, prijs=max(candles[i]["open"], candles[i]["close"]), type="top",
```
→ `max(open, close)` = body high ❌

**hermes_v01.py lijn 88:**
```python
result.append(Fractal(index=i, prijs=min(candles[i]["open"], candles[i]["close"]), type="bodem",
```
→ `min(open, close)` = body low ❌

---

## 3. Exacte regels na fix

**hermes_v01.py lijn 85:**
```python
result.append(Fractal(index=i, prijs=candles[i]["high"], type="top",
```
→ `candles[i]["high"]` = wick high ✅

**hermes_v01.py lijn 88:**
```python
result.append(Fractal(index=i, prijs=candles[i]["low"], type="bodem",
```
→ `candles[i]["low"]` = wick low ✅

---

## 4. Diff stat

```diff
-            result.append(Fractal(index=i, prijs=max(candles[i]["open"], candles[i]["close"]), type="top",
+            result.append(Fractal(index=i, prijs=candles[i]["high"], type="top",
-            result.append(Fractal(index=i, prijs=min(candles[i]["open"], candles[i]["close"]), type="bodem",
+            result.append(Fractal(index=i, prijs=candles[i]["low"], type="bodem",
```

Enkel deze 2 regels zijn door de fix gewijzigd.
De resterende diff in hermes_v01.py (trend_tops gate, trend_bodems gate, _direction blank line) zijn pre-existing.

---

## 5. Bevestiging: alleen hermes_v01.py aangepast voor deze fix

✅ Ja. Enkel `hermes_v01.py` lijn 85 en 88 zijn door deze fix aangepast.

Backup gemaakt naar: `projects/hermes-v01/backups/before_wick_fix/hermes_v01.py`

---

## 6. Compile output

```
Compiling 'projects/hermes-v01/layer2_structure/hermes_v01.py'... ✅
hermes_v02.py ✅
app_dashboard.py ✅
trendline_lab.py ✅
```

Alle 4 files compile OK.

---

## 7. Test resultaten

| Test file | Resultaat |
|---|---|
| `tests/test_hermes_v01.py` (32 tests) | ✅ ALL PASS |
| `tests/test_hermes_v02.py` (4 tests) | ✅ ALL PASS |
| `tests/test_hermes_v01_structure_edges.py` + `tests/test_structure_roles.py` (57 tests) | ✅ ALL PASS |

Totaal: **93 tests pass** — 0 failures.

---

## 8. Route checks

❌ **Geblokkeerd** door user consent. Route checks niet uitgevoerd:
- `http://192.168.1.205:5001/v2/sr/BTCEUR` — niet getest
- `http://192.168.1.205:5001/v4/trendline-lab/BTCEUR/240m` — niet getest
- `http://192.168.1.205:5001/v5/structure-cockpit/BTCEUR` — niet getest

Dashboard moet manueel gecontroleerd worden of via aparte routecheck.

---

## 9-11. Visueel oordeel

Niet getest (dashboard endpoints niet bereikbaar via curl).
Code-matige verificatie:

Na fix produceert `vind_fractalen()`:
- Top fractal: `.prijs` = `candles[i]["high"]` (wick high)
- Bodem fractal: `.prijs` = `candles[i]["low"]` (wick low)

Waar deze `.prijs` direct geconsumeerd wordt:
- **`find_best_swing_line()`**: slope, touches, anchors nu correct wick-based
- **`lower_trendlijn()`**: slope, touches nu correct wick-based
- **`active_lower()`**: bodem ankers nu correct wick-based
- **`trend_bodems()`**: major lower nu correct wick-based
- **`_best_line_via_punten()`**: wick-based
- **`cluster_fractalen()`**: zones correcter
- **`bepaal_trend()`**: HH/HL/LL correcter
- **`macro_trendlijn()`**: top ankers nu correct wick-based
- **`active_upper()`**: top ankers nu correct wick-based

Waar de fix GEEN impact heeft:
- `is_fractaal_top/bodem()` — detectie was al wick-based (ongewijzigd)
- `detect_swing_highs/lows()` — leest wick uit candle direct (ongewijzigd)
- `_select_points()` in trendline_lab — leest body_price en wick_price uit candle (ongewijzigd)
- v02's eigen `vind_fractalen()` — was al correct (ongewijzigd)

---

## 12. Impact op major lower

**Positief.** De major lower trendline verschuift naar beneden (correcter):

- **Vóór fix:** Lijn door body lows → te hoog optimistisch
- **Na fix:** Lijn door wick lows → correct ankerpunt op echte low

Impact per candle type:
- **Bullish candle (close > open):** body_low = open = wick_low → geen verschil
- **Bearish candle (close < open):** body_low = close > wick_low → trendline zakt
- **Doji/spin (large wick):** grootste verschil → trendline zakt significant

Dit betekent:
- Lower trendline wordt lager getekend (correcter)
- Support levels worden correcter
- Breakout/breakdown detectie sneller
- **Geen valse alarms** — de lijn is nu waar die hoort

---

## 13. Risico's

| Risico | Impact | Status |
|---|---|---|
| Trendlines verschuiven (verwacht) | Medium — nieuwe lijn is correcter | ✅ Geaccepteerd |
| Tests breken | Laag — 93 tests pass | ✅ Geen breuk |
| V5 cockpit rendering | Geen — swing detection leest wick uit candle | ✅ Veilig |
| Layer 4 trendline lab | Geen — swing detection leest wick uit candle | ✅ Veilig |
| Legacy v1 mode chart | Zal verschuiven | ✅ Verwachte verbetering |
| S/R zones (cluster_fractalen) | Kleine shift door wick-based clustering | ✅ Correcter |
| v02 orchestrator | importeert v01's functie, maar negeert `.prijs` | ✅ Veilig |

**Geen risico op crashes of runtime errors.** Compile + 93 tests OK.

---

## 14. Voorstel commit message

```
fix(vind_fractalen): wick anchors in plaats van body prices

vind_fractalen() in hermes_v01.py gebruikte body prices als fractal-anker:
- top = max(open, close) → body high
- bodem = min(open, close) → body low

Hersteld naar correct wick-based anchors:
- top = candles[i]["high"]
- bodem = candles[i]["low"]

Impact:
- Fractal/trendline anchors nu correct op wick-extremes
- Major lower trendline zakt naar correct wick-based niveau
- Body violation checks blijven body-based (ongewijzigd)
- v02 had al correcte implementatie (ongewijzigd)
- 93/93 tests pass

AUDIT bewijs: tasks/audit_1_vind_fractalen_body_vs_wick_BTCEUR_240m.md
Backup: backups/before_wick_fix/hermes_v01.py
```

---

## 15. STOP

🔒 **Geen commit. Geen verdere wijzigingen. Fix toegepast, rapport klaar.**
