# Layer 9 — Final Baseline

**Datum:** 2026-06-16
**Status:** L9 final baseline
**Commit:** `581ad940` (basis) + L7/L9 uitbreidingen

---

## Commits (NOA-Reign)

```
581ad940 feat(layer9): add validation snapshot MVP
[bestaande L8 commits]
[+ L7 replay-safe + L9 integratie]
[+ L9 replay runner + aggregator + reporting]
```

## Second-brain commit

```
c4c5781 docs(hermes): freeze layer8 market context baseline
[+ L9 final baseline note]
```

---

## Wat L9 doet

1. Bouwt validation snapshots uit L6/L7/L8 op een historisch moment
2. Meet future outcome van de pair na dat moment
3. Future windows: next_3, next_5, next_10, next_20 candles
4. Replay runner: bouwt meerdere snapshots over een tijdsvenster
5. Aggregator: droge samenvatting over veel snapshots
6. Reporting: tekstregels volgens L9 reporting contract
7. Alle functies zijn pure (geen IO, geen fetch)
8. Optionele JSONL writer apart van pure functies

---

## Wat L9 niet doet

- Geen voorspelling
- Geen strategie
- Geen trade-advies
- Geen buy/sell/long/short/entry/exit/setup/signaal/trade-taal
- Geen "bewijst" of "Hermes zag"
- Geen bullmarkt/bearmarkt interpretatie
- Geen dashboard
- Geen routes
- Geen tradebot-koppeling
- Geen AI/LLM analyse
- Geen L10

---

## Welke lagen inbegrepen zijn

| Laag | Functie | Status in L9 |
|------|---------|-------------|
| L6 | `analyze_candle_micro(candles, ...)` | ✅ Pure, replay-safe |
| L7 | `read_indicator_context_from_candles(pair, tf, candles)` | ✅ Nieuw toegevoegd, pure, replay-safe |
| L8 | `read_market_context_from_candles(pair, tf, pair_c, btc_c, eth_c)` | ✅ Pure, replay-safe |

Elke laag heeft poison-test die bewijst dat future candles geen invloed hebben.

---

## Welke lagen geparkeerd zijn en waarom

| Laag | Reden |
|------|-------|
| L2 | Geen `_from_candles` functie. Gebruikt `fetch_kraken` intern. |
| L3 | Idem. Is afhankelijk van L2. |
| L4 | `fetch_and_prepare` doet live fetch. Interne helpers wel zuiver maar geen wrapper. |

Parkeren betekent: deze lagen komen pas in L9 als ze een replay-safe `_from_candles` variant hebben. Geen geforceerde refactor.

---

## Poison-test policy

Elke laag in L9 heeft een poison-test die bewijst dat future candles geen invloed hebben:

- **L6**: `test_poisoned_future_does_not_change_l6_l8_layers` — bewijst dat L6 identiek blijft
- **L7**: `test_closed_candle_exclusion` (L7) + `test_l7_gets_only_visible_candles` (L9) — bewijst dat L7 identiek blijft
- **L8**: `test_poisoned_future_does_not_change_l6_l8_layers` — bewijst dat L8 identiek blijft

Nieuwe lagen in L9 moeten een poison-test hebben.

---

## Reporting contract

Alle L9 rapporten moeten voldoen aan:

```
L9 rapporteert metingen, geen interpretatie.
Elke zin moet direct terug te voeren zijn op een outputveld.
Als een conclusie extra data vereist, moet L9 zeggen:
"niet gemeten" of "buiten L9A scope".
```

Verboden: bullmarkt, bearmarkt, Hermes zag, bewijst (bij 1 sample), bleef sterker dan (zonder data), setup, signaal, trade, entry, exit, long, short, buy, sell.

Zie `wiki/projects/hermes-layer9-reporting-contract.md` voor volledige regels.

---

## Hoe L9 later gebruikt mag worden

- Als validatie-tool naast Hermes
- Om te meten wat er gebeurde na een Hermes-context
- Om aggregaten te bouwen over veel snapshots
- Om droge rapporten te genereren
- Als basis voor eventuele L9B (L2/L3/L4 integratie) na replay-safe refactor

---

## Stoplijst

- **Geen L10** — niet beginnen zonder expliciet akkoord
- **Geen dashboard** — L9 blijft CLI/file-based
- **Geen tradebot-koppeling** — L9 is validatie, geen productie
- **Geen strategie** — L9 meet alleen achteraf
- **Geen L8-uitbreiding** — L8 is frozen
- **Geen L2/L3/L4 integratie** zonder replay-safe refactor + poison-test
- **Geen interpretatieve rapportage** — reporting contract is bindend

---

## Bestanden

```
layer7_indicator/indicator_context.py       — L7 + read_indicator_context_from_candles()
layer9_validation_lab/__init__.py            — package marker
layer9_validation_lab/validation_lab.py      — build_validation_snapshot_from_candles()
layer9_validation_lab/replay_runner.py       — run_validation_replay_from_candles()
layer9_validation_lab/aggregate.py           — aggregate_validation_snapshots()
layer9_validation_lab/reporting.py           — build_dry_validation_report()
tests/test_layer7_indicator.py               — L7 tests (41)
tests/test_layer9_validation_lab.py          — L9 snapshot tests (25)
tests/test_layer9_replay_aggregate.py        — L9 replay/aggregate/report tests (21)
```
