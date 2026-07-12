---
type: mission
version: 1
status: canonical
last_verified: 2026-07-12
last_verified_against: e242074
workstream: field_ops
tags: [workstream-mission, field-capture, external-input-surface, d1-primary, portal-as-writer, its-owned-sor-write-back, code-actuation-gate, capability-tiers, manager-tier, subcontractor-tier, job-tracker-authoritative, dual-active-jobs-mirror, site-photos-option-d, image-attachment-screening, sop-daily-form, checklist-engine, material-receipts, crew-time-amend, no-external-send, standalone-workspace-pair]
---

# ITS Field-Ops Portal — Mission v1 (as-built)

*Originated as the Field-Ops Expansion of the [Safety Portal](../safety-portal/mission.md) (program start 2026-06-27), built by porting and hardening the URS-Marine field-ops layer under ITS doctrine. This v1 mission is the first blueprint capture of the workstream as-built — condensed from the exec-side program record — pinned to exec `e242074`.*

## 1. Purpose

Turn the Safety Portal into the firm's **field-operations capture system**. Field PMs, managers, and subcontractors log in and run the daily site loop from a browser: create and lifecycle jobs, keep a crew/personnel roster, track equipment (status / location / logs), log time (with append-only corrections), receive expected materials and file material incidents, run assigned tasks and a **daily SOP form** (the Site Supervisor SOP rendered as a guided, deep-linked form), and complete inspection checklists. Photos are captured against a §34-screened pool.

The Field-Ops Portal is the same Cloudflare **Worker + D1 + SPA** application as the Safety Portal — one deployment, one auth/session model, one capability system. It is a **thin, send-free capture-and-hand-off surface**: it owns authentication, form display, and a durable D1 record of everything captured; it never calls Anthropic, never sends customer-facing mail, and holds no Smartsheet or Box write credentials. Structured writes flow to the systems of record through the Mac-side daemons (below).

## 2. Scope

- **Job Tracker (authoritative writer).** The portal "new job" form is the authoritative job-creation and lifecycle (`active | inactive | archived`) writer. It assigns the canonical `JOB-######` and carries a parallel Safety + Progress routing block (contacts + CC, "Same as safety" copy) — the PM no longer hand-edits Smartsheet rows.
- **Personnel + tiers.** Accounts plus an optional non-login roster; DB-driven capability model (migration `0013`: `roles` / `capabilities` / `role_capabilities`, resolved per request, **fail-closed**). Four presented tiers: **subcontractor** (a display label over the `submitter` key — security fail-safe default), **submitter** (field PM), **manager** (crew lead — personnel + crew-assign, full task authority), **admin** (accounts, form-builder, submit-as).
- **Equipment, time, materials, tasks, checklists.** Equipment roster + status/location/machine logs; time entry with a server-authoritative append-only `amends_uuid` correction chain; per-job expected-materials receive (`cap.materials.receive`) + material incidents; assigned-tasks / My-Tasks; a checklist engine (templates → instances) serving both the daily flow and admin-composed inspection libraries.
- **Site photos.** A constrained image-attachment class, §34-screened on the Mac (see §4).
- **Out of scope.** No external send from anywhere in this workstream; no warehouse inventory (materials = catalog + per-job receive/incidents only); no canonical-Evergreen PJOB→JOB integration (deferred, [decision_p2.4](../../references/memory-archive.md)); no AI at capture time.

## 3. Architecture — portal-as-writer, §51 ITS-owned-SoR write-back

**D1 is the primary; the daemon mirrors UP.** All field-ops data is written to D1 first by the send-free, code-free Worker (`20+ fieldops_*.ts` route modules — job/task/time/equipment/personnel/material/checklist writes, each capability-gated as Hono middleware, every mutation batched with its audit row). The Mac-side daemon **`field_ops/fieldops_sync.py`** (launchd `org.solutionsmith.its.fieldops-sync`, StartInterval + RunAtLoad) is the sole privileged actuator that carries D1 up into the Smartsheet systems of record:

- **Dual Active-Jobs mirror.** Dirty portal-origin jobs mirror UP into **BOTH** `ITS_Active_Jobs` (Safety workspace) **and** `ITS_Active_Jobs_Progress` (Progress workspace) via `shared/active_jobs_writer.py` (find-or-create keyed on the **`Portal Job Key`** column; lifecycle → the `Active` picklist). One writer ⇒ the safety and progress workstreams never drift.
- **Progress mirror passes.** The same daemon drives the progress **hours / equipment / materials / incidents** mirror passes (`_mirror_hours_pass` / `_mirror_equipment_pass` / `_mirror_material_list_pass` / `_mirror_material_incidents_pass`, using `progress_reports.{hours_log, equipment_status, material_list, material_incidents}`) — **one host / lock / heartbeat**, each pass independently gated by its own ITS_Config `polling_enabled`.
- **Egress is allowlisted, never a raw send.** All HTTP to the ITS Worker goes through `shared/portal_client.py` (bearer `ITS_PORTAL_FIELDOPS_TOKEN`, F02-allowlisted); the module imports no raw network library, no `anthropic*`, and no `graph_client.send_mail` / `resend` / `smtplib` / `email.mime`. This is the **§51 ITS-owned structured-SoR write-back** actuated through the **§50 privileged code-actuation gate**.
- **Identity + consistency.** The portal assigns `JOB-######` from a D1 `job_counter` singleton (migration `0022`, allocated atomically after validation so a rejected create never burns a number); `origin` stays `'portal'` forever; `canonical_job_id` is set from birth; a `mirror_version` + per-sheet watermarks (`safety_mirrored_version` / `progress_mirrored_version`) with a **per-sheet mark-mirrored commit point** make a dual-sheet partial failure self-healing on the next cycle (at-least-once, idempotent). Watched by watchdog Check C (marker slug `fieldops_sync`) + an `ITS_Daemon_Health` row.

