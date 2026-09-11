---
title: Hermes-project — consolidatie-audit 2026-09-11
type: audit
status: afgerond (read-only audit — migratie NIET uitgevoerd)
tags: [hermes-project, consolidatie, crypto-data, hermes-v03, audit, runtime, systemd]
created: 2026-09-11
updated: 2026-09-11
---

# Hermes-project — consolidatie-audit (2026-09-11)

## Doel

Bewijzen wat er exact onder één canonical root
`projects/hermes-project/` zou moeten komen, wanneer alle onderdelen van het
Hermes-botproject samengebracht worden.

Modus: **read-only**. Geen moves, geen renames, geen systemd/cron-wijzigingen,
geen codewijzigingen. Alleen inventaris + afhankelijkheden + feiten.

Primaire bron: `/mnt/otherdrive1/dataLexi/NOA-Reign_audit_consolidatie_20260911.md`
Methode: echte bestanden, git, systemd/cron, live processen, `find`/`grep`.
Onbekend = UNKNOWN. Geen aannames.

Scope: `/mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/`

## Conclusie vooraf

**JA MAAR MET BLOCKERS** — consolidatie onder `projects/hermes-project/` is
technisch mogelijk, maar meerdere harde blockers vereisen codewijziging
(hardcoded paden, systemd units, cron, ~90 worktrees, draaiende server,
bind mount, .gitignore).

Migratie: **NIET uitgevoerd.** Dit is alleen de audit.

---

## A. Kerfeit — `crypto-data` HOORT bij het Hermes-project

Lexi's uitgangspunt (crypto-data valt binnen het project) is **bewezen door de
code**, niet weerlegd. Er is geen enkel bewijs dat `crypto-data` een
onafhankelijk product is dat buiten Hermes zou horen.

Bewijs:

- `hermes-v03/L0_data/__init__.py` regel 16:
  `CRYPTO_DATA = ".../projects/crypto-data"` — HARDCODED absoluut pad.
  Leest uit `crypto-data/{logs/live_cache, logs/ohlc_archive, historischedata}`.
- `hermes-v03/src/hermes_v03/outcome/outcome_builder/`
  (`archive_reader.py`, `ohlc_cache.py`, `cli.py`) leest
  `crypto-data/logs/{live_cache,ohlc_archive}`.
- `hermes-v03/scripts/run_outcome_build.sh` → `ARCH="../crypto-data/logs/ohlc_archive"`.
- `ohlc-bridge.service` (ACTIEF) draait `crypto-data/scripts/universe_ohlc_bridge.py`
  met `WorkingDirectory=.../projects/crypto-data`.

## B. Actief vandaag (bewezen)

- `hermes-v03 server.py` draait op **:5001** (PID 1630346, uptime ~74 dagen).
- `ohlc-bridge.service` — ENABLED / ACTIVE (PID 2704351), Restart=always.
- cron `nightly_ohlc_backfill.py` (crypto-data, 00:00) — geschreven 2026-09-11.
- cron `auto_backtest.py` (crypto-tradebot, 05:30) — resultaten 2026-09-11.
- cron `journal_scanner.py` (crypto-tradebot, 07:00).
- L4-filler code bewezen groen (4/4 regressietests), service static;
  **timer DISABLED** (bewust — incident 2026-09-04 gefixt, zie
  [[hermes-v03-directorysanering-2026-09-10]]).

## C. Niet actief

- **Geen live traders** — geen screens actief (`screen -ls` = leeg),
  geen trader-processen.
- `crypto-test-bot-v3` code **DORMANT** (git last commit `6cd4bb0a`, 2026-06-18).
- **MAAR**: research-output daar werd nog geschreven op **2026-09-10**
  (`logs/research/walk_forward_*`). Nuance: code slaapt, output niet.

## D. Harde verplaatsingsblockers

Verplaatsen naar `projects/hermes-project/` vereist codewijziging:

1. **Hardcoded paden** — `hermes-v03/L0_data/__init__.py` r16 (CRYPTO_DATA
   absoluut) + `scripts/run_outcome_build.sh` (`ARCH=../crypto-data/...`).
2. **systemd unit paths** — `ohlc-bridge.service` + `l4-filler.service`
   (ExecStart + WorkingDirectory, absolute paden).
3. **crontab absolute paths** — `cd` naar `projects/crypto-data` en
   `projects/crypto-tradebot`.
4. **~90 git worktrees** — verplaatsen breekt elke worktree-referentie.
5. **Draaiende server :5001** — herstart nodig bij verplaatsing.
6. **Second-brain bind mount** — zie E.
7. **.gitignore / runtime-path assumptions** — regels verwijzen naar
   `projects/crypto-data/...` en `projects/hermes-v03/runtime/`.

## E. Second Brain is een bind mount (geen kopie)

