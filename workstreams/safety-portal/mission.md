---
type: mission
version: 1
status: canonical
last_verified: 2026-05-25
last_verified_against: 40a3509
workstream: safety_portal
tags: [workstream-mission, customer-facing, external-input-surface]
---

# ITS Safety Portal — Mission v1

2026-05-25 — Initial mission, absorbed grill-me session decisions.

*Originated from `safety_portal_architecture.md` v1 draft (2026-05-24); split into [mission](mission.md) + [brief](brief.md) per the [new-workstream scaffold](../../prompts/scaffold/new-workstream.md). All Q1–Q10 grill-me decisions absorbed. Companion grill-me session log: [`session-logs/2026-05-25_safety-portal-grill.md`](../../session-logs/2026-05-25_safety-portal-grill.md).*

## 1. Purpose

Replace the inbox-and-PDF safety-report submission path with a web portal that field PMs use to submit daily safety paperwork directly. Field PMs log in, pick a project, pick a form, fill structured fields, capture per-worker signatures on-screen, and submit. The portal renders a PDF that matches the existing paper form layout, packages it with the structured payload, and hands it to the existing `safety_reports` intake pipeline via an email shim that the polling daemon already knows how to consume.

The shift is from "extract structure from handwritten PDFs after the fact" to "enforce structure at entry, render the PDF as a derived artifact." This eliminates OCR confidence loss, handwriting illegibility, multi-day packet splitting, Spanish-name normalization fragility, and most of the SDK-vs-Live extraction surface that a prior `jha_split.py` plan would have built.

## 2. Audience

Three distinct audiences with different surfaces:

- **Field PMs (portal users):** Daniel, Devin, Henry, and equivalent field-side roles on each active project. They submit forms. They never see Smartsheet, Box, or any ITS operator surface.
- **Office PMs (administration users):** Whoever maintains the active-jobs list. They edit `ITS_Active_Jobs` and `ITS_Forms_Catalog` in Smartsheet. They never log into the portal as a field user.
- **Operator-maintainer-developer (initially Seth, eventually a trained Evergreen employee):** Provisions portal accounts via a backend admin route; monitors submissions via existing operator surfaces (`ITS_Daemon_Health`, `ITS_Errors`); ships new forms by writing single-file declarative `form.ts` modules with AI assistance (Claude / Claude Code); handles edge cases that fall to the review queue.

Submissions flow into the same downstream surfaces as the legacy PDF-email path: `Daily Reports` per-project sheets, Box `D. JSA's/` folder structure, `Weekly Rollup` aggregation, customer-facing `WPR_Pending_Review` drafts.

## 3. Inputs

