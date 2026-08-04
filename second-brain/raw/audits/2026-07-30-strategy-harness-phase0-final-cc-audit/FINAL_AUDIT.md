# Strategy Test Harness — Phase 0 Final — Independent Read-Only Audit

Audited by: Claude Code (independent verifier role only — no product code, tests, or
branches were modified; no commits, no pushes)
Audit date: 2026-07-30

## 1. Executive Verdict

**VERDICT: ORANGE — NOOP PIPELINE GREEN, HARDEN BEFORE ADAPTER**

The no-op pipeline (single strategy, always `NO_SIGNAL`) works correctly end-to-end
against real BTCEUR and ETHEUR production data, is deterministic, idempotent, and the
Foundation Release Gate is fully green (951/951 real-data tests passing). However,
four confirmed HIGH-severity defects mean the harness is **not yet safe to hand a real
strategy adapter**: (1) the runner returns a `result_hash` that is not the value it
actually persisted, and drops `result_id` entirely from its return value; (2) the
decision validator accepts structurally invalid decisions (non-dict, `None`, list) as
`valid: True`, with no checks on reason-code shape/sorting/dedup or forbidden fields in
`decision.details`; (3) the market-context filter silently deletes 100% of real
trendline-quality `score` fields from every real A0 snapshot tested (BTCEUR and
ETHEUR), via blind keyname matching rather than path/meaning-aware filtering; (4) the
CLI/batch entry points cannot select or configure any strategy other than the
hardcoded `noop v1` — there is no way to operationally exercise a second, real
strategy adapter today. None of these are leaks of Outcome data into Zone A (no
CRITICAL contract/data-leak was found), so the verdict is ORANGE, not RED — but none
of the four should ship un-hardened before a real adapter is built.

## 2. Target SHA and Git Graph

- Repo: `/mnt/otherdrive1/dataLexi/LexiProjects/NOA-Reign`
- Fetched branch: `candidate/strategy-test-harness-phase0-final-20260728`
- `origin/...` resolved to: `835c077fb0e380348bbfdb18e7b736c018af7e44` — **exact match** to the required target SHA.
- Frozen foundation: `798dde1d51f183abfa29a3a35555f870359732a4` — confirmed **ancestor** of target (`git merge-base --is-ancestor` → true).
- Distance foundation→target: **exactly 3 commits** (`af9c6e1e`, `c4fe2654`, `835c077f`).
- Audit worktree: `/tmp/cc-strategy-harness-phase0-final-audit-20260730`, created via `git worktree add --detach`.
  - HEAD == target SHA exactly.
  - Detached (`git symbolic-ref -q HEAD` → exit 1).
  - `git status --short` → clean, both at start and end of audit.

## 3. Diff Scope

`git diff --name-status 798dde1d..835c077f` → **28 files, all additions, 2690 insertions**,
entirely under `projects/hermes-v03-strategy-harness/` (16 `strategy_harness/*` modules +
1 README + 13 test files under `tests/`). `git diff --check` → clean (no whitespace
errors). No file outside the harness directory was touched by this branch.

## 4. Worktree and Import Isolation

Printed `__file__` for every relevant module after inserting only the audit worktree's
paths onto `sys.path`:

```
strategy_harness              -> .../audit-20260730/.../strategy_harness/__init__.py
strategy_harness.runner       -> .../audit-20260730/.../strategy_harness/runner.py
strategy_harness.strategy_runtime -> .../audit-20260730/.../strategy_harness/strategy_runtime.py
strategy_harness.outcome_adapter  -> .../audit-20260730/.../strategy_harness/outcome_adapter.py
strategy_harness.canonical_json   -> .../audit-20260730/.../strategy_harness/canonical_json.py
outcome_builder.canonical_json    -> .../audit-20260730/.../hermes-v03-outcome/outcome_builder/canonical_json.py
outcome_builder.outcome_store     -> .../audit-20260730/.../hermes-v03-outcome/outcome_builder/outcome_store.py
outcome_builder.l4_reader         -> .../audit-20260730/.../hermes-v03-outcome/outcome_builder/l4_reader.py
```

