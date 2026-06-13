---
type: session_log
status: archived
workstream: safety_portal
tags: [reconciliation, v5, mission, site-photos, attachment-screening, pdf-download, form-request, two-mode-send, lifting-plan, doctrine-drafts, verify-before-fix]
---

# 2026-06-12 — Safety Portal v5 reconciliation (photo / download / Form-Request program)

## Purpose

Reconcile `workstreams/safety-portal/mission.md` v4 → v5 against the as-built six-PR program
**#271–#276** (photo upload, Crane & Rigging Critical Lift Plan form, request-driven PDF download,
Graph upload-session, Form Request browse), merged + CI-green + audit-verified on exec `~/its`. Fold the
three exec-side doctrine flags that the v4 window opened (`../its/docs/tech_debt.md` lines 25/2117/2166),
deliver two new doctrine drafts **propose-only**, and open a small exec-side CLAUDE.md/tech-debt/manifest
sync PR. Worktree `~/its-blueprint-v5` on branch `doctrine/safety-portal-v5` per
[`references/worktree-discipline.md`](../references/worktree-discipline.md).

## Pre-flight findings

A per-delta verification fan-out (one agent per delta + one exec-sync-surface agent) stood in for the
`brief-validator` agent, which is **unreachable from a home-rooted (`/Users/sethsmith`) CC session**: the
blueprint `.claude/agents` symlink targets `../../its/.claude/agents`, so the agent registry is not loaded
as session subagents. Every code-shape claim was checked against merged exec code with PR + SHA cited.
Corrections folded in **before** any mission text landed:

