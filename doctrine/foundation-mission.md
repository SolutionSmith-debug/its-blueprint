---
type: doctrine
version: 10
status: canonical
last_verified: 2026-05-29
last_verified_against: 585823d
supersedes: doctrine/foundation-mission.md@v9
workstream: null
tags: [invariants, external-send-gate, adversarial-input-handling, maintenance-roles, successor-operator, capability-gating-through-line]
---

**ITS Foundation Mission v10**

2026-05-29 — Maintenance-Role Principle Added: Developer-Operator vs Successor-Operator

*Operating Principles gain a named maintenance-role distinction (Developer-Operator vs Successor-Operator) · Invariant 1's two-process capability-gating philosophy is composed into a through-line: a Successor-Operator repair session is structurally barred from high-capability-class operations · the non-developer-safe enforcement layer that would hold this boundary WITHOUT a developer present is named as a pre-cutover build requirement, not a present capability · invariant principles and the six-layer structure unchanged · v9 Layer 5 framing carried forward verbatim*

# Purpose of v10

Foundation-level invariants are non-negotiable. Every workstream inherits both. v10 adds an Operating Principle: ITS is maintained under two named roles — a Developer-Operator and a Successor-Operator — and it composes Invariant 1's two-process capability-gating philosophy into a maintenance through-line. v10 changes no invariant and no defense layer; it makes explicit a principle the prior docs left implicit (an undifferentiated "operator") and states honestly that the enforcement layer the through-line depends on does not yet exist.

v10 trigger: the planning model for a non-developer successor (a Successor-Operator who approves while Claude does the diagnostic and repair work) needs an invariant-level anchor, and the prior "operator" abstraction conflated a git/shell-fluent maintainer with a Smartsheet-UI-only successor. Promoting the maintenance-role distinction to a principle, and composing the capability-gating philosophy onto it, is a substantive operating-principle change. v9 retires on acceptance of v10.

