# Audit — Layer 2 v02 S/R bucket=20 impact

**Datum:** 2026-06-13
**Status:** Geen code gewijzigd

---

## 1. Exacte codeplaatsen

Alle bucket-logica zit in `layer2_structure_v2/sr_block.py`:

| Regel | Code | Functie |
|---|---|---|
| 11 | `key = round(bh / 20) * 20` | `_gather_candidates` — swing highs |
| 18 | `key = round(bl / 20) * 20` | `_gather_candidates` — swing lows |
| 29 | `pivot_prices.add(round(price / 20) * 20)` | pivot markering |
| 33 | `pivot_prices.add(round(max(...) / 20) * 20)` | pivot markering (body high) |
| 36 | `pivot_prices.add(round(min(...) / 20) * 20)` | pivot markering (body low) |

**Hardcoded `20` — 0 parameters, 0 config, 0 pair-awareness.**

## 2. Gebruikspaden

| Wie | Wat | Actief? |
|---|---|---|
| `chart_engine.py` (v2 mode) | `draw_sr_zones()` | ✅ Ja — via `/v2/sr/` route |
| `structure_cockpit.py` (V5) | `draw_sr_zones()` | ✅ Ja — via `/v5/` |
| `director` | Geen S/R output | ❌ Nee |
| testbot/tradebot | Niet direct | ❌ Nog niet |

**Momenteel:** enkel visual rendering. Geen structurele output voor testbot/tradebot.

## 3. Pair-impact tabel

| Pair | TF | Close | Bucket% | Uniq buckets | Impact |
|---|---|---|---|---|---|
| **BTCEUR** | 240m | 55280 | **0.04%** | 37/37 | ✅ OK |
| **BTCEUR** | 60m | 55280 | **0.04%** | 38/43 | ✅ OK |
| **BTCEUR** | 5m | 55280 | **0.04%** | 18/45 | ✅ OK |
| **ETHEUR** | 240m | 1450 | **1.38%** | 21/42 | ⚠️ COARSE |
| **ETHEUR** | 60m | 1450 | **1.38%** | 8/42 | ⚠️ COARSE |
| **ETHEUR** | 5m | 1450 | **1.38%** | **1/53** | ❌ ALL_IN_1 |
| **SOLEUR** | 60m | 58.68 | **34.08%** | **1/42** | ❌ ALL_IN_1 |
| **ADAEUR** | 60m | 0.15 | **13344%** | **1/43** | ❌ ALL_IN_1 |
| **PEPEEUR** | 60m | 0.0000 | **812M%** | **1/47** | ❌ ALL_IN_1 |

## 4. Conclusie per pair

- **BTCEUR:** bucket=20 is 0.04% — uitstekend, ~37 unieke levels ✓
- **ETHEUR:** bucket=20 is 1.38% — te grof. Op 5m alle 53 pivots in 1 bucket ✗
- **SOLEUR:** bucket=20 is 34% — alle pivots in bucket 60 ✗
- **ADAEUR/PEPEEUR:** bucket=20 is >10000% — alle pivots in bucket 0, compleet nutteloos ✗

## 5. Visual-only of structureel?

**Visual-only, maar met risico.**

- Momenteel: enkel `draw_sr_zones()` gebruikt de buckets — zuiver rendering
- In de toekomst (testbot/tradebot/assessment): S/R levels als data-output gaan dit wél gebruiken
- **Advies:** fix vóór L8 (assessment), want assessment heeft correcte S/R nodig

## 6. Hypothethische alternatieven (niet gebouwd)

| Aanpak | BTC 60m | ETH 60m | ADA 60m | PEPE 60m |
|--------|---------|---------|---------|----------|
| Hardcoded 20 | 0.04% ✅ | 1.38% ⚠️ | 13344% ❌ | 812M% ❌ |
| **0.25% van prijs** | ~138 ✅ | ~3.6 ✅ | ~0.0004 ✅ | ~0.00000006 ✅ |
| **0.5× ATR** | ~var ✅ | ~var ✅ | ~var ✅ | ~var ✅ |

**Percentage-based (bv 0.25% van prijs) is de simpelste correcte fix.** Werkt voor alle pairs zonder config.

## 7. Advies

**Scenario A — fix is nodig, maar niet urgent.**

- Fix nodig? **Ja**
- Vóór L6? **Nee** — L6 is candle micro, heeft geen S/R nodig
- Vóór L7/L8? **Ja** — assessment heeft correcte S/R nodig
- Minimale files voor fix: `layer2_structure_v2/sr_block.py`
- Fix: `round(price / 20) * 20` → `round(price / (price * 0.0025)) * (price * 0.0025)` of equivalent in 1 centrale functie
- Risico: laag — enkel visual rendering, breekt niks
- Geen code gewijzigd in deze audit
