---
type: doctrine
version: 9
status: canonical
last_verified: 2026-06-01
last_verified_against: 585823d
supersedes: doctrine/vision-and-roadmap.md@v8
workstream: null
tags: [phases, ship-and-leave, successor-operator-threshold, training-bounded-co-resolution, customer-2-prep]
---

**ITS Vision ****&**** Roadmap v9**

2026-06-01 — Tier-2 Enforcement Layer Removed from the Threshold: Training-Bounded Co-Resolution

*v9 removes the Tier-2 "non-developer-safe enforcement layer" that v8 named as a hard pre-cutover gate (Pre-Cutover Condition 5 + crossing-criterion 4) and reframes the Tier-2 boundary as training-bounded co-resolution — no structural maintenance enforcement layer exists or is required (FM v11 / Op Stds v16) · the Tier-1 self-heal pre-cutover gate survives, its status corrected (the implemented mechanism is the watchdog Check C marker-file staleness floor — earlier mis-named "Check H" — which already covers all four tracked daemons, plus the live UptimeRobot external ping (audit F16); the lone residual is the weekly_generate Friday-crash catch-up) · the Successor-Operator is redefined as a trained operator who runs Claude Code himself · the ship-and-leave threshold definition and the v7.2 phases/gates carry forward · v8 retires*

# Purpose of v9

v9 modifies the v8 ship-and-leave threshold. The threshold definition, the three-tier model, and v7.2's phases / gates / preconditions all carry forward. v9's substantive change: it removes the Tier-2 "non-developer-safe enforcement layer" that v8 named as a hard pre-cutover gate (Pre-Cutover Condition 5) and the corresponding crossing-criterion, and reframes the Tier-2 boundary as training-bounded co-resolution. This matches the v9 trigger v8 set for itself ("the successor-maintainability criterion changes, or a pre-cutover gate is added or removed"). There is no structural maintenance enforcement layer; none is built or required (FM v11 / Op Stds v16).

The cutover target: ITS after developer departure is not unattended — it is operated by the Successor-Operator (a trained operator who runs Claude Code himself, not a Smartsheet-UI-only approver) with Seth, the Developer-Operator, reachable as a Tier-3 escalation asset, not as the primary operator. The three-tier maintenance model (Self-healing → Claude-assisted Successor-Operator repair → escalate to the Developer-Operator) is the operating assumption the cutover threshold is measured against. See Foundation Mission v11 and Operational Standards v16 for the role definitions and the Tier-2 repair path; this doc holds the threshold and the pre-cutover gates that protect it.

v8 retires on acceptance of v9; v9 is the canonical baseline.

# Ship-and-Leave Threshold (Developer-Departure Definition) (NEW in v8)

"Ship-and-leave" does not mean the system runs unattended. It means the Developer-Operator (Seth) has stepped out of the day-to-day operating loop and the system is operated, day to day, by the Successor-Operator — a trained operator at the customer who runs Claude Code himself and follows the §43 runbooks, but is not a developer (writes no code; does no git/terminal developer-context work) and is not a Smartsheet-UI-only approver. He carries out low-capability-class repairs and escalates the four high-class categories. Seth remains reachable as a Tier-3 escalation asset, not as the primary operator. The three tiers:

- Tier 1 — Self-healing. Daemons recover on their own; the watchdog catches stale state. No human.
- Tier 2 — Claude-assisted Successor-Operator repair. The trained Successor-Operator runs Claude Code himself, following the §43 runbook; the repair is audit-trailed. In scope is the LOW-capability-class set only: re-run a daemon, toggle an ITS_Config value, re-send an approval, re-seed a row, clear a stuck lock. The boundary is held by training + the both-rule + co-resolution, not a structural enforcement layer.
- Tier 3 — Escalate to the Developer-Operator. Any fault that is NOVEL (no successor-remediation runbook entry covers it) OR HIGH-capability-class (touches the External Send Gate, secrets/auth, doctrine, or requires a code change) escalates to Seth. High-capability-class always escalates regardless of documentation.

The through-line: the capability-gating philosophy that keeps the AI out of the send path (Foundation Mission Invariant 1, two-process model) informs how the Tier-2 boundary is drawn — but, unlike that two-process model, the maintenance boundary is not structurally enforced; it is held by training + the both-rule + co-resolution. Foundation Mission v11 and Operational Standards v16 hold the role definitions, the escalation boundary, and the Tier-2 repair path in full.

## Crossing the threshold — successor-maintainability criterion (NEW in v8)