All eight modules load from the audit worktree. **No shadowing** from the main
worktree, other worktrees, `/tmp/phase1b-review-worktree`, site-packages, or stale
`PYTHONPATH` entries. Import isolation: **CLEAN**.

## 5. Test Totals and Test Quality

`pytest --collect-only`: **91 collected**, 0 collection errors.
`pytest -q --tb=short`: **91 passed, 0 failed, 0 skipped, 0 xfailed, 0 warnings, exitcode 0**.
`python3 -m compileall -q strategy_harness`: exitcode 0, no output (clean).

### Quality breakdown of the 91 tests

| Class | Count | Notes |
|---|---|---|
| Strong (real logic, real files, meaningful assertions) | ~78 | `test_identities.py`, `test_canonical_json.py`, `test_result_store.py`, `test_contracts.py` (tests what the validator *actually* checks), `test_outcome_adapter.py`, most of `test_content_hash_regression.py` |
| Placeholder (0 real assertions) | 1 | `test_a0_adapter.py::test_empty_pair_rejected` — body is a bare `pass` with docstring "Wordt getest in real data smoke test"; that smoke test is not part of the automated suite |
| Misleading name vs. behavior | 1 confirmed + 3 narrower-than-claimed | `test_leakage_boundary.py::test_noop_no_forbidden_imports` docstring claims it checks "time/random/uuid/network/file-I/O" but calls `check_no_outcome_imports`, which only checks for the substring `"outcome"`. `test_zone_a_clean`, `test_strategy_runtime_no_outcome_imports`, and `test_noop_strategy.py::test_zone_a_no_outcome_imports` are true but check a materially narrower surface than §6.7 requires (see Finding F7). |
| Duplicate/overlapping | 1 | `test_noop_strategy.py::TestLeakageGuards::test_zone_a_no_outcome_imports` duplicates `test_leakage_boundary.py::test_zone_a_clean` (same call, same dir, same assertion). |
| Mocked away from the two most severe bugs found | 9 | All of `test_runner.py` (5) and `test_batch_runner.py` (4) mock both `a0_adapter.read_a0_context`/`extract_source_snapshot` and `outcome_adapter.lookup_outcome`. This is legitimate for testing control flow (dry-run/rerun/decision-freeze), but it means **none** of these 91 tests exercise real A0 output or catch the `result_hash`/`result_id` return-value bug (F1) or the real-data `score`-stripping bug (F3) — both were only found by this audit's live real-data verification, not by the test suite. |

**No test total was accepted as quality proof without this breakdown**, per audit
mandate.

## 6. Foundation Gate

```
python3 scripts/run_foundation_release_gate.py --real-data \
  --real-data-l4-dir .../hermes-v03-interpreter/l4_store \
  --real-data-cache-dir .../crypto-data/logs/live_cache \
  --output-dir <tmp>
```
Result: **FOUNDATION GREEN — READY FOR STRATEGY TEST HARNESS**, exitcode 0.
14/14 suites green, **951 passed / 0 failed** (sum of all suite counts: 11+98+76+198+
15+29+59+126+61+6+68+48+138+18 = 951, exactly matching the required threshold).
`real-data`: `all_green=True`, `production_safety=True`. `frozen_integrity`: A0 frozen=True,
Phase1A frozen=True, `b5f5b9a_clean=True`. `backflow`: violations=0, all_green=True.
`index`: columns=True, explain_ok=True. The gate's own internal outcome-store writes
went to an isolated temp dir (`/tmp/outcome_store_...`), not the production Outcome
store, and its own `pre_post_manifest_match=True` self-check confirms it did not
mutate the production L4/cache paths it was pointed at.

## 7 & 8. Real-Data Audit — BTCEUR and ETHEUR

