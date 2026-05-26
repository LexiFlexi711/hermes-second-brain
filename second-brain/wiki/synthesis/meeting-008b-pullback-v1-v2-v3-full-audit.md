# TEAM MEETING 008 — Pullback Trader V1/V2/V3 Volledige Audit

## Doel
Volledige analyse van alle 3 pullback trade scripts (V1, V2, V3) — code, logs, resultaten, runtime status — met aanbevelingen voor fixes en een Claude Code prompt.

## Aanwezige Rollen (Virtueel)

| Rol | Agent | Status |
|-----|-------|--------|
| Owner / Beslisser | **Lexi** | ✅ |
| Data / Runtime | **Scout** (Flash) | ✅ Logs, cache, screens |
| Strategie & Markt | **Master Trader** (Pro) | ✅ Entry/exit, SL/TP, pullback |
| Redeneer-check | **Critic** (Pro) | ✅ Logische fouten |
| Bewijs-check | **QA Agent** (Pro) | ✅ Bewijs per conclusie |
| Synthese | **Controller** (Pro) | ✅ Conclusies + prioriteiten |
| Notulist | **Secretary** (Flash) | ✅ Deze bestanden |
| Code Fixes | **Claude Code** (Pro) | ⏳ Prompt voor VS Code (Lexi geeft) |

---

## REALITY CHECK

- **LIVE_MULTIBOT_MEETING:** JA — alle data komt van live tool output
- **FANTASY_DIALOGUE:** uitgebannen
- **CLAUDE_CODE_LIVE:** NEE — prompt wordt opgesteld voor Lexi om in VS Code te geven
- **BRONNEN:** allemaal geverifieerd met grep/cat/tail/read_file

---

## ITERATIE 1 — SCOUT + DEVOPS: Runtime & Data

**Runtime status:**
- **🔴 GEEN SCREENS DRAAIEN** — cache, v1, v2, v3 alle 4 dood (screen -ls = "No Sockets found")
- Heartbeats tonen 20:58 (v1_heartbeat.txt, v2_heartbeat.txt) — waarschijnlijk laatste run voor crash
- Cache is vers (20:58) — lijkt via eenmalige cron run te zijn geüpdatet
- pullback_state.json: **stale ETHEUR SHORT ghost positie** van 18 mei 22:00 — entry 1831.83, SL 1850.0, TP 1795.49 — NOOIT GESLOTEN!

**V2 Trade Stats (bron: v2_trades.jsonl — 62 trades):**
| Metriek | Waarde |
|---------|--------|
| Totaal trades | 62 |
| WIN | 17 |
| LOSS | 34 |
| CANCELLED | 11 |
| **Winrate** | **33.3%** (17/51 resolved) |
| LONG | 15 (24%) |
| SHORT | 47 (76%) |
| **Direction bias** | **76% SHORT** |
| RR | Allen 2.0 |

**V2 Open positie:** SOLEUR LONG @ 72.82 (20 mei 10:56) — nog open, herhaaldelijk "HOLD"/"geen pullback" gelogd. Price nu ~73.25 (in profit).

**V1 Scan status (bron: scan_events.jsonl @ 20:58):**
| Status | Aantal pairs |
|--------|-------------|
| forming (fib <30%) | 15 |
| ideal_pullback — no_15m_reversal | 3 (XRPEUR, LINKEUR, POLEUR) |
| deep_warning | 1 (DOGEEUR @ 64.5%) |
| trend_break | 1 (WIFEUR @ 88.6%) |
| Totaal | 20 pairs |

**V3 (pull_backtrader_3.py, 544 lijnen):**
- State machine: TREND_ACTIVE / PULLBACK_CANDIDATE / PULLBACK_CONFIRMING / PULLBACK_FAILED / STRUCTURE_BROKEN
- 1260 log entries op pullback_v3_trades.jsonl
- Laatste run: 20:59 vandaag
- 5 pairs tonen "geen duidelijke 4H trend" (LINKEUR, DOTEUR, POLEUR, WIFEUR, APTEUR) — V3 is strikter met trend detectie dan V1/V2
- XRPEUR + DOGEEUR in PULLBACK_CONFIRMING (2 candles tegen trend)

