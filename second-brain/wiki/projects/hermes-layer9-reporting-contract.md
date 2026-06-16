# Layer 9 — Reporting Contract

**Datum:** 2026-06-16
**Status:** L9A reporting contract
**Commit:** `581ad940` feat(layer9): add validation snapshot MVP

---

## Waarom deze regel nodig is

L9A rapporteert metingen, geen interpretatie. Het vorige readback-rapport over SOLEUR 60m bevatte zinnen die niet direct terug te voeren waren op outputvelden:

- "bullmarkt" — niet gemeten in L9A
- "Hermes zag" — anthropomorfisme, Hermes berekent alleen
- "L9A bewijst" — één snapshot bewijst niets
- "SOL bleef sterker dan BTC/ETH" — future BTC/ETH zijn niet gemeten in L9A

L9-reporting moet **droog** zijn. Alleen wat er staat in L6, L8 en future_outcomes.

---

## Verboden taal

| Zin | Waarom verboden |
|-----|----------------|
| bullmarkt / bearmarkt | Niet gemeten in L9A. Geen bull/bear definitie in output. |
| Hermes zag / dacht / besloot | Anthropomorfisme. Hermes berekent, niet ziet. |
| bewijst / toont aan / bevestigt | Eén snapshot is onvoldoende voor bewijs. |
| bleef sterker dan BTC/ETH (in future) | Future BTC/ETH return niet gemeten in L9A. |
| trend zet door | Interpretatie. L9 output geeft `did_continue_direction` zonder causaliteit. |
| sterke setup / zwakke setup | Setup-taal. L9 is geen setup-detector. |
| signaal / setup / trade / entry / exit | Verboden per L9 contract. |
| koop / verkoop / long / short | Verboden per L9 contract. |
| verwachting / vermoedelijk / waarschijnlijk | L9 doet geen voorspelling. |

---

## Toegestane taal

| Zin | Waarom toegestaan |
|-----|-------------------|
| "L8 output: `field` = `value`" | Direct uit outputveld. |
| "L6 output: `field` = `value`" | Direct uit outputveld. |
| "Future next_N candles: return_pct = X" | Direct uit outputveld. |
| "`did_continue_direction`: true/false" | Direct uit outputveld. |
| "Deze snapshot toont één meting." | Correcte kwalificatie. |
| "Niet gemeten in L9A: ..." | Eerlijke begrenzing. |
| "Buiten L9A scope: ..." | Eerlijke begrenzing. |

---

## Correct voorbeeld — SOLEUR 60m

### Input

```
Snapshot-index: 179
Visible candles: 180 (0..179)
Future candles beschikbaar: 20 (180..199)
```

### L8 output

```
pair_return_pct:         +10.46%
btc_return_pct:          +4.61%
eth_return_pct:          +5.69%
pair_direction:          up
direction_alignment:     aligned_with_benchmark
relative_behavior:       stronger_than_benchmarks
market_wind:             benchmark_up
```

### L6 output

```
micro_state:             rejection_like
body_trend:              expanding
dominant_pattern:        medium_body
last_3_sequence:         bullish-bearish-bullish
```

### Future outcomes (SOL only)

```
next_3:  return +1.68%,  continue true
next_5:  return +4.05%,  continue true
next_10: return +2.74%,  continue true
next_20: return +2.72%,  continue true
```

### Correcte tekst

```
Deze snapshot toont één meting.
Op snapshot_index 179 rapporteerde L8 dat SOLEUR over het L8-venster
sterker was dan BTC/ETH (relative_behavior: stronger_than_benchmarks,
pair +10.46% vs BTC +4.61%, ETH +5.69%).
L6 rapporteerde micro_state rejection_like, body_trend expanding.

Daarna stegen de gemeten SOLEUR future candles in alle vier de windows
(next_3 +1.68%, next_5 +4.05%, next_10 +2.74%, next_20 +2.72%).
Alle windows complete.

BTC/ETH future outcomes zijn niet gemeten in L9A.
Deze snapshot zegt niets over volgende of eerdere metingen.
```

---

## Harde reporting-regel

```
L9 rapporteert metingen, geen interpretatie.
Elke zin moet direct terug te voeren zijn op een outputveld.
Als een conclusie extra data vereist (bv. future BTC/ETH return,
statistische spreiding, meerdere snapshots), moet L9 zeggen:
"niet gemeten" of "buiten L9A scope".
```

---

## Freeze-regel

Alle toekomstige L9A readbacks moeten deze reporting-regel volgen.

Als Hermes interpretatieve taal gebruikt in een L9-rapport, is het rapport fout — ook als de code en tests groen zijn.

Corrigeren (geen nieuwe code), her-rapporteren (geen nieuwe metingen).
