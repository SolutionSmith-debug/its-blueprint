---
type: session_log
status: archived
workstream: null
tags: [safety-portal, forensic-audit, capability-gating, external-send-gate, circuit-breaker, atomic-write, doctrine-drift, grill-me]
---

# 2026-05-25 — Safety Portal architecture + forensic audit grill-me session

## Purpose

Walk the Safety Portal Architecture v1 (draft) + ITS Forensic Audit 2026-05-25 (draft) decision-tree with the operator. Resolve open architectural questions and audit findings before either doc lands canonically. Identify shortcomings spanning both ITS (execution) and blueprint (planning) layers.

## Pre-flight findings

- Both source docs sat in `~/Downloads/` (`safety_portal_architecture.md` v1 draft, `ITS_Forensic_Audit_2026-05-25.md` draft) — neither landed in blueprint yet. Architecture doc had not been split into `workstreams/safety-portal/{mission,brief}.md`. Audit had not been moved to `audits/2026-05-25_forensic-audit.md`.
- `safety_portal` is not yet in `CANONICAL_WORKSTREAMS` in `scripts/lint_frontmatter.py`. Pre-flight taxonomy PR required per arch doc §0 before workstream bootstrap.
- Two-doc tension surfaced immediately: arch doc §4 locked plaintext password storage; same-author audit (F01) flagged that as Tier-1 blocker. Audit and arch were written in separate planning sessions and disagreed.
- Both docs reference "Op Stds **v11**" extensively. Canonical is v12 as of 2026-05-24. Per CONVENTIONS.md, version-pinned cross-refs violate the stable-anchor rule regardless of staleness.
- Execution-repo verification: heartbeat-row state file (`safety_reports/intake_poll.py:326,341` + `weekly_send_poll.py:228,242`) uses in-place `write_text` and has no fcntl lock despite being shared between two daemons. Strictly worse than F19's seen-set (which is single-writer). `shared/alert_dedupe._dump_state` uses truncate-then-write inside flock — locked but not atomic.
- `HeartbeatStatus` Literal has drifted between `intake_poll.py:137` (`OK | WARN | ERROR | SKIPPED | skipped_swo_other`) and `weekly_send_poll.py:117` (`OK | WARN | ERROR | DEGRADED | SKIPPED`). Predicted second-order cost of preservation-over-refactor duplication.

## Decisions made

### Q1 — Sequencing: Phase 1.4 hardening cluster before Safety Portal build
- **Alternative considered:** parallel scaffolding; portal-first.
- **Rationale:** F02 (capability gating) is harder to retrofit than design in; F16/F17 close observability gaps the portal would inherit. Cluster is small relative to portal build.

### Q2 — bcrypt cost=10 for portal passwords; reverses F01 plaintext lockup
- **Alternative considered:** argon2id; keep plaintext with documented risk acceptance.
- **Rationale:** bcrypt has cleanest Workers runtime story (`bcryptjs`, no WASM CPU concern at cost=10 ~60ms). Fits Workers CPU budget. Reversing later requires force-resetting every user. Decision moves before D1 schema lands; backfill cost is zero today.

### Q2b — Per-user password scheme deferred to Phase 7 / build session
- **Alternative considered:** lock now (lastname+year vs generic shared vs random passphrase).
- **Rationale:** scheme can be decided at admin-route implementation time; not on the critical path for D1 schema. Operator considered shared-password scheme; pushed back on the audit-trail-defensibility grounds (per-user accountability defeated by shared credentials). Decision deferred, framing captured.

### Q3 — HMAC-SHA256 on portal payload at portal initial deploy (F15)
- **Alternative considered:** defer HMAC; header-only permanently.
- **Rationale:** construction safety records are exactly the artifact an injury-lawsuit defendant tampers with. Lands cleanly with Phase 5 submission pipeline. Becomes load-bearing post-Correction-A (single-mailbox routing removes the dedicated-inbox implicit second factor).

### Q4 — Backdating stays as-locked (operator risk acceptance to land in arch §19)
- **Alternative considered:** surface submission timestamp on PDF when it differs from work_date; cap backdating window.
- **Rationale:** operator accepts the litigation-defensibility trade-off in favor of PM zero-friction. Risk-acceptance must land explicitly in arch doc §19 Risks table (currently a design choice without acknowledged trade-off).

### Q5 — F02 option 3: invert capability gating to network-library allowlist + keep doctrine claim + bind test to claim
- **Alternative considered:** weaken doctrine to match current code; defer.
- **Rationale:** doctrine claim is structurally correct (two-process model); enforcement is the gap. Tighten test, keep claim, document the relationship in CLAUDE.md + FM v8.

