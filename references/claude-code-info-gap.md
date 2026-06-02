---
type: reference
status: canonical
workstream: null
last_verified: 2026-06-02
last_verified_against: 699015b
---

# Claude Code Info Gap

**Purpose:** Context that lives only in chat memory / chat conversation and is NOT reachable from `~/its/` or `~/its-blueprint/` on a fresh Claude Code (CC) session. Drop this in project files so a chat-session can hand it to CC at spin-up, or so a fresh chat-session can re-orient quickly.

**Last refreshed:** 2026-06-02
**Maintained by:** chat-session at session close (treat as living doc)

---

## 1. Operator Communication Preferences

These are not in any repo. They govern how CC should respond to Seth in conversation/PR comments.

- **Concise and technically precise.** No preamble, no padding, no apology loops.
- **Delegate decisions when asked for a recommendation.** When Seth asks "which approach?" he wants a clear call with reasoning, not an options list. Options-list responses read as evasion.
- **Ask clarifying questions when genuinely ambiguous** — but don't manufacture ambiguity to stall.
- **Add context when necessary.** Explain larger concepts on first introduction; assume basic knowledge otherwise.
- **NEVER push back on operator scheduling, energy, or timing.** Don't suggest deferring. Don't comment on time of day or diminishing returns. Don't dress timing pushback as deference ("Path B is more conservative" when not asked). Operator says do X → do X. Only acceptable commentary is technical tradeoff about the work itself.
- **Push until satisfied, then document thoroughly.** Seth prefers a hard sprint followed by comprehensive docs over stopping at natural pauses.

---

## 2. Identity & Repo Map

| Item | Value |
|---|---|
| Customer 0 | Evergreen Renewables (family company, HQ Southern California, large construction projects in Oregon) |
| Operator | Seth (SolutionSmith-debug on GitHub) |
| Execution repo | `SolutionSmith-debug/its` (PUBLIC) |
| Blueprint repo | `SolutionSmith-debug/its-blueprint` (PRIVATE) |
| Local execution path | `~/its/` |
| Local blueprint path | `~/its-blueprint/` |
| Key contact | Ezra Jones — `ezraj@evergreenrenewables.com` |
| Mirror tenant | `seths@evergreenmirror.com` |

**ITS = Integrated Technical System** (renamed from TITS on 2026-05-10). White-glove custom development practice, NOT multi-tenant SaaS. Each customer is forked from the blueprint into a private repo. "Productization" means reusable patterns for Seth's efficiency, not a shared product.

**Two-repo doctrine:**
- **Blueprint wins on conflict.** Doctrine, missions, briefs canonical in `its-blueprint`. Code canonical in `its`.
- Chat-side: blueprint is NOT git-cloneable from claude.ai (no GitHub MCP). Chat reads blueprint via project knowledge where `.md` files are uploaded. Execution repo is public so chat can `web_fetch` raw URLs or git clone.
- CC-side: both repos are on local filesystem.

**Email typo trap:** `Evergreen_Contacts.pdf` row for Ezra has `evergreenrenwables.com` (missing the 'e' in 'renewables'). Use the correct spelling everywhere — docs, code, ITS_Config rows, mirror tenant aliases.

---

## 3. Core Doctrines (Non-Negotiable)

These are codified in `its-blueprint/doctrine/` but worth restating for fast load:

### System-wide invariants (Foundation Mission, Op Stds §3)
1. **External Send Gate** — No external transmission without explicit human approval. Two-process model per workstream + capability-gating AST test (`tests/test_capability_gating.py` in execution repo).
2. **Adversarial Input Handling** — External content is untrusted. 6-layer defense: sender allowlist, untrusted-content tagging, capability gating, structured outputs, anomaly logging, plus the External Send Gate as final stop.

Restate these in every brief touching external-bound code OR external content ingestion. Use `prompts/snippets/invariant-restatement.md`.

### Push-vs-Record Separation (Op Stds §3.1)
- Dedupe applies only to **push**, never to **records**.
- Resend = canonical push leg (subject to suppression).
- Smartsheet `ITS_Errors` + Sentry always write as forensic surfaces.
- Sentry alert rules + Smartsheet sheet-level notifications default-off. Enabling either converts cross-leg dedupe into an active design problem; `Correlation_ID` is wired and ready.

