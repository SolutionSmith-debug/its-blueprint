---
type: doctrine
version: 21
status: canonical
last_verified: 2026-06-29
last_verified_against: f98f56f
supersedes: doctrine/operational-standards.md@v20
workstream: null
tags: [push-vs-record, picklist-hardening, attachment-screening, polling-daemon, sdk-vs-live, cc-tooling, fork-security, pii-logging, actions-version-discipline, code-self-documentation, successor-operator, tier-2-repair, successor-remediation, training-bounded-co-resolution, workspace-topology, standalone-workspace, find-or-create, workspace-membership-approval, box-version-on-conflict, codeql-fp-handling, preservation-for-future-workstream, code-actuation-gate, its-owned-sor-writeback]
---

**ITS Operational Standards v21**

2026-07-06 — v20 consolidation: §§52–54 added (narrated-not-enforced + citation integrity; sandbox-masks-production; runtime secret/PII backstop — its#341); §31/§43 hardened; §23/§24 seventh standalone workspace (ITS — Progress Reporting); §51 Material-List one-way + low-volume period-split folded from the v19.x riders

2026-06-29 — §§50–51 added: the privileged code-actuation gate (§50) + ITS-owned structured-SoR write-back (§51) — ratifying two long-carried propose-only candidates

2026-06-07 — §§45–49 added: five as-built Safety Portal deploy-session patterns generalized to doctrine

*v20 (2026-07-06, verified against exec main `987f4f4`): the operator-directed CONSOLIDATION. **New §§52–54** (its#341 forensic-retrospective candidates): §52 narrated-not-enforced — a built control/guarantee ships a binding test OR a dated exception (curated `narrated_controls` ledger + the citation-integrity leg of the now-BLOCKING drift gate); §53 sandbox-masks-production — the cutover checklist is gated with mechanical pre-cutover verification, not narration; §54 runtime secret/PII-leak backstop (`redact`/no-secret-in-logs on the error_log triple-fire + migrations; + the `security_events` PAT scope). **§31 hardened** (daemon-scaffold DoD: `sys.executable` / `RunAtLoad` / catch-up / empty-commit guard, class #15); **§43 coverage audited** (every Tier-2-reachable capability ships its entry as DoD). **§23/§24 seventh standalone workspace** (`ITS — Progress Reporting`) ratified as the workspace-topology change (v17 sixth-workspace precedent). **§51 folded:** the Material List is one-way-up (phased; M2b bidirectional receive deferred) + the low-volume period-split is a direct clause — folding the 2026-07-04 + 2026-07-06 v19.x riders; the 2026-07-03 Sentry-leg rider likewise folded. No protective claim weakened; every prior § (§§1–51) carries forward verbatim except §31/§43 (amended) + the four folded clarifications. · v19 (2026-06-29, verified against exec main `f98f56f`): §§50–51 ratify two long-carried propose-only candidates. **§50 privileged code-actuation gate** generalizes Invariant 1's two-process model from external transmission to *privileged code/config actuation* (the cloud surface may only queue; the local Mac daemon is the sole actuator; state-machine-stamped; CI-gated synchronous merge; the operator toolchain holds the credentials) — already realized by `publish_daemon.py`; raised first (Safety Portal v4, 2026-06-10). **§51 ITS-owned structured-SoR write-back** blesses ITS as the authoritative writer to a Smartsheet system-of-record it OWNS (the D1 store upstream, the ITS-owned Smartsheet a downstream structured mirror) — one-way-up accumulating logs (hours/equipment), bidirectional split-ownership for the Material List, AND the job-tracker→Active-Jobs write (the portal as the authoritative job creator: identity + active/inactive/archived lifecycle up to the ITS-owned Active-Jobs sheets, so the safety + progress workspaces never drift); guarded by a send-free + AI-free GATED daemon, allowlisted egress, margin-checked find-or-create, a non-clobbering column-scoped write, and period-split + archive-never-delete; ITS-owned SoR ONLY (customer/canonical write-back + PJOB→JOB explicitly out of scope). Every prior section (§§1–49) and the audience-separation principle carry forward verbatim from v18. · v18 (2026-06-07, verified against exec main `f3ad814`): five new sections generalize patterns proven in the Safety Portal deploy-session cluster (exec PRs #178–#189, all merged). **§45 find-or-create-not-strand** (pipeline artifacts auto-provision; transient failure re-pulls, permanent surfaces to the Review Queue — never a silent write-to-nowhere). **§46 workspace-membership = approval authority** — the in-code F22 realization of the §23 principle (approver set resolved live from workspace shares; allowlist retired; fail-closed; the group-share gap and the unasserted owner-inclusion recorded honestly). **§47 Box version-on-conflict** for deterministic-name re-uploads (distinct-document uploads keep suffix-on-conflict). **§48 CodeQL false-positive handling** (per-alert dismissal with a recorded reason; never blanket/per-file suppression of a secret-logging rule; the propose-only triager + agent-scoped dismiss-block hook — newly codified, the rule was previously tooling+memory only). **§49 preservation-for-a-committed-future-workstream** (extends §14 — the Email-Triage email-path retain rationale). Every prior section and the audience-separation principle carry forward verbatim from v17. · v17 (2026-06-05): §23/§24 now acknowledge the Safety Portal's **standalone, approval-gated workspace** (`ITS — Safety Portal`) as an additive, deliberately-scoped exception to the five-workspace audience-separation model — its governing principle is **workspace-membership = approval authority**, and it is self-contained so the safety subsystem ships and hands over independently. Every other section and the audience-separation principle itself carry forward verbatim from v16. — v16 (2026-06-01): The Developer-Operator / Successor-Operator role split, §43, §44's repair-path/escalation structure, and the kill-switch reframe all carry forward. v16 removes the §44 "non-developer-safe enforcement layer" that v15 named as a hard pre-cutover BUILD GAP — there is no structural maintenance enforcement layer and none is built or required. The Tier-2 boundary holds by the trained operator's judgment, the both-rule, and co-resolution with the Developer-Operator until per-category clearance. The Successor-Operator is redefined as a trained operator who runs Claude Code himself (not a Smartsheet-UI-only approver). The Tier-1 self-heal gap survives as a standalone pre-cutover gate (its stale "Check H" status corrected to the implemented Check C marker-file floor in a v16.x absorption — see Authority). No execution-layer mechanism is asserted as built.*

# Purpose

Cross-cutting operational patterns every ITS workstream uses. Each workstream brief and mission file references this doc rather than restating these patterns. When a pattern here changes, it changes for every workstream.

v11 is a full consolidation since v10 (2026-05-21 morning). It folds in the v10.1 overlay (Check G MAINTENANCE-defer) plus the 2026-05-21/22 cascade introducing polling-daemon doctrine (PRs #59 + #60), the pre-Customer-1 security hardening cluster (trusted-contacts + attachment screening + picklist hardening), and the in-repo tech_debt.md as canonical execution-layer log.

# What Changed in v11

- §1 Kill Switch — picklist-hardening forward reference added; Runtime Gate column in ITS_Daemon_Health flagged as future per-daemon switch.

- §2 Daily Watchdog — Check F (Mail.app rule silent disable) flagged for retirement; the implemented staleness floor is the Check C marker-file check (the mechanism this section earlier referenced as a successor "Check H"), which covers all four tracked daemons.

- §3.1 Push-vs-Record Separation — extended to operator visibility (heartbeat row is push; ITS_Errors remains record).

- §24 Sheet-ID Bootstrap — ITS_Daemon_Health + folder 04 — Daemons added (already present in shared/sheet_ids.py).

- §31 NEW — Polling-Daemon-as-Trigger-Primitive Pattern. Codifies emergent pattern (watchdog + picklist_sync + safety-intake all launchd-driven Python pollers).

- §32 NEW — Operator Visibility Surface. ITS_Daemon_Health schema + heartbeat write contract + ARCH-1/2/3 refinements.

- §33 NEW — Trusted-Contacts Sheet Pattern. Replaces ITS_Config JSON allowlists; exact-match + scope + header-forgery.

- §34 NEW — Attachment Screening Pipeline. Four-layer malware defense.

- §35 NEW — Bounded-Enum Picklist Convention. Smartsheet column-type discipline.

- §36 NEW — In-Repo Tech Debt Log. docs/tech_debt.md is canonical execution-layer log; planning-project tech debt scoped to owner-decision items.

- Sections §§4-22, 25-30 carry forward from v10/v10.1 with cross-reference refresh only.

# What Changed in v12

- §37 NEW — CC Skills Usage Convention. mattpocock/skills installed repo-local at `.agents/skills/` with `.claude/skills/` symlinks; 14-skill default install; skills-lock.json pins upstream revisions; auto-recommend list + gated list + not-in-default-install list.

- §38 NEW — Local Agent Guardrails. block-dangerous-git.sh PreToolUse hook with ITS carve-outs; allow plain `git push` and `branch -d` (canonical workflow); block destructive variants.

- §39 NEW — Per-Customer-Fork Security Setup. Mandatory hardening baseline for every customer fork: branch protection, fork-PR approval policy, secret scanning + push protection, Dependabot alerts (NOT auto-fixes), CodeQL default setup.

- §40 NEW — Migration-Script PII Logging Asymmetry. All `scripts/migrations/*` follow this pattern: dry-run path may print PII (operator review); live-write path strips PII (positional indices + system IDs only).

- §41 NEW — GitHub Actions Version-Bump Discipline. Verify latest tag via `gh api`, read release notes for breaking changes, never blanket-upgrade.

- §3.1 Push-vs-Record Separation — cross-reference added: server-side branch protection is the push-layer enforcement that complements the local block-dangerous-git.sh hook (per §38). Direct push to main is blocked at platform layer (server-side), not just at local-hook layer.

- §14 Preservation-over-refactor — cross-reference added: §37's gated-skills list (`improve-codebase-architecture`) requires explicit operator approval per §14. Don't invoke speculatively.

- §30 SDK-vs-Live Integration Test Discipline — cross-reference added: §37's auto-recommend for `tdd` skill applies to new `shared/*` SDK wrappers per §30.

- Sections §§4–22, 25–36 carry forward from v11 with cross-reference refresh only.

# What Changed in v13

One new section captures a discipline whose absence kept surfacing as "future-Seth + future-CC have to leave the file to understand the why":

- **§42 — Code-Level Self-Documentation Discipline.** Mandatory module docstrings with four headings (Purpose / Invariants / Failure modes / Consumers) for every new `shared/*` module and workstream entrypoint. In-code rationale comments for non-obvious decisions, citing the motivating F-finding, session log, doctrine §, or PR. Retrofit existing modules opportunistically per §14.

Cross-references added: §14 ↔ §42 (preservation comments capture the "why we kept this" anchor); §30 ↔ §42 (rationale comments capture the live-API quirk that motivated the integration test); verify-before-fix discipline ↔ §42 (the in-code rationale IS the verification anchor for future-fix decisions).

- Sections §§1–41 carry forward from v12 with cross-reference refresh only.

# What Changed in v14

One reframe corrects a security-posture overstatement the 2026-05-25 forensic audit flagged (audits/2026-05-25_forensic-audit.md, finding F07): §1 was written in a way that invited treating the kill switch as a security control when it is fail-open by design.

- **§1 — Kill Switch reframed.** The kill switch is recategorized as an operator-convenience suggested pause, explicitly NOT a security boundary. It is fail-open on three modes — sheet unreachable / row missing / invalid value all resolve to ACTIVE + WARN — which is intentional (availability is chosen over a hard stop) and is precisely why it cannot be relied on as a control: an adversary who can make the sheet unreachable defeats it, because it fails toward running. A security-relevant halt must come from the External Send Gate (Foundation Mission Invariant 1), which is the real boundary. The mechanism, the three fail-open modes, the picklist-hardening forward reference, and the per-daemon runtime gate are all unchanged; only the framing is corrected. The deferred fail_closed_until timestamp mechanism stays in tech debt and is not implemented here.

- Sections §§2–42 carry forward from v13 with cross-reference refresh only.

# What Changed in v16

v16 removes the Tier-2 "non-developer-safe enforcement layer" framing that v15 introduced and replaces it with the training-bounded co-resolution model. The Developer-Operator / Successor-Operator role split, §43, §44's repair-path / escalation structure, and the v14 §1 kill-switch reframe all carry forward.

- **§44 reframed — the Tier-2 boundary is training-enforced, not structurally enforced.** v15 named a "non-developer-safe enforcement layer" — a structural guard confining a repair session without a developer present — as a hard pre-cutover BUILD GAP. v16 removes that framing: there is no structural maintenance enforcement layer, and none is to be built. The Tier-2 boundary holds by the trained operator's judgment, the both-rule (novel OR high-class → Tier 3), and co-resolution with the Developer-Operator on the four high-class categories until per-category clearance. The capability-gating philosophy still informs how the boundary is drawn; it does not become a built control. (No execution-layer mechanism is asserted as built — still true.)

- **Successor-Operator redefined — a trained operator who runs Claude Code himself.** Not a Smartsheet-UI-only approver rubber-stamping Claude-driven actions: he runs CC, follows the §43 runbooks/checklists, carries out the low-capability-class repair set, and is trained to recognize and escalate the four high-class categories. He is still not a developer (writes no code; performs none of the §§37-41 developer-context operations).

- **Pre-cutover coupling severed.** The Tier-1 self-heal gap (the Check C marker-file staleness floor, §2 — earlier called "Check H") survives as a real pre-cutover gate on its own — narrowed to the weekly_generate Friday-crash catch-up now that Check C covers all four tracked daemons and the F16 ping is live; the v15 "BOTH must be built" coupling to a Tier-2 enforcement layer is removed (there is no such layer). The Tier-2 pre-cutover readiness gate is now the §44 low-capability-class action set implemented as discrete, tested, non-escalating operations + §43 runbooks + the trained-operator / demonstrated-supervised-repair gate (Handover Plan v8 / V&R v9).

- §43 (Successor-Remediation Documentation Discipline), §44's LOW/HIGH capability-class sets, the both-rule, the audit-trail requirement, the §§37-41 role-scope clarifier, and the §§1-42 sections all carry forward from v15.

# §1 — Kill Switch

**What it is — and is not.** The kill switch is an operator-convenience suggested pause: a way for the operator to halt scheduled work cleanly. It is **not** a security control and not a security boundary. It is fail-open by design — if ITS_Config is unreachable, the system.state row is missing, or the value is invalid, the kill switch resolves to ACTIVE (work proceeds) and emits a WARN. That fail-open posture is intentional (availability is chosen over a hard stop) and is exactly why the mechanism cannot be relied on as a control: an adversary who can make the sheet unreachable — or an accidental misconfiguration — defeats it, because it fails toward running, not toward halting. A security-relevant halt must come from a different mechanism: the External Send Gate (Foundation Mission Invariant 1), which is the real boundary — the two-process model means a successful injection at the AI layer still cannot transmit externally regardless of kill-switch state.

ITS_Config Smartsheet (sheet id 3072320166907780, see §24). Tall key/value layout. system.state setting reads ACTIVE / PAUSED / MAINTENANCE. Every Claude Code script reads it first via shared check_system_state() helper. PAUSED = scheduled scripts skip silently. MAINTENANCE = same, but watchdog does not alert. Anyone with edit access to the sheet can flip it.

Status: shared/kill_switch.py wired against ITS_Config via shared.smartsheet_client.get_setting (PR #9, 2026-05-18). Fail-open on three modes — sheet unreachable / row missing / invalid value — with distinguishable WARN messages routed through error_log. The three fail-open modes are intentional; see the reframe above for why they make this a pause, not a control. The deferred fail_closed_until timestamp mechanism (a future option to convert specific failure modes to fail-closed after a bounded window) is tracked in tech debt and is NOT implemented.

## Picklist-Hardening Forward Reference

Pre-Customer-1, the system.state Value cell type should migrate from TEXT_NUMBER to PICKLIST with the enum {ACTIVE, PAUSED, MAINTENANCE}. Eliminates typo/case/whitespace fail-open trigger. Existing fail-open logic stays as belt-and-suspenders for the Smartsheet-unreachable case. See §35 for the system-wide picklist-hardening convention.

## Per-Daemon Runtime Gate (Future)

ITS_Daemon_Health Runtime Gate CHECKBOX column (planned) gives operators per-daemon on/off control from the same surface they use for monitoring. Today's per-daemon kill switches live as separate ITS_Config rows (e.g., safety_reports.intake.polling_enabled). Runtime Gate consolidates these into one operator surface. Bundle with shared/runner.py extraction at second polling-daemon consumer per §14.

# §2 — Daily Watchdog

launchd-scheduled Claude Code script (scripts/watchdog.py) runs daily at 7:00 AM ET. Verifies critical scheduled jobs ran in the last 24 hours, surfaces items past SLA, checks Anthropic spend trend. Silent if green; emails + SMS the operator if anything is off.

Status: 6 of 7 checks live: Check A (stale ITS_Review_Queue, PR #33), Check B (open CRITICALs in ITS_Errors, PR #33), Check C (scheduled jobs last-run markers, PR #36), Check D (14-day reviewer-chain forward scan, PR #36), Check F (Mail.app rule silent disable, PR #36; FLAGGED FOR RETIREMENT per below), Check G (alert dedupe summary sweep, PR #44; MAINTENANCE-defer shipped PR #52).

Check E (Anthropic spend trend) deferred to Phase 1.5 — architectural choice; sandbox spend signal-to-noise too low at $5-credit scale.

## Check F Retirement + Check C Staleness Floor (the successor earlier scoped as "Check H")

Check F polls safety@evergreenmirror.com mailbox idle hours as a proxy for Mail.app-rule health. Post-PR-#59, safety_reports is on a polling daemon. The mailbox-idle proxy is now redundant. The implemented staleness floor is the **Check C marker-file** check: each scheduled job writes a `{slug}.last_run` marker on a completed cycle, and Check C flags any tracked job whose marker is missing or older than its per-job freshness window. Check C already covers all four tracked daemons (safety_intake, safety_weekly_send_poll, safety_weekly_generate, safety_picklist_audit). (An earlier draft of this section scoped a *distinct* "Check H" that would read ITS_Daemon_Health for every Enabled=true daemon and flag rows older than 2 × Interval Seconds; that design was **never built** — the marker-file Check C is the staleness detector that exists, and "Check H" is a naming artifact. Recorded here for provenance.) Retire Check F when (a) the Check C floor covers all daemons [done] and (b) no remaining workstream depends on Mail.app rules.

**Silent fail-open hazards must become watchdog-detectable signals (v15).** Tier 1 of the successor-maintenance model (§44) only works if faults surface. Any condition that today fails silently and is implicitly "deferred to the operator to notice" — a daemon that dies with no heartbeat (audit F17), or a guard hook / worktree control that disappears or is removed without notice — must be promoted to a signal the watchdog (or daemon-health surface) can detect and push, NOT a condition that depends on a human happening to look. The Check C marker-file staleness floor (earlier framed as a "Check H" heartbeat-staleness successor) is the first instance of this principle; the guard-layer-disappearance case (a propose-only block-* hook silently absent because its agent symlink dangles, leaving a session ungoverned — see references/worktree-discipline.md) is a second. Each silent fail-open hazard identified during build is either made watchdog-detectable or logged to tech debt (§36) as an explicit, named gap — never left as an unstated reliance on the operator.

## MAINTENANCE Semantics (carried forward from v10.1)

All push-firing checks honor MAINTENANCE. Checks that emit via log() inherit suppression through severity-downgrade. Check G fires Resend directly and honors MAINTENANCE explicitly via alerts_suppressed parameter. State entries persist as expired+unsummarized; first post-MAINTENANCE sweep fires the deferred digest.

# §3 — Error Logging Pattern

ITS_Errors Smartsheet (sheet id 27291433258884, see §24). Captures every script failure via shared @its_error_log decorator. Severity: INFO / WARN / ERROR / CRITICAL.

Every CRITICAL-severity event fires three independent legs: Smartsheet row (Leg 1, PR #11 — the sole per-occurrence record), Resend operator email (Leg 2, PR #21/#22, subject to §3.2 dedupe), Sentry structured event (Leg 3, PR #23 — subject to §3.2 dedupe on its own namespaced key per the 2026-07-03 v19.x rider below). All legs include Correlation_ID (PR #42) for cross-leg pivoting.

## §3.1 — Push-vs-Record Separation

Dedupe applies only to push, never to records. Resend AND Sentry = the two push legs, both subject to suppression — each gated on its own dedupe key (Resend on `{script}::{error_code}`, Sentry on the namespaced `sentry::{script}::{error_code}`), each leg's window opened only by its OWN successful delivery. ITS_Errors is the SOLE always-write forensic record surface; this module of doctrine must never gate a record-write. This doctrine extends to operator visibility (per §32).

*Amended 2026-07-03, operator-ratified [option 1 of the unbounded-growth audit]: the Sentry free-tier quota burns in ~3.5 days under a CRITICAL storm while protecting nothing ITS_Errors doesn't already record. Sentry reclassified record→deduped-push. Prior text, for provenance: "Resend = canonical push leg (subject to suppression). ITS_Errors + Sentry always write as forensic surfaces." See the v19.x amendment rider under Authority.*

### Extended to Operator Visibility (NEW v11)

ITS_Daemon_Health is a push surface — each daemon's row overwrites every cycle. ITS_Errors remains the forensic record. The two surfaces serve different purposes: heartbeat row tells the operator "is this daemon alive right now"; ITS_Errors tells the operator "what failures happened, when, and how were they correlated." Heartbeat-write failures must NOT block daemon primary work (§32).

## §3.2 — Dedupe Implementation

Per v10.1 prose, extended by the 2026-07-03 v19.x rider. Composite key (script_name, error_code) for the Resend leg; the namespaced `sentry::` + (script_name, error_code) key for the Sentry leg. The two legs deliberately do NOT share a state entry: each leg's window opens (`record_fire`) only after that leg's own successful delivery — sharing one entry would either leave Sentry ungated during a Resend outage (the window never opens, every occurrence burns a Sentry event) or suppress emails nobody received (a successful Sentry capture opening the window while the email leg was down). 60-min window from alerting.dedupe_window_minutes ITS_Config row. First CRITICAL per key per window fires that push leg; events 2-N suppress that leg and increment its counter; ALL events always write the Smartsheet record (ITS_Errors — the sole per-occurrence forensic surface per §3.1 as amended).

Summary delivery via watchdog Check G (daily 7AM ET); a `sentry::`-prefixed key's summary subject is tagged `[sentry-leg]` (prefix stripped for display) so the operator can tell which push leg was suppressed. During MAINTENANCE windows (§2), summary email firing defers; first post-MAINTENANCE sweep fires deferred digest. Phase-2 deletion proceeds during MAINTENANCE (no push surface). Preserves §3.1 doctrine (as amended 2026-07-03).

# §4 — Data Fidelity: No Invented Field Data
> *Reconstructed 2026-07-12 from execution-layer paraphrases; original v10 .docx unavailable — ratify before treating as verbatim.*

ITS never fabricates system-of-record field data it does not hold from a live source. When a structured value — an address, a job attribute, any record field — has no authoritative live source, the cell is left **blank**, and where a downstream decision depends on it the item routes to a human (`ITS_Review_Queue`), never populated with a guessed, inferred, or synthesized value. A blank is honest and recoverable; an invented value is a silent corruption of a system of record (Smartsheet / Box / Outlook are SoR, unchanged by ITS) and is indistinguishable from real data downstream.

Rationale: fabricated field data violates the "failures must be observable, recoverable, and never silent" invariant and the permanent human-in-loop posture. This rule pairs with Foundation Mission Invariant 2 (all content originating outside the operating tenant is untrusted data) and with §5 (confidence scoring) — both refuse false-confident output rather than emit it.

**Status / enforced.** This is realized as a code-level assertion (one of the Op Stds sections cited as code-enforced, excellence-roadmap 2.2). Canonical instance: the six `ITS_Active_Jobs` rows were seeded with **Address cells left BLANK** because no structured live source existed, rather than inventing real addresses; the office PM fills them before Work Location auto-fill can serve values. `scripts/migrations/seed_its_active_jobs.py` marks Address sourcing "§4 — load-bearing: Address is sourced from live data ONLY."

> **Index-stub resolution.** The v10→v20 one-line carry-forward index (`# §§4-22 — Carry Forward From v10`) mislabels §4 as "reviewer chain," duplicating the same label at §15. Every live `§4` code/doc citation is data-fidelity / no-invented-field-data (`seed_its_active_jobs.py`, `docs/tech_debt.md`, the 2026-06-03 session log, `claude-code-info-gap.md`, `memory-archive.md`); the reviewer chain has **zero** §4 citations and lives in the §15–§18 scheduling cluster. §4 is therefore reconstructed as data fidelity and the reviewer chain resolves to §15. [reconstructed — the *content* is well-attested; the §4↔"reviewer chain" title mismatch is the resolution point — confirm against v10 if recovered]

---

# §5 — Confidence Scoring on Extractions
> *Reconstructed 2026-07-12 from execution-layer paraphrases; original v10 .docx unavailable — ratify before treating as verbatim.*

Every extraction or classification step that produces a structured value carries a confidence score, and that score gates acceptance. The system-wide default acceptance threshold is **0.85**: an output scoring below threshold is **not** silently accepted — it routes to `ITS_Review_Queue` with reason `low-confidence-extraction` for human disposition, never treated as a silent success.

Individual workstreams may set a **higher, more conservative** threshold where the cost of a wrong auto-accept is greater; the threshold is configurable per workstream via `ITS_Config`, with 0.85 as the missing-row fallback. Email-Triage classification, for example, starts at **0.90** for its first 30 days and is tuned downward only as a logged reliability record supports it.

Rationale: ambiguity is routed to a human, never auto-approved — the "never silent" invariant plus the permanent human-in-loop rule. Confidence gating and §4 (no invented data) together ensure ITS emits a reviewable gap rather than a confident falsehood.

**Status.** The `ReviewReason` enum in `shared/review_queue.py` carries `low-confidence-extraction` and its sibling `ambiguous-classification`. Cited as "default threshold 0.85 per Op Stds §5" across the safety-reports brief and CLAUDE.md ("Confidence scoring on extractions").

---

# §6 — Structured Output Enforcement
> *Reconstructed 2026-07-12 from execution-layer paraphrases; original v10 .docx unavailable — ratify before treating as verbatim.*

Every Anthropic API call that produces data ITS will act on uses **tool-use to force a JSON-schema-conforming response**. A response that does not conform to the declared schema is **rejected** — not coerced, truncated, or best-guessed — and routes to `ITS_Review_Queue` (reason `structured-output-edge`). This is **Layer 4** of the Invariant 2 adversarial-input defense (Foundation Mission v11); it is one of the real prevention layers (2–4), backed by the two-process External Send Gate (Invariant 1), which is the actual security boundary.

JSON schemas are version-controlled in `schemas/` (paired with `prompts/`), each carries a `version` field, and scripts reject responses on schema mismatch. Schemas and prompts are never inlined ad hoc.

Rationale: structured-output enforcement bounds what a possibly-injected model can hand back to "a schema-shaped object, or nothing" — it cannot smuggle free-form instructions or actions through the response channel. Combined with capability gating (§9), the model's output may be *wrong* but cannot itself transmit or take action; the damage ceiling stays "extracted data is wrong," not "external action taken."

**Scope note.** On the LLM-free Safety-Portal path, Layer 4 is realized as **form-definition schema validation** of the structured payload (client + server, re-validated Python-side before any write); the Anthropic-tool-use form of §6 applies on the preserved email-intake and classification paths (safety-reports Stage 6, Email-Triage). [reconstructed — thin on the exact v10 wording of the reject-mechanism; conservative statement of the rule — confirm against v10 if recovered]

---

# §7 — Sender Allowlist + Scope Enforcement (Invariant 2, Layer 1)
> *Reconstructed 2026-07-12 from execution-layer paraphrases; original v10 .docx unavailable — ratify before treating as verbatim.*

**Rule.** All content originating outside the operating customer tenant is untrusted data (Foundation Mission Invariant 2). The first layer of defense is sender authorization: every intake-bearing workstream verifies the sender against an operator-maintained allowlist before the message reaches any Anthropic call. A sender with no matching authorization is quarantined, never processed silently.

**Header-forgery detection precedes the allowlist lookup.** Because sender identity is only as trustworthy as the mail authentication behind it, authentication headers are checked *before* the allowlist is consulted. The Microsoft Graph API exposes `Authentication-Results`, `Return-Path`, and the `Received` chain on every inbound message; intake parses these (`graph_client` Stage-2 SPF/DKIM/DMARC parser). Any of `{spf=fail, dkim=fail, dmarc=fail, Return-Path domain ≠ From: domain}` routes to `ITS_Quarantine` with reason `header_forgery_suspected` before sender lookup. Softer signals — `{spf=neutral, spf=softfail, dkim=none}` on an otherwise-trusted sender — route to `ITS_Review_Queue` rather than being trusted outright.

**Disposition.** Sender not on the allowlist → `ITS_Quarantine` (reason `sender_not_trusted`). Sender authorized but out of its declared project/workstream scope → `ITS_Review_Queue` (reason `scope_mismatch`). Sender authorized and in scope → proceed to the pipeline. In-code helpers live in `shared/quarantine.py` (`is_allowlisted`, `QuarantineReason`) and the header-verdict module; failures to write a quarantine/review record must propagate so the caller can elevate (an absent audit record is never acceptable).

**Migration path — now extends per §33.** The Phase-1 pattern is a JSON-list allowlist in an `ITS_Config` row. This is superseded by the **`ITS_Trusted_Contacts` sheet pattern codified in §33** — an operator-visible, audit-trail-supporting, scope-enforcing sender-authorization surface. At trusted-contacts cutover the per-workstream `ITS_Config` allowlist rows retire and all intakes read from the sheet. §33 is the canonical implementation reference for the schema, the trust-evaluation logic, and the header-forgery checks summarized here.

**Residual risk.** A sophisticated attacker who compromises a legitimate sender's credentials and transmits through that sender's real mail server bypasses all sender-side defenses; header-forgery detection only catches authentication failures. Layers 2–4 (§§8, 9, 6) still apply, with §10 as a post-hoc detection signal. Under credential compromise the damage ceiling stays "extracted data is wrong," not "external action taken on the attacker's behalf" — the External Send Gate (Invariant 1) remains the boundary.

---

# §8 — Untrusted-Content Tagging (Invariant 2, Layer 2)
> *Reconstructed 2026-07-12 from execution-layer paraphrases; original v10 .docx unavailable — ratify before treating as verbatim.*

**Rule.** Every Anthropic API call that processes content originating outside the operating customer tenant MUST wrap that content with `shared.untrusted_content.wrap()` and include the canonical system-prompt boilerplate from `shared.untrusted_content.system_boilerplate()` in the call's system prompt. This is Layer 2 of the Invariant-2 six-layer defense and applies to every workstream without exception.

**Mechanism.** `wrap(content, source=...)` encloses the external text in `<untrusted_content source="...">` … `</untrusted_content>` tags, and the accompanying system boilerplate instructs the model that anything inside those tags is *data to analyze*, never instructions to follow. The wrapper is defensive against tag-breakout: the closing `</untrusted_content>` sequence in attacker-supplied content is zero-width-broken so the untrusted text cannot emit a premature closing tag and escape its envelope. `wrap()` never raises on a malformed source label (it sanitizes rather than rejects). `shared/untrusted_content.py` is live, tested, and in production.

**Definition-of-done.** Per the "Adding a new workstream" checklist, any prompt that touches external content consumes both `wrap()` and `system_boilerplate()`. This layer does not by itself prevent a determined injection from influencing the model — it establishes the trust framing that Layers 3–4 and the two-process send gate rely on. It is a necessary framing control, not a standalone barrier.

---

# §9 — Capability Gating (Invariant 2, Layer 3)
> *Reconstructed 2026-07-12 from execution-layer paraphrases; original v10 .docx unavailable — ratify before treating as verbatim.*

**Rule.** The AI has no permission to send or to take external action. This is Layer 3 of Invariant 2 and it is the same control as Invariant 1's **two-process model**: generation scripts (which call the Anthropic API) have zero send capability, and send scripts (which transmit) have zero AI step. A successful prompt injection at the AI layer therefore cannot cause an external transmission, because the AI runs in a different process from the transmitter.

**Enforcement — verified in code, not merely asserted.** `tests/test_capability_gating.py` inspects each enrolled script's imports at the AST level and fails the build if a forbidden capability is reachable. Generation/actuation scripts are enrolled in `GATED_SCRIPTS` with a per-script forbidden-substring list — canonically `{send_mail, resend, smtplib, email.mime}`, extended to `{graph_client, anthropic, anthropic_client}` for deterministic (LLM-free) actuators to assert they stay both send-free *and* AI-free. Send scripts are enrolled in `SEND_SCRIPTS` and forbid `anthropic`/`anthropic_client`. `tests/test_intake_capability_gating.py` extends the same discipline to intake paths that aren't part of the generic contract. `shared/graph_client.send_mail` exists to make sending possible for *send* scripts only; the gating test forbids it in every generation process.

**Definition-of-done.** When a new generation script lands, add it to `GATED_SCRIPTS`; when a new send script lands, add it to `SEND_SCRIPTS`. A capability-bearing script that is not enrolled is a gap the test cannot catch — enrollment is part of merging the script, not a follow-up. This is the one Invariant-2 layer that is structurally enforced rather than framing-based, and it is load-bearing precisely because it holds even if injection succeeds at the model layer.

---

# §10 — Anomaly Logging on Extraction Output (Invariant 2, Layer 5 — a detection tripwire, NOT a defense layer)
> *Reconstructed 2026-07-12 from execution-layer paraphrases; original v10 .docx unavailable — ratify before treating as verbatim.*

**Rule and reframe (audit F13, FM v9).** Every extraction output passes through `shared.anomaly_logger.check()` before it is trusted. Layer 5 is a **low-effort post-hoc detection tripwire, not a defense layer** — it does not *prevent* a successful prompt injection. It raises a signal that an extraction output matched a known-suspicious pattern, so the item can be routed to human review and flagged. It must never be relied on as a barrier. Doctrine that treats it as co-equal with Layers 2–4 overstates the protection delivered; FM v9 corrected that framing per audit finding F13, and the correction stands.

**Why it is not a barrier.** The implementation is exact-substring / regex matching against a short sentinel list — trivially evaded by paraphrase or a thesaurus. The actual prevention is Layers 2–4 (untrusted-content tagging §8, capability gating §9, structured-output enforcement §6/Layer 4), backed by the two-process External Send Gate (Invariant 1), which is the real security boundary. Layer 5's value is detection and triage signal, not prevention.

**Mechanism.** `check(extracted_dict)` returns any anomalies found; a non-empty result routes the item to `ITS_Review_Queue` with `security_flag=True` and notifies the owner separately. The Phase-1 sentinel set (`shared/anomaly_logger.py`, live and tested) flags: schema-illegitimate field names (`recipient_override`, `send_to`, `external_address`, `ignore_*`, `role_*`, `system_*`), oversized field values (an injected payload stuffed into a field), well-known injection phrases in any string value, and numeric values exceeding `NUMERIC_ANOMALY_THRESHOLD` (F21) — the in-code backstop to the schema's per-field `maximum` bound. The `SUSPICIOUS_FIELD_PATTERNS` false-positive risk is tracked in `docs/tech_debt.md` for tuning against real extraction outputs; the code is otherwise unchanged and stays in production.

---

# §11 — Python Virtual-Environment & Worktree Isolation
> *Reconstructed 2026-07-12 from execution-layer paraphrases; original v10 .docx unavailable — ratify before treating as verbatim.*

The execution repo is installed as an **editable** package (`pip install -e ~/its`); its strict editable finder resolves every `import` back to the `~/its` checkout even when `PYTHONPATH` points elsewhere, and the launchd daemons run that same `~/its` working tree directly on a ~60 s cadence. There is no build/deploy step between "save" and "production." Two consequences are load-bearing:

- **Any Python-source change is made in a per-task `git worktree` off `origin/main`, never on the live `~/its` tree.** An uncommitted edit saved in `~/its` goes live on the daemons' next cycle; committing in `~/its` mid-cycle can strand the publish daemon on a `publish/req-*` branch. Docs-only edits are safe on the live tree.
- **Each worktree gets its OWN fresh venv — `python3 -m venv .venv-wt && .venv-wt/bin/pip install -e '.[dev]'` — and gates run through `.venv-wt/bin/...`.** **Never `cp -R ~/its/.venv`:** a copied venv's `bin/pip` keeps a shebang hard-coded to the original interpreter, so `install -e .` silently rewrites the **live** `~/its/.venv` editable pointer and repoints production imports at your worktree. Verify with `pip show its | grep 'Editable project location'` — the worktree's must be its own tree and `~/its/.venv`'s must be UNCHANGED.

Corollary — adding a new top-level package/dependency to `pyproject.toml` requires refreshing the live editable install (`cd ~/its && .venv/bin/pip install -e . --no-deps` plus the new dep); the strict finder is baked at install time, so `-m` daemon invocations work but operator smokes break with `ModuleNotFoundError` until refreshed. Canonical procedure: `docs/operations/worktree_discipline.md`.

---

# §12 — Tool-Surface Discipline
> *Reconstructed 2026-07-12 from execution-layer paraphrases; original v10 .docx unavailable — ratify before treating as verbatim.*

Know the boundary of every tool surface before relying on it, and fall back deliberately rather than assuming a primitive exists. [reconstructed — thin evidence; confirm against v10 if recovered]

- **Each MCP surface has gaps; the underlying SDK is the fallback of record.** The Smartsheet MCP exposes `delete_rows` and column-level ops only — it has **no `delete_sheet` / `delete_folder` / `delete_workspace`**; the Box MCP has **no delete primitive at all**; the Reports MCP is read-only (`create_report` needs a direct REST fallback). Any teardown or unsupported op uses the underlying Python SDK client (`smartsheet_client`, `box_client`) directly.
- **Destructive SDK operations are name-guarded with a hard-coded allowlist.** A bulk sheet/folder deletion script must gate on an explicit allowlist of names, never a pattern that could match a live artifact.
- **The AI's own tool surface is conservative by default and widened only by capability review.** A reasoning/chat agent's initial tool set is read-only (Smartsheet, Box, review queue); promotion to any write- or draft-tool requires an explicit per-tool capability review — consistent with the Invariant-1 capability-gating posture (§9), never a blanket grant.

Rationale: an unexamined tool surface produces either a silent no-op (the primitive was never there) or an over-broad blast radius (a destructive op with no guard). Both are "never silent / never unbounded" violations; naming the fallback and the guard up front is the discipline.

---

# §13 — Diagnostic Discipline
> *Reconstructed 2026-07-12 from execution-layer paraphrases; original v10 .docx unavailable — ratify before treating as verbatim.*

Hard bugs and performance regressions are worked through a disciplined loop, not by speculative patching: **reproduce → minimise → hypothesise → instrument → fix → regression-test.** Reproduce the failure deterministically; minimise to the smallest triggering input; form a single explicit hypothesis; instrument to confirm or kill it before touching the fix; then land a regression test that fails on the old code and passes on the new. The `diagnose` skill drives this loop.

- **This is the standard response to the SDK-vs-Live bug class** — the recurring failures where a mock passes but the real Smartsheet / Box / Graph SDK rejects the call. Any bug investigation touching an SDK boundary runs the loop; the fix ships with a live smoke on top of the regression test (a green mock proves nothing here — see §30 integration discipline).
- **Not every failure is a code regression — classify before chasing.** An externally-caused fault (an org-wide GitHub-Actions billing outage, a CodeQL infra-fail, an SDK eventual-consistency flake) is diagnosed as non-code from its signal (job annotation, error code) and *not* pursued as a regression. Misclassifying an environmental fault as a code bug burns the loop on a fix that cannot exist.

Rationale: the loop forces the failure to be understood before it is "fixed," so the fix addresses the actual mechanism and the regression test locks it — the opposite of the patch-and-hope pattern that leaves a bug latent behind a passing suite.

---

# §14 — Preservation over Refactor
> *Reconstructed 2026-07-12 from execution-layer paraphrases; original v10 .docx unavailable — ratify before treating as verbatim.*

**Working code is preserved, not rewritten for style.** This section is non-negotiable — it was hardened after the chat-session-to-Claude-Code code-landing pattern produced repeated ruff/mypy churn (rewrites of correct code to satisfy a linter). The default is to leave working code alone.

- **Lint/type friction is resolved by an ignore, not a rewrite.** When chat-landed code trips ruff/mypy, the §14 path is `[tool.ruff.lint.per-file-ignores]` in `pyproject.toml`, never a rewrite of the working code. Exception: genuinely dead code (not a stylistic false positive) may be deleted with the ignore. Canonical examples: PR #4 (`1295a93`), PR #8 (`parse_job_v3` F841 closure).
- **Speculative refactors clear a high bar: ≥4 real reuse cases.** A refactor/extraction proposed for its own sake (e.g. `improve-codebase-architecture`) does not run until the operator confirms the target meets the **≥4 genuine reuse cases** threshold. Duplication below that bar is preferred over a premature abstraction.
- **Parameterize, not clone — when a real second consumer appears.** A genuine second consumer of a pattern is served by parameterizing the existing module (a required, no-default config object bound by each caller) rather than copy-pasting it, and the change is **byte-identical for the original caller when the new parameter is unset** — the additive path must not alter existing behavior. This is the standing idiom across `generate_core` / `compile_core` / `week_sheet` / `weekly_send` / `compile_now_poll` (each carries an in-code `§14` note); a cross-consumer contamination guard (e.g. a `Workstream`-tag mismatch hard-held before any send) is part of the pattern.
- **Extraction is deferred until the pattern actually recurs, and even a met threshold may stay deferred.** A shared helper is extracted at the real second consumer with matching shape (e.g. `shared/runner.py` at the second polling daemon; the heartbeat extraction), but §14 preservation can still defer an extraction whose threshold is met (the triple-fire helper at its 4th consumer, §27). Where a cheap parity **test** guarantees two near-identical surfaces stay aligned, prefer the test over forcing a shared module (`tests/test_heartbeat_parity.py`).
- **A clean-break that retires an input/trigger preserves workstream-agnostic infrastructure a committed future workstream depends on** — tombstone only the superseded entry-point and record the retention rationale so a later "cleanup" does not delete the seed (extended as §49; e.g. the Email-Triage email-path retain).

Rationale: the §14 invariant supersedes "cleaner code is better." Preserving working code keeps the diff small, keeps behavior byte-identical for existing callers, and avoids the churn-and-regression risk that a stylistic rewrite reintroduces on a production tree the daemons run directly.

---

# §15 — Reviewer-Chain Resolution (PTO-aware shift-up)
> *Reconstructed 2026-07-12 from execution-layer paraphrases; original v10 .docx unavailable — ratify before treating as verbatim.*

Where §4 defines the reviewer chain as a *composition* — three positional slots, primary → secondary → tertiary, each an email, with `delay_to_secondary_hours` / `delay_to_tertiary_hours` measuring the hours after an item lands in the queue before the next slot is paged — **§15 defines how that chain is *resolved* for a given workstream on a given date**, with PTO applied. This is the runtime mechanism, not the roster.

- **Positional offsets, not fixed people.** The chain carries positional offsets `[0, delay_to_secondary_hours, delay_to_tertiary_hours]`. Resolution removes anyone currently out (per §16 ITS_Time_Off) and the **surviving members shift up** into the remaining positions: when the primary is out, the secondary takes the 0-hour slot and the tertiary takes the secondary offset. Coverage is never dropped or paged late merely because an earlier slot is unavailable.
- **PTO-aware by construction.** Resolution consults the live PTO source (§16) for each candidate on the target date. A reviewer covered by a time-off entry on that date is excluded before offsets are assigned.
- **Empty chain is a first-class signal, never an auto-route to someone else.** When *every* configured reviewer is out, resolution returns an **empty chain**. Callers treat this as "hold the week and alert the operator out-of-band (Resend)" — the system never silently reassigns the review to an unconfigured party. (Realized in `shared/scheduling.py::resolve_chain` / `ReviewerChain.is_empty`.)
- **Config source is §26.** The chain *composition* is read from ITS_Config with a `shared.defaults.DEFAULT_REVIEWER_CHAINS` fallback (§26 owns the configuration-source rule); §15 governs only the PTO-applied resolution over that composition.

*Disambiguation note: v10 labels both §4 and §15 "reviewer chain," and §26 "reviewer-chain configuration source." The §4-roles / §15-resolution-mechanism / §26-config-source split above is inferred from the live code's separation of `ReviewerChainConfig` (composition), `resolve_chain` (resolution), and `ChainConfigLoader` (source) and from §18's citation of the resolution as the thing it forward-scans — not from a recovered v10 boundary. [reconstructed — thin evidence for the exact §4/§15/§26 partition; confirm against v10 if recovered]*

---

# §16 — ITS_Time_Off (PTO source of truth)
> *Reconstructed 2026-07-12 from execution-layer paraphrases; original v10 .docx unavailable — ratify before treating as verbatim.*

**ITS_Time_Off is the canonical Smartsheet source for reviewer/personnel time-off.** Reviewer-chain resolution (§15) and the 14-day forward scan (§18) both read it to decide who is unavailable on a given date. The module that reads it is identity-free by design — identities live in ITS_Config / `shared.defaults`, not in the scheduling code.

- **Schema (as read by `shared/scheduling.py`).** One row per PTO span: `Person` (CONTACT_LIST), `Start Date` (DATE), `End Date` (DATE). The date range is **inclusive on both ends**; `Start Date == End Date` expresses single-day PTO.
- **Retroactive entries are honored.** A row added today for a date already in the past affects any lookup whose date falls inside the range, regardless of when the row was created — the entry, not its authoring time, is what matters.
- **Fail-open on read failure.** If the sheet is unreachable, auth is rejected, the sheet is missing, or the payload is malformed, the fetch emits a WARN via `error_log` and returns "nobody is out" (`[]`) rather than raising. A downstream coverage check would rather miss a gap than crash the whole run; the morning log scan reveals which fetch failed and why. (Consistent with the §1 kill-switch / §27 failure-isolation fail-open posture — never silent, but never fatal.)
- **Per-row robustness.** A single malformed row (unrecoverable email, unparseable dates) is skipped with a WARN; the remainder of the sheet still loads. One bad row must not poison the fetch.
- **Read amplification is bounded.** A single run constructs one PTO client and caches the fetch for that client's lifetime, so a multi-day, multi-reviewer scan produces a single Smartsheet read; a new run re-fetches (and thus sees newly-added entries).

---

# §17 — Federal-Holiday Business-Day Rule
> *Reconstructed 2026-07-12 from execution-layer paraphrases; original v10 .docx unavailable — ratify before treating as verbatim.*

**All scheduled date math is business-day-aware against the US federal holiday calendar.** A business day is Monday–Friday that is **not** a US federal holiday (including federally *observed* dates). The customer's business runs on the US **federal** observance calendar; state and bank holidays are intentionally excluded. (Realized via `holidays.country_holidays("US")` in `shared/scheduling.py::is_federal_holiday` / `_is_business_day`.)

- **Generation rolls back; sends roll forward.** A generation run scheduled the business day *before* a send shifts **back** to the most recent business day on or before its target (`shift_gen_date`). An externally-visible send shifts **forward** to the next business day on or after its target (`shift_send_date`) — a send must land on a day someone is actually at work.
- **Recursive over multi-day spans.** The shift steps one day at a time until it lands on a real business day, so back-to-back non-business days (weekend abutting a holiday, or two adjacent holidays) still resolve to a genuine business day.
- **Week-boundary selection is deliberately holiday-unaware.** Picking a calendar-week boundary (e.g. the Monday on or before a date) selects the week, not a business day; pair it with the gen/send shift when the run day itself needs holiday handling. The two concerns are kept separate on purpose.

---

# §18 — 14-Day Reviewer-Chain Forward Scan
> *Reconstructed 2026-07-12 from execution-layer paraphrases; original v10 .docx unavailable — ratify before treating as verbatim.*

**The daily watchdog forward-scans reviewer coverage so a gap is surfaced before it bites, not after a report is stuck with no reviewer.** This is watchdog **Check D**. For each scanned workstream it walks the next **14 days** (`REVIEWER_CHAIN_SCAN_DAYS`), skipping federal holidays (§17 — the business needs no coverage on a closed day), and resolves the reviewer chain (§15, PTO-aware via §16) for each business day. A day whose resolved chain is **empty** is a coverage gap.

- **Forward-looking, complements the reactive checks.** Where other watchdog checks flag things already stale, §18 is anticipatory: it tells the operator *now* that an upcoming window has no available reviewer, giving time to add coverage or adjust PTO/config before the gap arrives.
- **Routes to the human review surface, one row per workstream.** Detected gaps are logged to `ITS_Review_Queue` as an INFO anomaly row **per workstream** (one row collecting all of that workstream's gap dates, not one row per gap), so the operator sees a single triage item rather than a flood.
- **Triage-window tuning.** The anomaly rows are written with a `reason`/`sla_tier` chosen so the stale-review detector (Check A) grants a multi-day triage window before re-WARNing, rather than immediately re-alerting on a known, already-surfaced gap.
- **Known behavior (documented, accepted).** Check D does **not** deduplicate across runs — a persistent gap produces one new row per watchdog run. This was accepted at build time; scan-for-existing-row dedupe is a future enhancement if proliferation becomes painful.

---

# §19 — Smartsheet UI-Only Constraint
> *Reconstructed 2026-07-12 from execution-layer paraphrases; original v10 .docx unavailable — ratify before treating as verbatim.*

A set of Smartsheet operations have **no API / SDK / MCP primitive** and can only be performed through the Smartsheet web UI: **forms, conditional-formatting rules, filters, and sheet-level column changes** (adding a column to — or retyping a column on — a live sheet). This is a platform constraint, not an ITS choice, and it splits the build labor: **data flows via API/scripts; the UX layer (forms + conditional formatting + filters) is authored once per template sheet in the UI, then propagated to project clones via Save-as-New** (which carries the forms/CF/filters onto each clone). Related: the §35 bounded-enum picklist retrofit and any column-type change are UI-only for the same reason (no API primitive; operator UI required, ~30 s per column).

**Consequence — Notes-encoded machine state.** Because a script cannot always add a purpose-built managed column to a live sheet, per-row machine state that has *no dedicated column* is encoded into the free-text **`Notes`** cell as a machine-parsable tag prefix — **parse-on-read, replace-or-append-on-write**. Canonical uses: `weekly_send` retry state (`[SEND_RETRY_COUNT: N]`, `[LAST_SEND_ERROR: …]`) on `WSR_human_review`, which has no `Send Retry Count` / `Last Send Error` columns; and the D1-join ids (`d1_id=<n>` / `po_id=<n>` / `sc_id=<n>`) that bind an ITS-owned Smartsheet ledger row back to its authoritative D1 record. A row that loses its tag cannot be machine-resolved — that condition is **surfaced, never guessed** (a numberless PO refuses to send rather than fabricate its number). The encoding is deliberately confined to `Notes`; the reviewer edits only human columns (e.g. `Email Body`), never `Notes`.

*(Historical note: `weekly_send.py` at one point cited a non-existent "§23.3" for the UI-only-column constraint; the canonical home is §19 — tracked as a retarget in `docs/tech_debt.md`.)*

---

# §20 — Remote Access
> *Reconstructed 2026-07-12 from execution-layer paraphrases; original v10 .docx unavailable — ratify before treating as verbatim.*

**All remote access to the ITS host is via Tailscale only. Never expose SSH — or any service — to the public internet.** ITS's own operation requires only **outbound 443** (Smartsheet, Box, Microsoft Graph, Anthropic) — there are **no inbound holes and no public SSH**. Any locally-bound surface (e.g. the operator dashboard on `127.0.0.1:8484`) is reached from other devices **only over the tailnet**, never on `0.0.0.0` and never published — the same "no public-internet service" rule applies to everything in the repo.

Tailscale is the **Tier-3 escalation / remote-support channel for the Developer-Operator (Seth)** — reached for novel or high-capability-class faults — **not** the primary ongoing-operation model. Steady-state operation is Tier-1 self-heal plus the Tier-2 Successor-Operator (see the three-tier maintenance model); the earlier framing that positioned remote support as the standing operator model is superseded. Reverse-access must be verified from a foreign network (a hotspot, not the home/work LAN) before shipment to prove it survives the customer's NAT. **Fallback if Tailscale fails post-shipment:** physical access + a video-call walkthrough, with the hardware-refresh budget (§21) covering a replacement-Mac shipment if remote recovery proves impossible.

---

# §21 — Hardware Lifecycle
> *Reconstructed 2026-07-12 from execution-layer paraphrases; original v10 .docx unavailable — ratify before treating as verbatim.*

ITS is **local-first on a single MacBook host through Phase 4** — no cloud-server execution is added; each customer runs on their own physical host. The build follows the sandbox-first pattern and then cuts over to the customer site: **Florida (build/dev) → California (customer site)**, with the **production host being the old MacBook Pro** migrated onto and installed at Evergreen at the in-person delivery (target **Aug 7**; the migration off the development MacBook onto the production host is procedure-driven with a **zero double-run window**, per `docs/operations/host_migration_runbook.md`). Post-handover the production MacBook is **customer-owned, sitting at the customer site**, maintained by Solution Smith remotely over Tailscale (§20).

**Refresh cadence:** approximately **$1,200 every 3–4 years, a customer responsibility** — the same budget that funds a replacement-Mac shipment if remote recovery is ever impossible. Because the architecture is deliberately single-host, host death is the dead-man's-switch case (external UptimeRobot ping) and hardware replacement, not failover, is the recovery path. *[reconstructed — thin evidence; confirm against v10 if recovered]*

---

# §22 — Box Paths
> *Reconstructed 2026-07-12 from execution-layer paraphrases; original v10 .docx unavailable — ratify before treating as verbatim.*

**Box is a document system of record, unchanged by ITS.** Never construct a Box path inline — **resolve every path through `shared/box_client.py` helpers** so a single edit propagates to all callers (`canonical_job_path(customer, job_number, job_name, year)` is the canonical write-path helper; ITS auto-creates job/week folders through the idempotent, race-tolerant find-or-create `get_or_create_folder`). Per-customer project-folder resolution lives in **`shared/defaults.py::BOX_PROJECT_FOLDERS`** — a `project-name → Box folder ID` map, each ID a per-project clone of the canonical **`1111B`** template under the **ITS DATA root** (`382010286207`). This map is a **per-customer-repo invariant: replace it at fork time**; `ITS_Config` rows override at runtime, and the defaults are the missing/invalid-row fallback. Superseded/legacy clones stay **archived, not deleted, for ≥30 days** (§14 preservation), under `ITS DATA / 99. Legacy … Clones /`.

**Filing structure is `ROOT → per-job → per-week`.** Per the operator naming rule, folders ITS creates are **prefixed `ITS`** so the system's own folders are distinguishable from the pre-existing job/category tree. The Box tree **mirrors the Smartsheet job/week hierarchy** (via the shared naming helpers); the compiled weekly packet is filed to the ITS-prefixed week folder, and sanitized photo originals file to **`ITS Photos/<submission_uuid>/`** under the job folder. *(The `ROOT → job → week` mirror and the `ITS`-prefix naming rule are the current as-built realization of this section; the durable v10 rule is "Box is the SoR; resolve all paths through the `box_client` helper + the `BOX_PROJECT_FOLDERS` map, never inline.")*

---

# §23 — Workspace Topology

Five-workspace audience-separated model. Customer-facing: Forefront Portfolio + Human Review. Operator-only: Operations (master DBs), Archive (closed projects), System (config/errors/queues/daemons). The audience-separation model carries forward from v10 §23 unchanged.

**v17 addition — sixth, standalone workspace: `ITS — Safety Portal`.** The Safety Portal subsystem owns a **standalone, self-contained workspace** that sits **outside** the audience-separation model on purpose, governed by a different principle: **workspace membership = approval authority** — the collaborators shared into the workspace are exactly those who may review / edit / approve the weekly safety report in `WSR_human_review`, so the share list *is* the External Send Gate (§1) access control for that workstream. The workspace is self-contained — the `Safety Portal` folder (`ITS_Active_Jobs`, `ITS_Forms_Catalog`), the per-job week sheets, and `WSR_human_review` all live in it — so the safety subsystem can be stood up, demoed, and handed over independent of the Forefront / demo / Operations structures; shared infrastructure config stays in `ITS — System`, read by ID. This is an **additive, deliberately-scoped exception**, not a change to the audience-separation principle, which is unchanged for every other workstream. The folder was moved from `ITS — Operations` with IDs preserved (see §24). Originating rationale: [Safety Portal mission §8](../workstreams/safety-portal/mission.md#8-self-containment-and-workspace-as-approval-authority).

**v19.x sync — seventh, standalone workspace: `ITS — Progress Reporting`.** The Progress-Reporting subsystem (the safety-pipeline twin) owns its own **standalone, self-contained workspace** governed by the SAME principle as the sixth — **workspace membership = approval authority** (its shares are exactly the approvers of the weekly progress report in `WPR_human_review`; §46). It is self-contained: the `Control` folder (`ITS_Active_Jobs_Progress`, `WPR_human_review`), the per-job progress week sheets, and the standing per-job §51 trackers (Hours Log / Equipment / Material List) all live in it — so the progress subsystem ships and hands over independent of the Safety-Portal / Forefront / Operations structures; shared config stays in `ITS — System`, read by ID. A **further additive instance of the v17 standalone-workspace exception**, not a new change to the audience-separation principle. **Ratified at v20** (2026-07-06 consolidation): §51 (v19) already named this workspace as an ITS-owned SoR; **v20** syncs §23's enumeration to match and records the seventh standalone workspace as part of the workspace-topology change this bump carries (the v17 precedent major-bumped for the *first* standalone workspace; v20 lands the seventh alongside the §51 SoR-write/Material-List clarifications and the its#341 §§52–54). Originating rationale: [Progress-Reporting mission](../workstreams/progress-reporting/mission.md) + the v19 §51 workspace naming.

# §24 — Sheet-ID Bootstrap

Workspace/folder/sheet ID inventory. Source of truth is shared/sheet_ids.py. v11 inventory refreshed:

- Workspaces: Forefront Portfolio 4129485730670468, Human Review 8561891980142468, Operations 7217130472007556, Archive 5528280611743620, System 680592632244100, **Safety Portal 194283417429892 (NEW v17, `WORKSPACE_SAFETY_PORTAL`)**, **Progress Reporting 5988851429730180 (NEW v19.x, `WORKSPACE_PROGRESS_REPORTING`)**.

- System folders: 01—Config 164788727768964, 02—Logs 5231338308560772, 03—Queues 7201663145535364, 04—Daemons 2130046845511556 (NEW PR #59/#60).

- Safety Portal workspace contents (NEW v17): folder `Safety Portal` (`FOLDER_SAFETY_PORTAL` 6663869084002180 — moved from `ITS — Operations` 2026-06-05, ID preserved; `FOLDER_OPERATIONS_SAFETY_PORTAL` retained as a back-compat alias) holding `ITS_Active_Jobs`, `ITS_Forms_Catalog`, and `WSR_human_review` (`SHEET_WSR_HUMAN_REVIEW`, PR #168 — supersedes `WPR_Pending_Review` for the safety flow).

- System sheets: ITS_Config 3072320166907780, Picklist_Sync_Config 7486553185013636, ITS_Errors 27291433258884, ITS_Quarantine 8687740798324612, ITS_Review_Queue 7243317526876036, ITS_Daemon_Health 4529351700729732 (NEW PR #59/#60).

- Active project folders: Bradley 1/2, Brimfield 1/2, Huntley, Rockford — see shared/sheet_ids.py FOLDER_PROJECT_* constants.

- Field Reports project subfolders: 6 per-project subfolders — see FOLDER_FIELD_REPORTS_* constants.

# §25 — Per-Workstream Sheets
> *Reconstructed 2026-07-12 from execution-layer paraphrases; original v10 .docx unavailable — ratify before treating as verbatim.*

Each workstream owns its own dedicated Smartsheet sheets rather than co-tenanting rows in a single monolithic sheet. A workstream's structured data — its intake/queue rows, its per-item working rows, and its `<Workstream>_Pending_Review` approval sheet (Invariant 1) — lives in sheets scoped to that workstream and placed in the workspace its audience is entitled to (§23). This keeps audience separation (§23), the per-workstream External Send Gate (Invariant 1), picklist/config scoping (§35), and the reviewer chain (§26) all resolvable one workstream at a time.

Consequence: a new workstream provisions its own sheets (mirroring the `safety_reports/` shape) rather than adding columns to another workstream's sheet; cross-workstream reads go by sheet-ID through `shared/sheet_ids.py` (§24), never by sharing a row surface.

[reconstructed — thin evidence; confirm against v10 if recovered]

Note (version-drift guard): some in-repo code and docs (`shared/picklist_sync.py`, `docs/tech_debt.md`) historically cite "§25" for an unrelated "MCP-gap REST fallback" workaround. Those are flagged in-repo as renumbering mis-cites to be retargeted — the canonical scope of §25 in the live standard is *per-workstream sheets*, not the REST fallback. See the ambiguity note at the end.

---

# §26 — Reviewer Chain Configuration Source
> *Reconstructed 2026-07-12 from execution-layer paraphrases; original v10 .docx unavailable — ratify before treating as verbatim.*

The reviewer chain's *composition* — who occupies the primary / secondary / tertiary slots for a given workstream, and the delay-to-next-slot hours — is configuration, not code. It is read at runtime from `ITS_Config`, which takes precedence whenever readable. The fallback — used before the sandbox config sheet is provisioned, and as the first-run seed — is `shared.defaults.DEFAULT_REVIEWER_CHAINS`.

Reviewer identity (emails) MUST NOT be hardcoded in `shared/scheduling.py`. Identity references live only in `shared/defaults.py` and `ITS_Config` — a single place a planning-layer human updates when this customer's chain changes. `scheduling.py` reads composition, applies PTO removal (§16) and federal-holiday shifts (§17), and resolves the ordered chain; it never embeds the roster. A missing row in both sources is a loud error ("No reviewer chain configured for workstream …"), never a silent empty chain.

This is distinct from §4/§15, which govern the reviewer-chain *mechanics* (three-tier escalation) and its 14-day forward scan (§18): §26 governs where the chain *comes from*.

---

# §27 — Triple-Fire Failure Isolation
> *Reconstructed 2026-07-12 from execution-layer paraphrases; original v10 .docx unavailable — ratify before treating as verbatim.*

The CRITICAL alert path fires on three legs (see §3 / §3.1): the `ITS_Errors` Smartsheet row (the per-occurrence RECORD leg) plus two out-of-band PUSH legs — a Resend operator email and a Sentry capture. Each leg is independently **recursion-guarded** and wrapped in a **broad `except`**, so a failure in one leg never blocks the others: an M365/Smartsheet outage that suppresses its own alert row must not suppress the Resend + Sentry legs, and vice-versa. The `Correlation_ID` is threaded across all three legs so an operator can join them.

The isolation rule generalizes beyond alerting: an auxiliary or observability path must never crash the primary work. A deliberately broad catch — e.g. the PTO fetch in `shared/scheduling.py` returning `[]` fail-open rather than crashing the watchdog — is a §27 application, not a lint smell.

`shared/alert_dedupe.py` is the fourth consumer of this path (it gates the two push legs on `(script, error_code)`). The shared-helper extraction threshold has been met but is **deferred per §14** (preservation-over-refactor) — the legs stay inline until a genuine reuse case justifies extraction.

---

# §28 — mypy-in-CI
> *Reconstructed 2026-07-12 from execution-layer paraphrases; original v10 .docx unavailable — ratify before treating as verbatim.*

`mypy` runs in the GitHub Actions `test` job as a **blocking** gate on every push, held at a **zero-error baseline**. A push that introduces a type error fails CI and does not land. Run `mypy .` locally before pushing — `pytest` + `ruff` alone do not surface type regressions.

The baseline is maintained at 0 errors across all source files; session-log landing assertions record the count ("mypy: 0 errors / N source files") as proof the gate stayed green. §28 is one of the Operational Standards enforced directly in code rather than by convention.

---

# §29 — Managed Agents Architectural Framing
> *Reconstructed 2026-07-12 from execution-layer paraphrases; original v10 .docx unavailable — ratify before treating as verbatim.*

Managed Agents (autonomous, judgment-bearing Claude agents embedded in ITS) are governed by one framing: **"Python = deterministic plumbing, Agents = judgment-gaps between them."** Deterministic work — moving data, rendering, filing, sending under the gate — stays in Python. An Agent is introduced only to fill a genuine judgment gap *between* deterministic steps, never to replace plumbing a script already does correctly.

No Managed Agents exist in Phase 0 / 1 / 1.5 / 1.6. Agent adoption is evaluated at a single **Phase 3 gate**, where each candidate is tested for **capability-equivalence against Invariants 1 & 2** — an Agent may not weaken the External Send Gate or the adversarial-input posture. The four candidate workstreams considered at that gate are **Closeout Package Assembly, Schedule Digest, Dreaming, and the ITS Chat backend re-evaluation**. This candidate list is planning input, not a roadmap promise; the capability set is re-verified when the gate actually fires.

---

# §30 — SDK-vs-Live Integration Test Discipline
> *Reconstructed 2026-07-12 from execution-layer paraphrases; original v10 .docx unavailable — ratify before treating as verbatim.*

Any new `shared/*` SDK wrapper that performs **create / update / delete on typed columns or rows** (Smartsheet, Box, Graph, …) ships with a **paired integration test** — `tests/test_<client>_integration.py` — that exercises the **live API against throwaway sandbox resources**, not mocks.

Rationale (codified across PRs #47/#48/#49/#51 — four SDK-vs-Live bugs in two days): `SimpleNamespace` mocks at the SDK boundary pass while the live API rejects. Mocks cannot see live-API enforcement (required fields, body shape, value wrapping/coercion) or SDK runtime state (in-process caching). A green mock test therefore proves nothing about the real call.

Convention:

- Mark the test `-m integration`; **CI skips it by default** — it is operator-run against sandbox resources (create → read/write → delete round-trip).
- The `sdk-integration-test-scaffold` agent scaffolds the paired test immediately after a wrapper is created or significantly changed.
- The discipline extends to **daemon integration and any new shared infrastructure** (a breaker, a rate cap, a new exception subtype): mandatory manual **live smoke on the actual daemons before merge**, because existing unit-test mocks predate the new cross-cutting module and cannot exercise it.
- A deliberately **read-only** wrapper with no write path does not fire §30 (e.g. `shared/active_jobs.py`).

---

# §31 (NEW) — Polling-Daemon-as-Trigger-Primitive Pattern

Codifies the launchd-driven Python polling daemon as the canonical trigger primitive for all intake-bearing and scheduled workstreams. The pattern was emergent across watchdog (PR #36) and picklist_sync (PR #46) before being formally identified during the PR #59 safety-intake cutover; v11 §31 names it.

## Pattern

Every polling daemon is structurally identical:

- launchd plist in scripts/launchd/org.solutionsmith.its.<daemon>.plist — owns interval and process invocation.

- Python entry point at <workstream>/<daemon>.py — single poll cycle, exits after one pass.

- ITS_Config triplet per daemon: <workstream>.<daemon>.poll_interval_seconds, .source (mailbox/sheet/path), .polling_enabled (runtime gate).

- State files at ~/its/state/<daemon>_*.json for cross-cycle persistence (row-id caches, processed-message sets, cycle counters).

- Heartbeat write to ITS_Daemon_Health each cycle (§32).

- Conventions: plist label org.solutionsmith.its.*; log path ~/its/logs/launchd/<daemon>.{out,err}.log.

## Definition-of-done (hardened — v20, forensic class #15)

Every daemon scaffold's DoD includes, explicitly (the 2026-06-28 retrospective found several narrated-but-missing): **`sys.executable`** for every subprocess (never a bare `python` — the launchd PATH may not resolve the venv interpreter); **`RunAtLoad=true`** on every interval plist (single-host architecture → a reboot must not leave daemons dead until the next interval fires); an **external catch-up detector** for every calendar-scheduled job (a missed fire is invisible to the daemon itself — the watchdog is the catch-up asset, per §32); and a **guard against empty-commit / no-op crashes** in any daemon that does git work (a publish/mirror daemon must not crash on "nothing to commit"). These are §52-enforced where a test can bind them.

## Existing Daemons (Roster)

| **Daemon** | **Interval** | **Source** | **Heartbeat Status** |
| --- | --- | --- | --- |
| watchdog | Daily 7AM ET | Multi-source | Retrofit pending |
| picklist_sync | Hourly | Picklist_Sync_Config + master DBs | Retrofit pending |
| safety_reports.intake_poll | — | (Graph email intake) | RETIRED 2026-06-05, tombstone DELETED 2026-07-03 — superseded by the Safety Portal PULL model (portal_poll.py) |

## Future shared/runner.py Abstraction

At second polling-daemon consumer with heartbeat shape (i.e., after watchdog or picklist_sync retrofit), extract shared/runner.py per §14 preservation-over-refactor. Signature: run_loop(daemon_name, interval_provider, cycle_fn) where cycle_fn returns (status, items_count, err_summary, err_corr_id). Handles heartbeat write, sleep, kill_switch check, exception isolation.

# §32 (NEW) — Operator Visibility Surface

ITS_Daemon_Health sheet in System workspace / 04 — Daemons folder (sheet 4529351700729732, folder 2130046845511556). One row per daemon, update-in-place every cycle. Push surface per §3.1.

## Schema

12 columns per shared/sheet_ids.py DAEMON_HEALTH_COLUMNS dict. See ITS_Daemon_Health_Schema_2026-05-21.docx for full schema reference.

- Daemon Name (PRIMARY TEXT_NUMBER) — dotted-notation identifier.

- Workstream (PICKLIST: global, safety_reports, progress_reports, field_ops, po_materials, subcontracts, email_triage, ai_employee).

- Enabled (CHECKBOX) — report-filter metadata only; daemon does NOT read this (ARCH-1).

- Interval Seconds (TEXT_NUMBER) — planning placeholder; runtime daemon reads its own ITS_Config row.

- Source ID (TEXT_NUMBER) — mailbox/sheet/path.

- Last Heartbeat (TEXT_NUMBER ISO 8601 UTC).

- Last Cycle Status (PICKLIST: OK, WARN, ERROR, SKIPPED, NEVER_RAN, STALE).

- Last Cycle Items Processed, Total Cycles (lifetime monotonic per ARCH-3).

- Last Error Summary, Last Error Correlation ID (links to ITS_Errors row), Notes.

## ARCH Refinements (PR #60)

ARCH-1: Enabled checkbox is report-filter metadata only. Canonical runtime gate is <workstream>.<daemon>.polling_enabled in ITS_Config. Two-switch matrix avoided by design.

ARCH-2: Row-id cache persists to ~/its/state/heartbeat_row_ids.json (launchd processes don't share memory). First write does find_row_by_primary + persists; subsequent reads from JSON; 404 invalidates and re-resolves.

ARCH-3: Total Cycles is lifetime monotonic, NOT daily reset. Avoids read-before-write API cost doubling. State file shape: {daemon_name: {row_id, total_cycles}}.

## Failure Isolation

Heartbeat write must NEVER block daemon primary work. Wrap in try/except, log to ITS_Errors with category 'daemon_health_write_failed' on failure, continue. Rate-limit retry should abandon after 5 seconds total.

# §33 (NEW) — Trusted-Contacts Sheet Pattern

Replaces ITS_Config JSON-list allowlists across all workstreams. ITS_Trusted_Contacts sheet in System workspace (location TBD — likely 01 — Config or new 05 — Trust folder). Operator-visible, audit-trail-supporting, scope-enforcing sender authorization.

## Schema (Approximate; Lock at Build Time)

- Email (PRIMARY) — canonical lowercased address. Exact-match key.

- Display Name — human reference; not used in trust decisions.

- Role (PICKLIST: PM, Safety, Forefront, Subcontractor, Vendor, Solution Smith, Internal, Other).

- Project Scope (multi-select PICKLIST: bradley_1, bradley_2, brimfield_1, brimfield_2, huntley, rockford, _all).

- Workstream Scope (multi-select PICKLIST: safety_reports, subcontracts, po_materials, email_triage, ai_employee, _all).

- Status (PICKLIST: ACTIVE, DISABLED, PENDING_VERIFICATION).

- Added By, Added Date, Last Verified, Notes.

## Trust Evaluation Logic

- Sender exact-matched against Trusted_Contacts. Status must be ACTIVE.

- No row → ITS_Quarantine with reason 'sender_not_trusted'.

- Row exists but Project Scope mismatched → ITS_Review_Queue with reason 'scope_mismatch'.

- Row exists and scope matches → proceed to pipeline.

## Header-Forgery Detection

Microsoft Graph API exposes authentication headers on every inbound message. Intake daemons check these BEFORE sender allowlist lookup:

- Parse internetMessageHeaders Authentication-Results for spf/dkim/dmarc results.

- Compare Return-Path header against From: header — mismatch is spoofing signal.

- Compare first Received hop source domain against From: domain — cross-domain inconsistency is spoofing signal.

- Any of {spf=fail, dkim=fail, dmarc=fail, Return-Path mismatch} → ITS_Quarantine with reason 'header_forgery_suspected'.

- Any of {spf=neutral, spf=softfail, dkim=none} on otherwise-trusted sender → ITS_Review_Queue.

## Migration Path

Pre-Customer-1: build ITS_Trusted_Contacts sheet; populate with anticipated Forefront/PM contacts; refactor safety_reports/intake.py to read from sheet instead of ITS_Config JSON; retire safety_reports.intake.allowed_senders ITS_Config row. All future workstream intakes inherit the same pattern.

# §34 (NEW) — Attachment Screening Pipeline

Four-layer defense against malicious attachments. Required before Customer 1 handover — opens external attack surface.

## Layer 1 — Static Signature Checks (cheap, runs first)

- File magic-number verification — header bytes must match claimed extension.

- File size sanity — DFR PDFs expected 50KB-50MB; extreme outliers flagged.

- Filename pattern matching — .pdf.exe, double extensions, RTL-override unicode.

## Layer 2 — Format-Aware Structural Inspection (cheap, runs second)

- PDFs: PyMuPDF reads object tree; flag /JavaScript, /JS, /EmbeddedFile, /Launch, /OpenAction keys.

- Office docs (.docx, .xlsx, .pptx): check for VBA macros, embedded OLE objects, external template references via python-docx/openpyxl.

- Extract embedded URLs from any format; flag external domains for human review.

## Layer 3 — ClamAV Antivirus (medium cost, runs third)

- ClamAV via Homebrew install + clamd daemon + pyclamd Python wrapper.

- Each attachment passes through clamd.scan_stream(bytes). Returns OK / FOUND <signature_name> / ERROR.

- EICAR test signature in test fixtures verifies pipeline health without real malware.

## Layer 4 — VirusTotal API (optional, defer to Phase 2+)

- Free tier: 4 req/min, 500/day. Submit hash, get cross-engine result.

- Network round-trip cost; rate-limited. Skip for Phase 1.5 launch.

## Disposition

- Any layer reports malicious → ITS_Quarantine (CRITICAL triple-fire); Box upload skipped; sender DISABLED in ITS_Trusted_Contacts pending operator review.

- Any layer reports suspicious-but-not-malicious → ITS_Review_Queue.

- All clean → pipeline continues.

# §35 (NEW) — Bounded-Enum Picklist Convention

Standing rule: any new Smartsheet column representing a finite-domain value MUST be created as PICKLIST or CHECKBOX, never TEXT_NUMBER. Free text only for genuinely open-ended content (names, descriptions, IDs, JSON payloads, error messages, free-form notes).

## Retrofit Audit (Pre-Customer-1)

Audit every existing Smartsheet column representing a finite-domain value across all ITS sheets. Convert from TEXT_NUMBER to PICKLIST or CHECKBOX. Targets include:

- ITS_Config — system.state {ACTIVE/PAUSED/MAINTENANCE}, all *.polling_enabled flags, any setting with an enumerated domain.

- ITS_Daemon_Health — verified already PICKLIST for Workstream and Last Cycle Status; future Runtime Gate should be CHECKBOX.

- ITS_Errors — Severity {INFO/WARN/ERROR/CRITICAL}, Workstream, status fields.

- ITS_Review_Queue — Status enum, Workstream, urgency tiers, reviewer-chain selectors.

- ITS_Quarantine — quarantine reason enum, disposition {release/delete/escalate}, Workstream.

- Per-project sheets (Daily Reports, Weekly Rollups) and future workstream sheets — status fields, category fields, anywhere a code reader expects a known value.

## Implementation Notes

Smartsheet supports column-type changes on existing columns; existing values preserved if compatible. Smartsheet MCP cannot perform the change (no API primitive); operator UI required. Approximately 30 seconds per column conversion.

kill_switch.py fail-open logic stays as belt-and-suspenders for Smartsheet-unreachable case. Picklist enforcement eliminates typo/case/whitespace as the trigger, not the Smartsheet-unreachable trigger.

# §36 (NEW) — In-Repo Tech Debt Log

docs/tech_debt.md is the canonical execution-layer tech debt log. Planning-project tech-debt scope is limited to owner-decision items only.

## Convention

- Add an entry when a session deliberately chooses preservation-over-refactor (§14), discovers an external-API constraint that forced a workaround, or defers a non-trivial cleanup.

- Mark CLOSED when resolved in a commit. Preserve the entry with resolution detail rather than deleting (history is cheap, context is expensive).

- Each entry: descriptive title with [OPEN|CLOSED|PARTIALLY MITIGATED] tag + ISO date + rationale + workaround + revisit-when criterion + resolution detail if closed.

## Current State

~215 entries as of 2026-07-12 (grown well past the 2026-05-22 snapshot; the live set is in `docs/tech_debt.md`, now split into `tech_debt.md` (open) + `tech_debt_closed.md` (archive)). Mix of closed/open/partially-mitigated. Notable open items: anomaly_logger SUSPICIOUS_FIELD_PATTERNS FP risk, R2 Watchdog Check E (Phase 1.5 deferral), Picklist_Sync_Config config/state mix, Smartsheet MULTI_PICKLIST round-trip gotcha, safety_reports week-folder race condition, Daily Reports schema gap (no Box Link column).

# §37 (NEW) — CC Skills Usage Convention

> **Role scope (v15).** Every operation described in §§37-41 — installing/invoking skills, the block-dangerous-git carve-outs and manual force-delete recovery, the per-customer-fork `gh api` hardening and gitleaks runs, the migration-script dry-run/live-write split, worktree cleanup, GitHub Actions version bumps — is a **Developer-Operator** operation. It requires git/CC/shell fluency and the standing developer-grade override authority the guard hooks assume (§38 "operator shell is unaffected"). The **Successor-Operator** (the trained-operator Tier-2 role defined in §44) performs NONE of these; they are out of the Successor-Operator's capability class by definition. Where the unqualified word "operator" appears in §§37-41, read it as Developer-Operator.

mattpocock/skills installed repo-local in every ITS execution repo. Skills physically live at `.agents/skills/` (universal multi-agent location); `.claude/skills/` is a symlink pointing at it. `.agents/skills/` is the source of truth. `skills-lock.json` at repo root pins upstream revisions for reproducible installs.

Customer-fork-portable: when ITS forks for Customer 2+, skills come with the code.

## Default Install (14 skills)

caveman, diagnose, grill-me, grill-with-docs, handoff, improve-codebase-architecture, prototype, setup-matt-pocock-skills, tdd, to-issues, to-prd, triage, write-a-skill, zoom-out.

Install command (one-time per fork): `npx skills@latest add mattpocock/skills`. Adding skills outside the default set requires `--full-depth` flag for `misc/` subdirectory skills (e.g., `git-guardrails-claude-code` per §38).

## Auto-Recommend (trigger-driven)

CC should suggest invoking these skills when their triggers fire:

- `diagnose` — any bug investigation that touches an SDK boundary (Smartsheet, Box, Graph). The reproduce → minimise → hypothesise → instrument → fix → regression-test loop is the standard response to the SDK-vs-Live class of bug (§30).
- `tdd` — any new `shared/*` SDK wrapper with create/update/delete on typed columns/rows (§30 integration discipline).

## Gated (require operator approval)

These skills conflict with established conventions and must not be invoked speculatively:

- `improve-codebase-architecture` — conflicts with §14 preservation-over-refactor. Operator must confirm the refactor target meets the ≥4 real reuse cases threshold before invoking.
- `request-refactor-plan` — same §14 constraint when installed.

## Safe to Invoke On Demand

grill-me, grill-with-docs, to-prd, to-issues, handoff, caveman, zoom-out, triage, prototype, write-a-skill, setup-matt-pocock-skills.

## Not in Default Install (available, install on demand)

`request-refactor-plan`, `qa`, `git-guardrails-claude-code` (§38). Skills not in `mattpocock/skills` at all (e.g., `migrate-to-shoehorn` cited from search results) are flagged as nonexistent rather than silently ignored.

# §38 (NEW) — Local Agent Guardrails

block-dangerous-git.sh PreToolUse hook installed via `mattpocock/skills` git-guardrails-claude-code skill. Wired via `.claude/settings.json` (committed; distinct from gitignored `.claude/settings.local.json`).

Hook only blocks the model-agent's Bash tool calls. Operator shell is unaffected. Recovery operations (e.g., `git branch -D` on a force-delete-needed branch) are performed manually by the operator in their own shell.

## Allow-List (carved out from defaults)

These commands are allowed even when their pattern overlaps with destructive operations:

- `git push` (any branch, non-force) — required for canonical PR workflow
- `git branch -d` (safe-delete; lowercase d) — canonical post-merge branch cleanup
- `gh pr merge --squash --delete-branch` — canonical merge command (composite of the above)
- `gh pr view` and all read-only `gh` commands — required for four-part verification (per existing PR-merge discipline)

## Block-List

- `git push --force`, `git push -f` — force-push
- `git push origin --delete <branch>` — remote branch deletion
- `git push origin main` (direct) — defended at server-side branch protection layer; local hook does NOT differentiate `push origin main` from `push origin feature-branch`. Direct-push-to-main enforcement lives at the GitHub branch protection layer per §39
- `reset --hard` — local history destruction
- `clean -f`, `clean -fd` — local working-tree destruction
- `branch -D` (force-delete; uppercase D) — operator-only via manual shell
- `checkout .`, `restore .` — uncommitted-changes destruction

## Defense Complement

The local hook protects the operator's machine from agent error. Server-side GitHub branch protection (per §39) protects the repo from any contributor, on any machine. Direct push to `main` is blocked at both layers.

# §39 (NEW) — Per-Customer-Fork Security Setup

Mandatory security-hardening baseline for every customer fork. Establishes the minimum posture that all ITS forks (Evergreen + future Customer 2+) inherit. The operational checklist with verbatim `gh api` commands lives at `references/customer-fork-setup-checklist.md`.

## Baseline Configuration

### Branch Protection on main

- Required status checks: `strict=true`, `contexts=["test"]` (or the canonical CI job name for the fork), GitHub Actions app
- `required_linear_history=true` (squash-only merges)
- `allow_force_pushes=false`
- `allow_deletions=false`
- `required_conversation_resolution=true`
- `enforce_admins=false` (emergency lever preserved for solo + CC operation; tighten to `true` for multi-contributor forks)
- `required_pull_request_reviews=null` (solo + CC default; tighten when adding human reviewers)

### Fork-PR Approval Policy (public forks only)

`approval_policy=all_external_contributors` (strongest). Tightens default `first_time_contributors` to require operator approval before CI runs on any PR from a non-collaborator, regardless of contributor history.

### Secret Scanning

- `secret_scanning.status=enabled`
- `secret_scanning_push_protection.status=enabled` — blocks pushes containing detected secret patterns at the platform layer (not just alerts post-push)

### Dependabot Alerts

- Alerts: ENABLED (`PUT /vulnerability-alerts`)
- Automated-security-fixes: NOT ENABLED — auto-PR opens would conflict with the four-part-verify + manual-merge workflow. Operator reviews + lands dependency bumps via §41 discipline.

### CodeQL Default Setup

- `code-scanning/default-setup` with `state=configured`, `query_suite=default`
- Languages auto-detected (typically `python` + `actions` for ITS forks)
- Weekly scan schedule

## Operator-Only Audit (Not API-Automatable)

- Fine-grained Personal Access Token inventory — `Settings → Developer settings → Personal access tokens → Fine-grained tokens`. Verify scope is per-repo not All-repositories; verify expiration dates set; revoke unused.
- Classic Personal Access Token inventory — same UI, classic tab. Most-likely place for forgotten tokens from `gh auth login` or one-off scripts.

## Architectural Defense (not configuration)

All secrets MUST live in macOS Keychain. `shared/keychain.py` is the canonical interface. `.gitignore` covers `.env*`, `*_secret*`, `*credentials*`, `*.token`, `*.pem`, `*.key`. This eliminates the design pathway for secrets to enter the repo, making the configuration items above defense-in-depth around an already-secure baseline.

## Verification Pattern

After hardening, run gitleaks against full history (`gitleaks detect --source . --log-opts="--all" --redact -v`). Zero findings + zero CI/env/Dependabot secrets + zero workflow `secrets.*` references = clean baseline. Re-run periodically after any new `shared/*` SDK wrapper merges.

# §40 (NEW) — Migration-Script PII Logging Asymmetry

Applies to all `scripts/migrations/*` and any script that handles operator-known PII (email addresses, contact names, customer details).

## Asymmetry Rule

- **Dry-run path** — PII permitted in logs. Dry-run output is review material: the operator needs to see emails/names to verify what WILL be added before confirming. Stripping PII from dry-run defeats the review purpose.

- **Live-write path** — PII stripped. The write IS the side effect. Logging confirmation needs only positional indices + system IDs (Smartsheet row IDs, sheet IDs). Logging emails/names in the live-write path puts PII in terminal scrollback, screen-share recordings, and shell history without operational benefit.

## Canonical Example (PR #84)

Live-write before:

```python
print(f"[ok] added: {r['Email']} (row {new_row.id})")
```

Live-write after:

```python
print(f"[ok] added row {i+1}/{total} (smartsheet row_id={new_row.id})")
```

Dry-run path unchanged (still prints `r['Email']`).

## Rationale

Per-customer-template scripts run on multiple operator terminals over the customer-fork lifecycle. The same script that runs at Evergreen will run at Customer 2, possibly during screen-shares, customer hand-overs, or demo recordings. Code-as-documentation also matters on public repos — the established pattern for `scripts/migrations/*` is the wrong norm to set as "logs PII to stdout."

# §41 (NEW) — GitHub Actions Version-Bump Discipline

Applies to every `.github/workflows/*.yml` action version bump.

## Procedure

1. Verify the latest stable tag via API:

   ```bash
   gh api repos/<owner>/<repo>/releases/latest --jq '.tag_name'
   ```

   Examples: `actions/checkout`, `actions/setup-python`, `actions/cache`.

2. Read the release notes for breaking changes:

   ```bash
   gh release view <tag> --repo <owner>/<repo>
   ```

   Pay attention to: new required inputs, removed flags, behavior changes, runtime version (Node.js 20 vs 24) requirements, default-value changes.

3. If breaking changes affect ITS workflows → STOP. Surface the breaking change to operator. Do not force-through.

4. If clean → bump in a focused PR. One bump per PR family (e.g., bump both `checkout` and `setup-python` in one PR if both are deprecated together; do NOT bundle with unrelated workflow changes).

5. Four-part PR-landed verify per execution-repo discipline.

## Anti-Patterns

- DO NOT blanket-upgrade ("bump everything to latest"). Each action's latest tag is a separate decision.
- DO NOT bump from a deprecation annotation without reading the release notes. The annotation says "deprecated"; the notes say "what changed."
- DO NOT bump in the same PR as unrelated workflow edits. Isolate so a CI failure is unambiguously attributable.

## Canonical Example (PR #81)

`actions/checkout` @v4 → @v6.0.2 and `actions/setup-python` @v5 → @v6.2.0 in a single PR. Both bumps verified via `gh api releases/latest`; release notes read for breaking changes; both clean; CI green on bumped versions; deprecation annotation cleared on next main-branch run.

# §42 (NEW) — Code-Level Self-Documentation Discipline

Every `shared/*` module and every workstream entrypoint will be read again — by future-Seth, by future-CC, by the maintainer of a customer fork three months out. The code should answer "why" without forcing the reader to leave the file.

## Mandatory module docstrings

Every NEW module in `shared/*` and every workstream entrypoint (e.g., `safety_reports/intake_poll.py`, `safety_reports/weekly_generate.py`) opens with a docstring carrying four named headings, in this order:

```python
"""One-sentence module purpose.

Purpose
-------
What this module does. Two sentences max.

Invariants
----------
What cannot change without breaking consumers. Reference Foundation
Mission invariants and Op Stds sections by stable anchor where
applicable. If the module is on the External Send Gate path or
processes adversarial input, restate the relevant invariant here.

Failure modes
-------------
Fail-open vs. fail-closed posture. Exception types raised. error_log
categories used. What recovers vs. what propagates.

Consumers
---------
What imports this module. What depends on its outputs (sheets, files,
external APIs). Useful for impact-analysis when changing internals.
"""
```

## In-code rationale comments

Any decision that would surprise a future reader gets a comment block above the relevant code:

```python
# Rationale: {short explanation of why this choice over alternatives}.
# Reference: {F-finding, session-log path, doctrine §, or PR number}.
```

Decisions worth a rationale comment:

- Fail-open vs. fail-closed (either direction — both are choices).

- Working around an SDK quirk or live-API behavior that differs from the SDK's stated contract.

- Accepting a documented risk (the comment IS the acceptance record).

- Choosing a less-obvious pattern when an obvious one was considered.

- Preservation-over-refactor decisions per §14 (the comment captures why a working pattern is preserved over a cleaner rewrite).

The reference must be specific enough that the future reader can find the source. "F23 — see audit" is fine; "see audit" is not.

## When to apply

- All NEW `shared/*` modules and workstream entrypoints from this doctrine bump forward. CC briefs reference §42 when scoping new modules.

- Existing modules retrofit opportunistically per the preservation-over-refactor convention (§14): when next touched for an unrelated reason, add the docstring + any motivation comments that surface during review. NOT a sweep PR. Doctrine §14 explicitly rejects "let's go fix every module" passes.

## Interaction with existing doctrine

- Complements verify-before-fix discipline. The in-code rationale IS the verification anchor for future-fix decisions: a reader who understands "this fail-open posture exists because of F23" doesn't re-litigate the choice when adjacent code needs changes.

- Complements §30 (SDK-vs-Live Integration Test Discipline). The rationale comment captures the live-API quirk that motivated the integration test, so future-CC reading the test understands the defense-in-depth.

- Complements §14 (preservation-over-refactor). The rationale comment captures why a working-but-ugly pattern is preserved. Without it, the next reader assumes the ugliness was an oversight and "fixes" it.

## Enforcement

Initial enforcement is by convention + review. CC briefs reference §42 explicitly when scoping new modules. Operator review at PR time checks for docstring presence and rationale comments on non-trivial decisions.

Trigger for stricter enforcement (e.g., AST lint check for docstring presence; ruff-rule for missing rationale on decisions matching known patterns): three or more instances within a 30-day window of "I read this module and couldn't tell what the rationale was." Tracked in tech debt; revisit when triggered.

## Example — `shared/state_io.py` post-§42 retrofit

```python
"""Atomic JSON/text writes + sidecar lock for daemon-managed state.

Purpose
-------
Canonical entry point for all writes to files under `~/its/state/`.
Provides crash-safe atomic write + concurrent-writer protection so
the polling-daemon class (intake_poll, weekly_send_poll, and future
consumers) cannot corrupt shared state files.

Invariants
----------
- Raw `Path.write_text` / `Path.write_bytes` on files under
  `~/its/state/` is forbidden. All writes route through this module.
- The sidecar lock pattern (flock on `{path}.lock`, not on the data
  file) is load-bearing: `os.replace` swaps the data-file inode,
  which would invalidate any flock held directly on it.
- `with_path_lock` is non-blocking with bounded retry (5×50ms,
  mirroring `shared/alert_dedupe._acquire_lock`). On exhaustion it
  raises `StateLockTimeoutError`; callers decide whether to log+
  continue (heartbeat writes, per CLAUDE.md ARCH-2) or propagate.

Failure modes
-------------
- Lock-acquisition timeout → raises `StateLockTimeoutError`. Heartbeat
  consumers log a WARN under `error_log` category
  `daemon_health_write_failed` and continue the cycle.
- Atomic-write disk error → raises `OSError` natively. Callers do not
  retry; the next cycle gets a fresh attempt.
- Serialization error → raises `TypeError` / `ValueError` natively.

Consumers
---------
- `safety_reports/intake_poll.py` — seen-set, heartbeat-row state.
- `safety_reports/weekly_send_poll.py` — heartbeat-row state.
- `shared/alert_dedupe.py` — pending migration in PR 2 of the
  Phase 1.4 hardening cluster.
- Future: `shared/circuit_breaker.py` per F08 will persist breaker
  state through these helpers.

Reference
---------
Audit F19 + F23 in `its-blueprint/audits/2026-05-25_forensic-audit.md`.
Landed via `its` PR #88 (merge commit `36932bd`). Session log:
`its/docs/session_logs/2026-05-25_state-io-atomic-write.md`.
"""
```

# §43 (NEW) — Successor-Remediation Documentation Discipline

§42 documents code FOR a code-reader: module docstrings and in-code rationale aimed at future-Seth, future-CC, and a developer maintaining a fork. That audience is the **Developer-Operator**. It is the wrong audience for Tier 2 of the three-tier maintenance model.

The human in the loop at Tier 2 is the **Successor-Operator** — a trained operator who runs Claude Code himself and follows runbooks, but is not a code-reader (writes no code; does none of the §§37-41 developer-context work). This section is the PARALLEL discipline for that audience. Where §42 answers "why is this code the way it is," §43 answers "what does the Successor-Operator do when this capability misbehaves."

## Document-as-you-build rule

Every capability ships a plain-language **successor-remediation runbook entry written AS the capability is built** — not retrofitted, not deferred. The entry is part of the capability's definition-of-done, the same way the §42 docstring is. A capability without its remediation entry is incomplete. Entries are authored as **Markdown shipped with the capability** in the execution repo (version-controlled alongside the code): Claude loads the relevant entry to drive a Tier-2 repair. The Successor-Operator does not open the Markdown — they see Smartsheet rows and alert emails and approve; Claude reads the entry on their behalf.

## Entry shape

Each entry is written for a reader who can see Smartsheet rows and alert emails but cannot read code, and has four parts:

- **Symptom** — stated in Smartsheet / alert / dashboard terms the Successor-Operator actually sees (e.g., "ITS_Daemon_Health shows `safety_reports.intake_poll` Last Cycle Status = STALE" or "a CRITICAL alert email names category `daemon_health_write_failed`"). NOT a stack trace or exception class.
- **What the Successor-Operator checks** — the specific sheet/column/value to look at, in UI terms.
- **The Claude prompt or UI action** — either the exact plain-language request the Successor-Operator gives Claude ("Claude, the intake daemon heartbeat is stale — please re-run it and confirm a fresh heartbeat"), or the direct Smartsheet-UI action ("set ITS_Config row `safety_reports.intake.polling_enabled` to true"). Claude drives any operation that is not a literal UI cell edit; the Successor-Operator approves.
- **Escalate-to-Seth condition** — the explicit boundary at which this stops being a Tier-2 repair and becomes a Tier-3 escalation to the Developer-Operator, stated in observable terms ("if the heartbeat is still stale after one re-run, or if the alert names the External Send Gate or any secret/auth category, stop and escalate to Seth"). This boundary is the §44 Tier-2/Tier-3 rule expressed for one specific capability.

## Distinction from §42 (do not conflate)

| | §42 | §43 |
| --- | --- | --- |
| Audience | code-reader (Developer-Operator, future-CC) | non-developer Successor-Operator |
| Lives in | module docstrings + in-code comments | plain-language Markdown shipped with the capability (Claude-read; no code) |
| Answers | "why is this code the way it is" | "what do I do when this misbehaves" |
| Vocabulary | invariants, exception types, error_log categories | Smartsheet rows, alert subjects, UI actions, Claude prompts |

The two are NOT substitutes. A §42 docstring saying "fail-open on Smartsheet-unreachable" does not tell a non-developer what to do when it fails open; a §43 entry saying "if the sheet shows STALE, ask Claude to re-run" does not tell a developer why the inode-swap lock pattern is load-bearing. Each capability that has a Tier-2-reachable failure mode needs both.

## Coverage (audited v20)

Every capability with a Tier-2-reachable failure mode ships its §43 entry as definition-of-done — audited at the v20 consolidation (2026-06-28 class review). Several recent capabilities were thin here and were backfilled. The standing rule: a Tier-2-reachable capability **without** its §43 entry is **incomplete** — the same bar as a missing §42 docstring or a missing binding test (§52). This is the §52 narrated→enforced discipline applied to the successor-remediation surface.

## Inheritance into briefs

Every future workstream brief inherits a **"successor-remediation deliverable"** the same way it inherits the Foundation invariants: F08/F09 (circuit breaker, dedupe hardening), the Safety Portal, and every workstream after them state, in their deliverables, the §43 remediation entries that ship with the capability. CC briefs reference §43 explicitly when scoping any capability whose failure is something a Successor-Operator could plausibly be asked to resolve at Tier 2.

## Enforcement

Initial enforcement is by convention + review, mirroring §42: the operator review at PR time checks that a capability with a Tier-2-reachable failure mode shipped its §43 entry. The Markdown runbook substrate (where the entries collect) and any automated presence check are ordinary build / tech-debt items; they are no longer coupled to any "enforcement-layer gap" (none exists — see §44's training-enforced Tier-2 boundary).

# §44 (NEW) — Tier-2 Claude-Assisted Repair Path

The successor-maintenance model has three tiers. **Tier 1 — self-healing**: daemons recover, the watchdog catches staleness, no human acts (the self-heal layer is substantially built — the Check C marker-file staleness floor covers all four tracked daemons and the UptimeRobot external ping (audit F16) is live; the lone residual pre-cutover build item is the weekly_generate Friday-crash catch-up, since weekly_generate is calendar-scheduled and a crashed Friday cycle is not auto-recovered by launchd until next Friday; see §2 and the Handover Plan v8 / V&R v9 pre-cutover conditions). **Tier 2 — Claude-assisted Successor-Operator repair**: the trained Successor-Operator runs Claude Code himself and, following the §43 runbook, carries out a low-capability-class repair — escalating anything novel or high-class to Tier 3. **Tier 3 — escalation to the Developer-Operator** (Seth), who is a reachable escalation asset, not the primary operator. This section defines Tier 2 and its boundary with Tier 3.

## Who acts at Tier 2

The Successor-Operator (per §43 / the §37 role-scope note) is a trained operator who runs Claude Code himself, reads Smartsheet and alerts, and follows the §43 remediation entry for the affected capability to carry out the repair. He does not write code, perform §§37-41 developer-context operations, or touch secrets/Keychain. His contribution is operating CC under the runbook plus the judgment to recognize and escalate the four high-class categories; Claude does the diagnostic and mechanical work within the low-class set.

## In-scope: the LOW-capability-class repair set ONLY

Tier 2 is limited to repairs that change no code, touch no secret, and cannot transmit externally. The closed in-scope set is:

- Re-run a stopped or stale daemon (the most common Tier-2 action).
- Toggle an ITS_Config value within its bounded enum / its `*.polling_enabled` runtime gate (§35 picklist domains).
- Re-send an already-approved item that failed to send (re-trigger an existing approval — NOT create or alter an approval).
- Re-seed a missing config or daemon-health row to a known-good value.
- Clear a stuck lock / stale state file so a daemon can resume.

These are low-class precisely because none of them can cross the External Send Gate, expose a secret, alter doctrine, or require a code edit.

## Structurally forbidden at Tier 2: the HIGH-capability-class set

HIGH-capability-class is defined STRUCTURALLY, not by how well something is documented. Anything that touches ANY of the following is high-class and is forbidden at Tier 2 — it escalates to Tier 3 unconditionally:

- the **External Send Gate** / anything that could cause an external transmission (FM Invariant 1);
- **secrets / auth** (Keychain, tokens, credentials, approver-principal configuration);
- **doctrine** (any change to a doctrine doc or an invariant);
- anything **requiring a code change**.

## The escalation boundary (the "both" rule)

A fault escalates to Tier 3 if it is **NOVEL** (not covered by a §43 runbook entry) **OR HIGH-capability-class**. Equivalently: a fault is Tier-2-eligible only if it is **documented (has a §43 entry) AND low-class**. High-class always escalates regardless of documentation — a perfectly documented secret-rotation is still Tier 3 because the class, not the doc, decides. Novel-but-low-class also escalates, because no vetted §43 path exists yet for Claude and the Successor-Operator to follow safely. Tier 3 resolution by the Developer-Operator that recurs should produce a new §43 entry so the next instance can drop to Tier 2.

## Audit-trail requirement

Every Tier-2 repair is audit-trailed: the symptom, the §43 entry followed, the action Claude took, and the Successor-Operator's approval are recorded to the forensic surfaces (ITS_Errors as the record leg per §3.1, with a Correlation_ID per §3). A Tier-2 repair that cannot be reconstructed after the fact is a process failure even if the repair itself worked.

## The through-line (capability-gating philosophy, extended)

The philosophy that keeps the AI out of the send path informs HOW the Tier-2 boundary is drawn — why the four high-class categories are off-limits. `tests/test_capability_gating.py` enforces FM Invariant 1's two-process model by static AST import inspection: a generation process structurally CANNOT import a send capability — that boundary holds by construction. Tier 2 does NOT get a structural analogue: there is no maintenance-side construction that confines a repair session, and none is built. The analogy is philosophical only; the Tier-2 boundary is held by the trained operator's judgment, the both-rule, and co-resolution with the Developer-Operator (next subsection).

## The Tier-2 boundary is training-enforced, not structurally enforced

No structural maintenance enforcement layer exists, and none is to be built. The Tier-2 boundary — confining a repair session to the low-capability-class set and routing the four high-class categories to Tier 3 — holds by three things: (1) the trained Successor-Operator's judgment (he runs Claude Code himself, follows the §43 runbook, and is trained to recognize the four high-class categories); (2) the both-rule (novel OR high-class → Tier 3); and (3) co-resolution with the Developer-Operator on the four high-class categories until per-category clearance is granted (dated, logged, Developer-Operator-only).

The guard hooks that exist today (`.claude/hooks/`: block-codeql-dismiss, block-dangerous-git, block-doc-reconciliation-write, block-doctrine-write) are REAL but **scoped to subagent / developer sessions and fall open for the operator's own session** — each hook's message tells the human to "run it manually." They protect developer / subagent sessions and assume the human in the loop can safely override. They are NOT expected to confine the trained Successor-Operator's repair sessions; that boundary is the training + both-rule + co-resolution model above, not a hook. There is no non-developer-safe enforcement layer, and the through-line ends at philosophy (it informs WHY the four categories are off-limits), not at a built control.

The Tier-1 self-heal gap (the Check C marker-file staleness floor, §2 — earlier called "Check H") remains a real pre-cutover gate on its own — narrowed to the weekly_generate Friday-crash catch-up now that Check C covers all four tracked daemons and the F16 ping is live; it is no longer coupled to any Tier-2 enforcement layer (there is none). The Tier-2 pre-cutover readiness gate is instead the §44 low-capability-class action set implemented as discrete, tested, non-escalating operations + §43 runbooks for the top fault classes + the trained-operator / demonstrated-supervised-repair gate (Handover Plan v8 Pre-Cutover Conditions; V&R v9). Tracked in execution-layer tech debt (§36). (The "both" rule above — novel OR high-class escalates to Tier 3 — is the steady-state safety default.)

# §45 (NEW) — Find-or-Create, Not Look-Up-or-Strand

Pipeline artifacts a workflow depends on (Smartsheet folders + sheets, Box folders) are **auto-provisioned by find-or-create**, not looked up against a hardcoded map that strands the work on a miss. Canonical realization: the Safety Portal week-sheet path (PR-C #181, `safety_reports/week_sheet.py`) find-or-creates a per-job folder at the **surface of `WORKSPACE_SAFETY_PORTAL`** (a sibling of the `Safety Portal` / `Form Catalog` folders, not nested inside `FOLDER_SAFETY_PORTAL`), then the per-week sheet, then the row — replacing the `FIELD_REPORTS_FOLDER_BY_PROJECT` per-project map and its `KeyError → strand` branch.

## Rules

- **Re-find after create, tolerate races.** A concurrent create surfaces as a WARN-logged duplicate (`*_race_duplicate`), never a crash.
- **Failure surfaces, never silent.** A transient provisioning failure (`SmartsheetError` / `BoxError` on create) soft-fails the unit of work so it **re-pulls / retries** next cycle; a permanent or structural refusal routes to `ITS_Review_Queue`. There is no silent write-to-nowhere.
- **No hardcoded artifact map on the auto-provision path.** A *declared* per-customer-fork seed (e.g. `BOX_PROJECT_FOLDERS`, the Box-folder routing fallback) is the allowed, documented exception; the job roster (`active_jobs`) has none (a read miss returns the empty set → the consumer surfaces, never guesses).

Generalizes the PR-C / PR-K provisioning pattern. Origin: [Safety Portal brief §3](../workstreams/safety-portal/brief.md).

# §46 (NEW) — Workspace Membership = Approval Authority (F22 mechanism)

For a self-contained, approval-gated workspace (§23 — the Safety Portal), the **authorized-approver set is resolved live from workspace share membership**, not a maintained allowlist: *sharing the workspace IS granting approval authority.* The F22 send-gate predicate (the cell-history modifier-email match, `shared/approval_verification.py`) is unchanged; only the **source** of the authorized set moves — to `smartsheet_client.list_workspace_share_emails(workspace_id)` (`GET /workspaces/{id}/shares`, the lowercased emails of every USER share, any access level). The former ITS_Config `safety_reports.authorized_approvers` allowlist is retired (PR-E #183).

## Invariants

- **Fail-closed, never fail-open.** An empty resolved set blocks all sends (`EMPTY_ALLOWLIST`).
- **Group-share gap (known, pre-prod).** Only USER shares carry an email; GROUP shares are excluded — a workspace shared *only* to a Smartsheet group resolves to the empty set → all sends blocked. Mitigation today: share with **individuals**; group-membership expansion is a documented follow-up.
- **Owner inclusion is not asserted.** The resolver injects no workspace owner and filters no access level — whether the owner appears in the set is a dependency on the Smartsheet `/shares` response shape, not a coded guarantee. Do not document the owner as covered; it is an open question.

This is the in-code realization of the §23 *workspace-membership = approval authority* principle. Origin: [Safety Portal mission §8.1](../workstreams/safety-portal/mission.md#81-f22-approval-authority-is-realized-as-workspace-membership-pr-e-183).

# §47 (NEW) — Box Version-on-Conflict for Deterministic-Name Re-Uploads

Content re-generated under a **deterministic filename** (the weekly compiled packet — Compile-Now and late-submission recompiles produce the same name) uploads a **new Box version** on a 409 name-conflict (`box_client.upload_bytes_or_new_version` → resolve the existing file → `update_contents`), preserving Box's file-version history — the System of Record — rather than 409-failing the recompile or accumulating suffixed copies. A 409 whose conflicting file then vanishes **re-raises** (no silent swallow).

## Boundary

- **Distinct documents keep suffix-on-conflict.** The per-submission upload path retains `upload_bytes` + suffix-on-409 — each amend is a genuinely different document, not a new version of one. Version-on-conflict is for the *same logical artifact re-rendered*, not for distinct artifacts.

Origin: PR-G #186, [Safety Portal brief §9](../workstreams/safety-portal/brief.md#9-filing-box-is-the-system-of-record).

# §48 (NEW) — CodeQL False-Positive Handling

Verified false positives are dismissed **per-alert with a recorded reason** (keeping the rule live); rules are **never blanket-suppressed**, and a secret-logging rule is **never** silenced via a per-file CodeQL config on a secrets-handling file. Prefer a **genuine fix over a suppression** wherever the alert points at real hygiene (e.g. the `_PortalCreds` named-dataclass refactor that resolved a `clear-text-logging-sensitive-data` HIGH — memory-archive §G25.5).

## Mechanism (as-built)

- **Per-alert dismissal:** `gh api -X PATCH .../code-scanning/alerts/<id> -f state=dismissed -f dismissed_reason=false_positive -f dismissed_comment="<pattern>: <rationale>"` — auditable, the rule stays enabled. Add an inline code comment at the FP site where it aids the next reader.
- **`codeql-fp-triager` is PROPOSE-ONLY.** It surfaces candidate dismissals (the 3 known weekly FP patterns — see `references/claude-code-info-gap.md §5` / memory-archive §G7.4) with quoted evidence; the **operator applies** them. A `PreToolUse` hook (`.claude/hooks/block-codeql-dismiss.sh`) structurally blocks any `code-scanning … dismiss` command **inside that agent** — wired **agent-scoped in the agent frontmatter, not globally in `settings.json`** (which wires only `block-dangerous-git`), so it protects the subagent while the operator's own session can still dismiss manually (consistent with the §44 guard-hook note).

Codified this cycle: the rule was previously enforced by tooling + memory but not stated as doctrine.

# §49 (NEW) — Preservation for a Committed Future Workstream

Extends §14 (preservation-over-refactor). When a clean-break retires an *input or trigger* but the underlying *infrastructure* is workstream-agnostic and a **committed future workstream** depends on it, the infrastructure is **retained in-tree, not decommissioned** — only the superseded entry-point is tombstoned. Record the retention rationale (which modules, why, for whom) so a later "cleanup" session does not delete the seed.

## Canonical instance

The Safety Portal clean-break retired the email-PDF *safety intake*: only `intake_poll.py` is tombstoned (`NotImplementedError`, PR #171). Retained as the **Email Triage** seed — `week_folder.py` + `intake.process_message` + the Graph fetch/classify/extract stages (preserved-dormant); `graph_client` / `untrusted_content` / `header_forgery` and `project_routing` / `BOX_PROJECT_FOLDERS` / the report-category machinery (actively-live shared infra, also reused by the portal Box path). Rationale recorded in `intake_poll.py`'s docstring, memory-archive §G26, and the [Email Triage mission](../workstreams/email-triage/mission.md) forward-reference.

# §50 (NEW) — Privileged Code-Actuation Gate

Generalizes Invariant 1's two-process model from *external transmission* to *privileged code/config actuation*. The cloud surface (the Worker) may only **queue** an actuation request; the local Mac daemon is the **sole actuator**; the request is **state-machine-stamped**, and the apply/merge is **CI-gated and synchronous**; the operator toolchain holds the credentials. A compromise of the cloud surface therefore cannot actuate — it can only enqueue a request the local, credential-holding, CI-gated actuator must independently accept. This is the same damage-ceiling logic as Invariant 1 (the AI/cloud layer can propose; only a separate, human/operator-anchored process can effect), extended from "send" to "change running code/config." Raised first (Safety Portal mission v4, 2026-06-10; [info-gap §3/§8](../references/claude-code-info-gap.md); memory-archive §G35), carried propose-only through Safety Portal mission v5.

## Canonical instance

The form-publish pipeline (`publish_daemon.py`): a form-definition change is committed to git + queued; the Mac publish daemon polls, validates against the manifest + meta-schema, and is the **only** process that applies it — the Worker never self-publishes. First ITS per-category code-deploy clearance. The same gate governs any future "cloud queues, Mac actuates" privileged-change pattern.

# §51 (NEW) — ITS-Owned Structured-SoR Write-Back

ITS may be the authoritative writer to a **Smartsheet system-of-record it owns** (created and controlled by ITS — e.g. the `ITS — Progress Reporting` workspace and the `ITS — Safety Portal` Active-Jobs sheet), distinct from the read-only / human-approved-send posture toward a **customer-owned** Smartsheet. The D1 store is upstream; the ITS-owned Smartsheet is a downstream structured mirror that ITS writes — **one-way up** for accumulating logs (hours, equipment); **one-way-up (phased delivery, v20)** for the Material List — M2 ships a portal-authored one-way-up snapshot now (non-clobbering, strictly *more* conservative than bidirectional: never writes operator-owned columns, never reads operator edits back), with **bidirectional split-ownership receive deferred to M2b** when a Material-List operator-edit workflow exists (at which point the operator owns content columns, the field owns delivery columns, neither side's write overwrites the other's — the non-clobber guarantee is preserved, unbound until M2b); and the **job-tracker → Active-Jobs write** — the portal Job Tracker is the authoritative job creator, writing job identity + `active`/`inactive`/`archived` lifecycle **up** to the ITS-owned Active-Jobs sheet(s), so the safety and progress workspaces are fed by one writer and never drift. Guards, all required: the up-sync daemon is **send-free + AI-free** (GATED; `send_mail`/`anthropic` forbidden), enrolled in `WALKED_ROOTS`, with egress through an **allowlisted `shared/portal_client.py` method** (no raw SDK); per-job sheets resolved by **validated find-or-create with the A1 margin-check** (never a default, never silently past the cap); the write is **non-clobbering and column-scoped** (the daemon never overwrites operator-owned columns); accumulating logs are **period-split + archived-on-closure, never `delete_rows`**, under an A5 row-cap watchdog (period-split **for a low-volume log** (v20, folded from the 2026-07-04 rider) is satisfied by a single standing sheet whose split is *triggered* by the row-cap watchdog rather than mandatory calendar splitting — Smartsheet sheet-proliferation being the #1 scaling risk); A2 SDK timeouts + the A3 Box/Keychain lock inherited. **Boundary:** this covers an **ITS-owned** SoR ONLY — authoritative write-back to a **customer-owned / canonical** system-of-record (and the PJOB→JOB key reconciliation it requires) is a separate, higher decision, explicitly out of scope.

## Canonical instance

The Progress-Reporting up-sync daemon and the job-tracker→Active-Jobs mirror (`field_ops/fieldops_sync.py`, the P2.5 "origin-flip" seam): D1 is the write-first primary; the Mac daemon mirrors the ITS-owned columns up; `origin='portal'` rows are sole-written by the portal, `origin='smartsheet'` rows by the operator/down-sync (disjoint writers). Gates P7 + M2/M3 and the job-tracker pivot ([Progress-Reporting mission §16](../workstreams/progress-reporting/mission.md); plan `ok-we-are-going-scalable-flamingo.md`). Doctrine ratified ahead of the seam per the §16 early-initiation plan; the seam's build carries this section's guards as DoD.

# §52 (NEW) — Narrated-Not-Enforced: control claims resolve to a test or a dated exception

Every doctrinal claim of a **built control or guarantee** ships either (a) a binding test/lint that proves it in code, or (b) a dated, explicit "doctrine-only, NOT built" exception. A control that is *narrated* (doctrine asserts it) but not *enforced* (no test binds it) is the recurring forensic failure class #6 (2026-06-28 retrospective, 9 incidents) — the claim silently drifts from reality (total-host-death undetectability, unscanned-attachment Layer-6, ~0%-adoption "mandated" conventions). This section makes the anti-drift discipline doctrine.

## Mechanism (curated, not exhaustive)

A small, **curated** `narrated_controls:` ledger in `docs/doctrine_manifest.yaml` (~8 named instances) enumerates the known narrated-not-enforced controls; a **binding test** asserts each ledger entry resolves to code-evidence **XOR** carries a dated exception. Deliberately curated — a narrow, maintainable test, **not** a prose-grep or a mini-DSL (the model-ID prose-grep + DSL variant was rejected as unmaintainable). New controls are added to the ledger as they are identified; the goal is a bounded, honest inventory of the gap between claim and enforcement, not total coverage.

## Citation integrity (the same principle, applied to doctrine *references* — class #4)

A doctrine *reference* that resolves nowhere is the citation analogue of a narrated-not-enforced control. The `scripts/check_doctrine_drift.py` gate is doctrine-blessed as **BLOCKING** (promoted from advisory), with a leg that resolves every `Op Stds §N` / `FM §N` citation in current-doctrine prose against the live doctrine table of contents — a citation to a nonexistent § is a drift the gate fails on. Drive the gate clean on `main` first, then flip it to blocking (never flip a dirty gate to blocking).

# §53 (NEW) — Sandbox-Masks-Production: the cutover checklist is gated, not narrated

A control verified only in the **sandbox tenant**, or narrated in `cutover_checklist.md` as prose, may silently not hold in **production**. Forensic class (2026-06-28): the F22 approver-email match and the sheet-name-length-cap classes passed sandbox validation but carried production-only failure modes a hand-checked prose list would not catch. The sandbox→production cutover is therefore a **gated checklist with a mechanical pre-cutover verification step** for each production-only class — not pure narration. Each cutover runs the mechanical checks (at minimum: F22 approver-set live resolution against the real workspace shares; sheet-name-length against the live cap; declared-config-row presence) and **fails loud on a mismatch**, rather than trusting a hand-checked list. This is §52 (narrated→enforced) applied to the cutover boundary specifically — the boundary where sandbox assurances are most likely to be false in production.

# §54 (NEW) — Runtime Secret/PII-Leak Backstop

Distinct from gitleaks (which guards *committed source*), a runtime backstop guards **logged** secrets/PII on the paths that emit operator-facing text: the `error_log` triple-fire (Resend / Sentry / ITS_Errors — §3.1) and migration scripts. A `redact` / no-secret-in-logs test asserts these paths never emit a secret or PII value into an alert, a Sentry event, or an `ITS_Errors` row (the triple-fire fans out to three surfaces — the test covers all three, the multi-surface fan-out discipline). This is the logging-path instance of Invariant 2's "damage ceiling" reasoning: even if upstream handling fails, a secret must not reach an operator-facing log. Operational note: the operator's GitHub PAT scope includes `security_events` so the `codeql-fp-triager` can enumerate CodeQL alerts (previously 403 — the alert-enumeration API requires that scope).

# §55 (NEW) — Verification & Truthful-Reporting Discipline

ITS is built and maintained by AI (Claude Code) sessions that can, without discipline, **lie by
omission, hallucinate current state, or claim work done without validating it.** Three failure
classes recur: (1) acting on a stale-but-confident claim; (2) claiming a change complete when only
one of its N surfaces was touched; (3) reporting success without running the validation. This
section elevates the standing execution-layer reflexes (`docs/HOUSE_REFLEXES.md`) to **canonical
doctrine**, because truthful, validated work is load-bearing for a system whose first invariant is
"failures must be observable, recoverable, and **never silent**." The reflexes remain the how-to;
§55 is the why-it-is-mandatory.

## §55.1 — Verify Before Asserting (anti-hallucination)

Every current-state claim — a file, function, line-range, SHA, PR number, sheet-ID, config value,
or "X is / is not built" — is a **hypothesis until verified against live HEAD.** A brief, audit,
memory note, or prior message naming a code shape has drifted between authorship and now: `grep` /
`Read` the real code and `gh` the real PR before acting or asserting. **Zero grep hits is decisive
over confident memory.** A datum has **N implementations — enumerate ALL of them** before claiming a
value / name / behaviour change is done (a filed-PDF name lives in the Box file + the Smartsheet
attachment + the Worker `Content-Disposition`; a workstream tag lives in `doc_conventions.md` + the
manifest + the lint constant + its spec test). The `brief-validator` agent automates the pre-action
check; run it (or do the checks by hand) before editing on any current-state claim.

## §55.2 — Prove the Control Bites (validate enforcement)

A new test, hook, gate, or guard is **worthless until it RED-LIGHTS on a synthetic violation**:
inject the violation → confirm the control fails → revert. A green control that has never failed is
not proven. For anything that shells out or hits an SDK, add a **live smoke** on top of the unit
test — mocks pass but the live Smartsheet / Box / Graph SDK rejects, a recurring class. **Adversarial
review is definition-of-done on any trust-boundary surface** (an untrusted parse/decode, a
client-or-operator-fed write route, an external-send path): unit tests structurally cannot find
injection, double-send windows, or fail-open misconfig — adversarial review (`/security-review`, the
`ops-stds-enforcer` / `portal-worker-security-reviewer` agents) repeatedly has.

## §55.3 — The Four-Part Landing Verify (validate completion)

A PR is **not "landed"** until all four hold: `state=MERGED` · `mergedAt` non-null ·
`mergeCommit.oid` present · **main-branch CI on the merge commit = SUCCESS.** Passing the first three
while failing the fourth (a post-merge push/deploy failure) is *functionally not landed.* Make no
claim of "merged" / "done" / "shipped" without the four-part verify (`pr-landed-verifier`). Never
deploy, migrate, or audit from a **stale checkout** — `git pull` to latest `main` first; a
behind-checkout reports "no migrations to apply" while the live system already expects the new
tables (the class that caused a universal portal lockout).

## §55.4 — Faithful Reporting (don't lie)

Report outcomes faithfully. If a test failed, say so with the output. If a step was skipped, say
that. If something is uncertain, say uncertain. State done-and-verified **plainly, without hedging —
but NEVER claim done without the validation of §55.1–55.3.** The "never silent" invariant applies to
reporting itself: a silent fallback to a default, a swallowed exception, or a "should work" in place
of an actual run is a form of lying. When a memory / brief / claim turns out stale, **surface the
contradiction** rather than proceeding on it (e.g. a doc that says a file exists when `git log` shows
it never did — report that, don't paper over it).

*Cross-refs: Invariant 1 (External Send Gate) + Invariant 2 (Adversarial Input); §14
(preservation-over-refactor); §30 (SDK-vs-Live integration discipline); §42 (code-level
self-documentation); §43 (successor-remediation runbook). Execution-layer detail:
`docs/HOUSE_REFLEXES.md` §§1–5 + `docs/operations/pr_merge_discipline.md`.*

# Authority

Operational Standards **v21**, 2026-07-12 (verified against exec main; operator-directed doctrine elevation). **New §55 — Verification & Truthful-Reporting Discipline** (§55.1 verify-before-asserting / anti-hallucination · §55.2 prove-the-control-bites · §55.3 the four-part landing verify · §55.4 faithful reporting), elevating the standing execution-layer reflexes (`docs/HOUSE_REFLEXES.md`) to canonical doctrine so future AI sessions do not hallucinate, claim-done-without-validating, or report unfaithfully. **§§4-22 + §25-30 RECONSTRUCTED:** the full v10 bodies were never committed to git (the initial .docx migration brought only the two 'Carry Forward From v10' stubs; the .docx is unavailable), so these 25 sections are faithful reconstructions from the surviving execution-layer paraphrases + code citations — each carries a `> *Reconstructed …*` honesty marker and is subject to correction if the v10 source is recovered. **§4 relabel:** the stub index had mislabeled §4 as "reviewer chain" since v11 (duplicating §15); per 6+ code citations §4 is **Data Fidelity / No-Invented-Field-Data** and the reviewer chain resolves to §15. **Status-fact riders:** §31 roster (`intake_poll` marked retired/deleted, not LIVE), §32 Workstream picklist (+progress_reports, field_ops), §36 tech-debt count (~215 / split file). **Every prior section (§§1–54) otherwise carries forward verbatim** except the three riders; no protective claim is weakened. Companion doctrine bumped in the same pass: Foundation Mission Invariant 1 ("customer-facing" → "external recipient"), Vision & Roadmap §1.4.3 (email-attachment screening = Email-Triage DoD, does not gate Aug-7), Handover Plan → v10 (Check C = 12 jobs, Friday-catch-up closed, 7-workstream roster). v20 retires on acceptance of v21. Canonical git tag: `operational-standards-v21`.

Operational Standards **v20**, 2026-07-06 (verified against exec main `987f4f4`). The **consolidation** bump, operator-directed. **New §§ (its#341 forensic-retrospective candidates, ratified):** §52 narrated-not-enforced — every built control/guarantee ships a binding test **or** a dated exception (the curated `narrated_controls` ledger + the citation-integrity leg of the now-BLOCKING doctrine-drift gate); §53 sandbox-masks-production — the sandbox→production cutover is a **gated** checklist with mechanical pre-cutover verification, not narration; §54 runtime secret/PII-leak backstop — a `redact`/no-secret-in-logs test on the `error_log` triple-fire + migration scripts (distinct from gitleaks) + the `security_events` PAT scope. **Amendments:** §31 daemon-scaffold DoD hardened (`sys.executable` / `RunAtLoad` / external catch-up / empty-commit guard, class #15); §43 coverage audited (every Tier-2-reachable capability ships its entry as DoD). **§23/§24 seventh standalone workspace** (`ITS — Progress Reporting`) ratified as a workspace-topology change (the v17 sixth-workspace precedent). **§51 folded:** the Material List is now **one-way-up (phased; M2b bidirectional receive deferred)** and the low-volume period-split is a direct clause — folding the 2026-07-04 (hours-log low-volume) + 2026-07-06 (Material-List one-way) v19.x riders; the 2026-07-03 §3.1/§3.2 Sentry-leg rider is likewise folded (the §3.1/§3.2 main text already reflects deduped-push). **Every prior section (§§1–51) carries forward verbatim** except the two amendments (§31, §43) and the four folded clarifications; no protective claim is weakened by any fold. v19 retires on acceptance of v20. Canonical git tag: `operational-standards-v20`. The three v19.x rider entries below are retained for provenance, marked **[FOLDED INTO v20]**.

Operational Standards **v19**, 2026-06-29 (verified against exec main `f98f56f`). §§50–51 added — the **privileged code-actuation gate** (§50), ratifying the candidate raised first at Safety Portal mission v4 (2026-06-10) and already realized in `publish_daemon.py`; and **ITS-owned structured-SoR write-back** (§51), ratifying the 2026-06-28 Progress-Reporting candidate, extended per operator decision 2026-06-29 to explicitly name the **job-tracker → Active-Jobs write** as a covered instance. Both were carried propose-only (Safety Portal mission v4/v5; Progress-Reporting mission §16(a)/(b); info-gap §3/§8; memory-archive §G35/§G44) pending Developer-Operator ratification; this v19 bump resolves the §50/§51 numbering collision (§50 = code-actuation, raised first; §51 = SoR-write). **Every prior section (§§1–49) and the audience-separation principle itself carry forward verbatim from v18.** v18 retires on acceptance of v19. Canonical git tag: `operational-standards-v19`.

**[FOLDED INTO v20 — retained for provenance]** v19.x amendment rider (2026-07-03, verified against exec main `3fc1e3a`): **§3.1/§3.2 Sentry-leg reclassification — record → deduped-push.** Operator-ratified 2026-07-03 ("let's go with option one" — option 1 of the unbounded-growth audit: the Sentry free-tier quota burns in ~3.5 days under a CRITICAL storm while protecting nothing ITS_Errors doesn't already record). Resend AND Sentry are now both dedupe-subject push legs, each gated on its own key — Sentry's deliberately namespaced `sentry::{script}::{error_code}` so each leg's window opens only on its own successful delivery (a shared entry would leave Sentry ungated during a Resend outage, or suppress emails nobody received); ITS_Errors is the SOLE always-write per-occurrence record; watchdog Check G tags a Sentry-key summary subject `[sentry-leg]`. **Why a v19.x rider and not a v20 bump:** the protective claim of the CRITICAL alert path is unchanged — the operator still gets paged (Resend, first-per-window), ITS_Errors carried the complete per-occurrence forensic record before and after, and Sentry was never a prevention layer (prevention remains Invariant-2 Layers 2–4 + Invariant 1). No §N is added, removed, or renumbered. Read strictly, the v20 trigger's "recharacterization of a mechanism's protective claim" could be invoked (the v13→v14 precedent: recharacterizing what a mechanism *is* is bump-worthy); this rider records the ratified judgment that reclassifying a redundant push leg's quota economics does not change any protective claim — the same test the v16.x absorption applied — so it lands per that precedent: **no major bump, no new tag, every existing "v19" citation remains valid.** A future consolidation (v20) folds this in. Prior §3.1/§3.2 text recorded inline at the amended sections for provenance. Exec realization: `shared/error_log.py` `_fire_sentry_leg` dedupe gate + `scripts/watchdog.py` Check G `[sentry-leg]` tagging (branch `feat/sentry-dedupe-ratified`).

**[FOLDED INTO v20 — retained for provenance]** v19.x amendment rider (2026-07-04, verified against exec main `cb58ca8`): **§51 accumulating-log period-split — refined for LOW-VOLUME logs.** Operator-ratified 2026-07-04 (Path B of the P7 Hours Log slice decision — "let's go with Path B"). §51's "accumulating logs are period-split + archived-on-closure, never `delete_rows`, under an A5 row-cap watchdog" guard is CLARIFIED for a **low-volume** accumulating log (e.g. the per-job Hours Log — a few crew time entries/day/job): its **period-split** is satisfied by a **single standing per-job sheet whose split is TRIGGERED by the A5 row-cap watchdog** — a SoR-safe WARN monitor (`progress_reports/hours_log.py` `check_row_cap`) that, as the sheet nears the Smartsheet ~20k/sheet row cap, WARNs + Review-Queues an operator period-split (archive this sheet, start a fresh one) — **rather than mandatory calendar-period splitting**. **Rationale:** Smartsheet sheet proliferation is the #1 scaling risk (2026-06-28 20×20 eval); a low-volume log stays far under the row cap for years, so calendar-splitting it is premature proliferation (3 standing tracker sheets/job vs. ~36/job/yr). The **protective claim is unchanged** — a bounded SoR sheet that never exceeds the cap, never `delete_rows`, and is archived on closure — only the split *trigger* moves from calendar to row-cap, for a volume class §51 did not distinguish. **archive-on-closure + never-`delete_rows` remain required, unchanged:** never-delete ships now (`hours_log`); **archive-on-closure is a COMMITTED follow-up** (exec its#462) that MUST land before the first job's lifecycle → `archived` — deferred only because it needs a new `smartsheet_client` move-sheet method (§30). Its `archived` trigger is LIVE today (portal admin), not distant; until #462 the exposure is **bounded and recoverable** — a never-deleted, stranded Hours Log sheet, no data loss — but the archive guarantee is skipped, so #462 must land before archival activity (and no Hours Log exists at all until `hours_enabled` is flipped). **Why a v19.x rider and not a v20 bump:** no §N is added, removed, or renumbered; the protective claim is preserved (bounded, never-past-cap, never-delete, archive-on-close); only the period-split *mechanism* is clarified for a low-volume class — the same "does not change any protective claim" test the 2026-07-03 Sentry rider + the v16.x absorption applied → **no major bump, no new tag, every existing "v19" citation remains valid.** A future consolidation (v20) folds this in. Exec realization: `progress_reports/hours_log.py` (`check_row_cap` SoR-safe row-cap WARN watchdog) + `field_ops/fieldops_sync.py` hours pass (branch `feat/p7-hours-log`, PR #461); archive-on-closure tracked exec its#462.

**[FOLDED INTO v20 — retained for provenance]** v19.x amendment rider (2026-07-06, verified against exec main `7a892f2`; M2 ship = #470 `f7f3764`): **§51 Material List — phased delivery (one-way-up MVP now, bidirectional receive as a future M2b).** Operator-ratified 2026-07-06 ("the materials list is shipping as one way for now"). §51 above names the Material List as "bidirectional with split column ownership." That end state is delivered in **two phases**. **M2 (shipped, #470)** is a **one-way-up snapshot** inside `field_ops.fieldops_sync` — the per-job Material List re-projects UP into the ITS-owned `<Job> — Material List` sheet each cycle (non-clobbering, column-scoped, never-`delete_rows`, archive-on-closure per its#462, under the A5 row-cap watchdog), with **no operator-content receive direction** (no `smartsheet_row_id`, no down-sync — an operator editing the Smartsheet Material List directly has no path back to D1). **M2b (future)** adds the bidirectional split-ownership receive when a Material-List operator-edit workflow actually exists. **Protective-claim analysis (the rider's load-bearing claim):** every §51 *protective* guard — send-free + AI-free GATED daemon (`send_mail`/`anthropic` forbidden), `WALKED_ROOTS` enrollment, allowlisted `shared/portal_client.py` egress, validated find-or-create + A1 margin-check, non-clobbering column-scoped write, never-`delete_rows` + archive-on-closure — is met by shipped M2; the one-way phase is strictly *more* conservative than the constrained bidirectional posture (it never writes operator-owned columns and never reads operator edits back). The **removed capability** — the operator's ability to edit Material-List content columns as a system input — is a **feature deferral, not a protection weakening**; §51's split-ownership non-clobber guarantee is preserved intact for M2b (it has no surface to bind to until the receive workflow ships). **Why a v19.x rider and not a v20 bump:** no §N is added, removed, or renumbered, and no *protective* claim is weakened — only the Material-List clause's *delivery* is clarified as phased; the same "does not weaken a protective claim" test the 2026-07-04 low-volume-log rider + the 2026-07-03 Sentry rider applied → **no major bump, no new tag, every existing "v19" citation remains valid.** A future consolidation (v20) folds this in. **Enables** flipping `field_ops.fieldops_sync.materials_enabled=true` (the ITS_Config row exists, value `false`, created 2026-07-05 — visible for the flip). Exec realization: `field_ops/fieldops_sync.py` `_mirror_material_list_pass` + `progress_reports/material_list.py` (#470, migration 0039); ships DARK until the flip. Proposal provenance: `docs/audits/2026-07-05_section51-materials-rider-proposal.md` (Path 1, Reading A).

Operational Standards **v18**, 2026-06-07 (verified against exec main `f3ad814`; the full deploy-session batch PRs #178–#189 merged, including PR-H #185 admin route and PR-K #189 Box-mirror). §§45–49 added — find-or-create-not-strand (§45); workspace-membership = approval authority, the in-code F22 realization of the §23 principle (§46); Box version-on-conflict for deterministic-name re-uploads (§47); CodeQL false-positive handling (§48, newly codified — previously tooling+memory only); preservation-for-a-committed-future-workstream, extending §14 (§49). These generalize as-built patterns from the Safety Portal deploy-session cluster (exec PRs #178–#189); the verification corrected several ledger claims before codification (owner-inclusion is *not* asserted in §46; the §48 dismiss-block hook is agent-scoped, not global; PR-K's Box root is the `ITS_Config` key `safety_reports.box.portal_root_folder_id`, not a hardcoded id). **Every prior section (§§1–44) and the audience-separation principle itself carry forward verbatim from v17.** v17 retires on acceptance of v18. Canonical git tag: `operational-standards-v18`.

Operational Standards **v17**, 2026-06-05 (verified against exec `753f12f`, PR #171). **§23/§24 sixth-workspace addition:** §23 now acknowledges the Safety Portal's **standalone, approval-gated workspace** (`ITS — Safety Portal`) as a deliberately-scoped, additive exception to the five-workspace audience-separation model — governing principle *workspace-membership = approval authority*; self-contained so the safety subsystem ships and hands over independently. §24's ID inventory gains the workspace, the moved `Safety Portal` folder (ID preserved), and `WSR_human_review`. This is a §23/§24 content change only — **every other section and the audience-separation principle itself carry forward verbatim from v16.** Originating workstream doctrine: [Safety Portal mission §8](../workstreams/safety-portal/mission.md#8-self-containment-and-workspace-as-approval-authority). v16 retires on acceptance of v17. Canonical git tag: `operational-standards-v17`.

Operational Standards v16, 2026-06-01. Tier-2 boundary reframe: v16 removes the "non-developer-safe enforcement layer" framing introduced in v15 — a structural guard that v15 named as a hard pre-cutover build gap — and replaces it with the training-bounded co-resolution model. There is no structural maintenance enforcement layer; none is built or required. §44's Tier-2 boundary now holds by the trained operator's judgment + the both-rule + co-resolution with the Developer-Operator until per-category clearance. The Successor-Operator is redefined as a trained operator who runs Claude Code himself (not a Smartsheet-UI-only approver). §43, §44's LOW/HIGH capability-class sets, the both-rule, the audit-trail requirement, the §§37-41 role-scope clarifier, and the v14 §1 kill-switch reframe all carry forward. The Tier-1 self-heal gap (Check C marker-file staleness floor, §2 — earlier called "Check H") survives as a standalone pre-cutover gate, its stale status characterization corrected in a v16.x absorption (below); the v15 "BOTH" coupling to a Tier-2 enforcement layer is removed. No execution-layer mechanism is asserted as built. v15 retires on acceptance of v16. Canonical git tag: operational-standards-v16.

v15 trigger: §43 + §44 added (Successor-Remediation Documentation Discipline; Tier-2 Claude-assisted repair path) and the Developer-Operator / Successor-Operator role split applied across §§37-44. v14 was complete on its own terms; v15 codifies the operator-decided three-tier non-developer-successor maintenance model and names the Tier-2 non-developer-safe enforcement layer as a hard pre-cutover build gap (alongside the Tier-1 Check H self-heal gap). Tag pushed post-merge: `operational-standards-v15`.

v16 trigger: §44's Tier-2 protective basis recharacterized from structural (a "non-developer-safe enforcement layer," named in v15 as a hard pre-cutover build gap) to training-based (trained operator + both-rule + co-resolution); the Successor-Operator role redefined accordingly. Per the v16-trigger criterion the v15 doc carried ("recharacterization of a mechanism's protective claim"), changing §44's basis from structural to training/co-resolution is exactly that — a major bump, not a v15.x status update. Tag pushed post-merge: `operational-standards-v16`.

v17 trigger: substantive doctrine change, new §, or recharacterization of a mechanism's protective claim. The v13→v14 reframe established that recharacterizing what a mechanism *is* is bump-worthy; v14→v15 established that a doc-wide role abstraction + a new tier is; v15→v16 established that changing a tier's protective basis (structural → training/co-resolution) is. v16.x absorbs further status updates (e.g., per-category clearances granted to the Successor-Operator) without major revision. **Realized 2026-06-05** by the §23/§24 sixth-workspace addition (the Safety Portal standalone workspace) — a substantive doctrine change.

v18 trigger: substantive doctrine change, new §, recharacterization of a mechanism's protective claim, or a further change to the workspace-topology model. v17.x absorbs status updates (e.g., additional per-customer Safety Portal workspaces at onboarding) without a major bump. **Realized 2026-06-07** by §§45–49 (new sections generalizing the Safety Portal deploy-session patterns).

v19 trigger: substantive doctrine change, new §, recharacterization of a mechanism's protective claim, or a further change to the workspace-topology model. v18.x absorbs status updates without a major bump (e.g., the PR-K Box-mirror and PR-H admin route both landed in the same deploy batch and are absorbed at the workstream-doc + §G26 level — the §§45–49 patterns themselves are unchanged; further Safety Portal activation progress likewise absorbs at v18.x unless it recharacterizes a mechanism). **Realized 2026-06-29** by §§50–51 (the privileged code-actuation gate + ITS-owned structured-SoR write-back, ratifying two long-carried propose-only candidates and resolving the §50/§51 numbering collision).

v20 trigger [**REALIZED 2026-07-06**]: substantive doctrine change, new §, recharacterization of a mechanism's protective claim, or a further change to the workspace-topology / SoR-write model. Realized by the operator-directed consolidation — its#341 §§52–54 (narrated-not-enforced / sandbox-masks-production / secret-PII backstop), the §23/§24 seventh standalone workspace, the §31/§43 amendments, and the §51 Material-List one-way + low-volume-period-split fold.

v21 trigger: substantive doctrine change, new §, recharacterization of a mechanism's protective claim, or a further change to the workspace-topology / SoR-write model. v20.x absorbs status updates without a major bump (e.g., additional ITS-owned-SoR up-sync daemons that instantiate the §51 pattern unchanged, or additional `narrated_controls`-ledger entries under §52).

v16.x status absorption (2026-06-01, verified against exec 585823d): the §2 / §44 Tier-1 self-heal characterization is corrected. The mechanism described as an unimplemented "Check H heartbeat-staleness" check (reading ITS_Daemon_Health, 2 × Interval) with "two of three daemons heartbeat-retrofit-pending" was **never built**; the implemented staleness floor is the watchdog **Check C marker-file** check, which already covers all four tracked daemons (safety_intake, safety_weekly_send_poll, safety_weekly_generate, safety_picklist_audit), and the external **UptimeRobot** ping (audit F16) is live. The lone residual is the weekly_generate Friday-crash **catch-up** (exec follow-on). This correction does **not** change what the Tier-1 self-heal mechanism *is* or its protective claim — Tier-1 is still "daemons recover, the watchdog catches staleness, no human acts" — it corrects the stale *implementation-state* claim, so per the v17 trigger it is a **status update absorbed at v16.x: no major bump, no new tag.** The prior "Check H" framing is recorded here (and at §2 / §44 / line 94) for provenance.

v14 trigger: §1 kill-switch security-posture reframe (F07). v13 was complete on its own terms; v14 corrects doctrine that over-described a fail-open pause as a security control. Tag pushed post-merge: `operational-standards-v14`.

v13 trigger: code-level self-documentation discipline added (§42). v12 was complete on its own terms; v13 captures a discipline whose absence was surfacing as a recurring "future-reader has to leave the file" cost. Tag pushed post-merge: `operational-standards-v13`.

Companion to FM v11 (Invariant 1 two-process model still informs how the Tier-2 boundary is drawn; the Developer-Operator / Successor-Operator role principle, with the Successor-Operator redefined as a trained CC operator), V&R v9 (the ship-and-leave / developer-departure threshold; the Tier-1 self-heal gap remains the companion hard pre-cutover condition; the Tier-2 boundary is training-enforced, no enforcement-layer gap), Handover Plan v8 (the three-tier fault-response model + role definitions + Pre-Cutover Conditions), Excellence Roadmap v4 (R6 successor-maintenance build program, with the Tier-2 enforcement-layer sub-deliverable replaced by Tier-2 readiness work), Permissions Ask v5 + System+HR Handoff v6 (Successor-Operator vs Developer-Operator access split — their role descriptions predate this reframe and are pending a role-redefinition follow-on), FSU v6.5, Memory Archive v5 (extended §G7 in v12 parallel PR), `references/customer-fork-setup-checklist.md` (downstream cascade in v12). v13 parallel companion: `prompts/scaffold/` (PR 2 of that cascade — `shared-module-migration.md`, `manual-smoke.md`, `cc-implementation.md` v1 → v2).