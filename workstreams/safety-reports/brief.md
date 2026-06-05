---
type: brief
version: 6
status: canonical
last_verified: 2026-06-05
last_verified_against: 025215d
workstream: safety_reports
tags: [workstream-brief, llm-free, deterministic-weekly]
---

**ITS Safety Reports Brief v6.3**

2026-06-05 — LLM-free deterministic weekly product + Safety Portal clean-break overlay (was v6.1, 2026-05-22)

*v6.4 (2026-06-05, exec `025215d`): **WSR rewire CODE-COMPLETE** — `weekly_generate`, `weekly_send`, `weekly_send_poll` all repointed WPR→WSR (PRs #173–#177). `portal_poll.py` GATED pending deploy. WPR = decommission-by-doc. Remaining = deploy + live smoke (next session). See memory-archive §G25. · v6.3 (2026-06-05, exec `cf86a9e`): **the Safety Reports workflow is now LLM-free** — the weekly product is a **deterministic merge** of the week's submitted-form PDFs (`form_pdf.merge_pdfs`) + a **fixed-template email body**; the Anthropic-drafted-narrative WPR is **retired** (LLM stays in scope for other workstreams only). Foundation invariants unchanged; Adversarial **Layer 2 N/A** for this path (no LLM ingestion). See §What Gets Built. · v6.2 (2026-06-05, exec `753f12f`): the safety review surface is now `WSR_human_review` (in the standalone ITS — Safety Portal workspace), **not** `WPR_Pending_Review`; safety intake is **portal-only at launch** (the Safety Portal's Python pull transport), the email-PDF intake path **retired as the safety input** (`intake_poll.py` tombstoned in exec PR #171; the `weekly_generate`/`weekly_send` WSR rewire is in-flight — `WPR_Pending_Review` is **decommissioned-by-doc** in code until then, see §What Gets Built); the email infrastructure (`graph_client` / `untrusted_content` / `header_forgery`) is **preserved** for the committed Email Triage workstream. See [Safety Portal brief §8.1](../safety-portal/brief.md#81-clean-break-safety-intake-is-portal-only-at-launch). · v6.1 (2026-05-22): intake.py + intake_poll.py + heartbeat shipped · Polling daemon canonical*

# Purpose of v6.1

Status overlay on Safety Reports Brief v6 (2026-05-17). Absorbs the post-v6 work: R3 Session 1 ship (intake.py end-to-end), polling daemon doctrine (replaces Mail.app rule trigger), heartbeat integration, Phase 1.4 security hardening framing. No change to engineering architecture or design decisions; status section + module-status table substantively refreshed.

v6 retires on acceptance of v6.1; v6.1 is operative reference.

# What Changed in v6.1

- Mission pointer: v5 → v5.1.

- Operational Standards pointer: v7 → v11.

- Foundation Mission pointer: v4 → v8.

- Trigger architecture: "Mail.app rules (daily intake) + launchd jobs (weekly)" → "launchd-driven polling daemon (60s cadence) for intake + launchd jobs (weekly)."

- Mail.app rule mechanism design decision: superseded by polling daemon per Op Stds v11 §31. Hot-folder pattern retired.

- intake.py status: "Stub" → "Working, live-validated end-to-end (PR #57). 1083 lines, 12-stage pipeline."

- intake_poll.py: NEW module (PR #59). 632 lines. Polling daemon with fcntl lock + ITS_Config gate + seen-set idempotency + heartbeat write.

- week_folder.py: NEW module (PR #54). 168 lines. Per-project per-week folder scaffolding.

- MacBook reliability risk: "if laptop closed when email arrives, Mail.app rule does not fire" — retired. Polling daemon does not depend on email-arrival event; it polls inbox per launchd cadence. Distinct failure modes: (a) MacBook off / sleeping — launchd doesn't fire; (b) Tailscale down — operator can't remote in but daemon still polls; (c) M365 Graph outage — polling cycles fail visibly via heartbeat surface.

- Sender allowlist maintenance: ITS_Config row → ITS_Trusted_Contacts sheet (Op Stds v11 §33). Cutover scheduled V&R v7.2 Phase 1.4.

- Adversarial Input Handling: 5 layers → 6 layers (attachment screening per Op Stds v11 §34 added in v8).

- All other engineering content carries forward from v6 unchanged.

# Pointer to Mission

Engineering complement to ITS — Safety Reports Mission v5.1 (2026-05-22). Mission file owns scope, success criteria, operating principles, the Q1-Q9 decision capture (all resolved), the three intake document types, and the cross-workstream foundational decisions. This brief covers engineering implementation.

# Status (REFRESHED in v6.1)

- Phase: 1 (active build target)

- State as of 2026-05-22: 9 of 9 owner decisions resolved. R3 Session 1 shipped (intake.py end-to-end). Polling daemon + heartbeat shipped. Bradley 1 sandbox demo-complete (43-row DFR backfill). Box 1111A clone cascade complete.

- Test count contribution: ~59 new tests from PRs #54-#60. Cumulative repo state: 779 passed / 3 skipped / 10 deselected.

- Remaining critical-path: R3 Session 2 (weekly_generate.py) + R3 Session 3 (weekly_send.py). Then Phase 1.4 security hardening cluster (3 deliverables per V&R v7.2). Then Phase 1.5 cutover.

- Estimated time to R3 completion: 2-3 focused sessions (Sessions 2 + 3 + Phase 1.4 hardening).

# Architecture (REFRESHED in v6.1)

ITS — Safety Reports runs as a set of Python scripts on the production MacBook (launchd-driven). **The active safety-reports path is now LLM-free:** portal submissions arrive structured (no classify/extract) and the weekly product is a deterministic merge (no drafting) — the pipeline does data movement (Smartsheet, Box via API) with **no Anthropic call**. The Anthropic-based classification/extraction stages (Stages 6–7 below) survive only in the **preserved** email-intake path (`intake.py`, reserved for Email Triage — see the v6.2 clean-break overlay). See ITS Operational Standards for the cross-cutting patterns.

Foundation Invariants implementation: 6-layer Adversarial Input Handling per FM v8. See Mission v5.1 for the layer-by-layer breakdown.

# What Gets Built (REFRESHED in v6.1)

## Polling daemon trigger (safety_reports/intake_poll.py) — SHIPPED PR #59

632-line launchd-driven Python poller. Per-cycle: ITS_Config polling_enabled gate; fcntl file lock at ~/its/state/safety_intake.lock; graph_client.list_inbox with unread_only filter (top=50); per-message seen-set idempotency guard; call intake.process_message; mark_read on success; heartbeat write to ITS_Daemon_Health.

Operator visibility: ITS_Daemon_Health sheet (4529351700729732, folder 04 — Daemons 2130046845511556 in System workspace). One row per daemon, update-in-place. ARCH-1/2/3 refinements per Op Stds v11 §32.

## Intake script (safety_reports/intake.py) — SHIPPED PR #57

1083-line module. process_message(message_id) is the public API invoked by intake_poll per message. SmartsheetError/GraphError soft-fail returns rather than raise.

12-stage pipeline:

- Stage 1: Fetch message + attachments via Graph.

- Stage 2: Sender allowlist gate (Adversarial Input Handling Layer 1). Non-allowlisted → ITS_Quarantine. Trusted-contacts sheet migration scheduled V&R v7.2 Phase 1.4.

- Stage 3: Extract attachments + plain-text body via Graph structured fields.

- Stage 4: Resolve which Forefront project the report belongs to (subject prefix or body scan; ambiguous → ITS_Review_Queue).

- Stage 5: ensure_current_week_folder via week_folder.py — find-or-create per-project per-week Field Reports + Daily Reports + Weekly Rollup folder scaffolding.

- Stage 6: Classify document type (Daily Safety Brief / JSS Worksheet / Machine Pre-Inspection / Stop Work Order / Other) via Anthropic API with untrusted-content tagging + structured output enforcement (Layers 2 + 4).

- Stage 7: Extract structured fields (date, site, PM, etc.) via Anthropic. Anomaly logging on output (Layer 5).

- Stage 8: Daily Reports row write to current-week sheet.

- Stage 9: Box upload (path determined by project + week + document type). SWO + Other skip Box (tag in Notes) per Q6 owner decision.

- Stage 10: Attachment screening — to be added Phase 1.4 (Op Stds v11 §34 Layers 1-3).

- Stage 11: Capability-gated AST test verifies intake has no send capability.

- Stage 12: mark_read on success.

## Week folder helper (safety_reports/week_folder.py) — SHIPPED PR #54

168-line module. Idempotent find-or-create for per-project per-week Field Reports folder + Daily Reports sheet + Weekly Rollup sheet. Race condition tracked in docs/tech_debt.md.

## Weekly compile (safety_reports/weekly_generate.py) — DETERMINISTIC, LLM-free — CODE-COMPLETE (PR #175, `49b393d`)

The weekly product is a **deterministic merge** (`form_pdf.merge_pdfs`) of the week's submitted-form PDFs **+ a fixed-template email body — no Anthropic / LLM call** (the prior Anthropic-drafted-narrative WPR is retired with the portal cutover; LLM stays in scope for other workstreams only). Two-process model per FM v8 Invariant 1 holds structurally: the compile process has **zero send capability** and writes the draft row to `WSR_human_review` (the standalone ITS — Safety Portal workspace; supersedes `WPR_Pending_Review` under the clean-break) with the **template-seeded**, editable Email Body as the send's source of truth. Friday-afternoon launchd cadence (or the `Compile Now` checkbox). **Code-state (exec `025215d`):** deterministic rewire LANDED (PR #175); `portal_poll.py` GATED pending deploy. NOT yet live on host (deploy session required — see §G25.8).

## Weekly send (safety_reports/weekly_send.py) — CODE-COMPLETE (PR #176, `e628044`)

Reads approved rows from `WSR_human_review` (ITS — Safety Portal workspace) where `Approve for Scheduled Send`=true, reading the human-edited Email Body as the source of truth. Sends via Resend or Graph send_mail. Zero AI step per FM v8 Invariant 1.

# Operational Conventions Honored (REFRESHED for v11)

- Kill switch first: shared.kill_switch.check_system_state() or @require_active at script entry.

- Error log decorator: @its_error_log on every script main function.

- Confidence scoring: default threshold 0.85 per Op Stds v11 §5. Below threshold → ITS_Review_Queue.

- External Send Gate: per FM v8 Invariant 1. No generation script imports send capability.

- Adversarial Input Handling: per FM v8 Invariant 2 6-layer (inherited, unchanged). **Layer 2 (untrusted-content wrapping) is N/A for the active safety-reports path — no LLM ingestion surface** (portal intake is structured; the weekly compile is deterministic). The wrap-+-anomaly-log mechanism applies to the preserved email-intake path / Email Triage, not the active safety flow.

- Credentials from macOS Keychain: shared.keychain.get_secret(name). Never env files.

- Schemas in schemas/. Prompts in prompts/. Both version-controlled.

# Risks (REFRESHED in v6.1)

- MacBook off / sleeping: launchd doesn't fire. The watchdog Check C marker-file staleness floor (the staleness detector earlier called "Check H", successor to Check F per Op Stds v16 §2) plus the external UptimeRobot heartbeat ping (audit F16) catch stale-daemon / dead-host state. Tailscale-managed remote wake-up possible.

- Classification accuracy on three real intake types: unknown until benchmarked. Plan: pull 50-100 historical samples per type, run classifier, manually verify, tune.

- Field PM compliance: if reports do not come in consistently, weekly summary has gaps. Not addressable in code; operator/customer process item.

- Empty reviewer chain edge case: if Teala + Sam + Jacob all on PTO same week, workstream holds + emits out-of-band Resend alert. 14-day forward scan (Op Stds v11 §18) surfaces in advance.

- Customer-side variability: per-customer WPR template variants. Defer to first real customer feedback.

- Prompt injection in safety reports: field PMs unlikely vector but external recipient lists or pasted-in content could be. First 90 days = injection-stress test per Mission v5.1.

- Spoofed sender within trusted-contacts (Mission v5.1 Layer 1): header-forgery detection mitigates; residual risk under credential compromise.

- Malicious attachment from compromised subcontractor (Mission v5.1 Layer 6): four-layer attachment screening pipeline mitigates Layers 1-3; Layer 4 (VirusTotal) deferred Phase 2+.

# Engineering Decisions (REFRESHED in v6.1)

- Trigger mechanism: launchd polling daemon (canonical per Op Stds v11 §31). Hot-folder Mail.app rule pattern retired.

- Polling cadence: 60s from safety_reports.intake.poll_interval_seconds ITS_Config row. Tunable. Trade-off: lower = faster intake response + more Graph API calls; higher = batchier processing + lower API spend.

- Confidence threshold for classification: default 0.85 per Op Stds v11 §5. Tune from real Evergreen mail samples in first 30 days.

- Confidence threshold for extraction fields: default 0.85.

- Schema versioning: JSON schemas in ~/its/schemas/ with version field; scripts reject responses on schema mismatch.

- Anomaly detection sentinels: Phase 1 sentinel list covers system_*, role_*, ignore_*, recipient_override. SUSPICIOUS_FIELD_PATTERNS FP risk tracked in docs/tech_debt.md.

- Quarantine review cadence: daily watchdog includes ITS_Quarantine summary. Operator reviews periodically; senders added to trusted-contacts explicitly per Op Stds v11 §33.

- Reviewer chain configuration source: DEFAULT_REVIEWER_CHAINS["safety_reports"] in shared/defaults.py + ITS_Time_Off PTO fetcher overlay.

- Heartbeat write contract: never blocks daemon primary work. Failure logs to ITS_Errors category 'daemon_health_write_failed'; daemon continues.

# Authority

Safety Reports Brief v6.1, 2026-05-22. Status overlay on v6 (2026-05-17) absorbing R3 Session 1 ship + polling daemon + heartbeat + Mail.app trigger retirement + Mission v5.1 pointer.

v7 trigger criteria: substantive engineering architecture change (e.g., new module decomposition pattern, fundamentally different trigger mechanism). v6.x absorbs ship-status updates without architecture changes.