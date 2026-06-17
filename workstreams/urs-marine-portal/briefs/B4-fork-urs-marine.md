---
type: brief
version: 1
status: draft
last_verified: 2026-06-16
last_verified_against: SolutionSmith-debug/its@fb15881
workstream: urs_marine_portal
tags: [workstream-brief, cc-brief, urs-marine, fork, data-model, integrity-bar, demo-seed, branding]
---

# CC Brief B4 — Fork the URS Marine exec + brand + URS data model + demo seed

> **You start with no context.** DIRECTION + INCLUSION below. This is the brief where the URS
> *context home* pays off: read it rather than have it re-narrated. Pinned to `its@fb15881` +
> `its-portal-template` HEAD; **run `brief-validator` first.** B4 touches the outbound adapter
> wiring and photo ingestion — **paste `prompts/snippets/invariant-restatement.md` into the
> output.**

## Cold-start context

**Where you are.** You will create a new private repo `~/its-urs-marine` by **forking
`its-portal-template`** (the platform), then add URS-specific schema, brand, and seed data.
`~/its-blueprint` is a sibling.

**DIRECTION — read first (this is the URS context, in the repo).**
- `~/its-blueprint/workstreams/urs-marine-portal/mission.md` — the ratified + resolved decisions,
  the three-tier RBAC, the D1-as-SoR data architecture, the integrity bar, the invariants, branding,
  maintenance model. **This is your authority for everything URS-specific.**
- `~/its-blueprint/workstreams/urs-marine-portal/brief.md` §2 (the D1 data model you implement here)
  + §4 (named adapter seam) + §5 (demo scope).
- `~/its-portal-template/CLAUDE.md` — the platform contract (D1-as-SoR posture, both invariants,
  discipline, subagent roster). The capability model (B2) and the adapter seam + no-op adapter (B3)
  are already in the template — inherit them.
- `~/its-blueprint/references/customer-fork-setup-checklist.md` — the §39 baseline for the new repo.

**INCLUSION — engagement decisions (already captured in the mission/brief above; restated only
where B4 acts).**
- **D1 = structured-data SoR / Box = document SoR / Monday = bounded outbound view** — and URS
  **reverses** the Safety Portal's "no timesheet/financial data" scoping + backdating acceptance, so
  the **integrity bar is mandatory** on `time_entries` / `inspections` / `equipment_logs` (see
  brief §4).
- **Brand assets are operator-provided.** Wire the slots + the gold-script "Integrated Technical
  System" wordmark; use a clearly-marked placeholder logo until the real URS Marine division asset
  lands. `tokens.css` is unchanged.
- **The Monday adapter is NOT in B4.** The demo runs against the no-op reference adapter from B3
  (D1 is the SoR — nothing downstream is needed). Monday is a follow-on (B6).

## PR-1 — Fork + §39 + brand + wiring (Developer-Operator for the `gh api` steps)

- Fork `its-portal-template` → private `its-urs-marine`; apply the §39 baseline; verify.
- **Brand:** swap the logo slot for the URS Marine division logo (placeholder until provided); set
  the `AppHeader.tsx` lockup to the gold-script "Integrated Technical System" wordmark; leave
  `tokens.css` (BRG `#013d2b` + gold `#c6a04d`) untouched.
- **Wiring:** the fork's `CLAUDE.md` states the URS scope + D1-as-SoR, cites
  `../its-blueprint/workstreams/urs-marine-portal/{mission,brief}.md` as the workstream authority and
  `../its-blueprint/doctrine/{foundation-mission,operational-standards}.md` as doctrine; inherit the
  skills symlinks + guard hooks from the template.

## PR-2 — URS D1 data model (implements brief §2 + the §4 integrity bar)

New migrations, continuing the template's numbering. Tables per brief §2: `clients`, `jobs` (fed
from work contracts — **not** the Smartsheet-mirror shape the template dropped), `personnel`,
`equipment`, `time_entries`, `inspections`, `equipment_logs`, `equipment_location`,
`task_assignments`. Mark each accumulating-vs-bounded per the table.

**Integrity bar (mandatory on `time_entries`, `inspections`, `equipment_logs`):**
- Server-authoritative `created_at` / `edited_at` via `unixepoch()` — **never the phone clock.**
- Field-reported *event* time (e.g. `work_started_at` / `work_ended_at`) in **separate** claim
  fields, distinct from the record timestamps.
- Generalize the Safety Portal's dual-attribution (`actor_username` / `submitted_as`, migration
  0008) onto each accumulating record.
- Append-only edit chain via the `amends_uuid` pattern + an `audit_log` row per create/edit.
- Version-pin `form_code` + `version` on each `inspections` row.

`inspections` follows the inherited `submissions` shape. `equipment_location` is an append-only
point-in-time event log; "current location" is the bounded latest-read view (**no live tracking;
the EXIF/location capture keeps its display-only, best-effort, 'unavailable'-path behavior**).
Honor ORDER DEPENDENCY (apply before the Worker that reads the new columns deploys).

## PR-3 — URS roles seed + marine inspection forms

- Seed the capability model (B2's `roles`/`capabilities`/`role_capabilities`) with the three URS
  tiers (Submitter / Supervisor / Admin) + the **Tier-1 field-guy / field-manager** subset
  (provisional — flag pending the discovery split). Re-use the starter capability keys from B2.
- Seed the **marine equipment-inspection forms** from the Evergreen templates as starting points
  (the skid-steer / telehandler definitions + the `circle_one` fuel pattern), via the inherited
  declarative form engine + `meta-schema.json`. Reviewed by `form-definition-reviewer`. (Net-new
  marine forms are a follow-on, B7.)

## PR-4 — Demo seed + adapter wiring + three-tier validation

- Seed realistic marine-construction demo data: clients, jobs (e.g. seawall / dock / pile-driving),
  a personnel roster (field crew + supervisors mapped to tiers), a marine-equipment roster, time
  entries, filled inspections, fuel/hours/maintenance logs, task assignments, progress.
- Configure the **no-op reference adapter** (from B3) as the active adapter for the demo.
- Validate the full demo on the **real stack** (`wrangler dev` + local D1 + Vite): Tier 1 capture +
  time entry **with the integrity bar visibly enforced** (server timestamp; backdating leaves an
  audit trail); Tier 2 Personnel / Equipment / Job-Tracker dashboards real against seeded D1; Tier 3
  account/role management + form-builder/publish.

## Definition of done

- `its-urs-marine` boots on the real stack, seeded, with all three tiers working and the integrity
  bar demonstrable on time entries.
- The portal runs fully with the adapter as a no-op (D1 is the SoR); no PM tool required for the
  demo.
- Brand slots wired (placeholder logo noted for operator replacement); `tokens.css` unchanged.
- §39 verified; reviewed by `portal-worker-security-reviewer` (the new schema/endpoints don't
  weaken auth/HMAC/capability) + `ops-stds-enforcer` + `form-definition-reviewer` (the seeded forms).
- **§43 note** for the URS data surfaces (symptom + low-class repair + escalate-to-Seth boundary).
- Squash; linear; propose-only. The demo is the production foundation.

## Follow-ons after B4 (not in scope here)

- **B5** — blueprint doctrine cascade: record the portal-template fork-model amendment in
  `doctrine/excellence-roadmap.md` (markdown-only, behind the `block-doctrine-write` guard).
- **B6** — the Monday adapter (implement B3's `Adapter` interface for Monday.com).
- **B7** — net-new marine-specific forms via the form-builder + publish pipeline.
