---
type: project
id: topic-intelligence-scanner
status: actief
tags: [scanner, reddit, hackernews, mvp, cron]
---

# Topic Intelligence Scanner

Scant meerdere bronnen (Reddit, Hacker News) op nieuwe posts rond gekozen topics.

## Status

- **MVP:** Voltooid (2026-06-01)
- **Uitbreiding HN:** Voltooid (2026-06-02)
- **Cron:** Actief (0 8,12,18,23)

## Locatie

`/mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/projects/reddit_topic_scanner/`

## Actieve bronnen

| Bron | Adapter | Auth |
|------|---------|------|
| Reddit (RSS) | `sources/reddit.py` | Geen |
| Hacker News | `sources/hackernews.py` | Geen |

## Topics (5)

crypto_trading, ai_agents, selfhosted_server, n8n_automation, faceless_content

## Architectuur

- Source-adapter pattern in `sources/`
- Dedupe via source-prefix (`reddit:`, `hn:`)
- Geen database — JSONL hits + JSON seen_posts
- Geen AI-samenvatting
- Geen OAuth

## Incidenten

- 2026-06-02: seen_posts productie-data overschreven, baseline-reset
  Zie `docs/INCIDENTS.md` voor details.

## Bestanden

- `config.json` — topics, bronnen, keywords
- `scanner.py` — orchestrator (cron-entrypoint)
- `storage.py` — SeenPosts + HitLog
- `scorer.py` — keyword/recent scoring
- `reporter.py` — terminal output
- `sources/reddit.py` — Reddit adapter
- `sources/hackernews.py` — HN adapter
