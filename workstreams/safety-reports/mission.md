---
type: mission
version: 5
status: canonical
last_verified: 2026-05-24
last_verified_against: 3b7d56d
workstream: safety_reports
tags: [workstream-mission]
---

**ITS Safety Reports Mission v5.1**

2026-05-22 — Status Overlay Refreshing v5

*R3 Session 1 shipped + polling daemon + trusted-contacts cluster · Q4-Q8 resolved · Substance unchanged*

# Purpose of v5.1

Status overlay on Safety Reports Mission v5 (2026-05-17). Absorbs substantial post-v5 work: R3 Session 1 ship (intake.py end-to-end via PR #57), polling daemon doctrine (PR #59), heartbeat surface (PR #60), Q4-Q8 owner-decision resolutions, pre-Customer-1 security hardening cluster framing.

v5 retires on acceptance of v5.1; v5.1 is operative reference. v6 trigger remains a substantive scope change to Safety Reports workstream (not anticipated; R3 Sessions 2 + 3 are incremental within v5.1 scope).

# What Changed in v5.1

- Operational Standards reference: v7 → v11 (four cascade events absorbed).

- Foundation Mission reference: v4 → v8.

- Trigger pattern: "Mail.app rule (daily intake)" → "safety_reports/intake_poll.py launchd polling daemon (60s cadence)" per Op Stds v11 §31.

- Sender allowlist mechanism: "ITS_Config sender allowlist row" → "ITS_Trusted_Contacts sheet with scope enforcement" per Op Stds v11 §33 (cutover scheduled in V&R v7.2 Phase 1.4 pre-Customer-1 hardening).

- Adversarial Input Handling: 5-layer defense → 6-layer defense (Layer 6 attachment screening pipeline per Op Stds v11 §34 + FM v8 Invariant 2).

- Q4-Q8 owner-decision deferrals: now all resolved per ITS_Q4-Q8_Resolution_2026-05-21.docx.

- Status section: "sandbox build active; 5 of 9 owner decisions resolved" → "R3 Session 1 shipped; intake.py + intake_poll.py + heartbeat live in production; all 9 owner decisions resolved".

# Mission (Carried Forward From v5 — Substance Unchanged)

Replace Evergreen's manual handling of daily safety reports with ITS automation. Field PMs submit reports per site per day; ITS captures them as structured data, files compliance documentation in Box, tracks every report in Smartsheet, and generates the customer-facing Weekly Project Report (WPR) for each active job. Every external send is gated by explicit human approval (External Send Gate, per FM v8).

Why this is Phase 1: simplest of the workstreams in workflow shape (read inbox → classify → Smartsheet lookup → file in Box → gated weekly summary → customer email), highest daily volume, and the workstream that establishes the foundational patterns (auth, Smartsheet schema, Box paths, trusted-contacts pattern, External Send Gate implementation, reviewer chain, ITS_Time_Off integration) that POs, Subcontracts, Email Triage, and AI Employee Capabilities will inherit.

# Foundation Invariants Inherited (Refreshed for FM v8)

External Send Gate — implementation: WPR_Pending_Review Smartsheet with Approved for Send (checkbox), Approved By, Approved At, Sent At, Send Status columns. Two-process model: weekly-summary script (calls Anthropic, no send capability) writes drafts to the sheet; weekly-send script (no AI step) reads only approved rows and sends. Permanent rule, not time-bounded. Implemented end-to-end at the module level via shared/graph_client.py — capability gating verified by tests/test_capability_gating.py.

Adversarial Input Handling — implementation (6-layer per FM v8):

- Layer 1 (Sender Allowlist + Scope + Header-Forgery): ITS_Trusted_Contacts sheet exact-match with Status=ACTIVE; project/workstream scope enforcement; SPF/DKIM/DMARC + Return-Path validation precedes lookup. Cutover from ITS_Config JSON list scheduled V&R v7.2 Phase 1.4.

- Layer 2 (Untrusted-Content Tagging): email body + attachments wrapped in <untrusted_content> XML tags in every Anthropic call via shared/untrusted_content.py.

- Layer 3 (Capability Gating): two-process model + tests/test_intake_capability_gating.py.

- Layer 4 (Structured Output Enforcement): JSON-schema-conforming Anthropic responses; non-conforming rejected.

- Layer 5 (Anomaly Logging): shared/anomaly_logger.py on every extraction output; security_flag=True routes to ITS_Review_Queue.

- Layer 6 (Attachment Screening — NEW v8): four sub-layers per Op Stds v11 §34: static signatures + structural inspection + ClamAV + optional VirusTotal. Cutover scheduled V&R v7.2 Phase 1.4.

# Three Intake Document Types (Unchanged From v5)

- Daily safety brief + Daily Job Site Safety Worksheet (JSS worksheet). Most frequent.

- Machine pre-inspections (skid steer, lifts, other equipment).

- Stop Work Orders (SWO) — incident events; pattern shows hours/days lost as a category.

# Status as of 2026-05-22 (REFRESHED in v5.1)

- R3 Session 1 SHIPPED (PR #57, c4c4bc9): safety_reports/intake.py end-to-end against live sandbox. 12 pipeline stages. Capability-gated AST test passes.

- Polling-daemon trigger SHIPPED (PR #59, f1e724f): safety_reports/intake_poll.py replaces Mail.app rule. 60s cadence. 242+ confirmed cycles in production.

- Heartbeat integration SHIPPED (PR #60, 7397b07): ITS_Daemon_Health row update per cycle. ARCH-1/2/3 refinements operational.

- Q4-Q8 owner-decision deferrals all RESOLVED 2026-05-21: Q4 = sheet_ids.py folder constants; Q5 = Daily Reports 9 cols + Weekly Rollup 4 cols verified live; Q6 Box = 1111A template prescriptive; Q8 = recipients in ITS_Config safety_reports.recipients.<job>.

- Bradley 1 sandbox demo-complete: 43-row DFR backfill, ~552 total Bradley 1 rows.

- Box 1111A clone cascade complete: 6 project folders under ITS DATA.

- R3 Session 2 (weekly_generate.py) — next critical-path target. Zero code-side prereqs.

- R3 Session 3 (weekly_send.py) — follows Session 2.

- Phase 1.4 security hardening cluster — three deliverables required before Phase 1.5 cutover (V&R v7.2).

# Q1-Q9 Owner Decisions (All Resolved as of v5.1)

v5 captured 9 owner decisions with 5 resolved + 4 deferred (Q4/Q5/Q6/Q8). Per ITS_Q4-Q8_Resolution_2026-05-21.docx, all four deferrals resolved 2026-05-21. v5.1 records all 9 as resolved.

- Q1 — Three intake document types — RESOLVED v5.

- Q2 — Reviewer chain (3-tier: Teala → Sam → Jacob) — RESOLVED v5.

- Q3 — Sandbox verification approach — RESOLVED v5.

- Q4 — Sheet ID structure — RESOLVED 2026-05-21: sheet_ids.py folder constants.

- Q5 — Schema details (Daily Reports + Weekly Rollup) — RESOLVED 2026-05-21: 9 cols + 4 cols verified live.

- Q6 — Box template structure — RESOLVED 2026-05-21: 1111A template prescriptive.

- Q7 — Sam Rigney intro — RESOLVED v5.

- Q8 — Per-job recipients — RESOLVED 2026-05-21: ITS_Config safety_reports.recipients.<job> rows. Closed-loop testing values; real Forefront contacts coordinated Phase 1.4.

- Q9 — Holiday handling — RESOLVED v5.

# Success Criteria (Refreshed for FM v8)

- All daily safety reports captured as Smartsheet rows + Box files with no operator manual entry.

- WPR drafted weekly per active job; approved or edited by Teala/Sam/Jacob within reviewer-chain SLA.

- Every external WPR send gated by explicit human approval (External Send Gate).

- Zero prompt-injection bypasses observed in first 90 days (Adversarial Input Handling 6-layer defense).

- Zero malicious-attachment incidents reaching operator-visible storage (Layer 6 attachment screening).

- Polling daemon ship-and-leave: zero operator intervention required per week after Phase 1.5 cutover.

# Authority

Safety Reports Mission v5.1, 2026-05-22. Status overlay on v5 (2026-05-17) absorbing R3 Session 1 ship + polling daemon + heartbeat + Q4-Q8 resolution + Phase 1.4 security hardening framing + FM v8 6-layer Invariant 2.

v6 trigger criteria: substantive scope change to Safety Reports workstream (e.g., new intake document type, cadence change, fundamentally different output artifact). v5.x absorbs ship-status updates without scope changes.