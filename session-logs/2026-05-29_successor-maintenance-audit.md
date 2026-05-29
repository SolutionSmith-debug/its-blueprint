---
type: session_log
status: archived
workstream: null
tags: [audit, successor-maintenance, document-as-you-build, role-abstraction, ship-and-leave, tier-2-gap, build-shaping, propose-only]
---

# 2026-05-29 — Successor-maintenance-model audit (propose-only)

## Purpose

Answer a question the operator needs settled **before** treating "a non-developer
Evergreen successor maintains ITS via Claude after Seth steps back" as a designed-for
requirement (and before it shapes the Safety Portal build): **does current doctrine
actually specify that model, or merely assume "runs unattended" and leave the
successor-maintenance model unstated?**

These are different engineering targets. "Runs unattended" (daemons self-heal,
watchdog catches, CRITICALs page someone) is believed captured. "A non-developer
successor maintains/updates/fixes it via Claude, developer gone" is a much taller
bar (documented processes, a non-developer workflow, Claude-assisted-change
guardrails, a defined escalation tier) — believed thin or unstated. The audit
measures doctrine against the operator's **three-tier model** (Tier 1 self-healing /
Tier 2 non-developer + Claude / Tier 3 escalate to Seth) and the load-bearing
**document-as-you-build** requirement.

**This was a read-and-report audit.** It produced one audit doc and edited **no
doctrine**. Any doctrine-writing is a separate follow-on PR after the operator reads
the findings.

Deliverable: [`audits/2026-05-29_successor-maintenance-audit.md`](../audits/2026-05-29_successor-maintenance-audit.md).

## Pre-flight findings (brief-validator)

`brief-validator` ran at session start against live `~/its-blueprint`. The brief's
current-state claims were largely sound but three things needed correcting before any
finding could rest on them:

- **Version numbers — frontmatter vs. title split.** The brief's guesses (Handover
  v6.3, V&R v7.2) match the **title lines**, not the frontmatter. Frontmatter carries
  the *major* integer (`6`, `7`, `9`, `14`, `2`); titles carry the operative *minor*
  (v6.3, v7.2, v9, v14, **v2.3**). Both forms are reported in the audit. (This split is
  itself a successor-reference hazard → Gap G7.)
- **Ship-and-leave threshold is NOT defined in prose anywhere in doctrine.** It exists
  only as a frontmatter *tag* in V&R (L9). The brief's premise that V&R has a quotable
  threshold wording was false — that absence became a finding (G5), not a citation.
- **The negative claim is true.** `non-developer`, `Claude-assisted maintenance`,
  `contact Seth` → **zero** hits in `doctrine/*.md`. "successor" appears only as the
  watchdog "Check H (successor to Check F)". Confirmed and re-confirmed during
  adversarial verification.

`references/system-hr-handoff.md` is **human-review** handoff (Smartsheet workspaces),
not human-resources/succession; `customer-fork-setup-checklist.md` is per-customer repo
init. Neither closes the successor-maintenance gap.

## Method — multi-agent extract → synthesize → adversarially challenge

Ran a dynamic workflow: 6 parallel per-doc readers (5 doctrine docs + a references
sweep) → 1 synthesizer → 3 adversarial challenge lenses (over-claim / under-claim /
quote-integrity), each re-opening the source files. Operator ground-truthed the two
heaviest references quotes (`permissions.md` L119, `system-hr-handoff.md` L41/L106)
independently.

The adversarial pass mattered:

- **Quote-integrity caught a fabricated quote.** An early synthesis attributed a "30
  consecutive days…permanent human review" threshold to V&R; it does **not exist**
  (zero grep hits), and FM L38 says the *opposite* — review is *"Permanent, not
  time-bounded"* (the old 30-60 day window is superseded). The quote was **removed**;
  the corrected fact *strengthens* the no-departure-threshold gap (G5). This is exactly
  the failure mode the brief's honesty mandate warns against.
- **Over-claim auditor reframed the verdict** away from "two tiers partially supported"
  (which would read as "half built") toward the honest per-tier read below.

