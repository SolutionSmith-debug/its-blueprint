---
type: audit
status: canonical
last_verified: 2026-06-10
last_verified_against: ab920bc
workstream: safety_portal
audited_against: exec `its` @ `ab920bc` + its-blueprint doctrine @ main (Operational Standards v18, Foundation Mission v11, Handover Plan v9); trigger = blueprint reconciliation `429d377` (safety-portal mission→v4 + brief→v4, reconciled to exec as-built over the 62-commit window `f3ad814..ab920bc`)
tags: [doc-reconciliation, propose-only, safety-portal, v4-reconciliation, code-actuation-gate]
---

# Doc-reconciliation audit — 2026-06-10 (PROPOSE-ONLY; operator applies)

Emitted by the `doc-reconciliation-auditor` agent (propose-only; a `PreToolUse` hook structurally blocks any Edit/Write). **Nothing was applied** — every item below is a proposal for operator action.

## 0. Verdict (read this first)

**The v4 reconciliation is accurate — it introduced NO new drift and correctly held the doctrine line** (flags-only; `git show --stat 429d377 -- doctrine/` is empty). Nine fact-classes were cross-checked against the exec as-built at `ab920bc` and **all confirmed clean** (§3). The single substantive thing to fix is **pre-existing in the exec `~/its/CLAUDE.md`**: the incomplete v16→v18 sweep (the already-tracked M9), out of scope for this blueprint/flags-only pass.

**Baseline:** exec HEAD `ab920bc` / blueprint HEAD `429d377` / `doctrine_manifest.yaml manifest_version 1`.
**Mechanical tier:** `.venv/bin/python -m scripts.check_doctrine_drift` → 4 drift / 33 coverage (1 real, 2 informative false-positives, see §1).

## 1. Mechanical tier (script-backed)

- **[REAL drift, low-med] `~/its/CLAUDE.md:131`** — `(the Op Stds v16 / FM v11 reframe)`; canonical is **v18**. The §44 training-bounded reframe was *made in* v16 and carries forward unchanged to v18. **Proposed fix (exec):** `(the Op Stds v18 / FM v11 reframe)` (or `… v16 reframe, carried forward in v18`). Part of the M9 close-out (§2).
- **[FALSE POSITIVE — do NOT "fix"] `CLAUDE.md:65/81`** — `(reframed FM v9, audit F13)` are correct **historical** citations (CLAUDE.md declares FM **v11** governing throughout). The checker's `_near_historical` skip-list (`scripts/check_doctrine_drift.py:105`) lacks the `reframed` marker. *Optional checker hardening:* add `reframe[d]?` to that regex. No CLAUDE.md edit warranted.
- **[FALSE POSITIVE — attribution bug] `docs/tech_debt.md:1720`** — the deploy-prereqs `[OPEN]` entry is mis-flagged as "asserts completion": `check_stale_tech_debt`'s `header_re` only matches `## Title [STATUS YYYY-MM-DD]`, so bracket-first / bracketless headers (lines ~1739, 1765, 1870, 1906) aren't recognized and a later entry's closure phrase is mis-attributed. *Optional:* extend `header_re` to the bracket-first variant **or** normalize those headers. **Underneath:** the deploy-prereqs entry is arguably stale on its merits (the prerequisites are done on the **mirror** per mission/brief §11) — operator may re-status it `PARTIALLY_MITIGATED` (mirror done, Evergreen production cutover outstanding).

## 2. Semantic tier (opus judgment)

- **[HIGH] v4 docs introduced no new semantic drift** — every verify-before-fix correction point checked clean against code at `ab920bc` (§3).
- **[MED — pre-existing, exec] CLAUDE.md governing-version block contradicts itself and doctrine (the M9 residual).** `~/its/CLAUDE.md:22–23` asserts "Operational Standards is canonically at **v16** … v16 is the governing version," yet every actual citation in the same file reads "Op Stds **v18** §N" (lines 26, 70, 72, 88, 104, 106, 153, 180, 222, 226, 255), and blueprint `doctrine/operational-standards.md` frontmatter is `version: 18 status: canonical`. PR #191 (`d393ee6`) landed the v16→v18 sweep but left the governing block (22–23) + the line-131 attribution. **Proposed fix (exec):** update lines 22–23 + 131 to v18 (numbering is append-only since v11 → no §N renumbers / no citation-body changes). This is the M9 tech-debt close-out; **exec-side, not this blueprint pass.**
- **[LOW — scrutinized-clean, NOT drift] `<Workstream>_Pending_Review` quotes** in mission §7 / brief §3 are verbatim doctrine quotes, each immediately reconciled to the as-built `WSR_human_review` instance. Pattern-name-vs-instance relationship stated; classified clean.

## 3. Confirmed clean (verified — do NOT "fix")

1. **No `doctrine/*` edit** in `429d377`; the two flags (candidate Op Stds §50 code-actuation gate; form-maintenance-principle promotion) are correctly framed flags-only. Live doctrine frontmatter unchanged (Op Stds v18 / FM v11 / Handover v9).
2. **Publish status vocabulary** — mission §14 + brief §18 byte-match `0010_create_publish_requests.sql` CHECK: `queued, validated, tested, merged, live, archived, failed`.
3. **Actuator naming** — `_actuate` orchestrator (`publish_daemon.py:340`) vs `apply_publish` manifest helper (`publish_manifest.py:71`); `CI_TIMEOUT_S=900`, `sys.executable`, `_unstrand_if_needed`, `_wait_for_ci` all present as described.
4. **Token / gate map** — `requireInternalToken`→`PORTAL_INTERNAL_API_TOKEN` (shared by `portal_poll` + `publish_daemon` via Keychain `ITS_PORTAL_INTERNAL_TOKEN`); `requireAdminToken`→separate `PORTAL_ADMIN_API_TOKEN`; `adminGate=[requireSession, requireRole("admin")]`.
5. **Worker endpoint inventory** — brief §17's 4 groups match `worker/index.ts` exactly (public 6 / admin 9 / internal 6 / operator-CLI 6); `GET /api/admin/publish-request` present (line 1141).
6. **Migrations 0007–0010** number↔content all confirmed.
7. **Smartsheet ID map** — brief §3's 7-row table matches `shared/sheet_ids.py` at `ab920bc` exactly.
8. **Admin idle window** — 30 min (#258) consistent across mission §2 / §13 + brief; no 5-vs-30 residue.
9. **Manifest** — doctrine versions (v18/v11/v9) accurate vs live frontmatter; only the provenance pins (`meta.blueprint_head 0e85a1a` / `its_head f3ad814`) lag — *optional refresh* to `429d377` / `ab920bc`.

## 4. Operator action queue (all exec-side; none blocks the v4 reconciliation)

1. **CLAUDE.md v16→v18 close-out (M9)** — lines 22–23 + 131 → v18. One-line-class fix; already tracked in exec `docs/tech_debt.md` M9.
2. *(optional)* checker hardening — `reframe[d]?` in `_near_historical`; `header_re` bracket-first variant (clears the two mechanical false positives).
3. *(optional)* re-status the `tech_debt.md` deploy-prereqs entry → `PARTIALLY_MITIGATED`.
4. *(optional)* refresh `doctrine_manifest.yaml` provenance pins.
5. **VERIFY-REQUIRED (operator):** CLAUDE.md model strings (`claude-sonnet-4-6` / `claude-haiku-4-5-20251001` / `claude-opus-4-7`) agree with the manifest but currency is **not** asserted — verify against current Anthropic model docs.
