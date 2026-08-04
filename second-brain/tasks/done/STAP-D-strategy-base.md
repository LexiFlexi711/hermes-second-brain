---
stap: D
naam: strategy-base-en-aggregator
status: done
uitgevoerd-door: Hermes
datum: 2026-05-29
---

## Wat gedaan

Twee nieuwe bestanden aangemaakt:

1. **`strategies/base.py`** — `Strategy(ABC)` met `compute_checks()`, `build_signal()`, `evaluate()`
2. **`strategies/aggregator.py`** — `Aggregator` met `gate`, `score`, `mixed` modes

## Testresultaat

```bash
Strategy ABC OK
gate OK — gate: ok — alle 2 required checks geslaagd
gate no-go OK — gate: mislukt — trend
score OK — score: 0.67 >= 0.6 — go
mixed OK — mixed: required ok + 0/1 optioneel
ValueError OK — Ongeldige mode: 'ongeldig'. Kies uit {'gate', 'mixed', 'score'}
Alle Aggregator tests OK
```

Bestaande tests: 9 passed in 0.99s ✅

## Afwijkingen
Geen. Code exact volgens spec.

## Aangeraakte bestanden
- NIEUW: `strategies/base.py` ✅
- NIEUW: `strategies/aggregator.py` ✅
- GEEN bestaande bestanden gewijzigd ✅