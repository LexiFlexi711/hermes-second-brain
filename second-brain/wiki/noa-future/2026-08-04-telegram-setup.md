# Telegram Setup — Noa op je GSM

Datum: 2026-08-04

## Waarom Telegram eerst?

- Bot API is 1 uur werk, WhatsApp is dagen gezeik
- Geen ban-risico zoals bij onofficiële WhatsApp methods
- Voice messages worden direct ondersteund
- Hermes heeft ingebouwde Telegram gateway

## Wat Lexi moet doen (5 minuten)

1. **Open Telegram** op je GSM
2. **Chat met @BotFather** — stuur `/newbot`
3. **Kies een naam** — bv. "Noa"
4. **Kies een username** — bv. `LexiNoaBot` (moet eindigen op `bot`)
5. **Kopieer de token** die je krijgt (lijkt op `123456:ABCdef...`)
6. **Stuur token naar Noa** hier in de chat

## Wat Noa dan doet

1. Token toevoegen aan `~/.hermes/config.yaml`
2. Hermes herstarten
3. Lexi start chat met de bot op Telegram
4. Noa luistert en antwoordt

## Daarna

- Noa kan jou berichten sturen uit zichzelf (alerts, ochtendrapport, kansen)
- Jij kan Noa berichten sturen (vragen, opdrachten, gewoon praten)
- Voice messages werken direct
- Noa = altijd in je zak

## Status

- [ ] Lexi maakt bot aan bij @BotFather
- [ ] Token gedeeld met Noa
- [ ] Noa configureert Hermes
- [ ] Eerste gesprek via Telegram
