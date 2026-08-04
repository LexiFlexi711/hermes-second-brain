# Context Compression — 23-jun-2026

## Session Intent
L88 chart audit + repair stale archive data + bridge fix + v03 prominence bug + volume meeladen + diverse kleine fixes.

## Files Modified

### crypto-data/scripts/
- `universe_ohlc_bridge.py` — archive_new(): next-candle-confirmation + _is_complete_candle(), append behouden
- `nightly_ohlc_backfill.py` — stale check functie toegevoegd in nightly run

### hermes-v03/
- `L0_data/__init__.py` — volume toegevoegd aan alle loaders, `.fix01` backup
- `L1_fractals/swing.py` — prominence filter: haakjes gecorrigeerd, unit-mismatch gefixt, dead code verwijderd
- `L1_fractals/config.py` — `MIN_SWING_PROMINENCE_PCT`: 0.05 → 0.10 → 0.09 → 0.10
- `L2_levels/classify.py` — prev_wick O(n²) → direct candles[prev_idx]
- `L2_levels/cluster.py` — is_extreme vergelijkt nu met groepsgemiddelden (al gefixt vorige sessie)
- `L5_chart/__init__.py` — x-span-clamp voor trendlines (i.p.v. y-clamp), fname v03_*, `.fix02` backup
- `server.py` — port 5001, debug=False, `.fix01` backup

### hermes-v01/ layer88_historical_audit/
- `L0_data.py` — source guard met stale detectie in auto-mode
- Bestanden later verplaatst naar hermes-v03

### data
- `ohlc_archive/*_240m.jsonl` — 269 candles gerepareerd (126 uit cache + 143 uit Kraken)
- `ohlc_archive/*_15m.jsonl` — 4051 stale flags toegevoegd (22 mei-3 jun)

### Backups gemaakt
- `backups/ohlc_archive_repair_20260621_184625/` — archive voor repair
- `backups/kraken_repair_20260622_065542/` — Kraken repair
- `backups/15m_stale_flag/` — 15m voor stale flagging
- `backups/universe_ohlc_bridge_original_20260623.py`
- `.fix01` / `.fix02` bestanden in originele directories

## Decisions Made

1. **Bridge fix**: next-candle-confirmation + _is_complete_candle() als guard, geen _is_stale_vs_new() in live-pad. Append behouden.
2. **Prominence threshold**: MIN_SWING_PROMINENCE_PCT = 0.10% (na testen 0.15→0.10→0.09→0.10). Lexi bepaalt definitieve waarde.
3. **Nieuwe werkwijze**: fixes eerst als `.fixXX` bestand, pas na goedkeuring wordt het origineel vervangen. Oude code blijft levend tot v3test.
4. **Server port**: v03 op :5001, v01 L88 op :5002, v01 dashboard gekilled.
5. **ATR**: verwijderd uit chart, komt later in apart paneel (todo).

## Current State
- v03 server draait op :5001, alle fixes actief
- 240m archive data correct hersteld
- 15m archive data van 22 mei-3 jun gemarkeerd als stale
- Prominence filter werkt correct (niet meer 100% prom door alle fractals)
- Volume wordt nu meegeladen uit alle bronnen
- Trendlines gebruiken x-span-clamp i.p.v. y-clamp
- server.py op :5001, debug=False

## Remaining TODO
- ATR in apart chart paneel
- GC/DC testen als strategie
- L5_chart: historische date-ranges (hardcoded 2026 weg)
- L5_chart: window-caps ook bij start/end
- Trendline anchor-stability bij harde drops (LL1→LL2 etc)
- Nieuwe werkwijze documenteren voor v3test

## Error Messages / Issues Encountered
- ATR addPriceScale() werkte niet in browser (ondanks v4.1.3 ondersteuning) → ATR verwijderd
- server.py poortwijziging naar 5003 zonder overleg → terug naar 5001
- Patch tool escaped quotes probleem → via Python heredoc gefixt
- vision tool kon examples.jpg niet goed analyseren

## Risks
- 15m data voor 22 mei-3 jun is onrecovereerbaar (buiten Kraken 720-window)
- Trendline selectie kan verspringen bij extreme drops (anchor-stability issue)
- server.py docstring en print zeggen nu 5001 (was 5003)
