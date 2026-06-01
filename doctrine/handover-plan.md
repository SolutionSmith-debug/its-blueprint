---
type: doctrine
version: 8
status: canonical
last_verified: 2026-06-01
last_verified_against: 585823d
supersedes: doctrine/handover-plan.md@v7
workstream: null
tags: [california-cutover, hardware-handoff, permissions, successor-operator, training-bounded-co-resolution]
---

**ITS Handover Plan v8**

2026-06-01 — Tier-2 Enforcement Layer Removed; Successor-Operator = Trained CC Operator

*Modifies the v7 three-tier model · the Tier-2 "non-developer-safe enforcement layer" pre-cutover build gap is REMOVED (no structural maintenance enforcement layer exists or is required) · the Tier-2 boundary is held by training + the both-rule + co-resolution with the Developer-Operator until per-category clearance · the Successor-Operator is redefined as a TRAINED operator who runs Claude Code himself (not a Smartsheet-UI-only approver) · the Tier-1 self-heal pre-cutover gate (Check H) survives unchanged · v7's model, roles, escalation boundary, and Step 8/Day-7 reframes carry forward*

# Purpose of v8

v8 modifies the three-tier fault-response model that v7 established. v7's model, the Developer-Operator / Successor-Operator role pair, the Tier-2/Tier-3 escalation boundary, the Step 8 and Day-7 reframes, and the Tier-1 self-heal pre-cutover gate all carry forward. v8 makes two changes: it removes the Tier-2 "non-developer-safe enforcement layer" that v7 named as a hard pre-cutover build gap (there is no structural maintenance enforcement layer; none is built or required — see FM v11 / Op Stds v16), and it redefines the Successor-Operator from a Smartsheet-UI-only approver to a trained operator who runs Claude Code himself, follows the §43 runbooks, and escalates the four high-class categories.

The three-tier model as it now stands: (1) Tier 1 self-heal; (2) two named operator roles — Developer-Operator (Seth) and the trained Successor-Operator; (3) the Tier-2/Tier-3 "both" rule over the four high-class categories (External Send Gate, secrets/auth, doctrine, code changes) — the structural *definition* of high-class stands; only the idea of *structurally enforcing* it at Tier 2 is removed, replaced by training + co-resolution; (4) Step 8 acceptance + Day-7 routing to the Successor-Operator with Seth at Tier 3; (5) pre-cutover conditions — the Tier-1 self-heal gate (real) plus a Tier-2 *readiness* gate (the §44 low-class action set implemented + §43 runbooks + trained-operator/demonstrated-repair). The v7 Tier-2 enforcement-layer build gap is removed.

v7 retires on acceptance of v8. v8 is the canonical baseline and operative reference (frontmatter version and title both read v8). v9 trigger: a further structural change to the cutover runbook or the fault-response model.

# What Changed in v8

v8 removes the Tier-2 "non-developer-safe enforcement layer" that v7 named as a hard pre-cutover build gap and redefines the Successor-Operator. v7's three-tier model, role pair, escalation boundary, Step 8 / Day-7 reframes, and the Tier-1 self-heal pre-cutover gate all carry forward.

- Tier-2 boundary — reframed from "structurally enforced by a to-be-built non-developer-safe enforcement layer" to "held by the trained operator's judgment + the both-rule + co-resolution with the Developer-Operator until per-category clearance." No structural maintenance enforcement layer exists or is required (FM v11 / Op Stds v16).

- Successor-Operator — redefined from a Smartsheet-UI-only approver who never touches a terminal to a TRAINED operator who runs Claude Code himself, follows the §43 runbooks, carries out the low-class repair set, and escalates the four high-class categories. Still a non-developer (no code; no §§37-41 developer-context work).

- Pre-Cutover Conditions — the v7 "Tier-2 non-developer-safe enforcement layer built" condition is REMOVED and replaced by a Tier-2 *readiness* condition (low-class action set implemented + §43 runbooks + trained-operator/demonstrated-repair). The Tier-1 self-heal condition (Check H) survives unchanged as a standalone gate; the v7 "both must be built" coupling is gone.

- The high-capability-class *definition* (External Send Gate / secrets-auth / doctrine / code change) and the "both" escalation rule are unchanged; only the structural *enforcement* of the boundary at Tier 2 is removed.

- Cross-references refreshed: Op Stds v15 → v16, Foundation Mission v10 → v11, V&R v8 → v9, Excellence Roadmap v3 → v4.