The invariant principles themselves are unchanged. Invariant 1 (no external transmission without explicit human approval; two-process model) and Invariant 2 (all content originating outside the operating customer tenant is untrusted data; six-layer defense with v9's Layer 5 tripwire framing) carry forward verbatim. v10 adds a principle that sits beside the invariants and an explicit note that the non-developer-safe maintenance enforcement layer is a pre-cutover build requirement, not a present capability.

# Product Context

Carries forward from v7 verbatim. ITS is a white-glove custom-development practice; Evergreen Renewables is Customer 0; per-customer repo invariant applies; production-quality reliability bar; California cutover destination.

# Operating Principles

Carries forward from v7 verbatim. Audience-based access boundaries (operator vs customer-employee surfaces) and per-customer repo invariant unchanged.

## Maintenance is performed under two named roles (added in v10)

"Operator" is not one role. ITS is maintained under two, and every doc uses the names identically:

- **Developer-Operator** — git/CC/shell/worktree-fluent. Performs every developer-context operation (code changes, repository and migration work, secrets/Keychain handling, running scripts). Is the Tier-3 escalation asset, not the day-to-day operator of a handed-over system.

- **Successor-Operator** — a non-developer. Interacts only through Smartsheet UI and approval surfaces, with Claude doing the diagnostic and repair work; approves but never reads code, never uses git or a terminal directly. Resolves only the low-capability-class fault set (re-run a daemon, toggle an ITS_Config value, re-send an approval, re-seed a row, clear a stuck lock).

Every use of "operator" in any ITS doc must be classifiable to exactly one of these roles. Developer-context operations are Developer-Operator-only by definition; a Successor-Operator cannot perform them. The operational mechanics of the two-role maintenance model — the three-tier fault model, the Tier-2/Tier-3 escalation boundary, and the per-capability successor-remediation runbook discipline — live in Operational Standards v15 (§§43–44) and the Handover Plan v7; this principle only fixes the role vocabulary and asserts that the distinction is load-bearing, not cosmetic.

# Invariants

## Invariant 1 — External Send Gate (Unchanged from v7)

No external transmission without explicit human approval. Permanent, not time-bounded. Earlier framing in Op Stds v4 that described review as a 30-60 day window is superseded.

- Every workstream that produces customer-facing output uses a <Workstream>_Pending_Review Smartsheet with Approved for Send / Approved By / Approved At / Sent At / Send Status columns.

- Two-process model. Generation scripts (which call the Anthropic API) have zero send capability. Send scripts (which transmit) have zero AI step.

- Successful prompt injection at the AI layer cannot cause external transmission, because the AI is in a different process from the transmitter.

- Enforced at the code level by tests/test_capability_gating.py — every generation script and every send script is registered to the appropriate list there.

## Capability-Gating Through-Line — From the Send Gate to Maintenance (added in v10)

Invariant 1 keeps the AI out of the send path by structure, not by trust: a generation process cannot transmit because send capability lives in a different process it cannot reach. The same philosophy governs how a handed-over system is maintained. A Tier-2 repair session — a Successor-Operator approving while Claude drives — must be unable to perform high-capability-class operations, for the same structural reason the generation process is unable to send: the capability is not present in that session's reach, regardless of what the session is asked to do.

High-capability-class is defined structurally, not by who is asking. It is anything that touches the External Send Gate, secrets/auth, doctrine, or that requires a code change. High-capability-class operations are Developer-Operator-only and always escalate to Tier 3. The complementary low-capability-class set (re-run a daemon, toggle an ITS_Config value, re-send an approval, re-seed a row, clear a stuck lock) is the only set in scope for a Tier-2 Successor-Operator repair.

This through-line is a principle, not yet a built control. Invariant 1's gating is real and verified in code (tests/test_capability_gating.py inspects script imports so a generation process literally cannot import send capability). The equivalent boundary for maintenance — a guard layer that keeps a Tier-2 repair session out of high-capability-class operations and that holds WITHOUT a Developer-Operator present to adjudicate an override — DOES NOT YET EXIST. Today's guard hooks are scoped to subagent/developer sessions and fall open for the human's own session, on the assumption that human is a developer who can safely override; that assumption fails for a non-developer Successor-Operator. Building the non-developer-safe enforcement layer is a pre-cutover requirement, tracked alongside the Tier-1 self-heal/watchdog completion gap (forensic-audit Check H). Until it exists, the Tier-2 boundary holds by documented discipline and approval, not by structural enforcement, and doctrine must never describe Tier-2 repair as capability-gated in the present tense.

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

- Foundation Mission (this doc, v10) — invariants, principles (including the Developer-Operator / Successor-Operator maintenance-role distinction and the capability-gating maintenance through-line), project-level architecture, per-customer-repo invariant.

- Operational Standards v15 — cross-cutting patterns every workstream uses; §43 successor-remediation discipline + §44 Tier-2 repair path.

- Vision & Roadmap v8 — phase plan with the ship-and-leave / developer-departure threshold and the Phase 1.5 security-hardening precondition.

- Handover Plan v7 — Phase 1.5 cutover + handover runbook with the three-tier fault-response model and operator-role abstraction.

- Permissions Ask v5 — cutover-phase admin grants; Successor-Operator (EDITOR) vs Developer-Operator (ADMIN) split.

- Excellence Roadmap v3 — R4 + R5 + R6 (successor-maintenance build program) status.

- Foundation Scaffold Update v6.5 — execution-layer state.

- Memory Archive v5 — operational detail.

- Smartsheet Handoff v5 + System+HR Handoff v6 — sibling docs.

- Cascade Unification Update 2026-05-22 Security Hardening — cascade event record.

# Authority

Foundation Mission v10, 2026-05-29. Operating-principle addition: maintenance is performed under two named roles — Developer-Operator (git/CC/shell-fluent; Tier-3 escalation asset; sole performer of developer-context operations) and Successor-Operator (non-developer; Smartsheet-UI + approval only; Claude-driven; low-capability-class repairs only). Invariant 1's two-process capability-gating philosophy is composed into a maintenance through-line: a Tier-2 repair session is structurally barred from high-capability-class operations (External Send Gate, secrets/auth, doctrine, or anything requiring a code change). The non-developer-safe enforcement layer that would hold this boundary without a Developer-Operator present is named as a pre-cutover build requirement, NOT a present capability, tracked alongside the Tier-1 self-heal/Check H gap. Invariant principles, the six-layer structure, and Layers 1–4 + 6 are unchanged from v9; v9's Layer 5 tripwire framing carries forward verbatim. v9 retires on acceptance of v10. Canonical git tag: foundation-mission-v10.

v11 trigger: substantive invariant principle change, business-model change, any defense-layer addition/removal/recharacterization, or any change to the maintenance-role principle or the capability-gating through-line. v10.x absorbs status updates (including "the non-developer-safe enforcement layer is now built") without a framing change.

Companion to Op Stds v15, V&R v8, Handover Plan v7, Excellence Roadmap v3, FSU v6.5, Memory Archive v5.