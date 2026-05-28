---
type: mission
version: 6
status: canonical
last_verified: 2026-05-28
last_verified_against: c5cc456
workstream: email_triage
tags: [workstream-mission]
---

**ITS — Email Triage Mission v6**

*v5 | Adversarial Input Handling as primary architecture; Layer 6 attachment screening assigned to this workstream | 2026-05-28*

# Mission

Classify inbound mail at one or more shared Evergreen mailboxes and route each message into the appropriate downstream ITS workstream or to a human review queue when classification is uncertain. Reduce the manual triage burden on whoever currently reads the shared inbox.

**Architectural significance: **this workstream is the primary entry point for external content into ITS. The Foundation Mission v8 Invariant 2 (Adversarial Input Handling) applies more directly here than anywhere else — sender allowlist, untrusted-content tagging, capability gating, structured output enforcement, anomaly logging, and attachment screening (Layer 6) are mandatory architecture, not optional defenses.

**Note on grounding: **no May 7 progress doc exists for this workstream. Content here remains forward-looking until a first orientation session produces real reference material. Below content is conceptual and subject to revision once a progress doc is generated.

# Product Context

ITS is being built with Evergreen Renewables as Customer 0 — the first deployment and design partner, receiving the system at no cost during validation. Solution Smith owns all IP, with explicit intent to iterate and offer ITS to additional construction and renewables customers.

# Foundation Invariants Inherited

This workstream inherits two Foundation-level invariants: External Send Gate — no external transmission without explicit human approval; and Adversarial Input Handling — all external content treated as untrusted data. See Foundation Mission v8 for canonical definitions and Operational Standards v13 for implementation patterns.

**Adversarial Input Handling — implementation (primary focus of this workstream):**

- **Sender allowlist: **every shared mailbox under this workstream's classification has an explicit allowlist of permitted sender domains and addresses. Mail.app rule fires only on allowlisted senders; non-allowlisted mail routes to ITS_Quarantine.

- **Untrusted-content tagging: **every Anthropic API call wraps the email body, subject, and any extracted attachment text in <untrusted_content source="..."> XML tags. System prompt boilerplate directs the classifier to treat content as data only.

- **Structured output enforcement: **the classification response must conform to a JSON schema (category, confidence, rationale). Non-conforming responses rejected and routed to ITS_Review_Queue.

- **Capability gating: **the classifier script's only outputs are: write to ITS_Triage_Log, write to ITS_Review_Queue, or hand off to a downstream workstream's intake script. The classifier cannot send external email, cannot modify ITS_Config, cannot write outside its sandbox of allowed sheets.

- **Anomaly logging: **extracted classification fields are checked for sentinels (e.g., classifier returning a category outside the enumerated set, suspiciously long rationale, references to known injection phrases). Anomalies route to ITS_Review_Queue with security_flag = true; owner notified.

- **Attachment screening (Layer 6): **Email Triage ingests arbitrary inbound mail with arbitrary attachments, so it is the **load-bearing owner** of Foundation Mission v8 Invariant 2 Layer 6 (new in v8; implementation pattern in Operational Standards v13 §34). Every attachment passes four sub-layers before being uploaded to Box or referenced in any AI call: (a) static signature checks — magic-number verification, size sanity, filename pattern matching; (b) format-aware structural inspection — PDF JavaScript/embedded-file detection, Office macro detection, polyglot detection; (c) ClamAV antivirus scan via pyclamd; (d) optional VirusTotal hash check (Phase 2+ enhancement, deferred). Failure disposition: malicious → ITS_Quarantine + CRITICAL triple-fire + sender DISABLED in ITS_Trusted_Contacts pending operator review; suspicious → ITS_Review_Queue; clean → proceed. **Operator prerequisite:** ClamAV installed (Homebrew) with the `clamd` daemon running for sub-layer (c); an EICAR test signature in fixtures verifies pipeline health.

**External Send Gate — implementation: **this workstream does not directly send external mail — it routes inbound. However, mis-routed external content can flow into a downstream workstream's external-send path, so the gate at the destination workstream protects this layer as well. Defense in depth.

# Status

Phase 3 — deferred until Safety Reports + at least one other workstream are live with real downstream destinations. Building the classifier before the destinations exist means classifying mail with no place for it to go.

# Scope

**In**

- Inbound classification at designated shared mailboxes (allowlisted senders only).

- Routing into downstream ITS workstream intake (Safety Reports, POs, Subcontracts).

- Quarantine routing for non-allowlisted senders.

- Logging every triaged message with classification, confidence, route taken, anomaly flags.

- False-classification recovery surface (one-click reclassify and re-route).

- Calibration period reporting (accuracy on real traffic vs. benchmark).

**Out**

- Triage of individual employee mailboxes — only shared/role-based inboxes.

- Drafting responses to triaged messages — handled by the destination workstreams (which apply their own External Send Gate).

- Spam filtering at the M365 layer — already handled by Outlook.

- HR, legal, financial, and other PII-sensitive content categories — either excluded entirely or summary-only handling, owner decision.

# Open Questions / Blockers (forward-looking)

- **Shared mailbox(es) to triage. **Identify which inbox(es) get classified — the company general inbox, an ops inbox, or both.

- **Category list. **Starting set: safety report, supplier quote response, customer correspondence, internal admin, spam/marketing, unknown. Refine after seeing real mail.

- **Historical email sample. **100–200 recent inbound messages, hand-labeled with the correct category. Used to benchmark classifier accuracy before going live.

- **Confidence threshold. **Above what classifier confidence does ITS auto-route vs. send to human review. Tune from the historical sample.

