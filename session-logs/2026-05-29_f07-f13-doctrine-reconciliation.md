---
type: session_log
status: archived
workstream: null
tags: [doctrine-revision, foundation-mission, op-stds, kill-switch, anomaly-logger, invariant-2, security-posture, forensic-audit, f07, f13]
---

# 2026-05-29 — F07 + F13 doctrine reconciliation (FM v8 → v9, Op Stds v13 → v14)

## Purpose

Reconcile two forensic-audit findings (`audits/2026-05-25_forensic-audit.md`) where doctrine **over-promised** a security mechanism relative to what the code delivers. Over-describing a tripwire as a wall is a worse failure than an honest description — it invites trusting the mechanism as a boundary it is not. Both are doctrine-language corrections, not code changes:

- **F07 — kill switch.** `kill_switch.py` was documented in a way that invited treating it as a security control. It is fail-OPEN by design (sheet unreachable / row missing / invalid value all resolve to ACTIVE + WARN). A fail-open mechanism is an operator-convenience pause, not a security boundary — an adversary who can make the sheet unreachable defeats it. Op Stds §1 reframed accordingly (v13 → v14).
- **F13 — anomaly logger.** FM v8 Invariant 2 **Layer 5** (anomaly logging) was framed as a co-equal defense layer. The implementation is exact-substring matching against a short sentinel phrase list — trivially evaded by paraphrase. The real adversarial defenses are Layers 2–4 backed by the External Send Gate (Invariant 1). Layer 5 reframed from defense layer to post-hoc detection tripwire (FM v8 → v9). **Code unchanged.**

Implements the **Q8 ruling** in `session-logs/2026-05-25_safety-portal-grill.md` ("F07: suggested pause, not security control; `fail_closed_until` deferred. F13: tripwire, not defense layer; keep code.").

This is the F07/F13 cascade PR the v13-revision log (`session-logs/2026-05-25_op-stds-v13-revision.md`, Out-of-scope line) deferred.

## Pre-flight findings

`brief-validator` ran at session start against live `~/its-blueprint` + `~/its`. All 14 brief claims verified, with three refinements that changed the work:

- **FM kill-switch edit is a confirmed NO-OP.** `grep` of `foundation-mission.md` for `kill.switch` / `require_active` / `security control` returned **zero hits** — FM contains no kill-switch text at all. The kill switch lives entirely in Op Stds §1 + execution-repo `CLAUDE.md`. Per the brief's explicit anti-pattern ("DO NOT invent an FM kill-switch edit"), **no kill-switch text was added to FM.** FM v9 is therefore driven **solely by F13** (the Layer 5 reframe).
- **Exec HEAD is `64526a1`, not the brief's `eea3553`.** `last_verified_against` set to `64526a1` (`64526a16f771dac43c0e4ae50acf5877beafce62`) on both docs.
- **Op Stds §1 did not previously enumerate the three fail-open modes by name** — it said "three modes"; the names lived in `CLAUDE.md:131`. The v14 reframe enumerates them in §1 prose (sheet unreachable / row missing / invalid value), an additive clarification.

Live frontmatter confirmed pre-edit: FM `version: 8`, `last_verified_against: 3b7d56d`, `supersedes: @v7`; Op Stds `version: 13`, `last_verified_against: a1dc227`, `supersedes: @v12`. Clean working tree on `main`. Tags `foundation-mission-v8` + `operational-standards-v13` exist (convention `{slug}-v{N}`).

Inbound-anchor map (so no heading rename breaks a cross-ref): `CLAUDE.md:51` → `#invariant-2-adversarial-input-handling-revised-in-v8` (Invariant 2 heading — **left unchanged**, reframe lives inside the Layer 5 subsection); all inbound Op Stds links point at §39 (untouched). Nothing links to the Layer 5 or `#1-kill-switch` anchors → safe to retitle Layer 5 / extend §1.

## Decisions made

- **Decision**: FM v9 bump despite the v8 Authority's narrow "v9 trigger" wording ("principle change OR business-model change").
  - **Alternative considered**: treat the Layer 5 reframe as a v8.x status update (no bump).
  - **Rationale**: recharacterizing a defense layer's protective claim is a substantive security-posture change, not a status update — downstream readers treat Layer 5 differently now. Precedent: v7 → v8 bumped on an enforcement-pattern change, not a principle change. `doctrine-revision.md`: "when in doubt, bump." The brief + Q8 both direct v9. Corrected the next-trigger line (now "v10 trigger") to explicitly include "defense-layer add/remove/recharacterization" so the trigger definition matches actual practice (the old line would not have predicted this very bump).

- **Decision**: Reframe lives *inside* FM's Layer 5 subsection; the `## Invariant 2 — Adversarial Input Handling (Revised in v8)` heading is **unchanged**.
  - **Alternative considered**: retitle the Invariant 2 heading to "(Revised in v9)".
  - **Rationale**: `CLAUDE.md:51` links to `#invariant-2-adversarial-input-handling-revised-in-v8`; retitling would break that cross-ref (lint_crossrefs validates it). The umbrella structure of Invariant 2 (six layers) is genuinely a v8 artifact; only Layer 5's *characterization* changed in v9.

