---
type: audit
status: canonical
last_verified: 2026-05-29
last_verified_against: e7f8764
workstream: null
audited_against: its-blueprint doctrine @ main (e7f8764) — Foundation Mission (frontmatter v9 / title v9), Operational Standards (frontmatter v14 / title v14), Vision & Roadmap (frontmatter v7 / title v7.2), Handover Plan (frontmatter v6 / title v6.3), Excellence Roadmap (frontmatter v2 / title v2.3); references sweep
also_reviewed: references/permissions.md, references/system-hr-handoff.md (v5), references/customer-fork-setup-checklist.md (v1), references/daemon-health-schema.md (v1), references/worktree-discipline.md, references/foundation-scaffold.md, references/claude-code-info-gap.md
tags: [successor-maintenance, document-as-you-build, role-abstraction, ship-and-leave, tier-2-gap, propose-only, customer-facing-assurance]
---

# ITS — Successor-Maintenance Model Audit (2026-05-29)

## 0. Verdict (read this first)

**The operator's three-tier successor-maintenance model is `ASSUMED-BUT-UNSTATED` in doctrine — and on the load-bearing tier it is `ABSENT`.**

This audit measures current ITS doctrine against the operator's stated model:
a **non-developer Evergreen successor**, assisted by **Claude**, keeps the system
running after the developer (Seth) steps back from daily operation — fixing
faults by **intuiting them from processes documented at build time**, and
escalating only severe/undocumented faults to Seth as a reachable asset.

Doctrine does not specify that model. It specifies a **different, lower-bar
model**: a system that **runs unattended and fails loud**, maintained by
**remote developer support** (Solution Smith over Tailscale), with eventual
handoff to a **trained, developer-grade maintainer** "when one exists." Where
doctrine gestures at a successor at all, it specifies the *opposite* of a
non-developer.

| The operator's claim | Verdict **as audited** | What doctrine actually contains |
|---|---|---|
| **Tier 1** — daemons self-heal, no human needed | **ABSENT** (self-heal) · the adjacent lower bar is **PARTIAL & partly unbuilt** | Detection + degrade-and-continue + page-a-**developer**. No autonomous arbitrary-fault repair. Even the monitoring is 2/3 unbuilt today. |
| **Tier 2** — non-developer + Claude diagnose and fix | **ABSENT** | Nothing. Zero hits for "non-developer", "document-as-you-build", "intuit", or a human "successor…fix". The one successor doctrine names is a *trained, traceback-reading* maintainer. |
| **Tier 3** — Seth = reachable escalation asset, *not* the operator | **CONTRADICTED** | Doctrine makes "Solution Smith…the primary operator" (remote-support is "what's offered"). Seth is never named as a fault-escalation tier. |
| **Document-as-you-build** for non-dev maintainability | **GAP** (build-time-discipline) | Only §42 *code* self-documentation — wrong audience (code-readers) and soft, developer-gated enforcement. |
| A defined **non-developer successor role** | **ABSENT** | "The operator" = a git/CC/shell-fluent developer throughout. Three conflated, undefined role labels. |