Real snapshots used (read-only from production L4, `mode=ro`):
- BTCEUR: `BTCEUR-1785401940-1m5m15m60m240m-90922149f762` (asof_ts=1785401940)
- ETHEUR: `ETHEUR-1785401940-1m5m15m60m240m-a1f6c66c725d` (asof_ts=1785401940)

Real A0 output pulled via the actual A0 CLI (`a0_snapshot_readout.cli`, no
mocks) — BTCEUR 27,153 bytes, ETHEUR 31,807 bytes, both exit 0.

Temporary Outcome Store built via the real frozen API
(`OutcomeStore.write_record`, `make_windows_hash`, `make_outcome_id` — no
hand-rolled records) in an isolated `/tmp` directory. For both pairs, ran via the
actual `strategy_harness.cli` subprocess (no shortcuts):

| Step | BTCEUR | ETHEUR |
|---|---|---|
| dry-run | `written=0`, `result_hash=""` (correct: no bytes computed) | same |
| write | `written=1`, `evaluation_id` deterministic, `decision_id` deterministic | same |
| identical rerun | `written=0`, `skipped_existing=1`, identical `decision_id`/`evaluation_id` | same |
| batch (single-id) | `all_ok=true`, `not_applicable=1` | n/a (batch demoed on BTCEUR) |
| idempotent batch rerun | `written=0`, `skipped_existing=1`, `all_ok=true` | n/a |
| results.jsonl | 1 line, file sha256 `3982a4d5...` | 1 line, file sha256 `7ff971eb...` |

Both pairs: `score.status="NOT_APPLICABLE"`, `score.reason_codes=["NO_SIGNAL"]` (correct
for the noop strategy). Pipeline is deterministic and idempotent against real data —
**confirmed positive**.

## 9. Result Identities (Hypothesis 6.1) — CONFIRMED HIGH

See Finding **F1**. Reproduced against both a mocked fixture and real BTCEUR
production data with concrete SHA-256 values (see §17).

## 10. A0-Context Integrity (Hypothesis 6.2) — CONFIRMED HIGH

See Finding **F3**. Reproduced against real BTCEUR (12 `score` fields) and real
ETHEUR (16 `score` fields) snapshots: **100% silently stripped, 0% survive**,
`run_strategy` returns `valid=True` with no warning.

## 11. Outcome Identity Validation (Hypothesis 6.5) — MOSTLY ROBUST, ONE CONFIRMED GAP

The frozen resolver's cryptographic checks are **robust**: corrupting
`windows_hash`, `outcome_id`, `record_id`, `record_hash`, `previous_record_hash`
(rev-1 non-null), `record_revision`, or `store_schema_version` (unknown value) each
independently caused `lookup_outcome` to fail closed with
`OUTCOME_RESOLVER_FAILED` (frozen `resolve_outcome` rejecting the record). This is
good news, not a defect — the identity chain does **not** accept a "just
non-empty" corrupted field as valid.

One confirmed gap: see Finding **F6** (content_hash silently unverified when
demanded-but-absent).

## 12. Leakage/Backflow (Hypothesis 6.7) — CONFIRMED MEDIUM (test-coverage gap, not an active leak today)

See Finding **F7**. The actual `noop_v1.py` only imports `copy`, so there is **no
active leak today** — but the guard code and its tests prove a much narrower
claim than the full forbidden-surface list in the audit mandate (subprocess,
socket, requests/urllib/httpx/aiohttp, `os.environ`/`getenv`, `secrets`, `uuid`,
`datetime.now/utcnow`, dynamic-import-of-unauthorized-module are **not** checked
by any test or guard function).

## 13. Result Store (Hypothesis 6.6) — MOSTLY ROBUST, ONE LOW GAP

Confirmed correct: append-only under `fcntl` lock, canonical bytes + trailing
newline, incomplete-last-line rejected, unparseable-record rejected, duplicate
`evaluation_id` + identical bytes → skip, duplicate `evaluation_id` + different
bytes → `CONFLICT`, dry-run creates no directory/file/lock artifact, interior
blank line between two records → rejected as corrupt.

