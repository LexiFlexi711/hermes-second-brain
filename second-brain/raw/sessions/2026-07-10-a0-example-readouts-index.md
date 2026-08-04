# A0 EXAMPLE READOUTS INDEX

## 1. Status

A0 voorbeeldreadouts zijn vastgelegd als documentatie.

Deze bestanden zijn géén pipeline-input.

A0 output is presentation, not data.

## 2. Bron

Commit:
- f55a22c537e26a32e805a5a7612d2876f5db7546
- Add A0 snapshot readout scaffold

## 3. Voorbeeldreadouts

| Pair | Bestand | Format |
|------|---------|--------|
| ETHEUR | raw/sessions/a0-example-readouts/2026-07-10-a0-example-ETHEUR.md | markdown |
| BTCEUR | raw/sessions/a0-example-readouts/2026-07-10-a0-example-BTCEUR.md | markdown |

## 4. Belangrijke grens

Deze readouts mogen niet gebruikt worden als input voor:
- Analyst A1
- Outcome Builder
- Strategy Test Harness
- Testbot
- Paper Trader
- Live Trader

Latere lagen moeten snapshots/gestructureerde data lezen, niet A0-proza.

## 5. Wat deze voorbeelden tonen

Deze voorbeelden tonen:
- hoe A0 echte L4 snapshots weergeeft
- hoe stored_values zichtbaar worden gemaakt
- hoe scope notes zichtbaar zijn
- hoe guardrails output beperken
- hoe A0 context toont zonder tradebeslissing

## 6. Wat deze voorbeelden NIET tonen

Deze voorbeelden tonen NIET:
- een trade
- een setup
- een entry
- een exit
- een buy/sell-signaal
- een long/short advies
- een voorspelling
- een score
- een candidate/no_candidate oordeel

## 7. Conclusie

A0 voorbeeldreadouts zijn documentatievoorbeelden.

Projectlijn blijft:

Crypto-data
→ Hermes chart reader
→ Interpreter / L4 store
→ A0 Snapshot Readout

Nog gesloten:

→ Analyst A1
→ Outcome Builder
→ Strategy Test Harness
→ Testbot
→ Paper Trader
→ Live Trader
