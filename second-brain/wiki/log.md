
# Wiki Log

## 2026-09-10 — CLAUDE.md: Claude = Reviewer + verplichte write-back (zonder git)
- **Type:** governance + fix
- **Bestanden:** `CLAUDE.md`, [[2026-09-10-second-brain-commit-gap]]
- "Claude Code" → "Claude" (11×), titel nu "Noa Second Brain — Claude Guide".
- **Rol gewijzigd: `Claude = Director` → `Claude = Reviewer`** — onafhankelijke reviewer,
  falsificatie i.p.v. bevestiging, verdict GREEN/ORANGE/RED met redenen, controleert of werk
  is weggeschreven; beslist/voert niet uit als eigenaar. Slotzin nu "Claude reviews.
  Hermes executes. Lexi decides."
- Nieuwe verplichte sectie **"Claude moet zijn eigen activiteiten wegschrijven (VERPLICHT)"**:
  raw/ → wiki/ → wiki/log.md → index (`wiki-index-gen.py --write` + lint + graph).
  **Claude doet GEEN `git add/commit/push` — Noa (Hermes) commit + pusht.**
  Claude is klaar wanneer de bestanden + log-entry + index geschreven zijn en meldt dat.
- Delegation Pattern stap 6 toegevoegd/aangepast (write-back, geen git voor Claude).
- Directe aanleiding: de commit-gap 04-08 → 10-09 waardoor Claude "niets nieuws" zag.
- **Aanvulling:** `wiki/reviews/<project>/` en `wiki/audits/` vallen NIET onder de gewone
  wiki-regel — `wiki-index-gen.py` scant enkel `*.md` op het eerste niveau van elke submap,
  dus een review in een project-submap moet handmatig in `wiki/index.md`.
- **Incident (bewezen):** `wiki/reviews/` en `wiki/reviews/crypto-tradebot/` zijn
  **root:root 755** → schrijven als `sjoe` geeft `Permission denied` (gereproduceerd met
  `touch`, exit 1). Géén SMB/NAS- en géén MCP-allowlist-probleem; 21 root-owned paden in de
  tree (allemaal juni 2026, o.a. de reviews-map, `wiki/projects/eveline-mail-*`,
  `wiki/synthesis/l8-*`, `raw/inbox/hermes-skills-2026-06-10.md`).
  Fix gepland: `sudo chown -R sjoe:sjoe` — wacht op Lexi's akkoord.

## 2026-09-10 — Causal Snapshot Tape V0.2 FROZEN + second-brain commit-gap hersteld
- **Type:** project + freeze + fix
- **Bestanden:** [[causal-snapshot-tape-v0]], [[2026-09-10-second-brain-commit-gap]]
- Kantelpunt: een geometrisch correcte level/interaction-tape is NIET automatisch causaal.
  Bewezen fouten: HISTORICAL_WINDOW_TRUNCATION (`final_window[:i+1]` → vroege snapshots 3/10/30 candles),
  TEMPORAL_LEVEL_LEAKAGE (3.474 cluster-preexistentie + 7.901 swing-preconfirmation van 15.062 rijen),
  en SAME-BAR self-reference.
- V0.2 lost dit op: rolling-240 per T (`load_window(end=T, limit=240)`), STATE_BEFORE_T (`end=PREV_T`)
  strikt gescheiden van STATE_AFTER_T, INTERACTION_DURING_T = candle(T) × LEVELS_BEFORE_T,
  snapshot_level_id zonder lineage. 2400 snapshots (alle 240 bars), 8942 interacties,
  alle gates groen, bookkeeping net 13 = observed 13, same-bar 266 = 265 cluster + 1 swing,
  SWING_PROVIDER_REPAINTS = True (1024 zichtbaar / 581 verdwenen / 0 terug).
  **V0.2_FREEZE_READY = True · CAUSAL_SNAPSHOT_TAPE_V0.2 = FROZEN**