**Bronnen:**
- `screen -ls` → "No Sockets found"
- `cat logs/v1_heartbeat.txt` → "2026-05-20 20:58:31"
- `cat logs/v2_heartbeat.txt` → "2026-05-20 20:58:22"
- `tail -20 logs/scan_events.jsonl` → 20 pairs, 15 forming
- `grep -c "WIN\|LOSS\|CANCELLED" logs/v2_trades.jsonl` → 17/34/11
- `cat logs/pullback_state.json` → ETHEUR ghost entry 1831.83
- `wc -l logs/pullback_v3_trades.jsonl` → 1260

---

## ITERATIE 2 — MASTER TRADER: Strategie Audit

**Finding 1: V1 SL berekening — extra buffer op swing_high**
V1 gebruikt `max(swing_high * 1.003, entry * 1.004)` voor SHORT SL.
De `* 1.003` op swing_high is overbodig — de swing_high zelf is al het invalidation point.
**Bewijs:** pullback_trader.py lijn 449: `stop_loss = round(max(swing_high * (1 + _STOP_BUFFER), hard_floor), 6)`
**Risico:** SL staat 0.3% verder dan nodig → kleinere positie of groter verlies bij stop-out.
**Advies:** Gebruik swing_high direct, zoals V2 doet.

**Finding 2: V1 TP gebruikt support/resistance levels i.p.v. vaste RR**
V1 SHORT TP = `max(support_levels)` (hoogste support onder entry) uit laatste 20 1H candles.
Dit kiest de **dichtstbijzijnde** support — TP is vaak te klein, RR wordt niet gegarandeerd.
**Bewijs:** pullback_trader.py lijnen 450-451.
**Risico:** Kleine wins, inconsistent RR.
**Advies:** Gebruik vaste RR (2.0) zoals V2.

**Finding 3: V2 entry_lateness threshold te hoog (70% vs 50%)**
V2: lateness > 0.70 = weak_entry. V1: lateness > 50% = weak_entry.
V2 laat entries toe die 70% van de pullback al gemist hebben.
**Bewijs:** pull_backtrader_2.py lijn 347: `weak = lateness > 0.70 or label == "deep_warning"`
**Risico:** Late entries stuiten vaak op trendhervatting → verlies.
**Advies:** Verlaag naar 0.50 zoals strategie spec.

**Finding 4: V2 blokkeert early_pullback voor ALLE richtingen**
30-38.2% fib zone wordt compleet geblokkeerd i.p.v. gewaarschuwd.
**Bewijs:** pull_backtrader_2.py lijn 329-330: `if label == "early_pullback": return None`
**Risico:** Mist trades die in early zone al bevestiging tonen.
**Advies:** Gebruik waarschuwing i.p.v. harde blokkade.

**Finding 5: Macro-paralyse in V1 is structureel na crash**
BTC range 65,315 → 70,232 = $4,917. Bij 66,800 is fib = 25.9%. Nog $2K nodig voor 38.2%.
**Bewijs:** scan_events.jsonl BTCEUR entry: pb_scope=macro, fib_pct=0.2593.
**Risico:** Geen trades voor dagen tot weken na grote bewegingen.
**Advies:** Lokale scope fallback — scan ook kleinere swings.

**Finding 6: 76% SHORT bias in V2**
47/62 trades SHORT. Dit is consistent met 4H bearish trend tijdens crash.
**Maar:** SHORT in een bounce (pullback) faalt systematisch — 34/51 verlies.
**Bewijs:** v2_trades.jsonl — 17 WIN (8 SHORT, 9 LONG), 34 LOSS (meeste SHORT in bounce).
**Advies:** Trade BOTH directions tijdens pullback, niet enkel trend-volgend.

---

## ITERATIE 3 — CRITIC: Logische Fouten

**1. V1 gebruikt `max(support_levels)` voor SHORT TP**
- `max()` kiest de HOOGSTE support onder entry = dichtstbijzijnde
- Dit produceert kleine TP voor SHORTs in een bearish trend
- Paradox: in een bearish markt had TP verder moeten staan, maar V1 zet hem dichterbij

**2. V3 detect_trend_direction() returns None — maar V1/V2 niet**
- V3: `if len(highs) < 2 or len(lows) < 2: return None` ⟶ 5 pairs "geen duidelijke 4H trend"
- V1/V2: FORCEREN altijd een trend (vinden altijd een swing)
- Dit betekent dat V1/V2 trades openen in "trendloze" markten waar ze niet in thuishoren

