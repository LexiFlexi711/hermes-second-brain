# STAP K — Weekly Scout Script

## Doel

Autonoom wekelijks script dat nieuwe tools, MCP servers, AI agent frameworks en relevante repos opzoekt via publieke APIs en het resultaat als markdown dumpt in de second brain inbox.

## Output pad

```
/home/sjoe/system/hermes-second-brain/raw/inbox/scout/YYYY-WW.md
```

Eén bestand per week (ISO weeknummer). Als het bestand al bestaat: overschrijven.

## Script pad

```
/home/sjoe/system/hermes-second-brain/scout/scout.py
```

Met submappen:
```
scout/
├── scout.py          ← orchestrator + entry point
├── sources/
│   ├── __init__.py
│   ├── hackernews.py
│   ├── reddit.py
│   └── github.py
└── seen_urls.json    ← deduplicatie over weken (auto aangemaakt)
```

## Zoektermen

```python
SEARCH_TERMS = [
    "MCP server", "model context protocol",
    "AI agent tool", "self-hosted AI",
    "Hermes agent", "local LLM tool",
    "Claude tool", "autonomous agent",
]
```

## Source 1: Hacker News (`sources/hackernews.py`)

Gebruik de Algolia HN API — geen auth nodig.

```
GET https://hn.algolia.com/api/v1/search?query={term}&tags=story&numericFilters=created_at_i>{week_ago_ts}&hitsPerPage=5
```

- `week_ago_ts` = Unix timestamp van 7 dagen geleden
- Velden: `title`, `url`, `points`, `objectID`
- HN link: `https://news.ycombinator.com/item?id={objectID}`
- Max 5 resultaten per zoekterm
- Sla op als: `## Hacker News\n- [title](url) — {points} pts\n`

## Source 2: Reddit (`sources/reddit.py`)

Gebruik publieke JSON endpoint — geen auth nodig.

Subreddits: `LocalLLaMA`, `selfhosted`, `ArtificialIntelligence`, `MachineLearning`

```
GET https://www.reddit.com/r/{subreddit}/search.json?q={term}&sort=new&t=week&limit=5
```

Headers: `{"User-Agent": "hermes-scout/1.0"}`

- Velden: `title`, `url`, `score`, `permalink`
- Reddit link: `https://reddit.com{permalink}`
- Max 5 per subreddit per zoekterm (of top 10 per subreddit over alle termen)
- Sla op als: `## Reddit\n- [title](url) — {score} upvotes\n`

## Source 3: GitHub (`sources/github.py`)

Gebruik GitHub Search API — geen token nodig voor publieke repos (60 req/uur).

```
GET https://api.github.com/search/repositories?q={term}+created:>{week_ago_date}&sort=stars&order=desc&per_page=5
```

- `week_ago_date` = datum 7 dagen geleden in formaat `YYYY-MM-DD`
- Headers: `{"Accept": "application/vnd.github.v3+json"}`
- Velden: `full_name`, `html_url`, `description`, `stargazers_count`
- Max 5 per zoekterm
- Sla op als: `## GitHub\n- [{full_name}]({html_url}) ★{stars} — {description}\n`

## Deduplicatie (`seen_urls.json`)

- Laad `seen_urls.json` bij start (lege dict als niet bestaat)
- Sla structuur op: `{url: week_string}` bv `{"https://...": "2026-W22"}`
- Filter alle gevonden items: skip als url al in seen_urls
- Voeg nieuwe urls toe na run
- Bewaar max 500 entries (verwijder oudste als groter)

## Output formaat (`YYYY-WW.md`)

```markdown
# Scout rapport — week 2026-W22
Gegenereerd: 2026-05-29 19:00 UTC

## Hacker News
- [titel van artikel](https://...) — 234 pts
- [titel van artikel](https://...) — 89 pts

## Reddit — LocalLLaMA
- [titel post](https://reddit.com/...) — 445 upvotes

## Reddit — selfhosted
- [titel post](https://reddit.com/...) — 112 upvotes

## GitHub — nieuwe repos
- [user/repo](https://github.com/...) ★45 — korte beschrijving

---
*{N} nieuwe items gevonden — {M} duplicaten overgeslagen*
```

