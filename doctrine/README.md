# Doctrine

Non-negotiable invariants and the operational standards that enforce them.
Every workstream inherits from these. If a workstream mission/brief
contradicts doctrine, doctrine wins; flag the inconsistency.

Doctrine docs change rarely. Each substantive change bumps the `version`
in the doc's frontmatter and tags the canonical commit (`<topic>-vN`).
Filenames never change.

## Docs

- [`foundation-mission.md`](foundation-mission.md) — purpose, principles,
  invariants. The two architectural invariants (External Send Gate,
  Adversarial Input Handling) are defined here.
- [`operational-standards.md`](operational-standards.md) — how the
  invariants get enforced in practice. Polling-daemon doctrine,
  push-vs-record separation, picklist hardening, SDK-vs-live test
  discipline.
- [`vision-and-roadmap.md`](vision-and-roadmap.md) — phasing (0 → 4),
  gates, ship-and-leave threshold.
- [`handover-plan.md`](handover-plan.md) — Florida → California cutover
  + hardware handover sequence.
- [`excellence-roadmap.md`](excellence-roadmap.md) — quality bar, tooling
  stack, observability stack.
