# Audit — S/R bucket fix simulatie

**Datum:** 2026-06-13
**Status:** Geen production code gewijzigd, geen commit

---

## 1. Simulatiemethode

- Oude bucket: `round(price / 20) * 20`
- Nieuwe bucket: `round(price / (close * 0.0025)) * (close * 0.0025)`
- Zelfde pivots, zelfde candles, zelfde swing detectie als v2 S/R route
- Enkel read-only simulatie

## 2. Resultaten per pair/timeframe

| Pair | TF | Old unique | New unique | Old issue | New result | Impact |
|---|---|---|---|---|---|---|
| **BTCEUR** | 240m | 37 | 32 | OK | OK — 0.04%→0.25% | NO_CHANGE |
| **BTCEUR** | 60m | 38 | 21 | OK | Iets grover, nog OK | SMALL_CHANGE |
| **BTCEUR** | 15m | 26 | 8 | OK | Grover cluster | SMALL_CHANGE |
| **BTCEUR** | 5m | 18 | 4 | OK | Grover, max 24 pivots/bucket | SMALL_CHANGE |
| **ETHEUR** | 60m | 8 | 20 | COARSE | 20 unieke levels ✅ | IMPROVES |
| **ETHEUR** | 15m | 3 | 10 | COARSE | 10 unieke levels ✅ | IMPROVES |
| **ETHEUR** | 5m | **1** | **5** | ALL_IN_1 | 5 levels, max 26/bucket ✅ | **FIXES** |
| **SOLEUR** | 60m | **1** | **26** | ALL_IN_1 | 26 levels ✅ | **FIXES** |
| **SOLEUR** | 15m | **1** | **14** | ALL_IN_1 | 14 levels ✅ | **FIXES** |
| **SOLEUR** | 5m | **1** | **7** | ALL_IN_1 | 7 levels ✅ | **FIXES** |
| **ADAEUR** | 60m | **1** | **28** | ALL_IN_1 (bucket=0) | 28 levels ✅ | **FIXES** |
| **ADAEUR** | 15m | **1** | **17** | ALL_IN_1 (bucket=0) | 17 levels ✅ | **FIXES** |
| **ADAEUR** | 5m | **1** | **11** | ALL_IN_1 (bucket=0) | 11 levels ✅ | **FIXES** |
| **PEPEEUR** | 60m | **1** | **16** | ALL_IN_1 (bucket=0) | 16 levels ✅ | **FIXES** |
| **PEPEEUR** | 15m | **1** | **10** | ALL_IN_1 (bucket=0) | 10 levels ✅ | **FIXES** |
| **PEPEEUR** | 5m | **1** | **6** | ALL_IN_1 (bucket=0) | 6 levels ✅ | **FIXES** |

## 3. Waar zichtbaar in routes

| Route | S/R render? | Verandert? | Meest zichtbaar |
|---|---|---|---|
| `/v2/sr/<pair>` | ✅ Ja | ✅ Ja | ETH 5m, SOL, ADA, PEPE |
| `/v5/structure-cockpit` | ✅ Ja | ✅ Ja | SOL, ADA, PEPE paneel |
| `/chart/<pair>` (v1 mode) | ❌ Nee | ❌ Nee | — |
| Director/testbot/tradebot | ❌ Nog niet | ❌ Nvt | — |

## 4. Risicoanalyse

| Vraag | Antwoord |
|---|---|
| Zou 0.25% BTC kapot maken? | **Nee** — BTC blijft OK, enkel iets grovere clusters (0.04%→0.25%) |
| Zou 0.25% ETH verbeteren? | **Ja** — 5m van 1 naar 5 unieke buckets |
| Zou 0.25% low-price pairs bruikbaar maken? | **Ja** — SOL/ADA/PEPE van 1 nutteloze bucket naar 6-28 levels |
| Is 0.25% te fijn of te grof? | **Goudlokje** — niet te fijn, niet te grof. BTC/ETH behouden levels, SOL/ADA/PEPE krijgen levels |
| Is 0.50% beter? | **Nee** — 0.25% is al goed genoeg voor low-price; 0.50% zou BTC/ETH te grof maken |
| Moeten we clampen met min/max? | **Optioneel** — min 0.000001 voor PEPE, max geen nodig |
| reference_price = last close veilig? | **Ja** — close is consistent over de candle set |

## 5. Advies voor latere patch

**Fix doen: Ja.** Veilig, simpel, enkel sr_block.py.

### Minimale patch

```
File: projects/hermes-v01/layer2_structure_v2/sr_block.py

Helper toevoegen:
    def _bucket_key(price, ref_price, bucket_pct=0.0025):
        bs = max(ref_price * bucket_pct, 1e-10)
        return round(price / bs) * bs

Alle 6 plaatsen:
    round(price / 20) * 20
    → _bucket_key(price, close_of_candle_window)
```

### Visueel opnieuw testen na patch

- BTCEUR 5m/60m — controleer of levels niet te grof zijn
- ETHEUR 5m — moet 5+ levels tonen ipv 1
- SOLEUR 5m — moet 7+ levels tonen ipv 1
- ADAEUR 60m — moet 28 levels tonen ipv bucket=0
- PEPEEUR 60m — moet 16 levels tonen ipv bucket=0
- V5 cockpit BTCEUR/SOLEUR/ADAEUR — S/R moet kloppen

### Risico's

- BTC: SMALL_CHANGE — 37→32/38→21 levels. Nog OK, maar 60m en 5m worden grover
- ETHEUR/15m: ook grover (3→10 is nog steeds OK)
- **Geen risico op crashes** — enkel rendering verandert
- **Rollback**: `git revert` op sr_block.py

## 6. Conclusie

**0.25% bucket is de juiste fix.** Werkt voor alle pairs zonder config.
Fix is veilig, klein (1 file, 6 regels), en lost alle problemen op.
