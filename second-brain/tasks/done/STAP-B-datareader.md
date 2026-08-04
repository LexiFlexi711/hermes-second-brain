---
stap: B
naam: datareader-abc-en-readers
status: done
uitgevoerd-door: Hermes
datum: 2026-05-29
---

## Wat gedaan

DataReader ABC + BacktestReader + LiveReader aangemaakt in:
`src/crypto_test_bot_v3/infrastructure/reader.py`

- **DataReader(ABC)** — abstracte interface met `get_candles(pair, interval, n)`
- **BacktestReader** — leest ohlc_archive JSONL, optioneel ts_from/ts_to filter (geen lookahead)
- **LiveReader** — leest live_cache JSON (rolling), resolved pad via crypto-data → local fallback

## Testresultaat

```bash
BacktestReader OK — 100 candles, source=FALLBACK_OLD_CRYPTO_TRADEBOT
LiveReader OK — 50 candles
Lookahead filter OK — 200 candles tot cutoff
Alle tests geslaagd
```

Bestaande tests: 9 passed in 0.73s ✅

## Afwijkingen

1. **`_CACHE_DIR` bestaat niet in `paths.py`** — taakspec importeert `from crypto_test_bot_v3.infrastructure.paths import resolve_ohlc_dir, _CACHE_DIR`, maar `_CACHE_DIR` is niet gedefinieerd in paths.py. Opgelost door LiveReader zelf het cache pad te laten resolven via `_resolve_cache_dir()` (crypto-data → local fallback, zelfde logica als `resolve_ohlc_dir()`).

2. **`ohlc_archive.py` bestaat niet** — taakspec zegt "ohlc_archive.py bestaat al" maar het bestand heet `jsonl_store.py`. BacktestReader gebruikt `resolve_ohlc_dir()` uit paths.py en leest direct de JSONL-bestanden, dus geen probleem.

## Aangeraakte bestanden

- NIEUW: `src/crypto_test_bot_v3/infrastructure/reader.py` (enkel dit)
- GEEN bestaande bestanden gewijzigd ✅

## Volgende stap aanbeveling

DataReader werkt. Volgende logische stap: Strategy base class of Config loader.