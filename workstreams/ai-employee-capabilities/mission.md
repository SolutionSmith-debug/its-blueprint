---
type: mission
version: 4
status: canonical
last_verified: 2026-05-24
last_verified_against: 3b7d56d
workstream: ai_employee_capabilities
tags: [workstream-mission]
---

**ITS — AI Employee Capabilities Mission v4**

*v4 | External Send Gate on draft surfaces; productization framing | 2026-05-13*

# Mission

Provide the conversational and proactive surfaces that make ITS feel like an employee rather than a set of background flows. Five capabilities: ITS Chat, Proactive Daily Briefing, Voice Intake from Field, Meeting Notes & Action Items, and Company Brain Semantic Search.

**Why this is the headline differentiator: **the foundation workstreams (Safety, POs, Subs, Triage) produce real value but are largely invisible. This sub-project is what the owner and team interact with directly. The shift from “the system handles X” to “I just asked Claude” is what makes ITS perceptually different from a workflow tool.

**Note on grounding: **no May 7 progress doc exists for this sub-project — it is a forward-looking concept set established in the May 9 vision and roadmap. Content here remains conceptual until a first session generates implementation specifics.

# Product Context

ITS is being built with Evergreen Renewables as Customer 0 — the first deployment and design partner, receiving the system at no cost during validation. Solution Smith owns all IP, with explicit intent to iterate and offer ITS to additional construction and renewables customers.

# Foundation Invariants Inherited

This workstream inherits two Foundation-level invariants: External Send Gate — no external transmission without explicit human approval; and Adversarial Input Handling — all external content treated as untrusted data. See Foundation Mission v4 for canonical definitions and Operational Standards v5 for implementation patterns.

**External Send Gate — implementation (primary concern for this workstream): **several capabilities produce content that could end up in external-bound messages — chat-drafted follow-up emails, daily briefing items that include drafted communications, meeting-notes-derived action items that produce follow-up emails. Every such path is gated by an explicit Pending_Review row before any external send. The capability surfaces (chat, briefing) can produce draft content visible internally without gating; the moment a draft is queued for external transmission, the gate applies.

**Adversarial Input Handling — implementation: **voice intake from field and meeting recordings are external content. Audio transcripts wrapped in <untrusted_content> tags before Anthropic structuring. Company Brain Semantic Search retrieves from Box content that may have been authored by external parties (e.g., received emails, vendor documents) — retrieved content is wrapped in untrusted-content tags before being shown to Claude in chat context.

# Status

Phase 3+ — sequenced after foundation workstreams have at least 30 days of structured ITS data. Cannot ship sensibly until there is real data to converse about, brief on, or search through.

# Capabilities

## 1. ITS Chat — Conversational Surface

- Owner, PMs, and admin staff can ask ITS anything that touches structured ITS data.

- Surface: Microsoft Teams bot. Confirmed by owner on May 10, 2026. Evergreen already standardizes on Teams as the primary collaboration tool, so ITS Chat lives where the team already works. Alternative surfaces (web app, terminal UI) are off the table unless this decision is revisited explicitly.

- Reads from the same Smartsheet/Box systems of record as every other workstream. No separate data layer.

- External Send Gate applies: when chat draft a follow-up email or external communication, the draft goes into the appropriate downstream Pending_Review sheet; the chat surface cannot directly send.

## 2. Proactive Daily Briefing

- Scheduled launchd job runs nightly on the MacBook; reads everything in scope; Claude Code synthesizes via Anthropic API into a one-page morning brief.

- Delivered by 7am ET via email or Teams message to the owner (internal recipient — no External Send Gate needed for the briefing itself).

- Length-controlled (10–15 items max, ranked).

- Becomes more valuable as more workstreams come online — more data to synthesize equals more useful briefing.

## 3. Voice Intake from the Field

- Voice memo or phone-call ingestion lets field PMs dictate hands-free — daily reports, RFIs, change requests, punchlist items.

- Anthropic-native audio or Whisper transcribes; Claude Code structures and routes.

- Adversarial Input Handling applies: transcripts treated as untrusted content; sender allowlist on the voice-intake channel (caller ID or recipient email allowlist).

- Adoption multiplier for Safety Reports specifically — PMs do not type well on phones in the rain.

## 4. Meeting Notes and Action Items

- Recorded meetings (with consent) become structured notes, action items, and follow-up email drafts.

- Whisper or Anthropic audio for transcription, Anthropic for structuring.

- Adversarial Input Handling applies: transcripts treated as untrusted content (external participants in meetings).

- External Send Gate applies: any follow-up email draft goes through Pending_Review before send.

- Consent and data-handling policies need to be defined before this ships.

## 5. Company Brain Semantic Search

- Searches across Box documents, drawings, specs, contracts, past correspondence.

- Built into ITS Chat (capability 1). Semantic search is one of the things ITS knows how to do when asked.

