---
type: scaffold
name: doctrine-revision
version: 1
audience: chat
usage_count: 0
---

# Doctrine Revision

For chat (planning side) revising a doctrine doc in the its-blueprint
repo. Doctrine changes have their own discipline because they're
load-bearing for every downstream decision; this scaffold codifies the
discipline.

## When to revise (v-bump) vs. extend (no v-bump)

**Revise** — substantive change to invariants, enforcement patterns,
phase gates, or operational standards sections. New defense layer; new
mandatory section; new criterion for a phase gate.

**Extend** — clarification of existing intent, typo fixes, cross-reference
updates, adding examples that don't change the rule. Frontmatter
`last_verified` bumps; version does not.

When in doubt: bump. The cost of an unnecessary bump is one tag; the
cost of a missed bump is downstream docs treating a substantive change
as cosmetic.

## Procedure

1. Decide: revise or extend.
2. Edit the doc in-place. Filename never changes.
3. If revising:
   - Bump `version` in frontmatter (integer +1).
   - Add `supersedes: doctrine/{name}.md@v{N-1}` to frontmatter.
   - Add an entry to the doc's "Change log" section (create if missing
     at the bottom of the doc).
4. If extending:
   - Don't bump `version`.
   - Update `last_verified` to today's date.
   - Update `last_verified_against` to current `its` repo HEAD SHA.
5. Run both linters:

   ```bash
   cd ~/its-blueprint
   python scripts/lint_frontmatter.py
   python scripts/lint_crossrefs.py
   ```

6. Commit with message `doctrine: {doc} v{N} — {one-line change summary}`.
7. Push to main.
8. If revising: tag the canonical commit.

   ```bash
   git tag {doc-slug}-v{N}
   git push --tags
   ```

9. Write a session log at
   `session-logs/YYYY-MM-DD_{doc}-v{N}-revision.md` capturing what
   changed and why.
10. In the session log, note any downstream docs that need follow-on
    updates (workstream briefs, references, execution-repo CLAUDE.md).

## What NOT to do

- DO NOT create a new file like `foundation-mission-v9.md`. Filenames
  are stable; versions live in frontmatter.
- DO NOT bump versions without changing the body. A v-bump with no
  substantive change is noise that wastes future audit cycles.
- DO NOT update doctrine without a session log. Future maintainers need
  the "why" trail.
- DO NOT cascade-update downstream docs in the same PR as the doctrine
  bump. Land the doctrine bump first, validate it absorbed cleanly,
  then sweep downstream in a separate PR.

## Why this works

Stable filenames + frontmatter versions + git tags = a doc can be
referenced at a specific version (via the tag) without breaking forward
links. The "no cascade in same PR" rule prevents the failure mode where
a doctrine bump and seven downstream updates land together, and any
issue with the doctrine bump requires reverting the whole bundle.
