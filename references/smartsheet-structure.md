---
type: reference
version: 1
status: canonical
workstream: safety_portal
last_verified: 2026-06-08
last_verified_against: 21bd909
tags: [smartsheet, safety_portal, workspace-structure, standalone-workspace, workspace-membership-approval, find-or-create, box-mirror]
---

# ITS — Safety Portal Smartsheet Structure v1

**Scope.** This reference documents the **`ITS –– Safety Portal`** Smartsheet workspace — the live operational surface of the Safety Portal pipeline (the standalone, approval-gated workspace introduced 2026-06-05). It is **structure-only** (workspace → folders → sheets, roles, provisioning rules). The other Smartsheet workspaces — `ITS — System`, `ITS — Human Review`, and the customer-portfolio / template workspaces (`Forefront Portfolio — ITS Demo`, the `Evergreen Portfolio Template` master + seed) — are **out of scope here** and covered by [`smartsheet-handoff.md`](smartsheet-handoff.md); none of them is retired by this doc.

**No numeric IDs here (by convention).** Per repo [`CLAUDE.md`](../CLAUDE.md) ("don't put Customer-0-specific operational data here — specific Smartsheet sheet IDs … belong in the `its` repo"), this doc names every object by its **`shared/sheet_ids.py` constant** and its **live Smartsheet name**. The authoritative numeric IDs live in `~/its/shared/sheet_ids.py` (the single source of truth; tests monkeypatch it). Verified live against the workspace on 2026-06-08 (exec `21bd909`).

## 1. The workspace

| Constant | Live name | Role |
|---|---|---|
| `WORKSPACE_SAFETY_PORTAL` | `ITS –– Safety Portal` | Standalone Safety Portal pipeline workspace. **Workspace membership = approval authority** — sharing this workspace with a person is what grants them F22 approve/send authority (the `authorized_approvers` ITS_Config allowlist was retired; see [safety-portal mission §8](../workstreams/safety-portal/mission.md)). Deliberately **outside** the five-workspace audience-separation model (Op Stds §23/§24 acknowledge it as an additive standalone exception). |

The Safety Portal folder + its three core sheets were **moved here 2026-06-05 from `ITS — Operations` with their IDs preserved** (`sheet_ids.py` amendment b); `FOLDER_OPERATIONS_SAFETY_PORTAL` remains as a back-compat alias of `FOLDER_SAFETY_PORTAL`.

## 2. Folder topology (live, top level)

```
ITS –– Safety Portal  (WORKSPACE_SAFETY_PORTAL)
├── 00_Safety Portal        (FOLDER_SAFETY_PORTAL)   — core registry + review sheets
│   ├── ITS_Active_Jobs                              (SHEET_ACTIVE_JOBS)
│   └── WSR_human_review                             (SHEET_WSR_HUMAN_REVIEW)
├── 00_Form Catalog                                  — form definitions
│   └── ITS_Forms_Catalog                            (SHEET_FORMS_CATALOG)
├── <per-job folders>  (find-or-create, one per Active job)
│   ├── Bradley 1 / Bradley 2 / Brimfield 1 / Brimfield 2 / Huntley / Rockford
│   └── …each holds per-week submission sheets — see §4
└── ZZ Portal Proof    (validation/proof job)
    └── "ZZ Portal Proof — week of 2026-06-06"        (a per-week submission sheet)
```

Note: `ITS_Forms_Catalog` lives in its **own `00_Form Catalog` folder**, *not* inside `00_Safety Portal`. (The `FOLDER_SAFETY_PORTAL` inline comment in `sheet_ids.py` predates the catalog split and still lists all three sheets together — the live structure above supersedes that comment; flagged for an exec `sheet_ids.py` comment refresh.)

The per-job folders (`Bradley 1`, `Bradley 2`, `Brimfield 1`, `Brimfield 2`, `Huntley`, `Rockford`, plus `ZZ Portal Proof`) are **created in this workspace by `find-or-create`** at submission time — they are distinct from the like-named `FOLDER_PROJECT_*` constants in `sheet_ids.py`, which are the customer-portfolio project folders under `WORKSPACE_DEMO` (a separate workspace; see [`smartsheet-handoff.md`](smartsheet-handoff.md)).

