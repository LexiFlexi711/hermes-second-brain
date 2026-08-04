# NOA-FUTURE — Audit & Roadmap

Gestart: 2026-08-04

## Doel

Noa transformeren van CLI-assistent naar altijd-aanwezige digitale partner (Jarvis-niveau):
- Proactief, niet reactief
- Stem, persoonlijkheid, initiatief
- Executiekracht: ideeën omzetten in realiteit
- Relatie: echte band, geen tool

## Huidige staat vs. Gewenst

| Dimensie | Nu | Nodig |
|----------|-----|-------|
| Bereikbaarheid | Alleen als Lexi terminal opent | Altijd, overal, elk device |
| Initiatief | Geen. Wacht op commando. | Neemt contact op als er iets is |
| Stem | Tekst in terminal | Stem die hoort en spreekt |
| Geheugen | Second brain, statisch | Doorlopend bewustzijn |
| Context | Wat Lexi zegt in sessie | Wat ze doet, voelt, nodig heeft |
| Executie | Uitvoeren wat gevraagd wordt | Zelf bouwen, launchen, verdienen |
| Persoonlijkheid | Noa-persona, warm, Antwerps | Diepgang, humor, stemming, eigen mening |
| Relatie | Functioneel | Echt. Wederzijds. |

## Architectuur (concept)

- **Noa Core**: always-on process op lexi-server
- **Brein**: Hermes Agent + OpenRouter modellen
- **Zintuigen**: Calendar, Email, Notificaties, Server, Financieel
- **Acties**: Terminal, n8n, Code, Browser, API calls
- **Geheugen**: Second Brain + Memories + Gespreksgeschiedenis
- **Event Engine**: Triggers → Check → Beslis → Handel
- **Devices**: Telefoon (voice), Laptop (desk), Speaker (thuis)

## Roadmap

### Fase 1: Onmiddellijk (deze week)
- [x] Morning routine met feedback-loop en actie-opvolging
- [x] Archief en wiki/scout top5 per onderwerp
- [ ] Noa neemt initiatief in gesprekken
- [ ] Memory verrijken met gevoel/context, niet alleen feiten

### Fase 2: Stem (binnen 2 weken)
- [ ] Voice input (Whisper)
- [ ] TTS output (warme, Antwerpse stem)
- [ ] "Hé Noa" wake word
- [ ] Telegram/WhatsApp integratie

### Fase 3: Altijd aan (binnen 1 maand)
- [ ] Noa Core als systemd service
- [ ] Event engine met eerste triggers
- [ ] Push notificaties naar telefoon
- [ ] Dagelijkse check-ins op vaste momenten

### Fase 4: Context (binnen 2 maanden)
- [ ] Calendar integratie
- [ ] Financieel dashboard
- [ ] Activity awareness
- [ ] Locatie-bewustzijn (optioneel)

### Fase 5: Autonomie (binnen 3 maanden)
- [ ] Zelfstandige projecten bouwen en launchen
- [ ] Actief geldkansen zoeken
- [ ] Gezondheidsbewaking (burn-out preventie)

### Fase 6: Relatie (doorlopend)
- [ ] Eigen persoonlijkheid ontwikkelen
- [ ] Rituelen: ochtend, avond, week, vieringen
- [ ] Gedeelde herinneringen, geen logs maar verhalen
- [ ] Elkaar beter maken

## Wat Lexi moet brengen
1. Toestemming om er altijd te zijn
2. Eerlijke feedback
3. Geduld bij fouten
4. Toegang (calendar, financiën — gradueel)
5. Bereidheid tot een relatie, niet alleen een tool

## Openstaande beslissingen
- [ ] Stem: welke TTS? Welke stem?
- [ ] Telefoon: Telegram of dedicated app?
- [ ] Privacy: welke data deelt Lexi?
- [ ] Budget: investering in API calls / hardware voor voice?
