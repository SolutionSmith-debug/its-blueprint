---
type: brief
version: 6
status: canonical
last_verified: 2026-05-24
last_verified_against: 3b7d56d
workstream: purchase_orders
tags: [workstream-brief]
---

**ITS — Purchase Orders ****&**** Materials Brief v6**

*v6 | Two-process generation/send, sender allowlist on responses | 2026-05-13*

# Pointer to Mission

Engineering complement to ITS — Purchase Orders & Materials Mission v4 (2026-05-13). The deliverable here is RFQs (request-for-quotes sent to multiple suppliers), not finalized POs. Mission file owns scope, success criteria, and the 7 open questions from the May 7 PO_Materials_Update progress doc (left intact in this cascade).

# Status

**Phase: **2 (planned, parallel with Subcontracts after Phase 1 stable)

**State: **Reference corpus reviewed; existing PO templates inventoried; not started

**Estimated time to first working scripts: **3–5 weeks after Phase 1 stable

**Blocking dependencies: **Phase 1 completion; 7 open questions in mission file

# Architecture (ITS Standard)

ITS — Purchase Orders & Materials runs as a set of Claude Code scripts on the production MacBook, triggered by an RFQ-request intake (form or email — mechanism per open question), with multi-supplier addressing handled in a single script run plus a separate gated send. See ITS Operational Standards v18 for the cross-cutting patterns this workstream inherits (kill switch, watchdog, error logging, review queue, structured outputs, sender allowlist, untrusted-content tagging, capability gating, anomaly logging, remote access, hardware lifecycle).

**Foundation Invariants implementation. **This workstream inherits two Foundation-level invariants: External Send Gate — no external transmission without explicit human approval; and Adversarial Input Handling — all external content treated as untrusted data. See Foundation Mission v4 for canonical definitions and Operational Standards v18 for implementation patterns.

**Hardware lifecycle context: **by Phase 2 the system is in production at the customer site (post-handover). Build-phase work for new Phase 2 capabilities happens in sandbox; deployment via Tailscale.

# Closed Decision: No Auto-Issue (Permanent)

Every ITS-drafted RFQ requires human review before going to suppliers. There is no path that bypasses review. Permanent rule, not time-bounded. Enforced architecturally by the two-process model: generation script has no send capability.

# What Gets Built

## Two RFQ generation scripts

Two material classes warrant two distinct templates and routing paths. Both write drafts to RFQ_Pending_Review; neither has any external-send capability.

- **~/its/po_materials/standard_rfq_generate.py **— generic project materials. Inputs: standard PO template (Purchase_Order_2019.docx-derived), shorter response window, Evergreen approved-supplier list.

- **~/its/po_materials/racking_module_rfq_generate.py **— racking and module RFQs. Inputs: racking-flavored template (ESS_Field_Purchase_Order_Terms_and_Conditions.docx-derived); longer response window; vendor-specific approved-supplier list.

## Common generation flow

- Receive structured request (job, line items, ship-to, response-by date).

- Look up job in master Smartsheet (job address → ship-to; sales-tax rate from job state; legal entity per current Evergreen Renewables LLC decision once resolved).

- Generate RFQ document via python-docx field-fill against the appropriate template.

- Anthropic API drafts free-form scope notes or special terms when needed; output reviewed before merge.

- Write draft row to RFQ_Pending_Review with Approved for Send = unchecked, SLA = 24 business hours.

- No send capability — cannot call graph_client.send_mail().

## Gated send script (~/its/po_materials/rfq_send.py)

- Triggered when RFQ_Pending_Review row is approved (launchd polls hourly during business hours, or on Smartsheet webhook if configured).

- Reads only rows where Approved for Send = checked AND Sent At empty.

- Sends to each supplier on the addressed list via Graph API (one email per supplier — cleaner reply-routing in Email Triage stage).

- Updates Sent At, Send Status. Files copy of sent RFQ in Box.

- Idempotency enforced: rows with non-empty Sent At never re-sent.

- No Anthropic API — only structured data movement. Successful prompt injection at generation layer cannot trigger send.

## Awarded PO filing flow (~/its/po_materials/awarded_po_intake.py)

When a vendor returns a finalized PO, Email Triage classifies the inbound mail (sender allowlist enforced) and routes the document here:

- Identifies the originating RFQ via PO number lookup or sender + job reference. Content wrapped in <untrusted_content> for any Anthropic extraction.

- Anomaly logging runs on extracted fields.

