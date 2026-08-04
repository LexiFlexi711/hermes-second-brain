"""Hermes Agent release monitor — GitHub Releases API (geen auth nodig)."""

from __future__ import annotations

import json
import urllib.request
from pathlib import Path
from typing import Any

RELEASES_URL = "https://api.github.com/repos/nousresearch/hermes-agent/releases/latest"
VERSION_FILE = Path(__file__).resolve().parent.parent / "hermes_version.json"


def check() -> dict[str, Any]:
    """Check of er een nieuwe Hermes release is. Retourneert dict met status."""
    result: dict[str, Any] = {
        "new_release": False,
        "current_version": None,
        "latest_version": None,
        "alert": "",
        "url": "",
        "body_snippet": "",
        "error": None,
    }

    # Lees opgeslagen versie
    stored: dict[str, str] = {}
    if VERSION_FILE.exists():
        try:
            stored = json.loads(VERSION_FILE.read_text())
        except Exception:
            pass
    result["current_version"] = stored.get("last_version")

    # Haal latest release op van GitHub
    try:
        req = urllib.request.Request(
            RELEASES_URL,
            headers={"Accept": "application/vnd.github.v3+json", "User-Agent": "hermes-scout/1.0"},
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        result["error"] = str(e)[:200]
        result["alert"] = f"⚠️ Kon Hermes releases niet checken: {e}"
        return result

    tag = data.get("tag_name", "")
    html_url = data.get("html_url", "")
    body = data.get("body", "") or ""
    published = data.get("published_at", "") or ""

    result["latest_version"] = tag
    result["url"] = html_url
    result["body_snippet"] = body[:300]

    # Vergelijk met opgeslagen versie
    if tag and tag != stored.get("last_version"):
        result["new_release"] = True
        result["alert"] = (
            f"🚨 **NIEUWE HERMES RELEASE: {tag}** — {published[:10]}\n"
            f"- [Release notes]({html_url})\n"
            f"- Eerste 300 chars: {body[:300]}...\n"
            f"- ⚠️ Upgrade: `hermes update`"
        )
    elif tag:
        result["alert"] = (
            f"✅ Geen nieuwe release. Huidig: {tag} ({published[:10]}). "
            f"[Release notes]({html_url})"
        )
    else:
        result["alert"] = "⚠️ Kon versie niet bepalen uit GitHub API."

    # Update state file
    try:
        VERSION_FILE.write_text(json.dumps({
            "last_version": tag,
            "last_checked": published[:10] if published else "",
            "release_url": html_url,
        }, indent=2))
    except Exception:
        pass

    return result
