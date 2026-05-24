# Audits

Time-bound forensic snapshots against a closed scope. Each audit is
date-prefixed and immutable once committed — they're the truth-of-record
for a point-in-time investigation.

## Convention

- Filename: `YYYY-MM-DD_<topic-slug>.md`
- Frontmatter: `type: audit`, `status: archived` (audits don't have
  successors; they're snapshots), `workstream: null` for cross-cutting
  or specific workstream tag for scoped audits.
- No version bump after publication — audits are write-once.
- When a follow-up audit revisits the same scope, it's a new doc with
  a new date prefix. The relationship can be noted in the new doc's
  preamble.

## Current audits

- [`2026-05-17_box-smartsheet-reconciliation.md`](2026-05-17_box-smartsheet-reconciliation.md) —
  Box folder ↔ Smartsheet sheet ID reconciliation against the live mirror
  tenant.
- [`2026-05-21_cascade-verification.md`](2026-05-21_cascade-verification.md) —
  Forensic verification of the 2026-05-21 cascade against the actual
  repo state, before the 05-22 cascade absorbed findings.
- [`2026-05-21_security-hardening-and-doc-drift.md`](2026-05-21_security-hardening-and-doc-drift.md) —
  Pre-Customer-1 security review + doc-drift inventory.
