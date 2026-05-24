---
type: session_log
status: archived
workstream: null
tags: [migration, bootstrap, doctrine, retirement-registry]
---

# 2026-05-24 — Initial migration: .docx corpus → markdown blueprint

Initial commit `3e7f967` on `main`. Repo
[`SolutionSmith-debug/its-blueprint`](https://github.com/SolutionSmith-debug/its-blueprint)
created private; CI green on first push (`lint` workflow, 11s).

This is the first session log in this repo and the bootstrap event itself.
The planning-side doc corpus moved from `.docx` attachments in the
Claude.ai project to canonical markdown in a dedicated GitHub repo. 35
markdown files landed in one big-bang commit alongside scaffolding (CI,
lint scripts, retirement registry).

## Purpose

Two structural problems with the prior `.docx`-in-project-knowledge
arrangement justified the move:

1. **No diff surface.** A `.docx` substitution loses the change. Doctrine
   v-bumps were tracked in prose preamble inside each doc rather than in
   anything queryable.
2. **No cross-ref enforcement.** "See Foundation Mission v8 §X" was a
   string that drifted whenever a section number changed. Nothing
   caught the drift until a chat session tried to follow the reference.

Markdown + git + lint scripts close both gaps. Doctrine versions are
git tags; cross-refs are markdown links the linter walks.

## Non-obvious decisions captured here

These were settled in planning conversation prior to the migration
session itself; the rationale belongs in the log because the doc diff
doesn't carry it.

### 1. Big-bang migration, not workstream-by-workstream

35 files in one commit. The alternative — migrate doctrine first, then
each workstream as a separate PR — was rejected because cross-references
between docs would be broken during the staggered period (a `mission.md`
linking back to `foundation-mission.md` only works once both exist).
Big-bang means the cross-ref linter passes from commit 1.

**Carveout for future migrations:** this exemption is specific to the
bootstrap event. Subsequent doc changes follow narrow-PR discipline
(one workstream's mission revision = one PR).

### 2. Separate repo, not subdirectory of `its`

`its-blueprint` ships as its own private repo rather than
`its/blueprint/`. Rationale: the execution repo is **Customer-0-specific
Python**; the blueprint is **customer-agnostic doctrine**. They have
different change cadences (doctrine is stable; execution is active) and
will diverge further when Customer 2 forks the execution layer. Keeping
them separate now avoids a future surgical split.

### 3. Retirement registry, not deletion-by-omission

19 docs from the `.docx` corpus are not migrating. Rather than silently
dropping them, `archive/README.md` lists each retired doc with rationale
and a pointer to what supersedes it. Categories:

- 6 Cascade Unification Updates → git log replaces them
- 2 Cascade Audit Errata → absorbed into doctrine
- 2 Cascade Implementation Checklists → execution-repo PR history
- 5 Session Updates + Comprehensive Syntheses → execution-repo session logs
- 3 operational point-in-time docs → absorbed into doctrine / memory-archive
- 1 already-markdown cluster wrap → absorbed

The Claude.ai project knowledge still holds the original `.docx` files
indefinitely; the retirement registry is the index back into them if a
future question needs that content.

### 4. Lint-from-day-one, lazy retrofit elsewhere

`scripts/lint_frontmatter.py` + `scripts/lint_crossrefs.py` ship at
commit 1 and run warn-only in CI. Both pass clean on all 35 files at
migration time. The lazy-retrofit policy applies only to future
grandfathering decisions (none yet); the bootstrap corpus is conformant.

### 5. Doctrine git tags as canonical-state markers

Six tags pushed alongside the initial commit:

- `foundation-mission-v8`
- `operational-standards-v11`
- `vision-and-roadmap-v7.2`
- `handover-plan-v6.3`
- `excellence-roadmap-v2.3`
- `memory-archive-v5`

The version lives in frontmatter; the tag is the immutable pointer at
that canonical commit. Future v-bumps bump the frontmatter `version`
field in the same filename and add a new tag (e.g.,
`foundation-mission-v9`).

## What landed

```
its-blueprint/  (35 .md files + scaffolding)
├── doctrine/                  5 canonical invariant docs
├── workstreams/               5 workstream pairs (mission + brief = 10)
├── references/                7 evergreen docs (memory-archive v4+v5 merged)
├── audits/                    3 forensic snapshots
├── archive/README.md          retirement registry only (no docs in-tree)
├── session-logs/              empty except for README + this log
├── scripts/                   lint_frontmatter, lint_crossrefs, render_handoff_packet
├── .github/workflows/lint.yml CI: both linters on every push
├── README.md, CLAUDE.md, CONVENTIONS.md
└── .editorconfig, .gitignore
```

## Verification

| Stage | Result |
|---|---|
| `python scripts/lint_frontmatter.py` | clean (35 files) |
| `python scripts/lint_crossrefs.py` | clean (35 files) |
| GitHub Actions `lint` on push to main | SUCCESS in 11s |
| 6 doctrine tags pushed | all visible at `refs/tags/` |

## Deviations from HANDOFF.md

**One.** HANDOFF.md Step 2 specified
`git remote add origin git@github.com:SolutionSmith-debug/its-blueprint.git`
(SSH). The operator's `gh` is configured for HTTPS and no SSH key is
registered on this MacBook — SSH push failed with
`Host key verification failed`. Remote was switched to
`https://github.com/SolutionSmith-debug/its-blueprint.git`; `gh`'s
stored token authenticates the push. Future operations work over HTTPS
without setup. Adding an SSH key remains optional, not required.

## Known follow-ons (not blockers, from HANDOFF.md)

1. **Re-upload to Claude.ai project knowledge.** Recommended Option A —
   retire `.docx` files in the project, upload the new `.md` files in
   their place. Cleanest going forward. Operator action; not a CLI step.
2. **Doctrine docs include legacy preamble text** from the `.docx`
   originals (bolded duplicate titles, dated headers). Harmless — H1
   is what GitHub renders. Optional cleanup pass.
3. **Cross-references between migrated docs** are still in prose form
   ("see Foundation Mission v8 §X") rather than clickable markdown
   links. Linter passes because there are no broken links yet, but
   converting prose → links is a meaningful quality follow-on.
4. **Update execution-repo `CLAUDE.md`** to link doctrine references at
   `its-blueprint` rather than referring by version in prose. Low
   priority; not blocking.

## Operator-side actions remaining

1. **Project knowledge swap** (per follow-on 1 above) — browser action
   in the Claude.ai project.
2. **First substantive planning session under the new shape** will
   establish the cadence: chat decision → small PR here → optional
   session log if non-obvious. The current log is itself the example.

## Out-of-scope notes

- **No content changes.** Migration is representational only; the words
  in each doc match the `.docx` source. Editorial cleanup is deferred
  to whenever a doc is next touched for an actual content reason
  (lazy-retrofit policy).
- **No doctrine v-bumps.** All five doctrine docs migrated at their
  current canonical versions; the tags reflect existing state, not new
  state.
- **No new workstreams.** The five workstreams in `workstreams/` match
  the existing roadmap (Safety Reports, Email Triage, POs, Subcontracts,
  AI-Employee Capabilities).
