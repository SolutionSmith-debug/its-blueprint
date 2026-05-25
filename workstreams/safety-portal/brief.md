---
type: brief
version: 1
status: canonical
last_verified: 2026-05-25
last_verified_against: 40a3509
workstream: safety_portal
tags: [workstream-brief, cloudflare, d1, r2, hmac, ai-one-shot-extensibility]
---

# ITS Safety Portal — Brief v1

2026-05-25 — Initial brief, absorbed grill-me session decisions.

*Companion to [mission.md](mission.md). Originated from `safety_portal_architecture.md` v1 draft (2026-05-24); split per the [new-workstream scaffold](../../prompts/scaffold/new-workstream.md). All Q1–Q10 decisions absorbed; companion [grill-me session log](../../session-logs/2026-05-25_safety-portal-grill.md).*

## 1. Architecture Overview

```
┌──────────────────────┐         ┌─────────────────────────┐
│   Field PM Browser   │  HTTPS  │ Cloudflare Pages        │
│ (phone / tablet /    ├────────►│ + Workers (backend)     │
│  desktop)            │         │ + D1 (SQLite database)  │
│                      │         │ + R2 (PDF object store) │
└──────────────────────┘         └─────────────┬───────────┘
                                               │
                                               │ Periodic sync (daily 00:00 ET)
                                               │ + on-demand from Smartsheet button
                                               │
                                  ┌────────────▼────────────┐
                                  │ Smartsheet              │
                                  │  • ITS_Active_Jobs      │
                                  │  • ITS_Forms_Catalog    │
                                  └─────────────────────────┘

         Submission path:

┌──────────────────────┐         ┌─────────────────────────┐
│   Cloudflare Worker  │  SMTP   │ safety@                 │
│ (submit handler)     ├────────►│ evergreenrenewables.com │
│                      │         │ (unified intake mailbox │
│ - validate payload   │         │  — also legacy PDF path)│
│ - render PDF         │         └─────────────┬───────────┘
│ - email shim         │                       │
│   (X-ITS-Portal-*    │                       │ polled by intake_poll.py
│    headers + HMAC)   │                       │ at 60s cadence
│                      │         ┌─────────────▼───────────┐
└──────────────────────┘         │ safety_reports/         │
                                 │   intake.py             │
                                 │ - allowlist gate first  │
                                 │ - HMAC-verify portal    │
                                 │ - if portal: fast-path  │
                                 │ - else: legacy classify │
                                 │ - writes Smartsheet row │
                                 │ - uploads PDF to Box    │
                                 │ - Stage 12.5: notify D1 │
                                 │   of box_upload_verified│
                                 │ - keys writes off       │
                                 │   indicated work date   │
                                 └─────────────────────────┘
```

The portal feeds the existing pipeline. It does not bypass `intake.py`; it produces a submission that `intake.py` consumes via the same polling-daemon path that handles legacy PDF emails. Single-mailbox routing post-Correction-A means the trust boundary is HMAC-verified `X-ITS-Portal-*` headers + allowlisted `portal-noreply@` sender, NOT the destination address.

## 2. Data Model (D1 / SQLite)

D1 holds all portal-owned state. Mirror tables sync from Smartsheet; canonical tables are portal-native.

### Mirror tables (synced from Smartsheet, read-only from portal perspective)

```sql
-- Mirrors ITS_Active_Jobs
CREATE TABLE jobs_mirror (
    job_id            TEXT PRIMARY KEY,           -- stable key, e.g., "huntley-2024"
    project_name      TEXT NOT NULL,              -- "Huntley Solar"
    address           TEXT NOT NULL,
    active_status     TEXT NOT NULL,              -- "Active" | "Inactive" | "Archived"
    smartsheet_row_id TEXT NOT NULL,
    synced_at         INTEGER NOT NULL
);

-- Mirrors ITS_Forms_Catalog (Q6: Form Version column dropped; Available For Jobs column added)
CREATE TABLE forms_catalog_mirror (
    form_code            TEXT PRIMARY KEY,        -- stable key, e.g., "jha-v1" or "jha-bradley-v1"
    display_name         TEXT NOT NULL,
    description          TEXT,
    display_order        INTEGER NOT NULL,
    active_status        TEXT NOT NULL,
    available_for_jobs   TEXT,                    -- CSV of job_ids; NULL/empty = available on all jobs
    smartsheet_row_id    TEXT NOT NULL,
    synced_at            INTEGER NOT NULL
);
```

### Canonical tables (portal-owned)

```sql
-- Q2: password column renamed; bcrypt cost=10 hash stored
CREATE TABLE users (
    username       TEXT PRIMARY KEY,              -- e.g., "martinez.mario"
    password_hash  TEXT NOT NULL,                 -- bcrypt cost=10 hash (60 chars)
    display_name   TEXT NOT NULL,
    active         INTEGER NOT NULL DEFAULT 1,
    created_at     INTEGER NOT NULL,
    last_login_at  INTEGER
);

-- Q10: box_upload_verified columns + pdf_pruned_at marker added
CREATE TABLE submissions (
    submission_id            TEXT PRIMARY KEY,    -- UUID v4
    username                 TEXT NOT NULL REFERENCES users(username),
    job_id                   TEXT NOT NULL REFERENCES jobs_mirror(job_id),
    form_code                TEXT NOT NULL,       -- e.g., "jha-v1", "jha-bradley-v1"
    work_date                TEXT NOT NULL,       -- ISO date, PM-selected
    payload_json             TEXT NOT NULL,       -- per-form-code structured payload
    pdf_url                  TEXT,                -- R2 path while present; nullable after prune
    submitted_at             INTEGER NOT NULL,    -- epoch seconds, server-set
    shim_status              TEXT NOT NULL DEFAULT 'pending',  -- pending | sent | failed
    shim_sent_at             INTEGER,
    box_upload_verified      INTEGER NOT NULL DEFAULT 0,        -- Q10: 0|1; set by intake.py Stage 12.5
    box_upload_verified_at   INTEGER,                            -- Q10: epoch seconds; null until verified
    pdf_pruned_at            INTEGER                             -- Q10: epoch seconds; set by prune Worker
);

CREATE INDEX idx_submissions_work_date ON submissions(work_date);
CREATE INDEX idx_submissions_username ON submissions(username);

-- Q10: partial indexes for staleness alert + prune candidate queries
CREATE INDEX idx_submissions_pending_box_verify ON submissions(submitted_at)
  WHERE shim_status = 'sent' AND box_upload_verified = 0;
CREATE INDEX idx_submissions_prune_candidates ON submissions(submitted_at)
  WHERE shim_status = 'sent' AND box_upload_verified = 1 AND pdf_pruned_at IS NULL;
```

