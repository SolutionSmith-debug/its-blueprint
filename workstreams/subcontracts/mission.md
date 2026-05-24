---
type: mission
version: 4
status: canonical
last_verified: 2026-05-24
last_verified_against: 3b7d56d
workstream: subcontracts
tags: [workstream-mission]
---

**ITS — Subcontracts Mission v4**

*v4 | Productization framing + Foundation invariants applied | 2026-05-13*

# Mission

Automate Evergreen's subcontract drafting from project metadata and standard scope language. The high-effort, automation-eligible portion of every subcontract package is Exhibit A — Scope of Work, which is heavily project- and trade-specific. Boilerplate annexes (D, F, K) and the Subcontract Agreement body are static and attached verbatim. The mission is field-fill of Exhibit A from Smartsheet job data + scope library + AI-drafted scope-specific language.

This workstream also covers subcontractor quote drafting (when a sub needs a quote prepared), per the original project description — though no quote templates have yet been uploaded to the project.

# Product Context

ITS is being built with Evergreen Renewables as Customer 0 — the first deployment and design partner, receiving the system at no cost during validation. Solution Smith owns all IP, with explicit intent to iterate and offer ITS to additional construction and renewables customers.

# Foundation Invariants Inherited

This workstream inherits two Foundation-level invariants: External Send Gate — no external transmission without explicit human approval; and Adversarial Input Handling — all external content treated as untrusted data. See Foundation Mission v4 for canonical definitions and Operational Standards v5 for implementation patterns.

**External Send Gate — implementation: **Subcontract_Pending_Review Smartsheet with Approved for Send (checkbox), Approved By, Approved At, Sent At, Send Status, Legal Review Status columns. Two-process model: subcontract_generate.py writes drafts (no send); subcontract_send.py reads approved rows (no AI). Subcontract send also requires Legal Review Status = APPROVED — belt-and-suspenders gating layered on top of External Send Gate.

**Adversarial Input Handling — implementation: **inbound executed-contract returns from subs (post-signature) treated as untrusted external content. Sender allowlist enforced. Untrusted-content tagging on any Anthropic extraction. Anomaly logging on extracted fields.

# Current State (per May 7 progress doc)

**Status: **in progress — reference-material inventory complete, engineering not started. Reference materials from past jobs loaded into the project (~96% of project capacity at the time). Inventory and structural assessment of the subcontract document set complete.

## Reference jobs represented in uploaded materials

- 2023.126 Oregon (Kendall) — Rodeo, Apricus, Lincoln subprojects.

- 2024.112 Almon Lomaside — Perrydale.

- 2025.108 Bonacci 1 & 2.

- 2025.112 Kendall CSP Port — Colfax, Coker.

- 2025.358 Keystone (templates only).

- 2025.364 Steger & Roxbury (active).

- 2025.201 KSI 4 IL (single document).

## Document structure identified

Each subcontract package consists of:

- **Subcontract Agreement — **boilerplate legal body, lightly parameterized (Contractor/Subcontractor names, project, date, contract price).

- **Exhibit A — Scope of Work — **heavily project- and trade-specific; this is where most field-filling happens. Primary automation target.

- **Annex C — Schedule of Values — **simple price/scope breakdown (one .xlsx example available: Steger/Roxbury Legacy SOV).

- **Annex D — Insurance Requirements **(“CLEAN_9_30_24”) — appears static across jobs.

- **Annex F — Lien Waivers — **static template; subcontractor fills at invoice time, not at contract drafting.

- **Annex K — Exhibit K-1 Testing Protocols — **static.

- **Other annexes referenced but not all uploaded: **B (Schedule), G (Sub-tier Vendors), H (OSHA Competent Personnel), J (Delivery Notice), L (Commissioning Forms).

## Fillable fields identified for Exhibit A

- Project full name (e.g., “Steger Solar Project”).

- Project short name (e.g., “Steger”, “Roxbury”).

- Project address + coordinates.

- Owner LLC (e.g., “Rodeo Solar, LLC”, “Coker Solar, LLC”, “Danville Farm, LLC”).

- Subcontractor legal name.

- Scope category (Surveying, Civil, Fencing, Paving, Electrical Terminations, etc.).

- Execution date (header + footer dates).

- Contract price.

- Application-for-payment cutoff (varies — 23rd vs 25th of month observed).

- Pier refusal pricing line items (varies; $1,200/refusal and $755/cut-and-drill seen on Bonacci).

## File-naming convention (stable across jobs)