- v7's three-tier model, roles, escalation boundary, and Step 8/Day-7 reframes, plus v6.3's Phase 1.4 hardening additions, carry forward. Step 1-7 carry forward verbatim from v6.2.

# Operator Roles (NEW v7)

Post-cutover, two operator roles are named and used identically across this plan and its companion docs. Every "operator" usage elsewhere must be classifiable to exactly one of these.

- **Developer-Operator** (Solution Smith / Seth). git-, Claude-Code-, shell-, and worktree-fluent. Performs ALL developer-context operations: everything in Op Stds v16 §§37-41 (gh api, gitleaks, migrations, worktree cleanup, code changes), Keychain access, and running scripts directly. Post-cutover the Developer-Operator is a reachable Tier-3 escalation ASSET — not the day-to-day operator.

- **Successor-Operator** (the customer-side trained operator who owns the running system day to day). A non-developer — writes no code, performs none of the Op Stds v16 §§37-41 developer-context operations — but he **runs Claude Code himself**, follows the §43 remediation runbooks/checklists, and carries out the low-capability-class repair set. He is trained to recognize and escalate the four high-class categories (External Send Gate, secrets/auth, doctrine, code changes), which co-resolve with the Developer-Operator until per-category clearance. He is not a Smartsheet-UI-only approver rubber-stamping Claude-driven actions.

This pair replaces the earlier framing in which a "trained maintainer" was assumed to acquire maintainer-level system understanding and in which Solution Smith "remains primary operator" indefinitely (references/system-hr-handoff.md, references/permissions.md §3.2, excellence-roadmap.md). Companion docs are reconciled to these two roles.

# Fault-Response Model (NEW v7)

After Solution Smith hands the system over, a fault resolves through three tiers. The tier is determined by the fault, not by who happens to notice it.

## Tier 1 — Self-Heal

The system recovers on its own: daemons restart, the watchdog catches a stalled heartbeat, no human is involved. This tier is partly built. Watchdog Check H (heartbeat staleness, successor to Check F per Op Stds v16 §2) is the load-bearing mechanism, and as of 585823d it is an UNMET pre-cutover condition — operational for one daemon's pattern but not yet across all daemons (2 of 3 daemons are heartbeat-pending). Completing the self-heal layer is a pre-cutover requirement (see Pre-Cutover Conditions).

## Tier 2 — Claude-Assisted Successor-Operator Repair

Where Tier 1 does not recover, the trained Successor-Operator runs Claude Code himself and, following the §43 runbook, carries out a low-capability-class repair — escalating anything novel or high-class to Tier 3. He is a non-developer (writes no code, performs none of the §§37-41 developer-context operations), but he operates CC under the runbook rather than rubber-stamping a Claude-driven action.

In-scope Tier-2 repairs are the LOW-capability-class set ONLY:

- re-run a stalled daemon;
- toggle an ITS_Config value (within picklist-enforced bounds);
- re-send an already-approved row;
- re-seed a missing reference row;
- clear a stuck lock.

Each in-scope repair ships with a plain-language successor-remediation runbook entry (symptom in Smartsheet/alert terms -> what the Successor-Operator checks -> the Claude prompt or UI action -> the escalate-to-Seth condition), written as the capability is built and shipped as Markdown alongside the capability that Claude loads to drive the repair. That runbook discipline is a build-time deliverable parallel to — and distinct from — Op Stds v16 §42 code-level self-documentation, whose audience is code-readers, not the Successor-Operator (see Op Stds v16 §43).

Through-line. The capability-gating philosophy that keeps the AI out of the send path — the two-process External Send Gate (Foundation Mission v11 Invariant 1, the generation process cannot import send capability, enforced by tests/test_capability_gating.py) — informs how the Tier-2 maintenance boundary is DRAWN: why the External Send Gate, secrets/auth, doctrine, and code changes are off-limits at Tier 2. But unlike Invariant 1's two-process model, the maintenance boundary is NOT structurally enforced and no structural enforcement layer is built or required. It holds by the trained operator's judgment, the both-rule (novel OR high-class → Tier 3), and co-resolution with the Developer-Operator on the four high-class categories until per-category clearance is granted. There is no non-developer-safe enforcement layer; the trained-operator-plus-co-resolution model is the chosen control. Cutover's Tier-2 readiness gate (see Pre-Cutover Conditions) is the §43 runbooks + the §44 low-class action set + demonstrated supervised repair — not a built enforcement layer.

## Tier 3 — Escalate to the Developer-Operator

Seth is a reachable escalation asset. A fault escalates to Tier 3 when it is NOVEL or HIGH-capability-class.

