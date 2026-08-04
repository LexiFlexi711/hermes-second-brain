# Crypto Testbot Health

## Superpower 7 — Programmeerdiscipline

Controleer de gezondheid van de testbot: tests, interfaces, code kwaliteit.

## Wat deze skill doet

Read-only. Draait tests en controleert code-integriteit.

1. Draai de volledige test suite: `python -m pytest tests/ -q`
2. Controleer of alle kern-interfaces ongewijzigd zijn:
   - `CheckResult(name, ok, value, why)`
   - `Signal(direction, entry, sl, tp, checks, context)`
   - `DataReader.get_candles(pair, interval, n) → list[dict]`
   - `Strategy.compute_checks(data) → dict[str, CheckResult]`
3. Controleer of elke strategie-map heeft: `config.py`, `logic.py`, `strategy.py`
4. Controleer of `runner.py` pending_signal patroon gebruikt (entry fix)
5. Toon hoeveel strategieën er zijn en welke gebacktest zijn

## Output formaat

```
TESTBOT GEZONDHEID

Tests:        101/101 ✓
Strategieën:  V1 ✓  V2 ✓  V3A ✓  V4 ✓
Interfaces:   CheckResult ✓  Signal ✓  DataReader ✓
Entry fix:    pending_signal patroon aanwezig ✓
Backtest:     V1/V2/V3A/V4 — resultaten in logs/research/ ✓

OORDEEL: Gezond
```

## Paden

```
Testbot: projects/crypto-test-bot-v3/
Tests:   projects/crypto-test-bot-v3/tests/
Runner:  projects/crypto-test-bot-v3/src/crypto_test_bot_v3/runner.py
```

## Regels

- Geen code aanpassen
- Als tests falen: toon de fout, geen fix
- Geen nieuwe tests schrijven in deze skill
- **Rapporteer resultaat naar `second-brain/tasks/done/` als Lexi vraagt om een audit**