# TEAM MEETING 009 — V1/V2 Pullback Scripts Analyse (20 Mei 2026)

## Doel
Analyseer pullback_trader.py (V1) en pull_backtrader_2.py (V2) nadat Lexi's fixes en Claude Code patches zijn doorgevoerd. Identificeer overgebleven bugs en doe fixes.

## Aanwezige Rollen (Virtueel)
- **Lexi (Owner)** — voorzitter, eindbeslisser
- **Noa/Scout (Hermes)** — data verzameling uit logs
- **DevOps Guard (Hermes)** — runtime/screen/cache/heartbeat check
- **Master Trader (Hermes+Pro)** — trading strategie audit
- **Critic (Hermes+Pro)** — zwakke redeneringen blootleggen
- **QA Agent (Hermes+Pro)** — bewijsbaarheid valideren
- **Controller (Hermes+Pro)** — synthese en prioriteiten
- **Finance Guard (Hermes)** — kostenbewaking
- **Claude Code (Director)** — code-implementatie (via Lexi's VS Code)
- **Secretary (Hermes)** — notulist

---

## REALITY CHECK
- **LIVE_MULTIBOT_MEETING:** JA
- **FANTASY_DIALOGUE:** NEE — alle claims uit live tool output
- **CLAUDE_CODE_CALLED:** NEE (nog niet — prompt voorbereid voor Lexi)
- **DECISIONS_USABLE:** JA (alle bronnen getraceerd)

---

## ITERATIE 1 — Scout (data verzamelen)

**Bronnen:**
- `pullback_trader.py` (V1, 649 lijnen) — `/mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/projects/crypto-tradebot/scripts/pullback_trader.py`
- `pull_backtrader_2.py` (V2, 990 lijnen) — `/mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/projects/crypto-tradebot/scripts/pull_backtrader_2.py`
- `v2_trades.jsonl` (63 trades) — `/mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/projects/crypto-tradebot/logs/v2_trades.jsonl`
- `scan_events.jsonl` (live) — `/mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/projects/crypto-tradebot/logs/scan_events.jsonl`
- `v2_cycles.jsonl` — `/mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/projects/crypto-tradebot/logs/v2_cycles.jsonl`
- `v1_heartbeat.txt` — `/mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/projects/crypto-tradebot/scripts/logs/v1_heartbeat.txt` (BESTAAT NIET — path mismatch)
- `v2_heartbeat.txt` — `/mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/projects/crypto-tradebot/logs/v2_heartbeat.txt` (18:04 UTC)

**Runtime status (16:45 — 20 Mei):**
| Screen | PID | Status | Uptime |
|--------|-----|--------|--------|
| cache | 2535956 | ✅ draait | ~3u |
| V1 | 2536221 | ✅ draait | ~3u (geen heartbeat) |
| V2 | 2536594 | ✅ draait | ~3u (heartbeat OK) |

**V2 Trades (63 trades):**
- 3 meest recente: SUIEUR LONG WIN, NEAREUR LONG WIN, SOLEUR LONG WIN — ALLEMAAL WINS 🎯
- Geen open trades (v2_state.json leeg)

**V1 Scanner (16:03 UTC — 15 pairs):**
- 9/15 trend_break (fib >70%)
- 4/15 pullback_forming
- 2/15 ideal_pullback (XRPEUR 57.9%, BONKEUR 50.9%)
- 0/15 confirmed_ready
- **100% direction="short"** — ALLE pairs, zelfs met 4H UP trend

**V1 Trade History (pullback_trades.jsonl — 5 trades):**
- 1 WIN (INJEUR LONG, +0.27 EUR)
- 4 EARLY_EXIT (gemiddeld 3.25 candles)

---

## ITERATIE 2 — Master Trader (analyse)

**Finding 1 — V1 100% short bias (richtingblindheid na fix)**
- **Bewijs:** Alle 15 scan_events tonen `direction: "short"`. SOLEUR met 4H UP trend en 117% fib krijgt `direction: "short"`.
- **Risico:** V1 mist alle LONG opportuniteiten. V2 pakt longs en wint, V1 staat blind.
- **Advies:** `_is_bullish_structure()` matcht niet omdat het lows checkt i.p.v. highs. Tijdens herstel stijgen highs én lows. Bearish structuur faalt (recent_high < prev_high = False), bullish faalt ook (recent_low > prev_low = kan ook False zijn in herstel). Geen van beide True → V1 blokkeert.

**Finding 2 — V2 produceert winnende longs**
- **Bewijs:** 3 recente trades allemaal LONG WINS. Eerder 0% WR op SUIEUR → nu WIN.
- **Risico:** Laag. Richting-fix werkt.
- **Advies:** Laat V2 draaien.

**Finding 3 — V1 produceert 80% EARLY_EXIT**
- **Bewijs:** 4/5 V1 trades exit na 2-7 candles. ETHEUR SHORT: entry 1815 → exit 1832 in 2 candles (−17 EUR).
- **Risico:** V1 heeft geen pullback_fast monitoring. EARLY_EXIT uitkomsten komen van externe logica of V1's eigen exit condities.

---

## ITERATIE 3 — Critic (diepe analyse)

**Zwakte 1 — V2 calc_sl() returnt 0.0 i.p.v. hard_floor**
- Lijn 187-188: `if (stop - entry_price) / entry_price < MIN_STOP_DIST: return 0.0`
- Moet zijn: `return hard_floor`
- Blokkeert geldige trades als swing high dicht bij entry ligt.

**Zwakte 2 — entry_lateness drempel inconsistent**
- V1: >50% = weak_entry
- V2: >0.70 (70%) = weak
- V2 is 20% losser dan V1. Onlogisch.

**Zwakte 3 — V1 _is_bullish_structure asymmetrie**
- `_is_bearish_structure`: recent_high < prev_high
- `_is_bullish_structure`: recent_low > prev_low
- Tijdens herstel kunnen highs én lows stijgen. Bullish check moet highs vergelijken, niet lows.

---

## ITERATIE 4 — QA Agent (validatie)

| Check | Resultaat | Detail |
|-------|-----------|--------|
| V1 heartbeat schrijft | ❌ FAIL | Path mismatch: `/scripts/logs/` |
| V1 richtingslogica | ❌ FAIL | 100% short bias |
| V1 scan output | ✅ PASS | 16:03 UTC, draait |
| V2 calc_sl() hard floor | ❌ FAIL | returnt 0.0 ipv hard_floor |
| V2 heartbeat | ✅ PASS | 18:04 recent |
| V2 entry_lateness | ⚠️ WARN | 70% vs V1 50% |
| V2 open trades | ✅ PASS | State leeg |

**Verdict:** `needs_revision` — 3 issues

---

## ITERATIE 5 — Controller (synthese & prioriteiten)

**P1 — V2 calc_sl() returnt 0.0 ipv hard_floor** — 1 lijn, laag risico
**P1 — V1 heartbeat path mismatch** — 1 lijn, laag risico
**P2 — V1 _is_bullish_structure moet highs checken** — midden risico
**P2 — entry_lateness harmoniseren** — midden risico

---

## BESLISSINGEN

| # | Beslissing | Details |
|---|-----------|---------|
| 1 | **Prompt voor Claude Code** | Noa stelt prompt op voor Lexi om in VS Code te plakken |
| 2 | **V2 calc_sl() fix** | 1 lijn wijzigen |
| 3 | **V1 heartbeat path** | 1 lijn wijzigen |
| 4 | **V1 direction bug** | _is_bullish_structure aanpassen |
| 5 | **Lexi beslist over timing** | Prompt klaar voor copy-paste |

---

## OPEN VRAGEN VOOR LEXI
- Wil je dat ik de kleine patches zelf doe (calc_sl, heartbeat) of alles via Claude Code?
- entry_lateness harmoniseren: ook via Claude Code of later?

## NEXT STEPS
1. ✅ Prompt klaar voor Claude Code
2. ✅ Meeting docs + second brain sync
3. ⏳ Lexi geeft prompt aan Claude Code in VS Code
4. ⏳ Screens herstarten na patches

---

**Secretary notities:** Alle data uit live tool calls. Pro model gebruikt voor Master Trader, Critic, QA, Controller. Heathcare.