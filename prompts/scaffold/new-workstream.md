---
type: scaffold
name: new-workstream
version: 1
audience: chat
usage_count: 0
---

# New Workstream Bootstrap

For chat directing the creation of a new workstream — mission doc +
brief doc in its-blueprint, scaffolding in `its` execution repo.
Workstreams are large undertakings; this scaffold codifies the
sequencing so each phase ships cleanly.

## Pre-flight: extend the workstream taxonomy

Before authoring any mission/brief content, land a small PR that adds
the new workstream tag to:

1. `its-blueprint/scripts/lint_frontmatter.py` — `CANONICAL_WORKSTREAMS`
   set.
2. `its-blueprint/CONVENTIONS.md` — workstream table.
3. `its/docs/operations/doc_conventions.md` — execution-repo mirror.

This is its own PR. Adding the tag inline with mission/brief creation
makes lint failures confusing ("which thing broke first?").

## Mission doc (its-blueprint/workstreams/{slug}/mission.md)

Required sections in this order:

1. **Purpose** — what this workstream does. Two-paragraph max.
2. **Audience** — who consumes the output. Operator-facing,
   customer-facing, external recipient, or some combination. This
   shapes everything downstream.
3. **Inputs** — what triggers it; what data it reads.
4. **Outputs** — what artifacts it produces; where they land
   (Smartsheet sheets, Box folders, email recipients).
5. **Success criteria** — concrete, measurable. "Reduce manual
   intervention by 80%" is not measurable; "Field PM no longer
   manually creates DFR rows" is.
6. **Out of scope** — what this workstream explicitly doesn't do.
7. **Foundation invariants** — restate External Send Gate and
   Adversarial Input Handling with workstream-specific application.
   Paste the contents of `snippets/invariant-restatement.md` and fill
   in the workstream-specific application notes.

## Brief doc (its-blueprint/workstreams/{slug}/brief.md)

Required sections in this order:

1. **Implementation phases** — numbered, each phase shippable
   independently. Phase 1 is always "scaffolding + first end-to-end
   path."
2. **Data flow** — diagram (mermaid preferred) or prose. Show the
   pipeline from trigger to output.
3. **Modules to create** — paths in the `its` repo. One bullet per
   module.
4. **Schemas** — paths in `its/schemas/`. One bullet per schema.
5. **Prompts** — paths in `its/prompts/` (runtime prompts, not
   scaffolds). One bullet per prompt.
6. **Tests** — what gets tested, what stays mocked, what needs
   integration coverage per the SDK-vs-Live discipline.
7. **Sequencing dependencies** — what other workstreams or shared
   modules must be ready before this one can ship.

## Execution-repo scaffolding (after mission + brief land)

Once mission and brief are merged in blueprint:

1. Create `its/{workstream}/` directory.
2. Mirror the `safety_reports/` shape: separate `intake.py`,
   `{workstream}_generate.py`, `{workstream}_send.py`, polling daemon
   variants as needed. Don't deviate from this shape without explicit
   doctrine guidance.
3. Add both generation and send scripts to
   `tests/test_capability_gating.py` per Foundation Mission Invariant
   1. The `GATED_SCRIPTS` and `SEND_SCRIPTS` lists are the enforcement
   mechanism.
4. Wire `@require_active` kill-switch decorator + `@its_error_log`
   decorator on every entry point.
5. Add launchd plist if polling daemon is the trigger pattern.
6. First PR: scaffolding + stubs + capability-gating test green +
   ruff/mypy clean. No actual logic yet.

## Anti-patterns

- DO NOT skip the taxonomy PR. Adding a workstream tag inline with the
  mission/brief PR makes the lint failure mode confusing.
- DO NOT collapse generation + send into one script "for now." The
  two-process model is non-negotiable per Invariant 1; once collapsed,
  it's painful to unwind.
- DO NOT defer adding the workstream to capability-gating tests. Empty
  list entries are fine; the wiring is what matters.
- DO NOT author the brief before the mission. The mission constrains
  the brief; reversed order produces a brief that drifts from intent.

## Why this works

The mission-then-brief-then-scaffolding sequence catches "we don't
actually agree on what this workstream does" before any code lands.
The two-process model enforced via capability-gating tests at
scaffolding time means the invariant can't be accidentally violated
by later commits — the test fails first.
