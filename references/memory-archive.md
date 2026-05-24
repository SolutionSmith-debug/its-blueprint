---
type: reference
version: 5
status: canonical
last_verified: 2026-05-24
last_verified_against: 79eec73
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

# Cross-References

- Memory Archive v4 — operational detail through 2026-05-21 morning. v5 extends, does not supersede.

- ITS_Comprehensive_Session_Update_2026-05-21_EOD.docx — canonical record for PRs #59 + #60.

- ITS_Daemon_Health_Schema_2026-05-21.docx — canonical schema + heartbeat contract.

- ITS_Cascade_Verification_Audit_2026-05-21.docx — forensic verification predecessor for 2026-05-22 cascade.

- ITS_Security_Hardening_and_Doc_Drift_Audit_2026-05-21.docx — earlier security-decision capture; doc-drift findings superseded by Verification Audit's verified-from-repo claims.

# Authority

Memory Archive v5, 2026-05-22. Append-only extension of v4. §A-§G4 carry forward verbatim from v4; §G5 (2026-05-21 evening + 2026-05-22 cascade) added. v4 is not retired — v5 is the active reference for restoration of late-cycle operational detail; v4 remains the active reference for earlier-cycle detail.

Loading model: not part of the canonical doc set loaded by default. Load on demand when specific operational details from this period are needed for restoration. v6 trigger: next major cycle of operational detail accumulation (anticipated post-Phase-1.5 cutover).
