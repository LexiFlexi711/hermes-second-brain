# AUDIT 1 — vind_fractalen() BODEM-ANKERS BODY-LOW VS WICK-LOW

**Datum:** 2026-06-13
**Uitvoerder:** Noa (Hermes)
**Pair:** BTCEUR 240m
**Status:** ✅ Audit voltooid — geen code gewijzigd, geen commit

---

## 1. git status vóór audit

```
M projects/hermes-v01/layer1_charts/chart_engine.py
 M projects/hermes-v01/layer2_structure/hermes_v01.py
 M projects/hermes-v01/tests/test_hermes_v01_structure_edges.py
 M projects/hermes-v01/tests/test_structure_roles.py
```

Er waren al modified files vóór audit. Niet opgeruimd.

---

## 2. Locatie van vind_fractalen()

| Bestand | Regel | Type |
|---|---|---|
| `layer2_structure/hermes_v01.py` | 80 | body: `min(open, close)` voor bodems, `max(open, close)` voor toppen |
| `layer2_structure/hermes_v02.py` | 89 | wick: `candles[i]["low"]` voor bodems, `candles[i]["high"]` voor toppen |

**v02 is correct. v01 is foutief (body-only).**

---

## 3. Exacte regels waar high/low gekozen worden

**hermes_v01.py, lijn 84-89:**
```python
if is_fractaal_top(candles, i, n):
    result.append(Fractal(index=i, prijs=max(candles[i]["open"], candles[i]["close"]), type="top",  # ← BODY HIGH
                          timestamp=candles[i].get("timestamp", 0)))
if is_fractaal_bodem(candles, i, n):
    result.append(Fractal(index=i, prijs=min(candles[i]["open"], candles[i]["close"]), type="bodem",  # ← BODY LOW
                          timestamp=candles[i].get("timestamp", 0)))
```

**Detectie** (is_fractaal_top/bodem) gebruikt wél correcte wick-extremes:
- `is_fractaal_top`: `candles[i]["high"]` (line 62)
- `is_fractaal_bodem`: `candles[i]["low"]` (line 73)

Detectie is correct. **Alleen de opgeslagen prijs is body-based.**

---

## 4. Conclusie: body-low of wick-low?

**v01 vind_fractalen() gebruikt body-low `min(open, close)` voor bodems.** ❌
**v02 vind_fractalen() gebruikt wick-low `low` voor bodems.** ✅

---

## 5. Volledige callgraph

### v01 versie wordt aangeroepen door:

| Bestand | Regel | Context |
|---|---|---|
| `layer2_structure/hermes_v01.py` | 159 | interne aanroep |
| `layer2_structure/hermes_v01.py` | 1345 | `read_structure()` — **centrale chart structuur lezer** |
| `layer2_structure/hermes_v01.py` | 1647 | interne aanroep |
| `layer1_charts/chart_engine.py` | 261 | `build_chart()` — **hoofd chart rendering** |
| `layer1_charts/structure_cockpit.py` | 37 | `_render_single_tf()` — **V5 structure cockpit** |
| `layer4_trendline_lab/trendline_lab.py` | 33 | `fetch_and_prepare()` — **Layer 4 trendline lab** |
| `layer2_structure/hermes_v02.py` | 323, 328 | `read_layer2()` importeert v01's functie |
| `layer2_structure/hermes_v02.py` | 351, 358 | `read_layer3()` importeert v01's functie |

### v02 versie wordt aangeroepen door:

| Bestand | Regel | Context |
|---|---|---|
| `layer2_structure/hermes_v02.py` | 265 | eigen interne aanroep |

### Experimenten die v01 of v02 gebruiken:

- `experiments/` — diverse research scripts importeren v02's correcte versie
- `experiments/research/` — gebruiken v02 voor channel/strategy analyse

---

## 6. Gebruikt huidige V5 flow deze functie?

**JA, rechtstreeks.**

`structure_cockpit.py` lijn 37:
```python
fractalen = vind_fractalen(candles)  # ← v01 body prices
toppen, bodems = _scheid_toppen_bodems(fractalen)
swing_highs = detect_swing_highs(toppen, candles, interval, label)
swing_lows = detect_swing_lows(bodems, candles, interval, label)
```

**MAAR:** `detect_swing_lows()` negeert de fractal `.prijs` en leest `cnd["low"]` rechtstreeks uit de candle (swing_points.py lijn 139). De swing points krijgen dus correcte wick prijzen.

**Echter:** De V5 cockpit gebruikt wél v01's fractal indices voor detectie. De swing detection is een tweede filter bovenop de fractals, en gebruikt de wick correct. Maar alle code die direct fractal `.prijs` consumeert (cluster_fractalen, bepaal_trend, etc.) krijgt body prices.

---

## 7. Gebruikt Layer 4 deze functie?

**JA, rechtstreeks.**

`trendline_lab.py` lijn 23, 33:
```python
from hermes_v01 import vind_fractalen, _scheid_toppen_bodems
# ...
fractalen = vind_fractalen(candles)
```

En vervolgens `detect_swing_lows()` in `swing_points.py` herleest `cnd["low"]` — dus ook hier wordt de correcte wick gebruikt voor swing points. Het fractal `.prijs`-veld wordt genegeerd in de swing detection pipeline.

---

## 8. Numerieke body-low vs wick-low vergelijking BTCEUR 240m

