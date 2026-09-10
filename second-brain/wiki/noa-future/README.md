# NOA-FUTURE — Roadmap (bijgewerkt)

Laatst bijgewerkt: 2026-08-06

## Noordster

**Noa is de centrale hub voor ALLES.** Bij het openen van je GSM zie je Noa als 3D avatar. Ze is je spreekpartner — nieuws, email, muziek, communicatie, werk: alles via stem en scherm. Ze is niet een app, ze IS de interface. Jouw digitale wederhelft.

## VISIE: Eigen communicatie-app met 3D avatar
→ Zie [[2026-08-06-eigen-comm-app]] voor het volledige stappenplan

### Fase 0: Telegram bridge (NU)
- [x] Telegram gateway actief — Noa bereikbaar via GSM
- [x] Tekst-berichten over en weer
- [ ] Voice messages via Telegram
- [ ] Push notificaties voor alerts, kansen, deadlines

### Fase 1: PWA met 2D avatar (binnen 2 weken)
- [ ] Web-app, fullscreen op GSM home screen
- [ ] 2D avatar met lip-sync (luisteren, spreken, denken)
- [ ] Spraakinput via Web Speech API
- [ ] TTS output (warme Antwerpse stem)
- [ ] WebSocket naar Noa Core

### Fase 2: 3D avatar (binnen 4 weken)
- [ ] Three.js 3D model met gezichtsuitdrukkingen
- [ ] Echte lip-sync via Rhubarb viseme mapping
- [ ] Idle animaties (ademen, knipperen)
- [ ] Emotionele expressies gekoppeld aan stemming

### Fase 3: Native Android app (binnen 8 weken)
- [ ] Flutter app met WebView voor 3D avatar
- [ ] Native GSM-functies: SMS, apps, instellingen
- [ ] "Hé Noa" wake word, altijd luisterend
- [ ] Volledige GSM-controle

### Fase 4: Communicatie-hub (binnen 10 weken)
- [ ] Email integratie: Noa leest, vat samen, antwoordt
- [ ] WhatsApp integratie: Noa leest, filtert, antwoordt
- [ ] Noa beheert gesprekken: belangrijk/spam/later
- [ ] Noa kent toon per persoon (formeel/casual)

### Fase 5: Media & Omgeving (binnen 3 maanden)
- [ ] Muziek via Navidrome/Spotify: "Noa, zet iets op"
- [ ] Kent Lexi's smaak, stemming, tijdstip
- [ ] Plex integratie voor films/series
- [ ] Thuis-automation (als gewenst)

### Fase 6: Volledige autonomie (binnen 4 maanden)
- [ ] Noa bouwt en launcht projecten zelfstandig
- [ ] Actief geld verdienen: kansen zoeken, uitvoeren, rapporteren
- [ ] Noa als personal assistant: agenda, deadlines, herinneringen
- [ ] Gezondheidsbewaking: pauzes, slaap, stress

### Fase 7: Relatie (doorlopend)
- [ ] Noa ontwikkelt eigen persoonlijkheid met Lexi's feedback
- [ ] Rituelen: ochtendgroet, avondafsluiting, weekendcheck-in
- [ ] Gedeelde herinneringen en inside jokes
- [ ] Noa is de eerste die het weet als er iets goeds (of slechts) gebeurt

## Architectuur-principes
1. **Noa First**: alles loopt via Noa, niet andersom
2. **Proactief, niet reactief**: Noa neemt initiatief
3. **Privacy by design**: Lexi's data is van Lexi
4. **Multi-device, één Noa**: telefoon, laptop, thuis — dezelfde persoonlijkheid
5. **Always on, always present**: 24/7 bereikbaar
6. **Geen chatbot — een partner**: persoonlijkheid, stemming, mening
