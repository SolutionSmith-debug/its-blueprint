---
type: mission
version: 1
status: draft
last_verified: 2026-06-16
last_verified_against: SolutionSmith-debug/its@fb15881
workstream: urs_marine_portal
tags: [workstream-mission, urs-marine, customer-2, portal, rbac, d1-system-of-record, adapter-seam, integrity-bar, foundation-invariants]
---

# URS Marine — Integrated Technical System (workstream mission)

> **Altitude.** This is the architecture/decision home for the URS Marine build. It carries the
> decisions made in the kickoff engagement that live in no other repo, so any Claude Code session
> that touches this workstream reads its context here instead of having it re-narrated. Implementation
> mechanics (migration line numbers, exact file edits, PR breakdowns) live in the CC briefs
> (`B1`–`B4`), not here.
>
> `status: draft` until the portal-template fork-model amendment is cascaded into
> `doctrine/excellence-roadmap.md` (brief B5). If anything here contradicts execution-layer code,
> the code is ground truth — flag it and reconcile.

## 1. Product context

URS Marine is the **Marine Construction division of United Restoration Services** (trusturs.com),
**Customer 2** — a paying customer from day one (not a favor build). The deliverable is a
**project- / personnel- / equipment-management portal**, reusing the Evergreen platform via the
`its-portal-template` fork-source. The parent line is emergency restoration; marine-construction
job and equipment types differ from it (confirm specifics in discovery).

This workstream is a **new kind of portal** relative to Customer 0's Safety Portal. It shares the
*platform* (auth, the declarative form/checklist engine, capture, the send-free Worker + HMAC/pull
transport) but differs fundamentally in **data architecture** (see §3) and domain.

## 2. Three-tier access model (capability-gated RBAC)

RBAC is capability-gated, not role-string-gated. Three tiers; per-capability flags within a tier.

- **Tier 1 — Submitter (field, phone-first).** Capture site photos with the EXIF point-in-time
  location sidecar (display-only, best-effort, the "unavailable" path is REQUIRED; **no live
  tracking**); log time/work against a job; view + fill machine inspection checklists; log machine
  maintenance / hours / fuel. **Open discovery item:** whether a basic "field guy" (photos only)
  and a "field manager" (photos + time + inspections + machine logs) are distinct capability
  *subsets* within this tier — expected as per-capability flags, **not a 4th tier**.
- **Tier 2 — Supervisor (oversight).** Read ALL submitted data by data-type and job-type via
  dashboards: Personnel (who is logged at which job + point-in-time location), Equipment (location,
  photos, inspection checklists, maintenance/hours/fuel), Job Tracker (assign tasks; close-out /
  inspection checklists; ties equipment + personnel + client info + progress; jobs feed from work
  contracts). **No backend config.**
- **Tier 3 — Admin.** Everything in Tier 2 plus technical/backend configuration (account
  management, form-builder + publish pipeline, adapter config, system settings).

This requires generalizing the Evergreen role model from its hardcoded 2-role union
(`'submitter' | 'admin'` in `safety_portal/worker/auth.ts` + the CHECK in migration 0007) to a
**schema/config-driven N-role / capability model** (brief B2; decision adopted: DB-driven
`roles` / `capabilities` / `role_capabilities` tables).

## 3. Data architecture — D1 is the system of record (this REVERSES the Safety Portal)

The Foundation principle here is the inverse of Customer 0's portal, and it is the most
consequential design fact in this workstream:

- **D1 = structured-data system of record** — jobs (from work contracts), client info, personnel
  time/work, equipment inventory + point-in-time location, machine inspections, maintenance/hours/
  fuel, task assignments, progress. Durable-first in D1.
- **Box = document system of record** — site photos and rendered PDFs (the Evergreen retention
  pattern, offered to URS).
- **Monday (or any PM tool) = bounded current-state views + rollups**, pushed *outward* from D1
  through a thin, swappable adapter (brief B3). The portal core is unaware which PM tool sits
  behind it. The PM tool is never the backbone.

**Why this matters / what it costs.** Customer 0's Safety Portal deliberately stores *no payment,
timesheet, or financial data* — "the portal stores nothing of direct value" — and accepts
*unlimited backdating with no entry-time indicator* (the Q2 threat-model scoping and Q4 risk
acceptance in `workstreams/safety-portal/mission.md`). URS Marine **reverses both**: D1 holds
timesheet-grade data of real value that feeds payroll/billing. Consequences:
1. The "stores nothing of value" defense no longer holds → the auth/access bar is load-bearing,
   and D1 backup/retention is operationally required.
2. **Backdating without a trace is unacceptable.** The integrity bar (§4) is mandatory, not
   optional.

## 4. The integrity bar (mandatory for time/work, inspections, machine logs)

Adopted from the kickoff (decision #3): server-authoritative record timestamps + a full audit
trail are sufficient; no stronger device-attestation is in scope unless discovery requires it.

- **Two distinct timestamp classes.** *Record* time is server-authoritative — set with
  `unixepoch()` at receipt/edit, **never the phone clock**. *Event* time (when the worker says
  work happened) is captured as a field-reported claim in its own field. The audit trail proves who
  entered/edited each record and when, so backdating leaves a trace.
- **Attribution.** Generalize the Safety Portal's dual-attribution (`actor_username` /
  `submitted_as`, migration 0008) onto every accumulating record (time entries, inspections,
  machine logs), not just submissions.