One LOW gap confirmed live: a **trailing** blank line immediately before EOF is
*not* detected as corruption, because the corruption check does
`existing.strip().split("\n")` — `.strip()` silently eats a trailing blank line
before the empty-line check ever sees it. Interior blank lines are caught
correctly; only the trailing-before-EOF case slips through. LOW severity —
doesn't cause silent data loss, just a hardening gap in the corruption detector.

No public store-wide validation/lookup/verify-all function exists beyond
`write_result` itself; there is no `read_and_verify_store()` style API for
external consumers to independently re-validate a full `results.jsonl`.

## 14. Historical Snapshot Reachability (Hypothesis 6.9)

Both `BTCEUR/` and `ETHEUR/` under the production L4 store currently contain
**exactly one** `.sqlite` file each (`2026-07.sqlite`; BTCEUR 6179→6185 rows
during the audit window, ETHEUR 6134→6140 rows — see §16). **No current
correctness blocker** — with a single file per pair, `_find_latest_db()`'s
"always pick the single newest file" logic is trivially correct.

Forward-looking limitation (not a current bug): the frozen `_find_latest_db()`
in `outcome_builder/l4_reader.py` always returns only the lexicographically
last `.sqlite` filename for a pair, with no parameter to select an older month.
Once a second month's file appears, snapshots in the older file will become
unreachable via `read_snapshot_metadata`/`extract_source_snapshot` regardless of
which `snapshot_id` is requested. Classify as **scalability limitation to harden
before the store spans multiple months**, not a Phase-0 blocker.

## 15. First-Adapter Wiring (Hypothesis 6.11) — CONFIRMED HIGH

See Finding **F4**. Adapter contract (function signatures) exists; adapter
*selection* via CLI/batch does not.

## 16. Source Safety

Manifested (path, size, mtime_ns, sha256) before and after all testing:
frozen `outcome_builder/{canonical_json,l4_reader,outcome_store,outcome_identity}.py`,
all of `a0_snapshot_readout/`, `scripts/run_foundation_release_gate.py`, all of
`strategy_harness/` — **all identical before/after** (0 diffs). No test/probe run
by this audit modified any of these.

**L4 SQLite files did change** during the audit window:
- BTCEUR: 6179→6185 rows, max `asof_ts` 1785401940→1785403980 (monotonic forward growth, +6 rows, ~34 min advance)
- ETHEUR: 6134→6140 rows, max `asof_ts` 1785401940→1785403920 (monotonic forward growth, +6 rows)

This is **attributed to the live external production data-ingestion pipeline**
that continues to run in this environment independent of the audit, not to any
audit action, based on: (1) every L4 read performed by this audit used
`mode=ro` (frozen `l4_reader.py`) or `sqlite3 "file:...?mode=ro"`, both
structurally incapable of writing; (2) growth is strictly forward/additive
(no rows changed or disappeared — consistent with a live feed appending new
5-minute snapshots, not corruption); (3) the Foundation Gate's own internal
`production_safety=True` / `pre_post_manifest_match=True` self-check confirms
its test suites did not touch the production L4 path either. `live_cache`
directory file count was stable (854 files before and after); this audit never
passed `--cache-dir` to any harness invocation (consistent with Finding F5:
the parameter is unused by the code under test anyway).

`git status --short` in the audit worktree: clean, before and after. `git
status --short` in the main worktree: unchanged from the session's starting
state (same untracked scratch directories/files present before this audit
began — not created by this audit).

## 17. Findings by Severity

