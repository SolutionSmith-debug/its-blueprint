---
type: doctrine
version: 3
status: canonical
last_verified: 2026-05-29
last_verified_against: 585823d
supersedes: doctrine/excellence-roadmap.md@v2.3
workstream: null
tags: [quality-bar, tooling, observability, successor-maintenance]
---

**ITS Excellence Roadmap v3**

2026-05-29 — R6 Opened (Successor-Maintenance Build Program) · maintenance model reframed: Developer-Operator (Seth) = Tier-3 escalation asset, not standing operator

*Major bump from v2.3 · Track 1 reliability completion extended through R6 (successor-maintenance build program) · Tracks 2 + 3 carry forward, Track 3 remote-support exclusion reframed*

# Purpose of v3

Major bump from Excellence Roadmap v2.3 (2026-05-22). v3 (a) adds R6 — the successor-maintenance build program — as a new Track 1 critical-path cluster, and (b) reframes the post-handover maintenance model in the Track 3 scope-exclusions to align with the three-tier successor-maintenance model: the Developer-Operator (Seth) is a Tier-3 escalation asset, not the standing daily operator.

v3 also reconciles this doc's frontmatter integer and title to a single bare-integer version (G7), retiring the v2.x minor-overlay scheme.

The R4/R5 closeout and security-hardening additions carried by v2.3 stand verbatim. Tracks 2 (Quality bar enforcement) and Track 3 (Per-customer customization discipline) carry forward from v2.3 except for the remote-support / operator-driven-runbook reframes called out below. Grade snapshot carries forward.

v2.3 retires on acceptance of v3; v2.1 remains canonical baseline; v3 is operative reference.

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
| R6 — Successor-Maintenance Build Program (NEW v3) | OPEN | The build work the three-tier successor-maintenance model requires before the Developer-Operator can step back to a Tier-3-only role. Three sub-deliverables, all pre-Phase-1.5-cutover (hard gates per Handover Plan v7 + V&R v8): (a) **Tier-1 self-heal completion** — the watchdog heartbeat-staleness floor must see all daemons (Check H is an UNMET pre-cutover condition; `watchdog` + `picklist_sync` are retrofit-pending, only `intake_poll` writes a heartbeat today); (b) **Tier-2 non-developer-safe enforcement layer** — a guarded, capability-gated path that lets Claude drive a Successor-Operator-approved field repair (the LOW-capability-class set only: re-run a daemon, toggle an ITS_Config value, re-send an approval, re-seed a row, clear a stuck lock) while STRUCTURALLY forbidding HIGH-capability-class operations (External Send Gate, secrets/auth, doctrine, anything requiring a code change). **This enforcement layer does not exist today** — the real capability-gating (`tests/test_capability_gating.py`) and the four guard hooks are scoped to subagent/developer sessions and fall open for the operator's own session, assuming a developer-in-loop who can safely override. Building a guard layer that holds WITHOUT a Developer-Operator present to adjudicate is the open work; (c) **Successor-remediation runbook tooling** — the build-time discipline (Op Stds v15 §43) and authoring substrate for plain-language remediation entries shipped as Markdown with the capability (Claude-read; Smartsheet/alert-keyed in content), aimed at the non-developer Successor-Operator (parallel to, and distinct from, Op Stds §42 code-docstrings). Through-line: the same capability-gating philosophy that keeps the AI out of the send path (Foundation Mission Invariant 1 two-process model) is the philosophy this Tier-2 layer extends to keep a repair session out of high-class operations. Cross-referenced as a pre-cutover gap alongside the Check H self-heal condition. Blocks Phase 1.5 cutover. |

# Track 2 — Quality Bar Enforcement (carries forward verbatim from v2.2)

Tooling that turns operational discipline into automation. Survives the white-glove reframe — quality patterns inherited by every customer fork via the blueprint.

- 2.1 — CLAUDE.md as enforced contract. UN-BUILT. LOW-MEDIUM priority. Saves ~30 min per cascade event. Acquires renewed urgency after this 5/22 cascade event (the verification audit caught significant CLAUDE.md drift that an enforced contract would have surfaced earlier).

- 2.2 — Operational Standards as code-level CI assertions. SIGNIFICANT PROGRESS. 8 Op Stds sections now enforced in code (§1, §3, §4, §7, §9, §14, §23+§24, §28). v11's §35 (picklist convention) is a new candidate for CI-assertion conversion. MEDIUM priority. Urgent at next CI tightening pass.

- 2.3 — Session-log convention fold into CLAUDE.md. SELF-ORGANIZING. LOW priority. Triggered at next CLAUDE.md touch — which per this cascade is happening NOW (cc reconciliation handoff in Cascade Unification Update 2026-05-22).