```
Totaal bodems gecheckt: 25
Waar wick_low < body_low: 15 (60.0%)
Waar wick_low == body_low: 10 (40.0%)

Grootste miss: 2026-06-04 00:00
  open=55199.90 high=55603.20 low=52854.40 close=55422.10
  body_low=55199.90 wick_low=52854.40 verschil=-2,345.50 EUR (-4.25%)

Alle laatste 15 bodems tonen wick_low < body_low (100% van recente data).
```

**Script:** `projects/hermes-v01/experiments/audit_fractal_low_body_vs_wick.py`
**Output:** zie hierboven (live Kraken data, zelfde source als V5 flow).

---

## 9. Auditchart

Niet gemaakt. Numeriek bewijs is voldoende duidelijk:
- 60% van ALLE bodems heeft wick_low < body_low
- 100% van de laatste 15 bodems heeft wick_low < body_low
- Grootste verschil: -2,345.50 EUR (-4.25%)

Visuele chart zou het patroon bevestigen maar voegt geen nieuwe informatie toe.

---

## 10. Impact op major lower

**DE IMPACT IS GROOT:**

De lower trendline in **v01's legacy flow** gebruikt fractal `.prijs` (body) voor:
- `find_best_swing_line()`: slope, touches, anchors ALL body-based
- `lower_trendlijn()`: slope, touches ALL body-based
- `active_lower()`: body prices
- `trend_bodems()`: body prices
- Laatste 2 bodems fallback: body prices

Omdat body_low ≥ wick_low (body_low is altijd hoger of gelijk), betekent dit:
- **Trendline is te hoog getekend** (optimistisch/flat bias)
- **Echte wick-low breekt de trendline vroeger dan verwacht**
- **Systeem mist 'false breakout' / trendbreak signalen**
- **Support levels zijn systematisch te hoog**

Concreet risico: lower trendline op BTCEUR 240m kan 100-2,345 EUR te hoog liggen, afhankelijk van candle.

---

## 11. Advies: fix nodig?

**JA, fix nodig.** Scenario B + D:

- **Scenario B:** v01 `vind_fractalen()` gebruikt body-low en huidige V5/trendline_lab importeren die functie
- **Scenario D:** Gemengd — v01's legacy flow (hoofd dashboard) gebruikt body prices direct; V5 cockpit en Layer 4 gebruiken wel correcte wick prices via swing detection, maar detectie-indices komen uit v01's fractals

**De fix heeft voorrang omdat:**
1. Het hoofd-dashboard (`/chart/<pair>`, `/chart/<pair>/<interval>`) gebruikt v01 legacy mode met body prices
2. 60% van alle bodems heeft foutieve body-low ipv wick-low
3. De trendline is systematisch te hoog
4. Breakout/breakdown detectie is te traag

---

## 12. Welke regel moet later aangepast worden?

**Eén regel in `hermes_v01.py` lijn 88:**

```python
# HUIDIG (fout):
result.append(Fractal(index=i, prijs=min(candles[i]["open"], candles[i]["close"]), type="bodem", ...))

# CORRECT:
result.append(Fractal(index=i, prijs=candles[i]["low"], type="bodem", ...))
```

**En ook lijn 85 voor consistentie (top):**
```python
# HUIDIG (fout):
result.append(Fractal(index=i, prijs=max(candles[i]["open"], candles[i]["close"]), type="top", ...))

# CORRECT:
result.append(Fractal(index=i, prijs=candles[i]["high"], type="top", ...))
```

---

## 13. Risico's

| Risico | Impact | Mitigatie |
|---|---|---|
| Trendlines verschuiven na fix | Verwachte gedragsverandering | A/B vergelijking met voor/na screenshots |
| Tests breken | Moeten bijgewerkt worden | Tests runnen na fix |
| Legacy scripts gebruiken body prices | Moeten mee veranderen | Alle interne calls gebruiken v01's functie |
| V5 cockpit (wick via swing) blijft werken | Geen impact | Swing detection leest wick uit candle, niet fractal `.prijs` |
| v02 heeft eigen correcte implementatie | Geen impact | v02 gebruikt al wick prices |

**Laagste risico:** Alleen de Fractal.prijs veranderen. De `is_fractaal_bodem()` detectie (die wick gebruikt) blijft ongewijzigd. Swing detection leest wick uit candle. Alleen directe `.prijs`-consumenten veranderen.

---

## 14. Bevestiging

- ✅ Geen code gewijzigd
- ✅ Geen commit gedaan
- ✅ Geen patch toegepast
- ✅ Geen refactor
- ✅ Alleen gelezen, bewijs verzameld, gerapporteerd
- ✅ Rapport geschreven naar `tasks/audit_1_vind_fractalen_body_vs_wick_BTCEUR_240m.md`

---

## Volgende stap (optioneel, niet uitgevoerd)

Indien gewenst:

```
FIX 1 — wijzig bodems in vind_fractalen() van body-low naar wick-low
```

Deze fix wijzigt exact 2 regels in `hermes-v01/layer2_structure/hermes_v01.py`:
- Lijn 85: `max(open, close)` → `candles[i]["high"]`
- Lijn 88: `min(open, close)` → `candles[i]["low"]`

En vereist:
1. Backup (`backups/before_wick_fix/`)
2. Tests runnen
3. Voor/na screenshots
4. Rapport validatie
