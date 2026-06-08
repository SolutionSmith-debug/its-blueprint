---
type: brief
version: 5
status: canonical
last_verified: 2026-05-24
last_verified_against: 3b7d56d
workstream: ai_employee_capabilities
tags: [workstream-brief]
---

**ITS — AI Employee Capabilities Brief v5**

*v5 | Tool-gated chat agent, untrusted-content on transcripts and retrievals | 2026-05-13*

# Pointer to Mission

Engineering complement to ITS — AI Employee Capabilities Mission v4 (2026-05-13). Five capabilities: ITS Chat, Proactive Daily Briefing, Voice Intake from Field, Meeting Notes & Action Items, Company Brain Semantic Search.

# Status

**Phase: **3+ (sequenced after foundation workstreams have at least 30 days of structured ITS data)

**State: **Not started; no progress doc; concept set established in May 9 vision

**Chat surface: **Microsoft Teams bot (confirmed by owner May 10, 2026)

**Earliest reasonable build start: **After Phase 2 stable; data exists to converse about

# Architecture (Tier 3 Additions)

All five capabilities run on the standard MacBook + Claude Code + Apple automation stack (see ITS Operational Standards v18). Tier 3 introduces three architectural additions beyond the foundation workstreams:

- **Chat surface: Microsoft Teams bot. **Confirmed by owner May 10, 2026. Holds conversation state in a per-user Smartsheet, calls Claude Code on demand to query Smartsheet/Box, renders responses naturally with citations.

- **Scheduled “thinking” job **(launchd-triggered Claude Code script, runs nightly) that synthesizes overnight events from across all workstreams into a one-page morning brief.

- **Audio + embeddings infrastructure **for voice intake and semantic search. Whisper or Anthropic-native audio for transcription. Vector store for semantic indexing of Box content.

**Foundation Invariants implementation. **This workstream inherits two Foundation-level invariants: External Send Gate — no external transmission without explicit human approval; and Adversarial Input Handling — all external content treated as untrusted data. See Foundation Mission v4 for canonical definitions and Operational Standards v18 for implementation patterns.

**Hardware lifecycle context: **by the time Phase 3+ work starts, hardware handover is complete. The production MacBook is customer-owned, sitting at customer site, with Solution Smith maintaining via Tailscale. All Tier 3 surfaces deliver to / interact with the owner directly through this customer-owned device.

# Capabilities (Engineering Detail)

## 1. ITS Chat

Conversational surface. Owner, PMs, and admin staff can ask ITS anything that touches structured ITS data.

- **Channel: **Microsoft Teams bot. Registered as an Entra ID app and deployed tenant-wide (Teams Administrator role required to deploy). Conversations happen in DMs to the bot (private to the user) or in dedicated Teams channels (shared with project members).

- **Implementation: **Claude Code agent loop with tool use. Initial tool set (read-only, capability-gated): smartsheet_query, box_search, box_read_doc, smartsheet_recent_changes, review_queue_status.

- **Tool gating: **no external-send tools in the initial set. Drafting an external email goes through the appropriate workstream's Pending_Review (e.g., chat drafts an RFQ → writes to RFQ_Pending_Review, NOT sent). Promotion to write-tools requires explicit per-tool review.

- **Citations: **every answer drawing from documents must cite the source (Smartsheet row link or Box document link).

- **Untrusted content: **any Box-retrieved content (especially received emails, vendor documents) wrapped in <untrusted_content source="box-document"> tags before being shown to the chat agent.

- **Conversation state: **stored in a per-user Smartsheet (ITS_Chat_Sessions) for cross-session continuity.

- **Initial rollout: **owner-only for first two weeks; PMs added second; admin staff third.

## 2. Proactive Daily Briefing

Scheduled launchd job (~/its/ai_employee/daily_briefing.py) runs nightly at e.g. 6:30 AM ET. The script:

- Reads everything in scope: open review-queue items past or near SLA, schedule changes since last run, expiring insurance certs, late deliveries, unhandled inbound mail (post-Email Triage), recent error log entries, Pending_Review items awaiting approval.

- Calls Anthropic API with a synthesis prompt: rank by urgency, summarize in plain English, deduplicate vs. yesterday's briefing.

- Output: compact email (or Teams message) at 7:00 AM ET. Length-controlled to 10–15 items max.

- Each item is one line + a link to the underlying Smartsheet row or Box document.

- Delivered to internal owner only — no External Send Gate needed for internal recipient.

## 3. Voice Intake from Field

Two channels: voice memo attachment to a designated email or Teams chat (simplest); call-in number that records and processes (highest adoption for non-tech-comfortable PMs).

- Audio file arrives (allowlisted sender/caller); gets uploaded to Box temp folder.

- Whisper or Anthropic-native audio transcribes.

- Transcript wrapped in <untrusted_content source="voice-transcript"> before Anthropic structuring call.