- **Field PM credentials** — `lastname.firstname` username + bcrypt-hashed password (per-user, operator-provisioned via admin route). Session cookie persists 90 days.
- **PM-selected work date** — ISO date, unbounded backdating window per operator decision (risk-accepted; see [Risks](#10-risks)).
- **PM-selected project** — from `jobs_mirror` (synced daily from Smartsheet `ITS_Active_Jobs`).
- **PM-selected form** — from `forms_catalog_mirror` (synced from Smartsheet `ITS_Forms_Catalog`), filtered by `Available For Jobs` matching the selected project.
- **Form payload** — per-form-version structured fields, schema-validated client-side AND server-side. Worker roster entries with per-row name + company + signature (SVG path data, optional).
- **Portal-internal Box-verification callback** — `intake.py` Stage 12.5 POSTs back to the portal to flip `box_upload_verified` after successful Box archival of each submission's PDF.

## 4. Outputs

- **Cloudflare R2 object** — generated PDF at `submissions/{submission_id}.pdf`, hot-cache for "View PDF" UX. Conditionally pruned 90 days after Box upload is verified (per Q10); retained indefinitely if Box upload never confirmed.
- **D1 `submissions` row** — durable record of every submission with payload JSON, work date, submission timestamp, PM, shim status, Box-upload-verified status, prune marker.
- **Email shim message** — JSON payload + PDF attachment, sent from `portal-noreply@` to the unified `safety@` intake mailbox (consolidated with legacy PDF-email path; trust boundary is HMAC-verified `X-ITS-Portal-*` headers, not destination address).
- **Daily Reports row** (via `intake.py` portal-marker branch) — Smartsheet row keyed off the indicated work date, in the correct per-project per-quarter sheet.
- **Box PDF** — uploaded under `ITS DATA/{Project}/{Year}/W{ISO week}_{Month}{StartDay}-{Month}{EndDay}/D. JSA's/` (or form-specific subfolder pending build-session decision).
- **Weekly Rollup update** — for past-week backdated submissions, the rollup aggregator re-runs synchronously inside `intake.py` Stage 13' to update the corresponding Weekly Rollup row. Already-sent WPRs are NOT retroactively updated; operator surfaces discrepancy via daily watchdog.

## 5. Success criteria

- **Zero handwritten-PDF safety submissions from onboarded field PMs by 60 days post-validation cutover.** Measured via Daily Reports `source` column (portal vs legacy).
- **OCR-derived extraction surface retired for safety reports.** `safety_reports/jha_split.py` plan is superseded; structured payload at entry replaces extraction at receipt.
- **PM submission median latency < 2 minutes.** From login to confirmation page, including form fill + signature capture. Measured via portal-side telemetry.
- **Zero customer-facing send caused by AI-process compromise.** Verified by F02 capability-gating allowlist + F22 row-history approval verification — the architectural defenses that close prompt-injection bypass at both the network-library and approval-column boundaries.
- **Trained Evergreen operator can ship a new form variant end-to-end (schema + Smartsheet catalog row + deploy) in under 1 hour with AI assistance.** Validates the AI-one-shot extensibility design.

## 6. Out of scope

- **No payment, timesheet, or financial data.** Portal stores form payloads + signatures only. Per Q2 threat-model discussion (grill session 2026-05-25), this scoping is the substantive defense of the bcrypt-hashing decision — the portal stores nothing of direct value; hashing prevents credential leakage from becoming a cross-service compromise.
- **No personnel master database in v1.** Worker names are free-text per row, deferred to Phase 2. Name normalization (Mario Martinez vs M. Martinez vs mario martinez) is deduplicated only within the Weekly Rollup aggregator's case-insensitive walk.
- **No mobile native app.** Browser-based PWA; signature canvas uses standard touch events.
- **No idle session timeout.** Explicit Sign Out only (per zero-friction operator goal).
- **No self-service password reset for field PMs.** Operator-mediated reset only via admin route.
- **No retroactive WPR send for backdated submissions.** WPR is frozen at original send time; operator decides whether to send an addendum (manual, not automated).
- **No AI calls from the portal at submission time.** Portal is structured-payload-only; downstream `weekly_generate.py` is the only AI call site in the pipeline (unchanged from current).

## 7. Foundation Invariants Inherited

Per [Foundation Mission](../../doctrine/foundation-mission.md) (canonical v8 as of 2026-05-24). Both invariants apply to this workstream with specific application:

### Invariant 1 — External Send Gate

Portal submissions do not constitute external transmission. The portal writes to operator-controlled Smartsheet and Box surfaces; nothing customer-facing leaves the system without explicit approval. The existing `weekly_send.py` two-process model continues to gate the only external send path (the WPR). Portal submission triggers Weekly Rollup aggregation but does not bypass the WPR approval gate.

**Capability gating extension:** the portal backend's email-shim sender is registered in `tests/test_capability_gating.py` `SEND_SCRIPTS` list. It can send only to the configured `safety@` intake mailbox (operator-controlled, same inbox the polling daemon already monitors); cannot send to any external recipient. Verified by AST test post-F02 (network-library allowlist).

**F22 inheritance (cross-cutting `shared/`-layer protection):** Q3 + Q5 + F22 decisions tightening the WPR_Pending_Review approval boundary protect portal submissions equally, since the portal feeds the same WPR pipeline. Once F22's row-history verification lands in `shared/approval_verification.py`, every workstream's external send path is platform-attested. See [forensic audit F22](../../audits/2026-05-25_forensic-audit.md).

### Invariant 2 — Adversarial Input Handling

The portal is a new external-input surface. The submission payload — every field, every signature image, every PM-entered name — is untrusted data. Six-layer application:

- **Layer 1 (Authentication boundary).** Portal users authenticate via username + bcrypt-hashed password (cost factor 10) against the D1 `users` table. Sessions are long-lived (90 days). This is the trust boundary equivalent to `ITS_Trusted_Contacts` for the email-intake path; portal users are explicitly provisioned by the operator. No self-registration.
- **Layer 2 (Untrusted-content tagging).** All PM-entered text fields are wrapped in `<untrusted_content>` tags when passed to any Anthropic API call. The portal itself does not call Anthropic at submission time, but downstream aggregation (the JHA Weekly Compliance Rollup if it ever runs an LLM pass for pattern detection) honors this layer.
- **Layer 3 (Capability gating).** The portal backend has exactly four write capabilities: write to D1 (its own database), send to the operator-controlled `safety@` intake mailbox via the email shim, read from Smartsheet (`ITS_Active_Jobs`, `ITS_Forms_Catalog`), and serve HTTP responses. It cannot write to Smartsheet, cannot write to Box, cannot call Anthropic, cannot send to any other email recipient. Enforced by Cloudflare Workers binding scope.
- **Layer 4 (Structured output enforcement).** Form payloads conform to per-form JSON schemas defined in code (one declarative `form.ts` per form directory). Submissions that fail schema validation route to a portal-side error log and never reach the email shim.
- **Layer 5 (Anomaly logging).** Suspicious patterns in PM-entered text (sentinel patterns matching `system_*`, `role_*`, `ignore_*`, prompt-injection attempts) flag the submission to `ITS_Review_Queue` via the existing email-shim pipeline. Per Q8 doctrine reconciliation, this is acknowledged as a tripwire-grade defense, not a load-bearing security layer.
- **Layer 6 (Attachment screening).** Signature images are SVG path data (vector, not raster); no executable file format risk. PMs cannot attach arbitrary files. If the portal ever adds file-attachment capability (e.g., site photos), Layer 6 from the [Operational Standards](../../doctrine/operational-standards.md) attachment-screening pattern applies: signature, structural inspection, ClamAV scan.

**HMAC-verified portal payload (Q3 decision, load-bearing post-Correction-A):** beyond the six layers, every portal-shim message carries an HMAC-SHA256 signature in a dedicated `X-ITS-Portal-HMAC` header. `intake.py` verifies the HMAC before the portal-fast-path activates; mismatch routes to `ITS_Quarantine` with CRITICAL alert. Shared secret in Cloudflare Workers binding + macOS Keychain. Since Correction A consolidated portal traffic onto the same `safety@` intake mailbox as legacy PDFs, the HMAC IS the second factor distinguishing portal payloads from impersonation attempts (the address no longer is).

## 8. Decisions Locked

All resolved with operator across two sessions (2026-05-24 architecture + 2026-05-25 grill-me). Decisions are non-negotiable for v1 unless explicitly revisited. Q-references indicate decisions absorbed from the [2026-05-25 grill-me session log](../../session-logs/2026-05-25_safety-portal-grill.md).

| Decision | Resolution |
|---|---|
| Portal vs. inbox-PDF as primary submission path | Portal. PDF-email path remains operational during transition, sunsets when portal adoption is real. |
| **Authentication password storage** | **Username + bcrypt-hashed password (cost factor 10)** — Q2. Long-lived sessions (90-day), no MFA, no complexity rules, no rotation. Plaintext storage is NOT acceptable per Q2 threat-model resolution; hashing is non-reversible decision at code-write time. |
| Per-user password scheme | **Deferred to Phase 7 / build session** — Q2b. Lock the scheme at admin-route implementation; per-user-variability mandatory (shared passwords incompatible with audit-trail defensibility). |
| Hosting / domain | Cloudflare Pages + Workers + D1 + R2. Validation deployment at `safety.evergreenmirror.com`. Production migration to `safety.evergreenrenewables.com` via CNAME when validated. |
| Forms catalog at v1 | All four daily forms: JHA, Daily Site Safety Worksheet, Equipment Pre-Inspection, Toolbox Talk. |
| Active jobs source of truth | New Smartsheet `ITS_Active_Jobs` in Operations workspace, office-PM-maintained. |
| **Forms catalog source of truth** | New Smartsheet `ITS_Forms_Catalog` in Operations workspace. **Forms may be globally available (default) OR job-scoped via `Available For Jobs` column** — Q6. Replaces the original "Forms are global (not per-project)" lockup. Supports the JHA-Bradley use case (per-client form variants). |
| Form schema versioning + structure | **One declarative `form.ts` per directory + shared `_runtime/` renderer + PDF generator** — Q6b. Code-canonical; `Form Version` column dropped from `ITS_Forms_Catalog`. Operator extends via AI-one-shot workflow (paste existing form into Claude, describe changes, paste result back). Captured in operator memory at `~/.claude/projects/-Users-sethsmith/memory/project_ai_one_shot_extensibility.md` (outside this repo). |
| Sync mechanism | Daily midnight cron + manual "Sync Now" button via Smartsheet webhook → Cloudflare Workers endpoint. |
| Active project flag | Picklist column (Active / Inactive / Archived). |
| Personnel database | None in v1. Free-text name + signature canvas per row. Phase 2 introduction triggered by ≥4 real reuse cases per [preservation-over-refactor convention](../../doctrine/operational-standards.md). |
| Signature handling | Per-row on-screen signature capture, SVG path data, rendered inline on PDF. |
| Backdating | Unlimited. PM selects work date; no upper bound. Submission timestamp NOT surfaced on PDF or Smartsheet row. **Q4 risk-acceptance:** operator accepts the litigation-defensibility trade-off in favor of PM zero-friction; see [Risks](#10-risks). |
| **Submit pipeline (unified inbox post-Correction-A)** | Email shim. Portal generates PDF + JSON payload, sends to the unified `safety@` intake mailbox (`safety@evergreenrenewables.com` production / `safety@evergreenmirror.com` validation) — same address legacy PDF-email submissions land in. Polling daemon picks up; `intake.py` allowlist-gates first, then HMAC-verifies `X-ITS-Portal-Submission-Id` header, then takes the portal fast-path or falls through to legacy classification. Trust boundary is HMAC + header shape, NOT destination address. |
| **HMAC-signed portal payload** | **Q3.** HMAC-SHA256 of canonicalized payload, signed by the shim Worker, verified in `intake.process_message` before fast-path. Reject on mismatch with CRITICAL triple-fire alert. Ships with Phase 5 initial deploy. Load-bearing post-Correction-A consolidation. |
| **R2 PDF retention policy** | **Q10.** Conditional 90-day prune via daily Cron Worker: prunes only after `submissions.box_upload_verified=true`. Indefinite retention for un-verified submissions (only-copy safety). 24h staleness alert (WARN, aggregated) for submissions with `shim_status=sent AND box_upload_verified=false`. Confirmation/Recent-submissions UI hides "View PDF" past prune (option a). |

## 9. Integration with safety_reports Workstream

`safety_portal` and `safety_reports` are sibling workstreams sharing the downstream pipeline. They do not overlap on intake (post-Correction-A, they share the same `safety@` inbox; intake.py routes via HMAC-verified header). They overlap on the consumer side (Smartsheet writes, Box uploads, Weekly Rollup aggregation, WPR generation).

**Module boundaries:**

| Concern | Owned by |
|---|---|
| Portal UI, auth, form schemas, PDF rendering, submission storage | `safety_portal` |
| Email shim sender (`portal-noreply@` → unified `safety@` intake mailbox) | `safety_portal` |
| `intake.py` portal-marker branch (Stages 1.5, 8'–13' + Stage 12.5 D1 verification callback) | `safety_reports` (extension) |
| `week_folder.py`, Daily Reports row write, Box upload | `safety_reports` |
| `weekly_generate.py` + `weekly_send.py` (WPR generation + send) | `safety_reports` |
| JHA Weekly Compliance Rollup aggregator | `safety_reports` |
| `shared/approval_verification.py` (F22 row-history check, cross-cutting `shared/` layer) | `shared/` — protects both workstreams |

**Shared infrastructure:**
- `shared/smartsheet_client.py` — both workstreams use it.
- `shared/box_client.py` — both workstreams use it (read-only for safety_portal sync; full read/write for safety_reports intake).
- `shared/graph_client.py` — safety_reports only.
- `shared/keychain.py` — safety_reports continues to use it for M365 + Box + Anthropic; new `ITS_PORTAL_INTERNAL_API_TOKEN` for portal's Box-verification callback (Q10 Step 12.5).
- `shared/state_io.py` (NEW per F19+F23 bundle) — `atomic_write_json` + `with_path_lock`; safety_reports adopts; safety_portal not directly affected but shares the lesson.
- `shared/circuit_breaker.py` (NEW per F08) — `smartsheet_client` first consumer; pattern extends to `graph_client` + `box_client` in follow-on PR.

**Capability gating extension** (post-F02 network-library allowlist):
- `tests/test_capability_gating.py` `GATED_SCRIPTS` list adds the portal Worker submit handler (no Smartsheet write, no Box write, no Anthropic).
- `SEND_SCRIPTS` list adds the portal email-shim Worker (M365 send capability, scoped to the configured `safety@` intake mailbox only).
- `safety_reports/portal_notify.py` (NEW per Q10 Stage 12.5) joins the network-library allowlist with rationale comment.

## 10. Risks

| Risk | Mitigation |
|---|---|
| Cloudflare Pages outage prevents PM submissions | PMs revert to paper + email path during outage. Polling daemon picks up paper-PDF submissions as before. |
| D1 data loss | Cloudflare D1 has point-in-time recovery (35 days). Sync Workers re-populate `jobs_mirror` and `forms_catalog_mirror` from Smartsheet on next cron. Submissions table loss is genuinely bad. Mitigation: daily D1 export to R2. |
| PM forgets password and operator unreachable | PM submits paper version that day. Operator resets password next time online. |
| Smartsheet outage during sync | Sync fails, logs to ITS_Errors. Mirror tables retain previous state. Portal continues to work with stale data until next successful sync. |
| Browser localStorage cleared mid-form | Draft loss. PM re-enters form. Communicate "don't clear browser data mid-shift" in onboarding. |
| PM submits same form twice (network retry duplicate) | Backend dedupes on `(username, form_code, work_date, job_id)` if a submission with those keys was inserted within the past 5 minutes. |
| Signature canvas does not work on legacy browser | Onboarding: PMs given a known-working browser configuration. |
| Workers cron does not fire | Sync staleness up to 24 hours. Manual Sync Now button available. |
| Schema drift between portal frontend and backend | Single source of truth: `form.ts` modules imported by both layers. CI fails on schema-referenced-from-only-one-side. |
| Late submission triggers Weekly Rollup recompute on a week with an already-sent WPR | Daily watchdog surfaces the discrepancy. Operator decides whether to send WPR addendum. No automated retroactive WPR send (Invariant 1). |
| Portal becomes attack surface (per Adversarial Input Handling) | Six-layer defense + HMAC. Capability gating + F02 + F22 (post-fix) limit damage ceiling to "weird Smartsheet rows and weird PDFs in Box" — same ceiling as legacy PDF-email path. |
| Personnel name normalization deferred to Phase 2 | v1 stores names verbatim. Weekly Rollup aggregator dedupes by case-insensitive normalized form. Personnel master DB introduction triggered by ≥4 real reuse cases. |
| **Backdating + missing submission-timestamp on PDF (Q4 risk acceptance)** | **Operator-acknowledged trade-off (2026-05-25):** unlimited backdating, no submission-timestamp indicator on PDF or Smartsheet row, in exchange for PM zero-friction submission. Litigation defensibility scenario: a PM (or anyone with PM credentials) could submit a JHA dated months prior with no audit trail of when it was actually entered. Mitigation deliberately not pursued; operator owns the consequence. If a specific litigation event makes this load-bearing, reverse via PDF-footer additions (~2 hours) without redesigning the submission flow. |
| **F08 / F09 / F19 / F23 cluster dependency (operational hygiene before launch)** | Portal launches only AFTER Phase 1.4 hardening cluster lands per Q1: F02 + F22 (capability gating + approval attestation), F19 + F23 (`shared/state_io.py` atomic-write bundle), F08 + F09 (Smartsheet circuit-breaker + alerts-per-hour cap), F16 + F17 + F18 + F03 + F04 + F10 (observability + tag-escape + keychain + lockfile). Cluster scope discipline: if F08 grows past ~2.5 days, cutover slips (not F08). See [forensic audit](../../audits/2026-05-25_forensic-audit.md). |
| **Single-mailbox routing risk (Correction A)** | Email consolidation to `safety@` (per operator decision 2026-05-25) doubles the blast radius if `safety@` is unavailable. HMAC verification becomes load-bearing (no longer a second layer over dedicated-inbox separation). Operator inbox triage burden increases slightly. ITS_Trusted_Contacts.Scope schema may want multi-value for `safety_reports + safety_portal` attribution accuracy — deferred to build session. |

## Authority

ITS Safety Portal Mission v1, 2026-05-25 canonical. Companion brief at [`brief.md`](brief.md). All Q1–Q10 grill-me decisions absorbed; companion session log: [`session-logs/2026-05-25_safety-portal-grill.md`](../../session-logs/2026-05-25_safety-portal-grill.md).

v2 trigger: substantive scope change — authentication-model swap (e.g., SSO), hosting-platform change, submission-pipeline replacement. Status-overlay updates (v1.1, v1.2) absorb implementation progress without scope changes.

Cross-references:
- [Foundation Mission](../../doctrine/foundation-mission.md) — invariants inherited.
- [Operational Standards](../../doctrine/operational-standards.md) — patterns honored.
- [Vision & Roadmap](../../doctrine/vision-and-roadmap.md) — Phase placement: Phase 1.6+ as a new workstream beyond the security hardening cluster.
- [safety_reports mission](../safety-reports/mission.md) + [brief](../safety-reports/brief.md) — sibling workstream sharing the downstream pipeline.
- [Forensic audit 2026-05-25](../../audits/2026-05-25_forensic-audit.md) — F22 (approval attestation), F23 (heartbeat state file) added during the grill session.
- [Grill-me session log 2026-05-25](../../session-logs/2026-05-25_safety-portal-grill.md) — decision rationale.
