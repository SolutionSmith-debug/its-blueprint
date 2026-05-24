---
type: doctrine
version: 7
status: canonical
last_verified: 2026-05-24
last_verified_against: 3b7d56d
supersedes: doctrine/vision-and-roadmap.md@v7.1
workstream: null
tags: [phases, ship-and-leave, customer-2-prep]
---

**ITS Vision ****&**** Roadmap v7.2**

2026-05-22 — Phase 1.5 Security Hardening Precondition

*Status overlay on v7.1 · Pre-Customer-1 security hardening cluster gated before cutover · v7.1 retires*

# Purpose of v7.2

Status overlay on Vision & Roadmap v7.1 (2026-05-20). Single substantive change: Phase 1.5 (combined cutover + hardware delivery) now requires the pre-Customer-1 security hardening cluster (trusted-contacts sheet + attachment screening pipeline + picklist-hardening) as a precondition. Without these, cutover ships a vulnerable intake pipeline to California.

v7.1 retires on acceptance of v7.2; v7 remains canonical baseline; v7.2 is operative reference.

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

- Estimated effort: ~30 min operator UI + ~1 hour audit pass.

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

- Estimated effort: ~half-day to one-day session (operator-side ClamAV install + code + tests).

### Phase 1.4 Gate

All three deliverables verified live in sandbox before Phase 1.5 begins. No Phase 1.5 work commences if any deliverable is open. Sequencing within Phase 1.4: deliverables can run sequentially or in parallel; recommendation is sequential (picklist-hardening first as fastest, then trusted-contacts, then attachment screening) to allow incremental verification.

## Phase 1.5 — Combined Cutover + Hardware Delivery (REVISED PRECONDITIONS)

Phase 1.5 preconditions per Handover Plan v6.3 (companion doc) now explicitly include the Phase 1.4 hardening cluster as a hard prerequisite. Cutover does not proceed if any Phase 1.4 deliverable is open.

- Pre-Cutover Condition 1: triple-fire CRITICAL alert path has fired on a real issue and been triaged (carried forward from v7.1).

- Pre-Cutover Condition 2 (NEW v7.2): Phase 1.4 security hardening cluster complete — all three deliverables shipped, verified, and tested in sandbox.

- Pre-Cutover Condition 3 (NEW v7.2): Teala-coordinated real-recipient wiring complete — Forefront/PM contacts added to trusted-contacts sheet with Status=ACTIVE.

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
| ClamAV signature database not auto-updating on customer Mac | Low | freshclam daemon auto-installs via Homebrew; watchdog Check H (heartbeat staleness) catches stale daemon state. |
| Trusted-contacts sheet schema needs change after Customer 1 onboarding | Medium | Schema explicitly versioned; column adds non-breaking; column removals require migration script. |
| Managed Agents capability/pricing drift between v7.2 and Phase 3 gate | Medium (carried from v7.1) | Re-verify at gate firing; candidate list is planning input. |
| Tailscale fails post-shipment (carried from v6) | Medium | Tested before shipment; physical access + video-call walkthrough fallback. |
| Watchdog false alarms in first 7 days (carried from v6) | Medium | Day 7 routing change gate. |

# Cascade Impact

| **Doc** | **Cascade absorbed by this v7.2 bump** |
| --- | --- |
| Foundation Mission v7.1 → v8 | Invariant 2 Layer 6 added (attachment screening); Layer 1 revised (trusted-contacts + header-forgery). Substantive companion. |
| Operational Standards v10.1 → v11 | Five new sections (§§31-35) + §36 in-repo tech debt + existing-section edits. Substantive companion. |
| Handover Plan v6.2 → v6.3 | Step 8 + Pre-Cutover + Risk Inventory updates for Phase 1.4 hardening. Companion. |
| Excellence Roadmap v2.2 → v2.3 | R4 (polling daemon + operator visibility) closed; R5 (security hardening cluster) opened. Companion. |
| Foundation Scaffold Update v6.4 → v6.5 | PR window through #60; box_migration/ + smartsheet_migration/ first-time enumeration. Companion. |
| Memory Archive v4 → v5 | Operational detail through 2026-05-22 absorbed. Companion. |
| Workstream Mission/Brief docs | Pointer drift only. Mail.app references deprecated per Op Stds v11 §31; refresh at next natural workstream cascade. |

# Authority

Vision & Roadmap v7.2, 2026-05-22. Status overlay on v7.1 absorbing Phase 1.4 security-hardening precondition. v7 remains canonical baseline; v7.2 is operative reference.

v8 trigger criteria (unchanged from v7): the build-everything-in-sandbox bet substantively changes (deferred ship, scope reduction, multi-step ship sequence forced). v7.x absorbs further status updates without phase-plan changes.