- Fix: second brain was sinds **2026-08-04** niet meer gecommit/gepusht (147 gewijzigde/untracked
  bestanden) terwijl de wiki-inhoud t/m 26-08 liep → Claude zag "niets nieuws". Oorzaak en herstel
  in [[2026-09-10-second-brain-commit-gap]].

## 2026-09-08 — Trader-Story A1/A2: audit → RFC → Standalone Story Linker V0 + blind review
- **Type:** project + audit
- **Bestanden:** [[trader-story-a1a2-story-linker-v0]]
- A1 (BREAKOUT→RETEST→HOLD) en A2 (HTF TREND→LTF PULLBACK→LEVEL HOLD) = `ARCHITECTURALLY_NOT_YET_TESTABLE`
  (v03 kent geen event-chain over 3+ snapshots en geen level-identiteit over tijd).
- RFC-eindadvies **A. STANDALONE_STORY_LINKER_SUFFICIENT** (9/10 levels deterministisch volgbaar;
  geen persistente Hermes-laag nodig). `LEVEL_MATCH_CONTRACT_V0` gefrozen.
- Story Linker V0 in `tmp/` (24 tests green); dry replay 9 weken: A1 643/65/132/446, A2 22/14/8.
- FASE 3A blind review pack: 58 charts, SET A=18/B1=20/B2=20, seed `20260908`, ASOF-safety PASS.
- Render-les: eigen matplotlib-renderer afgekeurd → **bestaande `L5_chart.render_chart`** hergebruikt.
- Adversarial re-audit REV_0050..0058 onder STORY CONTRACT V1 → `SYSTEMIC_LEVEL_PROVIDER_BIAS = True`
  (relevant level was vernauwd tot generated 60m-zones).

## 2026-09-08 — Market Situation V0: canonical calendar replication + nieuwe predicates V0.1
- **Type:** project + study
- **Bestanden:** [[market-situation-canonical-calendar-v0-predicates-v01]]
- `CANONICAL_CALENDAR_REPLICATION_V0_COMPLETE`: 9 weken × 672 canonical_T, 0 failures;
  CAL_05 discovery-week byte-identiek (5975 situations, hash `8a2cf8f4…`).
  `MTF_DIRECTION_CONFLICT` bleek 4 pos / 4 neg → eerdere observatie NIET bevestigd.
- `NEW_MARKET_SITUATION_PREDICATES_V01_VALIDATED`: `LEVEL_PROXIMITY_STATE`,
  `WICK_BIAS_STATE`, `HIGH_VOLATILITY_STATE` additief toegevoegd; 27/27 tests;
  `EXISTING_SIX_CHANGED = NO`, `RUNNER_CHANGED = NO`.

## 2026-09-07 — Market Situation V0 — menselijke visuele review voorbereid
- **Type:** project
- **Bestanden:** [[trader-story-a1a2-story-linker-v0]], [[market-situation-canonical-calendar-v0-predicates-v01]]
- Historische scale validation volledig PASS (672 evaluaties, 0 PIT-failures, 0 determinism-mismatches,
  0 duplicate identities, boundary off-by-one gecorrigeerd). Enkel de menselijke visuele audit reste.
- 30 bestaande charts (al gegenereerd via de echte `L5_chart` `render_chart()`) verplaatst naar een
  toegankelijke locatie buiten `/tmp`. Geen charts opnieuw gegenereerd, geen nieuwe random sample.

## 2026-09-06 — 2% prijs-swings augustus 2026 herberekend
- **Type:** fix + analyse
- **Bestanden:** [[trader-story-a1a2-story-linker-v0]]
- Na de correctie van 03-09 zijn de 2%-swingtellingen opnieuw opgebouwd met correcte chronologie.

## 2026-09-05 — Media download gestart (Telegram)
- **Type:** media
- Telegram-sessie: download gestart via de *arr/qBittorrent-stack.

