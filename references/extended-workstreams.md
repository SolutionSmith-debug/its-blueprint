---
type: reference
version: 4
status: canonical
last_verified: 2026-05-24
last_verified_against: 3b7d56d
supersedes: references/extended-workstreams.md@v4
workstream: null
tags: [phase-2-plus, future-workstreams]
---

**ITS Extended Workstreams Brief v4.1**

2026-05-22 — Pointer Overlay Refreshing v4 References

*Status overlay on v4 · Op Stds + invariants + trigger-pattern pointers refreshed · Substance unchanged*

# Purpose of v4.1

Pointer-overlay on Extended Workstreams Brief v4 (2026-05-13). Absorbs SIX cascade events worth of operational standards reference drift (v5 → v11) plus the polling-daemon doctrine retirement of Mail.app rules. No change to the Tier 1 / Tier 2 workstream card content; pure pointer refresh.

v4 retires on acceptance of v4.1; v4.1 is operative reference. v5 trigger remains substantive workstream-card restructure or addition (not anticipated).

# What Changed in v4.1

- Operational Standards pointer: v5 → v11 (six cascade events absorbed).

- Foundation invariants reference: Foundation Mission v4 → v8.

- Trigger-pattern reference: "Mail.app rule fires Claude Code script" deprecated; polling daemon (Op Stds v11 §31) is canonical.

- Allowlist mechanism reference: ITS_Config JSON allowlist deprecated; ITS_Trusted_Contacts sheet (Op Stds v11 §33) is canonical.

- Attachment screening reference: Op Stds v11 §34 four-layer pipeline applies to any workstream ingesting attachments.

- All Tier 1 and Tier 2 workstream card content carries forward verbatim from v4.

# v4 Substance (Carried Forward Verbatim)

Captures workstreams beyond the original four (Safety Reports, POs/Materials, Subcontracts, Email Triage) plus AI Employee Capabilities. Two groups: Tier 1 extensions of existing workstreams, and Tier 2 construction/renewables-specific workstreams that stand alone.

Architecture (refreshed in v4.1): every automation here follows ITS Operational Standards v11, including the two Foundation invariants per FM v8 (External Send Gate, Adversarial Input Handling with 6-layer defense including attachment screening). Each runs as a Claude Code script on the MacBook, triggered by launchd-driven polling daemons (canonical pattern per Op Stds v11 §31) with Shortcuts for manual operator-triggered jobs. No new architectural patterns; everything reuses the foundation stack.

Format: compact "automation cards" rather than full briefs. Each card is enough to scope and prioritize. A full brief gets created when a card is promoted to active build.

# Tier 1 — Extensions of Existing Workstreams (Carried Forward Verbatim)

These extend or sit adjacent to the original four and inherit their patterns directly. v4 enumerates ~6-8 Tier 1 cards including Vendor Invoice Matching to POs, Insurance Certificate Tracking, Lien Waiver Tracking, etc. Substance unchanged; trigger references refreshed:

- Trigger references universally updated: "Mail.app rule fires Claude Code script" → "polling daemon (Op Stds v11 §31) fetches from allowlisted senders."

- Allowlist references universally updated: "allowlisted senders" → "ITS_Trusted_Contacts sheet with scope enforcement (Op Stds v11 §33)."

- Attachment-handling references universally updated: any card ingesting PDFs/Office docs inherits the 4-layer attachment screening pipeline (Op Stds v11 §34).

For full v4 card content (which carries forward unchanged in substance), reference ITS_Extended_Workstreams_Brief_v4_2026-05-13.docx for the Tier 1 + Tier 2 enumeration. v4.1 is a pointer-only overlay.

# Tier 2 — Construction/Renewables-Specific Workstreams (Carried Forward Verbatim)

Stand-alone workstreams specific to construction and renewables operations. v4 enumerates cards like RFI Tracking, Safety Incident Reporting, Site Visit Log, etc. Substance unchanged; trigger references refreshed per Tier 1 pattern above.

# Adversarial Input Handling Implementation (Refreshed in v4.1)

All Extended Workstreams cards inherit Invariant 2 per FM v8 — six defense layers, not five (v4 referenced five). The sixth layer (attachment screening pipeline) is new in v8 and applies to every card ingesting attachments. Sender allowlist mechanism upgrades from ITS_Config JSON list to ITS_Trusted_Contacts sheet with project + workstream scope enforcement plus SPF/DKIM/DMARC + Return-Path header-forgery detection.

Card-level implementation notes for Adversarial Input Handling in v4 cards should be read as referring to the v8 enforcement patterns — same principle, evolved implementation.

# Authority

Extended Workstreams Brief v4.1, 2026-05-22. Pointer overlay on v4 (2026-05-13) absorbing six cascade events of Op Stds drift + FM invariant evolution + polling-daemon doctrine + trusted-contacts pattern + attachment screening pipeline.

v5 trigger criteria: substantive Tier 1 or Tier 2 card restructure, new card addition, or scope reduction. v4.x absorbs further pointer-drift status updates without card-substance changes.