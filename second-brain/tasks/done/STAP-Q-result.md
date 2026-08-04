---
type: result
task: STAP-Q
created: 2026-05-30
status: completed
---

# STAP Q — V3A Kandidaatbeoordeling

## Volledig rapport

```
============================================================
  V3A KANDIDAATBEOORDELING — 2026-05-30
============================================================

  Criterium 1 — Consistentie over pairs:  SLAAGT NIET
    1/7 pairs ≥ 40.0% WR
    ❌ ETHEUR     12.5%
    ❌ BTCEUR     0.0%
    ❌ SOLEUR     0.0%
    ❌ ADAEUR     0.0%
    ✅ XRPEUR     50.0%
    ❌ LINKEUR    0.0%
    ❌ INJEUR     33.3%

  Criterium 2 — Parameterstabiliteit:  SLAAGT
    Gem. WR spread: 13.4%  Max: 66.7%

  Criterium 3 — Paper/backtest alignment:  SLAAGT NIET
    Overlap: 0.0%  (backtest=8, paper=0)
    → live_cache dekt de backtest-periode niet

  Criterium 4 — Exit potentieel (MFE/L):  SLAAGT
    MFE verliezers max: 2.90% (V1)
    Exit verbetering max: +304% (V1: -18% → +36.88%)

  ────────────────────────────────────────────────────────────
  EINDOORDEEL: NIET KLAAR
  Aanbeveling: Eerst fixes nodig

  Score: 2/4 slaagt  2/4 faalt  0/4 onbekend
============================================================
```

## Analyse per criterium

### Criterium 1 — Consistentie (SLAAGT NIET)
V3A haalt enkel op XRPEUR een WR ≥ 40%. De meeste pairs (ETHEUR, BTCEUR, SOLEUR, ADAEUR, LINKEUR) scoren 0-12.5%. Dit kan komen doordat:
- Het archief te weinig data heeft voor sommige pairs
- V3A enkel onder specifieke marktcondities werkt die niet universeel voorkomen
- De pendelde markten van de laatste weken ongunstig zijn voor pullback-strategieën

### Criterium 2 — Stabiliteit (SLAAGT)
Gemiddelde WR spread van 13.4% is onder de 15%-drempel. Maar INJEUR heeft 66.7% spread (strikt 100% WR op 1 trade). De "stabiliteit" is deels een artefact van te kleine samples.

### Criterium 3 — Alignment (SLAAGT NIET)
Paper vs backtest vergelijking is niet mogelijk omdat live_cache enkel de laatste uren dekt en de backtest-signalen van 19-20 Mei dateren. Structureel probleem met de data-architectuur.

### Criterium 4 — Exit potentieel (SLAAGT)
V1 en V2 hebben significante MFE-giveback (verliezers waren ooit +2.90% / +1.33% in winst). Exit simulatie toont dat trailing stops historisch V1 van -18% naar +36.88% brengen.

## Conclusie

V3A is **NIET KLAAR** voor live paper trading. De strategie produceert te weinig signalen op de meeste pairs en de data-brug tussen backtest en live is onvoldoende.

**Aanbevolen fixes:**
1. Onderzoek waarom V3A zo weinig signalen geeft (data-periode vs marktconditie)
2. Fix de paper-vs-backtest data-brug (live_cache langer bewaren)
3. Overweeg of V3A enkel op ETHEUR/XRPEUR/INJEUR moet draaien