## 2026-09-03 — Correctie: 2% price-swing count ONGELDIG
- **Type:** fix
- **Bestanden:** [[trader-story-a1a2-story-linker-v0]]
- De eerdere 1H-swingoutput bevat aantoonbare chronologische onmogelijkheden (opeenvolgende
  extreme met timestamp vóór de vorige; meerdere HIGH↔LOW legs binnen exact dezelfde 1H-timestamp).
  Met 1H OHLC kan intrabar-ordering niet bepaald worden → tellingen niet bewezen; opnieuw opgebouwd.

## 2026-09-01 — Post-Phase1D evaluation readiness + thin end-to-end driver
- **Type:** project
- **Bestanden:** [[strategy-harness-evaluation-pipeline]]
- Readiness-discovery op de gefrozen base `fd117d9f` (wat kan de pipeline nu werkelijk, wat ontbreekt
  contractueel vóór de eerste strategie-evaluatie). Daarna de kleinst mogelijke end-to-end driver
  bovenop Phase1A→Phase1D (geen nieuwe fase, geen nieuwe metrics, geen strategie-run).

## 2026-08-31 — Phase1D numeric threshold policy — methodologische wording fix (RC2)
- **Type:** fix + methodology
- **Bestanden:** [[strategy-harness-evaluation-pipeline]]
- RC1 `41b1f31c`, frozen semantic contract `be76dd55`. Enkel overclaiming in de woordvoering
  gecorrigeerd; het getal (`min_raw_N=30`, `min_cluster_N=30`) bleef ongewijzigd en is door
  Claude expliciet aanvaard. Geen threshold-wijziging, geen nieuw onderzoekstraject.

## 2026-08-26 — Strategy Harness Evaluation Phase 1B primitives gefrozen
- **Type:** project + freeze
- **Bestanden:** [[strategy-harness-evaluation-pipeline]], [[strategy-harness-evaluation-phase1b-primitives]]
- Phase1B RC1 `a30fce5e` → RC2 `ea7e0467` → RC3 `1c824599` → review `45e8f1ca` (GREEN 0/0/0/3) → freeze `ca1bfd2a`
- Tag: `strategy-harness-evaluation-phase1b-primitives-frozen-20260826` — niet gepusht
- Phase1B 123 passed, Phase1A 52, Phase3B 68/9s, Outcome 186, Guardrail 70/12s, full core 462/17/21s (0 nieuw)

## 2026-08-25 — Phase1A join gefrozen + Hermes/MCP reparaties
- **Type:** freeze + fix
- **Bestanden:** [[strategy-harness-evaluation-pipeline]], [[2026-08-25-hermes-update-mcp-repair]]
- Phase1A join review `4d996d26` (GREEN 0/0/0/2) → freeze `45109f2e`; tag `strategy-harness-evaluation-phase1a-join-frozen-20260825`
- Hermes update v0.20.5 (gateway PID 956674), filesystem MCP `--args` fix, health-monitor better-sqlite3 op `/usr/bin/node` v24

## 2026-08-19 — Evaluation Phase0 contract + Phase3B gefrozen
- **Type:** freeze
- **Bestand:** [[strategy-harness-evaluation-pipeline]]
- Phase3B `213d77db` + Phase0 contract `1225cd8e` (review `2d06134d` GREEN)
- Tag: `strategy-harness-evaluation-contract-phase0-frozen-20260819`

## 2026-08-06 — Eigen communicatie-app met 3D avatar (visie-beslissing)
- **Type:** visie-beslissing
- Lexi beslist: eigen app met 3D avatar, niveau C (volledige GSM-controle)
- Roadmap herzien naar 7 fases: Telegram → PWA → 3D → Native → Hub → Autonomie → Relatie
- Nieuw document: [[noa-future/2026-08-06-eigen-comm-app]]
- README.md en roadmap geüpdatet

