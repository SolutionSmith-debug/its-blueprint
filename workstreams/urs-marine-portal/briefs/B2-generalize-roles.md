---
type: brief
version: 1
status: draft
last_verified: 2026-06-16
last_verified_against: SolutionSmith-debug/its@fb15881
workstream: urs_marine_portal
tags: [workstream-brief, cc-brief, urs-marine, rbac, capabilities, fail-safe, sqlite-rebuild]
---

# CC Brief B2 — Generalize the 2→N role/capability model (in `its-portal-template`)

> **You start with no context.** DIRECTION + INCLUSION below. Pinned to `its@fb15881`; **run
> `brief-validator` first** — the role surface is the source of truth, re-read the cited lines
> against current HEAD before editing. A failed claim halts the brief.

## Cold-start context

**Where you are.** A session in `~/its-portal-template` (created by B1). `~/its-blueprint` is a
sibling.

**DIRECTION.**
- `~/its-portal-template/CLAUDE.md` — now carries the platform contract, the D1-as-SoR posture, and
  both invariants.
- The role surface is ground truth — re-read `worker/types.ts`, `worker/auth.ts`,
  `worker/index.ts`, `migrations/0007_add_user_role_and_audit_log.sql` at the lines below.

**INCLUSION — engagement decisions.**
- **Model ⟫OVERRIDE (decision #2 = tables):** DB-driven `roles`, `capabilities` (the stable
  vocabulary), `role_capabilities` (junction), admin-editable. (Alternative: a config-keyed
  capability map — simpler ship, not admin-editable.)
- **Preserve the fail-safe — this is the security crux.** The generalized resolver must, on an
  unknown/missing role, yield **no capabilities, never a privileged one.** Carry migration 0007's
  "belt to the suspenders" reasoning verbatim into the new code's comments.
- The starter capability set + the **Tier-1 field-guy-vs-field-manager split is provisional** (a
  discovery item) — seed it, flag it.

## Verified current-state (`@fb15881` — re-confirm)

- Hardcoded union `export type Role = "submitter" | "admin";` (`types.ts:39`); `role: Role` on
  `Vars`, set from D1 not the cookie (`types.ts:67`).
- `coerceRole(raw) => raw === "admin" ? "admin" : "submitter"` — the fail-safe (`auth.ts:83–84`).
- Per-request D1 role read in `requireSession` (`index.ts:228/279`; the fail-safe comment at `:259`).
- Gates `requireRole(role)` / `role === "admin"` at `index.ts:291/316/503` (the submit-as gate is
  `:503`) + the admin idle timeout at `:220`.
- `ALTER TABLE users ADD COLUMN role TEXT NOT NULL DEFAULT 'submitter' CHECK (role IN
  ('submitter','admin'));` + the `audit_log` table (`0007:13–14`).

## PR-1 — Schema

New migration: CREATE `roles`(key UNIQUE, label, is_system, created_at), `capabilities`(key PK,
label, description), `role_capabilities`(role_key, capability_key, PK(both), FKs). **Rebuild
`users`** — SQLite cannot `ALTER … DROP CHECK` or `ADD FOREIGN KEY`, so a copy-preserving table
rebuild is required: build the new `users` without the literal 2-value CHECK, add `FOREIGN
KEY(role) REFERENCES roles(key)`, copy rows, drop, rename. Preserve 0007's `audit_log` + every
comment; note that the value-list CHECK is superseded by `roles`.

Seed the three tiers + a **starter capability set**: `cap.photo.capture`, `cap.time.log`,
`cap.inspection.fill`, `cap.machine.log`, `cap.dashboard.{personnel,equipment,jobtracker}`,
`cap.admin.{accounts,formbuilder,adapter,settings}`, `cap.submit_as` — with the **Tier-1 split as
two capability subsets** (field-guy = photos only; field-manager = + time/inspection/machine;
provisional pending discovery).

**ORDER DEPENDENCY:** apply this migration to live D1 *before* the new Worker deploys (else
`requireSession` 401s every session — the 0006/0007/0009 rule); the rebuild preserves existing rows
for the fork.

## PR-2 — Worker generalization (preserve the fail-safe)

- `types.ts`: replace `Role = "submitter" | "admin"` with a role-key `string` + `type Capability =
  string` + a resolved `capabilities: Set<Capability>` on `Vars`.
- `auth.ts`: replace `coerceRole` with `resolveCapabilities(roleKey, db): Promise<Set<string>>` that
  **fails safe — unknown/missing role yields the empty set, never a privileged capability** (carry
  0007's reasoning into the comment).
- `index.ts`: `requireSession` additionally resolves + attaches the capability set in the *same*
  per-request D1 read (same fail-closed, change-effective-next-request posture); `requireRole(role)`
  → `requireCapability(cap)`; the `role === "admin"` checks (`:291/:503`) → capability checks
  (submit-as gate → `cap.submit_as`); drive the admin idle timeout (`:220`) off `cap.admin.*`
  presence, not the literal string. `audit_log` gains a `capability_change` / `role_capability_change`
  action once roles become admin-editable.

## PR-3 — Tests + review

Extend the inherited worker tests (`test/admin.test.ts`, `test/submit-as.test.ts`,
`test/session-epoch.test.ts`): a Tier-1-only role is 403'd on admin routes; **unknown role → empty
caps (the fail-safe regression test — mirrors 0007's intent; do not skip)**; submit-as requires
`cap.submit_as`; demotion drops capability on the next request (mirrors the existing demotion test
near `index.ts:323`). Reviewed by `portal-worker-security-reviewer` (no privilege-escalation path;
per-request resolution; submit-as still gated) + `ops-stds-enforcer`.

## Definition of done

- The 2-value union is gone; capabilities are data; the fail-safe is preserved + regression-tested.
- Tier-1 field-guy/field-manager is expressible as a capability subset (seed provisional).
- ORDER DEPENDENCY honored; the SQLite rebuild preserves rows.
- **§43 successor-remediation note** (symptom: a user has the wrong capabilities; low-class repair:
  edit the `role_capabilities` seed / re-run the migration; escalate-to-Seth boundary: any edit to
  auth/capability *code* is high-class).
- Squash; linear; propose-only.