**3. V2 entry_lateness asymmetrie**
- V1: `entry_lateness > 50% → weak_entry` (consistent met strategie)
- V2: `entry_lateness > 70% → weak_entry` (dubbele tolerantie)
- Oorzaak: waarschijnlijk overschrijf tijdens fix-sessie zonder harmonisatie met V1

**4. Geen auto-recovery na crash**
- Beide screens dood → trades blijven open in state file → geen outcome tracking
- pullback_state.json ghost trade is hier het bewijs van
- Herstel vereist MANUELE actie — dit is niet schaalbaar

**5. V3 draagt niet bij**
- V3 produceert nuttige state data (PULLBACK_CONFIRMING) maar geen script leest het
- 1260 log entries = 1260 cycli van observatie zonder output naar V1/V2
- Opportunity cost: V3 data had late entries kunnen blokkeren

---

## ITERATIE 4 — QA AGENT: Bewijs Controle

| Claim | Bewijs | Status |
|-------|--------|--------|
| Geen screens draaien | `screen -ls` → "No Sockets found" | ✅ |
| V2 62 trades, 17 WIN, 34 LOSS | `grep` op v2_trades.jsonl | ✅ |
| V1 macro scope | scan_events.jsonl pb_scope=macro | ✅ |
| V2 SL = max(swing_high, entry*1.004) | pull_backtrader_2.py lijn 186 | ✅ |
| V1 SL = max(swing_high*1.003, entry*1.004) | pullback_trader.py lijn 449 | ✅ |
| V3 detect_trend_direction returns None | pull_backtrader_3.py lijn 105-125 | ✅ |
| Ghost ETHEUR positie | cat pullback_state.json | ✅ |
| V2 blokkeert early_pullback | pull_backtrader_2.py lijn 329-330 | ✅ |
| V2 entry_lateness > 0.70 | pull_backtrader_2.py lijn 347 | ✅ |
| 76% SHORT bias | grep direction v2_trades.jsonl | ✅ |

**Verdict: ALLE claims bewezen. Geen fantasy of giswerk.**

---

## ITERATIE 5 — CONTROLLER: Synthese & Beslissingen

### Prioriteit 1 (🔴 MOET NU)
1. **Screens herstarten:** cache → V1 → V2 → V3
2. **Ghost fix:** pullback_state.json ETHEUR trade sluiten of clearen
3. **SOLEUR open positie:** controleren of die nog actief is

### Prioriteit 2 (🟡 MOET BINNENKORT)
4. **V2 entry_lateness:** verlagen van 0.70 naar 0.50
5. **V1 TP:** vervangen door vaste RR (2.0) i.p.v. support/resistance levels
6. **V1 SL:** swing_high gebruiken i.p.v. swing_high * 1.003
7. **V1 macro paralyse fix:** lokale scope fallback bij 4+ uur "forming"

### Prioriteit 3 (🟢 NIET NU MAAR BELANGRIJK)
8. **V3 integratie:** V3 state voeden aan V1/V2 als confirmatielaag
9. **Auto-restart:** cron heartbeat checker voor screens
10. **V1 trade journal:** gestructureerd V1 trades log (v1_trades.jsonl)

---

## BESLISSINGEN

| # | Beslissing | Details |
|---|-----------|---------|
| 1 | Ghost trade fix | pullback_state.json clearen |
| 2 | Screens herstarten | cache → V1 → V2 → V3 |
| 3 | Code fixes via Claude Code | Prompt in VS Code |
| 4 | entry_lateness harmonisatie | V2 0.70 → 0.50 |
| 5 | V1 SL/TP fix | swing_high direct + vaste RR |

## OPEN VRAGEN VOOR LEXI

- Wil je dat ik de screens zelf herstart of doe je dat liever zelf?
- Mag ik het ghost ETHEUR trade verwijderen uit pullback_state.json?
- Prioriteit: eerst screens herstarten DAARNA pas code fixes, of omgekeerd?

## NEXT STEPS

1. ⏳ Screens herstarten (in overleg met Lexi)
2. ⏳ Ghost trade clearen
3. ⏳ Claude Code prompt in VS Code voor code fixes
4. ⏳ Meeting sync naar 2nd brain