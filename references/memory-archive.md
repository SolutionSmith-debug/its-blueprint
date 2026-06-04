---
type: reference
version: 5
status: canonical
last_verified: 2026-05-29
last_verified_against: df83713
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

# Cross-References

- Memory Archive v4 — operational detail through 2026-05-21 morning. v5 extends, does not supersede.

- ITS_Comprehensive_Session_Update_2026-05-21_EOD.docx — canonical record for PRs #59 + #60.

- ITS_Daemon_Health_Schema_2026-05-21.docx — canonical schema + heartbeat contract.

- ITS_Cascade_Verification_Audit_2026-05-21.docx — forensic verification predecessor for 2026-05-22 cascade.

- ITS_Security_Hardening_and_Doc_Drift_Audit_2026-05-21.docx — earlier security-decision capture; doc-drift findings superseded by Verification Audit's verified-from-repo claims.

# Authority

Memory Archive v5, 2026-05-22. Append-only extension of v4. §A-§G4 carry forward verbatim from v4; §G5 (2026-05-21 evening + 2026-05-22 cascade) added. v4 is not retired — v5 is the active reference for restoration of late-cycle operational detail; v4 remains the active reference for earlier-cycle detail.

Loading model: not part of the canonical doc set loaded by default. Load on demand when specific operational details from this period are needed for restoration. v6 trigger: next major cycle of operational detail accumulation (anticipated post-Phase-1.5 cutover).
