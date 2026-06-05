---
type: brief
version: 2
status: canonical
last_verified: 2026-06-05
last_verified_against: ffad86b
supersedes: workstreams/safety-portal/brief.md@v1
workstream: safety_portal
tags: [workstream-brief, cloudflare-workers, static-assets, d1, hmac, python-option-b, standalone-workspace, parent-variant-forms]
---

# ITS Safety Portal — Brief v2

2026-06-05 — As-built architecture reconciliation. Companion to [mission.md](mission.md). Supersedes v1 (2026-05-25) on every point the 2026-06-04/05 build sessions changed: **Workers + Static Assets** deploy (not Pages), **Python Option-B** PDF rendering (not client-side TS), the portal **never reads or writes Smartsheet** (job/form data served from D1), **6-digit `AUTO_NUMBER` Job ID** (kebab `Job Slug` retired), **Saturday→Friday** weeks, the **`WSR_human_review`** central approval sheet, **TEXT** recipient columns, and the standalone **`ITS — Safety Portal`** workspace.

> **Altitude note.** This brief is doctrine/architecture-level. Implementation mechanics (migration line numbers, exact column lists, API call shapes, test scaffolds) live in the execution-repo briefs (`safety_portal_backhalf_cc_brief.md`, `safety_portal_phase4_forms_cc_brief.md`) and in `shared/sheet_ids.py`. Customer-0 IDs are intentionally **not** copied here (per repo `CLAUDE.md`); they live in `sheet_ids.py`.

## 1. Architecture Overview

```
┌──────────────────────┐  HTTPS   ┌──────────────────────────────────┐
│   Field PM Browser   ├─────────►│ Cloudflare Workers + Static Assets│
│ (phone / tablet /    │          │  • single Worker serves the SPA   │
│  desktop)            │          │    AND same-origin /api/*         │
│                      │          │  • D1  (jobs/forms + submissions) │
└──────────────────────┘          └───────────────┬──────────────────┘
                                                   │  HMAC-signed email shim
                                                   │  (X-ITS-Portal-* headers)
                                                   ▼
                                   ┌──────────────────────────────────┐
                                   │ safety@ (unified intake mailbox)  │
                                   └───────────────┬──────────────────┘
                                                   │ polled by the Python pipeline
                                                   ▼
                                   ┌──────────────────────────────────┐
                                   │ safety_reports/ intake (Python)   │
                                   │  • allowlist gate → HMAC verify   │
                                   │  • dedup on submission UUID       │
                                   │  • render per-submission PDF      │
                                   │    in PYTHON (Option B)           │
                                   │  • file to Box + write week-sheet │
                                   │  • fail-closed receipt callback   │
                                   │    → portal "received & filed"    │
                                   │  HOLDS THE ONLY WRITE CREDENTIALS  │
                                   └──────────────────────────────────┘
```

Two facts define the architecture:

1. **The portal never reads or writes Smartsheet.** Job and form data are served from the portal's own **D1** store (`GET /api/jobs`, `GET /api/forms`), populated from `ITS_Active_Jobs` / `ITS_Forms_Catalog` out of band. The portal has no Smartsheet credential at request time. (Verified in execution: `safety_portal/worker/index.ts` — *"Active jobs for the dropdown (from D1; the portal never reads Smartsheet)."*)
2. **The Python pipeline owns everything customer-adjacent.** It holds the only Smartsheet/Box write credentials, renders the PDF, files to Box, writes the week sheet, compiles the weekly packet, and runs the gated send. The portal hands off a signed payload and waits for a fail-closed receipt.

