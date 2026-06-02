---
type: reference
version: 1
status: canonical
last_verified: 2026-05-24
last_verified_against: 3b7d56d
workstream: null
tags: [smartsheet-schema, observability, polling-daemons]
---

**ITS_Daemon_Health — Schema ****&**** Runner Heartbeat Contract**

Version: v1

Author: chat-side parallel session to PR #59

Date: 2026-05-21

Scope: Smartsheet-side scaffolding for polling-daemon operator visibility across all current and future runners.

Authority: Op Stds v10 §23 (5-workspace topology), §3.1 (Push-vs-Record Separation), §30 (SDK-vs-Live Integration Test).

# 1. Live IDs

Paste these into PR #59's brief and any follow-up work. All IDs verified live in Smartsheet at doc-write time.

| **Asset** | **Name** | **ID** |
| --- | --- | --- |
| Workspace | ITS — System | 680592632244100 |
| Folder | 04 — Daemons (NEW) | 2130046845511556 |
| Sheet (canonical) | ITS_Daemon_Health | 4529351700729732 |
| ITS_Config row | daemons.heartbeat_sheet_id | 3528790636429188  (Value = 4529351700729732) |
| ITS_Config row | daemons.health_report_id | 8032390263799684  (Value = TBD — see §7) |
| ⚠ Empty duplicate | ITS_Daemon_Health (empty duplicate) | 3717381690969988  — operator-delete in UI |

## 1.1 Cleanup: duplicate empty sheet

A second ITS_Daemon_Health sheet (ID 3717381690969988) was created during this session before the canonical sheet landed. It has zero columns and zero rows. The Smartsheet MCP does not expose a delete-sheet primitive; operator action required:

- Open ITS — System → 04 — Daemons in Smartsheet.

- Two sheets appear with the same name. Open each by ID; the empty one has no columns. Right-click → Delete.

- Confirm only one ITS_Daemon_Health (ID 4529351700729732) remains.

# 2. Folder placement

Created a new folder 04 — Daemons under ITS — System rather than placing the sheet in an existing folder. Rationale:

- 01 — Config holds static-lookup tables (ITS_Config, Picklist_Sync_Config). ITS_Daemon_Health is runtime state, not config.

- 02 — Logs holds immutable forensic records (ITS_Errors, ITS_Quarantine). ITS_Daemon_Health is a push surface that gets overwritten every cycle — directly contradicts the append-only convention of that folder.

- 03 — Queues holds operator-action queues (ITS_Review_Queue). ITS_Daemon_Health is not an action queue.

- 04 — Daemons groups all future runner-related sheets (daemon registry, heartbeats, maybe a future daemon-config sheet) under one operator-visible heading. Forward-compatible to retrofits and new workstreams.

This expansion of the System workspace folder set is the only structural deviation from the brief. Adopt or revert; the sheet itself is folder-agnostic and can be moved without breaking anything (shared/sheet_ids.py will reference SHEET_DAEMON_HEALTH directly).

# 3. Schema

