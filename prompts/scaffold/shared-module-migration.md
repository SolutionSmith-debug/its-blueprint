---
type: scaffold
name: shared-module-migration
version: 1
audience: chat
usage_count: 1
---

# Shared-Module Migration

For chat directing CC to add a new helper module to `shared/*` AND
migrate consumers in one PR. The pattern proven by `shared/state_io.py`
(PR #88, F19 + F23). Reusable for `shared/circuit_breaker.py` (F08),
`shared/approval_verification.py` (F22), and future shared/* extractions.

## When to use

- New `shared/*` module landing with one or more consumer migrations.
- Existing helper getting a new consumer that touches multiple callsites
  in one or more files.
- Refactor that pulls duplicated code into a `shared/*` helper.

## When NOT to use

- Pure new module with zero consumer changes (no migration needed) —
  use `cc-implementation.md`.
- Pure refactor inside an existing module with no API shape change —
  use `cc-implementation.md`.

## How to use

Six-step pattern. Each step is a section in the resulting CC brief.

### Step 1 — Identify callsites with verified line numbers

Grep explicitly for the patterns being replaced. Capture file path +
line number + before-text. Re-verify at pre-flight; brief-authoring
to CC-execution drift invalidates the table.

```bash
grep -n "{pattern}" {file1} {file2} ...
```

Build a markdown table in the brief:

```markdown
| File | Line | Current | After |
|------|------|---------|-------|
| ...  | ...  | ...     | ...   |
```

### Step 2 — Design helper signature

Resolve these decisions before drafting the brief:

- **API shape.** What functions does the helper expose? What types?
- **Lock semantics** (if applicable). Non-blocking with bounded retry
  matching `shared/alert_dedupe._acquire_lock`? Indefinite blocking?
  Caller-provided timeout? **Default: match alert_dedupe pattern for
  consistency.**
- **Error semantics.** What gets raised vs. returned? What's the typed
  exception class? Where does the exception cross module boundaries?
- **Failure posture per consumer.** Each consumer decides fail-open vs.
  fail-closed in its own catch site. The helper raises; consumers
  decide. Document the decision per consumer in the brief.

### Step 3 — Write helper + tests FIRST

The brief should specify: helper module + unit tests land before any
consumer migration. TDD on the helper. Helper passes its own tests
before any consumer code is touched.

Test surface to cover:

- Happy path for each public function.
- Error paths (each typed exception class).
- Concurrent-access regression (if a lock is involved — spawn threads,
  assert no clobber).
- Cleanup regression (if temp files are involved — assert no residue
  on success, on exception, on lock failure).

### Step 4 — Migrate callsites with consistent error handling

Every consumer of the new helper handles errors the same way for the
same class of decision. If consumer A logs+continues on
`StateLockTimeoutError`, consumer B does too (unless there's an
explicit rationale comment per §42).

The brief enumerates each callsite with the explicit before/after.
No "and similar elsewhere" — every callsite gets a row.

### Step 5 — Docs / doctrine updates this PR

- **CLAUDE.md table row** in the execution repo. New `shared/{module}.py`
  row in the "What's stubbed vs real" table.
- **Tech-debt entry** (`docs/tech_debt.md`) — CLOSED entry referencing
  the audit F-finding(s) closed by this PR.
- **§42 module docstring** on the new helper (Purpose / Invariants /
  Failure modes / Consumers).
- **Doctrine cascade** if applicable. New shared helper may motivate a
  blueprint-side doctrine bump; the brief calls it out explicitly.

### Step 6 — Manual smoke + four-part verify

The brief includes:

- Manual-smoke section per `manual-smoke.md` scaffold. Operator-side,
  post-CC-completion, pre-merge.
- Four-part verify reference per `pr-merge-verify.md`.

## Template (skeleton)

```markdown
# CC Brief — {helper name} + {migration scope summary}

## Purpose

{What helper, what callsites, which F-findings closed, predecessor PR}

## Pre-flight verification

1. Confirm {helper module path} does not exist.
2. Confirm migration callsites still match the line table (re-grep).
3. Confirm {any predecessor work landed cleanly}.

## New module — `shared/{name}.py`

{Signature + behavior + error semantics. §42 docstring drafted inline.}

## Migration callsites

{Explicit table: file + line + before + after for every callsite}

## Tests

- `tests/test_{name}.py` — N test cases covering {…}
- Consumer test files — {modifications needed}

## Docs / doctrine updates this PR

- CLAUDE.md row
- docs/tech_debt.md CLOSED entry
- §42 module docstring

## Out of scope

{Explicit fence — what's NOT touched this PR}

## Verification gate

- pytest / mypy / ruff
- Manual smoke (operator-side, per manual-smoke.md scaffold)
- Four-part PR-landed verify (per pr-merge-verify.md scaffold)

## Cross-references

- Audit F-findings
- Predecessor PRs
- Related doctrine sections
```

## Why this works

- **Helper-first TDD** prevents the "helper exists but the migration
  reveals an API gap" rework cycle.
- **Verified line tables** make the brief auditable. CC re-verifies at
  pre-flight; the discipline catches drift.
- **Consistent error handling per consumer** prevents the "fail-open in
  daemon A, fail-closed in daemon B, no one remembers why" drift.
- **§42 docstring in the new module** captures the rationale at the
  exact moment the choices are fresh, before the next session forgets.
- **Manual-smoke + four-part verify built into the scaffold** means no
  paste-ready brief skips them under deadline pressure.
