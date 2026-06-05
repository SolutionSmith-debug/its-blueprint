---
type: session_log
status: archived
workstream: safety_portal
tags: [doctrine-change, mission-bump, brief-bump, safety-portal, workspace-topology, deploy-resolved, wsr-human-review, drift-flags]
---

# 2026-06-05 — Safety Portal blueprint reconciliation (mission/brief → v2; topology + deploy resolved)

Chat-side session bringing the blueprint current with the as-built Safety Portal (execution HEAD `ffad86b` — Phase 5 PR 1 landed mid-session) and the 2026-06-04/05 design+build decisions. Doctrine-authoring only — no execution code touched. Companion to the [2026-05-28 portal-pivot reconciliation](2026-05-28_portal-pivot-reconciliation.md) and the [2026-05-25 grill-me log](2026-05-25_safety-portal-grill.md).

## What landed this session

- **`workstreams/safety-portal/mission.md` → v2** and **`brief.md` → v2** (supersede v1, 2026-05-25). Both restate the two Foundation invariants **verbatim** from [Foundation Mission v11](../doctrine/foundation-mission.md) (the portal touches both external-bound send and external-content ingestion).
- **`references/memory-archive.md`** — appended **§G21** (the consolidated reconciliation) and pointered the stale "Operations workspace" locations in §G16/§G18/§G19.
- **`references/claude-code-info-gap.md`** — resolved the "topology TBD / mission §11 assumed Pages" notes to Workers; refreshed `last_verified_against` → `ffad86b` and the "Last refreshed" line; marked Phase 4 complete + Phase 5 PR 1 landed.
- **`references/{foundation-scaffold,project-organization,smartsheet-handoff}.md`** — added the sixth `ITS — Safety Portal` workspace to the topology tables (pending the §23 doctrine bump); `last_verified` refreshed.
- The three queued session-close commits (`5367505`, `d3a8131`, `d1dd076`) were pushed to `origin/main` at the top of the session.

## Decisions absorbed (the as-built that postdates mission/brief v1)

1. **Deploy = Cloudflare Workers + Static Assets**, not Pages (Pages in maintenance mode). A single Worker serves the SPA + same-origin `/api/*`. **Requires Workers Paid (~$5/mo)** — the free plan's 10 ms CPU cap cannot run bcrypt cost-10 (Error 1102).
2. **Standalone `ITS — Safety Portal` workspace.** The Safety Portal folder + sheets were moved there from `ITS — Operations`, IDs preserved. Config stays in `ITS — System`. **Workspace access = approval authority.**
3. **`WSR_human_review`** central approval sheet (Phase-5 design) supersedes `WPR_Pending_Review` for the safety path: one row per (job, week), compiled PDF, editable email body = source of truth for send, recipients, Approve-for-Scheduled-Send + Send-Now, auto-stamped Approved By/At.
4. **PDF rendered in Python (Option B)**, not client-side TS (a v1 architecture reversal).
5. **The portal never reads or writes Smartsheet** — job/form data is served from D1; the Python pipeline holds the only Smartsheet/Box write credentials (verified in `safety_portal/worker/index.ts`). This corrects §G16's "the sheets the portal reads" framing.
6. **Job ID = 6-digit `AUTO_NUMBER`** (`JOB-000001`), UI-created; legacy kebab **`Job Slug` retired**. **Saturday→Friday** weeks. Recipient columns are **TEXT** (MULTI_CONTACT_LIST drops external emails on read-back).
7. **Phase 4 complete** — PRs #164/#166/#167 landed (the CC brief listed PR2/PR3 as "in flight"; verified merged). **Phase 5 PR 1 (back-half foundation: `WSR_human_review` sheet + weekly PDF merge + `sheet_ids` constants + amendments b/c) landed mid-session** (PR #168, `ffad86b`); the intake/compile/gated-send wiring is the rest of Phase 5.

## Non-obvious reconciliation: the forms count

The CC brief said "5 parents + 7 variants"; memory-archive §G20 (PR #164's intermediate state) recorded "11 definitions / 5 parents + 6 variants." Verified against HEAD `2946184`: the definition set was **revised** by PR #166/#167 to **10 definition files = 5 parents** (JHA, Equipment Pre-Inspection, HSS&E Work Observation, Visitor Sign-In, Toolbox Talk) **+ 7 variants** (equipment: skid-steer, telehandler; toolbox-talk: back-sprains, electrical, ergonomics, hard-hat, ppe). The CC brief's "5 + 7" is correct for the current as-built; the "11" was superseded. The doctrine docs state the durable structure and named parents and do **not** pin the (drifting) definition-file count.

## ⚑ Open flags for the operator (NOT actioned this session)

These are deliberately left for operator decision — two touch version-gated doctrine; one is execution-repo code.

1. **Op Stds §23 + §24 doctrine bump (v17).** §23 ("five-workspace audience-separated model… No change") and §24 (sheet-ID bootstrap, 5 workspaces) do not acknowledge the sixth, standalone, approval-gated `ITS — Safety Portal` workspace. Doctrine is version-gated; **not edited here**. Proposed framing for §23: "five-workspace audience-separated + one-workspace standalone approval-gated (Safety Portal)." Reference docs were updated to the six-workspace reality with a "pending §23 bump" note so they don't imply the doctrine already changed.

2. **`WPR_Pending_Review` → `WSR_human_review` drift in sibling/handoff docs.** `workstreams/safety-reports/mission.md` (v5.1, line ~47) and `brief.md` (v6.1, lines ~115/119), plus `references/system-hr-handoff.md` (lines ~41, ~179, ~191-201), still name `WPR_Pending_Review` as the safety approval surface. The safety pipeline's approval sheet is now `WSR_human_review` in the Safety Portal workspace. Reconciling those is a sibling-workstream / handoff-doc edit (a `safety_reports` v5.2/v6.2 + system-hr-handoff touch) beyond this session's portal scope — **flagged, not done**, to keep the version bump intentional.

3. **`shared/sheet_ids.py` label + workspace-ID drift (execution repo) — RESOLVED mid-session by Phase 5 PR 1 (PR #168).** At authoring time the folder constant was still `FOLDER_OPERATIONS_SAFETY_PORTAL` with no `WORKSPACE_SAFETY_PORTAL` constant (the move was live in Smartsheet, IDs preserved → code functioned, labels lagged). PR #168 then added `WORKSPACE_SAFETY_PORTAL = 194283417429892`, renamed the folder to `FOLDER_SAFETY_PORTAL` (`FOLDER_OPERATIONS_SAFETY_PORTAL` kept as a back-compat alias), and added `SHEET_WSR_HUMAN_REVIEW`. No execution tech-debt remains for this item.

## Authority / scope

Doctrine-authoring session. Files touched: `workstreams/safety-portal/{mission,brief}.md` (v2), `references/{memory-archive,claude-code-info-gap,foundation-scaffold,project-organization,smartsheet-handoff}.md`. Doctrine (`doctrine/*`) intentionally **not** edited — the §23/§24 bump is flagged above for operator approval per the version-gated-doctrine rule.

Cross-references:
- [Safety Portal mission v2](../workstreams/safety-portal/mission.md) · [brief v2](../workstreams/safety-portal/brief.md)
- [memory-archive §G21](../references/memory-archive.md)
- [Operational Standards §23/§24](../doctrine/operational-standards.md) — doctrine bump flagged
- [Foundation Mission v11](../doctrine/foundation-mission.md) — invariants restated verbatim
- [2026-05-28 portal-pivot reconciliation](2026-05-28_portal-pivot-reconciliation.md)