- **Decision**: Adjusted the FM Residual-Risk sentence ("Layers 2-5 still apply") to "Layers 2-4 still apply … with Layer 5 anomaly logging as a post-hoc detection signal, not a barrier."
  - **Rationale**: leaving "Layers 2-5 … anomaly logging" as co-equal defenses would self-contradict the new Layer 5 framing. In-scope (same Layer 5 characterization, different paragraph). Left FM:102 (enforcement-pattern enumeration) untouched — a tripwire is still an enforcement pattern; no contradiction there.

- **Decision**: No new `[text](#anchor)` markdown links added; invariants referenced in prose ("the External Send Gate (Foundation Mission Invariant 1)").
  - **Rationale**: matches existing doctrine voice (Op Stds already references FM in prose, not validated links) and makes it structurally impossible for these edits to introduce a crossref violation.

- **Decision**: Both doctrine bumps land in **one PR**; the execution-repo `CLAUDE.md` touch is a **separate companion PR** (see Out of scope). No downstream cascade bundled.
  - **Rationale**: `doctrine-revision.md` prohibits bundling a doctrine bump with a downstream cascade. Two co-equal doctrine bumps from the same Q8 ruling are the bump, not a cascade. The exec `CLAUDE.md` edit cannot be made from a blueprint-rooted session and is a companion, not a cascade.

- **Decision**: Version-pin seam — the two PR docs are made mutually current in their **companion-ledger** references (each Authority block + FM's "Scope of This Project" list now name each other at FM v9 / Op Stds v14); **inline body `§`-pointers** (`Op Stds v11 §33/§34/§29` in FM body) and version pins to non-PR docs (V&R v7.2, Handover v6.3, etc.) are **preserved** for the separate stable-anchor / version-refresh sweep.
  - **Alternative considered**: bump every `Op Stds v11 §N` inline ref to v14 (full currency); or leave even the companion ledgers stale (full defer).
  - **Rationale**: companion-ledger lines are the small curated "what version is my sibling" record a bump owns keeping current; inline `§`-pointers are numerous, are the CONVENTIONS-discouraged version-pinned-cross-ref pattern, and are the explicit target of the deferred mechanical sweep. Bounds scope while removing every bump-introduced inconsistency. The `Op Stds v4` reference in FM Invariant 1 is a deliberate historical "superseded framing" pointer and stays.

- **Decision**: Acted on the 4-lens adversarial review's blocker (the review's primary catch).
  - **Context**: the review found the **Op Stds Authority block** had not been rolled to v14 — I had updated FM's Authority but missed Op Stds's, so the doc self-contradicted (v14 frontmatter/title/What-Changed vs. v13 Authority). A blind spot from editing the two docs asymmetrically.
  - **Rationale**: rewrote the Op Stds Authority block mirroring FM's v9 pattern + the v13-revision-log precedent (roll predictive trigger forward to v15, add a v14 history line with the post-merge tag, retain v13/v12 history, update companion `FM v8` → `FM v9`). An independent re-verification agent confirmed all fixes clean (6/6 PASS).

## Doc changes (this PR)

- Edited `doctrine/foundation-mission.md` (v8 → v9):
  - Frontmatter: `version` 8 → 9; `last_verified` 2026-05-24 → 2026-05-29; `last_verified_against` 3b7d56d → 64526a1; `supersedes` → `@v8`.
  - Title / date / summary lines rewritten for v9 (Layer 5 reframe headline).
  - `# Purpose of v8` → `# Purpose of v9` (Layer 5 reframe rationale, F13 citation, what-stays-unchanged).
  - **Layer 5 subsection reframed** (F13): heading `(Unchanged)` → `(Reframed in v9: Tripwire, Not Defense Layer)`; two new framing paragraphs (tripwire-not-defense; real defenses = Layers 2–4 + External Send Gate); mechanism description retained verbatim **including the `SUSPICIOUS_FIELD_PATTERNS` FP-risk tech-debt reference**. Code unchanged.
  - Residual-Risk sentence adjusted (Layers 2-5 → 2-4 + Layer 5 as detection signal).
  - Authority block: v9 rewrite; "v10 trigger" line broadened (recharacterization is bump-worthy); companion line `Op Stds v11` → `v14`; dropped the v8-dated cascade-event line.
  - *(review-driven)* Scope-of-project line `(this doc, v8)` → `(this doc, v9)` and companion `Operational Standards v11` → `v14`; Invariant 2 lead sentence now flags the v9 Layer 5 recharacterization (heading text **unchanged** — preserves the `CLAUDE.md` inbound anchor `#invariant-2-...-revised-in-v8`).