## 2026-08-05 — OHLC Bridge Dedup Hardening RC3 (Claude ORANGE review resolutie)
- **Type:** review-resolutie
- **Bestand:** [[crypto-data-ohlc-bridge-dedup-hardening-rc2-rc3-2026-08-05]]
- Claude ORANGE-review → 3 findings RESOLVED: MEDIUM pairs_failed counting, LOW count_archive_lines ambigu, LOW Unicode decode test
- Commit: `5fbba6a8` op `candidate/crypto-data-ohlc-bridge-dedup-hardening-rc3-20260805`
- 40/40 tests PASS. Niet gepusht.

## 2026-07-11 — A0 Phase 1 per-TF rendering + empty section fixes
- **Type:** synthesis + patch
- **Bestanden:** [[a0-snapshot-readout]], [[2026-07-11-a0-per-tf-rendering]]
- Drie iteraties: empty sections → meaningful TF fallback → per-TF rendering
- Hard audit bewees: Hermes-v03 genereert per TF, L4 slaat per TF op, A0 toonde maar 1 TF
- Commit: `735dd471` — Render A0 market context per timeframe
- 61 tests, alle pass. OHLC boundary condition op 12:00 UTC bevestigd als verwacht.
- Bron: Noa sessie 2026-07-11.

## 2026-07-07 — Hermes Skill / Tool Hygiene Audit opgeslagen
- **Type:** audit
- **Bestand:** [[hermes-skill-tool-hygiene-audit-2026-07-07]]
- HERMES AUDIT 07 afgerond. 209 skills, 36 categorieën, 6 leeg. Curator actief (36 stale, 1 reactivated). LLC consolidation OFF.
- Verdict: PARTIAL — cleanup later nodig, niet urgent. 10 critical skills, ~60 stale candidates.
- Geen skills verwijderd of gewijzigd.
- Bron: Noa HERMES AUDIT 07 op 2026-07-07.

## 2026-07-07 — Hermes Boot Policy Summary toegevoegd aan .hermes.md
- **Type:** startup-policy
- **Bestand:** `.hermes.md`
- HERMES AUDIT 06 afgerond. Policies blijven on-demand, maar kernregels staan nu compact in startup/load-pad.
- 10-regel boot summary + on-demand lookup tabel + anti-bloat regel.
- Geen SOUL.md wijziging.
- Backup: .hermes.md.backup-boot-policy-20260707_180004
- Bron: HERMES AUDIT 06.

## 2026-07-07 — Hermes Autonomie Policy vastgelegd
- **Type:** policy
- **Bestand:** [[hermes-autonomie-policy]]
- HERMES AUDIT 05A+05B afgerond. Autonomiegedrag is CLEAR. Policy met 3 zones: GROEN (observeren/rapporteren autonoom), ORANJE (binnen prompt-scope), ROOD (altijd akkoord).
- Correcties: COMMITPROMPT ≠ push akkoord. "Noa beslist" ≠ model/config wijzigen. PRODUCTIEPROMPT = alleen exact beschreven actie.
- Prompt-scope tabel + 12 acceptatietests + stopregels.
- Bron: Noa HERMES AUDIT 05A+05B op 2026-07-07.

## 2026-07-07 — Hermes Health-Monitor Policy vastgelegd
- **Type:** policy
- **Bestand:** [[hermes-health-monitor-policy]]
- HERMES AUDIT 04 afgerond. Health-monitor is MCP meta-monitor, geen systeemmonitor. Bewaakt alleen MCP servers (plex, filesystem).
- Shell blijft verplicht voor CPU/RAM/disk/Docker/systemd. Health-monitor = thermometer voor MCP, niet voor de server.
- Drempels: MCP latency >1000ms warning, >3000ms critical.
- Bron: Noa HERMES AUDIT 04 op 2026-07-07.

## 2026-07-07 — Hermes Final Review Policy vastgelegd
- **Type:** policy
- **Bestand:** [[hermes-final-review-policy]]
- HERMES AUDIT 03 afgerond. Final-review discipline is OK. Policy vastgelegd: status→diff→test→secrets→junk→rollback→akkoord vóór commit/push.
- Stopregels: secrets, generated files, brede diff, test failure, branch onzekerheid.
- Geen git hooks geïnstalleerd. Review blijft handmatig met Pro model.
- Bron: Noa HERMES AUDIT 03 op 2026-07-07.

