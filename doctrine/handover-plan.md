---
type: doctrine
version: 10
status: canonical
last_verified: 2026-07-12
last_verified_against: f3ad814
supersedes: doctrine/handover-plan.md@v9
workstream: null
tags: [california-cutover, hardware-handoff, permissions, successor-operator, training-bounded-co-resolution, portal-user-admin, safety-portal]
---

**ITS Handover Plan v10**

2026-07-12 — v10 status-fact refresh (operator-directed doctrine elevation). (1) Watchdog **Check C covers 12 tracked jobs** (`TRACKED_JOBS`), not "all four" — the v9 "four tracked daemons" figure is stale. (2) The `weekly_generate` Friday-crash catch-up — v9's "lone residual / remaining pre-cutover requirement" — is **BUILT** (watchdog **Check I** catch-up); that Tier-1 gap is CLOSED. (3) Live workstream roster is now **seven** (safety-reports, safety-portal, field-ops, progress-reporting, po-materials, subcontracts, operator-dashboard) across **15 daemon plists / 14 loaded at cutover** (`po-send` stays unloaded — send-gate); the pre-cutover conditions' per-workstream cutover sequence extends to all seven. The Tier-2 readiness model, the both-rule, and the four high-class categories are UNCHANGED from v9.

2026-06-07 — Safety Portal field-PM account administration runbook added to Step 8 (Phase 7 admin CLI landed, PR-H #185)

*v9 adds the **Safety Portal field-PM account provision/deprovision runbook** to Step 8 (Owner-Side Activation) — the operator manages portal accounts via the Mac CLI `safety_reports.portal_admin` (`add-user`/`reset-password`/`disable-user`/`enable-user`/`list-users`), with server-side session revocation; this realizes the v8→v9 trigger ("a further structural change to the cutover runbook") now that the Phase-7 admin route merged (PR-H #185, exec `f3ad814`). Portal-user administration is a **Tier-2 low-class operator action** (rotating the admin TOKEN itself is Tier-3 secrets/auth). A one-time Developer-Operator live-activation gate precedes it (byte-equal admin tokens; migration 0006 to live D1 before redeploy; redeploy). v8's three-tier model, roles, escalation boundary, and all prior structure carry forward verbatim.*

**ITS Handover Plan v8 (retained for provenance)** — 2026-06-01 — Tier-2 Enforcement Layer Removed; Successor-Operator = Trained CC Operator

*Modifies the v7 three-tier model · the Tier-2 "non-developer-safe enforcement layer" pre-cutover build gap is REMOVED (no structural maintenance enforcement layer exists or is required) · the Tier-2 boundary is held by training + the both-rule + co-resolution with the Developer-Operator until per-category clearance · the Successor-Operator is redefined as a TRAINED operator who runs Claude Code himself (not a Smartsheet-UI-only approver) · the Tier-1 self-heal pre-cutover gate survives, its stale "Check H" status corrected to the implemented Check C marker-file floor (all four daemons) + live UptimeRobot ping (F16), residual = weekly_generate Friday-crash catch-up · v7's model, roles, escalation boundary, and Step 8/Day-7 reframes carry forward*

# Purpose of v8

v8 modifies the three-tier fault-response model that v7 established. v7's model, the Developer-Operator / Successor-Operator role pair, the Tier-2/Tier-3 escalation boundary, the Step 8 and Day-7 reframes, and the Tier-1 self-heal pre-cutover gate all carry forward. v8 makes two changes: it removes the Tier-2 "non-developer-safe enforcement layer" that v7 named as a hard pre-cutover build gap (there is no structural maintenance enforcement layer; none is built or required — see FM v11 / Op Stds v16), and it redefines the Successor-Operator from a Smartsheet-UI-only approver to a trained operator who runs Claude Code himself, follows the §43 runbooks, and escalates the four high-class categories.

The three-tier model as it now stands: (1) Tier 1 self-heal; (2) two named operator roles — Developer-Operator (Seth) and the trained Successor-Operator; (3) the Tier-2/Tier-3 "both" rule over the four high-class categories (External Send Gate, secrets/auth, doctrine, code changes) — the structural *definition* of high-class stands; only the idea of *structurally enforcing* it at Tier 2 is removed, replaced by training + co-resolution; (4) Step 8 acceptance + Day-7 routing to the Successor-Operator with Seth at Tier 3; (5) pre-cutover conditions — the Tier-1 self-heal gate (real) plus a Tier-2 *readiness* gate (the §44 low-class action set implemented + §43 runbooks + trained-operator/demonstrated-repair). The v7 Tier-2 enforcement-layer build gap is removed.

v7 retires on acceptance of v8. **v9 (2026-06-07) is now the canonical baseline** (frontmatter version and title read v9); it carries v8's three-tier model forward verbatim and adds the Safety Portal field-PM account-administration runbook to Step 8 (below). v10 trigger: a further structural change to the cutover runbook or the fault-response model.

# What Changed in v8

v8 removes the Tier-2 "non-developer-safe enforcement layer" that v7 named as a hard pre-cutover build gap and redefines the Successor-Operator. v7's three-tier model, role pair, escalation boundary, Step 8 / Day-7 reframes, and the Tier-1 self-heal pre-cutover gate all carry forward.

- Tier-2 boundary — reframed from "structurally enforced by a to-be-built non-developer-safe enforcement layer" to "held by the trained operator's judgment + the both-rule + co-resolution with the Developer-Operator until per-category clearance." No structural maintenance enforcement layer exists or is required (FM v11 / Op Stds v16).

- Successor-Operator — redefined from a Smartsheet-UI-only approver who never touches a terminal to a TRAINED operator who runs Claude Code himself, follows the §43 runbooks, carries out the low-class repair set, and escalates the four high-class categories. Still a non-developer (no code; no §§37-41 developer-context work).

- Pre-Cutover Conditions — the v7 "Tier-2 non-developer-safe enforcement layer built" condition is REMOVED and replaced by a Tier-2 *readiness* condition (low-class action set implemented + §43 runbooks + trained-operator/demonstrated-repair). The Tier-1 self-heal condition (the Check C marker-file staleness floor, earlier called "Check H") survives unchanged in scope as a standalone gate — its status corrected (Check C covers all four tracked daemons + the F16 ping is live; residual = weekly_generate Friday-crash catch-up); the v7 "both must be built" coupling is gone.

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

The system recovers on its own: interval daemons re-run at their next launchd `StartInterval` (a crashed cycle is simply re-invoked — no `KeepAlive` needed), the watchdog catches staleness, no human is involved. This tier is substantially built. The load-bearing mechanism is the watchdog **Check C marker-file staleness floor** (the staleness detector earlier mis-named "Check H", successor to Check F per Op Stds v16 §2): each scheduled job writes a `{slug}.last_run` marker on a completed cycle, and Check C flags any tracked job whose marker is missing or stale. As of 585823d Check C covers **all four** tracked daemons (safety_intake, safety_weekly_send_poll, safety_weekly_generate, safety_picklist_audit) with per-job freshness windows, and the external **UptimeRobot** ping (audit F16) is the live dead-man's switch for total-host failure. The lone residual: `weekly_generate` runs on `StartCalendarInterval` (Friday 14:00), so a crashed Friday cycle is detected by Check C (8-day window) but not auto-recovered by launchd until next Friday; the watchdog-side **catch-up recovery** closing that gap is the remaining pre-cutover requirement (see Pre-Cutover Conditions).

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

## New items (NEW v9) — Safety Portal field-PM account administration

The Safety Portal authenticates field PMs against per-user accounts (no self-registration). Provisioning, password reset, and revocation are an **operator** responsibility, performed from the Mac via the CLI `python -m safety_reports.portal_admin <subcommand>` (Phase 7, PR-H #185, exec `f3ad814`). This is a **Tier-2 low-capability-class** operator action — application-level user administration that touches neither the External Send Gate, system secrets/auth, doctrine, nor code — so it is in the trained Successor-Operator's scope.

- **Subcommands:** `add-user <username>` (provision — prompts for a password, the **backend** bcrypt-hashes it; plaintext is never stored on the Mac or logged), `reset-password <username>`, `disable-user <username>` (revoke), `enable-user <username>` (restore), `list-users` (usernames + disabled flag). Username convention is `lastname.firstname`.
- **Revocation is server-side and immediate-ish:** `disable-user` sets `users.disabled` in D1; the Worker's `requireSession` checks it per request, so a disabled (or deleted) user is locked out on their next request (`401 revoked`), not merely at cookie expiry. Re-enable with `enable-user`.
- **Auth + the Tier boundary:** the CLI authenticates with the macOS Keychain bearer `ITS_PORTAL_ADMIN_TOKEN`, byte-equal to the Worker secret `PORTAL_ADMIN_API_TOKEN` (privilege-separated from the poller's `PORTAL_INTERNAL_API_TOKEN`). Provisioning/resetting/disabling a *field-PM account* is low-class (Tier 2). **Rotating the admin TOKEN itself** (`PORTAL_ADMIN_API_TOKEN` / `ITS_PORTAL_ADMIN_TOKEN`) is **secrets/auth → Tier 3 (Developer-Operator)** per the high-class definition (Fault-Response Model).
- **One-time live-activation prerequisite (Developer-Operator, at cutover):** the merged admin route is **inert** until (1) `PORTAL_ADMIN_API_TOKEN` (Worker) + `ITS_PORTAL_ADMIN_TOKEN` (Keychain) are set **byte-equal**; (2) migration **0006** (`users.disabled`) is applied to the live D1 **before** the Worker redeploys (else `requireSession` fail-closes every session to `401`); (3) the Worker is redeployed. Until then the CLI's calls error. See [memory-archive §G26](../references/memory-archive.md#g26-2026-06-07-safety-portal-deploy-session-reconciliation-exec-prs-178189) (§G26.9) for the as-built detail.
- **Step-8 acceptance test (add to the owner-side checklist):** the customer admin / Successor-Operator demonstrates `add-user`, `disable-user` (confirm the disabled PM is locked out on next request), and `list-users` against the live portal.

# Pre-Cutover Conditions (EXTENDED v6.3)

## Existing conditions (carried forward from v6.2)

- Triple-fire CRITICAL alert path has fired on a real issue and been triaged — Smartsheet ITS_Errors row written, Resend operator email received and read, Sentry event captured. Confirms all three legs operational under realistic conditions, not just smoke-tested.

- Reviewer chain real-data validation: at least one WPR draft has gone through the full 3-tier reviewer chain (Teala → Sam fallback → Jacob fallback) in sandbox, with at least one tier 2 fallback exercised.

- Box OAuth refresh-token rotation verified: setup_box_oauth.py has run at least once; subsequent ITS sessions confirm refresh-token rotation is persisting to Keychain (test_store_tokens_persists_refresh_token covers the code path; operator verifies via Keychain Access).

- Sandbox 30-day clean-operation window: no CRITICAL alerts unexplained, no Mail.app rule silent disables (replaced post-PR-#59 by polling-daemon heartbeat-staleness watchdog check), no Box token expiry, no Smartsheet auth drift.

## New conditions (NEW v6.3)

- PHASE 1.4 SECURITY HARDENING COMPLETE — all three deliverables verified live in sandbox per V&R v7.2 Phase 1.4 gate: (a) picklist-hardening across all ITS sheets per Op Stds v11 §35; (b) ITS_Trusted_Contacts sheet live + populated with anticipated real-recipient PMs/Forefront contacts; intake daemons refactored to query the sheet; ITS_Config JSON allowlists retired per Op Stds v11 §33; (c) attachment screening pipeline Layers 1-3 implemented per Op Stds v11 §34, verified against EICAR test fixtures plus a corpus of legitimate DFR samples. Cutover does not proceed if any Phase 1.4 deliverable is open.

- REAL-RECIPIENT WIRING COORDINATED — Teala has provided real Forefront/PM contact addresses; trusted-contacts sheet populated with Status=ACTIVE for verified contacts; per-job recipient ITS_Config rows updated from closed-loop testing values to real recipients.

- CLAMAV SIGNATURE DATABASE FRESH — freshclam daemon installed and confirmed updating signature DB at least daily. The watchdog Check C marker-file staleness floor (successor to Check F per Op Stds v16 §2) operational and configured to flag stale clamd state.

- TIER-1 SELF-HEAL LAYER COMPLETE (NEW v7) — the watchdog Check C marker-file staleness floor (the staleness detector earlier called "Check H", successor to Check F per Op Stds v16 §2) covers ALL FOUR tracked daemons (safety_intake, safety_weekly_send_poll, safety_weekly_generate, safety_picklist_audit) with per-job freshness windows, and the external UptimeRobot ping (audit F16) is the live dead-man's switch for total-host failure (the watchdog itself is deliberately NOT self-tracked — a daemon can't detect its own death — so its liveness is covered by the F16 ping, by design). As of 585823d the lone residual is the weekly_generate Friday-crash watchdog catch-up: `weekly_generate` runs on `StartCalendarInterval`, so a crashed Friday cycle is detected by Check C but not auto-recovered by launchd until next Friday. This is the Tier-1 leg of the Fault-Response Model. Cutover does not proceed until that catch-up recovery is built — the all-daemon Check C coverage and the F16 ping legs are already met.

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

- Operational Standards v16 — §2 Check C (the marker-file staleness floor, earlier called "Check H") is the Tier-1 self-heal mechanism, complemented by the F16 UptimeRobot ping; §§37-41 enumerate the Developer-Operator-only developer-context operations; §42 (code-level self-documentation) is for code-readers and is the WRONG audience for the Tier-2 successor-remediation runbook; §43 is the Successor-Remediation Documentation Discipline; §44 is the Tier-2 Claude-assisted repair path whose boundary is training-enforced (the v15 enforcement-layer build gap is removed). §§31-36 carry forward (polling-daemon, operator visibility, trusted-contacts, attachment screening, picklist convention, in-repo tech debt).

- Vision & Roadmap v9 — the ship-and-leave / developer-departure threshold (operated by the Successor-Operator with Seth at Tier 3); Phase 1.4 security hardening as named precondition phase before Phase 1.5; Pre-Cutover Condition 4 (Tier-1 self-heal complete) and Condition 5 reframed to Tier-2 readiness (no enforcement layer).

- Excellence Roadmap v4 — R6 (successor-maintenance build program): (a) Tier-1 self-heal + (b) Tier-2 readiness + (c) runbook tooling, opened as a Track 1 critical-path cluster; R4 closed (polling daemon + operator visibility); R5 (security hardening cluster) open.

- Foundation Scaffold Update v6.5 — PR window through #60; first-time enumeration of box_migration/ + smartsheet_migration/.

- Memory Archive v5 — operational detail through 2026-05-22.

- Cascade Unification Update 2026-05-22 Security Hardening — cascade event record.

- Permissions Ask v5 — §3.1/§3.2 reframed in this cascade to the Successor-Operator (EDITOR, Tier-2) / Developer-Operator (ADMIN, Tier-3 asset) split.

- Smartsheet Handoff v5 (unchanged) + System+HR Handoff v6 (reframed in this cascade to the two-role model) — sibling docs.

# Authority

Handover Plan **v9**, 2026-06-07 (verified against exec main `f3ad814`). v9 adds the **Safety Portal field-PM account-administration runbook** to Step 8 (Owner-Side Activation) — operator provision/reset/disable/enable/list of portal accounts via the `safety_reports.portal_admin` CLI, with server-side session revocation (`requireSession` D1 `disabled` check), a Keychain↔Worker byte-equal admin bearer (privilege-separated from the poller token), and a one-time Developer-Operator live-activation gate (tokens + migration 0006-before-redeploy + redeploy). Portal-user administration is classified **Tier-2 low-class**; rotating the admin token itself is **Tier-3 secrets/auth**. This realizes the v8→v9 trigger ("a further structural change to the cutover runbook") now that the Phase-7 admin route merged (PR-H #185). **v8's three-tier model, the two operator roles, the Tier-2/Tier-3 escalation boundary, the Step 1–7 carry-forwards, and all Pre-Cutover Conditions carry forward verbatim.** v8 retires on acceptance of v9. Canonical git tag: `handover-plan-v9`.

Handover Plan v8, 2026-06-01. v8 removes the Tier-2 "non-developer-safe enforcement layer" that v7 named as a hard pre-cutover build gap (there is no structural maintenance enforcement layer; none is built or required — FM v11 / Op Stds v16) and redefines the Successor-Operator as a trained operator who runs Claude Code himself, follows the §43 runbooks, and escalates the four high-class categories — not a Smartsheet-UI-only approver. The Tier-2 boundary is held by training + the both-rule + co-resolution with the Developer-Operator until per-category clearance; the v7 Tier-2 pre-cutover condition is replaced by a Tier-2 readiness gate. The Tier-1 self-heal gate survives unchanged in scope; its stale "Check H" status characterization is corrected in a v8.x absorption (below). v7's three-tier model, roles, escalation boundary, and Step 8/Day-7 reframes, plus v6.3's Phase 1.4 hardening, carry forward. v7 retires on acceptance of v8; v8 is the canonical baseline and operative reference (frontmatter version and title both read v8). Canonical git tag: handover-plan-v8.

v10 trigger criteria: a further structural change to the cutover runbook or to the fault-response model. Status updates that do not change runbook or model structure are absorbed without a major bump (e.g., the Safety Portal live-activation tracks completing is a status update, not a v10 trigger). **Realized 2026-06-07** by the v9 Step-8 Safety Portal account-administration runbook.

v8.x status absorption (2026-06-01, verified against exec 585823d): the Tier-1 self-heal gate's characterization (Tier 1 — Self-Heal section; ClamAV + TIER-1 SELF-HEAL pre-cutover conditions; the Op Stds §2 cross-reference) is corrected. The mechanism described as an unimplemented "Check H heartbeat-staleness" check with "2 of 3 daemons heartbeat-pending" was **never built**; the implemented staleness floor is the watchdog **Check C marker-file** check, which already covers all four tracked daemons, and the external **UptimeRobot** ping (audit F16) is live. The "every Enabled daemon emits a heartbeat that Check H reads" criterion was mis-specified — the watchdog is deliberately NOT self-tracked (its liveness is the F16 ping). The lone residual gate is the weekly_generate Friday-crash **catch-up** (exec follow-on). This is a Tier-1 self-heal **status update** that changes neither the cutover runbook nor the fault-response model structure, so per the v9 trigger it is **absorbed at v8.x: no major bump, no new tag.** A stale "Op Stds v11 §2" citation in the ClamAV condition is corrected to v16 §2 in the same pass. The prior "Check H" framing is recorded here for provenance.