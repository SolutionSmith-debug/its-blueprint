---
type: brief
version: 4
status: canonical
last_verified: 2026-06-10
last_verified_against: ab920bc
supersedes: workstreams/safety-portal/brief.md@v3
workstream: safety_portal
tags: [workstream-brief, cloudflare-workers, static-assets, d1, hmac, pull-transport, python-option-b, standalone-workspace, parent-variant-forms, clean-break, workspace-membership-approval, job-sync, find-or-create, mirror-deploy, box-mirror, admin-dashboard, form-publish-pipeline, code-actuation-gate, publish-requests]
---

# ITS Safety Portal — Brief v4

**2026-06-10 — v4: admin dashboard + form-publish pipeline engineering (exec `f3ad814` → `ab920bc`, PRs #190–#258; brief-validator-checked).** This is the brief's biggest jump: it last pinned at `f3ad814` (Phase 7), so v4 absorbs **both** Phase 8 (admin dashboard) **and** Phase 9 (form editor / publish pipeline) — which the companion [mission](mission.md) already reached at v3.2 → v4. New engineering: the in-browser admin SPA + account/role model (migrations **0007** role+audit_log, **0008** submit-as attribution, **0009** `session_epoch`; §17); the **form-publish pipeline** — `publish_requests` (migration **0010**), the Worker enqueue/queue endpoints, and the Mac `publish_daemon.py` sole-actuator chain (§18); Part A/B/C + send-leg + bugfix-chain hardening (§19); the Smartsheet surface as-built map + Orphaned Reports (§3); and the portal CI job + blocking gitleaks (§17). Every engineering specific is verified against the live code at `ab920bc` (a 62-commit `brief-validator` pass) — notably the publish status vocabulary **`queued → validated → tested → merged → live → archived | failed`**, the `_actuate` orchestrator vs the `apply_publish` manifest helper, the two-bearer-token gate map (`PORTAL_INTERNAL_API_TOKEN` is **shared** by `portal_poll` + `publish_daemon`; `PORTAL_ADMIN_API_TOKEN` is separate), and the admin idle window now **30 min** (#258). The companion [mission v4](mission.md) §§13–14 carries the *doctrine* framing (the code-actuation gate + the two flags raised); this brief carries the *engineering*.

2026-06-07 — Deploy + as-built reconciliation (exec PRs #178–#189; verified against exec main `f3ad814`). Companion to [mission.md](mission.md). v3 supersedes v2 on every point the 2026-06-06/07 deploy sessions changed: week-sheet filing **auto-provisions** at the surface of `WORKSPACE_SAFETY_PORTAL` (per-job folder → per-week sheet, find-or-create; the legacy `FIELD_REPORTS_FOLDER_BY_PROJECT` map is dropped from the portal path — §3); **`ITS_Active_Jobs` → D1 job sync** (bearer-gated `POST /api/internal/sync`, portal-poll push — §3, resolves the §16 sync Q); **F22 approval authority = Safety Portal workspace membership** (the `authorized_approvers` ITS_Config allowlist is retired — see [mission §8](mission.md#8-self-containment-and-workspace-as-approval-authority)); rendered PDFs **attached inline** on the Submission / Rollup / WSR rows (§8, supplementary — Box stays SoR); **version-on-conflict** for the recompiled weekly packet (§8/§9); the validation deploy points at the operator's **mirror D1** (`its-safety-portal-db`, custom domain `safety.evergreenmirror.com` declared in `wrangler.jsonc` — §11); the **secret map** is corrected to the as-built names (`HMAC_PAYLOAD_SECRET` / `PORTAL_INTERNAL_API_TOKEN`, not the v2 `HMAC_SECRET` / `INTERNAL_BEARER_TOKEN` — §11). **The full deploy-session batch (PRs #178–#189) is now merged:** PR-I #187 sheet styling, PR-J #188 custom domain, **PR-K #189 Box-mirrors-Smartsheet** (merged but **config-gated/live-inert** until the operator sets `safety_reports.box.portal_root_folder_id` — §9), and **PR-H #185 Phase 7 admin + server-side revocation** (now **landed**, with a 3-part live-activation gate — §4, §14). Three operator-gated **activation tracks** remain before production (§14).

**2026-06-08 — v3.1 status overlay: mirror live-validation (no scope change; exec code HEAD `f3ad814` unchanged).** The three activation tracks are **closed on the operator's mirror** (`evergreenmirror.com`): admin route live (migration `0006`, byte-equal tokens, **session revocation proven**); Box mirror tree live (`safety_reports.box.portal_root_folder_id` set, `ROOT → job → week` filing active); custom domain `safety.evergreenmirror.com` live (the `custom_domain` route disabled `*.workers.dev` → `error 1042` until `worker_base_url` was repointed — [info-gap §5](../../references/claude-code-info-gap.md)). End-to-end submit → pull → intake → Box → WSR proven, and a **real unattended timed send fired and SENT** (`weekly_send_poll` Monday 07:12 PT, F22-verified, forensic-clean). The **Evergreen production cutover** is the sole remaining step. See [mission §11](mission.md) + [memory-archive §G27](../../references/memory-archive.md) + the [2026-06-08 session log](../../session-logs/2026-06-08_safety-portal-mirror-activation.md).

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

### Orphaned Reports sheet (Part C)

A portal submission whose `Job ID` is unknown (`job_not_found`) or not Active (`job_inactive`) is rerouted — in `intake.process_portal_submission` (the **LIVE** portal flow, **not** `resolve_project`, which the original reconciliation note mis-cited) — from the generic `ITS_Review_Queue` to a dedicated **Orphaned Reports** sheet + Box folder: render the PDF (reuse `form_pdf`), file to Box (version-on-conflict), write an Orphaned-Reports row (`Status=Pending`). A *structurally*-bad submission (PDF / Box failure) still falls back to `ITS_Review_Queue` with a note — never silently drained. An **empty** `job_id` (`no_job_id`) stays in `ITS_Review_Queue` (structurally ambiguous → human review), not Orphaned Reports. **Config-gated** on `SHEET_ORPHANED_REPORTS` (default `0` = OFF → reroute is a no-op; also the safe-revert switch); **activated #235 (`fbeef44`)** by flipping the constant to the live sheet. `intake.py` stays in `GATED_SCRIPTS` (send-free).

### Workspace structural snapshot (as-built map — validation mirror; `sheet_ids.py` is the authority)

The deliberate doctrine-side map requested by the 2026-06-08 state-reconciliation audit. These are the **validation-mirror** (`evergreenmirror.com`) IDs; `shared/sheet_ids.py` remains the in-repo bootstrap authority, and the brief's general no-Customer-0-IDs altitude note is relaxed **for this map only**. Every ID cross-checked against `sheet_ids.py` at `ab920bc` (`brief-validator` pass):

| Surface | Constant | ID (mirror) |
|---|---|---|
| Workspace `ITS — Safety Portal` | `WORKSPACE_SAFETY_PORTAL` | `194283417429892` |
| `Safety Portal` folder (ITS_Active_Jobs + ITS_Forms_Catalog) | `FOLDER_SAFETY_PORTAL` | `6663869084002180` |
| `ITS_Active_Jobs` | `SHEET_ACTIVE_JOBS` | `6223950341164932` |
| `ITS_Forms_Catalog` | `SHEET_FORMS_CATALOG` | `423274885369732` |
| `WSR_human_review` | `SHEET_WSR_HUMAN_REVIEW` | `5035670127988612` |
| `Orphaned Reports` (Part C) | `SHEET_ORPHANED_REPORTS` | `2577084374273924` |
| `ITS_Config` (in `ITS — System`, read by ID) | `SHEET_CONFIG` | `3072320166907780` |

Plus per-job folders + week sheets (find-or-create, above) and the **`ZZ Portal Proof`** validation job set (a mirror-only cleanup candidate at cutover). **WSR datetime columns** (`Approved At` / `Sent At`) were retyped DATE → **ABSTRACT_DATETIME** on the mirror (§19); the production cutover defers the same retype.

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
| `PORTAL_INTERNAL_API_TOKEN` | `ITS_PORTAL_INTERNAL_TOKEN` | bearer gate on `/api/internal/*` (queue drain, mark-filed, job sync, **+ publish claim/stamp**) — **shared** by `portal_poll` AND `publish_daemon` (privilege-separated only from the admin token below; see §17 gate map + §18) | `401` |
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
- **Phase 7 — admin + revocation (LANDED, PR-H #185, exec `f3ad814`):** bearer-gated `/api/internal/admin/*` under `PORTAL_ADMIN_API_TOKEN` + Mac CLI `portal_admin.py` + server-side `requireSession` disabled-check + migration `0006` (§4). Merged; **live on the mirror (2026-06-08)** — the 3-part activation gate is satisfied (v3.1 overlay; session revocation proven).
- **Box-mirror SoR (LANDED, PR-K #189, exec `ecb06d9`):** config-gated Box-mirrors-Smartsheet (§9). Merged; **live on the mirror (2026-06-08)** — root Box folder created + `safety_reports.box.portal_root_folder_id` set; `ROOT → job → week` filing active (v3.1 overlay).
- **All three operator activation tracks CLOSED on the mirror (`evergreenmirror.com`, 2026-06-08; v3.1 overlay):** **(a) Admin route** — byte-equal tokens set, migration 0006 applied to live D1 before redeploy, redeployed; session revocation proven. **(b) Box mirror tree** — root Box folder created, `ITS_Config` key set; `ROOT → job → week` filing live. **(c) Custom domain** — `safety.evergreenmirror.com` provisioned (disabled `*.workers.dev` → `error 1042` until `worker_base_url` repointed). End-to-end + a real unattended timed send confirmed (forensic-clean, F22-verified). Pre-activation portal Box filings (legacy category layout) are pre-launch sandbox orphans (no migration; validation-tenant). The **Evergreen production** cutover (Evergreen-owned Cloudflare account, fresh D1, re-provisioned PMs, `safety.evergreenrenewables.com` via subdomain NS-delegation) remains a separate, later step (§11 production cutover).
- **Phase 8 — admin dashboard (LANDED + live on mirror, PRs #193–#202, exec `b7bad5a`):** role model (migrations 0007/0008) + per-request `requireRole` + a two-tab admin SPA (submit-as + account management, atomic last-admin guard) + the first Worker-TS CI + a security audit / 11-finding hardening pass (CSP enforcing). Engineering in §17; [memory-archive §G29](../../references/memory-archive.md).
- **Phase 9 — form editor + publish pipeline (BUILT + LIVE + operator-exercised, PRs #203–#218, exec `b736691`):** the B8 Form Editor + `PublishMonitor` + `publish_requests` (migration 0010) + Worker enqueue/queue endpoints + the Mac `publish_daemon.py` sole-actuator chain + session_epoch revocation (0009) + the admin idle window. Daemon **LOADED + live**; the **incident-report create→v2→v3** chain (reqs 16–18) exercised editor→publish→deploy→submit→file end-to-end (errors=0). Engineering in §18; [memory-archive §G30](../../references/memory-archive.md).
- **Phase-9 hardening + Parts A/B/C + send-leg (LANDED + live, exec → `ab920bc`):** the publish bugfix chain (#222/#224/#236/#241/#242/#244, §G31); Part A login/session + daily D1 prune (#230, §G31); Part B `compile_now_poll` (#232/#233); Part C Orphaned Reports (#234 build / **#235** flip, §3); Form Editor UX + draft cache (#249/#250, §G32); send-leg hardening + the 12-dimension forensic audit (#247/#248/#252/#253/#245, §G33); and the admin idle window **5 → 30 min** + bounded keep-alive (#258, §G34). Engineering in §19.

## 15. Sequencing Dependencies

- The Phase 1.4 hardening cluster (F02/F22 capability-gating + approval attestation, F08/F09 circuit-breaker + alert cap, `shared/state_io.py`) predates and unblocks the portal pipeline; it has landed ahead of Phase 5.
- The pull transport authenticates by `HMAC_PAYLOAD_SECRET` (payload HMAC) + `PORTAL_INTERNAL_API_TOKEN` (the `/api/internal/*` bearer) — see the §11 secret map — **no `ITS_Trusted_Contacts` entry is needed for the portal path** (there is no inbound portal email; the prior `portal-noreply@` allowlist requirement is retired with the email shim).
- `WSR_human_review` must be provisioned in the Safety Portal workspace before the compile/dual-write step of Phase 5 — **done** (Phase 5 PR 1 / PR #168).
- The Workers Paid-plan upgrade gates any deploy that exercises the bcrypt login path.

## 16. Open Questions Remaining

- ~~**Smartsheet "Sync Now" / catalog→D1 sync mechanism**~~ — **RESOLVED (PR-D #182):** the job sync is a **pipeline push** — `portal_poll` POSTs the full `ITS_Active_Jobs` set to the bearer-gated `POST /api/internal/sync` each cycle (full-replace, never-wipe-on-empty); see §3. (Form/catalog → D1 sync remains an execution-brief detail; the doctrine fact is unchanged — the portal reads D1, never Smartsheet.)
- ~~**Form-specific Box subfolders vs a single per-week folder**~~ — **RESOLVED (PR-K #189, §9):** the merged Box-mirror **drops** the category subfolders for a per-job → per-week tree (config-gated); the legacy category layout survives only as the gate-OFF / dormant-email fallback.
- **`WSR_human_review` exact schema + automation** (auto-stamp rules, Send-Now vs Scheduled semantics) — execution-brief detail; the send leg + F22 gate are landed **and exercised end-to-end** (the incident-report E2E + a real unattended timed send), and `Approved At` / `Sent At` now carry time (ABSTRACT_DATETIME, #245, §19). Remaining is operator UI work (conditional formatting / Smartsheet automation rules), not a code gap.
- **F22 workspace-owner inclusion** — whether the workspace **owner** appears in the resolved approver set is an **unstated dependency on the Smartsheet `/shares` response** (no owner-injection logic exists in code); group-share member expansion is a known pre-prod gap (group shares yield no email → excluded → fail-closed). See [mission §8](mission.md#8-self-containment-and-workspace-as-approval-authority).
- **Production D1 backfill of receipt state at cutover** — lazy vs bulk.
- **Form publish-queue resilience** *(new, v4)* — the `publish_requests` lease columns have **no reclaim path** (a dead lease is not reclaimed) and `/api/internal/publish/stamp` enforces **no state-machine transition** (**M5**); the publish daemon has **no watchdog / `ITS_Daemon_Health` row** (**M6**) and runs git on the live tree (**M7**). The code-actuation gate's *correctness* is in place; its *resilience* layer is the open work. Tracked exec-side (Brief-1 PR-2/PR-3 + [`../its/docs/tech_debt.md`](../../../its/docs/tech_debt.md)).
- **Per-identity required-content manifest** *(new, v4)* — the legal-invariants-in-code commitment (§6; [mission §14](mission.md#14-form-management-and-publish-pipeline-as-built)) is **partially realized**: structural validation + the CI render-smoke gate are live; enforcing the JHA "if conditions change…" footer / equipment lock-tag-out line as **required content on every version** (not merely present in a seed) is **Brief-1 PR-1** (exec).

## 17. Admin dashboard & account model (as-built engineering)

Companion to [mission §13](mission.md#13-admin-dashboard-and-account-model-as-built) (doctrine). Verified against `safety_portal/worker/index.ts` + `migrations/` at `ab920bc`.

**Migration delta (0007–0010)** — each carries the same ORDER-DEPENDENCY rule as 0006 (apply to live D1 **before** the Worker redeploys, else `requireSession`'s read errors and 401s every session):

- **0007** `users.role TEXT NOT NULL DEFAULT 'submitter' CHECK (role IN ('submitter','admin'))` + `CREATE TABLE audit_log`.
- **0008** `submissions.actor_username` + `submissions.submitted_as` (submit-as attribution).
- **0009** `users.session_epoch INTEGER NOT NULL DEFAULT 0` (revocation).
- **0010** `CREATE TABLE publish_requests` with `lease_owner` / `lease_at` lease columns (§18).

**Worker endpoint inventory** (verified verbatim against `worker/index.ts`):

- **Public / session:** `POST /api/login`, `GET /api/session`, `POST /api/logout`, `GET /api/jobs`, `GET /api/recent`, `POST /api/submit`.
- **In-app admin (`adminGate` = session + role):** `GET|POST /api/admin/users`, `POST /api/admin/users/credentials`, `POST /api/admin/users/role`, `POST /api/admin/users/delete`, `POST /api/admin/publish`, `GET /api/admin/publish-status`, `POST /api/admin/publish-dismiss`, `GET /api/admin/publish-request`.
- **Internal (bearer `PORTAL_INTERNAL_API_TOKEN`):** `GET /api/internal/pending`, `POST /api/internal/mark-filed`, `POST /api/internal/sync`; publish: `GET /api/internal/publish/pending`, `POST /api/internal/publish/claim`, `POST /api/internal/publish/stamp`.
- **Operator-CLI admin (bearer `PORTAL_ADMIN_API_TOKEN`, separate):** `GET|POST /api/internal/admin/users`, `POST /api/internal/admin/users/role`, `POST /api/internal/admin/users/reset`, `POST /api/internal/admin/users/disable`, `POST /api/internal/admin/users/enable`. (Password reset here is `/users/reset` — distinct from the in-app `/api/admin/users/credentials`.)

**Gate map — three gates, TWO bearer secrets:**

- `adminGate` = cookie session (`requireSession`'s single fail-closed D1 `SELECT disabled,role,session_epoch`) + D1 role.
- `requireInternalToken` = `PORTAL_INTERNAL_API_TOKEN` — **shared** by `portal_poll` (drain / receipt / sync) AND `publish_daemon` (publish claim / stamp).
- `requireAdminToken` = `PORTAL_ADMIN_API_TOKEN` — operator provisioning CLI only (the poller/daemon token cannot create/reset/disable users; last-admin guard bypassed here as break-glass — [mission §13](mission.md#13-admin-dashboard-and-account-model-as-built)).

**Account-model mechanics.** Role authoritative from D1 (not the cookie) → demotion immediate; `coerceRole` fails safe (unknown → submitter); `session_epoch` bumped on logout + password-change (captured-cookie kill); last-admin guard atomic in-WHERE; account mutation + `audit_log` row in one atomic D1 batch.

**Prune / retention** (`worker/prune.ts`, daily cron `0 9 * * *` via `scheduled()`): filed submissions >90 d, `audit_log` >365 d, **`box_verified=0` (unfiled) NEVER evicted**, terminal publish rows via `/api/admin/publish-dismiss`.

**CI** (`.github/workflows/ci.yml`): a **`portal`** job — `tsc` (SPA + Worker) + vitest workerd pool (`@cloudflare/vitest-pool-workers` vs real Miniflare D1) + jsdom pool + SPA render-smoke (the third renderer leg) — and a separate **blocking `secrets`** gitleaks job over full history. Because the publish daemon merges on a CLEAN `mergeStateStatus`, **branch-protection required checks are load-bearing** (the Python `test` job, the `portal` job, and the `secrets` job must all be required).

## 18. Form-publish pipeline (as-built engineering)

Companion to [mission §14](mission.md#14-form-management-and-publish-pipeline-as-built) (doctrine: the code-actuation gate). Verified against `safety_reports/publish_daemon.py` + `publish_manifest.py` + `worker/index.ts` at `ab920bc`.

**State machine.** `publish_requests.status CHECK (status IN ('queued','validated','tested','merged','live','archived','failed'))` (migration 0010) is the **authoritative** vocabulary. The SPA Status Monitor renders operation-aware stepper labels via `stepsForOp(op)` (Publish → *Live · Archived · Done*; Retire → *Removed · Done*; #242).

**Enqueue → actuate.**

- **Worker** `POST /api/admin/publish` runs `publishValidation.ts` (closed vocabulary + reserved-key denylist + cross-section-unique keys + hard bounds + the parent/variant grouping guard) and, only if valid, INSERTs a `publish_requests` row. The Worker **never** touches git, the filesystem, or a deploy.
- **Daemon** `publish_daemon.py` (`org.solutionsmith.its.publish-daemon`, `StartInterval 120`, on the live `~/its` tree): `_unstrand_if_needed()` (unconditional Stage-0 self-heal, #224) → claim (`POST /api/internal/publish/claim`) → **`apply_publish`** (the pure manifest transform in `publish_manifest.py` — create / edit / add_version / delete / rollback; identity uniqueness, monotonic version, variant-mixing, rollback target) re-validated vs **live git HEAD** → **`_actuate`** (the orchestrator) commits the **append-only** form file (design **C1**) on a per-request branch + PR → `_wait_for_ci` polls `mergeStateStatus == CLEAN` (`CI_TIMEOUT_S = 900`) → `gh pr merge --squash --delete-branch` + verify merge-commit OID → `npm run deploy` (local wrangler) → liveness ping → `_regenerate_archive` (Box blank-archive, **`sys.executable`** not bare `python`, #241) → stamp (`POST /api/internal/publish/stamp`). Per-request deploy serialized per parent (design **C8**). Any error → row `failed` + monitor updated; `definition_json` retained for **"Edit & re-publish."**
- **No `--auto`:** repo auto-merge is disabled (`gh pr merge --auto` silently no-ops) and would break deploy-after-merge ordering — the daemon polls CI then merges directly (#218).

**Capability gating.** `publish_daemon.py` is in the **generation** list of `tests/test_capability_gating.py` (no Graph / Resend / SMTP / AI) — the code-actuation gate is verified at the import level exactly as the External Send Gate is.

**Open engineering gaps (tracked exec-side, [`../its/docs/tech_debt.md`](../../../its/docs/tech_debt.md)):** lease columns exist but there is **no reclaim path** (a dead lease isn't reclaimed — Brief-1 PR-2/PR-3); `/api/internal/publish/stamp` has **no state-machine transition guard** (the shared internal token can forge/revert a status — **M5**); the daemon has **zero watchdog / `ITS_Daemon_Health` coverage** (**M6**); it runs destructive git on the live tree without a lock/worktree (**M7**, mitigated by `_unstrand_if_needed`). The per-identity required-content manifest (legal-invariants-as-required-content) is **Brief-1 PR-1**.

## 19. Part A/B/C + send-leg & bugfix-chain hardening (as-built engineering)

The remainder of the window, engineering-level (Part C reroute is in [§3](#orphaned-reports-sheet-part-c)).

**Part A — login/session + idempotency (#230).** `useSubmissionId` keeps `submission_uuid` **stable across a lost-ACK retry** (A1) — the Worker `INSERT OR REPLACE` is idempotent only on a reused id; renewed on success-reset. Daily D1 prune cron (A3, §17). Poison-pill resistance already held (A4 — per-row fence + one-shot HMAC-reject). **A2 rate-limiting + A5 PBKDF2 deferred to cutover** as operator-gated config, not code (`safety_portal/README.md` "Production hardening").

**Part B — on-demand compile (#232/#233).** `compile_now_poll.py` (`org.solutionsmith.its.compile-now-poll`, 90 s) compiles a triggered job-week on demand by **reusing** `weekly_generate._compile_job_week` via an additive `selection` param (default `None` = Friday-fire-identical; non-None = partial compile of selected rows). The `Compile Now` checkbox is row-type-dependent (Rollup = compile trigger; Submission = opt-into-partial); an empty Rollup placeholder is pre-created at `ensure_week_sheet` (#233, best-effort) so the checkbox shows on a never-compiled week. Single-flight fcntl lock; fail-loud; capability-gated; watchdog Check-C marker `safety_compile_now_poll`.

**Send-leg hardening.**

- **Write-ahead SENDING marker (#247):** `weekly_send` writes `Send Status=SENDING` *before* `send_mail` (aborts if that write fails), then `SENDING → SENT` after confirmed delivery. `SENDING` is excluded from `weekly_send_poll.DISPATCH_STATUSES`, so a failed post-send stamp leaves the row stuck in `SENDING` (one delivery, never re-dispatched) instead of re-dispatchable `PENDING`. Surfaced by watchdog **Check N** (`_check_stuck_wsr_send`, hourly WARN, cap 10).
- **Append-only compilations (#248):** a recompile never overwrites a durable (possibly already-SENT) record — Box timestamped filename, WSR `add_wsr_row` (was `upsert`), week sheet `append_rollup_row` (was in-place); no-new-docs skip preserved.
- **WSR datetime (#245):** `Approved At` / `Sent At` retyped DATE → ABSTRACT_DATETIME; written **naive Pacific** `YYYY-MM-DDTHH:MM:SS` (`wsr_review.to_wsr_datetime()`). **Sequencing rule (not git-reversible):** retype the live columns *first*, then merge the writer — else the 15-min poller writes a naive string into a DATE column and silently truncates. ABSTRACT_DATETIME rejects offset/`Z` strings (errorCode 5536).
- **Portal filing fails LOUD (#252):** `portal_poll` no longer writes the Check-C marker on a no-creds/auth-failed cycle (which masked the 2026-06-07 1042 storm); CRITICAL fires immediately on missing-creds / `PortalAuthError`; a 5-consecutive-transport-failure counter escalates ERROR → CRITICAL; `resend_client` gained an explicit `(10,30)` timeout.
- **Picklist registry regression (#253):** #247's new `SENDING` value was missing from `shared/picklist_validation.py` REGISTRY → `validate_row` rejected it → `weekly_send_poll` went DEGRADED (fail-closed) until `_WSR_SEND_STATUS_VALUES |= {SENDING}`. The mocks-pass-but-live-fails class (Op Stds §30) — a new bounded-enum value must enter the REGISTRY in the same PR that writes it.

**Publish bugfix chain (one line each):** `sys.executable` archive (#241, bare-`python` died at `archived` under launchd PATH after the form was already live); op-aware stepper (#242); redundant-retire empty-commit guard at `apply_publish` + `git diff --cached --quiet` backstop (#244); id-keyed blank archives so same-`form_name` defs don't collide (#236); self-defeating-CI-gate fix — 9 hardcoded count/inventory assertions made dynamic + frozen-fixture behavior tests (#222/#227/#228); `PublishMonitor.fmtTime` ×1000 scaling (#222).

**Forensic audit (12-dimension).** Both invariants **INTACT**; H2 (double-send) fixed (#247); H1 (auto-merge + deploy under branch protection) **accepted by-design** under C12=A. Deferred medium/low findings **M1 / M2 / M4 / M5 / M6 / M7 / M9** + ITS_Daemon_Health observability drift + half-applied-publishes backfill — pointers only; bodies in [`../its/docs/tech_debt.md`](../../../its/docs/tech_debt.md).

## Authority

ITS Safety Portal Brief v4, 2026-06-10 canonical. Supersedes v3 (2026-06-07; status overlay v3.1 carried forward). Companion to [mission.md](mission.md) (v4). Verified against exec main `ab920bc` (a 62-commit reconciliation `f3ad814..ab920bc`, `brief-validator`-checked). Workstream briefs are frontmatter-versioned (not git-tagged). **The v4 trigger was met** by absorbing Phase 8 (admin dashboard, §17) + Phase 9 (form-publish pipeline, §18) — the brief had pinned at Phase 7 / `f3ad814`.

v5 trigger: substantive engineering-architecture change — deploy-platform change away from Cloudflare Workers, a return to client-side PDF rendering, an authentication-model swap, a change to the portal-never-touches-Smartsheet boundary, or doctrine adoption of the §50 code-actuation-gate flag ([mission §14 + Doctrine flags](mission.md#14-form-management-and-publish-pipeline-as-built)). **Open track:** the Evergreen production cutover (the three mirror activation tracks closed at v3.1); status-overlay updates absorb activation/phase progress.

Cross-references:
- [Mission](mission.md) — invariants (restated verbatim), audience, decisions, self-containment, phase status, risks.
- [Operational Standards](../../doctrine/operational-standards.md) — §23 topology (doctrine-reconciliation flagged), patterns honored.
- [Foundation Mission v11](../../doctrine/foundation-mission.md) — invariants inherited.
- [safety_reports brief](../safety-reports/brief.md#what-gets-built-refreshed-in-v61) — sibling workstream owning the shared pipeline (`weekly_generate` / `weekly_send`).
- [Forensic audit 2026-05-25](../../audits/2026-05-25_forensic-audit.md) — F02/F22 cluster.
- [Blueprint-update session log 2026-06-05](../../session-logs/2026-06-05_safety-portal-blueprint-update.md) — v2 decisions + doctrine-reconciliation flags.
