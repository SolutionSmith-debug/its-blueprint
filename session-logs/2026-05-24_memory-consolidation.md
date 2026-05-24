---
type: session_log
status: archived
workstream: null
tags: [memory, consolidation, structural-guidance]
---

# 2026-05-24 — Memory consolidation: 30 → 15 entries

## Purpose

Consolidate Claude.ai memory from 30 entries (at cap) to 15 entries
focused on structural navigation and hard-fought rule enforcement.
Retire nuance/contextual/historical entries that duplicated content
better captured in the its-blueprint repo, git history, or
execution-repo state.

## Pre-flight findings

Memory hit the 30-entry cap during the same session that big-bang
migrated the .docx forest to markdown. With doctrine now properly
captured in the repo with stable filenames + frontmatter + cross-ref
linter, much of the in-memory doctrine restatement became redundant.
The 30-entry budget shifted from "we don't have room" to "we have too
much signal-loss."

## Decisions made

- **Decision**: Slim doctrine-restating entries to pointers ("X lives in
  doctrine/Y.md §Z; rule is W").
  - **Alternative considered**: Keep full doctrine restated in memory
    as defense-in-depth.
  - **Rationale**: Doctrine drift was the original failure mode the
    memory entries were trying to prevent. With doctrine now
    version-controlled and lint-enforced in its-blueprint, the canonical
    source is reliable. Memory becomes navigation, not duplication.

- **Decision**: Retire all point-in-time operational entries (folder IDs,
  sheet IDs, recipient lists, PR cascade ship dates).
  - **Alternative considered**: Compress them into one combined entry.
  - **Rationale**: These items live authoritatively in code
    (shared/defaults.py, shared/sheet_ids.py), in Smartsheet config, or
    in git log + session logs. Memory carrying them duplicates with
    drift risk.

- **Decision**: Keep the four hard-fought behavioral rules verbatim
  (verify-before-fix, four-part PR verify, operator workflow,
  preservation-over-refactor).
  - **Alternative considered**: Slim these to pointers too.
  - **Rationale**: These are mistake-prevention rules. Each has a
    documented violation history (PR #34 ghost, PR #68 propagation,
    Path A/B violation 2026-05-22, F841 stylistic debate). The full
    statement in memory is the enforcement mechanism — pointing at
    doctrine for a behavioral rule risks the rule not firing when
    chat is mid-action.

- **Decision**: Append §G6 to references/memory-archive.md capturing
  the Ezra email typo before retiring its memory entry.
  - **Alternative considered**: Delete the memory entry outright;
    rely on operator memory to catch the typo.
  - **Rationale**: The typo affects multiple workstreams (mirror tenant
    aliases, ITS_Config recipients, any doc referencing Ezra). Capturing
    it in the §G* archive preserves the knowledge for future chat
    sessions that might draft contact-related artifacts.

## Memory operations executed

- **3 replaces** (in-place at lines 2, 4, 14): slimmed doctrine-restating
  entries to pointers + canonical examples.
- **15 removes** (high-to-low line numbers to prevent index shift):
  Pre-Customer-1 hardening progress, bootstrap drift cleanup, heartbeat
  ARCH refinements, ITS_Daemon_Health IDs, polling-daemon doctrine,
  Bradley 1 demo-complete, CC auto-mode observation, ITS_Config
  recipients filled, Box canonical state (PR #75), R3 session 1,
  2026-05-23 EOD repo state, 2026-05-22 cascade SHIPPED, 5-workspace
  topology, Managed Agents Phase 3 framing, Ezra typo.

Final state: 15 entries.

## Doc changes (this PR)

- Appended §G6 to `references/memory-archive.md` (Contacts Data Quality)
- Created `session-logs/2026-05-24_memory-consolidation.md` (this file)

## Verification

- `python scripts/lint_frontmatter.py` → clean (48 files)
- `python scripts/lint_crossrefs.py` → clean (48 files)

## Out of scope

- Did NOT modify any other memory-archive section.
- Did NOT modify any doctrine doc.
- Did NOT change the lint scripts or CI.
- Did NOT touch execution-repo files.

## Sequencing context

This is the final cleanup PR for the 2026-05-24 work cluster (.docx
migration → prompts/ scaffolding → memory consolidation). After this
lands, the planning-layer foundation is structurally clean for the
next phase of work.

## Cross-references

- Related PRs: its-blueprint PR #1 (prompts/ scaffolding), this PR (#2)
- Memory state snapshot: 15 entries post-consolidation (final list
  available via memory_user_edits view in any future chat)
