
# Wiki Log

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
