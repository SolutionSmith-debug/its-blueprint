---
type: brief
version: 1
status: draft
last_verified: 2026-06-16
last_verified_against: SolutionSmith-debug/its@fb15881
workstream: urs_marine_portal
tags: [workstream-brief, urs-marine, data-model, d1-system-of-record, integrity-bar, adapter-seam, demo-scope, build-sequence]
---

# URS Marine — portal architecture brief

> **Altitude.** Architecture-level. Companion to [`mission.md`](mission.md), which holds the
> decisions and invariants. This brief holds the data model, the demo scope, and the build
> sequence. Implementation mechanics live in the CC briefs B1–B4. `status: draft` per the mission.

## 1. Architecture overview

```
┌──────────────────────┐  HTTPS   ┌──────────────────────────────────────┐
│  Field / Supervisor  ├─────────►│ Cloudflare Workers + static SPA        │
│  browser (phone /    │  /api/*  │  • single Worker serves SPA + same-     │
│  tablet / desktop)   │          │    origin /api/*                        │
└──────────────────────┘          │  • D1 = STRUCTURED-DATA SYSTEM OF RECORD │
                                   │    (jobs, time, equipment, inspections, │
                                   │     machine logs, tasks, attribution)   │
                                   │  • send-free; HMAC-signed outbound queue │
                                   └──────▲───────────────────┬─────────────┘
                            bearer-gated  │ PULL (drain)       │ bearer-gated
                            /api/internal/ │                    │ /api/internal/
                            pending  ──────┘                    │ mark-filed · sync
                                   ┌──────────────────────────┴─────────────┐
                                   │ Integration-device host (Mac mini OR     │
                                   │  Solution-Smith-hosted OR GH Actions)    │
                                   │  • host-agnostic transport (pull + HMAC)  │
                                   │  • pluggable PM ADAPTER (Monday = sibling │
                                   │    of Smartsheet; portal core unaware)    │
                                   │  • Box = document system of record        │
                                   └──────────────────────────────────────────┘
```

Three facts define it: the Worker is **send-free** (Invariant 1); **D1 is the structured-data
system of record** (inverts Customer 0); the PM tool is reached only through a **named adapter** over
the bearer-gated `/api/internal/*` contract, and the host is abstracted behind the HMAC/pull
transport.

## 2. D1 data model (first-cut; implemented by brief B4)

Box = document SoR; D1 = structured-data SoR; Monday = bounded outbound views/rollups.

| Table | Holds | Accumulating vs bounded |
|---|---|---|
| `clients` | client info | Accumulating (SoR) |
| `jobs` | jobs ← work contracts; client, status, progress | Accumulating (SoR) — **inverts Evergreen's Smartsheet mirror** |
| `personnel` | roster → capabilities | Accumulating (SoR, reference) |
| `equipment` | inventory / vehicles | Accumulating (SoR, reference) |
| `time_entries` | time/work per job | Accumulating (SoR) — integrity bar |
| `inspections` | filled machine checklists | Accumulating (SoR) — submissions-shaped, version-pinned |
| `equipment_logs` | maintenance / hours / fuel | Accumulating (SoR, event log) |
| `equipment_location` | point-in-time location reads | Accumulating event log; "current" = bounded latest-read |
| `task_assignments` | assignments | Accumulating; "open tasks" = bounded view |

**Integrity bar** (applies to `time_entries`, `inspections`, `equipment_logs` — reverses the Safety
Portal's backdating acceptance): server-authoritative `created_at`/`edited_at` via `unixepoch()`
(never the phone clock); field-reported *event* time as a separate claim field; generalize
`actor_username`/`submitted_as` (migration 0008) onto every accumulating record; append-only
`amends_uuid` edit chain + an `audit_log` row per edit; version-pin `form_code`+`version` on each
inspection.

`submissions` (the platform's submission record, preserved from the template) is the shape
`inspections` follows. `jobs` for URS is a fork table fed from contracts (NOT the Evergreen
Smartsheet-mirror shape, which the template drops).

## 3. Three-tier capability model

Implemented by brief B2 (in the template): DB-driven `roles` / `capabilities` /
`role_capabilities`, fail-safe (unknown role → no capabilities). The URS seed (Submitter /
Supervisor / Admin + the Tier-1 field-guy/field-manager subset) lands in the fork (brief B4),
pending the discovery split.

## 4. Named adapter seam

Implemented by brief B3 (in the template). The Worker is already adapter-unaware — it only exposes
`GET /api/internal/pending`, `POST /api/internal/mark-filed`, `POST /api/internal/sync`
(bearer-gated). The adapter = the host-side implementation that consumes those endpoints and files
to a PM tool. The template ships the named protocol + a host-agnostic transport client + a no-op
reference adapter; the **Monday adapter is a URS-fork follow-on** (the demo runs against the no-op
adapter because D1 is the SoR).

## 5. Demo scope (real stack: Wrangler local + local D1 + Vite)

All three tiers, seeded marine data. **Tier 1:** photo capture with EXIF point-in-time caption (+
"unavailable" fallback); time entry **with the integrity bar visibly enforced** (server timestamp,
no silent backdating); equipment inspection; fuel/hours/maintenance log. **Tier 2:** Personnel /
Equipment / Job-Tracker dashboards, **real against seeded D1**. **Tier 3:** account/role management
on the capability model + the form-builder/publish pipeline. **Stubbed/deferred:** the Monday
adapter (no-op reference adapter), Box retention, the live integration-device host.

## 6. Build sequence (template-first)

`B5` (small doctrine cascade, can run in parallel) → `B1` extract `its-portal-template` → `B2`
(2→N roles) + `B3` (adapter seam) in the template, parallelizable → `B4` fork URS + brand + URS data
model + demo seed. Follow-ons after B4: the Monday adapter (B6), net-new marine forms (B7).

Template-first is chosen because the role generalization and the adapter seam belong in the
template regardless of customer; forking all of Customer 0's `its` and stripping is worse.

## 7. Reuse map (what carries / what doesn't)

Platform-universal (→ `its-portal-template`): auth/session/capability *mechanism*, the declarative
form/checklist engine + `meta-schema.json` + FormEditor + publishValidation + the send-free publish
queue, photo/signature/EXIF capture, the HMAC/pull transport contract, `tokens.css`, the reusable
subagents + guard hooks + skills scaffolding. Evergreen-specific (does NOT carry): the safety form
content + reference PDFs + catalog, the Smartsheet dialect, the weekly-safety-report workstream,
brand assets, seed migrations. Reusable exceptions: the equipment-inspection form templates
(skid-steer/telehandler + the `circle_one` fuel pattern) seed into the URS fork; the `portal_poll` +
`portal_hmac` transport pattern becomes the adapter-host seam.
