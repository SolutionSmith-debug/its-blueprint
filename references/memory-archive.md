---
type: reference
version: 5
status: canonical
last_verified: 2026-06-07
last_verified_against: f3ad814
supersedes: references/memory-archive.md@v4
workstream: null
tags: [restoration, operational-detail, post-compaction-recovery]
---

# ITS Memory Archive

**Append-only operational-detail archive.** Loaded on demand, not by default.
Consulted when restoring context after memory compaction or when a specific
operational detail (a sheet ID, a wiring history, a class-of-bug doctrine)
is needed verbatim.

This is the v4+v5 merge: v4 covered §A–§G4 + §H (Picklist Sync); v5 added
§G5 (PRs #59/#60 polling daemon + heartbeat surface + 2026-05-22 cascade).
Both prior docs retired into this single file 2026-05-24 during the
markdown migration. From this point forward the archive grows by appending
new sections (§G6, §G7, …) in-place; no more vN+1 doc spawning.

## **What v4 changes from v3**

v4 supersedes v3 as the operative archive reference. v3 is retained in project knowledge as the historical baseline; v3 itself preserves v2 verbatim, which preserves v1 verbatim. The lossless restoration chain is intact.

**Three changes only in v4:**

- Section H NEW. Captures 2026-05-20/21 Picklist Sync Ship: PR #46 smoke outcome, PR #47/#48/#49 SDK body-shape hotfix sequence, PR #50 hardening pass (integration tests + @require_active + launchd cadence), PR #51 REST swap (closes SDK same-session-cache bug), Op Stds v10 §30 SDK-vs-Live Integration Test Discipline doctrine.

- G5 in-place update. PR #46 smoke-test "TBD at session close" annotation closes: 4-phase smoke passed live against sandbox; PRs #47/#48/#49 + #50 + #51 land downstream as Section H.

- Active memory table refreshed to 16 entries (entry #16 = SDK-vs-Live Integration Test Discipline). Memory entry #10 v2→v4 pointer updated to point at this doc. Memory entry #9 cascade list refreshed with v10 + v6.4 + Picklist Sync Ship cascade.

All other content (Sections A through G1-G4, plus introductory framing about restoration protocol) carries forward verbatim from v3. v3 still in project knowledge for byte-for-byte content of archived sections.

## **Active memory after this consolidation**

For reference, the sixteen entries that remain in active memory after the 2026-05-21 Picklist Sync Ship consolidation:

| **#** | **Entry** | **Why it stays** |
| --- | --- | --- |
| 1 | Core identity: ITS = Integrated Technical System (renamed from TITS 2026-05-10), white-glove custom dev, Evergreen = Customer 0 (Southern California HQ, Oregon project sites), user owns IP | Frame-setting; every chat needs this |
| 2 | System-wide invariants: External Send Gate + Adversarial Input Handling (Foundation Mission v7) | Non-negotiable architectural rules |
| 3 | Design principle: defensive build + ship-and-leave threshold | Behavioral rule, every code/architecture turn |
| 4 | Preservation-over-refactor convention (Op Stds v10 §14) | Behavioral rule, most code-touching sessions |
| 5 | Verify-before-fix discipline | Behavioral rule, every brief-driven session start |
| 6 | MCP-gap REST-fallback pattern | Operational pattern when MCP lacks a primitive |
| 7 | Ezra Jones email correction (PDF typo) | Specific data trap that gets re-introduced otherwise |
| 8 | IP & ownership resolved — do not raise | Guardrail against unwanted nag behavior |
| 9 | Canonical doc set pointer (FM v7+v7.1, V&R v7+v7.1, Op Stds v10 [consolidates v9.x + new §30], Handover Plan v6+v6.1+v6.2, Excellence Roadmap v2.1+v2.2, FSU v6 through v6.4, Handoff v5) | Tells fresh Claude what to read first |
| 10 | This Memory Archive v4 pointer | Tells fresh Claude where operational detail lives |
| 11 | PR-landing verify pattern (gh pr view --json mergedAt,mergeCommit,state) | Behavioral rule, every cc-driven PR session |
| 12 | Managed Agents Phase 3 framing (no Agents until Phase 3 gate; 4 candidates) | Architectural decision affecting all future capability builds |
| 13 | Box auth = OAuth 2.0 User Auth (not JWT); refresh tokens rotate | Specific data trap; wrong auth path is permanent damage |
| 14 | Push-vs-Record Separation doctrine (Op Stds v10 §3.1) | Behavioral rule, every alerting/observability turn |
| 15 | Smartsheet 5-workspace audience-separated topology (Op Stds v10 §23) | Architectural principle affecting every Customer 2+ build |
| 16 | SDK-vs-Live Integration Test Discipline (Op Stds v10 §30) | Behavioral rule, every shared/* SDK wrapper turn |

## **How to use this archive**

Sections are organized by category: infrastructure (A), wiring history (B), major work windows (C), schema and architectural decisions (D), add-ons and roadmap (E), verbatim carry-forward from v1 (F), 2026-05-20/21 session additions (G), 2026-05-21 Picklist Sync Ship (H, new in v4). None of this is loaded by default — consult when needed.

If any archived entry needs to return to active memory, copy the original memory text from the relevant subsection verbatim back into a new memory edit. Original wording is preserved specifically to make restoration lossless.

## **Sections A through F (infrastructure, wiring history, work windows, schema decisions, add-ons, v1 carry-forward)**

Carry forward verbatim from v3. v3 contains the complete text:

- A1 M365 sandbox configuration (Entra app, EXO ServicePrincipal, App Access Policy)

- A2 EXO ServicePrincipal sync gotcha

- A3 Smartsheet three-workspace topology — SUPERSEDED 2026-05-21 by §G1 (5-workspace)

- A4 Smartsheet demo workspace folder structure — SUPERSEDED 2026-05-21 by §G2

- A5 Evergreen mirror tenant roster

- B1 smartsheet_client.py + sheet_ids.py wiring (2026-05-18)

- B2 Triple-fire CRITICAL alert path operational (2026-05-19)

- B3 Phase 1 critical path unblocked (review_queue + quarantine wired)

- C1 Cascade Unification 2026-05-19 master pass

- C2 23-PR window summary

- D1 FL flat structure decision; D2 FL design committed; D3 Box archive schemas; D4 review_queue item ID format; D5 review_queue failure propagation; D6 schema-verify-before-code; D7 preservation-over-refactor honored; D8 CC autonomy calibration

- E1 Add-ons roadmap (pre-Phase-1 free, Customer 2+, eventual, skip)

- F1-F6 v1 verbatim carry-forward (M365 wiring history, smartsheet_client landing detail, triple-fire ship dates, Smartsheet API constraint origins, parse_job_v3 F841 closure)

Cross-reference: read v3 sections A through F verbatim for full content. Restoration to active memory uses the verbatim "Original memory text" block in v3's subsections.

## **Section G — 2026-05-20/21 Session Additions**

G1, G2, G3, G4 carry forward verbatim from v3. G5 receives an in-place update closing the PR #46 smoke-test "TBD" annotation.

### **G1. Smartsheet five-workspace audience-separated topology (supersedes A3)**

Active model. Verbatim text in v3 §G1. Pointer: Op Stds v10 §23 (canonical specification with rationale + multi-customer generalization). 5 workspaces: Forefront Portfolio — ITS Demo (4129485730670468), ITS — Human Review (8561891980142468), ITS — Operations (7217130472007556), ITS — Archive (5528280611743620), ITS — System (680592632244100). Active memory entry #15 carries short form.

### **G2. Portfolio folder restructure (supersedes A4)**

Portfolio workspace now contains only 3 folders: 01 — Active Projects (5819628569028484, 6 project subfolders), 02 — Portfolio Rollups (8071428382713732, empty), 03 — Field Reports (705799988242308). 03-Operations was promoted to ITS — Operations workspace; 04-Archive was promoted to ITS — Archive workspace. Active project folder IDs: Bradley 1 (8025248894347140, template), Bradley 2 (5210499127240580), Brimfield 1 (7462298940925828), Brimfield 2 (7180823964215172), Huntley (8306723871057796), Rockford (6828980243326852). Verbatim text in v3 §G2. Pointer: Smartsheet Handoff v5, shared/sheet_ids.py.

### **G3. Outreach Log → Buyout — Subs merge precedent (2026-05-20 evening)**

In-session: Outreach Log sheet created on Bradley 1 template, cloned to all 6 projects under new 04 — Outreach Logs folder, then merged into Buyout — Subs via schema enhancement (4 new columns: Date Contacted, Contact Method PICKLIST, Outreach By CONTACT_LIST, Follow-up Date; RFP Status renamed to Status, picklist extended 6→9 values; Scope picklist extended to include Fence). Outreach Log sheets, 6 project subfolders, parent folder all deleted in same session. Precedent: when in-session sheet creation reveals overlap with existing surface, merge via schema enhancement rather than carrying parallel structures forward. Verbatim text in v3 §G3.

### **G4. Bradley 1 demo seeding completion (2026-05-20/21)**

Bradley 1 = showcase / template project. All 12 sheets populated, ~509 rows total. Real migrated data: Schedule 53, Closeout K-1 92, Financial Ledger 292. Demo data (plausible + cross-referenced): Buyout — Subs 12 (from Sub Tracker), Buyout — Materials 10, Buyout — Equipment 7, PCO Log 6, Punchlist 10, Permits & Inspections 7, Submittal Log 8, RFI Log 6, Drawing Revisions Index 6. Five cross-reference storytelling threads (bedrock, trench depth, Casey Solar conduit, erosion control, fence). Demo data does NOT migrate to Evergreen production tenant. Other 5 projects empty by design pending form-and-clone cascade. Verbatim text in v3 §G4.

### **G5. PR #45 + #46 (smartsheet_client helpers + picklist sync) landed — STATUS UPDATE in v4**

**v3 left this entry with smoke-test ****"****TBD at session close.****"**** v4 closes the loop:**

- PR #45 (prep, commit 16cf1d7): +4 helpers to shared/smartsheet_client.py + 12 tests. Baseline 595 → 607, mypy 0/76. Closed.

- PR #46 (commit 7a3cdc9, merged 2026-05-21T02:24:19Z): full picklist sync subsystem. shared/picklist_sync.py (410 lines), scripts/run_picklist_sync.py (295 lines), scripts/migrations/create_picklist_sync_config.py (217 lines, ran live), scripts/launchd plist (15-min initial, not installed). +sheet_ids.py 4 IDs, +defaults.py 3 thresholds. 607 → 651 tests, mypy 0/80, ruff clean. Live mutations: Picklist_Sync_Config sheet (7486553185013636) created in FOLDER_SYSTEM_CONFIG; ITS_Config +2 rows (picklist_sync.size_warn_threshold=200, picklist_sync.size_hard_halt_threshold=400). Closed.

- Smoke-test outcome: 4-phase smoke (create 2 sandbox sheets → exercise add + reference-blocked remove + size-warn + size-halt paths → tear down) passed live. PR #46 ship complete.

- Downstream: PRs #47/#48/#49 SDK body-shape hotfix sequence + PR #50 hardening + PR #51 REST swap. See Section H.

## **Section H — 2026-05-21 Picklist Sync Ship + SDK-vs-Live Integration Test Discipline**

New in v4. Captures the post-PR-#46 PR sequence #47 through #51, the SDK-vs-Live class-of-bug doctrine, and the cascade closure into Op Stds v10 + FSU v6.4.

### **H1. PR #47 / #48 / #49 — SDK body-shape hotfix sequence**

*Original memory text (this section is operational detail, not a verbatim active-memory entry — pointer for restoration is the H6 SDK-vs-Live doctrine):*

- PR #47 (commit 3b6632c): drop column.id from body. Live errorCode 1032 ("attribute(s) column.id are not allowed for this operation"). SDK silently accepted the id field; live API rejected. Unit-test regression guard at tests/test_smartsheet_client.py::test_update_column_options_body_excludes_id.

- PR #48 (commit 0b48eab): include column.type in body. Live errorCode 1090 ("Column.type is required when changing options"). Unit-test guard at test_update_column_options_body_includes_type.

- PR #49 (commit ef2973e): unwrap EnumeratedValue → plain str in list_columns_with_options. Live API rejects body where type is wrapped (SDK strips it silently). Defensive str fallback if SDK shape ever changes. Unit-test guard at test_list_columns_with_options_unwraps_picklist_type_mock.

**Canonical location going forward:**

- docs/tech_debt.md "SDK-vs-live body-shape mismatches need integration coverage" entry (OPEN-but-mitigated)

- Op Stds v10 §30 SDK-vs-Live Integration Test Discipline — formal codification

- tests/test_smartsheet_client.py — three regression guards

**Why archive: **Specific PR history. The class-of-bug is what carries forward in active memory (entry #16) and Op Stds v10 §30. PR commit SHAs preserved for audit.

### **H2. PR #50 — picklist-sync hardening (commit 1cf2c7b, merged 2026-05-21T03:05:25Z)**

Post-live-smoke hardening pass. Six items resolved against a cc-driven brief:

- Item 1: alert dedupe integration verified correct (no fix needed)

- Item 2: @require_active decorator added to scripts/run_picklist_sync.py CLI entry point (respects ITS_Config system.state)

- Item 3: TEXT_NUMBER live confirmed for last_run_at (sub-daily cadence resolution preserved)

- Item 4: launchd cadence changed 900s → 3600s (hourly) per operator decision (no real mappings yet; API churn unwarranted)

- Item 5: existing type check at update_column_options catches non-PICKLIST/MULTI_PICKLIST target — no fix needed

- Item 6: Picklist_Sync_Config state-vs-config separation accepted as tech debt (Phase 1.5 doesn't need split; resolves if multi-customer fork edge cases emerge)

- Item 7: 5 integration tests added at tests/test_smartsheet_client_integration.py, gated by @pytest.mark.integration marker; pyproject.toml addopts = -m 'not integration' (CI default skip)

### **H3. PR #51 — find_sheet REST swap + integration-test followups (commit 8ec4c80, merged 2026-05-21T03:17:32Z)**

Integration tests immediately caught a real production bug:

- find_sheet_by_name_in_folder had SDK same-session caching. SDK's Folders.get_folder() caches folder state within a single Client session. A sheet created via create_sheet_in_folder() did NOT appear in a subsequent get_folder() from the same Python process. Direct REST GET /folders/{id} sees the new sheet immediately.

- PR #46's migration script avoided this bug accidentally (no back-to-back create+find in same Python process). Integration test caught it the moment it was written.

- Fix: swap from SDK to direct REST. Unit tests updated to mock requests.get instead of SDK shape. Removes DeprecationWarning AND fixes the same-session-create-then-find bug. Closes tech-debt entry.

- Sandbox-name length fix: integration tests overran Smartsheet's 50-char sheet.name limit (errorCode 1041). _sandbox_name helper renamed to _int_<label>_HHMMSS_µµµµµµ (drops date prefix to save 9 chars + namespace prefix shortened).

- MULTI_PICKLIST round-trip deferred: live API quirk surfaced — creating sheet with MULTI_PICKLIST column returns 200 OK but GET shows type=TEXT_NUMBER. Investigation deferred until real use case emerges (may need Smartsheet support ticket). Defensive code path retained in update_column_options + unit test covers body shape.

### **H4. Final main baseline at end of session**

- ruff: clean

- mypy: 0 errors across 81 source files

- pytest -q (default): 651 passed / 2 skipped / 4 deselected (integration tests excluded by addopts)

- pytest -m integration: 4 passed against live sandbox (PR #50 added 5, PR #51 deferred MULTI_PICKLIST round-trip to docstring-only, net 4)

- PR count since FSU v6 baseline: 28 incremental PRs (#32–#51 plus #34 ghost)

### **H5. SDK-vs-Live Integration Test Discipline doctrine codified**

*Active memory entry #16 (short form):*

ITS SDK-vs-Live Integration Test Discipline (Op Stds v10 §30, codified 2026-05-21 across PRs #47/#48/#49/#51): SimpleNamespace mocks at SDK boundary miss live API enforcement (body shape, required fields, value wrapping) AND SDK runtime state (in-process caching). 4 instances in 2 days. Mitigation: pytest -m integration against throwaway sandbox resources. Any future shared/* SDK wrapper with create/update/delete on typed columns/rows gets parallel integration test. CI skips by default.

**Canonical location going forward:**

- Op Stds v10 §30 — full operational protocol (when to apply, pre-deployment smoke, tech-debt tracking)

- tests/test_smartsheet_client_integration.py — canonical reference implementation (4 tests)

- pyproject.toml — markers + addopts config

- docs/tech_debt.md "SDK-vs-live body-shape mismatches" entry (kept open for visibility — re-introduction guard)

### **H6. Cascade closure: Op Stds v10 + FSU v6.4 + Cascade Unification Update 2026-05-21**

- Op Stds v10: full consolidation. Replaces v9 / v9.1 / v9.2 / v9.3 as both canonical baseline and operative reference. All 30 sections present in full prose. New §30 SDK-vs-Live Integration Test Discipline.

- FSU v6.4: status overlay absorbing PRs #45–#51. Picklist sync subsystem documented; integration test pattern noted; test counts refreshed (595 → 655); PR window log extends through #51.

- Cascade Unification Update 2026-05-21 (Picklist Sync Ship): master record for this cascade event.

- Memory entries updated: #9 (canonical doc set), #10 (v3→v4 pointer), #16 (NEW SDK-vs-Live discipline).

### **Why archive Section H**

Picklist sync subsystem is operational; 4 PRs of post-ship hardening landed cleanly; SDK-vs-Live discipline doctrine is codified. The PR commit SHAs, smoke test outcomes, and tech-debt entries are preserved for audit. Active-memory carries entry #16 (SDK-vs-Live discipline) and entry #9 (cascade list including Picklist Sync Ship). Operational restoration uses Op Stds v10 §30 as the authoritative source.

## **Restoration protocol**

If any archived entry needs to return to active memory, copy the original memory text from the relevant subsection verbatim back into a new memory edit. Original wording is preserved specifically to make restoration lossless. The pointer entry in active memory (#10) provides the path back to this doc; this doc provides the path back to active memory.

Sections A through F: byte-for-byte content in v3 (still in project knowledge). Sections G1-G4: byte-for-byte content in v3. Sections G5 (status update) + H (new): content in this v4 doc.

*End of ITS Memory Archive v4.*
---

# §G5 — 2026-05-21 Evening + 2026-05-22 Cascade (NEW v5)

## §G5.1 — PR #59 (Polling Daemon Trigger)

Shipped 2026-05-21 evening, commit f1e724f. Replaces Mail.app rule trigger for safety_reports with a launchd-driven Graph polling daemon.

### Modules added

- safety_reports/intake_poll.py (632 lines) — polling daemon entry point. Single-cycle execution: poll_once() is public API; __main__ guard calls it once and exits. launchd handles cadence.

- safety_reports/intake.py refactored — extracted process_message(message_id) from prior main(); SmartsheetError/GraphError soft-fail returns rather than raise. Preserves manual-rerun CLI.

- scripts/launchd/org.solutionsmith.its.safety-intake.plist — 60s cadence plist. Reads poll_interval_seconds from ITS_Config at install time via shell substitution.

- scripts/install_safety_intake_daemon.sh + uninstall — idempotent install/uninstall.

- scripts/migrations/seed_safety_intake_polling_config.py — seeds 3 ITS_Config rows: poll_interval_seconds (60), mailbox (safety@evergreenmirror.com), polling_enabled (true).

### Per-cycle behavior

- polling_enabled ITS_Config gate — false short-circuits.

- fcntl file lock at ~/its/state/safety_intake.lock — skip-if-held. Prevents launchd-overlap collisions.

- graph_client.list_inbox with unread_only filter (top=50).

- Per-message: seen-set idempotency guard (prevents double-process if mark_read failed prior cycle), call intake.process_message, mark_read on success.

- Heartbeat write to ITS_Daemon_Health (PR #60 addition; see §G5.2).

### Doctrine codification

PR #59 is the codification of the polling-daemon-as-trigger-primitive pattern. The pattern itself pre-dates this PR: scripts/launchd/org.solutionsmith.its.watchdog.plist (daily) and scripts/launchd/org.solutionsmith.its.picklist-sync.plist (hourly) were both already this shape. PR #59 added safety-intake to the roster and made the doctrine explicit. Op Stds v11 §31 holds the formal codification.

## §G5.2 — PR #60 (Heartbeat Integration)

Shipped 2026-05-21 evening, commit 7397b07. GitHub auto-numbered as PR #60 though it was briefed as PR #59.5; both numbers refer to the same heartbeat-integration work.

### ITS_Daemon_Health surface

- Folder 04 — Daemons (2130046845511556) in ITS — System workspace.

- ITS_Daemon_Health sheet (4529351700729732). 12 columns per DAEMON_HEALTH_COLUMNS dict in shared/sheet_ids.py.

- ITS_Config rows: daemons.heartbeat_sheet_id 3528790636429188; daemons.health_report_id 8032390263799684 (TBD pending operator UI build).

- Empty duplicate sheet 3717381690969988 from parallel chat build — pending operator UI delete (Smartsheet MCP has no delete-sheet primitive).

### Heartbeat write contract

Each daemon writes its row in ITS_Daemon_Health each cycle, in place. Push surface per Op Stds v11 §3.1 (extension to operator visibility). Failure must NEVER block daemon primary work — wrap in try/except, log to ITS_Errors with category 'daemon_health_write_failed', continue.

### ARCH refinements

Three architectural decisions codified in PR #60, captured here for future-reference clarity (see Op Stds v11 §32 for the formal doctrine):

- ARCH-1: Enabled checkbox in ITS_Daemon_Health is report-filter metadata only. Canonical runtime gate is <workstream>.<daemon>.polling_enabled in ITS_Config. Two-switch matrix avoided by design — operators have ONE place to look (ITS_Config) for daemon on/off.

- ARCH-2: Row-id cache persists to ~/its/state/heartbeat_row_ids.json. State file shape: {daemon_name: {row_id, total_cycles}}. First write does find_row_by_primary + persists; subsequent reads from JSON; 404 invalidates and re-resolves. Launchd processes don't share memory — required for per-cycle efficiency.

- ARCH-3: Total Cycles is lifetime monotonic, NOT daily reset. Avoids read-before-write API cost doubling. Operator's report-side aggregation handles per-day/per-week views downstream.

### shared/* additions

- shared/smartsheet_client.py find_row_by_primary(sheet_id, primary_value) — used by heartbeat first-write.

- shared/smartsheet_client.py update_row_cells_by_id(sheet_id, row_id, cells_dict) — used by heartbeat subsequent writes.

- shared/sheet_ids.py FOLDER_SYSTEM_DAEMONS, SHEET_DAEMON_HEALTH, DAEMON_HEALTH_COLUMNS dict (12 column IDs).

### Production verification

Daemon live in production: 60s launchd cadence, 242+ confirmed cycles at 2026-05-21 evening session close. Heartbeat row writing each cycle. ITS_Daemon_Health surface operational; operator can monitor via direct sheet view (formal report TBD pending operator UI build).

## §G5.3 — Verification Audit + 2026-05-22 Cascade

Verification audit conducted 2026-05-21 evening + 2026-05-22 afternoon. Forensic pass against live repo state at HEAD 07dc8e1 (github.com/SolutionSmith-debug/its — now public).

### Drift items surfaced (high-severity)

- CLAUDE.md marked safety_reports/intake.py as 'Stub' — actual is 1083-line fully-built 12-stage pipeline live-validated end-to-end. cc was working with stale view of its own canonical context file.

- CLAUDE.md + README.md cited Foundation Mission v7, Op Stds v9 — operative is FM v7.1, Op Stds v10.1. Stale by two cascade events.

- CLAUDE.md Invariant 2 §1 still referenced Mail.app rule allowlist — would cause cc to design new workstreams against retired trigger primitive.

- CLAUDE.md missing safety_reports/intake_poll.py (632 lines) and safety_reports/week_folder.py (168 lines) from stubs/real table.

- README.md test count claimed 663; actual 779.

- Memory entry 18 claimed 781/1/10 tests; verified actual 779/3/10.

### Project-knowledge gaps surfaced

- box_migration/ — 4 modules (parse_job v1/v2/v3 + reconcile harness). ~10 tech_debt entries reference this surface. Never enumerated in canonical project docs.

- smartsheet_migration/ — 10 modules including ss_api.py (canonical Smartsheet REST escape hatch). Never enumerated.

- docs/tech_debt.md — 39 entries, far richer than planning-project visibility. Op Stds v11 §36 codifies as canonical execution-layer log.

### Cascade event

8-doc cascade landed 2026-05-22 against verified repo state: FSU v6.5, Op Stds v11, FM v8, V&R v7.2, Handover Plan v6.3, Excellence Roadmap v2.3, this Memory Archive v5, Cascade Unification Update 2026-05-22 Security Hardening. Predecessor: ITS_Cascade_Verification_Audit_2026-05-21.docx.

### Pre-Customer-1 security hardening cluster (V&R v7.2 Phase 1.4)

Three deliverables required before Phase 1.5 cutover commences. Captured as memory entry 30. Detailed in Op Stds v11 §§33-35:

- Picklist-hardening across all bounded-enum cells. ~30 min operator UI + ~1 hour audit pass.

- ITS_Trusted_Contacts sheet replacing ITS_Config JSON allowlists. Header-forgery detection (SPF/DKIM/DMARC + Return-Path) via Graph headers. ~half-day session.

- Attachment malware screening 4-layer pipeline (Layers 1-3 for Phase 1.5; Layer 4 VirusTotal deferred to Phase 2+). ~half-day to one-day session.

## §G5.4 — Workflow Refinements

### PR merge verification discipline (reinforced)

PR #34 ghost (closed-not-merged in branch cleanup, claimed landed in memory) remains the canonical failure case. Verification pattern: gh pr merge --squash --delete-branch is ALWAYS followed by gh pr view --json mergedAt,mergeCommit,state. Verify MERGED status + non-null mergedAt + present mergeCommit.oid before considering PR landed. Memory entry 11 holds the rule.

### Operator workflow rule (reinforced 2026-05-22)

Memory entry 25 strengthened after Claude violated the rule with Path A vs Path B framing on whether to continue cascade work. Rule explicitly prohibits: timing pushback, energy-budget commentary, deferred-recommendation framing, choice-architecture not requested by operator. Operator says do X, Claude does X — no preamble, no choice-architecture. Only acceptable commentary: technical tradeoffs about the work itself.

### Forensic verification before cascade (NEW pattern)

2026-05-22 verification audit established the pattern: before any v-bumped cascade doc lands, verify every claim against live repository state. Drift between canonical docs and repo is the rule, not the exception. Operator's verify-before-fix discipline (memory entry 5) extends to cascade authorship: don't write v-bumped authority against memory state; write against verified live state.

# §G6 — Contacts Data Quality (NEW 2026-05-24)

Captures known data-quality issues in operator-provided contact data
that survived migration from memory. Append future contact-data issues
here as discovered.

## §G6.1 — Ezra Jones email typo in Evergreen_Contacts.pdf

The `Evergreen_Contacts.pdf` operator-data artifact (in Claude.ai project
knowledge; not in this repo) contains a typo in Ezra Jones's row only:
`evergreenrenwables.com` (missing the 'e' in 'renewables'). The correct
spelling is `ezraj@evergreenrenewables.com`.

Operationally relevant when:
- Drafting any doc that references Ezra by email
- Wiring ITS_Config rows that include Ezra as a recipient
- Setting up mirror tenant aliases at Phase 1.5 cutover

Other rows in the PDF do NOT have this typo — verified by spot-check
2026-05-21. The typo is isolated to Ezra's row.

Resolution path: when the PDF is next regenerated (operator-side action),
correct the typo at source. Until then, anywhere chat or cc references
Ezra by email, use the corrected spelling.

# §G7 — 2026-05-24 Security-Hardening + CC-Tooling Cluster (NEW 2026-05-24)

Day-record for the 2026-05-24 work cluster. Seven execution-repo PRs (#79–85) plus two server-side configuration passes (branch protection on main; audit-gap closures). Adds doctrine sections §§37–41 to Op Stds (PR 1 in this blueprint repo) and a derived operational checklist (PR 2). This entry captures the day-record per the memory-archive append-only convention.

## §G7.1 — Execution-repo PRs landed

| PR | Topic | Merge SHA | Date | Notes |
|---|---|---|---|---|
| #79 | mattpocock/skills install | 18e90fd | 2026-05-24 | 14 skills at `.agents/skills/` with `.claude/skills/` symlinks |
| #80 | git-guardrails install | e948944 | 2026-05-24 | block-dangerous-git.sh with ITS carve-outs |
| #81 | actions version bumps | 59b440f | 2026-05-24 | checkout v4→v6, setup-python v5→v6 |
| #82 | CLAUDE.md post-merge habit | c6333e7 | 2026-05-24 | docs: add post-merge checkout-main habit |
| #83 | .gitignore *.pem and *.key | 13af7a7 | 2026-05-24 | defense-in-depth, audit gap #5 closure |
| #84 | trusted-contacts PII stripping | be6f8f7 | 2026-05-24 | live-write strips PII; dry-run preserves for review |
| #85 | explicit workflow permissions | 79eec73 | 2026-05-24 | contents: read; closed CodeQL TP |

origin/main HEAD after PR #85: `79eec73`. All four-part verify clean.

## §G7.2 — Server-side configuration (no PR artifacts)

**Branch protection on main:** required_status_checks (strict=true, contexts=["test"], app_id=15368), required_linear_history=true (squash-only), allow_force_pushes=false, allow_deletions=false, required_conversation_resolution=true, enforce_admins=false (emergency lever), required_pull_request_reviews=null (solo+CC, CI is gate).

**Audit-gap closures:**
- Secret scanning + push protection: enabled
- Dependabot alerts: enabled (automated-security-fixes deliberately NOT enabled)
- CodeQL default setup: state=configured, query_suite=default, languages=python+actions, schedule=weekly
- Fork-PR approval policy: tightened from `first_time_contributors` (default) to `all_external_contributors` (strongest)

## §G7.3 — Audit baseline

Comprehensive secret-exposure audit run 2026-05-24 via gitleaks 8.30.1 against full git history (112 commits, all refs). **Zero findings.** Full audit report in `audits/2026-05-24_secret-exposure-audit.md`. Clean baseline by architecture (all secrets in macOS Keychain via `shared/keychain.py` + `.gitignore` + CLAUDE.md doctrine).

## §G7.4 — CodeQL initial-scan FP patterns

Three false-positive patterns surfaced during the 2026-05-24 initial CodeQL scan triage. Documented here for future scan triage:

1. Variable names containing TOKEN/SECRET/KEY logged as names (not values) — e.g., Keychain service-name constants logged in error messages.
2. OAuth 2.0 authorize URLs containing public `client_id` + single-use CSRF `state` token — public by design.
3. Module paths containing `trusted_contacts` triggering py/clear-text-logging-sensitive-data on every print() in the file regardless of content (filename heuristic over-trigger).

Future alerts matching these patterns default to dismiss-as-FP unless content shows actual secret/PII value being logged.

## §G7.5 — Doctrine implications cascaded

Op Stds v11 → v12 (PR 1 in this blueprint repo, landed `74ee6f8`):
- §37 CC Skills Usage Convention
- §38 Local Agent Guardrails
- §39 Per-Customer-Fork Security Setup
- §40 Migration-Script PII Logging Asymmetry
- §41 GitHub Actions Version-Bump Discipline

Derived operational checklist:
- `references/customer-fork-setup-checklist.md` (PR 2 in this blueprint repo, landed `5f80ff8`)

This memory-archive extension (§G7) — captured in PR 3 (this PR).

## §G7.6 — Class-of-bug observations

**Verify-before-fix extends to citations.** The original CLAUDE.md draft for PR #79 referenced `migrate-to-shoehorn` as a "TypeScript-specific, ignore" skill. CC's pre-PR verification surfaced that the skill doesn't exist in `mattpocock/skills` upstream at all — it was cited from search-result snippet without verifying against the actual repo. Codified in Op Stds (verify-before-fix discipline now explicitly covers citations and external-state claims, not just PR-landed claims).

**Push-vs-Record extends to multi-layer defense.** Op Stds §3.1 push-vs-record separation pattern generalizes to defense-in-depth at multiple layers: local hook (operator's machine) + server-side branch protection (everyone, all sources). Each layer protects a different threat surface; neither is redundant.

**Architecture-as-defense is the dominant pattern.** Today's clean audit was not luck. The "all secrets in Keychain" architectural choice means there's no design pathway for secrets to enter the repo. This pattern (make the secure path the obvious path; eliminate design pathways for unsafe outcomes) is more durable than vigilance-based defenses. Worth surfacing when designing future capabilities.

## §G8 — 2026-05-28 Portal-pivot reconciliation + HIGH-2 supersession

The safety-report intake model pivoted from inbox-and-PDF to the form-fill **Safety Portal** (`workstreams/safety-portal/mission.md` v1, 2026-05-25 canonical; `brief.md`). The portal feeds the *same* `safety_reports` intake via an HMAC-verified email shim (`portal-noreply@` → unified `safety@` inbox; the `X-ITS-Portal-HMAC` header is the trust boundary, not the destination address). Signatures are SVG vector path data; PMs cannot attach arbitrary files; mission §7 rules Foundation Mission v8 Invariant 2 **Layer 6 (attachment screening) N/A** for the portal.

**This superseded the 2026-05-28 forensic audit's HIGH-2 for safety reports.** The execution repo's #96 HIGH-2 artifacts were undone: the NOT-WIRED `shared/attachment_screening.py` stub deleted, the `docs/tech_debt.md` HIGH-2 entry flipped to `[SUPERSEDED 2026-05-28]`, the audit-doc finding marked superseded (preserved, not rewritten).

**Layer 6 reassigned to Email Triage** (`workstreams/email-triage/` — mission v4→v5, brief v5→v6), the workstream that actually ingests arbitrary inbound attachments. Wording mirrors FM v8 §34 sub-layers (a)–(d); clamd (Homebrew ClamAV + pyclamd) is the operator prerequisite for sub-layer (c); VirusTotal stays Phase 2+.

**Cross-repo drift guard added** (root cause: the execution repo asserted a model the blueprint had superseded, with no divergence check). `~/its/.claude/agents/session-close-maintainer.md` gained a recurring "Cross-repo supersession check" (both directions: blueprint workstream with no exec acknowledgment; exec asserting a superseded model); `~/its/docs/operations/doc_conventions.md` gained a "Cross-repo supersession drift" note pointing at the existing `last_verified`/`last_verified_against` + audit-snapshot mechanisms. No automated cross-repo check exists by design.

Landed PRs (all four-part PR-landed verify clean): exec #98 `bf2a94a` (undo), #99 `a1fe04b` (exec docs reconcile), #100 `8c09a6b` (drift guard); blueprint #15 `133afb8` (Email Triage Layer 6). Logs: `~/its/docs/session_logs/2026-05-28_portal-pivot-reconciliation.md` (execution) + `session-logs/2026-05-28_portal-pivot-reconciliation.md` (here).

Operational notes for restoration: the portal-marker intake branches (brief §8 Step 4 — Stage 1.5 HMAC gate, Stage 8' JSON parse, Stage 13' rollup) are PLANNED, not built; the legacy PDF-email path is the transition fallback; the legacy ITS_Config `allowed_senders` fallback in `intake.py` must NOT be removed before the trusted-contacts sheet is seeded (would quarantine all real reports). The repo-local `.claude/agents/` were unreachable this session (CC rooted at `/Users/sethsmith`), so this entry + the session logs were authored manually; `claude-code-info-gap.md` §8 snapshot was not refreshed — left for an in-repo `session-close-maintainer` run.

## §G9 — 2026-05-28 Doc-reconciliation: Op Stds v13 drift correction + canonical manifest + reconciliation agent

Parallel session to §G8 (landed second + rebased onto its merges). Three threads:

1. **Doctrine-version drift correction.** Op Stds canonical = **v13** (v12 added §§37-41, v13 added §42 code-level self-documentation); the execution repo trailed at v11. Exec PR #101 (`4b145b8`) bumped all 12 current-doctrine `Op Stds v11` refs in `CLAUDE.md` → v13 (historical refs left), closed the boxsdk `[jwt]` tech-debt entry (fixed by #96, verified `pyproject.toml:18`), §42-retrofitted `shared/untrusted_content.py` (docstring only), and added a §42-compliance inventory — **1/22** `shared/*` compliant, i.e. §42 is effectively un-applied, including the doctrine's own un-landed `state_io.py` example. Blueprint PR #17 (`da6adff`) swept `workstreams/email-triage/` `Op Stds v11`→v13 (mission v5→v6, brief v6→v7; the two `Operational Standards v5` refs left as historical provenance) and refreshed `claude-code-info-gap.md` §8 (the snapshot §G8 noted as unrefreshed) + the stale "5 workstreams" → 6.

2. **Canonical-doctrine manifest** (exec PR #103, `9d6378c`): `~/its/docs/doctrine_manifest.yaml` — machine-readable canonical facts (Op Stds v13, FM v8, §42 headings, the two pinned sheet IDs `SHEET_CONFIG`/`SHEET_DAEMON_HEALTH`, 6 workstream slugs, doc-conventions taxonomy, model strings flagged **verify-required**, never asserted-current). Home = execution-repo-resident + blueprint-derived: CI never checks out the blueprint, so the checker's facts must be self-contained in `~/its`; per-fact `source` + `blueprint_verified_against` point upstream.

3. **doc-reconciliation-auditor agent** (exec PR #106, `feba074`; superseded #105, which GitHub auto-closed when its stacked base #103 merged). Propose-only (opus) — the **heavy half** of the cross-repo drift guard (§G8's `session-close-maintainer` check is the light half; referenced, not duplicated). MECHANICAL tier = `scripts/check_doctrine_drift.py` (deterministic, reads the manifest: version drift / stale tech-debt / §42 coverage / sheet-ID / workstream coverage); SEMANTIC tier = opus judgment. Write-block hook `block-doc-reconciliation-write.sh` (refuses Edit/Write + mutating Bash) + 22-case guard test, mirroring #93's codeql-fp-triager. Registered in `CLAUDE.md` (`## Agents` section + session-close invocation; other 7 agents flagged undocumented-in-CLAUDE.md as a follow-on).

Self-test (run once vs HEAD, at `~/its/docs/audits/2026-05-28_doc-reconciliation.md`): **0 false positives** across 8 adversarially-verified finding-classes. Real drift surfaced beyond this session's scope (operator follow-ons): README.md `Op Stds v11` (3), `.claude/agents/ops-stds-enforcer.md` hardcodes v11/§41 (no §42), blueprint `workstreams/README.md` omits safety-portal. Calibration caught two of the checker's own FPs mid-build (historical `Op Stds v4 … superseded` line; the loose M2 heuristic that flagged the legitimately-deferred Watchdog Check E) — both fixed before merge.

Landed PRs (all four-part verify clean): exec #101 `4b145b8`, #103 `9d6378c`, #106 `feba074`; blueprint #17 `da6adff`. Logs: `~/its/docs/session_logs/2026-05-28_doc-reconciliation.md` + `session-logs/2026-05-28_doc-reconciliation.md` (here).

Restoration notes: repo-local `.claude/agents/` were unreachable (CC rooted at `/Users/sethsmith`) — close-out done manually (lint scripts direct, four-part verify via `gh`, logs + this §G9 by hand), same as §G8. The new `doc-reconciliation-auditor` is itself one of those unreachable-from-here agents; it runs when CC is rooted at `~/its`. Stacked-PR lesson: squash-merging a base PR with `--delete-branch` auto-CLOSES the PR stacked on it (here #105) — rebase the child onto main + open fresh. Concurrency lesson: rapid sequential squash-merges trip `cancel-in-progress` (the LOW-3 config) — the intermediate merge commit's main `ci` is cancelled by the next merge's; re-run the cancelled `ci` on that commit for a clean four-part leg-4 (done for #101 `4b145b8`).

## §G10 — 2026-05-28 `alert_dedupe` → `state_io` migration (Phase 1.4 cluster PR 2)

## §G10.1 — Summary

`shared/alert_dedupe.py`'s five state-file callsites were migrated off the same-FD-flock pattern (`STATE_FILE.open("a+")` + `fcntl.flock` + private `_acquire_lock` / `_load_state(fh)` / `_dump_state(fh)` helpers) onto the `shared/state_io.py` sidecar-lock + atomic-write helpers landed in PR #88 (Phase 1.4 cluster PR 1). This is the second and final PR that closes audit findings F19 + F23 — all three `~/its/state/` consumers (intake_poll, weekly_send_poll, alert_dedupe) are now compliant with the CLAUDE.md "no direct `Path.write_text` under `~/its/state/`" rule.

Landed as PR #104, squash-merge `45be1498afd156e489103228531e69b11de5188e`, mergedAt 2026-05-28T23:58:55Z. Four-part verify clean. Session log: `~/its/docs/session_logs/2026-05-28_alert-dedupe-state-io-migration.md`.

## §G10.2 — Technical decisions that are load-bearing for future work

**Lock-free read for `list_expired_summaries` is correct and intentional.** The function does a single `read_text()` call. `atomic_write_json` writes to a temp inode and does `os.replace(tmp, STATE_FILE)` — a `rename(2)` that atomically repoints the directory entry. The reader's fd is bound to whatever inode `STATE_FILE` pointed to at `open()` time; that inode is never truncated, only unlinked when its reference count drops to zero. So the reader always sees one complete file: the pre-replace version or the post-replace version, never a torn half-write. A lock would only serialize reader against writers; with no torn-read window the lock adds latency against CRITICAL-path writers for zero safety gain. Writers still lock because concurrent read-modify-write cycles can lose an update (lost-update problem, distinct from torn reads). The docstring §42 rationale comment carries this justification in-code.

**`StateLockTimeoutError` catch ordering is load-bearing.** In each R-M-W function, `except state_io.StateLockTimeoutError` comes BEFORE `except Exception`. This ordering matters: `StateLockTimeoutError` subclasses `Exception`; reversing the order would swallow the timeout in the broad handler, losing the §3.1 rationale comment and the precise fail-open semantics documented for callers.

**Marker text preserved byte-identical.** Lock-failure markers read "could not acquire flock on … after retries" — unchanged from the old `_acquire_lock` phrasing. Existing test assertions pin this; any future refactor that changes the marker text must update those tests.

## §G10.3 — Operational context that surfaced this session

**PR-number prediction trap.** PR was briefed and coded-against as "#103". The actual number was #104 because #103 was an unrelated open PR that advanced the counter. Fixed in a follow-up correction commit before the PR merged. Lesson: never embed a predicted PR number into docs/code before `gh pr create` returns the real number.

**Mid-merge main advance.** Between branch-cut and merge authorization, main advanced +5 commits (PR #101 v11→v13 drift fix; #103 doctrine manifest; #106/#107 doc-reconciliation agent + hook). Resolved by merging `origin/main` into the branch. CLAUDE.md conflict resolved by taking main's v13-corrected `error_log` row (main's change) + keeping the migrated `alert_dedupe` + `state_io` rows (branch's changes). Pre-existing uncommitted CLAUDE.md "Agent skills" hunk + untracked `docs/agents/` (separate operator WIP) were preserved untouched throughout using selective staging (`git apply --cached` on a truncated patch).

**Op Stds is now v13.** PR #101 established v13 as canonical this session. v12 added §§37–41; v13 added §42 (code-level self-documentation). `alert_dedupe.py`'s new §42 docstring cites v13 §3.1 + §42. Historical v11 cites in older docs are grandfathered.

**`check_doctrine_drift.py` is warn-only.** The new `scripts/check_doctrine_drift.py` (PR #106) checks `docs/doctrine_manifest.yaml` against running constants; its pytest tests cover the checker mechanics, not a repo-wide version scan. It is NOT a blocking CI step.

## §G10.4 — Final baseline at session close

- pytest -q (post-merge, main): 1090 passed / 16 deselected
- mypy: 0 errors / 134 source files
- ruff: clean
- main-branch CI on merge commit `45be149`: SUCCESS

## §G11 — 2026-05-28 Phase 1.4 hardening sweep: F17 + F04 + docstring drift (PR #113)

### F17: intake_poll watchdog Check C registration

`safety_reports/intake_poll.py` was not tracked by Watchdog Check C (missed-job detection) despite being the highest-criticality ITS daemon. Fix: added `_write_watchdog_marker()` to `intake_poll.py` (mirrors `weekly_send_poll`, fail-soft per Op Stds §3.1 — failure does NOT abort the poll cycle). `WATCHDOG_JOB_SLUG = "safety_intake"`. In `scripts/watchdog.py`, `"safety_intake"` was appended to `TRACKED_JOBS` (a `list[str]`) and a per-job window added as `TRACKED_JOB_WINDOWS["safety_intake"] = timedelta(minutes=5)` (5-minute freshness window = ~5× the 60s launchd cadence; jobs absent from the window map fall back to the 24h default).

**Deliberate divergence from weekly_send_poll:** marker is written ONLY after a completed `_poll_inside_lock` cycle — NOT on the disabled-gate or lock-held skip paths. Rationale (§42 docstring comment in code): marker staleness should signal "the poll loop is not running," not "the loop ran but found nothing to do." If it fired on skip paths, the watchdog would stay green even during a lock-starved or polling-disabled outage. Tests lock this contract.

**Live-confirmed:** before PR #113 merged, the production launchd daemon (`org.solutionsmith.its.safety-intake`, running the `~/its` working tree with uncommitted edits) wrote the real `~/its/.watchdog/safety_intake.last_run` on an actual 60s cycle. This also surfaced the live-daemon-runs-working-tree hazard: uncommitted edits in `~/its` go live in ≤60s.

### F04: shared/keychain.set_secret stdin correctness

The brief's prescribed argv shape for `security add-generic-password` (`[... "-w", "-U"]` + `input=value`) was broken against the live `security` CLI. Two bugs:

1. `-w` swallows the next token (`-U`) as the password literal (not a flag), because `-w` reads stdin ONLY when it is the LAST option.
2. stdin must be `f"{value}\n{value}\n"` — password + retype confirmation. A single newline hangs the process waiting for the second entry.

**Corrected form:** `argv = [... "-U", "-a", account, "-s", service, "-w"]` (flags first, `-w` last); `input = f"{value}\n{value}\n"`. Live create→read→rotate→delete round-trip verified before merge. Classic SDK-vs-Live (Op Stds §30) finding: the brief's description was plausible-looking but wrong against the real CLI.

### Docstring drift

Three locations in `scripts/watchdog.py` contained the prose "TRACKED_JOBS is empty by design" — accurate at original ship (R2 Session 2) but false after the picklist-audit and weekly-send-poll jobs were added. All three removed in PR #113.

### Landed PRs
- PR #113 (merge commit `9ef0a66a19dc2a89e7192d84358a6d91fcca42f9`, 2026-05-28) — four-part verify clean.
- PR #115 (merge commit `539792c493fb5097df309cd9431b33b67a86c7cd`, 2026-05-28) — session log, four-part verify clean.

Session log: `~/its/docs/session_logs/2026-05-28_f17-f04-docstring-sweep.md`.

Final baseline (post-PR #113, main): pytest 1097 passed / 16 deselected, mypy 0 errors / 134 source files, ruff clean, main CI on `9ef0a66`: SUCCESS.

## §G12 — 2026-05-29 FM v9 + Op Stds v14: F07/F13 doctrine reconciliation (PR #23)

### What changed and why

Two doctrine bumps from a single Q8 ruling (`session-logs/2026-05-25_safety-portal-grill.md`), reconciling findings from the 2026-05-25 forensic audit where doctrine over-promised security mechanisms that the code does not enforce.

**F13 — Foundation Mission v8 → v9 (Invariant 2 Layer 5):**
Layer 5 (anomaly logging via `SUSPICIOUS_FIELD_PATTERNS`) was described as a "co-equal defense layer." The forensic audit confirmed that anomaly logging is post-hoc detection — it fires after a suspect value has already been processed, offers no real-time blocking, and cannot prevent a successful injection. Reframed to "post-hoc detection tripwire." The `SUSPICIOUS_FIELD_PATTERNS` reference is preserved; the security posture claim is honest. **Code unchanged** — this was a doctrine-text correction only.

**F07 — Op Stds v13 → v14 (§1 kill switch):**
§1 described the kill switch in language that implied a security boundary (e.g., "system-wide pause"). The forensic audit's Q8 noted that the kill switch is fail-open by documented design — it cannot enforce a guaranteed halt, and the External Send Gate (Invariant 1) is the real security boundary. §1 reframed to "operator-convenience suggested pause, NOT a security boundary." `fail_closed_until` (a true fail-closed window mechanism) was discussed but deferred to tech debt — the fail-open behavior is correct for a solo-operator system.

Both bumps landed together in blueprint PR #23, squash commit `29000f1` on `origin/main`, 2026-05-29. Tags pushed: `foundation-mission-v9`, `operational-standards-v14`. Both docs' `last_verified_against` = exec-repo HEAD `64526a1`. Planning session log: `session-logs/2026-05-29_f07-f13-doctrine-reconciliation.md`. Four-part verify clean.

### Non-obvious gotchas

**(a) The F07 FM edit was a confirmed no-op.**
Before editing `foundation-mission.md` for F07, the file was read end-to-end. FM has zero kill-switch text — the kill switch is solely an Op Stds §1 construct. FM v9 is driven entirely by F13 (Layer 5 reframe); F07 touched Op Stds only. Any future brief or audit that says "FM covers the kill switch" is incorrect.

**(b) Doctrine version bumps require symmetric Authority-block + companion-ref updates in BOTH docs.**
FM's Authority block was edited thoroughly (self-version v8→v9 plus its companion ref to Op Stds updated to v14), but Op Stds's OWN Authority block was forgotten — it still declared the doc "v13", carried a stale "v14 trigger" prediction, and still read "Companion to FM v8", so Op Stds self-contradicted (v14 in frontmatter/title, v13 in Authority). The trap is asymmetry: one doc's Authority block updated, the sibling's left untouched. A four-lens adversarial review of the diff caught it before merge. The pattern:
- Every doctrine doc has an `Authority` section that states its own version.
- Companion docs that cross-reference each other (FM ↔ Op Stds, V&R ↔ FM) must have their version refs updated symmetrically.
- The diff review lens "does the Authority block match the frontmatter `version:`?" catches the self-reference; the lens "do companion-doc cross-refs still resolve?" catches the reciprocal side.
This is not enforced by `lint_frontmatter.py` — it is a manual diff-review obligation.

## §G13 — 2026-05-29 F02+F22: network-capability allowlist + approval-attestation verification (PR #118)

### Summary

Two Phase 1.4 hardening items landed together in exec PR #118 (`a3efca7`, 2026-05-29, four-part verify clean). Session log: `~/its/docs/session_logs/2026-05-29_f02-f22-capability-approval.md`.

**F02 — network-capability allowlist in `tests/test_capability_gating.py`:**
Extended the capability-gating test suite with a network-library allowlist walker. The test walks `shared/` and `safety_reports/` (operational scripts deliberately excluded — see below) and asserts that any module importing network-capable libraries (`socket`, `requests`, `httpx`, `urllib`, `aiohttp`) appears on a 5-entry allowlist (`shared/keychain.py`, `shared/graph_client.py`, `shared/box_client.py`, `shared/smartsheet_client.py`, `shared/resend_client.py`). Uses dotted-segment matching (not substring) to avoid `urllib.parse` false positives from same-name stdlib modules. The walker does NOT include `scripts/` — operational scripts (smoke tests, seed scripts, install helpers) legitimately need network access and are not production daemon code.

**F22 — `shared/approval_verification.py` (NEW module) + per-row approval gate in `weekly_send_poll.py`:**
`verify_approval(row_id, row_data, authorized_approvers)` is a fail-CLOSED total function: returns `(verified: bool, event_data: dict)`. It fetches Smartsheet cell history for the `Approved for Send` column on the given row, walks the history for a `True`-valued event where `modified_by.email` is in the `authorized_approvers` set. **Identity match on email only** (see §G13.1 below). `weekly_send_poll.py` calls `verify_approval` per row before dispatching to `send_one_row`; unverified rows are skipped with a forensic `approval_unverified` WARN event (threaded correlation_id). The ITS_Config row `safety_reports.authorized_approvers` holds a comma-separated email list; `scripts/seed_its_config.py` seeds it. `docs/operations/cutover_checklist.md` (NEW) covers operator prerequisites at Phase 1.5 cutover.

### §G13.1 — Load-bearing technical decisions

**(a) Smartsheet `get_cell_history` `modifiedBy` has name+email only — no stable user ID.**
The Smartsheet REST API's cell-history endpoint returns `modifiedBy` with `name` and `email` fields; there is no unique stable user-ID field exposed in the response. `approval_verification.py` therefore matches on email address, compared against the `authorized_approvers` ITS_Config row. Implications: approver identity is only as reliable as the email claim, if an approver's email changes the ITS_Config row must be updated, and there is no cross-tenant user-object comparison available. Documented as a deliberate limitation in the module's §42 docstring.

**(b) F02 walk-scope decision: `shared/` + `safety_reports/` only; `scripts/` excluded.**
The allowlist check was scoped to production daemon code, not all Python files in the repo. `scripts/` (smoke tests, seed scripts, setup helpers) legitimately use network libraries; including them would require a prohibitively long allowlist that would dilute the signal the test exists to provide. The operator rationale: the External Send Gate and Invariant 2 defenses are daemon-code concerns; operational scripts are operator-run one-shots.

**(c) `approval_verification.py` is fail-CLOSED.**
If `get_cell_history` raises, if the history is empty, or if no authorized-approver match is found, the function returns `verified=False`. This is the opposite of the fail-open pattern used in kill-switch and heartbeat helpers. Rationale: a false negative here (blocking a send that was legitimately approved) is recoverable by operator recheck; a false positive (allowing an unverified send) violates Invariant 1 and is not recoverable.

### §G13.2 — Worktree `gh pr merge --delete-branch` quirk

When the session is rooted in a git worktree (here `~/its-f02-f22` on branch `f02-f22`), `gh pr merge --squash --delete-branch` lands the GitHub-side merge successfully but cannot execute the post-merge local `checkout main` step (main lives in `~/its`, not the worktree). The remote branch `origin/f02-f22` is also NOT auto-deleted. The four-part verify still passes. The git-guardrail hook blocks `git push origin --delete` syntax; the correct cleanup path is `gh api -X DELETE repos/SolutionSmith-debug/its/git/refs/heads/f02-f22`. As of this session close, `origin/f02-f22` is still live — tracked in `docs/tech_debt.md`.

### §G13.3 — Final baseline

- pytest: 1109 passed / 16 deselected
- mypy: 0 errors / 135 source files (new `shared/approval_verification.py` + `tests/test_approval_verification.py` + `tests/test_approval_verification_integration.py`)
- ruff: clean
- main-branch CI on merge commit `a3efca7`: SUCCESS

## §G14 — 2026-06-02 F08+F09: Smartsheet circuit breaker + alerts-per-hour cap (PRs #137+#138)

### Summary

F08 and F09 landed together across two PRs on exec `origin/main` (both four-part-verify clean). Deployed live same session: pulled `~/its` to `699015b`, confirmed CLOSED/healthy on the new `first_opened_at` schema.

**F08 — `shared/circuit_breaker.py`:** Domain-agnostic `guard(open_exc, count, ignore, ...)` decorator. A single global breaker persisted to `~/its/state/circuit_breaker.json` (launchd daemons are fresh-process-per-cycle — the consecutive-failure count and OPEN deadline MUST outlive the process; in-process state would reset on every invocation and never trip). State machine: CLOSED → OPEN → HALF_OPEN (single probe) → CLOSED/OPEN. Lock-free hot path; locked transition-writes. Fail-open everywhere: missing/corrupt JSON → CLOSED; lock timeout → CLOSED; `enabled=False` in ITS_Config → `is_open()` returns False. `bypass()` context manager for control/forensic-plane operations. 16 `smartsheet_client.py` network methods decorated; `SmartsheetCircuitOpenError(SmartsheetError)` subtype so existing `except SmartsheetError` catch blocks handle it unchanged. `_smartsheet_log` (ITS_Errors write in `error_log.py`) wrapped in `bypass()` so error recording survives an open breaker. Daemons (`intake_poll`, `weekly_send_poll`) gained `CIRCUIT_OPEN` heartbeat status. §43 runbook at `docs/runbooks/circuit_breaker.md`. ITS_Config seed rows in `scripts/seed_its_config.py`. §30 integration coverage at `tests/test_circuit_breaker_integration.py` (CI-skipped).

**F09 — alerts-per-hour cap:** `ALERTING_MAX_ALERTS_PER_HOUR=15` (ITS_Config `alerting.max_alerts_per_hour`, fallback `defaults.ALERTING_MAX_ALERTS_PER_HOUR`) added as a second gate inside `error_log._fire_resend_leg`, using a reserved `_alerts_per_hour_window` key in `alert_dedupe.py`. **Fail-CLOSED at the ceiling** — only the Resend PUSH leg is capped. The ITS_Errors RECORD leg and Sentry leg always fire regardless of the cap (Op Stds §3.1 push-vs-record separation). The watchdog Check K (`_check_alert_rate_cap_window`) sweeps expired cap-window state on a schedule so the suppress window resets cleanly.

**PR 2 additions (PR #138):** Added `first_opened_at` (monotonic episode start, PRESERVED across probe-failure re-opens) + `seconds_open()` lock-free reader. Watchdog Check J (`_check_circuit_breaker_prolonged_open`) — inline `_alert_critical` wrapped in `bypass()`, stable error_code `circuit_breaker_prolonged_open`, MAINTENANCE-defer. `resend_client.send_alert` recipient fallback chain: `system.operator_email` (guarded) → `defaults.OPERATOR_EMAIL_FALLBACK` → raise — so the prolonged-open page still delivers when the breaker short-circuits the config read during the very outage it's paging about. Check K (`_check_alert_rate_cap_window`) — cap-window summary sweep (guaranteed delivery of a summary when the cap was hit).

### §G14.1 — Three bugs caught by mandatory live smoke (the lesson)

All unit-test mocks passed for all three bugs. All three were caught only by running the actual daemons against the live sandbox before merge.

1. **`intake_poll` crashed on `polling_enabled` config read when breaker was OPEN.** `_read_str_setting` called `get_rows(SHEET_CONFIG, ...)` which is decorated with `@_breaker_guard`. When the breaker tripped during the smoke, the config read raised `SmartsheetCircuitOpenError`. `intake_poll._poll_inside_lock` didn't catch it → uncaught exception → daemon crash. Fix: added `SmartsheetCircuitOpenError` to the `except (SmartsheetError, SmartsheetCircuitOpenError)` catch in the `polling_enabled` read path, with a fail-open fallback to `DEFAULT_POLLING_ENABLED`.

2. **`weekly_send_poll` wrote bare `ERROR` heartbeat on scan failure instead of `CIRCUIT_OPEN`.** The scan-failure branch deep in `_poll_inside_lock` had a hardcoded `HeartbeatStatus.ERROR` write. In the mocks, the breaker never opened so the branch was never hit. Fix: check `isinstance(exc, SmartsheetCircuitOpenError)` and write `CIRCUIT_OPEN` status.

3. **`circuit_breaker.is_open()` ignored the `enabled` flag.** The `is_open()` method read the persisted state file and returned `True` if it found an OPEN state, without checking whether the circuit breaker was globally enabled. A freshly-seeded sandbox had no `circuit_breaker.enabled` ITS_Config row, so `enabled` resolved False — but `is_open()` still returned True, blocking all Smartsheet calls on the first probe cycle. Fix: `is_open()` checks `_is_enabled()` first; disabled → return False regardless of file state.

**The operational lesson:** new cross-cutting infrastructure (a breaker, a rate cap, a new exception subtype) is almost never fully exercised by existing unit-test mocks — the mocks were written before the cross-cutting module existed. The operator's practice is mandatory manual live smoke on the actual daemons before merge for any new shared infrastructure that changes how existing callsites behave. This is the third multi-instance case of this pattern (also: SDK-vs-Live §30, `security` CLI stdin shape F04). Consider it a class rule, not a per-PR decision.

### §G14.2 — Deploy: clearing the hung intake_poll daemon

The F08/F09 deploy revealed a pre-existing hung `intake_poll` daemon (PID 292, visible in `ps aux | grep intake_poll`). The daemon had been running for ~88 minutes, well past its normal 60s cycle. It was holding the `fcntl` file lock at `~/its/state/safety_intake.lock`, which prevented new launchd-invoked cycles from proceeding (they see the lock and exit, writing no heartbeat). The watchdog's Check C marker-file floor would have caught this on the next watchdog run — the staleness window for `safety_intake` is 5 minutes.

**Clearance procedure used:** `launchctl kickstart -k org.solutionsmith.its.safety-intake` (the `-k` flag kills the existing instance before relaunching). This is the standard operator intervention for a hung daemon — `kickstart -k` is safe here because the daemon is single-shot-per-invocation (stateless beyond the lock file and heartbeat state) and the fcntl lock is automatically released when the process exits. Post-kickstart: fresh cycle completed on the new code within seconds; heartbeat advanced (`17:23 → 18:53:57 | Status OK | Cycles 11056`), breaker CLOSED/healthy, imports clean.

**Why the daemon hung:** the old code (pre-F08) had no timeout on Graph API calls. An indefinite network wait in `graph_client.list_inbox` or similar would hold the lock until the OS reclaimed the process (launchd's `ThrottleInterval` eventually does this, but the window is long). This is tracked in `docs/tech_debt.md` as an open item — `graph_client` needs request timeouts.

### §G14.3 — Final baseline

- PR #135: CLAUDE.md trim (b428d8c), four-part verify clean.
- PR #137: F08+F09 core (fc5d14f), four-part verify clean.
- PR #138: F08+F09 watchdog (699015b), four-part verify clean.
- pytest: not re-run at this session close (the PR-2 CI run is the ground truth).
- Live deployment: intake_poll on new code, CLOSED/healthy, Cycles 11056.

## §G15 — 2026-06-03 Phase 3a/3b/E1 decisions + live side effects + two worktree gotchas (PRs #151–#153)

### Summary

Three feature branches built and CI-green (pending operator merge), with live Smartsheet side effects already applied this session. This was the "finish the 2026-06-02 work" session — all three decisions resolved in the prior session's planning were executed here.

**Phase 3a — Decision D1=ADD (`feat/phase3a-add-dormant-columns`, PR #151):** Two DORMANT picklist columns that `picklist_validation.REGISTRY` declared but the live sheets lacked were added via a new `shared/smartsheet_client.create_picklist_column` helper (additive column-create, §42 docstring, `@_breaker_guard`). An idempotent `scripts/migrations/add_dormant_picklist_columns.py` (preview-default, `--commit`, title+type idempotency) seeded them with the registry options. **Live side effects applied this session:** ITS_Errors·Workstream (column ID `368377473568644`) + ITS_Quarantine·Disposition (column ID `8535753050328964`) created as PICKLIST with all registry options populated. `audit_picklist_drift --no-emit` now runs clean (0 findings). Phase 3a tech_debt entry flipped to RESOLVED inside PR #151.

**E1 project-routing cutover — Decision D3=NOW (`feat/e1-project-routing-cutover`, PR #152):** `shared/sheet_ids.py` line 85 flipped `SHEET_PROJECT_ROUTING = 3500842291253124` (was 0 / pre-cutover sentinel). **Live side effects applied this session:** ITS_Project_Routing sheet built via `build_its_project_routing_sheet.py` + seeded with 6 BOX_PROJECT_FOLDERS rows via `seed_its_project_routing.py`. `get_folder_id` verified reading from the sheet (not the hardcoded dict). The flip+merge deploys the live cutover — `BOX_PROJECT_FOLDERS` remains as the warn-not-crash fallback. A real doc bug was found and fixed: build/seed/project_routing docstrings described order as build→seed→flip, but seed READS `SHEET_PROJECT_ROUTING`, so the correct order is build→**flip**→seed→verify; all three docstrings corrected. A `sheet_unwired` fixture was added to isolate the pre-cutover-fallback unit test so it simulates the unwired state correctly.

**Phase 3b — Decision D2=AUTOMATE (`feat/phase3b-apply-automation`, PR #153):** Added `--apply` (dry-run by default) and `--apply --commit` flags to `scripts/audit_picklist_drift.py`, built on `ensure_picklist_options`. The `--apply` path is additive + option-only: if the column doesn't exist in the live sheet it logs and skips (no crash). Prune is out of scope for v1. A live smoke ran `audit_picklist_drift --apply` (no `--commit`) on the clean registry: 0 missing columns, 0 missing options — confirms the Phase 3a live side effects landed correctly. Phase 3b tech_debt entry flipped to RESOLVED inside PR #153.

### §G15.1 — Decisions resolved (chat-side planning)

These decisions were made in the planning session and are now implemented:

| Decision | Outcome | PR |
|---|---|---|
| D1 — Phase 3a: dormant columns | ADD (create ITS_Errors·Workstream + ITS_Quarantine·Disposition) | #151 |
| D2 — Phase 3b: automation | AUTOMATE (--apply mode in audit_picklist_drift.py) | #153 |
| D3 — E1 cutover timing | NOW (flip SHEET_PROJECT_ROUTING, deploy on merge+pull) | #152 |

### §G15.2 — Two worktree-workflow gotchas (new lessons)

**(a) Worktree review subagent reads wrong tree — "phantom diff" false report.**
When a `code-review` subagent was run over the `~/its-3b` worktree, the synthesizer sub-step re-verified findings by reading files from `~/its` (the main checkout, where the branch changes are not present). It declared the committed diff "phantom" — code that was clearly in the worktree and in `git diff` was reported as absent. The identically-shaped Phase-3a review in `~/its-3a` worked correctly (and caught a real blocker: title-only idempotency in `add_dormant_picklist_columns.py` that would silently skip a wrong-typed column — the guard was extended to check column type as well). The Phase-3b review was unaffected on correctness because the diff was also verified via `git diff HEAD` and unit tests; the phantom report was caught before acting on it.

**Prevention:** when running any review subagent over a worktree, (1) pin ALL file reads to the worktree absolute path in the invocation prompt, (2) explicitly instruct the synthesizer that the committed branch diff (`git show HEAD` or `git diff <base>..HEAD`) is ground truth — it takes precedence over any file-existence re-check. This is an instruction-discipline fix, not a code change.

**(b) Editable-install + PYTHONPATH import resolution confirmed.**
`PYTHONPATH=<worktree>` wins over the `__editable__.its-0.1.0.pth` editable finder. Tests and scripts in a worktree run against worktree code correctly via `PYTHONPATH=<worktree> ~/its/.venv/bin/python -m pytest ...`. This was confirmed across three parallel worktrees (`~/its-3a`, `~/its-e1`, `~/its-3b`). The open question in `docs/operations/worktree_discipline.md` is resolved: PYTHONPATH wins.

### §G15.3 — Operator deploy checklist (post-session)

1. Merge PRs #151, #152, #153 (any order — `git merge-tree` verified clean cross-merge).
2. `git -C ~/its pull` to deploy to the production MacBook tree.
3. Run `pr-landed-verifier` four-part verify on each PR after merge.
4. The `#152` merge + pull is the live E1 cutover — `get_folder_id` will start routing to the ITS_Project_Routing sheet on the next daemon cycle.
5. Load unloaded daemons: `scripts/launchd/install.sh load org.solutionsmith.its.picklist-sync`, `...watchdog`, `...weekly-generate`, `...weekly-send`. Only `safety-intake` + `weekly-send-poll` are currently active on the production MacBook.
6. Clean ~14 stale worktrees (~/its-3a, ~/its-e1, ~/its-3b, plus the 2026-06-02 batch).

### §G15.4 — Final baseline (per-branch, pre-merge)

All three branches: pytest green, mypy 0, ruff clean, branch CI green. Main-branch CI on merge commits: PENDING operator merge.

- `feat/phase3a-add-dormant-columns` (PR #151): pytest passed, mypy 0, ruff clean, branch CI green.
- `feat/e1-project-routing-cutover` (PR #152): pytest passed, mypy 0, ruff clean, branch CI green.
- `feat/phase3b-apply-automation` (PR #153): pytest passed, mypy 0, ruff clean, branch CI green.
- Last verified main baseline: `5d25b47` (exec PR #150 merge commit).

## §G16 — 2026-06-03 Safety Portal config sheets + unifying alignment audit (PRs #155–#156)

### Summary

Two more exec PRs landed this session after the Phase 3a/3b/E1 cluster (§G15), both four-part-verify clean.

**PR #155 — `feat(safety-portal): build ITS_Active_Jobs + ITS_Forms_Catalog config sheets` (merge `141a573`):** Built the two Smartsheet config sheets the Safety Portal reads (its only two Smartsheet inputs). Live side effects applied same session:

- New folder "Safety Portal" in the ITS — Operations workspace (folder id `6663869084002180`). **[Superseded: this folder was later MOVED to the standalone `ITS — Safety Portal` workspace during the 2026-06-04/05 sessions, IDs preserved — see §G21.]**
- **ITS_Active_Jobs** (sheet id `6223950341164932`): 6 rows seeded — `bradley-1`, `bradley-2`, `brimfield-1`, `brimfield-2`, `huntley`, `rockford`. Columns: Project Name (TEXT_NUMBER, primary — display name matching ITS_Project_Routing), Job ID (TEXT_NUMBER, kebab-case stable key), Address (TEXT_NUMBER), Active (PICKLIST: Active/Inactive/Archived), Notes (TEXT_NUMBER), Last Modified (system MODIFIED_DATE), Modified By (system MODIFIED_BY). **Address cells seeded BLANK** — §4 forbids inventing real addresses and no structured live source exists; the office PM fills them before Work Location auto-fill can serve values.
- **ITS_Forms_Catalog** (sheet id `423274885369732`): 4 rows seeded — `jha-v1`, `daily-site-safety-v1`, `equipment-preinspection-v1`, `toolbox-talk-v1` (no `jha-bradley-v1` variant — that's a meeting decision). Columns: Form Name (TEXT_NUMBER, primary), Form Code (TEXT_NUMBER, == code form.ts directory), Active (PICKLIST: Active/Inactive/Archived), Description (TEXT_NUMBER), Display Order (TEXT_NUMBER), Available For Jobs (TEXT_NUMBER, CSV of Job IDs or empty=all), Last Modified (system MODIFIED_DATE), Modified By (system MODIFIED_BY).
- Two new `smartsheet_client` primitives: `find_folder_by_name_in_workspace(workspace_id, name)` + `create_folder_in_workspace(workspace_id, name)` — direct REST (`requests.get`/`requests.post` on `/workspaces/{id}[/folders]`), `@_breaker_guard`, full §42 docstrings (only folder-in-folder existed before).
- §30 live integration test: `tests/test_safety_portal_config_sheets_integration.py` (2 tests, integration-marked / CI-skipped, run live this session — 2 passed; verifies columns, system-column types, Active picklist options, and seeded rows).
- §43 successor-remediation runbook: `docs/runbooks/safety_portal_config_sheets.md`.
- Per-sheet build + seed migrations (`build_its_active_jobs_sheet.py` / `build_its_forms_catalog_sheet.py` / `seed_its_active_jobs.py` / `seed_its_forms_catalog.py`), live-default with a `--dry-run` preview, idempotent (find-or-create folder/sheet; seeds key on Job ID / Form Code).
- Guarded `picklist_validation.REGISTRY` entries added for the `Active` column on BOTH sheets (Active/Inactive/Archived), gated on non-zero sheet IDs (Trusted-Contacts placeholder precedent).

**PR #156 — `docs(audit): unifying forensic alignment & drift audit` (merge `9e4b51b1`):** Propose-only meta-audit at `docs/audits/2026-06-03_unifying-alignment-audit.md` (status: draft). No code changes. Purpose: single consolidated view of doctrine/code alignment for a funder (Ben) presentation. Key findings and corrections:

- Per-axis verdicts A–F; ranked drift register — **NO Critical findings; no surviving High findings** after adversarial verification (earlier audits' High findings either already resolved or reclassified).
- Consolidated open-findings register replacing four prior-audit fragmented lists.
- **Corrections to live claims (CLAUDE.md stale):**
  - Watchdog check count: CLAUDE.md says "6 of 7 checks operational" — actual is **11 operational** (A, B, C, D, F, G, I, J, K, L, M), only E (Anthropic spend) deferred.
  - Subagent/hook sourcing: 9 subagents + 4 hooks are RELATIVE symlinks from `~/its-blueprint/.claude/` into `~/its/.claude/` (single source of truth); they are NOT copies.
  - CI: gitleaks + doctrine-drift checks ARE in CI (landed PRs #142, #143); CLAUDE.md implied they were not.
- **Open findings surfaced (not fixed this session):**
  - **DR-D1 / H1:** Guard hooks fail-open if the `~/its/.claude` symlink to blueprint dangles. Watchdog Check M only detects post-hoc (after a missed cycle). No preventive mechanism.
  - **DR-C2:** Invariant 2 Layer 6 (attachment screening) is entirely unbuilt for legacy PDF-email to `safety@`. Attachments upload to Box unscanned. The Portal pivot makes this N/A for portal-submitted safety reports, but the legacy email path remains open. Email Triage workstream carries this.
  - **DR-E1 / OPEN-1:** `ops-stds-enforcer` agent's system prompt pins "Op Stds v13" — 3 major versions behind v16. It is blind to §43 (successor-remediation documentation), §44 (Tier-2 repair model), and the F07/F13 kill-switch + anomaly-logging reframes. Agent-file update needed.

### §G16.1 — Safety Portal ITS sheet IDs

For a fresh CC session wiring portal logic:

| Sheet / Folder | ID |
|---|---|
| Safety Portal folder (now in standalone `ITS — Safety Portal` workspace; moved from Operations, IDs preserved — see §G21) | `6663869084002180` |
| ITS_Active_Jobs | `6223950341164932` |
| ITS_Forms_Catalog | `423274885369732` |

These are sandbox (evergreenmirror.com) IDs. Live-tenant IDs will differ at Phase 1.5 cutover.

### §G16.2 — Alignment audit key verdicts (for rapid re-orientation)

The audit's per-axis verdicts confirm the architecture is sound. Drift is in lower-authority layers (planning docs, agent prompts, CLAUDE.md table, memory files) lagging the de-1b doctrine cascade. The code/doctrine core is well-aligned. The three open findings (DR-D1, DR-C2, DR-E1) are known, tracked in `docs/tech_debt.md`, and non-blocking for the current build phase.

# Cross-References

- Memory Archive v4 — operational detail through 2026-05-21 morning. v5 extends, does not supersede.

- ITS_Comprehensive_Session_Update_2026-05-21_EOD.docx — canonical record for PRs #59 + #60.

- ITS_Daemon_Health_Schema_2026-05-21.docx — canonical schema + heartbeat contract.

- ITS_Cascade_Verification_Audit_2026-05-21.docx — forensic verification predecessor for 2026-05-22 cascade.

- ITS_Security_Hardening_and_Doc_Drift_Audit_2026-05-21.docx — earlier security-decision capture; doc-drift findings superseded by Verification Audit's verified-from-repo claims.

# Authority

Memory Archive v5, 2026-05-22. Append-only extension of v4. §A-§G4 carry forward verbatim from v4; §G5 (2026-05-21 evening + 2026-05-22 cascade) added. v4 is not retired — v5 is the active reference for restoration of late-cycle operational detail; v4 remains the active reference for earlier-cycle detail.

Loading model: not part of the canonical doc set loaded by default. Load on demand when specific operational details from this period are needed for restoration. v6 trigger: next major cycle of operational detail accumulation (anticipated post-Phase-1.5 cutover).

## §G17 — 2026-06-04 Safety Portal Phase 2 Cloudflare scaffold (PR #158)

### Summary

PR #158 (squash `fe615db`, four-part-verify clean) introduced the `safety_portal/` TypeScript/Cloudflare execution tree — a new workstream alongside the Python `safety_reports/` workstream. Zero Python touched; all new code is TypeScript/Node/Cloudflare. Locally validated end-to-end (wrangler dev --local + Playwright). Deploy deferred to operator Cloudflare token step.

### §G17.1 — Architecture of the safety_portal/ tree

```
safety_portal/
  worker/
    src/
      worker/
        index.ts          # Hono app root + static-asset binding
        auth.ts           # bcryptjs login; HMAC session-cookie issue
        middleware/
          requireSession.ts  # HMAC-verify session cookie; iat+90d expiry
        routes/
          login.ts        # POST /login
          jobs.ts         # GET /api/jobs → ITS_Active_Jobs via Smartsheet
          forms.ts        # GET /api/forms → ITS_Forms_Catalog via Smartsheet
          submit.ts       # POST /api/submit (Phase 4+ JHA/safety form submission)
          logout.ts       # GET /logout (cookie clear)
        db/
          schema.sql      # D1: users + form_submissions tables
    public/
      forms/              # 10 PDF reference forms (static asset)
    wrangler.toml         # D1 binding, nodejs_compat, static assets config
    package.json          # hono, bcryptjs, signature_pad, vite, typescript
  spa/
    src/                  # React/Vite SPA (BRG/gold design system)
      components/
        SignaturePad.tsx  # SVG-vector signature capture (signature_pad library)
      pages/
        Login.tsx
        JobHazardAnalysis.tsx  # JHA form stub (Phase 4)
    vite.config.ts
```

**D1 database:** two tables — `users` (id, username, password_hash, role, created_at) and `form_submissions` (id, form_type, job_id, submitted_by, payload JSON, signature SVG, submitted_at). `wrangler d1` CLI manages schema; `npm run db:migrate:local` applies locally.

**Auth model:** bcryptjs cost-10 password hash; HMAC-signed session cookie (shared `SESSION_SIGNING_SECRET`); `requireSession` middleware validates HMAC + iat+90d expiry. No server-side session table yet (revocation deferred to Phase 7).

**Smartsheet reads:** the Worker reads ITS_Active_Jobs + ITS_Forms_Catalog directly via Smartsheet API (PAT from Cloudflare secret). These are the two sheets built in PR #155 (§G16.1 has their IDs).

### §G17.2 — Local dev workflow

```bash
cd ~/its/safety_portal/worker
npm install
npm run db:migrate:local          # creates .wrangler/d1/local/its-safety-portal-db.sqlite
npm run dev                        # wrangler dev --local on :8787 (Worker + D1)
# in a second terminal:
cd ../spa && npm run dev           # Vite dev server on :5173 (hot-reload SPA)
```

Playwright smoke (`npm run test` or `npx playwright test`) validates login + JHA stub against wrangler dev.

**Local D1 wipe hazard:** any `wrangler d1 migrations apply --local` invocation in the same directory (e.g., a review subagent running it) wipes and re-creates the local DB. If the DB is missing/empty, login correctly fails with 500. Fix: re-run `npm run db:migrate:local` to restore schema; then `npm run seed:local` (if a seed script exists) or manually insert a test user.

### §G17.3 — Deploy checklist (operator steps, deferred)

All steps require `CLOUDFLARE_API_TOKEN` (scopes: Workers, D1, R2 optional, custom-domain bind):

1. `wrangler login` or export `CLOUDFLARE_API_TOKEN=...`
2. `wrangler d1 create its-safety-portal-db` → copy `database_id` into `wrangler.toml` under `[[d1_databases]]`
3. `wrangler d1 migrations apply its-safety-portal-db` (remote, runs `db/schema.sql`)
4. `wrangler secret put SESSION_SIGNING_SECRET` (≥32-byte random, e.g., `openssl rand -hex 32`)
5. `wrangler secret put SMARTSHEET_TOKEN` (PAT with read on Operations workspace)
6. Decide topology: **Workers Static Assets** (recommended, better D1 binding) or **Cloudflare Pages**. Workers Static Assets: `wrangler deploy`. Pages: `wrangler pages deploy dist/`. Update blueprint `workstreams/safety-portal/mission.md` §11 after decision.
7. Bind custom domain `safety.evergreenmirror.com` in Cloudflare dashboard → Workers route or Pages domain.
8. Smoke-test: `curl -X POST https://safety.evergreenmirror.com/login -d '{"username":"...","password":"..."}'`

### §G17.4 — Open decisions at deploy

| Decision | Options | Notes |
|---|---|---|
| Pages vs Workers Static Assets | Workers SA (recommended) / Pages | Code deploy-agnostic; blueprint §11 assumed Pages |
| Free vs Paid plan | Paid (simpler) / Free + PBKDF2 swap | bcryptjs cost-10 > 10ms CPU on Free → Error 1102 |
| Session revocation | Phase 7 D1 sessions table | No server-side revocation until then |
| Form catalog v1 | Confirm with PM | Committed PDFs ≠ ITS_Forms_Catalog 4 forms; confirm before Phase 4 |
| TS capability gate | Phase 5 (email shim) | Python AST gate doesn't reach TS Worker |

## §G18 — 2026-06-05 Safety Portal Phase 3: Job-ID resolution + active_jobs + safety_week

PR #160 (squash `827c374`, four-part verify clean). Replaced `safety_reports/intake.py`'s legacy name-matching `resolve_project()` with a Job-ID-keyed lookup backed by `shared/active_jobs.py`. The portal payload now carries an explicit `Job ID` field; the intake pipeline reads it directly rather than fuzzy-matching a project name.

### §G18.1 — New modules

**`shared/active_jobs.py`** — read-only Job-ID lookup mirror for ITS_Active_Jobs. Key facts:

- `get_job_by_id(job_id: str) -> Optional[JobRecord]` — fetches the ITS_Active_Jobs sheet and returns the row whose `Job Slug` column matches `job_id` (case-insensitive). Returns `None` if no match or the sheet is unreachable.
- `JobRecord` is a typed dataclass with at minimum: `job_slug`, `project_name`, `address`, `stakeholder_email`, `safety_contact_email`, `active`.
- Read-only; no write path. The sheet is the system of record.
- Mirrors the `project_routing.py` pattern — same defensive caching + error surfacing.

**`shared/safety_week.py`** — Sat→Fri week rule and canonical Saturday-date key.

- `get_week_key(dt: date) -> date` — returns the Saturday that starts the week containing `dt`. If `dt` is already a Saturday, returns `dt`; otherwise rolls back to the prior Saturday.
- Canonical key format: `YYYY-MM-DD` (the Saturday date). All week-sheet references use this format.
- Handles Dec→Jan boundary correctly (no year-rollover bug).
- Used by `intake.py` to build the per-job week-sheet name and by any consumer that needs a consistent "which week does this date belong to?" answer.

### §G18.2 — resolve_project rewrite and legacy retirement

`safety_reports/intake.py::resolve_project()` was rewritten. Old behavior: fuzzy name-match against `BOX_PROJECT_FOLDERS` dict (hardcoded). New behavior: reads `job_id` from the portal payload; calls `active_jobs.get_job_by_id(job_id)`; returns a `ProjectResolution(project, reason)` named tuple.

`ProjectResolution` fields:
- `project`: the resolved project slug / `JobRecord`, or `None` on failure.
- `reason`: one of `"job_id_match"` | `"not_found"` | `"inactive"` | `"sheet_error"`.

**Legacy retired:** the old `resolve_project` fuzzy-match path (name-matching against `BOX_PROJECT_FOLDERS`) is removed. PDF-email intake that does NOT include a `job_id` in the payload will resolve as `not_found` and route to `ITS_Review_Queue`. The documented fallback for legacy PDF-email senders is operator-assisted re-send with the job ID added.

### §G18.3 — ITS_Active_Jobs live schema (post-Phase-3 migration)

Phase 3 migration added 4 contact columns and renamed one system column. Final schema as seeded (6 rows: bradley-1..rockford-s2):

| Column | Type | Notes |
|---|---|---|
| Project Name | TEXT_NUMBER (primary) | Human name, e.g. "Bradley 1 BBCHS" |
| Job Slug | TEXT_NUMBER | kebab-id, e.g. "bradley-1" — the lookup key |
| Address | TEXT_NUMBER | Blank (PM fills) |
| Active | CHECKBOX | Default true |
| Stakeholder Name | TEXT_NUMBER | |
| Stakeholder Email | TEXT_NUMBER | Required for portal auth |
| Stakeholder Phone | TEXT_NUMBER | |
| Safety Reports Contact Email | TEXT_NUMBER | Required; receives weekly report |
| Notes | TEXT_NUMBER | |
| Job ID | AUTO_NUMBER (pending) | UI-only — NOT yet created; operator must add in Smartsheet UI (prefix JOB-, **6-digit fill → `JOB-000001`** — corrected from "4-digit" per §G21), start 1. `active_jobs.py` reads it the moment it exists. **This `Job ID` is the decided permanent key; `Job Slug` (above) is being retired — see §G21.** |

Sheet ID: `6223950341164932` (standalone `ITS — Safety Portal` workspace → Safety Portal folder `6663869084002180`; moved from Operations, IDs preserved — see §G21).

Note: column order is cosmetically scrambled in the UI (contact columns interleave with Active/Notes — added one-at-a-time). Not load-bearing; `active_jobs.py` resolves by title.

### §G18.4 — Smartsheet API constraint: AUTO_NUMBER columns are UI-only

`type: AUTO_NUMBER` is rejected by the Smartsheet REST API with `errorCode 1008` regardless of column position or `systemColumnType` field. The only path is the Smartsheet UI (Insert Column → System → Auto-Number/Series). This is a permanent platform constraint, not a gap to fix in code. The older `AUTO_NUMBER at sheet creation` entry in `docs/tech_debt.md` covers the at-create variant; Phase 3 discovered the same applies to post-create column additions.

**Workaround pattern:** run the API-doable schema steps (add columns, rename) in code; detect-or-instruct on the UI-only step; document in `docs/tech_debt.md` for operator follow-up.

### §G18.5 — Deferred items (Phase 3 boundaries)

- **D1 dropdown sync (A.1.4):** deferred to deploy session. Needs D1 (Phase 2 deploy) + Python→D1 write mechanism decision (Worker `/api/sync` vs D1 HTTP API).
- **Portal forms (Phase 4):** the JHA + daily safety form rendering and submission pipeline.
- **Intake portal-marker branches (Phase 5):** `intake.py` HMAC-verified shim branches for portal-sourced submissions. Legacy PDF-email is the documented fallback.
- **Submission pipeline (Phase 5):** `POST /api/submit` Worker route → HMAC-verified email → `intake.py` → week-sheet write.

## §G19 — 2026-06-05 Safety Portal Phase 3 contacts amendment (PR #162)

PR #162 (squash `9e1ff9c`, four-part-verify clean). Extended `shared/active_jobs.py` and ITS_Active_Jobs to support TO/CC email routing and a named greeting contact. Zero impact on the portal Worker or the intake pipeline (sending is Phase 5).

### §G19.1 — ITS_Active_Jobs schema after Phase 3 contacts amendment

6 new TEXT columns added via additive API migration (run once, idempotent detect-or-skip):

| New column | Type | Purpose |
|---|---|---|
| Safety Reports Contact Name | TEXT_NUMBER | Greeting name for the weekly report ("Dear {name}") |
| CC 1 | TEXT_NUMBER | CC slot 1 — one email address string |
| CC 2 | TEXT_NUMBER | CC slot 2 |
| CC 3 | TEXT_NUMBER | CC slot 3 |
| CC 4 | TEXT_NUMBER | CC slot 4 |
| CC 5 | TEXT_NUMBER | CC slot 5 |

Full post-Phase-3-amendment column list (inheriting §G18.3 baseline + these 6): `Project Name`, `Job Slug`, `Address`, `Active`, `Stakeholder Name`, `Stakeholder Email`, `Stakeholder Phone`, `Safety Reports Contact Email`, `Safety Reports Contact Name`, `CC 1`–`CC 5`, `Notes`, `Job ID (AUTO_NUMBER, pending)`.

Sheet ID: `6223950341164932` (standalone `ITS — Safety Portal` workspace → Safety Portal folder `6663869084002180`; moved from Operations, IDs preserved — see §G21). Cosmos from §G16.1 carried forward.

### §G19.2 — Email routing model (Phase 3 definition)

| Role | Source column | Used in | Notes |
|---|---|---|---|
| TO | Safety Reports Contact Email | `weekly_send` (Phase 5) | Required; single address |
| CC | CC 1–CC 5 (flattened) | `weekly_send` (Phase 5) | 0–5 addresses; empty cells skipped |
| Greeting | Safety Reports Contact Name | Report body — "Dear {name}" | Falls back to TO address if blank |
| Stakeholder | Stakeholder Email/Name | Packet body reference only | NOT in the TO/CC envelope — referenced inside the weekly report as PM/project contact |

All sending is Phase 5. This session only defined the model and wired the data model; no `weekly_send` code was changed.

### §G19.3 — active_jobs.ActiveJob dataclass additions

`shared/active_jobs.ActiveJob` now carries:

```python
safety_reports_contact_name: str   # from "Safety Reports Contact Name" TEXT column
cc_emails: list[str]               # flattened, deduped; empty list if all CC slots blank
```

**`_flatten_cc(row, columns)` helper** — internal to `active_jobs.py`. For each of CC 1–5:
1. Reads the TEXT cell value (empty string if blank).
2. Comma-splits (handles multi-email strings in a single cell — not the design intent but handled defensively).
3. Strips whitespace.
4. Validates email shape (basic `@` check; malformed → WARN log + skip).
5. Deduplicates the final list (preserving first-seen order).

Returns a `list[str]` of validated email strings. Never raises; WARN on bad input.

### §G19.4 — Key live finding: MULTI_CONTACT_LIST loses external email addresses on API read-back

**Empirically confirmed in this session.** When a `MULTI_CONTACT_LIST` column holds external (non-org-member) email addresses via the API, `cell.value` returns display names (`"One, Two"`) and `cell.objectValue` is similarly name-only. The email addresses are silently dropped — Smartsheet resolves them to display names at write time and never persists the email string for externals.

Behavior breakdown by column type and contact kind:

| Column type | Contact kind | `cell.value` | `cell.objectValue` |
|---|---|---|---|
| MULTI_CONTACT_LIST | External email | Display names only | Name-only — email dropped |
| CONTACT_LIST (single) | External email | Email address (reliable) | `{email, name}` |
| CONTACT_LIST (single) | Org member | Email address | `{email, name}` |

**Conclusion:** Do NOT use `MULTI_CONTACT_LIST` (or `CONTACT_LIST` in multi-mode) to store arbitrary external recipient emails. **Use TEXT columns** — store the email string directly. TEXT cell value is always the literal string you wrote.

**TEXT → CONTACT_LIST column type flip:** verified live — `PUT /columns/{id}` with `{"type": "CONTACT_LIST"}` on a TEXT column returns 200. The reverse (CONTACT_LIST → TEXT) would lose contact data. This is a one-way operator escape hatch; not a routine code operation.

**Applied decision in PR #162:** all 5 CC slots and the Contact Name column are `TEXT_NUMBER`. `_flatten_cc` reads them as plain strings. No CONTACT_LIST columns involved in the CC/TO routing path.

### §G19.5 — Deferred items (Phase 3 contacts amendment boundaries)

- **Phase 5 `weekly_send` wiring:** `send_one_row` must resolve TO + CC from `ActiveJob.safety_reports_contact_email` + `ActiveJob.cc_emails`; log the full resolved TO+CC list at send. Tech-debt entry filed (accepted-risk — addresses are operator-entered, not allowlist-validated).
- **CC recipient allowlist validation:** currently none. Accepted risk documented in `docs/tech_debt.md`. Revisit at Phase 5 `weekly_send` build.
- **ITS_Active_Jobs Address cells still BLANK** — PM fills manually; unchanged from Phase 3 baseline.

## §G20 — 2026-06-05 Safety Portal Phase 4 PR 1: form definitions foundation (PR #164)

### Summary

PR #164 (squash `940999e`, four-part-verify clean) landed the form definitions foundation for Phase 4. No Python daemons or Smartsheet wiring changed — this PR is entirely within `safety_portal/forms/` + tests + the ITS_Forms_Catalog live migration. Session log: `docs/session_logs/2026-06-05_safety-portal-phase4-pr1-forms-foundation.md`.

### §G20.1 — meta-schema.json: section archetype contract

`safety_portal/forms/meta-schema.json` is the JSON-Schema contract that governs every form definition. It is the single source of truth for BOTH the Phase 4 PR 2 TS display renderer and the Phase 4 PR 3 Python reportlab PDF renderer. Render = Option B (definitions drive renderers; no renderer-specific schema forks).

Top-level fields:
- `formId` (string, kebab-case stable key matching the filename stem)
- `title`, `description`, `version`
- `variantOf` (optional, string — points to the parent `formId` for the parent/variant model)
- `sections[]` — ordered list of section objects

Section object fields:
- `id`, `title`
- `type` — one of 3 archetypes: `rows_with_signatures`, `grouped_checklist`, `sectioned_assessment`
- Archetype-specific fields (rows, groups, subsections) carry their own required shapes per the meta-schema

The 3 archetypes map directly to the 3 renderer components that Phase 4 PR 2 must implement. A fresh CC session building the TS renderer should load `meta-schema.json` to understand the exact shape before writing rendering logic.

### §G20.2 — The 11 form definitions

| File | formId | Archetype(s) | Notes |
|---|---|---|---|
| `jha.json` | `jha` | rows_with_signatures | JHA hazard-item rows + multi-row sig section |
| `equipment-preinspection.json` | `equipment-preinspection` | grouped_checklist | Telehandler; 64 checklist items across groups |
| `equipment-preinspection-crane.json` | `equipment-preinspection-crane` | grouped_checklist | Crane variant; `variantOf: equipment-preinspection` |
| `visitor.json` | `visitor` | sectioned_assessment | Visitor sign-in + content sections |
| `hsse.json` | `hsse` | grouped_checklist | 11 category groups (HSS&E combined) |
| `toolbox-talk-general.json` | `toolbox-talk-general` | sectioned_assessment | General TBT; sign-in rows |
| `toolbox-talk-fire.json` | `toolbox-talk-fire` | sectioned_assessment | Fire safety TBT |
| `toolbox-talk-ppe.json` | `toolbox-talk-ppe` | sectioned_assessment | PPE TBT |
| `toolbox-talk-excavation.json` | `toolbox-talk-excavation` | sectioned_assessment | Excavation TBT |
| `toolbox-talk-ladders.json` | `toolbox-talk-ladders` | sectioned_assessment | Ladders/fall-protection TBT |

All were transcribed faithfully from the 10 reference PDFs in `safety_portal/worker/public/forms/`. Note: the source TBT PDFs have no Presenter/Date-on-page header fields — the digital record gets job + work-date from the submission envelope. If a header field is wanted, it must be added explicitly (tech-debt entry filed).

### §G20.3 — ITS_Forms_Catalog parent/variant migration

PR #164 migrated ITS_Forms_Catalog (sheet id `423274885369732`) from the original 4 flat rows to the parent/variant model. New schema adds two columns: `Parent Form` (TEXT_NUMBER — points to the parent's `formId`, blank for parents) and `Variant Tag` (TEXT_NUMBER — short discriminator, blank for parents).

**V1 catalog after PR #164 (12 rows):**

| Form Code | Parent Form | Variant Tag | Notes |
|---|---|---|---|
| `jha` | — | — | Parent |
| `equipment-preinspection` | — | — | Parent |
| `equipment-preinspection-crane` | `equipment-preinspection` | crane | Variant |
| `visitor` | — | — | Parent (new; was absent from v0) |
| `hsse` | — | — | Parent (new; was absent from v0) |
| `toolbox-talk-general` | `toolbox-talk` | general | Variant |
| `toolbox-talk-fire` | `toolbox-talk` | fire | Variant |
| `toolbox-talk-ppe` | `toolbox-talk` | ppe | Variant |
| `toolbox-talk-excavation` | `toolbox-talk` | excavation | Variant |
| `toolbox-talk-ladders` | `toolbox-talk` | ladders | Variant |
| `toolbox-talk` | — | — | Parent (virtual; no standalone definition file) |
| ~~`daily-site-safety-v1`~~ | removed | — | Not a form-fill candidate |

Migration ran via `scripts/migrations/migrate_forms_catalog_parent_variant.py` (idempotent; preview-default; `--commit` for live). Live migration applied this session: 2 columns added, 5 rows updated (parents), 5 variant rows added, 1 row deactivated (daily-site-safety). Verified live: all 12 rows present with correct column values.

### §G20.4 — Test baseline (PR #164)

- `tests/test_forms_validation.py`: 49 tests — one test per (definition file × validation check), including: each definition validates against the meta-schema, `formId` matches filename stem, `version` is semver-shaped, `variantOf` references a known `formId` when set. All 49 passed; mypy 0; ruff clean; branch CI green; main-branch CI on merge commit SUCCESS.
- `jsonschema` added to `pyproject.toml` runtime deps (not dev-only; the renderer will also use it at runtime for submission validation).

### §G20.5 — Phase 4 remaining work

Two PRs remain before Phase 5:

**PR 2 — TS display runtime:** generic definition-driven renderer in `safety_portal/spa/src/` for the 3 archetypes. Must implement: form-type + variant dropdowns (ITS_Forms_Catalog parent/variant); multi-row SVG signature capture via `signature_pad`; amend/prefill from a prior submission; structured-data emit to the HMAC shim. Replaces hard-coded `JhaStubPage.tsx`. Tech-debt: `docs/tech_debt.md` "Safety Portal Phase 4 PR 2".

**PR 3 — Python reportlab PDF renderer:** reads `safety_portal/forms/*.json` + structured submission → print-parity PDF (Evergreen header, table/checklist/section layout, legal invariants in code, embedded SVG signatures). Deterministic, no AI. Per-form parity tests. Invoked by Phase 5 intake (Option B path); PDFs land in Box. Add `reportlab` dep (one-line `pyproject.toml` edit). Tech-debt: `docs/tech_debt.md` "Safety Portal Phase 4 PR 3".

**Build approach used for PR #164:** each form definition was built by loading the reference PDF in `safety_portal/worker/public/forms/` and manually transcribing the structure (section titles, item labels, signature-block positions) into JSON per the meta-schema. This required iterative meta-schema refinement as edge cases surfaced (e.g., the TBT sign-in model needed a `content_then_signin` subtype of `sectioned_assessment`). No AI extraction was used — deterministic transcription is load-bearing for legal-invariant preservation.
- **New Job form (UI-only):** Smartsheet form on ITS_Active_Jobs for office PM. Fields: Project Name, Address, Stakeholder Name/Email/Phone, Safety Reports Contact Email, Active.

## §G21 — 2026-06-05 Safety Portal blueprint reconciliation (Phase 4 PR 2/3 landed; workspace move; WSR_human_review design; deploy + topology resolved)

### Summary

Blueprint doctrine brought current with the as-built Safety Portal (exec HEAD `ffad86b`, Phase 5 PR 1 / PR #168) and the 2026-06-04/05 design+build decisions. `workstreams/safety-portal/{mission,brief}.md` bumped to **v2**; the topology and the deploy decision were reconciled across the reference docs; a doctrine-update flag was raised for Op Stds §23/§24 (not edited — version-gated). This §G21 consolidates the operational detail and supersedes the stale locations pointered inline in §G16/§G18/§G19. (Phase 5 PR 1 landed mid-session — see §G21.8 — and resolved the code-label drift this §G21 originally flagged.)

### §G21.1 — Phase 4 PRs 2 + 3 landed; form definition set revised

- **PR #166** (`23af65f`) — definition-driven TS display runtime. **PR #167** (`2946184`) — Python Option-B `reportlab` renderer + equipment tri-state. Phase 4 (PRs 1–3) is **complete**.
- The form definition set was **revised** from PR #164's intermediate set (§G20). Current as-built = **10 definition files** in `safety_portal/forms/*.json` = **5 parents + 7 variants**:
  - Parents (no-variant parents render their own definition): `jha-v1`, `hsse-work-observation-v1`, `visitor-sign-in-v1`. Variant-parents (collapse under a 3rd picklist, no own definition): Equipment Pre-Inspection, Toolbox Talk.
  - Variants: equipment `skid-steer`, `telehandler`; toolbox-talk `back-sprains`, `electrical`, `ergonomics`, `hard-hat`, `ppe`.
  - Daily Site Safety Worksheet is **out**; Visitor Sign-In + HSS&E Work Observation are **in** (canonical = the 10 reference PDFs).
- **Equipment checklists are tri-state OK / NOT OK / N/A** (N/A distinct from blank). Legal-invariants-in-code (JHA "if conditions change…" footer; equipment lock/tag-out line) are mandatory + non-editable.
- The single declarative definition drives **both** the TS display runtime and the Python renderer (the no-drift contract).

### §G21.2 — Workspace move to standalone `ITS — Safety Portal` (live; IDs preserved)

The `Safety Portal` folder (id `6663869084002180`) and its two sheets — `ITS_Active_Jobs` (`6223950341164932`), `ITS_Forms_Catalog` (`423274885369732`) — were **MOVED from `ITS — Operations` to a new STANDALONE workspace `ITS — Safety Portal`**, with **all IDs preserved**. The per-job week sheets and the `WSR_human_review` approval sheet live in the same workspace. Config sheets (`ITS_Config`, `ITS_Errors`, `ITS_Trusted_Contacts`, `ITS_Review_Queue`, `ITS_Quarantine`) stay in `ITS — System` and are read by ID (shared infra, not safety-specific).

Doctrine consequence: **workspace access = approval authority** (sharing the workspace is the send-gate access control); the safety subsystem ships independent of the Forefront/demo structures. Supersedes the "Operations workspace" locations in §G16 (lines 708, 736), §G18.3 (894), §G19.1 (930) — pointered inline.

**Code label drift — RESOLVED same session by Phase 5 PR 1 (PR #168; see §G21.8):** at mid-session authoring, `shared/sheet_ids.py` still named the folder `FOLDER_OPERATIONS_SAFETY_PORTAL` with "ITS — Operations / Safety Portal" comments and had **no `WORKSPACE_SAFETY_PORTAL` constant** (the move was live in Smartsheet, IDs preserved → code still functioned, but the labels lagged). PR #168 then added `WORKSPACE_SAFETY_PORTAL = 194283417429892`, renamed the folder constant to `FOLDER_SAFETY_PORTAL` (keeping `FOLDER_OPERATIONS_SAFETY_PORTAL` as a back-compat alias), and added `SHEET_WSR_HUMAN_REVIEW`.

### §G21.3 — Topology is now 6 workspaces (doctrine-update FLAGGED)

The canonical model (Op Stds §23) is the **five-workspace audience-separated** topology. The standalone `ITS — Safety Portal` is a **sixth** workspace, deliberately **outside** that audience-separation model (approval-gated, self-contained). **DOCTRINE-UPDATE FLAGGED** (not edited — version-gated): Op Stds **§23** ("Carries forward… No change", 5-workspace) and **§24** (sheet-ID bootstrap, 5 workspaces) need a v17 bump to acknowledge the sixth workspace. Active-memory entry #15 and §G1's 5-workspace list remain as historical records; the **live count is 6**. The reference topology tables (`foundation-scaffold.md`, `project-organization.md`, `smartsheet-handoff.md`) were updated to add the sixth workspace pending the §23 bump. **[RESOLVED 2026-06-05 — Op Stds bumped to v17; §23/§24 now acknowledge the sixth workspace. See §G23.3.]**

### §G21.4 — Deploy resolved: Cloudflare Workers + Static Assets

Deploy = **Cloudflare Workers + Static Assets** (a single Worker serves the SPA + same-origin `/api/*`). **NOT Cloudflare Pages** (Pages is in maintenance mode). Validation host `safety.evergreenmirror.com`; production on `evergreenrenewables.com`. This resolves the §G17.4 "Decide topology" open row and the `claude-code-info-gap.md` "topology TBD" / "blueprint mission §11 assumed Pages" notes. **Requires Workers Paid (~$5/mo)** — see §G21.6(c).

### §G21.5 — `WSR_human_review` (Phase 5 design) supersedes `WPR_Pending_Review` for the safety path

NEW central approval sheet in the Safety Portal folder — **not** the legacy `WPR_Pending_Review` in `ITS — Human Review`. One row per **(job, week)**: compiled PDF, **editable email body (source of truth for send)**, recipients (TO = Safety Reports Contact Email; CC = non-empty CC 1–5), `Approve for Scheduled Send` + `Send Now`, auto-stamped Approved By/At. **Review + edit + approve + send happen only here.** `weekly_send` (Phase 5) reads the approved, human-edited body from this sheet; default cadence **7 AM Pacific Monday** from an `ITS_Config` row, watchdog retries, resolved recipient list logged. **Compile** (week-sheet `Compile Now` checkbox or auto Friday; skips if already compiled and no new docs; merges Sat→Fri ascending; never closes the week) dual-writes the rollup to the week sheet (read-only snapshot) and to `WSR_human_review` (editable). Late arrivals → next uncompiled week + Review-Queue flag. The sheet was **built by Phase 5 PR 1** (PR #168, `build_wsr_human_review_sheet.py`; `SHEET_WSR_HUMAN_REVIEW = 5035670127988612`); the intake/compile/send wiring that populates and reads it is the rest of Phase 5 (§G21.8).

This is the safety workstream's `<Workstream>_Pending_Review` surface under FM v11 Invariant 1. **Drift flagged:** `safety_reports/{mission,brief}.md` and `system-hr-handoff.md` still name `WPR_Pending_Review`; reconciliation deferred to the operator (the safety pipeline's approval sheet is now `WSR_human_review`).

### §G21.6 — Empirical findings (consolidated, durable)

Three platform constraints, surfaced here so no future session re-discovers them:

- **(a) Smartsheet `AUTO_NUMBER` columns are UI-only.** REST API rejects `type: AUTO_NUMBER` with `errorCode 1008` (§G18.4). The `Job ID` column (`AUTO_NUMBER`, `JOB-000001` — **6-digit**, corrected from §G18.3's "4-digit") must be created in the Smartsheet UI; code reads it once it exists. This 6-digit `Job ID` is the **decided permanent key**; the legacy kebab `Job Slug` is **retired** (vestigial — `active_jobs.py` still matches on `Job Slug` pending the column creation + migration).
- **(b) Smartsheet `MULTI_CONTACT_LIST` drops external emails on API read-back** (§G19.4) → recipient columns (Safety Reports Contact Email, CC 1–5) use **`TEXT`**, storing the literal email string.
- **(c) Cloudflare Workers free-tier 10 ms CPU cap cannot run a secure password hash.** `bcryptjs` cost-10 exceeds it (Error 1102) → **Workers Paid plan required**. Resolves the §G17.4 "Free vs Paid" row as a hard constraint, not a tuning choice.

### §G21.7 — Portal never reads or writes Smartsheet (correction to §G16 framing)

Verified in execution code (`2946184`): `safety_portal/worker/index.ts` serves `/api/jobs` "from D1; the portal never reads Smartsheet"; `safety_portal/src/forms/registry.ts` derives the catalog from the bundled definitions + the D1 sync. This **supersedes** §G16's "the two Smartsheet config sheets the Safety Portal reads" framing: the portal reads its **own D1** (populated out of band from `ITS_Active_Jobs` / `ITS_Forms_Catalog`), and the **Python pipeline holds the only Smartsheet/Box write credentials**. The catalog→D1 sync mechanism is a deferred execution detail; the durable doctrine fact is the portal↔Smartsheet decoupling (the External Send Gate two-process model as a deployment boundary).

### §G21.8 — Phase 5 PR 1 landed mid-session (PR #168, `ffad86b`) — back-half foundation

PR #168 — `feat(safety-portal): Phase 5 PR 1 — back-half foundation (WSR_human_review + PDF merge + sheet_ids + amendments b/c)` — merged during this same 2026-06-05 window (after Phase 4's `2946184`, which several inline citations above reference as the then-current HEAD). What it landed:

- **`WSR_human_review` sheet built** — `scripts/migrations/build_wsr_human_review_sheet.py`; `SHEET_WSR_HUMAN_REVIEW = 5035670127988612` in `shared/sheet_ids.py`. This is the §G21.5 review surface, now provisioned (the intake/compile/send *wiring* that populates and reads it remains the rest of Phase 5).
- **`sheet_ids.py` standalone-workspace constants** — `WORKSPACE_SAFETY_PORTAL = 194283417429892`; folder constant renamed to `FOLDER_SAFETY_PORTAL = 6663869084002180` with `FOLDER_OPERATIONS_SAFETY_PORTAL` kept as a back-compat alias. **This resolves the code-label drift §G21.2 originally flagged** (no separate execution tech-debt needed for the rename/capture).
- **Weekly PDF merge** primitive + amendments b/c (the amend-supersede path).

Net effect on this §G21: the deploy decision (§G21.4), topology (§G21.3 — doctrine flag still stands; Op Stds §23/§24 unchanged), and empirical findings (§G21.6) are unaffected; the §G21.2 code-drift flag is **closed**; the §G21.5 WSR sheet is **built**. The blueprint `last_verified_against` for the docs touched this session is `ffad86b`.

## §G22 — 2026-06-05 Safety Portal Phase 4 PR 2/3 + Phase 5 PRs 1+2: display runtime, renderer, transport queue

### Summary

PRs #166–#169 (exec HEAD `fc034eb`) completed Phase 4 and landed Phase 5 PRs 1+2. Four PRs in one session; all four-part-verified clean. The dominant design decision was the **Phase 5 transport model**: operator ratified a Python pull model (Worker D1 queue + Mac-side `portal_poll.py`) over the brief's email-shim design. Session log: `docs/session_logs/2026-06-05_safety-portal-phase4-runtime-renderer-phase5-foundation-transport.md`.

### §G22.1 — Phase 4 PRs 2+3: display runtime + PDF renderer

**PR #166** (`23af65f`, four-part-verify clean) — TS definition-driven display runtime:
- `safety_portal/src/forms/` — 3 archetype renderer components (rows+signatures, grouped-checklist, sectioned-assessment).
- Form-type + variant dropdowns populated from ITS_Forms_Catalog (parent/variant columns); variant-parent model data-driven.
- Multi-row SVG signature capture via `signature_pad`; amend/prefill from a prior submission (D1 lookup by submission UUID).
- Structured-data emit to Worker on submit.
- 3 new Worker endpoints: `GET /api/jobs` (active job list for the dropdown), `GET /api/forms/:id` (form definition), `POST /api/submissions` (store + queue).
- D1 migration 0004: `jobs` + `submissions` tables.

**PR #167** (`2946184`, four-part-verify clean) — Python Option-B reportlab renderer + equipment tri-state:
- `safety_reports/form_pdf.py` — reads `safety_portal/forms/*.json` + structured submission payload → deterministic print-parity PDF.
- Layout engine: Evergreen header, per-archetype table/checklist/section layout, legal invariants in code (JHA "conditions change" footer; equipment lock/tag-out line), embedded SVG signatures (rasterized to PNG via cairosvg, then placed in the PDF).
- **Equipment tri-state:** checklist items are OK / NOT OK / N/A (N/A is distinct from blank/unchecked; the N/A branch is a deliberate "inspected, not applicable" signal — not the same as "skipped").
- `form_pdf.merge_pdfs(pdf_paths) -> bytes` primitive: merges a list of PDFs into one packet via pypdf.
- No AI step; no Anthropic calls. Deterministic.
- `+reportlab` + `+pypdf` to `pyproject.toml` runtime deps (one-line edits; CI `pip install -e ".[dev]"`, no lockfile to regen).
- N/A-vs-blank distinction is load-bearing: the PDF renderer must faithfully represent "inspector deliberately marked N/A" vs "inspector did not reach this item."

### §G22.2 — Phase 5 PR 1: back-half foundation (PR #168, `ffad86b`)

Landed the structural scaffolding Phase 5 needs before any wiring:

- **`WSR_human_review` sheet** — built by `scripts/migrations/build_wsr_human_review_sheet.py`; `SHEET_WSR_HUMAN_REVIEW = 5035670127988612`. Schema: one row per (job, week); columns: Job ID, Week Ending, PDF URL, Email Body (editable; source of truth for send), Approved By, Approved At, Approve for Scheduled Send (checkbox), Send Now (checkbox), Send Status, Sent At. This is the safety workstream's `<Workstream>_Pending_Review` surface under FM v11 Invariant 1. `WPR_Pending_Review` in `ITS — Human Review` is superseded for the portal flow (legacy weekly-generate still writes there; the portal-backed compile will dual-write WSR going forward).
- **`sheet_ids.py` constants:** `WORKSPACE_SAFETY_PORTAL = 194283417429892`; `FOLDER_SAFETY_PORTAL = 6663869084002180`; `FOLDER_OPERATIONS_SAFETY_PORTAL` kept as back-compat alias; `SHEET_WSR_HUMAN_REVIEW = 5035670127988612`.
- **Amendments b/c** (stale comment fixes; runbook Job ID format corrected to 6-digit `JOB-000001`).

### §G22.3 — Phase 5 PR 2: transport queue — pull model decided (PR #169, `fc034eb`)

**The transport decision (operator-ratified 2026-06-05, supersedes brief's email-shim design):**

The portal→intake transport is a **Python pull model**. The brief had specified a `portal-noreply@` email shim that would relay submissions as HMAC-verified emails into the unified `safety@` mailbox (intake_poll would read them like legacy emails, just with a trust marker). This was rejected in favor of:

- **Worker = durable D1 queue (send-free).** Submission stored atomically in D1 at submit time — cloud-always-on. The Worker never emails. It exposes two authenticated internal endpoints:
  - `GET /api/internal/pending` — bearer-authed; returns unprocessed submission rows.
  - `POST /api/internal/mark-filed` — bearer-authed; marks a submission as processed + stores the receipt.
- **`shared/portal_hmac.py` — the cross-language HMAC verify contract.** Signs/verifies `X-ITS-Portal-HMAC` headers (`HMAC-SHA256(secret, payload_json)`). Cross-language validation confirmed in PR #169 tests (Python signs → TS verifies; TS signs → Python verifies).
- **`portal_poll.py` (to build)** — Mac-side daemon polling the Worker. Standard daemon contract (heartbeat, kill-switch, fcntl lock, `@its_error_log`). Polls `/api/internal/pending`, verifies the HMAC, hands each submission to `intake.py`'s processing path, posts receipt.
- **D1 migration 0005** — adds the `pending_submissions` queue table + `processed` flag.

**Why pull over email shim:**
1. Reliability: one local D1 write vs a multi-hop Worker→email-provider→mailbox→poll chain. "Submitted" is atomic at the D1 write, not eventual.
2. Edge security: Worker holds no send capability, no outbound SMTP/Resend key. Can't become a spam cannon even if compromised at the Worker layer.
3. No new infrastructure: no `portal-noreply@` mailbox, no sending domain, no M365 app registration.
4. Operator preference: leaning away from Microsoft for non-critical paths; Resend would work but adds a dependency for no gain.

**Capture cloud-always-on; filing on the Mac (deliberate doctrine choice).**
Submission queues in D1 if the Mac is offline; drains when it wakes. Nothing is lost. Filing (Smartsheet/Box write + Python reportlab render) stays on the Mac. This is NOT a doctrine change from the planning layer's "Mac-first through Phase 4" model — the cloud holds only the submission queue, no write credentials or rendering capability.

**Approval stays human-in-loop (F22 preserved):** a human flips `Approve for Scheduled Send` on `WSR_human_review`; Smartsheet `MODIFIED_BY` auto-captures the approver identity; F22 `verify_approval` checks the actor is in the authorized-approvers list before `weekly_send` proceeds.

### §G22.4 — Deploy secrets enumerated (Phase 5 additions)

Phase 5 adds two new Worker secrets beyond the base deploy entry (see §G21.4 / §G17.4):

| Secret | Worker name | Mac Keychain name | Description |
|---|---|---|---|
| HMAC payload secret | `HMAC_PAYLOAD_SECRET` | `ITS_PORTAL_HMAC_SECRET` | ≥32-byte random; used by `shared/portal_hmac.py` + Worker signing |
| Internal bearer token | `PORTAL_INTERNAL_API_TOKEN` | `ITS_PORTAL_INTERNAL_TOKEN` | Bearer auth for `/api/internal/*`; Mac daemon presents this to poll |

Both must be set before `portal_poll.py` can authenticate. The HMAC secret must be identical on both sides (Worker `wrangler secret put` + Mac Keychain). `wrangler.jsonc` also needs the D1 `database_id` placeholder filled (migrations 0001–0005 applied remotely).

### §G22.5 — Remaining Phase 5 (all deploy/live-gated)

In dependency order:

1. **Deploy prerequisites** (§G22.4 + §G21.4): Cloudflare token + D1 create + secrets + `wrangler deploy` + custom domain.
2. **`portal_poll.py`** — Mac-side puller daemon. Standard daemon contract. Locally testable on `wrangler dev --local`.
3. **Intake portal-marker branch** — in `safety_reports/intake.py`: HMAC verify (already done by `portal_poll`) → UUID dedupe guard → Sat→Fri week key via `safety_week` → `active_jobs` lookup → `form_pdf.render` (Option B) → per-job/week Box tree via `week_folder` → file PDF → write week-sheet row → receipt POST. **`box_client.canonical_job_path()` is still a stub** (format unconfirmed with owner; see existing tech-debt entry); a `get_or_create_folder` primitive is needed. UUID idempotency guard must prevent double-filing on retry.
4. **`weekly_generate` compile step** — on Friday 14:00 (or `Compile Now` checkbox): merge Sat→Fri submission PDFs via `form_pdf.merge_pdfs` + generate narrative; dual-write to per-job week sheet (read-only snapshot) and `WSR_human_review` row (editable body + resolved recipients). Skip if already compiled + no new docs since last compile. Late arrivals → next uncompiled week + Review-Queue flag.
5. **`weekly_send` rewire** — Phase 5 send: reads approved `WSR_human_review` rows; attaches merged PDF; TO = `safety_reports_contact_email`, CC = flattened `cc_emails` from `ActiveJob`; logs full resolved TO+CC at send; refuses on blank recipients or `[GENERATION_FAILED:]` tag; Pacific-Monday 7 AM cadence from `ITS_Config`. Watchdog catch-up (Check I) retries missed Friday compile.
6. **D1 dropdown sync** (deferred to deploy session) — push ITS_Active_Jobs active jobs → Worker D1 `active_jobs` table so the portal's Job dropdown stays current. Mechanism TBD: Worker `/api/sync` (POST, HMAC-authed) vs Cloudflare D1 HTTP API from Python.

Phase 7: server-side session revocation table (D1 `sessions` with `revoked_at`).

## §G23 — 2026-06-05 Safety Portal blueprint delta: clean-break + production-cutover DNS + Op Stds v17 (6th workspace)

### Summary

Blueprint-side reconciliation (no exec code) bringing doctrine current with the transport decision (§G22.3) plus two **new operator decisions** this session — the **clean break** (portal-only safety intake) and the **production-cutover DNS plan** — and applying the **operator-approved Op Stds v16 → v17** workspace-topology bump. Verified against exec HEAD `753f12f` (PR #171; the repo advanced `0cff5f9` → `753f12f` during this blueprint session). Companion blueprint session log: `session-logs/2026-06-05_safety-portal-transport-cleanbreak.md`.

### §G23.1 — Clean break: safety intake is portal-only at launch

Evergreen cuts over all-at-once with **no integration of the legacy email-PDF system** — no Evergreen safety data flows the old path. Decisions:

- `intake_poll.py` (the Microsoft Graph safety mailbox poller) is **superseded by `portal_poll.py`** as the safety input.
- `WPR_Pending_Review` is **decommissioned**; the safety pipeline unifies on `WSR_human_review`. This closes the §G21.5 WPR→WSR drift flag — `safety-reports` mission (v5.2) + brief (v6.2) reconciled this session.
- **Scope boundary — NOT an email teardown.** The shared email infrastructure (`shared/graph_client.py`, `shared/untrusted_content.py`, `shared/header_forgery.py`) and `intake.py`'s Graph `process_message` path are **preserved** for the committed **Email Triage** workstream (its mission updated with the inherited-infra note).
- **Code-state (verify-before-fix, exec `753f12f` / PR #171):** a ratified decision, actively landing. **`intake_poll.py` is now retired/tombstoned** (PR #171 — raises `NotImplementedError`; the shared Graph infra is explicitly preserved for Email Triage). Still **in-flight (not on main):** `portal_poll.py`, the `intake.py` portal-marker branch, and the `weekly_generate`/`weekly_send` WSR rewire — so the `weekly_*` scripts still reference `WPR_Pending_Review` (**decommissioned-by-doc** until the rewire lands). The blueprint encodes the decided architecture and records this landed/in-flight boundary.

### §G23.2 — Production cutover DNS plan (applicable at cutover, NOT now)

- Evergreen's site is **GoDaddy-hosted WordPress + Elementor**; the apex `evergreenrenewables.com` DNS and M365 email live on GoDaddy.
- **Evergreen has no Cloudflare account** — one is created fresh at cutover, **Evergreen-owned** (Daniel creates the Evergreen account).
- Do **not** migrate the apex zone. Attach **only** `safety.evergreenrenewables.com` to Cloudflare — **likely via subdomain NS-delegation** at GoDaddy (delegate that label's NS records to Cloudflare), leaving WordPress + M365 email untouched. Exact subdomain-attach mechanism resolved at deploy prep — **likely path, not locked.**

### §G23.3 — DOCTRINE: Op Stds v16 → v17 (sixth, standalone workspace)

Operator-approved doctrine bump. §23/§24 now acknowledge **`ITS — Safety Portal`** as a **6th, standalone, approval-gated workspace** — governing principle **workspace-membership = approval authority**; self-contained subsystem; an additive, deliberately-scoped exception to the five-workspace audience-separation model (otherwise unchanged). Tag `operational-standards-v17`. This **clears the topology doctrine drift** the §G21.3 flag raised — doctrine now matches the 6-workspace reality already recorded in the reference tables + `sheet_ids.py`. Active-memory entry #15 + §G1's "5-workspace" text remain historical; the **canonical count is now 6** per Op Stds v17 §23/§24.

### §G23.4 — Blueprint docs reconciled this session

`workstreams/safety-portal/{mission,brief}.md` (transport pull-model + clean-break + cutover delta; kept at v2 per the operator's "delta on v2" framing; `last_verified_against 753f12f`) · `workstreams/safety-reports/mission.md` v5.2 + `brief.md` v6.2 (WSR surface, email-PDF safety intake retired, preserved-infra note) · `workstreams/email-triage/mission.md` (inherited shared-email-infra note) · `references/claude-code-info-gap.md` (clean-break + cutover + v17 + SHA) · `doctrine/operational-standards.md` **v17** (the doctrine edit) · `session-logs/2026-06-05_safety-portal-transport-cleanbreak.md`.

### §G23.5 — Flags handed to the execution layer (out of scope this session)

- **`ops-stds-enforcer` agent is pinned at Op Stds v13.** The v17 bump **widens** that gap; the agent-file update (Op Stds version + §43/§44 awareness + the §23 6th-workspace acknowledgement) is an exec-repo task. Until then the agent is blind to §23's v17 change.
- **`check_doctrine_drift` scan-scope** widening (to recognize the topology acknowledgement) is exec-side — not touched from this blueprint session.

## §G24 — 2026-06-05 Safety Reports is LLM-free (deterministic weekly product)

### Summary

Operator-confirmed 2026-06-05: the **Safety Reports workflow uses no LLM.** The weekly product is a **deterministic merge** of the week's submitted-form PDFs (`form_pdf.merge_pdfs`) **+ a fixed-template email body**, written to `WSR_human_review` for human review/edit/approve/send. The prior design — Anthropic drafts a narrative Weekly Project Report (WPR) — is **retired** with the portal cutover. Scoped to Safety Reports **only**: LLM/Anthropic remains in scope for Email Triage and AI Employee Capabilities. Blueprint-only change (no doctrine bump; foundation invariants unchanged). Verified against exec HEAD `cf86a9e` (PR #172; the repo advanced `753f12f` → `cf86a9e` — R2/PDF_BUCKET binding removed, consistent with Box-SoR + Option-B).

### §G24.1 — What changed in the blueprint

- `safety-reports/mission.md` → **v5.3** overlay; `brief.md` → **v6.3** overlay. The weekly "generation" is reframed as a deterministic **compile** (merge + template body), not an Anthropic draft. Architecture §67 reframed: the active safety path is LLM-free; the Anthropic classify/extract stages survive only in the preserved email-intake path (Email Triage).
- `safety-portal/brief.md` §8 step 7 (Compile) made **LLM-free / deterministic** explicit (alongside the Option-B per-submission render already in v2); step 8 notes the Email Body is template-seeded, not LLM-drafted.
- **Adversarial Input Handling (Invariant 2) — N/A layers for the active safety path:** Layer 2 (untrusted-content wrapping before an LLM) is **N/A** — no LLM ingestion surface (mirrors the portal's Layer-6-N/A pattern). Layer 4 is now realized as form-definition schema validation (not Anthropic tool-use JSON); Layer 5's extraction-output anomaly check is N/A (no extraction). **The invariant itself is unchanged and still inherited by every workstream**; all LLM-tied layers re-apply on the preserved email-intake path / Email Triage if reactivated. Capability-gating: the Anthropic surface is removed from the safety-reports weekly path.

### §G24.2 — Code-state (verify-before-fix, exec `cf86a9e`)

A ratified **decision**, not yet in code: `weekly_generate.py` at `cf86a9e` **still calls Anthropic** (`generate_weekly_project_report` tool-use, `narrative_summary`, `claude-sonnet-4-6`) and writes `WPR_Pending_Review`. The deterministic-merge rewire (merge the week's per-submission PDFs + template body → `WSR_human_review`, no Anthropic) is part of the in-flight Phase 5 `weekly_*` rewire — not on main. The blueprint encodes the decided LLM-free architecture and records this landed/in-flight boundary.

### §G24.3 — Why deterministic (rationale)

The per-submission PDFs are already render-parity artifacts (Option-B Python renderer, PR #167); a weekly packet is their Sat→Fri merge — a narrative LLM pass added cost, an injection-relevant LLM surface, and review burden without changing the legal artifact. A fixed-template email body + the merged PDF is the customer-facing product; the human edits the body in `WSR_human_review` before the gated send. Removing the LLM from this path also removes Invariant 2's LLM-defense layers as live concerns there (they remain inherited).

## §G25 — 2026-06-05 WSR rewire: Python-side Safety Portal pull model code-complete (PRs #173–#177)

### Summary

Five execution-repo PRs landed 2026-06-05 (all four-part-verified, CodeQL-clean), completing the **Python side** of the Safety Portal pull model. Exec HEAD `025215d` (PR #177 session log). **NOT yet live-verified** — deploy + live smoke = next session. The `~/its` working tree still has the old code on disk (live daemons keep it); the rewired code is on main but not yet pulled to the host.

This section records the non-obvious, non-git-derivable decisions and gotchas for the next CC session.

### §G25.1 — What landed (five PRs)

- **#173 `df3f748` — infra layer:** `shared/portal_client.py` (Worker transport: `get_pending` / `mark_filed`, `F02`-allowlisted); `box_client.upload_bytes` + `get_or_create_folder`; `form_pdf.load_definition` (load a form definition JSON by `formId`); `safety_reports/week_sheet.py` (idempotent Saturday per-(job,week) sheet, columns built via API); `prompts/snippets/invariant-restatement.md` (shared prompt snippet).
- **#174 `bdb9f8f` — consumers:** `intake.process_portal_submission` (parallel to the email path; UUID dedupe via week-sheet; deny-by-default job resolution; payload validation vs Phase-4 form definition; deterministic render; Box filing; amend-supersede; poison-message-safe drain policy) + `safety_reports/portal_poll.py` (fail-closed creds; per-row HMAC verify→reject-never-file; mark-filed receipt; seen-set; daemon-health / heartbeat / watchdog; `GATED` — does NOT run until the deploy session enables it).
- **#175 `49b393d` — `weekly_generate` rewired** to a deterministic compile (Anthropic narrative core RETIRED): gather per-submission PDFs → `form_pdf.merge_pdfs` → ITS-prefixed Box week folder → dual-write the week-sheet Rollup snapshot + one `WSR_human_review` row per (job,week). `wsr_review.py` added; WSR Send-Status picklist registered; orphaned Anthropic prompt + schema deleted.
- **#176 `e628044` — `weekly_send` + `weekly_send_poll` repointed WPR→WSR:** recipients resolved from `ITS_Active_Jobs` at SEND TIME (not from WSR display columns); compiled PDF attached; HELD on empty-TO / missing-PDF; FAILED+retry on transient errors; F22 verify on the driving Send-Now/Scheduled-Send checkbox + approver stamp; `active_jobs.ActiveJob.job_slug` field DROPPED. Watchdog Check-I repointed to WSR (Saturday Week Of). WPR = decommission-by-doc (no live runtime reference).
- **#177 `025215d` — session log + doc-index regen.** Final main SHA = `025215d`.

### §G25.2 — Box filing model (owner override of the brief)

Per-submission PDFs file into the job's **existing category subfolders** (JHAs / Toolbox Talks / Inspection Reports), named `<work_date>-<type>.pdf`. The compiled WSR packet files into an **auto-created `ITS`-prefixed week folder** (`ITS Week of <YYYY-MM-DD>/`) inside the job's Box tree. Operator rule: all ITS-auto-created Box folders start with `ITS` to distinguish them from human-created folders.

`canonical_job_path()` in `box_client.py` remains a **stub** — the brief originally envisioned it for per-job path resolution, but the portal instead uses `project_routing.get_folder_id` (ITS_Project_Routing lookup) + the email-path category subfolder convention. The stub is left in-tree and is NOT called by portal code.

### §G25.3 — Dedupe authority: week-sheet UUID check (survives state-file wipe)

The **week-sheet Submission-UUID column** is the canonical dedupe authority — it is durable (Smartsheet survives a Mac state-file wipe). The `portal_poll` seen-set (in `~/its/state/portal_poll_seen.json`) is a defense-in-depth fast-path that also:

- Re-posts a lost `mark-filed` receipt on a UUID it already processed (idempotent POST, Worker ignores dup).
- One-shot flags a rejected (bad-HMAC) UUID with a `security_flag=True` Review-Queue record and drains it (no repeat CRITICAL spam).

### §G25.4 — Poison-message policy: drain vs retry

`intake.process_portal_submission` returns one of three outcomes:

| Return | Meaning | `portal_poll` action |
|--------|---------|----------------------|
| `processed` / `already_filed` | Success / already handled | POST `mark-filed` → drains from D1 |
| `review_queue` | Permanent refusal (bad payload, no matching job) | POST `mark-filed` → drains WITH a Review-Queue record holding the full payload (operator re-files) |
| `error` | Transient failure (Smartsheet / Box network error) | NOT drained → stays in D1 → re-pulled next cycle |

A permanently-bad message MUST drain (via mark-filed) to avoid infinite CRITICAL spam; the Review-Queue record is the operator's re-file path.

### §G25.5 — CodeQL FP root-cause: tuple-unpacking taint (PR #174)

`py/clear-text-logging-sensitive-data` HIGH was triggered by tuple-unpacking taint. `_resolve_credentials` originally returned `(base_url, bearer_token, hmac_secret)`. CodeQL propagated the `bearer_token` secret-taint onto `base_url` (taint-imprecise for tuples), which rode into the Worker request and appeared in every logged submission field.

**Fix:** refactored to a named-field `_PortalCreds` dataclass (field-sensitive — CodeQL tracks taint per field, not per tuple position) + isolated the HMAC secret to a verification-only code path that never enters the row dict flowing to logs or intake. This is genuine hygiene, not a suppression.

**Reusable pattern:** when a function returns a tuple containing a secret alongside non-secrets, CodeQL may taint all tuple elements. Use a named dataclass so the secret field is tracked in isolation.

### §G25.6 — Scheduled send: window + F22 verify

`Approve for Scheduled Send` rows dispatch only inside `safety_reports.weekly_send.scheduled_send_local` (default `MON 07:00` Pacific, DST-aware via `zoneinfo`). `Send Now` rows dispatch on the next `weekly_send_poll` cycle. F22 (`shared/approval_verification.py`) verifies the **driving checkbox** (Send Now or Scheduled Send, depending on which is True), not just any checkbox on the row.

### §G25.7 — WPR decommission-by-doc (cleanup follow-up)

After the rewire, no live runtime code references `SHEET_WPR_PENDING_REVIEW`. The constant + picklist entry + the catch-up smoke remain until the operator deletes the WPR sheet in Smartsheet. Tracked in exec `docs/tech_debt.md`. No runtime consequence — the sheet is simply orphaned.

### §G25.8 — Deploy-session checklist (next session)

The following must happen before the rewired code is live — the `portal_poll` daemon is GATED until all are done:

1. **Cloudflare:** `wrangler secret put ITS_PORTAL_INTERNAL_TOKEN` + `wrangler secret put ITS_PORTAL_HMAC_SECRET` on the Worker; `wrangler deploy`.
2. **Mac Keychain:** add `ITS_PORTAL_INTERNAL_TOKEN` + `ITS_PORTAL_HMAC_SECRET` via `shared/keychain.set_secret`.
3. **ITS_Config row:** `safety_reports.portal.worker_base_url` = deployed Worker URL.
4. **`portal_poll` launchd job:** load via `scripts/launchd/install.sh`; add `safety_portal_poll` to `TRACKED_JOBS` in `scripts/watchdog.py`.
5. **Pull + reload:** `git -C ~/its pull origin main && git -C ~/its checkout main` so the live daemons pick up the rewired code.
6. **Operator-manual retirement:** unload the retired `safety-intake` launchd job (`scripts/uninstall_safety_intake_daemon.sh`); operator-delete the `WPR_Pending_Review` sheet + `Job Slug` column from `ITS_Active_Jobs` when convenient.
7. **Smoke:** `pytest -m integration` against live Smartsheet/Box; live portal submission → verify D1 queue → verify `portal_poll` pull + file + receipt; verify `weekly_generate` compile → `WSR_human_review` row; verify `weekly_send` send + attachment.

### §G25.9 — week_sheet.py: Saturday-keyed per-(job,week) sheet

`safety_reports/week_sheet.py` creates (idempotently) one Smartsheet sheet per (job_slug, week_saturday) with a stable, predictable title (`<Job Slug> — Week of <YYYY-MM-DD>`). Columns are built via the Smartsheet API at first creation; idempotent on re-run. The sheet is the UUID-dedupe surface AND the read-only Rollup snapshot written by `weekly_generate`. UUID column is TEXT (not AUTO_NUMBER — the AUTO_NUMBER constraint from §6 applies here too; the UUID is a portal-supplied string, not a system counter).

## §G26 — 2026-06-07 Safety Portal deploy-session reconciliation (exec PRs #178–#189)

### Summary

Blueprint-side and execution-side reconciliation capturing the **deploy-session + Phase-7 batch** — exec PRs **#178–#189, all merged; exec main HEAD `f3ad814`** (PR-H #185 admin route merged last, after its 2 CodeQL `py/clear-text-logging` FPs were operator-dismissed). §§26.1–26.9 were verified against exec code by a 13-agent verification pass; §26.10 (PR-I/J/K) + §26.11 (PR-H merge roll-forward) are the closures. Several ledger statements were corrected, flagged ⚠. Blueprint docs reconciled this cycle: safety-portal mission v2→**v3** + brief v2→**v3**; safety-reports mission v5.4→**v5.5** + brief v6.4→**v6.5**; Operational Standards v17→**v18** (new §§45–49); Handover Plan v8→**v9** (the portal-user admin-CLI runbook, now that PR-H merged); this §G26; the email-triage forward-reference; info-gap; a 2026-06-07 planning session log. Workstream/reference docs are frontmatter-versioned (not git-tagged); doctrine tags this cycle: `operational-standards-v18`, `handover-plan-v9`.

### §G26.1 — The PR ledger (#178–#189, all merged; exec main `f3ad814`)

| PR | Slug | What landed | Exec SHA |
|---|---|---|---|
| #178 | — | UI: drop stray "+ Add row" button | `e7b564d` |
| #179 | PR-A | `portal_poll` launchd plist + `install.sh` wiring + watchdog Check-C | `f858334` |
| #180 | PR-B | `wrangler.jsonc` → live **mirror** D1 (`924f142b-…`, `its-safety-portal-db`, ENAM) | `df549df` |
| #181 | PR-C | week-sheet filing → `WORKSPACE_SAFETY_PORTAL` surface (find-or-create) | `361bbb9` |
| #182 | PR-D | `ITS_Active_Jobs` → D1 sync (`POST /api/internal/sync` + portal-poll push) | `053d627` |
| #183 | PR-E | F22 approval authority = workspace membership (allowlist retired) | `595a469` |
| #184 | PR-F | rendered PDFs attached inline on Submission/Rollup/WSR rows | `b320a24` |
| #186 | PR-G | Compile-Now Box-409 → version-on-conflict (packet path) | `34e271d` |
| #185 | PR-H | Phase 7 admin route + session revocation (merged last, after CodeQL FP dismissal) | `f3ad814` |
| #187 | PR-I | Smartsheet sheet styling (`apply_column_styles`; `_formats` meta-key; `WEEK_SHEET_STYLES`; one-time styling pass) | `53c27ac` |
| #188 | PR-J | `wrangler.jsonc` custom domain `safety.evergreenmirror.com` (NOT deployed) | `6c1993d` |
| #189 | PR-K | `safety_naming.py` shared naming + config-gated Box mirror tree (`ROOT→per-job→per-week`) | `ecb06d9` |

### §G26.2 — Deploy: mirror/validation, NOT the Evergreen cutover

`wrangler.jsonc` binding `DB` points at the operator's **mirror/validation** D1 `its-safety-portal-db` (`database_id 924f142b-c812-49fd-a262-2eb6fb34fe95`, region ENAM); the all-zeros placeholder is gone (PR-B). The Cloudflare **account** is supplied at deploy via `CLOUDFLARE_ACCOUNT_ID` (no committed account id; "account = mirror" is asserted by the D1 comments + the `safety.evergreenmirror.com` custom-domain choice, not a hard-coded field). **"Live" = the mirror is functional + admin-controllable + edge-case-proven — NOT the Evergreen cutover.** Production (`evergreenrenewables.com`, Evergreen-owned fresh Cloudflare account, `safety.evergreenrenewables.com` via subdomain NS-delegation) remains a separate later step (unchanged from §G23.2). `portal_poll` is now a real launchd daemon (`org.solutionsmith.its.portal-poll`, `StartInterval` 60 s, `RunAtLoad=false`, Background, send-free), watchdog Check-C marker `safety_portal_poll.last_run` on a **5-min** window — **this closes §G25.8 item 4** (TRACKED_JOBS registration was a deferred item, done in PR-A; a stale "deferred" comment lags in `portal_poll.py:111-113`, exec tech-debt).

### §G26.3 — Secret map (verified as-built; corrects the v2 brief names)

Worker Secret ↔ macOS Keychain mirror (byte-equal where mirrored):

| Worker Secret | Keychain | Purpose | Unset |
|---|---|---|---|
| `PORTAL_INTERNAL_API_TOKEN` | `ITS_PORTAL_INTERNAL_TOKEN` | `/api/internal/*` bearer (drain, mark-filed, sync) | 401 |
| `HMAC_PAYLOAD_SECRET` | `ITS_PORTAL_HMAC_SECRET` | per-submission HMAC | 503 (fail-closed) |
| `SESSION_SIGNING_SECRET` | Worker-only (no mirror) | session cookie | — |
| `PORTAL_ADMIN_API_TOKEN` | `ITS_PORTAL_ADMIN_TOKEN` | **PR-H #185 (landed)** — admin route, privilege-separated from the poller token; set byte-equal at activation | 401 |

⚠ The v2 safety-portal brief named these `HMAC_SECRET` / `INTERNAL_BEARER_TOKEN` — **stale**; the as-built names are above (v3 corrected). Send-leg seeds are **`ITS_Config` Smartsheet rows** (not files): `safety_reports.weekly_send.from_mailbox` (`safety@evergreenmirror.com`), `.scheduled_send_local` (`"MON 07:00"`, Pacific), `.polling_enabled` (`true`); the `.polling_enabled` suffix is per-daemon (`weekly_send` / `portal_poll` / `intake`).

### §G26.4 — Box filing: as-built vs the planned PR-K mirror ⚠ (ledger corrected)

⚠ The ledger described the Box-mirrors-Smartsheet model as if decided/known; it was **not in code at `34e271d`**. **As-built at `34e271d`:** per-submission PDF → existing email-path category subfolder (`PORTAL_FORM_CATEGORY` → `BOX_SUBPATH_BY_CATEGORY`, suffix-on-409); packet → per-week `ITS`-prefixed folder with version-on-conflict.

**PR-K (`ecb06d9`) landed:** the Box mirror-tree model is now in code, config-gated. When `safety_reports.box.portal_root_folder_id` is set, **both** per-submission and packet filings use the new `ROOT→per-job→per-week` tree via `safety_naming.py` naming + `box_client.get_or_create_folder`. Category subfolders are dropped in the new path. The legacy path remains for email-intake. The **config key is `portal_root_folder_id`** (not `safety_portal_root_folder_id`); the planned folder id `388017263015` in the ledger was never set in code — the operator creates the Box root folder and provides the actual id at activation.

### §G26.5 — F22 approval authority = workspace membership ⚠ (owner edge case corrected)

PR-E (#183): the F22 send-gate predicate (`approval_verification.verify_approval`, cell-history modifier match) is **unchanged**; the **source** of the authorized set moved from the `safety_reports.authorized_approvers` ITS_Config allowlist (seed **removed** 2026-06-06; no live reader) to **live workspace membership** — `smartsheet_client.list_workspace_share_emails(WORKSPACE_SAFETY_PORTAL)` (`GET /workspaces/{id}/shares?includeAll=true`, lowercased USER-share emails, any access level), via `weekly_send_poll._load_authorized_approvers`. Empty set → `EMPTY_ALLOWLIST` → fail-closed. **Mechanism gone; naming survives** (`_load_authorized_approvers` resolves from shares now; `parse_authorized_actors` retained-unused; tombstone comments + historical logs). Edge cases: **(a) group-share expansion is a known pre-prod gap** — GROUP shares carry no email → excluded → a group-only share fail-closes (mitigation: share with individuals; documented in helper docstring + cutover checklist + a unit test). **(b) ⚠ workspace-OWNER inclusion is NOT handled in code** — no owner-injection, no access-level filter; whether the owner appears in the set is an **unstated dependency on the Smartsheet `/shares` response**. The ledger framed owner-inclusion as a recorded edge case; it is not — record it as an open question, not a guarantee.

### §G26.6 — Email-intake path retained as the Email-Triage seed (load-bearing)

The clean break retired **only** the safety email *input*, not the infrastructure. **Resident in `main`, do not decommission:** preserved-**dormant** (no live caller, parses, not tombstoned) = `week_folder.py` (+ `FIELD_REPORTS_FOLDER_BY_PROJECT` consumer), `intake.process_message` + Graph fetch/classify/extract stages, `graph_client.py` / `untrusted_content.py` / `header_forgery.py`; **actively LIVE shared infra** (reused by the *portal* path, so doubly load-bearing) = `project_routing.get_folder_id` + `defaults.BOX_PROJECT_FOLDERS` (the Box-folder routing with its deliberate hardcoded fallback — ⚠ distinct from `active_jobs`, which has none) and the report-category machinery (`BOX_SUBPATH_BY_CATEGORY` / `VALID_CATEGORIES` via `PORTAL_FORM_CATEGORY`). **Tombstoned (only one):** `intake_poll.py` (`NotImplementedError`, PR #171). Rationale (recorded in `intake_poll.py`'s own docstring + here + the email-triage forward-ref): the Graph plumbing is workstream-agnostic and seeds the committed **Email Triage** workstream — so no future session decommissions it as "clean-break cleanup."

### §G26.7 — Doctrine generalizations this cycle (Op Stds v18, §§45–49)

Five as-built patterns generalized into Operational Standards v17→**v18** (co-resolution bump; new §§): **§45 find-or-create-not-strand** (portal artifacts auto-provision; transient failure re-pulls, permanent surfaces to the Review Queue — never a silent write-to-nowhere; from PR-C/PR-K); **§46 workspace-membership = approval authority** (the F22 mechanism + the two edge cases above); **§47 Box version-on-conflict** (deterministic-name re-uploads → new Box version; distinct-document uploads keep suffix-on-conflict); **§48 CodeQL false-positive handling** ⚠ (per-alert dismissal with a recorded reason + a genuine-fix-not-blanket-suppression rule; the dismiss-block hook is **agent-scoped** in `codeql-fp-triager.md` frontmatter, **NOT** in `settings.json` which wires only `block-dangerous-git` globally — the ledger's "live dismiss-block" is real but agent-scoped; the per-alert/inline-comment/never-per-file-suppress rule was **previously uncodified** and is newly written, not as-built); **§49 preservation-for-future-workstream** (the §G26.6 email-retain rationale generalized — extends §14 preservation-over-refactor). See the doctrine for the canonical text.

### §G26.8 — Confirmed invariants (grounded this cycle)

- `active_jobs` is the **single source of truth** for the portal job set — **no hardcoded fallback** (read miss → empty set → portal-poll skips the push, never wipes the dropdown). Contrast `project_routing`/`BOX_PROJECT_FOLDERS`, which deliberately keeps a fallback.
- **Recipient resolution** = sheet-sourced at send time (`active_jobs.get_job`; TO = Safety Reports Contact, CC 1–5) + **surface-not-strand**: unresolvable job or empty/invalid TO → `Send Status = HELD` + WARN, excluded from poller re-dispatch — never a silent send or crash.
- `shared/safety_week.py` is the **single Saturday→Friday** week helper (`_SATURDAY=5`, walk-back-to-Saturday), used by intake / weekly_generate / week_sheet / watchdog — ⚠ distinct from the Monday-ISO `week_folder.py` scaffold (different concern; do not conflate).
- Inline-PDF attaches (PR-F) are **supplementary + best-effort**; **Box stays SoR** (Box-link cells unchanged, compile still reads PDFs from Box; attach failure → WARN `row_pdf_attach_failed`, never fails the filing/compile).

### §G26.9 — Phase 7 admin (PR-H #185): LANDED on exec main `f3ad814` (byte-equal to the verified branch)

Merged into `main` (squash-merge; the 5 Phase-7 files are byte-identical to the verified branch commit `4916a57`): bearer-gated `POST/GET /api/internal/admin/users[/reset|/disable|/enable]` under `requireAdminToken` + the **separate** `PORTAL_ADMIN_API_TOKEN` (privilege separation); Mac CLI `portal_admin.py` with verbs **`add-user`/`reset-password`/`disable-user`/`enable-user`/`list-users`** (⚠ not the literal `provision/reset/disable/enable/list` of the ledger); backend `bcrypt.hash(pw,10)` (plaintext never stored/logged; the CLI prints status + known args only); `requireSession` per-request `SELECT disabled FROM users WHERE username=?` → `401 revoked` (fail-closed) = server-side session revocation; migration `0006_add_user_disabled.sql` (`disabled INTEGER NOT NULL DEFAULT 0`) with an **order dependency** (apply to live D1 BEFORE the reading Worker deploys, else every session 401s). **The merged code is live-inert until the 3-part activation gate:** (1) set `PORTAL_ADMIN_API_TOKEN` (Worker) + `ITS_PORTAL_ADMIN_TOKEN` (Keychain) byte-equal; (2) apply 0006 to live D1 before redeploy; (3) redeploy the Worker. The admin-CLI is the successor-operator's portal user provision/deprovision runbook — now codified in **[Handover Plan v9](../doctrine/handover-plan.md) Step 8**.

**PR-H CodeQL block (resolved):** CI GREEN except 2 `py/clear-text-logging` FPs (`portal_admin.py:52` + `:148`) — interprocedural taint from bearer token through `admin_request`'s return value; refactor cleared 1 of 3 (stopped echoing raw response dict); remaining 2 unfixable without contorting correct code. Resolution (a clean live exercise of the §48 doctrine): operator ran `codeql-fp-triager` → applied the 2 dismissals in the GitHub UI (CC hook-blocked) → PR-H merged at `f3ad814`. Not one of the three auto-dismiss patterns; `codeql-fp-triager` evaluated it explicitly. The exec-side info-gap captured the pattern (interprocedural taint through a shared request fn on an operator CLI) + the merge-serialization gotcha (require-up-to-date-branch serialized the #185–#189 batch).

### §G26.10 — PR-I/J/K landed (exec HEAD `ecb06d9`, 2026-06-07)

The three PRs that were "in flight, not yet opened" at §G26.1 write time all landed this session:

**PR-I (#187 `53c27ac`) — Smartsheet sheet styling:**
- `smartsheet_client.apply_column_styles(sheet_id, col_specs)` — post-create column width + format. Key SDK-vs-Live finding: **column FORMAT string MUST be set via the model ATTRIBUTE** (`col.format = "..."`) not the dict constructor (silently dropped; column width is safe either way).
- `_resolve_cells` additive `_formats` meta-key: per-cell format at write time (skip `_`-prefixed keys, attach `Cell.format`). Rows without `_formats` are byte-identical. Enables Status-cell coloring as a substitute for UI-only conditional-format rules.
- Palette from `GET /2.0/serverinfo` `.formats.color`: index 38 = `#237F2E` (dark green), 7 = `#E7F5E9` (light green), 18 = `#E5E5E5` (gray).
- `scripts/style_safety_portal_sheets.py` one-time pass — ran live: 3 static sheets (`ITS_Active_Jobs`, `ITS_Forms_Catalog`, `WSR_human_review`) + 7 week sheets.
- `week_sheet.WEEK_SHEET_STYLES` constant (widths + bold dark-green primary + status-cell coloring Active=green/Superseded=gray) applied at `ensure_week_sheet` time going forward.

**PR-J (#188 `6c1993d`) — custom domain:** `wrangler.jsonc` `routes` entry with `custom_domain: true` for `safety.evergreenmirror.com`. NOT deployed — operator activates via Cloudflare dashboard custom-domain add + `npm run deploy`.

**PR-K (#189 `ecb06d9`) — Box schema mirrors Smartsheet schema:**
- `safety_reports/safety_naming.py` — single source of truth for Box + Smartsheet naming (`job_folder_name`, `week_label`, `CFG_BOX_PORTAL_ROOT` key name). Both `intake` and `weekly_generate` import from it; `week_sheet` delegates to it.
- Config-gate pattern: `safety_reports.box.portal_root_folder_id` in ITS_Config — unset/empty → legacy path (current behavior unchanged); set to the root folder ID → new `ROOT→per-job→per-week` Box mirror tree. **Merging and pulling is inert** until the operator creates the Box root folder and sets the config value.
- `intake._resolve_portal_box_folder` + `weekly_generate._ensure_its_week_folder` both have the gated branch. Legacy `project_routing`/`BOX_PROJECT_FOLDERS` path preserved for the email-intake dormant path.
- Live SDK-vs-Live nesting round-trip verified.
- Pre-activation sandbox filings are orphans under the old category subfolders — tracked in `docs/tech_debt.md` ("Pre-mirror-tree portal Box filings are sandbox orphans").

**Live actions this session:** one-time styling pass (10 sheets); JOB-000008 "ZZ Portal Proof" DEACTIVATED (Active → Inactive in ITS_Active_Jobs).

### §G26.11 — PR-H merged; blueprint rolled forward to exec main `f3ad814` (2026-06-07 close)

The §G26.1–§G26.10 capture above was written when PR-H (#185) was still OPEN at `ecb06d9`. PR-H then merged at **`f3ad814`** (the 2 `py/clear-text-logging` FPs were operator-dismissed per §48; CLI verbs `add-user`/`reset-password`/`disable-user`/`enable-user`/`list-users`, byte-equal to the verified branch — see §G26.9). So **all four deploy-batch PRs (#185 PR-H, #187 PR-I, #188 PR-J, #189 PR-K) are merged**, and the blueprint's `last_verified_against` for the safety docs + Op Stds + memory-archive is **`f3ad814`**. Net activation state: nothing is live yet — three operator **activation tracks** remain, all merged-but-inert: **(a) admin route** (set byte-equal admin tokens, apply migration 0006 to live D1 *before* redeploy, redeploy); **(b) Box mirror tree** (create the root Box folder, set `ITS_Config` `safety_reports.box.portal_root_folder_id`); **(c) custom domain** (`wrangler deploy` / dashboard add). PR-H merging realized the deferred Handover trigger: **Handover Plan v8 → v9** now carries the full successor-operator portal-user provision/deprovision runbook (Step 8). The earlier §G26.4 "as-built at `34e271d`" lines are retained as the pre-PR-K historical baseline.

## §G27 — 2026-06-08 Safety Portal mirror activation (operational session; exec HEAD `f3ad814` unchanged)

### Summary

The Safety Portal is **fully activated and live-validated on the mirror/validation environment** (`evergreenmirror.com`, Cloudflare account `sethsmithusmc`). This was a pure **operational session** — zero new commits to `~/its` (exec HEAD stays `f3ad814`). All three activation tracks from §G26.11 are now complete. End-to-end submit → pull → intake → Box → WSR-staged proven; a **real unattended timed send confirmed** (Mon 07:12 PT, Graph, `safety@evergreenmirror.com` → `seth@solutionsmith.org`, SENT + stamps, F22-verified, ITS_Errors forensic clean). **Next milestone: Evergreen production cutover.**

### §G27.1 — Activation sequence (order-of-operations; migration 0006 MUST precede deploy)

The three tracks were executed in this order:

1. **Admin route activation** (track a):
   - Applied migration `0006_add_user_disabled.sql` to the **live** D1 (`wrangler d1 migrations apply its-safety-portal-db --remote`) — MUST precede the Worker deploy. The reading Worker's `requireSession` does a `SELECT disabled FROM users`; without the column, every session 401s immediately after deploy.
   - Set `PORTAL_ADMIN_API_TOKEN` via `wrangler secret put PORTAL_ADMIN_API_TOKEN`.
   - Set `ITS_PORTAL_ADMIN_TOKEN` in Keychain via `security add-generic-password -U -a "$USER" -s ITS_PORTAL_ADMIN_TOKEN -w VALUE` (argv form — see §G27.3 Keychain gotcha).
   - `npm run deploy` (Cloudflare); confirmed admin routes `/api/internal/admin/*` live (return 401-not-404 without token).
   - `portal_admin list-users` + `portal_admin add-user seths PASSWORD` → user provisioned.
   - **Session revocation proven**: disabled a user via `portal_admin disable-user seths`; the user's existing session then returned `401 revoked` on `GET /api/jobs` (requireSession intercepts at the per-request `SELECT disabled FROM users` check).
   - Re-enabled the user for continued proof.

2. **Box mirror tree** (track b):
   - Created `ITS_Safety_Portal` Box root folder (owner: `seths@evergreenmirror.com`, collaborator: `daniels@evergreenmirror.com` editor).
   - Box folder ID: **`388017263015`**.
   - Set `safety_reports.box.portal_root_folder_id = 388017263015` in ITS_Config (Smartsheet row).
   - Verified `get_or_create_folder` find-or-create logic via `portal_poll` drain cycle: per-job and per-week subfolders auto-provisioned; filed PDFs resolved to the `ROOT → job → week` tree.

3. **Custom domain + worker_base_url repoint** (track c):
   - `npm run deploy` (run again after migration + secrets were in place).
   - The `custom_domain: true` route in `wrangler.jsonc` provisioned `safety.evergreenmirror.com` as a Cloudflare-hosted zone and simultaneously **disabled the `*.workers.dev` URL** (wrangler warning: "workers_dev will be disabled by default"). The old workers.dev URL immediately returned Cloudflare `error 1042` ("No Workers script was found for this host on workers.dev").
   - ~15 `portal_pending_fetch_failed` ERROR rows wrote to ITS_Errors from `portal_poll` before diagnosis.
   - Fixed by repointing `safety_reports.portal.worker_base_url` in ITS_Config to `https://safety.evergreenmirror.com` (the new canonical base URL).

4. **Proof setup**: JOB-000008 "ZZ Portal Proof" set Active; `Safety Reports Contact Email = seth@solutionsmith.org`; `scheduled_send_local = "MON 07:00"`.

### §G27.2 — Live daemon state after activation

| Daemon | launchd job | Interval | Status |
|---|---|---|---|
| `portal_poll.py` | `org.solutionsmith.its.portal-poll` | 60 s | LIVE, heartbeat OK |
| `weekly_send_poll.py` | `org.solutionsmith.its.weekly-send` | 900 s | LIVE, heartbeat OK |
| picklist-sync | `org.solutionsmith.its.picklist-sync` | not loaded | NOT loaded |
| watchdog | `org.solutionsmith.its.watchdog` | not loaded | NOT loaded |
| weekly-generate | `org.solutionsmith.its.weekly-generate` | not loaded | NOT loaded |
| safety-intake | retired/tombstoned | — | RETIRED (operator unloads manually) |

`portal_poll` polling_enabled + `weekly_send_poll` polling_enabled both `true` in ITS_Config.

### §G27.3 — Keychain gotcha: bare `-w` prompts TTY in interactive shell

`security add-generic-password -U -a "$USER" -s NAME -w` — the **bare `-w` flag** (no value token following it) prompts the controlling TTY for a password and retype. In an interactive shell session (Warp, Terminal, zsh), **piped stdin is ignored**; only what is typed at the TTY prompt is stored. A 6-character garbage value was silently written this session because the operator used `echo VALUE | security add-generic-password -U -a "$USER" -s NAME -w`, trusting that stdin would be read — it was not.

**Root-cause:** the Keychain was set to a garbage value → `portal_admin list-users` received a 401 → diagnosed by comparing the Worker token against the Keychain read-back.

**Fix:** always use the argv form: `security add-generic-password -U -a "$USER" -s NAME -w VALUE` where VALUE is the next token on the command line. The `shared/keychain.set_secret` function (subprocess, no TTY, stdin explicitly written) is unaffected — this is a **manual shell use only** gotcha.

### §G27.4 — Scheduled-send window semantics (live-verified)

`weekly_send_poll._is_scheduled_window` logic: the window is **open iff today's Pacific weekday == configured weekday AND now >= configured time**, with **no upper-bound closure**. "MON 07:00" means all of Monday from 07:00 onward. An `Approve for Scheduled Send` row checked on Sunday or Monday before 07:00 waits; checked Monday after 07:00 it dispatches on the next poller cycle. `Send Now` bypasses the window entirely (dispatches any cycle). The scheduled-send spec is read live each cycle (hot-reloadable without daemon restart).

**Live-confirmed (2026-06-08):** operator checked `Approve for Scheduled Send` on Sunday; on Monday 07:12 PT the `weekly_send_poll` poller dispatched the row → Graph send confirmed, `SENT` + `Approved By / Approved At` stamped (poller-stamped, not manually), F22 verify passed; ITS_Errors clean.

### §G27.5 — Three tech-debt findings (now in exec `docs/tech_debt.md`)

1. **`validateUser` does not gate on `users.disabled`** — `/api/login` (`auth.ts:50-67`) selects only `id, username, password_hash`; `disabled` is never checked. A disabled user with a valid password can still mint a session cookie. The cookie is useless (every downstream endpoint 401s at `requireSession`), so there is **no capability bypass** — the security boundary holds. But login appears to succeed (misleading UX + defense-in-depth gap). Proposed fix: add `disabled` to the `validateUser` SELECT; return `null` when `row.disabled`. ~15 min + a test. `[OPEN 2026-06-08]`.
2. **`custom_domain` route disables `workers.dev` URL on deploy (Cloudflare `error 1042`)** — see §G27.1 track c. Decision: custom-domain-only end-state is fine for the mirror and future Evergreen deployment. If both routes are ever needed, add `"workers_dev": true` to `wrangler.jsonc`. `[OPEN 2026-06-08]`.
3. **`scheduled_send_local` not in `seed_its_config.py` + silent fail-open on malformed value** — row was added manually to the mirror; a fresh tenant build would lack it and silently fall back to the `DEFAULT_SCHEDULED_SEND_LOCAL` constant (functionally OK, but undocumented in the seeder). A malformed value is coerced to MON 07:00 with no log. `[OPEN 2026-06-08]`.

### §G27.6 — Named follow-ups (not done this session)

- **Full edge-case matrix** — each scenario is proven by design (drain policy, HMAC verify, UUID dedupe, inactive-job routing, amend-supersede, empty-week-still-writes, Friday-skip, empty-TO HELD, F22 non-member, live-contact-wins, locked footers) but has NOT been exercised live. Separate session recommended before production cutover.
- **Blueprint doctrine commit** — separate `~/its-blueprint` session required; the blueprint docs should be rolled forward through `f3ad814` activation (safety-portal mission/brief `last_verified_against` + CLAUDE.md daemon-state table update). Not done here (blueprint is clean at `0e85a1a`; the exec CLAUDE.md/tech_debt changes are uncommitted working-tree in `~/its`).
- **Revert ZZ Portal Proof to Inactive** — once confidence in the pipeline is sufficient; keeps the proof row available without generating weekly send traffic.
- **Worktree + branch cleanup** — `~/its-portal-fix*` worktrees + merged branches (`branch -D`); operator manual step.
- **Load remaining daemons** — picklist-sync, watchdog, weekly-generate not yet loaded on the host.

## §G28 — 2026-06-08 Blueprint reconciliation pass (Smartsheet-structure reference + doctrine-citation sweep; brief premises corrected)

A blueprint-native reconciliation session driven by a chat brief whose current-state premises were **substantially stale** (verified via `brief-validator` + `doc-reconciliation-auditor` + a live Smartsheet MCP browse against exec `21bd909`). Recorded so a future session does not re-trust the stale premises. Re-scoped with the operator to the verifiable subset; **no demo content touched, no doctrine body edited, no git tag.**

### §G28.1 — Brief premises that did NOT hold (corrected)

- **"All demo Smartsheet architecture is abandoned"** — FALSE against live state. `WORKSPACE_DEMO = 4129485730670468` ("Forefront Portfolio — ITS Demo") is **live in exec `sheet_ids.py:22` ("customer-facing")**, with the Bradley/Brimfield/Huntley/Rockford **project folders under it** (Forefront / 01 — Active Projects), and Op Stds **§24 (doctrine)** documents it. Abandoning it blueprint-only would manufacture blueprint↔exec drift. **Re-scoped:** the abandonment is a cross-repo decision (exec `sheet_ids.py` + Op Stds §24, both Scope-OUT) that must land in exec/doctrine first/together — NOT a blueprint-only edit. Demo content left untouched.
- **Phantom "old Safety Portal workspace ID `4021545954764676`"** — appears **nowhere** in either repo OR in the live Smartsheet workspace list. Nothing to sweep. The correct ID `194283417429892` was already in the blueprint (6 files) + exec `sheet_ids.py:34`.
- **"Abandoned" Template Master `3333320395253636` + Demo Seed `685696395569028`** — exist as **live OWNER Smartsheet workspaces** ("Evergreen Portfolio Template (Master)" / "(Demo Seed)") but appear in **no code**; not abandoned.
- **"Permissions v5"** — it is **v6** (`references/permissions.md`, a reference doc, not doctrine).
- **`ITS_Active_Jobs` "spec/unbuilt" / WSR-WPR / safety-portal "to-build"** — all already correct: `ITS_Active_Jobs` built everywhere (`6223950341164932`, 2026-06-03); `WSR_human_review` supersession already reconciled (§G27 + handoff v8); safety-portal already v3.1 as-built (§G27).

### §G28.2 — Live `ITS –– Safety Portal` workspace structure (verified 2026-06-08, exec `21bd909`)

Captured in new reference `references/smartsheet-structure.md` (v1, ID-free per repo `CLAUDE.md` — names + `sheet_ids.py` constants only). Topology (workspace `194283417429892`):
- `00_Safety Portal` (`FOLDER_SAFETY_PORTAL`) → `ITS_Active_Jobs` (`SHEET_ACTIVE_JOBS`) + `WSR_human_review` (`SHEET_WSR_HUMAN_REVIEW`).
- **`00_Form Catalog`** (separate folder) → `ITS_Forms_Catalog` (`SHEET_FORMS_CATALOG`). **Discrepancy resolved:** the exec `sheet_ids.py` `FOLDER_SAFETY_PORTAL` comment ("holds ITS_Active_Jobs + ITS_Forms_Catalog + WSR_human_review") is **stale** — Forms_Catalog has its own folder. The brief's companion structure was right; the code comment is outdated. (Flagged for an exec comment refresh.)
- Per-job folders **Bradley 1/2, Brimfield 1/2, Huntley, Rockford + ZZ Portal Proof** — created in this workspace by `find-or-create` (distinct from the like-named `FOLDER_PROJECT_*` under `WORKSPACE_DEMO`). Each holds per-week submission sheets named `"<Job> — week of <Saturday-date>"` (e.g. `ZZ Portal Proof — week of 2026-06-06`).
- `ITS_Config` (`SHEET_CONFIG`) lives in `ITS — System`, not the Safety Portal workspace.
- **Live workspace inventory (9):** Evergreen Portfolio Template Demo Seed `685696395569028` · Template Master `3333320395253636` · Forefront Portfolio — ITS Demo `4129485730670468` · **Forfront IL portfolio `2228567565199236`** (ADMIN, in no code — purpose unknown, flagged) · ITS –– Safety Portal `194283417429892` · ITS — Archive `5528280611743620` · ITS — Human Review `8561891980142468` · ITS — Operations `7217130472007556` · ITS — System `680592632244100`.

### §G28.3 — Doctrine-citation currency sweep

27 **present-tense** doctrine-version citations updated across 10 blueprint docs (Op Stds → **v18**, Handover → **v9**): `safety-reports/{brief,mission}.md`, `references/{daemon-health-schema,project-organization,extended-workstreams}.md`, and the frozen Phase-2/3 planning docs (`purchase-orders`, `subcontracts`, `ai-employee-capabilities` `{brief,mission}.md`, which were at Op Stds v5). **Provenance preserved** (NOT swept): all "What Changed"/changelog blocks, "new in v8"/"revised in v8"/"introduced in vN" origin-pins, `daemon-health` build-rationale §-cites (only its `Authority:` line updated), the `:128` "acknowledged in Op Stds v17" origin-pin, and **all of `email-triage/{mission,brief}.md`** (a coherent self-documented v8/v13 snapshot — left whole; recommend a dedicated currency touch). Judgment calls: `project-organization.md`'s canonical-doc-set block was fully refreshed (FM v11 / Op Stds v18 / V&R v9 / Handover v9 / Excellence v4) for internal coherence; FM/V&R/Excellence citations **elsewhere** were left per the brief's "don't churn" (a handful of stale `FM v4`/`v8` inheritance-boilerplate cites remain — flagged for a follow-up FM-currency pass).

### §G28.4 — Process + named follow-ups

- Process: blueprint CI = `lint_frontmatter` + `lint_crossrefs` only (no tests) — a "four-part verify" reduces to "those two lints pass" for a blueprint PR. Contacts roster (Finkhousen=Sr PM, Jechiah Stephens=Head of Eng, Tiffany Montastirsky=Head of Permitting; CEO = **Jacob** Stephens) is **exec-only** (`~/its/docs/operations/cutover_checklist.md`); NOT added to the blueprint (Customer-0 data per `CLAUDE.md`).
- **Flagged (not acted on):** (1) demo-abandonment as a cross-repo exec+doctrine decision; (2) exec `sheet_ids.py` `FOLDER_SAFETY_PORTAL` comment refresh (Form Catalog split); (3) the residual stale `FM v4/v8` inheritance-boilerplate cites; (4) email-triage currency touch (v8/v13 → current); (5) `Forfront IL portfolio` workspace `2228567565199236` — unknown purpose, in no code.

## §G29 — 2026-06-08 Safety Portal Admin Dashboard (Phase 1) + security hardening + Phase-2 form-editor design (exec `f3ad814` → `b7bad5a`)

Exec session postdating §G27/§G28. The Safety Portal gained an **admin dashboard**, a **security hardening pass** (with a live incident), and a fully-designed-but-not-built **Phase-2 form editor**. Exec PRs #193–#202 merged (each four-part verified) + exec docs #199.

### §G29.1 — Admin Dashboard Phase 1 (built + live on the mirror)
- **Role model:** migration **0007** `users.role` + `audit_log`; per-request `requireRole('admin')` reads role FRESH from D1 (demotion is immediate); session-gated `/api/admin/*` (distinct from the bearer `/api/internal/admin/*` CLI). **0008** `submissions.actor_username`/`submitted_as`.
- **Two-tab admin SPA** (behind `requireRole`): "Submit a form" (+ admin-only **"filled out as"** submit-as with dual-attribution; the canonical HMAC payload + `/api/internal/pending` columns are **UNCHANGED** → portal_poll/intake/downstream byte-unchanged) | "Accounts" (create / edit-login / change-role / delete). **Last-admin guard is ATOMIC** (count-subquery inside the demote/delete WHERE + a `changes()`-conditional audit row).
- **Worker CI born:** the `portal` job (`@cloudflare/vitest-pool-workers`, real workerd+D1, tsc×3) — the FIRST CI coverage of the Worker TS (the Python `test` job never touched it).
- Admins `stephens.jacob` + `finkhousen.ben` provisioned (role=admin). PRs: **#193** confirmation-shows-the-JOB (all users) · **#194 (PR-L)** blank-form Box archive + `form_pdf.render_blank_fillable` + `scripts/generate_form_archive.py` · **#195** role model + Tab2 + CI · **#197** submit-as.

### §G29.2 — Adversarial audit (live) + 11-finding hardening (#198) + the asset-500 INCIDENT (#200) + CSP
- Audit (Workflow, 6 dimensions): posture SOUND — injection 0/4 (bound params), no auth bypass (HMAC cookie unforgeable), no priv-esc, **the atomic last-admin guard survived a live TOCTOU race**. 12 findings, none critical.
- Hardening **#198** closed 11: null/non-object body→400 on all 12 handlers + global `app.onError`; `values:[]`→400; security headers (XFO:DENY/nosniff/Referrer/HSTS + Cache-Control:no-store on /api/*) via `run_worker_first:true`; UNIQUE-race→409; delete/demote 404-vs-409.
- **INCIDENT + new doctrine-grade gotcha:** #198 shipped Hono `secureHeaders()`, which mutates response headers in place. **`c.env.ASSETS.fetch()` responses have IMMUTABLE headers** → under `run_worker_first:true` it THREW → `app.onError` → **500 on every static asset + the SPA document** (only Hono-built /api/* survived — deceptive partial failure). Root cause: **`vitest-pool-workers` does NOT serve the built assets**, so the unit suite (42 green) never hit the asset path. **Hotfix #200** reconstructs each response with a mutable Headers copy. **RULE: verify any asset/document path with `wrangler dev` + curl, never vitest alone** (the mocks-pass/live-fails class).
- **CSP:** shipped Report-Only (#198) → flipped **ENFORCING (#201)** after a Playwright browser smoke (admin login → dashboard → JHA form WITH signature capture → 0 violations) → finding #2 actually closed. The Cloudflare Web Analytics beacon (`static.cloudflareinsights.com`) was then CSP-blocked → allowlisted in script-src/connect-src (**#202**). Live Worker `80ec62ea`; console clean.
- Deferred audit **#7** (session-epoch: logout is client-only, a captured cookie stays valid to `iat+90d`; `requireSession` checks only `disabled`) → Phase-2 session hardening.
- **CC deployed the hotfix + CSP-flip + beacon-fix itself** (auto-mode permitted live `npm run deploy`, unlike the earlier classifier-blocked D1 migration).

### §G29.3 — Phase-2 Form Editor + Session Hardening (DESIGNED, not built)
Grilled + red-teamed (Workflow, 46 findings). Exec design brief on exec main: **`docs/phase2_form_editor_and_session_hardening_brief.md`** (Part B design + Part C red-team revisions). Load-bearing decisions:
- **Git is the source of truth + a git-committed catalog manifest** (active-set / current-version-per-form / parent-variant / order); renderers byte-unchanged. **Files are append-only on disk; the manifest is the ONLY active-set gate** — Edit/retire/delete flip the manifest, never delete a `.json` → every historical `form_code` resolves forever.
- **4 ops:** create-from-blank · **Edit** (version-bump + auto-swap-PM-facing + auto-retire-old; `-vN` admin-visible; REPLACE) · **Add-version** (clone-as-template → rename → PARALLEL variant; naming-only, no form↔job binding) · Delete (retire, soft).
- **Mac daemon = the sole privileged actuator** (sibling to `portal_poll`): the portal enqueues a publish-request in D1 (send-free) → daemon validates → commits file+manifest in ONE commit → merges → **deploys via LOCAL wrangler** (the CF credential never goes on the cloud/GitHub) → **fast-forwards `~/its` so `load_definition` sees the file** → Box archive → stamps "Live" after a post-deploy health check. **NOT a GitHub Action.**
- **Server + daemon + CI = the safety boundary** (not the editor): the Worker validates the composed def at enqueue (meta-schema + renderer-contract rules + a reserved-key denylist incl. `job`/`work_date` + cross-section-unique keys); the daemon re-validates vs git HEAD; CI runs a **3-renderer non-degraded render smoke**.
- **C12 RESOLVED = A (fully automatic, NO human merge gate)** — operator's call (he will NOT hand-review each publish), CONDITIONAL on a load-bearing MANDATE: (1) the automated gates (CI 3-renderer smoke + server/daemon validation + branch protection + PreToolUse hooks + doctrine-drift/secret-scan CI) MUST fail-closed and STOP a bad publish; (2) the portal MUST **detect publish progress + ALERT** (operator CRITICAL triple-fire + the monitor going red) on any stop/failure — **NO silent stall**. Doctrine tension: form-publish COMMITS+DEPLOYS code (the highest capability class, normally a human gate), so A is a deliberate **per-category clearance** backed by the mandate; **(B) one-click-approval stays a one-line switch**.
- **Publish Status Monitor** (Queued→Validated→Tested→Live→Archived, red+reason+CRITICAL on failure; full state machine + rollback + per-parent serialization). **Box archive = historical storage of record** (DR fallback: total outage → print/fill blanks by hand). **Session Hardening:** role-aware — submitters keep 90-day, **admins 5-min idle** (sliding) + **#7 session-epoch** (migration; logout + password-change bump). Decoupled from the publish op's lifecycle.
- **Canonical-mission TODO:** fold §G29.3 into `workstreams/safety-portal/mission.md` when the Phase-2 build starts (this is the spec). The red-team's "no role model / no Worker CI / no PR-L" findings were **stale** (it read the un-pulled `~/its`; all three shipped in Phase 1).

### §G29.4 — Process
- Exec main `f3ad814` → `b7bad5a` (PRs #193/#194/#195/#197/#198/#200/#201/#202 + exec-docs #199 brief). All four-part verified; live mirror Worker `80ec62ea`.
- **Operator cleanup pending:** exec worktrees `~/its-admin`/`~/its-formarchive`/`~/its-submitas`/`~/its-harden`/`~/its-brief`; pull `~/its` → main (it was stale at the session-start commit — which tripped the red-team agents into the stale-context findings).
- Background **AGENTS were FS-sandboxed to `~/its` only** this session (couldn't write sibling worktrees); main-thread CC retained full access — so CC ran the worktree edits on the main thread.

## §G30 — 2026-06-09 Safety Portal Phase-2 Form Manager — full build (exec `b7bad5a` → `b736691`)

### Summary

The entire Phase-2 **Form Manager** — schema-driven form editor + automated publish pipeline — was designed in §G29.3 and **fully built this session** (exec PRs #203–#216, #218; PR #217 was a daemon-created failed-attempt PR, CLOSED). Exec HEAD advanced from `b7bad5a` to `b736691`. All PRs four-part verified. The publish daemon is the first ITS component that **commits code, merges, and deploys autonomously** under a per-category clearance (C12=A).

### §G30.1 — Components shipped

| Component | PR(s) | Notes |
|---|---|---|
| `safety_portal/catalog.json` + `catalog.schema.json` | #203 | The active-set manifest contract; CI consistency check (`scripts/check_catalog_consistency.py`); append-only on disk — manifest is the ONLY active-set gate |
| `safety_reports/publish_manifest.py` (`apply_publish`) | #213 | Pure transform: create/edit/add_version/delete/rollback; enforces identity uniqueness, monotonic version, variant-mixing rule, rollback target |
| `FormEditor.tsx`, `FormsPage.tsx`, `editorModel.ts`, `editorValidation.ts` | #211 | B8 sectioned form editor + create/edit/add-version/retire ops |
| `PublishMonitor.tsx` | #211 | Queued→Validated→Tested→Live→Archived status monitor; red+reason on failure |
| Phase-2 8a: `users.session_epoch` | #206 | Real session revocation — logout + password-change bump the epoch; `requireSession` rejects stale cookies. D1 migration 0009. |
| Phase-2 8b: admin 5-min idle window | #215 | Sliding 5-minute idle timeout for admin sessions (role-aware; submitter sessions unchanged) |
| Worker publish enqueue (`POST /api/admin/publish`) + `publishValidation.ts` | #209 | Send-free enqueue + hand-rolled Worker-side validator (meta-schema + renderer-contract + reserved-key denylist + `validateParentGrouping` vs the deployed `catalog.json`; needed `resolveJsonModule` in `tsconfig.worker`) |
| Daemon queue endpoints (pull/claim/stamp) | #212 | `/api/admin/publish-status`, `/api/admin/publish-dismiss`, `/api/admin/publish-request` |
| `safety_reports/publish_daemon.py` | #214 | Privileged Mac actuator: claim → re-validate vs git HEAD → commit → CI render-smoke → `_wait_for_ci` (polls `mergeStateStatus`) → `gh pr merge --squash` → deploy → Box archive → stamp each milestone; `_reset_to_main` Stage-0 recovery (see §G30.2); new launchd job `org.solutionsmith.its.publish-daemon` (StartInterval 120, RunAtLoad false) |
| D1 migration 0010 | #214 | `publish_requests` table |
| 3-renderer render-smoke net (3c) — Python half | #208 | Pytest suite covering the Python renderer path |
| 3-renderer render-smoke net (3c) — SPA half | #210 | `jsdom` FormRenderer smoke (third leg) |
| Parent-grouping guard (#216) | #216 | Client editor `checkParentGrouping` + Publish Monitor "Clear finished" button |
| `_wait_for_ci` + `_edit_failed_publish` (#218) | #218 | Daemon polls `mergeStateStatus == CLEAN` before merge (no `--auto`); `portal_admin edit-publish` verb to requeue a failed request |

### §G30.2 — Publish daemon: architecture + two critical operational facts

**Architecture:** the daemon is the **sole privileged actor** — the portal enqueues a send-free D1 publish-request; the daemon claims it, re-validates vs the authoritative git HEAD copy of `catalog.json`, runs the 3-renderer CI smoke, waits for CI to go CLEAN (polling `mergeStateStatus`), then `gh pr merge --squash`, deploys via local `wrangler deploy` (CF credential never leaves the Mac), fast-forwards `~/its` so `load_definition` sees the file, archives a blank-fillable to Box, and stamps "Live."

**Critical fact 1 — GitHub auto-merge DISABLED.** `gh pr merge --auto` is rejected by the repo with a GraphQL `enablePullRequestAutoMerge` error. This is a permanent repo setting. The daemon therefore polls CI itself (`mergeStateStatus`) then calls `gh pr merge --squash` directly (PR #218). `--auto` was also problematic because it merges ASYNCHRONOUSLY — the daemon needs to know the merge commit OID before it deploys. Never re-add `--auto` to the publish daemon without addressing both constraints.

**Critical fact 2 — the daemon operates on the live `~/its` tree and can strand it on a `publish/*` branch.** A failed publish cycle (CI red, merge error, crash mid-cycle) can leave `~/its` on `publish/req-<N>-<identity>`. This happened during development (left on `publish/req-5-incident-report`). PR #218 added `_reset_to_main()` as Stage-0 recovery: on daemon startup and before claiming a new request, it stashes any uncommitted changes and force-checks out `main` + fast-forwards. The daemon NEVER touches operator untracked files (stash is a safety net; untracked are left). After an incident, verify: `git -C ~/its branch` should be `main` after the next daemon cycle.

### §G30.3 — Parent-grouping rule: three-layer enforcement

The rule — a form's sections must all have the same parent grouping scheme, i.e., no mixing of a `parent`-keyed section with a non-parent-keyed sibling — is enforced at THREE layers:

1. **Client editor** (`checkParentGrouping` in `editorValidation.ts`) — immediate UI feedback.
2. **Worker enqueue** (`validateParentGrouping` in `publishValidation.ts`, evaluated against the deployed `catalog.json` imported via `resolveJsonModule` in `tsconfig.worker`) — server-side gate at submission.
3. **Daemon** (`apply_publish` in `publish_manifest.py`) — authoritative check vs git HEAD.

The Worker needed `"resolveJsonModule": true` in `tsconfig.worker.json` for the static `catalog.json` import — this was the blocking gotcha during PR #213/#209 authoring.

### §G30.4 — ITS_Config additions this session

- Row added to Smartsheet `ITS_Config` (sheet `3072320166907780`, row 41): `safety_reports.publish_daemon.polling_enabled = true`, Workstream `safety_reports`.
- The daemon reuses existing Keychain key `ITS_PORTAL_INTERNAL_TOKEN` + ITS_Config key `safety_reports.portal.worker_base_url` (shared with `portal_poll`).

### §G30.5 — Deferred / tech-debt

- **Rollback UI picker** — the backend is DONE (`apply_publish` rollback op + daemon rollback path + `PublishOp` type carrying rollback target); only the retired-version-history PICKER UI in the editor is missing. The rollback op can be triggered via API today; the UI is the deferred piece.
- **S1 — per-item scale/comment authoring** — survives an edit today (existing `hsse` items carry `scale`/`comment`); no new-item authoring UI in the editor. Only `hsse` uses it.
- **Daemon privileged ops are operator-validated-live only** — `git/gh/wrangler` subprocess chains are mocked in unit tests per Op Stds §30 (mock at the subprocess boundary); #218's `_wait_for_ci` + `_reset_to_main` are running live for the first time on the operator's recovery. A dedicated integration test harness for the commit→merge→deploy chain does not exist; operator's live smoke is the gate.

### §G30.6 — §43 coverage

`safety_reports/README.md` carries the §43 successor-remediation entry for the publish daemon (symptom, low-class repair steps, escalate-to-Seth boundary). Publish-daemon operations (git/merge/deploy) are HIGH-capability-class (category 4: code changes) — the §43 entry exists for SYMPTOM recognition and escalation, not for Tier-2 repair.

### §G30.7 — Process

Exec `b7bad5a` → `b736691` (PRs #203–#216, #218; #217 closed/not merged). All four-part verified. `~/its` is currently on branch `publish/req-5-incident-report` (publish daemon stranded it before `_reset_to_main` was added; the next daemon cycle will recover it, or `git -C ~/its checkout main && git pull` manually). Remaining operator actions: pull `~/its` to `main`, clean worktrees from this session, load the publish-daemon launchd job (`RunAtLoad false` — operator-gated; HIGH-capability-class, Tier-3 escalation per §43).

Blueprint: no new doc updates required this session (the Phase-2 design brief in §G29.3 is the spec; fold into `workstreams/safety-portal/mission.md` when starting Phase-3).
