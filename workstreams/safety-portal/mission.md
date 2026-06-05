---
type: mission
version: 2
status: canonical
last_verified: 2026-06-05
last_verified_against: 753f12f
supersedes: workstreams/safety-portal/mission.md@v1
workstream: safety_portal
tags: [workstream-mission, customer-facing, external-input-surface, external-send-gate, standalone-workspace, pull-transport, clean-break]
---

# ITS Safety Portal — Mission v2

2026-06-05 — As-built reconciliation. Absorbs the 2026-06-04/05 design+build sessions (Phases 2–4 landed) and the architecture decisions that postdate v1: standalone `ITS — Safety Portal` workspace, Cloudflare **Workers + Static Assets** (not Pages), **Python Option-B** PDF rendering, the **`WSR_human_review`** central approval sheet, **6-digit `AUTO_NUMBER` Job ID** (legacy kebab `Job Slug` retired), **Saturday→Friday** weeks, and **TEXT** recipient columns. Foundation Mission reference bumped v8 → v11.

**2026-06-05 transport+clean-break delta (verified against exec `753f12f`, PR #171):** the v2 **email shim is retired** — transport is a **Python PULL model** (send-free Worker D1 queue → Mac-side `portal_poll.py`; §1, §7). Safety intake is **portal-only at launch** (clean break — see [brief §8.1](brief.md#81-clean-break-safety-intake-is-portal-only-at-launch)); `WPR_Pending_Review` is **decommissioned** in favor of `WSR_human_review`, and the `safety_reports` docs are reconciled this session. Phase 5 PRs 1+2 (`ffad86b`/`fc034eb`) + the **`intake_poll.py` retirement** (PR #171, tombstoned) landed; `portal_poll.py` + the intake portal-branch + the `weekly_*` WSR rewire remain in-flight (so `WPR_Pending_Review` is decommissioned-by-doc until that rewire lands). Companion: [2026-06-05 transport+clean-break session log](../../session-logs/2026-06-05_safety-portal-transport-cleanbreak.md).

*Originated from `safety_portal_architecture.md` v1 draft (2026-05-24); split into [mission](mission.md) + [brief](brief.md) per the [new-workstream scaffold](../../prompts/scaffold/new-workstream.md). v1 absorbed the Q1–Q10 grill-me decisions ([2026-05-25 session log](../../session-logs/2026-05-25_safety-portal-grill.md)); v2 absorbs the build-session decisions ([2026-06-05 session log](../../session-logs/2026-06-05_safety-portal-blueprint-update.md)).*

## 1. Purpose

Replace the inbox-and-PDF safety-report submission path with a web portal that field PMs use to submit daily safety paperwork directly. Field PMs log in, pick a project, pick a form, fill structured fields, capture per-worker signatures on-screen, and submit. The structured submission is handed to the existing `safety_reports` pipeline via a **send-free Cloudflare Worker queue** that a Mac-side poller (`portal_poll.py`) drains — the **Python PULL transport** (no email shim); the pipeline renders the matching PDF in Python (Option B) as a derived artifact.

The shift is from "extract structure from handwritten PDFs after the fact" to "enforce structure at entry, render the PDF as a derived artifact." This eliminates OCR confidence loss, handwriting illegibility, multi-day packet splitting, Spanish-name normalization fragility, and most of the SDK-vs-Live extraction surface a prior `jha_split.py` plan would have built.

**The portal facilitates; the Python scripts run the pipeline.** The portal is a thin capture-and-hand-off surface. It owns authentication, form display, signature capture, and a durable receipt of each submission. It does **not** run the pipeline: it never touches Smartsheet or Box, never calls Anthropic, and never sends a customer-facing message. The per-submission PDF render, all Smartsheet writes, all Box filing, weekly compilation, and the gated weekly send are owned by the existing Python pipeline ([`safety_reports`](../safety-reports/mission.md), which holds the only write credentials). This division is the [External Send Gate](#7-foundation-invariants-inherited) two-process model expressed as a deployment boundary, not just a code boundary.

## 2. Audience

Three distinct audiences with different surfaces:

- **Field PMs (portal users):** Daniel, Devin, Henry, and equivalent field-side roles on each active project. They submit forms. They never see Smartsheet, Box, or any ITS operator surface.
- **Office PMs (administration users):** Whoever maintains the active-jobs list. They edit `ITS_Active_Jobs` (job list, contacts, Active/Inactive/Archived status) in Smartsheet. They never log into the portal as a field user.
- **Approvers + operator-maintainer (initially Seth, eventually a trained Evergreen employee):** Approvers review, edit, and approve the compiled weekly report in the `WSR_human_review` sheet. The operator provisions portal accounts via a backend admin route, monitors submissions via existing operator surfaces (`ITS_Daemon_Health`, `ITS_Errors`), and ships new forms by adding declarative form definitions with AI assistance.

Submissions flow into the downstream surfaces the Python pipeline owns: per-job **week sheets** in the `ITS — Safety Portal` workspace, the Box job/week folder tree (system of record), the weekly compiled PDF, and the customer-facing approval sheet `WSR_human_review` (see [Integration](#10-integration-with-safetyreports-workstream)). The portal writes to **none** of these directly.

## 3. Inputs

- **Field PM credentials** — `lastname.firstname` username + bcrypt-hashed password (per-user, operator-provisioned via admin route). Session cookie persists 90 days.
- **PM-selected work date** — ISO date, unbounded backdating window per operator decision (risk-accepted; see [Risks](#12-risks)). The work date determines the **Saturday→Friday week** the submission buckets into (weekend work rolls forward to the following Friday).
- **PM-selected project** — from the portal's own D1 store, populated from Smartsheet `ITS_Active_Jobs` out of band. **The portal never reads Smartsheet at request time.** Only `Active` jobs are offered. The job's permanent key is its **6-digit `AUTO_NUMBER` Job ID** (`JOB-000001`); the human-readable **Project Name** is display only.
- **PM-selected form** — from the catalog the portal serves out of D1 (populated from `ITS_Forms_Catalog`), filtered to the selected job, with parent/variant collapse under a third picklist (see [Forms](#9-decisions-locked)).
- **Form payload** — per-form structured fields, schema-validated client-side and server-side. Worker roster entries with per-row name + company + signature (SVG path data, optional). Equipment checklists are **tri-state (OK / NOT OK / N/A)**.
- **Pipeline receipt callback** — the Python pipeline POSTs back to the portal after the submission is filed, flipping the D1 receipt so the portal can show "received & filed." The callback is **fail-closed**: an unconfirmed submission stays visibly pending.

## 4. Outputs

- **HMAC-signed D1 queue entry** — on `POST /api/submit` the send-free Worker HMAC-signs the submission and stores it in D1 as a durable queue entry. The Mac-side `portal_poll.py` daemon pulls it over the bearer-gated `GET /api/internal/pending`, verifies the HMAC, and hands it to the pipeline. **No email is sent.** Dedup keys on the submission UUID.
- **D1 submission record** — the portal's durable record of every submission (payload, work date, PM, HMAC, `box_verified` / `filed_at` receipt fields). This is the portal's only native system of record; everything customer-facing lives downstream.
- **(Downstream, pipeline-owned, listed for completeness)** — a per-submission PDF rendered in Python (Option B), filed to Box and reflected as a row in the per-job **week sheet**; the weekly **compiled PDF**; the `WSR_human_review` approval row. **Box is the system of record**, its folder tree mirroring the Smartsheet job/week hierarchy.

## 5. Success criteria

- **Zero handwritten-PDF safety submissions from onboarded field PMs by 60 days post-validation cutover.** Measured via week-sheet `source` (portal vs legacy).
- **OCR-derived extraction surface retired for safety reports.** A `jha_split.py`-style extraction plan is superseded; structured payload at entry replaces extraction at receipt.
- **PM submission median latency < 2 minutes** from login to confirmation, including form fill + signature capture.
- **Zero customer-facing send caused by AI-process compromise.** Guaranteed structurally: the portal cannot send customer-facing mail, and the only external send (`weekly_send`) reads an approved, human-edited row from `WSR_human_review` (Invariant 1, two-process).
- **A trained Evergreen operator can ship a new form (or variant) end-to-end** — declarative definition + `ITS_Forms_Catalog` row — in under 1 hour with AI assistance, with the TS display runtime and the Python renderer both honoring the single definition without drift.

## 6. Out of scope

- **No payment, timesheet, or financial data.** Portal stores form payloads + signatures only. Per the Q2 threat model, this scoping is the substantive defense behind the bcrypt-hashing decision — the portal stores nothing of direct value.
- **No personnel master database in v1.** Worker names are free-text per row. Name normalization is deduplicated only within the weekly aggregator's case-insensitive walk.
- **No mobile native app.** Browser-based; signature canvas uses standard touch events.
- **No idle session timeout.** Explicit Sign Out only (zero-friction operator goal).
- **No self-service password reset for field PMs.** Operator-mediated reset only.
- **No retroactive customer send for backdated submissions.** A sent weekly report is frozen at send time; the operator decides whether to send an addendum (manual).
- **No AI calls from the portal at submission time.** The portal is structured-payload-only; the downstream `weekly_generate` step (owned by `safety_reports`) is the only AI call site in the pipeline.

## 7. Foundation Invariants Inherited

Per [Foundation Mission v11](../../doctrine/foundation-mission.md). The Safety Portal touches **both** external-bound send (the weekly report) **and** external-content ingestion (every field-PM submission), so it restates **both** invariants verbatim from doctrine, then states the portal-specific application. The canonical statements below are quoted from doctrine; the doctrine wins on any conflict.

### Invariant 1 — External Send Gate

Canonical statement ([Foundation Mission §Invariant 1](../../doctrine/foundation-mission.md#invariant-1-external-send-gate-unchanged-from-v7)):

> No external transmission without explicit human approval. Permanent, not time-bounded. Earlier framing in Op Stds v4 that described review as a 30-60 day window is superseded.
>
> - Every workstream that produces customer-facing output uses a `<Workstream>_Pending_Review` Smartsheet with Approved for Send / Approved By / Approved At / Sent At / Send Status columns.
> - Two-process model. Generation scripts (which call the Anthropic API) have zero send capability. Send scripts (which transmit) have zero AI step.
> - Successful prompt injection at the AI layer cannot cause external transmission, because the AI is in a different process from the transmitter.
> - Enforced at the code level by `tests/test_capability_gating.py` — every generation script and every send script is registered to the appropriate list there.

**Portal application.** The portal produces no customer-facing output and has **no transmission capability at all** — the Cloudflare Worker is **send-free** (no Graph/Resend, no email; verified in `worker/index.ts`). Submissions are stored in D1 and **pulled** by the Mac-side `portal_poll.py`; the portal never pushes anything outward. The customer-facing artifact (the weekly report) is gated by the `WSR_human_review` sheet, which **is** the workstream's `<Workstream>_Pending_Review` surface: the **editable email body in that row is the source of truth for the send**, and `weekly_send` (no AI step) transmits only after a human sets `Approve for Scheduled Send` / `Send Now`. The two transmission-relevant components both live on the Python side, **inside** the AST capability-gate (`tests/test_capability_gating.py`): `portal_poll.py` (a puller — send-free) and `weekly_send` (the only customer-facing sender, in `SEND_SCRIPTS`). Choosing a Python pull over a TS email shim *closed* the trust-boundary gap a shim would have opened — a TS sender transmits outside the Python AST scan (decision `decision_phase5-portal-transport`).

### Invariant 2 — Adversarial Input Handling

Canonical statement ([Foundation Mission §Invariant 2](../../doctrine/foundation-mission.md#invariant-2-adversarial-input-handling-revised-in-v8)):

> All content originating outside the operating customer tenant is untrusted data. Six-layer defense (v8 expanded from v7's five). The invariant itself is unchanged from v7; Layers 1 and 6 are revised/added (v8), and Layer 5 is recharacterized as a detection tripwire, not a defense layer (v9, see below).

Portal application of the six layers (every field, every signature, every PM-entered name is untrusted data):

- **Layer 1 (Authentication boundary + scope).** Portal users authenticate via username + bcrypt-hashed password (cost factor 10) against D1. No self-registration; accounts are operator-provisioned. This is the portal's equivalent of the `ITS_Trusted_Contacts` allowlist for the email-intake path. On the transport side, the Layer-1 controls are the **bearer token** gating `/api/internal/*` and the **per-submission HMAC** the Mac-side poller verifies (`shared/portal_hmac.py`) before filing — there is no inbound mailbox to allowlist (the email shim is retired).
- **Layer 2 (Untrusted-content tagging).** The portal calls no Anthropic API. Downstream `weekly_generate` wraps any PM-entered text in `<untrusted_content>` tags via `shared/untrusted_content.py` before any model call.
- **Layer 3 (Capability gating).** The portal has no Smartsheet write, no Box write, no Anthropic, and no customer-facing send. Enforced by Cloudflare Workers binding scope and by `tests/test_capability_gating.py` on the Python side.
- **Layer 4 (Structured output enforcement).** Submissions conform to per-form definitions; payloads failing schema validation are rejected (client + server) and never enter the D1 queue. The Python side validates again before any write (defense in depth).
- **Layer 5 (Anomaly logging — tripwire, not a defense layer).** Per v9 framing, this is a low-effort detection tripwire, not a barrier. Suspicious patterns in PM-entered text route the submission to `ITS_Review_Queue` for human attention; it is never relied on for prevention.
- **Layer 6 (Attachment screening).** Signatures are SVG path data (vector, not raster) — no executable-file risk, and PMs cannot attach arbitrary files. If the portal ever gains file-attachment capability (e.g., site photos), the four-sub-layer screening pipeline (signatures → structural inspection → ClamAV → optional VirusTotal) from [Operational Standards §34](../../doctrine/operational-standards.md) applies before any Box upload or model call.

**HMAC-verified portal payload (load-bearing).** Beyond the six layers, the send-free Worker HMAC-signs every submission (HMAC-SHA256 of the canonical payload) before storing it in D1; the Mac-side `portal_poll.py` re-verifies it (`shared/portal_hmac.py`, constant-time `compare_digest`) before handing the submission to `intake` — a mismatch is rejected/flagged and never filed. The `HMAC_SECRET` lives in a Cloudflare Workers Secret with a macOS Keychain mirror for the poller.

## 8. Self-containment and workspace-as-approval-authority

The whole safety workflow lives in **one standalone Smartsheet workspace, `ITS — Safety Portal`**. The `Safety Portal` folder (`ITS_Active_Jobs` + `ITS_Forms_Catalog`) was **moved** there from `ITS — Operations` with **IDs preserved**; the per-job week sheets and the `WSR_human_review` approval sheet live in the same workspace. Shared infrastructure config (`ITS_Config`, `ITS_Errors`, `ITS_Trusted_Contacts`, `ITS_Review_Queue`, `ITS_Quarantine`) stays in `ITS — System` and is read by sheet ID — it is shared infra, not safety-specific.

Two consequences are load-bearing doctrine:

- **Workspace access = approval authority.** Sharing the `ITS — Safety Portal` workspace is the send-gate access control: the people who can review/edit/approve `WSR_human_review` are exactly the workspace's shared collaborators. There is no separate per-sheet ACL to maintain.
- **The system ships independent of the Forefront/demo structures.** Safety-path code must not depend on non-safety sheets. The Safety Portal can be stood up, demoed, and handed over without the portfolio/operations/archive workspaces. This is why it is a *standalone* workspace rather than a folder inside the five-workspace audience-separated topology of [Operational Standards §23](../../doctrine/operational-standards.md). **Doctrine reconciliation — done:** [Operational Standards v17](../../doctrine/operational-standards.md) (2026-06-05) now acknowledges this sixth, standalone, approval-gated workspace in §23/§24 — doctrine and the as-built are aligned. (Resolves the flag raised in the [2026-06-05 blueprint-update session log](../../session-logs/2026-06-05_safety-portal-blueprint-update.md); the v17 bump was applied in the [transport+clean-break session](../../session-logs/2026-06-05_safety-portal-transport-cleanbreak.md).)

## 9. Decisions Locked

v1 locked the Q1–Q10 grill-me decisions ([2026-05-25](../../session-logs/2026-05-25_safety-portal-grill.md)); v2 supersedes the rows the build sessions changed. Decisions are non-negotiable for the current phase unless explicitly revisited.

| Decision | Resolution (v2) |
|---|---|
| Hosting / deploy | **Cloudflare Workers + Static Assets** (single Worker serves the SPA + same-origin `/api/*`; Cloudflare Pages is in maintenance mode). **Requires Workers Paid (~$5/mo)** — the free plan's 10 ms CPU cap cannot run a secure bcrypt hash. Validation host `safety.evergreenmirror.com`; production on `evergreenrenewables.com`. Supersedes v1's "Cloudflare Pages + Workers." |
| Authentication | Username + **bcrypt (bcryptjs, cost 10)** password hash, `nodejs_compat`. Long-lived (90-day) sessions, no MFA, no complexity rules. `SESSION_SIGNING_SECRET` is a Workers Secret. Plaintext storage rejected (Q2). |
| Active-jobs source of truth | Smartsheet **`ITS_Active_Jobs`** in the standalone **`ITS — Safety Portal`** workspace, office-PM-maintained. **`Active / Inactive / Archived` picklist gates the per-job pipeline** — only `Active` jobs run and appear in the portal. Supersedes v1's "Operations workspace." |
| Job key | **`Job ID` = 6-digit Smartsheet `AUTO_NUMBER`** (`JOB-000001`; UI-created — the API cannot make `AUTO_NUMBER` columns). It is the permanent key the pipeline resolves on. **Project Name** is display. The legacy kebab **`Job Slug` is retired** (vestigial). |
| Recipient routing | Contacts are **TEXT** columns on `ITS_Active_Jobs` (Safety Reports Contact Name/Email + CC 1–5; one email per slot or comma-separated). `MULTI_CONTACT_LIST` is *not* used — it drops external emails on API read-back. `weekly_send` TO = the safety-reports contact; CC = the non-empty CC 1–5. |
| Forms catalog | **`ITS_Forms_Catalog`** in the same standalone workspace. A **parent/variant catalog** (5 parents + 7 variants live): a no-variant parent renders its own definition; a variant parent collapses its variants under a **third picklist** (JHA supports future job-specific variants the same way). |
| Form definitions | **Single-source declarative definitions** (one per form) consumed identically by the **TS display runtime** and the **Python PDF renderer** — the contract that keeps them from drifting. Canonical = the 10 reference PDFs. **Legal-invariants-in-code** (JHA "if conditions change…" footer; equipment lock/tag-out line) are mandatory and non-editable. Equipment checklists are **tri-state OK / NOT OK / N/A** (N/A distinct from blank). |
| PDF rendering | **Python, "Option B"** — the per-submission PDF is rendered server-side in the Python pipeline with render-parity to the Evergreen header, *not* client-side in the browser. Supersedes v1's client-side `pdf_renderer.ts`. |
| Week bucketing | **Saturday→Friday** week (`[Job] — week of [date]`). Weekend work rolls to the following Friday; bucketing keys on the form work-date. Supersedes v1's ISO-week framing. |
| Review + approval | **`WSR_human_review`** — one central sheet in the Safety Portal folder, one row per (job, week): compiled PDF, **editable email body (source of truth for send)**, recipients, `Approve for Scheduled Send` + `Send Now`, auto-stamped Approved By/At. **Review + edit + approve + send happen only here.** Supersedes v1's reliance on `WPR_Pending_Review` in `ITS — Human Review`. |
| Submit pipeline | **Python PULL transport** (no email shim): send-free Worker D1 queue → Mac-side `portal_poll.py` drains bearer-gated `/api/internal/pending` → **HMAC-verified** (`shared/portal_hmac.py`) → `intake.py` portal-marker branch, **dedup on submission UUID** → files → `POST /api/internal/mark-filed` receipt (**fail-closed**) → portal shows "received & filed." Decision `decision_phase5-portal-transport`. |
| System of record | **Box**, with a folder tree **mirroring** the Smartsheet job/week hierarchy. Smartsheet rows carry Box links; the compiled weekly PDF also attaches to the review row. Evergreen retains in Box as long as needed (no OSHA-floor gating in our code). |

## 10. Integration with safety_reports Workstream

`safety_portal` and `safety_reports` are **sibling workstreams sharing one pipeline** (intake → generate → send). Safety intake is **portal-only** at launch (clean break, see [brief §8.1](brief.md#81-clean-break-safety-intake-is-portal-only-at-launch)); the portal feeds the pipeline via the **Python pull transport**, not a shared mailbox. `safety_reports` owns the pipeline; `safety_portal` is its intake source.

| Concern | Owned by |
|---|---|
| Portal UI, auth, form display, signature capture, send-free D1 queue | `safety_portal` |
| The `/api/internal/*` pull endpoints (send-free Worker) | `safety_portal` |
| `portal_poll.py` puller + `intake.py` portal-marker branch (HMAC verify, dedup, receipt) | `safety_reports` (extension) |
| Per-submission **Python PDF render** (Option B), Box filing, week-sheet row write | `safety_reports` |
| Weekly **compile** (Sat→Fri merge), dual-write to week sheet + `WSR_human_review` | `safety_reports` |
| `weekly_generate` (draft) + `weekly_send` (gated send, 7 AM Pacific Monday) | `safety_reports` |
| `shared/approval_verification.py` (F22 row-history check) | `shared/` — protects both workstreams |

The Python pipeline holds the **only** write credentials for Smartsheet and Box; the portal holds none. See [safety_reports mission](../safety-reports/mission.md#mission-carried-forward-from-v5-substance-unchanged) for the end-to-end pipeline scope and [safety_reports brief §What Gets Built](../safety-reports/brief.md#what-gets-built-refreshed-in-v61) for the generation + send module detail. Under the clean break (§8.1), `WPR_Pending_Review` is **decommissioned** in favor of `WSR_human_review`, and the `safety_reports` mission/brief are reconciled accordingly this session. The email *infrastructure* (`graph_client`, `untrusted_content`, `header_forgery`) is **preserved** for the committed [Email Triage](../email-triage/mission.md) workstream — not torn down.

## 11. Phase status (as-built)

| Phase | Scope | Status |
|---|---|---|
| Phase 2 — front-half | Login + SPA + Worker scaffold | **Landed** (PR #158) |
| Phase 3 — job model | Live Job-ID resolution, Saturday→Friday rule, legacy slug retired, schema + contacts amendment | **Landed** (PR #160, #162) |
| Phase 4 — forms | Meta-schema + parent/variant catalog + declarative form definitions; TS display runtime; Python Option-B renderer + equipment tri-state | **Landed** (PR #164, #166, #167) |
| Phase 5 — submission pipeline | **PR 1** (WSR sheet + PDF merge + `sheet_ids`) **landed** (PR #168); **PR 2** (Worker pull transport + `shared/portal_hmac.py` contract) **landed** (PR #169). In-flight Python rewire (not on main): `portal_poll.py`, `intake.py` portal-marker branch, `weekly_*` rewire onto `WSR_human_review` | **In progress** |
| Deploy | D1 sync, secrets, Workers Paid-plan upgrade, custom domains | **Pending** |

## 12. Risks

| Risk | Mitigation |
|---|---|
| Cloudflare outage prevents PM submissions | Accepted submissions are durable in D1 (drained on the next poll — no silent-loss mode); during a full outage PMs fall back to paper, entered when the portal returns. No email-PDF safety path remains post-clean-break (§8.1). |
| Workers Paid-plan lapse | Login (bcrypt) fails closed on the free-tier 10 ms CPU cap (observed: Error 1102). Plan status is an operational pre-req, surfaced in deploy runbook. |
| D1 data loss | D1 point-in-time recovery (35 days); daily export. Job/form data re-syncs from Smartsheet. The submission receipt is the only portal-native durable state. |
| PM forgets password, operator unreachable | PM submits paper that day; operator resets next time online. |
| Backdating + no submission-timestamp on PDF (Q4 risk acceptance) | Operator-acknowledged trade-off: unlimited backdating, no entry-time indicator, in exchange for zero-friction submission. Reversible via PDF-footer additions if a litigation event makes it load-bearing. |
| Late arrival after a week is compiled/sent | Late submissions route to the next uncompiled week + a Review-Queue flag; compile never closes a week (multiple packets/week allowed). A sent report is not retroactively updated; the operator decides on an addendum. |
| Portal becomes an attack surface | Six-layer defense + HMAC + capability gating cap the damage ceiling at "weird Smartsheet rows and weird PDFs in Box" — the same ceiling as the legacy PDF-email path, since the portal cannot send customer mail. |
| Cross-repo drift (blueprint vs `sheet_ids.py`) | **Resolved by Phase 5 PR 1 (PR #168):** `shared/sheet_ids.py` now defines `WORKSPACE_SAFETY_PORTAL`, `FOLDER_SAFETY_PORTAL`, and `SHEET_WSR_HUMAN_REVIEW` (the old `FOLDER_OPERATIONS_SAFETY_PORTAL` name kept as a back-compat alias). |

## Authority

ITS Safety Portal Mission v2, 2026-06-05 canonical. Supersedes v1 (2026-05-25). Companion brief at [`brief.md`](brief.md). Both Foundation invariants restated verbatim from [Foundation Mission v11](../../doctrine/foundation-mission.md).

v3 trigger: substantive scope change — authentication-model swap (e.g., SSO), deploy-platform change away from Cloudflare Workers, submission-pipeline replacement, or a change to the standalone-workspace / workspace-as-approval-authority model. Status-overlay updates (v2.1, v2.2) absorb phase progress without scope changes.

Cross-references:
- [Foundation Mission v11](../../doctrine/foundation-mission.md) — invariants inherited (restated verbatim in §7).
- [Operational Standards](../../doctrine/operational-standards.md) — §23 workspace topology (doctrine-reconciliation flagged in §8), patterns honored.
- [Vision & Roadmap](../../doctrine/vision-and-roadmap.md) — phase placement.
- [safety_reports mission](../safety-reports/mission.md) + [brief](../safety-reports/brief.md) — sibling workstream owning the shared pipeline.
- [Forensic audit 2026-05-25](../../audits/2026-05-25_forensic-audit.md) — F02/F22 capability-gating + approval attestation.
- [Grill-me session log 2026-05-25](../../session-logs/2026-05-25_safety-portal-grill.md) — v1 decision rationale.
- [Blueprint-update session log 2026-06-05](../../session-logs/2026-06-05_safety-portal-blueprint-update.md) — v2 build-session decisions + doctrine-reconciliation flags.
