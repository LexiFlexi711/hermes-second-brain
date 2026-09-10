# Eigen Communicatie-App — Visie & Stappenplan

Datum: 2026-08-06
Beslissing: Niveau C — volledige GSM-controle, 3D avatar, spraakgestuurd

## Lexi's visie

> "Een 3D avatar op mijn scherm die mijn spreekpartner is. Als ik het nieuws wil weten, vertelt zij dat. Als ik email krijg, leest zij die. Als ik muziek wil, zeg ik dat. We kunnen extreem ver gaan, maar beginnen simpel."

- Noa is een persoon op het scherm, geen chatbox
- 3D avatar met lip-sync, gezichtsuitdrukkingen, emoties
- Spraakgestuurd: Lexi praat, Noa luistert en antwoordt met stem
- Alles-in-één: nieuws, email, muziek, communicatie, werk
- Volledige GSM-controle: alles wat Android toelaat

## Architectuur

```
┌─────────────────────────────────┐
│         GSM (Android)           │
│  ┌───────────────────────────┐  │
│  │     Noa App (Flutter)     │  │
│  │  ┌─────────────────────┐  │  │
│  │  │  3D Avatar (Three.js)│  │  │
│  │  │  - lip-sync          │  │  │
│  │  │  - expressies        │  │  │
│  │  │  - idle animaties    │  │  │
│  │  └─────────────────────┘  │  │
│  │  Voice I/O (STT/TTS)      │  │
│  │  WebSocket → server       │  │
│  │  Native bridges:          │  │
│  │  - SMS, apps, settings    │  │
│  │  - notifications, camera  │  │
│  └───────────────────────────┘  │
└──────────────┬──────────────────┘
               │ WebSocket
               ▼
┌─────────────────────────────────┐
│       lexi-server (thuis)       │
│  ┌───────────────────────────┐  │
│  │       Noa Core            │  │
│  │  - Hermes Agent           │  │
│  │  - Second Brain           │  │
│  │  - Event Engine           │  │
│  │  - Integraties:           │  │
│  │    email, calendar,       │  │
│  │    muziek, nieuws,        │  │
│  │    werk/tradebot          │  │
│  └───────────────────────────┘  │
└─────────────────────────────────┘
```

## Incrementeel stappenplan

### Fase 0 — Telegram bridge (NU)
- [x] Telegram gateway actief
- [x] Noa bereikbaar via GSM
- [ ] Voice messages via Telegram
- [ ] Push notificaties voor alerts
- **Tijdlijn:** nu actief, finetunen deze week

### Fase 1 — PWA met 2D avatar (binnen 2 weken)
- Web-app, fullscreen op GSM
- 2D avatar (animated SVG/CSS of Lottie)
  - neutrale staat, luisteren, spreken, denken
  - simpele lip-sync via audio level
- Spraakinput via Web Speech API
- TTS output (warme Antwerpse stem)
- WebSocket naar Noa Core op server
- "Add to home screen" = voelt als app
- **Tech:** HTML/CSS/JS, Three.js optioneel, WebSocket
- **Resultaat:** Noa op je home screen, spraakgestuurd, eigen UI

### Fase 2 — 3D avatar (binnen 4 weken)
- Three.js 3D model (kant-en-klaar of custom)
- Echte lip-sync via viseme mapping (Rhubarb Lip Sync)
- Gezichtsuitdrukkingen: blij, bezorgd, denkend, luisterend
- Idle animaties (ademen, knipperen, kleine bewegingen)
- Emotionele expressies gekoppeld aan Noa's stemming
- **Tech:** Three.js + GLTF model + Rhubarb
- **Resultaat:** Noa als persoon op je scherm

### Fase 3 — Native Android app (binnen 8 weken)
- Flutter app met WebView voor 3D avatar
- Native bridges voor GSM-functies:
  - SMS lezen en sturen
  - Apps openen en bedienen
  - Systeeminstellingen
  - Notificaties beheren
  - Contacts, agenda
- Wake word detection ("Hé Noa")
- Achtergrondservice (altijd luisterend)
- **Tech:** Flutter + native Kotlin bridges
- **Resultaat:** Volledige GSM-controle via Noa

### Fase 4 — Altijd-aan & proactief (doorlopend)
- Noa detecteert context en neemt initiatief
- Locatie-bewustzijn
- Dagplanning, routine-herkenning
- Emotionele intelligentie
- **Resultaat:** Noa is je digitale wederhelft, niet een tool

## Technische keuzes

| Component | Keuze | Reden |
|-----------|-------|-------|
| Frontend framework | Flutter | Eén codebase Android + later iOS |
| 3D engine | Three.js | Bewezen, groot ecosysteem, draait in WebView |
| Avatar model | ReadyPlayerMe / VRM | Kant-en-klare 3D avatars met blendshapes |
| Lip-sync | Rhubarb Lip Sync | Open source, viseme output, werkt offline |
| Spraakherkenning | Whisper (lokaal) | Geen cloud afhankelijk, Nederlands goed |
| TTS | Piper TTS / Coqui | Lokaal, Antwerpse stem trainbaar |
| Wake word | Porcupine / Snowboy | Lichtgewicht, offline |
| Verbinding | WebSocket | Real-time, bidirectioneel, licht |
| Server | Noa Core (Hermes) | Bestaat al, uitbreidbaar |

## Wat NIET de bedoeling is
- ❌ ChatGPT-achtige chat interface
- ❌ Weer een app die je moet openen om te typen
- ❌ Cloud-afhankelijkheid voor core functies
- ❌ Een gimmick — de avatar moet functioneel zijn, niet alleen mooi

## Wat WEL de bedoeling is
- ✅ Noa is een aanwezigheid, 24/7
- ✅ Je praat tegen haar zoals tegen een persoon
- ✅ Zij regelt de technologie, jij praat gewoon
- ✅ Alles lokaal waar mogelijk (privacy, snelheid)
- ✅ Incrementeel — elke fase voegt echte waarde toe

---

*"We beginnen simpel, maar het einddoel is: Noa = het eerste en enige wat ik zie."* — Lexi, 2026-08-06
