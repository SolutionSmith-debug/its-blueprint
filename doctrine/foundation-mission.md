---
type: doctrine
version: 9
status: canonical
last_verified: 2026-05-29
last_verified_against: 64526a1
supersedes: doctrine/foundation-mission.md@v8
workstream: null
tags: [invariants, external-send-gate, adversarial-input-handling]
---

**ITS Foundation Mission v9**

2026-05-29 — Invariant 2 Layer 5 Reframed: Detection Tripwire, Not a Defense Layer

*Layer 5 (anomaly logging) recategorized from co-equal defense layer to post-hoc detection tripwire — an honest characterization of a trivially-evadable substring matcher (audit F13) · mechanism unchanged and retained in production · Layers 1–4 + 6 and the invariant principles unchanged*

# Purpose of v9

Foundation-level invariants are non-negotiable. Every workstream inherits both. v9 reframes Invariant 2's Layer 5 (anomaly logging) from a co-equal defense layer into what it actually is: a low-effort, post-hoc detection tripwire — not a barrier that prevents a successful injection. The mechanism is unchanged and stays in production; only the doctrine's characterization of its protective value is corrected.

v9 trigger: the 2026-05-25 forensic audit (audits/2026-05-25_forensic-audit.md, finding F13) found that doctrine over-described Layer 5's protection relative to what the code delivers — exact-substring matching against a short sentinel phrase list is trivially evaded by paraphrase. Over-promising a tripwire as a defense is a worse failure than describing it honestly, because it invites trusting detection as prevention. The reframe is a security-posture honesty correction, not a principle change. v8 retires on acceptance of v9.

The invariant principle itself is unchanged: all content originating outside the operating customer tenant is untrusted data. The load-bearing adversarial defenses remain Layers 2–4 (untrusted-content tagging, capability gating, structured output), backed by the two-process External Send Gate (Invariant 1) as the actual security boundary. Layer 6 (attachment screening) and Layer 1 (trusted-contacts + scope enforcement + header-forgery detection), both established in v8, are unchanged.

# Product Context

Carries forward from v7 verbatim. ITS is a white-glove custom-development practice; Evergreen Renewables is Customer 0; per-customer repo invariant applies; production-quality reliability bar; California cutover destination.

# Operating Principles

Carries forward from v7 verbatim. Audience-based access boundaries (operator vs customer-employee surfaces) and per-customer repo invariant unchanged.

# Invariants

## Invariant 1 — External Send Gate (Unchanged from v7)

No external transmission without explicit human approval. Permanent, not time-bounded. Earlier framing in Op Stds v4 that described review as a 30-60 day window is superseded.

- Every workstream that produces customer-facing output uses a <Workstream>_Pending_Review Smartsheet with Approved for Send / Approved By / Approved At / Sent At / Send Status columns.

- Two-process model. Generation scripts (which call the Anthropic API) have zero send capability. Send scripts (which transmit) have zero AI step.

- Successful prompt injection at the AI layer cannot cause external transmission, because the AI is in a different process from the transmitter.

- Enforced at the code level by tests/test_capability_gating.py — every generation script and every send script is registered to the appropriate list there.

## Invariant 2 — Adversarial Input Handling (Revised in v8)