- Edited `doctrine/operational-standards.md` (v13 → v14):
  - Frontmatter: `version` 13 → 14; `last_verified` 2026-05-25 → 2026-05-29; `last_verified_against` a1dc227 → 64526a1; `supersedes` → `@v13`.
  - Title / date / summary lines rewritten for v14 (kill-switch reframe headline).
  - `# What Changed in v14` section inserted between `# What Changed in v13` and `# §1 — Kill Switch`.
  - **§1 reframed** (F07): new "What it is — and is not" lead paragraph (operator-convenience pause, not a security control/boundary; fail-open-by-design rationale; External Send Gate = real boundary); existing ITS_Config mechanism + Status paragraphs retained; three fail-open modes now enumerated in prose; `fail_closed_until` noted as deferred / NOT implemented. Picklist-hardening + per-daemon-runtime-gate subsections unchanged.
  - *(review-driven)* **Authority block rolled to v14**: opening line rewritten (F07 reframe summary; "v13 retires on acceptance of v14"); predictive trigger → "v15 trigger" (recharacterization is bump-worthy); "v14 trigger" history line added with the `operational-standards-v14` tag; "v13 trigger" history retained; companion `FM v8` → `FM v9`.
- New `session-logs/2026-05-29_f07-f13-doctrine-reconciliation.md` (this file).

## Verification

- `python3 scripts/lint_crossrefs.py` → **clean (65 files).** No new `[text](path)` links introduced (prose §/invariant references only); the only renamed slug (FM `purpose-of-v8` → `purpose-of-v9`) has zero inbound links.
- `python3 scripts/lint_frontmatter.py` → 1 error, **pre-existing and out of scope**: `references/claude-code-info-gap.md` has no frontmatter delimiter — confirmed identical on `origin/main` (untouched by this PR; diff is only the two doctrine files + this log). Lint runs without `--strict` (exit 0). Flagged as a separate follow-on (see Out of scope).
- **Adversarial review (4-lens workflow over the uncommitted diff)**: intent-fidelity (**pass**), requirement-coverage (**1 blocker**), consistency-overclaim (**2 should-fix + 2 nits**), version-anchor-safety (**4 should-fix**). The reframe *wording* passed every lens; all findings were incomplete-propagation of the version bump (see Decisions). Blocker = Op Stds Authority block not rolled to v14 — fixed, plus the FM Scope / reciprocal-companion / Invariant-2-lead-sentence fixes.
- **Focused re-verification** (independent agent over the post-fix state): **6/6 PASS** — Op Stds Authority self-consistent at v14; no over/under-claim (fail_closed_until still "deferred / not implemented"; External Send Gate named as the boundary); FM↔Op Stds reciprocal companions match; no current-version self-reference left at the old number; FM Invariant 2 heading slug intact; both linters as above.
- Four-part PR-landed verify + tags `foundation-mission-v9` / `operational-standards-v14`: **post-merge** (see Sequencing). Per `doctrine-revision.md`, tags pushed on the canonical merge commit.

## Out of scope

- **Execution-repo `CLAUDE.md` companion PR (F07).** Cannot be made from a blueprint-rooted session. The `~/its/CLAUDE.md:97` "Kill switch first" guidance should gain a one-clause note that `@require_active` is an operator pause, not a security gate (cite Op Stds v14 §1). The `:131` capability-table row already reads "fail-open on three modes (…)" and is accurate — no change. Do this from `~/its` **after** this doctrine PR merges, citing the merged v14 §1 wording. Proposed clause prepared (handed to operator).
- **`fail_closed_until` mechanism (F07).** Deferred to tech debt per Q8. Doctrine references the deferral; not implemented.
- **F20 (schema-version enforcement).** Execution-repo CODE change — separate session (Session B), not this PR.
- **`anomaly_logger.py` code (F13).** Doctrine-only reframe; no code touched. (F21 numeric-range check is a separate finding, not in this bundle.)
- **Version-pinned cross-ref drift sweep.** FM/Op Stds bodies still carry some stale version-pinned prose references to *other* docs (e.g. FM body "Op Stds v11"); a mechanical stable-anchor / version-refresh pass is a separate cascade, not this doctrine bump.
- **`references/claude-code-info-gap.md` missing frontmatter.** Pre-existing lint error; one-line fix in a separate PR (unrelated to this reconciliation).

## Sequencing context

- **Prerequisite (landed)**: the 2026-05-25 forensic audit (`audits/2026-05-25_forensic-audit.md`) + the Q8 ruling (`session-logs/2026-05-25_safety-portal-grill.md`). `last_verified_against` → exec HEAD `64526a1`.
- **This PR**: FM v8 → v9 (F13) + Op Stds v13 → v14 (F07), one PR. Tags `foundation-mission-v9` + `operational-standards-v14` pushed post-merge.
- **Companion (separate, post-merge)**: exec-repo `CLAUDE.md:97` one-clause note, from `~/its`.
- **Independent**: Session B (F20 schema-version enforcement) — exec code, non-overlapping files; runs separately.

## Cross-references

- Doctrine: `doctrine/foundation-mission.md` (v9), `doctrine/operational-standards.md` (v14).
- Operator ruling: `session-logs/2026-05-25_safety-portal-grill.md` Q8.
- Audit: `audits/2026-05-25_forensic-audit.md` (F07, F13).
- Cascade precedent: `session-logs/2026-05-25_op-stds-v13-revision.md` (deferred F07/F13 to this PR), `session-logs/2026-05-24_op-stds-v12-revision.md`.
- Scaffold used: `prompts/scaffold/doctrine-revision.md` (this PR's shape).
