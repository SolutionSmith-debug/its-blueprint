---
type: reference
version: 7
status: canonical
last_verified: 2026-05-24
last_verified_against: 3b7d56d
workstream: null
tags: [smartsheet, system-workspace, human-review, successor-operator, training-bounded-co-resolution]
---

ITS — Smartsheet System & Human Review Handoff v7

# ITS — Smartsheet System & Human Review Handoff v7

ITS — System and ITS — Human Review workspaces, schemas, bootstrap, API constraints, operational patterns

Generated 2026-05-17 evening; **schemas corrected 2026-05-18 morning against live**** ****get_columns**** ****verification** — Solution Smith

# Authority and scope

**This document is v5 of the Smartsheet Handoff series.** It covers the two Smartsheet workspaces created on 2026-05-17 evening — **ITS — System** (operator-only plumbing) and **ITS — Human Review** (Evergreen-employee-facing approval and personnel surfaces). It is the canonical handoff for those two workspaces and supersedes any references to those surfaces in prior versions.

**Smartsheet Handoff v4 remains canonical** for the customer-facing **Forefront Portfolio — ITS Demo** workspace — its 5 top-level folders, 12-sheet flat-per-project model, Bradley 1 source-of-truth template, FL flat-ledger design, Schedule and Closeout K-1 schemas, Vendor DB / Sub DB / Equipment DB seeding, and the production attachment plan. **Do not retire v4** when this document is filed; the two are sibling docs covering parallel workspaces.