### Preservation-over-Refactor (Op Stds §14)
- When chat-session code lands in `~/its/` and trips ruff/mypy, prefer `[tool.ruff.lint.per-file-ignores]` in `pyproject.toml` over rewriting working code.
- Defer abstraction until **≥4 real reuse cases**.
- Exception: real dead code (not stylistic FP) may be deleted with the ignore.
- Canonical examples: PR #4 (1295a93) + PR #8 (parse_job_v3 F841 closure).

### SDK-vs-Live Integration Test Discipline (Op Stds §30)
- `SimpleNamespace` mocks at SDK boundary miss live API enforcement (body shape, required fields, value wrapping) AND SDK runtime state (in-process caching).
- 4 instances of this bug in 2 days (PRs #47/#48/#49/#51) is what forced this rule.
- Any new `shared/*` SDK wrapper with create/update/delete on typed columns/rows gets a parallel integration test.
- Run with `pytest -m integration` against throwaway sandbox resources. CI skips by default.

### Verify-before-fix
- Cascade updates, session-wraps, briefs, and PR-landed claims capture state at authorship.
- Before acting on any such claim, verify state hasn't changed.
- PR #34 ghost (closed-not-merged, claimed landed in memory) is the canonical failure case.
- **Cost of pausing = minutes; cost of not pausing = shipping stale work.**

### Brief-authoring discipline (2026-05-24, post-PR #86 drift catch)
- When generating CC briefs that name specific files, functions, or current-state claims ("X is hardcoded", "Y not built"), **READ THE CODE FIRST**.
- For chat: `git clone SolutionSmith-debug/its` (public) or `web_fetch` raw URLs.
- PR #86 drift: §A1 already delivered, §A4 named nonexistent `shared/alert.py`, §A5/§B3 wrong specifics. CC caught all of it.
- Briefs making code-shape claims get a code read first.

---

## 4. PR Workflow Discipline

### Four-part PR-landed verification (codified 2026-05-23, PR #74, `docs/operations/pr_merge_discipline.md`)

All four required before a PR is considered landed:

1. `state == MERGED`
2. `mergedAt` is non-null
3. `mergeCommit.oid` is present
4. **Main-branch CI on the merge commit = SUCCESS**

Run: `gh pr view <num> --json mergedAt,mergeCommit,state` immediately after `gh pr merge --squash --delete-branch`. Then check main CI run on the merge commit.

Session logs say **"four-part verify clean"** when confirmed. The earlier three-part verification missed Run 229+ post-merge reds from PR #68 (6 consecutive). Four-part is required every PR.

### Merge command
```bash
gh pr merge --squash --delete-branch
gh pr view <num> --json mergedAt,mergeCommit,state
# then verify CI on merge commit on main
```

### Branch protection (configured 2026-05-24, server-side)
- Strict status checks, contexts=`["test"]`, app_id=15368
- `required_linear_history=true` (squash-only)
- `allow_force_pushes=false`, `allow_deletions=false`
- `required_conversation_resolution=true`
- `enforce_admins=false` (emergency lever)
- `required_pull_request_reviews=null` (solo + CC, CI is the gate)
- Local complement: `block-dangerous-git.sh` hook

---

## 5. Known Traps & FP Patterns

### PR-number prediction drift (2026-05-28)
Never hard-code a predicted PR number into docs/code before `gh pr create` returns the actual number. The issue/PR counter advances unpredictably — predicted #103 was actually #104 because #103 was an unrelated open PR. Pattern: use a placeholder (`#TBD`) and fill in after creation, or accept a follow-up correction commit. A correction commit is cheap; stale PR citations in docs are not.

### Op Stds is canonically v16 (as of 2026-06-02)
v12 added §§37–41 (CC Skills / Agent Guardrails / Per-Customer-Fork Security / Migration-Script PII / Actions Version-Bump). v13 added §42 (code-level self-documentation discipline). v14 (F07, PR #23, 2026-05-29) reframed §1 kill switch from implied "security control" to "operator-convenience suggested pause, NOT a security boundary" (fail-open by design; External Send Gate = real boundary). v15 added §43/§44 (successor-remediation documentation discipline + Tier-2 Claude-assisted repair path) with the Developer-Operator / Successor-Operator role split. v16 reframed §44's Tier-2 boundary as training-bounded co-resolution — no structural maintenance enforcement layer built or required. New content citing `Op Stds §N` should reference v16. Historical version references in older tech-debt entries and session logs are grandfathered.

### CodeQL false positives (Python + Actions, weekly, since 2026-05-24)
Dismiss-as-FP unless content shows actual secret/PII value being logged:
1. Logging Keychain **service-name constants** (name, not value).
2. OAuth URL with public `client_id` + single-use CSRF `state`.
3. Any `print()` in modules with `trusted_contacts` in path (filename heuristic).

### `security` CLI — `set-generic-password` stdin shape (F04, 2026-05-28)
`shared/keychain.set_secret()` passes the secret via stdin, not argv. The argv shape is load-bearing and non-obvious:

- **`-w` MUST be the last option.** `-w` reads from stdin when it's last; if any option follows it (e.g., `-U`) that next token is consumed as the password literal instead.
- **stdin must be `f"{value}\n{value}\n"`** (password + retype confirmation). A single newline causes the CLI to wait for the second entry.
- **The safe ordering:** `["security", "add-generic-password", "-U", "-a", account, "-s", service, "-w"]`
- Discovered as a textbook SDK-vs-Live (Op Stds §30) bug: the brief's prescribed shape (`[... "-w", "-U"]` + `input=value`) was broken against the live `security` CLI — `-w` swallowed `-U` as the password, and stdin was the retype prompt, not the primary read. Live-verified with a create→read→rotate→delete round-trip before PR #113 merged.

### Secret-exposure baseline (gitleaks 8.30.1, 2026-05-24)
- 0 findings, 0 CI/env/Dependabot secrets, 0 env/credential files ever committed.
- Clean by architecture — all secrets in macOS Keychain (`shared/keychain.py` + `.gitignore`).
- Repo stays public. Re-run gitleaks periodically after new `shared/*` SDK wrappers.

### GitHub Actions version bumps
- Verify latest tag via `gh api repos/<owner>/<repo>/releases/latest`.
- Read release notes for breaking changes before bumping.
- Never blanket-upgrade.
- PR #81 reference: `actions/checkout @v4→@v6` (v6.0.2), `actions/setup-python @v5→@v6` (v6.2.0), cleared Node 20 deprecation.

### `gh pr merge --delete-branch` fails when cwd is a worktree, not ~/its (F02/F22, 2026-05-29)
When the session is rooted in a git worktree (e.g., `~/its-f02-f22` on branch `f02-f22`) and the PR is merged with `gh pr merge --squash --delete-branch`, the GitHub-side merge lands successfully but the post-merge local `checkout main` step fails because `main` lives in `~/its`, not the worktree. The remote branch (`origin/f02-f22`) is also NOT auto-deleted — the `--delete-branch` flag's local-cleanup leg cannot run. **Workaround:** merge lands GitHub-side (four-part verify still passes); manually delete the remote branch afterward with `git push origin --delete <branch>`. The git-guardrail hook blocks `push --delete` syntax as a false positive on this form — use `gh api -X DELETE repos/{owner}/{repo}/git/refs/heads/<branch>` instead.

### Smartsheet cell-history `modifiedBy` has name+email only — no user ID (F22, 2026-05-29)
`get_cell_history` returns `CellHistoryEvent.modified_by` with `name` and `email` fields; there is no stable user-ID field. `shared/approval_verification.py` therefore matches on email address (compared against the `safety_reports.authorized_approvers` ITS_Config row, which stores a comma-separated email list). This means: (a) approver identity is only as reliable as the email claim, (b) if an approver's email changes, the ITS_Config row must be updated, (c) there is no cross-tenant user-object comparison available. Documented as a deliberate limitation in `shared/approval_verification.py` §42 docstring.

### Mocks pass but live fails — mandatory live smoke required before merge (2026-06-02)
Three distinct live failures surfaced during the F08/F09 manual smoke that all unit-test mocks passed cleanly:

1. `intake_poll` crashed on its `polling_enabled` config read when the breaker was OPEN — `_read_str_setting` didn't propagate `SmartsheetCircuitOpenError`; mocks never trip the breaker path.
2. `weekly_send_poll` scan-failure path wrote `ERROR` heartbeat status instead of `CIRCUIT_OPEN` — dead path in unit tests.
3. `circuit_breaker.is_open()` ignored the `enabled` flag — mock returned True regardless.

Pattern: new cross-cutting behavior (a breaker, a rate cap, a new exception subtype) is almost never fully exercised by existing unit-test mocks because the mocks were written before the cross-cutting module existed. The operator's rule is **mandatory manual live smoke on the actual daemons before merge** for any new shared infrastructure. All three bugs above were caught this way; all three would have gone to production had the smoke been skipped. SDK-vs-Live (Op Stds §30) applies to daemon integration, not just SDK wrappers.

### Circuit-breaker control-plane vs data-plane distinction (F08, 2026-06-02)
`shared/circuit_breaker.py` wraps the 16 Smartsheet network methods with a `guard` decorator. Two patterns a fresh CC session must know:

- **`circuit_breaker.bypass()` context manager:** wraps operations that MUST proceed even when the breaker is OPEN — specifically the ITS_Errors row write (`_smartsheet_log` in `error_log.py`) and the watchdog's own CRITICAL alert for a prolonged-open breaker. These are the control/forensic plane; bypassing them preserves observability during an outage. Pattern: `with circuit_breaker.bypass(): <smartsheet write>`.
- **Fail-OPEN everywhere (data-plane calls):** if the breaker JSON is missing, corrupt, or the lock times out, the breaker defaults to CLOSED. If the `enabled` flag is False in ITS_Config, `is_open()` returns False regardless of state. The circuit breaker is an **availability hardening** tool, NOT a security control.
- **F09 cap is fail-CLOSED at the ceiling:** `ALERTING_MAX_ALERTS_PER_HOUR` (default 15) blocks ONLY the Resend push leg — the ITS_Errors RECORD leg and Sentry leg always fire (Op Stds §3.1 push-vs-record separation). The cap is implemented as a reserved `_alerts_per_hour_window` key in `alert_dedupe.py`.
- **`first_opened_at` vs `opened_at`:** the breaker persists two timestamps. `opened_at` resets on every HALF_OPEN→OPEN re-trip. `first_opened_at` is PRESERVED across probe-failure re-opens, giving a monotonic "episode start" clock used by watchdog Check J (`_check_circuit_breaker_prolonged_open`) to page when the outage exceeds the prolonged-open threshold.

---

## 6. Tooling & Infrastructure

### CI gates
- `mypy = 0` enforced as **blocking** step (PR #31).
- `pytest -m integration` skipped by default; run against throwaway sandbox resources.
- Branch protection requires `test` context to pass.

### Smartsheet
- **5-workspace audience-separated topology** (Op Stds §23):
  - Customer-facing: Forefront Portfolio + Human Review
  - Operator-only: Operations (master DBs), Archive (closed projects), System (config/errors/queues)
- Principle: split by audience, not data type.
- Customer 2+: System is singleton across customers; Operations + Archive shared-vs-per-customer TBD; Portfolio + Human Review always per-customer.
- MCP gotchas: `get_columns`, `browse_folder`, `create_sheet_in_folder_from_template` with `include=["data"]` are reliable. `update_rows`/`get_report` may hit "No approval received" gate on first call — retry resolves.
- Reports MCP is read-only; `create_report` needs REST fallback.
- `get_sheet_summary` applies default sort by primary column (breaks header-row-context sheets); true native order requires `ss_api.py` via local execution.
- Filter operators: EQUAL, NOT_EQUAL, LESS_THAN/GREATER_THAN variants only — no CONTAINS/LIKE.

### Smartsheet REST via curl
- Write multi-line JSON payloads to files, use `-d @/path/to/file`. Inline shell quoting produces misleading 401/400 errors.
- **A 401 with `errorCode:2000` on POST is more likely a malformed payload than auth failure** if the same token succeeds on GET. PAT scope is uneven — platform behavior, not user error.

### Box
- OAuth 2.0 User Auth via `boxsdk` (NOT JWT — JWT path not licensed).
- Auth as `seths@evergreenmirror.com`.
- `store_tokens` Keychain callback is **CRITICAL** — refresh tokens rotate every use.
- Keychain keys: `ITS_BOX_CLIENT_ID`, `ITS_BOX_SECRET`, `ITS_BOX_REFRESH_TOKEN`.
- Setup: `setup_box_oauth.py` (one-time). Smoke test: `smoke_test_box.py`.

### MCP-gap REST-fallback pattern
When Smartsheet/Box/Graph MCP lacks a primitive:
1. Short-lived sandbox token + inline curl in `bash_tool`
2. Verify-after via OAuth MCP
3. Never persist token to file or env
4. Operator rotates token post-session

Applies across all three external systems.

### Exec-host worktree topology (observed 2026-05-28)
The operator uses per-task git worktrees alongside `~/its` (main). Observed: `~/its-sweep` (branch `f17-f04-docstring-sweep`) + `~/its-f16` (branch `f16-heartbeat-ping`) alongside `~/its` (main). Two hazards:
- **Branch-name collision:** a fresh session starting in `~/its` that tries to create a branch a reserved worktree already holds will fail. Check `git worktree list` before branching.
- **Live daemon runs `~/its` working tree:** `org.solutionsmith.its.safety-intake` executes `~/its/safety_reports/intake_poll.py` from disk every ~60s. Uncommitted edits in `~/its` go live on the next cycle. Do daemon/intake feature edits in a worktree, not the `~/its` main checkout.

### CC skills installed (PR #79, mattpocock/skills)
14 skills in `.agents/skills/` + `.claude/skills/` symlinks, pinned via `skills-lock.json`:

`caveman, diagnose, grill-me, grill-with-docs, handoff, improve-codebase-architecture, prototype, setup-matt-pocock-skills, tdd, to-issues, to-prd, triage, write-a-skill, zoom-out`

- Auto-recommend: `diagnose` (SDK-vs-Live), `tdd` (§30).
- Gated: `improve-codebase-architecture` (§14 preservation-over-refactor).
- `git-guardrails` planned as follow-up PR.

---

## 7. Orchestration Model

- **Chat = strategy, sequencing, paste-ready prompts with structured context blocks.**
- **CC = implementation.**
- Seth directs CC for code; chat handles planning and drafts CC briefs.
- Session documentation at close: `.docx` files following `ITS_[Topic]_[Date].docx` convention, output to `/mnt/user-data/outputs/`. `/mnt/project/` is read-only.
- Sequencing: alert-routing / deduplication before workstream consumer integration. Filler tasks (parser tech_debts, regex refinement) scheduled between critical-path items.

---

## 8. Current State Snapshot (as of last memory refresh)

### Recently landed
- Triple-fire CRITICAL alert path complete (PRs #11/#21/#22/#23)
- `shared/review_queue.py` + `shared/quarantine.py` wired (PRs #24/#25)
- mypy=0 enforced (PR #31)
- Alert deduplication shipped (PRs #42/#43/#44)
- Picklist Sync shipped + hardened (PRs #45–51)
- Box OAuth wired (PR #39, commit `2ce6ece`)
- Polling daemon + heartbeat (PRs #59/#60)
- Branch protection on main (2026-05-24, server-side)
- CC skills installed (PR #79)
- Actions version bumps (PR #81)
- Secret-exposure audit clean (2026-05-24)
- CC subagents + session-close convention (PRs #90–#94); codeql-fp-triager propose-only + structural dismiss block (#93)
- 2026-05-28 forensic audit: tag-breakout injection fix in `untrusted_content.wrap()` (#95) + LOW hygiene batch + audit doc (#96)
- Safety Portal pivot reconciled into exec repo (Task A, #99); HIGH-2 attachment-screening superseded for safety reports → reassigned to Email Triage (#98); NOT-WIRED `attachment_screening.py` stub deleted
- Cross-repo supersession drift-guard: session-close-maintainer check + doc_conventions note (Tasks B+D, #100)
- Op Stds v13 drift fix + doctrine manifest + doc-reconciliation agent (PRs #101/#103/#106/#107, 2026-05-28)
- `shared/state_io.py` atomic-write + sidecar-lock (PR #88, 2026-05-25; Phase 1.4 cluster PR 1)
- `shared/alert_dedupe.py` migrated onto `state_io` helpers — same-FD-flock pattern retired (PR #104, 2026-05-28; Phase 1.4 cluster PR 2)
- Phase 1.4 hardening sweep (PR #113, 2026-05-28): F17 (intake_poll watchdog Check C registration — `_write_watchdog_marker` added, live-confirmed on production daemon), F04 (`shared/keychain.set_secret` stdin correctness — `security -w` must be last arg, double-feed `value\nvalue\n`; live create→read→rotate→delete verified), watchdog docstring drift removed from 3 spots
- Network-capability allowlist + approval-attestation verification (F02+F22, exec PR #118, 2026-05-29)
- **FM v9 + Op Stds v14 (F07/F13 doctrine reconciliation, blueprint PR #23, 2026-05-29, squash `29000f1`):** Two doctrine reframes reconciling forensic-audit findings where doctrine over-promised security mechanisms. FM v8→v9: Invariant 2 Layer 5 (anomaly logging) reframed from "co-equal defense layer" → "post-hoc detection tripwire." Op Stds v13→v14: §1 kill switch reframed from implied "security control" → "operator-convenience suggested pause, NOT a security boundary" (fail-open by design; External Send Gate = real boundary). Code unchanged in both cases. Tags `foundation-mission-v9` + `operational-standards-v14` pushed on `29000f1`. Both docs' `last_verified_against` = exec-repo HEAD `64526a1`.
- CLAUDE.md trim 42.9KB→33.9KB (-21%) (exec PR #135, `b428d8c`, 2026-06-02) — removed stale/redundant prose under the size warning; content-reducing, not superseding.
- **Smartsheet circuit breaker + alerts-per-hour cap — F08+F09 (exec PRs #137+#138, `fc5d14f`/`699015b`, 2026-06-02):** `shared/circuit_breaker.py`: domain-agnostic `guard` decorator, single global persisted breaker (`~/its/state/circuit_breaker.json`), CLOSED→OPEN→HALF_OPEN→CLOSED/OPEN state machine, lock-free hot path with locked transition-writes, fail-open everywhere, `bypass()` for control/forensic-plane operations. 16 `smartsheet_client.py` network methods decorated; `SmartsheetCircuitOpenError(SmartsheetError)` subtype so existing catch blocks handle it unchanged. F09: `ALERTING_MAX_ALERTS_PER_HOUR=15` cap on the Resend push leg only (RECORD legs ITS_Errors+Sentry unaffected, per Op Stds §3.1). ITS_Errors bypass-wrapped so error recording survives open breaker. Daemons gained `CIRCUIT_OPEN` heartbeat status. §43 runbook at `docs/runbooks/circuit_breaker.md`. Watchdog Check J (prolonged-open alert, bypass-wrapped, MAINTENANCE-defer) + Check K (cap-window summary sweep). `first_opened_at` monotonic episode clock preserved across probe-failure re-opens. Deployed live 2026-06-02: imports clean, breaker CLOSED on new schema, hung intake_poll daemon (PID 292, ~88 min) cleared via `launchctl kickstart -k`, fresh cycle confirmed on new code. Three bugs caught by mandatory live smoke before merge (see §5 "Mocks pass but live fails").

### Bradley 1 (BBCHS 1)
- Template project, six sheets migrated, demo seeding complete.
- Next: UI work (conditional formatting, forms, filter views — Seth runs UI-only work himself) before cloning template to the other five projects.

### Open queue
- Phase 1.4 hardening cluster remaining: F16, F18, F03, F10 (F08+F09 landed PRs #137+#138; F17+F04 landed PR #113; F02+F22 landed PR #118)
- `person_tag` regex refinement (138 hits, likely FPs)
- Three `box_migration` parser tech_debts deferred: V/S vendor-sub parser, ISO date prefix, import-time hygiene wrap
- `shared/heartbeat.py` extraction (heartbeat helpers now copied verbatim across THREE consumers — intake_poll, weekly_send_poll, and intake_poll._write_watchdog_marker added in F17; 2nd-consumer extraction signal per Op Stds §14 still deferred)
- Graph API calls have no timeout — indefinite daemon hang possible during a Graph outage (surfaced by F08/F09 hung-daemon incident; tracked `docs/tech_debt.md`)
- `weekly_send_poll` has no `ITS_Daemon_Health` row — heartbeat writes are silently inert (tracked `docs/tech_debt.md`)
- `error_log.log(Severity.CRITICAL, …)` does not fire the triple-fire alert path — no Resend or Sentry (tracked `docs/tech_debt.md`)
- Update `docs/doctrine_manifest.yaml` in exec repo to reflect FM v9 + Op Stds v16 (blueprint bumps)
- Inline doctrine-pin normalization across `shared/*` + `safety_reports/*` (~50 sites, tracked `docs/tech_debt.md`)
- Remote branch `origin/f02-f22` not auto-deleted (worktree `gh pr merge --delete-branch` quirk); needs `gh api -X DELETE repos/SolutionSmith-debug/its/git/refs/heads/f02-f22`

### On the horizon
- Safety Portal build (blueprint `workstreams/safety-portal/` mission v1 + brief; Cloudflare Worker, intake.py portal-marker branches, HMAC-verified shim — all PLANNED, not built). Replaces PDF-email submission; the portal feeds the existing `intake.py` via the HMAC-verified shim (legacy PDF-email is the documented fallback). Attachment-screening (Invariant 2 Layer 6) is N/A for safety reports and reassigned to Email Triage.
- Email Triage workstream build — now carries Invariant 2 Layer 6 (attachment screening) per the portal pivot reassignment
- `fail_closed_until` kill-switch mechanism deferred from F07 (Q8 resolution) — currently fail-open by documented design; revisit in Phase 2+ when multi-operator scenario makes a true fail-closed window safe to add.
- DFR backfill and Portfolio Rollups Reports continued expansion.
- **Managed Agents Phase 3 gate** (V&R v7.2 + FM v9 + Op Stds §29): No agents in Phase 0/1/1.5/1.6. Phase 3 gate evaluates 4 candidates against capability-equivalence for Invariants 1 & 2:
  - Closeout Package Assembly
  - Schedule Digest
  - Dreaming
  - ITS Chat backend re-eval

  Framing: **"Python = deterministic plumbing, Agents = judgment-gaps between them."** Re-verify capability set at gate firing. Candidate list is planning input, not roadmap promise.
- Dedicated ITS Box user deferred to Phase 1.5.

---

## 9. Memory Restoration Notes

If a fresh chat-session needs to reload operational detail, the canonical source is:

- **`its-blueprint/references/memory-archive.md`** — append-only, loaded on demand. Covers M365 IDs + EXO gotcha, full Smartsheet topology + IDs, wiring history, 23-PR window, Bradley 1 migration + demo seeding, schema decisions, Picklist Sync (PRs #45–51), SDK-vs-Live class-of-bug, polling daemon + heartbeat, 2026-05-22 cascade.
- **`its-blueprint/doctrine/`** — Foundation Mission, V&R, Op Stds, Handover Plan, Excellence Roadmap. Version in frontmatter, not filename. Git tags mark canonical versions (e.g., `foundation-mission-v9`, `operational-standards-v14`).
- **`its-blueprint/workstreams/<slug>/{mission,brief}.md`** — 6 workstreams (safety-portal added 2026-05-25).
- **`its-blueprint/audits/`** — historical audits.

Linters: `scripts/lint_frontmatter.py` + `scripts/lint_crossrefs.py`, CI on every push.

Future operational detail extends `memory-archive.md` in-place via new `§G*` sections — no more `vN+1` doc proliferation.

---

## 10. Things This File Does NOT Cover

CC has these via filesystem and doesn't need them re-stated here:
- Full doctrine text (read from `its-blueprint/doctrine/`)
- Code (read from `~/its/`)
- Workstream missions and briefs (read from `its-blueprint/workstreams/`)
- Operational detail covered in `memory-archive.md`

This file is the **bridge** between chat-only context and what CC can reach on disk. If something belongs in a repo, move it there and remove it here.
