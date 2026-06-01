---
type: doctrine
version: 16
status: canonical
last_verified: 2026-06-01
last_verified_against: 585823d
supersedes: doctrine/operational-standards.md@v15
workstream: null
tags: [push-vs-record, picklist-hardening, attachment-screening, polling-daemon, sdk-vs-live, cc-tooling, fork-security, pii-logging, actions-version-discipline, code-self-documentation, successor-operator, tier-2-repair, successor-remediation, training-bounded-co-resolution]
---

**ITS Operational Standards v16**

2026-06-01 — Tier-2 Boundary Reframed: Training-Bounded Co-Resolution (v15 enforcement-layer framing removed)

*The Developer-Operator / Successor-Operator role split, §43, §44's repair-path/escalation structure, and the kill-switch reframe all carry forward. v16 removes the §44 "non-developer-safe enforcement layer" that v15 named as a hard pre-cutover BUILD GAP — there is no structural maintenance enforcement layer and none is built or required. The Tier-2 boundary holds by the trained operator's judgment, the both-rule, and co-resolution with the Developer-Operator until per-category clearance. The Successor-Operator is redefined as a trained operator who runs Claude Code himself (not a Smartsheet-UI-only approver). The Tier-1 self-heal gap survives as a standalone pre-cutover gate (its stale "Check H" status corrected to the implemented Check C marker-file floor in a v16.x absorption — see Authority). No execution-layer mechanism is asserted as built.*

# Purpose

Cross-cutting operational patterns every ITS workstream uses. Each workstream brief and mission file references this doc rather than restating these patterns. When a pattern here changes, it changes for every workstream.