### F1 — HIGH — `runner.py` returns a `result_hash` that is not the persisted record's `result_hash`, and omits `result_id` entirely
- File/function: `strategy_harness/runner.py:114-124` (`run_single`), consuming `strategy_harness/result_store.py:16-133` (`write_result`), `strategy_harness/identities.py:59-76` (`result_id`/`result_hash`)
- Status: **CONFIRMED** (mocked fixture *and* real BTCEUR production data)
- Reproduction: live write-run, output dir `/tmp/cc_strategy_harness_phase0_final_VvEvK1/btceur_single`.
  - Runner returned: `result.result_hash = 3982a4d5767c4638257e77bf1eeae13bfbb31ebc9bf1759c9110d3ca218c7835`
  - Physical JSONL line SHA-256 (incl. trailing newline): `3982a4d5767c4638257e77bf1eeae13bfbb31ebc9bf1759c9110d3ca218c7835` — **identical to what the runner returned**
  - Actual stored record's `result_hash` field (the semantically-defined value per `identities.result_hash()`): `f28e0728201bc949e7f4aaa3512c4b841385951e1e1a49d6702351795dc1aab0` — **different**
  - Stored record's `result_id`: `7ebe0736df87df26d906d6443e0ec79b2894761676f60eb71731cc8ce87a1a6a` — **not present anywhere in `runner["result"]`**
- Root cause: `runner.py:122` does `"result": {**result, "result_hash": wr.get("sha256", ""), ...}` where `wr["sha256"]` is `result_store.py`'s physical-line SHA (used internally for byte-identity/idempotency comparisons), not the semantic `result_hash()` that actually gets written into the record.
- Impact: any caller of `run_single`/`run_batch` (CLI `--json` output, a future adapter, an audit script) that trusts `result["result_hash"]` as the record's content-integrity hash is silently checking the wrong value, and cannot recover `result_id` from the return value at all.
- Minimal fix: after `write_result` returns, either (a) re-read the persisted record and return its actual `result_id`/`result_hash` fields, or (b) have `write_result` return the correct `result_id`/`result_hash` values it computed (it already has them in `full_result` before writing).

### F2 — HIGH — `validate_decision()` accepts structurally invalid decisions as valid
- File/function: `strategy_harness/contracts.py:129-158` (`validate_decision`)
- Status: **CONFIRMED**
- Reproduction (live probe):
  - `decision="not-a-dict"` → `{"valid": True}`
  - `decision=[]` → `{"valid": True}`
  - `decision=None` → `{"valid": True}`
  - `decision={..., "details": "not-a-dict"}` → `{"valid": True}`
  - `decision={..., "reason_codes": [1, None, "lowercase", "DUP", "DUP"]}` → `{"valid": True}`
  - `decision={..., "reason_codes": ["Z", "A"]}` (unsorted) → `{"valid": True}`
  - `strategy_id=""` → `{"valid": True}`
  - `strategy_version=0` or `"1"` (string) → `{"valid": True}`
  - `source_snapshot="not-a-dict"` (inside the decision record itself) → `{"valid": True}`
  - `strategy_input_hash=""` or `"abc"` (too short) → `{"valid": True}`
  - `decision.details={"pnl": 100}` (forbidden-outcome-shaped field) → `{"valid": True}` — **`validate_decision` never runs the forbidden-key scan that `validate_strategy_input` does**
- Root cause: the signal/eligible/reason_codes checks in `validate_decision` are gated behind `if isinstance(decision, dict):` — when the value is not a dict, the whole block is skipped and no error is recorded. There is no type/format/positivity check on `strategy_id`, `strategy_version`, `strategy_input_hash`, or `source_snapshot` at all, and no forbidden-key scan of `decision.details`.
- Impact: not exploitable today (the only strategy, `noop_v1.evaluate`, always returns a well-formed dict), but this is exactly the checkpoint a real strategy adapter must pass through. A buggy or malicious future strategy module could return a non-dict decision, unsorted/duplicated/lowercase reason codes, or outcome-shaped data inside `details`, and it would sail through validation undetected.
- Minimal fix: require `isinstance(decision, dict)` unconditionally (else error); validate `reason_codes` elements are non-empty uppercase strings, sorted, deduplicated; validate `strategy_id` non-empty str, `strategy_version` positive int, `strategy_input_hash` fixed-length hex string, `source_snapshot` is a dict with required keys; run the existing `_check_forbidden` scan over `decision.details`.

