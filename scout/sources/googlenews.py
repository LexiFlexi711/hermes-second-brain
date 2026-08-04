"""Google News RSS source — geen auth nodig (RSS feed)."""

from __future__ import annotations

import html
import urllib.parse
import urllib.request
import urllib.error
from typing import Any
from xml.etree import ElementTree


def fetch(terms: list[str]) -> list[dict[str, Any]]:
    """Zoek Google News per term via RSS. Retourneert lijst items, max 4 per term."""
    seen_urls: set[str] = set()
    items: list[dict[str, Any]] = []

    for term in terms:
        query = urllib.parse.quote(term)
        url = (
            f"https://news.google.com/rss/search"
            f"?q={query}&hl=en-US&gl=US&ceid=US:en"
        )
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "hermes-scout/1.0"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                raw = resp.read().decode("utf-8")
                root = ElementTree.fromstring(raw)
        except Exception:
            continue

        count = 0
        for item_elem in root.iter("item"):
            if count >= 4:
                break

            title_tag = item_elem.find("title")
            link_tag = item_elem.find("link")
            source_tag = item_elem.find("source")

            title = html.unescape(title_tag.text) if title_tag is not None and title_tag.text else ""
            link = link_tag.text if link_tag is not None and link_tag.text else ""
            source = source_tag.text if source_tag is not None and source_tag.text else "Google News"

            if not title or not link or link in seen_urls:
                continue

            # Google News links are redirect URLs — strip de display URL
            seen_urls.add(link)
            items.append({
                "title": title,
                "url": link,
                "meta": source,
            })
            count += 1

    return items