## 2026-07-07 — Hermes Context Policy vastgelegd
- **Type:** policy
- **Bestand:** [[hermes-context-policy]]
- HERMES AUDIT 02 afgerond. Context-hygiëne is OK. Policy per taaktype vastgelegd: chat/debug/repo/audit/architectuur.
- Harde limieten: max files, max logregels, max wiki pages per type.
- Stale-context regels: fixnotes >90d, logs >14d, inbox >30d.
- Bron: Noa HERMES AUDIT 02 op 2026-07-07.

## 2026-07-07 — Hermes MCP Cleanup + Health-Monitor Fix
- **Type:** fix
- **Bestand:** [[hermes-mcp-cleanup-health-monitor-fix]]
- 6 oude Jul06 MCP zombies gekilled (plex + filesystem). health-monitor config gefixt: args dict→list.
- Na fix: 3/3 MCP servers online (plex 45, filesystem 14, health-monitor 8 tools).
- Backup: config.yaml.backup-mcp-health-20260707_162407
- Bron: Noa + Lexi MCP audit op 2026-07-07.

## 2026-07-07 — L4 Runner V2 Productie Actief — pair-isolated mode
- **Type:** project
- **Bestand:** [[l4-runner-v2-production-active]]
- L4 Runner V2 --pair-isolated geactiveerd in productie l4-filler.service.
- Enkel --pair-isolated toegevoegd aan ExecStart. Geen extra pairs, geen code-wijzigingen.
- Preflight no-write: OK. Handmatige run: +1/+5/+5 per pair. Timer-run: success, pairs_success=2.
- Service backup: l4-filler.service.bak_20260707_155607
- Bron: Noa Hermes productie-activatie op 2026-07-07.

## 2026-07-07 — L4 Raw Blobs Dedup Audit: 0% DEDUP VERKLAARD
- **Type:** project
- **Bestand:** [[l4-raw-blobs-dedup-audit]]
- Audit van 0% raw_blob hergebruik in L4 store. Conclusie: verwacht gedrag — marktdata verandert tussen 5-min snapshots.
- raw_hash = SHA-256 van volledige raw_json (candles + meta + indicators + candle_micro). Geen volatile velden uitgesloten.
- Advies: nu niets wijzigen. Pas bij opschaling naar veel pairs capaciteit meten.
- Bron: Noa Hermes audit op 2026-07-07.

## 2026-07-07 — L4 Autofill 24U Status: ETHEUR + BTCEUR STABIEL
- **Type:** project
- **Bestand:** [[l4-autofill-24u-status]]
- L4 autofill draait 24u stabiel. 297 runs: 283 success (95.3%), 9 ETHEUR transient alignment failures (zelfhelend), 0 BTCEUR failures.
- DB ratios perfect: raw/snap=5.0, tf/snap=5.0. Klaar voor Runner V2 (pair-isolated).
- Bron: Noa Hermes statuscheck op 2026-07-07 14:45.

## 2026-07-04 — OHLC Bridge: SSH disconnect → systemd service + clean store proof
- **Type:** fix
- **Bestand:** [[ohlc-bridge-ssh-disconnect-systemd]]
- Writer stierf door SSH disconnect (SIGHUP). Nu onder systemd user service met Restart=always en Linger=yes.
- Clean store proof: 1/5/5 counts, 240 candles per TF, 0 errors.
- PID 2950878, 26 pairs, 156 OK / 0 fail per cycle.

## 2026-06-11 — structure_roles known debt gedocumenteerd
- **Type:** decision
- **Bestand:** `wiki/decisions/structure-roles-horizontal-zone-known-debt.md`
- **Inhoud:** Consumer-audit van `structure_roles()` horizontale zone substitutie. Conclusie: enkel in test suite gebruikt, geen productie-impact. Parkeren als known debt.
- **CLAUDE.md:** Waarschuwing toegevoegd over `structure_roles().local_upper` als production truth.