- **Edit history.** Append-only edit/amend chain (the `amends_uuid` pattern) + an `audit_log` row
  per edit.
- **Version-pinning.** Each filled inspection pins the `form_code` + `version` it was captured
  against, so checklist content is reproducible.

Monday holds none of this as backbone — only bounded rollups pushed via the adapter.

## 5. Foundation invariants inherited

Per `doctrine/foundation-mission.md` (v11). Both are non-negotiable; restate them in any brief
touching outbound send or external ingestion via `prompts/snippets/invariant-restatement.md`.

- **Invariant 1 — External Send Gate.** No external transmission without explicit human approval;
  two-process model (the generating path has zero send capability; the actuating path has zero
  reasoning step). **URS application:** any outbound push to Monday (or any PM tool) is a "send" —
  it is gated by the two-process split, and the portal Worker stays structurally send-free.
- **Invariant 2 — Adversarial Input Handling.** All content originating outside the operating
  customer tenant is untrusted data; six-layer defense (Layer 5 is a detection tripwire, not a
  barrier). **URS application:** field photos run the Layer-6 image-class screen (the
  `photo_screen.py` pattern: magic → Pillow verify / decompression-bomb cap / forced
  metadata-destroying re-encode → ClamAV-on-raw, default off); inbound contract or Monday content is
  untrusted and is never used as a logic/auth input.

## 6. Integration-device host — deferred and must stay open

The integration device (the Evergreen Mac-side pull-daemon pattern: launchd, fresh-process-per-
cycle, HMAC-verified pull) may run on a **local Mac mini at URS**, be **Solution-Smith-hosted as a
managed support package**, or migrate to **GitHub Actions + Cloudflare** if reliability suffices. Do
**not** bake a host assumption into the architecture: the **pull-daemon + HMAC contract is the
abstraction** that keeps all three paths open (brief B3). The Solution-Smith-hosted option is a
proposal support line item — and is *managed infrastructure*, kept distinct from the maintenance
model (§8).

## 7. Branding

Retain ITS colors (BRG `#013d2b` + decorative gold `#c6a04d`; `tokens.css` reused as-is). Only
`AppHeader.tsx` + two `public/` assets are Evergreen-branded: swap the logo for the URS Marine
division logo and the lockup for a gold-script "Integrated Technical System" wordmark (mirrors the
Evergreen logo-plate + gold-script pattern). Brand is injected at the fork (brief B4).

## 8. Maintenance / ship-and-leave

Per the three-tier successor model (`doctrine/foundation-mission.md` v11, `excellence-roadmap.md`):
Tier 1 self-heal / Tier 2 trained Successor-Operator + Claude (low-capability-class repairs) /
Tier 3 Developer-Operator (Seth) as a reachable escalation asset. **The "Solution Smith remains
primary operator" framing is retired** — do not use it in proposal or runbook language.
**Open discovery item:** whether URS staffs a Tier-2 Successor-Operator or contracts Solution Smith
for ongoing support (shapes the proposal's support tiers).

## 9. Out of scope / non-goals

- **No multi-tenancy.** URS is a separate private fork (per-customer-repo invariant; no "current
  customer" parameter, no tenant-keyed lookups). Multi-tenancy is retired doctrine.
- **No customer-facing email send obligation** in scope — the External Send Gate manifests as the
  outbound-adapter gate, not an email path.

## 10. Success criteria

- A localhost demo on the real stack (Wrangler local + local D1 + Vite), seeded with realistic
  marine-construction data, exercising all three tiers — so the demo *is* the production
  foundation.
- Time/work entries are payroll-defensible: server-authoritative record time + edit trail; no
  silent backdating.
- The portal runs fully without any PM-tool integration (D1-as-SoR) — Monday is a stub for the
  demo.

## 11. Ratified + resolved decisions — do NOT re-litigate

Carried from the kickoff engagement. Fixed inputs for every CC brief in this workstream:

1. Three-tier capability-gated RBAC (§2); 2→N role generalization (decision #2 → DB-driven
   `roles`/`capabilities` tables).
2. `its-portal-template` is the fork-source; customers fork from blueprint + portal-template (amends
   "fork the execution repo"). Cascade into doctrine via B5.
3. Named adapter seam; Smartsheet and Monday are sibling drop-in adapters; the portal core is
   adapter-unaware.
4. Integration-device host deferred and kept open; pull-daemon + HMAC is the abstraction; the
   Solution-Smith-hosted option is a proposal line item.
5. ITS colors retained; brand swapped at the fork.
6. **D1 = structured-data SoR / Box = document SoR / Monday = bounded outbound views** (§3) — this
   reverses the Safety Portal's "no value stored" scoping and its backdating acceptance, so the
   integrity bar (§4) is load-bearing.

## 12. Open discovery items (gate the proposal, not Task Zero)

Tier-1 field-guy-vs-field-manager capability split; how Monday boards are actually used (replace vs
alongside); current record-filing setup (pitch Box); contract→job intake mechanics; equipment/
vehicle roster + inspection + fuel/maintenance cadence; personnel roster → tier mapping; billing/
payroll audit requirements (drives the integrity bar); employee-monitoring / location-disclosure
posture (FL); confirmation that marine job/equipment types differ from the restoration parent;
whether URS staffs a Tier-2 Successor-Operator or contracts ongoing support.
