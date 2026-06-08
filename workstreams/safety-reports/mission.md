---
type: mission
version: 5
status: canonical
last_verified: 2026-06-07
last_verified_against: f3ad814
workstream: safety_reports
tags: [workstream-mission, llm-free, deterministic-weekly, email-path-retained, box-mirror]
---

**ITS Safety Reports Mission v5.5**

2026-06-07 — Deploy-session overlay (Box version-on-conflict + Box-mirror config-gate + email-path retain rationale) atop the LLM-free deterministic weekly product + Safety Portal clean-break (was v5.1, 2026-05-22)

*v5.5 (2026-06-07, exec `f3ad814`): **deploy-session overlay.** (1) The compiled weekly packet uploads to Box with **version-on-conflict** (`box_client.upload_bytes_or_new_version` — a recompile re-produces the same deterministic packet name → a new Box VERSION, not a 409 or a suffixed copy; PR-G #186); the per-submission upload keeps **suffix-on-conflict** (distinct documents). (2) The **Box-mirrors-Smartsheet** model is **LANDED (PR-K #189) but config-gated/live-inert** — when the `ITS_Config` key `safety_reports.box.portal_root_folder_id` is set, `weekly_generate` (and `intake`) file into a root → per-job → per-week tree via the shared `safety_naming` names (category subfolders dropped); unset → the legacy per-job category subfolder via `project_routing.get_folder_id` (the value is NOT the earlier-circulated `388017263015`/`safety_portal_root_folder_id` — those are absent from the code). See [Safety Portal brief §9](../safety-portal/brief.md#9-filing-box-is-the-system-of-record). (3) **Email-path retain (load-bearing):** the email-intake code is **retained, not decommissioned** — `week_folder.py` + `intake.process_message` (and the Graph classify/extract stages) are preserved-**dormant**, while `project_routing` / `BOX_PROJECT_FOLDERS` / the report-category machinery (`BOX_SUBPATH_BY_CATEGORY`) are **actively live shared infra** (reused by the portal Box path). Only `intake_poll.py` is tombstoned (PR #171). Recorded so no future session decommissions these as "clean-break cleanup" — they are the seed for the committed [Email Triage](../email-triage/mission.md) workstream. See memory-archive §G26. · v5.4 (2026-06-05, exec `025215d`): **WSR rewire CODE-COMPLETE.** `weekly_generate`, `weekly_send`, `weekly_send_poll` all repointed WPR→WSR (PRs #173–#177). `portal_poll.py` GATED pending deploy. WPR = decommission-by-doc. Remaining = deploy + live smoke (next session). See memory-archive §G25. · v5.3 (2026-06-05, exec `cf86a9e`): **the Safety Reports workflow is now LLM-free.** The weekly product is a **deterministic merge** of the week's submitted-form PDFs (`form_pdf.merge_pdfs`) + a **fixed-template email body** — the prior Anthropic-drafted-narrative WPR is **retired** with the portal cutover. (LLM/Anthropic stays in scope for **other** workstreams — Email Triage, AI Employee Capabilities — this removal is scoped to Safety Reports only.) Foundation invariants are **unchanged and still inherited**; Adversarial Input Handling **Layer 2** (untrusted-content wrapping before an LLM) is **N/A for this path now** — there is no LLM ingestion surface. See [Safety Portal brief §8 compile](../safety-portal/brief.md#8-submission-pipeline). · v5.2 (2026-06-05, exec `753f12f`): the customer-facing weekly safety report is now reviewed/approved/sent through `WSR_human_review` (standalone ITS — Safety Portal workspace), **not** `WPR_Pending_Review`; safety intake is **portal-only at launch** (the Safety Portal's Python pull transport), the email-PDF path **retired as the safety input** (`intake_poll.py` is tombstoned in exec PR #171; the `weekly_generate`/`weekly_send` WSR rewire is in-flight, so `WPR_Pending_Review` is **decommissioned-by-doc** in code until then); email infrastructure (`graph_client`/`untrusted_content`/`header_forgery`) is **preserved** for the committed [Email Triage](../email-triage/mission.md) workstream. See [Safety Portal brief §8.1](../safety-portal/brief.md#81-clean-break-safety-intake-is-portal-only-at-launch). · v5.1 (2026-05-22): R3 Session 1 shipped + polling daemon + trusted-contacts cluster · Q4-Q8 resolved · Substance otherwise unchanged*

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

External Send Gate — implementation: `WSR_human_review` Smartsheet (in the standalone ITS — Safety Portal workspace; supersedes the legacy `WPR_Pending_Review` under the Safety Portal clean-break) with `Approve for Scheduled Send` + `Send Now` checkboxes, auto-stamped Approved By/At, and an editable Email Body column as the send's source of truth. Two-process model: the weekly-compile script — a **deterministic, LLM-free** merge (`form_pdf.merge_pdfs` of the week's submitted-form PDFs) + a **fixed-template email body**, with **zero send capability** — writes the draft row; the weekly-send script (no AI step) reads only approved rows and sends. (The prior Anthropic-drafted-narrative WPR is retired — see the v5.3 overlay.) Permanent rule, not time-bounded. Capability gating verified by tests/test_capability_gating.py.

