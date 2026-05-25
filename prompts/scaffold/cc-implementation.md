---
type: scaffold
name: cc-implementation
version: 2
audience: chat
usage_count: 6
---

# CC Implementation Prompt

For chat to write to CC when directing implementation work in the
execution repo. This is the highest-volume scaffold; it's the shape
of every implementation brief.

## v1 → v2 changes (2026-05-25)

Three additions absorbed from `its` PR #88 (F19 + F23 atomic-write):

1. **Line-number re-grep at pre-flight** — explicit instruction to
   re-verify line tables; brief-authoring-to-CC-execution drift
   invalidates the original table.
2. **Real-API-signature discipline** — when the brief references a
   `shared/*` function (error_log, smartsheet_client, etc.), CC MUST
   verify against actual module API before applying. Mismatch is the
   verify-before-fix discipline working as designed — surface it,
   don't blindly apply.
3. **Manual-smoke callout** — if the work touches persistent state
   (`~/its/state/`) or has external-API side effects, include a
   manual-smoke section referencing `manual-smoke.md` scaffold.
   Operator-side, post-CC-completion, pre-merge.

## When to use

- Chat is directing CC to write code, modify code, or land a PR in `its`
- The work has clear inputs (files to touch, tests to add) and clear
  outputs (acceptance criteria, verification gates)

## When to use a different scaffold

- New `shared/*` module + consumer migrations → use
  `shared-module-migration.md`
- Doctrine bump in blueprint → use `doctrine-revision.md`
- New workstream bootstrap → use `new-workstream.md`

## How to use

1. Fill in every placeholder. Don't leave `{...}` literal text in the
   final prompt.
2. Cross-reference doctrine docs by stable anchor path
   (`doctrine/foundation-mission.md#invariant-1-...`), not by version.
3. If the work touches external-bound code, include the invariant
   restatement (see `snippets/invariant-restatement.md`).
4. Always include the verification gates verbatim. CC should never
   have to infer "what does done mean."
5. If the brief lists specific line numbers or function signatures,
   instruct CC to re-verify at pre-flight.

## Template

```
# Brief: {one-line summary of what's being built}

## Objective

{2-3 sentences: what this delivers, why now, what it unblocks}

## Pre-flight: verify baseline + brief assertions

cd ~/its && git status                          # clean on main, sync'd with origin
pytest -q && mypy . && ruff check .            # all green

Re-verify the following assertions in this brief before coding:

1. {Any specific line numbers cited in the file/line table — re-grep}
2. {Any specific shared/* function signatures cited — read the actual
   module}
3. {Any "X does not exist yet" claims — confirm via ls / find}
4. {Any "Y is currently broken" claims — confirm via the cited
   reproduction}

If any assertion has drifted, surface it and pause before coding.

## Context

- Files touched: {list with paths}
- Doctrine references: {doctrine/foo.md#anchor links}
- Prior PRs: {list of PR numbers and SHAs}

## Decisions already resolved

1. {decision} — {one-line rationale}
2. {decision} — {one-line rationale}

## Foundation invariants

{If this work touches code that produces external-bound output OR processes
external content, paste the contents of snippets/invariant-restatement.md
here verbatim with workstream-specific notes filled in.}

## Substance

Phase 1: {one phase per logical chunk; numbered}
  - File: {path}
  - Change: {what changes}
  - Test: {what test covers it}

Phase 2: {...}

## API signatures referenced

If this brief calls out specific functions in `shared/*` or workstream
code, list them here. CC MUST verify each signature against the actual
module before applying. Mismatches are caught early via verify-before-fix.

- `shared/error_log.py`: `log(severity, script_name, msg, error_code=...)`
- `shared/smartsheet_client.py`: `{...}`
- {etc.}

## §42 self-documentation requirements

If this brief creates a new `shared/*` module or workstream entrypoint:

- Module docstring with four headings: Purpose / Invariants / Failure
  modes / Consumers (per Op Stds §42).
- In-code rationale comments for non-obvious decisions, citing the
  motivating F-finding, session-log, doctrine §, or PR.

## Tests

- New test files: {paths}
- Modified test files: {paths}
- Test counts target: {N} new tests; total suite must stay green
- §30 integration test (live sandbox, `pytest -m integration`) if this
  PR touches an SDK boundary wrapper.

## Out of scope

- {thing this PR explicitly does NOT touch}
- {another thing}

## Verification gates (pre-merge)

pytest                                          # green
mypy {file paths}                              # 0 errors
ruff check {file paths}                        # clean
{any workstream-specific live smoke}

If this PR touches `~/its/state/` or has external-API side effects,
operator runs manual-smoke per `prompts/scaffold/manual-smoke.md`
between CC completion and authorize-merge.

## Done when

- All gates green
- Operator manual-smoke (if applicable) passes assessment
- PR landed via four-part verify (see prompts/scaffold/pr-merge-verify.md)
- Session log committed at docs/session_logs/YYYY-MM-DD_{slug}.md

## Anti-patterns to avoid

- DO NOT apply brief-cited line numbers or signatures without
  pre-flight re-verification.
- DO NOT silently fix API-signature mismatches; surface them.
- DO NOT skip the §42 docstring on new modules.
- DO NOT scope-creep beyond the explicit file list.
- DO NOT {workstream-specific specific thing easy to do wrong}.
```

## Why this works

Seven load-bearing properties (v2 adds two to v1's five):

1. Explicit file paths, not descriptions. "shared/quarantine.py" not
   "the quarantine module."
2. Invariants restated even though they're in doctrine — defense in depth.
3. Out-of-scope list prevents scope creep.
4. Verification commands provided verbatim — CC doesn't infer.
5. Done criteria explicit — no "ship when CC thinks it's ready."
6. **(v2)** Pre-flight verify of brief assertions — line numbers and
   API signatures get re-checked, catching brief-authoring drift before
   it becomes a wrong-code commit.
7. **(v2)** §42 docstring + rationale comments mandated for new modules
   — makes future-reader's first question ("why is this here?")
   answerable without leaving the file.
