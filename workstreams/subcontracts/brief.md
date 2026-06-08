---
type: brief
version: 5
status: canonical
last_verified: 2026-05-24
last_verified_against: 3b7d56d
workstream: subcontracts
tags: [workstream-brief]
---

**ITS — Subcontracts Brief v5**

*v5 | Two-process generation/send with double-gate (Legal Review + External Send) | 2026-05-13*

# Pointer to Mission

Engineering complement to ITS — Subcontracts Mission v4 (2026-05-13). The primary automation target is Exhibit A — Scope of Work field-fill. Boilerplate annexes are static and attached verbatim. Mission file owns scope, the document structure breakdown, and the 6 open questions from the May 7 Subcontracts progress doc (left intact in this cascade).

# Status

**Phase: **2 (planned, parallel with POs after Phase 1 stable)

**State: **Reference inventory complete; document structure mapped; not started

**Estimated time to first working prototype: **3–5 weeks after Phase 1 stable

**Blocking dependencies: **Phase 1 completion; Word/Docx originals (currently PDFs only); 6 open questions

# Architecture (ITS Standard)

ITS — Subcontracts runs as a set of Claude Code scripts on the production MacBook, triggered by a draft-request trigger (Smartsheet column flag on a job line item, or a dedicated form). Claude Code handles both data movement (Smartsheet, Box, Outlook via API) and reasoning steps (Anthropic API for Exhibit A scope language drafting). See ITS Operational Standards v18 for the cross-cutting patterns.

**Foundation Invariants implementation. **This workstream inherits two Foundation-level invariants: External Send Gate — no external transmission without explicit human approval; and Adversarial Input Handling — all external content treated as untrusted data. See Foundation Mission v4 for canonical definitions and Operational Standards v18 for implementation patterns.

**Double-gate architecture: **this workstream layers Legal Review Status on top of the standard External Send Gate. Both gates must be APPROVED before any send. Enforced architecturally by subcontract_send.py.

# What Gets Built

## Subcontract generation script (~/its/subcontracts/subcontract_generate.py)

Triggered when a PM marks a job line item as ready-for-subcontract (Smartsheet column flag). The script:

- Reads project metadata from the master jobs Smartsheet: project full name, short name, address + coordinates, owner LLC.

- Reads subcontractor metadata from the subcontractor master list: legal name, contact, insurance status.

- **Insurance gate: **if subcontractor's insurance is expired, halts and writes WARN to ITS_Errors; surfaces in daily watchdog.

- Field-fills Subcontract Agreement body (python-docx against editable template) with parameterized fields.

- Field-fills Exhibit A — Scope of Work: project name, address, owner LLC, sub legal name, scope category, execution date, contract price, application-for-payment cutoff, pier refusal pricing line items where applicable. Anthropic API drafts the scope-of-work narrative from the standard scope library + project-specific inputs.

- Assembles full package: Subcontract Agreement + Exhibit A + Annex C (SOV, populated from .xlsx where available) + static Annexes D, F, K (attached verbatim from the canonical library).