The "both" rule:

- A fault is Tier 2 only if it is documented (covered by a successor-remediation runbook entry) AND low-capability-class.
- A fault is Tier 3 if it is novel (no runbook entry) OR high-capability-class.

HIGH-capability-class ALWAYS escalates, regardless of how well documented it is. It is defined structurally as anything that touches:

- the External Send Gate (the two-process boundary of FM v11 Invariant 1);
- secrets or authentication (Keychain, OAuth tokens, ServicePrincipal credentials);
- doctrine; or
- a code change.

These map one-to-one to the Developer-Operator's exclusive operations (Op Stds v16 §§37-41). The Successor-Operator cannot perform them; by construction they route to the Developer-Operator at Tier 3.

# Step 1-7 — Carry Forward From v6.2

All cutover steps preceding Owner-Side Activation carry forward unchanged from Handover Plan v6.2. Reference v6.2 for the operative text of Steps 1 (pre-arrival hardware prep), 2 (Tailscale install + verification), 3 (M365 ServicePrincipal cutover), 4 (credential cutover including Resend + Sentry), 5 (per-workstream cutover sequence), 6 (launchd enablement), 7 (watchdog activation with Day 7 routing gate).

# Step 8 — Owner-Side Activation (EXTENDED v6.3)

After all workstreams cut over and watchdog is stable:

## Existing items (carried forward from v6.2)

- Owner reviews and signs the post-handover acceptance — concise written acknowledgment that the system is operating in production, that Phase 1.5 is closed, and that ongoing operation is per the three-tier fault-response model: the Successor-Operator owns day-to-day operation (Tier 2, Claude-assisted), the system self-heals where it can (Tier 1), and the Developer-Operator (Seth) is the Tier-3 escalation asset reached over the remote-support channel (Tailscale-managed VPN) for novel or high-capability-class faults — not the primary operator.

- Customer admin tested for ability to: flip ITS_Config system.state to PAUSED and back; approve a _Pending_Review row; respond to a Sentry alert email.

- Solution Smith publishes Phase 1.5 close notice in the planning project as a session log; updates Foundation Scaffold Update to a status overlay capturing the actual handover date.

## New items (NEW v6.3)

- Customer admin tested for ability to: add a new trusted-contact row to ITS_Trusted_Contacts (e.g., new subcontractor onboarding) with all required fields — Email, Display Name, Role, Project Scope, Workstream Scope, Status — populated correctly. Admin understands that new entries default to Status=PENDING_VERIFICATION and require operator verification (voice call or in-person) before flipping to ACTIVE.

- Customer admin tested for ability to: disable a trusted-contact (Status=DISABLED) for offboarding (subcontractor contract ends, PM leaves the company) without deleting the row. Preserves audit history for compliance and incident review.

- Customer admin demonstrates understanding of picklist-enforced columns. Typing values not in the picklist will be rejected by Smartsheet at entry time — this is intentional. If a new picklist value is needed (e.g., a new project name), the column itself must be updated by Solution Smith via remote support or by the customer admin's UI-level Smartsheet admin.

- Customer admin briefed on header-forgery detection. A legitimate sender whose mail server has SPF/DKIM/DMARC misconfigurations will land in ITS_Review_Queue rather than the pipeline — this is expected behavior, not a malfunction. Customer admin escalates to operator if persistent legitimate-sender routing fails surface.

# Pre-Cutover Conditions (EXTENDED v6.3)

## Existing conditions (carried forward from v6.2)

- Triple-fire CRITICAL alert path has fired on a real issue and been triaged — Smartsheet ITS_Errors row written, Resend operator email received and read, Sentry event captured. Confirms all three legs operational under realistic conditions, not just smoke-tested.

- Reviewer chain real-data validation: at least one WPR draft has gone through the full 3-tier reviewer chain (Teala → Sam fallback → Jacob fallback) in sandbox, with at least one tier 2 fallback exercised.

- Box OAuth refresh-token rotation verified: setup_box_oauth.py has run at least once; subsequent ITS sessions confirm refresh-token rotation is persisting to Keychain (test_store_tokens_persists_refresh_token covers the code path; operator verifies via Keychain Access).