## 4. Foundation invariants inherited

Per [Foundation Mission v11](../../doctrine/foundation-mission.md); doctrine wins on any conflict.

- **Invariant 1 — External Send Gate: no external send exists in this workstream.** The Worker is send-free (no Graph/Resend, no email path), and `fieldops_sync.py` is customer-send-free — its Smartsheet WRITE is SoR mirroring, not a customer transmission — and is enrolled in `tests/test_capability_gating.py` `GATED_SCRIPTS` (AI-free, send-free, enforced at import). The only customer-facing sends in the wider system are the sibling weekly reports (`weekly_send` / `progress_send`), which read a human-approved row from `WSR_human_review` / `WPR_human_review` — a separate, gated, two-process path this workstream never touches.
- **Invariant 2 — Adversarial Input Handling.** Every field-PM entry, name, and photo is untrusted data. The **SPA capability checks are convenience only — the Worker re-gates every call server-side** (the real boundary). D1 mutations and their audit rows are written in one atomic `db.batch([...])`; job-scoped reads flow through `worker/fieldops_scope.ts`; crew/task/report-facing WHO fields resolve display-name-only. **Site photos = §34 Option-D screened pool** ([reference](../../references/memory-archive.md)): capture → Mac `safety_reports/photo_screen.py` §34 screen (magic → Pillow `verify()` / decompression-bomb cap / forced metadata-destroying re-encode → ClamAV-on-raw) → Box → **delete-on-screen** (D1 holds bytes only while pending; **no serving route ever**); a domain-separated HMAC covers the payload; a non-clean photo refuses before filing (MALICIOUS → CRITICAL naming the account + a security-flagged Review-Queue row).

## 5. Current state — LIVE (P2.5 up-sync cut over; field-capture suite built + verified)

- **P2.5 job up-sync is LIVE** (cut over 2026-07-01, validated end-to-end): a portal-created job received the portal-assigned `JOB-000017` and mirrored into **both** Active-Jobs sheets with `Job ID = Portal Job Key = JOB-000017` (confirmed by direct sheet reads). The daemon runs at a 90s interval, `field_ops.fieldops_sync.sync_enabled = true`.
- **Field-capture suite built + four-part verified on `main`:** Job Tracker + unified job-create flow; the manager tier (`0023`, `cap.crew.assign`) and subcontractor tier (`0027`, `cap.crew.create`); equipment multi-view; assigned-tasks / My-Tasks; the **SOP daily form** (`daily-report-v2+`, the Site Supervisor SOP as a guided deep-linked form with live Filed✓ indicators and loop-closure into the weekly pipeline); per-job daily-requirements overlays; the checklist engine + inspection library; material receipts + incidents (`0031`); crew time corrections (append-only amend chain); item photos (Option-D). Design-language + optimization/resiliency passes landed.
- **Progress-Reporting workstream go-live is complete + deployed** (Track 0, exec `cb58ca8`): progress `ITS_Config` rows set, `compile_now_poll` generalized across safety + progress, F22 approver set resolved from workspace membership.
- **Residual operator follow-up:** create the `progress@evergreenmirror.com` mailbox + add it to the Entra `Mail.Send` Application Access Policy before any progress send (tracked its#460; a missing mailbox HELDs at approval, never sends silently). Standard cutover discipline: apply pending D1 migrations `--remote` **before** `npm run deploy`; deploys are operator-terminal-only.

## Superseded design (do not re-introduce as current)

- **The 0017 "origin-flip" identity model is retired as a BUG.** An earlier design flipped a promoted portal job's `origin` to `'smartsheet'` (with a canonical-job-id conversion) on mirror. That was replaced by the **typed-key-stable** model: `origin='portal'` forever, a `Portal Job Key` TEXT bridge column carrying the downstream join, no AUTO_NUMBER→TEXT conversion.
- **Office-employee-typed Job IDs are retired.** The build once had the office employee type a validated `job_id` while Smartsheet's `AUTO_NUMBER` separately assigned the canonical `JOB-####` (two identifiers per job). Superseded by the **portal-assigned** sequential number (D1 `job_counter`, migration `0022`); the typed Job-ID input and its regexes were removed and the daemon's `get_row` read-back deleted.

## Cross-references

- [Safety Portal mission v5](../safety-portal/mission.md) — the sibling capture surface sharing the same Worker/D1/SPA app and the §34 `photo_screen.py` pipeline.
- [Progress Reporting mission](../progress-reporting/mission.md) — the workstream whose Smartsheet+Box SoR this daemon feeds (the mirror passes above).
- [Foundation Mission v11](../../doctrine/foundation-mission.md) — Invariants 1 (send gate) + 2 (adversarial input, §34 Layer 6).
- [Operational Standards v20](../../doctrine/operational-standards.md) — §50 privileged code-actuation gate, §51 ITS-owned structured-SoR write-back, §31 polling-daemon pattern, §34 attachment screening.
