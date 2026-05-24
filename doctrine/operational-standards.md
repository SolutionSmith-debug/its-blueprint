---
type: doctrine
version: 11
status: canonical
last_verified: 2026-05-24
last_verified_against: 3b7d56d
supersedes: doctrine/operational-standards.md@v10
workstream: null
tags: [push-vs-record, picklist-hardening, attachment-screening, polling-daemon, sdk-vs-live]
---

**ITS Operational Standards v11**

2026-05-22 — Full Consolidation Absorbing 2026-05-21/22 Cascade

*Five new sections: §31 polling daemons, §32 operator visibility, §33 trusted contacts, §34 attachment screening, §35 picklist convention · §36 in-repo tech debt*

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

# Authority

Operational Standards v11, 2026-05-22. Full consolidation absorbing v10/v10.1 overlay + 2026-05-21/22 cascade (polling daemons, operator visibility, trusted contacts, attachment screening, picklist hardening, in-repo tech debt). v10 + v10.1 retire on acceptance of v11.

v12 trigger: substantive doctrine change or new §. v11.x absorbs further status updates without major revision.

Companion to FM v8 (Invariant 2 layer-6 addition), V&R v7.2 (Phase 1.5 security-hardening precondition), Handover Plan v6.3, Excellence Roadmap v2.3, FSU v6.5, Memory Archive v5, Cascade Unification Update 2026-05-22 Security Hardening.