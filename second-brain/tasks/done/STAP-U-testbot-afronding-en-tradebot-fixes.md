---
type: result
task: STAP-U
created: 2026-05-30
status: completed
---

# STAP U — Testbot afronding + tradebot selector fixes

## Testbot — wat gebouwd is (sessie 2026-05-30)

### Nieuwe scripts
- `research/signal_pre_analysis.py` → `run.py signal-pre` — welke checks rijpen VOOR een WIN-trade
- `research/reject_analyse.py` → `run.py reject` — root cause van REJECT entries (met JSON output)
- `paper/paper_trader.py` → `run.py paper` — live paper trading loop (15m cycle, zelfde journal als backtest)
- `research/compare/v3a_grid_search.py` → `run.py grid` — grid search via itertools.product, nu parallel (4 workers)
- `run.py` — centrale launcher met alle commando's gedocumenteerd in docstring

### Fixes (na ChatGPT review)
- Journal isolatie: multi-pair run schrijft naar dated submap `logs/multirun_journals/YYYY-MM-DD_HHMMSS/`
- Kandidaatrapport: grid_search toegevoegd aan CRITERIA, score dynamisch (`/5`), grid robuust voor list/dict
- Reject-analyse: JSON output + bronvermelding (journals gelezen, entries geteld)
- Test fix: `test_kandidaat_rapport.py` gebruikte `"winrate"` ipv `"winrate_pct"` → gecorrigeerd
- 49/49 unit tests groen

### Parameters
Alle V3A parameters nu als args/kwargs — niets hardcoded:
fib_min/max, min_pullback, counter_window, extreme_lookback, near_extreme_pct,
wick_body_ratio, min_rr, max_sl_pct, trail_pct, pivot_n, pivot_lookback,
sma_fast, sma_slow, sma_long_window, sma_threshold, sl_buffer_pct, tp_buffer_pct, n_4h, n_15m

### Grid search (loopt nog)
81 combos × 2 pairs (ADAEUR + LINKEUR) — sequentieel gestart, parallel beschikbaar voor volgende run.
Reject-analyse toonde: fib blokkeert 54% van alle rejects → grid zoekt betere fib_min/max.

### Architectuur inzicht
Testbot heeft de juiste scheiding: Signal Generator → Trade Manager → Journal.
Productie-traders zijn te monolithisch geworden. Als V3A KANDIDAAT wordt →
testbot-architectuur wordt de basis voor nieuwe productie-trader, oude scripts weg.

---

## Crypto-tradebot fixes (sessie 2026-05-30)

### Bug: stale_cache misleidend gelabeld als pullback_required
**Bestand:** `scripts/pullback_trader.py`
**Probleem:** Pairs zonder verse bridge-data (26u+ oud) werden geblokkeerd met
`blocked_reason: "pullback_required"` terwijl de echte reden datacabsentie was.
3710/5725 scan events (65%) waren misleidend gelabeld.
**Fix:** Stap 0 toegevoegd vóór trend check — als c4h én c1h leeg zijn →
`blocked_reason: "stale_cache"`, reason: "geen verse cache data — pair niet gevolgd door bridge"
**V3 trader heeft zelfde bug** — nog niet gefixed, ter goedkeuring.

### V1 en V3 selector naar TOP_N = 15
**Bestanden:** `v1_selector.py`, `v3_selector.py`
**Reden:** Bridge volgde 29 unieke pairs (4× top 10). Met 15 per selector → ~38-42 pairs.
Meer verse cache data → minder stale_cache blocks bij de traders.
V2 en range blijven op 10.
**Selectors herstart** in nieuwe screen sessions.

### V1 trader (pullback_trader.py) herstart
Geen open posities op moment van herstart.

---

## Nog te doen

1. Grid search resultaat analyseren zodra klaar → run.py rapport
2. V3 trader stale_cache fix toepassen
3. V2 trader silent skip logging toevoegen
4. Paper trading starten voor alignment data (criterium 3)
5. Als grid goed resultaat → multi-pair run op alle 7 pairs
