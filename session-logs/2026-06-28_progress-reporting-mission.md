---
type: session_log
status: archived
workstream: progress_reporting
tags: [new-workstream, progress-reporting, materials-manifest, its-owned-sor, monthly-sheets, parameterize-not-clone, external-send-gate, doctrine-flags, sor-write, section-numbering-collision, decision-a, decision-b, verify-before-write]
---

# 2026-06-28 — ITS — Progress Reporting mission v1 (draft) + doctrine flags raised

## Purpose

Codify the just-locked "ITS — Progress Reporting" + P3 Materials program into the planning layer as a
workstream mission, and raise — **propose-only** — the doctrine questions it surfaces, so the
execution-repo plan finally has its planning-layer backing. Scope: author
`workstreams/progress-reporting/mission.md` (v1, draft), resolve Decision A (workstream scope/naming)
and Decision B (the §50 numbering collision) as propose-only flags, add the new workstream tag to the
canonical enum, and write this log. **No `doctrine/*` edit.**

## Pre-flight findings (ground-before-write)

Everything was grounded against the master plan, the execution handoff brief + session log, the
neighbouring missions, and the live doctrine/lint state before any write:

- **No `field-ops` workstream exists.** The field-ops portal capture surface (Worker + D1 + React SPA,
  three-tier capability-gated RBAC, `personnel`/`equipment`/`hours`/`materials`) is owned by the
  `urs-marine-portal` mission's data architecture (D1-as-SoR, integrity bar), instantiated for
  Customer 0 in the execution repo. This is decisive for **Decision A**.
