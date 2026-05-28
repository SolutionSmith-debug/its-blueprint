---
type: session_log
status: archived
workstream: null
tags: [portal-pivot, high-2-supersession, attachment-screening, invariant-2, email-triage, layer-6, cross-repo-drift]
---

# 2026-05-28 — Portal-pivot reconciliation + HIGH-2 supersession (planning-side log)

Planning-side companion to the execution-repo log `~/its/docs/session_logs/2026-05-28_portal-pivot-reconciliation.md`. Captures the blueprint-side decisions; the execution log carries the per-PR detail.

## Purpose

The Safety Portal pivot (this repo's `workstreams/safety-portal/mission.md` v1, 2026-05-25 canonical) superseded the 2026-05-28 forensic audit's HIGH-2 (attachment screening) for safety reports. This session reconciled the execution repo to that already-canonical doctrine, reassigned Invariant 2 Layer 6 to the workstream that actually owns the arbitrary-attachment surface (Email Triage), and added a cross-repo drift guard. **Blueprint wins on doctrine; no doctrine was invented.**

## Blueprint changes

- **`workstreams/email-triage/mission.md` (v4 → v5) + `brief.md` (v5 → v6)** — PR #15. Added Invariant 2 Layer 6 (attachment screening) as load-bearing for Email Triage, mirroring Foundation Mission v8 §34 sub-layers (a)–(d) verbatim: malicious → ITS_Quarantine + CRITICAL triple-fire + sender DISABLED; suspicious → ITS_Review_Queue; clean → proceed. Added the `clamd` (Homebrew ClamAV + pyclamd) operator prerequisite to "Inputs Needed Before Build"; VirusTotal sub-layer (d) deferred to Phase 2+. Reconciled the FM v4→v8 / Op Stds v5→v11 refs the new layer directly contradicted; refreshed `last_verified` to 2026-05-28 / exec HEAD `09f8c02`.
- **`references/memory-archive.md` §G8** — this PR. Restoration detail for the portal-pivot reconciliation (append-only, §G7 → §G8 per the canonical pattern).

## Decisions / rationale

- **Layer 6 belongs to Email Triage, not Safety Reports.** Portal signatures are SVG vector path data and PMs cannot attach arbitrary files (safety-portal mission §7 rules Layer 6 N/A for the portal), so the four-sub-layer attachment screen is not a safety-reports gate. Email Triage ingests arbitrary inbound mail with arbitrary attachments — FM v8 already names it a Layer 6 consumer — so the framework-default was applied to the workstream that owns the surface. Applying an existing FM v8 default to its rightful owner is in scope; it is not new doctrine.
- **Email Triage docs were version-stale** (cited FM v4 / Op Stds v5, "five defense layers"). Only the refs the Layer-6 addition directly contradicted were reconciled; broader pre-v8 staleness in those docs was left for a dedicated workstream-doc refresh and flagged in the PR.

## Coverage sweep (no drift)

All six blueprint workstreams have `mission.md` + `brief.md` with `status: canonical` frontmatter and slugs in `CANONICAL_WORKSTREAMS`. Execution repo: only `safety_reports` is built; the rest are coherently planned (reserved enum/folder/cap-gating templates), none stranded — AI Employee and PO/contract drafting specifically confirmed. Aliases `purchase_orders`↔`po_materials`, `ai_employee_capabilities`↔`ai_employee` are stable, not drift.

## Note on tooling

The repo-local `.claude/agents/` (`session-close-maintainer`, `session-log-writer`, `brief-validator`, `ops-stds-enforcer`) were **unreachable** this session — the CC session was rooted at `/Users/sethsmith`, not `~/its`, and the agent registry is fixed at session start. Manual equivalents were used throughout (lint scripts run directly, four-part verification via `gh`, these logs + the §G8 archive authored by hand). `references/claude-code-info-gap.md` §8 (Current State Snapshot) was NOT updated — flagged for the operator to run `session-close-maintainer` in-repo.
