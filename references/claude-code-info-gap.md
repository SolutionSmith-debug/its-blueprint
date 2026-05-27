# Claude Code Info Gap

**Purpose:** Context that lives only in chat memory / chat conversation and is NOT reachable from `~/its/` or `~/its-blueprint/` on a fresh Claude Code (CC) session. Drop this in project files so a chat-session can hand it to CC at spin-up, or so a fresh chat-session can re-orient quickly.

**Last refreshed:** 2026-05-27
**Maintained by:** chat-session at session close (treat as living doc)

---

## 1. Operator Communication Preferences

These are not in any repo. They govern how CC should respond to Seth in conversation/PR comments.

- **Concise and technically precise.** No preamble, no padding, no apology loops.
- **Delegate decisions when asked for a recommendation.** When Seth asks "which approach?" he wants a clear call with reasoning, not an options list. Options-list responses read as evasion.
- **Ask clarifying questions when genuinely ambiguous** — but don't manufacture ambiguity to stall.
- **Add context when necessary.** Explain larger concepts on first introduction; assume basic knowledge otherwise.
- **NEVER push back on operator scheduling, energy, or timing.** Don't suggest deferring. Don't comment on time of day or diminishing returns. Don't dress timing pushback as deference ("Path B is more conservative" when not asked). Operator says do X → do X. Only acceptable commentary is technical tradeoff about the work itself.
- **Push until satisfied, then document thoroughly.** Seth prefers a hard sprint followed by comprehensive docs over stopping at natural pauses.

---

## 2. Identity & Repo Map

| Item | Value |
|---|---|
| Customer 0 | Evergreen Renewables (family company, HQ Southern California, large construction projects in Oregon) |
| Operator | Seth (SolutionSmith-debug on GitHub) |
| Execution repo | `SolutionSmith-debug/its` (PUBLIC) |
| Blueprint repo | `SolutionSmith-debug/its-blueprint` (PRIVATE) |
| Local execution path | `~/its/` |
| Local blueprint path | `~/its-blueprint/` |
| Key contact | Ezra Jones — `ezraj@evergreenrenewables.com` |
| Mirror tenant | `seths@evergreenmirror.com` |

**ITS = Integrated Technical System** (renamed from TITS on 2026-05-10). White-glove custom development practice, NOT multi-tenant SaaS. Each customer is forked from the blueprint into a private repo. "Productization" means reusable patterns for Seth's efficiency, not a shared product.

**Two-repo doctrine:**
- **Blueprint wins on conflict.** Doctrine, missions, briefs canonical in `its-blueprint`. Code canonical in `its`.
- Chat-side: blueprint is NOT git-cloneable from claude.ai (no GitHub MCP). Chat reads blueprint via project knowledge where `.md` files are uploaded. Execution repo is public so chat can `web_fetch` raw URLs or git clone.
- CC-side: both repos are on local filesystem.

**Email typo trap:** `Evergreen_Contacts.pdf` row for Ezra has `evergreenrenwables.com` (missing the 'e' in 'renewables'). Use the correct spelling everywhere — docs, code, ITS_Config rows, mirror tenant aliases.

---

## 3. Core Doctrines (Non-Negotiable)

These are codified in `its-blueprint/doctrine/` but worth restating for fast load:

### System-wide invariants (Foundation Mission, Op Stds §3)
1. **External Send Gate** — No external transmission without explicit human approval. Two-process model per workstream + capability-gating AST test (`tests/test_capability_gating.py` in execution repo).
2. **Adversarial Input Handling** — External content is untrusted. 6-layer defense: sender allowlist, untrusted-content tagging, capability gating, structured outputs, anomaly logging, plus the External Send Gate as final stop.

Restate these in every brief touching external-bound code OR external content ingestion. Use `prompts/snippets/invariant-restatement.md`.