`submitted_at` is recorded for portal-internal forensic purposes only. It is **never surfaced on the PDF, in the Smartsheet row, or in any output artifact**. Per operator Q4 decision, the PDF is identical regardless of submission timing. Backdating risk acceptance documented in [mission Risks](mission.md#10-risks).

### Sessions

Long-lived sessions stored as signed cookies, not in a server-side table. Session secret in Cloudflare Workers secret binding. 90-day expiry.

## 3. Smartsheet Integration

### ITS_Active_Jobs (new sheet)

Office PM maintains. ITS Operations workspace.

| Column | Type | Purpose |
|---|---|---|
| Project Name | TEXT_NUMBER (primary) | Display name in portal dropdown. |
| Job ID | TEXT_NUMBER | Stable key (kebab-case). Never changes. |
| Address | TEXT_NUMBER | Full street address. Auto-fills Work Location on every form. |
| Active | PICKLIST | Active / Inactive / Archived. Only Active rows appear in portal dropdowns. |
| Notes | TEXT_NUMBER | Free-text for office PM. Not consumed by portal. |
| Last Modified | DATETIME (system) | Auto-populated. |
| Modified By | CONTACT_LIST (system) | Auto-populated. |

### ITS_Forms_Catalog (new sheet) — Q6 updated

Same workspace. Office PM (or operator) maintains. **Form Version column dropped (Q6); Available For Jobs column added.** Versioning happens implicitly via the form_code directory name in code (jha-v1 → jha-v2 is two distinct rows).

| Column | Type | Purpose |
|---|---|---|
| Form Name | TEXT_NUMBER (primary) | Display name in picker. "Job Hazard Analysis" |
| Form Code | TEXT_NUMBER | Stable key matching code directory. `jha-v1`, `jha-bradley-v1`, `equipment-preinspection-v1`. |
| Active | PICKLIST | Active / Inactive / Archived. Only Active rows offered. |
| Description | TEXT_NUMBER | Tooltip text. |
| Display Order | TEXT_NUMBER | Sort key. |
| **Available For Jobs** | TEXT_NUMBER | **Q6 NEW.** CSV of Job IDs OR empty (= available on all jobs). E.g., `bradley-1,bradley-2` for the Bradley variant; empty for the standard JHA. |
| Last Modified | DATETIME (system) | |
| Modified By | CONTACT_LIST (system) | |

### Sync mechanism

**Scheduled sync.** Cloudflare Worker cron trigger fires at 00:00 ET daily. Calls Smartsheet `list_rows` against `ITS_Active_Jobs` and `ITS_Forms_Catalog`, upserts into D1 mirror tables. Stamps `synced_at`. Failures log to ITS_Errors via the email-shim.

**On-demand sync (Smartsheet "Sync Now" button).** Smartsheet automation rule on a dedicated trigger row fires webhook to Workers endpoint. Endpoint validates webhook signature (`SMARTSHEET_WEBHOOK_SECRET` binding), runs sync, writes "Last Sync" timestamp back. Button location decision deferred to build session (see [Open Questions Remaining](#16-open-questions-remaining)).

**Sync latency tolerance.** New project added at 9am does not appear in portal dropdowns until midnight unless office PM hits Sync Now. Known trade-off.

**Sync conflict handling.** Last-write-wins. Portal never writes to Smartsheet, so no merge logic.

## 4. Authentication

Username + bcrypt-hashed password (cost factor 10) against D1 `users.password_hash` column. Per Q2: plaintext storage was rejected at grill-me session 2026-05-25. Login form POSTs to a Workers endpoint that runs `await bcrypt.compare(submitted, stored_hash)`, sets a signed session cookie on success, redirects to home page.

**Username convention:** `lastname.firstname` lowercase. Collisions handled by appending a digit (`martinez.mario2`).

**Password convention (Q2b deferred to Phase 7):** per-user-variability mandatory. Specific scheme (lastname+year vs random passphrase) locked at admin-route implementation. Shared passwords explicitly rejected at grill-me session — they defeat the per-user audit-trail-defensibility of signature-per-row submissions.

**Session cookie:** HTTP-only, Secure, SameSite=Lax, 90-day expiry, signed with `SESSION_SIGNING_SECRET` in Workers binding.

**Admin provisioning route.** Separate `/admin` route, password-gated by single operator-only credential in `ADMIN_PASSWORD` binding. CRUD UI for users table: add user, edit display name, set active=0 (revoke), reset password. Operator types plaintext at provisioning/reset time; backend hashes before INSERT/UPDATE. Operator-side workflow per [mission §6](mission.md#6-out-of-scope): no self-service password reset for field PMs.

**Out of scope per operator decision:** CSRF tokens, rate limiting, account lockout, audit log of failed logins. Threat model does not warrant the friction.

## 5. User-Facing UX

### Login page (`/`)

Two fields (username, password), one button. Failed login shows generic "Username or password incorrect" — no enumeration of which field is wrong.

### Home page (`/home`)

Work Date picker (default today; any past date allowed per Q4; no future dates), Project dropdown (from `jobs_mirror.active_status=Active`), Form dropdown filtered by selected project per Q6:

```sql
-- Form picker filter
SELECT * FROM forms_catalog_mirror
WHERE active_status = 'Active'
  AND (available_for_jobs IS NULL
       OR available_for_jobs = ''
       OR :selected_job_id IN (SELECT trim(value) FROM json_each(json_array_split(available_for_jobs))))
ORDER BY display_order;
```

Recent submissions list shows last 10. Tapping one opens a read-only PDF view. UI handles pruned PDFs per Q10 option (a):

```typescript
function ViewPdfControl({ submission }: { submission: SubmissionRow }) {
  if (submission.pdf_pruned_at !== null) {
    return <span className="archived-pdf-marker">Archived to Box</span>;
  }
  return <a href={submission.pdf_url}>View PDF</a>;
}
```

### Form page (`/form/{form_code}`)

Rendered generically from the form definition's `sections` array via the shared `_runtime/renderer.tsx`. See [Form Schemas](#6-form-schemas-q6b-rewrite) below for the declarative structure.

- Work Date, Project Name, Project Address pre-filled from home-page selection.
- Per-form fields rendered per declarative schema.
- Worker Acknowledgement section: repeatable rows of Name + Company + Signature (touch canvas → SVG path data).
- localStorage draft persistence keyed by `{username}-{form_code}-{work_date}-{job_id}`. 7-day auto-prune (cadence open question).
- Submit button: schema-validates, client-generates PDF via `_runtime/pdf_renderer.ts`, posts payload to backend.

### Confirmation page (`/confirm/{submission_id}`)

Submission summary. "View PDF" honors prune state per Q10 (a). "Submit Another" returns to home page.

## 6. Form Schemas (Q6b rewrite)

**Each form is one declarative TypeScript file in its own directory.** No separate schema / render / pdf files — the shared `_runtime/` walks the declarative spec generically. Designed for AI-one-shot extensibility (per operator project memory at `~/.claude/projects/-Users-sethsmith/memory/project_ai_one_shot_extensibility.md` — outside this repo): the trained operator pastes an existing form into a Claude chat, describes the change, pastes the result back, CI validates, deploy.

### Directory structure

```
its/safety_portal/forms/
├── _runtime/
│   ├── types.ts              # FormDefinition TypeScript type — meta-schema for AI validation
│   ├── renderer.tsx          # ONE generic React renderer (walks sections)
│   ├── pdf_renderer.ts       # ONE generic PDF generator (walks sections; pdf-lib)
│   ├── meta-schema.json      # JSON Schema for FormDefinition; CI lint + AI self-validation
│   └── README.md             # operator-facing "How to add a new form" instructions
├── jha-v1/
│   └── form.ts               # ONE declarative file — full form definition
├── jha-bradley-v1/
│   └── form.ts
├── equipment-preinspection-v1/
│   └── form.ts
├── toolbox-talk-v1/
│   └── form.ts
└── daily-site-safety-v1/
    ├── form.ts
    └── pdf_override.ts       # escape hatch — only for forms whose layout doesn't fit the generic walker
```

### `form.ts` shape

```typescript
import type { FormDefinition } from "../_runtime/types";

const form: FormDefinition = {
  code: "jha-bradley-v1",
  display_name: "JHA — Bradley",
  description: "Job Hazard Analysis with Bradley-required extra fields",
  display_order: 11,

  sections: [
    {
      title: "Project Information",
      fields: [
        { id: "project_name",          type: "text", label: "Project Name",        required: true, source: "from-job" },
        { id: "job_being_performed",   type: "text", label: "Job Being Performed", required: true, max_length: 200 },
        { id: "bradley_permit_number", type: "text", label: "Bradley Permit #",    required: true },
      ],
    },
    {
      title: "Task Hazards",
      fields: [{
        id: "task_rows", type: "repeatable", min: 1, max: 8,
        row_fields: [
          { id: "task",          type: "text", label: "Task",          required: true },
          { id: "major_hazards", type: "text", label: "Major Hazards", required: true },
          { id: "mitigation",    type: "text", label: "Mitigation",    required: true },
        ],
      }],
    },
    {
      title: "Worker Acknowledgement",
      fields: [{
        id: "worker_roster", type: "repeatable", min: 1, max: 30,
        row_fields: [
          { id: "name",      type: "text",      label: "Name",      required: true },
          { id: "company",   type: "text",      label: "Company",   required: false },
          { id: "signature", type: "signature", label: "Signature", required: false },
        ],
      }],
    },
  ],
};

export default form;
```

### AI-one-shot extension workflow

1. Operator opens Claude (chat or Claude Code).
2. Pastes an existing form file as template (e.g., `jha-v1/form.ts`).
3. Describes the change: *"Bradley needs these extra fields: permit number, weather conditions, supervisor on-site name. Make a Bradley variant available only on bradley-1 and bradley-2 projects."*
4. Claude generates `jha-bradley-v1/form.ts`.
5. Operator pastes into the repo at the documented path.
6. CI runs: TypeScript compile + meta-schema validation against `_runtime/meta-schema.json`.
7. On pass: deploy → form auto-registers in catalog mirror.
8. Operator adds the Smartsheet `ITS_Forms_Catalog` row with `Form Code=jha-bradley-v1`, `Available For Jobs=bradley-1,bradley-2`, `Active=Active`.

**CI guarantees:** TypeScript type catches structural errors at compile time; meta-schema validation catches type-level errors before deploy; runtime fall-back to safe-render on unexpected field types prevents portal hard-crash even if a malformed form somehow ships.

### Per-form override escape hatch

For forms whose layout doesn't fit the generic walker — currently anticipated only for Daily Site Safety's sum-to-100 physical-demands grid — the form directory may include a `pdf_override.ts` (and optionally `render_override.tsx`) that exports a custom renderer the `_runtime/` walker delegates to. Escape hatch is opt-in per form; 90% of forms fit the generic walker.

### Per-form field inventories (v1 forms)

Source design notes for each v1 form's field set, derived from the existing paper forms during the 2026-05-24 architecture session. Preserved here as build-time reference for the operator-developer; informs each `form.ts` implementation in Phase 4 (build sequencing per §14).

**jha-v1** — `its/safety_portal/forms/jha-v1/form.ts`

Original sketch:

```typescript
{
  form_code: "jha-v1",
  fields: {
    work_date: { type: "date", required: true, source: "home-page" },
    project_name: { type: "text", required: true, source: "home-page" },
    project_address: { type: "text", required: true, source: "home-page" },
    job_being_performed: { type: "text", required: true, max_length: 200 },
    crew_members: { type: "text", required: true, max_length: 200 },
    task_rows: {
      type: "repeatable",
      min: 1, max: 8,
      fields: {
        task: { type: "text", required: true },
        major_hazards: { type: "text", required: true },
        mitigation: { type: "text", required: true }
      }
    },
    worker_roster: {
      type: "repeatable",
      min: 1, max: 30,
      fields: {
        name: { type: "text", required: true },
        company: { type: "text", required: false },
        signature: { type: "signature", required: false }
      }
    }
  }
}
```

The Q6b declarative-form structure expresses this as `sections: [{ title: "Project Information", fields: [...] }, { title: "Task Hazards", fields: [{ id: "task_rows", type: "repeatable", min: 1, max: 8, row_fields: [...] }] }, { title: "Worker Acknowledgement", fields: [{ id: "worker_roster", ... }] }]` per the §6 example pattern.

**daily-site-safety-v1** — `its/safety_portal/forms/daily-site-safety-v1/form.ts`

The largest form. Field inventory (paper-form-derived):

- **Project metadata:** project_name, project_number, address (auto-fill from job), job_type, area_onsite, prepared_by, date.
- **Today's work:** description (multi-line text).
- **Environmental conditions** (multi-select): Inside, Outside, Heat, Cold, Wet, Dry, Dust, Vapors-Mist, Noise, Vibration, Other (text-input fallback).
- **Heat/cold index:** expected_temp (text).
- **Physical demands percentages** (sum-to-100 validation): Standing, Sitting, Walking, Pushing, Pulling, Bending/Stooping, Kneeling, Reaching, Carrying-lbs.
- **Basic job sequence:** sequence_steps (repeatable text).
- **Potential hazards found:** hazards_found (repeatable text).
- **Commonly faced hazards matrix** (5 rows × 4 control columns):
  - Rows: Slips/Trips/Falls, Pinch Points, Lifting/Handling, Caught on or Between, Over Exertion.
  - Columns (each a checkbox per row): PPE, Procedure, Training, Guards.
- **Safety requirements and procedures:** safety_requirements (repeatable text).
- **Additional considerations:** additional_considerations (text).
- **Worker roster:** Name & Company, Time In, Lunch, Time Out, Signature.

This is the form most likely to need `pdf_override.ts` per §6 escape hatch — specifically for the sum-to-100 physical-demands grid layout and the 5×4 hazards matrix.

**equipment-preinspection-v1** — `its/safety_portal/forms/equipment-preinspection-v1/form.ts`

Field inventory:

- **Header:** operator, operator_signature, unit_identifier (equipment ID), date.
- **Before-engine-start** (two parallel columns of OK/Not-OK checkbox pairs):
  Bucket, Cutting Edge, Mirror/Windows, Windshield, Tires, Tracks, Ladder/Grab Handles, Hydraulic Cylinder Lines, Hydraulic Level, Leaks Exterior, FOPS/ROPS, Engine Oil, Coolant, Belts, Air Filter, Next Oil Change Hours, Leaks Motor.
- **After-startup** (two parallel columns of OK/Not-OK checkbox pairs):
  Owner Manual, Seat Bar, Seat Belt, Park Brake, Vibrations, Engine Noise, Horn, Bucket/Attachment Tilt, Lift Arm, Steering, Forward, Reverse, Backup Alarm, Transmission Noise, Lights, Fuel Level (picklist: ¼ / ½ / ¾ / Full), Hours on Machine.
- **Maintenance:** Maintenance Done (text), Maintenance Required (text).

Generic walker handles this with `type: "ok-not-ok"` field rendering for the checkbox pairs.

**toolbox-talk-v1** — `its/safety_portal/forms/toolbox-talk-v1/form.ts`

Field inventory:

- topic_title (text)
- topic_body (text — open question deferred to build session: free-text per submission, or library of pre-written topics with editable body? See [§16 Open Questions Remaining](#16-open-questions-remaining))
- date
- instructor_name
- worker_roster (Name, Signature)

The simplest of the four forms in absolute terms — recommended as the second form to build (after jha-v1) per §14 Phase 4b sequencing to validate the pattern works for forms without the task/hazard structure.

## 7. Signature Handling

Signature canvas is a standard touch-event handler that records SVG path data as the user draws. Storage format: SVG `<path d="...">` element data (~500B–3KB per signature).

PDF rendering: signatures rendered inline as SVG in the worker roster section. Optional per row (unsigned worker counted in Weekly Compliance Rollup's `unsigned_worker_count`).

## 8. Submission Pipeline

### Step 1 — Client-side validation and PDF generation

On Submit, form validates payload against schema. On valid, client generates PDF via `_runtime/pdf_renderer.ts` (or per-form `pdf_override.ts` if present). Result: Uint8Array of PDF bytes.

### Step 2 — Backend submission

Client POSTs to `/api/submit` with `{ form_code, work_date, job_id, payload, pdf_base64 }`. Backend Worker:

1. Verifies session cookie.
2. Validates payload against backend's copy of the FormDefinition (defense in depth).
3. Generates submission UUID.
4. Stores PDF in R2 at `submissions/{submission_id}.pdf`.
5. Inserts row into `submissions` with `shim_status=pending`, `box_upload_verified=0`.
6. Returns `{ submission_id }`.
7. Client redirects to `/confirm/{submission_id}`.

### Step 3 — Email shim (asynchronous)

Separate Worker (cron 60s or queue-triggered) picks up pending submissions and sends to the unified `safety@` intake mailbox.

Email shape:
- **From:** `portal-noreply@evergreenmirror.com` (validation) / `portal-noreply@evergreenrenewables.com` (production).
- **To:** `safety@evergreenmirror.com` (validation) / `safety@evergreenrenewables.com` (production). Unified with legacy PDF intake per Correction A.
- **Subject:** `[ITS-PORTAL] {form_code} · {project_name} · {work_date}`.
- **Headers:**
  - `X-ITS-Portal-Submission-Id: {submission_id}`
  - `X-ITS-Portal-Form-Code: {form_code}`
  - `X-ITS-Portal-Work-Date: {work_date}`
  - `X-ITS-Portal-Job-Id: {job_id}`
  - `X-ITS-Portal-Username: {username}`
  - `X-ITS-Portal-HMAC: {HMAC-SHA256 of canonicalized payload}` — Q3.
- **Body:** JSON-encoded full payload.
- **Attachment:** rendered PDF (`{form_code}_{work_date}_{project_name}.pdf`).

On successful send: `submissions.shim_status='sent'` + `shim_sent_at`. On failure: log to `ITS_Errors` via shim with `X-ITS-Portal-Error` marker.

### Step 4 — intake.py portal-marker branch

The existing `safety_reports/intake.py` 12-stage pipeline gets a new branch:

- **Stage 1 (existing):** Fetch message via Graph.
- **Stage 1.5 (NEW):** Allowlist gate (`portal-noreply@` in `ITS_Trusted_Contacts`). If sender allowlisted AND `X-ITS-Portal-Submission-Id` header present AND HMAC verifies → portal fast-path; skip Stages 2-7 (sender allowlist already passed; attachment extraction unneeded; payload is structured; classification skipped). If allowlisted sender + headers present BUT HMAC fails → ITS_Quarantine + CRITICAL triple-fire (header forgery attempt).
- **Stage 8' (NEW):** Parse JSON body. Validate against the FormDefinition meta-schema. Invalid → ITS_Errors + ITS_Review_Queue.
- **Stage 9' (NEW):** Resolve project via Job ID (direct lookup against `shared/sheet_ids.BOX_PROJECT_FOLDERS` + jobs mirror). No ambiguity.
- **Stage 10' (NEW):** Ensure week folder for the **indicated work date** (not today's date) via `week_folder.py`.
- **Stage 11' (NEW):** Write Daily Reports row keyed off `work_date`. Existing 9-column schema with portal-specific values: classification = the form_code, attachment_path = Box upload location.
- **Stage 12' (NEW):** Decode PDF attachment, upload to Box under `D. JSA's/` (or form-specific subfolder pending build-session decision).
- **Stage 12.5 (NEW per Q10):** ONLY if portal-marker submission AND Stage 12' succeeded. POST `submission_id` to portal's `/api/internal/mark-box-verified` endpoint with `ITS_PORTAL_INTERNAL_API_TOKEN` bearer auth. Backend flips `submissions.box_upload_verified=1`, sets `box_upload_verified_at`. Sequence is non-negotiable: Box upload first, D1 flip second; never reversed. Soft-fail on D1 unreachable (INFO log; 24h staleness alert will eventually surface). Hard-fail CRITICAL on bearer-token rejection (misconfiguration, not transient).
- **Stage 13' (NEW):** If `work_date` is in a past week, trigger Weekly Rollup re-aggregation (idempotent).
- **Stage 14 (existing):** Mark message read.

Feature flag: `safety_reports.intake.portal_handler_enabled` controls activation. Additive to intake.py — legacy PDF-email path remains.

## 9. Filing Behavior

Per Q4: all filing operations key off the **indicated work date**, not the submission timestamp.

### Box filing path

```
ITS DATA/
└── {Project}/
    └── {Year}/
        └── W{ISO Week}_{Month}{StartDay}-{Month}{EndDay}/
            └── D. JSA's/
                └── {work_date}_{form_code}_{submission_id_short}.pdf
```

Week folder is the week containing the **work_date**, not today. A submission for Sept 22 lands in W38_Sep22-Sep28 regardless of submission timing.

`week_folder.py` already idempotent (PR #54).

### Smartsheet Daily Reports row

Daily Reports sheet for project's current quarter (or quarter containing `work_date`) gets new row. Date column = `work_date`. Standard 9-column schema honored.

### Weekly Rollup re-aggregation

Past-week `work_date` → Stage 13' triggers `safety_reports/jha_weekly_rollup.py` for that week. Aggregator is idempotent: reads all Daily Reports rows for the week, recomputes aggregate values, updates the Weekly Rollup row in place.

**Already-sent WPRs are not retroactively updated.** Operator surfaces discrepancy via daily watchdog and decides whether to send an addendum.

## 10. PDF Rendering (Q6b rewrite)

Generic walker in `_runtime/pdf_renderer.ts` produces PDFs by walking the form's `sections` array. Uses `pdf-lib` + embedded Liberation Sans / Helvetica for text, embedded SVG for signatures. No external font dependencies (fonts bundled in Workers).

Design goals (unchanged from arch doc):
- Rendered PDF visually equivalent to paper form (OSHA inspector parity).
- Signatures appear inline as drawn (not typed names).
- Logo + form title at top.
- `work_date` in same position as paper form (no submission timestamp, no backdate indicator — Q4).
- Filename: `{form_code}_{work_date}_{project_name_slug}.pdf`.

**Per-form override escape hatch:** a form directory MAY include `pdf_override.ts` that exports `function renderPdf(form, payload): Uint8Array` to handle layouts the generic walker cannot. Anticipated for Daily Site Safety's sum-to-100 physical-demands grid. Override is opt-in; absent override file → generic walker used.

## 11. Deployment Topology

### Validation environment (`safety.evergreenmirror.com`)

- **Frontend:** Cloudflare Pages serving React SPA, deployed from `its/safety_portal/frontend/` via `git push`.
- **Backend:** Cloudflare Workers at same Pages project (`/api/login`, `/api/submit`, `/api/sync`, `/api/internal/mark-box-verified`, `/admin/*`).
- **Database:** Cloudflare D1, bound to Workers.
- **PDF storage:** Cloudflare R2, bucket `its-safety-portal-pdfs-validation`. Conditional 90-day prune via daily Cron Worker per Q10.
- **DNS:** GoDaddy-managed CNAME `safety.evergreenmirror.com` → `its-safety-portal.pages.dev`.
- **SSL:** Cloudflare Universal SSL.
- **Email shim sender:** `portal-noreply@evergreenmirror.com` — M365 mirror tenant; M365 client-id + client-secret in Workers bindings.
- **Email shim recipient:** `safety@evergreenmirror.com` — unified intake mailbox.

### Production migration (`safety.evergreenrenewables.com`)

Per arch doc §15 with email destination per Correction A:
1. GoDaddy CNAME `safety.evergreenrenewables.com` → `its-safety-portal-prod.pages.dev`.
2. Fresh D1 instance; field PMs re-provisioned manually.
3. Production R2: `its-safety-portal-pdfs-prod`.
4. Email shim sender: `portal-noreply@evergreenrenewables.com`.
5. Email shim recipient: `safety@evergreenrenewables.com` (unified; no new portal-submit@ needed).

### Workers secret bindings (Q10 + Q3 + Q2 updates)

| Secret | Purpose |
|---|---|
| `SMARTSHEET_API_TOKEN` | Read-only token scoped to `ITS_Active_Jobs` + `ITS_Forms_Catalog`. |
| `SESSION_SIGNING_SECRET` | HMAC key for session cookies. |
| `ADMIN_PASSWORD` | Single credential for `/admin` route. |
| `EMAIL_SHIM_M365_CLIENT_ID` | M365 app registration for `portal-noreply@` sender. |
| `EMAIL_SHIM_M365_CLIENT_SECRET` | M365 app secret. |
| `SMARTSHEET_WEBHOOK_SECRET` | Verifies Sync Now webhook payloads from Smartsheet. |
| **`HMAC_PAYLOAD_SECRET`** | **Q3.** HMAC-SHA256 secret for portal payload signing. Mirror copy in macOS Keychain as `ITS_PORTAL_HMAC_SECRET` for intake.py verification side. |
| **`PORTAL_INTERNAL_API_TOKEN`** | **Q10.** Bearer token validating `/api/internal/mark-box-verified` callbacks from intake.py Stage 12.5. Mirror copy in macOS Keychain as `ITS_PORTAL_INTERNAL_API_TOKEN`. |

All secrets in Cloudflare Workers Secrets; never in code, never in environment files. Operator-side mirrors in macOS Keychain per existing convention.

### R2 prune Cron Worker (Q10 NEW)

Cloudflare Worker on daily cron trigger (03:00 UTC). Two operations per run:

1. **Prune:** delete R2 objects for `submissions WHERE shim_status='sent' AND box_upload_verified=1 AND submitted_at < now()-90d AND pdf_pruned_at IS NULL`. Update `submissions.pdf_pruned_at` after each successful delete. Log aggregate counts to ITS_Errors INFO (`r2_prune_daily_summary`).
2. **Staleness alert:** query `submissions WHERE shim_status='sent' AND box_upload_verified=0 AND submitted_at < now()-24h`. If count > 0: ONE ITS_Errors WARN row (`portal_box_verification_stuck_24h`) with count + oldest timestamp. Operator investigates via runbook.

## 12. Operational Conventions Honored

Per [Operational Standards](../../doctrine/operational-standards.md):

- **Kill switch first:** portal sync Worker + email-shim Worker + R2 prune Worker check `system.state` from ITS_Config at every invocation. PAUSED → no sync, no shim send, no prune.
- **Error logging:** Workers log to `ITS_Errors` via email shim (same mechanism as legacy intake errors). Standard `@its_error_log` semantics: severity, workstream=`safety_portal`, correlation_id threaded.
- **Confidence threshold:** N/A. Portal payloads are structured; no AI classification step.
- **External Send Gate:** portal email-shim Worker registered in SEND_SCRIPTS; can only send to configured `safety@` intake mailbox. WPR send gate (`weekly_send.py`) unchanged. Portal shim→safety@ traffic is internal-tenant, NOT external transmission per Invariant 1.
- **Adversarial Input Handling:** six layers + HMAC verification per [mission Invariant 2](mission.md#invariant-2-adversarial-input-handling).
- **Capability gating (post-F02):** the network-library allowlist permits only enumerated `shared/*_client.py` modules + `safety_reports/portal_notify.py` + portal Worker modules to make outbound HTTPS calls. Other modules importing `requests` / `urllib` / `httpx` / `socket` / `subprocess` fail CI. Pre-portal-launch dependency per Q1.
- **Credentials:** Cloudflare Workers Secrets bindings, not env files. M365 OAuth via client-credentials flow.
- **Schemas in code, version-controlled:** form definitions live as `its/safety_portal/forms/{form_code}/form.ts`. CI meta-schema validation per Q6b.
- **SDK-vs-Live Integration Test Discipline:** Smartsheet API client used in sync Worker has parallel integration tests against throwaway sandbox sheet, gated behind `pytest -m integration` (or Workers-equivalent runner).
- **Picklist hardening:** `active_status` columns on `ITS_Active_Jobs` and `ITS_Forms_Catalog` are PICKLIST, not TEXT_NUMBER.

## 13. Transition Plan

Two paths run in parallel until adoption is real:

- **Phase A (validation):** Portal live at `safety.evergreenmirror.com`. Field PMs use portal voluntarily. Legacy PDF-email path remains official.
- **Phase B (soft launch):** Production portal live. Field PMs onboarded one project at a time. Both paths accepted. Communication: "Portal preferred, paper fallback acceptable."
- **Phase C (deprecation announcement):** Email to field PMs announcing legacy sunset date (operator-chosen, typically 30-60 days). Daily Reports surface flags submissions still arriving via legacy with soft warning.
- **Phase D (sunset):** Legacy PDF-email path disabled via `safety_reports.intake.legacy_pdf_handling_enabled` ITS_Config flag. intake.py rejects non-portal-marker `safety@` submissions with auto-reply ("Please submit via portal").

Legacy code remains in-tree, deactivated via flag per [preservation-over-refactor convention](../../doctrine/operational-standards.md).

## 14. Implementation Phases

Per [Q1 decision](../../session-logs/2026-05-25_safety-portal-grill.md): **hardening cluster first; portal Phase 2+ unblocked AFTER cluster lands.** Cluster scope discipline locked (Q7b): cutover slips if cluster overruns, F08 stays in scope.

### Pre-portal: Phase 1.4 hardening cluster (~2.5 days)

1. **F19 + F23 atomic-write bundle** — `shared/state_io.py` with `atomic_write_json` + `with_path_lock`; migrate seen-set + heartbeat + alert_dedupe callsites. ~4 hours.
2. **F02 + F22 cluster** — invert capability-gating to network-library allowlist; introduce `shared/approval_verification.py` with row-history check + optional `update_row` wrapper. ~6 hours + 1 hour optional + 30 min doctrine reconciliation.
3. **F08 + F09 cluster** — `shared/circuit_breaker.py` with persistent state + CIRCUIT_OPEN status surfacing; sliding-window alerts-per-hour cap in `alert_dedupe.py`. ~1.5–2 days. Cutover slips if this overruns.
4. **F16 UptimeRobot heartbeat ping wiring** — 1 hour.
5. **F17 intake_poll TRACKED_JOBS addition + marker write** — 30 minutes.
6. **F18 + F03 tag-escape test + fix** — 45 minutes.
7. **F04 keychain stdin-mode** — 15 minutes.
8. **F10 lockfile + pip-audit** — 1 hour.
9. **Doctrine reconciliation (Q8: F07 + F13 + F20)** — ~1 hour code + ~1 hour doc work.

### Portal Phase 0 — Mission + brief land (THIS PR)

Mission + brief land in `workstreams/safety-portal/`. Taxonomy PR-equivalent: `safety_portal` added to `CANONICAL_WORKSTREAMS` + CONVENTIONS.md + execution-repo doc_conventions.md.

### Portal Phase 1 — Smartsheet surfaces

- Create `ITS_Active_Jobs` sheet. Seed with 6 active projects (Bradley 1/2, Brimfield 1/2, Huntley, Rockford).
- Create `ITS_Forms_Catalog` sheet with Available For Jobs column.
- Add sheet IDs to `shared/sheet_ids.py`.

### Portal Phase 2 — Cloudflare scaffolding

- Provision Cloudflare account, Pages project, Workers project, D1, R2.
- Provision GoDaddy CNAME `safety.evergreenmirror.com`.
- M365 mirror tenant: create `portal-noreply@` mailbox. App registration.
- Land minimal portal: login + home + hard-coded JHA stub. Validates full stack end-to-end.

### Portal Phase 3 — Sync Worker

- Implement sync Worker (cron + manual webhook).
- D1 schema migrations (users, submissions with Q10 box_upload_verified columns, mirror tables with Q6 available_for_jobs).
- Smartsheet automation rule for Sync Now button.

### Portal Phase 4 — Form runtime + first form

- Ship `_runtime/`: types.ts + renderer.tsx + pdf_renderer.ts + meta-schema.json + README.md.
- Ship `jha-v1/form.ts` as the canonical first form. End-to-end smoke against validation environment.
- Subsequent forms (toolbox-talk-v1 → equipment-preinspection-v1 → daily-site-safety-v1 with pdf_override.ts) as one PR each.

### Portal Phase 5 — Submission pipeline (HMAC, Stage 12.5, prune Worker)

- Email shim Worker with HMAC signing.
- `intake.py` portal-marker branch (Stages 1.5, 8'–13' + Stage 12.5 D1 callback). Feature-flagged.
- `safety_reports/portal_notify.py` for Stage 12.5.
- R2 prune Cron Worker (Q10).
- End-to-end test: portal submission → HMAC-signed shim → intake.py → Daily Reports row + Box upload + Stage 12.5 D1 flip → (if past-week) Weekly Rollup recompute.

### Portal Phase 6 — JHA Weekly Compliance Rollup aggregator

- `safety_reports/jha_weekly_rollup.py` — idempotent aggregator.
- Wired to intake.py Stage 13' AND a Friday-afternoon cron for current-week aggregation.

### Portal Phase 7 — Admin route + password scheme lock (Q2b)

- `/admin` route with operator credential gate.
- User CRUD UI with bcrypt hashing at write time.
- Per-user password scheme locked at this implementation (Q2b — deferred from grill session).
- Provision real Evergreen field PMs (10–15 initially).

### Portal Phase 8 — Validation in field

- Operator + Daniel + 1–2 field PMs use portal in parallel with paper for 2–4 weeks.
- Operator monitors submission accuracy, PDF quality, signature capture UX, Weekly Rollup correctness.

### Portal Phase 9 — Production cutover

- New Cloudflare project for production.
- Coordinate with Evergreen GoDaddy contact for CNAME.
- M365 production tenant: provision `portal-noreply@` (no new portal-submit@ — unified with safety@).
- Re-provision field PMs in production database.
- Soft launch: portal preferred, paper accepted.

### Portal Phase 10 — Legacy sunset

Per [Transition Plan](#13-transition-plan). Operator-paced.

## 15. Sequencing Dependencies

- **Hardening cluster (Phase 1.4) must land before Portal Phase 2.** Per Q1.
- **F22 (`shared/approval_verification.py`) must land before any new workstream's customer-facing send.** Per Q5 — cross-cutting `shared/` protection.
- **F08+F09 (`shared/circuit_breaker.py` + alerts cap) must land before Portal Phase 5 submission pipeline.** Per Q7 — portal's downstream WPR pipeline benefits from the cascade-failure protection.
- **Box 1111B canonical blueprint** already shipped (PR #70); portal's Box folder targeting uses the canonical 1111B-derived clones.
- **ITS_Trusted_Contacts (Phase 1.4 mechanism)** must accept `portal-noreply@` allowlist entry before Phase 5.

## 16. Open Questions Remaining

Q6 (Form Versioning) and Q10 (R2 retention) were LOCKED at the grill-me session (now reflected in [Decisions](mission.md#8-decisions-locked)). Remaining open questions deferred to build:

- **Smartsheet "Sync Now" button location:** dedicated row in `ITS_Config`, or dedicated `ITS_Portal_Sync_Trigger` sheet with single checkbox? Recommendation: dedicated single-row sheet for clarity.
- **Form-specific Box subfolders:** all forms file to `D. JSA's/`, or each form gets its own subfolder (`D. JSA's/`, `E. Daily Site Safety/`, `F. Equipment/`, `G. Toolbox Talks/`)? Recommendation: separate subfolders.
- **localStorage draft auto-prune cadence:** 7 / 14 / 30 days? Defer to UX testing.
- **Toolbox Talk topic library:** free-text topic per submission, or library of pre-written topics PMs select from with editable body? Defer to operator-Evergreen discussion.
- **Daily Reports `source` column:** add column distinguishing portal vs. legacy origin. Recommendation: yes, as a small migration PR after Phase 5 lands.
- **Sign-out vs. session timeout:** explicit Sign Out only confirmed; no idle timeout (per zero-friction goal).
- **Per-form PDF override escape-hatch trigger:** when does a form get `pdf_override.ts`? Heuristic recommended: only when generic walker cannot represent the layout (e.g., Daily Site Safety sum-to-100 grid).
- **ITS_Trusted_Contacts.Scope schema (post-Correction-A):** does `portal-noreply@` need multi-value scope (`safety_reports + safety_portal`)? Defer; current single-value scope is acceptable for v1 attribution.
- **Q2b per-user password scheme:** locked at Phase 7 build session (lastname+year vs random-passphrase vs other).
- **Q10 D1 backfill strategy for box_upload_verified at production cutover:** lazy (let staleness alert surface) or bulk-verify migration script? Recommendation: lazy for validation, bulk-verify for production.

## Authority

ITS Safety Portal Brief v1, 2026-05-25 canonical. Companion to [mission.md](mission.md). All Q1–Q10 grill-me decisions absorbed.

v2 trigger: substantive engineering architecture change (e.g., schema runtime overhaul, authentication model swap, hosting platform change). Status-overlay updates (v1.1, v1.2) absorb implementation progress without architecture changes.

Cross-references:
- [Mission](mission.md) — invariants, audience, decisions locked, integration, risks.
- [Forensic audit 2026-05-25](../../audits/2026-05-25_forensic-audit.md) — F22, F23, F08+F09 cluster updates.
- [Grill-me session log 2026-05-25](../../session-logs/2026-05-25_safety-portal-grill.md) — Q1–Q10 decision rationale.
- [Operational Standards](../../doctrine/operational-standards.md) — patterns honored.
- [Foundation Mission](../../doctrine/foundation-mission.md) — invariants inherited.
- [safety_reports brief](../safety-reports/brief.md) — sibling workstream sharing the downstream pipeline.
