# Audit — Layer 4a Recent Active Trendline

**Datum:** 2026-06-13
**Status:** Audit-only — geen code gewijzigd

---

## 1. Huidige Layer 4 functies en verantwoordelijkheden

Layer 4 zit in `layer4_trendline_lab/trendline_lab.py` (554 lijnen) en bestaat uit:

| Functie | Doel | Geschikt voor Layer 4a? |
|---|---|---|
| `fetch_and_prepare()` | Haalt candles + swing highs/lows op | ✅ Ja |
| `_select_points()` | Selecteert max N meest recente swing points | ✅ Ja, maar nu max 15 |
| `select_upper_points()` | Wrapper voor highs | ✅ Ja |
| `select_lower_points()` | Wrapper voor lows | ✅ Ja |
| `_generate_candidates()` | Alle paren van 2 swing points | ✅ Ja, maar nu alle combinaties |
| `_validate_candidate()` | Body violations, touch count, recency | ✅ Ja |
| `validate_upper/lower_candidate()` | Wrappers | ✅ Ja |
| `_pick_top()` / `pick_top_*()` | Score en selectie | ✅ Ja, bonuslogica aanpasbaar |
| `classify_swing_high/low_structure()` | HH/HL/LH/LL/EH/EL labels | ⚠️ Niet direct nodig |
| `_render_line()` | Teken lijn op chart | ✅ Ja |
| `build_trendline_lab_chart()` | Volledige chart build | ❌ Te veel, aparte render nodig |

---

## 2. Welke Layer 4 stukken zijn herbruikbaar

**Volledig herbruikbaar zonder wijziging:**
- `fetch_and_prepare()` → levert candles + swing_highs + swing_lows
- `_validate_candidate()` → body violation + touch + recency checks
- `validate_upper_candidate()` / `validate_lower_candidate()` → wrappers
- `calculate_median_range()` → voor toleranties
- `inspect_strengths()` → diagnostics
- `_render_line()` → teken 1 lijn

**Aanpasbaar herbruikbaar:**
- `_select_points()` → nu max 15 punten over hele chart. Layer 4a = max 5 vanuit laatste swing
- `_generate_candidates()` → nu alle paren. Layer 4a = enkel laatste → vorige
- `_validate_candidate()` → recency check kan losser of anders. Body violation check perfect
- `pick_top_upper_candidates()` / `pick_top_lower_candidates()` → bonuslogica ok, maar anders voor recent

---

## 3. Welke Layer 4 stukken zijn NIET geschikt

| Functie | Waarom niet |
|---|---|
| `build_trendline_lab_chart()` | Volledige Fase A/B chart — te zwaar voor enkel recente lijnen |
| `classify_swing_high/low_structure()` | HH/HL/LH/LL is Layer 4 major structuur, niet nodig voor recent |
| `_render_structure_labels()` | Idem — structuurlabels niet nodig voor Layer 4a |
| `pick_top_upper_candidates()` bonus (dalend) | Layer 4a recent upper mag ook stijgend zijn (local bounce) |

---

## 4. Beoordeling idee: “laatste swing + max 5 vorige”

**Werkt voor:**
- **5m** ✅ — 5-6 swings dekken ~50-100 candles (4-8 uur). Perfect voor recente actieve lijn
- **15m** ✅ — 5-6 swings dekken ~75-150 bars. Nog steeds recent genoeg
- **60m** ⚠️ — 5-6 swings = 5-6 dagen. Layer 4 major is hier al goed. Layer 4a optioneel
- **240m** ❌ — Layer 4 major blijft dominant. Layer 4a niet nodig

**Probleem met “max 5”:**
- Als er maar 2-3 swings zijn: nog steeds geldig — gewoon minder candidates
- Als swing detection te weinig punten geeft: Layer 4a kan niks doen (correct)
- De “laatste swing” is de meest recente bevestigde high/low — NIET de open candle

**Voorstel max lookback:**

| TF | Max points | Reden |
|---|---|---|
| 5m | 5 | 5 swings ~ 4-8 uur, ideaal voor daghandel |
| 15m | 5 | 5 swings ~ 1-2 dagen |
| 60m | 6-8 | Optioneel, langere lookback voor context |
| 240m | n.v.t. | Layer 4 major blijft dominant |

---

## 5. Advies: Layer 4a of Layer 6?

**Layer 4a in `layer4_trendline_lab/recent_trendline.py`** — ✅

Redenen:
- Hergebruikt `fetch_and_prepare()`, `_validate_candidate()`, `_render_line()` direct uit Layer 4
- Geen kruisende imports (Layer 6 zou Layer 4 moeten importeren — onlogisch)
- Logisch: Layer 4 = major + recent, in 1 directory
- Apart bestand `recent_trendline.py` blijft proper gescheiden van `trendline_lab.py`

Layer 6 blijft voor **actieve microstructure** (anders dan trendlines).

---

## 6. Voorstel modulepad

```
projects/hermes-v01/layer4_trendline_lab/
├── __init__.py
├── trendline_lab.py          (bestaand — major)
└── recent_trendline.py       (nieuw — Layer 4a)
```

---

## 7. Voorstel outputcontract

