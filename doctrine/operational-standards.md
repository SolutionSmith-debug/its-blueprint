---
type: doctrine
version: 12
status: canonical
last_verified: 2026-05-24
last_verified_against: 79eec73
supersedes: doctrine/operational-standards.md@v11
workstream: null
tags: [push-vs-record, picklist-hardening, attachment-screening, polling-daemon, sdk-vs-live, cc-tooling, fork-security, pii-logging, actions-version-discipline]
---

**ITS Operational Standards v12**

2026-05-24 — CC-Tooling + Fork-Security + PII-Logging Cluster Absorb

*Five new sections: §37 CC skills, §38 local agent guardrails, §39 per-customer-fork security setup, §40 migration-script PII asymmetry, §41 GitHub Actions version-bump discipline*

# Purpose

Cross-cutting operational patterns every ITS workstream uses. Each workstream brief and mission file references this doc rather than restating these patterns. When a pattern here changes, it changes for every workstream.

v11 is a full consolidation since v10 (2026-05-21 morning). It folds in the v10.1 overlay (Check G MAINTENANCE-defer) plus the 2026-05-21/22 cascade introducing polling-daemon doctrine (PRs #59 + #60), the pre-Customer-1 security hardening cluster (trusted-contacts + attachment screening + picklist hardening), and the in-repo tech_debt.md as canonical execution-layer log.

# What Changed in v11

- §1 Kill Switch — picklist-hardening forward reference added; Runtime Gate column in ITS_Daemon_Health flagged as future per-daemon switch.

- §2 Daily Watchdog — Check F (Mail.app rule silent disable) flagged for retirement; successor Check H (heartbeat staleness) referenced.

- §3.1 Push-vs-Record Separation — extended to operator visibility (heartbeat row is push; ITS_Errors remains record).

- §24 Sheet-ID Bootstrap — ITS_Daemon_Health + folder 04 — Daemons added (already present in shared/sheet_ids.py).

- §31 NEW — Polling-Daemon-as-Trigger-Primitive Pattern. Codifies emergent pattern (watchdog + picklist_sync + safety-intake all launchd-driven Python pollers).

- §32 NEW — Operator Visibility Surface. ITS_Daemon_Health schema + heartbeat write contract + ARCH-1/2/3 refinements.

- §33 NEW — Trusted-Contacts Sheet Pattern. Replaces ITS_Config JSON allowlists; exact-match + scope + header-forgery.

- §34 NEW — Attachment Screening Pipeline. Four-layer malware defense.

- §35 NEW — Bounded-Enum Picklist Convention. Smartsheet column-type discipline.

- §36 NEW — In-Repo Tech Debt Log. docs/tech_debt.md is canonical execution-layer log; planning-project tech debt scoped to owner-decision items.

- Sections §§4-22, 25-30 carry forward from v10/v10.1 with cross-reference refresh only.

# What Changed in v12

- §37 NEW — CC Skills Usage Convention. mattpocock/skills installed repo-local at `.agents/skills/` with `.claude/skills/` symlinks; 14-skill default install; skills-lock.json pins upstream revisions; auto-recommend list + gated list + not-in-default-install list.

- §38 NEW — Local Agent Guardrails. block-dangerous-git.sh PreToolUse hook with ITS carve-outs; allow plain `git push` and `branch -d` (canonical workflow); block destructive variants.

- §39 NEW — Per-Customer-Fork Security Setup. Mandatory hardening baseline for every customer fork: branch protection, fork-PR approval policy, secret scanning + push protection, Dependabot alerts (NOT auto-fixes), CodeQL default setup.

- §40 NEW — Migration-Script PII Logging Asymmetry. All `scripts/migrations/*` follow this pattern: dry-run path may print PII (operator review); live-write path strips PII (positional indices + system IDs only).

- §41 NEW — GitHub Actions Version-Bump Discipline. Verify latest tag via `gh api`, read release notes for breaking changes, never blanket-upgrade.

- §3.1 Push-vs-Record Separation — cross-reference added: server-side branch protection is the push-layer enforcement that complements the local block-dangerous-git.sh hook (per §38). Direct push to main is blocked at platform layer (server-side), not just at local-hook layer.

- §14 Preservation-over-refactor — cross-reference added: §37's gated-skills list (`improve-codebase-architecture`) requires explicit operator approval per §14. Don't invoke speculatively.

- §30 SDK-vs-Live Integration Test Discipline — cross-reference added: §37's auto-recommend for `tdd` skill applies to new `shared/*` SDK wrappers per §30.

- Sections §§4–22, 25–36 carry forward from v11 with cross-reference refresh only.

# §1 — Kill Switch

ITS_Config Smartsheet (sheet id 3072320166907780, see §24). Tall key/value layout. system.state setting reads ACTIVE / PAUSED / MAINTENANCE. Every Claude Code script reads it first via shared check_system_state() helper. PAUSED = scheduled scripts skip silently. MAINTENANCE = same, but watchdog does not alert. Anyone with edit access to the sheet can flip it.

Status: shared/kill_switch.py wired against ITS_Config via shared.smartsheet_client.get_setting (PR #9, 2026-05-18). Fail-open on three modes with distinguishable WARN messages routed through error_log.

## Picklist-Hardening Forward Reference

Pre-Customer-1, the system.state Value cell type should migrate from TEXT_NUMBER to PICKLIST with the enum {ACTIVE, PAUSED, MAINTENANCE}. Eliminates typo/case/whitespace fail-open trigger. Existing fail-open logic stays as belt-and-suspenders for the Smartsheet-unreachable case. See §35 for the system-wide picklist-hardening convention.

## Per-Daemon Runtime Gate (Future)

ITS_Daemon_Health Runtime Gate CHECKBOX column (planned) gives operators per-daemon on/off control from the same surface they use for monitoring. Today's per-daemon kill switches live as separate ITS_Config rows (e.g., safety_reports.intake.polling_enabled). Runtime Gate consolidates these into one operator surface. Bundle with shared/runner.py extraction at second polling-daemon consumer per §14.

# §2 — Daily Watchdog

launchd-scheduled Claude Code script (scripts/watchdog.py) runs daily at 7:00 AM ET. Verifies critical scheduled jobs ran in the last 24 hours, surfaces items past SLA, checks Anthropic spend trend. Silent if green; emails + SMS the operator if anything is off.

Status: 6 of 7 checks live: Check A (stale ITS_Review_Queue, PR #33), Check B (open CRITICALs in ITS_Errors, PR #33), Check C (scheduled jobs last-run markers, PR #36), Check D (14-day reviewer-chain forward scan, PR #36), Check F (Mail.app rule silent disable, PR #36; FLAGGED FOR RETIREMENT per below), Check G (alert dedupe summary sweep, PR #44; MAINTENANCE-defer shipped PR #52).

Check E (Anthropic spend trend) deferred to Phase 1.5 — architectural choice; sandbox spend signal-to-noise too low at $5-credit scale.

## Check F Retirement + Check H Successor

Check F polls safety@evergreenmirror.com mailbox idle hours as a proxy for Mail.app-rule health. Post-PR-#59, safety_reports is on a polling daemon and writes a heartbeat to ITS_Daemon_Health every 60 seconds. The mailbox-idle proxy is now redundant. Check H (successor) reads ITS_Daemon_Health for every Enabled=true daemon and flags rows where Last Heartbeat is older than 2 × Interval Seconds. Retire Check F when (a) Check H is operational and (b) no remaining workstream depends on Mail.app rules.

## MAINTENANCE Semantics (carried forward from v10.1)

All push-firing checks honor MAINTENANCE. Checks that emit via log() inherit suppression through severity-downgrade. Check G fires Resend directly and honors MAINTENANCE explicitly via alerts_suppressed parameter. State entries persist as expired+unsummarized; first post-MAINTENANCE sweep fires the deferred digest.

# §3 — Error Logging Pattern

ITS_Errors Smartsheet (sheet id 27291433258884, see §24). Captures every script failure via shared @its_error_log decorator. Severity: INFO / WARN / ERROR / CRITICAL.

Every CRITICAL-severity event fires three independent legs: Smartsheet row (Leg 1, PR #11), Resend operator email (Leg 2, PR #21/#22, subject to §3.2 dedupe), Sentry structured event (Leg 3, PR #23). All legs include Correlation_ID (PR #42) for cross-leg pivoting.

## §3.1 — Push-vs-Record Separation

Dedupe applies only to push, never to records. Resend = canonical push leg (subject to suppression). ITS_Errors + Sentry always write as forensic surfaces. This doctrine extends to operator visibility (per §32).

### Extended to Operator Visibility (NEW v11)

ITS_Daemon_Health is a push surface — each daemon's row overwrites every cycle. ITS_Errors remains the forensic record. The two surfaces serve different purposes: heartbeat row tells the operator "is this daemon alive right now"; ITS_Errors tells the operator "what failures happened, when, and how were they correlated." Heartbeat-write failures must NOT block daemon primary work (§32).

## §3.2 — Dedupe Implementation

Per v10.1 prose. Composite key (script_name, error_code). 60-min window from alerting.dedupe_window_minutes ITS_Config row. First CRITICAL per key per window fires Resend; events 2-N suppress Resend and increment counter; all events always write Smartsheet + Sentry.

Summary delivery via watchdog Check G (daily 7AM ET). During MAINTENANCE windows (§2), summary email firing defers; first post-MAINTENANCE sweep fires deferred digest. Phase-2 deletion proceeds during MAINTENANCE (no push surface). Preserves §3.1 doctrine.

# §§4-22 — Carry Forward From v10

Reviewer chain (§4), confidence scoring (§5), structured outputs (§6), sender allowlist (§7 — now extends per §33 trusted-contacts), untrusted-content tagging (§8), capability gating (§9), anomaly logging (§10), Python venv (§11), tool surface discipline (§12), diagnostic discipline (§13), preservation vs refactor (§14), reviewer chain (§15), ITS_Time_Off (§16), federal-holiday rule (§17), 14-day forward scan (§18), Smartsheet UI-only constraint (§19), remote access (§20), hardware lifecycle (§21), Box paths (§22) — all carry forward verbatim from v10 with no substantive change.

# §23 — Workspace Topology

Five-workspace audience-separated model. Customer-facing: Forefront Portfolio + Human Review. Operator-only: Operations (master DBs), Archive (closed projects), System (config/errors/queues/daemons).

Carries forward from v10 §23. No change.

# §24 — Sheet-ID Bootstrap

Workspace/folder/sheet ID inventory. Source of truth is shared/sheet_ids.py. v11 inventory refreshed:

- Workspaces: Forefront Portfolio 4129485730670468, Human Review 8561891980142468, Operations 7217130472007556, Archive 5528280611743620, System 680592632244100.

- System folders: 01—Config 164788727768964, 02—Logs 5231338308560772, 03—Queues 7201663145535364, 04—Daemons 2130046845511556 (NEW PR #59/#60).

- System sheets: ITS_Config 3072320166907780, Picklist_Sync_Config 7486553185013636, ITS_Errors 27291433258884, ITS_Quarantine 8687740798324612, ITS_Review_Queue 7243317526876036, ITS_Daemon_Health 4529351700729732 (NEW PR #59/#60).

- Active project folders: Bradley 1/2, Brimfield 1/2, Huntley, Rockford — see shared/sheet_ids.py FOLDER_PROJECT_* constants.

- Field Reports project subfolders: 6 per-project subfolders — see FOLDER_FIELD_REPORTS_* constants.

# §25-§30 — Carry Forward From v10

Per-workstream sheets (§25), reviewer chain configuration source (§26), Triple-Fire Failure Isolation (§27 — note: alert_dedupe.py is 4th consumer; shared-helper extraction threshold met but deferred per §14), mypy-in-CI (§28), Managed Agents architectural framing (§29 — "Python = deterministic plumbing, Agents = judgment-gaps between them"), SDK-vs-Live Integration Test Discipline (§30 — codified across PRs #47/#48/#49/#51; pytest -m integration against throwaway sandbox resources).

# §31 (NEW) — Polling-Daemon-as-Trigger-Primitive Pattern

Codifies the launchd-driven Python polling daemon as the canonical trigger primitive for all intake-bearing and scheduled workstreams. The pattern was emergent across watchdog (PR #36) and picklist_sync (PR #46) before being formally identified during the PR #59 safety-intake cutover; v11 §31 names it.

## Pattern

Every polling daemon is structurally identical:

- launchd plist in scripts/launchd/org.solutionsmith.its.<daemon>.plist — owns interval and process invocation.

- Python entry point at <workstream>/<daemon>.py — single poll cycle, exits after one pass.

- ITS_Config triplet per daemon: <workstream>.<daemon>.poll_interval_seconds, .source (mailbox/sheet/path), .polling_enabled (runtime gate).

- State files at ~/its/state/<daemon>_*.json for cross-cycle persistence (row-id caches, processed-message sets, cycle counters).

- Heartbeat write to ITS_Daemon_Health each cycle (§32).

- Conventions: plist label org.solutionsmith.its.*; log path ~/its/logs/launchd/<daemon>.{out,err}.log.

## Existing Daemons (Roster)

| **Daemon** | **Interval** | **Source** | **Heartbeat Status** |
| --- | --- | --- | --- |
| watchdog | Daily 7AM ET | Multi-source | Retrofit pending |
| picklist_sync | Hourly | Picklist_Sync_Config + master DBs | Retrofit pending |
| safety_reports.intake_poll | 60s | safety@evergreenmirror.com via Graph | LIVE (PR #60) |

## Future shared/runner.py Abstraction

At second polling-daemon consumer with heartbeat shape (i.e., after watchdog or picklist_sync retrofit), extract shared/runner.py per §14 preservation-over-refactor. Signature: run_loop(daemon_name, interval_provider, cycle_fn) where cycle_fn returns (status, items_count, err_summary, err_corr_id). Handles heartbeat write, sleep, kill_switch check, exception isolation.

# §32 (NEW) — Operator Visibility Surface

ITS_Daemon_Health sheet in System workspace / 04 — Daemons folder (sheet 4529351700729732, folder 2130046845511556). One row per daemon, update-in-place every cycle. Push surface per §3.1.

## Schema

12 columns per shared/sheet_ids.py DAEMON_HEALTH_COLUMNS dict. See ITS_Daemon_Health_Schema_2026-05-21.docx for full schema reference.

- Daemon Name (PRIMARY TEXT_NUMBER) — dotted-notation identifier.

- Workstream (PICKLIST: global, safety_reports, po_materials, subcontracts, email_triage, ai_employee).

- Enabled (CHECKBOX) — report-filter metadata only; daemon does NOT read this (ARCH-1).

- Interval Seconds (TEXT_NUMBER) — planning placeholder; runtime daemon reads its own ITS_Config row.

- Source ID (TEXT_NUMBER) — mailbox/sheet/path.

- Last Heartbeat (TEXT_NUMBER ISO 8601 UTC).

- Last Cycle Status (PICKLIST: OK, WARN, ERROR, SKIPPED, NEVER_RAN, STALE).

- Last Cycle Items Processed, Total Cycles (lifetime monotonic per ARCH-3).

- Last Error Summary, Last Error Correlation ID (links to ITS_Errors row), Notes.

## ARCH Refinements (PR #60)

ARCH-1: Enabled checkbox is report-filter metadata only. Canonical runtime gate is <workstream>.<daemon>.polling_enabled in ITS_Config. Two-switch matrix avoided by design.

ARCH-2: Row-id cache persists to ~/its/state/heartbeat_row_ids.json (launchd processes don't share memory). First write does find_row_by_primary + persists; subsequent reads from JSON; 404 invalidates and re-resolves.

ARCH-3: Total Cycles is lifetime monotonic, NOT daily reset. Avoids read-before-write API cost doubling. State file shape: {daemon_name: {row_id, total_cycles}}.

## Failure Isolation

Heartbeat write must NEVER block daemon primary work. Wrap in try/except, log to ITS_Errors with category 'daemon_health_write_failed' on failure, continue. Rate-limit retry should abandon after 5 seconds total.

# §33 (NEW) — Trusted-Contacts Sheet Pattern

Replaces ITS_Config JSON-list allowlists across all workstreams. ITS_Trusted_Contacts sheet in System workspace (location TBD — likely 01 — Config or new 05 — Trust folder). Operator-visible, audit-trail-supporting, scope-enforcing sender authorization.

## Schema (Approximate; Lock at Build Time)

- Email (PRIMARY) — canonical lowercased address. Exact-match key.

- Display Name — human reference; not used in trust decisions.

- Role (PICKLIST: PM, Safety, Forefront, Subcontractor, Vendor, Solution Smith, Internal, Other).

- Project Scope (multi-select PICKLIST: bradley_1, bradley_2, brimfield_1, brimfield_2, huntley, rockford, _all).

- Workstream Scope (multi-select PICKLIST: safety_reports, subcontracts, po_materials, email_triage, ai_employee, _all).

- Status (PICKLIST: ACTIVE, DISABLED, PENDING_VERIFICATION).

- Added By, Added Date, Last Verified, Notes.

## Trust Evaluation Logic

- Sender exact-matched against Trusted_Contacts. Status must be ACTIVE.

- No row → ITS_Quarantine with reason 'sender_not_trusted'.

- Row exists but Project Scope mismatched → ITS_Review_Queue with reason 'scope_mismatch'.

- Row exists and scope matches → proceed to pipeline.

## Header-Forgery Detection

Microsoft Graph API exposes authentication headers on every inbound message. Intake daemons check these BEFORE sender allowlist lookup:

- Parse internetMessageHeaders Authentication-Results for spf/dkim/dmarc results.

- Compare Return-Path header against From: header — mismatch is spoofing signal.

- Compare first Received hop source domain against From: domain — cross-domain inconsistency is spoofing signal.

- Any of {spf=fail, dkim=fail, dmarc=fail, Return-Path mismatch} → ITS_Quarantine with reason 'header_forgery_suspected'.

- Any of {spf=neutral, spf=softfail, dkim=none} on otherwise-trusted sender → ITS_Review_Queue.

## Migration Path

Pre-Customer-1: build ITS_Trusted_Contacts sheet; populate with anticipated Forefront/PM contacts; refactor safety_reports/intake.py to read from sheet instead of ITS_Config JSON; retire safety_reports.intake.allowed_senders ITS_Config row. All future workstream intakes inherit the same pattern.

# §34 (NEW) — Attachment Screening Pipeline

Four-layer defense against malicious attachments. Required before Customer 1 handover — opens external attack surface.

## Layer 1 — Static Signature Checks (cheap, runs first)

- File magic-number verification — header bytes must match claimed extension.

- File size sanity — DFR PDFs expected 50KB-50MB; extreme outliers flagged.

- Filename pattern matching — .pdf.exe, double extensions, RTL-override unicode.

## Layer 2 — Format-Aware Structural Inspection (cheap, runs second)

- PDFs: PyMuPDF reads object tree; flag /JavaScript, /JS, /EmbeddedFile, /Launch, /OpenAction keys.

- Office docs (.docx, .xlsx, .pptx): check for VBA macros, embedded OLE objects, external template references via python-docx/openpyxl.

- Extract embedded URLs from any format; flag external domains for human review.

## Layer 3 — ClamAV Antivirus (medium cost, runs third)

- ClamAV via Homebrew install + clamd daemon + pyclamd Python wrapper.

- Each attachment passes through clamd.scan_stream(bytes). Returns OK / FOUND <signature_name> / ERROR.

- EICAR test signature in test fixtures verifies pipeline health without real malware.

## Layer 4 — VirusTotal API (optional, defer to Phase 2+)

- Free tier: 4 req/min, 500/day. Submit hash, get cross-engine result.

- Network round-trip cost; rate-limited. Skip for Phase 1.5 launch.

## Disposition

- Any layer reports malicious → ITS_Quarantine (CRITICAL triple-fire); Box upload skipped; sender DISABLED in ITS_Trusted_Contacts pending operator review.

- Any layer reports suspicious-but-not-malicious → ITS_Review_Queue.

- All clean → pipeline continues.

# §35 (NEW) — Bounded-Enum Picklist Convention

Standing rule: any new Smartsheet column representing a finite-domain value MUST be created as PICKLIST or CHECKBOX, never TEXT_NUMBER. Free text only for genuinely open-ended content (names, descriptions, IDs, JSON payloads, error messages, free-form notes).

## Retrofit Audit (Pre-Customer-1)

Audit every existing Smartsheet column representing a finite-domain value across all ITS sheets. Convert from TEXT_NUMBER to PICKLIST or CHECKBOX. Targets include:

- ITS_Config — system.state {ACTIVE/PAUSED/MAINTENANCE}, all *.polling_enabled flags, any setting with an enumerated domain.

- ITS_Daemon_Health — verified already PICKLIST for Workstream and Last Cycle Status; future Runtime Gate should be CHECKBOX.

- ITS_Errors — Severity {INFO/WARN/ERROR/CRITICAL}, Workstream, status fields.

- ITS_Review_Queue — Status enum, Workstream, urgency tiers, reviewer-chain selectors.

- ITS_Quarantine — quarantine reason enum, disposition {release/delete/escalate}, Workstream.

- Per-project sheets (Daily Reports, Weekly Rollups) and future workstream sheets — status fields, category fields, anywhere a code reader expects a known value.

## Implementation Notes

Smartsheet supports column-type changes on existing columns; existing values preserved if compatible. Smartsheet MCP cannot perform the change (no API primitive); operator UI required. Approximately 30 seconds per column conversion.

kill_switch.py fail-open logic stays as belt-and-suspenders for Smartsheet-unreachable case. Picklist enforcement eliminates typo/case/whitespace as the trigger, not the Smartsheet-unreachable trigger.

# §36 (NEW) — In-Repo Tech Debt Log

docs/tech_debt.md is the canonical execution-layer tech debt log. Planning-project tech-debt scope is limited to owner-decision items only.

## Convention

- Add an entry when a session deliberately chooses preservation-over-refactor (§14), discovers an external-API constraint that forced a workaround, or defers a non-trivial cleanup.

- Mark CLOSED when resolved in a commit. Preserve the entry with resolution detail rather than deleting (history is cheap, context is expensive).

- Each entry: descriptive title with [OPEN|CLOSED|PARTIALLY MITIGATED] tag + ISO date + rationale + workaround + revisit-when criterion + resolution detail if closed.

## Current State

39 entries as of 2026-05-22. Mix of closed/open/partially-mitigated. Notable open items: anomaly_logger SUSPICIOUS_FIELD_PATTERNS FP risk, R2 Watchdog Check E (Phase 1.5 deferral), Picklist_Sync_Config config/state mix, Smartsheet MULTI_PICKLIST round-trip gotcha, safety_reports week-folder race condition, Daily Reports schema gap (no Box Link column).

# §37 (NEW) — CC Skills Usage Convention

mattpocock/skills installed repo-local in every ITS execution repo. Skills physically live at `.agents/skills/` (universal multi-agent location); `.claude/skills/` is a symlink pointing at it. `.agents/skills/` is the source of truth. `skills-lock.json` at repo root pins upstream revisions for reproducible installs.

Customer-fork-portable: when ITS forks for Customer 2+, skills come with the code.

## Default Install (14 skills)

caveman, diagnose, grill-me, grill-with-docs, handoff, improve-codebase-architecture, prototype, setup-matt-pocock-skills, tdd, to-issues, to-prd, triage, write-a-skill, zoom-out.

Install command (one-time per fork): `npx skills@latest add mattpocock/skills`. Adding skills outside the default set requires `--full-depth` flag for `misc/` subdirectory skills (e.g., `git-guardrails-claude-code` per §38).

## Auto-Recommend (trigger-driven)

CC should suggest invoking these skills when their triggers fire:

- `diagnose` — any bug investigation that touches an SDK boundary (Smartsheet, Box, Graph). The reproduce → minimise → hypothesise → instrument → fix → regression-test loop is the standard response to the SDK-vs-Live class of bug (§30).
- `tdd` — any new `shared/*` SDK wrapper with create/update/delete on typed columns/rows (§30 integration discipline).

## Gated (require operator approval)

These skills conflict with established conventions and must not be invoked speculatively:

- `improve-codebase-architecture` — conflicts with §14 preservation-over-refactor. Operator must confirm the refactor target meets the ≥4 real reuse cases threshold before invoking.
- `request-refactor-plan` — same §14 constraint when installed.

## Safe to Invoke On Demand

grill-me, grill-with-docs, to-prd, to-issues, handoff, caveman, zoom-out, triage, prototype, write-a-skill, setup-matt-pocock-skills.

## Not in Default Install (available, install on demand)

`request-refactor-plan`, `qa`, `git-guardrails-claude-code` (§38). Skills not in `mattpocock/skills` at all (e.g., `migrate-to-shoehorn` cited from search results) are flagged as nonexistent rather than silently ignored.

# §38 (NEW) — Local Agent Guardrails

block-dangerous-git.sh PreToolUse hook installed via `mattpocock/skills` git-guardrails-claude-code skill. Wired via `.claude/settings.json` (committed; distinct from gitignored `.claude/settings.local.json`).

Hook only blocks the model-agent's Bash tool calls. Operator shell is unaffected. Recovery operations (e.g., `git branch -D` on a force-delete-needed branch) are performed manually by the operator in their own shell.

## Allow-List (carved out from defaults)

These commands are allowed even when their pattern overlaps with destructive operations:

- `git push` (any branch, non-force) — required for canonical PR workflow
- `git branch -d` (safe-delete; lowercase d) — canonical post-merge branch cleanup
- `gh pr merge --squash --delete-branch` — canonical merge command (composite of the above)
- `gh pr view` and all read-only `gh` commands — required for four-part verification (per existing PR-merge discipline)

## Block-List

- `git push --force`, `git push -f` — force-push
- `git push origin --delete <branch>` — remote branch deletion
- `git push origin main` (direct) — defended at server-side branch protection layer; local hook does NOT differentiate `push origin main` from `push origin feature-branch`. Direct-push-to-main enforcement lives at the GitHub branch protection layer per §39
- `reset --hard` — local history destruction
- `clean -f`, `clean -fd` — local working-tree destruction
- `branch -D` (force-delete; uppercase D) — operator-only via manual shell
- `checkout .`, `restore .` — uncommitted-changes destruction

## Defense Complement

The local hook protects the operator's machine from agent error. Server-side GitHub branch protection (per §39) protects the repo from any contributor, on any machine. Direct push to `main` is blocked at both layers.

# §39 (NEW) — Per-Customer-Fork Security Setup

Mandatory security-hardening baseline for every customer fork. Establishes the minimum posture that all ITS forks (Evergreen + future Customer 2+) inherit. The operational checklist with verbatim `gh api` commands lives at `references/customer-fork-setup-checklist.md`.

## Baseline Configuration

### Branch Protection on main

- Required status checks: `strict=true`, `contexts=["test"]` (or the canonical CI job name for the fork), GitHub Actions app
- `required_linear_history=true` (squash-only merges)
- `allow_force_pushes=false`
- `allow_deletions=false`
- `required_conversation_resolution=true`
- `enforce_admins=false` (emergency lever preserved for solo + CC operation; tighten to `true` for multi-contributor forks)
- `required_pull_request_reviews=null` (solo + CC default; tighten when adding human reviewers)

### Fork-PR Approval Policy (public forks only)

`approval_policy=all_external_contributors` (strongest). Tightens default `first_time_contributors` to require operator approval before CI runs on any PR from a non-collaborator, regardless of contributor history.

### Secret Scanning

- `secret_scanning.status=enabled`
- `secret_scanning_push_protection.status=enabled` — blocks pushes containing detected secret patterns at the platform layer (not just alerts post-push)

### Dependabot Alerts

- Alerts: ENABLED (`PUT /vulnerability-alerts`)
- Automated-security-fixes: NOT ENABLED — auto-PR opens would conflict with the four-part-verify + manual-merge workflow. Operator reviews + lands dependency bumps via §41 discipline.

### CodeQL Default Setup

- `code-scanning/default-setup` with `state=configured`, `query_suite=default`
- Languages auto-detected (typically `python` + `actions` for ITS forks)
- Weekly scan schedule

## Operator-Only Audit (Not API-Automatable)

- Fine-grained Personal Access Token inventory — `Settings → Developer settings → Personal access tokens → Fine-grained tokens`. Verify scope is per-repo not All-repositories; verify expiration dates set; revoke unused.
- Classic Personal Access Token inventory — same UI, classic tab. Most-likely place for forgotten tokens from `gh auth login` or one-off scripts.

## Architectural Defense (not configuration)

All secrets MUST live in macOS Keychain. `shared/keychain.py` is the canonical interface. `.gitignore` covers `.env*`, `*_secret*`, `*credentials*`, `*.token`, `*.pem`, `*.key`. This eliminates the design pathway for secrets to enter the repo, making the configuration items above defense-in-depth around an already-secure baseline.

## Verification Pattern

After hardening, run gitleaks against full history (`gitleaks detect --source . --log-opts="--all" --redact -v`). Zero findings + zero CI/env/Dependabot secrets + zero workflow `secrets.*` references = clean baseline. Re-run periodically after any new `shared/*` SDK wrapper merges.

# §40 (NEW) — Migration-Script PII Logging Asymmetry

Applies to all `scripts/migrations/*` and any script that handles operator-known PII (email addresses, contact names, customer details).

## Asymmetry Rule

- **Dry-run path** — PII permitted in logs. Dry-run output is review material: the operator needs to see emails/names to verify what WILL be added before confirming. Stripping PII from dry-run defeats the review purpose.

- **Live-write path** — PII stripped. The write IS the side effect. Logging confirmation needs only positional indices + system IDs (Smartsheet row IDs, sheet IDs). Logging emails/names in the live-write path puts PII in terminal scrollback, screen-share recordings, and shell history without operational benefit.

## Canonical Example (PR #84)

Live-write before:

```python
print(f"[ok] added: {r['Email']} (row {new_row.id})")
```

Live-write after:

```python
print(f"[ok] added row {i+1}/{total} (smartsheet row_id={new_row.id})")
```

Dry-run path unchanged (still prints `r['Email']`).

## Rationale

Per-customer-template scripts run on multiple operator terminals over the customer-fork lifecycle. The same script that runs at Evergreen will run at Customer 2, possibly during screen-shares, customer hand-overs, or demo recordings. Code-as-documentation also matters on public repos — the established pattern for `scripts/migrations/*` is the wrong norm to set as "logs PII to stdout."

# §41 (NEW) — GitHub Actions Version-Bump Discipline

Applies to every `.github/workflows/*.yml` action version bump.

## Procedure

1. Verify the latest stable tag via API:

   ```bash
   gh api repos/<owner>/<repo>/releases/latest --jq '.tag_name'
   ```

   Examples: `actions/checkout`, `actions/setup-python`, `actions/cache`.

2. Read the release notes for breaking changes:

   ```bash
   gh release view <tag> --repo <owner>/<repo>
   ```

   Pay attention to: new required inputs, removed flags, behavior changes, runtime version (Node.js 20 vs 24) requirements, default-value changes.

3. If breaking changes affect ITS workflows → STOP. Surface the breaking change to operator. Do not force-through.

4. If clean → bump in a focused PR. One bump per PR family (e.g., bump both `checkout` and `setup-python` in one PR if both are deprecated together; do NOT bundle with unrelated workflow changes).

5. Four-part PR-landed verify per execution-repo discipline.

## Anti-Patterns

- DO NOT blanket-upgrade ("bump everything to latest"). Each action's latest tag is a separate decision.
- DO NOT bump from a deprecation annotation without reading the release notes. The annotation says "deprecated"; the notes say "what changed."
- DO NOT bump in the same PR as unrelated workflow edits. Isolate so a CI failure is unambiguously attributable.

## Canonical Example (PR #81)

`actions/checkout` @v4 → @v6.0.2 and `actions/setup-python` @v5 → @v6.2.0 in a single PR. Both bumps verified via `gh api releases/latest`; release notes read for breaking changes; both clean; CI green on bumped versions; deprecation annotation cleared on next main-branch run.

# Authority

Operational Standards v12, 2026-05-24. Adds §§37–41 absorbing the 2026-05-24 CC-tooling + fork-security + PII-logging cluster. v11 retires on acceptance of v12.

v13 trigger: substantive doctrine change or new §. v12.x absorbs further status updates without major revision.

Companion to FM v8 (Invariant 2 layer-6 addition), V&R v7.2 (Phase 1.5 security-hardening precondition), Handover Plan v6.3, Excellence Roadmap v2.3, FSU v6.5, Memory Archive v5 (extended §G7 in parallel PR), `references/customer-fork-setup-checklist.md` (downstream cascade in next PR).