This is the [External Send Gate](mission.md#7-foundation-invariants-inherited) two-process model expressed as a **deployment** boundary: a compromised portal cannot reach Smartsheet, Box, Anthropic, or a customer mailbox.

## 2. Data Model (D1)

D1 holds the portal's two concerns: the **read cache** of job/form data it serves to the SPA, and the **submission receipts** that are the portal's only native durable record.

- **Job/form read cache** — populated from `ITS_Active_Jobs` + `ITS_Forms_Catalog` out of band (not a request-time Smartsheet read). The job's stable key is its **6-digit `AUTO_NUMBER` Job ID** (`JOB-000001`); `Project Name` is display. Only `Active` jobs are served. The form catalog mirrors the **parent/variant** structure (see §6).
- **Submission receipts** — one row per submission (UUID, username, Job ID, form code, work date, payload, shim status, receipt-verified flag). The **fail-closed receipt callback** flips the verified flag only after the Python pipeline confirms the submission was filed; an unconfirmed submission stays visibly pending. Dedup keys on the submission UUID.
- **Sessions** — long-lived signed cookies (90-day), signed with `SESSION_SIGNING_SECRET` (a Workers Secret); no server-side session table.

Exact DDL and column lists live in the execution brief; the load-bearing change from v1 is that the Job ID is an `AUTO_NUMBER` (`JOB-000001`), **not** a kebab slug, and that the submission record — not Smartsheet — is the portal's system of record.

## 3. Smartsheet Surfaces (read/written by the Python pipeline, not the portal)

All safety Smartsheet surfaces live in the standalone **`ITS — Safety Portal`** workspace (the `Safety Portal` folder was moved there from `ITS — Operations`, **IDs preserved**). Shared config (`ITS_Config`, `ITS_Errors`, `ITS_Trusted_Contacts`, `ITS_Review_Queue`, `ITS_Quarantine`) stays in **`ITS — System`** and is read by sheet ID — shared infra, not safety-specific.

### `ITS_Active_Jobs` — office-PM-maintained source of truth

- **`Job ID`** — 6-digit **`AUTO_NUMBER`** (`JOB-000001`). The permanent key the pipeline resolves on. **UI-created only** — the Smartsheet API cannot create `AUTO_NUMBER` columns (see [Empirical findings](#empirical-findings-durable)).
- **`Project Name`** — `TEXT`, display name.
- **Recipient contacts** — **`TEXT`** columns: Safety Reports Contact Name/Email + CC 1–5 (one email per slot or comma-separated). `MULTI_CONTACT_LIST` is deliberately **not** used because it drops external emails on API read-back (see [Empirical findings](#empirical-findings-durable)).
- **`Active`** — `PICKLIST` (`Active / Inactive / Archived`). **Gates the per-job pipeline**: only `Active` jobs run and appear in the portal.

### `ITS_Forms_Catalog` — parent/variant catalog

5 parents + 7 variants live, realized as the bundled declarative definitions (§6). Parents: JHA, Equipment Pre-Inspection, HSS&E Work Observation, Visitor Sign-In, Toolbox Talk. Variants fan out under Equipment Pre-Inspection (skid-steer, telehandler) and Toolbox Talk (5 topics). A no-variant parent renders its own definition; a variant parent collapses its variants under a **third picklist**.

### `WSR_human_review` — central weekly approval sheet (Phase 5)

NEW, in the Safety Portal folder — **not** the legacy `WPR_Pending_Review` in `ITS — Human Review`. One row per **(job, week)**:

- the compiled weekly PDF (attached);
- the **editable email body — the source of truth for the send**;
- the resolved recipients (TO + CC);
- `Approve for Scheduled Send` + `Send Now` checkboxes;
- auto-stamped Approved By / Approved At.

**Review + edit + approve + send happen only here.** This is the workstream's `<Workstream>_Pending_Review` surface under [Invariant 1](mission.md#7-foundation-invariants-inherited). The sheet was **built by Phase 5 PR 1** (PR #168, `build_wsr_human_review_sheet.py`; `SHEET_WSR_HUMAN_REVIEW` in `sheet_ids.py`); the intake/compile/send wiring that populates and reads it is the rest of Phase 5.

### Per-job week sheets

Per-job folders → week sheets (`[Job] — week of [date]`, **Saturday→Friday**), pipeline-provisioned, one row per submission. The rollup is dual-written here as a **read-only snapshot** and to `WSR_human_review` as the **editable** approval row.

## 4. Authentication

Username + **bcrypt** (`bcryptjs`, cost factor 10) against D1, under `nodejs_compat`. **This forces Workers Paid (~$5/mo)** — the free plan's 10 ms CPU cap cannot complete a cost-10 hash (observed Error 1102; see [Empirical findings](#empirical-findings-durable)). Login POSTs to a Worker route that runs `bcrypt.compare`, sets a signed 90-day session cookie, and redirects home. Username convention `lastname.firstname`. No self-registration; operator-provisioned via an admin route gated by an operator-only credential (Workers Secret); the operator types plaintext at provisioning/reset time and the backend hashes before write. Out of scope per operator decision: CSRF tokens, rate limiting, account lockout, failed-login audit log, idle timeout.

## 5. User-Facing UX

- **Login (`/`)** — username + password; generic failure message (no field enumeration).
- **Home** — work-date picker (default today; any past date; no future dates), Project dropdown (Active jobs from D1), Form dropdown filtered to the selected job with parent/variant collapse under the third picklist. Recent-submissions list shows receipt state ("received & filed" once the fail-closed callback confirms).
- **Form (`/form/...`)** — rendered by the **definition-driven TS display runtime** (PR #166): project fields prefilled from the home selection; per-form fields; tri-state equipment checklists (OK / NOT OK / N/A); repeatable worker-roster rows (Name + Company + Signature). localStorage draft persistence keyed by `{username}-{form}-{work_date}-{job_id}`.
- **Confirmation** — submission summary; receipt status; "Submit Another."
- **Amend path** — the portal prefills from its D1 cache; the submission supersedes in-sheet; Box keeps both versions.

## 6. Forms — single-source declarative definitions

Each form is one **declarative definition**, consumed **identically** by two runtimes — the **TS display runtime** (PR #166, `safety_portal/src/forms/`) and the **Python PDF renderer** (PR #167, Option B). That single source is the contract that keeps display and PDF from drifting; a meta-schema validates definitions in CI (PR #164).

- **Parent/variant catalog.** A no-variant parent renders its own definition; a variant parent has no definition of its own and collapses its variants under a third picklist. JHA supports future job-specific variants the same way.
- **Canonical = the 10 reference PDFs.** Daily Site Safety Worksheet is **out**; Visitor Sign-In + HSS&E Work Observation are **in**.
- **Tri-state equipment checklists.** OK / NOT OK / **N/A** — N/A is distinct from blank.
- **Legal-invariants-in-code.** Mandatory, non-editable lines (e.g., the JHA "if conditions change…" footer, the equipment lock/tag-out line) are part of the definition and cannot be edited away by a PM or a form author.
- **Render parity.** The Python renderer matches the Evergreen header and the paper-form layout (OSHA-inspector parity).

The AI-one-shot extension workflow (paste an existing definition into Claude, describe the change, paste the result back, CI validates, deploy, add the `ITS_Forms_Catalog` row) is unchanged in spirit from v1; the only structural change is that the definition now drives the **Python** renderer as well as the TS display.

## 7. Signature Handling

Per-row on-screen signature capture, stored as SVG path data (~0.5–3 KB). Rendered inline by the Python renderer in the worker-roster section. Optional per row; unsigned workers are counted in the weekly aggregator.

## 8. Submission Pipeline

The portal hands off; the Python pipeline runs the stages. End to end:

1. **Submit (portal).** The Worker verifies the session, validates the payload against the form definition, stores a D1 submission receipt (`pending`), and returns a submission UUID. The browser shows the confirmation page.
2. **Email shim (portal, async).** A signed message goes to `safety@` — `X-ITS-Portal-*` headers + `X-ITS-Portal-HMAC` (HMAC-SHA256 of the canonicalized payload), JSON body, sender `portal-noreply@`.
3. **Intake (Python).** Allowlist-gate the sender → **HMAC-verify** → **dedup on submission UUID**. Mismatch routes to `ITS_Quarantine` (CRITICAL). On the portal fast-path, classification/extraction is skipped (the payload is already structured).
4. **Render (Python, Option B).** The per-submission PDF is rendered server-side from the structured payload with render-parity to the Evergreen header.
5. **File + record.** Upload the PDF to Box (job/week tree, §9) and write the per-submission row to the week sheet (Box link on the row).
6. **Fail-closed receipt callback.** POST back to the portal to flip the D1 receipt to verified → the portal shows "received & filed." Unconfirmed = stays pending (fail-closed).
7. **Compile.** Triggered by a week-sheet `Compile Now` checkbox **or** automatically on Friday. **Skips if already compiled and no new docs.** Merges Sat→Fri ascending. **Never closes the week** — multiple packets per week are allowed.
8. **Dual-write the rollup.** To the week sheet (read-only snapshot) **and** to `WSR_human_review` (editable approval row).
9. **Human review.** An approver reviews/edits the email body (source of truth) and sets `Approve for Scheduled Send` / `Send Now` in `WSR_human_review`.
10. **`weekly_send` (Python, no AI step).** TO = the safety-reports contact; **CC = the non-empty CC 1–5**; Evergreen contact body-only; the **edited body is read from `WSR_human_review`**; the compiled PDF is attached. Default cadence **7 AM Pacific Monday** from an `ITS_Config` row; a watchdog retries; the resolved recipient list is logged.

**Late arrivals.** A submission whose week is already compiled/sent routes to the **next uncompiled week** plus a Review-Queue flag. A sent report is not retroactively updated; the operator decides on an addendum.

## 9. Filing — Box is the system of record

**Box is the system of record**, with a folder tree **mirroring** the Smartsheet job/week hierarchy:

```
[Box safety root]/
└── [Job]/
    └── [week of <Saturday date>]/           ← Saturday→Friday week
        ├── <submission>.pdf                  ← per-submission PDFs
        └── <compiled weekly>.pdf             ← the merged weekly packet
```

The week is the **Saturday→Friday** week containing the form work-date; weekend work rolls to the following Friday. Smartsheet rows carry Box links; the compiled weekly PDF also attaches to the `WSR_human_review` row. Evergreen retains in Box for as long as needed — there is **no OSHA-floor retention gating in our code**.

## 10. PDF Rendering — Python, Option B

The per-submission PDF and the compiled weekly PDF are rendered **server-side in Python (Option B)** — *not* client-side in the browser (the v1 client-side `_runtime/pdf_renderer.ts` plan is superseded). The renderer walks the same declarative form definition the TS display runtime uses, embeds signatures as SVG, and matches the Evergreen header for render parity. Landed in PR #167.

## 11. Deployment Topology

**Cloudflare Workers + Static Assets.** A single Worker serves the React SPA (static assets) **and** the same-origin `/api/*` backend. **Cloudflare Pages is not used** (it is in maintenance mode); any `*.pages.dev` reference is stale. **Workers Paid (~$5/mo) is required** for the bcrypt login hash (free-tier 10 ms CPU cap).

### Validation — `safety.evergreenmirror.com`

- Single Workers project serving SPA + `/api/*`; D1 bound to the Worker.
- DNS: GoDaddy-managed CNAME `safety.evergreenmirror.com` → the Cloudflare Workers custom domain (not `*.pages.dev`).
- Email shim sender `portal-noreply@evergreenmirror.com`; recipient `safety@evergreenmirror.com`.

### Production — `evergreenrenewables.com`

- Workers production project + custom domain `safety.evergreenrenewables.com`.
- Fresh D1; field PMs re-provisioned.
- Email shim sender `portal-noreply@evergreenrenewables.com`; recipient `safety@evergreenrenewables.com` (unified intake; no separate portal-submit@).

### Secrets

`SESSION_SIGNING_SECRET`, the operator admin credential, the HMAC payload secret, M365 shim credentials, and the receipt-callback bearer token are **Cloudflare Workers Secrets**; operator-side mirror copies in macOS Keychain per convention. The **Cloudflare API token used to provision is a short-lived env-var credential, revoked after provisioning — never stored in Keychain.**

## Empirical findings (durable)

Recorded so no future session re-discovers them (see also [memory-archive §G18.4 / §G19.4 / §G21](../../references/memory-archive.md)):

- **Smartsheet `AUTO_NUMBER` columns are UI-only.** The REST API rejects `type: AUTO_NUMBER` with `errorCode 1008` regardless of position or `systemColumnType`. The `Job ID` column must be created in the Smartsheet UI; code reads it once created.
- **Smartsheet `MULTI_CONTACT_LIST` drops external emails on API read-back.** Only display names come back for non-org contacts. Recipient columns (Safety Reports Contact Email, CC 1–5) therefore use **`TEXT`**, storing the literal email string.
- **Cloudflare Workers free-tier 10 ms CPU cap cannot run a secure password hash.** `bcryptjs` cost-10 exceeds it (Error 1102), forcing the **Workers Paid plan**. This is a hard deploy constraint, not a tuning choice.

## 12. Operational Conventions Honored

Per [Operational Standards](../../doctrine/operational-standards.md):

- **Kill switch first.** Portal-adjacent Workers (shim, sync) honor the `system.state` PAUSED flag.
- **Error logging.** Errors log to `ITS_Errors` with `workstream=safety_portal` and a threaded correlation id.
- **External Send Gate.** The shim sender is in `SEND_SCRIPTS`, scoped to `safety@`; `weekly_send` (no AI step) is the only customer-facing sender and reads only approved `WSR_human_review` rows.
- **Adversarial Input Handling.** Six layers + HMAC per [mission §7](mission.md#7-foundation-invariants-inherited).
- **Capability gating (post-F02).** Only enumerated modules make outbound calls; the portal has no Smartsheet/Box/Anthropic capability.
- **Credentials.** Workers Secrets + Keychain mirrors; the provisioning Cloudflare API token is short-lived and revoked.
- **Schemas in code.** Form definitions are version-controlled and CI-validated against the meta-schema.
- **Picklist hardening.** `Active` on `ITS_Active_Jobs` and the catalog status are `PICKLIST`, not free text.

## 13. Transition Plan

Two paths run in parallel until adoption is real: validation (portal voluntary, paper official) → soft launch (production portal, both paths) → deprecation announcement → sunset (legacy PDF path disabled via an `ITS_Config` flag). Legacy code remains in-tree, deactivated via flag per [preservation-over-refactor](../../doctrine/operational-standards.md).

## 14. Implementation Phases (as-built)

The as-built phase plan supersedes v1's speculative Phase 0–10 breakdown:

- **Phase 2 — front-half (LANDED, PR #158):** login + SPA + Worker scaffold.
- **Phase 3 — job model (LANDED, PR #160, #162):** live Job-ID resolution against `ITS_Active_Jobs`, the Saturday→Friday week rule, legacy `Job Slug` retired, schema + the contacts amendment (TEXT contacts + CC 1–5).
- **Phase 4 — forms (LANDED, PR #164, #166, #167):** meta-schema + parent/variant catalog + the declarative form definitions; the definition-driven TS display runtime; the Python Option-B renderer + equipment tri-state. (The definition set was revised after the PR #164 foundation; the current catalog is 5 parents + 7 variants — see [memory-archive §G21](../../references/memory-archive.md).)
- **Phase 5 — submission pipeline (IN PROGRESS):** PR 1 (back-half foundation) **landed** (PR #168, `ffad86b`) — the `WSR_human_review` sheet built, weekly PDF merge, and `sheet_ids` constants (`WORKSPACE_SAFETY_PORTAL`, `FOLDER_SAFETY_PORTAL`, `SHEET_WSR_HUMAN_REVIEW`) + amendments b/c. **Next:** the intake portal-marker branch (HMAC verify, dedup, fail-closed receipt callback) + per-submission Python render + Box filing + week-sheet write + **compile** + dual-write to `WSR_human_review` + the gated `weekly_send` (7 AM Pacific Monday) — i.e., the hybrid review model.
- **Deploy (PENDING):** D1 sync wiring, Workers Secrets, Workers Paid-plan upgrade, custom domains (validation then production).

## 15. Sequencing Dependencies

- The Phase 1.4 hardening cluster (F02/F22 capability-gating + approval attestation, F08/F09 circuit-breaker + alert cap, `shared/state_io.py`) predates and unblocks the portal pipeline; it has landed ahead of Phase 5.
- `ITS_Trusted_Contacts` must carry the `portal-noreply@` allowlist entry before Phase 5 send.
- `WSR_human_review` must be provisioned in the Safety Portal workspace before the compile/dual-write step of Phase 5 — **done** (Phase 5 PR 1 / PR #168).
- The Workers Paid-plan upgrade gates any deploy that exercises the bcrypt login path.

## 16. Open Questions Remaining

- **Smartsheet "Sync Now" / catalog→D1 sync mechanism** — how job/form data lands in D1 (cron, webhook, or pipeline push) is an execution-brief concern; the doctrine fact is only that the portal reads D1, never Smartsheet.
- **Form-specific Box subfolders** vs a single per-week folder — defer to build.
- **`WSR_human_review` exact schema + automation** (auto-stamp rules, Send-Now vs Scheduled semantics) — finalize at Phase 5 build.
- **Production D1 backfill of receipt state at cutover** — lazy vs bulk.

## Authority

ITS Safety Portal Brief v2, 2026-06-05 canonical. Supersedes v1 (2026-05-25). Companion to [mission.md](mission.md).

v3 trigger: substantive engineering-architecture change — deploy-platform change away from Cloudflare Workers, a return to client-side PDF rendering, an authentication-model swap, or a change to the portal-never-touches-Smartsheet boundary. Status-overlay updates (v2.1, v2.2) absorb phase progress.

Cross-references:
- [Mission](mission.md) — invariants (restated verbatim), audience, decisions, self-containment, phase status, risks.
- [Operational Standards](../../doctrine/operational-standards.md) — §23 topology (doctrine-reconciliation flagged), patterns honored.
- [Foundation Mission v11](../../doctrine/foundation-mission.md) — invariants inherited.
- [safety_reports brief](../safety-reports/brief.md#what-gets-built-refreshed-in-v61) — sibling workstream owning the shared pipeline (`weekly_generate` / `weekly_send`).
- [Forensic audit 2026-05-25](../../audits/2026-05-25_forensic-audit.md) — F02/F22 cluster.
- [Blueprint-update session log 2026-06-05](../../session-logs/2026-06-05_safety-portal-blueprint-update.md) — v2 decisions + doctrine-reconciliation flags.
