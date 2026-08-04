# A0 PHASE 1 COMMIT STATUS

## 1. Status

A0 Snapshot Readout Phase 1 is gecommit en remote geverifieerd.

Commit:
- f55a22c537e26a32e805a5a7612d2876f5db7546
- Add A0 snapshot readout scaffold

## 2. Wat A0 Phase 1 is

A0 Phase 1 is een read-only snapshot readout scaffold.

A0 doet:
- L4 snapshots lezen
- raw_blob velden whitelisten
- OHLC/candle-array backdoor blokkeren
- opgeslagen velden via vaste templates tonen
- stored_value exceptions veilig behandelen
- text/markdown/json output guardrailen
- CLI scaffold aanbieden
- tests met temp fixtures draaien

A0 is:
- presentatie
- readout
- contextweergave
- auditbare menselijke leeslaag

A0 is NIET:
- Analyst A1
- datalaag
- strategy engine
- outcome engine
- testbot
- trader
- entry/exit systeem
- signal engine

## 3. Architectuurregel

A0 output is presentation, not data.

Latere lagen mogen A0-output niet parsen als input.

Latere lagen moeten snapshots/gestructureerde data lezen, niet A0-proza.

## 4. Bewezen technische eigenschappen

Vastleggen:

- SQLite reader gebruikt mode=ro
- schema_version bewezen als raw_blob.meta.schema_version = 1
- ALLOWED_SCHEMA_VERSIONS = {1}
- contract_version ontbreekt in productie en wordt in Phase 1 toegestaan als missing
- raw_blob whitelist actief
- forbidden OHLC keys worden geblokkeerd
- price.current en price.previous mogen geen list zijn
- stored_values mogen forbidden woorden alleen tonen als opgeslagen waarde via whitelisted path
- guardrails scannen text, markdown en json
- JSON scope_notes en stored_values zijn correct afgehandeld
- false-positive bypass rond belong/longer/selloff is dicht
- CLI exit codes 2/3/4/5 zijn gedekt
- markdown headings zijn hersteld
- pair wordt correct getoond
- geen productie-DB gebruikt in tests

## 5. Tests

Vastleggen:

| Suite | Resultaat |
|-------|-----------|
| A0 Snapshot Readout | 50/50 groen |
| Inspector | 15/15 groen |
| Runner | 76/76 groen |
| Totaal | 141/141 groen |

## 6. Wat nu NIET openstaat

Nog niet bouwen:

- Analyst A1
- Outcome Builder
- Strategy Test Harness
- Testbot
- Paper Trader
- Live Trader
- candidate/no_candidate
- setup scoring
- trade confidence
- entry/exit logic
- buy/sell/long/short beslissingen
- MTF alignment/conflict oordeel
- support/resistance herberekening
- indicator herberekening
- candle-array reconstructie

## 7. Volgende veilige stap

Volgende veilige stap is géén grotere trader bouwen.

Mogelijke veilige volgende stappen later:

1. A0 smoke op echte latest snapshot, read-only, zonder output als data te gebruiken.
2. A0 voorbeeldreadouts opslaan als documentatie, niet als pipeline-input.
3. A0 review rubric maken.
4. Daarna pas nadenken over Outcome Builder plan.
5. Analyst A1 pas na Outcome/Strategy-harness fundament.

## 8. Conclusie

A0 Phase 1 staat op de projectlijn.

Huidige lijn:

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
