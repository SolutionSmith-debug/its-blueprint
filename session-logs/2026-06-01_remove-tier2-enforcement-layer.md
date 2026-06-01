---
type: session_log
status: archived
workstream: null
tags: [doctrine-cascade, de-1b, tier-2-boundary, training-bounded-co-resolution, successor-operator, enforcement-layer-removal, provenance-preserved]
---

# 2026-06-01 — Remove Tier-2 non-developer-safe enforcement layer; training-bounded co-resolution (FM v11 / Op Stds v16 / Handover v8 / V&R v9 / Excellence v4)

## Purpose

Implement a settled, Seth-approved decision: **remove the rejected "option 1b" Tier-2 non-developer-safe enforcement layer** that the 2026-05-29 three-tier-maintenance cascade (PR #28, FM v10 / Op Stds v15 / Handover v7 / V&R v8 / Excellence v3) had named as a hard pre-cutover BUILD gap, and replace it with the **training-bounded co-resolution** model. Landed as PR #30 (merge `8c708b9`).

This was a co-resolved **HIGH-capability-class doctrine change** (the very class the doctrine routes to Seth). Co-resolution happened in chat: Seth approved the decision and the per-doc edit plan via the brief. CC implemented; nothing was decided here.

## The corrected model (settled — not re-litigated)

- **No structural maintenance enforcement layer**, and none is to be built. The capability-gating philosophy (FM Invariant 1 two-process model) still informs *how the Tier-2 boundary is drawn* (why the four high-class categories are off-limits) — but it **ends at philosophy, not a built control**.
- The Tier-2 boundary is held by: **(a)** the trained Successor-Operator's judgment; **(b)** the both-rule (novel OR high-class → Tier 3); **(c)** co-resolution with the Developer-Operator on the four fixed high-class categories (External Send Gate / secrets-auth / doctrine / code change) until per-category clearance (dated, logged, Developer-Operator-only).
- **Successor-Operator redefined**: a *trained operator who runs Claude Code himself* and follows §43 runbooks — **not** a Smartsheet-UI-only approver rubber-stamping Claude-driven actions. Still a non-developer (writes no code; performs no §§37-41 developer-context work).

## What survived (deliberately not over-cut)

- **Tier-1 self-heal / Check H** pre-cutover gate — real, now standalone (the v8/v7 "BOTH must be built" coupling is removed).
- **§43 successor-remediation runbook discipline** — kept and now *more* load-bearing (runbooks + training carry the boundary 1b would have carried structurally).
- The **both-rule**, the **HIGH/LOW capability-class definitions**, the **§44 low-class action set**, the **audit-trail requirement**, and the **Developer-Operator / Successor-Operator role names**.
- Pre-cutover: the "Tier-2 enforcement layer built" condition → a **Tier-2 readiness** gate (low-class action set implemented as discrete tested operations + §43 runbooks + trained-operator / demonstrated-supervised-repair). Excellence R6 sub-deliverable (b) reframed the same way; (a) self-heal + (c) runbook tooling retained.

## Decisions / judgment calls

- **References left out of scope (flagged, not edited).** `references/permissions.md` §3.2 and `references/system-hr-handoff.md` still carry the old "non-developer / Smartsheet-UI-only / never terminal" Successor-Operator framing, which now contradicts the corrected doctrine. The brief scoped this cascade to the **5 doctrine docs** (doctrine-only cross-doc checks; no reference version bumps), so the references were **not** touched. The drift is flagged inline (Op Stds + V&R companion ledgers) and below as a **required role-redefinition follow-on**.
- **Provenance preserved, not blind-deleted.** Each of the 5 authority blocks records that the enforcement layer existed in the prior version and was deliberately removed; V&R retains a "Prior cascade — v8" provenance table; Op Stds retains the v15-trigger history line. Surviving "enforcement layer" mentions are all negations ("there is no…", "removed") or labeled provenance.
- **`Role scope (v15)` label left as-is** in Op Stds §37 — it marks when the role-scope note was introduced (provenance), and its substance (Successor-Operator performs none of §§37-41) is unchanged by v16. The enforcer assessed this as acceptable, not a block.
- **G7 maintained**: every changed doc bumped its frontmatter integer AND title to the same bare integer; no `vN.x` overlay reintroduced.
- **Classifier flapping**: the opus Bash-safety classifier hiccupped intermittently this session. Per the brief, edits use the Edit tool (no classifier needed), so the cascade could not be half-applied by a classifier outage — all 5 docs were edited fully before any git operation; git/merge ran cleanly when the classifier was up.

## Validation (the brief's gates)

- **6 cross-doc consistency checks — all pass:** (1) `non-developer-safe` / `enforcement layer` → only negation or labeled provenance; (2) `pre-cutover` → no Tier-2 enforcement-layer gate (only removal records); (3) Condition 5 / Criterion 4 rewritten consistently; (4) no forward stale version pins (all read FM v11 / Op Stds v16 / Handover v8 / V&R v9 / Excellence v4, except arrow-provenance); (5) frontmatter == title on all 5; (6) provenance preserved in all 5 authority blocks.
- **`ops-stds-enforcer`: BLOCK → PASS.** First pass caught two stale-paragraph leftovers my edits' `old_string` didn't span (an orphaned Excellence "v3 is operative reference" line; the stale §43 intro clause in Op Stds). Both removed; re-review PASS — §14 preservation, provenance, no enforcement-overclaim, and version pins all confirmed.
- **Linters clean** (`lint_frontmatter` + `lint_crossrefs`, 70 files).
- **Four-part PR-landed verify (PR #30):** state=MERGED · mergedAt=2026-06-01T16:20:36Z · mergeCommit `8c708b9` · main-branch CI (lint) on the merge commit = completed/success.

## Tags (operator pushes post-merge — NOT pushed from this session)

`foundation-mission-v11`, `operational-standards-v16`, `handover-plan-v8`, `vision-and-roadmap-v9`, `excellence-roadmap-v4` — all confirmed absent on main; named in each doc's Authority block.

## Required follow-on (out of scope here)

1. **References role-redefinition** — reframe `references/permissions.md` §3.2 + `references/system-hr-handoff.md` from "non-developer / Smartsheet-UI-only / never terminal" to the trained-CC-operator definition. (Folds naturally into Tranche 0 or a small reference PR.)
2. **Tranche 0 — exec-repo reconciliation** (separate `~/its`-rooted PR): `doctrine_manifest.yaml`, `CLAUDE.md`, `README`, `check_doctrine_drift.py` regexes for FM v11 / Op Stds v16. Cannot run from the blueprint root; runs after this lands (and after the tags exist).
3. The **inline-pin normalization sweep** still pending from the v10-cascade era folds into Tranche 0.
