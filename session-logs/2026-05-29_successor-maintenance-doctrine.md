---
type: session_log
status: archived
workstream: null
tags: [doctrine-cascade, successor-maintenance, three-tier-model, developer-operator, successor-operator, capability-gating, document-as-you-build, g7-version-reconcile, enforcement-honesty]
---

# 2026-05-29 — Three-tier non-developer-successor maintenance model → doctrine (FM v10 / Op Stds v15 / Handover v7 / V&R v8 / Excellence v3)

## Purpose

Turn the operator's settled decision — adopt a **three-tier non-developer-successor maintenance model** — into doctrine, implementing gaps **G1–G7** from the 2026-05-29 successor-maintenance audit ([`audits/2026-05-29_successor-maintenance-audit.md`](../audits/2026-05-29_successor-maintenance-audit.md), PR #27, which found the model **ASSUMED-BUT-UNSTATED / ABSENT on the load-bearing tier**). Landed as PR #28 (merge `6a46730`).

The model (operator-decided; not re-litigated this session):
- **Tier 1 — self-heal.** Daemons recover, watchdog catches. Partly built (Check H is an unmet pre-cutover condition; 2 of 3 daemons heartbeat-pending).
- **Tier 2 — Claude-assisted Successor-Operator repair.** A *non-developer* Successor-Operator APPROVES while Claude DRIVES; **LOW-capability-class set only** (re-run a daemon, toggle an ITS_Config value, re-send an approval, re-seed a row, clear a stuck lock).
- **Tier 3 — escalate to the Developer-Operator (Seth)** as a reachable asset, **not** the primary operator. The **"both" rule**: a fault is Tier-3 if NOVEL (no §43 runbook entry) OR HIGH-capability-class (External Send Gate / secrets-auth / doctrine / code change).

## Pre-flight findings (brief-validator)

`brief-validator` ran at session start against live `~/its` (`585823d`) + `~/its-blueprint`. **PROCEED.** The load-bearing verification (the honesty crux):

- **Capability gating is REAL** — `tests/test_capability_gating.py` does AST import inspection enforcing the two-process External Send Gate (a generation process cannot import send capability). This is the philosophy the Tier-2 enforcement layer must inherit.
- **The four `.claude/hooks` guards** (`block-codeql-dismiss`, `block-dangerous-git`, `block-doc-reconciliation-write`, `block-doctrine-write`) are REAL but **scoped to subagent/developer sessions and fall open for the operator's own session** ("operator must run it manually"). The guard architecture assumes a developer who can safely override.
- **Therefore the non-developer-safe Tier-2 enforcement layer DOES NOT EXIST.** This is the single most important constraint: doctrine names it as a **build gap**, never asserts it present.
- Doc versions confirmed (frontmatter integer vs title split on Handover/V&R/Excellence = Gap G7); the fabricated V&R "30 consecutive days" quote is absent (real text: FM "Permanent, not time-bounded"); `permissions.md`/`system-hr-handoff.md` still encoded the old developer-grade-maintainer model.

## Method — design → operator-approve → write → enforce

Multi-agent design pass (6 per-doc designers + adversarial cross-check). The cross-check returned **needs-revision** on reconciliation cleanups only — and confirmed the two things that matter: **no edit asserted Tier-2 enforcement as present**, and **no fabricated quote**. Operator approved the design + the load-bearing text, then answered 4 decisions; the doctrine was drafted as a working-tree diff, reviewed by `ops-stds-enforcer`, and landed via PR #28 (operator merge-approved after PR-diff review — no hook backstop in the blueprint, so operator approval was the gate).

## Decisions made

