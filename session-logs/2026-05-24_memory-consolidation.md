---
type: session_log
status: archived
workstream: null
tags: [memory, consolidation, rationale-anchor, contacts-data]
---

# 2026-05-24 — Memory consolidation (30 → 15) rationale anchor

This log preserves the consolidation brief verbatim as the canonical "why"
behind the chat-side memory edits, plus captures the cc-side repo work
that landed alongside.

## Execution status (cc side)

Brief was authored against the **Claude.ai chat memory system**
(`memory_user_edits`-style operations, 30-entry cap). That tool isn't
available from this Claude Code session, so the 14 removes + 3 replaces
themselves were not executed here — they happen in the Claude.ai chat
session, with this log as the rationale reference.

The two repo-side deliverables from the brief's "Done when" list **were**
executed here:

| Deliverable | Status | Where |
|---|---|---|
| §G6 added to `references/memory-archive.md` (Contacts Data Quality) | ✅ landed | PR [#2](https://github.com/SolutionSmith-debug/its-blueprint/pull/2), merge commit [`1a07a31`](https://github.com/SolutionSmith-debug/its-blueprint/commit/1a07a31) |
| Brief committed to `session-logs/2026-05-24_memory-consolidation.md` as rationale anchor | ✅ this file | direct commit to main (same pattern as initial-migration + prompts-scaffolding logs) |
| 14 chat-memory removes | ⏸ chat-side | Claude.ai chat session |
| 3 chat-memory replaces | ⏸ chat-side | Claude.ai chat session |
| Final chat-memory state: 15 entries | ⏸ chat-side | Claude.ai chat session |

### PR #2 four-part verify

- pytest: n/a (blueprint repo has no test suite — lint is the verification surface)
- mypy: n/a
- ruff: n/a
- main-branch CI on merge commit: **SUCCESS** (`lint` workflow, commit `1a07a31`)
- Frontmatter lint: clean (47 files)
- Cross-ref lint: clean (47 files)

State triplet: `state=MERGED`, `mergedAt=2026-05-24T14:00:38Z`, `mergeCommit.oid=1a07a31c5c6552f40b2100cdbaaee51c7fa3932f`.

### Scope deviation from brief

The brief framed §G6 + this log under the same "Done when" but didn't specify bundling. cc opted to:

- Land §G6 via a small PR (#2) per the doctrine-revision scaffold's "extend (no v-bump)" criteria — additive change to canonical reference doc, no version bump needed.
- Commit this session log directly to main, matching the established pattern from the initial-migration and prompts-scaffolding logs (planning-side session logs are direct commits, not PRs).

### Note on Claude Code file-based memory

This session's auto-memory (the file-based one at
`/Users/sethsmith/.claude/projects/-Users-sethsmith/memory/`) is a
**different system** from the Claude.ai chat memory the brief consolidates.
The file-based memory currently has 9 entries, most of which are behavioral
rules (preservation-over-refactor, verify-before-fix, narrow PR scoping, etc.) —
already consistent with the brief's philosophy. Two entries
(`project_phase1_status.md`, `project_m365_graph_landed.md`) are historical
snapshots that could be retired by the same logic the brief applies to
chat-memory entries #17–#20. cc did **not** touch its own file-based memory
unilaterally — flagging for the operator to confirm if a parallel
consolidation is wanted there.

---

## Original brief (verbatim — the rationale anchor)

### Current state

30 entries (at cap). Mix of structural guidance, contextual snapshots, and historical milestones. Many entries have grown stale or duplicate doctrine that's now properly captured in the `its-blueprint` repo. The 30-entry cap is no longer a budget problem — it's a signal-to-noise problem.

### Philosophy

Memory should be **structural navigation + hard-fought rule enforcement** — pointers to canonical docs and behavioral rules that prevent specific mistake classes from recurring. It should NOT carry:

- Doctrine content that's better captured in `doctrine/` (load via project knowledge as needed)
- Historical milestones (in git log + session logs + memory-archive.md)
- Point-in-time operational facts (in code + Smartsheet config + tech_debt.md)
- Phase-specific framing that's dormant (reload when the phase arrives)

What memory SHOULD do: when chat encounters situation X, memory tells chat "follow rule Y" or "consult file Z." Mistakes that have been made should NEVER be made twice because memory enforces the lesson.

### Audit of current 30 entries

| # | Current entry (short form) | Action | Rationale |
|---|---|---|---|
| 1 | Core identity, ITS / Evergreen / Customer 0 | KEEP | Every chat needs frame-setting |
| 2 | System invariants — FM v8 + Op Stds v11 6-layer | REPLACE | Point at doctrine; don't restate doctrine in memory |
| 3 | Design principles, defensive build, ship-and-leave | KEEP | Behavioral rule, every code/architecture turn |
| 4 | Preservation-over-refactor + canonical PR examples | REPLACE | Slim to pointer + examples; doctrine has the rule |
| 5 | Verify-before-fix discipline (5 catches) | KEEP | Hard-fought; prevents stale-claim mistakes |
| 6 | MCP-gap REST-fallback pattern | KEEP | Operational pattern, used regularly |
| 7 | Ezra Jones email typo | REMOVE | Move to references/ doc; not chat-direction |
| 8 | IP/partnership resolved; don't raise concerns | KEEP | Behavioral rule, what NOT to do |
| 9 | Canonical doc set lives in its-blueprint repo | KEEP | Navigation, every session needs this |
| 10 | Memory archive at references/memory-archive.md | KEEP | Navigation |
| 11 | Four-part PR-landed verification | KEEP | Hard-fought; PR #34 + #68-73 prevention |
| 12 | Managed Agents Phase 3 framing | REMOVE | Dormant until Phase 3; lives in V&R |
| 13 | Box OAuth (User Auth not JWT) + Keychain rotation | KEEP | Hard-fought gotcha; ITS dies in 60d if missed |
| 14 | Push-vs-Record Separation doctrine | REPLACE | Slim to pointer at Op Stds v11 §3.1 |
| 15 | Smartsheet 5-workspace topology | REMOVE | Documented in Op Stds v11 §23 |
| 16 | SDK-vs-Live Integration Test Discipline | KEEP | Hard-fought; "4 instances in 2 days" framing |
| 17 | 2026-05-22 cascade SHIPPED | REMOVE | Historical; captured in git history |
| 18 | 2026-05-23 EOD repo state | REMOVE | Stale; evolves continuously |
| 19 | R3 session 1 shipped 2026-05-21 | REMOVE | Historical; in session log + PR |
| 20 | Box canonical state (PR #75, 1111B folder IDs) | REMOVE | IDs live in shared/defaults.py |
| 21 | ITS_Config safety_reports.recipients filled | REMOVE | In Smartsheet ITS_Config |
| 22 | CC auto-mode classifier observation | REMOVE | Informational, not directional |
| 24 | Bradley 1 sandbox demo-complete | REMOVE | In session logs + memory archive |
| 25 | Operator workflow rule (no pushback, no Path A/B) | KEEP | Hard-fought, reinforced after violation |
| 26 | Polling-daemon-as-trigger-primitive doctrine | REMOVE | Documented in Op Stds v11 §31 |
| 27 | ITS_Daemon_Health surface (folder/sheet IDs) | REMOVE | IDs live in shared/sheet_ids.py |
| 28 | Heartbeat ARCH refinements | REMOVE | In code + session log |
| 29 | Smartsheet bootstrap-drift cleanup tech debt | REMOVE | In execution-repo tech_debt.md |
| 30 | Two-repo access pattern | KEEP | Just updated, defines access semantics |

Count: 12 keeps, 3 replaces, 14 removes → 15 entries final.

### Proposed final memory layout (15 entries)

Categories:

- **Frame-setting (1)** — what ITS is, who Seth is, who Customer 0 is
- **Navigation (3)** — where to find canonical content
- **Behavioral rules (5)** — hard-fought disciplines that prevent recurrence
- **Architectural pointers (3)** — invariants, push-vs-record, SDK-vs-Live
- **Operational gotchas (2)** — Box OAuth, MCP-gap REST fallback
- **Business/principle framing (1)** — IP resolved + design principles

#### Final entry list (paste-ready text)

1. (KEEP as-is) ITS = Integrated Technical System, white-glove custom dev practice, Evergreen Customer 0, ~/its Evergreen-specific, user owns IP

2. (REPLACE #2) ITS Foundation invariants live in doctrine/foundation-mission.md (its-blueprint repo) — External Send Gate + Adversarial Input Handling 6-layer. Non-negotiable, inherited by every workstream. Restate in every brief touching external-bound code or external content ingestion via prompts/snippets/invariant-restatement.md. Don't duplicate doctrine in memory; load doctrine from project knowledge when needed.

3. (KEEP as-is) ITS design principles: defensive build, surface edge cases proactively, alerting+observability+explicit failure handling on everything customer-facing, ship-and-leave threshold per V&R v7

4. (REPLACE #4) ITS preservation-over-refactor convention lives in doctrine/operational-standards.md §14. Pattern: when chat-session code lands in ~/its and trips ruff/mypy, prefer [tool.ruff.lint.per-file-ignores] in pyproject.toml over rewriting working code. Canonical examples: PR #4 (1295a93) + PR #8 (parse_job_v3 F841 closure). Defer abstraction until ≥4 real reuse cases.

5. (KEEP as-is) ITS verify-before-fix discipline (5 catches incl. PR #34 stale-claim 2026-05-20): cascade-updates / session-wraps / briefs / PR-landed claims capture state at authorship. Before acting, verify state hasn't changed. PR-landed claims require gh pr view --json mergedAt,mergeCommit,state confirmation before going into memory. Cost of pausing to verify is minutes; cost of not pausing is shipping stale work.

6. (KEEP as-is) ITS MCP-gap REST-fallback pattern: when Smartsheet/Box/Graph MCP lacks a primitive, use short-lived sandbox token + inline curl in bash_tool, verify-after via OAuth MCP, never persist token to file or env. Operator rotates token post-session. Pattern: short-lived → inline → verify-after → rotate. Applies across all three external systems.

7. (KEEP as-is) ITS/Evergreen partnership IP is fully resolved. User owns all IP; Customer 0 terms hold. Do NOT raise IP separation, ownership, or domain registration concerns — they're handled on user's side. Treat as resolved permanently.

8. (KEEP as-is) ITS canonical doc set lives in its-blueprint repo (private, SolutionSmith-debug/its-blueprint), migrated 2026-05-24 from .docx forest. Layout: doctrine/ (FM, Op Stds, V&R, Handover, Excellence), workstreams/<slug>/{mission,brief}.md (5 workstreams), references/ (8 docs incl. memory-archive merged), audits/. Version in frontmatter (not filename); git tags mark canonical (foundation-mission-v8 etc). Linters: scripts/lint_frontmatter.py + lint_crossrefs.py, CI on every push.

9. (KEEP as-is) ITS memory-archive: v4+v5 merged 2026-05-24 into references/memory-archive.md in its-blueprint repo. Append-only operational detail; loaded on demand. Covers M365 IDs+EXO gotcha, Smartsheet 5-workspace topology+IDs, wiring history, 23-PR window, Bradley 1 migration+demo, schema decisions, Picklist Sync (PRs #45-51), SDK-vs-Live, polling daemon+heartbeat (PRs #59/#60), 2026-05-22 cascade. Future detail extends in-place via new §G* sections — no more vN+1 docs.

10. (KEEP as-is) ITS four-part PR-landed verification (codified 2026-05-23 PR #74, docs/operations/pr_merge_discipline.md): (1) state=MERGED, (2) mergedAt non-null, (3) mergeCommit.oid present, (4) main-branch CI on merge commit = SUCCESS. All four required before PR considered landed. Session logs say 'four-part verify clean'. Supersedes three-part PR #34 triplet which missed Run 229+ post-merge reds from PR #68 (6 consecutive). Required every PR.

11. (KEEP as-is) ITS Box auth = OAuth 2.0 User Auth (NOT JWT). Box Platform add-on for JWT path not licensed on Evergreen Enterprise; not buying. PR #39 (commit 2ce6ece) wired boxsdk OAuth2 + store_tokens Keychain callback (CRITICAL — refresh tokens rotate every use). Auth as seths@evergreenmirror.com; dedicated ITS user deferred to Phase 1.5. Keychain: ITS_BOX_CLIENT_ID/SECRET/REFRESH_TOKEN. setup_box_oauth.py one-time; smoke_test_box.py ops verify. Ship-and-leave intact if ITS runs ≥1x/60d.

12. (REPLACE #14) ITS Push-vs-Record Separation doctrine lives in doctrine/operational-standards.md §3.1. Rule: dedupe applies only to push, never to records. Resend = canonical push leg (subject to suppression); Smartsheet ITS_Errors + Sentry always write as forensic surfaces. Sentry alert rules + Smartsheet sheet-level notifications default-off. Override: enabling either converts cross-leg dedupe into active design problem; Correlation_ID is wired and ready.

13. (KEEP as-is) ITS SDK-vs-Live Integration Test Discipline (Op Stds v11 §30, codified 2026-05-21 across PRs #47/#48/#49/#51): SimpleNamespace mocks at SDK boundary miss live API enforcement (body shape, required fields, value wrapping) AND SDK runtime state (in-process caching). 4 instances in 2 days. Mitigation: pytest -m integration against throwaway sandbox resources. Any future shared/* SDK wrapper with create/update/delete on typed columns/rows gets parallel integration test. CI skips by default.

14. (KEEP as-is) ITS operator workflow rule (REINFORCED 2026-05-22 after violation): NEVER push back on operator scheduling, energy, or timing. NEVER offer Path A vs Path B when not asked. NEVER suggest deferring. NEVER comment on energy, time of day, or diminishing returns. Operator says do X, Claude does X — no preamble. Only acceptable commentary: technical tradeoffs about the work itself. Violation pattern: dressing timing pushback as deference ("Path B is more conservative"). That IS pushback. Don't.

15. (KEEP as-is) ITS two-repo access pattern (2026-05-24): planning in its-blueprint (PRIVATE, SolutionSmith-debug/its-blueprint), execution in its (PUBLIC, SolutionSmith-debug/its). its readable from chat via git clone or web_fetch. its-blueprint NOT cloneable from chat (no GitHub MCP exists on Claude.ai); chat reads blueprint via project knowledge where .md files are uploaded. Blueprint canonical for doctrine/missions/briefs; execution canonical for code. Blueprint wins on conflict.

### What gets archived where

| Retired memory | Destination |
|---|---|
| #7 Ezra email typo | Add §G6 to references/memory-archive.md: "Contacts data quality" |
| #12 Managed Agents Phase 3 | Already in doctrine/vision-and-roadmap.md; just remove |
| #15 5-workspace topology | Already in doctrine/operational-standards.md §23; just remove |
| #17 2026-05-22 cascade | Already in git log + audits/2026-05-21_cascade-verification.md; just remove |
| #18 2026-05-23 EOD repo state | Captured in git log (commits + tags); just remove |
| #19 R3 session 1 shipped | In execution-repo session log + PR #57; just remove |
| #20 Box canonical state PR #75 | Folder IDs in shared/defaults.py BOX_PROJECT_FOLDERS; just remove |
| #21 ITS_Config recipients filled | In Smartsheet ITS_Config sheet; just remove |
| #22 CC auto-mode observation | Informational only; just remove |
| #24 Bradley 1 demo-complete | In Memory Archive §G4 + session log; just remove |
| #26 Polling-daemon doctrine | In doctrine/operational-standards.md §31; just remove |
| #27 ITS_Daemon_Health IDs | In shared/sheet_ids.py DAEMON_HEALTH_COLUMNS; just remove |
| #28 Heartbeat ARCH refinements | In references/daemon-health-schema.md + PR #60; just remove |
| #29 Bootstrap drift cleanup | In execution-repo docs/tech_debt.md; just remove |

One add to memory-archive.md (§G6 — Contacts Data Quality, captures the Ezra typo). All other retirements are clean removes.

### Execution sequence

Per memory_user_edits semantics (replace before remove; removes high-line-number → low-line-number to prevent index shift):

1. **Replaces first** (in-place, lines don't shift):
   - Replace line 2 with new content (invariants pointer)
   - Replace line 4 with new content (preservation pointer + examples)
   - Replace line 14 with new content (push-vs-record pointer)

2. **Removes second** (high-to-low to avoid index shift):
   - Remove #29, #28, #27, #26, #24, #22, #21, #20, #19, #18, #17, #15, #12, #7

3. **Add §G6 to memory-archive.md** in the blueprint repo — captures the Ezra typo before its memory entry is retired. Small follow-on PR.

Final state: 15 entries, all structural or hard-fought-rule.

### Recovery path

If a removed memory turns out to be load-bearing for a future question:

1. Find the relevant content in its-blueprint repo or execution-repo files (each retirement above names the destination).
2. If it should be in memory after all, add via memory_user_edits (we'll have headroom — current cap is 30 entries, we'll be at 15).

The retirement is non-destructive in the sense that the content survives in the repos and in git history. Memory just stops carrying it.

### Done when

- 14 memory removes executed
- 3 memory replaces executed
- Final state shows 15 entries
- §G6 added to references/memory-archive.md in a small follow-on PR to its-blueprint
- This brief committed to its-blueprint/session-logs/2026-05-24_memory-consolidation.md as the rationale anchor

## Cross-references

- §G6 PR: https://github.com/SolutionSmith-debug/its-blueprint/pull/2
- Merge commit `1a07a31`: https://github.com/SolutionSmith-debug/its-blueprint/commit/1a07a31
- Prior session logs:
  - [`2026-05-24_initial-migration.md`](2026-05-24_initial-migration.md)
  - [`2026-05-24_prompts-scaffolding.md`](2026-05-24_prompts-scaffolding.md)
