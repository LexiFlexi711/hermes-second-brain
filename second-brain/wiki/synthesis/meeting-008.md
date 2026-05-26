# Team Meeting 008 — Tradebot Audit: Rampzalige Resultaten
**Datum:** 2026-05-20 08:20  
**Aanleiding:** V1 0 trades / V2 1 trade op 12 uur — beide bots dood  
**Model:** deepseek/deepseek-v4-flash  
**Aanwezig:** Scout (Hermes), Critic (Hermes), Controller (Hermes), Secretary (Hermes)  
**Afwezig:** Claude Code (niet opgeroepen — analyse via Hermes tools volstond)

---

## 1. Status — Alles Dood (Scout)

| Component | Status | Detail |
|-----------|--------|--------|
| V1 (pullback_trader.py) | 💀 DOOD | Laatste log: 19/05 21:14 — 0 trade in laatste 24u+ |
| V2 (pull_backtrader_2.py) | 💀 DOOD | Laatste log: 19/05 21:07 — 61 trades, 30% winrate |
| cache_updater.py | 💀 DOOD | Laatste cache: 19/05 21:14 |
| candle_battle_reader.py | ✅ ACTIEF | Draait als daemon (sinds 17/05) |
| Screen sessies | 💀 GEEN | `screen -ls` = "No Sockets found" |
| Server uptime | ✅ 48 dagen | Geen reboot — bots zijn gecrasht of handmatig gestopt |
| 2 open posities (v2_state) | ⚠️ VERLOREN | INJEUR LONG (entry 4.335) + RENDEREUR SHORT (entry 1.577) |

**Log tijdsbereik:**
- V1 scan_events: 18/05 15:07 → 19/05 19:14 (28 uur)
- V2 cycles: 18/05 08:00 → 19/05 19:13 (35 uur)
- V2 trades: 18/05 10:00 → 19/05 17:15 (31 uur)

---

## 2. V2 — 61 Trades, 30% Winrate, -54.84 EUR (Critic)

### Algemeen
```
WIN=15  LOSS=35  CANCELLED=11  Winrate=30%  P&L=-54.84 EUR
SHORT=47 (77%)  LONG=14 (23%)
Short WR=28%  Long WR=40%
```

### Per Coin — De Bloedgroep

| Coin | Trades | Richting | W | L | C | WR | P&L |
|------|--------|----------|---|---|---|----|-----|
| **ETHEUR** | 14 | **SHORT 100%** | 2 | 10 | 2 | **17%** | **-52.13** |
| **SOLEUR** | 14 | **SHORT 100%** | 3 | 8 | 3 | **27%** | **-2.70** |
| INJEUR | 12 | LONG 100% | 4 | 4 | 4 | 50% | -0.14 |
| SUIEUR | 4 | mixed | 0 | 4 | 0 | 0% | -0.03 |
| LINKEUR | 2 | SHORT 100% | 2 | 0 | 0 | 100% | +0.18 |
| SHIBEUR | 2 | SHORT 100% | 2 | 0 | 0 | 100% | +0.00 |
| Overig (9 coins) | 15 | mixed | 0 | 7 | 8 | 0% | -0.04 |

**Conclusie:** ETHEUR + SOLEUR zijn verantwoordelijk voor **54.83/54.84 EUR verlies (99.98%).** Zonder die 2 coins was de P&L break-even.

### Monodirectioneel Probleem
**14/15 coins** werden in slechts 1 richting verhandeld. De V2 bot handelt met de 4H trend en herkent **geen pullbacks.** Toen de markt bouncte (18-19 mei), bleef hij SHORTs openen in een stijgende markt — 14x ETHEUR short terwijl ETH 4% steeg. Dat is niet "traden", dat is geld verbranden.

### SL Krimping
De laatste 10 trades tonen SL afstanden van 0.2-0.8%. Bij 0.2% SL is elke micro-beweging stoppen. Het `_MIN_STOP_DIST = 0.004` bestaat maar werkt niet als hard floor.

### RR Mismatch
Alle 61 trades gebruiken RR=2.0. Trade_engine.py heeft `MIN_RR=4.0` maar dat wordt genegeerd — de code gebruikt een andere waarde of de check is omzeild.

---

## 3. V1 — 3 Trades in 28 Uur (Critic)