- **Decision: cutover is a HARD BLOCKER on the Tier-2 enforcement layer (and Tier-1 self-heal).** Not the interim/Tier-3-fallback posture the first drafts used. Handover Pre-Cutover Conditions, V&R Pre-Cutover Condition 5, and Op Stds §44 all state cutover does not proceed — and a non-developer Successor-Operator does not take day-to-day operation — until BOTH layers are built and verified. *Rationale:* operator chose the stricter gate; it prevents shipping a non-developer into an un-enforced repair path.
- **Decision: §43 successor-remediation entries live as repo Markdown, Claude-read.** Shipped with the capability in the execution repo, version-controlled; Claude loads the entry to drive a repair; the Successor-Operator never opens it (they see Smartsheet + alerts and approve). *Alternative:* Smartsheet-hosted. *Rationale:* the discipline is "document AS you build," so it lives with the code; Claude is the actual reader.
- **Decision: reference reconciliations land in the SAME cascade.** `permissions.md` v5, `system-hr-handoff.md` v6, `worktree-discipline.md` v1 reframed in PR #28 (not deferred), because they actively contradicted the new model.
- **Decision: V&R bumps to v8** despite its narrow v8-trigger wording; the ship-and-leave threshold definition is substantive enough, and a major bump cleanly reconciles G7. Noted as a stretch in the V&R Authority block.
- **Decision: G7 reconciliation = bump frontmatter integer AND set title to the bare integer**, retiring the `vN.x` minor-overlay for the changed docs. FM/Op Stds were already integer-titled; Handover/V&R/Excellence dropped their `.x` overlays.
- **Decision: references are NOT git-tagged.** No reference doc has ever carried a canonical git tag in this repo (only `doctrine/*` do); creating `permissions-v5` etc. would introduce the convention inconsistently. References stay frontmatter-versioned. Five **doctrine** tags created on `6a46730`: `foundation-mission-v10`, `operational-standards-v15`, `handover-plan-v7`, `vision-and-roadmap-v8`, `excellence-roadmap-v3`.
- **Decision: inline carry-forward §-references preserved, not bumped.** §-references inside `(NEW v6.3)`-labeled blocks (Handover Risk Inventory "Op Stds v11 §§33-35"; FM Invariant 2 implementation-status "V&R v7.2"/"Op Stds v11"; Excellence R5-row "V&R v7.2") were left as-is — the §-numbers resolve, and this matches the prior cascade's discipline of deferring inline-pin normalization to a separate sweep. **Companion ledgers** (Authority footers, FM "Scope of This Project" list, Handover "Companion-Doc References") **were** fully refreshed to in-cascade targets. `ops-stds-enforcer` accepted the inline carry-forwards under §14.
- **Judgment: did NOT apply the cross-check's "worktree three→four hooks" flag.** The "three propose-only PreToolUse guard hooks" in `worktree-discipline.md` is contextually correct — the three *agent-symlink-scoped propose-only* hooks that vanish when the symlink dangles; `block-dangerous-git` is a separate, non-agent-scoped git guard. Bumping it to four would be wrong.

## G-gap → doctrine mapping

| Gap | Where it landed |
|---|---|
| G1 role abstraction | FM v10 Operating Principles (Developer-Operator / Successor-Operator); Op Stds v15 §§37-41 role-scope clarifier; Handover v7 Operator Roles |
| G2 document-as-you-build | Op Stds v15 **§43** (Successor-Remediation Documentation Discipline, parallel to §42) |
| G3 Claude-assisted fix workflow | Op Stds v15 **§44** (Tier-2 repair path + low/high capability-class + enforcement build gap) |
| G4 Seth-primary-operator contradiction | Handover v7 Step 8 + Day-7 gate; Excellence v3 Track-3 reframe; `permissions.md` §3.1/§3.2; `system-hr-handoff.md` |
| G5 ship-and-leave threshold | V&R v8 "Ship-and-Leave Threshold" section + successor-maintainability criterion |
| G6 silent fail-open hazards | Op Stds v15 §2 watchdog-detectable-signal note; `worktree-discipline.md` v1 |
| G7 version drift | frontmatter==title reconciled on Handover/V&R/Excellence; companion ledgers refreshed |

## Gates

- `brief-validator` PROCEED (above).
- `ops-stds-enforcer`: **BLOCK → PASS.** First pass flagged 3 §41 companion-ledger stale pins (Handover Companion-Doc References bullets; V&R in-body "Handover Plan v6.3"; system-hr Authority chain citing FM v6/Op Stds v8). All fixed; re-review **PASS** — preservation clean, no enforcement-overclaim, frontmatter==title on all 8.
- `lint_frontmatter.py` + `lint_crossrefs.py`: **clean (69 files)**.
- Landed via four-part verify: PR #28 MERGED · merge `6a46730` on main · tree clean · 8 version bumps live · 5 doctrine tags resolve · branch deleted.

## Out of scope / required follow-on

- **REQUIRED — exec-repo doctrine reconciliation (separate exec-rooted PR, NOT done here).** FM→v10 / Op Stds→v15 leaves `~/its` `doctrine_manifest.yaml`, `CLAUDE.md`, `README`, and `scripts/check_doctrine_drift.py` regexes citing the old versions. Must run from the `~/its` root (same pattern as exec PRs #125/#127). Cannot be done from the blueprint root.
- **Build work the new doctrine now mandates as pre-cutover (Excellence R6):** the Tier-2 non-developer-safe enforcement layer + Tier-1 self-heal completion (Check H across all daemons) + the §43 successor-remediation runbook substrate. Hard pre-cutover gates per Handover v7 / V&R v8.
- **Inline §-pointer normalization sweep** (the deferred carry-forward pins above) — a separate mechanical pass when convenient.