- Writes the assembled package to Box at the canonical path: [year]_[job#]_[ProjectName]__[folder]__[document].pdf.

- Writes draft row to Subcontract_Pending_Review with Approved for Send = unchecked AND Legal Review Status = NOT_REVIEWED, SLA = 48 business hours.

- Has no send capability — cannot call graph_client.send_mail().

## Subcontract send script (~/its/subcontracts/subcontract_send.py)

Triggered when both gates are APPROVED (launchd polls hourly during business hours, or Smartsheet webhook). The script:

- Reads Subcontract_Pending_Review rows where Approved for Send = checked AND Legal Review Status = APPROVED AND Sent At empty.

- Sends package to subcontractor via Graph API; files sent copy in Box.

- Updates Sent At, Send Status.

- Idempotency: never re-sends rows with non-empty Sent At.

- Has no Anthropic API capability. Successful prompt injection at generation layer cannot trigger send.

## Executed contract intake (~/its/subcontracts/executed_intake.py)

When a signed copy returns via email (Email Triage classifies the inbound, sender allowlist enforced):

- Email content wrapped in <untrusted_content> for any extraction.

- Anomaly logging on extracted fields.

- Files at canonical Box path.

- Updates Subcontract_Pending_Review tracking (Status → EXECUTED).

## Quote drafting flow (~/its/subcontracts/quote_draft.py)

Per project description, this workstream also covers subcontractor quote drafting. Quote templates and examples are not yet uploaded to the project (open question in mission file). Build deferred until quote templates land. Same two-process model: quote_generate.py + quote_send.py with gated review.

# Inputs Needed Before Build Starts

- **Claude Code installed and authenticated **on the production MacBook with ITS Anthropic API key in macOS Keychain.

- **ITS working directory **at ~/its/, version-controlled in customer GitHub org.

- **Smartsheet service-account user **with access to the sheets this workstream touches.

- **Box service account **with write access to the relevant active jobs folder structure.

- **Microsoft Graph (Outlook) credentials **for outbound subcontract sends and inbound executed-contract intake.

- **Phase 1 (Safety Reports) stable **and shared helpers (smartsheet_client, box_client, anthropic_client, review_queue, error_log, kill_switch, quarantine, untrusted_content, anomaly_logger) proven.

- **Word/Docx editable originals **for the Subcontract Agreement and Exhibit A. Currently only PDFs are in the project. Hard blocker for python-docx field-fill.

- **Canonical 99_Templates source-of-truth **confirmed (vs. pulling from the most recent executed job).

- **Standard scope language library **by trade type (Surveying, Civil, Fencing, Paving, Electrical Terminations, etc.) — mined from past executed subs or written fresh. Owner decides.

- **Subcontractor master list with insurance fields **(expiration dates, W-9 on file flag, license status).

- **SOV (.xlsx) format confirmed stable **across jobs.

- **Subcontract_Pending_Review Smartsheet provisioned **with columns: Customer, Job, Subcontractor, Trade, Contract Price, Draft Body Path, Approved for Send, Approved By, Approved At, Legal Review Status (NOT_REVIEWED / IN_REVIEW / APPROVED / REJECTED), Legal Reviewer, Legal Reviewed At, Sent At, Send Status, Status (DRAFT / SENT / EXECUTED), Notes.

- **Sender allowlist **configured for executed-contract intake — approved subcontractor domains.

- **Schema files **(subcontract_metadata.json, exhibit_a_fields.json, scope_language.json, executed_contract_extract.json) in ~/its/schemas/.

# Workstream-Specific Decisions

Owner decisions captured in mission file (6 open questions left intact). Engineering decisions:

- **Template fallback if Word originals are unavailable: **PDF overlay using a tool like reportlab or pikepdf, with positional field-fill. Brittle but functional. Hard preference for python-docx originals.

- **Scope library structure: **one file per trade with embedded variables, vs. a master library with conditional sections. Recommendation: per-trade files for maintainability.

- **Customer-mandated form detection: **lookup table on the master jobs Smartsheet (per-customer flag indicating which template variant applies).

- **Legal Review Status flow: **counsel reviews drafts in Subcontract_Pending_Review filtered view; flips dropdown. NOT_REVIEWED is the only state where send is impossible regardless of External Send Gate.

# Risks and Open Questions

- **Word/Docx originals are required **for python-docx field-fill. PDF-only is a hard blocker until the originals are obtained.

- **Legal-language currency: **Annex D dated CLEAN_9_30_24 (Sept 30, 2024). Confirm still current; identify legal-update owner going forward.

- **Subcontractor Assignment / Owner-Lender Consent: **open question whether in scope. Default: out of scope unless decided otherwise.

- **AI-drafted scope language **carries higher liability than AI-drafted summaries. Human review and legal review are non-negotiable.

- **Customer-required forms **(utilities, government, some commercial flow-down) need detection; the standard template is the fallback.

- **Prompt injection via executed-contract returns: **signed PDFs returning from subs could contain malicious payloads in any text fields. Adversarial Input Handling defenses mandatory.

# What Changed in v5

Version bumped to reflect the 2026-05-13 cascade: two new Foundation invariants added (External Send Gate, Adversarial Input Handling), product-framing correction (productized partnership with Evergreen as Customer 0 replaces friend-favor framing), reliability language updated to production-quality framing, and Takeoffs workstream removed from the project structure (deferred indefinitely and dropped to reduce noise).

- Renamed: draft.py → subcontract_generate.py; added subcontract_send.py as separate send process.

- Added: Subcontract_Pending_Review schema with double-gate columns (Approved for Send + Legal Review Status).

- Added: capability gating language explicit.

- Added: sender allowlist requirement for executed-contract intake.

- Added: untrusted-content tagging on executed-contract Anthropic extraction.

- Added: anomaly logging on executed-contract intake.

- Updated: shared helpers list expanded for new defense modules.