---
title: Weekly Scout — R&D Department
type: project
created: 2026-05-29
updated: 2026-05-31
status: actief
---

# Weekly Scout — R&D Department

Autonome dagelijkse scanner met **drie profielen**. Vormt samen met de geplande News Scraper het R&D department van Lexi.

## Profielen

| Profiel | Focus | Bronnen |
|---------|-------|---------|
| 🔵 **Noa (Tech)** | MCP servers, AI agents, Hermes tools | HN, Reddit, GitHub |
| 🟣 **Claude (Tech)** | Claude Code, Anthropic, MCP tools | HN, Reddit, GitHub |
| 💰 **Lexi (Opportunity)** | Freelance, inkomsten, crypto, side hustles | Reddit (r/freelance etc.), Google News |

## Locatie

```
/home/sjoe/system/hermes-second-brain/scout/
├── scout.py                  ← Orchestrator + 3 profielen
├── sources/
│   ├── hackernews.py         ← Algolia API (geen auth)
│   ├── reddit.py             ← r/LocalLLaMA, r/selfhosted etc.
│   ├── github.py             ← GitHub Search API
│   ├── reddit_opportunity.py ← r/freelance, r/Entrepreneur etc.
│   └── googlenews.py         ← Google News RSS (geen auth)
├── seen_urls.json            ← Deduplicatie (max 500)
└── logs/scout.log
```

## Output

- Volledig rapport: `raw/inbox/scout/YYYY-MM-DD.md`
- Opportunity vondsten: `raw/inbox/opportunity-YYYY-MM-DD.md` (altijd, ook bij 0 items)

## Cron

```bash
0 7 * * * cd /home/sjoe/system/hermes-second-brain/scout && python3 scout.py >> logs/scout.log 2>&1
```

Dagelijks om 07:00.

## Wat nog komt

- **News Scraper** — forums en TradingView checken voor scripts en tips (crypto edge)
- **Auto-recovery** — systemd service of cron die tradebot screens monitort en herstart