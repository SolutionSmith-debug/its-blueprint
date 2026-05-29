---
type: reference
status: canonical
workstream: null
last_verified: 2026-05-29
last_verified_against: 7fbb1cd
---

# Worktree Discipline (blueprint)

The blueprint repo's view of the parallel-session worktree discipline. The
execution-repo side — including the `import`-path / `PYTHONPATH` rules that
only apply to Python — is the canonical companion at
[`its/docs/operations/worktree_discipline.md`](https://github.com/SolutionSmith-debug/its/blob/main/docs/operations/worktree_discipline.md);
this doc is the blueprint half it points to.

## Why the blueprint needs this

The blueprint is markdown-native (doctrine, missions, references, scaffolds) —
there is **no venv / `PYTHONPATH` concern** here. But it has the **same
checkout-collision hazard** as the execution repo, and until 2026-05-29 it ran
as a single shared checkout. On that day two doctrine-touching sessions layered
edits onto the one `~/its-blueprint` working tree; the collision was avoided
only because the second session *noticed* and refused to stash over the first
(the work landed as PRs #23 → #24 → #25 in sequence). Nothing structural
prevented it. This doc closes that gap.

A `git worktree` gives each concurrent task its own working directory **and**
its own branch, all backed by the same `.git` object store. Sessions never see
each other's uncommitted files.

## The pattern

For any task that edits blueprint doctrine, references, or scaffolds, work from
a dedicated worktree created as a `~/`-level sibling:

```bash
git -C ~/its-blueprint fetch origin
git -C ~/its-blueprint worktree add ~/its-blueprint-<task> -b <branch> origin/main
#   cd ~/its-blueprint-<task> && claude
```

**Rule: never run two doctrine-touching sessions against the same blueprint
checkout.** Each doctrine/reference/scaffold-editing session gets its own
blueprint worktree — or it waits (see [Serialization fallback](#serialization-fallback)).

No `PYTHONPATH` step is needed — the blueprint has no importable code, so the
editable-install import gotcha that the execution-repo doc warns about does not
apply here.

## The load-bearing `~/`-sibling assumption (fail-open — read this)

`~/its-blueprint/.claude/agents` and `.../hooks` are committed **relative
symlinks** into `../../its/.claude/{agents,hooks}` — a single source of truth
shared with the execution repo (there are no duplicate copies to drift). They
resolve correctly **only when `~/its-blueprint` sits as a `~/`-level sibling of
`~/its`.** A blueprint worktree placed as a sibling (`~/its-blueprint-<task>`)
resolves correctly.

But the symlink **fails OPEN**, not closed:

- A **non-sibling** worktree location, or a **clone of the blueprint alone** (a
  CI runner, a fresh machine without `~/its` beside it), leaves the symlinks
  **dangling**.
- When they dangle, Claude Code finds **zero agents**, and because the three
  propose-only PreToolUse guard hooks (`block-codeql-dismiss`,
  `block-doc-reconciliation-write`, `block-doctrine-write`) are wired through
  those same symlinked paths, **the guard hooks silently disappear** — with
  **no error**.

This is a fail-*open*, not fail-closed: the structural backstops that exist
precisely so a misfire can't silently dismiss a CodeQL alert, rewrite doctrine,
or edit during a reconciliation pass would be *absent and unannounced*. So:

- **Keep blueprint worktrees as `~/`-level siblings of `~/its`.**
- **Do not assume the agent/hook guards are present** in a bare blueprint clone
  or a non-sibling checkout. Verify before trusting them:

  ```bash
  test -d ~/its-blueprint/.claude/agents \
    && echo "agents resolve — guards present" \
    || echo "DANGLING — zero agents, guard hooks silently absent"
  ```

- **Do not "fix" this by de-symlinking.** The single-source-of-truth property
  (one copy of each agent/hook, shared with `~/its`) is worth keeping; the
  fail-open is a documentation/awareness issue, not a topology bug.

A small **resolve health-check** — a `SessionStart` notice or a watchdog/CI
line that asserts the symlink resolves and warns loudly if it dangles — is
**recommended but deliberately deferred** to operator decision; it is **not
built here**. The full residual-risk analysis (clone fail-open, working-tree
branch coupling, the unguarded `settings.json` copy) is in the
[2026-05-29 agent/workflow audit](https://github.com/SolutionSmith-debug/its/blob/main/docs/audits/2026-05-29_agent-workflow-audit.md).

A second consequence of the symlink: it targets the `~/its` **working tree**,
not a pinned ref — so the agent registry a blueprint session sees is whatever
branch `~/its` is currently checked out on. Keep `~/its` on `main` between
tasks, or blueprint sessions silently load off-main agent definitions.

## Cleanup (operator action — by design)

When a task's worktree is done and its branch is merged:

```bash
git -C ~/its-blueprint worktree remove ~/its-blueprint-<task> --force \
  && git -C ~/its-blueprint branch -D <branch> \
  && git -C ~/its-blueprint worktree prune
```

`--force` (on `worktree remove`) and `-D` (force branch delete) are required: a
squash-merged branch isn't recognized as "merged" by safe-delete `-d`, and the
worktree may hold a now-empty index. **These commands are blocked by the
`block-dangerous-git.sh` PreToolUse hook from inside a CC session** — so
worktree cleanup is an **operator action run in a normal shell**, not something
a CC session performs. (This is the direct reason stale worktrees accumulate:
the sessions that created them cannot remove them.)

## Serialization fallback

If you'd rather not manage worktrees for a burst of work, the fallback is
strict serialization:

> **One blueprint session at a time. Land (merge) before starting the next.**

This trades parallelism for simplicity and is the right call when tasks are
quick and sequential. What you must **not** do is run two sessions against one
shared blueprint checkout — that is the collision this doc exists to prevent.

## Cross-references

- [`its/docs/operations/worktree_discipline.md`](https://github.com/SolutionSmith-debug/its/blob/main/docs/operations/worktree_discipline.md)
  — the execution-repo companion (the daemon-reads-working-tree hazard, the
  `PYTHONPATH` / editable-install import rule, the validation gates).
- [2026-05-29 agent/workflow audit](https://github.com/SolutionSmith-debug/its/blob/main/docs/audits/2026-05-29_agent-workflow-audit.md)
  — findings H1 (symlink fail-open) and H4 (no hook can catch the collision),
  plus the full residual-risk analysis (Appendix A/B).
