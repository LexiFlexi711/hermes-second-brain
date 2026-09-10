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

## L4-filler: GEFIXT 2026-09-10 — root cause TF-lijst (1440m)

Status: **GEFIXT** (commit `ea0f6f7e`). De timer staat nog steeds UIT tot Lexi
hem expliciet aanzet.

Bewezen root cause (exit code 2):
`tools/fill_l4_snapshot_store.py` `DEFAULT_TFS` had 5 timeframes
(1m/5m/15m/60m/240m) terwijl `L2_collect_mtf` / `L3_snapshot_build` /
`L4_snapshot_store` er **6** eisen incl. `1440m`. L2 rapporteert dan
`1440m: geen input` -> `bundle_usable=False` -> `status=dry_run_failed` -> **exit 2**.

Fix (minimaal): `1440m` toegevoegd aan `DEFAULT_TFS` en `TF_SECONDS_MAP`.
Regressietest `tests/regression/test_l4_filler_tf_contract.py` was eerst RED
(3 failed) en is na de fix GREEN (4 passed).

Bewezen tijdlijn (uit 17 331 run-logs, niet uit aannames):

| periode | uitkomst |
|---|---|
| 2026-07-06 -> 2026-09-03 | ~262 successen/dag, nul failures (15 314 runs) |
| 2026-09-04 | 93 ok / 169 failures — omslagdag |
| 2026-09-05 -> 2026-09-10 | 0 ok / 262 failures per dag, altijd `1440m: geen input` |

Dus **PRE-EXISTING SINDS 2026-09-04**, niet sinds juli.

Correctie op een eerdere claim: in het FASE B-rapport stond "0 successen sinds
juli (1624 failures)". Dat was fout — veroorzaakt door
`grep -c "status=0/SUCCESS"` op systemd-output. Voor een `Type=oneshot` logt
systemd succes als **"Finished l4-filler.service"** (15 685x), niet als
`status=0/SUCCESS`. De filler was dus twee maanden gezond en ging stuk op
2026-09-04.

Bewijs na de fix:
- manual run met exact hetzelfde command: **exit 0**, `status=success`, 2/2 pairs,
  snapshot_id `...1m5m15m60m240m1440m`, output in `runtime/l4_store/{ETHEUR,BTCEUR}/2026-09.sqlite`
- `PRAGMA integrity_check = ok` (859 / 879 snapshots intact)
- systemd service 1x: `Result=success`, `ExecMainStatus=0`, journal "Finished"
- timer: `inactive` + `disabled`

## Geleerde lessen

- Een pad-bonden freeze-check is onverenigbaar met een directorysanering; maak hem
  inhoud-bonden vóór je verhuist, anders is er geen bewijs meer.
- Verhuizing van runtime-data: eerst device bewijzen (zelfde device = atoom-rename),
  dan file count + bytes vóór/na vergelijken. Nooit deleten vóór het doel bewezen is.
- Een gedeelde `tools/`- of `tests/`-map kan geen component-specifieke
  forbidden-import-regel dragen: de backflow-scope moet de component-eigen code zijn.
- Tests die `sys.exit()` op moduleniveau doen, horen niet in pytest-collectie;
  dat hoort expliciet in `conftest.py::collect_ignore`, niet stil.