# Track 3 — Per-Customer Customization Discipline (carries forward verbatim from v2.2)

- 3.1 — Multi-tenancy framework: RETIRED (correctly per v2.1 errata). Per-customer-repo invariant subsumes.

- 3.2 — Configuration externalization: REINSTATED. MEDIUM priority. Urgent at first reviewer-chain-override fetcher implementation.

- 3.3 — Blueprint Fork Runbook (was: Customer 2 onboarding playbook): REINSTATED, renamed. MEDIUM priority. Triggered at Customer 2 conversation start; draft in parallel with V&R v7.2 Phase 1.6.

# What v3 Explicitly Does NOT Promise

Concrete scope exclusions carry forward from v2.3, except the maintenance-model lines reframed in v3 (Developer-Operator as Tier-3 asset, not standing operator):

- Operator surfaces are operator-only. Customer-facing surfaces are workstream-specific (_Pending_Review queues).

- Per-customer-repo invariant means no 'current customer' parameter, no tenant-keyed sheet-ID lookup.

- Blueprint Fork Runbook (3.3) is **Developer-Operator-driven** (git / CC / shell / `gh api` / migration / worktree work — see Op Stds v15 §§37-41); the customer participates at hand-off. The non-developer Successor-Operator does not run fork-setup steps; those are Developer-Operator-only by capability class.

- Each customer engagement is a separate contract, separate handover, separate maintenance arrangement. The intended steady-state maintenance arrangement is the three-tier successor-maintenance model: Tier 1 self-heal, Tier 2 Successor-Operator + Claude repair within the low-capability-class set, Tier 3 escalation to the Developer-Operator (Seth) as a reachable asset.

- Remote support (Tailscale-managed VPN) is a Tier-3 escalation channel for the Developer-Operator (Seth), **not** the primary ongoing-operation model. Seth is a reachable escalation asset; steady-state operation is Tier 1 (self-heal) and Tier 2 (Successor-Operator + Claude). The earlier framing that positioned remote support / "Solution Smith remains primary operator" as the standing maintenance model is superseded by the three-tier model (reconcile `references/permissions.md` §3.2 "Solution Smith remains primary operator" in the same cascade).

# Grade Snapshot (Post-PR-#60 + Verification Audit)

| **Dimension** | **v2.2 grade** | **v2.3 grade** | **Why** |
| --- | --- | --- | --- |
| Architecture & invariant clarity | A | A | Foundation Mission v8 absorbs Invariant 2 6th layer + Layer 1 expansion. Substantive invariant evolution without disturbing the principle. |
| Execution against plan | A | A | 26-PR window now extended to 35-PR window. R1 + R2 + R3 Session 1 + R4 all closed. Test count 137 → 779. |
| Productization readiness (Per-customer customization) | B+ | B+ | Unchanged. Tracks 3.2 + 3.3 unchanged. |
| Reliability completion (Phase 0 closeout) | A | A | R1 + R2 + R4 closed. R3 Session 1 closed (intake.py); Sessions 2+3, R5, and R6 (successor-maintenance build program — incl. the not-yet-built Tier-2 non-developer-safe enforcement layer and Tier-1 self-heal completion) are remaining critical-path items before Phase 1.5 cutover. |
| Documentation discipline | A | A | 8-doc cascade landing 2026-05-22 against verified-from-repo state. Cascade Verification Audit predecessor sets new bar for cascade quality. |
| Quality bar enforcement | B- | B- | Track 2.2 unchanged (8 sections enforced); Track 2.1 (test_doc_pointers) un-built; Track 2.3 self-organizing. §35 picklist convention is a new candidate for 2.2. |

# Authority

Excellence Roadmap v3, 2026-05-29. Major bump from v2.3, adding R6 (successor-maintenance build program) as a new Track 1 critical-path cluster and reframing the post-handover maintenance model in the Track 3 scope-exclusions: remote support is a Tier-3 escalation channel for the Developer-Operator (Seth), not the primary ongoing-operation model. Frontmatter integer and title reconciled to a single bare-integer version (v3) per Gap G7; the v2.x minor-overlay scheme is retired. v2.3 retires on acceptance of v3; v2.1 remains canonical baseline; v3 is operative reference. Canonical git tag: `excellence-roadmap-v3`.

v4 trigger criteria: substantive track restructuring or addition of a fundamentally new track. Status updates without track-structure changes are absorbed in-place at v3 (no minor-overlay; frontmatter and title stay equal per G7).

Companion to FM v10, Op Stds v15, V&R v8, Handover Plan v7, FSU v6.5, Memory Archive v5, Successor-Maintenance Model Audit 2026-05-29.