v11 is a full consolidation since v10 (2026-05-21 morning). It folds in the v10.1 overlay (Check G MAINTENANCE-defer) plus the 2026-05-21/22 cascade introducing polling-daemon doctrine (PRs #59 + #60), the pre-Customer-1 security hardening cluster (trusted-contacts + attachment screening + picklist hardening), and the in-repo tech_debt.md as canonical execution-layer log.

# What Changed in v11

- §1 Kill Switch — picklist-hardening forward reference added; Runtime Gate column in ITS_Daemon_Health flagged as future per-daemon switch.

- §2 Daily Watchdog — Check F (Mail.app rule silent disable) flagged for retirement; the implemented staleness floor is the Check C marker-file check (the mechanism this section earlier referenced as a successor "Check H"), which covers all four tracked daemons.

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

# What Changed in v13

One new section captures a discipline whose absence kept surfacing as "future-Seth + future-CC have to leave the file to understand the why":

- **§42 — Code-Level Self-Documentation Discipline.** Mandatory module docstrings with four headings (Purpose / Invariants / Failure modes / Consumers) for every new `shared/*` module and workstream entrypoint. In-code rationale comments for non-obvious decisions, citing the motivating F-finding, session log, doctrine §, or PR. Retrofit existing modules opportunistically per §14.

Cross-references added: §14 ↔ §42 (preservation comments capture the "why we kept this" anchor); §30 ↔ §42 (rationale comments capture the live-API quirk that motivated the integration test); verify-before-fix discipline ↔ §42 (the in-code rationale IS the verification anchor for future-fix decisions).

- Sections §§1–41 carry forward from v12 with cross-reference refresh only.

# What Changed in v14

One reframe corrects a security-posture overstatement the 2026-05-25 forensic audit flagged (audits/2026-05-25_forensic-audit.md, finding F07): §1 was written in a way that invited treating the kill switch as a security control when it is fail-open by design.

- **§1 — Kill Switch reframed.** The kill switch is recategorized as an operator-convenience suggested pause, explicitly NOT a security boundary. It is fail-open on three modes — sheet unreachable / row missing / invalid value all resolve to ACTIVE + WARN — which is intentional (availability is chosen over a hard stop) and is precisely why it cannot be relied on as a control: an adversary who can make the sheet unreachable defeats it, because it fails toward running. A security-relevant halt must come from the External Send Gate (Foundation Mission Invariant 1), which is the real boundary. The mechanism, the three fail-open modes, the picklist-hardening forward reference, and the per-daemon runtime gate are all unchanged; only the framing is corrected. The deferred fail_closed_until timestamp mechanism stays in tech debt and is not implemented here.

- Sections §§2–42 carry forward from v13 with cross-reference refresh only.

# What Changed in v16

v16 removes the Tier-2 "non-developer-safe enforcement layer" framing that v15 introduced and replaces it with the training-bounded co-resolution model. The Developer-Operator / Successor-Operator role split, §43, §44's repair-path / escalation structure, and the v14 §1 kill-switch reframe all carry forward.

- **§44 reframed — the Tier-2 boundary is training-enforced, not structurally enforced.** v15 named a "non-developer-safe enforcement layer" — a structural guard confining a repair session without a developer present — as a hard pre-cutover BUILD GAP. v16 removes that framing: there is no structural maintenance enforcement layer, and none is to be built. The Tier-2 boundary holds by the trained operator's judgment, the both-rule (novel OR high-class → Tier 3), and co-resolution with the Developer-Operator on the four high-class categories until per-category clearance. The capability-gating philosophy still informs how the boundary is drawn; it does not become a built control. (No execution-layer mechanism is asserted as built — still true.)

- **Successor-Operator redefined — a trained operator who runs Claude Code himself.** Not a Smartsheet-UI-only approver rubber-stamping Claude-driven actions: he runs CC, follows the §43 runbooks/checklists, carries out the low-capability-class repair set, and is trained to recognize and escalate the four high-class categories. He is still not a developer (writes no code; performs none of the §§37-41 developer-context operations).

- **Pre-cutover coupling severed.** The Tier-1 self-heal gap (the Check C marker-file staleness floor, §2 — earlier called "Check H") survives as a real pre-cutover gate on its own — narrowed to the weekly_generate Friday-crash catch-up now that Check C covers all four tracked daemons and the F16 ping is live; the v15 "BOTH must be built" coupling to a Tier-2 enforcement layer is removed (there is no such layer). The Tier-2 pre-cutover readiness gate is now the §44 low-capability-class action set implemented as discrete, tested, non-escalating operations + §43 runbooks + the trained-operator / demonstrated-supervised-repair gate (Handover Plan v8 / V&R v9).

- §43 (Successor-Remediation Documentation Discipline), §44's LOW/HIGH capability-class sets, the both-rule, the audit-trail requirement, the §§37-41 role-scope clarifier, and the §§1-42 sections all carry forward from v15.

# §1 — Kill Switch

**What it is — and is not.** The kill switch is an operator-convenience suggested pause: a way for the operator to halt scheduled work cleanly. It is **not** a security control and not a security boundary. It is fail-open by design — if ITS_Config is unreachable, the system.state row is missing, or the value is invalid, the kill switch resolves to ACTIVE (work proceeds) and emits a WARN. That fail-open posture is intentional (availability is chosen over a hard stop) and is exactly why the mechanism cannot be relied on as a control: an adversary who can make the sheet unreachable — or an accidental misconfiguration — defeats it, because it fails toward running, not toward halting. A security-relevant halt must come from a different mechanism: the External Send Gate (Foundation Mission Invariant 1), which is the real boundary — the two-process model means a successful injection at the AI layer still cannot transmit externally regardless of kill-switch state.

ITS_Config Smartsheet (sheet id 3072320166907780, see §24). Tall key/value layout. system.state setting reads ACTIVE / PAUSED / MAINTENANCE. Every Claude Code script reads it first via shared check_system_state() helper. PAUSED = scheduled scripts skip silently. MAINTENANCE = same, but watchdog does not alert. Anyone with edit access to the sheet can flip it.

Status: shared/kill_switch.py wired against ITS_Config via shared.smartsheet_client.get_setting (PR #9, 2026-05-18). Fail-open on three modes — sheet unreachable / row missing / invalid value — with distinguishable WARN messages routed through error_log. The three fail-open modes are intentional; see the reframe above for why they make this a pause, not a control. The deferred fail_closed_until timestamp mechanism (a future option to convert specific failure modes to fail-closed after a bounded window) is tracked in tech debt and is NOT implemented.

## Picklist-Hardening Forward Reference

Pre-Customer-1, the system.state Value cell type should migrate from TEXT_NUMBER to PICKLIST with the enum {ACTIVE, PAUSED, MAINTENANCE}. Eliminates typo/case/whitespace fail-open trigger. Existing fail-open logic stays as belt-and-suspenders for the Smartsheet-unreachable case. See §35 for the system-wide picklist-hardening convention.

## Per-Daemon Runtime Gate (Future)

ITS_Daemon_Health Runtime Gate CHECKBOX column (planned) gives operators per-daemon on/off control from the same surface they use for monitoring. Today's per-daemon kill switches live as separate ITS_Config rows (e.g., safety_reports.intake.polling_enabled). Runtime Gate consolidates these into one operator surface. Bundle with shared/runner.py extraction at second polling-daemon consumer per §14.

# §2 — Daily Watchdog

launchd-scheduled Claude Code script (scripts/watchdog.py) runs daily at 7:00 AM ET. Verifies critical scheduled jobs ran in the last 24 hours, surfaces items past SLA, checks Anthropic spend trend. Silent if green; emails + SMS the operator if anything is off.

Status: 6 of 7 checks live: Check A (stale ITS_Review_Queue, PR #33), Check B (open CRITICALs in ITS_Errors, PR #33), Check C (scheduled jobs last-run markers, PR #36), Check D (14-day reviewer-chain forward scan, PR #36), Check F (Mail.app rule silent disable, PR #36; FLAGGED FOR RETIREMENT per below), Check G (alert dedupe summary sweep, PR #44; MAINTENANCE-defer shipped PR #52).

Check E (Anthropic spend trend) deferred to Phase 1.5 — architectural choice; sandbox spend signal-to-noise too low at $5-credit scale.

## Check F Retirement + Check C Staleness Floor (the successor earlier scoped as "Check H")

Check F polls safety@evergreenmirror.com mailbox idle hours as a proxy for Mail.app-rule health. Post-PR-#59, safety_reports is on a polling daemon. The mailbox-idle proxy is now redundant. The implemented staleness floor is the **Check C marker-file** check: each scheduled job writes a `{slug}.last_run` marker on a completed cycle, and Check C flags any tracked job whose marker is missing or older than its per-job freshness window. Check C already covers all four tracked daemons (safety_intake, safety_weekly_send_poll, safety_weekly_generate, safety_picklist_audit). (An earlier draft of this section scoped a *distinct* "Check H" that would read ITS_Daemon_Health for every Enabled=true daemon and flag rows older than 2 × Interval Seconds; that design was **never built** — the marker-file Check C is the staleness detector that exists, and "Check H" is a naming artifact. Recorded here for provenance.) Retire Check F when (a) the Check C floor covers all daemons [done] and (b) no remaining workstream depends on Mail.app rules.

**Silent fail-open hazards must become watchdog-detectable signals (v15).** Tier 1 of the successor-maintenance model (§44) only works if faults surface. Any condition that today fails silently and is implicitly "deferred to the operator to notice" — a daemon that dies with no heartbeat (audit F17), or a guard hook / worktree control that disappears or is removed without notice — must be promoted to a signal the watchdog (or daemon-health surface) can detect and push, NOT a condition that depends on a human happening to look. The Check C marker-file staleness floor (earlier framed as a "Check H" heartbeat-staleness successor) is the first instance of this principle; the guard-layer-disappearance case (a propose-only block-* hook silently absent because its agent symlink dangles, leaving a session ungoverned — see references/worktree-discipline.md) is a second. Each silent fail-open hazard identified during build is either made watchdog-detectable or logged to tech debt (§36) as an explicit, named gap — never left as an unstated reliance on the operator.

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

> **Role scope (v15).** Every operation described in §§37-41 — installing/invoking skills, the block-dangerous-git carve-outs and manual force-delete recovery, the per-customer-fork `gh api` hardening and gitleaks runs, the migration-script dry-run/live-write split, worktree cleanup, GitHub Actions version bumps — is a **Developer-Operator** operation. It requires git/CC/shell fluency and the standing developer-grade override authority the guard hooks assume (§38 "operator shell is unaffected"). The **Successor-Operator** (the trained-operator Tier-2 role defined in §44) performs NONE of these; they are out of the Successor-Operator's capability class by definition. Where the unqualified word "operator" appears in §§37-41, read it as Developer-Operator.

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

# §42 (NEW) — Code-Level Self-Documentation Discipline

Every `shared/*` module and every workstream entrypoint will be read again — by future-Seth, by future-CC, by the maintainer of a customer fork three months out. The code should answer "why" without forcing the reader to leave the file.

## Mandatory module docstrings

Every NEW module in `shared/*` and every workstream entrypoint (e.g., `safety_reports/intake_poll.py`, `safety_reports/weekly_generate.py`) opens with a docstring carrying four named headings, in this order:

```python
"""One-sentence module purpose.

Purpose
-------
What this module does. Two sentences max.

Invariants
----------
What cannot change without breaking consumers. Reference Foundation
Mission invariants and Op Stds sections by stable anchor where
applicable. If the module is on the External Send Gate path or
processes adversarial input, restate the relevant invariant here.

Failure modes
-------------
Fail-open vs. fail-closed posture. Exception types raised. error_log
categories used. What recovers vs. what propagates.

Consumers
---------
What imports this module. What depends on its outputs (sheets, files,
external APIs). Useful for impact-analysis when changing internals.
"""
```

## In-code rationale comments

Any decision that would surprise a future reader gets a comment block above the relevant code:

```python
# Rationale: {short explanation of why this choice over alternatives}.
# Reference: {F-finding, session-log path, doctrine §, or PR number}.
```

Decisions worth a rationale comment:

- Fail-open vs. fail-closed (either direction — both are choices).

- Working around an SDK quirk or live-API behavior that differs from the SDK's stated contract.

- Accepting a documented risk (the comment IS the acceptance record).

- Choosing a less-obvious pattern when an obvious one was considered.

- Preservation-over-refactor decisions per §14 (the comment captures why a working pattern is preserved over a cleaner rewrite).

The reference must be specific enough that the future reader can find the source. "F23 — see audit" is fine; "see audit" is not.

## When to apply

- All NEW `shared/*` modules and workstream entrypoints from this doctrine bump forward. CC briefs reference §42 when scoping new modules.

- Existing modules retrofit opportunistically per the preservation-over-refactor convention (§14): when next touched for an unrelated reason, add the docstring + any motivation comments that surface during review. NOT a sweep PR. Doctrine §14 explicitly rejects "let's go fix every module" passes.

## Interaction with existing doctrine

- Complements verify-before-fix discipline. The in-code rationale IS the verification anchor for future-fix decisions: a reader who understands "this fail-open posture exists because of F23" doesn't re-litigate the choice when adjacent code needs changes.

- Complements §30 (SDK-vs-Live Integration Test Discipline). The rationale comment captures the live-API quirk that motivated the integration test, so future-CC reading the test understands the defense-in-depth.

- Complements §14 (preservation-over-refactor). The rationale comment captures why a working-but-ugly pattern is preserved. Without it, the next reader assumes the ugliness was an oversight and "fixes" it.

## Enforcement

Initial enforcement is by convention + review. CC briefs reference §42 explicitly when scoping new modules. Operator review at PR time checks for docstring presence and rationale comments on non-trivial decisions.

Trigger for stricter enforcement (e.g., AST lint check for docstring presence; ruff-rule for missing rationale on decisions matching known patterns): three or more instances within a 30-day window of "I read this module and couldn't tell what the rationale was." Tracked in tech debt; revisit when triggered.

## Example — `shared/state_io.py` post-§42 retrofit

```python
"""Atomic JSON/text writes + sidecar lock for daemon-managed state.

Purpose
-------
Canonical entry point for all writes to files under `~/its/state/`.
Provides crash-safe atomic write + concurrent-writer protection so
the polling-daemon class (intake_poll, weekly_send_poll, and future
consumers) cannot corrupt shared state files.

Invariants
----------
- Raw `Path.write_text` / `Path.write_bytes` on files under
  `~/its/state/` is forbidden. All writes route through this module.
- The sidecar lock pattern (flock on `{path}.lock`, not on the data
  file) is load-bearing: `os.replace` swaps the data-file inode,
  which would invalidate any flock held directly on it.
- `with_path_lock` is non-blocking with bounded retry (5×50ms,
  mirroring `shared/alert_dedupe._acquire_lock`). On exhaustion it
  raises `StateLockTimeoutError`; callers decide whether to log+
  continue (heartbeat writes, per CLAUDE.md ARCH-2) or propagate.

Failure modes
-------------
- Lock-acquisition timeout → raises `StateLockTimeoutError`. Heartbeat
  consumers log a WARN under `error_log` category
  `daemon_health_write_failed` and continue the cycle.
- Atomic-write disk error → raises `OSError` natively. Callers do not
  retry; the next cycle gets a fresh attempt.
- Serialization error → raises `TypeError` / `ValueError` natively.

Consumers
---------
- `safety_reports/intake_poll.py` — seen-set, heartbeat-row state.
- `safety_reports/weekly_send_poll.py` — heartbeat-row state.
- `shared/alert_dedupe.py` — pending migration in PR 2 of the
  Phase 1.4 hardening cluster.
- Future: `shared/circuit_breaker.py` per F08 will persist breaker
  state through these helpers.

Reference
---------
Audit F19 + F23 in `its-blueprint/audits/2026-05-25_forensic-audit.md`.
Landed via `its` PR #88 (merge commit `36932bd`). Session log:
`its/docs/session_logs/2026-05-25_state-io-atomic-write.md`.
"""
```

# §43 (NEW) — Successor-Remediation Documentation Discipline

§42 documents code FOR a code-reader: module docstrings and in-code rationale aimed at future-Seth, future-CC, and a developer maintaining a fork. That audience is the **Developer-Operator**. It is the wrong audience for Tier 2 of the three-tier maintenance model.

The human in the loop at Tier 2 is the **Successor-Operator** — a trained operator who runs Claude Code himself and follows runbooks, but is not a code-reader (writes no code; does none of the §§37-41 developer-context work). This section is the PARALLEL discipline for that audience. Where §42 answers "why is this code the way it is," §43 answers "what does the Successor-Operator do when this capability misbehaves."

## Document-as-you-build rule

Every capability ships a plain-language **successor-remediation runbook entry written AS the capability is built** — not retrofitted, not deferred. The entry is part of the capability's definition-of-done, the same way the §42 docstring is. A capability without its remediation entry is incomplete. Entries are authored as **Markdown shipped with the capability** in the execution repo (version-controlled alongside the code): Claude loads the relevant entry to drive a Tier-2 repair. The Successor-Operator does not open the Markdown — they see Smartsheet rows and alert emails and approve; Claude reads the entry on their behalf.

## Entry shape

Each entry is written for a reader who can see Smartsheet rows and alert emails but cannot read code, and has four parts:

- **Symptom** — stated in Smartsheet / alert / dashboard terms the Successor-Operator actually sees (e.g., "ITS_Daemon_Health shows `safety_reports.intake_poll` Last Cycle Status = STALE" or "a CRITICAL alert email names category `daemon_health_write_failed`"). NOT a stack trace or exception class.
- **What the Successor-Operator checks** — the specific sheet/column/value to look at, in UI terms.
- **The Claude prompt or UI action** — either the exact plain-language request the Successor-Operator gives Claude ("Claude, the intake daemon heartbeat is stale — please re-run it and confirm a fresh heartbeat"), or the direct Smartsheet-UI action ("set ITS_Config row `safety_reports.intake.polling_enabled` to true"). Claude drives any operation that is not a literal UI cell edit; the Successor-Operator approves.
- **Escalate-to-Seth condition** — the explicit boundary at which this stops being a Tier-2 repair and becomes a Tier-3 escalation to the Developer-Operator, stated in observable terms ("if the heartbeat is still stale after one re-run, or if the alert names the External Send Gate or any secret/auth category, stop and escalate to Seth"). This boundary is the §44 Tier-2/Tier-3 rule expressed for one specific capability.

## Distinction from §42 (do not conflate)

| | §42 | §43 |
| --- | --- | --- |
| Audience | code-reader (Developer-Operator, future-CC) | non-developer Successor-Operator |
| Lives in | module docstrings + in-code comments | plain-language Markdown shipped with the capability (Claude-read; no code) |
| Answers | "why is this code the way it is" | "what do I do when this misbehaves" |
| Vocabulary | invariants, exception types, error_log categories | Smartsheet rows, alert subjects, UI actions, Claude prompts |

The two are NOT substitutes. A §42 docstring saying "fail-open on Smartsheet-unreachable" does not tell a non-developer what to do when it fails open; a §43 entry saying "if the sheet shows STALE, ask Claude to re-run" does not tell a developer why the inode-swap lock pattern is load-bearing. Each capability that has a Tier-2-reachable failure mode needs both.

## Inheritance into briefs

Every future workstream brief inherits a **"successor-remediation deliverable"** the same way it inherits the Foundation invariants: F08/F09 (circuit breaker, dedupe hardening), the Safety Portal, and every workstream after them state, in their deliverables, the §43 remediation entries that ship with the capability. CC briefs reference §43 explicitly when scoping any capability whose failure is something a Successor-Operator could plausibly be asked to resolve at Tier 2.

## Enforcement

Initial enforcement is by convention + review, mirroring §42: the operator review at PR time checks that a capability with a Tier-2-reachable failure mode shipped its §43 entry. The Markdown runbook substrate (where the entries collect) and any automated presence check are ordinary build / tech-debt items; they are no longer coupled to any "enforcement-layer gap" (none exists — see §44's training-enforced Tier-2 boundary).

# §44 (NEW) — Tier-2 Claude-Assisted Repair Path

The successor-maintenance model has three tiers. **Tier 1 — self-healing**: daemons recover, the watchdog catches staleness, no human acts (the self-heal layer is substantially built — the Check C marker-file staleness floor covers all four tracked daemons and the UptimeRobot external ping (audit F16) is live; the lone residual pre-cutover build item is the weekly_generate Friday-crash catch-up, since weekly_generate is calendar-scheduled and a crashed Friday cycle is not auto-recovered by launchd until next Friday; see §2 and the Handover Plan v8 / V&R v9 pre-cutover conditions). **Tier 2 — Claude-assisted Successor-Operator repair**: the trained Successor-Operator runs Claude Code himself and, following the §43 runbook, carries out a low-capability-class repair — escalating anything novel or high-class to Tier 3. **Tier 3 — escalation to the Developer-Operator** (Seth), who is a reachable escalation asset, not the primary operator. This section defines Tier 2 and its boundary with Tier 3.

## Who acts at Tier 2

The Successor-Operator (per §43 / the §37 role-scope note) is a trained operator who runs Claude Code himself, reads Smartsheet and alerts, and follows the §43 remediation entry for the affected capability to carry out the repair. He does not write code, perform §§37-41 developer-context operations, or touch secrets/Keychain. His contribution is operating CC under the runbook plus the judgment to recognize and escalate the four high-class categories; Claude does the diagnostic and mechanical work within the low-class set.

## In-scope: the LOW-capability-class repair set ONLY

Tier 2 is limited to repairs that change no code, touch no secret, and cannot transmit externally. The closed in-scope set is:

- Re-run a stopped or stale daemon (the most common Tier-2 action).
- Toggle an ITS_Config value within its bounded enum / its `*.polling_enabled` runtime gate (§35 picklist domains).
- Re-send an already-approved item that failed to send (re-trigger an existing approval — NOT create or alter an approval).
- Re-seed a missing config or daemon-health row to a known-good value.
- Clear a stuck lock / stale state file so a daemon can resume.

These are low-class precisely because none of them can cross the External Send Gate, expose a secret, alter doctrine, or require a code edit.

## Structurally forbidden at Tier 2: the HIGH-capability-class set

HIGH-capability-class is defined STRUCTURALLY, not by how well something is documented. Anything that touches ANY of the following is high-class and is forbidden at Tier 2 — it escalates to Tier 3 unconditionally:

- the **External Send Gate** / anything that could cause an external transmission (FM Invariant 1);
- **secrets / auth** (Keychain, tokens, credentials, approver-principal configuration);
- **doctrine** (any change to a doctrine doc or an invariant);
- anything **requiring a code change**.

## The escalation boundary (the "both" rule)

A fault escalates to Tier 3 if it is **NOVEL** (not covered by a §43 runbook entry) **OR HIGH-capability-class**. Equivalently: a fault is Tier-2-eligible only if it is **documented (has a §43 entry) AND low-class**. High-class always escalates regardless of documentation — a perfectly documented secret-rotation is still Tier 3 because the class, not the doc, decides. Novel-but-low-class also escalates, because no vetted §43 path exists yet for Claude and the Successor-Operator to follow safely. Tier 3 resolution by the Developer-Operator that recurs should produce a new §43 entry so the next instance can drop to Tier 2.

## Audit-trail requirement

Every Tier-2 repair is audit-trailed: the symptom, the §43 entry followed, the action Claude took, and the Successor-Operator's approval are recorded to the forensic surfaces (ITS_Errors as the record leg per §3.1, with a Correlation_ID per §3). A Tier-2 repair that cannot be reconstructed after the fact is a process failure even if the repair itself worked.

## The through-line (capability-gating philosophy, extended)

The philosophy that keeps the AI out of the send path informs HOW the Tier-2 boundary is drawn — why the four high-class categories are off-limits. `tests/test_capability_gating.py` enforces FM Invariant 1's two-process model by static AST import inspection: a generation process structurally CANNOT import a send capability — that boundary holds by construction. Tier 2 does NOT get a structural analogue: there is no maintenance-side construction that confines a repair session, and none is built. The analogy is philosophical only; the Tier-2 boundary is held by the trained operator's judgment, the both-rule, and co-resolution with the Developer-Operator (next subsection).

## The Tier-2 boundary is training-enforced, not structurally enforced

No structural maintenance enforcement layer exists, and none is to be built. The Tier-2 boundary — confining a repair session to the low-capability-class set and routing the four high-class categories to Tier 3 — holds by three things: (1) the trained Successor-Operator's judgment (he runs Claude Code himself, follows the §43 runbook, and is trained to recognize the four high-class categories); (2) the both-rule (novel OR high-class → Tier 3); and (3) co-resolution with the Developer-Operator on the four high-class categories until per-category clearance is granted (dated, logged, Developer-Operator-only).

The guard hooks that exist today (`.claude/hooks/`: block-codeql-dismiss, block-dangerous-git, block-doc-reconciliation-write, block-doctrine-write) are REAL but **scoped to subagent / developer sessions and fall open for the operator's own session** — each hook's message tells the human to "run it manually." They protect developer / subagent sessions and assume the human in the loop can safely override. They are NOT expected to confine the trained Successor-Operator's repair sessions; that boundary is the training + both-rule + co-resolution model above, not a hook. There is no non-developer-safe enforcement layer, and the through-line ends at philosophy (it informs WHY the four categories are off-limits), not at a built control.

The Tier-1 self-heal gap (the Check C marker-file staleness floor, §2 — earlier called "Check H") remains a real pre-cutover gate on its own — narrowed to the weekly_generate Friday-crash catch-up now that Check C covers all four tracked daemons and the F16 ping is live; it is no longer coupled to any Tier-2 enforcement layer (there is none). The Tier-2 pre-cutover readiness gate is instead the §44 low-capability-class action set implemented as discrete, tested, non-escalating operations + §43 runbooks for the top fault classes + the trained-operator / demonstrated-supervised-repair gate (Handover Plan v8 Pre-Cutover Conditions; V&R v9). Tracked in execution-layer tech debt (§36). (The "both" rule above — novel OR high-class escalates to Tier 3 — is the steady-state safety default.)

# Authority

Operational Standards v16, 2026-06-01. Tier-2 boundary reframe: v16 removes the "non-developer-safe enforcement layer" framing introduced in v15 — a structural guard that v15 named as a hard pre-cutover build gap — and replaces it with the training-bounded co-resolution model. There is no structural maintenance enforcement layer; none is built or required. §44's Tier-2 boundary now holds by the trained operator's judgment + the both-rule + co-resolution with the Developer-Operator until per-category clearance. The Successor-Operator is redefined as a trained operator who runs Claude Code himself (not a Smartsheet-UI-only approver). §43, §44's LOW/HIGH capability-class sets, the both-rule, the audit-trail requirement, the §§37-41 role-scope clarifier, and the v14 §1 kill-switch reframe all carry forward. The Tier-1 self-heal gap (Check C marker-file staleness floor, §2 — earlier called "Check H") survives as a standalone pre-cutover gate, its stale status characterization corrected in a v16.x absorption (below); the v15 "BOTH" coupling to a Tier-2 enforcement layer is removed. No execution-layer mechanism is asserted as built. v15 retires on acceptance of v16. Canonical git tag: operational-standards-v16.

v15 trigger: §43 + §44 added (Successor-Remediation Documentation Discipline; Tier-2 Claude-assisted repair path) and the Developer-Operator / Successor-Operator role split applied across §§37-44. v14 was complete on its own terms; v15 codifies the operator-decided three-tier non-developer-successor maintenance model and names the Tier-2 non-developer-safe enforcement layer as a hard pre-cutover build gap (alongside the Tier-1 Check H self-heal gap). Tag pushed post-merge: `operational-standards-v15`.

v16 trigger: §44's Tier-2 protective basis recharacterized from structural (a "non-developer-safe enforcement layer," named in v15 as a hard pre-cutover build gap) to training-based (trained operator + both-rule + co-resolution); the Successor-Operator role redefined accordingly. Per the v16-trigger criterion the v15 doc carried ("recharacterization of a mechanism's protective claim"), changing §44's basis from structural to training/co-resolution is exactly that — a major bump, not a v15.x status update. Tag pushed post-merge: `operational-standards-v16`.

v17 trigger: substantive doctrine change, new §, or recharacterization of a mechanism's protective claim. The v13→v14 reframe established that recharacterizing what a mechanism *is* is bump-worthy; v14→v15 established that a doc-wide role abstraction + a new tier is; v15→v16 established that changing a tier's protective basis (structural → training/co-resolution) is. v16.x absorbs further status updates (e.g., per-category clearances granted to the Successor-Operator) without major revision.

v16.x status absorption (2026-06-01, verified against exec 585823d): the §2 / §44 Tier-1 self-heal characterization is corrected. The mechanism described as an unimplemented "Check H heartbeat-staleness" check (reading ITS_Daemon_Health, 2 × Interval) with "two of three daemons heartbeat-retrofit-pending" was **never built**; the implemented staleness floor is the watchdog **Check C marker-file** check, which already covers all four tracked daemons (safety_intake, safety_weekly_send_poll, safety_weekly_generate, safety_picklist_audit), and the external **UptimeRobot** ping (audit F16) is live. The lone residual is the weekly_generate Friday-crash **catch-up** (exec follow-on). This correction does **not** change what the Tier-1 self-heal mechanism *is* or its protective claim — Tier-1 is still "daemons recover, the watchdog catches staleness, no human acts" — it corrects the stale *implementation-state* claim, so per the v17 trigger it is a **status update absorbed at v16.x: no major bump, no new tag.** The prior "Check H" framing is recorded here (and at §2 / §44 / line 94) for provenance.

v14 trigger: §1 kill-switch security-posture reframe (F07). v13 was complete on its own terms; v14 corrects doctrine that over-described a fail-open pause as a security control. Tag pushed post-merge: `operational-standards-v14`.

v13 trigger: code-level self-documentation discipline added (§42). v12 was complete on its own terms; v13 captures a discipline whose absence was surfacing as a recurring "future-reader has to leave the file" cost. Tag pushed post-merge: `operational-standards-v13`.

Companion to FM v11 (Invariant 1 two-process model still informs how the Tier-2 boundary is drawn; the Developer-Operator / Successor-Operator role principle, with the Successor-Operator redefined as a trained CC operator), V&R v9 (the ship-and-leave / developer-departure threshold; the Tier-1 self-heal gap remains the companion hard pre-cutover condition; the Tier-2 boundary is training-enforced, no enforcement-layer gap), Handover Plan v8 (the three-tier fault-response model + role definitions + Pre-Cutover Conditions), Excellence Roadmap v4 (R6 successor-maintenance build program, with the Tier-2 enforcement-layer sub-deliverable replaced by Tier-2 readiness work), Permissions Ask v5 + System+HR Handoff v6 (Successor-Operator vs Developer-Operator access split — their role descriptions predate this reframe and are pending a role-redefinition follow-on), FSU v6.5, Memory Archive v5 (extended §G7 in v12 parallel PR), `references/customer-fork-setup-checklist.md` (downstream cascade in v12). v13 parallel companion: `prompts/scaffold/` (PR 2 of that cascade — `shared-module-migration.md`, `manual-smoke.md`, `cc-implementation.md` v1 → v2).