| Brief premise | Ground truth (cited) | Action |
|---|---|---|
| Header SHA list maps #275→`213d076`, #276→`13ef2bc` | Swapped: **#275 = `13ef2bc`** (Graph upload-session), **#276 = `213d076`** (Form Request). Per-delta PR numbers in the brief body were correct. | Cited PR #275 → `13ef2bc`, PR #276 → `213d076` throughout. |
| "intake post-back best-effort via `portal_client`" | The post-back is in **`portal_poll._service_pdf_requests`**, not `intake` — `intake.py` makes zero `portal_client` calls (capability/preservation). "Never blocks filing" holds, in the daemon. | §16 cites `portal_poll`, not intake. |
| Download keyed on the per-submission `pdf_requested` flag | That was the **#274** mechanism; **#276 migration 0012 `pdf_requests(submission_uuid, account)`** superseded it (requester-bound). The live mechanism is `pdf_requests`. | §16 describes the live `pdf_requests` table; notes Part-A flow became its first row. |
| Two-mode transport "checked before the write-ahead SENDING marker" | Split: the oversized → `held_oversized_packet` **refusal is pre-marker**; the **inline-vs-upload-session switch is post-marker** (`weekly_send.py`). | §7 Invariant 1 states the split precisely. |
| Lifting Plan = "four-party signature table" | A Section-12 *Authorizations* `signature_table`, `min_rows` 4, `allow_add`, **one** signature-input column (free-text `role`) — not four named parties. Checklist = **28 items** (brief/pre-build estimate said 26). | §14/§15 + v5 block say "Section-12 Authorizations table (`min_rows` 4)". |
| `required-content.json` rule = "strict entries require operator commission" | The file's verbatim rule is *"CHANGING A STRICT ENTRY IS A LEGAL-FLOOR (doctrine-adjacent) CHANGE: high-capability-class, Tier-3/Seth only — the Successor-Operator must NOT edit this file."* "operator commission" is not in the file. | Cited verbatim; ratification framed as Tier-3/Seth-only. |
| Email-delivery Form Request "analyzed and DECLINED" (artifact implied) | **No ADR/decision-record/tech_debt artifact exists.** The Worker is send-free by Invariant 1 (no email path at all) → in-portal delivery is the architectural default. Documented delivery decision = requester-bound D1 binding vs session/KV token. | Recorded as an **owner decision** in the mission decision record (§9 + §16), explicitly flagged as chat-only with no prior repo artifact. |
| `§34` manifest "pending, tracked exec-side (Brief-1 PR-1)" | `safety_portal/required-content.json` **already exists** with strict entries (jha, equipment-preinspection, toolbox-talk, incident-report, lifting-plan); no "manifest-pending" tech-debt item exists. | §14 upgraded ◐ → realized; not re-flagged as pending. |
| Pin to current `origin/main` (≥ `13ef2bc`) | `origin/main` = **`44370e1`**; `213d076..44370e1` is **not docs-only** — adds #279 (editor accepts `photo`), #280 (Form Request month/form-type filter), #281 (`photo-test-v1` publish, req 19). Verification read the tree at `44370e1`, so the pin is honest. | Pinned `44370e1`; scoped the five-delta program to #271–#276 and noted #279/#280/#281 where they extend a delta. |
| memory-archive: "append §G-next (program summary)" | **§G36 already archives the program** (#271–#276, per-PR subsections, deploy state). | Appended **§G37 for the reconciliation pass itself**, referencing §G36 (no re-archive — the §G35.1 lesson). |
| info-gap: "refresh §§" | **§8 was already refreshed today** (HEAD `2938c7a`: pin `213d076`, PRs #271–#276, "On the horizon (1) blueprint mission v4→v5"). | Targeted edits only — §3 flags + Last-refreshed + flag-fold/mission-v5-done status flips + pin. |

Also corrected against the repos: home chat-memory says "Op Stds v13" — the canonical version is **v18** (FM **v11**); used v18/v11 in all citations.

## Decisions made

- **Decision:** Pin `last_verified_against = 44370e1` (current `origin/main`), scope the formal five-delta
  reconciliation to #271–#276, and note #279/#280/#281 as thin follow-ons.
  **Alternative considered:** pin to `213d076` (the brief's #276 boundary).
  **Rationale:** the brief directs pinning to current `origin/main`, and the verification actually read
  the `44370e1` tree — pinning lower would understate what was verified. Scoping the program to #271–#276
  keeps the narrative honest while the Authority names the three extensions.

- **Decision:** Record the **declined email-delivery Form Request** as an owner decision in the mission
  decision record (§9 + §16), explicitly noting it has no prior repo artifact.
  **Alternative considered:** drop it (verifier found no artifact) — or assert it as a documented decision.
  **Rationale:** the brief is the owner (Seth) stating the decision; the mission decision record is the
  correct first home for a chat-only decision. But honesty requires flagging that in-portal delivery is the
  send-free Invariant-1 *default*, not the outcome of analyzing-and-rejecting a built email variant. Any
  revival is Seth-only, high-capability category 1 (External Send Gate).

- **Decision:** Doctrine stays **propose-only** — two drafts delivered below, no `doctrine/*` edit.
  **Alternative considered:** draft the §34 sub-pattern inline into Op Stds and submit for review.
  **Rationale:** doctrine is high-capability-class (the four fixed categories); a home-rooted session has no
  doctrine-write guard hook active anyway (the blueprint's guard is wired via the `session-close-maintainer`
  agent frontmatter, not session-wide, and is not loaded here) — so the discipline is **self-enforced**.
  Mixing a doctrine edit into a reconciliation PR also blurs the audit trail.

- **Decision:** Upgrade §14 legal-invariants-in-code ◐ → realized (the `required-content.json` manifest)
  rather than carry it as pending.
  **Rationale:** the file exists with strict entries enforced at both C3 layers; the lifting-plan strict
  entry is ratified here per the file's own Tier-3/Seth-only rule.

## Doc changes

Branch `doctrine/safety-portal-v5` (worktree `~/its-blueprint-v5`) — single commit; SHA recorded in the PR.

- **`workstreams/safety-portal/mission.md`** v4 → v5 — frontmatter (v5, supersedes @v4, pin `44370e1`,
  +8 tags); new dated v5 Authority reconciliation block; §7 Invariant 1 (two-mode transport, in place);
  §7 Invariant 2 Layer 6 (N/A → image-constrained, §34-screened) + HMAC note (photos ride `payload_json`);
  §9 Decisions Locked (System-of-record filing-principle amendment + Forms-catalog `lifting-plan` + four v5
  rows incl. the declined-email owner decision); §11 phase rows (5 v5 rows, deploy-pending noted); §12 two
  risk rows; §14 legal-invariants upgrade; **new §15** (site photos + §34 image-class screening); **new
  §16** (request-driven download + Form Request); new **v5 doctrine-flags** subsection; Authority rewrite
  (v6 trigger).
- **`references/memory-archive.md`** — appended **§G37** (the reconciliation pass; references §G36);
  frontmatter `last_verified`/`last_verified_against` → `2026-06-12` / `44370e1`.
- **`references/claude-code-info-gap.md`** — §3 candidate-doctrine-flags (added the two v5 drafts; noted v4
  program flags folded); `Last refreshed:` + frontmatter pin → `44370e1`; §8 status flips (flags folded /
  mission v5 done).
- **`session-logs/2026-06-12_safety-portal-v5-reconciliation.md`** — this log.
- **Exec-side (separate small PR in `~/its`)** — `CLAUDE.md` scaffold table (`photo_screen.py` row +
  intake/portal_poll/weekly_send refresh + Layer-6 note); `docs/tech_debt.md` (close the three mission-delta
  flag headers + refresh the Layer-6 SUPERSEDED entry); `docs/doctrine_manifest.yaml` `its_head` pin;
  `scripts/check_doctrine_drift.py` re-run clean.

## Verification

- `python scripts/lint_frontmatter.py` → **clean (84 files)**
- `python scripts/lint_crossrefs.py` → **clean (84 files)**
- Per-delta verification: all photo (Delta 1) claims confirmed; download/Form-Request (Deltas 2/3)
  confirmed except the post-back-location + `pdf_requests`-supersession + declined-email corrections above;
  send-transport (Delta 4) confirmed except the pre/post-SENDING-marker split; Lifting Plan (Delta 5)
  confirmed except the "four-party" + "operator commission" phrasings. Blueprint CI is lint-only; "four-part
  verify" applies to the exec-side sync PR.

## Out of scope

- **`brief.md`** — the v5 brief scopes the lift to `mission.md` only (unlike the v4 pass, which moved both).
  Not touched.
- **`doctrine/*`** — propose-only; no edit. Drafts below await Seth co-resolution.
- **PR-5 deploy** — migration 0012 + `npm run deploy` is a Developer-Operator step, not yet run even on the
  mirror; out of scope for a planning-layer pass.
- **Worktree removal** — a Developer-Operator action (hook-blocked inside CC; `worktree-discipline.md`).
- **The pre-existing exec M2 drift** — the "Safety Portal Phase 5 — deploy prerequisites" [OPEN] entry in
  `../its/docs/tech_debt.md` (body asserts completion) — unrelated to this program; left for its own pass.

## Sequencing context

- **Prerequisite:** PRs #271–#276 (+ #279/#280/#281) merged + four-part verified on exec `origin/main`
  `44370e1`; memory-archive §G36 + info-gap §8 already written by the 2026-06-12 exec session-close.
- **Unblocked:** future image-bearing intake workstreams can cite §15 + the propose-only §34 image-class
  sub-pattern; the request-driven download surface (§16) is a reference for any authenticated
  document-retrieval need.
- **Follow-ons:** (1) operator deploys PR-5 (migration 0012 + redeploy); (2) Seth co-resolves the four open
  doctrine flags (the two v5 drafts below + the two carried v4 flags); (3) exec-side sync PR merges +
  four-part verify; (4) worktree removal.

---

## Propose-only doctrine drafts (for Seth — no `doctrine/*` edit was made)

> These are **draft text** for Seth to apply to `doctrine/*` in a dedicated doctrine session. They are
> recorded here (and flagged in `mission.md §"Doctrine flags raised — v5"` + `info-gap §3`) per the
> propose-only discipline. Doctrine is one of the four fixed high-capability-class categories.

### Draft 1 — Operational Standards §34: canonical image-class screening sub-pattern

> **Proposed addition to Op Stds §34 (Attachment screening).** Add a named sub-pattern under §34 for a
> *constrained image-attachment class* (the first realized instance is the Safety Portal `photo` input,
> `safety_reports/photo_screen.py`, 2026-06-12):
>
> **§34.x — Image-class attachment screening (canonical sub-pattern).** When an intake surface accepts a
> constrained image class (JPEG/PNG only, header-level, bounded count + decoded size, no arbitrary file
> types), the §34 pipeline is realized as four ordered steps, all on the trusted (Mac) side **before** the
> bytes reach any renderer, model call, or system-of-record upload:
> 1. **Magic-byte + size gate** (Layer 1) — verify the declared type by signature (`FF D8 FF` / `89 50 4E
>    47`), reject on mismatch or over-budget.
> 2. **Decoder hardening** (Layer 2) — `Pillow` `verify()`; a **decompression-bomb pixel cap**; and a
>    **forced re-encode** that rebuilds the raster (destroying all embedded metadata: EXIF/ICC/XMP/COM).
>    Any provenance worth keeping (timestamp, GPS) is read to a sidecar and rendered as a **caption** before
>    the strip — *caption-then-strip*.
> 3. **Malware scan on RAW bytes** (Layer 3) — ClamAV on the **original** bytes (a re-encode would strip a
>    payload before the scanner saw it), **config-gated and default-OFF** (Layers 1–2 + the re-encode run
>    regardless; the operator enables the scanner as a pre-prod hardening step).
> 4. **Disposition** — `clean` files normally; `suspicious` files with a WARN review row; **`malicious`
>    fires a CRITICAL naming the offending account and a security-flagged Review-Queue row, and the
>    submission is refused before filing.** The renderer consumes **only** screened (re-encoded) bytes.
>
> The bounded-image-class scope keeps the §34 surface small; broadening to arbitrary file types (PDF/Office)
> re-opens the structural-inspection sub-layers and is a separate clearance.

### Draft 2 — Foundation Mission Invariant 2, Layer 6 wording touch (optional)

> **Proposed wording refresh to FM Invariant 2, Layer 6 (Attachment screening), safety-reports note.**
> Replace the "N/A for safety reports — reassigned to Email Triage" framing with an acknowledgement of the
> realized, constrained surface:
>
> *"For **safety reports**, Layer 6 is realized as a **constrained image-attachment class**: the Safety
> Portal accepts only header-level JPEG/PNG photos, bounds-gated at the send-free Worker and **§34-screened
> in code** on the Mac (`safety_reports/photo_screen.py`) before any render or Box upload — magic → Pillow
> verify/bomb-cap/forced re-encode → ClamAV-on-raw (config-gated). Arbitrary-file attachment screening
> (PDF/Office/executables over inbound mail) remains the load-bearing **Email Triage** surface."*
>
> Rationale: the prior "N/A — no attachments" wording is now contradicted by shipped code (PR #272); the
> refresh keeps doctrine honest without changing the invariant.

## Cross-references

- Mission: [`workstreams/safety-portal/mission.md`](../workstreams/safety-portal/mission.md) v5 (§7, §9, §11, §12, §14, §15, §16, Authority).
- Memory: [`references/memory-archive.md` §G36](../references/memory-archive.md) (program detail) + **§G37** (this pass).
- Info-gap: [`references/claude-code-info-gap.md` §3](../references/claude-code-info-gap.md) (doctrine flags).
- Prior pass: [2026-06-10 v4 reconciliation session log](2026-06-10_safety-portal-v4-reconciliation.md).
- Exec-repo program PRs: #271 `fadd53f`, #272 `5a979e2`, #273 `01e9d13`, #274 `814aec6`, #275 `13ef2bc`, #276 `213d076` (+ #279 `aaa161f`, #280 `ff00308`, #281 `44370e1`), `SolutionSmith-debug/its`.
- Exec session log: [2026-06-12 PR-5/PR-3 + tree cleanup](https://github.com/SolutionSmith-debug/its/blob/main/docs/session_logs/2026-06-12_pr5-form-request-pr3-graph-upload-tree-cleanup.md).
- Exec-side sync PR (CLAUDE.md scaffold table + tech-debt flag closes + manifest pin): linked at session close.
