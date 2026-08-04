# ADR — SNAPSHOT READOUT LOCATION

**Datum:** 2026-07-09
**Status:** Accepted

## 1. Context

L4 snapshots bevatten genoeg informatie voor betrouwbare context-readout:
- current/previous price-context
- indicators
- candle_micro
- structure
- support/resistance
- trendlines
- source/provenance

Maar L4 snapshots bevatten NIET:
- volledige 240-candle-array
- regime, bias, MTF alignment
- outcome, tradebeslissing

Het Readout Contract v2 legt vast dat Hermes context mag beschrijven, maar geen trades mag beslissen.

## 2. Probleem

Snapshot Readout zit op de grens tussen data inspecteren en betekenis geven.

Als readout stilletjes onder interpreter wordt gebouwd, vervaagt de grens tussen geheugen en analyse. Dat willen we vermijden.

## 3. Beslissing — Optie B

Snapshot Readout wordt NIET onder interpreter gebouwd.

**Snapshot Readout wordt conceptueel Analyst A0.**

A0 mag:
- read-only snapshots lezen
- marktcontext beschrijven
- S/R benoemen
- structure benoemen
- indicatorvelden benoemen
- candle_micro benoemen
- onzekerheden tonen
- zeggen wat de snapshot NIET bewijst

A0 mag niet:
- candidate maken
- score geven
- setup beoordelen
- long/short zeggen
- entry/exit geven
- buy/sell zeggen
- trade confidence geven
- voorspellen

## 4. Laagindeling

```
Interpreter (data/geheugen)
├── OHLC/snapshot opslag
├── L1-L4 data verwerking
├── raw blobs
├── source/provenance
├── inspector
└── integrity/audit tools

Analyst A0 (beschrijvende betekenis)
├── Snapshot Readout
├── geen oordeel
├── geen candidate
└── geen scoring

Analyst A1+ (contextweging, later)
├── MTF alignment
├── setup/no_setup
├── candidate/no_candidate
└── pas na outcome/backtest basis

Trader (executie, veel later)
├── paper trading
├── execution
├── risk sizing
└── pas na aparte contracten
```

## 5. Gevolgen

**Voordelen:**
- Interpreter blijft zuiver data/geheugen
- Readout wordt niet per ongeluk tradinglogica
- Analyst krijgt een veilige poortlaag
- Latere scoring blijft gescheiden van beschrijving
- Minder kans op grensvervaging

**Nadelen:**
- Extra architectuurstap vóór prototype
- Later mogelijk aparte directory nodig
- Readout-code nog niet gebouwd

## 6. Voorlopige toekomstige locatie

Nog geen directory maken. Conceptuele locatie later:

```
projects/hermes-v03-analyst/a0_snapshot_readout/
```

of:

```
projects/hermes-analyst/a0_snapshot_readout/
```

Niet nu uitvoeren.

## 7. Wat dit besluit NIET doet

- Geen code bouwen
- Geen prototype bouwen
- Geen Analyst, L5, Trader bouwen
- Geen Strategy Test, Outcome Builder
- Geen DB schema wijzigen
- Geen raw_hash, dedup wijzigen
- Geen service/timer, OHLC bridge wijzigen
- Geen L4 core wijzigen
- Geen interpreter contract.md wijzigen

## 8. Volgende stap later

Na dit ADR mag de volgende sessie starten met: **A0 Snapshot Readout Prototype Plan.** Maar alleen als aparte stap, zonder tradebeslissingen.

## 9. Conclusie

Snapshot Readout hoort conceptueel bij Analyst A0, niet bij de interpreter.

Interpreter blijft geheugen/data. A0 Readout wordt beschrijvende betekenis. Analyst A1+ wordt latere weging. Trader komt veel later.
