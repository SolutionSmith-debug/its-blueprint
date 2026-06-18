---
type: session_log
status: archived
workstream: urs_marine_portal
tags: [urs-marine, customer-2, portal-template, extraction, fork, capability-model, adapter-seam, integrity-bar, doctrine-cascade, propose-only, excellence-roadmap-v5]
---

# 2026-06-16 — URS Marine portal-template extraction + Customer-2 fork (B1–B5)

## Purpose

Execute the URS Marine (Customer 2) workstream package end-to-end: land the package into the
blueprint, extract the domain-free platform substrate `its-portal-template`, generalize the role
model + name the adapter seam in the template, fork `its-urs-marine` with the URS data model +
integrity bar + demo, and stage the doctrine cascade (B5, propose-only).

Pinned to `SolutionSmith-debug/its@fb15881` (current HEAD at session start — zero drift verified).

## What landed (verified)

- **Phase A** — workstream package (`mission.md`, `brief.md`, CC briefs B1–B5) merged into
  `its-blueprint` (PR #44, squash). Registered `urs_marine_portal` in `lint_frontmatter.py`;
  linters clean (91 files).
- **B1** — `SolutionSmith-debug/its-portal-template` (private) extracted from `safety_portal/`
  (flattened to root). Domain-free: generic form/catalog/required-content, brand placeholders,
  Evergreen content + seeds + reference PDFs stripped, live D1 `database_id` → `REPLACE_AT_FORK`.
  `CLAUDE.md` states the **D1-as-structured-data-SoR override**. tsc clean; vitest 195 worker + 64
  SPA; vite build green; grep gate 0; gitleaks 0. CI (TS) green on the runner.
- **B2** — PR #1 (squash): DB-driven `roles`/`capabilities`/`role_capabilities` + SQLite
  users-table rebuild (drop 2-value CHECK, add FK) + fail-safe `resolveCapabilities` (unknown role
  → empty set) + capability-gated worker. 263 tests; unknown-role→empty-caps regression test.
- **B3** — PR #2 (squash): the named **PM Adapter Protocol** doc + `adapter_host/` Python package
  (constant-time `verify_hmac`, no-op adapter, host-agnostic `run_once`, launchd template) + a CI
  `adapter` job. Bad-HMAC → `mark_rejected`, never filed. Worker stays send-free.
- **B4** — PR #1 (squash) into `SolutionSmith-debug/its-urs-marine` (private), forked from the
  template (platform lineage B1→B3 preserved). 9-table URS D1 model (`clients`/`jobs`(ALTERed)/
  `personnel`/`equipment`/`time_entries`/`inspections`/`equipment_logs`/`equipment_location`/
  `task_assignments`) with the **integrity bar** (migrations 0014/0015): server-authoritative
  `created_at`/`edited_at` hard-coded `unixepoch()` in the INSERT (never bindable from body — a
  forged timestamp is impossible, proved by `test/urs-integrity.test.ts`), separate event-time
  claim columns, dual attribution, append-only `amends_uuid` chain + per-edit `audit_log`,
  version-pinned `inspections`. `field_guy` role (0016, photos-only). Marine forms (skid-steer/
  telehandler). Demo seed (4 tier logins, seawall/dock/pile-driving jobs) + `docs/DEMO.md`. No-op
  adapter for the demo. **204 worker + 66 SPA + 13 adapter tests green**, grep gate 0.
  **Follow-on (FORK.md):** `parseRole` still admits only submitter/admin → the admin API can't yet
  provision supervisor/field_guy (SQL-seeded for the demo); the capability model + fail-safe are
  unaffected (unknown role → empty caps). A scoped B2-completion follow-on (needs `roles`-table
  validation across the provisioning routes); deferred deliberately rather than risk a late change to
  security-sensitive auth code. `inspections`/`equipment_logs` write endpoints + Tier-2 dashboard UIs
  are follow-ons (integrity bar verified at schema level there).

## Deviations / non-obvious decisions (the "why")

1. **B1 migration reconciliation.** B1's headline said drop `jobs`(0003) + pdf-cache(`0011/0012`)
   as "Smartsheet-mirror / Safety-Portal-specific." Kept them as **domain-neutral DDL** — they
   carry no Smartsheet/Evergreen strings (the semantics lived in comments, genericized), and
   dropping them would orphan inherited `worker/prune.ts` + `index.ts` and force unscoped surgery on
   the 98 KB `index.ts`. The genuine domain strip (forms/catalog/required-content/brand/reference
   PDFs/seeds) was fully applied. Recorded in the template `PROVENANCE.md`. B4 ALTERs `jobs` for URS.
2. **§39 baseline is plan-gated.** The `SolutionSmith-debug` account is free (`plan: null`), so
   server-side **branch protection + secret scanning + CodeQL are unavailable for private repos** —
   `its-blueprint` itself returns the identical 403; only `its` carries protection (set in an
   earlier Pro/trial window). Applied what's available: Dependabot alerts ON, gitleaks CI job + the
   `.gitleaks.toml` + Keychain-secrets discipline as the secret-scanning substitute. Net posture =
   `its-blueprint`. Documented in the template `PROVENANCE.md`. **Not** made public (privacy holds).
3. **CI gitleaks-action → binary.** `gitleaks-action@v2` now requires `GITHUB_TOKEN` for
   `pull_request` scans (a latent B1 defect that B2's PR surfaced); replaced with a direct binary
   scan (no token coupling).

## B5 — doctrine cascade — LANDED (excellence-roadmap v5; PR #46, squash `ad8f563`, tag `excellence-roadmap-v5`)

> **LANDED 2026-06-17** in a guarded blueprint session (the `block-doctrine-write` guard fired and was
> operator-approved). The amendment proposed below was applied to `doctrine/excellence-roadmap.md` as
> **v5**: Track 3.4 added (verbatim from the proposal + `(NEW v5)` marker) + Track 3.3 refined;
> frontmatter `version 5` / `last_verified 2026-06-17` / `last_verified_against fb15881` / `supersedes @v4`;
> Authority v5 paragraph + `v5 trigger (met)` + advanced `v6 trigger criteria` (v4 history preserved).
> Companion edits in the same PR: `references/customer-fork-setup-checklist.md` (source-agnostic
> fork-source note) + `references/project-organization.md` (canonical-doc-set pointer v4→v5). **Checked
> consistent / no edit needed** (all fork-source-agnostic): Op Stds §39, `doctrine/foundation-mission.md`
> (per-customer-repo isolation invariant only), `references/permissions.md` §3.2 (already corrected the
> "primary operator" framing in Permissions Ask v6 — the stale excellence-roadmap line-75 pointer was
> corrected in-doc).
>
> **Date note:** the proposal specified `last_verified: 2026-06-16`; landed `2026-06-17` (the actual
> landing date) applied consistently across frontmatter / title / Authority.
>
> **Verify — all green:** `lint_frontmatter` + `lint_crossrefs` clean (92 files); four-lens adversarial
> diff review all PASS_WITH_NITS (no blockers); `doc-reconciliation-auditor` — `check_doctrine_drift.py`
> EXIT=0 with **zero NEW exec↔blueprint drift** (the lone M2 drift is pre-existing/exec-resident), 0 semantic drift.
>
> **Deferred per the documented "don't churn" convention** (memory-archive:1526; `handover-plan.md` itself
> still carries a stale "Op Stds v16"): the present-tense **"Excellence Roadmap v4"** cites in the
> **FM / V&R / Op Stds / Handover** Authority blocks were NOT churned — they refresh at each doc's *own*
> next bump. Only the canonical-doc-set *pointer* (`project-organization.md`) was refreshed for coherence.
>
> **Post-merge exec follow-on — DONE:** `../its/docs/doctrine_manifest.yaml` `blueprint_head` → `ad8f563`
> + the two "Excellence v4"→"v5" `meta` provenance comments — landed via exec **PR #293** (squash `2f70d91`),
> CI green (`test`/`portal`/`secrets`/CodeQL). Excellence-roadmap is tracked only in those narrative comments
> (no mechanical `doctrine_versions` entry), so `check_doctrine_drift` was unchanged across the refresh.
>
> **Mission status (open, recommend):** `workstreams/urs-marine-portal/mission.md` is still `status: draft`;
> its frontmatter conditions draft-exit on B5 landing, now satisfied → recommend the operator flip it (draft→canonical).

This session was home-rooted (`/Users/sethsmith`) — no blueprint hook fires and the
`block-doctrine-write` guard is self-enforced — so the `doctrine/excellence-roadmap.md` edit is
staged here, NOT applied. A guarded blueprint session (or the Developer-Operator) lands it with the
symmetric Authority/companion update + the four-lens diff review (`lint_frontmatter.py` does not
catch asymmetry — see [[feedback_doctrine_bump_symmetric_authority]]).

**Amendment — `doctrine/excellence-roadmap.md` v4 → v5.** Record the **platform fork-source**: for
portal-centric customers, the fork-source is **blueprint + `its-portal-template`** (the domain-free
platform substrate), NOT a strip of Customer 0's full `its` execution repo.

- **Track 3 — add item 3.4 (Platform fork-source / portal-template):**

  > 3.4 — Platform fork-source (portal-template). Portal-centric customers fork from **blueprint +
  > `its-portal-template`** — the domain-free platform substrate (single Worker + React SPA + D1 +
  > the declarative form/checklist engine + the DB-driven N-role/capability model + the named
  > PM-adapter seam + the HMAC/pull transport contract) — NOT from a strip of Customer 0's full
  > `its` execution repo. `its-portal-template` was extracted from `its@fb15881` (PROVENANCE-tracked,
  > domain-free, grep-gated). Per-customer execution repos (`its-<customer>`) fork from it; the
  > blueprint stays one artifact (no per-customer blueprint forks — blueprint `CLAUDE.md`). This
  > amends any prior "fork the execution repo" framing for portal-centric customers. Customer 2
  > (URS Marine, `its-urs-marine`) is the first worked example. Non-portal customers continue per 3.3.

- **Refine 3.3** (Blueprint Fork Runbook): note the runbook now distinguishes the **portal-template
  fork path** (portal-centric customers → 3.4) from a full-exec fork; still Developer-Operator-driven.
- **Frontmatter bump:** `version: 5`, `last_verified: 2026-06-16`,
  `last_verified_against: fb15881`, `supersedes: doctrine/excellence-roadmap.md@v4`.
- **Authority block:** add the v5 entry — "v5 adds Track 3.4 (platform fork-source: portal-template).
  Trigger met: substantive Track-3 addition (a new platform fork-source mechanism for portal-centric
  customers). Canonical git tag `excellence-roadmap-v5`." (The v5 trigger criteria at the bottom of
  v4 — "substantive track restructuring or addition" — is satisfied.)
- **Companion cross-refs to check symmetrically in the SAME PR** (four-lens diff): `Op Stds §39`
  (new-per-customer-fork security setup) + `references/customer-fork-setup-checklist.md` (note the
  portal-template fork path) + `references/permissions.md` §3.2 (already flagged in excellence-roadmap
  v4 line 75) + `doctrine/foundation-mission.md` / `operational-standards.md` if either cross-refs
  the customer fork model. Update the doctrine manifest (`../its/docs/doctrine_manifest.yaml`) if the
  excellence-roadmap version is tracked there ([[project_doctrine_reconciliation_tooling]]).

## Open items

- ~~Land B5 from a guarded blueprint session (the amendment above).~~ **DONE 2026-06-17** — blueprint PR #46 (squash `ad8f563`), tag `excellence-roadmap-v5`; exec manifest sync PR #293 (squash `2f70d91`). Only open item: `workstreams/urs-marine-portal/mission.md` draft→canonical flip (B5-landing satisfies its draft-exit condition; operator decision — see the B5 section above).
- B6 (Monday adapter — implement B3's `Adapter` for Monday.com) + B7 (net-new marine forms) are
  post-B4 follow-ons.
- URS discovery items (mission §12) gate the proposal, not the build.