- `/mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign/second-brain`
  is een **bind mount** van
  `/home/sjoe/system/hermes-second-brain/second-brain` (zelfde inode 809287,
  `findmnt` bevestigt: bind van ubuntu-lv, ext4).
- Het is dus **geen gewone kopie** en **niet** git-tracked in de NOA-Reign repo
  (`git ls-files second-brain` = 0).
- Tweede git repo: `github.com/LexiFlexi711/hermes-second-brain`.

## F. Root-rommel

Losse scripts in de NOA-Reign root (`check_market_data.py`,
`forensic_analysis.py`, `inspect_*.py`, `run01_evaluation.py`, `swing_count.py`,
`tmp_archive_count.py`, `run01_batch_def.json`, …):

- **ALLES UNTRACKED** (`git status` = `??`).
- **NUL git-referenties** (`git grep` = leeg).
- Historisch/tijdelijk analysegereedschap (run01 / forensic / inspect).
- Volgens de audit **veilig archiveerbaar**; hoort niet in runtime.

## G. Werkelijkheid vs eerdere aannames (correcties)

- **main vs HEAD**: `main` (`b07daaf8`) IS een **ancestor** van de huidige HEAD
  (`8b1c9c24`); HEAD loopt **~30 commits vóór** main. **Geen divergentie** —
  main heeft niets dat HEAD niet heeft. (Eerdere premisse "main loopt 19
  inhoudelijke commits achter" is onjuist geframed.)
- **crypto-test-bot-v3**: code dormant sinds 2026-06-18, maar research-output
  recent (2026-09-10). "Dormant" geldt voor de code, niet voor de output.

---

## Huidige verspreiding van het actieve Hermes-project

CODE

- `projects/hermes-v03/` + `src/hermes_v03/{interpreter,analyst,outcome,strategy}`
- `scripts/run_foundation_release_gate.py` (root — V03-gate, gebruikt door
  `hermes-v03/README.md` + `tests/conftest.py`; staat BUITEN de V03-root)
- `.claude/settings.json` (refs crypto-data)

DATA (leverancier)

- `projects/crypto-data/logs/live_cache/`
- `projects/crypto-data/logs/ohlc_archive/`
- `projects/crypto-data/historischedata/` (40G totaal crypto-data)

RUNTIME

- `projects/hermes-v03/runtime/l4_store/` (2.6G)
- `projects/hermes-v03/runtime/logs/`, `runtime/tmp/`, `run/l4_filler_once.lock`

SERVICES / CRON

- `~/.config/systemd/user/ohlc-bridge.service` (enabled/active)
- `~/.config/systemd/user/l4-filler.service` (static, timer disabled)
- crontab: crypto-data backfill, crypto-tradebot backtest + journal

SECOND BRAIN

- bind mount → `/home/sjoe/system/hermes-second-brain/second-brain` (aparte repo)

GIT

- branch `refactor/v03-unified-layout-20260910`
- main `b07daaf8` (ancestor) · HEAD `8b1c9c24` (~30 commits voor)
- remote `github.com/LexiFlexi711/NOA-reign.git`
- ~90 worktrees (grotendeels prunable / frozen in `NOA-Reign-worktrees/` + `/tmp/`)

## Legacy / historisch

- `projects/crypto-test-bot-v3/` (2.7G) — research-lab, code dormant.
- `projects/crypto-tradebot/` (5.7G) — geen live trading; 2 cronjobs actief.
- `projects/crypto-tradebot-backup-2026-05-17/` (75M) — pure backup.
- `projects/hermes-v01/` — leeg skelet (6 files).
- `projects/hermes-v01-enkel-research-dont-use/` (88M) — historische research.

## Ongerelateerd aan het botproject

- `reddit_topic_scanner/` (eigen cronjob), `agents/`, `autonomous/`, `docs/`,
  `prompts/`, `data/`, `logs/`, `_template/`, `review*`.
- `validation_charts_v7/` — UNKNOWN (4 PNG, geen refs).

## UNKNOWN

- `validation_charts_v7/` — herkomst/gebruik onbekend.
- `crypto-tradebot-backup-2026-05-17/` — bewaren of weg? geen refs.
- `review-inputs/`, `review-artifacts/` — afgeronde reviews, geen runtime-refs.
- `scripts/intake-hook.py`, `render_l88_test.py` — laatste refs 2026-06-20.

## Volgende stap

Migratie **NIET** gestart. Wacht op nieuwe expliciete opdracht van Lexi.
Zie ook scope-correctie op [[hermes-v03-directorysanering-2026-09-10]].

> **UPDATE 2026-09-11:** de migratie is inmiddels **UITGEVOERD** — zie
> [[hermes-project-consolidatie-uitgevoerd-2026-09-11]] (commit `9d1d6e18`).