## 3. Core sheets (in `00_Safety Portal` / `00_Form Catalog`)

| Constant | Live name | Role |
|---|---|---|
| `SHEET_ACTIVE_JOBS` | `ITS_Active_Jobs` | The job registry (built 2026-06-03). Single source of truth for the portal's active-job set; pushed to the portal D1 via the bearer-gated `POST /api/internal/sync`. Carries the per-job recipient/contact columns used at send time. |
| `SHEET_WSR_HUMAN_REVIEW` | `WSR_human_review` | The customer-facing weekly safety report **review / approve / send gate**. **Supersedes the decommissioned `WPR_Pending_Review`** (which lived in `ITS — Human Review`; decommission-by-doc per the clean-break — see [`system-hr-handoff.md`](system-hr-handoff.md)). F22 approval is verified by workspace membership + cell-history attestation. |
| `SHEET_FORMS_CATALOG` | `ITS_Forms_Catalog` | The parent/variant form-definition catalog driving both the portal's TS display runtime and the Python Option-B PDF renderer. |

## 4. Per-week submission sheets (find-or-create)

Each portal submission is filed to a **per-job → per-week submission sheet**, auto-provisioned at the `WORKSPACE_SAFETY_PORTAL` surface by `find-or-create` (no static `sheet_ids.py` constant — these are runtime objects):

- **Naming:** `"<Job name> — week of <YYYY-MM-DD>"` where the date is the **Saturday** that opens the week (Saturday→Friday week rule; see `safety_reports/safety_week.py`). Example live sheet: `ZZ Portal Proof — week of 2026-06-06`.
- **Provisioning:** `safety_reports/week_sheet.py` finds the per-job folder (or creates it) and finds-or-creates the week sheet within it. Shared naming lives in `safety_reports/safety_naming.py`.
- A week is never auto-closed; late submissions route to the next uncompiled week (multiple packets per week allowed). The weekly compile dual-writes to the week sheet + `WSR_human_review`.

## 5. Cross-workspace dependency

| Constant | Live name | Workspace | Why |
|---|---|---|---|
| `SHEET_CONFIG` | `ITS_Config` | `ITS — System` (`WORKSPACE_SYSTEM`) | The portal pipeline reads operational config (e.g. `safety_reports.box.portal_root_folder_id`, `worker_base_url`, `scheduled_send_local`) from `ITS_Config`. It is **not** in the Safety Portal workspace. See [`system-hr-handoff.md`](system-hr-handoff.md) for the System-workspace map. |

Box is the system-of-record for filed artifacts; the Box mirror tree (`ROOT → per-job → per-week`) parallels this Smartsheet structure and is config-gated on `safety_reports.box.portal_root_folder_id` (see [safety-portal brief §9](../workstreams/safety-portal/brief.md)).

## Authority

ITS — Safety Portal Smartsheet Structure v1, 2026-06-08 canonical. Verified live against the `ITS –– Safety Portal` workspace on 2026-06-08 (exec `21bd909`). Numeric IDs are **not** carried here by repo `CLAUDE.md` convention — they live in `~/its/shared/sheet_ids.py`.

Cross-references:
- [safety-portal mission](../workstreams/safety-portal/mission.md) + [brief](../workstreams/safety-portal/brief.md) — the workstream that owns this pipeline (workspace-as-approval-authority, find-or-create week sheets, Box mirror).
- [safety-reports mission](../workstreams/safety-reports/mission.md) + [brief](../workstreams/safety-reports/brief.md) — the Python pipeline that reads/writes these sheets.
- [`smartsheet-handoff.md`](smartsheet-handoff.md) — the `ITS — System`, `ITS — Human Review`, and customer-portfolio / template workspaces (out of scope here).
- [`system-hr-handoff.md`](system-hr-handoff.md) — `ITS — System` + `ITS — Human Review` detail; `WPR_Pending_Review` decommission.
- [memory-archive §G27](memory-archive.md) — 2026-06-08 mirror activation (the live-validation that exercised this structure).
- `~/its/shared/sheet_ids.py` — the authoritative numeric IDs.