### F3 — HIGH — `market_context` filter silently deletes 100% of real trendline-quality `score` fields on every real snapshot
- File/function: `strategy_harness/strategy_runtime.py:14-36` (`_filter_market_context`)
- Status: **CONFIRMED** (real BTCEUR and ETHEUR production A0 output)
- Reproduction:
  - Real BTCEUR A0 output contains 12 `score`-keyed fields (e.g. `trendlines.5m.stored_values["trendlines.recent.upper"].score = 10`), all structural trendline-touch-quality metrics, not trading/outcome data.
  - Real ETHEUR A0 output contains 16 such fields.
  - After `build_strategy_input()` → `_filter_market_context()`, **0 of 12 (BTCEUR) and 0 of 16 (ETHEUR) survive** into `StrategyInput.market_context`.
  - `run_strategy()` returns `valid: True` in both cases — no error, no warning, no log that data was removed.
- Root cause: `STRIP_DEEP = {"score"}` matches purely on key **name**, with no awareness of path or semantic meaning. Any dict key literally named `score`, more than one filter-level deep, is deleted regardless of what it represents.
- Impact: this is the audit's own named concern realized in practice — the harness silently deprives every real strategy of legitimate, structural A0 information (trendline reliability scores) solely because of a keyname collision with the Outcome-domain's forbidden-field list (which uses `score` to mean *trading P&L score*, an unrelated concept).
- Minimal fix: leakage control must become path- and semantics-aware (e.g. only strip `score` when it appears under an actual outcome/result-shaped subtree, or maintain an explicit allow-list of legitimate A0 `score` paths) rather than a blind global keyname match.

### F4 — HIGH — CLI/batch cannot select or configure any strategy other than hardcoded `noop v1`
- File/function: `strategy_harness/cli.py:44-78` (`main`, `cmd_single`, `cmd_batch`)
- Status: **CONFIRMED**
- Evidence: `cli.py`'s `single`/`batch` subparsers expose `--pair --snapshot-id(s) --l4-dir --outcome-store --output-dir --cache-dir --dry-run --json` only. There is no `--strategy-id`, `--strategy-version`, or `--strategy-config` argument anywhere in `cli.py`, even though `run_single`/`run_batch` accept `strategy_id`/`strategy_version` keyword parameters that default to `"noop"`/`1`. `strategy_config` is not threaded through the CLI or `run_single`/`run_batch`/`build_strategy_input` call chain from the CLI at all.
- Impact: adapter **contract** exists (function signatures), but adapter **selection** does not — there is currently no operational way to run a second strategy end-to-end via the CLI or batch entry points. Consequently `scorer.py`'s `LONG`/`SHORT`/`UNSCORABLE` branches are entirely unexercised by any real code path today (only the `NO_SIGNAL`→`NOT_APPLICABLE` branch is reachable).
- Classification per audit's own framework: (A) adapter contract — ready; (B) adapter scorer — only the no-op branch is exercised, LONG/SHORT/partial-outcome behavior is unverified in practice; (C) trading performance — correctly out of scope for Phase 0.
- Minimal fix: add `--strategy-id`/`--strategy-version`/`--strategy-config` to both CLI subcommands and thread `strategy_config` through to `build_strategy_input`.

### F5 — MEDIUM — `cache_dir` is a dead/misleading parameter (API drift)
- File/function: `strategy_harness/a0_adapter.py:84-123` (`read_a0_context`)
- Status: **CONFIRMED**
- Evidence: `cli.py` exposes `--cache-dir`; `run_single`/`run_batch`/`runner.py` thread `cache_dir` through as a keyword parameter down to `read_a0_context(snapshot_id, l4_dir, pair, cache_dir=None)`. Inside `read_a0_context`, the `cache_dir` parameter is **never referenced anywhere in the function body** — not passed to the A0 CLI subprocess command list, not set as an environment variable, not used at all.
- Impact: an operator who supplies `--cache-dir` believing it affects the A0 lookup gets silent no-op behavior — API drift between what is offered and what is honored.
- Minimal fix: either wire `cache_dir` into the A0 CLI subprocess invocation (if the A0 CLI supports a cache flag) or remove the parameter from the public API until it is actually implemented.