All columns on sheet ID 4529351700729732. Column IDs are stable for the life of the sheet and should be referenced by ID (not title) in shared/* code, per the existing smartsheet_client.py pattern.

| **#** | **Column Title** | **Type** | **Column ID** | **Purpose** |
| --- | --- | --- | --- | --- |
| 0 | Daemon Name | TEXT_NUMBER (PRIMARY) | 817803644145540 | Stable runner identifier in dotted notation. Used as the de-facto key for row-update-in-place. Examples: safety_reports.intake_poll, shared.picklist_sync, watchdog. |
| 1 | Workstream | PICKLIST | 5321403271516036 | Controlled vocabulary: global, safety_reports, po_materials, subcontracts, email_triage, ai_employee. Prevents free-text drift across runners. |
| 2 | Enabled | CHECKBOX | 3069603457830788 | Operator-tunable. True = daemon is expected to write heartbeats. False = paused (e.g., disabled-by-launchd, MAINTENANCE state, or not yet shipped). Health report filters on Enabled=true so paused daemons don't trip alerts. |
| 3 | Interval Seconds | TEXT_NUMBER | 7573203085201284 | Planning-placeholder for the daemon's launchd interval (numeric, seconds). The runtime daemon reads its actual interval from its own ITS_Config row (e.g., safety_reports.intake.poll_interval_seconds); this column documents the design intent and feeds the stale-heartbeat threshold (2 × Interval Seconds). |
| 4 | Source ID | TEXT_NUMBER | 1943703550988164 | What the daemon polls (free text). Email address for mailbox pollers, sheet ID for Smartsheet-driven daemons, descriptive string ('N/A — multi-source') for cross-cutting runners like watchdog. |
| 5 | Last Heartbeat | TEXT_NUMBER | 6447303178358660 | ISO-8601 UTC timestamp the daemon writes at the end of every cycle. TEXT_NUMBER (not DATETIME) so the runner can write the canonical string format without locale risk; the operator-view report does its staleness math by comparing to now(). |
| 6 | Last Cycle Status | PICKLIST | 4195503364673412 | Controlled vocabulary: OK, WARN, ERROR, SKIPPED, NEVER_RAN, STALE. See §5 for the meaning of each. |
| 7 | Last Cycle Items Processed | TEXT_NUMBER | 8699102992043908 | Integer count for the most recent cycle. Mailbox pollers: number of new messages handled. Picklist sync: number of mappings written. Watchdog: number of checks passed. Defaults to 0. |
| 8 | Total Cycles Today | TEXT_NUMBER | 536328667434884 | Running count of cycles completed since 00:00 UTC today. Resets at UTC midnight (runner-side, on the first cycle of the new day; detect by comparing previous Last Heartbeat's date). |
| 9 | Last Error Summary | TEXT_NUMBER | 5039928294805380 | Short human-readable description (one sentence). Populated only when Last Cycle Status is ERROR or WARN. Cleared on the next OK cycle. |
| 10 | Last Error Correlation ID | TEXT_NUMBER | 2788128481120132 | Correlation_ID from the matching ITS_Errors row, so the operator can pivot directly from this sheet to the forensic record. Populated when Last Cycle Status is ERROR; optional for WARN. |
| 11 | Notes | TEXT_NUMBER | 7291728108490628 | Free-text operator notes. Persistent across cycles — the runner must NOT overwrite this column. (See §4.2 for the write rule.) |

## 3.1 Schema deviations from brief

Two refinements made during chat-side build, both judgment calls retained in the canonical sheet:

- Workstream column → PICKLIST (brief said TEXT_NUMBER). Controlled vocabulary {global, safety_reports, po_materials, subcontracts, email_triage, ai_employee} matches the same picklist already in use on ITS_Config, ITS_Errors, ITS_Review_Queue, and ITS_Quarantine. Prevents free-text drift across runners.

- Last Cycle Status PICKLIST gained a 6th option, STALE (brief listed 5). STALE is reserved for the health-report layer — not a status a runner writes directly. See §5 for semantics. If never used in practice, harmless; if a future watchdog successor wants to write it, the option already exists.

# 4. Heartbeat write pattern — row-update-in-place

Brief asked the open question: append-per-cycle vs. update-in-place. Decision: update-in-place, one row per daemon, always-current. Rationale below; pattern below that.

## 4.1 Why update-in-place

- Operator clarity. The operator opens the sheet and sees one row per daemon, current state at the top. Append-mode would put yesterday's heartbeat next to today's and make 'is this daemon currently healthy' a sort-and-scroll problem.

- Push-vs-Record Separation (Op Stds v10 §3.1). The heartbeat is a push (overwrite-OK). The forensic record is ITS_Errors (append-only). This sheet is NOT trying to be a replacement for ITS_Errors — for any historical 'was this daemon healthy at time T,' the operator pivots to ITS_Errors via Correlation ID.

- Sheet-size hygiene. A 60-second-interval daemon would generate 1440 rows/day in append-mode. After a month, the sheet would be 43k rows. Update-in-place: 5 rows, stable.

- shared/smartsheet_client.py already supports the update-by-cell pattern (used by review_queue and quarantine). The runner-side helper that wraps this is trivial.

## 4.2 Write rule for runners

Every cycle, the runner does one update_rows call against ITS_Daemon_Health with the following column writes against its own row (looked up by Daemon Name):

| **Column** | **Always?** | **Value** |
| --- | --- | --- |
| Last Heartbeat | Yes | ISO-8601 UTC at the moment the cycle completed (whether OK, WARN, ERROR, or SKIPPED). |
| Last Cycle Status | Yes | One of {OK, WARN, ERROR, SKIPPED}. NEVER_RAN is the initial seed-row value, never written by the runner. STALE is reserved for the report layer. |
| Last Cycle Items Processed | Yes | Integer count for this cycle. 0 if no work. |
| Total Cycles Today | Yes | Previous value + 1. Reset to 1 if the previous Last Heartbeat's UTC date differs from now's UTC date. |
| Last Error Summary | Conditional | Set when Last Cycle Status ∈ {WARN, ERROR}. Cleared (write empty string) on OK or SKIPPED. |
| Last Error Correlation ID | Conditional | Set when Last Cycle Status = ERROR (matches the ITS_Errors row's Correlation_ID). Optional for WARN. Cleared on OK or SKIPPED. |
| Daemon Name | No | Never overwritten — it's the lookup key. |
| Workstream | No | Set at registration time, never overwritten by the runner. |
| Enabled | No | Operator-tunable, never overwritten by the runner. |
| Interval Seconds | No | Set at registration, may be operator-edited. |
| Source ID | No | Set at registration, never overwritten. |
| Notes | No | Operator-only. Runner must never write this column. |

## 4.3 Row-lookup pattern

Find the row by Daemon Name (the primary column) before each write. Pseudocode:

# Once per runner startup (or cache for daemon lifetime):

row_id = find_row_by_primary(SHEET_DAEMON_HEALTH, 'safety_reports.intake_poll')

# Every cycle:

update_rows(SHEET_DAEMON_HEALTH, [{

    'id': row_id,

    'cells': [

        {'columnId': COL_LAST_HEARTBEAT,      'value': utc_iso_now()},

        {'columnId': COL_LAST_CYCLE_STATUS,   'value': 'OK'},

        {'columnId': COL_LAST_CYCLE_ITEMS,    'value': items_processed},

        {'columnId': COL_TOTAL_CYCLES_TODAY,  'value': total_cycles_today},

        {'columnId': COL_LAST_ERROR_SUMMARY,  'value': ''},

        {'columnId': COL_LAST_ERROR_CORRID,   'value': ''},

    ]

}])

Failure mode: if the row lookup fails (Daemon Name not found), the runner should write to ITS_Errors with category 'daemon_health_unregistered' and continue its primary work. Heartbeat failure must NEVER block the daemon's primary work — failure isolation, same doctrine as the triple-fire alert legs.

# 5. Last Cycle Status semantics

| **Status** | **Meaning** |
| --- | --- |
| OK | Cycle completed successfully. Items Processed reflects work done. Last Error Summary cleared. |
| WARN | Cycle completed but with a non-fatal anomaly the operator should see (e.g., source returned an unusually large dataset, soft thresholds exceeded). Last Error Summary populated; Items Processed reflects partial work. |
| ERROR | Cycle failed. Items Processed is the count up to the failure point. Last Error Summary + Correlation ID populated. The error itself also writes to ITS_Errors per the standard triple-fire path. |
| SKIPPED | Cycle ran but elected not to do work (e.g., kill switch in MAINTENANCE, no new items to process). Distinguished from OK so the operator can tell 'healthy and idle' from 'healthy and busy.' |
| NEVER_RAN | Initial state. Daemon is registered in this sheet but has not yet executed a cycle. Cleared on first heartbeat write. |
| STALE | Reserved for the health-report layer — not for direct runner writes. The report flags rows where now() − Last Heartbeat > 2 × Interval Seconds. (Optional: a watchdog successor can rewrite a stale row's status here as an explicit signal; for now, the report does the math.) |

# 6. Seed rows

All five rows present at doc-write time with NEVER_RAN status. The runner flips its row to a live status on its first cycle.

| **Daemon Name** | **Workstream** | **Enabled** | **Interval s** | **Source ID** | **Status** | **Notes (short)** |
| --- | --- | --- | --- | --- | --- | --- |
| safety_reports.intake_poll | safety_reports | False | 60 | safety@evergreenmirror.com | NEVER_RAN | PR #59 target. Daemon reads its operational interval from ITS_Config row safety_… |
| safety_reports.weekly_generate | safety_reports | False | 604800 | Daily Reports sheets (per project) | NEVER_RAN | R3 session 2 target. Generates Weekly Rollups from Daily Reports rows; writes to… |
| safety_reports.weekly_send | safety_reports | False | 604800 | WPR_Pending_Review (3096105695793028) | NEVER_RAN | R3 session 3 target. Picks up approved WPR rows, sends via Resend to per-project… |
| shared.picklist_sync | global | True | 3600 | Picklist_Sync_Config (7486553185013636) | NEVER_RAN | Existing daemon (PRs #45–51); retrofit to write heartbeat post-cascade. Interval… |
| watchdog | global | True | 3600 | N/A — multi-source (Checks A–F) | NEVER_RAN | Existing daemon; retrofit to write heartbeat post-cascade. Check F currently pol… |

# 7. Daemon Health — Operator View report

Smartsheet's REST API does not support programmatic report creation (POST /reports is not a public endpoint; reports are UI-only at creation time). Operator action required to build the report; this section is the spec. ITS_Config row daemons.health_report_id stays as TBD until populated.

## 7.1 Report spec

- Workspace: ITS — System.

- Source sheet: ITS_Daemon_Health (4529351700729732).

- Columns to show: Daemon Name, Workstream, Enabled, Interval Seconds, Last Heartbeat, Last Cycle Status, Last Error Summary, Last Error Correlation ID.

- Filter logic (AND): Enabled = true. Show only rows that need operator attention. Within that, OR-group: Last Cycle Status ∈ {ERROR, WARN, NEVER_RAN, STALE}, OR Last Heartbeat older than 2 × Interval Seconds.

- Sort: Last Heartbeat ascending (oldest first — most attention-worthy on top).

- Daily check: operator opens the report once daily; an empty report means all enabled daemons are healthy.

## 7.2 Step-by-step build (operator)

- In Smartsheet, navigate to ITS — System workspace. From the workspace context menu (•••), choose Create → Report → Row Report.

- Name: 'Daemon Health — Operator View'. Save into ITS — System workspace (NOT inside 04 — Daemons; the report sits at workspace level so it's discoverable next to the workspace dashboard if one is added later).

- Source Sheets: pick ITS_Daemon_Health (only).

- Columns: select the 8 columns listed in §7.1.

- Filters: Enabled = checked. Then add OR group: Last Cycle Status is one of (ERROR, WARN, NEVER_RAN, STALE). The 'older than 2× Interval Seconds' staleness check is a custom-formula filter — Smartsheet supports this as a relative-date condition on Last Heartbeat. If the relative-date wizard is fussy, fall back to a simpler 'Last Heartbeat older than 2 hours' threshold for now and tune once it's in operator-hand.

- Sort: Last Heartbeat ASC.

- Save. Copy the report ID from the URL (the long numeric segment after /reports/).

- Update ITS_Config row 8032390263799684 (daemons.health_report_id): set Value to the copied report ID. The chat or cc can do this via Smartsheet MCP update_rows once the operator pastes the ID.

# 8. PR #59 handoff — heartbeat write in intake_poll.py

This section is the contract cc folds into PR #59 (or lands as a small PR #59.5 follow-up). The brief gives the operator choice; folding into PR #59 is cleaner since it ships heartbeat-write atomically with the trigger refactor.

## 8.1 Where to write

intake_poll.py's main loop has a natural shape:

def main_loop():

    while not shutdown_requested():

        cycle_start = utc_now()

        try:

            items = poll_and_process()       # existing intake logic

            status, items_count = 'OK', len(items)

            err_summary, err_corr_id = '', ''

        except KillSwitchPaused:

            status, items_count = 'SKIPPED', 0

            err_summary, err_corr_id = 'kill_switch=PAUSED', ''

        except Exception as e:

            corr_id = log_to_its_errors(e)    # existing triple-fire path

            status, items_count = 'ERROR', items_handled_so_far

            err_summary, err_corr_id = str(e)[:200], corr_id

        finally:

            write_heartbeat('safety_reports.intake_poll', status,

                items_count, err_summary, err_corr_id, cycle_start)

        sleep(poll_interval_seconds())

## 8.2 write_heartbeat helper (where it lives)

Chat-side, we don't extract a shared helper yet — that's PR #60 territory after the second real consumer (intake_poll + picklist_sync retrofit) per Op Stds v10 §14 preservation-over-refactor. For PR #59, write the heartbeat directly in intake_poll.py against the smartsheet SDK's row-update call, using the column IDs in §3 above. The PR #60 shared/runner.py extraction will absorb it cleanly when the second consumer arrives.

## 8.3 What the heartbeat write must NOT do

- MUST NOT raise to the caller. Wrap in try/except, log to ITS_Errors with category 'daemon_health_write_failed' on failure, continue. The daemon's primary work is more important than its own observability.

- MUST NOT block on Smartsheet API rate limits. If a rate-limit retry sequence exceeds 5 seconds total, abandon the heartbeat for this cycle and continue. The next cycle's heartbeat will reflect the current state.

- MUST NOT write Daemon Name, Workstream, Enabled, Interval Seconds, Source ID, or Notes — see §4.2.

- MUST NOT overwrite a row whose Daemon Name doesn't exactly match. Lookup failure → log to ITS_Errors and continue (no row creation; registration is an operator-side activity to keep the runner roster auditable).

## 8.4 Test for PR #59 (or #59.5)

- Unit test: write_heartbeat called with each status produces correct cell-write payload.

- Unit test: write_heartbeat swallows exceptions (mocked smartsheet client raises; assertion: no exception bubbles to caller; assertion: ITS_Errors log call recorded).

- Integration test (gated, -m integration per Op Stds v10 §30): real Smartsheet call against the live ITS_Daemon_Health row 7461022174478212 (safety_reports.intake_poll seed row), verify Last Heartbeat ISO timestamp lands and Total Cycles Today increments. Use update_rows directly — no SimpleNamespace mocks at the SDK boundary.

# 9. Forward-compatibility notes

## 9.1 Adding a new daemon

- Add a row to ITS_Daemon_Health with: Daemon Name (e.g., 'subcontracts.intake_poll'), Workstream, Enabled=false, Interval Seconds, Source ID, Notes. Last Cycle Status = NEVER_RAN.

- Wire the daemon's write_heartbeat call (same column IDs and status semantics).

- Flip Enabled=true at daemon ship.

- The operator-view report inherits the new daemon automatically — no report-side change needed.

## 9.2 Retrofitting existing daemons (post-cascade)

picklist_sync and watchdog already have seed rows with Enabled=true. The retrofit PRs only need to add the write_heartbeat call to each runner's main loop. No registry change.

## 9.3 PR #60 (shared/runner.py extraction)

When intake_poll lands and picklist_sync gets retrofitted, both daemons have the same heartbeat-write shape and the same poll-loop scaffolding. That's the ≥2 real reuse cases threshold from Op Stds v10 §14. Extract shared/runner.py at that point with: run_loop(daemon_name, interval_provider, cycle_fn), where cycle_fn returns (status, items_count, err_summary, err_corr_id) and run_loop handles the heartbeat write + sleep + kill_switch check + exception isolation.

## 9.4 Watchdog Check F retirement

Today, watchdog Check F polls the safety@evergreenmirror.com mailbox for idle hours as a proxy for 'is intake_poll alive.' Once intake_poll is shipping heartbeats and the operator-view report is in place, Check F is redundant — the report's 'Last Heartbeat older than 2 × Interval Seconds' filter is the cleaner check. Retirement is a follow-up PR after this scaffolding lands and intake_poll is live.

# 10. Process-discipline notes

- Push-vs-Record Separation (Op Stds v10 §3.1) honored: ITS_Daemon_Health is a push surface (overwrite every cycle); ITS_Errors remains the forensic record. No attempt to replace ITS_Errors with this sheet.

- SDK-vs-Live (Op Stds v10 §30) deferred to cc: chat-side built no shared/* code. Integration test for write_heartbeat is named in §8.4 as PR-#59-or-#59.5 scope.

- Verify-before-fix honored: live-inspected System workspace topology before sheet creation. Confirmed no pre-existing daemon-health sheet (apart from the empty duplicate, flagged in §1.1).

- Preservation-over-refactor (Op Stds v10 §14): no shared/runner.py abstraction. Heartbeat write goes directly into intake_poll.py in PR #59. PR #60 extracts at the second consumer.

- White-glove framework default: the schema and folder pattern reproduces in every customer fork. Daemon Name namespaces (workstream.runner) are stable across customers; only the seed rows differ.

# 11. Open items at session close

- Operator: delete the empty duplicate sheet (ID 3717381690969988) via Smartsheet UI. ~30 seconds.

- Operator: create the 'Daemon Health — Operator View' report per §7.2. ~5 minutes.

- Operator (or cc): update ITS_Config row 8032390263799684 (daemons.health_report_id) with the new report ID. Smartsheet MCP update_rows.

- cc: fold §8 contract into PR #59 (or land as PR #59.5).

- Post-cascade follow-up PRs: retrofit picklist_sync and watchdog to write heartbeats. Same pattern as intake_poll.

- **[SUPERSEDED — pending references-pass, added 2026-06-02]** The "retrofit picklist_sync and watchdog to write heartbeats" follow-up immediately above — and the matching §6 roster notes ("`retrofit to write heartbeat post-cascade`", `NEVER_RAN`) on the `shared.picklist_sync` and `watchdog` rows (~L174–175) — describe the **pre-Check-C** ITS_Daemon_Health per-daemon heartbeat-read model. That model was **never built**: the implemented Tier-1 staleness floor is the watchdog **Check C marker-file** check (`scripts/watchdog.py`), which already covers all four tracked daemons, plus the external **UptimeRobot** ping (audit F16) as the total-host dead-man's switch; the watchdog is deliberately NOT self-tracked (its liveness is the F16 ping). This is inconsistent with the FM v11 / Op Stds v16 Tier-1 self-heal correction (blueprint PR #34) and the exec watchdog **Check I** weekly_generate catch-up (`its` PR #133). **Tracked correction (do not blind-delete — preserve provenance):** in the next references-pass, rewrite L174–175 (and reconcile this Open-items bullet) to the Check C marker-file model. This is a **logged-not-fixed** item — the stale rows remain until that pass.

- After Op Stds v10.1 cascade: add §31 (or extend §23) with the 04 — Daemons folder and ITS_Daemon_Health sheet schema. shared/sheet_ids.py adds FOLDER_SYSTEM_DAEMONS and SHEET_DAEMON_HEALTH constants.