- Anthropic structures the transcript based on context: safety report? RFI? change request? punchlist item?

- Disambiguation goes to ITS_Review_Queue. Job and date inferred from caller ID + timestamp + content.

- Routes to the appropriate downstream workstream's intake (which has its own External Send Gate if it produces external output).

## 4. Meeting Notes & Action Items

Recorded meetings (Teams recordings auto-pickup; or dropped audio file) become structured notes.

- Recording origin verified (allowlisted meeting source).

- Whisper / Anthropic audio transcribes with speaker diarization where possible.

- Transcript wrapped in <untrusted_content source="meeting-transcript"> before Anthropic structuring.

- Anthropic structures: notes by topic, action items extracted with assignees inferred from context.

- Notes filed at canonical Box path; action items written to ITS_Actions Smartsheet.

- Follow-up emails drafted per action item, queued for human review via Pending_Review (no direct send).

- Consent and retention policies: must be defined before this ships. Customer or sub voices in recordings are sensitive.

## 5. Company Brain Semantic Search

Built into ITS Chat (capability 1). Semantic search is one of the things ITS knows how to do when asked.

- Box content gets indexed nightly: titles, full text where extractable, metadata.

- Embeddings generated via OpenAI text-embedding or Anthropic-native embeddings.

- Query: ITS Chat detects search intent, queries vector store for candidates, retrieves top-N, Anthropic synthesizes the answer with citations.

- Retrieved content wrapped in <untrusted_content source="company-brain"> before being shown to the chat agent. Especially relevant for retrieved received emails or vendor documents — these are external content authored outside the customer.

- Index freshness: nightly re-index of changed Box content; full re-index quarterly.

# Inputs Needed Before Each Capability Ships

- **Claude Code installed and authenticated **on the customer-owned MacBook with the customer-owned Anthropic API key.

- **ITS working directory **at ~/its/, in customer GitHub org by Phase 3+.

- **Smartsheet, Box, Microsoft Graph credentials **customer-owned the entire time.

- **ITS Chat: **Teams bot registered and deployed in the customer M365 tenant; at least 30 days of structured ITS data; controlled-rollout cohort plan; tool gating reviewed.

- **Daily Briefing: **ranking and synthesis prompt iterated on real overnight data; delivery channel (email / Teams / SMS).

- **Voice Intake: **channel(s) decided (voice memo email vs. call-in number); allowlist of permitted senders/callers; transcription accuracy benchmarked on real field-noise audio.

- **Meeting Notes: **consent and retention policy in writing; recording channel identified; allowlist of permitted meeting sources.

- **Company Brain Search: **vector store choice; initial Box indexing cost estimated; citation pattern enforced; untrusted-content tagging on every retrieval.

# Risks and Open Questions

- Mediocre is worse than nothing in Tier 3. A flaky chat surface destroys trust faster than slow Tier 1 rollout.

- Hallucination matters more here than anywhere else. When Claude confidently states the wrong PO number in chat, the cost is immediate and visible.

- Adoption is gated by trust, not features. The first ten interactions with ITS Chat must be good ones.

- Voice intake adoption is a change-management problem more than a technology problem.

- Construction sites are loud. Transcription accuracy in noise is the real benchmark.

- Indexing cost and freshness on Company Brain Search. Real-time indexing is expensive; nightly re-index is the realistic cadence.

- Citations are non-negotiable on chat answers.

- **Prompt injection via meeting recordings and voice intake: **external participants in meetings could intentionally include injection payloads in speech. Untrusted-content tagging is mandatory; first 90 days serve as stress test.

- **Prompt injection via Company Brain retrieval: **received emails or vendor documents in Box could contain injection payloads. Untrusted-content tagging on retrieved content is mandatory. Worst case: chat agent attempts to follow injected instructions; since the agent has no external-send tools, the worst it can do is misrepresent retrieved content to the user. Capability gating contains the blast radius.

- **Tool-gating drift: **over time, capability requests will arrive (“make the chat agent able to draft and send emails directly”). Every promotion must be reviewed against External Send Gate. The answer to “direct external send” is no — always route through Pending_Review.

# What Changed in v5

Version bumped to reflect the 2026-05-13 cascade: two new Foundation invariants added (External Send Gate, Adversarial Input Handling), product-framing correction (productized partnership with Evergreen as Customer 0 replaces friend-favor framing), reliability language updated to production-quality framing, and Takeoffs workstream removed from the project structure (deferred indefinitely and dropped to reduce noise).

- Added: Tool gating language on ITS Chat with conservative initial tool set.

- Added: untrusted-content tagging on voice transcripts, meeting transcripts, Company Brain retrievals.

- Added: Sender/caller allowlist for voice intake.

- Added: allowlist for meeting recording sources.

- Added: capability-promotion review process language.

- Added: prompt-injection risks specific to Tier 3 (meeting recordings, retrieved Box content).

- Updated: each capability flow includes the relevant defense layer step.