### F6 — MEDIUM — `outcome_adapter.lookup_outcome` silently accepts a record as "verified" when the caller demands `content_hash` but the record has none
- File/function: `strategy_harness/outcome_adapter.py:174-179`
- Status: **CONFIRMED** (currently a latent/dead code path, not exploitable in Phase 0)
- Reproduction: `lookup_outcome(..., content_hash="expected_real_hash_xyz")` against a real, validly-signed record whose `source_snapshot` has no `content_hash` key → `found=True`, `error=None`.
- Root cause: `if content_hash and ss.get("content_hash"): ...compare...` — when the caller supplies a `content_hash` but the record's `source_snapshot.content_hash` is absent/falsy, the entire comparison block is skipped (both operands must be truthy), so no mismatch is ever raised.
- Impact today: **latent only** — `strategy_harness/a0_adapter.py`'s own docstring confirms the frozen L4 reader never supplies a `content_hash` (`extract_source_snapshot` never returns that key), so `runner.py` currently always calls `lookup_outcome` with `content_hash=None`, and this path is never actually exercised in the shipped pipeline (confirmed: `test_content_hash_regression.py` exercises this scenario directly and documents it as expected `Test C` behavior — the harness authors were aware and treat "no hash available" as an accepted trust boundary for Phase 0). It becomes a real risk the moment upstream starts supplying real `content_hash` values, since a caller that *thinks* it demanded verification would get a false sense of security for any record lacking the field.
- Minimal fix: when the caller passes a non-None `content_hash` but the record has none, return a distinguishable `error` (e.g. `CONTENT_HASH_UNVERIFIABLE`) rather than silently treating it as verified.

### F7 — MEDIUM — Leakage/backflow guard and its tests cover a materially narrower surface than the audit's forbidden-import contract, and one test's docstring overstates what it checks
- File/function: `strategy_harness/guardrails.py` (`audit_zone_a`, `check_no_outcome_imports`, `check_no_forbidden_imports`); `tests/test_leakage_boundary.py:20-26`
- Status: **CONFIRMED**
- Evidence:
  - `test_leakage_boundary.py::test_noop_no_forbidden_imports` docstring: *"noop_v1.py importeert geen time/random/uuid/network/file-I/O"* — but the test body calls `check_no_outcome_imports(fp)`, which **only** checks for the substring `"outcome"` in import names. It provides zero evidence about time/random/uuid/network/file-I/O.
  - `audit_zone_a()`'s own broader check (`check_no_forbidden_imports`) uses the list `["scorer", "result_store", "outcome_adapter", "trader", "testbot", "portfolio", "random", "time"]` — missing `secrets`, `uuid`, `os.environ`/`getenv`, `open`/`pathlib`, `subprocess`, `socket`, `requests`/`urllib`/`httpx`/`aiohttp`, `datetime.now/utcnow`, `A1`, and dynamic-import-of-unauthorized-module detection, all of which the audit mandate requires.
  - `audit_zone_a()` only scans files under a `strategies` directory; it is never run against `strategy_runtime.py` itself (which README.md explicitly names as part of Zone A) with the broader forbidden-import list — only the narrower `check_no_outcome_imports` runs against it.
- Impact today: **no active leak** — `noop_v1.py` imports only `copy`, so it happens to pass every check trivially. The gap is in test/guard **coverage**, not a demonstrated leak.
- Minimal fix: expand `check_no_forbidden_imports`'s forbidden list to match the full mandate; run it against `strategy_runtime.py` and all future strategy files, not just files under `strategies/`; fix the misleading docstring or make the test call the function its docstring claims to call.