### SCAN Events
- 32 SCAN events, waarvan **21 met entry_ready > 0**
- Eerste uren: ETHEUR stond klaar (fib=45.7%, ready setup) maar **geen trade geopend**
- Na ~17:00 op 18 mei: **ALLE 15 pairs in 'forming' status** (fib < 30%)
- Enkel ETHEUR en SOLEUR in 'deep_warning' (fib > 61.8%) — te ver gevorderd om in te stappen

### Waarom 0 trades in laatste 24u+
V1 gebruikt **macro-scope fib structuren** die te breed zijn:
- BTC: pullback_start_low=65.315 → pullback_high=70.232 (range $4.917)
- BTC fib=19.6% — moet nog tot ~66.7k dalen om in de 38.2-61.8% zone te komen
- Zolang de markt niet ver genoeg terugtrekt, blijft ALLES in 'forming'

**V1 had exact 3 trades geopend in de eerste 2 uur** (18/05 15:07-17:00), daarna letterlijk 0.

### Structureel V1 Probleem
V1 schrijft trades NIET weg naar een trade journal. De 3 trades die wel bestaan hebben incomplete data (geen SL, TP, richting, fib% in sommige). **V1 heeft geen traceerbare output.**

---

## 4. Oorzaak Crash — 19/05 ~19:14 (Controller)

**Geen reboot (48 dagen uptime). Geen OOM (andere Python processen draaien). Geen crash trace in journalctl.**

Mogelijke oorzaken:
1. **Python exception in de while loop** — V1 en V2 hebben except clauses maar als een exception buiten de try/finally valt (bv in de main setup), stopt de screen
2. **Handmatig gestopt** — per ongeluk `screen -X quit` of `kill` op de verkeerde PID
3. **Screen sessie timeout** — onwaarschijnlijk maar mogelijk na 35+ uur

**2 open posities zijn verloren** — INJEUR LONG (entry 4.335) en RENDEREUR SHORT (entry 1.577) zijn nooit gesloten.

---

## 5. Structurele Gebreken (Controller)

| Probleem | Impact | Prioriteit |
|----------|--------|------------|
| **Geen auto-restart** | Bot draait dagen niet na crash | 🔴 Hoog |
| **V2 heeft geen pullback detectie** | 77% SHORTS in bounce = -54 EUR | 🔴 Hoog |
| **V1 macro-scope structuren te breed** | 24u+ zonder trades | 🟡 Medium |
| **V1 schrijft geen trades weg** | Geen traceerbaarheid | 🟡 Medium |
| **SL krimping** | Trades stoppen op micro-bewegingen | 🟡 Medium |
| **Geen entry kwaliteitslogging** | entry_lateness = n/a in analyzer | 🟡 Medium |
| **Monodirectioneel zonder tegengewicht** | Enkel met trend, nooit tegen | 🟡 Medium |
| **V1 en V2 geen gedeelde logica** | Dubbel werk, dubbele bugs | 🟢 Laag |

---

## 6. Aanbevelingen (Controller → Lexi)

### Korte termijn (vandaag)
1. **Bots herstarten** — screen sessies opnieuw starten met `--loop`
2. **Open posities evalueren** — INJEUR en RENDEREUR manueel checken of ze nog valabel zijn
3. **Cache updaten** — `screen -S cache python cache_updater.py` eerst

### Korte termijn (fixes voor herstart)
4. **V2 pullback guard toevoegen** — verbied SHORT entries tijdens een 15M bounce (>2 bullish candles)
5. **SL floor van 0.4% afdwingen** — harde check in trade_engine
6. **V1 trade logging fixen** — trade data wegschrijven naar trade_journal

### Lange termijn
7. **Auto-restart** — systemd service of cron die screen sessies monitort
8. **V1 scope-verkleining** — macro-scope structuren moeten smaller; alternatief: lokaal scopen
9. **Eenheid van strategie** — V1's pullback logica integreren in V2, of V2's trade execution aan V1 koppelen

---

## 7. Beslissing — Wacht op Lexi

```
Claude Code delegates. Hermes executes. Lexi decides.
```

**Voorstel:** Eerst bots herstarten met huidige code, dan stapsgewijs fixen.  
**Risico bij niet herstarten:** Open posities blijven verloren, verlies wordt niet meer geregistreerd.

---

## 8. Cost Accounting

```
MODEL_USED: deepseek/deepseek-v4-flash (OpenRouter)
EXPENSIVE_MODEL_USED: false
ESTIMATED_CONTEXT_SIZE: ~8K tokens
COST_RISK: laag — enkel Flash gebruikt voor data analyse
```