```python
{
    "pair": "BTCEUR",
    "timeframe": "5m",
    "recent_upper": {
        "p1": {"index": 145, "wick_price": 55171.0, "label": "HH7"},
        "p2": {"index": 184, "wick_price": 54976.0, "label": "EH2"},
        "slope": -5.38,       # punten per candle
        "projected_now": 54950.0,
        "touches": 2,
        "score": 65,
        "status": "active"
    } or None,
    "recent_lower": { ... } or None,
    "recent_trend": "down",         # "up" | "down" | "squeeze" | "unclear"
    "status": "active",             # "active" | "weak" | "broken" | "conflict" | "none"
    "anchors": {
        "upper": {
            "last": {"index": 184, "wick": 54976.0, "label": "EH2"},
            "lookback_points": 5
        },
        "lower": {
            "last": {"index": 194, "wick": 54936.6, "label": "HL9"},
            "lookback_points": 5
        }
    },
    "reason": "recent upper through last 2 swing highs, 2 touches, active",
    "candles_since_anchor": 15
}
```

---

## 8. Validatieregels

Hetzelfde als Layer 4 `_validate_candidate()`:
- Body violation ratio ≤ 0.35
- Price side ratio ≤ 0.30
- Body cut ratio ≤ 0.35
- Min 1 extra touch (total ≥ 3 voor recent)
- **Geen recency check op "since last touch"** — bij recente lijn is dat logischerwijs recent

**Verschil met Layer 4:**
- Lichter: minder punten → minder candidates → sneller
- Strenger op body violations: recente lijn moet strakker zijn
- Geen recency rejection als >50 candles (recente lijn = per definitie recent)
- Bonus voor stijgende lower en dalende upper (zelfde als Layer 4)

---

## 9. Timeframe-regels

| TF | Points | Actief? |
|---|---|---|
| 5m | 5 | ✅ Altijd |
| 15m | 5 | ✅ Altijd |
| 60m | 6-8 | ⚠️ Optioneel, enkel als Layer 4 major unclear |
| 240m | - | ❌ Niet nodig |

---

## 10. Risico's

| Risico | Impact | Mitigatie |
|---|---|---|
| Te weinig swings door wick fix | Layer 4a geeft None — correct gedrag | Acceptabel |
| Body violations op recente volatile move | Lijn wordt weak/broken — correct | Acceptabel |
| Laatste swing is net geprint en nog niet bevestigd | Gebruik enkel bevestigde SwingPoints — die hebben `strength > 0` | Filter op strength |
| Overbodig op 60/240m waar Layer 4 al werkt | Niet renderen tenzij Layer 4 unclear | Config-optie |
| Dubbele render op 5m (Layer 4 + Layer 4a) | Aparte toggle in cockpit | Show/hide flag `show_recent_trend` |

---

## 11. Testcases waarop dit nodig is

Op basis van eerdere diagnostic op BTCEUR 5m:
```
#  Idx    Label     Wick
 14  120      LH9  54981.90
 15  126      EH1  54993.40
 16  134      HH6  55044.60
 17  144      HH7  55171.00    ← HIGH punt, maar 55 candles oud → Layer 4 rejected
 18  156     LH10  55076.60
 19  167     LH11  54944.20
 20  177      HH8  55018.70
 21  181     LH12  54963.00
 22  184      EH2  54976.00    ← LAATSTE swing high
```

Layer 4 kon deze niet pakken omdat HH7 te oud was (55 > 50 recency).
Layer 4a zou:
1. Laatste swing high = EH2 (184, 54976)
2. 5 vorige: HH8, LH11, LH10, HH7, LH9
3. Candidate: EH2 → HH7 (stijgend!) = recente trend, net 2 touches
4. Candidate: EH2 → HH8 (dalend) = recente weerstand
5. Validatie: body violations op recente candles checken

**Doel:** recentere lijn die niet 55 bars teruggaat, maar enkel de laatste 5 swings gebruikt.

---

## 12. Advies: bouwen ja/nee

**Ja, bouwen**, maar met deze grenzen:

1. Maak `layer4_trendline_lab/recent_trendline.py`
2. Hergebruik `fetch_and_prepare()` uit `trendline_lab`
3. Nieuwe candidate generatie: enkel laatste swing → vorige max 5
4. Hergebruik `_validate_candidate()` (zelfde body checks)
5. Recency check uitzetten (recente lijn = per definitie recent)
6. Score aanpassen voor korte span
7. Output via `read_layer4a(pair, tf)` in director
8. Apart renderen — geen visual impact op Layer 4

**Niet doen in eerste versie:**
- Geen structuur labels (HH/HL)
- Geen visuele cockpit integratie
- Geen trade signals
- Geen forced channel
- Geen 60/240m

---

## 13. Voorstel volgende prompt

```
BUILD — Layer 4a Recent Active Trendline module

Maak:
projects/hermes-v01/layer4_trendline_lab/recent_trendline.py

Gebruik:
- fetch_and_prepare() uit trendline_lab.py
- _validate_candidate() / validatie uit trendline_lab.py
- geen nieuwe imports naar director/v02

Algoritme recent upper:
1. select_upper_points met max_points=6 (laatste swing + 5 vorige)
2. candidate pairs: laatste swing → elk van de 5 vorige
3. validate via bestaande validate_upper_candidate()
4. pick beste (score, meeste touches)
5. return dict of None

Algoritme recent lower: symmetrisch.

Voeg read_layer4a() toe aan director/hermes_director.py.
Render optioneel via aparte functie.

Geen Layer 4 major aanraken.
Geen V5 cockpit wijzigen.
```
