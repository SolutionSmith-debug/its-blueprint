---
type: scaffold
name: cc-implementation
version: 1
audience: chat
usage_count: 0
---

# CC Implementation Prompt

For chat to write to CC when directing implementation work in the
execution repo. This is the highest-volume scaffold; it's the shape
of every implementation brief.

## When to use

- Chat is directing CC to write code, modify code, or land a PR in `its`
- The work has clear inputs (files to touch, tests to add) and clear
  outputs (acceptance criteria, verification gates)

## How to use

1. Fill in every placeholder. Don't leave `{...}` literal text in the
   final prompt.
2. Cross-reference doctrine docs by stable anchor path
   (`doctrine/foundation-mission.md#invariant-1-...`), not by version.
3. If the work touches external-bound code, include the invariant
   restatement (see `snippets/invariant-restatement.md`).
4. Always include the verification gates verbatim. CC should never
   have to infer "what does done mean."

## Template

```
# Brief: {one-line summary of what's being built}

## Objective

{2-3 sentences: what this delivers, why now, what it unblocks}

## Pre-implementation: verify baseline

cd ~/its && git status                          # clean on main, sync'd with origin
pytest -q && mypy . && ruff check .            # all green

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

## Tests

- New test files: {paths}
- Modified test files: {paths}
- Test counts target: {N} new tests; total suite must stay green

## Out of scope

- {thing this PR explicitly does NOT touch}
- {another thing}

## Verification gates

pytest                                          # green
mypy .                                          # 0 errors / N source files
ruff check .                                    # clean
{any workstream-specific live smoke}

## Done when

- All gates green
- PR landed via four-part verify (see prompts/scaffold/pr-merge-verify.md)
- Session log committed at docs/session_logs/YYYY-MM-DD_{slug}.md

## Anti-patterns to avoid

- DO NOT {specific thing easy to do wrong}
- DO NOT {another specific thing}
```

## Why this works

Five load-bearing properties:

1. Explicit file paths, not descriptions. "shared/quarantine.py" not "the quarantine module."
2. Invariants restated even though they're in doctrine — defense in depth.
3. Out-of-scope list prevents scope creep.
4. Verification commands provided verbatim — CC doesn't infer.
5. Anti-patterns explicit — captures the "what almost-correct looks like."

These five together turn implementation prompts from "instructions CC might misread" to "executable checklists CC follows mechanically."