- **The enforced workstream enum lives in `scripts/lint_frontmatter.py`, not `CONVENTIONS.md`.** The
  lint set already carried `urs_marine_portal`; `CONVENTIONS.md` did **not** — a pre-existing doc/lint
  drift. To lint a new mission clean, the tag must be added to the script; `CONVENTIONS.md` is the
  documentation companion (its own rule: "Adding a workstream = small PR editing
  `scripts/lint_frontmatter.py` and this file").
- **Operational Standards v18 ends at §49.** §50 is genuinely the next free number — confirming the
  **Decision B** collision is between two *unratified candidates*, not an edit to an existing section.
- **The §50 collision is already live in the references.** `references/claude-code-info-gap.md` uses
  "§50" for **both** the privileged code-actuation gate (§3/§5, realized by `publish_daemon.py`) **and**
  the SoR-write ("§50 v18→v19, D1-as-writer to ITS-owned Smartsheet"). Two different concerns, one
  number.
- **§G43 already records the four locked strategic decisions** (memory-archive). The mission captures
  them faithfully rather than re-deriving; §G43.8 noted the blueprint-side mission/log were still owed —
  this session is that follow-up.
- **All four Tier-A foundation PRs are four-part verified** (#325 `ef568c2`, #326 `b6ba870`,
  #327 `3b285f5`, #328 `9ef3d5b`) per the execution session log — the only landed slices; everything
  else in the program is open.

## Decisions made

### Decision A — workstream scope/naming → NEW sibling workstream `progress_reporting`

Resolved: Progress Reporting is a **new sibling workstream** (`workstreams/progress-reporting/`, tag
`progress_reporting`) that **depends on** the field-ops capture surface and **reuses** the
`safety_reports` pipeline machinery — **not** a v2 of `urs-marine-portal`. Justification (in mission §2):
the capture surface is already owned by the URS-Marine/field-ops data architecture; the established
precedent is exactly the `safety_portal` (capture) ↔ `safety_reports` (report-pipeline) split; and
Progress Reporting **introduces the external send** that the URS Marine mission §9 explicitly scopes
*out* ("no customer-facing email send obligation") — so it warrants its own External-Send-Gate
restatement and its own `WPR_human_review` approval surface, not a graft onto a portal mission that
scopes send out. Naming follows the generic Customer-0 register (`safety_*`), not a customer-keyed one.

Alternative considered: v2 extension of `urs-marine-portal`. Rejected — it would conflate capture with
report-pipeline and bury the new external-send invariant surface inside a mission that disclaims it.

### Decision B — the §50 numbering collision → propose §50 = code-actuation gate, §51 = SoR-write

Surfaced, not silently picked. Two concerns both informally called "§50":
1. **Privileged code-actuation gate** — generalize Invariant 1's two-process model to *code* changes.
   Raised first (Safety Portal mission v4, 2026-06-10), already realized in code (`publish_daemon.py`).
2. **ITS-owned structured-SoR write-back** — D1-as-writer to the ITS-owned Smartsheet (the up-sync +
   bidirectional Material List). Raised 2026-06-28; gates P7 + M2 + M3.

**Recommendation (propose-only — Seth ratifies):** §50 = the code-actuation gate (raised first, already
realized); §51 = the SoR-write. Either way, assign distinct numbers. Both are v18→v19 Operational
Standards bumps (the v19 "new §" trigger is already declared). The references (info-gap §3/§8,
memory-archive) need disambiguating once Seth ratifies — flagged for `session-close-maintainer`.

## Doc changes

- **NEW `workstreams/progress-reporting/mission.md` (v1, status: draft).** Mirrors the Safety Portal
  mission frontmatter + skeleton. Captures: Purpose / Workstream-placement (Decision A) / Audience /
  Inputs / Outputs / Success criteria / Out of scope; both Foundation invariants restated verbatim
  (Invariant 1 two-process external send for the Weekly Progress Report; Invariant 2 for incident
  photos + narrative/interpolation); the five locked strategic decisions (Tier-A front-loaded;
  monthly-both; ITS-owned SoR with canonical-Evergreen + PJOB→JOB deferred; same-PR doc skeleton +
  PDF-before-cutover; parameterize-not-clone via required no-default config + the Workstream-tag guard);
  the topology (job = parent folder; monthly period sheets; `WPR_human_review` the only cross-job sheet;
  period-split + archive-on-closure, never `delete_rows`); the data flows + contamination gate; the P3
  Materials manifest model (catalog + per-job Material List receive-against-manifest; the
  field-ownership conflict model — down-upsert content-only, up-sync delivery-only; incidents from the
  list); the Stage 0/1/2 + Track M sequence with as-built status (M1/P-A1/A2 + UI fix landed; rest
  open); integration with `safety_reports` + the field-ops/`urs-marine-portal` surface; risks; and a
  **"Doctrine flags raised (propose-only)"** section. **Status is draft** (not canonical): the
  load-bearing pipeline is a forward plan gated on unratified doctrine; promotion trigger = P5 lands +
  §50/§51 ratified.
- **`scripts/lint_frontmatter.py`** — added `progress_reporting` to `CANONICAL_WORKSTREAMS` (the
  enforced enum; required for the new mission to lint clean).
- **`CONVENTIONS.md`** — added `progress_reporting` **and** the missing `urs_marine_portal` to the
  workstream enum (frontmatter example + canonical-sets list). The `urs_marine_portal` addition fixes a
  pre-existing drift (it was enforced by the lint but undocumented). Called out explicitly as a
  convention edit.
- **Personnel CRUD (task #22) recorded as design-only with three OPEN product decisions** — not
  invented (mission §13): account-creation flow (separate vs inline toggle), dangling-username
  validation, default role.

## Verification

- `python scripts/lint_frontmatter.py` — clean (new mission + this log carry valid frontmatter; the new
  `progress_reporting` tag resolves; no new shape/staleness warnings).
- `python scripts/lint_crossrefs.py` — every cross-reference in the new mission + this log resolves
  (stable filenames + anchors per `CONVENTIONS.md`).
- An adversarial verification pass (multi-agent) checked the mission for faithfulness-to-plan,
  structural mirror of the Safety Portal skeleton, authority-boundary compliance (zero `doctrine/*`
  edits, no doctrine version bump), and doctrine-flag correctness.

## Out of scope (honored authority boundary)

- **Zero edits under `doctrine/`.** The §50/§51 SoR-write doctrine + the numbering-collision resolution
  are high-capability-class (doctrine) — Seth-only. Raised here propose-only, no doctrine `version:`
  bump.
- No execution-repo code. No promotion of the mission to canonical (gated on the pipeline landing +
  doctrine ratification).
- The canonical-Evergreen Smartsheet integration + PJOB→JOB reconciliation stay deferred (recorded as
  out-of-scope in the mission, not designed).

## Propose-only doctrine flags (for Seth — no `doctrine/*` edit was made)

Echoing mission §16 verbatim-in-substance, for the session-close trail:

1. **SoR-write doctrine candidate** — "ITS as the authoritative writer to an ITS-owned structured
   Smartsheet system-of-record." Candidate text drafted in mission §16(a): one-way-up for accumulating
   logs; bidirectional split-ownership for the Material List; required guards (send-free + AI-free
   GATED daemon, allowlisted egress, margin-checked find-or-create, period-split + archive never
   delete, A2/A3 locks); boundary = ITS-owned SoR only, customer-owned/canonical write-back explicitly
   out of scope.
2. **§-numbering collision (Decision B)** — propose §50 = code-actuation gate, §51 = SoR-write; surface
   the live "both called §50" state in info-gap.
3. **§41 version-bump checklist** — a ready checklist (mission §16(c)) to run if/when Seth ratifies a
   new §: add the section, bump v18→v19 + supersedes + last_verified, footer + v20 trigger, push
   `operational-standards-v19` tag, move the flags to resolved, reconcile the cross-references, lint +
   `doc-reconciliation-auditor`.

## Cross-references

- New mission: [`workstreams/progress-reporting/mission.md`](../workstreams/progress-reporting/mission.md)
- Master plan (authoritative spec): `~/.claude/plans/let-s-go-with-option-greedy-fiddle.md`
- Execution handoff brief: `~/its/docs/cc-brief_progress-reporting-program_2026-06-28.md`
- Execution session log: `~/its/docs/session_logs/2026-06-28_field-ops-progress-reporting-stage0_2.md`
- [memory-archive §G43](../references/memory-archive.md) — program launch + locked decisions + live-lockout root-cause
- [Safety Portal mission v5](../workstreams/safety-portal/mission.md) — the skeleton mirrored + the §50 code-actuation-gate flag (Decision B input)
- [URS Marine portal mission v1](../workstreams/urs-marine-portal/mission.md) — the field-ops data architecture (Decision A input)
- [Foundation Mission v11](../doctrine/foundation-mission.md) · [Operational Standards v18](../doctrine/operational-standards.md)
