#!/usr/bin/env python3
"""Weekly scout — autonome scanner voor tools, skills én inkomstenkansen.

Drie profielen:
  - Noa (Hermes): MCP servers, Hermes skills, AI agent tools
  - Claude: Claude Code updates, Anthropic releases, Claude MCP tools
  - Lexi (💰 Opportunity): freelance, AI consulting, webdesign, crypto income

Gebruik:
    python3 scout.py

Cron:
    0 7 * * * cd /home/sjoe/system/hermes-second-brain/scout && python3 scout.py >> logs/scout.log 2>&1

Optioneel: tag met `--force` om seen_urls te wissen en alles opnieuw te scannen.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

# Configuratie
SCOUT_DIR  = Path(__file__).resolve().parent
SEEN_FILE  = SCOUT_DIR / "seen_urls.json"
OUTPUT_DIR = Path("/home/sjoe/system/hermes-second-brain/raw/inbox/scout")
LOG_DIR    = SCOUT_DIR / "logs"

# ── Zoektermen per profiel ─────────────────────────────────────────────────

NOA_TERMS = [
    "MCP server",
    "AI agent tool",
    "Hermes Agent",
    "n8n workflow automation",
    "n8n MCP server",
    "Model Context Protocol tool",
]

CLAUDE_TERMS = [
    "Claude Code update",
    "Claude MCP tool",
]

OPPORTUNITY_TERMS = [
    "AI automation freelance",
    "n8n freelancer",
    "remote side income 2026",
    "crypto trading bot profit",
    "digital marketing kleine onderneming",
]

# Globale timeout per source call (seconden)
SOURCE_TIMEOUT = 8

# Sources pad
sys.path.insert(0, str(SCOUT_DIR))
from sources.hackernews import fetch as hn_fetch
from sources.reddit import fetch as reddit_fetch
from sources.github import fetch as github_fetch
from sources.reddit_opportunity import fetch as reddit_opp_fetch
from sources.googlenews import fetch as googlenews_fetch


# ── Crypto-filter (alleen voor Opportunity/Lexi profiel) ─────────────────

CRYPTO_BLACKLIST = [
    "tradebot", "trader", "backtest", "OHLC", "candle pattern",
    "pair trading", "BTCEUR", "ETHEUR", "grid search", "pullback",
    "scalping", "day trading", "swing trading", "technical analysis",
    "trading bot", "tradingview", "chart pattern", "price action",
    "support resistance", "breakout strategy", "crypto trading",
]


def is_crypto_noise(title: str, description: str = "") -> bool:
    """Check of een item crypto/tradebot ruis is — context-aware voor 'token'."""
    text = f"{title} {description}".lower()

    for term in CRYPTO_BLACKLIST:
        if term.lower() in text:
            return True

    # Context-aware "token": alleen uitsluiten in crypto/NFT context
    if "token" in text:
        safe_contexts = [
            "api token", "auth token", "security token",
            "access token", "token authentication", "bearer token",
        ]
        for ctx in safe_contexts:
            if ctx in text:
                return False  # Token in veilige context → NIET filteren
        # Token in onbekende context → wél filteren (voorzichtig)
        return True

    return False


from sources.hermes_releases import check as hermes_check


def run_profile(label: str, emoji: str, terms: list[str], sources: list[tuple[str, callable]], seen: dict, week_str: str, filter_fn=None) -> tuple[int, int, int, list[str]]:
    """Run een profiel door alle sources. Retourneert (new, skip, filtered, sections)."""
    new_total = skip_total = filtered = 0
    sections: list[str] = []

    for src_label, fetch_fn in sources:
        try:
            items = fetch_fn(terms)
        except Exception as e:
            sections.append(f"### {src_label}\n*Fout: {e}*\n")
            continue

        new_items: list[dict] = []
        for item in items:
            url = item.get("url", "")
            if url in seen:
                skip_total += 1
                continue
            if filter_fn and filter_fn(item.get("title", ""), item.get("meta", "")):
                filtered += 1
                continue
            seen[url] = week_str
            new_items.append(item)
            new_total += 1

        if new_items:
            lines = [f"### {src_label}"]
            for it in new_items:
                lines.append(f"- [{it['title']}]({it['url']}) — {it.get('meta', '')}")
            sections.append("\n".join(lines))

    return new_total, skip_total, filtered, sections


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    now = datetime.now(timezone.utc)
    date_str = now.strftime("%Y-%m-%d")
    week_str = now.strftime("%Y-W%W")
    week_ago_ts   = int((now - timedelta(days=7)).timestamp())
    week_ago_date = (now - timedelta(days=7)).strftime("%Y-%m-%d")

    # Laad seen urls
    seen = json.loads(SEEN_FILE.read_text()) if SEEN_FILE.exists() else {}

    # Sources (zelfde voor Noa & Claude — tech focus)
    sources = [
        ("Hacker News", lambda terms: hn_fetch(terms, week_ago_ts)),
        ("Reddit",      lambda terms: reddit_fetch(terms)),
        ("GitHub",      lambda terms: github_fetch(terms, week_ago_date)),
    ]

    # Opportunity profiel gebruikt eigen sources
    opportunity_sources = [
        ("Reddit — Freelance/Entrepreneur", lambda terms: reddit_opp_fetch(terms)),
        ("Google News", lambda terms: googlenews_fetch(terms)),
    ]

    # Profielen uitvoeren
    noa_new, noa_skip, _, noa_sections = run_profile(
        "Noa", "🔵", NOA_TERMS, sources, seen, week_str
    )
    claude_new, claude_skip, _, claude_sections = run_profile(
        "Claude", "🟣", CLAUDE_TERMS, sources, seen, week_str
    )
    lexi_new, lexi_skip, crypto_filtered, lexi_sections = run_profile(
        "Lexi", "💰", OPPORTUNITY_TERMS, opportunity_sources, seen, week_str,
        filter_fn=is_crypto_noise  # ← Alleen op Lexi profiel
    )

    total_new = noa_new + claude_new + lexi_new
    total_skip = noa_skip + claude_skip + lexi_skip

    # Bouw rapport
    header = (
        f"# Scout rapport — {date_str}\n"
        f"Gegenereerd: {now.strftime('%Y-%m-%d %H:%M UTC')}\n"
        f"*Week {week_str} — dagelijkse scan*\n"
    )

    body_parts: list[str] = []

    # 🚨 Hermes Releases — check voor nieuwe versie
    hermes = hermes_check()
    body_parts.append(f"## 🚨 Hermes Releases\n{hermes['alert']}")

    # 🔥 Top Picks — enkel uit het Opportunity profiel
    # Items met keywords die wijzen op concrete actie of inzicht
    top_keywords = [
        "make money", "income", "freelancer", "hustle", "profitable",
        "verdienste", "business idea", "how to", "tutorial", "guide",
        "review", "compare", "vs ", "best ", "top ",
    ]

    top_picks: list[str] = []
    for section in lexi_sections:
        lines = section.split("\n")
        for line in lines:
            if line.startswith("- [") and any(kw in line.lower() for kw in top_keywords):
                top_picks.append(line)

    if top_picks:
        body_parts.append(
            "## 🔥 Top Picks\n" + "\n".join(top_picks[:5])
        )

    if noa_sections:
        body_parts.append(
            "## 🔵 Noa (Tech)\n" + "\n\n".join(noa_sections)
        )
    if claude_sections:
        body_parts.append(
            "## 🟣 Claude (Tech)\n" + "\n\n".join(claude_sections)
        )
    if lexi_sections:
        body_parts.append(
            "## 💰 Opportunity (Inkomsten)\n" + "\n\n".join(lexi_sections)
        )

    if not body_parts:
        body_parts.append("*Geen nieuwe items vandaag — alles al gezien.*")

    footer = (
        f"\n\n---\n"
        f"*Totaal: {total_new} nieuwe items — {total_skip} duplicaten"
        f"{' — ' + str(crypto_filtered) + ' crypto uitgesloten' if crypto_filtered else ''}*\n"
        f"*🔵 Noa: {noa_new} — 🟣 Claude: {claude_new} — 💰 Lexi: {lexi_new}*"
    )

    out_path = OUTPUT_DIR / f"{date_str}.md"
    out_path.write_text(header + "\n" + "\n\n".join(body_parts) + footer)

    # ── Opslaan naar second brain raw/inbox ────────────────────────────────
    # Altijd schrijven — ook bij 0 nieuwe items zodat er nooit een dag mist
    try:
        sb_inbox = Path("/home/sjoe/system/hermes-second-brain/raw/inbox")
        sb_inbox.mkdir(parents=True, exist_ok=True)

        opp_note = [
            f"---",
            f"type: scout",
            f"date: {date_str}",
            f"source: weekly-scout (opportunity profile)",
            f"items: {lexi_new}",
            f"---",
            f"",
            f"# Opportunity Scout — {date_str}",
            f"",
        ]
        if top_picks:
            opp_note.append("## 🔥 Top Picks")
            for pick in top_picks[:5]:
                opp_note.append(pick)
            opp_note.append("")
        if lexi_sections:
            opp_note.append("## Alle vondsten")
            opp_note.append("\n\n".join(lexi_sections))
        else:
            opp_note.append("*Geen nieuwe opportunity items vandaag.*")

        opp_path = sb_inbox / f"opportunity-{date_str}.md"
        opp_path.write_text("\n".join(opp_note))
        print(f"  → Second brain: {opp_path}")
    except Exception as e:
        print(f"  !! Fout bij schrijven opportunity file: {e}")

    msg = (
        f"Scout klaar: {total_new} nieuw ({noa_new} Noa / {claude_new} Claude / {lexi_new} Lexi), "
        f"{total_skip} skip → {out_path}"
    )
    print(msg)

    # Log naar bestand (append — niet overschrijven)
    with open(LOG_DIR / "scout.log", "a") as lf:
        lf.write(f"[{now.strftime('%Y-%m-%d %H:%M')}] {msg}\n")

    # Bewaar seen (max 500)
    if len(seen) > 500:
        seen = dict(list(seen.items())[-500:])
    SEEN_FILE.write_text(json.dumps(seen, indent=2))


if __name__ == "__main__":
    main()