### Push-vs-Record Separation (Op Stds §3.1)
- Dedupe applies only to **push**, never to **records**.
- Resend = canonical push leg (subject to suppression).
- Smartsheet `ITS_Errors` + Sentry always write as forensic surfaces.
- Sentry alert rules + Smartsheet sheet-level notifications default-off. Enabling either converts cross-leg dedupe into an active design problem; `Correlation_ID` is wired and ready.

### Preservation-over-Refactor (Op Stds §14)
- When chat-session code lands in `~/its/` and trips ruff/mypy, prefer `[tool.ruff.lint.per-file-ignores]` in `pyproject.toml` over rewriting working code.
- Defer abstraction until **≥4 real reuse cases**.
- Exception: real dead code (not stylistic FP) may be deleted with the ignore.
- Canonical examples: PR #4 (1295a93) + PR #8 (parse_job_v3 F841 closure).

### SDK-vs-Live Integration Test Discipline (Op Stds §30)
- `SimpleNamespace` mocks at SDK boundary miss live API enforcement (body shape, required fields, value wrapping) AND SDK runtime state (in-process caching).
- 4 instances of this bug in 2 days (PRs #47/#48/#49/#51) is what forced this rule.
- Any new `shared/*` SDK wrapper with create/update/delete on typed columns/rows gets a parallel integration test.
- Run with `pytest -m integration` against throwaway sandbox resources. CI skips by default.

### Verify-before-fix
- Cascade updates, session-wraps, briefs, and PR-landed claims capture state at authorship.
- Before acting on any such claim, verify state hasn't changed.
- PR #34 ghost (closed-not-merged, claimed landed in memory) is the canonical failure case.
- **Cost of pausing = minutes; cost of not pausing = shipping stale work.**

### Brief-authoring discipline (2026-05-24, post-PR #86 drift catch)
- When generating CC briefs that name specific files, functions, or current-state claims ("X is hardcoded", "Y not built"), **READ THE CODE FIRST**.
- For chat: `git clone SolutionSmith-debug/its` (public) or `web_fetch` raw URLs.
- PR #86 drift: §A1 already delivered, §A4 named nonexistent `shared/alert.py`, §A5/§B3 wrong specifics. CC caught all of it.
- Briefs making code-shape claims get a code read first.

---

## 4. PR Workflow Discipline

### Four-part PR-landed verification (codified 2026-05-23, PR #74, `docs/operations/pr_merge_discipline.md`)

All four required before a PR is considered landed:

1. `state == MERGED`
2. `mergedAt` is non-null
3. `mergeCommit.oid` is present
4. **Main-branch CI on the merge commit = SUCCESS**

Run: `gh pr view <num> --json mergedAt,mergeCommit,state` immediately after `gh pr merge --squash --delete-branch`. Then check main CI run on the merge commit.

Session logs say **"four-part verify clean"** when confirmed. The earlier three-part verification missed Run 229+ post-merge reds from PR #68 (6 consecutive). Four-part is required every PR.

### Merge command
```bash
gh pr merge --squash --delete-branch
gh pr view <num> --json mergedAt,mergeCommit,state
# then verify CI on merge commit on main
```

### Branch protection (configured 2026-05-24, server-side)
- Strict status checks, contexts=`["test"]`, app_id=15368
- `required_linear_history=true` (squash-only)
- `allow_force_pushes=false`, `allow_deletions=false`
- `required_conversation_resolution=true`
- `enforce_admins=false` (emergency lever)
- `required_pull_request_reviews=null` (solo + CC, CI is the gate)
- Local complement: `block-dangerous-git.sh` hook

---

## 5. Known Traps & FP Patterns

### CodeQL false positives (Python + Actions, weekly, since 2026-05-24)
Dismiss-as-FP unless content shows actual secret/PII value being logged:
1. Logging Keychain **service-name constants** (name, not value).
2. OAuth URL with public `client_id` + single-use CSRF `state`.
3. Any `print()` in modules with `trusted_contacts` in path (filename heuristic).

### Secret-exposure baseline (gitleaks 8.30.1, 2026-05-24)
- 0 findings, 0 CI/env/Dependabot secrets, 0 env/credential files ever committed.
- Clean by architecture — all secrets in macOS Keychain (`shared/keychain.py` + `.gitignore`).
- Repo stays public. Re-run gitleaks periodically after new `shared/*` SDK wrappers.

### GitHub Actions version bumps
- Verify latest tag via `gh api repos/<owner>/<repo>/releases/latest`.
- Read release notes for breaking changes before bumping.
- Never blanket-upgrade.
- PR #81 reference: `actions/checkout @v4→@v6` (v6.0.2), `actions/setup-python @v5→@v6` (v6.2.0), cleared Node 20 deprecation.

---

## 6. Tooling & Infrastructure

### CI gates
- `mypy = 0` enforced as **blocking** step (PR #31).
- `pytest -m integration` skipped by default; run against throwaway sandbox resources.
- Branch protection requires `test` context to pass.

### Smartsheet
- **5-workspace audience-separated topology** (Op Stds §23):
  - Customer-facing: Forefront Portfolio + Human Review
  - Operator-only: Operations (master DBs), Archive (closed projects), System (config/errors/queues)
- Principle: split by audience, not data type.
- Customer 2+: System is singleton across customers; Operations + Archive shared-vs-per-customer TBD; Portfolio + Human Review always per-customer.
- MCP gotchas: `get_columns`, `browse_folder`, `create_sheet_in_folder_from_template` with `include=["data"]` are reliable. `update_rows`/`get_report` may hit "No approval received" gate on first call — retry resolves.
- Reports MCP is read-only; `create_report` needs REST fallback.
- `get_sheet_summary` applies default sort by primary column (breaks header-row-context sheets); true native order requires `ss_api.py` via local execution.
- Filter operators: EQUAL, NOT_EQUAL, LESS_THAN/GREATER_THAN variants only — no CONTAINS/LIKE.

### Smartsheet REST via curl
- Write multi-line JSON payloads to files, use `-d @/path/to/file`. Inline shell quoting produces misleading 401/400 errors.
- **A 401 with `errorCode:2000` on POST is more likely a malformed payload than auth failure** if the same token succeeds on GET. PAT scope is uneven — platform behavior, not user error.

### Box
- OAuth 2.0 User Auth via `boxsdk` (NOT JWT — JWT path not licensed).
- Auth as `seths@evergreenmirror.com`.
- `store_tokens` Keychain callback is **CRITICAL** — refresh tokens rotate every use.
- Keychain keys: `ITS_BOX_CLIENT_ID`, `ITS_BOX_SECRET`, `ITS_BOX_REFRESH_TOKEN`.
- Setup: `setup_box_oauth.py` (one-time). Smoke test: `smoke_test_box.py`.

### MCP-gap REST-fallback pattern
When Smartsheet/Box/Graph MCP lacks a primitive:
1. Short-lived sandbox token + inline curl in `bash_tool`
2. Verify-after via OAuth MCP
3. Never persist token to file or env
4. Operator rotates token post-session

Applies across all three external systems.

### CC skills installed (PR #79, mattpocock/skills)
14 skills in `.agents/skills/` + `.claude/skills/` symlinks, pinned via `skills-lock.json`:

`caveman, diagnose, grill-me, grill-with-docs, handoff, improve-codebase-architecture, prototype, setup-matt-pocock-skills, tdd, to-issues, to-prd, triage, write-a-skill, zoom-out`

- Auto-recommend: `diagnose` (SDK-vs-Live), `tdd` (§30).
- Gated: `improve-codebase-architecture` (§14 preservation-over-refactor).
- `git-guardrails` planned as follow-up PR.

---

## 7. Orchestration Model

- **Chat = strategy, sequencing, paste-ready prompts with structured context blocks.**
- **CC = implementation.**
- Seth directs CC for code; chat handles planning and drafts CC briefs.
- Session documentation at close: `.docx` files following `ITS_[Topic]_[Date].docx` convention, output to `/mnt/user-data/outputs/`. `/mnt/project/` is read-only.
- Sequencing: alert-routing / deduplication before workstream consumer integration. Filler tasks (parser tech_debts, regex refinement) scheduled between critical-path items.

---

## 8. Current State Snapshot (as of last memory refresh)

### Recently landed
- Triple-fire CRITICAL alert path complete (PRs #11/#21/#22/#23)
- `shared/review_queue.py` + `shared/quarantine.py` wired (PRs #24/#25)
- mypy=0 enforced (PR #31)
- Alert deduplication shipped (PRs #42/#43/#44)
- Picklist Sync shipped + hardened (PRs #45–51)
- Box OAuth wired (PR #39, commit `2ce6ece`)
- Polling daemon + heartbeat (PRs #59/#60)
- Branch protection on main (2026-05-24, server-side)
- CC skills installed (PR #79)
- Actions version bumps (PR #81)
- Secret-exposure audit clean (2026-05-24)

### Bradley 1 (BBCHS 1)
- Template project, six sheets migrated, demo seeding complete.
- Next: UI work (conditional formatting, forms, filter views — Seth runs UI-only work himself) before cloning template to the other five projects.

### Open queue
- `person_tag` regex refinement (138 hits, likely FPs)
- Three `box_migration` parser tech_debts deferred: V/S vendor-sub parser, ISO date prefix, import-time hygiene wrap

### On the horizon
- Safety Reports workstream build (Mission v5, Brief v6) — own dedicated session after shared modules stable.
- DFR backfill and Portfolio Rollups Reports continued expansion.
- **Managed Agents Phase 3 gate** (V&R v7.1 + FM v7.1 + Op Stds §29): No agents in Phase 0/1/1.5/1.6. Phase 3 gate evaluates 4 candidates against capability-equivalence for Invariants 1 & 2:
  - Closeout Package Assembly
  - Schedule Digest
  - Dreaming
  - ITS Chat backend re-eval

  Framing: **"Python = deterministic plumbing, Agents = judgment-gaps between them."** Re-verify capability set at gate firing. Candidate list is planning input, not roadmap promise.
- Dedicated ITS Box user deferred to Phase 1.5.

---

## 9. Memory Restoration Notes

If a fresh chat-session needs to reload operational detail, the canonical source is:

- **`its-blueprint/references/memory-archive.md`** — append-only, loaded on demand. Covers M365 IDs + EXO gotcha, full Smartsheet topology + IDs, wiring history, 23-PR window, Bradley 1 migration + demo seeding, schema decisions, Picklist Sync (PRs #45–51), SDK-vs-Live class-of-bug, polling daemon + heartbeat, 2026-05-22 cascade.
- **`its-blueprint/doctrine/`** — Foundation Mission, V&R, Op Stds, Handover Plan, Excellence Roadmap. Version in frontmatter, not filename. Git tags mark canonical versions (e.g., `foundation-mission-v8`).
- **`its-blueprint/workstreams/<slug>/{mission,brief}.md`** — 5 workstreams.
- **`its-blueprint/audits/`** — historical audits.

Linters: `scripts/lint_frontmatter.py` + `scripts/lint_crossrefs.py`, CI on every push.

Future operational detail extends `memory-archive.md` in-place via new `§G*` sections — no more `vN+1` doc proliferation.

---

## 10. Things This File Does NOT Cover

CC has these via filesystem and doesn't need them re-stated here:
- Full doctrine text (read from `its-blueprint/doctrine/`)
- Code (read from `~/its/`)
- Workstream missions and briefs (read from `its-blueprint/workstreams/`)
- Operational detail covered in `memory-archive.md`

This file is the **bridge** between chat-only context and what CC can reach on disk. If something belongs in a repo, move it there and remove it here.
