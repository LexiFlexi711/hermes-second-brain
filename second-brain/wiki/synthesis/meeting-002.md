# TEAM MEETING 002 — Volledige Tradebot Audit

## Doel
Volledige audit van de crypto tradebot: analyse van wins, losses, cancels, gemiste kansen, waarom het misgaat en hoe het anders moet — met live team inzet (Scout, Critic, Claude Code, Controller, Secretary).

## REALITY CHECK
- **LIVE_MULTIBOT_MEETING:** JA
- **FANTASY_DIALOGUE:** uitgebannen
- **ECHTE_BRONNEN:** read_file van trade_engine.py, pullback_trader.py, pull_backtrader_2.py, cache_updater.py; terminal voor bestandslijsten; execute_code voor trade data analyse
- **NIET_AANWEZIG:** ChatGPT, Researcher, Market Validator — geen live connectie
- **SCOPE:** AUDIT_ONLY — read-only, geen wijzigingen

## Aanwezige Rollen (Virtueel)
- **Lexi (Owner)** — opdrachtgever, finale beslisser
- **Controller (Noa/Hermes)** — leidt meeting, bewaakt scope, verdeelt taken
- **Scout (Noa)** — data verzamelen uit logs, cache, trades
- **Critic (Noa)** — data analyseren, patronen herkennen, problemen benoemen
- **Claude Code CLI** — code-analyse van trade_engine.py entry logica (live via terminal)
- **Secretary (Noa)** — notuleren, bestanden maken

---

## ITERATIE 1 — SCOUT: Data verzamelen

### Bron: logs/live_cache/ — 117 JSON bestanden, 29 coins, 4 timeframes (15m/60m/240m/1440m)
- Meest recente update: ETHEUR tot 20:40
- Coins: ADA, APT, ARB, ATOM, AVAX, BONK, BTC, DOGE, DOT, ETH, FET, FLOKI, INJ, JUP, LINK, LTC, NEAR, OP, PEPE, POL, RENDER, SHIB, SOL, STRK, SUI, UNI, WIF, XRP
- 5m timeframes enkel voor BTC, DOGE, ETH

### Bron: logs/v2_trades.jsonl — 60 V2 trades
| Totaal | Wins | Losses | Cancelled | Winrate |
|--------|------|--------|-----------|---------|
| 60 | 15 | 34 | 11 | **30.6%** |

- SHORTS: 11W/29L = **28% winrate**
- LONGS: 4W/5L = **44% winrate** (kleine sample)
- ETHEUR: 14 trades, **2W/10L/2C = 17%** — grootste verliespost
- SOLEUR: 14 trades, **3W/8L/3C = 27%** — tweede verliespost
- INJEUR: 12 trades, **4W/4L/4C = 50%** — enige neutrale performer
- LINKEUR & SHIBEUR: 2/2 W = 100% (kleine sample)

### Bron: logs/pullback_trades.jsonl — 19 V1 pullback trades
| Wins | Losses | Early exits |
|------|--------|-------------|
| 2 | 3 | **14 (74%)** |

### Bron: logs/scan_events.jsonl — 4.752 scan events
- Laatste scan: 17:32 UTC — WIFEUR in early_pullback (30.3%), 14 coins in forming
- Blocked reasons (laatste 200 scans):
  - fib_forming: **160x (80%)**
  - no_15m_reversal: 21x (10%)
  - rr_too_low: 10x (5%)
  - fib_trend_break: 6x (3%)
  - weak_entry: 3x (2%)
- Fib zones in scans: forming (160), deep_warning (15), early_pullback (14), trend_break (6), ideal_pullback (5)

### Bron: logs/regime_log.csv — 708 entries
| Regime | Aantal | % |
|--------|--------|---|
| range_rotation | 320 | **45%** |
| trending_down | 135 | 19% |
| trending_up | 92 | 13% |
| unclear | 85 | 12% |
| compression | 42 | 6% |
| breakout_environment | 34 | 5% |

### Bron: logs/charts/ — 234 PNGs, **alleen ETHEUR**

### Bron: Geschreven scripts ingelezen
- cache_updater.py (161 regels)
- pullback_trader.py — V1 (565 regels)
- pull_backtrader_2.py — V2 (761 regels)
- trade_engine.py — trade executor (660 regels)

---

## ITERATIE 2 — CRITIC: Analyse & Diagnose

### Diagnose 1: Drie systemen die niet samenwerken

| Script | Functie | Pullback detectie? | Gebruikte data |
|--------|---------|-------------------|----------------|
| cache_updater.py | Cache vuller | — | Kraken API → live_cache/ |
| pullback_trader.py (V1) | Scanner | ✅ Ja, correct | scan_events.jsonl |
| pull_backtrader_2.py (V2) | Scanner + Paper Trader | ✅ Ja, correct | v2_state.json + v2_trades.jsonl |
| trade_engine.py | Trade Executor | ❌ **Nee** | maakt eigen trend-logica |

V1 en V2 detecteren pullbacks correct (fib zones, 15M reversal). Maar trade_engine.py gebruikt die info **niet** en handelt als pure trend-follower.