## Verdict (as landed)

**`ASSUMED-BUT-UNSTATED` overall — and `ABSENT` on the load-bearing Tier 2.**

- **Tier 1** (self-heal): **ABSENT as audited**. What exists is a lower bar —
  detect + degrade-and-continue + page-a-**developer** — and it is itself partly
  unbuilt (Check H is an unmet pre-cutover *condition*; 2/3 daemons heartbeat-pending,
  Op Stds §31 roster L188-192). The kill-switch fail-open is **not** self-heal (v14 §1
  reframed it as operator-convenience, F07).
- **Tier 2** (non-developer + Claude fix): **ABSENT**. The only successor doctrine
  names is a *trained, traceback-reading, developer-grade* maintainer requiring
  *"maintainer-level system understanding"* (`system-hr-handoff.md` L41/L106) — the
  opposite of a non-developer. No Claude-assisted-fix workflow exists.
- **Tier 3** (Seth = asset, not operator): **CONTRADICTED**. Doctrine makes
  *"Solution Smith…the primary operator"* (`permissions.md` §3.2 L119), remote-support
  is *"what's offered"* (Excellence Roadmap L74), and Seth is never named as a
  fault-escalation tier ("future-Seth" = a code reader, §42 L550).
- **Document-as-you-build**: the discipline pattern *exists* (§42, enforced at PR) but
  is the **wrong kind** — CODE docstrings for code-readers, soft/developer-gated
  enforcement. Documenting operational *processes* for a non-developer successor is a
  **build-time-discipline GAP** (G2).
- **Role abstraction**: **FAIL**. "The operator" = a git/CC/shell-fluent developer
  throughout; the only invariant-level role split is *access-visibility* (FM L32), not
  a fix-capability boundary.

## Decisions / judgment calls

- **Did not inflate.** Per the brief, the operator may represent this model to the
  customer; an over-claimed "yes it's in doctrine" would be a false assurance. The
  verdict is stated bluntly as ASSUMED-BUT-UNSTATED / Tier-2-ABSENT, with an explicit
  anti-inflation note so the non-`ABSENT` cells can't be read as "half built."
- **Did not resolve the successor's identity.** Left the `<SUCCESSOR — operator to
  confirm>` placeholder; the audit is about the *model*, not the person. Noted that
  doctrine's own term ("future trained Evergreen maintainer", "when one exists") is
  equally unresolved and part of G1.
- **Did not edit doctrine.** Seven gaps (G1-G7) are **propose-only** — what doctrine
  *would need*, where it belongs, and build-time-discipline vs. handover-artifact, with
  priorities. Writing them is a separate decision for the operator.
- **Flagged the build-shaping decision point.** If the three-tier model becomes a
  requirement, every remaining brief needs a "Successor remediation" deliverable
  (build-time, distinct from §42); the Safety Portal must surface failures as
  non-developer-actionable signals or route to Tier-3; F08 needs a documented
  successor-maintenance boundary; F09 should establish the Claude-assisted-fix loop as a
  first-class capability-gated path. This is the operator's real decision.

## Gates

- `brief-validator` at session start (above).
- `lint_frontmatter.py` + `lint_crossrefs.py`: **clean (68 files)** after a frontmatter
  fix (inline colons in `audited_against` were read as YAML mappings → removed).
- No doctrine edited → no version bumps, no `doctrine_manifest` changes, no cascade.
- Audit ran on a branch in the main checkout (no worktree) per operator preference —
  blueprint audits have no daemon tree to protect. No worktree cleanup needed.

## Out of scope / follow-on

- **Doctrine-writing for G1-G7** — separate PR(s) after the operator reads the findings.
- **Execution-repo check** — this audit covered blueprint doctrine + references only;
  a follow-on could check whether `~/its` code/runbooks close any gap, though doctrine
  is the contract.
- Info-gap / memory-archive session-close refresh not bundled here (no current-state
  facts changed; this is a findings doc). Available via `session-close-maintainer` if
  the operator wants the gaps tracked there.
