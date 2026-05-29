---
type: session_log
status: archived
workstream: null
tags: [optimize-audit, scaffolds, doctrine-revision, brief-validator, worktree-discipline, symlink-fail-open, h1, h2, h3]
---

# 2026-05-29 — Optimize-audit "implement-now" scaffold fixes (H2 + H3 + H1-doc + blueprint worktree doc)

## Purpose

Implement the **implement-now** subset of the 2026-05-29 agent/workflow optimization audit (`~/its/docs/audits/2026-05-29_agent-workflow-audit.md`, landed on exec main via #121/#122). The audit is propose-only; this PR lands the four findings it explicitly scoped as implement-now for a future blueprint-rooted session:

- **H2** — `prompts/scaffold/doctrine-revision.md` had no step reconciling the Authority block / in-body version self-references after a bump. This is the exact class of bug that produced the v13/v14 self-contradiction earlier this day (Op Stds Authority block left at v13 while frontmatter said v14), caught only by adversarial review.
- **H3** — no scaffold routed brief current-state claims through `brief-validator` (`grep` returned zero hits across all scaffolds), even though stale code-shape claims kept recurring.
- **H1 (doc only)** — the blueprint's `.claude/{agents,hooks}` are committed **relative symlinks** that **fail OPEN**: a non-sibling checkout or bare clone dangles them → zero agents + guard hooks silently vanish. Document the assumption; do **not** de-symlink; the resolve-check is deferred.
- **Blueprint worktree doc** — the blueprint half of `worktree_discipline.md` (audit Appendix B): the worktree pattern + the "never two doctrine-touching sessions on one blueprint checkout" rule (the collision this whole thread was about).

Everything else in the audit (M1–M4, OBS-1, C-findings) is defer / confirmed-healthy and was **not** implemented.

## Pre-flight findings

- **Gating dependency cleared:** blueprint PR #25 (the parallel F02/F22 close-out) is **MERGED** (`846ff23`); blueprint `origin/main` is at that commit. The earlier shared-checkout collision (PRs #23 → #24 → #25) is fully resolved. Worktree created off `origin/main` per the brief — this session runs isolated in `~/its-blueprint-audit-fixes` (branch `audit-h2-h3-scaffold-fixes`), eating its own dog food (worktree isolation).
- **`brief-validator` ran at session start** against both repos. All 8 claim-groups VERIFIED, including the H3 zero-hits claim (direct `grep` confirmed no scaffold references `brief-validator`), the H1 symlink facts (`agents -> ../../its/.claude/agents`, `hooks -> ../../its/.claude/hooks`, both relative), and the implement-now-vs-defer call. One imprecision surfaced: the brief says "Appendix B" lives in `worktree_discipline.md`; it actually lives in the **audit doc**. `worktree_discipline.md` has the substance (the blueprint-repo pattern section + the "never two sessions" rule); Appendix B (the lift-into-blueprint draft) is in the audit. No impact on the work.
- Worktree `.claude` symlinks confirmed resolving (sibling layout holds), so this session has the full agent/guard set.

## Decisions made

- **Worktree-doc placement: new `references/worktree-discipline.md`** (the brief asked me to surface the call).
  - **Alternative considered:** add to an existing references doc, or create a blueprint `operations/` dir mirroring exec.
  - **Rationale:** the blueprint has no `operations/` dir; `references/` is "evergreen explanatory / operational docs," which fits exactly. `brief-validator` confirmed no existing `worktree-discipline.md` (additive). Indexed in `references/README.md`.

- **C8 optional one-liner: taken.** The brief permitted a one-line branch-protection note in `doctrine-revision.md` "if trivial and you're already in that file." Step 7 said a bare "Push to main", which is now inaccurate (blueprint `main` is branch-protected — every doctrine PR this day landed via PR + four-part verify). Replaced with "Land via a PR + four-part verify (not a direct push…)". A genuine accuracy fix, one line, surfaced here per the brief.

- **Scaffold version/usage_count bumps.** Bumped `version +1` on each touched scaffold (substantive revision): doctrine-revision 1→2, cc-implementation 2→3, session-orientation 1→2. Bumped `usage_count +1` per the CONVENTIONS comment ("monotonic; bump on substantive revision"). Note: the prior precedent (cc-implementation v1→v2) set `usage_count 0→6` as a one-time *use*-catch-up, which conflicts with the field's own comment; I followed the comment (revision-bump) going forward. Minor field — flag if the operator wants use-counting semantics instead.

- **`session-orientation.md` gets no in-doc changelog section** (unlike doctrine-revision + cc-implementation). Its change is a single cross-ref line; a `## v1 → v2 changes` heading would outweigh the change. The cross-ref line itself + this session log are the "why" trail. Proportionality over uniformity.

- **H1 documented, not enforced.** Documented the fail-open in `worktree-discipline.md`; did **not** de-symlink (single-source-of-truth property is worth keeping per the audit); did **not** build the resolve-check (deferred to operator per the audit) — it is described as "recommended but deliberately deferred… not built here," with a manual `test -d` verify snippet that is clearly a check-before-trust step, not an installed guard.

## Doc changes (this PR)

- **NEW `references/worktree-discipline.md`** — blueprint-side worktree discipline. Frontmatter `type: reference`, `last_verified_against: 7fbb1cd` (exec HEAD where the source docs live). Sections: why-the-blueprint-needs-this, the worktree pattern (no `PYTHONPATH` — markdown-native), the load-bearing `~/`-sibling fail-open assumption (H1: dangling → zero agents + guards silently absent; don't de-symlink; resolve-check deferred), operator-only cleanup (force-delete hook-blocked), serialization fallback, cross-refs (exec `worktree_discipline.md` + audit, via GitHub URLs).
- **`references/README.md`** — added the `worktree-discipline.md` index entry.
- **`prompts/scaffold/doctrine-revision.md`** (v1→v2, usage_count 0→1) — H2 reconcile step added under "If revising" (grep prior version string; reconcile Authority block [#1 miss] / What-Changed cross-refs / companion-doc pins); C8 branch-protection note on step 7; `## v1 → v2 changes` changelog.
- **`prompts/scaffold/cc-implementation.md`** (v2→v3, usage_count 6→7) — H3 "How to use" step 6 routing current-state claims through `brief-validator`; `## v2 → v3 changes` changelog.
- **`prompts/scaffold/session-orientation.md`** (v1→v2, usage_count 0→1) — H3 cross-ref note (points to `cc-implementation.md`).

## Verification

- `python3 scripts/lint_frontmatter.py` → **clean (66 files).**
- `python3 scripts/lint_crossrefs.py` → **clean (66 files).** New doc references exec files via GitHub URLs (external, lint-skipped); the one in-doc anchor (`#serialization-fallback`) resolves.
- **`brief-validator`** at session start: all claims verified (one imprecision surfaced, no impact).
- **Focused adversarial review** (independent agent over the diff + new doc): **7/7 PASS** — scope adherence (no M1–M4/OBS-1 creep), no doctrine bump, H2 closes the v13/v14 class, H1 fail-open + both prohibitions correct, no exec edits, cross-ref safety, H3 consistency.
- Four-part PR-landed verify: **post-merge.**

## Out of scope (deferred per the audit — NOT implemented)

- **M1** worktree-survey line in `session-close-maintainer`; **M2** settings.json warn-only CI check; **M3** blueprint doctrine-write guard; **M4** session-log scaffold exec-7-section pointer — all deferred.
- **H1 resolve-check** — documented as deferred/recommended; not built.
- **OBS-1** — exec `CLAUDE.md` v13→v14 / FM v8→v9 citation reconciliation is a separate exec-repo `doc-reconciliation-auditor` pass (already tracked as exec tech-debt @ `36e429e`), NOT this PR.
- C1–C7 confirmed-healthy; nothing to do.

## Cross-references

- Audit (source of truth): `~/its/docs/audits/2026-05-29_agent-workflow-audit.md` (exec main, #121/#122).
- Exec companion: `~/its/docs/operations/worktree_discipline.md`.
- Targets: `references/worktree-discipline.md` (new), `prompts/scaffold/{doctrine-revision,cc-implementation,session-orientation}.md`, `references/README.md`.
- Precedent: the v13/v14 self-contradiction caught + fixed in `session-logs/2026-05-29_f07-f13-doctrine-reconciliation.md` (the bug H2 now prevents).
