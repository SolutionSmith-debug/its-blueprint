---
type: session_log
status: archived
workstream: null
tags: [scaffold-pass, prompts, cc-tooling, shared-module-migration, manual-smoke, cc-implementation]
---

# 2026-05-25 — Scaffold pass: two new scaffolds + cc-implementation v2

## Purpose

Operationalize Op Stds v13 §42 with the scaffolds that turn the discipline into a paste-ready CC workflow. Adds `prompts/scaffold/shared-module-migration.md` (the brief-shape proven by its PR #88), adds `prompts/scaffold/manual-smoke.md` (the operator-side, zsh-paste-safe, post-CC pre-merge verification procedure proven by the same PR's operator smoke), and revises `prompts/scaffold/cc-implementation.md` v1 → v2 folding in three lessons from today's session (line-number re-grep, real-API-signature verify, manual-smoke callout). PR 2 of the 2026-05-25 doctrine + scaffold cascade.

## Pre-flight findings

Repo state pre-edit: clean main, last commit `3525dd6` (PR #12 — Op Stds v13). PR 1 of this cascade landed cleanly (four-part verify clean, tag `operational-standards-v13` pushed).

Verified at pre-flight:

- `python3 scripts/lint_frontmatter.py` → clean (58 files; PR #12 added 1 vs the 57-file baseline).
- `python3 scripts/lint_crossrefs.py` → clean (58 files).
- `prompts/scaffold/shared-module-migration.md` does not exist. ✓
- `prompts/scaffold/manual-smoke.md` does not exist. ✓
- `prompts/scaffold/cc-implementation.md` exists at `version: 1`, `usage_count: 0`. ✓
- `prompts/README.md` Scaffold index table has 8 rows (the brief's assertion). ✓

## Decisions made

- **Decision**: Two new scaffolds rather than one combined.
  - **Alternative considered**: Single combined `shared-module-migration-with-smoke.md` covering both the brief-shape and the operator-smoke procedure.
  - **Rationale**: They're separate concerns. `shared-module-migration` is the chat-to-CC brief shape (when chat writes the brief). `manual-smoke` is the chat-to-operator + operator-to-chat verification shape (when operator validates pre-merge). Different audiences; different lifecycle (brief used once per PR; smoke procedure adapts to each daemon/state-file). Keeping them separate also lets `cc-implementation.md` v2 reference `manual-smoke.md` without dragging the migration brief into every PR that touches state.

- **Decision**: `cc-implementation.md` v1 → v2 as in-place revision rather than v1-archived + v2-new.
  - **Alternative considered**: Archive v1 as `cc-implementation-v1.md` and add `cc-implementation-v2.md` as the new active scaffold.
  - **Rationale**: Established scaffold convention (per `prompts/README.md`): `version` is a frontmatter field, `usage_count` bumps on substantive revision. Versions live in frontmatter, not filenames. Filenames are stable so cross-references from session logs and other scaffolds (`session-log.md` already references `cc-implementation.md` by name) don't break on revision. The v1 → v2 lift in this PR is substantive (three new sections, two new anti-patterns) but is still recognizably the same scaffold.

- **Decision**: `usage_count: 1` on the two new scaffolds (not 0).
  - **Alternative considered**: Ship at `usage_count: 0` since they haven't yet been referenced in a paste-ready brief.
  - **Rationale**: Both scaffolds are extracted from real PRs already shipped — `shared-module-migration.md` codifies the shape used by its PR #88 (state_io); `manual-smoke.md` codifies the procedure used by its PR #88's operator smoke. The first "use" is this extraction; that's a legitimate count of 1, not 0. The 0 → 1 bump on substantive revision/use convention applies; the initial ship is a use.

- **Decision**: `cc-implementation.md` v2 at `usage_count: 6`.
  - **Alternative considered**: Set to 1 (this revision) or 2 (today's revision + initial v1 ship).
  - **Rationale**: The artifact explicitly specified 6: "today's session use + at least five prior implicit uses since the initial migration." The five prior uses are the implementation briefs for its PR #74 (conftest fix), #78 (doctrine refs), #82 (post-merge checkout-main), #85 (workflow permissions), #88 (state_io). Today's session (PR #88 + #89) is the sixth. The brief's count is grounded in real history, not arbitrary.

- **Decision**: No snippet extraction in this PR.
  - **Alternative considered**: Extract shared fragments (e.g., the four-part verify reference, the §42 docstring callout) into `prompts/snippets/`.
  - **Rationale**: Per `prompts/README.md` convention: "Snippets get extracted when used by 2+ scaffolds, not invented upfront." This PR's two new scaffolds don't share verbatim fragments with existing scaffolds; the references to `pr-merge-verify.md` and the §42-docstring callout are short enough that the cost of a snippet (file overhead + indirection) exceeds the cost of duplication. Revisit if a third scaffold lands that references the same fragments verbatim.

- **Decision**: No `usage_count` bumps on scaffolds other than `cc-implementation.md`.
  - **Alternative considered**: Bump `doctrine-revision.md` (used by PR #12 this session) and `session-log.md` (used by both this PR's session log and PR #12's).
  - **Rationale**: Per the brief's explicit instruction: "DO NOT bump usage_count on scaffolds not modified in this PR." Their next substantive revision is when they re-baseline. This keeps the PR scoped tightly to the announced changes.

- **Decision**: Did not modify `prompts/snippets/invariant-restatement.md`.
  - **Alternative considered**: Add the §42 docstring callout to the snippet so it propagates wherever the invariant-restatement is used.
  - **Rationale**: The invariant-restatement is about Foundation Mission invariants 1 & 2 (External Send Gate, Adversarial Input Handling). The §42 docstring is a separate concern (code-level self-documentation, not invariant restatement). Conflating them dilutes both. The §42 callout lives in `cc-implementation.md`'s template under its own heading.

## Doc changes (this PR)

- New `prompts/scaffold/shared-module-migration.md` — full scaffold per artifact 02. Six-step pattern (callsite identification → helper signature → helper + tests first → consumer migration → docs/doctrine updates → manual-smoke + four-part verify). Template skeleton + "Why this works" section.
- New `prompts/scaffold/manual-smoke.md` — full scaffold per artifact 03. Three-batch zsh-paste-safe template (setup + before-snapshot → invoke + per-script verify → cross-consumer integration + cleanup). Standard 7-assertion checklist (+ 8th for multi-consumer state files). Failure-handling rubric distinguishing non-blocking causes (pre-existing gaps, empty cycle paths) from blocking ones (non-zero exit, invalid state file, tmp residue, broken sidecar lock, F23 clobber).
- Revised `prompts/scaffold/cc-implementation.md` v1 → v2 per artifact 04:
  - Frontmatter `version` 1 → 2; `usage_count` 0 → 6.
  - New `v1 → v2 changes (2026-05-25)` section near the top.
  - New `When to use a different scaffold` section pointing to `shared-module-migration.md` / `doctrine-revision.md` / `new-workstream.md`.
  - New "Pre-flight: verify baseline + brief assertions" template section with explicit re-verify list (line numbers, API signatures, existence claims, broken-claim reproductions).
  - New `API signatures referenced` template section with `error_log.log(severity, script_name, msg, error_code=...)` example signature.
  - New `§42 self-documentation requirements` template section.
  - `Verification gates` extended with the manual-smoke conditional callout.
  - `Done when` extended with operator-manual-smoke gate.
  - `Anti-patterns to avoid` extended with two new bullets: re-verification at pre-flight, surface API-signature mismatches.
  - "Why this works" extended from 5 properties to 7 (v2 adds two).
- Edited `prompts/README.md` — Scaffold index extended with two new rows: `shared-module-migration.md` (after `cc-implementation.md`) and `manual-smoke.md` (after `new-workstream.md`). 8 rows → 10 rows. Snippet table unchanged.
- New `session-logs/2026-05-25_scaffold-pass.md` (this file).

## Verification

- `python3 scripts/lint_frontmatter.py` → clean (61 files at PR-completion; +3 vs PR 1 baseline = 2 new scaffolds + this session log).
- `python3 scripts/lint_crossrefs.py` → clean (61 files).

## Out of scope

- Bumping `usage_count` on scaffolds not modified in this PR (`doctrine-revision.md`, `session-log.md`, etc.). They bump on their next substantive revision.
- Extracting new snippets to `prompts/snippets/`. The two new scaffolds don't share verbatim fragments with existing scaffolds. Revisit when a third reference accumulates.
- Doctrine changes. PR 1 (Op Stds v13 with §42) is the doctrine half of this cascade.
- Execution-repo cascade. The `its` repo's `CLAUDE.md` may want a forward reference to Op Stds §42 at the next docs-touching execution-repo PR; folds into that PR's scope rather than spawning a third PR today.
- `references/memory-archive.md` §G8. N/A this cluster; operational detail is captured in session logs in both repos.

## Sequencing context

- **Prerequisite (landed)**: PR #12 (Op Stds v13, merge commit `3525dd6`). PR 2 references PR #12's merge commit in its pre-flight assertions.
- **This PR (PR 2 of the 2026-05-25 cascade)**: scaffold pass — two new scaffolds + `cc-implementation.md` v2 + README index.
- **Next (separate cascade)**: F02 / F07 / F13 / F20 doctrine reconciliation from `audits/2026-05-25_forensic-audit.md`. Distinct cascade; not blocked by this one.
- **Carry-forward (separate cluster)**: PR 2 of the Phase 1.4 hardening cluster (`its`-side `shared/alert_dedupe.py` migration to use `state_io` helpers). Different repo, different cluster.

## Cross-references

- Doctrine: `doctrine/operational-standards.md` v13 (PR #12, merge commit `3525dd6`).
- Sibling session log: `session-logs/2026-05-25_op-stds-v13-revision.md` (PR 1 of this cascade).
- Predecessor execution-repo PRs:
  - its PR #88 — `shared/state_io.py` (atomic-write + sidecar lock). The shape captured by `shared-module-migration.md`. Merge commit `36932bd`. Session log: https://github.com/SolutionSmith-debug/its/blob/main/docs/session_logs/2026-05-25_state-io-atomic-write.md
  - its PR #89 — session log + gh CLI gotcha. The discipline captured by `cc-implementation.md` v2's "Why this works" property #6. Merge commit `a1dc227`.
- Cascade precedent: 2026-05-24 v11 → v12 doctrine (PR #4 `74ee6f8`) + downstream `references/customer-fork-setup-checklist.md` (PR #5 `5f80ff8`) — same two-PR cascade pattern this session repeats.
- Existing scaffold infrastructure: `session-logs/2026-05-24_prompts-scaffolding.md` (the initial scaffold infrastructure PR in this blueprint repo).
