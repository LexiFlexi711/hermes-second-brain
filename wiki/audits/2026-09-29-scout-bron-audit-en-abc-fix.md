---
title: Scout bron-audit + A/B/C fix
type: audit
date: 2026-09-29
status: completed
related: ["scout", "hermes-core", "second-brain-maintenance"]
---

# 2026-09-29 — Scout bron-audit + A/B/C fix

## Scope
De daily scout (`/home/sjoe/system/hermes-second-brain/scout/scout.py`, cron `0 7 * * *`)
over 78 rapporten (2026-05-31 → 2026-09-29). Vraag van Lexi: welke bronnen leveren echt,
welke zijn ruis.

## Bewijsmateriaal
- `~/.hermes/cache/scratch/scout_audit.py` — historiek-parser over 78 rapporten
- `~/.hermes/cache/scratch/scout_probe.py` — live probe per source
- `~/.hermes/cache/scratch/scout_proof.py` — HTTP-fout + dedup-bewijs
- `~/.hermes/cache/scratch/scout_abc_test.py` — test van de A/B/C-fix
- backups: `scout/scout.py.bak-20260929-predateer-ABC`, `scout/seen_urls.json.bak-20260929-predateer-ABC`

## Bevindingen (alle getallen gemeten, niet geschat)

### 1. Reddit is dood — HTTP 403 Blocked
- Live probe: Reddit (Noa/Claude) = 0 items, Reddit-opportunity (Lexi) = 0 items
- Directe call `reddit.com/r/freelance/search.json` → `HTTP Error 403: Blocked`
- Historiek: 138 Lexi-items over 78 rapporten → **0** Reddit-sourced
- Kosten: 8 subreddits × 5 termen = 40 requests/dag + 5 = 45 requests/dag, allemaal 403,
  stil opgeslokt door `except: continue` (reddit_opportunity.py:39-40)

### 2. Dedup faalde op Google News
Google News geeft per dag/per query een **nieuwe redirect-URL** voor hetzelfde artikel.
`seen[url]` matchte dus nooit → listicles kwamen terug.
- Bewijs: 10 titels met >1 verschillende URL
- Lexi: 138 item-instanties, 104 unieke titels → **25% hergebruik**
- Voorbeelden 3x: "n8n vs Relevance AI 2026", "Facebook marketing for small business",
  "Best Cyber Monday/Black Friday deals for freelancers"

### 3. Dedup-geheugen was 500 URL's, niet chronologisch
`seen = dict(list(seen.items())[-500:])` (scout.py:283-284). Gemeten verdeling in het
live bestand: W34 (45), W35 (109), W36 (109), W37 (110), W38 (103), W39 (24) — dus
entries van half augustus bleven staan terwijl recentere eruit vielen.

### 4. Top Picks voegde niets toe
Keyword-filter over de Opportunity-items zelf (scout.py:200-210), niet over andere
profielen. 79 items over 78 rapporten = duplicaat van de Lexi-sectie in hetzelfde bestand.

### 5. Waar de waarde zit (1.273 item-instanties)
| profiel | source | items |
|---|---|---|
| Noa | GitHub 415 + Hacker News 327 | 742 |
| Claude | HN 143 + GitHub 122 | 265 |
| Lexi | Google News 138 (Reddit 0) | 138 |
| TopPicks | duplicaten | 79 |

GitHub + HN = **79%** van alles.

### 6. Hermes Releases werkt wél
55 dagen "geen nieuwe (correct)", 14 dagen nieuwe release gemeld, 9 dagen sectie ontbreekt.

> Correctie op een eerdere claim van Noa in dezelfde sessie: "Hermes Releases is 13 van 15
> dagen leeg" was **fout** — die kwam uit een parserfout in Noa's eigen digest-script.
> De harde cijfers hierboven zijn de juiste.

## Uitgevoerde fix (A/B/C, akkoord Lexi)

**A — Reddit eruit.** Imports + source-entries verwijderd. Noa/Claude 3→2 sources,
Lexi 2→1. 45 → 10 requests/dag. Modulebestanden blijven staan (voor eventuele OAuth).

**B — Dedup op titel.** Nieuwe `_norm_title()`; `seen` matcht op URL én genormaliseerde
titel. Test: dag 1 → 2 nieuw/1 skip; dag 2 met nieuwe URL's → 0 nieuw/2 skip.

**C — Snoei op tijd i.p.v. aantal.** `_week_to_dt()` parseert "2026-W39"; entries ouder
dan 14 dagen gaan eruit, vangnet op 20.000. Echte run: `seen_urls: 506 → 133`.

Bewijs van B in het echt: de Lexi-vondst van 12:02 ("Facebook marketing for small
business") was om 13:07 al gededupliceerd → Lexi 0 nieuwe items, Top Picks leeg.

## Open — bewust uitgesteld
- **E** Google News listicle-filter: wacht op meting, anders niet te bewijzen welke van
  B/C/E de ruis weg deed (één variabele per keer)
- **D** Top Picks schrappen: eerst kijken hoe vaak het nog vuurt
- Reddit definitief: enkel met OAuth-account, anders laten staan
- Restrisico B: repos met andere naam maar zelfde beschrijving (Alpha-Park vs
  alphaparkinc) glippen door titel-dedup — dat is GitHub-ruis, geen dedup-fout

## Vervolg
Meting op **2026-10-06** met hetzelfde audit-script: nieuwe items/dag, hergebruik-%,
per-source bijdrage. Op basis daarvan beslissen over D en E.
