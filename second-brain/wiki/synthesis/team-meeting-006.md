# TEAM MEETING 006 — Tradebot V1/V2 Audit & Fix Plan

## Doel
Volledige audit van de pullback trading bot (V1 + V2) op basis van live logs, met fixes voor monodirectionele bias, SL krimping, V1 macro-paralysis en orphaned positions.

## Aanwezige Rollen (Virtueel)
- **Lexi (Owner)** — voorzitter, eindbeslisser
- **Noa/Scout (Hermes)** — data verzameling uit logs
- **DevOps Guard (Hermes)** — runtime/screen/cache check
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
- **CLAUDE_CODE_CALLED:** JA (via Lexi-prompt, niet direct door Hermes)
- **DECISIONS_USABLE:** JA (alle bronnen getraceerd)

---

## ITERATIE 1 — Scout (data verzamelen)

**Bronnen:**
- `v2_trades.jsonl` (61 trades) — `/mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/projects/crypto-tradebot/logs/v2_trades.jsonl`
- `v2_cycles.jsonl` (2819 entries) — `/mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/projects/crypto-tradebot/logs/v2_cycles.jsonl`
- `v2_state.json` (2 orphaned positions) — `/mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/projects/crypto-tradebot/logs/v2_state.json`
- `scan_events.jsonl` (4992 entries) — `/mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/projects/crypto-tradebot/logs/scan_events.jsonl`
- `candle_battle_2026-05-20.log` (301784 lijnen) — `/mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/projects/crypto-tradebot/logs/candle_battle_2026-05-20.log`

**V2 Trades: WIN=15 LOSS=35 CANCELLED=11 (WR=30%)**
- SHORT: 47 (77%) | LONG: 14 (23%)
- ETHEUR: 2/10 WIN (16%) — alle 12 trades short
- SOLEUR: 3/8 WIN (27%) — alle 11 trades short
- INJEUR: 4/4 WIN (50%) — enige balanced pair (8 longs)
- SUIEUR: 0/4 WIN (0%)

**V1 Scanner (laatste scan 19 mei 19:14):**
- 13/16 pairs status=forming (fib <30%)
- 2/16 status=deep_warning (ETHEUR 62.5%, SOLEUR 62.6%)
- 0/16 allowed_to_enter
- 52% van scan_events heeft pb_scope=macro

**DevOps Guard:** Geen screens actief. Laatste cycle 19 mei 19:13. Bot ~24u out.

**Orphaned Positions in v2_state.json:**
- INJEUR LONG entry=4.335 SL=4.21 TP=4.585 (sinds 19 mei 17:00)
- RENDEREUR SHORT entry=1.577 SL=1.6064 TP=1.5182 (sinds 19 mei 18:45)

---

## ITERATIE 2 — Master Trader (analyse)

**Finding 1 — Monodirectioneel shorten (77% SHORT)**
47/61 trades short. ETHEUR 12/12 short, 10 verlies (16% WR). Geen long-mechanisme in bearish trend. Pullback LONGs (mean reversion na overshoot) worden nooit overwogen.

**Finding 2 — SL krimping naar 0.16%**
ETHEUR trade 12: SL=0.93%. Trade 18: SL=0.16%. Geen harde MIN_STOP vloer. In pull_backtrader_2.py is MIN_STOP_PCT een multiplier, geen harde afstandsgrens.

**Finding 3 — V1 macro-paralysis**
52% scan events macro-scope. BTC range $4917 (65K→70K), fib 19.6%. Moet $4K stijgen om 38.2% te bereiken.

**Finding 4 — Orphaned positions zonder heartbeat**
INJEUR + RENDEREUR sinds 19 mei 19:14 niet meer geëvalueerd.

**Finding 5 — entry_lateness niet in V2**
V2 miste entry_lateness check (in nieuwe versie toegevoegd).

---

## ITERATIE 3 — Critic (diepe analyse)

**Zwakste plek:** trade_engine.py heeft geen pullback detectie. V2 (pull_backtrader_2.py) heeft in NIEUWE versie richting-bewuste pullback setup.

**MIN_RR:** stond op 4.0 in code, alle 61 trades gebruiken 2.0. In nieuwe versie gefikst naar 2.0.

**SL krimping wiskundig bewijs:** ETHEUR SL progressie van 0.93% → 0.31% → 0.16% in opeenvolgende trades.

---

## ITERATIE 4 — QA Agent (validatie)

Alle bronnen getraceerd via live tool output:
- `v2_trades.jsonl` — 61 trades live uitgelezen ✅
- `v2_cycles.jsonl` — laatste entry 19 mei 19:13 bevestigd ✅
- `v2_state.json` — 2 orphaned positions bevestigd ✅
- `scan_events.jsonl` — 4992 entries, macro ratio bevestigd ✅
- `screen -ls` — 0 screens actief ✅
- `ls -la scripts/` — alle scripts bestaan ✅

**Conclusie: Alle claims onderbouwd. Geen fantasy.**

---

## ITERATIE 5 — Controller (synthese)

Nieuwe code (pull_backtrader_2.py vandaag 11:24 geüpdatet) heeft al:
- ✅ Richting-bewuste pullback (SHORT+LONG)
- ✅ MIN_IMPULSE_PCT=3%
- ✅ 15M bevestiging in 2 richtingen
- ✅ entry_lateness
- ✅ Volume check
- ✅ 1D filter voor shorts
- ✅ Pullback fast monitoring
- ✅ Multi-pair scanner
- ✅ MIN_RR=2.0 (trade_engine.py)
- ✅ _MIN_STOP_DIST=0.004 (trade_engine.py)

**Nog te implementeren via Claude Code prompt:**
1. calc_sl() — harde afstandsgrens i.p.v. multiplier
2. Heartbeat + orphaned recovery logging
3. V1 macro-paralysis fix (micro scope toevoegen)
4. V1 entry_lateness aanscherpen

---

## BESLISSINGEN

| # | Beslissing | Details |
|---|-----------|---------|
| 1 | **Prompt voor Claude Code** | Master Trader + Noa stellen prompt op voor Lexi om aan Claude Code in VS Code te geven |
| 2 | **Eerst pullback_trader.py fixen** | V1 macro-paralysis + entry_lateness aanscherpen |
| 3 | **Dan calc_s() fix** | Harde MIN_STOP afstandsgrens in V2 |
| 4 | **Heartbeat toevoegen** | Enkel logging, geen auto-restart |
| 5 | **Lexi beslist over timing** | Prompt klaar voor copy-paste naar VS Code |

---

## OPEN VRAGEN VOOR LEXI
- Start ze de screens manueel of wacht ze tot de code gepatcht is?
- Orphaned positions: manueel sluiten of laten lopen na restart?

## NEXT STEPS
1. ✅ Prompt klaar voor Claude Code (zie meeting output)
2. ⏳ Lexi geeft prompt aan Claude Code in VS Code
3. ⏳ Code patchen: calc_sl(), heartbeat, V1 macro fix
4. ⏳ Screens herstarten: cache → V1 → V2
5. ⏳ Monitor eerste trades na restart

---

**Secretary notities:** Meeting werd live gevolgd door Lexi. Alle data uit live tool calls. Claude Code wordt via Lexi's VS Code aangeroepen.