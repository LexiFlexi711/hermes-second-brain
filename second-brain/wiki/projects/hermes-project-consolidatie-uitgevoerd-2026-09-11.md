---
title: Hermes-project — consolidatie UITGEVOERD 2026-09-11
type: project
status: afgerond — migratie uitgevoerd en bewezen
tags: [hermes-project, consolidatie, crypto-data, hermes-v03, migratie, runtime, systemd]
created: 2026-09-11
updated: 2026-09-11
---

# Hermes-project — consolidatie UITGEVOERD (2026-09-11)

Vooraf: [[hermes-project-consolidatie-audit-2026-09-11]] (read-only audit, conclusie
JA MAAR MET BLOCKERS) en het migratieplan
`/mnt/otherdrive1/dataLexi/NOA-Reign_migratieplan_hermes-project_20260911.md`.

## Nieuwe canonical root

`projects/hermes-project/` is nu de **enige** Hermes-projectroot.
Commit `9d1d6e18` op branch `refactor/v03-unified-layout-20260910` (geen merge naar main).

## Source → target mapping (uitgevoerd)

| source | target |
|---|---|
| projects/hermes-v03 | projects/hermes-project/hermes-v03 |
| projects/crypto-data | projects/hermes-project/crypto-data |
| projects/crypto-tradebot | projects/hermes-project/crypto-tradebot |
| projects/crypto-test-bot-v3 | projects/hermes-project/crypto-test-bot-v3 |
| validation_charts_v7 | projects/hermes-project/charts/validation_v7 |
| projects/hermes-v01 | projects/hermes-project/archive/hermes-v01 |
| projects/hermes-v01-enkel-research-dont-use | projects/hermes-project/archive/hermes-v01-enkel-research-dont-use |
| projects/crypto-tradebot-backup-2026-05-17 | projects/hermes-project/archive/crypto-tradebot-backup-2026-05-17 |
| scripts/ (root) | projects/hermes-project/scripts/ |
| root-scratch *.py/\*.json/\*.txt | projects/hermes-project/archive/root-scratch/ |

Alle moves waren **atomische renames** (zelfde device 2065) — geen cp/rsync/40G-copy.
`git mv` voor tracked dirs, gewone `mv` voor volledig-untracked dirs.

## validation_charts_v7 — provenance

**IN** (hoort bij het project). Bewijs: generator =
`hermes-v01-enkel-research-dont-use/experiments/validate_v7.py`, dat
`OUT=Path('validation_charts_v7')` en `{pair}_{tf_n}_v7.png` schrijft voor exact
BTCEUR/ETHEUR/SOLEUR/ADAEUR 60m. Target:
`projects/hermes-project/charts/validation_v7/`.

## systemd (nieuwe paden) — `~/.config/systemd/user/`

- `ohlc-bridge.service`: WorkingDirectory + ExecStart →
  `.../projects/hermes-project/crypto-data/...`
- `l4-filler.service`: WorkingDirectory + ExecStart + `--base-dir` →
  `.../projects/hermes-project/hermes-v03/...`
- `l4-filler.timer`: **disabled + inactive** (blijft uit)
- `daemon-reload` uitgevoerd

## cron (nieuwe paden)

- `nightly_ohlc_backfill` (00:00, crypto-data)
- `auto_backtest` (05:30, crypto-tradebot)
- `journal_scanner` (07:00, crypto-tradebot)

Tijdens migratie uitgeschakeld, daarna geheractiveerd met canonical paden.
Andere cronregels onaangeroerd.

## path fixes (bewezen refs)

`L0_data/__init__.py` (CRYPTO_DATA), `L5_chart/__init__.py`,
`run_market_situations_audit.py`, `test_inspect_l4_snapshot.py`,
`run_foundation_release_gate.py` (REPO_ROOT → git-toplevel + FOUNDATION/cwd-paden),
`tests/test_run_foundation_release_gate.py`, `tests/integration/test_outcome_store.py`
(gitignore-diepte), `.claude/settings.json`, `crypto-tradebot/scripts/{audit_trades.py,
recovery_replay_2026_05_27.py,auto_commit.sh}`, `start_noa.sh`, `.gitignore`.

`LOGIC CHANGES = NONE`. Relatieve sibling-refs (bv. `run_outcome_build.sh`
`ARCH=../crypto-data/...`) blijven vanzelf correct.

## Testresultaten

- **hermes-v03 pytest**: 418 passed, 2 skipped, 0 failed.
- **filler regressietest**: 4/4 GREEN.
- **foundation gate**: 11/14 groen — **identiek aan baseline**:
  - A0 frozen: **groen**; phase1a frozen: 2 files (pre-existing D7); backflow: groen
  - rood (alle pre-existing, oorzaak 1440m-verwachting): `tools-audit-integrity` (54p/5f),
    `tools-real-data-e2e` (0/0), `fill-l4-store` (58p/3f — 3× "verwacht 5 TFs, got 6")
  - vóór de commit was A0 frozen rood (artefact: moves zaten in de index, niet in HEAD);
    ná commit groen.
- **NEW REGRESSIONS = 0**, oorzaken onveranderd.

## Runtimebewijs na herstart

- `ohlc-bridge.service`: **active**, nieuwe PID, canonical paden; bridge_status
  geschreven (union 26, ok 156, fail 0, new_candles 402).
- server `:5001`: HTTP 200, cwd `.../hermes-project/hermes-v03`.
- `l4-filler.service` one-shot: `Result=success`, `ExecMainStatus=0`, 2/2 pairs
  (ETHEUR+BTCEUR), 6 TF incl 1440m. Timer blijft disabled.

## Data-integriteit

- crypto-data: live_cache 854 files, ohlc_archive 710, historischedata 22298; 0 lege dirs.
- L4 store: 6 SQLite DB's, `PRAGMA quick_check = ok` voor alle 6; bytes identiek aan vóór de move.

## Werkelijkheids-correcties (t.o.v. eerdere aannames)

- main `b07daaf8` is een **ancestor** van HEAD; HEAD loopt ~30 commits voor. Geen divergentie.
- crypto-test-bot-v3: code dormant sinds 2026-06-18, maar research-output recent.

## Restende uitzonderingen / niet in scope

- **Buiten hermes-project/** (technisch noodzakelijk OS-config of ongerelateerd):
  `~/.config/systemd/user/*.service|*.timer` (+ `.bak_*`), crontab, `NOA-Reign/.git`,
  `second-brain/` (bind mount, aparte repo), `projects/reddit_topic_scanner/`,
  NOA-Reign meta (`agents/ autonomous/ docs/ prompts/ data/ logs/`), `_template/`,
  root `README.md`/`start_noa.*`/`.claude/`, `review{, -artifacts,-inputs}/`.
- Pre-existing verweesd proces: `http.server 8900` (PID 37014/37024, gestart 2026-06-18,
  dir al weg sinds juni) — niet door de migratie.
- Untracked gebleven (correct, niet gecommit): `crypto-data/historischedata/` (40G),
  `archive/root-scratch/`, overige pre-existing untracked.

## Harde eindcriteria

- ACTIVE HERMES PROJECT ROOTS OUTSIDE hermes-project = **0**
- ACTIVE OLD PATH REFERENCES = **0**
- BROKEN REFERENCES = **0**
- NEW REGRESSIONS = **0**
- LOGIC CHANGES = **NONE**

**FINAL VERDICT: HERMES_PROJECT_CONSOLIDATION = GREEN**