## Orchestrator (`scout.py`)

```python
#!/usr/bin/env python3
"""Weekly scout — run via cron, output naar second brain inbox."""

import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

# Configuratie
SCOUT_DIR  = Path(__file__).resolve().parent
SEEN_FILE  = SCOUT_DIR / "seen_urls.json"
OUTPUT_DIR = Path("/home/sjoe/system/hermes-second-brain/raw/inbox/scout")

SEARCH_TERMS = [
    "MCP server", "model context protocol",
    "AI agent tool", "self-hosted AI",
    "local LLM tool", "Claude tool", "autonomous agent",
]

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc)
    week_str = now.strftime("%Y-W%W")
    week_ago_ts = int((now - timedelta(days=7)).timestamp())
    week_ago_date = (now - timedelta(days=7)).strftime("%Y-%m-%d")

    # Laad seen urls
    seen = json.loads(SEEN_FILE.read_text()) if SEEN_FILE.exists() else {}

    sections = []
    new_count = skip_count = 0

    # Importeer sources
    from sources.hackernews import fetch as hn_fetch
    from sources.reddit import fetch as reddit_fetch
    from sources.github import fetch as github_fetch

    for fetch_fn, label in [
        (lambda: hn_fetch(SEARCH_TERMS, week_ago_ts), "Hacker News"),
        (lambda: reddit_fetch(SEARCH_TERMS), "Reddit"),
        (lambda: github_fetch(SEARCH_TERMS, week_ago_date), "GitHub"),
    ]:
        try:
            items = fetch_fn()
        except Exception as e:
            sections.append(f"## {label}\n*Fout: {e}*\n")
            continue

        new_items = []
        for item in items:
            url = item.get("url", "")
            if url in seen:
                skip_count += 1
                continue
            seen[url] = week_str
            new_items.append(item)
            new_count += 1

        if new_items:
            lines = [f"## {label}"]
            for it in new_items:
                lines.append(f"- [{it['title']}]({it['url']}) — {it.get('meta', '')}")
            sections.append("\n".join(lines))

    # Schrijf output
    out_path = OUTPUT_DIR / f"{week_str}.md"
    header = f"# Scout rapport — week {week_str}\nGegenereerd: {now.strftime('%Y-%m-%d %H:%M UTC')}\n"
    body   = "\n\n".join(sections) if sections else "*Geen nieuwe items gevonden.*"
    footer = f"\n\n---\n*{new_count} nieuwe items — {skip_count} duplicaten overgeslagen*"
    out_path.write_text(header + "\n" + body + footer)
    print(f"Scout klaar: {new_count} nieuw, {skip_count} skip → {out_path}")

    # Bewaar seen (max 500)
    if len(seen) > 500:
        seen = dict(list(seen.items())[-500:])
    SEEN_FILE.write_text(json.dumps(seen, indent=2))

if __name__ == "__main__":
    main()
```

## Cron instelling (na verificatie door Lexi)

```bash
# Elke maandag om 07:00
0 7 * * 1 cd /home/sjoe/system/hermes-second-brain/scout && python3 scout.py >> logs/scout.log 2>&1
```

## Verificatie

```bash
cd /home/sjoe/system/hermes-second-brain/scout
python3 scout.py
cat /home/sjoe/system/hermes-second-brain/raw/inbox/scout/*.md
```

Verwacht: markdown bestand met minimaal 1 sectie, geen Python errors.

## Foutafhandeling

- Elke source in try/except — als één source faalt, gaan de andere door
- Timeouts: gebruik `urllib.request.urlopen(url, timeout=10)`
- Als output map niet bestaat: aanmaken

## Geen externe dependencies

Gebruik alleen Python stdlib: `urllib.request`, `json`, `pathlib`, `datetime`.
Geen `requests`, geen `beautifulsoup`, geen pip install nodig.

## Resultaat schrijven

Schrijf resultaat naar:
`/home/sjoe/system/hermes-second-brain/second-brain/tasks/done/STAP-K-result.md`
