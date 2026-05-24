---
type: doctrine
version: 6
status: canonical
last_verified: 2026-05-24
last_verified_against: 3b7d56d
supersedes: doctrine/handover-plan.md@v6.2
workstream: null
tags: [california-cutover, hardware-handoff, permissions]
---

**ITS Handover Plan v6.3**

2026-05-22 — Phase 1.4 Security Hardening Precondition Absorbed

*Status overlay on v6.2 · Step 8 customer-admin tests extended · Pre-Cutover Phase 1.4 gate added · Risk Inventory + 3 new entries*

# Purpose of v6.3

Status overlay on Handover Plan v6.2 (2026-05-20). Three substantive additions absorb the V&R v7.2 Phase 1.4 security hardening precondition: (1) Step 8 customer-admin tests extended to include trusted-contacts management and picklist enforcement awareness; (2) Pre-Cutover Conditions explicitly require Phase 1.4 deliverables complete; (3) Risk Inventory adds three new entries covering spoofing, malware, and picklist-typo failure modes.

v6.2 retires on acceptance of v6.3; v6 remains canonical baseline; v6.3 is operative reference. v7 trigger remains substantive cutover-runbook restructuring (not yet anticipated).

# What Changed in v6.3

- Step 8 — Owner-side activation extended with three new customer-admin test items covering trusted-contacts add/disable, picklist-enforced columns awareness, header-forgery detection understanding.

- Pre-Cutover Conditions — Phase 1.4 security hardening cluster added as hard prerequisite (matches V&R v7.2).

- Risk Inventory — three new entries: spoofed sender within allowlist (mitigated), malicious attachment from compromised subcontractor (mitigated), operator typo in ITS_Config triggering fail-open (mitigated).

- Cross-references refreshed: Foundation Mission v7.1 → v8, Op Stds v10/v10.1 → v11, V&R v7.1 → v7.2.

- Step 1-7 carry forward verbatim from v6.2 with no substantive change.

# Step 1-7 — Carry Forward From v6.2

All cutover steps preceding Owner-Side Activation carry forward unchanged from Handover Plan v6.2. Reference v6.2 for the operative text of Steps 1 (pre-arrival hardware prep), 2 (Tailscale install + verification), 3 (M365 ServicePrincipal cutover), 4 (credential cutover including Resend + Sentry), 5 (per-workstream cutover sequence), 6 (launchd enablement), 7 (watchdog activation with Day 7 routing gate).

# Step 8 — Owner-Side Activation (EXTENDED v6.3)

After all workstreams cut over and watchdog is stable:

## Existing items (carried forward from v6.2)

- Owner reviews and signs the post-handover acceptance — concise written acknowledgment that the system is operating in production, that Phase 1.5 is closed, and that ongoing maintenance is per the remote-support model.

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

# Risk Inventory (EXTENDED v6.3)

| **Risk** | **Likelihood** | **Mitigation** |
| --- | --- | --- |
| EXO ServicePrincipal not synced to live tenant (carried) | Medium | Smoke test step 4 catches it. Apply v3.1 errata pattern: Connect-ExchangeOnline + New-ServicePrincipal -AppId <appId> -ObjectId <Enterprise-App-ObjectId>. ObjectId from Enterprise Apps, not App Registrations. |
| Tailscale fails post-shipment (carried) | Medium | Tested before shipment; physical access + video-call walkthrough fallback. ~$1,200 hardware refresh covers a replacement Mac shipment if remote-recovery impossible. |
| Watchdog false alarms in first 7 days (carried) | Medium | Day 7 routing gate: watchdog routes to Solution Smith only for the first 7 days post-cutover; switch to customer maintainer only after no false alarms observed. |
| Box refresh token expiry post-shipment (carried) | Low (mitigated) | Box refresh tokens rotate every use; ship-and-leave intact if ITS runs >=1x/60d. Watchdog Box-token-age check (queued for R2 follow-on PR) warns at 50 days, CRITICAL at 58 days. Until that check lands, the failure mode is the next ITS run after expiry firing CRITICAL via triple-fire — loud, not silent. Operator-touch recovery: re-run scripts/setup_box_oauth.py. |
| SPOOFED SENDER within trusted-contacts (NEW v6.3) | Low-Medium | ITS_Trusted_Contacts exact-match + header-forgery detection (SPF/DKIM/DMARC + Return-Path validation) per Op Stds v11 §33. Layers 2-5 of Invariant 2 (untrusted-content tagging, capability gating, structured output, anomaly logging) provide defense-in-depth — the damage ceiling under credential compromise is 'extracted data is wrong' not 'external action taken on attacker's behalf' per FM v8. |
| MALICIOUS ATTACHMENT from compromised subcontractor (NEW v6.3) | Low-Medium | Attachment screening pipeline Layers 1-3 per Op Stds v11 §34. ClamAV signature DB auto-updates daily via freshclam. EICAR test fixture verifies pipeline health. Layer 4 (VirusTotal) deferred to Phase 2+ — Layers 1-3 sufficient for Phase 1.5 launch. Zero-day exploits in PDF/Office formats remain residual risk; mitigation is that ITS does not open attachments in vulnerable viewers (Box web UI is downstream consumer; PyMuPDF/python-docx don't execute embedded code). |
| OPERATOR TYPO in ITS_Config control cell triggering fail-open (NEW v6.3) | Low | Picklist-hardening prevents at the column-type level per Op Stds v11 §35. Existing fail-open logic in kill_switch.py stays as belt-and-suspenders for Smartsheet-unreachable case. Pre-cutover picklist-hardening retrofit audit covers all bounded-enum control cells. |

# Companion-Doc References (Refreshed)

- Foundation Mission v8 — Invariant 2 6th layer (attachment screening) + Layer 1 expansion (trusted-contacts + header-forgery). Operative invariant reference.

- Operational Standards v11 — §§31-35 codify polling-daemon, operator visibility, trusted-contacts, attachment screening, picklist convention. Plus §36 in-repo tech debt.

- Vision & Roadmap v7.2 — Phase 1.4 security hardening as named precondition phase before Phase 1.5.

- Excellence Roadmap v2.3 — R4 closed (polling daemon + operator visibility); R5 opened (security hardening cluster).

- Foundation Scaffold Update v6.5 — PR window through #60; first-time enumeration of box_migration/ + smartsheet_migration/.

- Memory Archive v5 — operational detail through 2026-05-22.

- Cascade Unification Update 2026-05-22 Security Hardening — cascade event record.

- Permissions Ask v4 — unchanged in this cascade.

- Smartsheet Handoff v5 + System+HR Handoff v5 — sibling docs, unchanged.

# Authority

Handover Plan v6.3, 2026-05-22. Status overlay on v6.2 absorbing V&R v7.2 Phase 1.4 security hardening precondition into Pre-Cutover Conditions, Step 8 customer-admin tests, and Risk Inventory. v6.2 retires on acceptance of v6.3; v6 remains canonical baseline; v6.3 is operative reference.

v7 trigger criteria (unchanged): substantive cutover-runbook restructuring. v6.x absorbs further status updates without runbook structure changes.