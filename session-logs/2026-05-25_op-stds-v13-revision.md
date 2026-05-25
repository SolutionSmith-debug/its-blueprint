---
type: session_log
status: archived
workstream: null
tags: [doctrine-revision, op-stds, code-self-documentation, cc-tooling]
---

# 2026-05-25 — Operational Standards v12 → v13 revision

## Purpose

Codify the code-level self-documentation discipline as Op Stds §42. The discipline (mandatory module docstrings with Purpose / Invariants / Failure modes / Consumers headings on every new `shared/*` module and workstream entrypoint; in-code rationale comments citing the motivating F-finding / session log / doctrine § / PR for any non-obvious decision) had been an emergent convention but kept surfacing as a cost when "future-Seth + future-CC have to leave the file to understand the why." v12 was complete on its own terms; v13 adds the discipline. First PR of the 2026-05-25 doctrine + scaffold cascade; PR 2 (scaffold pass) follows.

## Pre-flight findings

Repo state pre-edit: clean main, last commit `a74215a` (PR #11 brief safety_portal preserved per-form field inventories).

Verified at pre-flight:

- `python3 scripts/lint_frontmatter.py` → clean (57 files).
- `python3 scripts/lint_crossrefs.py` → clean (57 files).
- `doctrine/operational-standards.md` frontmatter at `version: 12`, `last_verified_against: 79eec73`, `supersedes: doctrine/operational-standards.md@v11`. Matches brief assertion.
- `§41 GitHub Actions Version-Bump Discipline` is the last numbered section before the Authority block (line 490). §42 is the next sequential number.
- No `§42` placeholder exists. ✓
- §14 and §30 referenced from §42 prose are carry-forward sections from v10/v10.1 (covered by `# §§4-22 — Carry Forward From v10` at line 118 and `# §25-§30 — Carry Forward From v10` at line 142). They have no individual `# §14` / `# §30` headers in this file, but `lint_crossrefs.py` only validates `[text](path)` markdown links — prose mentions of `§14` / `§30` / `verify-before-fix` don't require anchor resolution. §42 references these by prose only; lint stays clean.

Blocker resolved at pre-flight: the brief referenced five "attached artifacts" (01_op_stds_v13_section_42.md through 05_prompts_readme_index_updates.md) by name; they weren't on the filesystem at session start. Operator dropped them at `~/Downloads/files/` and confirmed the path. Read all five; PR 1 applies artifact 01 only.

## Decisions made

- **Decision**: Apply the artifact's §42 prose verbatim but unwrap it to match the doc's one-paragraph-per-line convention. Bullets separated by blank lines per the §32 / §37 etc. precedent.
  - **Alternative considered**: Preserve the artifact's ~70-char wrap.
  - **Rationale**: Existing §§31–41 use unwrapped paragraphs with blank lines between bullets. Mixing wrap styles inside one doc is the kind of stylistic drift that lint won't catch but a careful reader will. Match the surrounding convention.

- **Decision**: Authority block updates beyond the artifact's "append" instruction.
  - **Alternative considered**: Strictly append the v13-trigger paragraph and leave the v12-current opening sentence alone.
  - **Rationale**: Strict-append leaves "Operational Standards v12, 2026-05-24" as the Authority opening sentence even though the frontmatter says v13 — a self-contradiction. Updated the opening sentence to v13-current and updated the predictive "v13 trigger:" line to "v14 trigger:" (the v13 prediction resolved when v13 happened; the next-version prediction maintains the pattern). The artifact's v13-trigger paragraph appended between the v14 prediction and the Companion line, per the artifact's "append" instruction interpreted as "append within the block."

- **Decision**: Companion line extended rather than replaced.
  - **Alternative considered**: Replace the v12-cascade parentheticals (`(extended §G7 in parallel PR)`, `(downstream cascade in next PR)`) with v13-specific ones; or leave the v12 line unchanged.
  - **Rationale**: The v12-cascade parentheticals are historical context for what was happening at v12-bump time and stay accurate as history. Added an explicit "v13 parallel companion:" clause referencing PR 2 of this cascade (`prompts/scaffold/` — the scaffold-pass PR with `shared-module-migration.md`, `manual-smoke.md`, `cc-implementation.md` v1 → v2). Reader sees both v12 history and v13 forward-reference in one block.

- **Decision**: New tag `code-self-documentation` appended to the existing tag list rather than replacing or reordering.
  - **Alternative considered**: Group the tag with `cc-tooling`.
  - **Rationale**: Tags are append-only in the existing convention. Order is chronological-by-introduction, not topical.

- **Decision**: Did NOT modify the "Memory Archive v5 (extended §G7 in parallel PR)" parenthetical to read "in v12 parallel PR" explicitly.
  - **Alternative considered**: Disambiguate by adding "v12" before "parallel PR".
  - **Rationale**: Actually did add this disambiguation — the parenthetical now reads "extended §G7 in v12 parallel PR" so future readers don't misinterpret "parallel PR" as something happening in v13's cascade.

- **Decision**: No downstream cascade in this PR. PR 2 (scaffold pass) follows separately.
  - **Alternative considered**: Bundle the scaffold pass into this PR.
  - **Rationale**: `prompts/scaffold/doctrine-revision.md` prohibits bundling doctrine bump with cascade. Same precedent as v11 → v12 (which was followed by `customer-fork-setup-checklist.md` as a separate PR). Land doctrine first, validate clean absorption, sweep downstream in PR 2.

## Doc changes (this PR)

- Edited `doctrine/operational-standards.md`:
  - Frontmatter: `version` 12 → 13; `last_verified` 2026-05-24 → 2026-05-25; `last_verified_against` 79eec73 → a1dc227 (its PR #89 merge commit); `supersedes` pointer bumped to v12; `tags` extended with `code-self-documentation`.
  - Subtitle and version-line updated (v12 → v13, new date 2026-05-25, new subtitle "Code-Level Self-Documentation Discipline + Scaffold Pass"); five-new-sections line replaced with one-new-section line.
  - `# What Changed in v13` section inserted between `# What Changed in v12` and `# §1 — Kill Switch`. Three bullet groups: the §42 introduction, the cross-references paragraph (§14 / §30 / verify-before-fix all referenced as prose), and the carry-forward acknowledgment for §§1–41.
  - `# §42 (NEW) — Code-Level Self-Documentation Discipline` inserted between §41 (line 490 area) and `# Authority` (was line 528). Sub-headings: Mandatory module docstrings, In-code rationale comments, When to apply, Interaction with existing doctrine, Enforcement, Example. Nested Python code fences preserve the docstring template + rationale-comment template + state_io.py retrofit example.
  - Authority block: opening sentence rewritten for v13; "v13 trigger" predictive line bumped to "v14 trigger"; v13-trigger paragraph appended after the v14 prediction; Companion line extended with v13 parallel-companion clause.
- New `session-logs/2026-05-25_op-stds-v13-revision.md` (this file).

## Verification

- `python3 scripts/lint_frontmatter.py` → clean (58 files; +1 = this session log).
- `python3 scripts/lint_crossrefs.py` → clean (58 files; §42 introduces no new `[text](path)` links, only prose §-references which the lint correctly ignores).

## Out of scope

- F02 / F07 / F13 / F20 doctrine reconciliation from `audits/2026-05-25_forensic-audit.md` — separate cascade PRs, not this one.
- `references/customer-fork-setup-checklist.md` updates — N/A this PR.
- `references/memory-archive.md` §G8 — N/A this cluster. Operational detail for the 2026-05-25 work (its PR #88, its PR #89, this doctrine bump, the upcoming scaffold-pass PR) is captured in session logs in both repos; §G8 not needed.
- Scaffold pass (`shared-module-migration.md`, `manual-smoke.md`, `cc-implementation.md` v1 → v2, `prompts/README.md` index) — PR 2 of this cascade.
- Execution-repo cascade — N/A from this PR. The execution-repo `CLAUDE.md` may want a forward reference to Op Stds §42 at the next docs-touching execution-repo PR; folds into that PR's scope rather than spawning a third PR.

## Sequencing context

- **Prerequisite (landed)**: its PR #88 (merge commit `36932bd`) + its PR #89 (merge commit `a1dc227`) — the work + session-log discipline that motivated §42. `last_verified_against` points at `a1dc227`.
- **This PR (PR 1 of the 2026-05-25 cascade)**: Op Stds v12 → v13 with §42 added. Tag `operational-standards-v13` pushed post-merge.
- **Next (PR 2 of the cascade)**: scaffold pass at `prompts/scaffold/`. References this PR's merge commit in its pre-flight assertions.
- **Carry-forward**: PR 2 of the Phase 1.4 hardening cluster (its-side `shared/alert_dedupe.py` migration) is a separate cluster from this doctrine cascade; the two clusters do not block each other.

## Cross-references

- Doctrine: `doctrine/operational-standards.md` (this PR; v13).
- Predecessor execution-repo PRs:
  - its PR #88 — atomic-write + sidecar lock (F19 + F23). Merge commit `36932bd`. Session log: https://github.com/SolutionSmith-debug/its/blob/main/docs/session_logs/2026-05-25_state-io-atomic-write.md
  - its PR #89 — session log + gh CLI gotcha (`docs(session_log)` PR pattern, four-part verify discipline extension). Merge commit `a1dc227`.
- Audit: `audits/2026-05-25_forensic-audit.md` — the forensic audit whose broader surface includes F19 / F23 / F02 / F07 / F08 / F09 / F13 / F20 / F22 etc. PR 1 addresses §42 only; other F-findings carry forward to subsequent PRs.
- Cascade precedent: 2026-05-24 v11 → v12 doctrine + downstream (`session-logs/2026-05-24_op-stds-v12-revision.md` + `references/customer-fork-setup-checklist.md`).
- Scaffold guides used: `prompts/scaffold/doctrine-revision.md` (this PR's shape), `prompts/scaffold/session-log.md` (this session log's shape).
