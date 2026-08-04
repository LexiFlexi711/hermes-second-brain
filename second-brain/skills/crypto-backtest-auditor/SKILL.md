# Crypto Backtest Auditor

## Superpower 1 — Backtesting zonder lookahead

Audit de testbot-backtest op lookahead bias en data-integriteit.

## Wat deze skill doet

Read-only. Geen code aanpassingen.

1. Controleer `runner.py` op 4H candle filtering — gebruikt het `bisect_right(ts - interval*60)` of iets anders?
2. Controleer dat entry = volgende candle open (pending_signal patroon)
3. Controleer dat gesloten candles (`[:-1]`) gebruikt worden voor signaaldetectie
4. Controleer of `BacktestReader` de `ts_from` filter correct toepast (CSV wordt volledig gelezen, gefilterd op timestamp)
5. Bekijk de meest recente backtest-resultaten in `logs/research/` — zijn de trade counts plausibel?
6. Controleer of incomplete candles worden uitgesloten in de OHLC bridge

## Paden

```
Runner:         projects/crypto-test-bot-v3/src/crypto_test_bot_v3/runner.py
BacktestReader: projects/crypto-test-bot-v3/src/crypto_test_bot_v3/infrastructure/reader.py
Results:        projects/crypto-test-bot-v3/logs/research/
Bridge archive: projects/crypto-data/scripts/universe_ohlc_bridge.py
```

## Output per bevinding

- Locatie (bestand + regelnummer)
- Wat fout is
- Lookahead risico (hoog/laag)
- Fix voorstel

## Regels

- Geen code aanpassen
- Evidence first — toon de exacte coderegel
- Meld ook wat correct is (geeft vertrouwen)
- **Rapporteer resultaat naar `second-brain/tasks/done/` als Lexi vraagt om een audit**