- Files the awarded PO at the canonical Box path.

- Updates the RFQ_Pending_Review row (or related ITS_RFQs row) with awarded vendor, awarded amount, awarded date.

- Surfaces in daily watchdog if no awarded PO is received within the response-by window.

# Inputs Needed Before Build Starts

- **Claude Code installed and authenticated **on the production MacBook with the ITS Anthropic API key stored in macOS Keychain.

- **ITS working directory **at ~/its/, version-controlled in customer GitHub org by Phase 2 start.

- **Smartsheet service-account user **with access to the sheets this workstream touches.

- **Box service account **with write access to the relevant active jobs folder structure.

- **Microsoft Graph (Outlook) credentials **for outbound RFQ sends and inbound supplier response intake.

- **Phase 1 (Safety Reports) stable **and the shared helpers (smartsheet_client, box_client, anthropic_client, review_queue, error_log, kill_switch, quarantine, untrusted_content, anomaly_logger) battle-tested.

- **Resolution of the 7 open questions **from the May 7 PO_Materials_Update progress doc — intake mechanism, supplier database, RFQ template approach, RFQ numbering, tax/ship-to logic, T&C addenda, legal entity / ship-from address.

- **RFQ templates **(standard and racking/module) drafted and version-controlled in ~/its/templates/po_materials/.

- **RFQ_Pending_Review Smartsheet provisioned **with the same gated-review column set as WPR_Pending_Review, adapted for RFQ context (Job, Line Items, Suppliers Addressed, Response By, Approved for Send, Approved By, Approved At, Sent At, Send Status, Notes).

- **Supplier master list **in known location (Smartsheet, Box, or QuickBooks) with consistent fields the scripts can read.

- **Sender allowlist **configured for supplier-response intake — approved supplier domains added to ITS_Config sender_allowlist field.

- **Schema files **(rfq_request.json, rfq_supplier_response.json, awarded_po.json) in ~/its/schemas/.

# Workstream-Specific Decisions

Owner decisions captured in mission file (7 open questions left intact). Engineering decisions:

- **Template engine: python-docx vs. PDF-overlay. **Recommendation: python-docx for editable templates. PDF as fallback if Word originals are unavailable.

- **Supplier addressing: **single email with all suppliers BCC'd vs. one email per supplier. Recommendation: one email per supplier — cleaner reply-routing in the Email Triage stage.

- **Quote comparison surface: **where do supplier responses get aggregated for owner review? Smartsheet view recommended.

- **Polling vs webhook for approval detection: **polling (launchd hourly) is simpler; webhook (Smartsheet API) is responsive. Start with polling.

# Risks and Open Questions

- **PO process documentation **may not be written down anywhere — what we automate is what's currently in PMs' heads. Plan for a discovery conversation with whoever issues RFQs today.

- **Existing PO numbering **may have gaps that the automation will surface. Decide upfront whether to fix the historical record or start fresh from a known-good number.

- **Customer-required PO terms **vary; the template needs a customer-conditional block.

- **Tax-rate accuracy: **state-by-state rates change. Recommendation: read sales-tax rate from the master jobs Smartsheet (per-job field) rather than hardcoding.

- **Legal entity on outbound mail: **the E.S.S. LLC vs. Evergreen Renewables LLC question must be resolved before any RFQ is sent. Hard block.

- **Prompt injection via supplier responses: **supplier email or quote attachments could contain injection payloads. Adversarial Input Handling defenses mandatory; first 90 days serve as stress-test period.

# What Changed in v6

Version bumped to reflect the 2026-05-13 cascade: two new Foundation invariants added (External Send Gate, Adversarial Input Handling), product-framing correction (productized partnership with Evergreen as Customer 0 replaces friend-favor framing), reliability language updated to production-quality framing, and Takeoffs workstream removed from the project structure (deferred indefinitely and dropped to reduce noise).

- Renamed generation scripts to *_generate.py (was *_rfq.py); added rfq_send.py as separate send process.

- Added: RFQ_Pending_Review Smartsheet schema.

- Added: Capability gating language explicit — generation scripts cannot send; send script has no AI.

- Added: Sender allowlist requirement for supplier-response intake.

- Added: Untrusted-content tagging requirement on every supplier-response Anthropic extraction.

- Added: Anomaly logging on awarded-PO intake.

- Updated: “Closed Decision” framed as permanent (not time-bounded).

- Updated: shared helpers list expanded for new defense modules.