> **Anti-inflation statement (per the brief's honesty mandate).** Do **not** read
> the two non-`ABSENT` cells as "the model is half-built." Tier 1's captured half
> belongs to a *different, lower* model (unattended-system-that-pages-a-developer),
> and even that is partly unbuilt; Tier 3's "remote-recovery capability exists" is
> positioned as the *primary* maintenance model with the developer as standing
> operator — the inverse of the audited claim. **The load-bearing Tier 2 is absent,
> and the framing of the other two tiers is contradicted by doctrine's actual
> maintenance model.** If "a non-developer maintains it via Claude" is represented
> to the Evergreen customer, doctrine does **not** substantiate it.

---

## 1. Scope, method, and actual versions

**This is a propose-only, read-and-report audit.** It edits no doctrine. Any
doctrine-writing that follows is a separate PR after the operator reads these
findings.

**Actual doc versions** (the brief's guesses were partly off; reported live):

| Doc | Frontmatter `version:` | Operative title | Brief guessed |
|---|---|---|---|
| Handover Plan | `6` | **v6.3** | v6.3 ✓ (title), not frontmatter |
| Vision & Roadmap | `7` | **v7.2** | v7.2 ✓ (title), not frontmatter |
| Foundation Mission | `9` | **v9** | v9 ✓ |
| Operational Standards | `14` | **v14** | v14 ✓ |
| Excellence Roadmap | `2` | **v2.3** | (not guessed) |

> Note: every doctrine doc carries the *major* integer in frontmatter and the
> operative *minor* in the title line. This split is itself a successor-reference
> hazard — see Gap **G7**.

**Read in full:** the five doctrine docs above, plus `references/permissions.md`,
`references/system-hr-handoff.md`, `references/customer-fork-setup-checklist.md`,
`references/daemon-health-schema.md`, `references/worktree-discipline.md`,
`references/foundation-scaffold.md`, `references/claude-code-info-gap.md`.

**Verification discipline.** Findings were produced by independent per-doc
extraction, synthesized, then **adversarially challenged** by three lenses
(over-claim, under-claim, quote-integrity), each re-opening the source files.
The quote-integrity pass caught **one fabricated supporting quote** in an early
draft (a non-existent "30 consecutive days…permanent human review" threshold
attributed to V&R); it has been **removed**, and the corrected fact strengthens
the finding it supported (see G5). Every quote below was verified verbatim
against the cited file and line.

**The empirical floor (grep-confirmed, re-run during verification):** across all
of `doctrine/` and `references/`, the strings **"non-developer", "document-as-you-build",
"intuit", and "successor…fix" return ZERO hits.** "successor" appears only as the
watchdog "Check H (successor to Check F)" — a *monitoring check* replacing another
check, never a human successor.

---

## 2. The yardstick (the model being measured)

- **Tier 1 — Routine / self-healing.** Daemons recover, watchdog catches, no human needed.
- **Tier 2 — Successor + Claude resolve it.** A *non-developer* successor, assisted by Claude, diagnoses and **fixes** the fault by intuiting it from processes **documented at build time** + guardrails. No developer needed. *(Load-bearing.)*
- **Tier 3 — Severe → escalate to Seth.** Seth is a reachable escalation **asset**, *not* the operator. Only severe/undocumented faults reach him.

---

## 3. Per-tier findings

### Tier 1 — "self-healing" → **ABSENT as audited**; lower bar **PARTIAL & partly unbuilt**

**What is genuinely captured (a lower, different bar):**
- Daily launchd watchdog pages a human: *"Silent if green; emails + SMS the operator if anything is off"* — Op Stds v14 §2, **L104**.
- Heartbeat-staleness detection: Check H *"reads ITS_Daemon_Health for every Enabled=true daemon and flags rows where Last Heartbeat is older than 2 × Interval Seconds"* — Op Stds v14 §2, **L112**.
- Triple-fire CRITICAL so failures surface loud — Op Stds v14 §3, **L122**; *"loud, not silent"* — Handover v6.3 Risk Inventory, **L89**.
- **Real fault-isolation / degrade-and-continue discipline** (this is genuine, mandated fault tolerance, not just detection): *"Heartbeat failure must NEVER block the daemon's primary work — failure isolation"* — `daemon-health-schema.md` §4.3 **L152**; *"MUST NOT raise to the caller. Wrap in try/except, log to ITS_Errors… continue"* — §8.3 **L263**. Confirmed in production: intake_poll with *"fcntl lock, ITS_Config gate, seen-set idempotency, heartbeat write… 242+ confirmed cycles in production"* — `foundation-scaffold.md` **L93**.

**Why this is not the audited Tier 1:**
- Daemons are **re-launched by launchd**, not self-repaired — restart-by-scheduler (Op Stds v14 §31, **L180-184**). *No doc describes autonomous recovery of an arbitrary fault.* The captured behavior is "fails loud, pages a human; recovery is a (developer) touch."
- **The monitoring floor is itself 2/3 unbuilt.** §31 daemon roster (**L188-192**): only `intake_poll` is `LIVE (PR #60)`; `watchdog` and `picklist_sync` are both **"Retrofit pending"** — Check H can see one daemon today. Check H is listed as an **unmet pre-cutover *condition*** (Handover v6.3, **L80**), not a live capability; Check E (spend) is *"deferred to Phase 1.5"*; the Box-token-age check is *"queued for R2 follow-on PR… Until that check lands"* (Handover v6.3 **L89**).
- The kill-switch fail-open is **not** a self-heal/graceful-degradation feature: v14 §1 reframed it as an *"operator-convenience suggested pause… explicitly NOT a security boundary… fail-open by design"* (**L82/88/92**, F07). It must not be credited toward Tier 1.

**Net:** the audited "self-heal, no human needed" is **ABSENT**. A lower bar
(detect + degrade-and-continue + page) is real but **developer-aimed and partly
unbuilt**.

### Tier 2 — "non-developer + Claude diagnose and fix" → **ABSENT** (load-bearing)

Judged strictly, this tier is absent. **No doc anywhere describes** (a) a
non-developer successor, (b) Claude-assisted fault diagnosis-and-fix, (c) intuiting
a fix from build-time-documented operational processes, or (d) a build-time
discipline producing non-developer-readable remediation docs. The grep floor (§1)
confirms it.

The closest real evidence **contradicts** the audited model:
- **The only successor doctrine names is developer-grade.** *"Operators handle ITS_Review_Queue items… and need **maintainer-level system understanding**. Day-to-day reviewers… do not need maintainer training"* — `system-hr-handoff.md` **L41**. There is **no middle "non-developer fixer" tier** — you are either a maintainer-level operator or a no-training reviewer.
- **That maintainer reads tracebacks as Seth's peer.** *"ITS_Errors is the surface **Seth and a trained maintainer scan during morning checks**"* — `system-hr-handoff.md` **L106** (the sheet carries a stack-trace column). The role is also explicitly aspirational: *"future trained Evergreen maintainer"* (**L39**), *"added later when one exists"* (**L49**).
- **It is backed only by an access grant, with no fix workflow.** *"Trained maintainer at customer (when one exists): ADMIN on ITS — System workspace. This is a graduation event; not granted at initial cutover."* — `permissions.md` §3.2 **L119**.

The real **non-developer** role that exists — the Handover v6.3 "customer admin" —
is scoped strictly to **Smartsheet data entry + understand-and-escalate**, never
diagnosis-and-fix: add/disable a trusted-contact row (**L54-56**), flip
`system.state`, approve a review-queue row, respond to a Sentry email (**L48**),
and *"escalates to operator if persistent legitimate-sender routing fails surface"*
(**L60**). Even within that, non-trivial change routes to the developer: a new
picklist value *"must be updated by Solution Smith via remote support"* (**L58**).

> If the operator represents "a non-developer maintains it via Claude" to Evergreen,
> **doctrine does not substantiate it — and the one successor doctrine does describe
> is the opposite of a non-developer.**

### Tier 3 — "Seth = reachable asset, not the operator" → **CONTRADICTED**

A remote-human-recovery capability exists, but doctrine positions it as the
**primary** ongoing-maintenance model with the **developer as standing operator** —
the inverse of the audited claim.

- *"ongoing maintenance is per the remote-support model"* — Handover v6.3 Step 8, **L46** (the operative post-handover model).
- *"Remote-support model (Tailscale-managed VPN) is what's offered"* — Excellence Roadmap v2.3, **L74**.
- *"**Solution Smith remains primary operator** until the customer has a trained maintainer in place"* — `permissions.md` §3.2, **L119**. Seth is the *standing* operator by default, not a backstop.
- **Seth is never named as a fault-escalation tier.** In Op Stds, "Seth" appears only as *"future-Seth"* — a **code reader** (§42, **L550**). The L1/L2/L3 "escalation" picklists in the references are a *content-review reviewer chain* (Teala → Sam → Jacob), not fault-maintenance escalation.
- **Permanent human-in-the-loop review is in tension with any "developer departs" model:** *"No external transmission without explicit human approval. Permanent, not time-bounded. Earlier framing… that described review as a 30-60 day window is superseded."* — Foundation Mission v9, Invariant 1, **L38**.

**Nuance (fair to doctrine):** §3.2 is *transitional* — Seth steps back *"until a
trained maintainer"* exists, and `permissions.md` L27 frames steady-state operation
as needing no privileged human action. So doctrine *does* anticipate Seth stepping
back — but **to a trained, developer-grade maintainer**, not to the audited
non-developer-with-Claude. The asset-vs-daily-operator distinction the operator
asserts is **contradicted, not captured**.

---

## 4. The document-as-you-build question — answered directly

> **Does doctrine mandate "document-as-you-build for non-developer-successor
> maintainability," or only assume a handover document gets written eventually?**

**Answer: NEITHER fully — and the load-bearing version is a GAP.** A build-time
documentation discipline exists and is the *right shape* — **Op Stds v14 §42** — but
it is the **wrong kind** for Tier 2 on two axes:

**1. Wrong audience — it documents CODE for code-readers.**
- §42 mandates module docstrings (Purpose / Invariants / Failure modes / Consumers)
  for *"every new `shared/*` module and workstream entrypoint"* (**L72, L554**).
- Its stated audience is explicit: *"Every `shared/*` module… will be read again — by
  **future-Seth, by future-CC, by the maintainer of a customer fork three months
  out**. The code should answer 'why' without forcing the reader to leave the file."*
  — **L550**. Every named reader reads **source code**; the "maintainer" here is a
  code-reading, developer-grade reader. A non-developer successor never opens a
  `.py` file.

**2. Soft, developer-gated enforcement.**
- *"Initial enforcement is by convention + review… Operator review at PR time checks
  for docstring presence"* — **L619-621**. Stricter (AST/ruff) enforcement is only a
  *future trigger* (**L623**); retrofit is *"opportunistic… NOT a sweep PR"* (**L609**).
- So even the code discipline depends on a **developer reviewing PRs** — the very role
  the audited model removes.

**What exists for operational processes is either developer-facing, one-time, or
document-AT-handover (not document-as-you-build):**
- `tech_debt.md` log (Op Stds §36) — build-time, but keyed to code/PR context for developer-readers.
- A daemon runbook exists — *"Operator runbook: daemon install + uninstall + troubleshooting"* (`foundation-scaffold.md` **L96**) — but lives in the exec repo and is CLI/launchd work.
- `customer-fork-setup-checklist.md` — a genuine operational-process doc, but a one-time **setup/provisioning** process run via `gh api` / `gitleaks` / CodeQL by a developer-operator, not fault remediation.
- Handover artifacts (post-handover acceptance sign-off; *"Captured here so it's transferred at handover"* — `system-hr-handoff.md` Pattern 3, **L340**) are **document-at-handover** end artifacts, not as-you-build.

**Conclusion:** doctrine **assumes** a handover document/runbook is written
eventually; it does **not mandate** documenting operational processes for a
non-developer successor as the system is built. **This is a build-time-discipline
gap (G2)** — the kind that changes *how* remaining work must be built.

---

## 5. The role-abstraction question — findings

**Verdict: FAIL.** "The operator" is overwhelmingly assumed to be a **developer
present at the machine**. There is no defined successor-operator role distinct from
Seth. Doctrine uses **three undefined, conflated** human-role labels — "operator",
"customer admin", "customer maintainer"/"trained maintainer" — without reconciling
them.

The only invariant-level human-role distinction is an **access-visibility** boundary,
**not** a maintenance/fix-capability boundary: *"Audience-based access boundaries
(operator vs customer-employee surfaces)"* — Foundation Mission v9, Operating
Principles, **L32**. (This is positive confirmation for Gap **G1**: what exists is
an access split, not a successor-fixer role.)

A minority of "operator" actions are genuinely non-developer (Smartsheet-UI:
kill-switch flip, picklist conversion, trusted-contact/quarantine review). But the
**bulk of documented maintenance/fix actions require git / CC / shell / `gh api` /
Keychain fluency** — each a **Tier-2 blocker**, none mentioning Claude assistance to
bridge the gap:

| Verbatim quote | Location | Why it blocks a non-developer successor |
|---|---|---|
| *"Recovery operations (e.g., `git branch -D`…) are performed manually by the operator in their own shell."* | Op Stds v14 §38, **L406** | Clearest single "operator = git/shell-fluent" statement. |
| *"Operator-touch recovery: re-run `scripts/setup_box_oauth.py`."* | Handover v6.3 Risk Inventory, **L89** | Recovery = running a Python script on the MacBook. |
| *"operator verifies via Keychain Access"* | Handover v6.3 Pre-Cutover (Box OAuth) | Inspecting macOS Keychain presumes OAuth/Keychain internals. |
| *"Apply v3.1 errata pattern: Connect-ExchangeOnline + New-ServicePrincipal -AppId… -ObjectId…"* | Handover v6.3 Risk Inventory, **L86** | Embedded PowerShell remediation runbook. |
| *"verify scope is per-repo not All-repositories; verify expiration dates set; revoke unused."* | Op Stds v14 §39 Operator-Only Audit, **L469** | GitHub PAT/security audit; `gh`-auth fluency. |
| *"run gitleaks against full history (`gitleaks detect --source . --log-opts="--all" --redact -v`)."* | Op Stds v14 §39, **L478** | Running gitleaks over git history from a shell. |
| *"Verify the latest stable tag via API: `gh api …/releases/latest`… Surface the breaking change to operator."* | Op Stds v14 §41, **L519/532** | Version-bump work; reading release notes for breaking changes. |
| *"All `scripts/migrations/*`… dry-run path may print PII (operator review); live-write path strips PII."* | Op Stds v14 §40, **L486-488** | Running migration scripts; reading dry-run vs live output. |
| *"State files at `~/its/state/<daemon>_*.json`… log path `~/its/logs/launchd/<daemon>.{out,err}.log`."* | Op Stds v14 §31, **L180-184** | Diagnosing a daemon fault means reading JSON state + launchd `.err` logs. |
| *"operator-side ClamAV install + code + tests"* | V&R v7.2 Deliverable 1.4.3, **L72** | "The operator" is expected to install, **write code**, and run tests. |
| *"Refactor `safety_reports/intake.py`… via `shared/graph_client.py` extensions."* | V&R v7.2 Deliverable 1.4.2, **L54-56** | Refactoring Python modules attributed to "the operator". |
| *"worktree cleanup is an operator action run in a normal shell, not something a CC session performs."* | `worktree-discipline.md` Cleanup, **L115-116** | `git worktree remove --force` / `git branch -D` in a shell. |
| *"the operator re-runs `scripts/setup_box_oauth.py`… the refresh token in Keychain rotates"* | `permissions.md` Ship-and-leave caveat, **L185** | Running a Python script + reasoning about Keychain refresh tokens. |
| Entire fork-setup checklist (`gh api` / gitleaks / brew / CodeQL) | `customer-fork-setup-checklist.md` | Security-savvy developer judgment throughout. |

---

## 6. Prioritized gap list (propose-only)

> These describe what doctrine **would need** to make the three-tier model real.
> They are **not written here** — surfacing them is the deliverable.

| ID | Gap | Belongs in | Type | Priority |
|---|---|---|---|---|
| **G1** | No defined **non-developer successor-operator role** distinct from Seth, with an explicit capability boundary (Smartsheet-UI + Claude vs. escalates). Doctrine conflates "operator" / "customer admin" / "trained maintainer" and the only role split is access-visibility (FM L32). | FM (promote Operating-Principles split into a maintenance-role model) + Handover (define the role the Day-7 routing gate hands off to) | handover-artifact | **P0** |
| **G2** | No mandated **build-time discipline producing non-developer-readable operational/fault-remediation docs** ("successor runbook") as each module/workstream is built — analogous to but distinct from §42. | Op Stds (new section parallel to §42) + CLAUDE.md session-close table | **build-time-discipline** | **P0** |
| **G3** | No **Claude-assisted fault-fix workflow** for a non-developer: entry point, the build-time-documented process Claude reads, and capability gating so a non-developer is never walked into a destructive shell/git/credential action. | Op Stds (new section) + a successor-facing runbook in `references/` (does not yet exist) | **build-time-discipline** | **P0** |
| **G4** | The **"remote-support / Solution Smith remains primary operator"** model is unreconciled with the audited **"Seth = reachable asset, not daily operator"** framing. Doctrine currently carries both. | Handover + Excellence Roadmap | handover-artifact | **P1** |
| **G5** | **No defined ship-and-leave / developer-departure threshold in the body** of V&R. The term exists *only* as a frontmatter tag (V&R L9); it is never defined in the v7.2 body. (Corrected from an earlier draft: there is **no** clean-operation-window threshold in current doctrine — review is *"Permanent, not time-bounded"*, FM L38 — which *strengthens* this gap.) | V&R (define a departure threshold incl. a successor-maintainability criterion) | handover-artifact | **P1** |
| **G6** | **Silent fail-open hazards a non-developer can never detect are punted, not guardrailed.** Guard hooks *"silently disappear"* *"with no error"* if the symlink dangles (`worktree-discipline.md` **L68-69**); the health-check is *"deliberately deferred to operator decision; it is not built here"* (**L89-92**). | `worktree-discipline.md` + Op Stds (failure-isolation/watchdog coverage) | **build-time-discipline** | **P2** |
| **G7** | **Version-reference drift degrades doctrine as a successor reference.** Frontmatter `version:` ≠ body title on three docs (HP 6/v6.3, V&R 7/v7.2, ER 2/v2.3); FM v9 body cites "Op Stds v11 §§" while its footer cites v14; and `~/its/CLAUDE.md` is pinned at "v13" while doctrine is at v14 (`claude-code-info-gap.md` **L136**). A non-developer reading these sees inconsistent versions. | all doctrine `*.md` frontmatter + `scripts/lint_frontmatter.py` coverage | handover-artifact | **P2** |

---

## 7. Build-shaping callouts (the operator's real decision point)

If the three-tier model becomes a designed-for requirement, it changes **how**
remaining work is built — not just what gets documented at the end.

- **`all-remaining-briefs` (the load-bearing change).** Add a mandated **"Successor
  remediation"** deliverable to every remaining workstream brief: for each fault
  class the workstream can surface, a plain-language, Smartsheet/alert-keyed entry —
  *symptom → non-developer check → Claude prompt or UI action → escalate-to-Seth
  condition* — authored **at build time**, distinct from §42 code docstrings.
  *Rationale:* Tier 2 is ABSENT and the only build-time doc discipline targets
  code-readers; document-at-handover demonstrably under-produces (it yields the
  assumed end artifact, not per-fault remediation).

- **`safety-portal`.** Design every Portal failure path to surface as a
  **non-developer-actionable signal** (a Smartsheet row / alert with a remediation
  pointer), never as a state requiring launchd logs, JSON state files, or a shell.
  Where a fix genuinely needs code/CLI, the Portal/alert must **explicitly route to
  Tier 3 (Seth)** rather than leave a non-developer stuck. *Rationale:* the Portal is
  the most successor-facing surface; if it inherits the §31/§32 developer-only
  diagnosis assumptions it will hard-block the successor.

- **`F08`.** Before building, **decide and document its successor-maintenance
  boundary**: which F08 faults a non-developer fixes via Claude (with a build-time
  remediation doc) vs. which escalate. Do not inherit the unstated "operator =
  developer" assumption pervading Op Stds §§37-41 (`gh api`, gitleaks, migration
  scripts, worktree cleanup). *Rationale:* shaping this at build time is far cheaper
  than retrofitting.

- **`F09`.** Build the **Claude-assisted-fix loop as a first-class, capability-gated
  path**: the entry point a non-developer uses, the build-time-documented process
  Claude reads, and gating that prevents a non-developer from being walked into a
  destructive shell/git/credential action; pair any irreversible operation with a
  Tier-3 escalation, not a self-service path. *Rationale:* Tier 2's entire viability
  rests on this loop, yet no doc describes it; F09 is the right place to establish a
  reusable pattern.

---

## 8. Successor identity — left for the operator

Per the brief, this audit does **not** resolve or invent the successor's identity.
The model, not the person, is what was audited. The placeholder stands:

> `<SUCCESSOR — operator to confirm name/role/email. NOT yet verified: the name
> "Daniel/Danielle" does not appear in the Evergreen contacts list; the F22 approver
> uses daniels@evergreenmirror.com. Operator must resolve who this is.>`

Doctrine's own term for this role is equally unresolved — "future trained Evergreen
maintainer" (`system-hr-handoff.md` L39), "added later when one exists" (L49) — which
is itself part of Gap **G1**.

## 9. What this audit did not do

- Did not execute code, exercise the live tenant, or run the test suite — findings are doc-grade.
- Did not edit any doctrine (propose-only).
- Did not audit the *execution* repo's code against this model — only blueprint doctrine + references. (A follow-on could check whether `~/its` code/runbooks close any gap, but doctrine is the contract, and per CLAUDE.md if code contradicts doctrine, doctrine wins / the inconsistency is flagged.)
