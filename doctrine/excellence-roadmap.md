---
type: doctrine
version: 2
status: canonical
last_verified: 2026-05-24
last_verified_against: 3b7d56d
supersedes: doctrine/excellence-roadmap.md@v2.2
workstream: null
tags: [quality-bar, tooling, observability]
---

**ITS Excellence Roadmap v2.3**

2026-05-22 — R4 Closed (Polling Daemon + Operator Visibility) · R5 Opened (Security Hardening)

*Status overlay on v2.2 · Track 1 reliability completion extended through R5 · Tracks 2 + 3 carry forward*

# Purpose of v2.3

Status overlay on Excellence Roadmap v2.2 (2026-05-20 evening). Reflects the closeout of R4 (polling-daemon doctrine + operator-visibility surface) via PRs #59 + #60 on 2026-05-21, and the addition of R5 (pre-Customer-1 security hardening cluster) as a new Track 1 critical-path item between R3 and Phase 1.5 cutover.

Tracks 2 (Quality bar enforcement) and Track 3 (Per-customer customization discipline) carry forward verbatim from v2.2. Grade snapshot refreshed for the post-PR-#60 state.

v2.2 retires on acceptance of v2.3; v2.1 remains canonical baseline; v2.3 is operative reference.

# Track 1 — Reliability Completion (REFRESHED in v2.3)

## Current state — 2026-05-22 afternoon (post-PR-#60 + verification audit)