### F22 (new) — External Send Gate is application-attested at the approval boundary
- **Surfaced by operator** during Q5; same class as F02 at a different layer.
- `*_Pending_Review` approval columns are writeable by any ITS script with sheet write access; `weekly_send_poll` trusts the values without consulting Smartsheet's row-history attestation.
- **Fix recommended:** application-layer row-history verification + optional `update_row` belt-and-suspenders wrapper. ~4 hours + 1 hour optional + 30 min doctrine update.
- **Portal inheritance:** yes — portal feeds the same WPR_Pending_Review gate; fix lands once in `shared/`-layer, protects both workstreams.
- **F#:** assigned F22; landed in audit Tier 1; listed in §5 blocker bucket as item 5b.

### Q6 + Q6b — Form variant + supersession model: per-job variants via `Available For Jobs` column; one declarative `form.ts` per directory + shared `_runtime/`
- **Pre-Q6 clarification:** arch doc §4 "Forms are global" had ambiguous wording; operator meant "all logged-in PMs see all available forms" (permissions concept), not "every form on every project." The Bradley-variant use case requires per-project filtering either way.
- **New first-class requirement surfaced:** AI-one-shot extensibility. Operator extends the portal via Claude/AI assistance pasting an existing form + describing changes. Three-file-per-form pattern fights this (~30% drift between schema/render/pdf field IDs). Collapsed to single declarative `form.ts` + shared generic renderer + PDF generator.
- **Saved to memory:** `project_ai_one_shot_extensibility.md` — load-bearing constraint for any future operator-extensible surface.

### Q7 + Q7a/b/c — F08 + F09 + F23 in blocker bucket; cutover slips if F08 overruns; smartsheet-only scope with follow-on for graph + box
- **F08 effort revised** from audit's ~half-day to ~1.5-2 days due to launchd-per-cycle daemon pattern requiring persistent breaker state, CIRCUIT_OPEN status surfacing (additive to both `HeartbeatStatus` declarations), and mandatory §30 integration tests.
- **F23 (new) — Heartbeat-row state file in-place write + no concurrent lock.** Sibling to F19, strictly worse (shared between two daemons). Bundled into atomic-write PR: new `shared/state_io.py` with `atomic_write_json` + `with_path_lock` migrates six callsites (seen-set, intake_poll + weekly_send_poll heartbeat read/write, `alert_dedupe._dump_state`). ~4 hours bundled.
- **Operator caught missing test:** CIRCUIT_OPEN status surfacing in ITS_Daemon_Health. Three unit tests added to F08 scope (intake_poll cycle-entry case, mid-cycle trip case, weekly_send_poll parallel — third guards against HeartbeatStatus drift becoming a CIRCUIT_OPEN-only-in-one-daemon bug).

### Q8 — Doctrine drift bundle (F07 + F13 + F20)
- **F07 (kill switch):** reframe FM v8 + Op Stds + CLAUDE.md to "suggested pause, not security control." `fail_closed_until` timestamp deferred to tech debt.
- **F13 (anomaly logger):** reframe FM v8 Invariant 2 Layer 5 to "tripwire, not defense layer." Keep code.
- **F20 (schema version enforcement):** strengthen code — require + validate `schema_version` on parse in `weekly_generate._load_tool_schema`. ~1 hour.

### Q9 — Doc-landing pass replaces every `Op Stds v11 §N` ref with stable-anchor links
- **Alternative considered:** file F24 conventions-drift finding + lint rule.
- **Rationale:** mechanical fix during landing is sufficient; pattern surfaced once is unlikely to recur if existing scaffolds enforce.

### Q10 — Conditional 90-day R2 prune (only after Box upload verified); UI option (a) hide pruned items past day 90
- **Operator rationale to land in arch §21:** Evergreen archive retention is keep-forever; Smartsheet + Box archive together when portfolios close. OSHA 29 CFR §1904.33 retention path is the archive model; R2 is purely hot-cache *provided* Box has the canonical. Verification step is the technical guarantee.
- **Required additions per operator:** `box_upload_verified` D1 column; intake.py Stage 12.5 post-Box-upload notify (Box-then-D1 sequence non-negotiable); daily prune Cron Worker; 24h staleness alert (WARN aggregate); UI hide-post-prune (option a, confirmed).