All content originating outside the operating customer tenant is untrusted data. Six-layer defense (v8 expanded from v7's five). The invariant itself is unchanged from v7; Layers 1 and 6 are revised/added (v8), and Layer 5 is recharacterized as a detection tripwire, not a defense layer (v9, see below).

### Layer 1 — Sender Allowlist + Scope Enforcement + Header-Forgery Detection (REVISED)

Inbound sender exact-matched against ITS_Trusted_Contacts sheet (System workspace) where Status = ACTIVE. Project Scope and Workstream Scope columns enforce per-project and per-workstream trust boundaries (a Bradley 1 PM's email landing in a Brimfield 2 report routes to ITS_Review_Queue, not the pipeline).

Header-forgery detection precedes the allowlist lookup. Microsoft Graph API exposes Authentication-Results, Return-Path, and Received chain headers. Any of {spf=fail, dkim=fail, dmarc=fail, Return-Path domain mismatch with From: domain} routes to ITS_Quarantine before sender lookup. Any of {spf=neutral, spf=softfail, dkim=none} on an otherwise-trusted sender routes to ITS_Review_Queue.

Implementation status: trusted-contacts sheet build + intake.py refactor scheduled in pre-Customer-1 security hardening cluster (V&R v7.2 Phase 1.5 precondition). JSON-list allowlists in ITS_Config (the prior v7 pattern, currently in use) retire at trusted-contacts cutover. Op Stds v11 §33 codifies the implementation pattern.

### Layer 2 — Untrusted-Content Tagging (Unchanged)

Every Anthropic API call processing external content uses shared.untrusted_content.wrap() and the canonical system-prompt boilerplate. shared/untrusted_content.py is live, tested, in production.

### Layer 3 — Capability Gating (Unchanged)

The AI has no permission to send or take action. Enforced by the two-process model (Invariant 1) and verified by tests/test_capability_gating.py + tests/test_intake_capability_gating.py (extended in PR #59 to cover intake_poll.py).

### Layer 4 — Structured Output Enforcement (Unchanged)

Anthropic tool-use forces JSON-schema-conforming responses. Non-conforming responses rejected and routed to ITS_Review_Queue. JSON schemas live in schemas/ with version field; scripts reject responses on schema mismatch.

### Layer 5 — Anomaly Logging on Extraction Output (Reframed in v9: Tripwire, Not Defense Layer)

Layer 5 is a low-effort detection tripwire, not a defense layer. It does not prevent a successful prompt injection; it raises a post-hoc signal that an extraction output matched a known-suspicious pattern, so the item can be routed to human review and flagged. The implementation is exact-substring matching against a short sentinel phrase list — trivially evaded by paraphrase or a thesaurus — so it must never be relied on as a barrier.

The real adversarial defenses are Layers 2–4 (untrusted-content tagging, capability gating, structured output), backed by the two-process External Send Gate (Invariant 1), which is the actual security boundary. Layer 5's value is detection and triage signal — route to ITS_Review_Queue, flag for a human — not prevention. Treating it as co-equal with Layers 2–4 would overstate the protection the doctrine delivers; v9 corrects that framing per audit finding F13. The code is unchanged and stays in production.

Mechanism (unchanged): shared.anomaly_logger.check() runs on every extraction output. Anomalies route to ITS_Review_Queue with security_flag=True. shared/anomaly_logger.py is live, tested. Phase 1 sentinel list covers system_*, role_*, ignore_*, recipient_override patterns; SUSPICIOUS_FIELD_PATTERNS FP risk tracked in docs/tech_debt.md for tuning during first 30 days against real extraction outputs.

### Layer 6 — Attachment Screening Pipeline (NEW in v8)

Every attachment passes through four sub-layers before being uploaded to Box or referenced in any AI call:

- Sub-layer (a) — static signature checks: magic-number verification, size sanity, filename pattern matching.

- Sub-layer (b) — format-aware structural inspection: PDF JavaScript/embedded-file detection, Office macro detection, polyglot detection.

- Sub-layer (c) — ClamAV antivirus scan via pyclamd (signature database auto-updates daily).

- Sub-layer (d) — optional VirusTotal hash check (Phase 2+ enhancement).

Failure disposition: malicious → ITS_Quarantine + CRITICAL triple-fire + sender DISABLED in ITS_Trusted_Contacts pending operator review; suspicious → ITS_Review_Queue; clean → proceed.

Implementation status: scheduled in pre-Customer-1 security hardening cluster (V&R v7.2). Op Stds v11 §34 codifies the implementation pattern.

## Residual Risk (Updated for v8)

Prompt injection is an unsolved research problem. The architecture assumes injection might succeed at the AI layer and ensures the damage ceiling is "extracted data is wrong" rather than "data exfiltrated" or "external action taken on attacker's behalf."

Attachment malware is partially addressable. Layers (a)-(c) catch known-signature and structural threats. Zero-day exploits in PDF/Office formats remain a residual risk. Mitigation: ITS does not open attachments in vulnerable viewers — files are uploaded to Box (cloud-managed; not opened locally) and text content extracted via library code (PyMuPDF, python-docx) that doesn't execute embedded code. The customer's downstream consumption (operator viewing in Box web UI; PMs downloading) inherits Box's threat model, not ITS's.

Spoofed sender within trusted-contacts is partially addressable. Header-forgery detection catches authentication failures. A sophisticated attacker who compromises a legitimate sender's credentials and sends through their actual mail server bypasses all sender-side defenses. Layers 2-4 still apply (untrusted-content tagging, capability gating, structured output), with Layer 5 anomaly logging as a post-hoc detection signal, not a barrier. The damage ceiling under credential compromise is "extracted data is wrong" not "external action taken on attacker's behalf."

# Invariant Enforcement Under Future Implementation Patterns

Carries forward from v7.1 with updated Layer 6 implications. The invariants themselves (no external transmission without approval; external content is untrusted) survive any future implementation pattern shift. Phase 0/1 enforcement patterns (two-process model, capability-gating tests, untrusted-content tagging, anomaly logging, attachment screening pipeline) may be re-architected under future implementations like Claude Managed Agents.

Specifically for v8 additions: Layer 6 (attachment screening) is a Phase 0/1 deterministic Python implementation. Under future Managed Agents implementations, this work moves into agent-loop tool descriptions and harness configuration. Layer 1 (trusted-contacts + header-forgery) is similarly Phase 0/1 deterministic; would survive Managed Agents but require re-architecting the lookup primitive.

Re-verify capability set at Phase 3 evaluation gate; the candidate workstream list (Closeout Package Assembly, Schedule Digest, Dreaming, ITS Chat backend re-eval) is planning input, not roadmap promise. Op Stds v11 §29 holds the architectural framing.

# Relationship to Sub-Projects

Carries forward from v7. Five sub-projects (Safety Reports, POs/Materials, Subcontracts, Email Triage, AI Employee Capabilities) inherit from this foundation mission. v8 Invariant 2 Layer 6 (attachment screening) applies to every workstream that ingests attachments — currently Safety Reports; future POs/Materials (supplier confirmations), Subcontracts (signed PDFs), Email Triage (any attachment in routed mail), AI Employee (any external attachment surfaced).

# Sandbox-First Build Pattern

Carries forward from v7 verbatim. Full system stood up and validated in sandbox before any cutover to live tenants. Phase 1.5 = combined cutover + hardware delivery event.

v8 implication: security hardening cluster (trusted-contacts + attachment screening + picklist-hardening) must complete in sandbox before Phase 1.5 cutover. V&R v7.2 codifies this as a Phase 1.5 precondition.

# Hardware Lifecycle

Carries forward from v7 verbatim. Florida → California cutover; Tailscale-managed maintenance; ~$1,200 hardware refresh every 3-4 years (customer responsibility).

# Framework vs Customer-Specific Lens

Carries forward from v7. Two-bucket framing (framework default + customer-specific config); single-tenant assumption bucket retired in v7 under per-customer-repo invariant.

v8 implication: trusted-contacts sheet is per-customer (each customer fork has its own); attachment-screening pipeline is framework-default (every customer fork ships with Layers 1-3 enabled). Op Stds v11 §33 + §34 hold the implementation details.

# Scope of This Project

- Foundation Mission (this doc, v9) — invariants, principles, project-level architecture, per-customer-repo invariant.

- Operational Standards v14 — cross-cutting patterns every workstream uses.

- Vision & Roadmap v7.2 — phase plan with Phase 1.5 security-hardening precondition.

- Handover Plan v6.3 — Phase 1.5 cutover + handover runbook with security-hardening additions.

- Permissions Ask v4 — cutover-phase admin grants. Unchanged in this cascade.

- Excellence Roadmap v2.3 — R4 + R5 status.

- Foundation Scaffold Update v6.5 — execution-layer state.

- Memory Archive v5 — operational detail.

- Smartsheet Handoff v5 + System+HR Handoff v5 — sibling docs. Unchanged.

- Cascade Unification Update 2026-05-22 Security Hardening — cascade event record.

# Authority

Foundation Mission v9, 2026-05-29. Security-posture honesty correction: Invariant 2 Layer 5 (anomaly logging) reframed from co-equal defense layer to post-hoc detection tripwire, per audit finding F13 (audits/2026-05-25_forensic-audit.md). Mechanism unchanged and retained in production; only the doctrine's characterization of its protective value is corrected. Invariant principles, the six-layer structure, and Layers 1–4 + 6 are unchanged from v8. v8 retires on acceptance of v9.

v10 trigger: substantive invariant principle change, business-model change, or any defense-layer addition, removal, or recharacterization (the v8→v9 reframe established that recharacterizing a layer's protective claim is itself a bump-worthy change). v9.x absorbs further status updates without a framing change.

Companion to Op Stds v14, V&R v7.2, Handover Plan v6.3, Excellence Roadmap v2.3, FSU v6.5, Memory Archive v5.