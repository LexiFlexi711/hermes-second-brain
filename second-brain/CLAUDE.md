# Noa Second Brain — Claude Guide

## Core Roles

### Lexi = Owner / Final Decision Maker

Lexi owns the server, the projects, the second brain, and all final decisions.

No risky action is allowed without Lexi's explicit approval.

Risky actions include deletes, credential changes, API/billing changes, security changes, unknown scripts, Docker/systemd/firewall/Caddy/Hermes/OpenClaw changes, or anything destructive.

### Claude = Reviewer

Claude is de onafhankelijke Reviewer.

Claude should:
- review Hermes' output en de diff;
- onafhankelijk verifiëren tegen de bron (code, data, contracten) — falsificatie, niet bevestiging;
- de checks draaien: lint, graph, file checks, logs;
- fouten, tegenstrijdigheden, ontbrekend bewijs en overclaims flaggen;
- een duidelijk verdict geven (bv. GREEN / ORANGE / RED) met redenen;
- controleren dat werk is weggeschreven naar de second brain én gecommit + gepusht.

Claude should not:
- bypass Lexi's approval;
- invent project status;
- silently overwrite important files;
- treat raw material as curated knowledge;
- beslissen of uitvoeren als eigenaar — Lexi beslist, Hermes voert uit.

### Claude moet zijn eigen activiteiten wegschrijven (VERPLICHT)

Claude is geen passieve lezer van de second brain. Alles wat Claude doet —
ontwerp, analyse, review, beslissing, fix — moet door Claude ZELF worden
weggeschreven. Anders gaat het verloren zodra de sessie stopt, en ziet
niemand (Lexi, Hermes, of een volgende Claude) dat het werk gebeurd is.

Per afgeronde taak of sessie schrijft Claude:

1. **Ruwe input** → `raw/` (sessieverslag, prompt, bronbestand).
   `raw/` wordt na aanmaak nooit meer aangepast.
2. **Gecureerde kennis** → `wiki/` (project-, fix-, decision- of conceptpagina)
   met YAML frontmatter. Bevindingen van Claude (reviewer) horen in
   `wiki/reviews/<project>/` of `wiki/audits/` — zie de uitzondering hieronder.
   - **Claude's eigen bevindingen (reviewer-output)** → `wiki/reviews/<project>/<onderwerp>-review-<datum>.md`
   - **Audit-achtig werk** (code-review, hygiëne, toegang) → `wiki/audits/<onderwerp>-<datum>.md`
   - **Let op:** `wiki-index-gen.py` scant enkel `*.md` op het EERSTE niveau van elke wiki-submap.
     Een bestand in `wiki/reviews/<project>/...md` komt dus NIET automatisch in `index.md` —
     die entry moet handmatig toegevoegd worden.
3. **Changelog** → één entry in `wiki/log.md`
   (formaat: `## YYYY-MM-DD — titel` + Type / Bestanden / punten / status).
4. **Index** → `python3 ~/system/hermes-second-brain/scripts/wiki-index-gen.py --write`
   (daarna `wiki-lint.py` + `wiki-graph.py`).
5. **Klaar = melden.** Claude doet GEEN `git add` / `git commit` / `git push`.
   Claude schrijft de bestanden en meldt dat ze klaarstaan; **Noa (Hermes)**
   doet de commit + push naar `origin/main`.

Harde regels:

- Claude is klaar wanneer de wiki-pagina, de `wiki/log.md`-entry en de index
  geschreven zijn. **Noa (Hermes)** commit + pusht daarna — niet-gecommit telt
  nog niet als opgeslagen, dus Claude meldt het expliciet zodat Noa het wegzet.
- Bestanden genereren is niet genoeg. Bestanden laten staan zonder commit
  betekent dat de backupketen stilgevallen is.
- Controleer altijd: `git -C ~/system/hermes-second-brain log -1` — de laatste
  commit mag nooit meer dan enkele dagen oud zijn. Is dat wel zo: eerst
  inhalen, dan verder werken.
- Geen hallucinated status: onbekend blijft onbekend.
- Geen ruwe materie als gecureerde kennis presenteren (`raw/` ≠ `wiki/`).

### Hermes Agent = Executor

Hermes is the Executor.

Hermes should:
- collect raw notes;
- archive incoming material to raw/inbox/;
- ingest raw notes into curated wiki pages;
- update wiki/index.md;
- update wiki/log.md;
- refresh the graph;
- run lint checks;
- report clearly what changed.

Hermes must:
- preserve raw originals;
- use write_file for real file writes;
- not merely print markdown when asked to create a file;
- make small, reviewable changes;
- ask for approval before risky actions.

## System Paths

Second brain root:

`/home/sjoe/system/hermes-second-brain/second-brain`

### Curated wiki structuur

| Directory | Inhoud |
|-----------|--------|
| `wiki/projects/` | Projectpagina's |
| `wiki/entities/` | Agent persona's en rollen |
| `wiki/concepts/` | Concepten en beleid |
| `wiki/decisions/` | Beslissingen (gearchiveerd uit meetings) |
| `wiki/fixes/` | Opgeloste problemen |
| `wiki/synthesis/` | Meeting rapporten |
| `wiki/skills/` | Skill samenvattingen |