### Correction A — Email destination consolidated to safety@; trust boundary is now header-shape + HMAC, not address
- **Per operator decision 2026-05-25.** Shim sends to existing `safety@evergreenmirror.com` / `safety@evergreenrenewables.com`, same inbox as legacy PDF intake. Routing inside intake.py keys off HMAC-verified `X-ITS-Portal-Submission-Id` header.
- **Seven second-order implications surfaced:** SPOF, defensive routing logic load-bearing, HMAC criticality upgrade, `ITS_Trusted_Contacts.Scope` schema may need multi-value, operator inbox triage burden, quarantine semantics expansion, F22 inheritance unchanged.

### Correction B — Mac mini → MacBook Pro
- Only three Mac-mini references existed (all in audit doc); all corrected. No hits in blueprint doctrine or execution-repo CLAUDE.md.

## Doc changes

### Landed in `its-blueprint` repo (this session)

- **`audits/2026-05-25_forensic-audit.md`** — moved from `~/Downloads/`. Frontmatter set to `status: canonical`, `last_verified: 2026-05-25`, `last_verified_against: 40a3509`, `workstream: null`. Mechanical v11→stable-anchor pass applied (Q9). Findings: 23 total. F22 (Tier 1: External Send Gate approval-attestation gap). F23 (Tier 2 sibling-to-F19: heartbeat-row state file in-place write + no concurrent lock). §5 reordered: F08+F09 + F19+F23 moved into the Customer-1-blocker bucket with F08 effort footnote (~half-day → ~1.5-2 days, scope discipline = cutover slips if overrun, smartsheet-only scope). Subtotal updated ~6 hours → ~2.5 days. Correction B: three Mac-mini references replaced with MacBook Pro.

- **`workstreams/safety-portal/mission.md`** (NEW, v1 canonical) — authored fresh from arch doc §§1-4 + §16 + §19 with all Q1-Q10 decisions baked in. Frontmatter `workstream: safety_portal` (newly canonical per taxonomy below). Sections: Purpose, Audience, Inputs, Outputs, Success criteria, Out of scope, Foundation Invariants Inherited (Q5/Q3/F22 updates), Decisions Locked (full Q1-Q10 absorption), Integration with safety_reports, Risks (Q4 backdating risk-acceptance row + F22 inheritance row + hardening-cluster dependency row + Correction A single-mailbox-routing risk row).

- **`workstreams/safety-portal/brief.md`** (NEW, v1 canonical) — authored fresh from arch doc §§5-15 + §17 + §18 + §20-21 with all Q1-Q10 decisions baked in. Sections: Architecture Overview (ASCII diagram with Correction A), Data Model (Q2/Q6/Q10 D1 schema updates), Smartsheet Integration (Q6 Available For Jobs column added, Form Version dropped), Authentication (Q2 bcrypt), User-Facing UX (Q6 form-picker filter + Q10 prune-aware View PDF link), Form Schemas (Q6b full rewrite: one declarative form.ts + shared `_runtime/`), Signature Handling, Submission Pipeline (Q3 HMAC + Q10 Stage 12.5), Filing Behavior, PDF Rendering (Q6b generic walker + per-form override escape hatch), Deployment Topology (Q3/Q10 secret bindings + R2 prune Cron Worker), Operational Conventions (post-F02 capability gating), Transition Plan, Implementation Phases (Q1 hardening-cluster-first sequencing), Sequencing Dependencies, Open Questions Remaining (Q6/Q10 locked items removed, residual items retained).

### Landed in taxonomy + execution-repo mirror

- **`its-blueprint/scripts/lint_frontmatter.py`** — `safety_portal` added to `CANONICAL_WORKSTREAMS` frozenset.
- **`its-blueprint/CONVENTIONS.md`** — `safety_portal` added to two workstream listings (frontmatter spec + canonical sets table).
- **`its/docs/operations/doc_conventions.md`** (execution-repo mirror) — `safety_portal` added to workstream field declaration + workstream scope table with descriptor row.

### Working copies (Downloads) — superseded by landed versions

- `~/Downloads/ITS_Forensic_Audit_2026-05-25.md` — was working draft; canonical version now at `its-blueprint/audits/2026-05-25_forensic-audit.md`. Working copy may be archived or deleted at operator's discretion.
- `~/Downloads/safety_portal_architecture.md` — was working draft; canonical version now split across `its-blueprint/workstreams/safety-portal/{mission,brief}.md`. Working copy may be archived or deleted at operator's discretion.

### Memory

- Saved `~/.claude/projects/-Users-sethsmith/memory/project_ai_one_shot_extensibility.md` + index update — captures the Safety Portal AI-one-shot constraint as project memory for future sessions.

