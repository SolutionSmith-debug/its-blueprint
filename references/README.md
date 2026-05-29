# References

Evergreen explanatory docs. Operational detail, schemas, handoff packets,
the memory archive. Different from doctrine in that these are explanatory
or stable-data rather than normative.

## Docs

- [`memory-archive.md`](memory-archive.md) — append-only operational
  detail. Restoration source after memory compaction. v4 + v5 merged
  2026-05-24; future detail extends in-place via new §G* sections.
- [`foundation-scaffold.md`](foundation-scaffold.md) — what's done in
  the execution layer. Status snapshot, bumped as the scaffold completes.
- [`project-organization.md`](project-organization.md) — naming
  conventions, project descriptions, organizational schema for the
  ITS planning + execution surfaces.
- [`daemon-health-schema.md`](daemon-health-schema.md) — schema spec
  for the ITS_Daemon_Health Smartsheet sheet. Source of truth for the
  12-column heartbeat layout.
- [`smartsheet-handoff.md`](smartsheet-handoff.md) — Smartsheet workspace
  + sheet ID handoff packet for operator-side provisioning.
- [`system-hr-handoff.md`](system-hr-handoff.md) — Smartsheet System +
  Human Review workspace handoff (subset of the above, dedicated doc
  for cross-reference).
- [`permissions.md`](permissions.md) — Customer-1 permissions matrix
  (M365, Box, Smartsheet) for the Florida → California cutover.
- [`extended-workstreams.md`](extended-workstreams.md) — Phase 2+
  workstream brief stubs (not yet planning-active).
- [`worktree-discipline.md`](worktree-discipline.md) — blueprint-side
  parallel-session worktree discipline: the `~/`-sibling `.claude`
  symlink fail-open warning (audit H1) and the "never two
  doctrine-touching sessions on one checkout" rule. Companion to the
  exec-repo `worktree_discipline.md`.