The 23-PR window of 2026-05-18/19 closed three structural milestones (triple-fire operational, review_queue + quarantine wired, mypy=0 in CI). The 2026-05-20 cascade (PRs #42/#43/#44) closed alert-routing dedupe (R2 closeout). The 2026-05-21 morning + afternoon cascade (PRs #45-#58) closed picklist sync foundation plus R3 Session 1 (intake.py end-to-end). The 2026-05-21 evening cascade (PRs #59 + #60) closed R4 (polling daemon + operator visibility).

Test count trajectory: 137 → 779 (+642, +469% from v2.1 baseline). Ruff clean throughout. mypy zero across 93 source files. 35 PRs landed across 5/18 → 5/21 window (#26 → #60 with PR #34/#41 gaps).

## Track Items

| **Item** | **Status** | **Notes** |
| --- | --- | --- |
| R1 — box_client.py wiring | CLOSED 2026-05-20 via PR #39 (Box OAuth pivot) | OAuth 2.0 User Auth chosen over JWT (Box Platform add-on not licensed). store_tokens Keychain callback critical for refresh-token rotation. |
| R2 — watchdog.py real checks | CLOSED 2026-05-21 via PR #52 (Check G MAINTENANCE-defer) | 6 of 7 checks live (A/B/C/D/F/G). Check E (Anthropic spend trend) deferred to Phase 1.5 — architectural choice, not capability gap. |
| R3 — First workstream consumer integration | PARTIALLY CLOSED 2026-05-21 via PR #57 (Session 1: intake.py end-to-end) | Session 2 (weekly_generate.py) and Session 3 (weekly_send.py) remaining. R3 Session 2 has zero prereqs; next critical-path target. |
| R4 — Polling-daemon doctrine + operator-visibility surface (NEW v2.3) | CLOSED 2026-05-21 via PRs #59 + #60 | safety_reports/intake_poll.py + ITS_Daemon_Health sheet + heartbeat write contract. Codifies emergent pattern (watchdog + picklist_sync were already this shape). Op Stds v11 §31 + §32 hold the doctrine. |
| R5 — Pre-Customer-1 Security Hardening Cluster (NEW v2.3) | OPEN | Three deliverables per V&R v7.2 Phase 1.4: picklist-hardening (~30 min UI + 1 hr audit); ITS_Trusted_Contacts sheet + intake refactor + header-forgery (~half-day); attachment screening Layers 1-3 (~half-day to one-day). Total ~1.5 dedicated day-sessions. Blocks Phase 1.5 cutover. |

# Track 2 — Quality Bar Enforcement (carries forward verbatim from v2.2)

Tooling that turns operational discipline into automation. Survives the white-glove reframe — quality patterns inherited by every customer fork via the blueprint.

- 2.1 — CLAUDE.md as enforced contract. UN-BUILT. LOW-MEDIUM priority. Saves ~30 min per cascade event. Acquires renewed urgency after this 5/22 cascade event (the verification audit caught significant CLAUDE.md drift that an enforced contract would have surfaced earlier).

- 2.2 — Operational Standards as code-level CI assertions. SIGNIFICANT PROGRESS. 8 Op Stds sections now enforced in code (§1, §3, §4, §7, §9, §14, §23+§24, §28). v11's §35 (picklist convention) is a new candidate for CI-assertion conversion. MEDIUM priority. Urgent at next CI tightening pass.

- 2.3 — Session-log convention fold into CLAUDE.md. SELF-ORGANIZING. LOW priority. Triggered at next CLAUDE.md touch — which per this cascade is happening NOW (cc reconciliation handoff in Cascade Unification Update 2026-05-22).

# Track 3 — Per-Customer Customization Discipline (carries forward verbatim from v2.2)

- 3.1 — Multi-tenancy framework: RETIRED (correctly per v2.1 errata). Per-customer-repo invariant subsumes.

- 3.2 — Configuration externalization: REINSTATED. MEDIUM priority. Urgent at first reviewer-chain-override fetcher implementation.

- 3.3 — Blueprint Fork Runbook (was: Customer 2 onboarding playbook): REINSTATED, renamed. MEDIUM priority. Triggered at Customer 2 conversation start; draft in parallel with V&R v7.2 Phase 1.6.

# What v2.3 Explicitly Does NOT Promise

Concrete scope exclusions carry forward verbatim from v2.2:

- Operator surfaces are operator-only. Customer-facing surfaces are workstream-specific (_Pending_Review queues).

- Per-customer-repo invariant means no 'current customer' parameter, no tenant-keyed sheet-ID lookup.

- Blueprint Fork Runbook (3.3) is operator-driven; customer participates at hand-off.

- Each customer engagement is a separate contract, separate handover, separate maintenance arrangement.

- Remote-support model (Tailscale-managed VPN) is what's offered.

# Grade Snapshot (Post-PR-#60 + Verification Audit)

| **Dimension** | **v2.2 grade** | **v2.3 grade** | **Why** |
| --- | --- | --- | --- |
| Architecture & invariant clarity | A | A | Foundation Mission v8 absorbs Invariant 2 6th layer + Layer 1 expansion. Substantive invariant evolution without disturbing the principle. |
| Execution against plan | A | A | 26-PR window now extended to 35-PR window. R1 + R2 + R3 Session 1 + R4 all closed. Test count 137 → 779. |
| Productization readiness (Per-customer customization) | B+ | B+ | Unchanged. Tracks 3.2 + 3.3 unchanged. |
| Reliability completion (Phase 0 closeout) | A | A | R1 + R2 + R4 closed. R3 Session 1 closed (intake.py); Sessions 2+3 + R5 are remaining critical-path items before Phase 1.5 cutover. |
| Documentation discipline | A | A | 8-doc cascade landing 2026-05-22 against verified-from-repo state. Cascade Verification Audit predecessor sets new bar for cascade quality. |
| Quality bar enforcement | B- | B- | Track 2.2 unchanged (8 sections enforced); Track 2.1 (test_doc_pointers) un-built; Track 2.3 self-organizing. §35 picklist convention is a new candidate for 2.2. |

# Authority

Excellence Roadmap v2.3, 2026-05-22. Status overlay on v2.2 absorbing R4 closeout (polling daemon + operator visibility) + R5 opening (security hardening cluster). v2.2 retires on acceptance of v2.3; v2.1 remains canonical baseline; v2.3 is operative reference.

v3 trigger criteria (unchanged): substantive track restructuring or addition of a fundamentally new track. v2.x absorbs further status updates without track-structure changes.

Companion to FM v8, Op Stds v11, V&R v7.2, Handover Plan v6.3, FSU v6.5, Memory Archive v5, Cascade Unification Update 2026-05-22 Security Hardening.