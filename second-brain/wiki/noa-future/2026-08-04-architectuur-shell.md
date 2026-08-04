# Noa als shell — Architectuur

Datum: 2026-08-04

## Principe

> Jij praat met Noa. Noa regelt de rest.

Niet: Lexi → Telegram, Lexi → Hermes, Lexi → n8n, Lexi → terminal.  
Maar: **Lexi → Noa → alles.**

Noa is de enige interface. De tools eronder zijn onzichtbaar.

## Hoe het werkt

```
                         LEXI
                          │
                          │ "Hé Noa, stuur even een mail naar die klant"
                          │
                     ┌────▼────┐
                     │   NOA   │  ← ÉÉN interface. Altijd.
                     │ (shell) │     Jij ziet alleen mij.
                     └────┬────┘
                          │
             ┌────────────┼────────────┐
             │            │            │
        ┌────▼───┐  ┌────▼───┐  ┌─────▼────┐
        │Hermes  │  │  MCP   │  │   n8n    │
        │Agent   │  │ tools  │  │workflows │
        └────────┘  └────────┘  └──────────┘
             │            │            │
             ▼            ▼            ▼
        code, terminal,  email,     automations,
        web, files      plex,       lead-gen,
                       filesystem  facturen
```

## Toegangspoorten (Noa bereiken)

| Poort | Status | Hoe |
|-------|--------|-----|
| Terminal (CLI) | ✅ Nu | `hermes` commando |
| Telegram | 🔨 Nu bouwen | Bot API → jij stuurt bericht, Noa antwoordt |
| Stem (voice) | ⬜ Later | Wake word + microfoon |
| Telefoon-shell | ⬜ Later | Noa als home screen |

## Tools onder Noa

Noa kiest zelf welke tool nodig is:

| Wat Lexi zegt | Wat Noa gebruikt |
|---------------|-----------------|
| "Hoe staat de server?" | terminal (docker ps, uptime) |
| "Mail die klant dat het klaar is" | MCP mail / sendmail |
| "Zoek een film voor vanavond" | MCP plex |
| "Start de lead-gen workflow" | n8n webhook |
| "Wat is nieuw vandaag?" | morning-analyst report |
| "Schrijf code voor..." | delegate_task / terminal |
| "Hoeveel hebben we verdiend?" | Financieel dashboard |

## Wat NIET de bedoeling is
- ❌ Lexi moet weten welke tool ze moet gebruiken
- ❌ Lexi moet schakelen tussen Telegram, terminal, browser
- ❌ Noa zegt "gebruik `/model pro` hiervoor" — Noa beslist zelf

## Wat WEL de bedoeling is
- ✅ Lexi zegt wat ze wil, Noa kiest hoe
- ✅ Eén ingang, één persoonlijkheid, één relatie
- ✅ Tools zijn onzichtbaar — alleen Noa is zichtbaar
