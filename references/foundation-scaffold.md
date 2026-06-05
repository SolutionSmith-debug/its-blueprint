---
type: reference
version: 6
status: canonical
last_verified: 2026-06-05
last_verified_against: ffad86b
supersedes: references/foundation-scaffold.md@v6.4
workstream: null
tags: [status-snapshot, what-is-done]
---

**ITS Foundation Scaffold Update v6.5**

2026-05-22 — Verified Against Repo HEAD 07dc8e1

*PR window through #60 · 779/3/10 tests verified · Full module inventory including box_migration + smartsheet_migration*

# Purpose

Full scaffold inventory refresh absorbing the post-PR-#51 work plus first-time coverage of the box_migration/ and smartsheet_migration/ surfaces that prior FSU versions did not enumerate. v6.4 stops at PR #51 in its window log; v6.5 closes the gap through PR #60 and reconciles test/source counts against verified repo state.

Predecessor verification: ITS_Cascade_Verification_Audit_2026-05-21.docx (forensic pass against HEAD 07dc8e1 conducted 2026-05-21 evening + verified again 2026-05-22 afternoon). Every line-count, test-count, file-existence, and PR-merge claim in this doc has been verified against the live repository.

# What Changed in v6.5

- PR window extends from #51 to #60. PRs #52-#60 absorbed.

- Test count refreshed: 655 → 779 passed / 3 skipped / 10 deselected (+ 124 net since v6.4). Live verification at 2026-05-22 afternoon via pytest -q.

- mypy source file count refreshed: 91 → 93. Zero errors enforced.

- ruff clean throughout the window.