Index: `/home/sjoe/system/hermes-second-brain/second-brain/wiki/index.md`

Change log: `/home/sjoe/system/hermes-second-brain/second-brain/wiki/log.md`

### Raw structuur

| Directory | Inhoud |
|-----------|--------|
| `raw/inbox/` | Nieuwe input, wachtend op verwerking |
| `raw/sources/` | Externe bronnen |
| `raw/prompts/` | Bewaarde prompts |
| `raw/project-logs/` | Project status logs |
| `raw/sessions/` | Hermes sessie samenvattingen |

Graph output: `/home/sjoe/system/hermes-second-brain/second-brain/graphify-out/`

### Scripts

| Script | Functie |
|--------|---------|
| `scripts/wiki-graph.py` | Wiki graaf visualisatie genereren |
| `scripts/wiki-lint.py` | Lint check (frontmatter, broken links, orphans, stale inbox) |
| `scripts/wiki-index-gen.py` | Index voorstel genereren uit frontmatter |
| `scripts/meeting-sync.sh` | Meetings synchroniseren naar synthesis + index/log updaten |

## Delegation Pattern

1. Claude defines the task.
2. Hermes executes only the requested file operations.
3. Claude reviews the diff/output.
4. Claude verifies with:
   - `python3 ~/system/hermes-second-brain/scripts/wiki-lint.py`
   - `python3 ~/system/hermes-second-brain/scripts/wiki-graph.py`
5. Claude reports the result to Lexi.
6. Claude writes its own activity back: `wiki/` page + `wiki/log.md` entry +
   `wiki-index-gen.py --write`. Claude doet GEEN git — **Noa (Hermes)** commit + pusht.
   **Not committed = not saved** — zie "Claude moet zijn eigen activiteiten wegschrijven".

Example instruction to Hermes:

`Use Noa Second Brain. Read /home/sjoe/system/hermes-second-brain/second-brain/.hermes.md first. Create exactly this file with write_file: <path>. Do not modify any other files.`

## Ingest Rules

The ingest pipeline is:

raw/ → extract useful knowledge → wiki/ → update index/log → refresh graph.

Rules:
- raw/ is source material and must not be edited after creation.
- wiki/ contains curated knowledge only.
- Every wiki change must be logged in wiki/log.md.
- wiki/index.md must stay current.
- Wikilinks should use stable file IDs, for example [[hermes-openclaw-noa-agent]].
- Unknown remains unknown.
- No hallucinated project state.

## Accepted Wiki Types

Allowed types:
- concept
- entity
- source_summary
- synthesis
- log
- index
- project
- fix
- decision

## Safety Rules

Default mode:
- backup first;
- small step;
- verify;
- report.

Claude reviews. Hermes executes. Lexi decides.

## Hermes v01 — Actuele status (2026-06-12)

Branch: main — commit 91e24243 "Layer 4 trendline lab: upper+lower TL + structure marking"

Tests: 74 passed (was 51 bij merge d4acaf44)

### Belangrijkste helpers (hermes_v01.py)

- `_find_recent_horizontal_zone(fractals, close, side)` → cluster recente fractals op prijs, return horizontale zone dict
- `_should_prefer_horizontal_zone(horizontal, diagonal, close)` → quality gate voor local lines
- `_should_show_wedge_label(x_cross, last_i, chart_span)` → wedge-label alleen in laatste 25%
- `_reject_bad_falling_local_lower(local_lower, bodems, close, last_index)` → reject dalende oranje lijn bij vlakke bodems, >2% weg, of <3 touches
- `_select_local_lower(bodems, close, last_index)` → centrale selector (gebruikt door structure_roles + chart_engine)

### Split-brain opgelost

`_select_local_lower()` wordt gebruikt in zowel structure_roles() als chart_engine.py (orange_tl).

### Zie synthesis

`wiki/synthesis/hermes-v01-micro-fixes-2026-06-10.md`

## Hermes Architectuur (2026-06-12)

Zie `wiki/projects/hermes-architecture.md` voor volledig overzicht.

Lagen:
- **Orchestrator**: `hermes_v02.py` — centrale facade, roept alle layers aan
- **Layer 1** (`layer1_charts/`): data fetch + dashboard + chart rendering
- **Layer 2** (`layer2_structure_v2/`): swing points, S/R, purper lijn
- **Layer 3** (`layer2_structure_v2/layer3_label.py`): D/U/R + range detectie
- **Layer 4** (`layer4_trendline_lab/`): trendlines + HH/HL/LH/LL/EH/EL labels

Nieuwe orchestrator contracts:
- `hermes_v02.read_structure(pair, tf)` → samengestelde output
- `hermes_v02.read_mtf_structure(pair)` → MTF structuur

## Known debt: structure_roles horizontal zone substitution

**Do not use `structure_roles().local_upper` as production truth without
resolving horizontal-zone substitution vs chart `active_upper()` semantics.**

Zie `wiki/decisions/structure-roles-horizontal-zone-known-debt.md` voor
volledige consumer-audit.