- Adversarial Input Handling applies: retrieved external content (received emails, vendor documents) wrapped in <untrusted_content> tags before being shown to Claude in chat context. Treat retrieved content as data, not instructions.

- Likely justifies a vector store (Pinecone, Weaviate, or Anthropic-native by the time Phase 4 lands).

# Architecture

ITS — AI Employee Capabilities runs on the production MacBook via Claude Code, triggered by Apple automation primitives — launchd schedules for time-based runs (daily briefing), Teams bot platform for ITS Chat events, and dedicated intake mechanisms for voice and meeting capture.

**Tier 3 architecture additions **(beyond the standard MacBook + Claude Code + Apple automation stack):

- Microsoft Teams bot as the chat surface.

- A scheduled “thinking” launchd job for the daily briefing.

- Audio + embeddings infrastructure (voice intake and semantic search). Both run inside the Claude Code / Anthropic stack with help: Whisper or Anthropic audio for transcription; a vector store for semantic search.

**Capability gating for chat: **ITS Chat is a Claude Code agent loop with tools. The tool set is gated by capability — smartsheet_query, box_search, review_queue_status (read-only). The chat agent CANNOT directly invoke external-send tools; if it drafts an external email, it writes to the appropriate Pending_Review sheet for human approval.

# Open Questions / Blockers (forward-looking)

- **Daily briefing delivery channel. **Email, Teams, SMS, or all three.

- **Voice intake channel. **Voice memo to email, dedicated phone number, or both. Sender/caller allowlist seed.

- **Meeting recording consent and retention. **Customer or sub voices in a recording are sensitive; storage, retention, and access policies need definition.

- **Vector store choice. **Pinecone, Weaviate, Anthropic-native (if available by Phase 4), or other. Decide closer to build.

- **Chat agent tool surface. **Initial tool set is conservative (read-only Smartsheet, Box, review queue). Promotion to write-tools or draft-tools requires explicit per-tool capability review.

# Success Criteria

- ITS Chat: owner uses it at least weekly within 30 days of launch; PM adoption follows.

- Daily Briefing: owner reads it consistently (open rate, not just delivery); content quality stays calibrated to actual events.

- Voice Intake: adopted by majority of field PMs within 60 days of go-live (adoption is the real metric, not capability).

- Meeting Notes: notes accurate enough that the human attendee uses them as the canonical record, not a starting point.

- Company Brain Search: zero citation failures (model citing a document that does not contain the cited claim).

- Zero ITS-Chat-drafted external messages sent without human approval (External Send Gate compliance 100%).

- Zero successful prompt injections via voice transcripts, meeting transcripts, or retrieved Box content in the first 90 days.

# Operating Principles

- Mediocre is worse than nothing in Tier 3. A flaky chat surface destroys trust faster than slow Tier 1 rollout.

- Hallucination is the dominant risk; every chat answer cites sources, and the chat is gated to internal owner-only use during initial calibration.

- Adoption is gated by trust, not features. The first ten interactions with ITS Chat must be good ones.

- Voice intake is a change-management problem more than a technology problem. Plan for change management explicitly.

- Each Tier 3 capability is gated on the previous one being adopted, not just shipped.

- External-bound content drafted by any Tier 3 capability flows through the appropriate downstream Pending_Review gate. No direct external-send capability anywhere in Tier 3.

- Retrieved external content (Company Brain) treated as untrusted data, not instructions.

# Cross-Workstream Impact

- All foundation workstreams must be live with at least 30 days of structured data before ITS Chat ships meaningfully.

- The daily briefing reads from every workstream's tracking sheet, error log, and review queue. Cross-workstream schema consistency matters here more than anywhere else.

- Voice intake writes into the foundation workstreams' intake mechanisms — e.g., a voice-dictated safety report enters the Safety Reports flow at the same point a typed/emailed report would. Safety Reports' sender allowlist must accommodate the voice-intake bridge.

- External Send Gate applies via downstream workstream Pending_Review sheets, not via this workstream directly. Every workstream that produces external output has its own gate; this workstream cannot bypass any of them.

# What Changed in v4

Version bumped to reflect the 2026-05-13 cascade: two new Foundation invariants added (External Send Gate, Adversarial Input Handling), product-framing correction (productized partnership with Evergreen as Customer 0 replaces friend-favor framing), reliability language updated to production-quality framing, and Takeoffs workstream removed from the project structure (deferred indefinitely and dropped to reduce noise).

- Added: Foundation Invariants Inherited section with External Send Gate as primary concern.

- Added: capability gating on chat agent tool set (read-only initial, explicit promotion review for write/draft tools).

- Added: untrusted-content tagging requirement for voice transcripts, meeting transcripts, and retrieved Box content (Company Brain).

- Added: zero-bypass and zero-injection metrics in success criteria.

- Updated: each of the 5 capabilities now explicitly references External Send Gate or Adversarial Input Handling where applicable.

- Removed: friend-favor and best-effort reliability language.