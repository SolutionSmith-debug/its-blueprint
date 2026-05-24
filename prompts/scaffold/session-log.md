---
type: scaffold
name: session-log
version: 1
audience: chat
usage_count: 0
---

# Session Log

Durable narrative record of a session that changed project state.
Captures the decisions made *during* the session — context that
doesn't survive in commit messages or in the doc-diff alone.

## When to write one

Both conditions must be true:

1. The session changed project state — ≥1 commit, doctrine revision,
   architectural decision, or operator-actioned external system change.
2. The session involved at least one non-obvious decision — a choice
   between valid alternatives, a deliberate carveout, an item handed
   off to the planning project, or a diagnosis that didn't match the
   initial brief.

Mechanical changes (typo fixes, dep bumps, formatting-only) don't need
logs. If unsure: write it. Cost of an unnecessary log is one extra
commit; cost of a missing log is reconstructing context from
transcripts.

## Where the log lives

- **Planning-side session** (touched its-blueprint doctrine, missions,
  briefs, references) → `session-logs/YYYY-MM-DD_{slug}.md` in
  its-blueprint.
- **Execution-side session** (touched its code, tests, scripts) →
  `docs/session_logs/YYYY-MM-DD_{slug}.md` in `its` repo.
- **Mixed session** (touched both repos) → log in each repo;
  cross-reference them in each session log's "Cross-references" section.

## Template (planning-side)

```markdown
---
type: session_log
status: archived
workstream: {tag} | null
tags: [{topical-tags}]
---

# YYYY-MM-DD — {one-line session focus}

## Purpose

1-2 sentences on what the session set out to do.

## Pre-flight findings

Anything surprising discovered before changes (state didn't match
prior brief, prior PR had drift, etc.).

## Decisions made

For each non-obvious decision:

- **Decision**: {what was decided}
- **Alternative considered**: {what was rejected}
- **Rationale**: {why}

## Doc changes

File-by-file summary. Include commit SHAs for changes landed.

## Verification

- `python scripts/lint_frontmatter.py` → clean (N files)
- `python scripts/lint_crossrefs.py` → clean (N files)

## Out of scope

Explicit list of what was deliberately NOT touched.

## Sequencing context

What this unblocks. What was prerequisite. What follow-ons remain.

## Cross-references

- Related execution-repo session log (if applicable):
  https://github.com/SolutionSmith-debug/its/blob/main/docs/session_logs/{path}
- Related PRs: {numbers}
```

## Template (execution-side — slightly different shape)

Execution-repo session logs use the four-part verification block per
`pr-merge-verify.md` instead of the lint block. The four-part block
is:

```
- pytest: <N> passed / <M> skipped / <D> deselected
- mypy: <E> errors / <F> source files
- ruff: clean
- main-branch CI on merge commit: SUCCESS
```

Otherwise the structure is the same.

## Why this works

Six months from now, "what shaped 2026-05-24" is answered in a 50-line
log rather than replayed transcripts. The cost of writing the log is
~10 minutes; the cost of reconstructing the context without one is
hours and frequently impossible.
