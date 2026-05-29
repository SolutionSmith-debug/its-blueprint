---
type: scaffold
name: doctrine-revision
version: 2
audience: chat
usage_count: 1
---

# Doctrine Revision

For chat (planning side) revising a doctrine doc in the its-blueprint
repo. Doctrine changes have their own discipline because they're
load-bearing for every downstream decision; this scaffold codifies the
discipline.

## v1 → v2 changes (2026-05-29)

- **New Procedure step: reconcile in-body version self-references after a
  bump** (audit H2). Closes the exact gap that let a v13/v14
  self-contradiction reach canonical doctrine — caught then only by
  adversarial review.
- Step 7 now lands via PR + four-part verify instead of a bare "push to
  main": blueprint `main` is branch-protected (audit C8).

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
   - **Reconcile in-body version self-references.** After the bump, run
     `grep -n "v{N-1}" doctrine/{name}.md` and update every in-body
     self-reference to `v{N}` — or frame it explicitly as superseded
     history. Reconcile in order of how-often-missed: (1) the **Authority
     block** — the #1 miss; it carries a predictive "v{N+1} trigger" line
     and a self-version line that are easy to leave at the old number;
     (2) the "What Changed in v{N}" heading and its cross-refs; (3) any
     companion-doc version pins (`Op Stds vM`, `FM vK`) that *this* bump
     makes current. A doc whose frontmatter says `v{N}` while its body
     still asserts `v{N-1}` is internally contradictory and silently
     authoritative — the exact v13/v14 self-contradiction that reached
     canonical doctrine and was caught only by adversarial review.
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
7. Land via a PR + four-part verify (not a direct push — blueprint `main`
   is branch-protected; same discipline as code-side `pr-merge-verify.md`).
8. If revising: tag the canonical (merge) commit.

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
