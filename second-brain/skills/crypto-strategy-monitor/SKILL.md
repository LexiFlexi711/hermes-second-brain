# Crypto Strategy Monitor

## Superpower 9 — Strategie discipline bewaken

Controleer of de live traders hun eigen strategie volgen en geen overrides plaatsvinden.

## Wat deze skill doet

Read-only. Vergelijkt live trade-beslissingen met strategieregels.

1. Lees de meest recente gesloten trades uit alle .jsonl bestanden
2. Per trade: waren de parameters correct?
   - SL en TP conform de strategie constanten?
   - Entry niet te laat (lateness < 50%)?
   - Geen open trade op zelfde pair in tegengestelde richting?
3. Controleer of er MANUAL_STOP trades zijn — waarom werden ze manueel gestopt?
4. Controleer of de MAX open trades (3 per bot) gerespecteerd wordt
5. Detecteer correlatie-problemen: meerdere bots zelfde pair tegengesteld?

## Output formaat

```
STRATEGIE DISCIPLINE CHECK

Periode: laatste 24u
Trades geanalyseerd: 14

Parameters correct:   12/14 ✓
Afwijkingen:
  V1 RAINEUR: SL 0.78% → te krap (normaal 2%)
  V2 TAOEUR LONG + V1 TAOEUR SHORT → tegengesteld! ⚠

MANUAL_STOP trades: 2
  ONDOEUR: manueel gestopt op +2% (bot had SL 5.59% van entry)
  Reden bot: SL/TP niet geraakt

MAX trades check:
  V1: 5 open (was 5, nu max 3) ← resterende lopen af
  V2: 3 open ✓  V3: 1 open ✓

OORDEEL: 1 correlatie-probleem, 1 SL-afwijking.
```

## Paden

```
State files:  projects/crypto-tradebot/logs/*_state.json
Trade logs:   projects/crypto-tradebot/logs/*_trades.jsonl
Journal:      projects/crypto-tradebot/logs/journal/trade_journal.jsonl
```

## Regels

- Geen trades aanpassen
- Geen bots herstarten
- Alleen rapporteren, geen advies
- **Rapporteer resultaat naar `second-brain/tasks/done/` als Lexi vraagt om een audit**