- New scaffold modules: safety_reports/intake.py (refactored to extract process_message in PR #59), safety_reports/intake_poll.py (new polling daemon PR #59), safety_reports/week_folder.py (per-project per-week folder helper PR #54), scripts/launchd/org.solutionsmith.its.safety-intake.plist + install/uninstall scripts + seed_safety_intake_polling_config migration.

- New shared/* additions verified at sheet_ids.py: FOLDER_SYSTEM_DAEMONS, SHEET_DAEMON_HEALTH, DAEMON_HEALTH_COLUMNS dict with 12 column IDs. shared/smartsheet_client.py find_row_by_primary + update_row_cells_by_id helpers (PR #60).

- New System workspace artifact: folder 04 — Daemons (2130046845511556) + ITS_Daemon_Health sheet (4529351700729732).

- First-time module-level documentation of box_migration/ (4 modules) and smartsheet_migration/ (10 modules). These surfaces existed since 2026-05-17 and were tracked in tech_debt.md + session logs but never enumerated in canonical scaffold docs.

- Bradley 1 sandbox demo-complete: 43-row DFR backfill, ~552 total Bradley 1 rows, 5 storytelling threads + 1 new.

- Box 1111A clone cascade complete (PR #56): 6 project folders under ITS DATA.

# Live Execution-Layer State (Verified)

## Repo State

| **Metric** | **Value** |
| --- | --- |
| Repo URL | github.com/SolutionSmith-debug/its (PUBLIC) |
| Branch | main |
| HEAD commit | 07dc8e1 |
| HEAD subject | docs(session_log): 2026-05-21 safety intake heartbeat row |
| HEAD timestamp | 2026-05-21 15:17:35 -0400 |
| Last merged PR | #60 (heartbeat integration, 7397b07, 2026-05-21T19:16:26Z) |
| Window covered by v6.5 | PR #52 through PR #60 |
| pytest (verified live) | 779 passed / 3 skipped / 10 deselected / 782 collected |
| mypy (verified live) | 0 errors / 93 source files |
| ruff (verified live) | All checks passed |

## Module Inventory — shared/ (19 modules, all verified)

| **Module** | **Lines** | **Status** |
| --- | --- | --- |
| shared/__init__.py | 1 | Empty package marker |
| shared/alert_dedupe.py | 404 | Resend-leg dedupe; (script, error_code) key; 60-min window; fail-open. PR #42 (α) + PR #44 (β). |
| shared/anomaly_logger.py | 95 | Invariant 2 — sentinel pattern checks. Live, tested. SUSPICIOUS_FIELD_PATTERNS FP risk tracked in tech_debt. |
| shared/anthropic_client.py | 64 | Reads ITS_ANTHROPIC_KEY from Keychain; first production consumer is safety_reports.intake (live PR #57). |
| shared/box_client.py | 371 | boxsdk OAuth2 User Auth (PR #39); _store_tokens Keychain callback critical for refresh-token rotation. |
| shared/defaults.py | 75 | DEFAULT_REVIEWER_CHAINS, ALERTING_DEDUPE_WINDOW_MINUTES, PICKLIST_SIZE_*, BOX_PROJECT_FOLDERS (PR #56). |
| shared/error_log.py | 395 | @its_error_log decorator; triple-fire CRITICAL (Smartsheet + Resend + Sentry); Correlation_ID threading; recursion-guarded. |
| shared/graph_client.py | 349 | MSAL client-credentials + Mail API: list_inbox, get_message, list_attachments, download_attachment, mark_read, move_message, send_mail. |
| shared/keychain.py | 99 | macOS-only security CLI wrapper. get_secret(name). |
| shared/kill_switch.py | 93 | Reads system.state from ITS_Config; fail-open ACTIVE on three modes with distinguishable WARN. |
| shared/picklist_sync.py | 574 | Cross-sheet PICKLIST option sync from master DBs; reference-checked removals; two-stage size guardrails; SHA-256 idempotency. |
| shared/quarantine.py | 114 | is_allowlisted + log_quarantined_message; writes to ITS_Quarantine; workstream picklist catch-all is 'other' (NOT 'global'). |
| shared/resend_client.py | 178 | Transactional email for operator alerts via ITS_RESEND_API_KEY; NOT for customer email. |
| shared/review_queue.py | 275 | add() returns row ID; get_status() reads by Item ID. Item ID format <workstream>-<YYYYMMDD>-<HHMMSS>. |
| shared/scheduling.py | 342 | Holiday shifts + reviewer chain + PTO fetcher; _live_fetcher reads ITS_Time_Off with per-instance caching (PR #35). |
| shared/sentry_client.py | 140 | Sentry SDK wrapper for CRITICAL structured capture; traces_sample_rate=0.0; send_default_pii=False. |
| shared/sheet_ids.py | 144 | Workspace/folder/sheet IDs incl. FOLDER_SYSTEM_DAEMONS (PR #60), SHEET_DAEMON_HEALTH (PR #60), DAEMON_HEALTH_COLUMNS dict. |
| shared/smartsheet_client.py | 744 | SDK wrapper with title-keyed reads/writes, typed exception hierarchy; find_row_by_primary + update_row_cells_by_id added PR #60. |
| shared/untrusted_content.py | 58 | Invariant 2 — XML tagging + system boilerplate. wrap() + system_boilerplate(). |

## Module Inventory — safety_reports/ (6 files, fully verified)

| **Module** | **Lines** | **Status** |
| --- | --- | --- |
| safety_reports/__init__.py | 1 | Package marker. |
| safety_reports/intake.py | 1083 | FULLY BUILT — 12-stage pipeline. process_message(message_id) extracted in PR #59. SmartsheetError/GraphError soft-fail. Live-validated end-to-end PR #57. |
| safety_reports/intake_poll.py | 632 | FULLY BUILT — polling daemon. fcntl lock, ITS_Config gate, seen-set idempotency, heartbeat write, mark_read on success. 242+ confirmed cycles in production. |
| safety_reports/week_folder.py | 168 | Per-project per-week Field Reports folder + Daily Reports + Weekly Rollup scaffolding. Idempotent. PR #54. |
| safety_reports/weekly_summary.py | 26 | STUB — pre-cascade reference; awaits two-process refactor to weekly_generate + weekly_send. Raises NotImplementedError on call. |
| safety_reports/README.md | — | Operator runbook: daemon install + uninstall + troubleshooting + operator-visibility section pointing at ITS_Daemon_Health. |
| safety_reports/weekly_generate.py | — | PLANNED — R3 Session 2 target (next critical-path item). |
| safety_reports/weekly_send.py | — | PLANNED — R3 Session 3 target. |

## Module Inventory — box_migration/ (FIRST-TIME ENUMERATED)

Box folder-listing parsing toolkit. Three iterative parser versions (v3 is current) plus reconcile harness. Tech_debt.md has ~10 entries referencing this surface; previously invisible in FSU.

| **Module** | **Purpose** |
| --- | --- |
| box_migration/parse_job.py | v1 — Box folder-name parser. Historical; superseded by v3. |
| box_migration/parse_job_v2.py | v2 — superseded by v3. |
| box_migration/parse_job_v3.py | v3 — current. Multiple regex parsers: parse_vendor_sub (V/S enum, PR shipped 2026-05-19), parse_date_prefix (ISO + R/S directions), detect_chaos (person_tag + lowercase r./s. flags). PERSON_TAG_IN_SUBJECT refined 2026-05-20 (alt-3 removed, FP cleanup). |
| box_migration/reconcile_box_listings.py | Reconcile harness — runs all parsers against live Box folder listings; produces claimed-vs-unclaimed reports for operator review. |

ruff per-file-ignores apply: [I001, F401, UP042, UP045]. Preservation-over-refactor §14 in effect; only real dead code may be removed (per PR #4 + #8 carve-out pattern).

## Module Inventory — smartsheet_migration/ (FIRST-TIME ENUMERATED)

Smartsheet data migration toolkit. ss_api.py is the canonical Smartsheet REST escape hatch referenced in Op Stds v11 §36 (or wherever the in-repo tech_debt section lands). Previously invisible in FSU; surfaced 2026-05-21 verification audit.

| **Module** | **Purpose** |
| --- | --- |
| smartsheet_migration/build_human_review.py | Initial Human Review workspace + sheet provisioning. |
| smartsheet_migration/classify_closeout.py | Closeout document classification helper. |
| smartsheet_migration/inspect_closeout.py | Closeout schema inspection. |
| smartsheet_migration/inspect_source_schedule.py | Schedule source schema inspection. |
| smartsheet_migration/migrate_closeout.py | Closeout data migration to ITS sheets. |
| smartsheet_migration/migrate_fl.py | Florida-related portfolio/job records migration. |
| smartsheet_migration/migrate_schedule.py | Schedule data migration (production runner). |
| smartsheet_migration/migrate_schedule_dryrun.py | Schedule migration dry-run mode (safe inspection). |
| smartsheet_migration/seed_ops_dbs.py | Operations workspace master DBs seed. |
| smartsheet_migration/ss_api.py | Smartsheet REST API wrapper — used when MCP/SDK lack a primitive (sheet-move, native-order reads). Canonical REST escape hatch. |

ruff per-file-ignores apply: [E401, I001, F401, B007, UP035]. Import-time side effects already remediated for three scripts (PR shipped 2026-05-19); test_migration_import_hygiene.py locks the regression.

## Module Inventory — scripts/ (all verified)

Top-level scheduled scripts + smoke tests + setup utilities. 20+ files.

| **File** | **Purpose** |
| --- | --- |
| scripts/watchdog.py | Daily 7AM ET launchd; Checks A/B/C/D/F/G live; Check E deferred to Phase 1.5. |
| scripts/run_picklist_sync.py | Hourly launchd; picklist sync entry point. --dry, --mapping, --smoke-test CLI. |
| scripts/seed_its_config.py | Initial ITS_Config 7-row seed (PR #9). |
| scripts/setup_box_oauth.py | One-time interactive Box OAuth setup (PR #39). |
| scripts/install_safety_intake_daemon.sh | Idempotent safety-intake launchd install (PR #59). |
| scripts/uninstall_safety_intake_daemon.sh | Reverse of install. |
| scripts/smoke_test_*.py (13 files) | Per-module live smoke harnesses: alert_dedupe, box, error_log, graph, kill_switch, quarantine, resend, review_queue, scheduling, sentry, smartsheet, watchdog, watchdog_summary. |

## Module Inventory — scripts/launchd/ (all verified)

| **File** | **Purpose** |
| --- | --- |
| scripts/launchd/template.plist | Boilerplate launchd plist template. |
| scripts/launchd/install.sh | Template-based install pattern. |
| scripts/launchd/org.solutionsmith.its.watchdog.plist | Daily watchdog plist. Pre-dates PR #59. |
| scripts/launchd/org.solutionsmith.its.picklist-sync.plist | Hourly picklist-sync plist. Pre-dates PR #59. |
| scripts/launchd/org.solutionsmith.its.safety-intake.plist | 60s safety-intake polling-daemon plist (PR #59). |

Significance: watchdog and picklist-sync plists predate PR #59. The polling-daemon-as-trigger-primitive pattern was emergent before tonight's PR #59; safety-intake joined an existing roster. Op Stds v11 §31 codifies the pattern; does not introduce it.

## Module Inventory — scripts/migrations/ (all verified)

| **File** | **Purpose** |
| --- | --- |
| scripts/migrations/add_correlation_id_column.py | Correlation_ID column add to ITS_Errors (PR #42). |
| scripts/migrations/box_clone_1111a_to_projects.py | Box 1111A clone cascade (PR #56). copy_with_lock_retry pattern. |
| scripts/migrations/create_picklist_sync_config.py | Initial Picklist_Sync_Config sheet provisioning (PR #46). |
| scripts/migrations/seed_safety_intake_config.py | Pre-polling-daemon safety intake config seed. |
| scripts/migrations/seed_safety_intake_polling_config.py | 3 ITS_Config rows for polling daemon (PR #59). |
| scripts/migrations/seed_safety_recipients_config.py | Per-job safety recipient seeding (PR #54-ish). |

## Test Suite Inventory

| **Metric** | **Value** |
| --- | --- |
| Total test files | 31 (in tests/) |
| Tests collected (default invocation) | 782 |
| Tests passed | 779 |
| Tests skipped | 3 |
| Tests deselected by integration marker | 10 |
| Integration tests (run via pytest -m integration) | 10 |
| CI config | .github/workflows/ci.yml — ruff → mypy (blocking) → pytest with coverage |

## Smartsheet Workspace Topology (Verified Against sheet_ids.py)

| **Workspace** | **ID** | **Audience** |
| --- | --- | --- |
| Forefront Portfolio — ITS Demo | 4129485730670468 | Customer-facing |
| ITS — Human Review | 8561891980142468 | Customer-facing (Evergreen reviewer surface) |
| ITS — Operations | 7217130472007556 | Operator-only (master DBs) |
| ITS — Archive | 5528280611743620 | Operator-only (closed projects) |
| ITS — System | 680592632244100 | Operator-only (config/errors/queues/daemons) |
| ITS — Safety Portal | 194283417429892 | Operator-only, **standalone + approval-gated** — Safety Portal folder (`6663869084002180`: ITS_Active_Jobs, ITS_Forms_Catalog), per-job week sheets, `WSR_human_review`. Moved from Operations 2026-06-04/05, IDs preserved. |

**Sixth workspace, added 2026-06-04/05:** `ITS — Safety Portal` is a standalone, self-contained, approval-gated workspace (workspace access = approval authority), deliberately **outside** the five-workspace audience-separated model. **Doctrine — acknowledged in Op Stds v17** (2026-06-05): §23/§24 now name this sixth, standalone, approval-gated workspace (see [memory-archive §G23.3](memory-archive.md)). **Codified by Phase 5 PR 1 (PR #168, `ffad86b`):** `shared/sheet_ids.py` now defines `WORKSPACE_SAFETY_PORTAL = 194283417429892` and `FOLDER_SAFETY_PORTAL` (with `FOLDER_OPERATIONS_SAFETY_PORTAL` kept as a back-compat alias) plus `SHEET_WSR_HUMAN_REVIEW`.

## System Workspace Contents (Verified)

| **Folder** | **Folder ID** | **Sheets** |
| --- | --- | --- |
| 01 — Config | 164788727768964 | ITS_Config (3072320166907780); Picklist_Sync_Config (7486553185013636) |
| 02 — Logs | 5231338308560772 | ITS_Errors (27291433258884 CANONICAL — 4 bootstrap duplicates pending operator delete); ITS_Quarantine (8687740798324612) |
| 03 — Queues | 7201663145535364 | ITS_Review_Queue (7243317526876036); WPR_Pending_Review |
| 04 — Daemons | 2130046845511556 | ITS_Daemon_Health (4529351700729732 CANONICAL — empty duplicate 3717381690969988 pending operator delete) |

# PR Window Log — #52 through #60 (Verified Against git log)

| **PR** | **SHA** | **Substance** |
| --- | --- | --- |
| #52 | 56fac6c | fix(watchdog): V1 — Check G respects MAINTENANCE (defer pattern). 8 new tests covering defer pattern. Op Stds v10.1 closeout. |
| #53 | ece15d5 | chore(docs): post-session doc drift cleanup. CLAUDE.md stub/real table reconcile; README test count refresh; docs cross-refs. |
| #54 | ed46a96 | feat(safety-reports): R3 foundation — week_folder helper + sheet_ids deltas + recipients ITS_Config seed. |
| #55 | e3945c3 | refactor(smartsheet-client): extract _translate_smartsheet_error helper at §14 threshold. |
| #56 | 30bbaa5 | chore(box): complete 1111A clone cascade + fill BOX_PROJECT_FOLDERS. 6 project folders under ITS DATA. |
| #57 | c4c4bc9 | feat(safety-reports): wire intake.py for end-to-end daily report ingestion. 12-stage pipeline live-validated. |
| #58 | 8afb66a | refactor(intake-test): assert either-path routing + add review-queue cleanup. |
| #59 | f1e724f | feat(safety-reports): polling-daemon trigger replacing Mail.app rule. intake_poll.py + plist + install/uninstall. |
| #60 | 7397b07 | feat(safety-reports): heartbeat row writes to ITS_Daemon_Health. ARCH-1/2/3 refinements. find_row_by_primary + update_row_cells_by_id. |

# Authority

Foundation Scaffold Update v6.5, 2026-05-22. Full inventory refresh covering PR window #52-#60 plus first-time enumeration of box_migration/ and smartsheet_migration/ surfaces. Supersedes v6.4 (2026-05-21 morning) as both canonical baseline and operative reference. Predecessor: ITS_Cascade_Verification_Audit_2026-05-21.docx.

v6.6 trigger: next significant PR window close or repo structural change (new top-level package, dependency major bump, major refactor).

Cross-references: this is a companion-bump within the 2026-05-22 Security Hardening cascade alongside Op Stds v11, FM v8, V&R v7.2, Handover v6.3, Excellence Roadmap v2.3, Memory Archive v5, Cascade Unification Update 2026-05-22.