Adversarial Input Handling — implementation (6-layer per FM v8):

- Layer 1 (Sender Allowlist + Scope + Header-Forgery): ITS_Trusted_Contacts sheet exact-match with Status=ACTIVE; project/workstream scope enforcement; SPF/DKIM/DMARC + Return-Path validation precedes lookup. Cutover from ITS_Config JSON list scheduled V&R v7.2 Phase 1.4.

- Layer 2 (Untrusted-Content Tagging): **N/A for the safety-reports workflow as it now runs** — there is no LLM ingestion surface (portal intake is structured; the weekly compile is a deterministic merge — no Anthropic). The invariant is unchanged and still inherited; if the **preserved** email-intake path (`intake.py` `process_message`, kept for Email Triage) is ever reactivated, Layer 2 re-applies via `shared/untrusted_content.py`. (Mirrors the Safety Portal's Layer-6-N/A pattern.)

- Layer 3 (Capability Gating): two-process model + tests/test_intake_capability_gating.py.

- Layer 4 (Structured Output Enforcement): now realized as **form-definition schema validation** of the structured portal payload (client + server); the prior "JSON-schema-conforming Anthropic responses" enforcement is N/A in the LLM-free path (re-applies on the preserved email-intake path).

- Layer 5 (Anomaly Logging): the LLM-**extraction-output** anomaly check is N/A in the deterministic/structured path (no extraction); a pattern tripwire on PM-entered text remains (see [Safety Portal mission §7 Layer 5](../safety-portal/mission.md#7-foundation-invariants-inherited)). `shared/anomaly_logger.py` re-applies on the preserved email-intake path.

- Layer 6 (Attachment Screening — NEW v8): four sub-layers per Op Stds v18 §34: static signatures + structural inspection + ClamAV + optional VirusTotal. Cutover scheduled V&R v7.2 Phase 1.4.

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

Safety Reports Mission **v5.5**, 2026-06-07 canonical (verified against exec `f3ad814`). Status overlays since v5.1 (2026-05-22): v5.2 WSR/clean-break, v5.3 LLM-free, v5.4 WSR-rewire code-complete, v5.5 deploy-session (Box version-on-conflict + email-path retain). Original v5.1 absorbed R3 Session 1 ship + polling daemon + heartbeat + Q4-Q8 resolution + Phase 1.4 security hardening framing + FM v8 6-layer Invariant 2. Workstream missions are frontmatter-versioned (not git-tagged).

v6 trigger criteria: substantive scope change to Safety Reports workstream (e.g., new intake document type, cadence change, fundamentally different output artifact). v5.x absorbs ship-status updates without scope changes (the v5.2–v5.5 overlays are all within-scope status, not scope changes).