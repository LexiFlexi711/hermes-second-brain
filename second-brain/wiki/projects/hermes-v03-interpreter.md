---
title: "Hermes-v03-interpreter — apart project naast Hermes-v03"
type: project
status: draft
date: 2026-06-29
tags: [hermes, interpreter, trading, architectuur]
---

## Concept

**Hermes-v03** is de lezer — produceert JSON met chart-structuur.
**Hermes-v03-interpreter** is het brein — leest de JSON en beslist wat het betekent voor de trade.

Volledig losstaand project. Geen code-imports naar Hermes-v03. Enkel JSON als contract.

## Directory

`/mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/projects/hermes-v03-interpreter/`

```
hermes-v03-interpreter/
├── contract.md                    # Datacontract tussen v03 en interpreter
├── L1_validate/                   # Ingangslaag — valideert JSON
│   └── __init__.py                # validate() — vorm/type/versie-check
└── (later: L2_..., core, ...)
```

## Contract

- **Additief mag, muteren niet.** v03 mag velden bijvoegen, nooit stille breaking changes.
- **Interpreter leest defensief.** Get-met-default, nooit crashen op extra velden.
- **Versie-stempel.** `meta.schema_version` (nu versie 1) telt op bij breaking changes.
- **De knip is heilig.** Interpreter krijgt enkel JSON, nooit directe toegang tot Hermes-v03.

Zie `contract.md` voor het volledige contract.

## Status

- ✅ `schema_version: 1` toegevoegd aan Hermes-v03 L8_synthesis
- ✅ `contract.md` geschreven met volledig datacontract
- ✅ `L1_validate` geschreven en getest (5/5 tests geslaagd)
- ⬜ L2_... (interpretatie-lagen)
- ⬜ Interpreter core
- ⬜ MTF-weging

## Validatie

L1_validate test resultaten (2026-06-29):
- Geldige JSON: ✅ valid=True
- Error passthrough: ✅ valid=False + reden
- Onbekende versie: ✅ valid=False + "ondersteunt enkel versie 1"
- Ontbrekend blok: ✅ valid=False + "levels ontbreekt"
- Geen schema_version: ✅ valid=False + "pre-contract JSON"

## Bronnen

- `contract.md` in project directory
- `L1_validate/__init__.py` — validate implementatie
- Hermes-v03 `L8_synthesis/__init__.py` (lijn 140: `"schema_version": 1`)
