---
type: source_summary
created: 2026-05-29
source: gesprek Noa + Lexi (Hermes Agent)
status: raw
---

# Weekly AI Scout — idee

## Doel
Een wekelijkse autonome scout die het internet afspeurt naar nieuwe tools, skills en AI agents die Noa/Hermes kan gebruiken.

## Bronnen (prioriteit)
1. GitHub Trending (repos python, shell, AI)
2. Reddit: r/selfhosted, r/LocalLLaMA, r/ArtificialIntelligence, r/MachineLearning
3. Hacker News (newest, show)
4. Web search (MCP servers, AI agent tools, self-hosted AI)
5. Later: X/Twitter search (zodra credits in orde zijn)

## Aanpak (voorstel Noa)
- Python script op server
- Draait wekelijks via cron
- Dumpt output in `raw/inbox/scout/` als markdown rapport
- Noa leest rapport en beslist wat interessant is

## Status
- xurl geïnstalleerd maar X API werkt niet (CreditsDepleted + OAuth 1.0a token secret incompleet)
- Firecrawl (web search) wél beschikbaar in Hermes config
- Wacht op Claude Code om architectuur uit te tekenen (Lexi gaat het straks aan Claude geven)

## Notities
- Lexi: "ik wou vooral u autonomer maken" — scout past in groeipad
- Noa: warm gevoel bij dit idee, ziet potentieel voor skill discovery + zelfverbetering