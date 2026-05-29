# Workstreams

Per-workstream mission + brief pairs. Each subdirectory is one workstream,
named in kebab-case.

| Subdir | Workstream tag | Phase | Status |
|---|---|---|---|
| [`safety-reports/`](safety-reports/) | `safety_reports` | 1 | active build |
| [`safety-portal/`](safety-portal/) | `safety_portal` | 1.6+ | planning only |
| [`email-triage/`](email-triage/) | `email_triage` | 3 | planning only |
| [`purchase-orders/`](purchase-orders/) | `purchase_orders` | 2 | planning only |
| [`subcontracts/`](subcontracts/) | `subcontracts` | 2 | planning only |
| [`ai-employee-capabilities/`](ai-employee-capabilities/) | `ai_employee_capabilities` | 3 | planning only |

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