## 2026-06-01 — Strategy Audit V1 & V2 voltooid
- **Type:** fix
- **Status:** DONE
- **Samenvatting:** 8 bevindingen waarvan 2 kritiek (testbot configs niet gesynchroniseerd, V2 fib-berekening inverted voor LONG)
- **Bestand:** `tasks/done/strategy-audit-v1-v2-resultaat.md`
- **Geüpload door:** Noa (Hermes) — in opdracht van Claude (Director)
2026-06-02T10:00Z | fix | V3A divergentie backtest_pair vs Runner+V3AStrategy gedocumenteerd | wiki/fixes/2026-06-02-v3a-backtest-divergentie.md
2026-06-02T10:15Z | project | Topic Intelligence Scanner projectpagina aangemaakt | wiki/projects/topic-intelligence-scanner.md
2026-06-02T23:00Z | synthesis | Fundament analyse — candle battle, test-bot fouten, herbouwplan | wiki/synthesis/2026-06-02-fundament-analyse.md
2026-06-04T12:45Z | synthesis | Hermes status: v02 channel_down + indicators + pipeline sync + SOUL.md update | wiki/synthesis/2026-06-04-hermes-status.md
2026-06-06T14:30Z | backtest | PULLBACK_BOUNCE_V0 — NIET tradebaar op ADAEUR/ETHEUR/XBTEUR | wiki/fixes/pullback-bounce-v0-backtest.md
2026-06-06T18:00Z | entity | Lennox profielpagina aangemaakt (sport, games, school, DJ, interesses) | wiki/entities/lennox.md
2026-06-07T16:00Z | fix | FASE 1C outer-envelope tunnel scorer v1-v5 afgekeurd — active/context mixing, upper<=lower, width_atr negatief, inside_ratio verkeerd | wiki/fixes/2026-06-07-outer-envelope-tunnel-v5.md
2026-06-08T19:48Z | fix | stable baseline zone-detectie vastgelegd (commit 002bd6c1) — vaste ATR-band parameters, referentie charts gecommit | —
2026-06-08T20:47Z | fix | Live Flask dashboard gebouwd (commit 92850414) — poort 5001, 4 pairs, Kraken 5m API, S/R +25 candle stippellijn | wiki/fixes/2026-06-08-hermes-v01-flask-dashboard.md
2026-06-08T21:00Z | fix | active_upper/lower herschreven naar score-based selectie — NIET gecommit, wacht op visuele validatie | wiki/fixes/2026-06-08-hermes-v01-active-upper-lower-score.md
2026-06-26T14:00Z | fix | "Warning: Unknown toolsets: moa" opgelost — `- moa` verwijderd uit platform_toolsets.cli in config.yaml | wiki/fixes/moa-unknown-toolset-config-2026-06-26.md
2026-07-01T11:47Z | fix | L4 audit integrity hardening — warnings naar errors, canonical hash, tests 8-12 toegevoegd (59 audit ✅, 162 L4 ✅) | wiki/fixes/2026-07-01-l4-audit-integrity-hardening.md
## 2026-07-11
- Outcome Builder Phase 1A geïmplementeerd en gecommit (901a68e1)
- 48/48 outcome tests, A0 frozen 68/68, totaal 207/207
- Fable Orange → fixes → Green → commit via review gate
- No-backflow regel: outcome data gescheiden van ASOF

2026-07-12T12:48:21+02:00 — wiki/projects/noa-reign-roadmap-v2.md: NOA-Reign Roadmap v2 (visie + Fable + Noa). Vervangt v1. Tijdlijn rond 5/8 operatie, 7-weken herstelvenster, Evidence Lab triggers, Phase 1B prioriteit.
2026-08-12 14:30 — wiki/mcp-stateless-2026-07-28.md aangemaakt (MCP stateless spec 2026-07-28, bron: mcp-use v2 blog + MCP announcement)