## Verification

- `python3 scripts/lint_frontmatter.py` — **clean (57 files).**
- `python3 scripts/lint_crossrefs.py` — **clean (57 files).** v11→stable-anchor pass per Q9 applied during landing; four cross-ref violations surfaced on first lint run (mission/brief invariant-2 double-hyphen anchor, brief §13 anchor stale → §16, brief + mission memory paths-outside-repo) — all fixed.
- Audit + mission + brief landed in `its-blueprint` repo with canonical frontmatter.
- Taxonomy PR-equivalent landed: `safety_portal` registered in lint_frontmatter.py + CONVENTIONS.md (blueprint side) + doc_conventions.md (execution side).

## Out of scope

- No code landed. All implementation paths (F22 row-history verification, F08+F09 breaker + cap, F19+F23 atomic-write bundle, Q10 D1 migration + Stage 12.5 + prune Worker) are proposals awaiting explicit operator code-go-ahead per the session's "propose, review, then code" discipline.
- Doctrine v12 PR-side changes (FM v8 + Op Stds v11 → v12 §1, §3, CLAUDE.md updates) for F02/F22/F07/F13 reconciliation: pending downstream PRs.
- Customer-fork-setup-checklist (referenced in Op Stds v12 §39): no action this session.
- `shared/heartbeat.py` consolidation per CLAUDE.md tech-debt entry: F23 fix is the correctness floor; the consolidation itself stays in tech debt.
- Architectural decisions for `safety_portal` workstream taxonomy (CANONICAL_WORKSTREAMS lint addition + CONVENTIONS.md row): pre-flight Task #5.
- §21 minor Open Questions (Sync Now button location, localStorage cadence, Toolbox Talk topic library, idle timeout): not walked. Personnel name normalization Phase-2 deferral: not walked. Tier 3 deferrals (F11/F12/F14): not walked.

## Sequencing context

This session is the alignment step before the Phase 1.4 hardening cluster + Safety Portal build. Three follow-on PRs are unblocked once decisions are absorbed:

1. **Taxonomy PR** — add `safety_portal` to `CANONICAL_WORKSTREAMS` lint + CONVENTIONS.md workstream table + execution-repo `its/docs/operations/doc_conventions.md`. Pre-flight per arch doc §0.
2. **Doc-landing PR** — move audit to `audits/2026-05-25_forensic-audit.md` with frontmatter, split arch doc into `workstreams/safety-portal/{mission,brief}.md` per scaffold, apply Q1-Q10 substantive updates, mechanical v11→stable-anchor pass.
3. **Hardening cluster begins** (after taxonomy + doc-landing). First PR: `shared/state_io.py` atomic-write bundle (F19 + F23 + alert_dedupe migration). Then F02 + F22 together. Then F08 + F09 together. Then F16, F17, F18+F03, F04, F10 in parallel-safe order.

Code follow-ons (post-cluster):
- F22 implementation (`shared/approval_verification.py` + `weekly_send_poll` integration + sandbox integration tests).
- F08+F09 implementation (`shared/circuit_breaker.py` + ITS_Config wiring + CIRCUIT_OPEN status surfacing in both daemons + §30 integration tests).
- Q10 implementation (D1 migration + intake.py Stage 12.5 + prune Cron Worker + 24h staleness alert + UI option-a + new `ITS_PORTAL_INTERNAL_API_TOKEN` provisioning).

## Cross-references

- Execution-repo audit (working copy): `~/Downloads/ITS_Forensic_Audit_2026-05-25.md` → lands at `~/its-blueprint/audits/2026-05-25_forensic-audit.md`.
- Safety Portal architecture (working copy): `~/Downloads/safety_portal_architecture.md` → splits into `~/its-blueprint/workstreams/safety-portal/{mission,brief}.md`.
- Foundation Mission v8: `doctrine/foundation-mission.md` — Invariant 1 + Invariant 2 inherited by both workstreams; doctrine updates pending per F02/F22/F07/F13.
- Operational Standards v12: `doctrine/operational-standards.md` — §3 push-vs-record, §31 polling daemons, §34 attachment screening, §35 picklist hardening referenced throughout; doctrine reconciliation pending.
- Memory: `project_ai_one_shot_extensibility.md` — Safety Portal extensibility constraint.
- Prior audits: `audits/2026-05-21_security-hardening-and-doc-drift.md`; `audits/2026-05-24_secret-exposure-audit.md`.