The developer-departure line is not crossed on a clock. (Review is permanent, not time-bounded — Foundation Mission Invariant 1.) It is crossed when the system is demonstrably operable by the Successor-Operator with Seth at Tier 3. The criterion:

1. Successor-remediation runbook entries exist for the top fault classes — each written in plain language for the Successor-Operator (symptom in Smartsheet/alert terms → what the Successor-Operator checks → the Claude prompt or UI action → the escalate-to-Seth condition), authored as each capability was built (the build-time successor-remediation discipline; see Operational Standards v16 §43).
2. The Successor-Operator has demonstrated a set of supervised, Claude-assisted LOW-capability-class repairs (re-run a daemon, toggle a config value, re-send an approval, re-seed a row, clear a stuck lock) — approving each, with Seth observing, before Seth steps out of the loop.
3. The Tier-1 self-heal layer is complete (see Phase 1.5 pre-cutover gates).
4. Tier-2 readiness is met (see Phase 1.5 pre-cutover gates): the §44 low-capability-class action set is implemented as discrete, tested, non-escalating operations, and the Successor-Operator is trained to run Claude Code, follow the runbooks, and recognize and escalate the four high-class categories. (There is no structural enforcement layer — that v8 build gap is removed.)

Criterion 4 is a readiness gate, not a built control. There is no structural "non-developer-safe enforcement layer," and none is required — the v8 framing that named one as a pre-cutover build gap is removed (FM v11 / Op Stds v16). The Tier-2 boundary is held by the trained operator's judgment, the both-rule (novel OR high-class → Tier 3), and co-resolution with the Developer-Operator on the four high-class categories until per-category clearance. The verified-live capability-gating tests and the four .claude/hooks guards remain real, but they protect developer / subagent sessions and fall open for the operator's own session; they are not expected to confine the trained Successor-Operator. The separate Tier-1 self-heal gate (the watchdog Check C marker-file staleness floor — earlier called "Check H") remains a real pre-cutover gate (criterion 3 / Pre-Cutover Condition 4); Check C coverage of all four tracked daemons and the F16 external ping are already operational, so its one remaining unmet leg is the weekly_generate Friday-crash watchdog catch-up.

# Phase Plan (Refreshed Status)

## Phase 0 — Scaffold (COMPLETE)