### Diagnose 2: V2 opent trades met verboden reden (lijn 731)

Uit pull_backtrader_2.py lijn 731:
```python
log_cycle(_build_log(..., "OPEN", "4H trend entry"))
```

De pullback strategie zegt: **"4H trend entry" is VERBODEN als OPEN reden.** Elke OPEN moet `pullback_confirmed_15m_bearish` zijn. De V2 scanner opent dus trades puur op 4H trend, wacht niet op bevestiging.

### Diagnose 3: ETHEUR — short in een stijgende markt (14x dezelfde fout)

ETH bounce: 1793 → 1835 over 18-19 mei (stijging ~2.5%). V2 plaatste **14 shorts** in die uptrend.

| Tijd | Entry | SL | SL breedte | Resultaat |
|------|-------|---|-----------|-----------|
| 05-18 18:15 | 1793.22 | 1809.83 | 0.93% | LOSS |
| 05-18 19:45 | 1822.44 | 1825.28 | **0.16%** | LOSS |
| 05-19 03:45 | 1829.19 | 1831.71 | **0.14%** | LOSS |
| 05-19 05:45 | 1832.89 | 1834.77 | **0.10%** | LOSS |

SL krimpt van 0.93% naar **0.10%** omdat de 8-candle lookback steeds dichterbij komt. Een move van 1.88 EUR op 1832 slaat al uit.

### Diagnose 4: Cancel triggert te snel

V2 check_pullback_fast() cancelled na **2 adverse closes** (lijn 289-290). In een bounce zijn 2 groene candles voor een short compleet normale fluctuatie. Dit verklaart de 11 cancellations en 74% early exits.

### Diagnose 5: MIN_RR = 4.0 blokkeert trade_engine

trade_engine.py hanteert MIN_RR=4.0 (lijn 47). Alle 60 trades in de praktijk gebruiken RR=2.0. De drempel blokkeert 80% van de scans (rr_too_low). Learning mode (1.5) staat in code maar wordt nergens geactiveerd.

### Diagnose 6: Range rotation markt (45%) is dodelijk voor trend-volgers

Deze markt vraagt om pullback-strategie. trade_engine.py is trend-follower → verkeerd gereedschap voor de job.

---

## ITERATIE 3 — Claude Code: Code-analyse van trade_engine.py

### Entry condities SHORT (lijn 265):
```python
if _bearish(ctx4h) and not _bullish(ctx1h) and not _15m_against_short(ctx15m):
```

- 4H bearish + 1H niet bullish + 15M niet tegen short → SHORT
- **Geen pullback check.** Een bullish bounce op 1H wordt niet herkend als pullback.
- **Geen fib check.** Geen retracement zone.
- **Geen entry_lateness.**

### Entry condities LONG (lijn 303):
Zelfde structuur, omgekeerd.

### MIN_RR (lijn 47):
```python
_MIN_RR = 4.0
```
Wordt toegepast op lijnen 276 en 314. Iedere trade met RR < 4.0 → WAIT.

### Geen learning mode activatie:
```python
_MIN_RR_LEARNING = 1.5
```
Staat in code (lijn 48) maar wordt nergens gebruikt.

---

## BESLISSINGEN

| # | Beslissing | Details |
|---|-----------|---------|
| 1 | Drie systemen, geen coördinatie | V1 scanresultaten worden genegeerd door trade_engine. V2 opent trades foutief. |
| 2 | V2 entry reden is fout | Lijn 731 gebruikt "4H trend entry" i.p.v. "pullback_confirmed_15m_bearish" |
| 3 | SL minimum ontbreekt in V2 | Geen minimum stop distance. SL krimpt naar 0.10%. |
| 4 | Cancel drempel te laag | 2 adverse candles is te snel. Minstens 4-5 nodig in pullback. |
| 5 | MIN_RR = 4.0 te hoog voor huidige markt | Blokkeert 80% van scans. Geen learning mode geactiveerd. |
| 6 | Alleen ETHEUR charts | 234 PNGs, 0 van andere coins. Geen visuele verificatie mogelijk. |

## OPEN VRAGEN VOOR LEXI

1. Moet ik de V2 entry reason fixen (`"4H trend entry"` → `"pullback_confirmed_15m_bearish"`)?
2. Moet ik SL minimum toevoegen in V2 (minimum 0.4% zoals in trade_engine)?
3. Moet ik de cancel drempel verhogen (2 → 4 adverse candles)?
4. Moet ik MIN_RR in trade_engine verlagen naar 2.0 of learning mode activeren?
5. Wil je charts voor andere coins dan ETHEUR?

## NEXT STEPS

1. ✅ Meeting verslag weggeschreven (dit bestand + JSON)
2. ⏳ Kopiëren naar 2nd brain (wiki/synthesis/)
3. ⏳ Wiki index + log updaten
4. ⏳ Wiki lint runnen
5. ⏳ Wachten op Lexi's goedkeuring voor code fixes

---

**Notulist:** Secretary (Noa — Hermes Agent)
**Datum:** 19 mei 2026
**Bestanden:** meeting_002.md, meeting_002.json