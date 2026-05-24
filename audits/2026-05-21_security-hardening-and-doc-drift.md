---
type: audit
status: archived
last_verified: 2026-05-24
last_verified_against: 3b7d56d
workstream: null
tags: [forensic, security-hardening, doc-drift]
---

**ITS Security Hardening Cascade + Doc Drift Audit**

2026-05-21 Late Evening

*Pre-Customer-1 Security Decisions + Canonical Doc Reconciliation + cc Handoff*

# Executive Summary

Three artifacts in one. First, this doc captures the security hardening decisions made in the late-evening session of 2026-05-21 (after ITS_Comprehensive_Session_Update_2026-05-21_EOD.docx closed at 19:16Z). Second, it audits every canonical doc in the project for drift against tonight's decisions plus the polling-daemon doctrine established earlier in the session. Third, it hands off a clean list of repo-side reconciliation items for cc.

Substance of the security decisions: three new pre-Customer-1 hardening items required before customer handover. (1) Picklist-hardening across all bounded-enum config/control cells to eliminate typo/case fail-open. (2) Trusted-Contacts sheet in System workspace replacing the current ITS_Config JSON-allowlist pattern, adding scope enforcement and header-forgery detection. (3) Attachment malware screening as a four-layer defensive pipeline. Each is well-scoped, each is non-blocking for the R3 critical path, all three are required before opening the safety mailbox to actual external Forefront/PM senders.

