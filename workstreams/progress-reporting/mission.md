---
type: mission
version: 1
status: draft
last_verified: 2026-06-28
last_verified_against: SolutionSmith-debug/its@9ef3d5b
workstream: progress_reporting
tags: [workstream-mission, progress-reporting, weekly-progress-report, external-send-gate, two-process-send, its-owned-sor, smartsheet-sor, box-sor, weekly-period-sheets, period-split-archive, field-ops-portal, materials-manifest, receive-against-manifest, field-ownership-conflict, parameterize-not-clone, contamination-gate, workstream-tag-guard, sor-write-gate, code-actuation-gate, image-attachment-screening, doctrine-flags]
---

# ITS — Progress Reporting — Mission v1 (draft)

**2026-06-28 — v1 (draft): codifies the just-locked "ITS — Progress Reporting" + P3 Materials program into the planning layer.** This mission is the architecture/decision home for the Progress-Reporting build: the **structural twin of the Safety Portal weekly pipeline** — an **ITS-owned Smartsheet structured system-of-record + Box document system-of-record + a Weekly Progress Report that is human-reviewed and *sent externally* to the job stakeholder** — plus **P3 Materials** (an admin type catalog + a per-job material-list/manifest receive flow). It is authored from the operator-confirmed master plan (`~/.claude/plans/let-s-go-with-option-greedy-fiddle.md`, "ITS — Progress Reporting + P3 Materials, scaling-reconciled"), the execution handoff brief (`~/its/docs/cc-brief_progress-reporting-program_2026-06-28.md`), and the 2026-06-28 execution session (exec `SolutionSmith-debug/its@9ef3d5b`; [memory-archive §G43](../../references/memory-archive.md)). The program was hardened through grill-me + four reviewers + a contamination hunt + a four-fork ultra-plan pass + a reconciliation against the **2026-06-28 forensic scaling eval (20×20)**, with five strategic decisions locked. **Status is `draft`, not `canonical`**, because the load-bearing pipeline (Stage-1 parameterize, Stage-2 progress send/compile, the SoR up-sync, the Material List receive) is a forward plan gated on **unratified doctrine** (the §50/§51 SoR-write decision, Seth-only — §16); only the Tier-A foundation (M1/P-A1/A2 + the field-ops UI fix) has landed. The promotion trigger is stated in the [Authority](#17-authority) section.

This v1 **raises two doctrine questions propose-only** (no `doctrine/*` edit this pass — [§16 Doctrine flags](#16-doctrine-flags-raised-for-seth-co-resolution-propose-only-no-doctrine-edit)): (a) a **SoR-write doctrine candidate** — "ITS as the authoritative writer to an ITS-owned structured Smartsheet system-of-record"; and (b) a **§-numbering collision** — both the SoR-write *and* the already-realized "privileged code-actuation gate" have been informally called **§50** across the references; this pass proposes a numbering for Seth to ratify. It also captures the program **honestly**: where a sub-program still has open product questions (Personnel CRUD's three decisions), they are marked open — not invented.

*Originated this session per the [new-workstream scaffold](../../prompts/scaffold/new-workstream.md), mirroring the [Safety Portal mission](../safety-portal/mission.md) frontmatter + skeleton. Companion: the [2026-06-28 progress-reporting-mission session log](../../session-logs/2026-06-28_progress-reporting-mission.md) and [memory-archive §G43](../../references/memory-archive.md).*

## 1. Purpose

Give the field-ops portal a **weekly external-facing reporting product**: take the daily site activity that field crews already capture in the portal (progress narrative, hours, equipment, materials) and turn it into a **Weekly Progress Report** — auto-compiled from the dailies, human-reviewed in a Smartsheet approval sheet, and **sent to the job stakeholder** after explicit human approval. Alongside it, **P3 Materials** adds a planned-vs-delivered **material list (manifest)** per job: an operator pre-loads what the job ordered, the field marks deliveries against it (or files a flagged off-list delivery), and material incidents reference the list.

This is the **report-and-send half** of the field-ops system. The capture half — the portal UI, the D1 structured store, personnel/equipment/hours/materials entry — is the field-ops portal surface owned by the [URS Marine / field-ops portal data architecture](#2-workstream-placement-and-lineage-decision-a). Progress Reporting layers on top of it the same way [`safety_reports`](../safety-reports/mission.md) layers the weekly-report pipeline on top of the [`safety_portal`](../safety-portal/mission.md) capture surface. The two systems are deliberately parallel: a daily-capture portal feeding a weekly-compile-and-gated-send pipeline, with an ITS-owned Smartsheet + Box system-of-record behind it.

The central engineering discipline is **harden-first, parameterize-once**. A naïve clone of the safety pipeline would double the scaling eval's #1 liability (per-job-per-week Smartsheet proliferation, ~1,040 → 2,080 sheets/yr), re-clone the un-hardened serial compile, re-create the 5,000-row silent-drop failure mode ×N jobs, and omit the operability/enablement docs. So the security-critical modules are **parameterized, not cloned** (the [contamination gate](#contamination-gate-parameterize-safely), an informed [§14](../../doctrine/operational-standards.md) deviation), the sheet model stays **weekly** (matching the weekly report cadence — see §9 Decision 2; monthly was reverted 2026-06-29), and the full Tier-A foundation is **front-loaded** before any slice that creates a sheet, compiles, or adds a daemon.

## 2. Workstream placement and lineage (Decision A)

**Decision A — resolved: Progress Reporting is a NEW sibling workstream (`workstreams/progress-reporting/`, tag `progress_reporting`), not a v2 extension of `urs-marine-portal`.** It **depends on** the field-ops/portal capture surface and **reuses** the `safety_reports` pipeline machinery; it does not own either.

The justification, grounded against what the neighbouring missions already claim:

- **The capture surface is already owned elsewhere.** The field-ops portal (Worker + D1 + React SPA, three-tier capability-gated RBAC, the `personnel`/`equipment`/`hours`/`materials` tables, D1-as-system-of-record) is the architecture carried by the [URS Marine portal mission](../urs-marine-portal/mission.md) (§2–§4: three-tier RBAC, D1-as-SoR, the integrity bar). The Evergreen field-ops portal realized in the execution repo (`migrations/0013` capabilities, `0014_urs_core_tables.sql`, the `fieldops_*` Worker modules) **is that data architecture instantiated for Customer 0**. Progress Reporting is **not a capture surface** — it adds no portal-entry tables of its own; it consumes what the field-ops portal captures. Folding it into `urs-marine-portal` would conflate "the portal that captures field data" with "the pipeline that reports on it."
- **The established precedent is exactly this split.** [`safety_portal`](../safety-portal/mission.md) (capture: auth, forms, signatures, the send-free D1 queue) and [`safety_reports`](../safety-reports/mission.md) (pipeline: intake → compile → gated weekly send, the ITS-owned Smartsheet/Box SoR) are **sibling workstreams sharing one pipeline**. Progress Reporting is the `safety_reports`-shaped sibling to the field-ops portal's `safety_portal`-shaped capture. Same shape, new workstream.
- **It introduces an invariant surface the portal mission explicitly scopes out.** The URS Marine mission §9 states *"No customer-facing email send obligation in scope — the External Send Gate manifests as the outbound-adapter gate, not an email path."* Progress Reporting **introduces ITS's customer-facing external send** for the field-ops side: the Weekly Progress Report transmitted to the job stakeholder via the two-process gate. A workstream whose mission scopes out external send is the wrong home for the workstream that adds it; the new send pipeline deserves its own [External Send Gate](#8-foundation-invariants-inherited) restatement and its own approval surface (`WPR_human_review`).
- **Naming follows the Customer-0 generic pattern.** `safety_reports` / `safety_portal` are generic Customer-0 (Evergreen) workstream names; `urs_marine_portal` is Customer-2-specific. The Progress-Reporting program executes in the Evergreen `~/its` tree, reusing `safety_reports` modules — so the generic `progress_reporting` tag (sibling to `safety_*`) is the correct register, not a customer-keyed one.

**Lineage / drift note.** The field-ops portal and `urs_marine_portal` share the *portal-template* data architecture, not the same execution repo: the field-ops surface is realized in Evergreen `~/its` (with URS-derived core tables), while `urs_marine_portal` is a separate Customer-2 fork. This mission therefore references the field-ops capture surface as a **dependency** and treats `urs_marine_portal` as its **data-architecture ancestor**, not its parent workstream. If the execution layer later unifies or re-forks these, flag it here (the planning layer wins on doctrine; the code wins on as-built — reconcile).

Adding `progress_reporting` as a canonical workstream tag is a [`CONVENTIONS.md`](../../CONVENTIONS.md) + `scripts/lint_frontmatter.py` enum edit (done this session, called out in the [session log](../../session-logs/2026-06-28_progress-reporting-mission.md); it also corrected a pre-existing drift where `urs_marine_portal` was in the lint enum but missing from `CONVENTIONS.md`).

## 3. Audience

- **Field crews / submitters (portal users).** Field-side roles who submit the daily progress narrative + hours + equipment + materials deliveries, and (optionally) a PM-authored weekly summary. They never see Smartsheet, Box, or any ITS operator surface — they capture in the portal only.
- **Approvers + operator-maintainer.** Review, edit, and approve the compiled **Weekly Progress Report** in `WPR_human_review` — the Progress-Reporting `<Workstream>_Pending_Review` surface. Approval authority is the new workspace's membership (the [§46 workspace-membership-=-approval](../../doctrine/operational-standards.md) F22 mechanism), so the approver re-share into `ITS — Progress Reporting` is a load-bearing activation gate (P5 pre-req).
- **Office PMs (administration).** Maintain `ITS_Active_Jobs`, including the new `Progress Reports Contact Name/Email` columns that route the weekly send.
- **The job stakeholder (external recipient).** The customer-facing recipient of the approved Weekly Progress Report — the first external-send audience the field-ops system acquires. Routing: the `Progress Reports Contact` column with a `stakeholder_email` fallback.
- **Admins (in-browser).** Manage the `material_catalog` (the 36-type vocabulary, M1) and — pending the open Personnel-CRUD decisions (§13) — personnel. The materials catalog and personnel surfaces are gated by per-capability flags (`cap.materials.manage` / `cap.personnel.manage`), not a role string.

## 4. Inputs

- **Daily progress submissions** — per-job daily entries (narrative + hours + equipment status + materials deliveries) captured in the field-ops portal, HMAC-signed and queued in the send-free Worker's D1 store, drained by the Mac-side `portal_poll`.
- **Optional PM-authored weekly summary** — a `weekly-progress-summary` progress-category form the PM may submit; the weekly compile includes it when present. The weekly report is **auto-compiled dailies + an *optional* weekly-summary** — the summary is not required for a report to compile.
- **Operator-filled Material List (manifest)** — the per-job planned-materials list (ITS-owned, manually filled now): each line prefers a `material_catalog` type but allows free text, with ordered qty + unit cost + value. This is the upstream of the bidirectional Material List sync (§12).
- **`material_catalog`** — the admin-editable 36-type materials vocabulary (+ optional reference unit cost, soft-retire), migration 0019, **landed** (M1).
- **`ITS_Active_Jobs`** — the office-PM-maintained job list, extended with `Progress Reports Contact Name/Email`. Only Active jobs run and appear.
- **Incident photos** — field-captured images attached to a material incident; untrusted input, screened on a **fenced + work-budgeted** `portal_poll` pass before any Box upload (§8 Invariant 2).
- **Smartsheet plan capacity** — the operator-confirmed per-plan sheet cap (Pro $600 vs Business $2,400 tier) feeding `smartsheet.sheet_count_ceiling`, the runtime margin-check ceiling for find-or-create.

## 5. Outputs

- **Weekly Progress Report (the customer-facing artifact)** — a Box packet + a `WPR_human_review` approval row per (job, week), compiled by `progress_weekly_generate` (instantiating the hardened shared compile core), human-approved, and transmitted to the stakeholder by `progress_send` (the only customer-facing sender; no AI step; in `SEND_SCRIPTS`).
- **ITS-owned structured Smartsheet system-of-record** — per-job, **weekly (Sat→Fri)**, **period-split + archive-on-closure** sheets in the `ITS — Progress Reporting` workspace: progress week-sheets, `Materials Status & Location`, `Equipment Status & Location`, `Hours Log`, `Material List`, `Material Incidents`. Plus the single cross-job `WPR_human_review`. **ITS owns and creates this workspace** (CC via Smartsheet MCP + Mac build scripts) — it is not the canonical Evergreen Smartsheet.
- **Box document system-of-record** — per-job daily + weekly PDFs; incident photos filed to `ITS Photos/<uuid>/` after screening. Box parallels the Smartsheet job hierarchy.
- **D1 read-aggregate (the rollup query surface)** — `GET /api/internal/progress-rollup` (send-free, bearer-gated, event-date-windowed, amend-chain-collapsed) renders Labor / Equipment / Progress% (+Δ, open tasks) now, with Materials wiring in at M2. Costs are computed but **gated OFF** by a config flip (internal-only until the operator flips the customer-report + portal cost switches on).
- **(Downstream of the capture portal, listed for completeness)** — the D1 `material_list` deliveries marked by the field, up-synced (delivery columns only) to the ITS-owned `Material List`; hours/equipment one-way up-synced to the period-split per-job sheets.

## 6. Success criteria

- **A Weekly Progress Report is compiled from the dailies, human-approved, and sent to the stakeholder** end-to-end on the mirror — submit → compile → `WPR_human_review` → approve → `progress_send` to a test mailbox — with the External Send Gate intact (the sender is AI-free, two-process, recipients resolved at send time).
- **Zero external send caused by an AI-process compromise.** Structural: the Worker is send-free; `progress_weekly_generate` (and the up-sync daemon) are send-free + AI-free and capability-gated; the only sender reads an approved, human-edited `WPR_human_review` row.
- **Sheet growth stays inside the plan cap.** Sheets are **weekly** (the report cadence); the proliferation guard is the layered defense, not a coarser period — every per-job find-or-create passes the A1 margin-check (routes to Review Queue on a would-breach, never silently past the cap), per-job logs are period-split + archived-on-closure (never `delete_rows`), and a **monthly config-flip is the documented fallback** if the margin-check ever fires (§9 Decision 2).
- **The safety pipeline is unharmed by the parameterization.** Across every Track-P slice, the live safety regression smoke is green — safety still sends with the new `Workstream` column present, and the safety packet output is byte-unchanged (safety stays weekly; there is no period migration).
- **The Material List receive does not clobber a pending delivery.** The bidirectional sync down-upserts operator content-only and up-syncs delivery-only — proven by the live "sync does NOT clobber a pending delivery" smoke.
- **Every shipped slice carries its enablement doc.** §6/A8 DoD: a §43 successor-remediation skeleton + a §6a-manifest registration land same-PR for any slice shipping a sheet/column/daemon/portal-surface; the polished distributable PDF lands before the 20-job cutover.

## 7. Out of scope

- **No canonical-Evergreen Smartsheet integration (deferred).** ITS owns the Progress-Reporting Smartsheet SoR; mapping to / writing the customer-owned canonical Evergreen Smartsheet, and the **PJOB→JOB key reconciliation** it requires, are deferred discovery tasks — not build tasks (the scaling eval's #4 liability; same don't-build-against-an-unseen-SoR blocker class as the parked P2.4 decision).
- **No new daemon for incident-photo screening.** Photos ride a **fenced + work-budgeted** screening pass on the existing `portal_poll` (no separate daemon), reusing the safety `photo_screen.py` §34 pipeline.
- **No customer-visible costs at launch.** Cost computation exists but is gated **OFF** behind config switches (off-customer-report + off-portal), default OFF; the operator flips them on later.
- **No automatic addendum after a sent weekly report.** A sent Weekly Progress Report is frozen at send time; late dailies route to the next uncompiled period + a Review-Queue flag; the operator decides on any addendum (manual).
- **No Personnel CRUD yet (design-only).** The personnel two-headed-roster surface is mapped but unbuilt, and three product decisions are open (§13). Out of scope until the operator confirms them.
- **No write-back to a customer-owned/canonical system-of-record.** The SoR-write doctrine candidate (§16) covers writing to the **ITS-owned** Smartsheet only; authoritative writes to a customer-owned SoR are a separate, higher decision, explicitly not in scope.

## 8. Foundation Invariants Inherited

Per [Foundation Mission v11](../../doctrine/foundation-mission.md). Progress Reporting touches **both** external-bound send (the weekly report) **and** external-content ingestion (incident photos + every field-entered narrative), so it restates **both** invariants verbatim from doctrine, then states the progress-reporting-specific application. The canonical statements below are quoted from doctrine; the doctrine wins on any conflict.

### Invariant 1 — External Send Gate

Canonical statement ([Foundation Mission §Invariant 1](../../doctrine/foundation-mission.md#invariant-1-external-send-gate-unchanged-from-v7)):

> No external transmission without explicit human approval. Permanent, not time-bounded. Earlier framing in Op Stds v4 that described review as a 30-60 day window is superseded.
>
> - Every workstream that produces customer-facing output uses a `<Workstream>_Pending_Review` Smartsheet with Approved for Send / Approved By / Approved At / Sent At / Send Status columns.
> - Two-process model. Generation scripts (which call the Anthropic API) have zero send capability. Send scripts (which transmit) have zero AI step.
> - Successful prompt injection at the AI layer cannot cause external transmission, because the AI is in a different process from the transmitter.
> - Enforced at the code level by `tests/test_capability_gating.py` — every generation script and every send script is registered to the appropriate list there.

**Progress-Reporting application.** This workstream **acquires the field-ops system's first customer-facing external send** — the Weekly Progress Report to the job stakeholder — and inherits the two-process gate by construction:

- **`<Workstream>_Pending_Review` = `WPR_human_review`** — one cross-job sheet, one row per (job, week), with the editable email body as the source of truth for the send and the standard Approved-for-Send / Approved By / Approved At / Sent At / Send Status columns. It is the **only** cross-job sheet in the workspace.
- **Two-process, AI-free send.** `progress_send` is the only customer-facing sender (in `SEND_SCRIPTS`, `anthropic` AST-forbidden); the generation/compile path (`progress_weekly_generate`) and the D1→Smartsheet **up-sync daemon** are send-free + AI-free (GATED-enrolled, in `tests/test_capability_gating.py`), with `WALKED_ROOTS` extended per package (`+= progress_reports` in P2; `+ field_ops` when the sync gains I/O).
- **The Worker stays structurally send-free.** The Cloudflare Worker has no Graph/email path (CI grep forbids `fetch(` in `safety_portal/worker/` except ASSETS); progress submissions are stored in D1 and **pulled** by the Mac-side `portal_poll` — the portal never pushes anything outward.
- **The up-sync is itself a "send" to a structured SoR.** Writing D1 data up to the ITS-owned Smartsheet is gated by the same two-process discipline and an allowlisted egress method (`shared/portal_client.py`); the up-sync daemon forbids `send_mail`/`anthropic` via `GATED_SCRIPTS`. The doctrine status of "ITS as the authoritative writer to this SoR" is raised propose-only (§16).

### Invariant 2 — Adversarial Input Handling

Canonical statement ([Foundation Mission §Invariant 2](../../doctrine/foundation-mission.md#invariant-2-adversarial-input-handling-revised-in-v8)):

> All content originating outside the operating customer tenant is untrusted data. Six-layer defense (v8 expanded from v7's five). The invariant itself is unchanged from v7; Layers 1 and 6 are revised/added (v8), and Layer 5 is recharacterized as a detection tripwire, not a defense layer (v9, see below).

Progress-Reporting application of the relevant layers (every field-entered narrative, every materials line, every incident photo is untrusted data):

- **Layer 1 (Authentication boundary + transport integrity).** Field crews authenticate to the portal; on the transport side, the bearer token gating `/api/internal/*` and the per-submission HMAC the Mac-side poller verifies are the Layer-1 controls — there is no inbound mailbox.
- **Layers 2–4 (tagging / capability gating / structured output).** Any field-entered text that reaches a model call (the rollup narrative / any interpolation in the rendered report) is wrapped in `<untrusted_content>` (`shared/untrusted_content.py`) and rendered as **plain text** — never executed, never used as a logic/auth input. Submissions conform to per-form definitions; the Python side re-validates before any write. The compile/up-sync daemons have no send and no Anthropic capability.
- **Layer 5 (Anomaly logging — tripwire).** Suspicious patterns route the submission to the Review Queue for human attention; never relied on for prevention.
- **Layer 6 (Attachment screening) — incident photos, image-constrained.** Incident photos run the [Operational Standards §34](../../doctrine/operational-standards.md) image-class screen exactly as realized for the Safety Portal: a **fenced, work-budgeted** pass on `portal_poll` invoking `safety_reports/photo_screen.py` — magic-byte check → Pillow `verify()` + decompression-bomb cap + a **forced metadata-destroying re-encode** → ClamAV-on-raw-bytes (config-gated, default OFF). A non-clean photo **refuses the whole submission before filing**: MALICIOUS → a CRITICAL page naming the offending account + a security-flagged Review-Queue row; the clean re-encoded original files to Box and the renderer consumes **only** screened bytes. Delivery write-back is bounded.

## 9. Locked strategic decisions

Five decisions are **locked** for the current phase; the authoritative record is the master plan's "Strategic decisions" list. Four of the five — all but the same-PR doc skeleton + PDF-before-cutover DoD (#4 below, also carried in §6/§7 and the §6/A8 DoD) — are distilled in [memory-archive §G43.2](../../references/memory-archive.md). **Do not re-litigate.**

| # | Decision | Resolution |
|---|----------|-----------|
| 1 | **Co-design with the full Tier-A foundation front-loaded** | Harden-first, parameterize-once. Every progress slice that **creates a sheet, compiles, or adds a daemon** is gated behind the minimum Tier-A gate: A1-decision + A2 + A3 + A6 + compile-core extraction, with A4 before progress raises submission volume. A1 runs parallel to P0 (~0 schedule cost). **M1 (material_catalog, D1-local) stays parallel-now** — zero scaling coupling. |
| 2 | **Weekly per-job sheets — both safety AND progress** *(2026-06-29: reverted from the 2026-06-28 "monthly" decision)* | Both reports ship on a **weekly (Sat→Fri) cadence**, so the sheet period **matches the report cadence**: one sheet per (job, Sat-week), keyed on the opening Saturday (`shared/safety_week.py`), self-delineating — the compile reads exactly one week sheet, with **no month-boundary straddle and no intra-sheet week-mixing**. Monthly would split a boundary week across two month sheets and force a date-windowed cross-sheet compile — a bad trade for a weekly deliverable. **No `sheet_period` abstraction is carried:** P1a parameterizes `week_sheet` to `(workspace_id, key_builder)` only; weekly is hardcoded. Monthly stays a documented **config-flip fallback** if proliferation ever threatens the cap, and the `shared/sheet_capacity` margin-check (P-A1, #326) is the armed tripwire (Review-Queue WARN, never silent) — now **more** relevant since weekly uses ~4–5× more headroom. **Live finding (P-A1, #326):** `SAFETY_PORTAL` = 7 sheets (ample). `verify_sheet_cap` + operator confirm the $600-vs-$2,400 tier. *Why reverted: monthly optimized sheet count at the cost of breaking the 1:1 sheet=week property for a weekly report; it was decision-only, never built (live safety was always weekly), so the revert drops only P1a's weekly→monthly migration sub-step.* |
| 3 | **ITS-owned Smartsheet + Box as SoR; canonical-Evergreen integration deferred** | ITS creates and owns the `ITS — Progress Reporting` workspace + sheets (CC via MCP + Mac build scripts). The D1→Smartsheet up-sync writes to ITS-owned sheets only. **Canonical-Evergreen Smartsheet integration and the PJOB→JOB reconciliation are deferred** (the schema is unseen — same blocker class as the parked P2.4 decision). |
| 4 | **Same-PR doc skeleton + PDF-before-cutover** | §6/A8 enablement docs are a definition-of-done obligation on every Stage-2 slice: a §43 successor-remediation skeleton + §6a-manifest registration land **same-PR**; the polished distributable PDF lands **before** the 20-job cutover. Not deferred to a follow-up pass. |
| 5 | **Parameterize (not clone) the security-critical modules** | An informed [§14](../../doctrine/operational-standards.md) deviation: the send/compile/`week_sheet` modules take **required (no-default) config objects** (missing config = immediate failure at import/construction, never a silent safety default), guarded by a **Workstream-tag row guard**. `ops-stds-enforcer` reviews each diff; §42 comments; **never merge→pull into `~/its` until the live safety smoke is green** on the new config path. `shared/heartbeat.py` is extracted first. |

## 10. Topology (job = parent folder; weekly period sheets)

```
ITS — Progress Reporting (workspace)
├── [Control folder]  └── WPR_human_review   ← ONLY cross-job sheet (1 row/job·week; carries a Workstream tag col)
└── <Job> folder   (RUNTIME find-or-create; A1 margin-checked)
      ├── Materials/  ├── Material List  (manifest: catalog-or-free-text, qty, unit cost, value, qty delivered, status, unplanned flag)
      │               ├── Materials Status & Location (period-split + archive-on-closure)
      │               └── Material Incidents (low-vol single sheet + Check-O monitor; value from the list)
      ├── Equipment/  └── Equipment Status & Location (period-split + archive-on-closure)
      ├── Hours/      └── Hours Log (period-split + archive-on-closure)
      └── Progress Reports/  └── "<Job> — week of <Saturday>" WEEK sheets (daily [+ optional weekly-summary] rows → WPR_human_review)
```

- **Job = parent folder.** Per-job period sheets and folders are **runtime find-or-create**, gated on the A1 margin-check — never silently past the cap. The workspace + control folder + `WPR_human_review` are CC-built (workspace via MCP; the cross-job sheet + control folder via `build_*.py` + ID-flip).
- **`WPR_human_review` is the only cross-job sheet** (one row per job·week; carries a `Workstream` tag column).
- **Per-job full-history logs are period-split + archived-on-closure** (to `WORKSPACE_ARCHIVE`), **never `delete_rows`** — the safety A5 delete-rotation is invalid for a system-of-record. All enrolled in an A5 row-cap watchdog (Check O).
- **Box parallels per job** (daily + weekly PDFs; incident photos → `ITS Photos/<uuid>/`).
- **The cross-job D1 read-aggregate (P6) is the reporting query surface**, so period-splitting the underlying sheets does **not** fragment reporting. Materials/Equipment/Hours roll up into the **weekly** report (the daily is the PM's manual narrative).

## 11. Data flows (Worker = D1-only + send-free)

The Worker is D1-only and send-free; the Mac daemons own all Smartsheet/Box I/O.

- **Progress:** daily [+ optional weekly-summary] → `/api/submit` → D1 → `portal_poll` → `intake` → PDF → Box + progress **week**-sheet → staggered Friday/Sat `progress_weekly_generate` (the **hardened shared compile core**) → Box packet + Rollup + `WPR_human_review` row → human approves → `progress_send` → stakeholder.
- **Material List (bidirectional — the field-ownership conflict model):** operator fills the list → Mac sync **down-upserts ONLY operator-owned content columns by line key into D1 `material_list`, NEVER delivery columns** → portal shows outstanding/undelivered → field marks delivered or files a flagged unplanned delivery (D1 write route) → Mac sync **up-writes ONLY delivery columns** back + appends unplanned lines. This is **not** the `POST /api/internal/sync` full-replace (that route is the Active-Jobs job-list push; using it for the Material List would clobber field deliveries).
- **Hours/Equipment (one-way up):** D1 → period-split per-job sheets (equipment job-linkage via `equipment_location`).
- **Rollup:** send-free read-aggregate, **event-date windowed** (`work_started_at` / `performed_at` / `received_at`, `created_at` fallback), **amend-chain-collapsed** (`NOT EXISTS`).

### Contamination gate (parameterize safely)

The SDK layer is safe by construction (explicit ids per call). Risk collapses onto the required-config bindings — **no field defaults to a safety value**:

| Binding | Guard |
|---|---|
| `week_sheet` workspace pin | **required `(workspace_id, key_builder)`** (no `sheet_period` — weekly is hardcoded; see §9 Decision 2); 3 live call sites updated; **safety binds its current weekly period byte-identically in P1a** (no period migration). |
| `weekly_send` recipient/sheet/subject/cols | per-script **`SendConfig`** baked as a module constant. |
| `weekly_send_poll` singletons (lock, heartbeat key, watchdog slug, config keys, F22 workspace, poll sheet, send_fn) | required **`DaemonConfig`** (core + a thin per-workstream entry). |
| **Workstream-tag guard** | add a `Workstream` column to **WSR (backfill `safety`) AND WPR**; `send_one_row` **HARD-HELDs (+CRITICAL)** on a present mismatch, match-with-WARN on absent (back-compat). P1b safety smoke proves safety still sends with the column. |
| **Cross-JOB guard** | the sync resolves each per-job `sheet_id` by validated find-or-create, never a default; per-slice cross-job assertion (job A's deliveries never reach job B's sheet). |
| **Same-PR enrollments** | WPR-specific picklist REGISTRY entry (**SENDING-inclusive**; clone `_WSR_`, not the decommissioned `_WPR_`); GATED/SEND enrollment; `WALKED_ROOTS += progress_reports` in P2, `+ field_ops` when the sync gains I/O. |

## 12. The P3 Materials manifest model

Materials are **received against a manifest**, not free-logged:

- **`material_catalog` (M1, landed).** An admin-editable 36-type vocabulary (+ optional reference unit cost, soft-retire); Worker write/read gated `cap.materials.manage` / `cap.materials.receive`; `MaterialsCatalogPage.tsx`. D1-local, zero scaling coupling — built parallel to the Tier-A foundation.
- **Per-job Material List (manifest, M2 — gated on P7 + §50/§51).** An ITS-owned per-job list (manually filled now): each line **prefers a catalog type but allows free text**, with ordered qty + unit cost + value. D1 shape: `material_list(job_id, line_uuid, smartsheet_row_id, catalog_id?, description, qty_ordered, unit_cost, value, qty_delivered, delivered_status, delivered_by, delivered_at, unplanned, synced_at)`.
- **The field-ownership conflict model.** The bidirectional sync splits column ownership: the **operator owns content columns** (catalog/description/qty/cost — down-upserted to D1 by line key, never touching delivery state); the **field owns delivery columns** (marked in the portal, up-synced to Smartsheet, never overwritten by a down-upsert). Value comes from the list line. **Flagged unplanned off-list deliveries are allowed** (a D1 write route appends an unplanned line; the up-sync appends it to Smartsheet).
- **Material Incidents (M3 — after M2).** An integrity-bar incident referencing a Material List line; **value computed from the list**; the Worker write reuses the L1 photo gate; a **fenced + work-budgeted** `portal_poll` deep-screen pass cleans the photo to Box (MALICIOUS → CRITICAL + Review-Queue, refused). Low-volume single sheet + a Check-O row-cap monitor.

## 13. Phase status (as-built) and the Stage 0/1/2 + Track M sequence

The program is sequenced **Tier-A foundation → parameterize/compile re-core → build progress + materials**. As-built status (exec `SolutionSmith-debug/its@9ef3d5b`):

| Slice | Scope | Status |
|---|---|---|
| **M1** | admin-editable `material_catalog` (migration 0019 + Worker CRUD + admin SPA); 36-type vocab + soft-retire; caps reuse 0013 | **Landed — four-part verified** (PR #325, `ef568c2`) |
| **P-A1** | `scripts/verify_sheet_cap.py` + `shared/sheet_capacity.py` margin-check (the armed cap tripwire); live finding 7 sheets; **weekly retained** (monthly reverted 2026-06-29 — §9 Decision 2) | **Landed — four-part verified** (PR #326, `b6ba870`) |
| **A2** | single-host resilience: SDK timeouts on `box_client`/`smartsheet_client`/`keychain`, `KeychainLockedError`, `RunAtLoad=true` on 8 interval plists (hardened, not cloned from `template.plist`) | **Landed — four-part verified** (PR #327, `3b285f5`). Box live smoke deferred to A3; **operator follow-up:** reload plists via `scripts/launchd/install.sh` |
| **Field-ops UI fix** | shared `PageShell` + restyle Job/Equipment/Personnel/Materials | **Landed — four-part verified** (PR #328, `9ef3d5b`); confirmed live after hard-refresh |
| **Stage 0 (remaining)** | A3 (Box OAuth cross-process refresh-lock + keychain write-lock + 50-day idle marker), A4 (unfiled-queue backlog alert + `portal_poll` outage escalation), A6 (`weekly_generate` hardening → extract `safety_reports/compile_core.py`), P0 (extract `shared/heartbeat.py`) | **Open** (live-safety; serialize against daemon cycles) |
| **Stage 1** | P1a (`week_sheet` → required `(workspace_id, key_builder)`; safety binds weekly byte-identically, **no period migration**), P1b (`weekly_send` → `SendConfig` + Workstream column), P1c (`weekly_send_poll` → `DaemonConfig`), P4-core (progress compile instantiates `compile_core`, staggered + host mutex) | **Open** |
| **Stage 2** | P2 (CC-built workspace + control folder + `WPR_human_review` + `WALKED_ROOTS += progress_reports` + SENDING-inclusive picklist REGISTRY entry + Progress-Reports-Contact columns + §6a manifest; **P5 pre-req: re-share every safety approver into the new workspace**), P3 (category routing, flag OFF until P4+P5; golden mixed-week test), P4 (progress compile, PDFs-only), P5 (`progress_send` + `progress_send_poll` + operability guards built once over **both** review sheets: `shared/recipient_health.py`, HELD-row scan, approver-drift watchdog — **sendable report works here**), P6 (rollup numbers), P7 (period-split structured sheets + the D1→Smartsheet up-sync — **§50/§51-gated**) | **Open** |
| **Track M** | M2 (per-job Material List + bidirectional receive — after P7 + §50/§51), M3 (Material Incidents + fenced photo pass — after M2) | **Open** |
| **Optional** | the `weekly-progress-summary` form; UI follow-ups (route form pages through PageShell; tracker action messages → `.banner`; a `--danger` button variant) | **Open** |

**Personnel CRUD (task #22) — design-only; three product decisions OPEN.** The `personnel`/`users` two-headed-roster surface is fully mapped (a nullable `username`, NO FK, soft-linked by string; `cap.personnel.read`/`manage`, admin-only). Build is pending **operator confirmation** of three decisions — recorded here as **open**, not invented:
1. **Where account creation lives** — keep account (`/api/admin/users`) and roster creation separate and link by username (Explore-agent rec: Option A), vs an inline "also create account" toggle on the personnel form.
2. **Dangling username on create** — validate that `users.username` exists (422 `unknown_account`; rec), vs allow a soft dangling reference.
3. **Default role for an account-personnel** — `submitter`/field-PM (rec); `admin` must be explicit.

## 14. Integration with safety_reports and the field-ops / urs-marine-portal surface

- **Reuses the `safety_reports` pipeline machinery.** The hardened compile core (`safety_reports/compile_core.py`, extracted in A6), the parameterized `week_sheet`/`weekly_send`/`weekly_send_poll`, `shared/heartbeat.py`, `shared/recipient_health.py`, the §34 `photo_screen.py`, and `form_pdf` are **shared, parameterized**, not cloned. The contamination gate (§11) is what makes that reuse safe: required config + the Workstream-tag guard keep safety and progress from cross-wiring. This mirrors how [`safety_portal`](../safety-portal/mission.md) and [`safety_reports`](../safety-reports/mission.md) are sibling workstreams sharing one pipeline.
- **Depends on the field-ops capture surface.** The daily progress/hours/equipment/materials data, the `material_catalog`, the D1 `material_list`, and the Worker write routes are the field-ops portal's — the [URS Marine portal data architecture](../urs-marine-portal/mission.md) (D1-as-SoR, three-tier capability-gated RBAC, the integrity bar) instantiated for Customer 0. Progress Reporting **consumes** that capture; it adds no capture tables of its own.
- **The split is deliberate.** Capture (field-ops portal) and report-pipeline (Progress Reporting) are separate workstreams so the new **external-send** surface (the Weekly Progress Report) gets its own gate restatement, its own `WPR_human_review` approval sheet, and its own contamination boundary from safety — without bloating the portal mission that explicitly scopes external send out (§2).

## 15. Risks

| Risk | Mitigation |
|---|---|
| **Per-job-per-period Smartsheet proliferation** (scaling eval #1 liability) | Weekly sheets (report-cadence-matched); the proliferation guard is the layered defense — per-job find-or-create passes the A1 margin-check (Review Queue on would-breach, never silent), period-split + archive-on-closure (never `delete_rows`), A5 Check-O row-cap watchdog per job; a **monthly config-flip is the documented fallback** if the margin-check fires (§9 Decision 2). |
| **Cross-workstream contamination** (a progress send reaching a safety recipient, or vice versa) | The contamination gate (§11): required no-default config objects; the Workstream-tag row guard (HARD-HELD + CRITICAL on mismatch); per-slice cross-job + cross-wiring assertions; a live **safety regression smoke on every Track-P slice** (safety still sends with the column; safety packet byte-unchanged — safety stays weekly, no period migration). |
| **The bidirectional Material List clobbers a pending field delivery** | The field-ownership conflict model: down-upsert content-columns-only, up-sync delivery-columns-only; never the `/api/internal/sync` full-replace; a live "sync does NOT clobber a pending delivery" smoke is a DoD. |
| **Un-hardened serial compile re-cloned** (scaling eval A6 CRITICALs; the 5,000-row silent-drop ×N jobs) | A6 hardens `weekly_generate` (per-job SIGALRM timeout, total-bytes memory guard, Rollup-watermark resumable skip, RunSummary counters) **then extracts the core**; the progress compile **instantiates** the hardened core (does not re-clone the loop); commit-point ordering writes the watermark last; staggered off safety's Friday + a host-level compile mutex. |
| **Single-host fragility under ~4 new daemons** (meta-002) | A2 hardened plists (`RunAtLoad`+`KeepAlive`, SDK timeouts, Keychain-locked handling); A3 Box OAuth refresh-lock + write-lock; all I/O through the A2-hardened shared clients (grep/assert no raw SDK); §43 host-down/stalled-call/token-stale runbook per slice. **Operator follow-up (meta-002):** define a Tier-3 backup / escalation SLA before the 20-job cutover. |
| **Malicious incident photo** | The §34 image-class screen on a fenced + work-budgeted `portal_poll` pass (`photo_screen.py`); MALICIOUS → CRITICAL naming the account + refused before filing; the renderer consumes only screened bytes; ClamAV config-gated default OFF. |
| **Mocks-pass-but-live-API-fails** (bitten ≥3×) | Mandatory live smoke for every live-safety slice + operator sign-off before merge: naive-Pacific datetime, 50-char sheet-name cap, picklist REGISTRY for every new Send Status value, F22 vs the shared workspace + approver re-share verified before the P5 send smoke, find-or-create + the A1 margin-check, Box refresh-race (≥2 daemons within 60s), per-job compile timeout + mid-crash resumability + memory guard. |
| **Building against an unseen canonical SoR** | ITS owns the Progress-Reporting Smartsheet SoR; canonical-Evergreen integration + PJOB→JOB are deferred (out of scope, §7) — no build against a schema not yet seen. |
| **Doctrine gate on the critical path** (P7 + M2/M3 write-back are §50/§51-gated, Seth-only) | Initiate the SoR-write doctrine bump **early, in parallel** to Stage 0/1 (§16), so it is not the critical-path blocker; the numbering collision is surfaced propose-only this pass. |

## 16. Doctrine flags raised (for Seth co-resolution; propose-only, no `doctrine/*` edit)

> **RESOLVED 2026-06-29 — ratified in Op Stds v19.** Both flags below were ratified by the Developer-Operator on 2026-06-29 as **Op Stds v19 §50** (privileged code-actuation gate) and **§51** (ITS-owned structured-SoR write-back — extended at ratification to explicitly name the **job-tracker → Active-Jobs write** as a covered instance). Decision B (the numbering collision) is resolved: **§50 = code-actuation** (raised first), **§51 = SoR-write**. P7 + M2/M3 and the job-tracker pivot (P2.5) are now **doctrine-unblocked** (the build remains gated on the seam + the progress workspace existing, not on doctrine). The propose-only text below is retained as the originating record.

_Original flags (propose-only at the time; retained for the record):_

The Progress-Reporting program surfaces **high-capability-class (doctrine)** questions. Per the [Capability-Gating Through-Line](../../doctrine/foundation-mission.md), doctrine changes are Developer-Operator-only — so they are raised here as **flags only**, exactly as the [Safety Portal mission v5](../safety-portal/mission.md#doctrine-flags-raised-v5-for-seth-co-resolution-propose-only-no-doctrine-edit-this-pass) raised its drafts. No `doctrine/*` file is edited and no doctrine `version:` is bumped this pass.

### (a) SoR-write doctrine candidate — "ITS as the authoritative writer to an ITS-owned structured Smartsheet system-of-record"

The progress program makes ITS **write data up** to a structured Smartsheet system-of-record it owns — the D1→Smartsheet up-sync (hours/equipment one-way; the bidirectional Material List content-vs-delivery) and the period-split per-job structured sheets (P7 + M2/M3). This is a posture ITS has not previously codified (the existing pattern is read-from / human-approved-write-to a review sheet, not authoritative structured-data write-back). Candidate doctrine text for Seth's consideration:

> **ITS-owned structured-SoR write-back.** ITS may be the authoritative writer to a **Smartsheet system-of-record it owns** (created and controlled by ITS, e.g. the `ITS — Progress Reporting` workspace), distinct from the read-only / human-approved-send posture toward a customer-owned Smartsheet. The D1 store is upstream; the ITS-owned Smartsheet is a downstream structured mirror that ITS writes — **one-way up** for accumulating logs (hours, equipment), and **bidirectional with split column ownership** for the Material List (the operator owns content columns; the field owns delivery columns; neither side's write overwrites the other's). Guards, all required: the up-sync daemon is **send-free + AI-free** (GATED; `send_mail`/`anthropic` forbidden), in `WALKED_ROOTS`, with egress through an **allowlisted `shared/portal_client.py` method** (no raw SDK); per-job sheets resolved by **validated find-or-create with the A1 margin-check** (never a default, never silently past the cap); logs **period-split + archived-on-closure, never `delete_rows`**, under an A5 row-cap watchdog; A2 SDK timeouts + the A3 Box/Keychain lock inherited. **Boundary:** this covers an **ITS-owned** SoR only — authoritative write-back to a **customer-owned / canonical** system-of-record (and the PJOB→JOB key reconciliation it requires) is a **separate, higher decision, explicitly out of scope** here.

### (b) §-numbering collision — surface, then propose (Decision B)

**The collision is live in the references.** Two *different* concerns have both been informally called **§50** of Operational Standards:

1. **The privileged code-actuation gate** — generalize Invariant 1's two-process model to *code* changes (cloud can only queue; the local Mac daemon is the sole actuator; state-machine-stamped; CI-gated synchronous merge; the operator toolchain holds the credentials). **Already realized in code** by the form-publish pipeline (`publish_daemon.py`), and **raised first** (Safety Portal mission v4, 2026-06-10; [info-gap §3/§8](../../references/claude-code-info-gap.md); memory-archive §G35). Carried (un-ratified) at Safety Portal mission v5.
2. **The SoR-write** above — "D1-as-writer to an ITS-owned Smartsheet SoR" — raised 2026-06-28 (the execution handoff brief + [info-gap](../../references/claude-code-info-gap.md), which calls it "§50 (v18→v19)"); gates P7 + M2 + M3.

Neither is ratified — Operational Standards v18 currently ends at **§49**; §50 is genuinely the next free number, and both candidates point at it. **Recommendation (propose-only — Seth ratifies):**

- **§50 = the privileged code-actuation gate** (raised first; already realized in code).
- **§51 = the ITS-owned structured-SoR write-back** (the candidate above).

Either way, **assign distinct numbers** so the two never collide in a citation. Ratifying either is a v18→v19 Operational Standards bump (the v19 trigger — "new §" — is already declared in the doc's version history). The blueprint's references (info-gap §3/§8, memory-archive) should then be disambiguated in the same pass (a session-close-maintainer item, since info-gap currently uses "§50" for both).

### (c) §41 version-bump checklist (ready, for if/when Seth ratifies a new §)

Per the [§41 version-bump discipline](../../doctrine/operational-standards.md), when Seth ratifies §50 and/or §51 (Seth-only — doctrine is high-capability-class):

1. Add the ratified section(s) to `doctrine/operational-standards.md` (§50 code-actuation gate and/or §51 SoR-write), each with a Reference line (session-log path / PR / first-instance workstream).
2. Bump frontmatter `version: 18 → 19`; set `supersedes: doctrine/operational-standards.md@v18`; refresh `last_verified` + `last_verified_against` to the verifying exec SHA.
3. Add a v19 entry to the version-history footer (the declared v19 trigger "new §" is satisfied) and a fresh v20 trigger line.
4. Push the canonical git tag `operational-standards-v19` post-merge (doctrine + memory-archive are the only git-tagged docs; blueprint lands on `main` + tags).
5. Move this mission's §16(a)/(b) flags **resolved**: cite the now-ratified §§ in place of "candidate / flag," and unblock P7 + M2/M3 (and promote this mission `draft → canonical` once the pipeline lands — see [Authority](#17-authority)).
6. Reconcile the cross-references that cited a candidate "§50": Safety Portal mission v4/v5 §14 framing moves "workstream-fact → cited doctrine"; info-gap §3/§8 disambiguates §50 vs §51; memory-archive notes the ratification.
7. Run `python scripts/lint_frontmatter.py` + `python scripts/lint_crossrefs.py` (clean); run `doc-reconciliation-auditor` to confirm the new §§ match the as-built (`publish_daemon.py` for §50; the up-sync daemon for §51 once built).

## 17. Authority

ITS — Progress Reporting Mission **v1, draft, 2026-06-28**. Authored from the operator-confirmed master plan (`~/.claude/plans/let-s-go-with-option-greedy-fiddle.md`) + the execution handoff brief + the 2026-06-28 execution session (exec `SolutionSmith-debug/its@9ef3d5b`; [memory-archive §G43](../../references/memory-archive.md)). Both Foundation invariants are restated verbatim from [Foundation Mission v11](../../doctrine/foundation-mission.md) (§8). Workstream missions are frontmatter-versioned (not git-tagged).

**Why `draft` and not `canonical`.** The locked strategic decisions (§9) are in force and non-negotiable, but the load-bearing pipeline this mission describes is a **forward plan** — only the Tier-A foundation (M1/P-A1/A2 + the UI fix) has landed, and the external-send + SoR-write legs are **gated on unratified doctrine** (§16). **Canonical-promotion trigger:** the Stage-2 progress send (P5) lands and the §50/§51 SoR-write doctrine is ratified — at which point this mission reconciles to `canonical` against the then-current exec SHA, with the §16 flags moved to resolved.

**Authority boundary honored this pass:** zero edits under `doctrine/`; the two doctrine candidates (SoR-write text + the §-numbering recommendation) are raised propose-only; no doctrine `version:` bumped. The only convention-layer edit is adding `progress_reporting` to the canonical workstream enum (`CONVENTIONS.md` + `scripts/lint_frontmatter.py`), which also corrected a pre-existing drift (`urs_marine_portal` was enforced by the lint but missing from `CONVENTIONS.md`).

Cross-references:
- [Foundation Mission v11](../../doctrine/foundation-mission.md) — invariants inherited (restated verbatim in §8); §8 honors Invariant 1 (two-process send) + Invariant 2 (Layer-6 image screen).
- [Operational Standards v18](../../doctrine/operational-standards.md) — §14 parameterize-not-clone deviation, §34 image screen, §43 successor-remediation DoD, §45 find-or-create, §46 workspace-membership = approval; §50/§51 raised propose-only (§16).
- [Safety Portal mission v5](../safety-portal/mission.md) + [Safety Reports mission](../safety-reports/mission.md) — the capture/report-pipeline sibling-split precedent and the shared, parameterized pipeline machinery.
- [URS Marine portal mission v1](../urs-marine-portal/mission.md) — the field-ops portal data architecture (D1-as-SoR, three-tier RBAC, integrity bar) this depends on.
- [memory-archive §G43](../../references/memory-archive.md) — the program launch + the four locked strategic decisions + the live-lockout root-cause.
- [2026-06-28 progress-reporting-mission session log](../../session-logs/2026-06-28_progress-reporting-mission.md) — this mission + the flags raised.

v2 trigger: a substantive scope change — the canonical-Evergreen Smartsheet integration moving in scope (PJOB→JOB reconciliation), a swap of the ITS-owned-SoR posture, doctrine ratification of the §50/§51 flags (which moves §16's framing from candidate to cited doctrine), or a Personnel-CRUD product decision that reshapes the field-ops surface this depends on. Status-overlay updates absorb slice-landing / activation progress without a major bump.
