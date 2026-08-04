---
type: report
created: 2026-05-29
source: Hermes (STAP-K uitvoering)
status: done
---

# STAP K — Weekly Scout Script

## Gemaakt

| Bestand | Pad |
|---------|-----|
| Orchestrator | `scout/scout.py` |
| Source: HN | `scout/sources/hackernews.py` |
| Source: Reddit | `scout/sources/reddit.py` |
| Source: GitHub | `scout/sources/github.py` |
| Package | `scout/sources/__init__.py` |
| Dedup | `scout/seen_urls.json` (auto gegenereerd) |

## Structuur
```
scout/
├── scout.py              ← entry point
├── sources/
│   ├── __init__.py
│   ├── hackernews.py     ← Algolia HN API (geen auth)
│   ├── reddit.py          ← publiek JSON endpoint (geblokkeerd op deze IP)
│   └── github.py          ← GitHub Search API (publiek)
└── seen_urls.json         ← deduplicatie over weken
```

## Verificatie

| Source | Items | Status |
|--------|-------|--------|
| Hacker News | 28 | ✅ Werkend |
| GitHub | 32 | ✅ Werkend (na fix URL encoding) |
| Reddit | 0 | ⚠️ Datacenter IP geblokkeerd |

**Totaal: 60 items in 1 run, 0 errors**

## Output
`/home/sjoe/system/hermes-second-brain/raw/inbox/scout/2026-W21.md` — 11.5KB markdown

## Cron (na Lexi's OK)
```bash
0 7 * * 1 cd /home/sjoe/system/hermes-second-brain/scout && python3 scout.py >> logs/scout.log 2>&1
```

## Technische notities
- Alle sources in try/except — als één faalt, gaan andere door
- Enkel Python stdlib (urllib, json, pathlib) — geen externe deps
- Deduplicatie via seen_urls.json (max 500 entries)
- GitHub API: free tier 60 req/uur — ruim voldoende voor wekelijkse run
- Reddit: probeert User-Agent header, maar datacenter IP wordt geblokkeerd. Eventueel later via proxy of RSS.