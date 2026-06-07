---
type: session_log
status: archived
workstream: safety_portal
tags: [deploy-session, mirror-deploy, f22-workspace-membership, box-version-on-conflict, box-mirror-planned, email-path-retain, phase7-admin, op-stds-v18, verify-before-writing]
---

# 2026-06-07 — Safety Portal deploy-session reconciliation (exec PRs #178–#186 + PR-H)

Blueprint-side reconciliation bringing doctrine current with the Safety Portal **deploy-session cluster**. Co-resolution: the operator reviews the doctrine portions. **Doctrine-authoring only — no execution code.** Verified live against exec `main` (`34e271d`, PR-G #186) + branch `feat/safety-portal-phase7-admin` (unmerged PR-H #185) before authoring.

## Method — verify-before-writing (13-agent pass)

The session opened by **grounding every ledger claim in exec code** via a 13-agent verification workflow (read-only over `~/its`), each returning file:line + verbatim-quote evidence, followed by a completeness critic. This is the "do not trust memory for current state" discipline — and it paid off: several ledger statements were **corrected** against the code (below). Prior reconciliation (blueprint PR #40 + the v17/LLM-free cascade) had already captured exec PRs #173–#177; this cycle captures the **gap = #178–#186 + this-cycle decisions**.

## What landed (verified) — exec PRs #178–#186

- **PR-A #179** — `portal_poll` is now a real launchd daemon (`org.solutionsmith.its.portal-poll`, `StartInterval` 60 s, `RunAtLoad=false`, send-free) + `install.sh` wiring + **watchdog Check-C** marker `safety_portal_poll.last_run` (5-min window). Closes §G25.8 item 4.
- **PR-B #180** — `wrangler.jsonc` → the **mirror/validation** D1 (`924f142b-…`, `its-safety-portal-db`, ENAM). Validation ≠ Evergreen cutover.
- **PR-C #181** — week-sheet filing auto-provisions a per-job folder + per-week sheet at the **surface of `WORKSPACE_SAFETY_PORTAL`** (find-or-create; the legacy `FIELD_REPORTS_FOLDER_BY_PROJECT` map dropped from the portal path).
- **PR-D #182** — `ITS_Active_Jobs` → D1 job sync (`portal_poll` push → bearer-gated `POST /api/internal/sync`, full-replace, never-wipe-on-empty). Resolved the v2 "Sync Now mechanism TBD" open question.
- **PR-E #183** — **F22 approval authority = Safety Portal workspace membership** (the `authorized_approvers` allowlist retired 2026-06-06). The principle was always doctrine; PR-E realizes it in code.
- **PR-F #184** — rendered PDFs attached inline on Submission / Rollup / WSR rows (supplementary, best-effort, Box stays SoR).
- **PR-G #186** — Compile-Now Box-409 → version-on-conflict on the packet path.

## Corrections the verification forced (ledger ≠ code)

These are the load-bearing reasons the verify-before-writing pass mattered:

1. **Box-mirror model is PLANNED, not built (PR-K).** The ledger described the `ITS_Safety_Portal` Box root (`388017263015`), the `safety_reports.box.safety_portal_root_folder_id` config key, per-job→per-week, category-subfolders-dropped, and version-on-conflict-everywhere as if known/decided. **None of it is in code** (zero hits for the key or the id at `34e271d`). As-built: per-submission PDFs file into the job's **existing email-path category subfolders** under a per-job project-clone root (`project_routing.get_folder_id`), category subfolders **retained**, **suffix-on-409**; only the compiled **packet** uses a per-week folder + version-on-conflict. The blueprint records the planned model clearly labeled PLANNED and defers its as-built reconciliation to when PR-K lands.
2. **F22 workspace-OWNER inclusion is NOT handled in code.** The ledger listed owner-inclusion as a recorded edge case; the resolver injects no owner and filters no access level — owner inclusion is an **unstated dependency on the Smartsheet `/shares` response**. Recorded as an open question, not a guarantee. (The **group-share** gap *is* real and documented: GROUP shares have no email → excluded → fail-closed.)
3. **Secret names in the v2 brief were stale.** As-built: `PORTAL_INTERNAL_API_TOKEN` (↔ Keychain `ITS_PORTAL_INTERNAL_TOKEN`) and `HMAC_PAYLOAD_SECRET` (↔ `ITS_PORTAL_HMAC_SECRET`), not the v2 `INTERNAL_BEARER_TOKEN` / `HMAC_SECRET`. `SESSION_SIGNING_SECRET` is Worker-only; `PORTAL_ADMIN_API_TOKEN` (↔ `ITS_PORTAL_ADMIN_TOKEN`) exists only on the PR-H branch.
4. **CodeQL dismiss-block hook is agent-scoped, not global.** It lives in the `codeql-fp-triager.md` frontmatter (`PreToolUse`, matcher Bash), **not** `settings.json` (which wires only `block-dangerous-git` globally) — so the operator's own session can still dismiss manually. And the "dismiss per-alert in the GitHub UI + inline comment; never blanket-suppress a secret-logging rule via per-file CodeQL config" rule was **not previously recorded anywhere** — it is newly codified (Op Stds §48), not as-built doctrine.
5. **Email-retain is finer-grained than "all dormant seed."** `project_routing` / `BOX_PROJECT_FOLDERS` / the category machinery are **actively live shared infra** (reused by the portal Box path today), not merely dormant email code; only `week_folder.py` + `intake.process_message` + the Graph stages are preserved-dormant. `intake_poll.py` is the only tombstone.
6. **PR-H Phase 7 admin is code-complete but INERT** — unmerged, absent from `main`; CLI verbs are `add-user`/`reset-password`/`disable-user`/`enable-user`/`list-users` (not the ledger's literal `provision/reset/disable/enable/list`).

## Roll-forward (same session): the whole batch merged → anchor advanced `34e271d` → `f3ad814`

The reconciliation above was authored against `34e271d` while PR-H/I/J/K were still in flight. The operator then completed the batch and confirmed all merged; a second verification pass (6 agents) grounded the newly-merged code, and the docs were rolled forward to exec main **`f3ad814`**. What changed from the snapshot above:

- **Box-mirror is LANDED, not planned (PR-K #189, `ecb06d9`)** — but **config-gated/live-inert**. The corrections in bullet 1 hold and matter: the root is an `ITS_Config` key **`safety_reports.box.portal_root_folder_id`** (the ledger's `388017263015` / `safety_portal_root_folder_id` are *not* in code), the shared `safety_naming.py` makes Box + Smartsheet names identical, category subfolders are dropped on the mirror path (legacy retained as the gate-OFF/email fallback), and version-on-conflict stays packet-only. Inert until the operator creates the root Box folder + sets the key.
- **PR-H Phase 7 admin is LANDED (`f3ad814`)** — byte-equal to the verified branch; merged last after its 2 CodeQL `py/clear-text-logging` FPs were operator-dismissed (a clean live exercise of the new §48 doctrine). Live-inert until the 3-part activation gate (tokens + migration 0006-before-redeploy + redeploy).
- **PR-I #187 styling + PR-J #188 custom domain — LANDED**, each operator-activated (one-time pass already run for styling; `wrangler deploy` gates the domain).
- **Handover Plan v8 → v9** — PR-H merging realized the deferred trigger; the full successor-operator portal-user provision/deprovision runbook is now in Step 8 (tag `handover-plan-v9`).
- **Three operator activation tracks** remain before production-ready (admin route / Box mirror / custom domain — all merged-but-inert). Pre-activation portal Box filings are pre-launch sandbox orphans (exec tech-debt; validation-tenant).

## Decisions ratified / recorded

- **Email-intake code is retained, not decommissioned** — load-bearing seed for the committed Email Triage workstream. Recorded in the safety-reports brief, memory-archive §G26, the new Op Stds §49, and a forward-reference in the Email Triage mission.
- **Validation deploy = the operator's mirror Cloudflare environment** (`evergreenmirror.com`); "live" = mirror functional + admin-controllable + edge-case-proven, NOT the Evergreen cutover. Production cutover facts (GoDaddy WordPress/Elementor apex untouched; attach only `safety.evergreenrenewables.com` via subdomain NS-delegation; Evergreen-owned fresh Cloudflare account) unchanged from §G23.2.
- **Op Stds v17 → v18 (co-resolution doctrine bump).** Five as-built patterns generalized into new §§45–49 (find-or-create-not-strand; workspace-membership-as-approval-authority; Box version-on-conflict; CodeQL-FP handling; preservation-for-future-workstream). Tag `operational-standards-v18`.
- **Handover v8 → v9 (co-resolution doctrine bump, realized at PR-H merge).** The operator pre-approved "forward-ref now, full v9 at merge"; PR-H merged, so v9 adds the successor-operator portal-user provision/deprovision runbook (Step 8). Tag `handover-plan-v9`.

## Docs reconciled this cycle (final, anchored `f3ad814`)

safety-portal mission v2→**v3** + brief v2→**v3**; safety-reports mission v5.4→**v5.5** + brief v6.4→**v6.5**; Operational Standards v17→**v18**; Handover Plan v8→**v9**; memory-archive **§G26** (incl. §G26.10/§G26.11 roll-forward); `claude-code-info-gap.md`; email-triage mission forward-reference; this log. Workstream/reference docs are frontmatter-versioned (not git-tagged); doctrine tags: `operational-standards-v18`, `handover-plan-v9`. **No longer pending** — the full deploy batch (PRs #178–#189) is merged; what remains is the operator's three live-activation tracks (admin route / Box mirror / custom domain) + the eventual Evergreen production cutover, all tracked in the brief §14 and §G26.11.
