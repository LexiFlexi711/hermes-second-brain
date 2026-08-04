---
stap: E
naam: v3a-strategy-klasse
status: done
uitgevoerd-door: Hermes
datum: 2026-05-29
---

## Wat gedaan

V3AStrategy als Strategy subklasse aangemaakt in nieuw bestand:
`strategies/v3a/strategy.py`

- 5 check-functies: `_check_trend`, `_check_pullback`, `_check_fib`, `_check_structure`, `_check_trigger`
- `compute_checks()` en `build_signal()` interface geïmplementeerd
- Aggregator (gate mode) voor go/no-go
- SL/TP berekening via `calc_sl_tp()` uit logic.py
- RR check voor minimum risk/reward

## Testresultaat

```bash
V3AStrategy is Strategy subclass OK
Initialisatie OK
Geen signaal op BTCEUR (normaal — markt voldoet niet aan criteria)
compute_checks keys OK: ['trend', 'pullback', 'fib', 'structure', 'trigger']
Alle V3AStrategy tests OK
```

Bestaande tests: 9 passed ✅

## Afwijkingen
Pyright LSP errors (4 stuks) zijn valse positieven — functies bestaan wel met juiste params. Runtime werkt.

## Aangeraakte bestanden
- NIEUW: `strategies/v3a/strategy.py` ✅
- GEEN bestaande bestanden gewijzigd ✅