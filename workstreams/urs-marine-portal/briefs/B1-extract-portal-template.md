---
type: brief
version: 1
status: draft
last_verified: 2026-06-16
last_verified_against: SolutionSmith-debug/its@fb15881
workstream: urs_marine_portal
tags: [workstream-brief, cc-brief, urs-marine, portal-template, extraction, provenance, d1-system-of-record]
---

# CC Brief B1 — Extract `its-portal-template` (the platform substrate)

> **You (Claude Code) start with no context.** Everything you need is reachable either by
> DIRECTION (read these on-disk files) or INCLUSION (decided this engagement, in no repo — stated
> below). Pinned to `SolutionSmith-debug/its@fb15881`; **run `brief-validator` on this brief first**
> and re-confirm every path/line against current HEAD before writing. A failed claim halts the
> brief — do not work around it (PR #86 / 2026-06-08 stale-brief lessons).

## Cold-start context

**Where you are.** A session in `~/its` (Evergreen, Customer 0 — the extraction *source*). You will
create a new sibling repo `~/its-portal-template`. `~/its-blueprint` is checked out as a sibling.

**DIRECTION — read before acting.**
- `~/its/CLAUDE.md` — the source contract (architecture, invariants, discipline).
- `~/its-blueprint/doctrine/foundation-mission.md` §Invariant 1 + §Invariant 2 (FM v11).
- `~/its-blueprint/references/customer-fork-setup-checklist.md` — the §39 security baseline you apply.
- `~/its-blueprint/prompts/snippets/invariant-restatement.md` — paste into the new repo's `CLAUDE.md`.
- Discipline (preservation §14, propose-only on protected surfaces, squash-only, linear history,
  secrets-in-Keychain, **no Customer-0 secrets/sheet-IDs in any fork**) is already in `CLAUDE.md` +
  the `.claude/hooks`. Follow it; it is not restated here.

**INCLUSION — engagement decisions (in no repo).**
- **Extraction method ⟫OVERRIDE:** fresh repo + a `PROVENANCE.md` recording source `its@<HEAD>` and
  the include/exclude manifest — *not* a fork or `git filter-repo` — so no Evergreen safety content
  lingers in a customer-distributable template's history. (Alternative if git-provenance matters
  more than a clean tree: `git filter-repo --path safety_portal/`, then strip.)
- **The new repo's `CLAUDE.md` must override the Evergreen data posture:** state **D1 =
  structured-data system of record, Box = document SoR**. The source `CLAUDE.md` says
  "Smartsheet/Box/Outlook = systems of record" — that does **not** carry to the template.
- The copy/strip manifest and the single surgical migration edit (below) are engagement decisions —
  do not re-derive them.

**Invariant gist (operative here).** The Worker stays send-free (Inv 1, two-process); all field
input is untrusted (Inv 2). This extraction must weaken neither.

## Goal

A clean, domain-free portal platform repo (Worker + SPA + D1 + scaffolding) that URS and future
portal-centric customers fork from.

## PR-1 — Repo + §39 baseline (Developer-Operator for the `gh api` steps)

Create private `its-portal-template`; land an initial commit + minimal CI so required-status
contexts resolve; then apply the §39 checklist verbatim (branch protection strict + linear +
no-force + no-delete + conversation-resolution; secret-scanning + push-protection; CodeQL
default-setup; Dependabot alerts, not auto-fixes). Verify with the checklist's read-back commands.

## PR-2 — Copy the platform-universal substrate (paths under `~/its/safety_portal/`)

**Copy:** `src/` (App; components AppHeader/FormEditor/PhotoField/PublishMonitor/SignaturePad/
AdminTabs; `forms/` registry/types/editorModel/editorValidation/FormRenderer; `lib/` api/auth/
draftCache/`exif`/useIdleLogout; `pages/`; `styles/` `tokens.css` + global.css); `worker/`
(auth/index/prune/publishValidation/types); `forms/meta-schema.json`; `catalog.schema.json`; build
config (package.json, tsconfig*, vite/vitest configs, index.html, .dev.vars.example).

**Migrations — copy verbatim:** 0001 (users), 0005 (transport/HMAC), 0006 (disabled), 0007 (role
mechanism + `audit_log`), 0008 (attribution), 0009 (session_epoch), 0010 (publish queue). **One
surgical edit to 0003:** keep the `submissions` CREATE (it is the base table 0005/0008 ALTER), and
**drop the `jobs` CREATE** (that is the Smartsheet-mirror shape; URS's `jobs` is a fork migration).
**Drop entirely:** 0002, 0004 (seeds), 0011, 0012 (PDF-download cache — Safety-Portal-specific).

**Strip (Evergreen content/IP):** all `forms/*.json` except `meta-schema.json` (+ keep one generic
fixture for the test suite); all `reference_forms/*.pdf`; `catalog.json` + `required-content.json`
content; `public/evergreen-logo.svg` + the ITS-branded `public/*` assets (brand injected at B4).

**Root scaffolding — copy:** `.claude/hooks/*`, `.claude/agents/*` **minus `smartsheet-rest-fallback`**,
`.claude/settings.json`, `.agents/skills/` + `skills-lock.json` + the skills symlinks, `.gitignore`,
`.gitleaks.toml`. **Adapt:** `.github/workflows/ci.yml` from Python ruff+pytest → TS `tsc` +
`vitest` (the template is portal-primary). The Python `shared/`, `pyproject.toml`, and daemons do
**not** carry — the adapter host is brief B3.

## PR-3 — `CLAUDE.md` + `PROVENANCE.md` + doctrine manifest

Write the template `CLAUDE.md`: the SoR override above, the platform scope, both invariants by
reference (cite `../its-blueprint/doctrine/foundation-mission.md` + paste the invariant snippet),
the discipline + subagent roster. Add `PROVENANCE.md` (source SHA, included/excluded manifest). Add
the **doctrine-citation manifest** — the pointer block to
`../its-blueprint/doctrine/{foundation-mission,operational-standards}.md`.

## Definition of done

- CI green (`tsc` + `vitest`) on a clean checkout.
- Boots under `wrangler dev` + local D1 with the kept migrations applied; login + a generic-form
  submit + the publish-queue path work against seeded local D1.
- **Grep gate: zero `smartsheet` / `evergreen` / safety-form-code strings** in `src` / `worker` /
  `migrations` (catches an incomplete strip).
- §39 baseline verified (the checklist's read-back commands).
- Reviewed by `portal-worker-security-reviewer` (auth/HMAC/capability posture intact post-copy) +
  `ops-stds-enforcer` (Send Gate, preservation, no doctrine drift).
- Squash; linear; propose-only on protected surfaces.
