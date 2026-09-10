---
title: Hermes V03 — directorysanering 2026-09-10
type: project
status: afgerond (FASE A-D)
tags: [hermes-v03, refactor, directory, freeze-gate, governance]
updated: 2026-09-10
---

# Hermes V03 — directorysanering (2026-09-10)

Doel: van vijf losse V03-projectroots terug naar **één canonical softwareproject**
zonder aan logica, strategie, entry/exit of optimalisatie te komen. Alleen structuur.

## Eindresultaat

`projects/hermes-v03/` is de **enige** actieve V03-root. Deze bestaan niet meer:

- `hermes-v03-analyst` → `src/hermes_v03/analyst/`
- `hermes-v03-interpreter` → `src/hermes_v03/interpreter/`
- `hermes-v03-outcome` → `src/hermes_v03/outcome/`
- `hermes-v03-strategy-harness` → `src/hermes_v03/strategy/`

Verder: tests centraal in `tests/{unit,integration,regression,fixtures}`,
tools in `tools/`, shells in `scripts/`, docs in `docs/`,
runtime-state in `runtime/{l4_store,logs,tmp}` (niet in git),
bewaard materiaal in `archive/`, gegenereerde output in `artifacts/`.
`README.md` bevat de kaart; `pyproject.toml` zet `pythonpath=src`.

## Werkwijze (branches)

- checkpoint: `safety/v03-pre-layout-20260910` @ `8755c810` (46 files, niets inhoudelijks)
- sanering: `refactor/v03-unified-layout-20260910`
- commits: `8984b9c5` (A) · `711e20df` + `f3c85a7d` (A-fix) · `8b06d354` (gate D5+D6) ·
  `9e211f19` + `f52a46df` (B) · `3cbc9d4d` (C) · `7b6439aa` (D) · `838ecba6` (README/root-tidy)
- alle moves via `git mv`; frozen worktrees buiten deze working tree onaangeroerd;
  geen force push, geen history rewrite.

## De gate moest mee: freeze-invariant is INHOUD, niet pad

`scripts/run_foundation_release_gate.py` controleerde de A0/Phase-1A freeze via
`git diff --name-only <frozen_sha> HEAD -- <oude paden>`. Een pure move maakt die
diff niet-lege → gate rood, en dat is met padwerk niet op te lossen (de nieuwe paden
bestaan niet in het freeze-commit).

Op beslissing van Lexi (**D5, optie a**) is de check omgezet naar
**blob@frozen(oud pad) vs blob@HEAD(canonicaal pad)**:

- pure move met identieke inhoud = GREEN
- één byte verschil = RED
- ontbrekend bestand, ontbrekende mapping of ontbrekende verplichte dir = RED (fail closed)
- `expected != checked` = RED (geen stille overslag)

Frozen reference commits en bestandslijsten bleven letterlijk ongewijzigd; er zijn
11 regressietests bijgekomen. **D6**: alle actieve paden (suite-entries, cwd's,
backflow-dirs, index-import) komen nu uit één expliciete `FOUNDATION`-mapping, en de
backflow-audit is fail-closed met dekking-rapportage per component (0 gescande
`.py` = hard fail).

Bewezen op echte data: A0 = `checked=7/7, mismatched=[]` na een volledige verhuizing.

## Wat NIET is aangepast (bewust)

- **Phase-1A frozen deviation** (`outcome_builder/cli.py` + `contracts.py`): wijkt
  inhoudelijk af sinds 2026-09-03 (commits `e62875f6`, `af1715a7`; freeze-commit was
  2026-07-11). Pre-existing. **D7 = optie (c)**: niet re-baselinen, niet terugzetten,
  niet verbergen — geregistreerd als PRE-EXISTING KNOWN DEVIATION.
- **1440m-testprobleem** in `interpreter-tools-audit-integrity` (5 failures),
  `tools-real-data-e2e`, `fill-l4-store`: pre-existing, oorzaak niet gewijzigd.
- **L4-filler**: zie hieronder.

## Saneringsgate: baseline en resultaat

Baseline-record: `projects/hermes-v03/docs/sanering_baseline_20260910.{md,json}`.

| | baseline (vóór B) | na A-D |
|---|---|---|
| suites groen | 11 / 14 | **11 / 14** |
| suites rood | 3 (audit-integrity 54p/5f, real-data-e2e, fill-l4-store) | **identiek** |
| REAL-DATA | NOT EXECUTED | NOT EXECUTED |
| FROZEN A0 | ✅ | ✅ |
| FROZEN phase1a | ❌ 2 files (D7) | ❌ 2 files (D7) |
| BACKFLOW | 0 violations | 0 violations |
| tests | — | 416 passed (interpreter + analyst + outcome + harness) |

**0 nieuwe failures, oorzaken ongewijzigd, LOGIC CHANGES = NONE.**

## L4-filler: PRE-EXISTING BROKEN (belangrijk)

De filler was al stuk **vóór** de sanering: `status=2/INVALIDARGUMENT` bij elke run,
**1624 falende runs en 0 successen** in 30 dagen; eerste falende run in het journal
`Jul 06 12:45:03` (~66 dagen). Args zijn allemaal geldig, dus exit 2 komt uit een
guard in de tool zelf.

Daarom (D8, optie a): runtime verhuisd, systemd-unit naar canonical paden,
`daemon-reload` — maar **timer blijft UIT** en de unit draagt de status
`PRE-EXISTING BROKEN — DISABLED PENDING SEPARATE REPAIR`.
De fout zelf is **niet** gerepareerd (buiten scope); daarvoor komt een aparte
opdracht **INCIDENT: L4-FILLER EXIT 2**.

## Geleerde lessen

- Een pad-bonden freeze-check is onverenigbaar met een directorysanering; maak hem
  inhoud-bonden vóór je verhuist, anders is er geen bewijs meer.
- Verhuizing van runtime-data: eerst device bewijzen (zelfde device = atoom-rename),
  dan file count + bytes vóór/na vergelijken. Nooit deleten vóór het doel bewezen is.
- Een gedeelde `tools/`- of `tests/`-map kan geen component-specifieke
  forbidden-import-regel dragen: de backflow-scope moet de component-eigen code zijn.
- Tests die `sys.exit()` op moduleniveau doen, horen niet in pytest-collectie;
  dat hoort expliciet in `conftest.py::collect_ignore`, niet stil.
