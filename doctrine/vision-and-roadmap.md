---
type: doctrine
version: 8
status: canonical
last_verified: 2026-05-29
last_verified_against: 585823d
supersedes: doctrine/vision-and-roadmap.md@v7.2
workstream: null
tags: [phases, ship-and-leave, successor-operator-threshold, customer-2-prep]
---

**ITS Vision ****&**** Roadmap v8**

2026-05-29 — Ship-and-Leave Threshold Defined: Successor-Operator + Tier-3 Escalation

*Ship-and-leave / developer-departure threshold defined in the body (was frontmatter tag only) · cutover target reframed from "runs unattended" to "operated by the Successor-Operator with Seth as Tier-3 escalation asset" · two new hard pre-cutover gates added (Tier-1 self-heal complete; Tier-2 non-developer-safe enforcement layer built) · Phase 1.4 security-hardening precondition unchanged · v7.2 retires*

# Purpose of v8

v8 is a clean integer baseline, retiring the v7.x overlay chain. It carries forward every phase, gate, and precondition from v7.2 unchanged and makes one substantive addition: it defines the ship-and-leave / developer-departure threshold in the body. Until v8, "ship-and-leave" was a frontmatter tag with no operative definition; the implicit reading was "the system runs unattended." That reading is wrong for the post-cutover reality and v8 corrects it.

The cutover target is reframed: ITS after developer departure is not unattended — it is operated by the Successor-Operator (a non-developer at the customer) with Seth, the Developer-Operator, reachable as a Tier-3 escalation asset, not as the primary operator. The three-tier maintenance model (Self-healing → Claude-assisted Successor-Operator repair → escalate to the Developer-Operator) is the operating assumption the cutover threshold is now measured against. See Foundation Mission v10 and Operational Standards v15 for the role definitions and the Tier-2 repair path; this doc holds the threshold and the pre-cutover gates that protect it.

v7.2 retires on acceptance of v8; v8 is the canonical baseline.

# Ship-and-Leave Threshold (Developer-Departure Definition) (NEW in v8)

"Ship-and-leave" does not mean the system runs unattended. It means the Developer-Operator (Seth) has stepped out of the day-to-day operating loop and the system is operated, day to day, by the Successor-Operator — a non-developer at the customer who works only through the Smartsheet UI and approval surfaces, never git, terminal, or code. Claude does the diagnostic and repair work; the Successor-Operator approves it. Seth remains reachable as a Tier-3 escalation asset, not as the primary operator. The three tiers:

- Tier 1 — Self-healing. Daemons recover on their own; the watchdog catches stale state. No human.
- Tier 2 — Claude-assisted Successor-Operator repair. The Successor-Operator approves; Claude drives, through a capability-gated, audit-trailed, guarded path. In scope is the LOW-capability-class set only: re-run a daemon, toggle an ITS_Config value, re-send an approval, re-seed a row, clear a stuck lock.
- Tier 3 — Escalate to the Developer-Operator. Any fault that is NOVEL (no successor-remediation runbook entry covers it) OR HIGH-capability-class (touches the External Send Gate, secrets/auth, doctrine, or requires a code change) escalates to Seth. High-capability-class always escalates regardless of documentation.

The through-line: the same capability-gating philosophy that keeps the AI out of the send path (Foundation Mission Invariant 1, two-process model) is the philosophy that keeps a Tier-2 repair session out of high-class operations. Foundation Mission v10 and Operational Standards v15 hold the role definitions, the escalation boundary, and the Tier-2 repair path in full.

## Crossing the threshold — successor-maintainability criterion (NEW in v8)

The developer-departure line is not crossed on a clock. (Review is permanent, not time-bounded — Foundation Mission Invariant 1.) It is crossed when the system is demonstrably operable by the Successor-Operator with Seth at Tier 3. The criterion:

1. Successor-remediation runbook entries exist for the top fault classes — each written in plain language for the non-developer Successor-Operator (symptom in Smartsheet/alert terms → what the Successor-Operator checks → the Claude prompt or UI action → the escalate-to-Seth condition), authored as each capability was built (the build-time successor-remediation discipline; see Operational Standards v15 §43).
2. The Successor-Operator has demonstrated a set of supervised, Claude-assisted LOW-capability-class repairs (re-run a daemon, toggle a config value, re-send an approval, re-seed a row, clear a stuck lock) — approving each, with Seth observing, before Seth steps out of the loop.
3. The Tier-1 self-heal layer is complete (see Phase 1.5 pre-cutover gates).
4. The Tier-2 non-developer-safe enforcement layer is built (see Phase 1.5 pre-cutover gates).

Criterion 4 names a capability that does not exist today. The verified-live enforcement (capability-gating tests asserting the External Send Gate; the four .claude/hooks guards) is real, but the guard hooks are scoped to subagent/developer sessions and explicitly fall open for the operator's own session — they assume the human in the loop is a developer who can safely override. A guard layer that holds WITHOUT a developer present to adjudicate — the layer Tier-2 non-developer repair requires — must be BUILT. It is a hard pre-cutover gate (Pre-Cutover Condition 5), tracked alongside the Tier-1 Check H self-heal gap below, not a present capability.

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