**Critical reading note: **This doc supersedes neither ITS_Comprehensive_Session_Update_2026-05-21_EOD.docx (the canonical record for tonight's PRs #59 + #60) nor ITS_Daemon_Health_Schema_2026-05-21.docx (schema reference). It is the third in tonight's doc trilogy: comprehensive record, schema reference, and now this cascade-and-audit overlay.

## What This Doc Is Not

This is not a versioned canonical-doc bump. It does not retire Op Stds v10.1, V&R v7.1, FM v7.1, FSU v6.4, etc. Those bumps land at the next formal cascade event. This doc is the input record that the next cascade event will absorb. Treat it like the Cascade Audit Errata 2026-05-19 pattern — surfaces drift, names the resolution, defers the formal v-bumps to a downstream cascade pass.

# Section A — Decisions Captured Tonight

## A.1 — Kill Switch Row Name Correction

Chat-side memory and one of tonight's intermediate responses referred to the system-wide kill switch as ITS_Config row "system.kill_switch". The actual row name is system.state. The correct values are ACTIVE, PAUSED, MAINTENANCE.

**Authority: **shared/kill_switch.py docstring (PR #9, 2026-05-18) plus Op Stds v10 §1 plus ITS_Operational_Standards_v10_1_2026-05-21.docx §"What Did NOT Change in v10.1" which explicitly preserves the system.state name.

Memory entry was not previously polluted with the wrong name — this was a chat-side speech error only, not a documented drift. No correction action needed in any canonical doc. Captured here for record because the user noticed and asked for clarification.

## A.2 — Pre-Customer-1 Security Hardening Cluster

Three hardening items grouped under one cluster because they share trigger (Customer 1 handover) and sequencing (must precede opening the system to external senders). All three were captured in memory entry 30.

### A.2.1 — Picklist-Hardening (Bounded-Enum Cells → PICKLIST / CHECKBOX)

Audit every Smartsheet column representing a finite-domain value across all ITS sheets. Convert from free-text TEXT_NUMBER to PICKLIST (multi-value enum) or CHECKBOX (boolean) as appropriate. Eliminates the structural failure mode where a typo, case-drift, or whitespace in a config cell triggers a fail-open WARN that an operator might not notice.

Canonical example: today's system.state row in ITS_Config is free text. An operator typing PAUSE (missing the D) instead of PAUSED falls through to the "invalid value" fail-open branch — system stays ACTIVE while the operator thinks it's stopped. With PICKLIST column type, the operator literally cannot type an invalid value; Smartsheet rejects the entry.

### Scope of the audit

Targets are not limited to ITS_Config. Every sheet with operator-editable control cells is in scope:

- ITS_Config — system.state, all *.polling_enabled flags, any setting with an enumerated domain.

- ITS_Daemon_Health — most columns already PICKLIST per parallel chat's good instinct (Workstream, Last Cycle Status); future Runtime Gate should be CHECKBOX.

- ITS_Errors — Severity (INFO/WARN/ERROR/CRITICAL), Workstream, possibly status fields.

- ITS_Review_Queue — Status enum, Workstream, urgency tiers, reviewer-chain selectors.

- ITS_Quarantine — quarantine reason enum, disposition (release/delete/escalate), Workstream.

- Per-project sheets (Daily Reports, Weekly Rollups, future): status fields, category fields, anywhere a code reader expects a known value.

- All future workstream sheets — Subcontracts statuses, PO/Materials statuses, Email Triage categories, AI Employee task states.

### Standing rule going forward

*Any new Smartsheet column representing a finite-domain value MUST be created as PICKLIST or CHECKBOX, never TEXT_NUMBER. Free text is acceptable only for genuinely open-ended content (names, descriptions, IDs, JSON payloads, error messages, free-form notes).*

This rule deserves codification in Op Stds (proposed §35 below). Today's parallel chat already followed it instinctively when building ITS_Daemon_Health — the instinct is good; the rule makes it consistent.

### Implementation cost estimate

Smartsheet allows column-type changes on existing columns with caveats — existing values preserved if compatible, new entries enforced. Smartsheet MCP can't do it (no API primitive for column-type change); operator UI definitely can. Per-column conversion is roughly 30 seconds. Full System workspace audit + conversion is approximately 30 minutes of operator clicks plus a script-side audit of any consumer that reads the Value as raw string.

kill_switch.py already handles fail-open robustly, so the picklist change is defense-in-depth, not a bug fix. Existing fail-open logic stays as belt-and-suspenders for the Smartsheet-unreachable case.

### A.2.2 — Trusted-Contacts Sheet (Replaces ITS_Config Allowlist JSON)

Today, sender allowlists live as JSON-encoded list cells in ITS_Config (e.g., safety_reports.intake.allowed_senders). This is operationally fragile:

- JSON in a cell is hard to audit — operator can't see at a glance who's trusted.

- One missing comma corrupts the parse and the entire allowlist fails.

- No metadata: who added each sender, when, why, last-verified date.

- No status: can't temporarily disable a sender without deleting and re-adding.

- No scoping: a Bradley PM and a Brimfield safety officer have identical trust levels even though they should only be trusted for their respective projects.

- No cross-workstream visibility — every workstream maintains its own list with no central audit surface.

### Replacement: ITS_Trusted_Contacts sheet in System workspace

New sheet in folder "01 — Config" (or potentially a new "05 — Trust" folder; deferred to schema build session). Schema sketch — all subject to refinement at build time:

| **Column** | **Type** | **Purpose** |
| --- | --- | --- |
| Email | TEXT_NUMBER (PRIMARY) | Canonical lowercased email address. Used as exact-match key. |
| Display Name | TEXT_NUMBER | Human reference; never used in trust decisions. |
| Role | PICKLIST | PM / Safety / Forefront / Subcontractor / Vendor / Solution Smith / Internal / Other |
| Project Scope | PICKLIST (multi-select) | bradley_1 / bradley_2 / brimfield_1 / brimfield_2 / huntley / rockford / _all |
| Workstream Scope | PICKLIST (multi-select) | safety_reports / subcontracts / po_materials / email_triage / ai_employee / _all |
| Status | PICKLIST | ACTIVE / DISABLED / PENDING_VERIFICATION |
| Added By | TEXT_NUMBER | Who added this contact; populated from Modified By at creation time. |
| Added Date | DATE | Audit trail. |
| Last Verified | DATE | Operator marks when they confirmed identity (e.g., voice call, in-person). |
| Notes | TEXT_NUMBER | Free-text context — reason for trust, special handling, etc. |

### Trust-evaluation logic in workstream intake daemons

Intake.py (and all future workstream intakes) replaces the current ITS_Config JSON lookup with a query against this sheet:

- Look up the From: address in ITS_Trusted_Contacts where Email = exact-match AND Status = ACTIVE.

- If no row: route to ITS_Quarantine with reason "sender_not_trusted". Heartbeat OK, no error.

- If row exists but Project Scope doesn't include the inferred project: route to ITS_Review_Queue with reason "scope_mismatch". The PM is trusted in general but not for this project — could be legitimate cross-coverage or could be spoofing.

- If row exists and scope matches: proceed to pipeline.

### Header-forgery detection (the SPF/DKIM/DMARC layer)

Even with exact-match sender allowlist, an attacker spoofing the From: header bypasses the first defense. Email Triage Brief v5 already acknowledged this risk verbatim: "Spoofed sender within allowlist: an attacker spoofing an allowlisted sender bypasses the first defense layer." The brief deferred to upstream M365 anti-spoofing (DMARC, DKIM, SPF) without ITS itself checking these.

Tonight's decision: ITS itself checks these too. Microsoft Graph API exposes the relevant headers on every inbound message:

- internetMessageHeaders contains Authentication-Results — parse for spf=pass/fail, dkim=pass/fail, dmarc=pass/fail.

- Return-Path header — compare against From: header. Mismatch is a spoofing signal.

- Received chain — first Received hop's source domain compared against From: domain. Cross-domain inconsistency is a spoofing signal.

Disposition logic: any of {spf=fail, dkim=fail, dmarc=fail, Return-Path mismatch} → route to ITS_Quarantine with reason "header_forgery_suspected". Any of {spf=neutral, spf=softfail, dkim=none} on a sender otherwise trusted → route to ITS_Review_Queue. All-pass + exact-match sender + scope-match → proceed to pipeline.

This is the most architecturally substantive of the three security items. It changes intake.py's input contract (richer message metadata required from graph_client) and adds a new structural decision branch in the pipeline.

### A.2.3 — Attachment Malware Screening (4-Layer Pipeline)

Today, attachments (PDFs from DFRs, Office docs, images) are downloaded via Graph, classified via Anthropic API, then uploaded to Box. There is no malware screening at any step. This is the largest single security gap in the current intake pipeline.

Threat model is real: subcontractors are external untrusted senders. A compromised subcontractor laptop sending an apparently-legitimate DFR PDF could embed JavaScript, macros, or actual malware payloads. ITS today would file the PDF in Box without inspection — propagating a compromised artifact into the customer's permanent record.

### Layer 1 — Static signature checks (cheap)

Runs first, fails fast on the obvious cases:

- File magic-number verification: does the bytestream's header match the claimed extension? A .pdf attachment that's actually a ZIP archive gets flagged. Python's filetype library is one option; manual byte-signature check is trivial.

- File size sanity: a Daily Field Report PDF should be 50KB-50MB. A 200-byte attachment is suspicious (truncated/empty). A 500MB attachment is suspicious (payload-padding or wrong file).

- Filename pattern matching: known-bad patterns including .pdf.exe, double-extensions, unicode lookalike characters, suspiciously long filenames, embedded RTL-override characters.

### Layer 2 — Format-aware structural inspection (cheap)

Runs second. Inspects the internal structure of common attachment formats for known-bad indicators:

- For PDFs: use PyMuPDF or pypdf to read the object tree. Flag presence of /JavaScript, /JS, /EmbeddedFile, /Launch, /OpenAction keys. These have legitimate uses in some PDFs but are unusual for DFRs.

- For Office docs (.docx, .xlsx, .pptx): check for VBA macros, embedded OLE objects, external template references. python-docx and openpyxl libraries expose this.

- For images: check EXIF for embedded data, polyglot signatures.

- For any: extract any embedded URLs, flag external domains for human review (legitimate DFRs may have URLs to forms or maps; the review-queue routing lets operator decide).

### Layer 3 — ClamAV antivirus engine (medium cost)

ClamAV is the canonical open-source antivirus. Free, runs locally as a daemon (clamd), maintains a signature database that auto-updates daily. macOS install via Homebrew.

- pyclamd Python library connects to the local clamd socket.

- Each attachment passes through clamd.scan_stream(bytes). Returns OK / FOUND <signature_name> / ERROR.

- Catches actual malware payloads that layers 1 and 2 miss.

- Test fixtures: EICAR test signature is a safe test string ClamAV always flags as a virus — use it in tests to verify the pipeline is hooked up correctly without using real malware.

### Layer 4 — VirusTotal API (optional, deferrable)

VirusTotal aggregates ~70 antivirus engines plus URL/domain reputation. Free tier: 4 requests/minute, 500/day.

- Submit file hash (SHA-256), get back "X of Y antivirus engines flagged this."

- Catches things ClamAV alone misses (other vendors' signatures, newer threats).

- Network round-trip cost; rate limits.

- Recommendation: defer to Phase 2 or later. Layers 1-3 are sufficient for Phase 1.5 / Customer 1 handover.

### Disposition logic

- Any layer reports malicious → ITS_Quarantine row with severity CRITICAL, Box upload skipped, ITS_Errors entry with full triple-fire (Smartsheet + Resend + Sentry), attachment bytes preserved on disk in a quarantine directory for forensics, sender DISABLED in ITS_Trusted_Contacts pending operator review.

- Any layer reports suspicious-but-not-malicious → ITS_Review_Queue with the layer-N flag noted, operator decides.

- All layers clean → pipeline continues as today.

### Implementation cost estimate (combined cluster)

| **Item** | **Estimated Effort** | **Dependencies** |
| --- | --- | --- |
| Picklist-hardening audit + conversion | ~30 min operator UI + ~1 hour audit pass | None — can do anytime |
| ITS_Trusted_Contacts sheet + schema doc | ~30 min build + ~1 hour design doc | None |
| intake.py refactor to read from trusted-contacts sheet | ~2 hours + tests | Trusted-contacts sheet built |
| Header-forgery detection (graph_client + intake.py) | ~3 hours + tests | Graph header field exploration |
| Attachment screening Layers 1+2 (static + structural) | ~3-4 hours + tests | PyMuPDF, python-docx pip-install |
| Attachment screening Layer 3 (ClamAV) | ~1 hour operator install + 2-3 hours code + tests | Homebrew clamav install |
| Total combined estimate | ~1.5 dedicated day-sessions | Best as 2 sessions: trusted-contacts day + malware-screening day |

## A.3 — Future Runtime Gate Column (Per-Daemon Smartsheet Operability)

Captured earlier in evening but worth re-flagging here for completeness. Add a Runtime Gate CHECKBOX column to ITS_Daemon_Health. Daemons read THAT column from their own row instead of (or in addition to) the polling_enabled flag in ITS_Config. ITS_Daemon_Health then becomes the single operator surface for both monitoring AND controlling every daemon.

Naturally pairs with Option 2 from earlier in the evening conversation. Recommended sequence: bundle with shared/runner.py extraction (PR #61+ at second consumer) so the runner abstraction reads Runtime Gate by default, all daemons inherit Smartsheet-operability for free, and Email Triage / weekly_generate / future workstreams ship with this surface from day one.

Distinct from the picklist-hardening item but conceptually adjacent — both improve operator control surfaces. Could ship in the same PR if sequencing allows.

# Section B — Canonical Doc Drift Audit

Pass through every canonical doc currently in project memory. Each subsection: name the doc, name the drift, propose the fix. Fixes are paste-ready for the next cascade event.

## B.1 — Foundation Mission v7 + v7.1 (Adversarial Input Handling)

### Drift identified

Invariant 2 enumerates five defense layers: sender allowlist, untrusted-content tagging, structured output enforcement, capability gating, anomaly logging. Tonight's decisions add three substantive extensions that aren't in v7.1:

- Sender allowlist mechanism evolves from "ITS_Config JSON list" to "ITS_Trusted_Contacts sheet with scope enforcement." The principle is unchanged; the canonical implementation is materially different.

- Header-forgery detection (SPF/DKIM/DMARC + Return-Path validation) is a new defense layer that doesn't map to any of the existing five.

- Attachment screening (4-layer malware pipeline) is a new defense surface entirely. The current Invariant 2 implementation guidance treats attachments as just "extracted attachment text wrapped in untrusted_content tags" — adequate for prompt-injection defense, silent about malware.

### Proposed amendment (for FM v7.2 or v8 cascade)

Add a sixth defense layer to Invariant 2's enforcement-pattern list, and expand the sender-allowlist bullet:

*Invariant 2 — Adversarial Input Handling. All content originating outside the operating customer tenant is untrusted data. Six defense layers govern the implementation. The invariant itself is unchanged from v7.1; layers 1, 6 are revised.*

*Layer 1 — Sender allowlist + scope enforcement. Inbound sender exact-matched against ITS_Trusted_Contacts sheet (System workspace). Match requires Status=ACTIVE. Project Scope and Workstream Scope columns enforce per-project and per-workstream trust boundaries. Header-forgery defense (SPF/DKIM/DMARC + Return-Path validation) precedes the allowlist check — any header-authentication failure routes to ITS_Quarantine before sender lookup. JSON-list allowlists in ITS_Config (the prior pattern) retire at trusted-contacts cutover.*

*Layer 6 (NEW) — Attachment screening pipeline. Every attachment passes through four sub-layers before being uploaded to Box or referenced in any AI call: (a) static signature checks (magic-number, size sanity, filename pattern matching); (b) format-aware structural inspection (PDF JS/embedded files, Office macros, EXIF anomalies); (c) ClamAV antivirus scan via pyclamd; (d) optional VirusTotal hash check (Phase 2+ enhancement). Layer failure dispositions: malicious → ITS_Quarantine + CRITICAL triple-fire + sender DISABLED in ITS_Trusted_Contacts; suspicious → ITS_Review_Queue; clean → proceed.*

Layers 2-5 carry forward verbatim from v7.1. The numbering shift requires no other change.

### v-bump justification

Invariant 2's enforcement-pattern set changes substantively. This is a v8 trigger by FM authority criteria ("substantive invariant change") — though arguably a v7.2 trigger if framed as "enforcement-pattern evolution, invariant principle unchanged." Recommend v8 to mark the addition of the 6th layer as architecturally significant rather than buried as v7.x status drift.

## B.2 — Vision & Roadmap v7 + v7.1 (Phase 1.5 Cutover Phase)

### Drift identified

V&R v7.1 Phase 1.5 is described as "combined cutover + hardware delivery event" with Handover Plan v6.2 as the operative runbook. Pre-cutover conditions in Handover Plan v6.2 require triple-fire CRITICAL alert path having fired on a real issue. Nothing in V&R or Handover Plan currently requires the security hardening cluster as a precondition.

This is a meaningful gap. Today the safety mailbox is operating in closed-loop testing mode — only Solution Smith's address is in the allowlist, no real external senders. The moment Teala wires in real Forefront/PM contacts (which is downstream of R3 Session 2 + Session 3 ship), the threat surface opens. If cutover happens before security hardening lands, the customer Mac ships into California with a vulnerable intake pipeline.

### Proposed amendment (for V&R v7.2 cascade)

Add to the Phase 1.5 entry's preconditions section:

*Pre-cutover security hardening cluster — three items required before cutover: (a) Picklist-hardening of all bounded-enum config/control cells, completed System-workspace-wide; (b) ITS_Trusted_Contacts sheet built and populated with all anticipated real-recipient PMs/Forefront contacts/subcontractor addresses; intake daemons refactored to read from it; ITS_Config JSON allowlists retired. (c) Attachment screening pipeline (Layers 1-3 minimum) implemented and verified against EICAR test fixtures plus a corpus of legitimate DFR samples. Cutover does not proceed if any of these three are open.*

### Phase plan implications

This means roughly 1.5 day-sessions of pre-cutover work that didn't have a named home before. Sequencing within Phase 1 (or as a Phase 1.4 pre-cutover phase):

- After R3 Session 3 (weekly_send.py) ships → Phase 1 complete → close R3 in the Excellence Roadmap.

- Security hardening session(s) land in the gap between Phase 1 complete and Phase 1.5 cutover commencement.

- Real-recipient wiring (Teala-coordinated) lands during security hardening or immediately after.

- Then Phase 1.5 cutover proceeds against the hardened system.

## B.3 — Operational Standards v10 + v10.1 (Multiple New Sections)

### Drift identified

Op Stds v10.1 is up-to-date for the work that landed before 2026-05-21 morning. Tonight's polling-daemon doctrine (PR #59) plus operator-visibility surface (PR #60) plus the security hardening cluster (this doc) all need codification.

### Existing sections needing edits

- §1 Kill Switch — note picklist-hardening as planned for the system.state value column (defense in depth, doesn't change current behavior). Also note Runtime Gate CHECKBOX in ITS_Daemon_Health as the per-daemon kill switch (future work).

- §2 Daily Watchdog — Check F (Mail.app rule silent disable) is now redundant. Polling-daemon doctrine retires Mail.app rules; heartbeat surface (ITS_Daemon_Health) is the cleaner check. Mark Check F for retirement, propose successor Check H that checks heartbeat staleness across all rows in ITS_Daemon_Health.

- §3.1 Push-vs-Record Separation — extend to operator visibility: ITS_Daemon_Health is a push surface (overwrite per cycle), ITS_Errors remains the forensic record. Same doctrine, broader scope.

- §24 Sheet-ID Bootstrap — add ITS_Daemon_Health (4529351700729732), folder 04 — Daemons (2130046845511556), future ITS_Trusted_Contacts (TBD).

### New sections to add

| **Proposed §** | **Title** | **Substance** |
| --- | --- | --- |
| §31 | Polling-Daemon-as-Trigger-Primitive Pattern | launchd plist → Python script → ITS_Config-driven config → process() new items → updates state → exits. Convention bindings: org.solutionsmith.its.* labels; ~/its/logs/launchd/*.{out,err}.log; ITS_Config triplet per daemon; state files at ~/its/state/. Generalizes Mail.app-rule replacement across all current and future workstream triggers. |
| §32 | Operator Visibility Surface | ITS_Daemon_Health sheet schema; heartbeat write contract; ARCH-1 (Enabled=metadata) / ARCH-2 (persistent row-id cache) / ARCH-3 (lifetime monotonic) refinements; daemon-health report spec; Watchdog Check F → Check H successor. |
| §33 | Trusted-Contacts Pattern | ITS_Trusted_Contacts sheet schema; exact-match sender check; scope enforcement (project + workstream); header-forgery detection (SPF/DKIM/DMARC + Return-Path); disposition logic for quarantine vs review-queue vs proceed. Retires ITS_Config JSON allowlist pattern. |
| §34 | Attachment Screening Pipeline | Four-layer defense: static signatures → format-aware structural → ClamAV → optional VirusTotal. Disposition logic: malicious → quarantine + DISABLE sender; suspicious → review queue; clean → proceed. EICAR test fixture for pipeline verification. |
| §35 | Bounded-Enum Picklist Convention | Every Smartsheet column representing a finite-domain value MUST be created as PICKLIST or CHECKBOX, never TEXT_NUMBER. Free text only for genuinely open-ended content. Standing rule going forward; retrofit audit triggered before Customer 1 handover. |

### v-bump justification

Five new sections plus four section edits is unambiguously a v11 trigger. v10.1's authority criteria explicitly name "substantive content change or new §" as the v11 condition. Recommended v-bump sequence: v10.1 retires on acceptance of v11. v11 absorbs all of the above plus the FSU v6.5 PR-window-reconcile work that v10.1 deferred.

## B.4 — Handover Plan v6 + v6.1 + v6.2

### Drift identified

Step 8 (Owner-side activation) tests customer admin for three things: flip ITS_Config system.state to PAUSED and back, approve a _Pending_Review row, respond to a Sentry alert email. With the security hardening cluster landing pre-cutover, customer admin should also be tested for:

- Adding a new entry to ITS_Trusted_Contacts (e.g., a new subcontractor).

- Disabling a trusted contact (Status=DISABLED) without deleting.

- Understanding the picklist constraints (cannot type free text into picklist columns).

Pre-Cutover Conditions need the security hardening cluster as a precondition (already covered in B.2's V&R amendment but Handover Plan needs the parallel update).

Risk Inventory needs two new entries: phishing/spoofing risk (mitigated by trusted-contacts + header-forgery detection) and attachment malware risk (mitigated by Layers 1-3 screening).

### Proposed amendments (for Handover Plan v6.3 or v7)

Step 8 bullet additions (after the existing three test items):

*Customer admin can add a new trusted-contact row (e.g., new subcontractor onboarding) with all required fields populated and correct Project/Workstream scope assignments. Customer admin understands that adding to ITS_Trusted_Contacts requires verification of the contact (voice call or in-person identity confirmation) before Status=ACTIVE; PENDING_VERIFICATION is the default state for new entries.*

*Customer admin can disable a trusted contact (Status=DISABLED) for offboarding (subcontractor contract ends, PM leaves the company) without deleting the row, preserving audit history.*

*Customer admin understands picklist-enforced columns: typing values that aren**'**t in the picklist will be rejected by Smartsheet at entry time. This is intentional. If a new picklist value is needed (e.g., a new project), the column itself must be updated by Solution Smith or the customer admin**'**s UI-level Smartsheet admin.*

Pre-Cutover Conditions addition (matches V&R amendment in B.2):

*Security hardening cluster complete: picklist-hardening shipped + ITS_Trusted_Contacts sheet live and populated + attachment screening Layers 1-3 verified. See V**&**R v7.2 (or v8) Phase 1.5 preconditions.*

Risk Inventory additions:

| **Risk** | **Likelihood** | **Mitigation** |
| --- | --- | --- |
| Spoofed sender within allowlist | Low-Medium | ITS_Trusted_Contacts exact-match + header-forgery detection (SPF/DKIM/DMARC) per Op Stds §33. |
| Malicious attachment from compromised subcontractor | Low-Medium | Layer 1-3 attachment screening per Op Stds §34. ClamAV signature DB auto-updates daily. EICAR test fixture verifies pipeline health. |
| Operator typo in ITS_Config control cell triggering fail-open | Low | Picklist-hardening prevents at the column-type level. Existing fail-open logic in kill_switch.py stays as belt-and-suspenders for Smartsheet-unreachable case. |

## B.5 — Excellence Roadmap v2.1 + v2.2

### Drift identified

v2.2 Track 1 R3 (first workstream consumer integration) is described as the only remaining Phase 0 → Phase 1 critical-path item. Phase 1 actually has two more layers above R3 that aren't currently scoped in the roadmap:

- Polling-daemon doctrine establishment (delivered tonight via PRs #59 + #60). Worth marking as a closed R4 milestone.

- Security hardening cluster (the three items in Section A). Worth marking as a new R5 track item, blocking on R3 completion and feeding Phase 1.5 cutover preconditions.

Quality Bar Enforcement Track 2 (2.2 — Operational Standards as code-level CI assertions) — could add picklist-validation as a CI assertion: read ITS_Config column types via Smartsheet MCP at CI time, fail if any column claiming to hold bounded-enum data is TEXT_NUMBER. Marginal value; deferrable.

### Proposed amendments (for Excellence Roadmap v2.3 cascade)

Track 1 — add R4 and R5 entries:

| **Track Item** | **Status** | **Notes** |
| --- | --- | --- |
| R4 — Polling-daemon doctrine + operator-visibility surface | CLOSED 2026-05-21 via PRs #59 + #60 | intake_poll daemon live; ITS_Daemon_Health surface writing heartbeats; doctrine codified pending Op Stds §31 + §32 cascade. |
| R5 — Pre-Customer-1 security hardening cluster | OPEN | Three items: picklist-hardening, trusted-contacts sheet, attachment screening pipeline. ~1.5 day-sessions estimate. Blocks Phase 1.5 cutover. |

Grade snapshot post-tonight: Reliability Completion grade likely moves A → A or stays A (R4 ships cleanly; R5 enters track but doesn't degrade prior grade). Documentation Discipline stays A — this cascade-and-audit doc plus the EOD comprehensive doc plus the schema doc constitute clean cascade discipline.

## B.6 — Foundation Scaffold Update v6.4 (Most-Drifted Doc)

### Drift identified

FSU v6.4's PR window log stops at PR #51. Actual through tonight is PR #60. v6.4's test count is 655 (+60 since prior bump). Actual after tonight's PR #60 is 781 (+126). v6.4 also does not include:

- ITS_Daemon_Health sheet in scaffold inventory.

- safety_reports.intake_poll daemon module.

- shared/sheet_ids.py FOLDER_SYSTEM_DAEMONS + SHEET_DAEMON_HEALTH constants + DAEMON_HEALTH_COLUMNS dict.

- shared/smartsheet_client.py new find_row_by_primary + update_row_cells_by_id helpers (PR #60).

- Bradley 1 DFR backfill (43 rows across 3 weeks; 25 Daily Reports + 18 Weekly Rollups).

- Box 1111A clone cascade (6 project folders under ITS DATA).

- scripts/launchd/org.solutionsmith.its.safety-intake.plist + install/uninstall scripts.

### Proposed amendment (FSU v6.5 cascade — overdue)

Full module inventory refresh. PR window extends 2026-05-18 through 2026-05-21 spans 35 PRs (#26 → #60 with gaps). Test count actual 781. mypy source file count 93. Detailed inventory updates are mechanical — cc can produce v6.5 via project_knowledge_search against the current state.

FSU v6.5 is the doc most overdue for a bump. Recommended as the first formal v-bump in the next cascade event.

## B.7 — Workstream Mission + Brief Docs (Pointer Drift Across All Five)

### Drift identified

All five workstream missions and briefs reference "Mail.app rule" as the canonical inbound-mail trigger:

| **Doc** | **Mail.app references** | **Drift** |
| --- | --- | --- |
| Safety Reports Mission v5 | Adversarial Input Handling — implementation | "sender allowlist on Mail.app rule (only emails from evergreenrenewables.com or evergreenmirror.com domain trigger intake; non-allowlisted senders quarantined)" |
| Safety Reports Brief v6 | Architecture (ITS Standard) | "triggered by Mail.app rules (daily intake)" + Mail.app rule mechanism design decision + MacBook reliability risk |
| Email Triage Mission v4 | Architecture | "Mail.app rule fires only on allowlisted senders; non-allowlisted mail routes to ITS_Quarantine" |
| Email Triage Brief v5 | Architecture (full section) | Two-stage Mail.app rule pattern is the central architecture; allowlist filter + classifier trigger via hot-folder. Brief retains "Mail.app rule reliability" as risk #5. |
| Subcontracts Mission v4 / Brief v5 | Architecture (if/when intake-side is built) | Inherits the Mail.app-rule pattern by reference; will need pointer update at build time. |
| POs / Materials Mission v4 / Brief v6 | Same as Subcontracts | Same pointer drift if/when supplier-response intake is built. |
| AI Employee Mission v4 / Brief v5 | References allowlist concepts generically | Lower drift than the other four; uses sender-allowlist language but doesn't bind to Mail.app implementation. |

### Proposed amendment approach

Two paths. Pick one or do both:

- Path 1 — Cascade-wide pointer bump. All five workstream docs get a v-bump (Safety Reports v5 → v5.1, Email Triage v4 → v4.1, etc.) with the Mail.app reference replaced by polling-daemon language and a pointer to Op Stds §31. Substance unchanged, just retiring the obsolete trigger mechanism. Roughly 2 hours of doc work.

- Path 2 — Pointer drift accepted; document the deprecation in Op Stds. Op Stds v11 §31 explicitly says "Mail.app rule references in pre-v11 workstream docs are deprecated; polling-daemon is the canonical trigger." Workstream docs get pointer bumps at next natural cascade for that workstream (e.g., when Email Triage actually gets built, Email Triage Brief v6 includes the doctrine refresh).

Recommendation: Path 2. Workstream docs aren't actively driving builds today (Safety Reports build is well underway and intake is shipped; Email Triage / Subcontracts / POs are Phase 2/3). Cascading five docs now for pointer-only updates is busy-work. Accept the drift, deprecate cleanly in Op Stds, refresh each workstream doc at its next natural cascade trigger.

## B.8 — Memory Archive v4

### Drift identified

Memory Archive v4 was last bumped 2026-05-21 (today). Should already absorb most of the morning + early afternoon work. Tonight's evening additions need to land in v4 or be deferred to v5:

- PR #59 + PR #60 details (already in EOD comprehensive doc).

- ITS_Daemon_Health build (already in schema doc).

- Security hardening cluster (this doc is the canonical capture).

- 5-duplicate ITS_Errors sheets + 1 empty duplicate Daemon_Health sheet (already in memory entry 29).

### Recommendation

Memory Archive v5 absorbs everything from 2026-05-21 14:00Z through end of day plus this cascade-and-audit doc. Single bump at the next cascade event. Not urgent — Memory Archive is not loaded by default; restoration on demand from the canonical doc set.

# Section C — Recommended Cascade Sequencing

## C.1 — What Lands Now (Tonight, Already Complete)

- Memory entry 30 captures the security hardening cluster (already added).

- This doc (ITS_Security_Hardening_and_Doc_Drift_Audit_2026-05-21.docx) goes into project memory.

- EOD comprehensive doc + schema doc already in place.

## C.2 — What Lands At Next Cascade Event (Formal V-Bumps)

Recommended sequence when next cascade pass runs:

- FSU v6.5 — overdue. Absorbs PR window through #60, test counts, scaffold additions. Mechanical. Fast.

- Op Stds v11 — new sections §31-§35 plus existing-section edits per B.3. Substantive. Largest single doc.

- FM v8 (or v7.2) — Invariant 2 layer-6 addition + Layer 1 expansion per B.1. v8 framing recommended for significance.

- V&R v7.2 (or v8) — Phase 1.5 security hardening precondition per B.2.

- Handover Plan v6.3 (or v7) — Step 8 + Pre-Cutover + Risk Inventory updates per B.4.

- Excellence Roadmap v2.3 — R4 closed + R5 open per B.5.

- Memory Archive v5 — absorbs tonight + cascade-completion.

- Workstream missions/briefs — DEFERRED per B.7 Path 2. Pointer-only updates at next natural workstream cascade.

Cascade Unification Update doc captures the cascade event itself. Standard pattern.

## C.3 — What Lands At Security Hardening Session (Code-Side Implementation)

Separate from the doc cascade. Implementation work for the three security hardening items, sequenced after R3 Session 2 + Session 3 ship:

- Session 1: Picklist-hardening audit + conversion + standing-rule codification.

- Session 2: ITS_Trusted_Contacts sheet build + intake.py refactor + header-forgery detection.

- Session 3: Attachment screening Layers 1-3 + EICAR test fixtures + integration tests.

Each session is ~half-day to one day. Could run in parallel with operator-side picklist conversion + trusted-contacts seeding if Seth wants to compress timeline. Total estimate: 2-3 calendar days of focused work.

# Section D — cc Handoff: Repo-Side Reconciliation

cc reconciles the in-repo CLAUDE.md and README.md surfaces against tonight's doctrine. Specific tasks:

## D.1 — CLAUDE.md Updates

- Add a Polling-Daemon Pattern section pointing to safety_reports/intake_poll.py as the canonical example. Reference the launchd plist + install script + ITS_Config triplet pattern.

- Add an Operator Visibility section pointing to ITS_Daemon_Health sheet + the heartbeat write contract.

- Update the open-questions section: Q4/Q5/Q6/Q8 resolutions already absorbed (per memory entry 23). Confirm CLAUDE.md is in sync.

- Add tech_debt deprecation note: Mail.app rule references in pre-#60 docs are deprecated; polling-daemon doctrine supersedes.

- Add forward-reference to pre-Customer-1 security hardening cluster: picklist-hardening + trusted-contacts + attachment screening. Note that R3 Session 2 + Session 3 ship before this work begins.

## D.2 — README.md Updates

- Test count refresh: 655 → 781.

- mypy source file count: 91 → 93.

- PR window extension: #51 → #60 (note GitHub auto-numbered PR #59.5 as PR #60).

- Add a brief paragraph about ITS_Daemon_Health as the new operator-visibility surface, with a one-line description and a sheet ID reference.

- Update the "current daemons" list: add safety_reports.intake_poll with 60s interval.

## D.3 — docs/tech_debt.md Updates

- Mail.app silent-disable entry: mark [PARTIALLY MITIGATED 2026-05-21] (already done in cc's PR #59 — confirm visible).

- Add: "Picklist-hardening pre-Customer-1" entry. Targets enumerated.

- Add: "Trusted-Contacts sheet replaces ITS_Config JSON allowlist" entry. Open.

- Add: "Attachment screening pipeline" entry. Four layers enumerated. Open.

- Add: "5-duplicate ITS_Errors sheets cleanup" entry. Canonical sheet ID 27291433258884; four dead sheet IDs enumerated.

- Add: "1 empty duplicate ITS_Daemon_Health sheet cleanup" entry. Sheet ID 3717381690969988; operator UI delete required.

- Add: "Watchdog Check F retirement / Check H heartbeat-staleness successor" entry.

## D.4 — Source-Code Notes (No Edits, Awareness Only)

- shared/kill_switch.py — robust; do not touch. Will benefit from picklist-hardening structurally but the code itself is correct.

- shared/graph_client.py — will need additions for header-field extraction (SPF/DKIM/DMARC, Return-Path, Received chain) at security-hardening Session 2.

- safety_reports/intake.py — process_message function will get a new pre-pipeline stage (trusted-contacts lookup with scope check + header-forgery check) at security-hardening Session 2. Existing pipeline stages preserved.

- safety_reports/intake_poll.py — no changes required for security hardening; the daemon doesn't change, only what process_message does inside it.

- Future shared/runner.py extraction (PR #61+) — should support trusted-contacts lookup as a built-in pre-process hook for all workstream daemons, not just safety reports.

# Section E — Authority + Cross-References

ITS Security Hardening Cascade + Doc Drift Audit, 2026-05-21 late evening. Captures: security hardening decisions (Section A); canonical-doc drift audit (Section B); cascade sequencing recommendations (Section C); cc repo-side reconciliation tasks (Section D).

Authority: chat-side decision capture + audit pass against canonical doc set. Does not supersede any v-bumped canonical doc. Does not retire any current canonical doc. Treated like the Cascade Audit Errata 2026-05-19 pattern — surfaces drift, names the resolution, defers formal v-bumps to a downstream cascade pass.

## Cross-References

- ITS_Comprehensive_Session_Update_2026-05-21_EOD.docx — canonical record for PRs #59 + #60.

- ITS_Daemon_Health_Schema_2026-05-21.docx — canonical schema + heartbeat contract reference.

- ITS_Foundation_Mission_v7_1_2026-05-20.docx — current operative invariants (subject to Section B.1 amendments).

- ITS_Vision_and_Roadmap_v7_1_2026-05-20.docx — current operative roadmap (subject to Section B.2 amendments).

- ITS_Operational_Standards_v10_1_2026-05-21.docx — current operative standards (subject to Section B.3 amendments).

- ITS_Handover_Plan_v6_2_2026-05-20.docx — current operative handover plan (subject to Section B.4 amendments).

- ITS_Excellence_Roadmap_v2_2_2026-05-20.docx — current operative excellence roadmap (subject to Section B.5 amendments).

- ITS_Foundation_Scaffold_Update_v6_4_2026-05-21.docx — current operative scaffold inventory (overdue per Section B.6).

- ITS_Memory_Archive_v4_2026-05-21.docx — current operational detail reference (extends per Section B.8).

- Memory entries 26-30 — tonight's doctrine + hardening cluster captures.

## Read Order on Fresh Chat

After loading the canonical doc set from memory entry 9, read tonight's three docs in this order:

- ITS_Comprehensive_Session_Update_2026-05-21_EOD.docx (what shipped + state).

- ITS_Daemon_Health_Schema_2026-05-21.docx (architectural reference).

- This doc (cascade audit + security hardening + cc handoff).

End of audit doc.