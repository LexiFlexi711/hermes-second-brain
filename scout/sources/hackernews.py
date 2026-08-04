"""Hacker News source — Algolia API (geen auth nodig)."""

from __future__ import annotations

import json
import urllib.parse
import urllib.request
import urllib.error
from typing import Any


def fetch(terms: list[str], week_ago_ts: int) -> list[dict[str, Any]]:
    """Zoek HN stories per term, max 5 per term. Retourneert lijst items."""
    seen_urls: set[str] = set()
    items: list[dict[str, Any]] = []

    for term in terms:
        query = urllib.parse.quote(term)
        url = (
            f"https://hn.algolia.com/api/v1/search"
            f"?query={query}&tags=story"
            f"&numericFilters=created_at_i>{week_ago_ts}"
            f"&hitsPerPage=5"
        )
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "hermes-scout/1.0"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except Exception:
            continue

        for hit in data.get("hits", []):
            title = hit.get("title", "")
            url   = hit.get("url") or f"https://news.ycombinator.com/item?id={hit.get('objectID', '')}"
            points = hit.get("points", 0)

            if not title or url in seen_urls:
                continue
            seen_urls.add(url)
            items.append({
                "title": title,
                "url":   url,
                "meta":  f"{points} pts",
            })

    return items