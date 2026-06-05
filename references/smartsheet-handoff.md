---
type: reference
version: 5
status: canonical
last_verified: 2026-06-05
last_verified_against: ffad86b
workstream: null
tags: [smartsheet, handoff, sheet-ids]
---

# ITS Smartsheet Handoff v5

**Date: **2026-05-21  |  **Supersedes: **Smartsheet Handoff v4 (2026-05-17)  |  **Workspace topology authority: **Op Stds v9.3 §23

## State at handoff

End of 2026-05-20 evening session. Smartsheet environment is in production-ready demo state on Bradley 1 (the showcase / template project). All structural changes are complete. Forms, Conditional Formatting, Filter Views, and Automation Rules remain deferred (UI-only, build at final pre-deployment per Op Stds v9.2 §6).

## Workspace topology (5 workspaces)

Per Op Stds v9.3 §23. Full inventory:

| **Workspace** | **ID** | **Folders** |
| --- | --- | --- |
| Forefront Portfolio — ITS Demo | 4129485730670468 | 01 — Active Projects; 02 — Portfolio Rollups; 03 — Field Reports (JHA/TBT) |
| ITS — Human Review | 8561891980142468 | (per existing Handoff v5 inventory) |
| ITS — Operations | 7217130472007556 | Master Databases (Vendor DB, Subcontractor DB, Equipment Master) |
| ITS — Archive | 5528280611743620 | Closed Projects (empty by design) |
| ITS — System | 680592632244100 | 01 — Config (incl. Picklist_Sync_Config from PR #46), plus existing system sheets |

> **Update 2026-06-04/05 — sixth workspace:** A standalone `ITS — Safety Portal` workspace was added (`WORKSPACE_SAFETY_PORTAL = 194283417429892` in `shared/sheet_ids.py`, captured by PR #168). The `Safety Portal` folder (`6663869084002180`: `ITS_Active_Jobs`, `ITS_Forms_Catalog`) was **moved there from `ITS — Operations`, IDs preserved**; per-job week sheets and the `WSR_human_review` approval sheet live there too. It is approval-gated (workspace access = approval authority) and deliberately outside the five-workspace audience-separated model — acknowledged in **Op Stds v17** (2026-06-05; §23/§24; see [memory-archive §G23.3](memory-archive.md)).

## Active Projects folder inventory

Folder ID 5819628569028484. 6 project subfolders. Bradley 1 is the source-of-truth template; other 5 clone from it at form-and-clone cascade time.

| **Project** | **Folder ID** | **Population state** |
| --- | --- | --- |
| Bradley 1 | 8025248894347140 | Fully populated (~509 rows across 12 sheets) |
| Bradley 2 | 5210499127240580 | 12-sheet structure, empty (re-clones at form cascade) |
| Brimfield 1 | 7462298940925828 | 12-sheet structure, empty |
| Brimfield 2 | 7180823964215172 | 12-sheet structure, empty |
| Huntley | 8306723871057796 | 12-sheet structure, empty |
| Rockford | 6828980243326852 | 12-sheet structure, empty |

## Outreach Logs merged into Buyout — Subs

During the 2026-05-20 evening session an Outreach Log sheet was created on the template and cloned to all 6 projects (in a new 04 — Outreach Logs folder). After review, the outreach lifecycle was found to substantially overlap with the existing Buyout — Subs schema (RFP Status + Award Decision already covered the outreach-to-award arc).

**Decision: **collapse Outreach Log functionality into Buyout — Subs. The 6 cloned Outreach Log sheets, their 6 project subfolders, and the parent 04 — Outreach Logs folder were deleted on 2026-05-20. Buyout — Subs absorbed the missing capability via schema enhancements (below).

## Buyout — Subs schema enhancements (Bradley 1 template + future clones)

**Bradley 1 Buyout — Subs sheet ID: **8615508038340484

Four columns added to capture outreach lifecycle (previously the Outreach Log's role):

- Date Contacted — DATE column, ID 2813666222444420

- Contact Method — PICKLIST column, ID 7317265849814916. Options: Email / Phone / In-person / SMS / Mail.

- Outreach By — CONTACT_LIST column, ID 1687766315601796

- Follow-up Date — DATE column, ID 6191365942972292

Two existing columns modified:

- RFP Status renamed to Status (column ID unchanged: 4071861372882820). Picklist extended from 6 to 9 values to cover full lifecycle:

- Not Contacted / Contacted / Interested / Won't Bid / RFP Sent / Bid Received / Bid Declined / No Response / Awarded

- Scope picklist extended (ID 2945961466040196) to include Fence — a real category from source Sub Tracker data. Full list: Civil / Electrical / Mechanical / Tree Clearing / Erosion Control / Entrance Install / Concrete / Trucking / Pile Driving / Module Install / Fence / Other.

## ITS_Review_Queue schema enhancements (PR #44)

**Sheet ID: **7243317526876036

7 columns added during PR #44 (landed prior to this session):

- Source Sheet ID (TEXT_NUMBER, 3742953549107076)

- Source Row ID (TEXT_NUMBER, 8246553176477572)

- Source Row Permalink (TEXT_NUMBER, 928203782000516)

- Sender (TEXT_NUMBER, 5431803409371012)

- Escalation Level (PICKLIST, 3180003595685764). Options: L1-Teala / L2-Sam / L3-Jacob / Escalated-External.

- Created By (system column, 7683603223056260)

- Modified By (system column, 2054103688843140)

## Bradley 1 demo seeding summary

Total ~509 rows across all 12 sheets. Sheet-by-sheet:

| **Sheet** | **Sheet ID** | **Rows** | **Source** |
| --- | --- | --- | --- |
| Schedule | (prior migration) | 53 | Real (Bradley 1 source) |
| Closeout K-1 | (prior migration) | 92 | Real (Bradley 1 source) |
| Financial Ledger | (prior migration) | 292 | Real (Bradley 1 source, 38 vendors) |
| Buyout — Subs | 8615508038340484 | 12 | Migrated from Sub Tracker (Bradley Bourbonnais 1 rows) |
| Buyout — Materials | 6432642449756036 | 10 | Demo (mixed lifecycle stages) |
| Buyout — Equipment | 7803114974302084 | 7 | Demo (long-lead equipment workflow) |
| Change Orders / PCO Log | 2003251267325828 | 6 | Demo (PCO-001 through PCO-006) |
| Punchlist | 1759030836940676 | 10 | Demo (Civil/Mechanical/Electrical/Cosmetic/Safety/Documentation mix) |
| Permits & Inspections Log | 2495145281802116 | 7 | Demo (Kankakee County / ComEd / IL EPA) |
| Submittal Log | 4990083194113924 | 8 | Demo (SUB-001 through SUB-008) |
| RFI Log | 8084383792582532 | 6 | Demo (RFI-001 through RFI-006) |
| Drawing Revisions Index | 3025736951615364 | 6 | Demo (C-001/C-002/E-001/E-005/S-001/M-001) |

### Cross-reference storytelling (intentional for demo)

Demo data is wired together to demonstrate how ITS threads data across workflow sheets:

- **Bedrock issue thread: **RFI-001 (Bradleys Solar to Engineer, Feb 8) → PCO-001 ($48.5k, converted to CO Mar 5) → drawing revision C-001 Rev 3 (Apr 30) → Schedule milestone slip.

- **Trench depth thread: **RFI-002 (Casey Solar to Engineer, Apr 18) → PCO-004 ($32.4k, approved May 10) → drawing E-005 Rev 2 (May 8).

- **Casey Solar conduit thread: **RFI-005 (Casey Solar, May 12) → SUB-007 rejected & resubmit (May 8).

- **Erosion control thread: **PCO-006 draft (rain event in March) → C-002 Rev 2 (May 12 erosion control plan update).

- **Fence thread: **RFI-004 (Fortress Fencing, May 2) → Punchlist item 3 (NE perimeter erosion).

## Source-of-truth note for production deployment

**Important: **the demo workspace data will NOT be migrated to Evergreen's production tenant. Production deployment will create a fresh Smartsheet workspace at Evergreen's tenant and migrate ONLY their real data. Bradley 1's demo seeding (everything except Schedule/FL/Closeout K-1, which are real) is demo-only.

## shared/sheet_ids.py constants delta

The following constants need to be added to shared/sheet_ids.py. PR #46 (picklist sync) already added SHEET_PICKLIST_SYNC_CONFIG plus Vendor/Sub/Equipment master DB sheet IDs. The remaining delta is workspace and folder IDs.

**New constants to add:**

# Workspaces (added 2026-05-20)

WORKSPACE_OPERATIONS = 7217130472007556

WORKSPACE_ARCHIVE = 5528280611743620

# Portfolio sub-folders

FOLDER_ACTIVE_PROJECTS = 5819628569028484

FOLDER_PORTFOLIO_ROLLUPS = 8071428382713732

FOLDER_FIELD_REPORTS = 705799988242308

# Operations + Archive sub-folders

FOLDER_OPERATIONS_MASTER_DBS = 471604011526020

FOLDER_ARCHIVE_CLOSED_PROJECTS = 1034553964947332

# Active project folders

FOLDER_PROJECT_BRADLEY_1 = 8025248894347140

FOLDER_PROJECT_BRADLEY_2 = 5210499127240580

FOLDER_PROJECT_BRIMFIELD_1 = 7462298940925828

FOLDER_PROJECT_BRIMFIELD_2 = 7180823964215172

FOLDER_PROJECT_HUNTLEY = 8306723871057796

FOLDER_PROJECT_ROCKFORD = 6828980243326852

**Constants to remove: **none. The Outreach-related constants were never added to sheet_ids.py (sheets and folder were created and deleted within the same session).

**CC follow-on PR brief: **a focused brief covering this delta will accompany the next session start. Estimated ~20 lines of additions, no test changes required (constants are inert).

## Pending items for next session

- Form build (deferred per ship-and-leave: build all forms on Bradley 1 templates at final pre-deployment, then clone cascade with include=[forms,filters,rules] to other 5 projects).

- Conditional Formatting rules, Filter Views — UI-only per Smartsheet API constraint (Op Stds v9.2 §6).

- Portfolio Rollups folder (8071428382713732) — empty, needs structural reports (Cross-Project Schedule, Financial, Punchlist) plus optional dashboard.

- Picklist Sync Automation post-merge verification (PR #46 landed; smoke test was mid-flight at session close; outcome verification pending).

- Mirror tenant data alignment — Picklist_Sync_Config sheet exists; mappings ship disabled per PR #46 design.