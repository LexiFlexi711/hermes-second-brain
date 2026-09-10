---
title: Trader-Story A1/A2 — Audit, RFC, Standalone Story Linker V0 + Blind Review
type: project
status: wacht op menselijke review
date: 2026-09-08
tags: [noa-reign, trader-story, story-linker, a1, a2, blind-review, pit-safety, level-identity]
---

# Trader-Story A1/A2 — Audit → RFC → Story Linker V0 → Blind Review

Doel: testen of bestaande PIT-safe Hermes-data twee vooraf vastgelegde trader-verhalen
mechanisch kan herkennen. **Niet** winstoptimalisatie, geen outcome-driven tuning,
geen nieuwe indicatoren, geen nieuwe strategieën.

## Fase 1 — Audit (geen code gewijzigd)

Beide setups: **`ARCHITECTURALLY_NOT_YET_TESTABLE`**

| Setup | Verhaal | Verdict |
|-------|---------|---------|
| A1 | BREAKOUT → RETEST → HOLD | ARCHITECTURALLY_NOT_YET_TESTABLE |
| A2 | HTF TREND → LTF PULLBACK → LEVEL HOLD | ARCHITECTURALLY_NOT_YET_TESTABLE |

Bewezen met code: de v03-pijplijn verwerkt snapshots geïsoleerd of max. curr/prev
(`L5_sequence.diff_snapshots`, `A1_sequence.diff_fields` = 2 snapshots; Market Situation
`temporal_role` = 1 stap terug; Study Runner evalueert elk T onafhankelijk; `a0_snapshot_readout`
leest 1 snapshot). Er is geen event-chain over 3+ momenten en geen level-identiteit over tijd.
N=0 zou hier GEEN trading-resultaat zijn.

## Fase 2 — RFC

**Verplicht eindadvies: A. STANDALONE_STORY_LINKER_SUFFICIENT**

Read-only empirisch onderzoek: 9/10 levels over 24 snapshots (6u) deterministisch volgbaar
via zone-overlap → geen persistent `level_id` nodig, geen nieuwe Hermes-persistentielaag.
Option B (permanente story/event-laag) is overkill/prematuur.

## Fase 3 — Implementatie (alles in `tmp/`, geen frozen component geraakt)

`/mnt/otherdrive1/dataLexi/LexiProjects/tmp/story_linker_v0/`

- `story_linker/{data_source,level_tracker,events,a1_detector,a2_detector}.py`
- `FROZEN/level_match_contract_v0.md` — **LEVEL_MATCH_CONTRACT_V0**:
  `center_tol=0.0002`, `origin_tol=0.0004`, `disappear=4`, `reappear=8`
  → 0 AMBIGUOUS op 15m/60m/240m; 107 stabiele tracks, gem. lengte 27.2;
  no-chain-drift bound 0.04% van origin.
- Tests: level tracker 12/12 + story detectoren 11/11 + golden immutability gate = 24 green.
- Lifecycle: OPEN → CONFIRMED / INVALIDATED / EXPIRED, met event-auditlog.
- A1: BREAKOUT (durable acceptance 2 bars) → MOVE_AWAY (3 bars) → REVISIT → HOLD_OR_REJECTION;
  expiry 12/3 bars.
- A2: HTF (240m) trend → LTF (60m) countertrend pullback → level touch → stall/rejection;
  expiry 3 LTF-bars. HTF/LTF mogen verschillen van richting (geen automatisch conflict).

## Fase 4 — Dry replay (9 weken 07-04 → 09-05, geen outcomes)

- A1: 643 OPEN / 65 CONFIRMED / 132 INVALIDATED / 446 EXPIRED (gem. 2.8 bars)
- A2: 22 OPEN / 14 CONFIRMED / 8 INVALIDATED
- Eerlijke caveat: A1-breakoutdetectie op 60m is ruisgevoelig (~71 stories/week);
  60m reader-levels liggen dicht bij elkaar.

## Fase 5 — FASE 3A Blind Review Pack

- 58 review-items `REV_0001..REV_0058`; SET A=18 (2 random per kalenderweek × 9),
  SET B1=20, SET B2=20; seed `20260908`.
- Harde blinding: geen detector-status, story_id, events, toekomst of outcome in de charts;
  sealed truth manifest; `max_visible_candle_ts <= review_asof` bewezen per paneel.
- Formulier: `blind_review_form.csv` (review_id/human_label/human_confidence/short_reason).

## Fase 6 — Render-correctie (belangrijke les)

Eerste render gebruikte een **eigen matplotlib-renderer** → afgekeurd (hairline-candles;
bovendien in strijd met de regel dat bestaande componenten exact hergebruikt worden).
Fix: **de bestaande Hermes-v03 component `L5_chart.render_chart`** (lightweight-charts HTML),
asof-begrensd via `end=`. Daarna PNG-export via headless chromium.
Dit is de correcte werkwijze: nooit een eigen chart-renderer bouwen als Hermes er al een heeft.

## Fase 7 — Adversarial herbeoordeling REV_0050..0058

- Provenance/alignment audit: `REVIEW_VALID`, alle mappings correct.
- Regime/local-leg/story splitsing (HTF-regime ≠ richting laatste candles; A1 is
  regime-onafhankelijk; A2 vereist directioneel regime).
- STORY CONTRACT V1 opgesteld (HTF_REGIME / LOCAL_LEG / exacte zone-touch / touch≠hold /
  geen fractal-labels als bewijs / A1 / A2 / BOTH / direction / NEITHER vs UNCERTAIN).
- Mechanische consistentie-audit vond concrete uitvoeringsfouten (REV_0003 touch-arithmetiek,
  REV_0009 geen touch, REV_0039 foutieve level-citatie, REV_0057 overgeneralisatie) én één
  systemisch probleem: **`RELEVANT_LEVEL_SHORTCUT_FOUND` / `SYSTEMIC_LEVEL_PROVIDER_BIAS = True`**
  — "relevant level" was stilzwijgend vernauwd tot generated 60m-zones; echte 240m-niveaus
  werden genegeerd. Daarom STOP vóór een rij-per-rij patch; eerst een level-provider audit nodig.

## Artefacten

- `/mnt/otherdrive1/dataLexi/LexiProjects/tmp/trader_story_a1a2_audit.txt`
- `/mnt/otherdrive1/dataLexi/LexiProjects/tmp/trader_story_a1a2_rfc.txt`
- `/mnt/otherdrive1/dataLexi/LexiProjects/tmp/story_linker_v0/`
- `.../story_linker_v0/blind_review_v0/` (charts_v3 HTML + charts_png 116 PNG's, formulier, SEALED/)

## Open / volgende stap

Menselijke blinde labeling van `blind_review_form.csv`, daarna confusion matrix tegen het
sealed truth-manifest. Geen story-implementatie in de live pijplijn.

## Gerelateerd

- [[market-situation-canonical-calendar-v0-predicates-v01]] · [[causal-snapshot-tape-v0]]
  · [[noa-reign-roadmap-v2]] · [[hermes-v03-interpreter]]