Phase 1.5 preconditions per Handover Plan v7 (companion doc) now explicitly include the Phase 1.4 hardening cluster as a hard prerequisite. Cutover does not proceed if any Phase 1.4 deliverable is open.

- Pre-Cutover Condition 1: triple-fire CRITICAL alert path has fired on a real issue and been triaged (carried forward from v7.1).

- Pre-Cutover Condition 2 (NEW v7.2): Phase 1.4 security hardening cluster complete — all three deliverables shipped, verified, and tested in sandbox.

- Pre-Cutover Condition 3 (carried from v7.2): Teala-coordinated real-recipient wiring complete — Forefront/PM contacts added to trusted-contacts sheet with Status=ACTIVE.

- Pre-Cutover Condition 4 (NEW v8): Tier-1 self-heal layer complete. The watchdog self-heal coverage — including Check H (heartbeat-staleness, the successor to Check F per Op Stds v15 §2) — is operational, and the 2-of-3 daemons currently heartbeat-pending have landed their heartbeat surface. Check H is an UNMET pre-cutover condition today; this gate makes completing the self-heal layer an explicit prerequisite, not an assumption.

- Pre-Cutover Condition 5 (NEW v8): Tier-2 non-developer-safe enforcement layer built. The guarded, capability-gated, audit-trailed path that lets Claude apply a LOW-capability-class field repair under Successor-Operator approval — without a Developer-Operator present to adjudicate — exists and is tested. This layer DOES NOT EXIST today: the verified-live capability-gating tests and the four .claude/hooks guards are real but assume a developer-grade human in the loop and fall open for the operator's own session. The non-developer-safe layer is a build requirement and a hard cutover gate. It is the operating-side analogue of the two-process External Send Gate (Foundation Mission Invariant 1): the same capability-gating philosophy, applied so a Tier-2 repair session is structurally barred from high-class operations (External Send Gate, secrets/auth, doctrine, code change).

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
| ClamAV signature database not auto-updating on customer Mac | Low | freshclam daemon auto-installs via Homebrew; watchdog Check H (heartbeat staleness) catches stale daemon state. NOTE: Check H is itself an UNMET pre-cutover condition (Tier-1 self-heal, Pre-Cutover Condition 4) — this mitigation is contingent on that gate closing. |
| Trusted-contacts sheet schema needs change after Customer 1 onboarding | Medium | Schema explicitly versioned; column adds non-breaking; column removals require migration script. |
| Managed Agents capability/pricing drift between v7.2 and Phase 3 gate | Medium (carried from v7.1) | Re-verify at gate firing; candidate list is planning input. |
| Tailscale fails post-shipment (carried from v6) | Medium | Tested before shipment; physical access + video-call walkthrough fallback. |
| Watchdog false alarms in first 7 days (carried from v6) | Medium | Day 7 routing change gate. |
| Cutover crosses the ship-and-leave threshold before the Successor-Operator can actually operate it | Medium | Successor-maintainability criterion is an explicit gate (top-fault-class runbook entries exist; Successor-Operator has demonstrated supervised low-class repairs; Tier-1 self-heal complete; Tier-2 non-developer-safe enforcement layer built). Tier-2 enforcement layer is a known pre-cutover gap, not a present capability. |

# Cascade Impact

The v7.1 → v7.2 security-hardening cascade (rows in the provenance table below) landed on 2026-05-22. The v8 threshold-definition bump is part of the three-tier successor-maintenance cascade and its companion impacts are:

| **Doc** | **Cascade absorbed by this v8 bump** |
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

Vision & Roadmap v8, 2026-05-29. Clean integer baseline retiring the v7.x overlay chain. Carries forward every phase, gate, and precondition from v7.2 and adds the body definition of the ship-and-leave / developer-departure threshold: ITS after developer departure is operated by the Successor-Operator with Seth as a Tier-3 escalation asset, gated by a successor-maintainability criterion and two new hard pre-cutover conditions (Tier-1 self-heal complete incl. Check H; Tier-2 non-developer-safe enforcement layer built — a build gap, not a present capability). v7.2 retires on acceptance of v8. The v7.x minor-overlay scheme is retired — frontmatter version and title both read v8. Canonical git tag: vision-and-roadmap-v8.

v9 trigger: the build-everything-in-sandbox bet substantively changes (deferred ship, scope reduction, multi-step ship sequence forced), OR the ship-and-leave threshold / three-tier maintenance model is substantively revised (a tier boundary moves, the successor-maintainability criterion changes, or a pre-cutover gate is added or removed). v8.x absorbs further status updates without phase-plan or threshold changes.

Companion to Foundation Mission v10, Operational Standards v15, Handover Plan v7, Excellence Roadmap v3, FSU v6.5, Memory Archive v5.