A future cascade event may merge the customer-portfolio handoff (v4) and this System + Human Review handoff into a single unified Smartsheet Handoff. That merge requires v4 in front of the author to faithfully carry the customer-portfolio detail. This document does not attempt that merge. (Note: this doc's version line advanced to v6 (2026-05-29 successor-model cascade) then v7 (2026-06-01 de-1b reconciliation); the unified merge will take the next integer available at merge time.)

**Authority chain.** Foundation Mission v11 (operator-vs-customer-employee audience-separation principle, originated v6; plus the Developer-Operator / Successor-Operator maintenance-role distinction added in v10 and refined in v11 — Successor-Operator = trained CC operator) → Operational Standards v16 (workspace topology, sheet-ID bootstrap, MCP-gap REST-fallback, API constraints — originated v8; plus §§43-44 successor-maintenance discipline) → this document.

**Correction note.** The original 2026-05-17 evening cut drafted ITS_Time_Off, ITS_Config, and ITS_Errors schemas from the Cascade Unification Update’s seed-row tables rather than from live get_columns against the provisioned sheets. The Session Wrap Inventory (late evening 2026-05-17) caught the divergence. Schemas below match live state as of 2026-05-18 morning.

# Workspace topology overview

Three workspaces, separated by audience, not by data type:

| Workspace | ID | Audience | Doc |
| --- | --- | --- | --- |
| Forefront Portfolio — ITS Demo | 4129485730670468 | Evergreen day-to-day (PMs, admins, field) | **Handoff v4** |
| ITS — Human Review | 8561891980142468 | Evergreen day-to-day (approvers, personnel admins) | This doc |
| ITS — System | 680592632244100 | System-role-only (Developer-Operator = Seth at ADMIN; trained Successor-Operator at EDITOR for Tier-2 repair) | This doc |

The split exists because the people who handle each surface play different roles in the three-tier successor-maintenance model. ITS — System surfaces (ITS_Review_Queue anomalies, security flags, low-confidence extractions, sender-allowlist violations) are worked by the **Successor-Operator** — a trained operator who **runs Claude Code himself** and follows the §43 runbooks, escalating to the **Developer-Operator** (Seth) when a fault is novel or high-capability-class. This is a Tier-2 role, not a developer role: the Successor-Operator does **not** need maintainer-level system understanding and is not a code-reader (writes no code; does no §§37-41 developer-context work). Day-to-day reviewers handle WPR_Pending_Review and future per-workstream approval queues and need no system role at all. Separating these workspaces makes the role boundary visible and enforceable.

The pattern generalizes to multi-tenancy: the System workspace stays singular across all customers. Each customer gets their own portfolio workspace and either their own Human Review workspace or shares a cross-customer one — that decision is deferred to Customer 2 onboarding.

# ITS — System workspace

**Workspace ID:** 680592632244100

**Audience:** System-role-only. Seth (the **Developer-Operator**) holds ADMIN in Phase 0 and retains it for developer-context operations. At cutover a **Successor-Operator** (a trained operator who runs Claude Code himself) is added at EDITOR for Tier-2 repair (re-run a daemon, toggle an ITS_Config value, re-send an approval, re-seed a row, clear a stuck lock) — see permissions.md §3.2. ADMIN stays Developer-Operator-only; the Successor-Operator never performs §§37-41 developer-context operations.

**Folder structure (3 subfolders, 4 sheets):**

ITS — System (680592632244100)
├── 01 — Config (164788727768964)
│   └── ITS_Config (3072320166907780)
├── 02 — Logs (5231338308560772)
│   ├── ITS_Errors (27291433258884)
│   └── ITS_Quarantine (8687740798324612)
└── 03 — Queues (7201663145535364)
    └── ITS_Review_Queue (7243317526876036)

## ITS_Config (3072320166907780)

**Purpose.** Runtime configuration for the ITS system. Read by shared/kill_switch.py at the start of every script invocation; read by reviewer-chain selectors, observability endpoints, and per-workstream allowlists.

**Schema decision: tall, not wide.** A wide single-row layout would require column adds for every new setting — incompatible with the way config grows organically per workstream. Tall (key/value) keeps the column count fixed; code reads by Setting name.

| Column | Type | Notes |
| --- | --- | --- |
| Setting | TEXT_NUMBER (primary) | Unique key. Convention: <scope>.<key> (e.g., system.state, safety_reports.reviewers). |
| Value | TEXT_NUMBER | Free-form value. JSON-encoded for non-scalar (lists, maps). |
| Workstream | PICKLIST | One of: global, safety_reports, subcontracts, po_materials, email_triage, ai_employee. Used for filter views. |
| Description | TEXT_NUMBER | Human-readable description of what the setting controls. |
| Last Modified | DATETIME (system MODIFIED_DATE) | Auto-populated by Smartsheet. |
| Modified By | CONTACT_LIST (system MODIFIED_BY) | Auto-populated by Smartsheet. |

**Workstream picklist note.** Six values total. The original 5/17 evening draft used system, purchase_orders, and multi; the live sheet uses global, po_materials, and omits multi. Code that filters by Workstream must use the live values.

**Live state as of 2026-05-18 morning.** Sheet provisioned with the schema above; **0 rows**. Initial seed lands alongside the kill_switch.py refactor.

**Seed rows to land alongside shared/kill_switch.py wiring** (Workstream values use the corrected live picklist):

| Setting | Value | Workstream |
| --- | --- | --- |
| system.state | ACTIVE | global |
| system.heartbeat_url | https://uptimerobot.com/heartbeat/ | global |
| system.sentry_dsn_keychain_key | ITS_SENTRY_DSN | global |
| system.resend_api_keychain_key | ITS_RESEND_API_KEY | global |
| system.operator_email | operator@evergreenmirror.com | global |
| safety_reports.reviewer_chain | [“teala@evergreenmirror.com”,“sam@evergreenmirror.com”,“jacob@evergreenmirror.com”] | safety_reports |
| safety_reports.external_send_gate | MANUAL | safety_reports |

The reviewer chain default lives in shared/defaults.py; the ITS_Config row exists so it can be overridden without a code change.

**Read pattern (now backed by shared/smartsheet_client.py as of 2026-05-18 morning):**

from shared.smartsheet_client import get_setting

# get_setting() requires workstream as a keyword (signature-enforced, test-covered)
state = get_setting("system.state", workstream="global", default="ACTIVE")

get_setting() lives in shared/smartsheet_client.py and reads from SHEET_CONFIG (imported from shared.sheet_ids). Column-map caching with invalidate-on-miss-and-refetch is handled by the client.

## ITS_Errors (27291433258884)

**Purpose.** Append-only error log. Every exception caught by shared/error_log.py (or its tested replacement) appends a row here. Sentry remains the primary observability surface for stack traces. ITS_Errors is the morning-check surface: the **Successor-Operator** scans it for new CRITICAL/ERROR rows and, following the §43 runbook, **runs Claude Code** on the row — Claude reads the Traceback and carries out a Tier-2 low-class repair, or the Successor-Operator escalates to the **Developer-Operator** (Seth) when the fault is novel or high-capability-class. The Successor-Operator does **not** read tracebacks himself; the Traceback column is for Claude and for Seth on escalation.

| Column | Type | Notes |
| --- | --- | --- |
| Error | TEXT_NUMBER (primary) | Code-populated descriptive label (e.g., safety_reports.intake.attachment-too-large). |
| Timestamp | DATE | Date the error occurred. Time-of-day recoverable from row created_at. |
| Severity | PICKLIST | INFO, WARN, ERROR, CRITICAL. CRITICAL triggers Resend out-of-band alert. |
| Script | TEXT_NUMBER | Which Python script raised the error (e.g., safety_reports/weekly_generate.py). Replaces the original draft’s Workstream column — the live schema captures which file, not which logical workstream. |
| Message | TEXT_NUMBER | One-line error description. |
| Traceback | TEXT_NUMBER | Stack trace. Sentry remains the primary observability surface; this column is for at-a-glance morning scans without leaving Smartsheet. |
| Surfaced At | DATE | Same as Timestamp for most cases; distinct only when an error is backfilled from logs after the fact. |
| Resolved At | DATE | Operator marks resolution date. Presence implies resolved (no separate CHECKBOX in live schema). |
| Resolved By | CONTACT_LIST | Who resolved it. |
| Notes | TEXT_NUMBER | Operator notes on resolution. |

**Differences from the 5/17 evening draft.** Live schema uses Script (which file) instead of Workstream (which logical surface); uses Traceback (stacktrace specifically) instead of Context (JSON blob); has no Resolved CHECKBOX (resolution implied by Resolved At + Resolved By being non-empty); and adds Timestamp, Resolved By, Notes columns that the evening draft omitted.

**Consequence for shared/error_log.py implementation.** The Smartsheet write path must populate the live columns. Use get_columns (via the now-wired smartsheet_client) at write-path test time to verify the column map; don’t trust this document as the schema source if your latest pull contradicts it.

**Note on DATE rather than DATETIME.** See §Smartsheet API Constraints below. Time-of-day for an error is recoverable from the row’s intrinsic created_at field via the API.

**Stale-duplicate cleanup.** Four stale ITS_Errors duplicates from the 5/17 provisioning retry sequence (IDs 4195780532326276, 470411799121796, 2704945844277124, 4505679602601860) were already 404 by 5/18 morning. No deletion action required; only the canonical 27291433258884 survives.

## ITS_Quarantine (8687740798324612)

**Purpose.** Holds inbound content that failed the adversarial-input-handling pipeline (sender allowlist, structured-output validation, capability gating). Operator reviews and either releases (mark as legitimate, re-feed to workstream) or destroys (mark as adversarial, retain for forensics).

| Column | Type | Notes |
| --- | --- | --- |
| Quarantined Message | TEXT_NUMBER (primary) | Code-populated label, e.g., safety_reports.unknown-sender:foo@bar.com:2026-05-17. |
| Workstream | PICKLIST | Same value set as ITS_Config: global, safety_reports, subcontracts, po_materials, email_triage, ai_employee. |
| Reason | PICKLIST | unknown-sender, unstructured-output, capability-gate-violation, anomaly. |
| Sender | TEXT_NUMBER | Email address of original sender (if applicable). |
| Subject | TEXT_NUMBER | Email subject or message title. |
| Source File | TEXT_NUMBER | Box path or Smartsheet row ID where original is stored. |
| Received At | DATE | See note on DATE vs. DATETIME above. |
| Status | PICKLIST | PENDING_REVIEW, RELEASED, DESTROYED. |
| Reviewed By | CONTACT_LIST | Operator who acted on the entry. |
| Reviewed At | DATE | Auto-populated by automation rule when Status changes from PENDING_REVIEW. |

**Retention.** Released entries get re-fed to the workstream and their Quarantine row is marked RELEASED but retained for audit. Destroyed entries retain the row indefinitely for forensics.

## ITS_Review_Queue (7243317526876036)

**Purpose.** Operator-facing anomaly queue. Surfaces things ITS isn’t sure how to handle: low-confidence extractions, ambiguous classifier results, content that triggered security flags but didn’t quite hit the quarantine threshold, weekly-summary edge cases.

**Provenance.** Originally provisioned by smartsheet_migration/build_human_review.py at 2026-05-17 ~01:26 UTC in the demo workspace’s 06 — Human Review folder. Moved 5/17 evening to ITS — System / 03 — Queues (the operator-facing surface) per the audience-separation principle. The original folder was deleted.

**Schema** (from build_human_review.py, unchanged):

| Column | Type | Notes |
| --- | --- | --- |
| Entry | TEXT_NUMBER (primary) | Code-populated label identifying the item. |
| Workstream | PICKLIST | Same value set as ITS_Config. |
| Type | PICKLIST | LOW_CONFIDENCE, SECURITY_FLAG, AMBIGUOUS, ANOMALY. |
| Confidence | TEXT_NUMBER | Numeric 0-1 for low-confidence entries. |
| Context | TEXT_NUMBER | JSON-encoded context. |
| Source File | TEXT_NUMBER | Box path or Smartsheet row reference. |
| Surfaced At | DATE | See DATETIME note. |
| Status | PICKLIST | PENDING_REVIEW, RESOLVED, ESCALATED. |
| Reviewer Notes | TEXT_NUMBER | Operator notes on resolution. |
| Resolved At | DATE | Automation-populated when Status leaves PENDING_REVIEW. |

# ITS — Human Review workspace

**Workspace ID:** 8561891980142468

**Audience:** Evergreen approvers and personnel administrators. PMs and admins with approval authority on specific workstreams; Personnel admins for time-off entries. No system-internal access required.

**Folder structure (6 subfolders, 2 sheets at present, 4 placeholders):**

ITS — Human Review (8561891980142468)
├── 01 — Safety Reports (2486957285631876)
│   └── WPR_Pending_Review (3096105695793028)
├── 02 — Subcontracts (1924007332210564)
│   └── (Subcontracts_Pending_Review — TBD)
├── 03 — Purchase Orders & Materials (2768432262342532)
│   └── (POs_Pending_Review, RFQ_Pending_Review — TBD)
├── 04 — Email Triage (8960881749976964)
│   └── (Email_Triage_Pending_Review — TBD)
├── 05 — AI Employee (1185135518345092)
│   └── (AI_Employee_Pending_Review — TBD)
└── 06 — Personnel (7377585005979524)
    └── ITS_Time_Off (1506418040459140)

## WPR_Pending_Review (3096105695793028)

**Purpose.** Weekly Performance Reports awaiting Teala’s (or backup reviewer’s) approval before external send. The primary path for the Safety Reports workstream’s human-review gate; cannot be bypassed except by deliberate operator override (which itself flags the External Send Gate invariant).

**Provenance.** Originally provisioned by smartsheet_migration/build_human_review.py at 2026-05-17 ~01:26 UTC. Moved 5/17 evening from the demo workspace’s 06 — Human Review folder to ITS — Human Review / 01 — Safety Reports. Schema unchanged from the build_human_review.py provisioning.

**Schema** (carry forward from build_human_review.py — Seth, please paste exact column list from v4 if you have it. The provisioning script’s WPR_SHEET dict is the source of truth.):

Operationally, the columns cover: Week ending date, vendor name (or aggregated week label), report content (extracted PDF text or summary), reviewer assignment, approval status, approved/rejected timestamp, send-after-approval flag. The exact schema lives in smartsheet_migration/build_human_review.py (archived but preserved in-tree).

**Important behavior detail.** The “approve and send” action is split across two scripts per Invariant 1 (External Send Gate two-process model): weekly_generate.py reads PENDING reviews + materials and produces a draft. weekly_send.py (separate script, no AI capability) reads APPROVED rows and sends. The split prevents an instruction-injection in a report from causing an autonomous send.

## ITS_Time_Off (1506418040459140)

**Purpose.** Personnel time-off records. Read by shared/scheduling.py to know when a reviewer is unavailable and the chain should shift to the next person. Personnel admins update this directly via Smartsheet UI; ITS does not write to it.

**Why in Human Review and not System.** Personnel admins need write access; granting them System workspace access would expose operator internals. Putting ITS_Time_Off in Human Review’s 06 — Personnel folder lets Personnel admins do their job without seeing anything else.

| Column | Type | Notes |
| --- | --- | --- |
| Entry | TEXT_NUMBER (primary) | Code-populated label, e.g., teala-2026-w20. Useful for filter views; not load-bearing. |
| Person | CONTACT_LIST | The person taking time off. |
| Start Date | DATE | First day off (inclusive). |
| End Date | DATE | Last day off (inclusive). |
| Reason | PICKLIST | PTO, Sick, Holiday, Personal, Other. (5 values, Title Case — not the 4 upper-case values in the original 5/17 evening draft.) |
| Notes | TEXT_NUMBER | Free-form. |

**Differences from the 5/17 evening draft.** Column is Reason, not Type. PICKLIST is 5 values in Title Case (PTO/Sick/Holiday/Personal/Other), not 4 in upper-case. No Modified system column — the original draft listed one but the live schema does not include it.

shared/scheduling.py reads this sheet to identify gaps in availability and shifts the reviewer chain accordingly. PTO lookup is currently injectable (default fetcher returns []); real fetcher implementation lands in the next session — now unblocked since shared/smartsheet_client.py wired 2026-05-18 morning.

**Consequence for shared/scheduling.py implementation.** The PTO fetcher reads the Reason column (not Type) and accepts the 5-value Title-Case picklist. Test fixtures must mirror the live picklist exactly.

## Future per-workstream pending-review queues

Folders 02 — Subcontracts, 03 — Purchase Orders & Materials, 04 — Email Triage, 05 — AI Employee are pre-allocated. Each will hold one or more pending-review sheets when the corresponding workstream is built.

The naming convention is <Workstream>_Pending_Review. For Purchase Orders & Materials, two sheets are likely needed: POs_Pending_Review (for finalized POs awaiting send) and RFQ_Pending_Review (for vendor quote requests). The folder is pre-allocated to hold both.

**Why preallocate folders rather than create on-demand.** Permissions are simpler to reason about when the folder structure exists in advance. Granting an approver access to 02 — Subcontracts covers all future subcontract approval surfaces without re-granting at each new sheet.

# Sheet ID bootstrap module (shared/sheet_ids.py)

**Purpose.** Static module holding every workspace, folder, and sheet identifier. Solves the chicken-and-egg of shared/kill_switch.py needing the ITS_Config sheet ID before it can read system_state from ITS_Config itself.

**Landed 2026-05-18 morning** alongside the shared/smartsheet_client.py wiring PR. (The module was scoped in the unexecuted 5/17 evening Claude Code brief; it landed in the 5/18 morning session because smartsheet_client.py’s tests and smoke script required it.)

**Content** (full module — single source of truth for the IDs in this document):

"""Smartsheet workspace, folder, and sheet IDs for the ITS sandbox.

Static identifiers needed by shared/* modules at startup, before they can
read ITS_Config dynamically. At Customer 2 onboarding, this module becomes
per-customer configuration (Phase 1.6 multi-tenancy refactor).
"""
from __future__ import annotations

# Workspaces
WORKSPACE_DEMO         = 4129485730670468
WORKSPACE_SYSTEM       = 680592632244100
WORKSPACE_HUMAN_REVIEW = 8561891980142468

# ITS — System folders
FOLDER_SYSTEM_CONFIG = 164788727768964
FOLDER_SYSTEM_LOGS   = 5231338308560772
FOLDER_SYSTEM_QUEUES = 7201663145535364

# ITS — Human Review folders
FOLDER_HR_SAFETY_REPORTS                = 2486957285631876
FOLDER_HR_SUBCONTRACTS                  = 1924007332210564
FOLDER_HR_PURCHASE_ORDERS_AND_MATERIALS = 2768432262342532
FOLDER_HR_EMAIL_TRIAGE                  = 8960881749976964
FOLDER_HR_AI_EMPLOYEE                   = 1185135518345092
FOLDER_HR_PERSONNEL                     = 7377585005979524

# System sheets
SHEET_CONFIG       = 3072320166907780
SHEET_ERRORS       = 27291433258884
SHEET_QUARANTINE   = 8687740798324612
SHEET_REVIEW_QUEUE = 7243317526876036

# Human-review sheets
SHEET_WPR_PENDING_REVIEW = 3096105695793028
SHEET_TIME_OFF           = 1506418040459140

**Usage convention.** Any shared/* module that needs a Smartsheet ID imports from shared.sheet_ids. Never hardcode IDs in scripts. Tests can monkeypatch this module’s constants to point at test fixtures.

**Multi-tenancy implication.** At Customer 2 onboarding, this module becomes per-customer configuration. The Phase 0 flat-and-static form is correct for one customer; Phase 1.6 (multi-tenancy framework, per V&R) is when this gets refactored to a customer-keyed lookup. The refactor is well-isolated — only this module changes, callers are unaffected.

# Smartsheet API constraints

**Source of truth:**** ****docs/tech_debt.md**** ****in the repo.** Reproduced here for at-a-glance reference; the canonical record with workarounds and revisit triggers lives in the repo.

## Constraint 1: DATETIME columns require system column type at create

type: DATETIME columns are rejected at sheet creation unless paired with systemColumnType: MODIFIED_DATE | CREATED_DATE. User-editable DATETIME (e.g., “Timestamp”, “Surfaced At”) returns HTTP 500 / error code 4000 with no descriptive message.

**Workaround.** Use DATE for user-editable date columns. Time-of-day precision is lost from the in-sheet representation but is recoverable from the row’s intrinsic created_at (and modified_at) attributes via the API.

**All affected sheets in this document:** ITS_Errors (Timestamp, Surfaced At, Resolved At), ITS_Quarantine (Received At, Reviewed At), ITS_Review_Queue (Surfaced At, Resolved At), ITS_Time_Off (Start Date, End Date). All use DATE; programmatic ordering uses intrinsic timestamps where time-of-day precision is required.

## Constraint 2: AUTO_NUMBER columns rejected at sheet creation

systemColumnType: AUTO_NUMBER is rejected at sheet creation regardless of primary status, with or without autoNumberFormat. Other system column types (MODIFIED_DATE, MODIFIED_BY) are accepted in the same payload — the rejection is specific to AUTO_NUMBER.

**Workaround.** Plain TEXT_NUMBER primary columns code populates with descriptive labels (e.g., Error, Quarantined Message, Entry). Smartsheet’s intrinsic row IDs (returned in every API response) serve as the unique identity for code-side references.

**All affected sheets in this document:** ITS_Errors, ITS_Quarantine, ITS_Review_Queue, ITS_Time_Off. All have descriptive TEXT_NUMBER primaries.

## Constraint 3: Forms, Conditional Formatting, Filter Views, Automation Rules are UI-only

Pre-existing constraint, carried forward from session 2026-05-17 morning discovery and Op Stds v6 §19. Not API-exposed. Build labor split: **data via API/scripts; UX layer via UI one-time per template sheet, then Save-as-New clones forms + CF + filters to project clones.**

ITS_Config, ITS_Errors, ITS_Quarantine, ITS_Review_Queue do not need forms (operator surfaces). WPR_Pending_Review and ITS_Time_Off may want forms for the reviewer/admin UX — Seth’s UI work.

# Operational patterns

## Pattern 1: OAuth-MCP-first, REST fallback for gaps

**The Smartsheet MCP doesn’t expose sheet-move, sheet-delete, or folder-delete.** These are deliberately omitted for safety reasons. When the operator needs one of these primitives, the pattern is:

- **Short-lived sandbox API token**, scoped tightly. Generate fresh; do not reuse stored tokens.

- **Inline curl** in bash_tool or local script. Token passed via environment variable for the single invocation; not written to file or persistent env.

- **Verify-after via OAuth-authorized MCP browse.** Never trust the REST response alone — confirm the state change in a separate, audited read path.

- **Operator rotates the token post-session.** No long-lived credentials in chat history or local env.

**Examples from the 5/17 evening session:**

- POST /sheets/{id}/move × 2 (WPR_Pending_Review, ITS_Review_Queue moves out of demo workspace)

- DELETE /folders/{id} × 1 (delete 06 — Human Review from demo workspace after empty)

Three operations, single short-lived token, verified after via MCP browse_workspace. Token rotated by Seth post-session.

**Applies equally to Box and Microsoft Graph.** Same discipline when MCP coverage is absent for those systems. Generalizable pattern.

## Pattern 2: Sheet-creation deviation logging

When the Smartsheet API rejects a column definition at sheet creation, the deviation goes to docs/tech_debt.md with the rejected payload, the workaround applied, and the date discovered. Two such deviations live there now (DATETIME, AUTO_NUMBER); both forced by API behavior, not by ITS design choice.

The discipline matters because **Customer 2 deployment will hit the same constraints** — same Smartsheet API, same rejections. Pre-captured workarounds save discovery time at every customer onboarding.

## Pattern 3: Save-as-new for template propagation

When a template sheet has UI-layer assets (forms, conditional formatting, filter views, automation rules), the propagation path to project clones is **Save-as-New within the Smartsheet UI**, not API recreation. Save-as-New carries forms + CF + filters; API clone does not.

This is operator-tier knowledge — Seth performs Save-as-New manually when standing up a new customer or new project. Captured here so it’s transferred at handover.

## Pattern 4: Verify schemas against live get_columns before drafting docs

**Lesson from this document’s correction history.** Schemas in handoff documents must be verified against live get_columns calls, not transcribed from upstream seed-row tables or planning notes. The 2026-05-17 evening cut of this document drafted three sheet schemas from the Cascade Update’s seed-row tables and diverged from the live state on all three. The Session Wrap Inventory caught it; this corrected version reconciles.

**Discipline going forward.** Any handoff document that documents Smartsheet, Box, or Microsoft Graph schemas pulls those schemas from the live system at draft time. Don’t trust a planning doc as the schema source.

# Open items

**Immediate (now unblocked by 5/18 morning smartsheet_client.py wiring):**

- shared/kill_switch.py refactor — read by Setting name from ITS_Config (tall schema). Currently returns hardcoded ACTIVE. Now unblocked.

- Initial ITS_Config row seeding — system.state=ACTIVE, reviewer chain defaults, observability endpoints. Sheet has 0 rows live.

- shared/error_log.py Smartsheet write path — append rows to ITS_Errors on every caught exception. **Include a logging filter to silence the Smartsheet Python SDK’s raw 404 stdout output** that runs before our SmartsheetNotFoundError translation.

- shared/review_queue.py real read/write — wire to ITS_Review_Queue.

- shared/quarantine.py real read/write — wire to ITS_Quarantine.

- shared/scheduling.py PTO fetcher — read from ITS_Time_Off, Reason column (not Type), 5-value Title-Case picklist.

- scripts/watchdog.py real checks — at minimum, CRITICAL-unread count from ITS_Errors and stale-pending count from ITS_Review_Queue.

**Workstream-buildout:**

- WPR_Pending_Review approval workflow (forms + conditional formatting + automation rules) — UI work per FL_Setup_Guide convention.

- Per-workstream Pending_Review sheets in the corresponding HR folders as workstreams are built.

# Revision triggers

This document bumps when:

- A new sheet is provisioned in either System or Human Review workspace.

- A schema changes on any sheet documented here (column add/remove/retype).

- A new operational pattern is discovered (e.g., a third API constraint, or a new MCP-gap fallback case).

- The workspace topology changes (e.g., per-customer Human Review at Customer 2 onboarding).

- Foundation Mission or Operational Standards bump in a way that affects workspace audience-separation.

Bumps go to v7, v8, etc. The current v4 (customer portfolio handoff) and this handoff (now v6, formerly v5; advanced in the 2026-05-29 successor-model reconciliation) may be merged into a future unified version — the next integer available at merge time, not "v6" — that merge requires the v4 author or v4 doc in front of the author to faithfully carry the customer-portfolio detail.

# Closing notes

The 2026-05-17 evening session + 2026-05-18 morning follow-on crystallized four things that had been carrying architectural uncertainty:

- **Workspace topology.** Was open; now answered with a pattern (audience-separation, three workspaces) that generalizes to multi-tenancy.

- **System sheet provisioning.** Was a blocker on kill_switch.py, error_log.py, scheduling.py, review_queue.py, quarantine.py, scripts/watchdog.py — all deferred to “ITS_Config + ITS_Errors + ITS_Review_Queue + ITS_Time_Off + ITS_Quarantine provisioned.” That blocker is gone; all sheets exist with schemas captured here (corrected against live state).

- **Bootstrap pattern.** Was an open architectural question (how does kill_switch find ITS_Config before reading it?); now answered with shared/sheet_ids.py, a clean separable module that generalizes.

- **smartsheet_client.py wiring.** Was the critical-path piece for everything downstream. WIRED 2026-05-18 morning, 22 tests + live smoke green. Consumer refactors now have a clean substrate.

What remains in the critical path is the consumer refactor sequence (kill_switch → error_log → review_queue → quarantine → scheduling PTO → watchdog). Each is its own focused session against the now-available primitives documented here.