23-PR window 2026-05-18/19 closed three structural milestones (triple-fire CRITICAL alert path, review_queue + quarantine wired, mypy=0 in CI). 2026-05-20 evening alert-dedupe cascade (PRs #42/#43/#44) closed alert-routing dedupe. Phase 0 → Phase 1 gate at owner-decision boundary.

## Phase 1 — Safety Reports + Parallel Workstreams (ACTIVE)

R3 Session 1 shipped 2026-05-21 (PR #57): safety_reports/intake.py end-to-end live-validated. Polling-daemon trigger + heartbeat surface shipped 2026-05-21 evening (PRs #59 + #60). R3 Session 2 (weekly_generate.py) and R3 Session 3 (weekly_send.py) remaining.

## Phase 1.4 — Pre-Customer-1 Security Hardening (NEW in v7.2)

Inserted between Phase 1 and Phase 1.5 as a named scope. Three deliverables, all required before Phase 1.5 cutover commences.

### Deliverable 1.4.1 — Picklist-Hardening

- Audit every Smartsheet column representing a finite-domain value across all ITS sheets.

- Convert from TEXT_NUMBER to PICKLIST or CHECKBOX. Targets: ITS_Config (system.state, polling_enabled flags), ITS_Errors (Severity), ITS_Review_Queue (Status, urgency), ITS_Quarantine (reason, disposition).

- Codified in Op Stds v11 §35 (standing rule going forward).

- Estimated effort: ~30 min Developer-Operator UI + ~1 hour audit pass. (Picklist conversion and the audit pass are developer-context work — Developer-Operator only; not in the Successor-Operator's Tier-2 set.)

### Deliverable 1.4.2 — Trusted-Contacts Sheet + Header-Forgery Detection

- Build ITS_Trusted_Contacts sheet in System workspace per Op Stds v11 §33 schema.

- Populate with anticipated real-recipient PMs, Forefront contacts, subcontractor addresses (coordinated with Teala).

- Refactor safety_reports/intake.py to query trusted-contacts sheet with scope enforcement.

- Add header-forgery detection (SPF/DKIM/DMARC + Return-Path) via shared/graph_client.py extensions.

- Retire safety_reports.intake.allowed_senders ITS_Config row at cutover.

- Estimated effort: ~half-day session (sheet build + intake refactor + header-forgery wiring + tests).

### Deliverable 1.4.3 — Attachment Screening Pipeline

- Implement Layers 1-3 per Op Stds v11 §34: static signatures + format-aware structural inspection + ClamAV via pyclamd.

- EICAR test fixtures verify pipeline health.

- Integration test against corpus of legitimate DFR samples.

- Layer 4 (VirusTotal) deferred to Phase 2+.

- Estimated effort: ~half-day to one-day session (Developer-Operator-side ClamAV install + code + tests). (Install, code, and tests are developer-context work — Developer-Operator only.)

### Phase 1.4 Gate

All three deliverables verified live in sandbox before Phase 1.5 begins. No Phase 1.5 work commences if any deliverable is open. Sequencing within Phase 1.4: deliverables can run sequentially or in parallel; recommendation is sequential (picklist-hardening first as fastest, then trusted-contacts, then attachment screening) to allow incremental verification.

## Phase 1.5 — Combined Cutover + Hardware Delivery (REVISED PRECONDITIONS)

Phase 1.5 preconditions per Handover Plan v8 (companion doc) now explicitly include the Phase 1.4 hardening cluster as a hard prerequisite. Cutover does not proceed if any Phase 1.4 deliverable is open.

- Pre-Cutover Condition 1: triple-fire CRITICAL alert path has fired on a real issue and been triaged (carried forward from v7.1).

- Pre-Cutover Condition 2 (NEW v7.2): Phase 1.4 security hardening cluster complete — all three deliverables shipped, verified, and tested in sandbox.

- Pre-Cutover Condition 3 (carried from v7.2): Teala-coordinated real-recipient wiring complete — Forefront/PM contacts added to trusted-contacts sheet with Status=ACTIVE.

- Pre-Cutover Condition 4 (NEW v8): Tier-1 self-heal layer complete. The watchdog Check C marker-file staleness floor (the implemented mechanism earlier mis-named "Check H", successor to Check F per Op Stds v16 §2) covers ALL FOUR tracked daemons (safety_intake, safety_weekly_send_poll, safety_weekly_generate, safety_picklist_audit) with per-job freshness windows, and the external UptimeRobot heartbeat ping (audit F16) is operational as the dead-man's switch for total-host failure. The lone residual: weekly_generate runs on StartCalendarInterval (Friday 14:00), so a crashed Friday cycle is detected by Check C (8-day window) but not auto-recovered by launchd until next Friday; the watchdog-side catch-up recovery closing that gap is the remaining build item. This gate makes completing that catch-up an explicit prerequisite — the all-daemon Check C coverage and the F16 ping legs are already operational, so once the catch-up lands, Condition 4 is met.

- Pre-Cutover Condition 5 (REVISED v9 — was "Tier-2 enforcement layer built"): Tier-2 readiness. The §44 low-capability-class action set (re-run a daemon, toggle an ITS_Config value, re-send an approval, re-seed a row, clear a stuck lock) is implemented as discrete, tested, non-escalating operations; §43 successor-remediation runbooks exist for the top fault classes; and the Successor-Operator (Daniel) is trained to run Claude Code, follow the runbooks, and recognize and escalate the four high-class categories (External Send Gate, secrets/auth, doctrine, code changes), having demonstrated supervised, Claude-assisted low-class repairs. There is NO structural "non-developer-safe enforcement layer" — that v8 build gap is removed (FM v11 / Op Stds v16); the Tier-2 boundary is held by training + the both-rule + co-resolution with the Developer-Operator until per-category clearance. Cutover does not proceed until Tier-2 readiness is met.

## Phase 1.6 — Blueprint Generalization (Unchanged)

Carries forward from v7. Pre-Customer-2 pass; extracts Customer-0-specific assumptions from shared/* so a Customer 2 fork-and-customize cycle is mechanical.

## Phase 2 / 3 / 4 (Unchanged)

Carry forward from v7.1. POs / Subcontracts (Phase 2); Email Triage / AI Employee (Phase 3); Renewables-specific surfaces (Phase 4). Phase 3+ Evaluation Triggers section for Managed Agents framing carries forward verbatim.

# Phase 3+ Evaluation Triggers

Carries forward from v7.1. Managed Agents architectural fit framing for specific candidate workstreams (Closeout Package Assembly, Schedule Digest, Dreaming, ITS Chat backend re-evaluation). All four candidates considered at a single Phase 3 evaluation gate per Op Stds v11 §29.

# Risks

Carries forward from v7.1 with one new entry.

| **Risk** | **Likelihood** | **Mitigation** |
| --- | --- | --- |
| Real-recipient wiring before security hardening completes | Medium | Phase 1.4 gate explicit; Teala coordination scheduled AFTER Phase 1.4 deliverables verified. |
| ClamAV signature database not auto-updating on customer Mac | Low | freshclam daemon auto-installs via Homebrew; the watchdog Check C marker-file staleness floor catches stale daemon state. NOTE: Check C coverage of all tracked daemons is operational; the only open Tier-1 leg (Pre-Cutover Condition 4) is the weekly_generate Friday-crash catch-up. |
| Trusted-contacts sheet schema needs change after Customer 1 onboarding | Medium | Schema explicitly versioned; column adds non-breaking; column removals require migration script. |
| Managed Agents capability/pricing drift between v7.2 and Phase 3 gate | Medium (carried from v7.1) | Re-verify at gate firing; candidate list is planning input. |
| Tailscale fails post-shipment (carried from v6) | Medium | Tested before shipment; physical access + video-call walkthrough fallback. |
| Watchdog false alarms in first 7 days (carried from v6) | Medium | Day 7 routing change gate. |
| Cutover crosses the ship-and-leave threshold before the Successor-Operator can actually operate it | Medium | Successor-maintainability criterion is an explicit gate (top-fault-class runbook entries exist; Successor-Operator has demonstrated supervised low-class repairs; Tier-1 self-heal complete; Tier-2 readiness met — low-class action set implemented + §43 runbooks + trained operator). The Tier-2 boundary is training-enforced (training + both-rule + co-resolution); there is no structural enforcement layer. |

# Cascade Impact

The v9 de-1b bump removes the Tier-2 "non-developer-safe enforcement layer" across the doctrine set (it was named, in the v8 cascade below, as a pre-cutover build gap) and reframes the Tier-2 boundary as training-bounded co-resolution. Its companion impacts:

| **Doc** | **Cascade absorbed by this v9 bump** |
| --- | --- |
| Foundation Mission v10 → v11 | Through-line reframed to end at philosophy, not a built control; the "non-developer-safe enforcement layer" framing removed; Successor-Operator redefined as a trained CC operator. Substantive companion. |
| Operational Standards v15 → v16 | §44's Tier-2 boundary recharacterized from structural (enforcement-layer build gap) to training-enforced (trained operator + both-rule + co-resolution); role redefinition; §43 / both-rule / capability-class sets unchanged. Substantive companion. |
| Handover Plan v7 → v8 | Tier-2 enforcement-layer pre-cutover condition removed, replaced by a Tier-2 readiness gate; Successor-Operator redefined; Tier-1 self-heal gate retained. Companion. |
| Excellence Roadmap v3 → v4 | R6 sub-deliverable (b) (Tier-2 enforcement layer) replaced by Tier-2 readiness work; (a) self-heal + (c) runbook tooling retained. Companion. |
| references/permissions.md, references/system-hr-handoff.md | Their Successor-Operator descriptions ("non-developer / Smartsheet-UI-only / never terminal") predate this reframe; a role-redefinition follow-on is pending (out of scope for this cascade). |
| Memory Archive | Append §G<next> recording the de-1b reframe (training-bounded co-resolution). Companion (append-only). |

## Prior cascade — v8 (2026-05-29 Three-Tier Successor-Maintenance), retained for provenance

The v8 bump defined the ship-and-leave threshold and named the Tier-2 non-developer-safe enforcement layer as a pre-cutover build gap (removed in v9). Its companion impacts were:

| **Doc** | **Cascade absorbed by the v8 bump** |
| --- | --- |
| Foundation Mission v9 → v10 | Developer-Operator / Successor-Operator role principle; capability-gating through-line from Invariant 1 to Tier-2 gating; non-developer-safe enforcement layer named as a pre-cutover build gap. Substantive companion. |
| Operational Standards v14 → v15 | §43 (successor-remediation documentation discipline, parallel to §42 but for the non-developer audience); §44 (Tier-2 repair path + low/high capability-class sets + enforcement build gap); §§37-41 role-tagging; §2 watchdog fail-open-to-signal note. Substantive companion. |
| Handover Plan v6.3 → v7 | Three-tier fault-response model; Developer-Operator / Successor-Operator role definitions; Tier-2/Tier-3 escalation boundary; Pre-Cutover Conditions (Tier-1 self-heal complete; Tier-2 enforcement built). Companion. |
| Excellence Roadmap v2.3 → v3 | R6 successor-maintenance build program added as a Track 1 critical-path cluster; "Solution Smith remains primary operator" contradiction resolved to the Developer-Operator-as-Tier-3-asset framing. Companion. |
| references/permissions.md v4 → v5, references/system-hr-handoff.md v5 → v6 | "Solution Smith remains primary operator" / "trained, developer-grade maintainer" framing reframed to the non-developer Successor-Operator + Claude model with Seth at Tier 3. Companion. |
| references/worktree-discipline.md → v1 | Symlink fail-open promoted toward a watchdog-detectable signal (G6). Companion. |
| Memory Archive | Append §G<next> recording the threshold-definition cascade and the three-tier model. Companion (append-only). |

## Prior cascade — v7.1 → v7.2 (2026-05-22 Security Hardening), retained for provenance

| **Doc** | **Cascade absorbed by the v7.2 bump** |
| --- | --- |
| Foundation Mission v7.1 → v8 | Invariant 2 Layer 6 added (attachment screening); Layer 1 revised (trusted-contacts + header-forgery). Substantive companion. |
| Operational Standards v10.1 → v11 | Five new sections (§§31-35) + §36 in-repo tech debt + existing-section edits. Substantive companion. |
| Handover Plan v6.2 → v6.3 | Step 8 + Pre-Cutover + Risk Inventory updates for Phase 1.4 hardening. Companion. |
| Excellence Roadmap v2.2 → v2.3 | R4 (polling daemon + operator visibility) closed; R5 (security hardening cluster) opened. Companion. |
| Foundation Scaffold Update v6.4 → v6.5 | PR window through #60; box_migration/ + smartsheet_migration/ first-time enumeration. Companion. |
| Memory Archive v4 → v5 | Operational detail through 2026-05-22 absorbed. Companion. |
| Workstream Mission/Brief docs | Pointer drift only. Mail.app references deprecated per Op Stds v11 §31; refresh at next natural workstream cascade. |

# Authority

Vision & Roadmap v9, 2026-06-01. v9 removes the Tier-2 "non-developer-safe enforcement layer" that v8 named as a hard pre-cutover gate (Pre-Cutover Condition 5 + crossing-criterion 4) and reframes the Tier-2 boundary as training-bounded co-resolution: there is no structural maintenance enforcement layer; none is built or required (FM v11 / Op Stds v16). The Successor-Operator is redefined as a trained operator who runs Claude Code himself. The Tier-1 self-heal pre-cutover gate (Condition 4) survives unchanged in scope; its stale "Check H" status characterization is corrected in a v9.x absorption (below). Condition 5 is replaced by a Tier-2 readiness gate. The ship-and-leave threshold definition and v7.2's phases / gates / preconditions carry forward. v8 retires on acceptance of v9; v9 is the canonical baseline. Canonical git tag: vision-and-roadmap-v9.

v9 was triggered by exactly the criterion v8 set for itself — a pre-cutover gate removed and the successor-maintainability criterion changed (the Tier-2 enforcement-layer gate → a Tier-2 readiness gate). Tag pushed post-merge: `vision-and-roadmap-v9`.

v9.x status absorption (2026-06-01, verified against exec 585823d): the Tier-1 self-heal pre-cutover gate's (Condition 4) characterization is corrected. Prior docs described the mechanism as a separate, unimplemented "Check H heartbeat-staleness" check with "2 of 3 daemons heartbeat-pending"; **that framing was inaccurate.** The implemented staleness floor is, and has been, the watchdog **Check C marker-file** check (`scripts/watchdog.py`), which already covers all four tracked daemons (safety_intake, safety_weekly_send_poll, safety_weekly_generate, safety_picklist_audit) with per-job freshness windows; the external **UptimeRobot** heartbeat ping (audit F16) is live as the total-host dead-man's switch. The lone residual is the weekly_generate Friday-crash **catch-up recovery** (exec follow-on — `weekly_generate` is calendar-scheduled, so a crashed Friday cycle is detected by Check C but not auto-recovered by launchd until next Friday). Per the v10 trigger this is a **status update absorbed within the v9 line** (no phase-plan, threshold, or gate change — the gate and its scope are unchanged, only the status text is corrected); **no version bump, no new tag.** The prior "Check H" framing is recorded here for provenance, not blind-deleted.

v10 trigger: the build-everything-in-sandbox bet substantively changes (deferred ship, scope reduction, multi-step ship sequence forced), OR the ship-and-leave threshold / three-tier maintenance model is substantively revised (a tier boundary moves, the successor-maintainability criterion changes, or a pre-cutover gate is added or removed). v9.x absorbs further status updates without phase-plan or threshold changes.

Companion to Foundation Mission v11, Operational Standards v19, Handover Plan v9, Excellence Roadmap v4, FSU v6.5, Memory Archive v5.