- Sandbox 30-day clean-operation window: no CRITICAL alerts unexplained, no Mail.app rule silent disables (replaced post-PR-#59 by polling-daemon heartbeat-staleness watchdog check), no Box token expiry, no Smartsheet auth drift.

## New conditions (NEW v6.3)

- PHASE 1.4 SECURITY HARDENING COMPLETE — all three deliverables verified live in sandbox per V&R v7.2 Phase 1.4 gate: (a) picklist-hardening across all ITS sheets per Op Stds v11 §35; (b) ITS_Trusted_Contacts sheet live + populated with anticipated real-recipient PMs/Forefront contacts; intake daemons refactored to query the sheet; ITS_Config JSON allowlists retired per Op Stds v11 §33; (c) attachment screening pipeline Layers 1-3 implemented per Op Stds v11 §34, verified against EICAR test fixtures plus a corpus of legitimate DFR samples. Cutover does not proceed if any Phase 1.4 deliverable is open.

- REAL-RECIPIENT WIRING COORDINATED — Teala has provided real Forefront/PM contact addresses; trusted-contacts sheet populated with Status=ACTIVE for verified contacts; per-job recipient ITS_Config rows updated from closed-loop testing values to real recipients.

- CLAMAV SIGNATURE DATABASE FRESH — freshclam daemon installed and confirmed updating signature DB at least daily. Watchdog Check H (heartbeat staleness, successor to Check F per Op Stds v11 §2) operational and configured to flag stale clamd state.

- TIER-1 SELF-HEAL LAYER COMPLETE (NEW v7) — watchdog Check H (heartbeat staleness, successor to Check F per Op Stds v16 §2) operational across ALL Enabled daemons, not just one. As of 585823d this is UNMET: 2 of 3 daemons are heartbeat-pending and Check H coverage is partial. This is the Tier-1 leg of the Fault-Response Model. Cutover does not proceed until every Enabled daemon emits a heartbeat that Check H reads and flags on staleness.

- TIER-2 READINESS (NEW v8 — replaces the v7 "enforcement layer built" condition) — the Tier-2 boundary is held by training + the both-rule + co-resolution, NOT by a structural enforcement layer (that v7 build gap is removed; there is no non-developer-safe enforcement layer — FM v11 / Op Stds v16). Readiness means: the §44 low-capability-class action set (re-run a daemon, toggle an ITS_Config value, re-send an approval, re-seed a row, clear a stuck lock) is implemented as discrete, tested, non-escalating operations; §43 successor-remediation runbooks exist for the top fault classes; and the Successor-Operator (Daniel) is trained to run Claude Code, follow the runbooks, and recognize and escalate the four high-class categories (External Send Gate, secrets/auth, doctrine, code changes), having demonstrated supervised, Claude-assisted low-class repairs. Cutover does not proceed until Tier-2 readiness is met.

# Risk Inventory (EXTENDED v6.3)

| **Risk** | **Likelihood** | **Mitigation** |
| --- | --- | --- |
| EXO ServicePrincipal not synced to live tenant (carried) | Medium | Smoke test step 4 catches it. Apply v3.1 errata pattern: Connect-ExchangeOnline + New-ServicePrincipal -AppId <appId> -ObjectId <Enterprise-App-ObjectId>. ObjectId from Enterprise Apps, not App Registrations. |
| Tailscale fails post-shipment (carried) | Medium | Tested before shipment; physical access + video-call walkthrough fallback. ~$1,200 hardware refresh covers a replacement Mac shipment if remote-recovery impossible. |
| Watchdog false alarms in first 7 days (carried, reframed v7) | Medium | Day 7 routing gate: watchdog routes to the Developer-Operator (Seth) only for the first 7 days post-cutover; switch primary routing to the Successor-Operator (Tier 2) only after no false alarms observed. The Developer-Operator remains the Tier-3 escalation asset after the switch — novel or high-capability-class flags still route to Seth per the Fault-Response Model "both" rule. |
| Box refresh token expiry post-shipment (carried) | Low (mitigated) | Box refresh tokens rotate every use; ship-and-leave intact if ITS runs >=1x/60d. Watchdog Box-token-age check (queued for R2 follow-on PR) warns at 50 days, CRITICAL at 58 days. Until that check lands, the failure mode is the next ITS run after expiry firing CRITICAL via triple-fire — loud, not silent. Operator-touch recovery: re-run scripts/setup_box_oauth.py. |
| SPOOFED SENDER within trusted-contacts (NEW v6.3) | Low-Medium | ITS_Trusted_Contacts exact-match + header-forgery detection (SPF/DKIM/DMARC + Return-Path validation) per Op Stds v11 §33. Layers 2-5 of Invariant 2 (untrusted-content tagging, capability gating, structured output, anomaly logging) provide defense-in-depth — the damage ceiling under credential compromise is 'extracted data is wrong' not 'external action taken on attacker's behalf' per FM v8. |
| MALICIOUS ATTACHMENT from compromised subcontractor (NEW v6.3) | Low-Medium | Attachment screening pipeline Layers 1-3 per Op Stds v11 §34. ClamAV signature DB auto-updates daily via freshclam. EICAR test fixture verifies pipeline health. Layer 4 (VirusTotal) deferred to Phase 2+ — Layers 1-3 sufficient for Phase 1.5 launch. Zero-day exploits in PDF/Office formats remain residual risk; mitigation is that ITS does not open attachments in vulnerable viewers (Box web UI is downstream consumer; PyMuPDF/python-docx don't execute embedded code). |
| OPERATOR TYPO in ITS_Config control cell triggering fail-open (NEW v6.3) | Low | Picklist-hardening prevents at the column-type level per Op Stds v11 §35. Existing fail-open logic in kill_switch.py stays as belt-and-suspenders for Smartsheet-unreachable case. Pre-cutover picklist-hardening retrofit audit covers all bounded-enum control cells. |

# Companion-Doc References (Refreshed)

- Foundation Mission v11 — Invariant 1 two-process External Send Gate is the capability-gating philosophy that informs how the Tier-2 boundary is drawn; the Developer-Operator / Successor-Operator maintenance-role principle (with the Successor-Operator redefined as a trained CC operator); v11 removes the v10 enforcement-layer framing — the through-line ends at philosophy. Invariant 2 layers (trusted-contacts + header-forgery, attachment screening) unchanged. Operative invariant reference.

- Operational Standards v16 — §2 Check H (heartbeat-staleness watchdog) is the Tier-1 self-heal mechanism; §§37-41 enumerate the Developer-Operator-only developer-context operations; §42 (code-level self-documentation) is for code-readers and is the WRONG audience for the Tier-2 successor-remediation runbook; §43 is the Successor-Remediation Documentation Discipline; §44 is the Tier-2 Claude-assisted repair path whose boundary is training-enforced (the v15 enforcement-layer build gap is removed). §§31-36 carry forward (polling-daemon, operator visibility, trusted-contacts, attachment screening, picklist convention, in-repo tech debt).

- Vision & Roadmap v9 — the ship-and-leave / developer-departure threshold (operated by the Successor-Operator with Seth at Tier 3); Phase 1.4 security hardening as named precondition phase before Phase 1.5; Pre-Cutover Condition 4 (Tier-1 self-heal complete) and Condition 5 reframed to Tier-2 readiness (no enforcement layer).

- Excellence Roadmap v4 — R6 (successor-maintenance build program): (a) Tier-1 self-heal + (b) Tier-2 readiness + (c) runbook tooling, opened as a Track 1 critical-path cluster; R4 closed (polling daemon + operator visibility); R5 (security hardening cluster) open.

- Foundation Scaffold Update v6.5 — PR window through #60; first-time enumeration of box_migration/ + smartsheet_migration/.

- Memory Archive v5 — operational detail through 2026-05-22.

- Cascade Unification Update 2026-05-22 Security Hardening — cascade event record.

- Permissions Ask v5 — §3.1/§3.2 reframed in this cascade to the Successor-Operator (EDITOR, Tier-2) / Developer-Operator (ADMIN, Tier-3 asset) split.

- Smartsheet Handoff v5 (unchanged) + System+HR Handoff v6 (reframed in this cascade to the two-role model) — sibling docs.

# Authority

Handover Plan v8, 2026-06-01. v8 removes the Tier-2 "non-developer-safe enforcement layer" that v7 named as a hard pre-cutover build gap (there is no structural maintenance enforcement layer; none is built or required — FM v11 / Op Stds v16) and redefines the Successor-Operator as a trained operator who runs Claude Code himself, follows the §43 runbooks, and escalates the four high-class categories — not a Smartsheet-UI-only approver. The Tier-2 boundary is held by training + the both-rule + co-resolution with the Developer-Operator until per-category clearance; the v7 Tier-2 pre-cutover condition is replaced by a Tier-2 readiness gate. The Tier-1 self-heal gate (Check H) survives unchanged. v7's three-tier model, roles, escalation boundary, and Step 8/Day-7 reframes, plus v6.3's Phase 1.4 hardening, carry forward. v7 retires on acceptance of v8; v8 is the canonical baseline and operative reference (frontmatter version and title both read v8). Canonical git tag: handover-plan-v8.

v9 trigger criteria: a further structural change to the cutover runbook or to the fault-response model. Status updates that do not change runbook or model structure are absorbed without a major bump.