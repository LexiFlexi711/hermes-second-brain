"""GitHub source — Search API (publiek, geen token nodig)."""

from __future__ import annotations

import json
import urllib.request
import urllib.parse
import urllib.error
from typing import Any


def fetch(terms: list[str], week_ago_date: str) -> list[dict[str, Any]]:
    """Zoek GitHub repos per term, max 5 per term, gesorteerd op stars."""
    seen_urls: set[str] = set()
    items: list[dict[str, Any]] = []

    for term in terms:
        encoded_term = urllib.parse.quote(term)
        query = f"{encoded_term}+created:>{week_ago_date}"
        url = (
            f"https://api.github.com/search/repositories"
            f"?q={query}&sort=stars&order=desc&per_page=5"
        )
        try:
            req = urllib.request.Request(url, headers={"Accept": "application/vnd.github.v3+json",
                                                        "User-Agent": "hermes-scout/1.0"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except Exception:
            continue

        for repo in data.get("items", []):
            full_name = repo.get("full_name", "")
            html_url  = repo.get("html_url", "")
            desc      = repo.get("description") or ""
            stars     = repo.get("stargazers_count", 0)

            if not full_name or html_url in seen_urls:
                continue
            seen_urls.add(html_url)
            items.append({
                "title": full_name,
                "url":   html_url,
                "meta":  f"★{stars} — {desc}",
            })

    return items