### F8 — LOW — `result_store.py`'s corruption check misses a trailing blank line before EOF
- File/function: `strategy_harness/result_store.py:66-104` (`write_result`)
- Status: **CONFIRMED**
- Reproduction: file content `{"a":1}\n\n{"b":2}\n` (interior blank line) → correctly rejected as `CORRUPT_RESULT_STORE: empty line`. File content `{"a":1}\n\n` (blank line trailing before EOF) → **accepted silently**, new record appended without error.
- Root cause: `existing.strip().split("\n")` — `.strip()` removes the trailing blank line before the per-line emptiness check ever runs.
- Impact: minor — doesn't cause data loss or misreads (the parseable line is still read correctly), just a hardening gap in the corruption detector's coverage.
- Minimal fix: check for trailing blank lines / require `existing` to end with a single `\n` and no earlier consecutive `\n\n`, without `.strip()`-ing before the split.

### F9 — LOW — Forward-looking scalability limitation: only the newest `.sqlite` file per pair is ever read
- File/function: `outcome_builder/l4_reader.py:34-45` (`_find_latest_db`, frozen dependency, not part of this diff)
- Status: **CONFIRMED, not currently exploitable** (single `.sqlite` file per pair exists today)
- Impact: once L4 store spans more than one month per pair, older-month snapshots become permanently unreachable via `extract_source_snapshot`/`read_snapshot_metadata` regardless of requested `snapshot_id`, since the function unconditionally picks the lexicographically-last filename. Flag for hardening before the harness needs to evaluate multi-month historical data — not a Phase-0 blocker.

### F10 — LOW — No `contract.md`; documentation is otherwise consistent with code
- File/function: `projects/hermes-v03-strategy-harness/README.md`
- Status: **CONFIRMED**
- Evidence: only `README.md` exists under the harness directory; no separate `contract.md`. README's stated three-zone architecture, CLI examples, and "Limitations (Phase 0)" list are all consistent with what the code actually does, **except** it does not mention the `cache_dir` dead-parameter (F5) or the content_hash-optional trust boundary (F6) as explicit limitations.
- Minimal fix: either add a `contract.md` per the original spec, or fold the F5/F6 caveats into README's Limitations section.

## 18. Required Corrections Before Next Phase

Before a real strategy adapter is built on top of this harness:
1. Fix F1 — align `run_single`/`run_batch`'s returned `result_hash`/`result_id` with the actually-persisted values.
2. Fix F2 — harden `validate_decision` (dict-type enforcement, reason-code shape/sort/dedup, forbidden-key scan on `details`, field format checks).
3. Fix F3 — make market-context leakage filtering path/semantics-aware so real A0 structural data (`score` etc.) is not silently dropped.
4. Fix F4 — expose strategy selection (`--strategy-id`/`--strategy-version`/`--strategy-config`) through the CLI and batch runner, and exercise the scorer's LONG/SHORT/partial-outcome branches with a real second strategy before declaring the adapter contract operational.
5. Harden F5–F8 (dead `cache_dir` parameter, content_hash silent-accept, leakage-guard coverage gap and misleading test, trailing-blank-line corruption check) — MEDIUM/LOW, but should be closed alongside the HIGH items rather than deferred indefinitely.
6. F9/F10 — track for future hardening (multi-month L4 reachability, `contract.md`), not blocking.

## 19. Definitive Verdict

**ORANGE — NOOP PIPELINE GREEN, HARDEN BEFORE ADAPTER.**

The no-op pipeline is real, deterministic, idempotent, and passes the Foundation Gate
against live production data with zero data-safety incidents caused by this audit.
It is not READY-GREEN for a first real strategy adapter because of four confirmed
HIGH-severity findings (F1–F4) that a real adapter would immediately expose or be
harmed by. It is not RED because no Outcome-domain data leak into Zone A was found,
identity chaining and cryptographic corruption-resistance are otherwise robust, and
the real-data/foundation-gate/idempotency requirements were all met.
