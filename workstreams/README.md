# Workstreams

Per-workstream mission + brief pairs. Each subdirectory is one workstream,
named in kebab-case.

| Subdir | Workstream tag | Phase | Status |
|---|---|---|---|
| [`safety-reports/`](safety-reports/) | `safety_reports` | 1 | active build |
| [`safety-portal/`](safety-portal/) | `safety_portal` | 1.6+ | active build — live on mirror; form manager + admin dashboard landed; open: prod cutover + tracked hardening |
| [`field-ops-portal/`](field-ops-portal/) | `field_ops` | 2.5 | as-built (v1) — LIVE; portal-as-writer + §51 dual Active-Jobs mirror (`fieldops_sync`) |
| [`progress-reporting/`](progress-reporting/) | `progress_reports` | 2 | as-built (v2, canonical) — live; safety-reports twin (mirror suite: hours/equipment/materials/incidents) |
| [`operator-dashboard/`](operator-dashboard/) | `operator_dashboard` | WS2 | as-built (v1 stub) — ships dark (PIN); localhost obs + PIN-gated ACT surface |
| [`email-triage/`](email-triage/) | `email_triage` | 3 | planning only |
| [`purchase-orders/`](purchase-orders/) | `purchase_orders` | 5 (Aug-7 WS1) | as-built (v5) — `po_materials` deterministic PO pipeline, live on mirror, ships dark; RFQ stage deferred post-delivery |
| [`subcontracts/`](subcontracts/) | `subcontracts` | 5 (Aug-7) | as-built (v5) — generation built + dark (ADR-0003, no-AI); SC-S4 send half remaining (in Aug-7 scope) |
| [`ai-employee-capabilities/`](ai-employee-capabilities/) | `ai_employee_capabilities` | 3 | planning only |
| [`urs-marine-portal/`](urs-marine-portal/) | `urs_marine_portal` | Customer 2 | active build — template-first; B1–B5 CC briefs in `briefs/` |

## Convention

Each workstream directory contains exactly two docs (initially):

- `mission.md` — what this workstream does, why it exists, success
  criteria. Audience: anyone forming a mental model of the workstream.
- `brief.md` — implementation-shaped: data flow, scripts, schemas,
  prompts, sequencing. Audience: cc + chat directing implementation.

Both inherit doctrine; both restate the External Send Gate + Adversarial
Input Handling invariants explicitly in the brief's "Foundation invariants"
section (defense in depth).

When a workstream grows complex enough that the brief stops fitting in
one file, split into `brief-architecture.md`, `brief-implementation.md`,
etc. — same directory, same workstream tag.
