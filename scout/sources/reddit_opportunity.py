"""Reddit Opportunity source — inkomensgerichte subreddits, geen auth nodig."""

from __future__ import annotations

import json
import urllib.request
import urllib.parse
import urllib.error
from typing import Any

SUBREDDITS = [
    "freelance",
    "Entrepreneur",
    "forhire",
    "smallbusiness",
    "WorkOnline",
    "beermoney",
    "sidehustle",
    "digitalnomad",
]


def fetch(terms: list[str]) -> list[dict[str, Any]]:
    """Zoek Opportunity subreddits per term, max 5 per subreddit per term."""
    seen_urls: set[str] = set()
    items: list[dict[str, Any]] = []

    for subreddit in SUBREDDITS:
        for term in terms:
            query = urllib.parse.quote(term)
            url = (
                f"https://www.reddit.com/r/{subreddit}/search.json"
                f"?q={query}&sort=top&t=week&limit=5"
            )
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "hermes-scout/1.0"})
                with urllib.request.urlopen(req, timeout=5) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
            except Exception:
                continue

            for child in data.get("data", {}).get("children", []):
                hit = child.get("data", {})
                title = hit.get("title", "")
                permalink = hit.get("permalink", "")
                url_full = f"https://reddit.com{permalink}"
                score = hit.get("score", 0)

                if not title or url_full in seen_urls:
                    continue
                seen_urls.add(url_full)
                items.append({
                    "title": title,
                    "url": url_full,
                    "meta": f"{score} upvotes ({subreddit})",
                })

    return items