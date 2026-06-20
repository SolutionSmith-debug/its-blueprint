---
type: reference
status: canonical
workstream: null
last_verified: 2026-06-20
last_verified_against: 16ae6fb
---

# Claude Code Info Gap

**Purpose:** Context that lives only in chat memory / chat conversation and is NOT reachable from `~/its/` or `~/its-blueprint/` on a fresh Claude Code (CC) session. Drop this in project files so a chat-session can hand it to CC at spin-up, or so a fresh chat-session can re-orient quickly.

**Last refreshed:** 2026-06-20 (Safety Portal banner rebrand — ITS-crest + "Portal" dropped; live gold-script "Integrated Technical System" (Great Vibes); PRs #297–#300; final Worker f9222eb3 live. See §G41.)
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

### Candidate doctrine flags (pending Seth co-resolution; all **flags only**, no `doctrine/*` edit)
The Safety Portal as-built surfaced four candidate doctrine changes across two reconciliation passes. Doctrine is high-capability-class → flags only. Recorded in [safety-portal mission §Doctrine flags](../workstreams/safety-portal/mission.md) + the respective blueprint session logs.

**Raised 2026-06-10 (v4 reconciliation) — carried, still open:**
1. **Candidate Op Stds §50 — "privileged code-actuation gate."** Generalize Invariant 1's two-process model to *code* changes: cloud can only queue / the local Mac daemon is the sole actuator / state-machine-stamped / CI-gated synchronous merge / the operator toolchain holds the credentials. First instance = the Safety Portal form-publish pipeline (`publish_daemon.py`); the PO + Subcontracts document-generation workstreams will want the same shape.
2. **Form-maintenance principle promotion.** Promote *"operator + Claude maintained, with critical invariants enforced in code, not just documented"* to foundation doctrine, now that the portal realizes it mechanically.

**Raised 2026-06-12 (v5 reconciliation) — new, propose-only drafts in the [2026-06-12 v5 session log](../session-logs/2026-06-12_safety-portal-v5-reconciliation.md):**
3. **Op Stds §34 — canonical image-class screening sub-pattern.** Record the photo pipeline (magic → Pillow `verify()` / decompression-bomb cap / forced metadata-destroying re-encode → ClamAV-on-raw, config-gated) as the canonical §34 instantiation for a constrained image-attachment class, with screen-before-render + MALICIOUS-pages-and-refuses-before-filing as the load-bearing ordering. First instance = `photo_screen.py`.
4. **FM Invariant-2 Layer-6 wording touch (optional).** Layer 6 for safety reports moves "N/A — no attachments" → "image-constrained attachment class, §34-screened in code."

*The three v4-window exec-side flags (`../its/docs/tech_debt.md` lines 25/2117/2166 — PR-3 transport, PR-4 receipt-cache, PR-5 browse) are now **folded into mission v5** (§7, §16) — closed, not carried.*

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

### Op Stds is canonically v18 (as of 2026-06-07)
v12 added §§37–41 (CC Skills / Agent Guardrails / Per-Customer-Fork Security / Migration-Script PII / Actions Version-Bump). v13 added §42 (code-level self-documentation discipline). v14 (F07, PR #23, 2026-05-29) reframed §1 kill switch from implied "security control" to "operator-convenience suggested pause, NOT a security boundary" (fail-open by design; External Send Gate = real boundary). v15 added §43/§44 (successor-remediation documentation discipline + Tier-2 Claude-assisted repair path) with the Developer-Operator / Successor-Operator role split. v16 reframed §44's Tier-2 boundary as training-bounded co-resolution — no structural maintenance enforcement layer built or required. v17 added §23/§24 acknowledgment of `ITS — Safety Portal` as the 6th, standalone, approval-gated workspace (workspace-membership = approval authority). v18 added §§45–49: §45 find-or-create-not-strand (portal artifact auto-provision); §46 workspace-membership = approval authority (as-built F22 pattern); §47 Box version-on-conflict (deterministic re-upload → new version; distinct docs keep suffix); §48 CodeQL FP handling (per-alert dismissal + genuine-fix rule; dismiss-block hook is agent-scoped in `codeql-fp-triager.md`, not global `settings.json`); §49 preservation-for-future-workstream (extends §14). New content citing `Op Stds §N` should reference v18. Historical version references in older tech-debt entries and session logs are grandfathered.

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

### macOS `security add-generic-password` bare `-w` prompts the TTY in an interactive shell (2026-06-08)

When running `security add-generic-password -U -a "$USER" -s NAME -w` **without a value** in an interactive shell (e.g., Warp or zsh), the bare `-w` flag **prompts the controlling TTY** and **silently ignores any piped stdin**. If the operator types a value at the prompt and presses Enter twice, only those chars are stored — a 6-char garbage value was silently written this session, root-causing an early `portal_admin list-users` 401. The fix is the **argv form**: `-w VALUE` (value as the next argv token, not stdin). This is distinct from the existing `shared/keychain.set_secret()` trap below (that code uses stdin intentionally, but it is a subprocess with no TTY — stdin works correctly there). **Rule:** when manually seeding a Keychain entry at the shell, always use `security add-generic-password -U -a "$USER" -s NAME -w VALUE` — never the bare `-w` in a TTY.

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

### Worktree review subagent reads wrong tree (2026-06-03)
When running a review subagent (e.g., `code-review`) over a git worktree, the synthesizer subagent may re-verify findings by reading files from `~/its` (the main checkout) instead of the worktree absolute path. This produces false "phantom diff" reports — the subagent declares that committed changes do not exist in the file it read, because it read the wrong tree. **Pattern:** always pin ALL reads in a review subagent invocation to the worktree absolute path (e.g., `~/its-3b/`) and explicitly instruct the synthesizer that the committed branch diff is ground truth. The same session's Phase-3a review correctly caught a real blocker (title-only idempotency that would silently skip a wrong-typed column) — the Phase-3b review faltered on this tree-read issue. The fix is instruction discipline, not a code change.

### CodeQL `py/clear-text-logging-sensitive-data` — tuple-unpacking taint (PR #174, 2026-06-05)

When a function returns a tuple containing a secret alongside non-secrets (e.g., `(base_url, bearer_token, hmac_secret)`), CodeQL's taint analysis is imprecise at tuple positions — it can propagate the secret-taint onto co-returned non-secret fields. This triggered a HIGH alert on `_resolve_credentials` in `portal_client.py`: `bearer_token` secret-taint leaked onto `base_url`, which appeared in every logged submission field.

**Fix pattern:** use a **named-field dataclass** (e.g., `_PortalCreds`) instead of a tuple. CodeQL tracks taint per named field — the secret field stays isolated and does not contaminate co-returned fields. Also ensure the secret is consumed only in a verification-only code path and never enters the row dict that flows to logs or intake.

This is genuine hygiene, not a suppression. See also: §5 "CodeQL false positives" for the three dismiss-as-FP patterns (this is NOT a dismissal — it was a real taint path).

### CodeQL `py/clear-text-logging` on operator CLI — interprocedural taint through shared request fn (PR #185, 2026-06-07)

When a bearer token (sensitive source) is passed into a shared HTTP request function whose **return value** is printed (e.g., a JSON response body), CodeQL's interprocedural taint marks all prints of that return value as clear-text logging of the sensitive input — even if the return value contains no credential data. This pattern fires in `portal_admin.py` on `list-users` (prints the response JSON, not the token) and `_fail` (prints an error response body).

**This is a FALSE POSITIVE** — the response body is not the bearer token. Refactoring to stop echoing the raw `response` dict cleared 1 of 3 alerts; the remaining 2 are unfixable without contorting correct code.

**Resolution pattern:** operator runs `codeql-fp-triager` to generate the dismissal proposals (with quoted evidence), then applies them in the GitHub UI. CC is hook-blocked from dismissing CodeQL alerts. This is NOT one of the three auto-dismiss FP patterns in §5 above — `codeql-fp-triager` must evaluate it explicitly.

### `gh pr merge --auto` is rejected — repo has auto-merge DISABLED (2026-06-09)

`gh pr merge --auto` fails with a GraphQL `enablePullRequestAutoMerge` error on `SolutionSmith-debug/its`. The repo-level auto-merge setting is OFF. Any code path (automation, scripts, publish daemon) that previously relied on `--auto` is broken. The correct pattern is: poll `gh pr view <branch> --json mergeStateStatus` until `CLEAN`, then `gh pr merge --squash`. `--auto` also merges ASYNCHRONOUSLY — if post-merge steps (e.g., deploy) depend on the merge commit OID being available, `--auto` breaks ordering. See also: §6 "Publish daemon operates on the live `~/its` tree."

### Require up-to-date branch before merge — merge serialization (2026-06-07)

GitHub branch protection enforces "require branches to be up to date before merging." When multiple PRs are open in a batch, each branching off an older `main`, the first merge advances `main` and all sibling PRs are immediately BEHIND. Each must be updated (`gh pr update-branch <N>`) — which triggers a fresh CI run — before it can merge. This **serializes** the batch even if the PRs are independently correct.

**Pattern:** in a batch session, plan for the serialization overhead. After each merge, update the next PR's branch and wait for CI before merging. The update also re-runs CI, catching any interaction regressions between the just-merged PR and the queued one.

### Cloudflare `custom_domain` route disables `workers.dev` URL on deploy (2026-06-08)

Adding `routes: [{ pattern: "...", custom_domain: true }]` to `wrangler.jsonc` with no `workers_dev` key causes `wrangler deploy` to **disable the `*.workers.dev` URL** (Cloudflare warns "it will be disabled by default"). The old `workers.dev` URL then returns **error 1042** ("No Workers script was found for this host on workers.dev"). This stranded `portal_poll` and `portal_admin` which were still pointing at the `workers.dev` URL via `safety_reports.portal.worker_base_url` in ITS_Config — ~15 `portal_pending_fetch_failed` errors before the config value was repointed to the custom domain.

**Rule:** after any deploy that activates a custom domain, immediately verify/repoint every ITS_Config `worker_base_url` to the custom domain URL. If you need both `workers.dev` AND the custom domain to remain live, add `"workers_dev": true` to `wrangler.jsonc`.

### Circuit-breaker control-plane vs data-plane distinction (F08, 2026-06-02)
`shared/circuit_breaker.py` wraps the 16 Smartsheet network methods with a `guard` decorator. Two patterns a fresh CC session must know:

- **`circuit_breaker.bypass()` context manager:** wraps operations that MUST proceed even when the breaker is OPEN — specifically the ITS_Errors row write (`_smartsheet_log` in `error_log.py`) and the watchdog's own CRITICAL alert for a prolonged-open breaker. These are the control/forensic plane; bypassing them preserves observability during an outage. Pattern: `with circuit_breaker.bypass(): <smartsheet write>`.
- **Fail-OPEN everywhere (data-plane calls):** if the breaker JSON is missing, corrupt, or the lock times out, the breaker defaults to CLOSED. If the `enabled` flag is False in ITS_Config, `is_open()` returns False regardless of state. The circuit breaker is an **availability hardening** tool, NOT a security control.
- **F09 cap is fail-CLOSED at the ceiling:** `ALERTING_MAX_ALERTS_PER_HOUR` (default 15) blocks ONLY the Resend push leg — the ITS_Errors RECORD leg and Sentry leg always fire (Op Stds §3.1 push-vs-record separation). The cap is implemented as a reserved `_alerts_per_hour_window` key in `alert_dedupe.py`.
- **`first_opened_at` vs `opened_at`:** the breaker persists two timestamps. `opened_at` resets on every HALF_OPEN→OPEN re-trip. `first_opened_at` is PRESERVED across probe-failure re-opens, giving a monotonic "episode start" clock used by watchdog Check J (`_check_circuit_breaker_prolonged_open`) to page when the outage exceeds the prolonged-open threshold.

### Smartsheet ABSTRACT_DATETIME accepts naive timestamps; plain DATETIME still rejected (2026-06-09)

**Verified live (PR #245, WSR_human_review retype).** `ABSTRACT_DATETIME` (the Smartsheet "Date/Time" user type) CAN be created and live-retyped to via `update_column` — it is NOT the same as `DATETIME` (which remains rejected with errorCode 4000). Key behaviours confirmed live:

- `update_column` retypes an existing `DATE` column to `ABSTRACT_DATETIME` in-place; existing date-only cells coerce to midnight.
- `ABSTRACT_DATETIME` accepts a **naive** `YYYY-MM-DDTHH:MM:SS` string (stored and displayed literally).
- `ABSTRACT_DATETIME` **rejects** any timezone offset or `'Z'` suffix → errorCode 5536. Write naive wall-clock only.
- Write order matters when migrating a running system: land the naive-format writers BEFORE retyping the live column. A running daemon writing `+00:00` offset into a freshly-retyped ABSTRACT_DATETIME column → errorCode 5536 → CRITICAL double-send path.

**Applied to:** `WSR_human_review` (id `5035670127988612`) columns "Approved At" (col `7944658226548612`) and "Sent At" (col `5129908459442052`) live-retyped DATE → ABSTRACT_DATETIME (2026-06-09). `weekly_send.py` / `weekly_send_poll.py` write via `wsr_review.to_wsr_datetime()` (naive Pacific wall-clock).

**Operator preference:** Pacific local time (tz-naive ABSTRACT_DATETIME, no UTC). Represents what the approver/sender sees on their clock.

### Self-defeating CI test class: hardcoded inventory counts / live-catalog fixture names block new-form publishes (2026-06-09)

The publish daemon's own CI gate was self-defeating: tests in `test_form_archive.py`, `test_form_definitions.py`, `test_form_catalog.py`, and `publish.test.ts` contained **hardcoded form-count assertions and fixture identities that referenced the live catalog**. A legitimate new-form publish (which increments the count and adds a catalog entry) red-CI'd the test suite, blocking the daemon's `_wait_for_ci` step. The form publish gate stalled itself.

**Fix (PR #222/#228):** made all count assertions dynamic (`len(expected_paths)` instead of `== 11`); replaced live-catalog fixture names with reserved sentinels (e.g., `zztest-brand-new-type`); decoupled `test_publish_manifest.py` from the live `catalog.json` with a frozen in-memory fixture. A "brand-new parent type" Worker test uses the sentinel — not a real identity — so a real publish of a new parent can't collide.

**Class:** "test couples to live inventory/catalog state." Any test asserting a specific count of forms, a specific set of catalog entries, or a specific fixture identity must be written to stay correct as the catalog grows. Use dynamic counts (`len(all_defs)`) and reserved sentinel names for new-type/new-parent edge cases.

### Smartsheet and Box MCP connectors cannot delete sheets/folders (2026-06-17)

The Smartsheet MCP exposes `delete_rows` and column-level ops only — it has **no `delete_sheet`, `delete_folder`, or `delete_workspace` primitive**. The Box MCP has **no delete primitive at all**. Any cleanup or teardown operation that removes Smartsheet sheets/folders or Box folders must use the underlying Python SDK clients directly:

- **Smartsheet:** `smartsheet_client.get_client().Folders.delete_folder(folder_id)` (cascades to child sheets); `.Sheets.delete_sheet(sheet_id)` for individual sheets; `.Rows.delete_rows(sheet_id, row_ids)` for row cleanup.
- **Box:** `box_client.get_client().folder(folder_id).delete(recursive=True)` for trees; `.file(file_id).delete()` for individual files.

Pattern: write a NAME-GUARDED one-off SDK script (hard-coded allowlist of test-artifact names; refuses any live name not on the list) to avoid accidental production deletes.

### Portal-poll regeneration after artifact delete: one-shot vs loop (2026-06-17)

When deleting test artifacts while `portal_poll` is running, a portal folder can reappear immediately if the poller finishes an in-flight submission concurrently. The correct diagnosis:

1. `GET /api/internal/pending` → check count. If `count > 0`, the Worker has a queued submission that will recreate the artifact on the next drain cycle.
2. If `count = 0` after the reappearance, the regeneration was a **one-shot** (one submission raced the delete) — delete the regenerated artifact and re-verify.
3. If `count` stays > 0, the artifact will regenerate on every poll cycle. Either drain the queue first (allow the submission to file) or pause `portal_poll` via the `safety_reports.portal_poll.polling_enabled` ITS_Config gate before cleanup.

Do NOT pause the daemon preemptively — an empty pending count means the reappearance is one-shot and the daemon can continue running uninterrupted.

### All 3 daily-PDF name surfaces must be updated together (2026-06-17, PRs #289/#290)

The portal produces per-submission PDFs that appear in three distinct surfaces, each controlled by a DIFFERENT code path:

1. **Box file name** — `intake._file_portal_pdf` (Python; uses `project_name + work_date + form_type`).
2. **Smartsheet row attachment filename** — the `requests` call inside `intake.py` that writes the attachment to the week-sheet row (~line 2208; separate from the Box path).
3. **Worker `Content-Disposition` download name** — `GET /api/submissions/:uuid/pdf` in `safety_portal/worker/` (TypeScript; requires a `submissions LEFT JOIN jobs` to resolve `project_name`).

A naming fix that touches only surface 1 leaves surfaces 2 and 3 inconsistent. A live test submission after PR #289 revealed exactly this: Box got the new name, but the Smartsheet attachment and Worker download header still used the old `<date>-<form>.pdf` pattern. All 3 must change together (or at minimum the PR must audit all 3 surfaces before merging). Surface 3 requires joining `jobs` — cannot compute `project_name` from `submissions` alone.

### Smartsheet sheet-name 50-char cap (errorCode 1041) — latent gap in dynamic name builders (PR #283, 2026-06-13)

`create_sheet_in_folder` 400s with `errorCode 1041` ("must be 50 characters in length or less") when the sheet name exceeds 50 chars. In the test suite and integration tests, sheet names are always short (sandbox prefixes). The production name builder `week_sheet.week_sheet_name` composes `"<project> — week of <Sat>"` (fixed 21-char suffix + variable project name) and had **no length bound** — a 36-char project name yields a 57-char sheet name and the create fails.

**Fix:** `SHEET_NAME_MAX = 50` added to `week_sheet.py`; `week_sheet_name` now truncates the project prefix to `SHEET_NAME_MAX - len(suffix)` characters, preserving the suffix whole (it disambiguates weeks within the per-job folder). Names already ≤50 are byte-identical.

**Class:** any dynamic Smartsheet name builder (folder names are NOT subject to this cap; only `create_sheet_in_folder`). All other `create_sheet_in_folder` callers in this codebase use static string `SHEET_NAME` constants — those are short by construction. If a future workstream composes a sheet name from user-supplied data, add a `SHEET_NAME_MAX = 50` guard at the composition site.

**Secondary fix:** a portal submission that hits a permanent HTTP 400 was being caught as a generic (transient) `SmartsheetError` → status=`error` → the submission re-queued FOREVER, writing an ERROR row to ITS_Errors on every 60s cycle. Fix: new `SmartsheetValidationError(SmartsheetError)` subclass for HTTP 400 in BOTH SDK and REST translate paths; `intake.process_portal_submission` catches it BEFORE the generic `SmartsheetError` and drains it to Review Queue (`machine_reason="smartsheet_validation"`, `reason=STRUCTURED_OUTPUT_EDGE`). Permanent 400s must not loop. §43 runbook entry added to `safety_reports/README.md`.

### `shared/picklist_validation.py` REGISTRY must include every bounded-enum value a daemon writes (2026-06-09)

`shared/smartsheet_client.update_rows` calls `picklist_validation.validate_row` before constructing the API payload. Any value written to a PICKLIST column that is NOT in the in-code REGISTRY raises `PicklistViolationError` and blocks the write — **independently of whether the live Smartsheet column's `validation=false`**. This is correct by design (the registry enforces the code-side bounded enum even when Smartsheet hasn't been hardened to reject free-text).

The trap: adding a new bounded-enum value (e.g., a new `Send Status`) requires TWO changes: (1) the code logic that writes the new value AND (2) adding the value to `REGISTRY` in `shared/picklist_validation.py`. PR #247 added the `SENDING` send-status marker but initially omitted the registry entry. `SENDING` passed the live Smartsheet column (which has `validation=false`) but was **rejected by the local registry** → `PicklistViolationError` → the double-send guard was inert. Unit tests all passed because they mock `update_rows`. PR #253 fixed the registry.

**Pattern:** when adding any new value to a StrEnum that feeds a PICKLIST column, update `REGISTRY` in the same PR. The unit-test mock boundary means CI cannot catch registry omissions — only a live smoke will.

See also: §5 "Mocks pass but live fails" and the `feedback_mandatory-live-smoke` auto-memory entry.

---

## 6. Tooling & Infrastructure

### CI gates
- `mypy = 0` enforced as **blocking** step (PR #31). The `test` CI job runs mypy first (blocking), then pytest, then ruff. Run `mypy .` locally before opening a PR — a mypy error blocks merge the same way ruff/pytest do.
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

### Smartsheet API constraint: AUTO_NUMBER columns are UI-only
`type: AUTO_NUMBER` is rejected by the Smartsheet REST API with `errorCode 1008` whether the column is added at sheet creation or post-create. The only path is the Smartsheet UI (Insert Column → System → Auto-Number/Series). Pattern: run the API-doable schema steps in code, detect-or-instruct on the UI-only step, document in `docs/tech_debt.md`. This affects ITS_Active_Jobs `Job ID` column (Phase 3, pending operator UI action). The older `DATETIME` user-column constraint (errorCode 4000) is a separate limitation (use `DATE` for user-defined date columns). See `docs/tech_debt.md` for both entries.

### Smartsheet API constraint: MULTI_CONTACT_LIST loses external emails on read-back

**Verified live (PR #162, 2026-06-05).** `MULTI_CONTACT_LIST` columns holding external (non-org-member) email addresses read back as display names only — `"One, Two"` — via BOTH `cell.value` AND `cell.objectValue`. The email addresses are silently dropped by Smartsheet. A `CONTACT_LIST` (single contact) yields the email address via `cell.value` even for externals (`objectValue = {email, name}`), but holds only one address per cell. A real org-member contact also yields the email via `cell.value`.

**Implication for any ITS column storing arbitrary external recipient emails: use `TEXT` columns.** Store the email string directly. `CONTACT_LIST`/`MULTI_CONTACT_LIST` are only reliable when the contacts are org members.

**Column-type flip note:** an in-place `TEXT` → `CONTACT_LIST` column-type change via `PUT /columns/{id}` returns 200 and succeeds. Useful for after-the-fact type correction if an operator decides a column should be a contact picker, but the reverse path (CONTACT_LIST → TEXT) loses existing data.

**Applied in:** ITS_Active_Jobs `Safety Reports Contact Name`, `CC 1`–`CC 5` columns are TEXT (PR #162). `active_jobs.ActiveJob.cc_emails` / `safety_reports_contact_name` consumed from TEXT cells, not contact columns.

### Smartsheet REST via curl
- Write multi-line JSON payloads to files, use `-d @/path/to/file`. Inline shell quoting produces misleading 401/400 errors.
- **A 401 with `errorCode:2000` on POST is more likely a malformed payload than auth failure** if the same token succeeds on GET. PAT scope is uneven — platform behavior, not user error.

### Box
- OAuth 2.0 User Auth via `boxsdk` (NOT JWT — JWT path not licensed).
- Auth as `seths@evergreenmirror.com`.
- `store_tokens` Keychain callback is **CRITICAL** — refresh tokens rotate every use.
- Keychain keys: `ITS_BOX_CLIENT_ID`, `ITS_BOX_SECRET`, `ITS_BOX_REFRESH_TOKEN`.
- Setup: `setup_box_oauth.py` (one-time). Smoke test: `smoke_test_box.py`.

### Smartsheet API constraint: column format via attribute only, not dict constructor

**Verified live (PR #187, 2026-06-07).** Column **format string** (bold, color, font, size) must be assigned via the Python SDK model **attribute** (`column.format = "..."`). Passing it via the dict constructor (`smartsheet.models.Column({"format": "..."})`) silently drops the value — the API returns 200 but the column is left unformatted. Column **width** works via either path. Per-cell format (e.g., Status cell coloring) works via the `Cell` dict through the `_resolve_cells` `_formats` meta-key extension.

**Palette index source:** `GET /2.0/serverinfo` → `.formats.color` (array, 0-indexed, index → hex). Known values: 38 = `#237F2E` (dark green), 7 = `#E7F5E9` (light green), 18 = `#E5E5E5` (gray). `dateFormat` enum at `.formats.dateFormat`.

**`_formats` meta-key extension to `smartsheet_client._resolve_cells`:** additive extension (skip `_`-prefixed keys, attach per-cell format string). Rows that do not carry `_formats` are byte-identical to before. Enables per-cell Status coloring at write time — the substitute for UI-only conditional-format rules (those cannot be set via the API). See `shared/smartsheet_client.py` `_resolve_cells`.

### Box version-on-conflict: `update_contents_with_stream` (PR #186, 2026-06-07)

When uploading a Box file with the same name as an existing file in the folder, the SDK raises a 409 conflict. The correct resolution for a same-name overwrite is to upload a **new version** of the existing file via `client.file(existing_id).update_contents_with_stream(BytesIO(data))`. This preserves the stable file ID and maintains Box version history (Box is a SoR; version history is meaningful for compiled packets). Pattern implemented in `box_client.upload_bytes_or_new_version` + `_find_child_file`. The per-submission PDF path keeps the filename-suffix strategy (amendments = distinct docs); only the compiled-packet path uses version-on-conflict.

### Config-gate pattern for inert SoR-path changes (PR-K, 2026-06-07)

When a PR changes a filing path (e.g., switches from `project_routing` category subfolders to a new Box mirror tree), gate the new path on an ITS_Config value. An **unset config value → legacy path**: the new code is merged and deployed but remains inert until the operator activates it. This allows merging and pulling without immediately switching live SoR filing — the operator activates when ready. Pattern: `safety_reports.box.portal_root_folder_id` (empty/missing → legacy; set to the root folder ID → mirror-tree path). The gating check is a single `if cfg` branch in `intake._resolve_portal_box_folder` and `weekly_generate._ensure_its_week_folder`.

### `safety_naming.py` — shared naming source of truth (PR-K, 2026-06-07)

`safety_reports/safety_naming.py` is the single source of truth for all Box + Smartsheet naming in the safety portal: `job_folder_name(job_slug)`, `week_label(saturday)`, `CFG_BOX_PORTAL_ROOT` (the ITS_Config key name). Both `intake` and `weekly_generate` import from it; `week_sheet` delegates `_folder_name` / `week_sheet_name` to it. No duplication of the naming logic. When adding a new naming convention for the safety portal, extend `safety_naming.py` — do not inline the pattern in a consuming module.

### GitHub auto-merge DISABLED on `SolutionSmith-debug/its`

`gh pr merge --auto` is permanently rejected (`enablePullRequestAutoMerge` GraphQL error). This is a repo-level setting. Any automation that needs to merge after CI must poll `mergeStateStatus == CLEAN` via `gh pr view <branch> --json mergeStateStatus,statusCheckRollup` and then call `gh pr merge --squash` directly. The publish daemon (`safety_reports/publish_daemon.py`) does this via `_wait_for_ci`. Never re-add `--auto` without addressing both the setting constraint AND the async-merge-ordering problem (daemon needs the merge commit OID before deploying).

### Publish daemon operates on the live `~/its` tree

`safety_reports/publish_daemon.py` (launchd `org.solutionsmith.its.publish-daemon`, NOT loaded as of 2026-06-09) branches off `~/its` for each publish request (`publish/req-<N>-<identity>`), commits, and merges. A failed cycle can **strand `~/its` on the feature branch**. Recovery: `_reset_to_main()` runs at daemon startup (stash + checkout main + pull). If the daemon is not loaded, recover manually: `git -C ~/its checkout main && git pull`. The daemon never touches operator untracked files.

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

### Editable-install + PYTHONPATH worktree import resolution (confirmed 2026-06-03)
With `its` installed editable (`__editable__.its-0.1.0.pth`), setting `PYTHONPATH=<worktree>` DOES win over the editable finder. Worktree code and tests run correctly via `PYTHONPATH=<worktree> ~/its/.venv/bin/python -m pytest ...`. This resolves the open question in `docs/operations/worktree_discipline.md` about whether PYTHONPATH wins. It does — confirmed across three parallel worktrees (~/its-3a, ~/its-e1, ~/its-3b) in the 2026-06-03 session.

### CC skills installed (PR #79, mattpocock/skills)
14 skills in `.agents/skills/` + `.claude/skills/` symlinks, pinned via `skills-lock.json`:

`caveman, diagnose, grill-me, grill-with-docs, handoff, improve-codebase-architecture, prototype, setup-matt-pocock-skills, tdd, to-issues, to-prd, triage, write-a-skill, zoom-out`

- Auto-recommend: `diagnose` (SDK-vs-Live), `tdd` (§30).
- Gated: `improve-codebase-architecture` (§14 preservation-over-refactor).
- `git-guardrails` planned as follow-up PR.

### Safety Portal form definitions architecture (PR #164, 2026-06-05)

`safety_portal/forms/` is the single source of truth for the 11 form definitions. Structure:

- **`meta-schema.json`** — JSON-Schema contract that every form definition must validate against. Defines: `formId`, `title`, `description`, `version`, `variantOf` (for variant-parent relationship), and `sections[]`. Each section carries a `type` from one of 3 archetypes: `rows_with_signatures`, `grouped_checklist`, `sectioned_assessment`. All form definitions are validated against this at test time (`tests/test_forms_validation.py`, 49 tests).
- **11 form definitions:** `jha.json`, `equipment-preinspection.json`, `equipment-preinspection-crane.json`, `visitor.json`, `hsse.json`, `toolbox-talk-general.json`, `toolbox-talk-fire.json`, `toolbox-talk-ppe.json`, `toolbox-talk-excavation.json`, `toolbox-talk-ladders.json`. Faithfully transcribed from the 10 reference PDFs in `safety_portal/worker/public/forms/`.
- **Key item counts:** telehandler (`equipment-preinspection-crane.json`) has 64 checklist items; HSSE (`hsse.json`) has 11 categories; 5 toolbox-talk variants.
- **render = Option B** — the meta-schema + definitions are the single source of truth for BOTH the TS display renderer (Phase 4 PR 2) and the Python reportlab PDF renderer (Phase 4 PR 3). No AI step in either renderer.
- **Parent/variant model:** `variantOf` field on a definition + `Parent Form`/`Variant Tag` columns on ITS_Forms_Catalog. Variant resolution is data-driven; no code change needed to add a new variant.
- **ITS_Forms_Catalog v1 after PR #164:** 5 parents + 7 variants = 12 rows. Parents: jha, equipment-preinspection, hsse, visitor, toolbox-talk. Daily Site Safety removed (not a form-fill candidate); Visitor + HSS&E added. All marked Active.
- **Adding a Python dep note:** `reportlab` (Phase 4 PR 3) is a one-line `pyproject.toml` edit; CI installs via `pip install -e .[dev]`, no lockfile.

### Safety Portal transport: Python PULL model — code-complete (PRs #169/#173/#174, 2026-06-05)

The portal→intake transport is a **Python pull model** (operator-ratified 2026-06-05; supersedes the brief's email-shim design). The full Python side landed PRs #173–#177; `portal_poll.py` is GATED pending deploy.

- **Worker = send-free durable D1 queue.** Submission stored in D1 at submit time (cloud-always-on capture). Worker exposes two internal endpoints: `GET /api/internal/pending` (bearer auth) + `POST /api/internal/mark-filed` (receipt). No outbound email from the Worker.
- **`portal_poll.py` (to build)** — Mac-side daemon (modeled on `intake_poll`); polls the Worker over outbound HTTPS; verifies `X-ITS-Portal-HMAC` using `shared/portal_hmac.py`; hands each submission to `intake.py`; POSTs receipt.
- **`shared/portal_hmac.py`** — the cross-language HMAC verify contract; validated in PR #169 tests.
- **Capture cloud-always-on; filing on the Mac.** Submissions queue in D1 if the Mac sleeps; drain when it wakes. Filing (Smartsheet/Box write + reportlab render) stays on the Mac — a deliberate doctrine choice (no write-creds in the cloud).
- **Approval stays human-in-loop (F22):** `Approve for Scheduled Send` on `WSR_human_review`; `MODIFIED_BY` auto-stamps approver identity; `verify_approval` still validates the actor before send.
- **WSR_human_review** (`SHEET_WSR_HUMAN_REVIEW = 5035670127988612`) supersedes `WPR_Pending_Review` for the safety portal flow. One row per (job, week): compiled PDF, editable email body, recipients (TO = Safety Reports Contact Email, CC = CC 1–5 flattened), `Approve for Scheduled Send` + `Send Now`, auto-stamped Approved By/At. Built by PR #168.
- **Secrets at deploy:** Worker needs `HMAC_PAYLOAD_SECRET` + `PORTAL_INTERNAL_API_TOKEN` (via `wrangler secret put`); Mac Keychain mirrors as `ITS_PORTAL_HMAC_SECRET` + `ITS_PORTAL_INTERNAL_TOKEN`.

### Cloudflare / Safety Portal TS tree (PR #158, 2026-06-04)
`safety_portal/` is the TypeScript/Cloudflare workstream — a separate execution tree from the Python `safety_reports/` workstream. Key tooling facts:

- **Local dev:** `npm run dev` (Vite dev server for React SPA) and `wrangler dev --local` (Worker + D1 in-process). Neither requires a Cloudflare account token. D1 state is local-only (`--local` flag).
- **Deploy requires token:** `wrangler d1 create`, `wrangler d1 migrations apply` (remote), `wrangler secret put SESSION_SIGNING_SECRET`, `wrangler deploy` — all need `CLOUDFLARE_API_TOKEN` or `wrangler login`. Deferred to operator token step.
- **`nodejs_compat` flag required** — bcryptjs imports `node:crypto`. Flag is in `wrangler.toml`; without it the Worker fails to parse on deploy.
- **Topology RESOLVED → Cloudflare Workers + Static Assets** (a single Worker serves the SPA + same-origin `/api/*`). **NOT Cloudflare Pages** (Pages is in maintenance mode); any `*.pages.dev` reference is stale. Validation host `safety.evergreenmirror.com`; prod `evergreenrenewables.com`. Blueprint `brief.md` §11 updated (v2). **Requires Workers Paid (~$5/mo)** — see the bcryptjs cost-10 CPU-cap note below.
- **Local D1 state wipe:** concurrent `wrangler` processes in the same directory (e.g., a review subagent running `wrangler d1 migrations apply --local` or `npm run build`) can reset the local D1 DB mid-session. Fix: re-run `npm run db:migrate:local`. Not a code bug — the local DB file is wiped by `wrangler`'s in-process setup.
- **bcryptjs cost-10 CPU cap:** on Workers Free plan (10ms CPU/request), a bcrypt compare triggers Error 1102. Deploy on Paid plan OR swap to Web-Crypto PBKDF2-SHA-256. See `docs/tech_debt.md`.
- **CI gap:** no frontend typecheck/build CI step yet. `tsc --noEmit` + `npm run build` are manual-only. See `docs/tech_debt.md`.

### Safety Portal clean break + production cutover (2026-06-05)

- **Clean break — safety intake is portal-only at launch.** Evergreen cuts over all-at-once with **no integration of the legacy email-PDF system**; no Evergreen safety data flows the old path. `intake_poll.py` (the safety mailbox poller) is **retired/tombstoned** (PR #171 — raises `NotImplementedError`) and superseded by `portal_poll.py` (PLANNED) for safety; `WPR_Pending_Review` is **decommissioned** in favor of `WSR_human_review` (by-doc in code — the `weekly_*` scripts still reference it until the WSR rewire lands). **NOT an email teardown:** the shared email infra (`graph_client` / `untrusted_content` / `header_forgery`) and `intake.py`'s Graph `process_message` path are **preserved** for the committed Email Triage workstream. **The weekly product is LLM-free too** — a deterministic merge (`form_pdf.merge_pdfs` of the week's submitted-form PDFs + a fixed-template email body), not an Anthropic-drafted narrative (decision 2026-06-05; `weekly_generate.py` still calls Anthropic at `cf86a9e` — the deterministic rewire is in-flight). So the whole active safety-reports path has **no LLM**; Adversarial Layer 2 is N/A there (no LLM ingestion). LLM stays in scope for Email Triage / AI Employee only.
- **Production cutover DNS (applicable at cutover, not now):** Evergreen's site is **GoDaddy-hosted WordPress + Elementor**; the apex `evergreenrenewables.com` DNS + M365 email live on GoDaddy. **Evergreen has no Cloudflare account** — one is created fresh at cutover, **Evergreen-owned** (Daniel creates it). Do **not** migrate the apex zone; attach **only** `safety.evergreenrenewables.com` to Cloudflare, **likely via subdomain NS-delegation** at GoDaddy (delegate that label's NS records to Cloudflare), leaving WordPress + M365 email untouched. Exact subdomain-attach mechanism resolved at deploy prep — **likely path, not locked.**
- **Doctrine:** Op Stds bumped **v16 → v17** (§23/§24 now acknowledge the standalone `ITS — Safety Portal` workspace as a 6th, approval-gated workspace; tag `operational-standards-v17`). Blueprint mission/brief carry the transport + clean-break delta; see memory-archive §G22.

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
- **2026-06-02/03 batch — PRs #139–#150 (exec, all four-part-verify clean):** Graph-call timeout/weekly_send_poll health-row gaps registered (#139); Tier-A watchdog+reliability cluster: daemon-health self-provision A1 + graph timeouts A2 (#140), CI doctrine-drift + gitleaks C1+C2 (#142), A3 log-CRITICAL-pages full fix (#141), B1 F21 numeric bounds + anomaly-logger range check (#144), B2 startup token write-capability probe watchdog Check L (#145), C3 blueprint guard-symlink + C4 picklist-marker wiring (#146), launchd install.sh placeholder substitution fix (#147), D2 Invariant-2 Layer-5 reframe + F21 tech-debt close (#148), E1 BOX_PROJECT_FOLDERS → ITS_Project_Routing cutover (shared/project_routing.py + build/seed/flip order corrected) (#149), picklist-drift classify + additive ensure_picklist_options + Reason-drift live-fix (#150). Baseline after #150: pytest ~1200+ passed, mypy 0, ruff clean.
- **2026-06-03 Phase 3a/3b/E1 — PRs #151+#152+#153 (exec, all four-part-verify clean, main `9ff87ea`):** Phase 3a ADD — new `shared/smartsheet_client.create_picklist_column` helper + idempotent `scripts/migrations/add_dormant_picklist_columns.py`; ITS_Errors·Workstream + ITS_Quarantine·Disposition created live (#151). E1 flip — `SHEET_PROJECT_ROUTING = 3500842291253124` live in `shared/sheet_ids.py`; ITS_Project_Routing built + seeded; `get_folder_id` reading from sheet (E1 cutover LIVE after deploy) (#152). Phase 3b AUTOMATE — `--apply`/`--apply --commit` mode added to `scripts/audit_picklist_drift.py`; `audit --apply` ran 0/0 on clean registry (#153). (Session log PR #154.)
- **2026-06-03 Safety Portal config sheets — PR #155 (exec, four-part-verify clean, merge `141a573`):** Built the two Smartsheet config sheets, in folder "Safety Portal" (id `6663869084002180`) — `ITS_Active_Jobs` (id `6223950341164932`, 6 jobs seeded: bradley-1..rockford) and `ITS_Forms_Catalog` (id `423274885369732`; catalog since migrated to 5 parents + 7 variants — see PR #164). **[Location update: created in ITS — Operations, later MOVED to the standalone `ITS — Safety Portal` workspace during the 2026-06-04/05 sessions, IDs preserved — see memory-archive §G21. Note also: the portal reads its own D1, not Smartsheet — §G21.7.]** Two new `smartsheet_client` primitives: `find_folder_by_name_in_workspace` + `create_folder_in_workspace` (direct REST, `@_breaker_guard`, §42 docstrings). §30 live integration test (2 passed). §43 runbook at `docs/runbooks/safety_portal_config_sheets.md`. Note: job Addresses seeded BLANK (§4 forbids inventing them; PM fills manually before Work Location auto-fill goes live).
- **2026-06-03 Unifying forensic alignment & drift audit — PR #156 (exec, four-part-verify clean, merge `9e4b51b`):** Propose-only meta-audit at `docs/audits/2026-06-03_unifying-alignment-audit.md` (status: draft). Per-axis verdicts A–F; ranked drift register (NO Critical, no surviving High after adversarial verification); consolidated open-findings register replacing four prior-audit lists. Key corrections to live claims: gitleaks + doctrine-drift ARE in CI; 9 subagents + 4 hooks are RELATIVE symlinks from blueprint into ~/its (single source); watchdog has 11 operational checks (A,B,C,D,F,G,I,J,K,L,M), only E deferred — CLAUDE.md still says "6 of 7" (stale). Open findings surfaced: DR-D1/H1 guard-hook self-presence (fail-open if .claude symlink dangles; Check M only detects post-hoc); DR-C2 Layer 6 attachment screening entirely unbuilt (legacy PDF-email attachments to safety@ upload to Box unscanned); DR-E1/OPEN-1 `ops-stds-enforcer` agent pinned at "Op Stds v13", 3 majors behind v16, blind to §43/§44.
- **2026-06-04 Safety Portal Phase 2 — PR #158 (exec, four-part-verify clean, merge `fe615db`):** New `safety_portal/` tree — Cloudflare Worker (Hono router + TypeScript), Vite/React SPA (BRG/gold design system), Cloudflare D1 SQLite DB (users + form-submissions), bcryptjs auth, HMAC session-cookie middleware, SVG-vector signature pad (`signature_pad` library), 10 PDF reference forms committed to `public/forms/`. Locally validated end-to-end (wrangler dev --local + Playwright). Deploy deferred to operator Cloudflare token step (D1 create, remote migrations, secret put, wrangler deploy, custom domain). Zero Python touched. See §6 "Cloudflare / Safety Portal TS tree" for tooling notes.
- **Safety Portal Phase 3 — PR #160 (exec, four-part-verify clean, merge `827c374`):** Live Job-ID resolution replacing intake's legacy name-matching. New `shared/active_jobs.py` (Job-ID lookup against ITS_Active_Jobs, read-only, mirrors `project_routing` pattern) + `shared/safety_week.py` (Sat-to-Fri week rule, canonical Saturday-date key, Dec→Jan boundary correct). `resolve_project()` rewritten to key on portal payload `Job ID`; returns `ProjectResolution(project, reason)` typed tuple; `reason` in {`job_id_match`, `not_found`, `inactive`, `sheet_error`}. Legacy fuzzy-match RETIRED. Live additive migration on ITS_Active_Jobs: 4 contact columns (Stakeholder Name/Email/Phone, Safety Reports Contact Email) + rename `Job ID`→`Job Slug` (freeing title for the future AUTO_NUMBER column). AUTO_NUMBER `Job ID` column pending operator UI step (`errorCode 1008` blocks API creation — see §6 Smartsheet API constraint). §43 runbook shipped. D1 dropdown sync, portal forms, and submission pipeline deferred to Phase 4/5.
- **Safety Portal Phase 3 contacts amendment — PR #162 (exec, four-part-verify clean, merge `9e1ff9c`):** Added 6 TEXT columns to ITS_Active_Jobs — `Safety Reports Contact Name` + `CC 1`–`CC 5`. Augmented `shared/active_jobs.ActiveJob` dataclass with `cc_emails: list[str]` + `safety_reports_contact_name: str`. `_flatten_cc()` helper: comma-splits each CC 1–5 cell, deduplicates, skips malformed addresses with a WARN log. Email routing model: TO = Safety Reports Contact Email, CC = all flattened CC 1–5, greeting = Contact Name, Stakeholder = reference-only in packet body. Sending is Phase 5. CONTACT_LIST/MULTI_CONTACT_LIST columns NOT used for CC slots — external email read-back failure (see §6 "MULTI_CONTACT_LIST loses external emails" — this session's key live finding). Tech-debt entry added: CC recipients are operator-entered, not allowlist-validated (accepted risk; External Send Gate still required before any send).
- **Safety Portal Phase 4 PR 1 — form definitions foundation (PR #164, exec, four-part-verify clean, merge `940999e`):** `safety_portal/forms/meta-schema.json` (JSON-Schema contract, single source of truth for both renderers) + 11 form definitions (`jha`, `equipment-preinspection`, `equipment-preinspection-crane`, `visitor`, `hsse`, `toolbox-talk-*` ×5) faithfully transcribed from the 10 reference PDFs. Live ITS_Forms_Catalog parent/variant migration: 5 parents + 7 variants = 12 rows (Daily Site Safety OUT; Visitor + HSS&E IN). `jsonschema` Python dep added. `tests/test_forms_validation.py` (49 tests). §43 forms runbook at `docs/runbooks/safety_portal_forms.md`. See §6 "Safety Portal form definitions architecture" for the full architecture note.
- **Safety Portal mirror activation — operational session, NO new commits (exec HEAD stays `f3ad814`, 2026-06-08):** All three activation tracks completed — (a) admin route: migration 0006 applied to live D1 BEFORE redeploy, `PORTAL_ADMIN_API_TOKEN` Worker secret + `ITS_PORTAL_ADMIN_TOKEN` Keychain set byte-equal via `security add-generic-password -U -a "$USER" -s NAME -w VALUE` (gotcha: bare `-w` in interactive shell prompts TTY, ignores piped stdin — see §5); session revocation proven (disabled user 401s `revoked` on every endpoint). (b) Box mirror: root folder `ITS_Safety_Portal` (id `388017263015`) created, `safety_reports.box.portal_root_folder_id` set, `ROOT→job→week` filing active for both intake + weekly_generate. (c) Custom domain: `npm run deploy` → `safety.evergreenmirror.com` live — Cloudflare provisioned the custom_domain route, which **disabled the workers.dev URL** (`error 1042`), stranding portal_poll until `worker_base_url` was repointed to the custom domain. ITS_Config: `scheduled_send_local=MON 07:00`, `worker_base_url=https://safety.evergreenmirror.com`. ZZ Portal Proof (JOB-000008) set Active, recipient `seth@solutionsmith.org`. End-to-end submit→portal_poll→intake→Box→WSR-staged proven. **Real unattended timed send confirmed** Mon 07:12 PT: `safety@evergreenmirror.com` → `seth@solutionsmith.org`, SENT, Approved By/At stamped by poller, F22-verified, ITS_Errors forensic clean. `portal_poll` + `weekly_send_poll` both loaded + healthy. Three new tech-debt findings: (1) `validateUser` doesn't gate on `users.disabled` (defense-in-depth gap, not capability bypass); (2) custom_domain disables workers.dev (see §5 new trap); (3) `scheduled_send_local` not in `seed_its_config.py` + silent fail-open on malformed value. See memory-archive §G27.
- **Safety Portal Phase-2 Form Manager — FULLY BUILT (exec `b7bad5a` → `b736691`, 2026-06-09), PRs #203–#216 + #218, all four-part verified.** Components: (1) `safety_portal/catalog.json` + `catalog.schema.json` + CI consistency check (PR #203) — the active-set manifest gate, append-only; `registry.ts` reads it (PR #205). (2) `safety_reports/publish_manifest.py` (`apply_publish`) — pure transform: create/edit/add_version/delete/rollback; enforces identity uniqueness, monotonic version, variant-mixing rule, rollback target (PR #213). (3) B8 sectioned form editor UI (`FormEditor.tsx`, `FormsPage.tsx`, `editorModel.ts`, `editorValidation.ts`) + `PublishMonitor.tsx` (PR #211). (4) Publish pipeline: Worker send-free enqueue + `publishValidation.ts` (PR #209) + daemon queue endpoints (PR #212) + **privileged Mac actuator `safety_reports/publish_daemon.py`** (PR #214): claim → re-validate vs git HEAD → commit → CI render-smoke → `_wait_for_ci` polls `mergeStateStatus == CLEAN` → `gh pr merge --squash` → deploy → Box archive → stamp milestones; `_reset_to_main` Stage-0 recovery. (5) 3-renderer render-smoke net Python half (PR #208) + SPA jsdom half (PR #210). (6) Phase-2 8a real session revocation via `users.session_epoch` / D1 migration 0009 (PR #206). (7) Phase-2 8b admin 5-min sliding idle window (PR #215). (8) Parent-grouping guard at 3 layers: client editor + Worker enqueue + daemon `apply_publish` (PR #216). (9) No `--auto`: `gh pr merge --auto` rejected by repo (`enablePullRequestAutoMerge` disabled) — daemon polls CI itself then merges directly (PR #218). New launchd `org.solutionsmith.its.publish-daemon` (StartInterval 120, RunAtLoad false — NOT loaded, operator-gated; Tier-3 HIGH-capability). ITS_Config row 41: `safety_reports.publish_daemon.polling_enabled = true`. See memory-archive §G30 for full detail. Deferred: rollback UI picker, S1 per-item scale/comment authoring, integration test harness for the git/gh/wrangler subprocess chain.
- **Safety Portal publish-pipeline hardening + WSR timestamps (exec `b736691` → `2aa2061`, 2026-06-09 afternoon), PRs #236/#241/#242/#244/#245, all four-part verified.** (1) PR #236 (`8b29ee9`): `generate_form_archive.py` keys blank-PDF filenames by `definition_id` (not `form_name`) — same-named defs no longer silently overwrite each other; fixes a self-defeating-test failure that blocked every version-bump publish at `tested`. (2) PR #241 (`880c535`): `publish_daemon._regenerate_archive` now uses `sys.executable` instead of bare `"python"` — bare `python` is not in launchd's minimal PATH (macOS has only `python3`; live interpreter is `.venv/bin/python`); every publish was dying at `archived` with `FileNotFoundError`. (3) PR #242 (`ff249f4`): `PublishMonitor.tsx` Retire op now shows `Queued·Validated·Tested·Removed·Done` stepper (not `…Live·Archived` — nothing goes "live" on retire and the form is not removed from the Box archive). (4) PR #244 (`241cd64`): `apply_publish` rejects a redundant retire at validate stage ("is already retired"); `_commit_test_merge` gains a `git diff --cached --quiet` backstop for any no-op apply; `form_archive_out/` added to `.gitignore`. (5) PR #245 (`2aa2061`): WSR "Approved At" / "Sent At" now carry date+time as `ABSTRACT_DATETIME` (naive Pacific); new `wsr_review.to_wsr_datetime()` helper; `build_wsr_human_review_sheet.py` schema updated DATE→ABSTRACT_DATETIME; live columns retyped on the mirror (see §5 "Smartsheet ABSTRACT_DATETIME"). Exec HEAD now `2aa2061`. Publish daemon IS loaded (confirmed live).
- **Safety Portal Form Editor UX + draft caching (exec `2aa2061` → `8c1600d`, 2026-06-09 evening), PRs #249/#250, all four-part verified.** (1) PR #249 (`d5e9442`): two Form Editor UX fixes — (a) checklist "Response scale" now uses the existing `OptionsEditor` per-option rows (previously a controlled comma-separated `<input>` erased trailing commas and vanished mid-edit options); (b) `FormsPage.explainPublish` maps the 401 admin idle-timeout to "Session expired — sign in again" + maps bad_request; final fallback names code + HTTP status so a publish rejection is never contentless. (2) PR #250 (`8c1600d`): per-account localStorage draft cache (`its-portal-draft:v1:<username>`): autosave on every editor change; auto-restore with "Restored your unsaved draft" banner; Discard (confirm) + successful publish clear the slot; Cancel keeps it. In-memory localStorage stub for jsdom tests. **Live SPA deploy:** `npm run deploy` → `safety.evergreenmirror.com` version `71428941-53e5-46fc-8d8b-3570232d58d7` (bundle `index-B3GEp7P5.js`). Post-deploy liveness: SPA index + JS asset + `/forms` deep route all HTTP 200. Exec HEAD now `8c1600d`. See memory-archive §G32.
- **Safety Portal forensic audit + E2E validation (exec `8c1600d` → `298496d`, 2026-06-09 late evening), PRs #247/#248/#252/#253/#254/#255, all four-part verified.** (1) PR #247 (`f135305`): write-ahead SENDING marker in `weekly_send.py` — writes `Send Status=SENDING` before sending + reverts on error; closes double-send window from the prior race. (2) PR #248 (`586d308`): append-only compilations in `weekly_generate.py` — never overwrites existing Box PDF, WSR row, or week-sheet Rollup record (each now has a distinct guard path). (3) PR #252 (`689e310`): portal-poll fail-loud + resend timeout — stalled puller raises a loud CRITICAL instead of silently soft-failing; Resend alert-path timeout set explicitly so a Graph outage doesn't hang the poll cycle. (4) PR #253 (`65e5954`): add `SENDING` to `shared/picklist_validation.py` REGISTRY — the SENDING status value from #247 was missing from the code-side picklist registry; `update_rows` rejected it with `PicklistViolationError` (mocks never ran the registry); PR #247 was inert on the live mirror until this fix. (5) PR #254 (`886e65e`): publish create — `incident-report-v1` added to catalog via publish daemon (req 16). (6) PR #255 (`298496d`): publish edit — `incident-report` bumped to v2 (req 17). **Exec HEAD now `298496d`.** Playwright E2E smoke: created `incident-report` v1 + v2 publish, submitted a JHA, intake filed with errors=0, weekly_send_poll recovered DEGRADED→OK. **12-dimension forensic audit filed:** 9 deferred findings added to `docs/tech_debt.md` (M1/M2/M4/M5/M6/M7/M9 + ITS_Daemon_Health drift + half-applied-publishes backfill). See memory-archive §G33.
- **Safety Portal admin idle-timeout widening + bounded dirty-editor keep-alive (exec `298496d` → `23c04e6`, 2026-06-10), PR #258, four-part verified.** Widened admin idle window 5→30 min (`ADMIN_IDLE_S=1800` / `IDLE_MS=30*60*1000`; login + slide cookies updated). `useIdleLogout` gained a `paused` arg; `AdminApp` threads an `editing` flag from `FormsPage` (dirty draft open) and `AccountsPage` (login editor open); each page has an unmount-reset effect so a tab-switch cannot pin `editing=true` shell-wide. When paused, the hook adds a 240s `fetch /api/session` keep-alive to slide the server window while editing — but proactive logout fires in BOTH modes, so an abandoned dirty tab still dies at ≈30 min (closes the unbounded-session hole from adversarial review; `draftCache` preserves work regardless). Stale "5-minute" copy updated in worker/hook/pages/README. Two new test files: `FormsPage.editing.test.tsx` (unmount-reset coverage — fails if the effect is removed) + `useIdleLogout.test.ts` (6 cases). Worker deployed version `276322a3`. See memory-archive §G34.
- **Blueprint reconciliation — safety-portal mission→v4 + brief→v4 (exec `f3ad814..ab920bc`, PRs #190–#258, 2026-06-10), blueprint commit `429d377` (local, ahead of `origin/main`).** 62-commit window reconciled, brief-validator-checked. Mission: v3.2→v4 — added §13 (admin dashboard + account model: bcryptjs auth, D1 users/sessions, HMAC session cookie, 30-min idle window, per-session revocation via `session_epoch`, full `GET/POST /api/admin/*` endpoint tree); added §14 (form-publish pipeline as a second privileged code-actuation gate — cloud queues only, Mac daemon actuates with git + Cloudflare credentials, state-machine-stamped, CI-gated); §11 phase rows refreshed (pipeline live, `incident-report` create→v2→v3 operator-exercised, Part A/B/C live on mirror); §12 risk pointers (M1/M2/M4/M5/M6/M7). Brief: v3.1→v4 — absorbed Phase 8+9 (was pinned at Phase 7/`f3ad814`); added §3 Smartsheet surface map (ITS_Active_Jobs/ITS_Forms_Catalog/WSR_human_review/Orphaned Reports); added §17 (endpoint inventory + migrations 0007–0010 + gate map); added §18 (publish state machine + daemon chain); added §19 (Part A/B/C + send-leg hardening + bugfix chain). **Two doctrine flags raised** (no `doctrine/*` edit): (1) candidate Op Stds §50 "privileged code-actuation gate" — generalize Invariant 1 two-process model to code; (2) form-maintenance principle promotion (operator + Claude maintained, invariants enforced in code). Flags in mission §"Doctrine flags raised" + info-gap §3. **Auditor verdict:** accurate, no new drift, doctrine line held. M9 exec CLAUDE.md v16→v18 (one-line fix `CLAUDE.md:131`) remains open. See memory-archive §G35.
- **Safety Portal photo upload (PRs #271–#272, exec `ab920bc` → `5a979e2`, 2026-06-12), four-part verified.** PR-1 (#271, `fadd53f`): photo input type + Worker bounds gate (≤8 × ≤400 KB) + D1-inline base64 capture. PR-2 (#272, `5a979e2`): Mac-side §34 screening via `attachment_screening.py` + PDF embed (photos watermarked + appended to the submission PDF via `form_pdf`) + Box originals. D1-inline base64 transport today; R2 upgrade path recorded in ADR-0001 (deferred until field crews need > 4 full-res photos per submission).
- **Safety Portal PR-4 Part B — Crane & Rigging Critical Lift Plan form (PR #273, exec `01e9d13`, 2026-06-12), four-part verified.** New `crane-critical-lift-plan.json` definition published to `catalog.json`.
- **Safety Portal PR-4 Part A — request-driven canonical PDF download (PR #274, exec `814aec6`, 2026-06-12), four-part verified.** D1-chunked `filed_pdfs` cache; `pdf_requested`/`box_file_id`/`pdf_ready_at` columns; `portal_poll._service_pdf_requests` pass; submitted-page receipt. D1 schema superseded by PR-5 `pdf_requests` table; Part A submitter flow becomes first row in that table, behavior preserved exactly.
- **Safety Portal PR-3 — Graph upload-session for large weekly packets (PR #275, exec `13ef2bc`, 2026-06-12), four-part verified.** `graph_client.send_mail_large_attachment` (draft → createUploadSession → chunked PUT → send). `weekly_send` selects transport by packet size: ≤2.5 MB inline, >2.5 MB upload-session, >~150 MB HELD. ADR-0001, §43 runbook, tech-debt entries filed. Doctrine flag: mission v4→v5 delta (two-mode transport + HELD terminal) — fold with PR-4+PR-5.
- **Safety Portal PR-5 — Form Request browse + requester-bound PDF download (PR #276, exec `213d076`, 2026-06-12), four-part verified.** New `pdf_requests` table (migration 0012, PK `(submission_uuid, account)`, 24h window). Worker: `GET /api/filed` browse, `POST /api/request-pdfs`, `/status`+`/pdf` re-gated on live row, `/api/internal/pdf-requests` filtered. `FormRequestPage` SPA. Two-stage prune (strip payload 90d, delete 30d after job inactive). Unfiled rows never evicted. **Worker NOT yet deployed** (migration 0012 + redeploy pending — apply 0012 BEFORE deploy). Doctrine flag: mission v4→v5 delta (browse + requester-bound download + two-stage prune). **Exec HEAD now `213d076`.**
- **Safety Portal — 50-char sheet-name cap + permanent-400 drain (PR #283, exec `e75c5a7`, 2026-06-13), four-part verified.** Root cause: `week_sheet.week_sheet_name` composed `"<project> — week of <Sat>"` (21-char suffix + variable project name) with no length bound — a 36-char project name yields 57 chars, `create_sheet_in_folder` 400s `errorCode 1041`. Fix: `SHEET_NAME_MAX = 50` + project-prefix truncation (suffix preserved whole). New `SmartsheetValidationError(SmartsheetError)` subclass for HTTP 400 in BOTH SDK + REST translate paths. `intake.process_portal_submission` catches it before the generic `SmartsheetError` and drains to Review Queue (`machine_reason="smartsheet_validation"`, `reason=STRUCTURED_OUTPUT_EDGE`) — permanent 400s no longer loop. §43 runbook row added to `safety_reports/README.md`. **Exec HEAD now `e75c5a7`.**
- **Live test-artifact cleanup — Smartsheet + Box (2026-06-17, no git trace — live API ops only).** Deleted 4 test folders + their week sheets from ITS — Safety Portal workspace (Smartsheet), cleared all rows of ITS_Active_Jobs + WSR_human_review (sheets kept), and deleted 6 Box folders under `ITS_Safety_Portal` (root `388017263015`). Mechanism: the Smartsheet MCP has no delete-sheet/folder primitive and the Box MCP has no delete primitive — used underlying Python SDK clients directly via a NAME-GUARDED one-off script. A regen of one folder was a one-shot (in-flight portal_poll submission raced the delete); verified GET /api/internal/pending = 0 and deleted the regen. NOT deleted: the 2 Evergreen Portfolio Template workspaces (Demo Seed + Master) and Box migration strays — operator chose to keep. Residue items: (a) test-job entries in the portal D1 job dropdown persist (portal_poll.push_jobs refuses empty sync; clearing requires a Worker/D1 op); (b) historical filed test submissions + filed-PDF cache remain in D1. Both are tech-debt items.
- **Safety Portal job-prefixed PDF naming — all 3 surfaces (PRs #289/#290, exec `7510f7a`, 2026-06-17), four-part verified.** PR #289 (`88bc8ade`): daily per-submission PDF `<work_date>-<type>.pdf` → `<job>_<work_date>_<type>.pdf` in Box + weekly packet `Weekly Safety Report … <stamp>.pdf` → `<Job>_week of <Sat>_WSR.pdf` with _v2/_v3 bump on recompiles. PR #290 (`7510f7a`): fixed the two remaining surfaces the live test revealed — the Smartsheet week-sheet row attachment (~line 2208 in `intake.py`) and the Worker `GET /api/submissions/:uuid/pdf` `Content-Disposition` header (required `submissions LEFT JOIN jobs` for `project_name`). All 3 surfaces now emit `<job>_<date>_<form>.pdf`. Already-filed PDFs keep their old names. Worker deployed version `c56335d2`. **Exec HEAD now `7510f7a`.**
- **B5 doctrine cascade — Excellence Roadmap v4→v5 + URS Marine mission canonical (blueprint PR #46, squash `ad8f563`, annotated tag `excellence-roadmap-v5`; commit `1d38d38`; 2026-06-17).** Track 3.4 (NEW): platform fork-source = `its-portal-template` (domain-free substrate; single Worker + React SPA + D1 + form/checklist engine + DB-driven N-role/capability model + named PM-adapter seam + HMAC/pull transport). Per-customer `its-<customer>` repos fork from the template, NOT from a strip of full `its`; blueprint stays one artifact. Track 3.3 refined. Line-75 stale permissions reconcile note corrected to "Permissions v6." `references/customer-fork-setup-checklist.md` + `references/project-organization.md` (v4→v5 pointer) updated as companions. Four-lens adversarial diff-review + lint_frontmatter + lint_crossrefs (92 files) + check_doctrine_drift.py all clean. URS Marine `workstreams/urs-marine-portal/mission.md` flipped draft→canonical. Exec manifest sync: exec PR #293 (`2f70d91`), `doctrine_manifest.yaml` `blueprint_head`→`ad8f563`. **Exec HEAD now `2f70d91`. Blueprint HEAD now `f4ef4c9` (§G39 close)**. See memory-archive §G40.
- **Safety Portal banner rebrand — ITS-crest + "Portal" dropped; gold-script wordmark "Integrated Technical System" (PRs #297–#300, exec `16ae6fb`, 2026-06-20), four-part verified.** PR #297 (`467e776`): `AppHeader.tsx` — replaced baked PNG lockup (`public/its-portal-header.png`) with self-hosted **Great Vibes** woff2 font + CSS `background-clip:text` gold gradient (`.app-header__wordmark`). `great-vibes.woff2` + `great-vibes-OFL.txt` (SIL OFL) committed; old PNG removed. No CSP change needed (Worker `default-src 'self'` covers same-origin woff2). Adversarial 3-lens Workflow = all safe. PRs #298–#300 (`644577b`/`6c79030`/`16ae6fb`): three iterations on a perceived capital-T "clip" — line-height 1.5, then 1.9, then the real cross-browser fix `line-height:1.3 + padding-block:0.65em 0.45em`. RESOLUTION: cap-T "loop" look is an **intrinsic Great Vibes font feature, NOT a clip** — operator confirmed and accepted. Worker final: `f9222eb3`. **Exec HEAD now `16ae6fb`.** See memory-archive §G41. Operational lessons: (1) Worker SPA-fallback returns HTTP 200 text/html for deleted assets — verify removal by content-type, not status; (2) WebKit `-webkit-background-clip:text` paint box = font CONTENT box, ignores line-height leading (Chromium includes it) — use padding for clipped gradient glyphs; (3) Playwright MCP browser is Chromium — Safari-facing CSS must be operator-screenshot-verified. Auto-memory: `reference_worker-spa-fallback-200-on-deleted-asset` + `reference_webkit-background-clip-text-padding`.

### Bradley 1 (BBCHS 1)
- Template project, six sheets migrated, demo seeding complete.
- Next: UI work (conditional formatting, forms, filter views — Seth runs UI-only work himself) before cloning template to the other five projects.

### Open queue
- Phase 1.4 hardening cluster remaining: F16, F18, F03, F10 (F08+F09 landed PRs #137+#138; F17+F04 landed PR #113; F02+F22 landed PR #118)
- `person_tag` regex refinement (138 hits, likely FPs)
- Three `box_migration` parser tech_debts deferred: V/S vendor-sub parser, ISO date prefix, import-time hygiene wrap
- `shared/heartbeat.py` extraction (heartbeat helpers copied verbatim across THREE consumers — intake_poll, weekly_send_poll, intake_poll._write_watchdog_marker; 2nd-consumer extraction signal per Op Stds §14 still deferred)
- Graph API calls have no timeout — indefinite daemon hang possible during Graph outage (tracked `docs/tech_debt.md`)
- `weekly_send_poll` has no `ITS_Daemon_Health` row — heartbeat writes are silently inert (tracked `docs/tech_debt.md`)
- Update `docs/doctrine_manifest.yaml` in exec repo to reflect FM v9 + Op Stds v16 (blueprint bumps) — excellence-roadmap-v5 `blueprint_head` sync landed exec PR #293 (`2f70d91`); FM/Op Stds manifest entries may still lag
- Inline doctrine-pin normalization across `shared/*` + `safety_reports/*` (~50 sites, tracked `docs/tech_debt.md`)
- Remote branch `origin/f02-f22` not auto-deleted (worktree `gh pr merge --delete-branch` quirk); needs `gh api -X DELETE repos/SolutionSmith-debug/its/git/refs/heads/f02-f22`
- **Unloaded daemons:** picklist-sync, watchdog, weekly-generate plists on disk in `scripts/launchd/` but NOT installed. `portal_poll` + `weekly-send-poll` are LIVE (2026-06-08 mirror activation). `safety-intake` retired/tombstoned. Operator: `git -C ~/its pull` then `scripts/launchd/install.sh load` for remaining unloaded jobs.
- **~14 stale worktrees** from 2026-06-02/03 batch remain on disk (~/its-3a, ~/its-e1, ~/its-3b, plus earlier batch). Operator cleanup.
- **ITS_Active_Jobs · Address cells BLANK (6 rows)** — §4 forbids inventing addresses; office PM fills manually. Work Location auto-fill is empty until then. Tracked `docs/tech_debt.md`.
- **`scripts/lint_doc_conventions.py` missing `safety_portal` workstream tag** — `docs/doctrine_manifest.yaml` lists it but the lint script's canonical set does not. One-line fix; warn-only today. Tracked `docs/tech_debt.md`.
- **CLAUDE.md watchdog count stale** — says "6 of 7 checks operational"; actual count is 11 checks operational (A,B,C,D,F,G,I,J,K,L,M), only E deferred. Surfaced by PR #156 alignment audit.
- **`ops-stds-enforcer` agent pinned at "Op Stds v13"** (DR-E1/OPEN-1) — 3 majors behind v16, blind to §43/§44 successor-remediation discipline. Needs agent-file update. Tracked `docs/tech_debt.md`.
- **DR-D1/H1 guard-hook self-presence** — `.claude` hooks fail-open if the blueprint `.claude` symlink dangles; watchdog Check M only detects post-hoc, not preventively. No code change made this session; flagged in PR #156 audit.
- **DR-C2 Layer 6 attachment screening entirely unbuilt** — legacy PDF-email attachments to safety@ upload to Box unscanned. Documented as planned Phase 1.4; now surfaced explicitly in the alignment audit. Email Triage workstream carries this.
- **Safety Portal FULLY ACTIVATED on mirror (2026-06-08) — RESOLVED.** All three tracks done (admin tokens + migration 0006 + deploy / Box root `388017263015` / custom domain). `portal_poll` + `weekly_send_poll` live. End-to-end + real timed send confirmed. See memory-archive §G27.
- **WPR sheet + `Job Slug` column cleanup** — decommission-by-doc: no runtime reference remains; operator deletes the `WPR_Pending_Review` sheet + `Job Slug` column from `ITS_Active_Jobs` when convenient. Tracked in exec `docs/tech_debt.md`.
- **Safety Portal frontend CI gap** — no `tsc --noEmit` / `npm run build` CI step for the TS tree. See `docs/tech_debt.md`.
- **Safety Portal topology RESOLVED** — Cloudflare **Workers + Static Assets** (NOT Pages; Pages in maintenance mode). Blueprint `brief.md` §11 updated to v2. (Closes the prior "topology TBD / mission §11 assumed Pages" item.)
- **Safety Portal form-catalog mismatch RESOLVED** — PR #164 migrated ITS_Forms_Catalog to 5 parents + 7 variants (12 rows). Original 4-form mismatch entry closed.
- **WSR rewire + Phase 5/6/7 batch — COMPLETE and LIVE.** PRs #173–#177 (Python-side pull model) + PRs #178–#189 (deploy wiring + Phase 7 features) all merged (`f3ad814`); `portal_poll.py` loaded + active; full pipeline live-validated 2026-06-08. See memory-archive §G25 + §G26 + §G27.
- **Safety Portal Phase-2 Form Manager — BUILT + publish-pipeline hardened + Form Editor UX polished + forensic audit (2026-06-09, exec HEAD `298496d`) + admin idle-timeout hardening (2026-06-10, exec HEAD `23c04e6`).** See "Recently landed" above + memory-archive §G30 + §G31 + §G32 + §G33 + §G34. Deferred: rollback UI picker (frontend only — backend done), S1 per-item scale/comment authoring, integration test harness for the daemon's git/gh/wrangler subprocess chain, portal admin Retire UI gate (shows for already-retired forms; backend rejects clean), `README.md:111` doc-drift (weekly-send idempotency key), `form_archive_out/` temp-dir cleanup, draft-cache one-slot-per-account limitation, 9 forensic-audit findings in `docs/tech_debt.md`.
- **`~/its` is on `main` (`16ae6fb`)** — publish daemon loaded + healthy.
- **Orphan per-job Smartsheet folder from JOB-000013 incident** — "I don't know project name Montgomery" folder in `ITS — Safety Portal` workspace is empty and harmless; operator deletes via Smartsheet UI. See `docs/tech_debt.md`.
- **Portal D1 test-job dropdown not cleared** — test job entries remain in the Worker D1 `jobs` table (portal job dropdown) because `portal_poll.push_jobs` refuses to sync an empty `ITS_Active_Jobs` set. Clearing requires a direct D1 operation (e.g., `wrangler d1 execute ... --command "DELETE FROM jobs WHERE ..."` scoped to test slugs) or provisioning a real job before cleanup. See `docs/tech_debt.md`.
- **Historical D1 test submissions + filed-PDF cache remain** — past test submissions and their chunked `filed_pdfs` cache rows in the Worker D1 are still present after the 2026-06-17 Smartsheet + Box cleanup. These have no operator-visible footprint once the job entries are gone but consume D1 space and could surface in browse queries if the D1 is not pruned. See `docs/tech_debt.md`.
- **`compile_now_poll` launchd job NOT yet loaded** — on disk, operator activation required. Orphaned Reports is CONFIG-GATED OFF (`SHEET_ORPHANED_REPORTS=0`); operator activates: run `build_orphaned_reports_sheet.py` → flip ID → deploy.
- **WSR_human_review live columns retyped DATE → ABSTRACT_DATETIME** (mirror, 2026-06-09) — `298496d` code writes naive Pacific timestamps; PRODUCTION sheet built from updated builder gets ABSTRACT_DATETIME from creation.
- **CLAUDE.md Op Stds version claim stale** — CLAUDE.md asserts "v16 is the governing version" (lines ~28–29 and ~131); actual canonical version is v18 (`~/its-blueprint/doctrine/operational-standards.md` frontmatter + `docs/doctrine_manifest.yaml`). Load-bearing §§45–49 incl. §46 (F22) were added in v17/v18. Surfaced as forensic audit finding M9. Fix: one-line update to the parenthetical.
- **ITS_Daemon_Health observability drifted** — RETIRED `intake_poll` row present (frozen, pending operator delete, row `7461022174478212`); `publish_daemon`/`compile_now_poll`/`picklist_audit` have no rows; `portal_poll` Last Error Summary stale. See `docs/tech_debt.md` "ITS_Daemon_Health observability drift" entry.
- **Half-applied morning publishes** — reqs 11/12/13 Box archive PDFs never generated (bare-python bug, fixed by #241). One-time backfill needed. See `docs/tech_debt.md`.
- **PR-5 Worker NOT deployed** — migration 0012 + `npm run deploy` pending (operator step; apply migration BEFORE deploy). `FormRequestPage` + requester-bound PDF download not live until then. See `docs/tech_debt.md`.
- **Three PR-3/PR-4/PR-5 doctrine flags — FOLDED into mission v5 (2026-06-12, RESOLVED).** The (a) two-mode weekly-send transport, (b) filed-PDF receipt cache, and (c) Form Request browse + requester-bound download + two-stage prune deltas are now in `mission.md` v5 (§7, §15, §16). The v5 pass raised **two new** propose-only doctrine drafts instead (§34 image-class screening sub-pattern + FM Layer-6 wording — see §3). Exec-side flag headers at `../its/docs/tech_debt.md` lines 25/2117/2166 are closed by the exec sync PR.

### On the horizon
- **Safety Portal** — **PRs #271–#276 landed 2026-06-12 + PR #283 landed 2026-06-13 + PRs #285/#287 (PDF beautification + ITS Portal rebrand) + PRs #289/#290 (job-prefixed PDF naming — all 3 surfaces) landed 2026-06-17 + PRs #297–#300 (banner wordmark rebrand) landed 2026-06-20 (now exec HEAD `16ae6fb`). Blueprint mission reconciled v4 → v5 (2026-06-12, branch `doctrine/safety-portal-v5`) — the three PR-3/PR-4/PR-5 doctrine flags FOLDED.** Phase-2 Form Manager fully built; pipeline hardened; UX polished; forensic audit filed; admin idle-timeout hardened (2026-06-10). Phase-1 mirror-activated + live-validated (2026-06-08). Publish daemon + portal_poll + weekly_send_poll all live + healthy. `incident-report` v1/v2/v3 + `lifting-plan` (Crane & Rigging) + `photo-test` in catalog. `ZZ Portal Proof` (JOB-000008) Active. Open doctrine items: §50 code-actuation gate + form-maintenance principle (v4, carried) + the two new v5 propose-only drafts (§34 image-class + Layer-6 wording). Next: (0) **deploy PR-5 to mirror** (migration 0012 + `npm run deploy` — operator-run; STILL PENDING — `FormRequestPage` + requester-bound download not live until then); (1) ~~blueprint mission v4→v5 reconciliation~~ **DONE 2026-06-12**; (2) load `compile_now_poll` daemon; (3) activate Orphaned Reports; (4) resolve CLAUDE.md v16→v18 doctrine drift (M9); (5) resolve ITS_Daemon_Health drift; (6) one-time Box archive backfill for reqs 11/12/13; (7) Evergreen production cutover. ~~Banner rebrand DONE (PRs #297–#300, 2026-06-20; final Worker f9222eb3).~~ Browser-tab `<title>` + favicon still say "ITS Portal" — deliberate (out of banner scope, operator's call). See memory-archive §G27 (activation) + §G30 (Phase-2 build) + §G31 (pipeline hardening) + §G32 (UX) + §G33 (forensic audit + E2E validation) + §G34 (idle-timeout hardening) + §G35 (blueprint v4 reconciliation) + §G36 (photo/form-request program) + §G37 (blueprint v5 reconciliation) + §G41 (banner rebrand).
- **Excellence Roadmap v5 landed (blueprint PR #46, 2026-06-17).** Track 3.4 = `its-portal-template` as the platform fork-source (domain-free substrate). URS Marine mission is now canonical. Tag `excellence-roadmap-v5` on blueprint `ad8f563`. Exec manifest synced (PR #293, `2f70d91`). See memory-archive §G40. Companion cites in FM/V&R/Op Stds/Handover Authority blocks are intentionally deferred to each doc's next version bump (bounded staleness).
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

## 2026-06-08 addendum — admin-dashboard + hardening session (CC-environment facts)

- **Cloudflare Static Assets responses have IMMUTABLE headers.** `c.env.ASSETS.fetch()` responses can't be header-mutated in place (Hono `secureHeaders()` / `c.header()` throw); under `run_worker_first: true` that 500s the SPA document + every asset (only Hono-built `/api/*` survive). **Reconstruct** the response with a fresh mutable `Headers` copy instead. And `@cloudflare/vitest-pool-workers` does NOT serve the built assets, so the unit suite can't catch this — **verify asset/document paths with `wrangler dev` + curl**, not vitest. (Detail: [memory-archive §G29.2](memory-archive.md).)
- **CC can run `npm run deploy` (wrangler deploy) in auto-mode** — it deployed the Safety Portal hotfix + CSP-flip + beacon-fix this session. But a live **D1 migration** (`wrangler d1 migrations apply --remote`) was classifier-**BLOCKED** for CC (the operator ran it). So: Worker deploys are CC-doable in auto-mode; live D1 migrations are operator-run.
- **Background subagents were FS-sandboxed to `~/its` only** this session — they could not write sibling worktrees (`~/its-harden`, etc.) and correctly refused to edit the live `~/its` tree. Main-thread CC retained full sibling access. Do worktree-mutating work on the main thread, or probe FS write access before delegating it.

This file is the **bridge** between chat-only context and what CC can reach on disk. If something belongs in a repo, move it there and remove it here.
