---
type: session_log
status: archived
workstream: null
tags: [prompts, scaffolds, lint-extension, conventions]
---

# 2026-05-24 — prompts/ scaffolding bootstrap

PR [#1](https://github.com/SolutionSmith-debug/its-blueprint/pull/1)
squash-merged as commit
[`42ac7e0`](https://github.com/SolutionSmith-debug/its-blueprint/commit/42ac7e0).
Four-part verify clean (see Verification below).

## Purpose

Land the `prompts/` directory holding orchestration scaffolds —
meta-prompts used by chat or operator to direct Claude Code.
Distinct from execution-repo `its/prompts/`, which holds runtime
prompts called by Python at API time. The blueprint repo now carries
two prompt corpora with deliberately different shapes: runtime prompts
(execution repo, schema-driven, called via API) and orchestration
scaffolds (this repo, prose-driven, copied by humans into chat).

## Pre-flight findings

Working tree had one untracked file from the prior turn —
`session-logs/2026-05-24_initial-migration.md` (the bootstrap session
log drafted but not yet committed). Resolved by committing directly to
main as `0af23be` before starting the feature branch. Lints were
already clean across 36 files including the uncommitted log.

## Decisions made

### 1. `_example.md` ships as scaffold #1, not as a hidden template

The `_` prefix flags it as a template rather than an active scaffold,
but it lives alongside the others (not in `_templates/`). Rationale:
keeps the index complete; future contributors find the template by
listing the scaffold directory rather than hunting through a separate
templates subtree. The lint check tolerates the leading underscore
because the filename-slug check only rejects double-underscores.

### 2. Snippets are pull-when-needed, not pushed upfront

Only `invariant-restatement.md` lands in `snippets/` despite the
brief listing the directory. Per `prompts/README.md`: snippets get
extracted when a fragment is used by ≥2 scaffolds, not invented
upfront. The invariant restatement qualifies because it's referenced
by both `cc-implementation.md` and `new-workstream.md`. The
"PR-merge verify block" was considered for extraction but lives only
in `pr-merge-verify.md` so far — defer until a second consumer
appears.

### 3. Scaffold frontmatter is a new canonical schema, not a doctrine reuse

Scaffolds use `name` + `version` + `audience` + `usage_count` rather
than the existing doctrine schema (`status` + `workstream` +
`last_verified` + `last_verified_against`). Reason: scaffolds aren't
canonical doctrine; they're tools with a different lifecycle. They
don't get "verified against" an execution-repo SHA; they get used,
revised, and counted. Lint changes gate the doctrine fields off for
`SCAFFOLD_TYPES` rather than reusing them with weak semantics.

### 4. Lint extension lands in the same PR as the scaffold files

The brief flagged this explicitly as an anti-pattern to avoid
splitting. Confirmed: a PR landing the files without the lint
extension would fail CI on its own commit (`type=scaffold` not in
canonical set). Bundle is correct.

## Doc changes

| File | Change |
|---|---|
| `prompts/README.md` | New — directory entry + scaffold/snippet index tables |
| `prompts/scaffold/_example.md` | New — copy-this template |
| `prompts/scaffold/cc-implementation.md` | New — highest-volume scaffold |
| `prompts/scaffold/session-orientation.md` | New — fresh-session load order |
| `prompts/scaffold/forensic-audit.md` | New — repo-audit pattern (`usage_count: 1` — already used) |
| `prompts/scaffold/pr-merge-verify.md` | New — four-part landed-verify discipline |
| `prompts/scaffold/doctrine-revision.md` | New — doctrine v-bump procedure |
| `prompts/scaffold/session-log.md` | New — session log shape (this log is the example) |
| `prompts/scaffold/new-workstream.md` | New — workstream bootstrap sequence |
| `prompts/snippets/invariant-restatement.md` | New — reusable invariant block |
| `CONVENTIONS.md` | New "Prompt Scaffolds" section + `scaffold`/`snippet` in canonical types |
| `CLAUDE.md` | New row in "What lives where" pointing at `prompts/` |
| `README.md` | New bullet in "Directory layout" for `prompts/` |
| `scripts/lint_frontmatter.py` | `SCAFFOLD_TYPES` gate added; scaffold-specific fields (`name`, `audience`, `usage_count`) enforced; `status`/`workstream` checks gated to non-scaffold types; `version` requirement extended to scaffolds |

## Verification

| Stage | Result |
|---|---|
| `python scripts/lint_frontmatter.py` | clean (46 files; was 36) |
| `python scripts/lint_crossrefs.py` | clean (46 files) |
| PR #1 CI (push + pull_request triggers) | both `lint` runs SUCCESS |
| PR state triplet | `state=MERGED`, `mergedAt=2026-05-24T13:50:15Z`, `mergeCommit.oid=42ac7e0…` |
| Main-branch CI on merge commit | SUCCESS |

Brief expected 47 files; actual is 46. The brief's file list (8
scaffolds + 1 snippet + 1 README) sums to 10 added, not 11. Verified
by re-counting the brief's enumerated files. Off-by-one in the brief's
predicted total, not in the file list.

## Out of scope

- **Execution-repo `its/prompts/`** — untouched per the brief. Different
  directory, different semantics.
- **CHANGELOG-style version-bump workflow** — deferred until a second
  or third substantive scaffold revision happens organically.
- **Snippets beyond `invariant-restatement.md`** — extracted on
  demand, not invented upfront.
- **`usage_count` bump tooling** — the field is monotonic and updated
  manually; no automation yet.
- **Cross-repo links** — the scaffolds reference both blueprint and
  execution-repo paths, but the cross-ref linter only walks
  intra-repo links. External GitHub URLs in markdown are not
  validated (and don't need to be — they'd require network access
  and aren't load-bearing for repo integrity).

## Sequencing context

This PR unblocks:

- **Chat sessions writing CC implementation briefs** can now reference
  `prompts/scaffold/cc-implementation.md` as the canonical shape
  rather than re-inventing per-session.
- **Doctrine revisions** have a documented procedure in
  `prompts/scaffold/doctrine-revision.md` — the next FM/Op Stds v-bump
  follows it.
- **New workstream bootstraps** (next likely: nothing currently
  imminent; Phase 2 POs/Subcontracts pre-2026-06) have a documented
  sequence in `prompts/scaffold/new-workstream.md`.

Prereqs absorbed:
- Initial migration (commit `3e7f967`) established the doctrine
  baseline these scaffolds reference.
- The `pr-merge-verify.md` scaffold codifies the four-part discipline
  from `its/docs/operations/pr_merge_discipline.md` (PR #74 in `its`).

Follow-ons noted but not queued:

1. **Cross-references inside scaffolds are prose-form** — e.g., "see
   `snippets/invariant-restatement.md`" rather than a markdown link.
   The cross-ref linter passes because nothing's broken, but
   converting prose → clickable links is a quality follow-on.
2. **Project-knowledge re-upload** — the new `prompts/` files should
   be added to the Claude.ai project knowledge so chat sessions
   benefit from them directly. Operator browser action; not a CLI
   step. Same workflow as the initial migration's project-knowledge
   swap.
3. **`usage_count` bump discipline** — first scaffold to bump
   `usage_count` from 0 establishes the convention. `forensic-audit`
   ships at `usage_count: 1` because it was already used in this
   session (the handoff-readiness audit immediately preceding this
   PR).

## Cross-references

- Initial-migration session log:
  [`session-logs/2026-05-24_initial-migration.md`](2026-05-24_initial-migration.md)
- PR: https://github.com/SolutionSmith-debug/its-blueprint/pull/1
- Merge commit:
  https://github.com/SolutionSmith-debug/its-blueprint/commit/42ac7e0
