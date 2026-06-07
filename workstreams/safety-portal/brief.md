---
type: brief
version: 3
status: canonical
last_verified: 2026-06-07
last_verified_against: f3ad814
supersedes: workstreams/safety-portal/brief.md@v2
workstream: safety_portal
tags: [workstream-brief, cloudflare-workers, static-assets, d1, hmac, pull-transport, python-option-b, standalone-workspace, parent-variant-forms, clean-break, workspace-membership-approval, job-sync, find-or-create, mirror-deploy, box-mirror]
---

# ITS Safety Portal — Brief v3

2026-06-07 — Deploy + as-built reconciliation (exec PRs #178–#189; verified against exec main `f3ad814`). Companion to [mission.md](mission.md). v3 supersedes v2 on every point the 2026-06-06/07 deploy sessions changed: week-sheet filing **auto-provisions** at the surface of `WORKSPACE_SAFETY_PORTAL` (per-job folder → per-week sheet, find-or-create; the legacy `FIELD_REPORTS_FOLDER_BY_PROJECT` map is dropped from the portal path — §3); **`ITS_Active_Jobs` → D1 job sync** (bearer-gated `POST /api/internal/sync`, portal-poll push — §3, resolves the §16 sync Q); **F22 approval authority = Safety Portal workspace membership** (the `authorized_approvers` ITS_Config allowlist is retired — see [mission §8](mission.md#8-self-containment-and-workspace-as-approval-authority)); rendered PDFs **attached inline** on the Submission / Rollup / WSR rows (§8, supplementary — Box stays SoR); **version-on-conflict** for the recompiled weekly packet (§8/§9); the validation deploy points at the operator's **mirror D1** (`its-safety-portal-db`, custom domain `safety.evergreenmirror.com` declared in `wrangler.jsonc` — §11); the **secret map** is corrected to the as-built names (`HMAC_PAYLOAD_SECRET` / `PORTAL_INTERNAL_API_TOKEN`, not the v2 `HMAC_SECRET` / `INTERNAL_BEARER_TOKEN` — §11). **The full deploy-session batch (PRs #178–#189) is now merged:** PR-I #187 sheet styling, PR-J #188 custom domain, **PR-K #189 Box-mirrors-Smartsheet** (merged but **config-gated/live-inert** until the operator sets `safety_reports.box.portal_root_folder_id` — §9), and **PR-H #185 Phase 7 admin + server-side revocation** (now **landed**, with a 3-part live-activation gate — §4, §14). Three operator-gated **activation tracks** remain before production (§14).

**2026-06-05 — As-built architecture reconciliation (v2, retained for provenance).** Supersedes v1 (2026-05-25) on every point the 2026-06-04/05 build sessions changed: **Workers + Static Assets** deploy (not Pages), **Python Option-B** PDF rendering (not client-side TS), the portal **never reads or writes Smartsheet** (job/form data served from D1), **6-digit `AUTO_NUMBER` Job ID** (kebab `Job Slug` retired), **Saturday→Friday** weeks, the **`WSR_human_review`** central approval sheet, **TEXT** recipient columns, and the standalone **`ITS — Safety Portal`** workspace.

**2026-06-05 WSR rewire code-complete delta (verified against exec `025215d`, PRs #173–#177):** the Python-side Safety Portal pull model is **fully landed** — `portal_poll.py` (GATED), `intake.process_portal_submission`, deterministic `weekly_generate`, WSR-repointed `weekly_send`/`weekly_send_poll`, `week_sheet.py`. WPR = decommission-by-doc. Remaining = deploy + live smoke (next session). See memory-archive §G25. · **2026-06-05 transport+clean-break delta (verified against exec `753f12f`, PR #171):** the v2 **email shim is retired** — transport is now a **Python PULL model** (send-free Worker D1 queue → Mac-side `portal_poll.py` drains it; §1, §8). Safety intake is **portal-only at launch** (clean break, §8.1); `WPR_Pending_Review` is **decommissioned** in favor of `WSR_human_review`. Production-cutover facts added (§11). Phase 5 PRs 1+2 (`ffad86b`/`fc034eb`) + `intake_poll.py` retirement (PR #171) landed.

> **Altitude note.** This brief is doctrine/architecture-level. Implementation mechanics (migration line numbers, exact column lists, API call shapes, test scaffolds) live in the execution-repo briefs (`safety_portal_backhalf_cc_brief.md`, `safety_portal_phase4_forms_cc_brief.md`) and in `shared/sheet_ids.py`. Customer-0 IDs are intentionally **not** copied here (per repo `CLAUDE.md`); they live in `sheet_ids.py`.

## 1. Architecture Overview

```
┌──────────────────────┐  HTTPS   ┌──────────────────────────────────┐
│   Field PM Browser   ├─────────►│ Cloudflare Workers + Static Assets│
│ (phone / tablet /    │  POST    │  • single Worker serves the SPA   │
│  desktop)            │ /api/    │    AND same-origin /api/*         │
│                      │ submit   │  • D1 = durable, SEND-FREE queue   │
└──────────────────────┘          │    (jobs/forms + submissions+HMAC) │
                                   └──────▲─────────────────┬──────────┘
                            bearer-gated  │ PULL            │ bearer-gated
                            /api/internal/ │ (queue drain)   │ /api/internal/
                            pending  ──────┘                 │ mark-filed
                                                             │ (receipt)
                                   ┌─────────────────────────┴──────────┐
                                   │ Mac-side  portal_poll.py  daemon    │
                                   │  • PULLS pending submissions        │
                                   │  • verifies cross-language HMAC      │
                                   │    (shared/portal_hmac.py)           │
                                   │  • → intake.py portal-marker branch  │
                                   │  • render PDF (Python, Option B)     │
                                   │  • file to Box + write week-sheet    │
                                   │  • POST /api/internal/mark-filed     │
                                   │  HOLDS THE ONLY WRITE CREDENTIALS    │
                                   │  (the only external send is weekly)  │
                                   └──────────────────────────────────────┘
```

Three facts define the architecture:

1. **The portal never reads or writes Smartsheet.** Job and form data are served from the portal's own **D1** store (`GET /api/jobs`, `GET /api/forms`), populated from `ITS_Active_Jobs` / `ITS_Forms_Catalog` out of band. The portal has no Smartsheet credential at request time. (Verified: `safety_portal/worker/index.ts` — *"Active jobs for the dropdown (from D1; the portal never reads Smartsheet)."*)
2. **Transport is a Python PULL model — the Worker is send-free; there is no email shim.** On `POST /api/submit` the Worker HMAC-signs the submission and stores it atomically in **D1 as a durable, send-free queue**. A Mac-side **`portal_poll.py`** daemon PULLS pending submissions over the **bearer-token-gated `GET /api/internal/pending`**, verifies the cross-language HMAC (`shared/portal_hmac.py`), hands each to the `intake.py` portal-marker branch, and POSTs the receipt to `POST /api/internal/mark-filed`. The v1/v2 `portal-noreply@ → safety@` **email shim is retired** (decision `decision_phase5-portal-transport`). **Why the pull model:** a TS email shim transmits from the edge, *outside* the Python AST capability-gate (`tests/test_capability_gating.py`) — the pull model keeps the Worker send-free and puts all transmission on the Python side, which **is** inside the gate, so it *closes* that trust-boundary gap rather than papering it. It also has **no silent-loss failure mode**: the D1 write is a local, always-on Cloudflare op, so a submission made while the Mac is offline is drained on the next poll — a shim email could age out or quarantine and vanish.
3. **The Python side owns everything customer-adjacent.** `portal_poll.py` + `intake.py` hold the only Smartsheet/Box write credentials, render the PDF, file to Box, write the week sheet, compile the weekly packet, and run the gated send. The **only external send is `weekly_send`** — a separate, human-approved process.

This is the [External Send Gate](mission.md#7-foundation-invariants-inherited) two-process model expressed as a **deployment** boundary: the Worker is structurally send-free, and a compromised portal cannot reach Smartsheet, Box, Anthropic, or a customer mailbox.

## 2. Data Model (D1)

D1 holds the portal's two concerns: the **read cache** of job/form data it serves to the SPA, and the **submission receipts** that are the portal's only native durable record.

- **Job/form read cache** — populated from `ITS_Active_Jobs` + `ITS_Forms_Catalog` out of band (not a request-time Smartsheet read). The job's stable key is its **6-digit `AUTO_NUMBER` Job ID** (`JOB-000001`); `Project Name` is display. Only `Active` jobs are served. The form catalog mirrors the **parent/variant** structure (see §6).
- **Submission receipts** — one row per submission (UUID, Job ID, form code, work date, payload, **HMAC**, `box_verified` / `filed_at` receipt fields, `box_link`). The Worker stores the row on `POST /api/submit`; the Mac-side `portal_poll.py` drains it via `GET /api/internal/pending` and, after the Python pipeline files it, calls `POST /api/internal/mark-filed` to flip `box_verified` / `filed_at` — **fail-closed**, so an unconfirmed submission stays visibly pending. Dedup keys on the submission UUID.
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

### Per-job week sheets — auto-provisioned (find-or-create, PR-C #181)

Per-job folders → week sheets (`[Job] — week of [date]`, **Saturday→Friday**), one row per submission. As of PR-C (#181, exec `361bbb9`) the pipeline **auto-provisions** these at the **surface of `WORKSPACE_SAFETY_PORTAL`** (`safety_reports/week_sheet.py`): `ensure_week_sheet` find-or-creates a **per-job folder** (`find_folder_by_name_in_workspace` → `create_folder_in_workspace` against the workspace directly — the per-job folder is a **sibling** of the `Safety Portal` / `Form Catalog` folders, **not** nested inside `FOLDER_SAFETY_PORTAL`), then find-or-creates the **per-week sheet** inside it, then writes the row. Both create legs re-find after create and WARN-log a race-duplicate (`week_sheet_folder_race_duplicate` / `week_sheet_race_duplicate`) rather than strand. **No hardcoded per-project folder map** is on this path: the legacy `FIELD_REPORTS_FOLDER_BY_PROJECT` mapping (and its old `except KeyError → project_no_field_reports_folder` strand branch) is **dropped from the portal path** — that map survives only for the dormant Monday-ISO email scaffold in `week_folder.py` (see [safety-reports brief §What Gets Built](../safety-reports/brief.md)). Provisioning failures **surface, never strand**: a transient `SmartsheetError` on create propagates → the submission soft-fails to `error` and re-pulls next cycle; a permanent refusal routes to `ITS_Review_Queue`. The rollup is dual-written here as a **read-only snapshot** and to `WSR_human_review` as the **editable** approval row. This is the **find-or-create-not-strand** pattern proposed for [Operational Standards](../../doctrine/operational-standards.md) this cycle.

### `ITS_Active_Jobs` → D1 job sync (PR-D #182)

The portal serves its job dropdown from D1, never Smartsheet — and as of PR-D (#182, exec `053d627`) that D1 cache is kept current by a **push from the Python side**, resolving the v2 "Sync Now mechanism TBD" open question (§16). `portal_poll.py` (`_push_active_jobs`, each cycle, best-effort/fenced so a sync failure never blocks intake) reads `active_jobs.list_all_jobs()` and POSTs `[{job_id, project_name, active}]` to the bearer-gated **`POST /api/internal/sync`** (`shared/portal_client.push_jobs`, `SYNC_PATH`). The Worker does a **full-replace** in one `DB.batch()` (upsert each row + deactivate any active D1 `job_id` absent from the payload), with a **never-wipe guard** (empty payload → `400 empty_jobs`; the Mac side also skips an empty set). `GET /api/jobs` then serves `WHERE active = 1` to the SPA. So a new `ITS_Active_Jobs` row reaches the dropdown within one poll cycle. This is a **control-plane write to our own Worker's D1**, not a customer-facing transmission — outside the [External Send Gate](mission.md#7-foundation-invariants-inherited) (Invariant 1), which governs external sends. `active_jobs` has **no hardcoded job fallback** (a read miss returns the empty set → portal-poll skips the push → the dropdown is never wiped; contrast `project_routing`'s `BOX_PROJECT_FOLDERS`, which deliberately *does* keep a fallback).

## 4. Authentication

Username + **bcrypt** (`bcryptjs`, cost factor 10) against D1, under `nodejs_compat`. **This forces Workers Paid (~$5/mo)** — the free plan's 10 ms CPU cap cannot complete a cost-10 hash (observed Error 1102; see [Empirical findings](#empirical-findings-durable)). Login POSTs to a Worker route that runs `bcrypt.compare`, sets a signed 90-day session cookie, and redirects home. Username convention `lastname.firstname`. No self-registration; operator-provisioned via an admin route gated by an operator-only credential (Workers Secret); the operator types plaintext at provisioning/reset time and the backend hashes before write. Out of scope per operator decision: CSRF tokens, rate limiting, account lockout, failed-login audit log, idle timeout.

**Phase 7 admin + server-side revocation — LANDED (PR-H #185, merged on exec main `f3ad814`).** Now in `main` (byte-equal to the verified branch). The merged code is **live-inert until the operator runs the 3-part activation gate below** — until then the deployed Worker still runs pre-Phase-7 code and D1 lacks `users.disabled`.

- Five bearer-gated routes `POST/GET /api/internal/admin/users[/reset|/disable|/enable]` under a `requireAdminToken` middleware guarded by the **separate** `PORTAL_ADMIN_API_TOKEN` (privilege separation — the poller's token cannot create/reset/disable users); fail-closed (`safeTokenEqual`) when the secret is unset.
- A Mac operator CLI `safety_reports/portal_admin.py` with subcommands **`add-user` / `reset-password` / `disable-user` / `enable-user` / `list-users`** (operator-run, `getpass`; bearer from Keychain `ITS_PORTAL_ADMIN_TOKEN`). The CLI sends plaintext over the bearer channel; the **backend** bcrypt-hashes (cost 10) — plaintext is never stored on the Mac, returned, or logged (the CLI prints status + known args only, never the raw response).
- **Server-side session revocation:** `requireSession` adds a per-request D1 check `SELECT disabled FROM users WHERE username = ?` — a missing or `disabled` user → `401 revoked` (and any D1 error → `401`, fail-closed). Migration **`0006_add_user_disabled.sql`** adds `users.disabled INTEGER NOT NULL DEFAULT 0`.
- **3-part live-activation gate** (operator, before it takes effect on the live deployment): (1) set `PORTAL_ADMIN_API_TOKEN` (Worker) + `ITS_PORTAL_ADMIN_TOKEN` (Keychain) **byte-equal**; (2) apply migration **0006** to the live D1 **before** redeploying the Worker (else `requireSession`'s `disabled` read errors → 401s every session); (3) redeploy the Worker. The successor-operator runbook for this CLI is [Handover Plan v9 Step 8](../../doctrine/handover-plan.md).

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

1. **Submit (portal, send-free).** The Worker verifies the session, validates the payload against the form definition, **HMAC-signs** it (`HMAC_SECRET`), stores a D1 submission row (unfiled), and returns the UUID. The browser shows the confirmation page. The Worker performs no transmission.
2. **Pull (Mac-side `portal_poll.py`).** The daemon polls the **bearer-gated `GET /api/internal/pending`** queue drain and, for each row, **verifies the HMAC** via `shared/portal_hmac.py` (cross-language, constant-time `compare_digest`). HMAC mismatch → rejected/flagged, never filed. (The endpoint fail-closes 503 if the Worker's `HMAC_SECRET` is unset.)
3. **Intake (Python portal-marker branch).** **Dedup on submission UUID.** The payload is already structured, so the email-PDF path's Anthropic classify/extract stages are skipped for portal submissions.
4. **Render (Python, Option B).** The per-submission PDF is rendered server-side from the structured payload with render-parity to the Evergreen header.
5. **File + record.** Upload the PDF to Box (§9) and write the per-submission row to the week sheet (Box link on the row). **Inline copy (PR-F #184):** the rendered PDF is also attached **inline on the Submission row** via `smartsheet_client.attach_pdf_to_row` (replace-same-named, breaker-guarded) so a reviewer sees it without a Box round-trip. This is **supplementary and best-effort** — Box stays the System of Record (the row's Box-link cell is unchanged, the weekly compile still reads PDFs from Box), and an attach failure logs `row_pdf_attach_failed` (WARN) without failing the filing.
6. **Receipt.** `portal_poll.py` POSTs `/api/internal/mark-filed`, flipping `box_verified` / `filed_at` on the D1 row → the portal shows "received & filed." **Fail-closed:** unconfirmed stays pending.
7. **Compile (deterministic, LLM-free).** Triggered by a week-sheet `Compile Now` checkbox **or** automatically on Friday. The weekly product is a **deterministic merge** (`form_pdf.merge_pdfs`) of the week's per-submission PDFs **+ a fixed-template email body — no Anthropic / LLM call** (the prior Anthropic-drafted-narrative WPR is retired with the portal cutover; LLM stays in scope for *other* workstreams only). **Skips if already compiled and no new docs.** Merges Sat→Fri ascending. **Never closes the week** — multiple packets per week are allowed. The compiled packet is uploaded to Box with **version-on-conflict** (PR-G #186): a recompile (Compile-Now / late submission) re-produces the **same deterministic packet filename**, so `box_client.upload_bytes_or_new_version` resolves the existing file on a 409 and uploads a **new Box version** (stable id, preserving Box's file-version history — the SoR) rather than 409-failing the recompile or accumulating suffixed copies. (A 409 whose conflicting file then vanishes re-raises rather than swallowing.)
8. **Dual-write the rollup.** To the week sheet (read-only snapshot) **and** to `WSR_human_review` (editable approval row — the Email Body **seeded from a fixed template**, not LLM-drafted). The compiled packet is **attached inline (PR-F)** on **both** the week-sheet Rollup row **and** the `WSR_human_review` row (same supplementary best-effort `attach_pdf_to_row` as step 5; Box stays SoR).
9. **Human review.** An approver reviews/edits the email body (source of truth) and sets `Approve for Scheduled Send` / `Send Now` in `WSR_human_review`.
10. **`weekly_send` (Python, no AI step).** TO = the safety-reports contact; **CC = the non-empty CC 1–5**; Evergreen contact body-only; the **edited body is read from `WSR_human_review`**; the compiled PDF is attached. Default cadence **7 AM Pacific Monday** from an `ITS_Config` row; a watchdog retries; the resolved recipient list is logged.

**Late arrivals.** A submission whose week is already compiled/sent routes to the **next uncompiled week** plus a Review-Queue flag. A sent report is not retroactively updated; the operator decides on an addendum.

### 8.1 Clean break — safety intake is portal-only at launch

Evergreen cuts over all-at-once with **no integration of the legacy email-PDF system** — no Evergreen safety data flows the old path. So the safety intake is **portal-only**: the email-PDF safety intake path is **retired** as Evergreen's safety input, and `intake_poll.py` (the Microsoft Graph mailbox poller) is superseded by `portal_poll.py` for the safety workstream. `WPR_Pending_Review` is **decommissioned**; everything unifies on `WSR_human_review`. (This resolves the v2 `WPR_Pending_Review` → `WSR_human_review` drift flag.)

**Scope boundary — this is NOT an email teardown.** The email *infrastructure* is **preserved** — `shared/graph_client.py` (list_inbox / mark_read / GraphError / MSAL), `shared/untrusted_content.py`, `shared/header_forgery.py` — because the **Email Triage** workstream (a committed future workstream) depends on it. `intake.py` **stays**: it gains a portal-marker branch driven by `portal_poll.py`, while its email/Graph `process_message` path remains in-tree (deactivated as the *safety* input; available to Email Triage).

**Code state (exec `025215d`, PRs #173–#177):** **Python-side CODE-COMPLETE.** All five Phase-5 Python PRs landed four-part-verified, CodeQL-clean. `portal_poll.py` is GATED (not loaded as a launchd job). `weekly_generate`, `weekly_send`, `weekly_send_poll` are all WSR-repointed; WPR = decommission-by-doc (no live runtime reference). `~/its` working-tree is behind origin/main pending the deploy-session `git pull`. **Remaining:** deploy + live smoke (see memory-archive §G25.8 checklist).

## 9. Filing — Box is the system of record

**Box is the system of record.** The Box tree **mirrors the Smartsheet job/week hierarchy** (PR-K #189, exec `ecb06d9`) — but the mirror is **config-gated and live-inert by default**: it activates only once the operator creates the root Box folder and sets the gate key, otherwise the code falls back to the legacy per-job category layout.

### Mirror tree — PR-K #189 (merged, config-gated)

When the gate key is set, both writers (per-submission `intake` and the weekly `weekly_generate` packet) file into the **same** tree:

```
[Box root]/                                   ← ITS_Config: safety_reports.box.portal_root_folder_id
└── [Job]/                                     ← safety_naming.job_folder_name(project)
    └── week of <Saturday date>/               ← safety_naming.week_label(work_date)  (Sat→Fri)
        ├── <submission>.pdf                   ← per-submission PDFs
        └── <compiled weekly>.pdf              ← the merged weekly packet (sibling of its week's PDFs)
```

- **The root is an `ITS_Config` row**, key **`safety_reports.box.portal_root_folder_id`** (constant `safety_naming.CFG_BOX_PORTAL_ROOT`), read at runtime via `smartsheet_client.get_setting`. There is **no hardcoded root id** in the code (the earlier-circulated `388017263015` / `safety_reports.box.safety_portal_root_folder_id` are *not* how PR-K was built — neither appears anywhere in the repo).
- **`shared/safety_naming.py`** is the single source of truth for the names — `job_folder_name(project)` (sanitize: drop non-printable, `/`→`-`) and `week_label(date)` (Saturday-keyed `"week of <iso>"`). `week_sheet.py` (the Smartsheet side) delegates to the **same** helpers, so the Box per-job folder + per-week folder and the Smartsheet per-job folder + week-sheet name are **byte-identical** — that is what "mirrors Smartsheet" means concretely. Folders are race-tolerant find-or-create (`box_client.get_or_create_folder`, 409-adopt), so a **brand-new job self-provisions** at every level and **never strands** (the headline new-job fix). **Category subfolders are dropped** on this path.
- **Config-gate (load-bearing):** with the key **unset/blank the mirror is OFF** and the legacy path (below) runs — so merging/pulling PR-K is **inert** until the operator (a) creates the root Box folder and (b) sets the `ITS_Config` key. A deliberate design choice so the live system-of-record filing path is not switched without operator intent.

### Legacy fallback (gate OFF) + the dormant email path

When the gate key is unset, the per-submission PDF files into the job's **existing per-job category subfolder** (`project_routing.get_folder_id` → `PORTAL_FORM_CATEGORY` → `BOX_SUBPATH_BY_CATEGORY`), with a per-job `ITS Portal Submissions` fallback — the pre-PR-K behavior, **preserved** (this same `project_routing`/category machinery is the live shared infra also used by the dormant email path; see [safety-reports brief §Email-intake path](../safety-reports/brief.md)).

### Versioning + retention

**Version-on-conflict is packet-only** (PR-K changed *which folder* each writer targets, not the upload primitives): the compiled packet uses `box_client.upload_bytes_or_new_version` (new Box version on a deterministic-name 409, §8 step 7); the per-submission upload keeps **suffix-on-409** (`<date>-<type>.pdf` → `<date>-<type>-<uuid8>.pdf`, each amend a distinct document). Smartsheet rows carry Box links; the compiled packet also attaches inline to the Rollup + `WSR_human_review` rows (§8). Evergreen retains in Box as long as needed — **no OSHA-floor retention gating in our code**. (Pre-activation submissions filed under the legacy category layout are **pre-launch sandbox orphans** — no migration, validation-tenant; exec tech-debt.)

## 10. PDF Rendering — Python, Option B

The per-submission PDF and the compiled weekly PDF are rendered **server-side in Python (Option B)** — *not* client-side in the browser (the v1 client-side `_runtime/pdf_renderer.ts` plan is superseded). The renderer walks the same declarative form definition the TS display runtime uses, embeds signatures as SVG, and matches the Evergreen header for render parity. Landed in PR #167.

## 11. Deployment Topology

**Cloudflare Workers + Static Assets.** A single Worker serves the React SPA (static assets) **and** the same-origin `/api/*` backend. **Cloudflare Pages is not used** (it is in maintenance mode); any `*.pages.dev` reference is stale. **Workers Paid (~$5/mo) is required** for the bcrypt login hash (free-tier 10 ms CPU cap).

### Validation — `safety.evergreenmirror.com` (the operator's mirror, NOT the Evergreen cutover)

The first remote deploy targets the operator's **mirror/validation** Cloudflare environment (the sandbox tenant `evergreenmirror.com`), explicitly **distinct from and prior to** the Evergreen production cutover (§"Production cutover"). **"Live" here means the mirror is fully functional + admin-controllable + edge-case-proven — it is NOT the Evergreen cutover.**

- Single Workers project serving SPA + `/api/*`; D1 bound to the Worker. As of PR-B (#180, exec `df549df`) `wrangler.jsonc` points `binding: DB` at the **live mirror D1** `its-safety-portal-db` (`database_id 924f142b-c812-49fd-a262-2eb6fb34fe95`, region ENAM); the all-zeros placeholder is gone. The Cloudflare **account** is supplied at deploy via `CLOUDFLARE_ACCOUNT_ID` (no committed account id) — "account = mirror" is asserted by the D1 comments + the `safety.evergreenmirror.com` custom-domain choice, not a hard-coded field.
- **Custom domain declared (PR-J #188, merged `6c1993d`):** `safety_portal/wrangler.jsonc` now carries `"routes": [{ "pattern": "safety.evergreenmirror.com", "custom_domain": true }]` — the **Workers Custom Domain** mechanism (Cloudflare provisions the hostname + TLS for the zone on deploy; not `*.pages.dev`, not a `*.workers.dev` route). It is **declared/version-controlled but inert**: cutover is operator-gated on an explicit `wrangler deploy` (or dashboard custom-domain add) under Cloudflare auth — not auto-activated on merge. The SPA uses relative paths + a host-default cookie, so no rebuild is needed.
- **Sheet styling baked in (PR-I #187, merged `53c27ac`):** week-sheet creation applies `WEEK_SHEET_STYLES` (column widths, bold dark-green primary, `MMM D YYYY` date) best-effort (create-path only, never blocks the data path); status cells are colored at write time (Active=green / Superseded=gray) via an additive `_formats` meta key; a one-time `scripts/style_safety_portal_sheets.py` backfilled existing sheets (ran live: 3 static + 7 week sheets). Colors are **palette-approximated** (Smartsheet has no exact hex; brand `#3a5a40` → palette indices, off `GET /serverinfo`); status coloring is **per-cell write-time formatting**, not Smartsheet conditional-format *rules* (those are UI-only / unavailable via the API). New primitive `smartsheet_client.apply_column_styles` (POST ignores width/format → applied via a column PUT; format must be set via the SDK model attribute, not the dict constructor — a live-verified gotcha, exec tech-debt).
- **Mac-side daemon deploy-wired (PR-A #179):** `portal_poll.py` is now a real launchd daemon — plist `org.solutionsmith.its.portal-poll` (`StartInterval`, default 60 s, `RunAtLoad=false`, `Background`, invokes only `python -m safety_reports.portal_poll` — no send/transport import), installed by `scripts/launchd/install.sh`, with **watchdog Check-C** silent-death coverage via a matched `safety_portal_poll.last_run` marker on a **5-minute** (~5-cycle) freshness window. (Minor known lag: a stale "registration deferred" comment in `portal_poll.py` — tracked as exec tech-debt.)
- **No email endpoint** — transport is the send-free D1 queue + Mac-side pull (§1, §8). The portal provisions no mailbox.

### Production cutover — `safety.evergreenrenewables.com`

Applicable **at cutover, not now.** Evergreen cuts over all-at-once (clean break, no legacy-system integration — see §8.1):

- Workers production project + custom domain `safety.evergreenrenewables.com`; fresh D1; field PMs re-provisioned.
- **Evergreen has no Cloudflare account today.** One is created fresh at cutover and is **Evergreen-owned** (the Daniel-creates-the-Evergreen-account plan).
- **Evergreen's website is GoDaddy-hosted WordPress + Elementor; the apex `evergreenrenewables.com` DNS and the M365 email both live on GoDaddy.** Do **not** migrate the apex zone. Attach **only** `safety.evergreenrenewables.com` to Cloudflare — **likely via subdomain NS-delegation** at GoDaddy (delegate just that label's NS records to Cloudflare), leaving the WordPress site and M365 email untouched. The exact subdomain-attach mechanism is resolved at deploy prep — **likely path, not locked.**
- No email infrastructure is provisioned for the portal — the pull transport needs none.

### Secrets — the as-built secret map (verified `f3ad814`)

All portal secrets are **Cloudflare Workers Secrets** (never committed; `.dev.vars` locally); the Mac side mirrors only the two the poller needs into the **macOS Keychain** (distinct names on purpose). The v2 brief named these `HMAC_SECRET` / `INTERNAL_BEARER_TOKEN`; the as-built names are below.

| Worker Secret | macOS Keychain mirror | Purpose | Fail-mode if unset |
|---|---|---|---|
| `PORTAL_INTERNAL_API_TOKEN` | `ITS_PORTAL_INTERNAL_TOKEN` | bearer gate on `/api/internal/*` (queue drain, mark-filed, job sync) | `401` |
| `HMAC_PAYLOAD_SECRET` | `ITS_PORTAL_HMAC_SECRET` | HMAC-signs each `/api/submit` payload; the poller re-verifies | `503 server_misconfigured` (fail-closed) |
| `SESSION_SIGNING_SECRET` | **Worker-only** (no Mac mirror) | signs the 90-day session cookie | — |
| `PORTAL_ADMIN_API_TOKEN` | `ITS_PORTAL_ADMIN_TOKEN` | **PR-H #185 (landed):** bearer gate on `/api/internal/admin/*`, **separate** from the poller token (privilege separation); set byte-equal at activation (§4) | `401` |

- The two mirrored pairs must be set **byte-equal** on both sides; `SESSION_SIGNING_SECRET` is Worker-only.
- The **Cloudflare API token used to provision is a short-lived env-var credential, revoked after provisioning — never stored in Keychain.**
- **Send-leg config seeds** live as **`ITS_Config` Smartsheet rows** (not checked-in files): `safety_reports.weekly_send.from_mailbox` (default `safety@evergreenmirror.com`), `safety_reports.weekly_send.scheduled_send_local` (default `"MON 07:00"`, interpreted Pacific / `America/Los_Angeles`), `safety_reports.weekly_send.polling_enabled` (default `true`). Note the `.polling_enabled` suffix is per-daemon: `weekly_send`, `portal_poll`, and `intake` each have their own kill-switch row.

## Empirical findings (durable)

Recorded so no future session re-discovers them (see also [memory-archive §G18.4 / §G19.4 / §G21](../../references/memory-archive.md)):

- **Smartsheet `AUTO_NUMBER` columns are UI-only.** The REST API rejects `type: AUTO_NUMBER` with `errorCode 1008` regardless of position or `systemColumnType`. The `Job ID` column must be created in the Smartsheet UI; code reads it once created.
- **Smartsheet `MULTI_CONTACT_LIST` drops external emails on API read-back.** Only display names come back for non-org contacts. Recipient columns (Safety Reports Contact Email, CC 1–5) therefore use **`TEXT`**, storing the literal email string.
- **Cloudflare Workers free-tier 10 ms CPU cap cannot run a secure password hash.** `bcryptjs` cost-10 exceeds it (Error 1102), forcing the **Workers Paid plan**. This is a hard deploy constraint, not a tuning choice.

## 12. Operational Conventions Honored

Per [Operational Standards](../../doctrine/operational-standards.md):

- **Kill switch first.** The Mac-side daemons (`portal_poll.py`, `weekly_send`) honor the `system.state` PAUSED flag read from `ITS_Config`; the Worker is send-free and holds no pipeline state, so a pause stops filing and sending without touching capture.
- **Error logging.** Errors log to `ITS_Errors` with `workstream=safety_portal` and a threaded correlation id.
- **Liveness (watchdog Check-C).** `portal_poll` writes a `safety_portal_poll.last_run` marker each cycle; the watchdog's Check-C marker-file staleness floor covers it on a 5-minute window (PR-A #179), so a dead puller surfaces — consistent with the [§31 polling-daemon](../../doctrine/operational-standards.md) primitive.
- **External Send Gate.** The **Worker is send-free** (no transmission capability — no Graph/Resend, verified in `worker/index.ts`); `portal_poll.py` is a *puller* (also send-free) inside the Python AST capability-gate; `weekly_send` (no AI step) is the **only** customer-facing sender and reads only approved `WSR_human_review` rows.
- **Adversarial Input Handling.** Six layers + per-submission HMAC per [mission §7](mission.md#7-foundation-invariants-inherited).
- **Capability gating (post-F02).** Only enumerated Python modules make outbound calls; the portal Worker has no Smartsheet/Box/Anthropic/send capability. (Known gap, W2: the TS Worker's `/api/internal/*` endpoints sit outside the Python AST scan — tracked in exec `docs/tech_debt.md`; the send-free design bounds the exposure.)
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
- **Phase 5 — submission pipeline (Python-side CODE-COMPLETE, `025215d`):**
  - **PR 1 landed** (PR #168, `ffad86b`) — `WSR_human_review` sheet, weekly PDF merge, `sheet_ids` constants (`WORKSPACE_SAFETY_PORTAL`, `FOLDER_SAFETY_PORTAL`, `SHEET_WSR_HUMAN_REVIEW`) + amendments b/c.
  - **PR 2 landed** (PR #169, `fc034eb`) — the **Worker-side pull transport**: `/api/submit` HMAC-signs each submission; bearer-gated `/api/internal/pending` (queue drain, `timingSafeEqual`, fail-closed 503 if `HMAC_SECRET` unset) + `/api/internal/mark-filed` (receipt); the cross-language `shared/portal_hmac.py` contract. Worker remains send-free.
  - **PRs #173–#177 landed** — full Python-side WSR rewire. `shared/portal_client.py` + `box_client.upload_bytes/get_or_create_folder` + `form_pdf.load_definition` + `week_sheet.py`; `intake.process_portal_submission` + `portal_poll.py` (GATED); deterministic `weekly_generate` (Anthropic narrative RETIRED); `weekly_send`/`weekly_send_poll` WSR-repointed; `wsr_review.py`; WPR decommission-by-doc. See memory-archive §G25.
- **Phase 6 — deploy wiring + as-built filing (LANDED, PRs #178–#188):** the deploy-session cluster — PR-A (#179) `portal_poll` launchd + `install.sh` + watchdog Check-C; PR-B (#180) `wrangler.jsonc` → mirror D1; PR-C (#181) week-sheet filing relocated to `WORKSPACE_SAFETY_PORTAL` (find-or-create, §3); PR-D (#182) `ITS_Active_Jobs` → D1 sync (§3); PR-E (#183) F22 approval = workspace membership; PR-F (#184) inline-PDF attach on Submission/Rollup/WSR rows (§8); PR-G (#186) Compile-Now Box-409 → version-on-conflict (§8/§9); **PR-I (#187)** sheet brand styling (§11); **PR-J (#188)** custom-domain declaration (§11). (Plus #178 — a UI fix dropping the stray "+ Add row" button.)
- **Phase 7 — admin + revocation (LANDED, PR-H #185, exec `f3ad814`):** bearer-gated `/api/internal/admin/*` under `PORTAL_ADMIN_API_TOKEN` + Mac CLI `portal_admin.py` + server-side `requireSession` disabled-check + migration `0006` (§4). Merged; live-inert until the 3-part activation gate.
- **Box-mirror SoR (LANDED, PR-K #189, exec `ecb06d9`):** config-gated Box-mirrors-Smartsheet (§9). Merged; live-inert until the operator creates the root Box folder + sets `safety_reports.box.portal_root_folder_id`.
- **Three operator activation tracks remain before production-ready** (all merged-but-inert): **(a) Admin route** — set byte-equal admin tokens, apply migration 0006 to live D1 *before* redeploy, redeploy. **(b) Box mirror tree** — create the root Box folder, set the `ITS_Config` key. **(c) Custom domain** — `wrangler deploy` / dashboard custom-domain add under Cloudflare auth. Pre-activation portal Box filings (legacy category layout) are pre-launch sandbox orphans (no migration; validation-tenant). The **Evergreen production** cutover (Evergreen-owned Cloudflare account, fresh D1, re-provisioned PMs, `safety.evergreenrenewables.com` via subdomain NS-delegation) remains a separate, later step (§11 production cutover).

## 15. Sequencing Dependencies

- The Phase 1.4 hardening cluster (F02/F22 capability-gating + approval attestation, F08/F09 circuit-breaker + alert cap, `shared/state_io.py`) predates and unblocks the portal pipeline; it has landed ahead of Phase 5.
- The pull transport authenticates by `HMAC_PAYLOAD_SECRET` (payload HMAC) + `PORTAL_INTERNAL_API_TOKEN` (the `/api/internal/*` bearer) — see the §11 secret map — **no `ITS_Trusted_Contacts` entry is needed for the portal path** (there is no inbound portal email; the prior `portal-noreply@` allowlist requirement is retired with the email shim).
- `WSR_human_review` must be provisioned in the Safety Portal workspace before the compile/dual-write step of Phase 5 — **done** (Phase 5 PR 1 / PR #168).
- The Workers Paid-plan upgrade gates any deploy that exercises the bcrypt login path.

## 16. Open Questions Remaining

- ~~**Smartsheet "Sync Now" / catalog→D1 sync mechanism**~~ — **RESOLVED (PR-D #182):** the job sync is a **pipeline push** — `portal_poll` POSTs the full `ITS_Active_Jobs` set to the bearer-gated `POST /api/internal/sync` each cycle (full-replace, never-wipe-on-empty); see §3. (Form/catalog → D1 sync remains an execution-brief detail; the doctrine fact is unchanged — the portal reads D1, never Smartsheet.)
- ~~**Form-specific Box subfolders vs a single per-week folder**~~ — **RESOLVED (PR-K #189, §9):** the merged Box-mirror **drops** the category subfolders for a per-job → per-week tree (config-gated); the legacy category layout survives only as the gate-OFF / dormant-email fallback.
- **`WSR_human_review` exact schema + automation** (auto-stamp rules, Send-Now vs Scheduled semantics) — execution-brief detail; the send leg + F22 gate are landed.
- **F22 workspace-owner inclusion** — whether the workspace **owner** appears in the resolved approver set is an **unstated dependency on the Smartsheet `/shares` response** (no owner-injection logic exists in code); group-share member expansion is a known pre-prod gap (group shares yield no email → excluded → fail-closed). See [mission §8](mission.md#8-self-containment-and-workspace-as-approval-authority).
- **Production D1 backfill of receipt state at cutover** — lazy vs bulk.

## Authority

ITS Safety Portal Brief v3, 2026-06-07 canonical. Supersedes v2 (2026-06-05). Companion to [mission.md](mission.md). Verified against exec main `f3ad814` (the full deploy-session batch PRs #178–#189 merged). Workstream briefs are frontmatter-versioned (not git-tagged).

v4 trigger: substantive engineering-architecture change — deploy-platform change away from Cloudflare Workers, a return to client-side PDF rendering, an authentication-model swap, or a change to the portal-never-touches-Smartsheet boundary. **Open as v3.x status overlays:** the three operator **activation tracks** (admin route, Box mirror tree, custom domain — all merged-but-inert, §14) and the Evergreen production cutover. Status-overlay updates (v3.1, v3.2) absorb activation/phase progress.

Cross-references:
- [Mission](mission.md) — invariants (restated verbatim), audience, decisions, self-containment, phase status, risks.
- [Operational Standards](../../doctrine/operational-standards.md) — §23 topology (doctrine-reconciliation flagged), patterns honored.
- [Foundation Mission v11](../../doctrine/foundation-mission.md) — invariants inherited.
- [safety_reports brief](../safety-reports/brief.md#what-gets-built-refreshed-in-v61) — sibling workstream owning the shared pipeline (`weekly_generate` / `weekly_send`).
- [Forensic audit 2026-05-25](../../audits/2026-05-25_forensic-audit.md) — F02/F22 cluster.
- [Blueprint-update session log 2026-06-05](../../session-logs/2026-06-05_safety-portal-blueprint-update.md) — v2 decisions + doctrine-reconciliation flags.