- **PII / sensitive content handling. **Some inbound mail contains sensitive data. Decide whether the classifier sees full content or summary-only.

- **Sender allowlist seed. **Initial set of permitted senders — customer domains, supplier domains, internal Evergreen, known partner domains. Quarantine review cadence.

- **Inbound supplier quote response handling. **Per POs progress doc, inbound supplier quote responses need classification and routing back to the POs workstream's quote-comparison view. Schema to be defined jointly with POs.

# Architecture

ITS — Email Triage runs on the production MacBook via Claude Code, triggered by a Mail.app rule on each designated shared mailbox that fires the classifier on every inbound message from an allowlisted sender. The Mail.app rule itself filters non-allowlisted mail to a Quarantine folder, which a separate script logs to ITS_Quarantine and (optionally) notifies the owner of for review.

Two-process model adapted for triage:

- **Classification process **(classify.py) — calls Anthropic API with content wrapped in untrusted-content tags; produces structured classification; writes to ITS_Triage_Log and either routes to downstream intake (high-confidence) or to ITS_Review_Queue (low-confidence or anomaly).

- **Quarantine process **(quarantine.py, shared helper) — logs non-allowlisted senders to ITS_Quarantine; no Anthropic API call on quarantined content.

- **Recovery process **(reclassify.py) — detects reviewer-flipped Smartsheet columns and re-routes misclassified items.

The classifier has no capability to send external email. Downstream workstreams that produce external output (Safety Reports WPRs, POs RFQs, etc.) each have their own External Send Gate; a successful prompt injection at the classifier cannot trigger external send because the classifier never has send capability and the downstream gates are separate processes.

# Success Criteria

- Open questions resolved with decisions captured in writing.

- Classifier accuracy >90% on a held-out validation sample of historical mail.

- Zero customer-facing issues lost in routing during the first 60 days.

- False-classification recovery within 1 business day in 100% of cases.

- At least one downstream workstream receives meaningful inbound volume routed by the classifier within 30 days of go-live.

- Zero non-allowlisted senders processed by the classifier (sender allowlist 100% compliance).

- Zero successful prompt injections producing external action in the first 90 days. Anomaly logging detects attempts; no injection produces external send, schema-violating output, or routing override.

# Operating Principles

- Sender allowlist is mandatory. Non-allowlisted mail does not reach the classifier.

- All processed content is untrusted. Untrusted-content tagging on every Anthropic call. No exceptions.

- Confidence threshold for auto-route starts conservative (0.90) and tunes downward only as the log proves reliability.

- Below threshold, items go to human review — never silently auto-routed at low confidence.

- Sensitive-content categories (HR, legal, financial) are handled separately or excluded.

- Every triaged message is logged with full audit trail; no message is routed without a record.

- This workstream needs the longest calibration period of the five; plan for 30–60 days of tuning post-launch.

- First 90 days of operation double as prompt-injection stress test. Every anomaly flag investigated; sentinel patterns expanded as new attacks emerge.

# Cross-Workstream Impact

- **Inbound supplier quote responses **must route to the POs workstream's quote-comparison view. The schema for inbound-quote intake should be defined jointly with the POs workstream before either picks up real work.

- **Inbound safety reports **from field PMs must route to the Safety Reports workstream's intake. Coordination with Safety Reports' intake mechanism decision required. Safety Reports already enforces its own sender allowlist; Email Triage's allowlist is a superset for shared inboxes.

- **Executed contracts **returning from subs route to Subcontracts' executed_intake.

- **Customer correspondence **may need routing to a human queue (no current automation destination). Owner decides where customer mail surfaces.

- **Sender allowlist coordination: **each downstream workstream maintains its own allowlist for direct intake; Email Triage maintains a master allowlist for shared inboxes. Both are configurable via ITS_Config.

# What Changed in v4

Version bumped to reflect the 2026-05-13 cascade: two new Foundation invariants added (External Send Gate, Adversarial Input Handling), product-framing correction (productized partnership with Evergreen as Customer 0 replaces friend-favor framing), reliability language updated to production-quality framing, and Takeoffs workstream removed from the project structure (deferred indefinitely and dropped to reduce noise).

- Elevated: Adversarial Input Handling promoted from a defensive practice to the primary architecture of this workstream. Every architectural decision explicitly maps to one of the five defense layers.

- Added: Foundation Invariants Inherited section with detailed implementation guidance.

- Added: sender allowlist as a hard requirement (was implicit in Operational Standards v5; now explicit in mission).

- Added: prompt-injection stress-test framing for first 90 days.

- Added: Open Question #6 seed sender allowlist.

- Updated: Operating Principles — every principle now references either the gate or the defense layers.

- Updated: Success criteria — added zero-allowlist-bypass and zero-injection metrics.

- Removed: friend-favor and best-effort reliability language.

# What Changed in v6

Doctrine-version-reference sweep (2026-05-28 doc-reconciliation pass). The remaining stale Operational Standards citations are swept from **v11** to **v13** (current canonical — v12 added §§37–41, v13 added §42); Foundation Mission references were already at v8. Reference currency only — no scope, architecture, or decision change. The two **Operational Standards v5** mentions are historical provenance (when a pattern was first introduced) and are intentionally left. This also completes the bookkeeping for the v5 portal-pivot reconciliation, which bumped the frontmatter but left these citations and the Authority block behind.

# Authority & Versioning

This is the canonical mission for this sub-project (v6, 2026-05-28). It supersedes v5 (2026-05-28 portal-pivot reconciliation) and v4 (2026-05-13, which first centered Adversarial Input Handling as primary architecture and added the two Foundation invariants).