[year]_[job#]_[ProjectName]__[folder]__[document].pdf — good signal that the Box filing structure can be predicted programmatically by ITS.

# Scope

**In**

- Exhibit A — Scope of Work generation from Smartsheet job data + scope library + AI-drafted scope language.

- Subcontract Agreement field-fill (Contractor/Subcontractor names, project, date, contract price).

- Annex assembly: D, F, K attached verbatim from the static library; C populated from the SOV when available.

- Subcontractor quote drafting (separate flow per project description).

- Gated send via Subcontract_Pending_Review with both External Send Gate approval AND Legal Review Status.

- Insurance certificate tracking with expiration alerts and renewal-request drafting (Tier 1 extension; later phase).

- Box filing per the established naming convention; Smartsheet tracking through draft → legal review → sent → executed.

**Out**

- Annexes D, F, K do not need ITS modification — attached verbatim.

- Subcontractor performance management — separate process if at all.

- Subcontractor payment processing — a downstream PO/AP concern.

- Pre-qualification / vetting of new subs — owner-driven, not automated.

- Subcontractor Assignment / Owner-Lender Consent forms — see open question; possibly out of scope.

# Closed Decisions (from May 7 progress doc)

- **Scope split confirmed: **Annexes D, F, K, and most of the Subcontract Agreement body are static and attached verbatim — ITS does not need to generate or modify them.

- **Exhibit A is the primary automation target. **This is where field-filling delivers most of the value.

- **File-naming convention is stable across jobs. **Box filing structure can be predicted programmatically.

# Open Questions / Blockers — LEFT INTACT

These remain unresolved. The 2026-05-13 cascade explicitly leaves these intact per owner direction.

- **Source-of-truth templates. **The 99_Templates folders contain “TBD Project” master files. Confirm these are the canonical templates to build automation against, vs. pulling from the most recent executed job.

- **Editable source files. **Only PDFs are uploaded for the Subcontract Agreement and Exhibit A. Need the Word/Docx originals for python-docx field-filling. PDF template engine is a fallback but more brittle. HARD BLOCKER.

- **SOV (.xlsx) format stability. **Only one Excel example is in the project (Steger/Roxbury Legacy SOV). Confirm column structure is consistent across jobs before automating.

- **Quote workflow. **Project description includes drafting subcontractor quotes (when a sub needs a quote drafted), but no quote templates are present. Need quote templates and an example or two before that path can be built.

- **Legal-language version. **Annex D filename CLEAN_9_30_24 suggests a Sept 30, 2024 legal review. Is that still current? Who owns legal updates going forward?

- **Subcontractor Assignment / Owner-Lender Consent. **Separate document seen in Kendall files (DEL Electric, OnPoint), executed at financing/substantial-completion milestones. Confirm whether this is in scope for the contract-drafting automation or handled separately.

# Architecture

ITS — Subcontracts runs on the production MacBook via Claude Code, triggered by a draft-request trigger (Smartsheet column flag on a job line item, or a dedicated form), with multi-step gating (legal review + External Send Gate) before any send. Claude Code handles data movement (Smartsheet, Box, Outlook via API) and reasoning steps (Anthropic API for Exhibit A scope language).

Two-process model with extra gate:

- **Generation: **subcontract_generate.py produces draft package; writes to Subcontract_Pending_Review with Approved for Send = unchecked AND Legal Review Status = NOT_REVIEWED.

- **Legal review: **human counsel reviews; flips Legal Review Status to APPROVED or REJECTED.

- **Send: **subcontract_send.py only acts on rows with BOTH Approved for Send = checked AND Legal Review Status = APPROVED. Hard rule.

# Success Criteria

- Open questions resolved with decisions captured in writing.

- Word/docx editable templates obtained for Subcontract Agreement and Exhibit A.

- Working Claude-API field-fill prototype on Exhibit A using one job's data, output to PDF, held for human review.

- Subcontract drafting time per agreement reduced by >70% relative to manual baseline.

- Customer-mandated subcontract forms (utilities, government, some commercial) detected and used in 100% of applicable cases.

- Legal review process preserved — every drafted subcontract reviewed by counsel before signing. Hard gate.

- Zero subcontracts sent without both External Send Gate approval and Legal Review APPROVED status.

# Operating Principles

- Every subcontract goes through legal review before signing — the existing process; automation feeds it, does not replace it. Legal review is a hard gate, layered on top of External Send Gate.

- Insurance gate is hard: subs with expired coverage cannot have a subcontract drafted until coverage is verified current.

- AI-drafted scope language is reviewed in every case; subtle scope errors carry construction-cost risk that exceeds the time savings.

- Static annexes are attached verbatim from the canonical library — the automation does not modify them.

- Inbound executed-contract returns from subs are untrusted content per Adversarial Input Handling.

# Cross-Workstream Impact

- **Foundation ****&**** PM: **Smartsheet jobs lookup needs to surface project name, address, owner LLC, sub name, scope category, and contract price.

- **Purchase Orders ****&**** Materials: **reuses the same Smartsheet lookup, supplier records, and Box filing patterns. Anything built here for sub identity/contact lookup should be designed to share with POs.

- **External Send Gate pattern: **extends the WPR/RFQ_Pending_Review pattern with a second gate (Legal Review Status) for this workstream.

- **Email Triage: **executed-contract send-out at end of flow uses the same Outlook integration as Safety Reports. Sender allowlist for sub-return intake is jointly maintained.

# Next Checkpoint

- Decision needed on items 1, 2, and 3 above (template source-of-truth, editable originals, SOV format).

- Once those are in hand, next milestone is a working Claude-API field-fill prototype on Exhibit A using one job's data, output to PDF, held for human review.

# What Changed in v4

Version bumped to reflect the 2026-05-13 cascade: two new Foundation invariants added (External Send Gate, Adversarial Input Handling), product-framing correction (productized partnership with Evergreen as Customer 0 replaces friend-favor framing), reliability language updated to production-quality framing, and Takeoffs workstream removed from the project structure (deferred indefinitely and dropped to reduce noise).

- Added: Foundation Invariants Inherited section with double-gate architecture (External Send Gate + Legal Review Status).

- Added: two-process generation/send model.

- Added: “LEFT INTACT” label on the 6 open questions per owner direction.

- Updated: Operating Principles — legal review framed as hard gate layered on External Send Gate.

- Updated: Success criteria — added zero-bypass metric on both gates.

- Removed: friend-favor and best-effort reliability language.