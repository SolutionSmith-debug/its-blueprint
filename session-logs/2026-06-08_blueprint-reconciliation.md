---
type: session_log
status: archived
workstream: null
tags: [reconciliation, smartsheet-structure, doctrine-citation-sweep, verify-first, brief-correction]
---

# Session Log — 2026-06-08 · Blueprint reconciliation pass

A Developer-Operator (Seth) blueprint-native session: author the canonical Safety Portal
Smartsheet-structure reference and sweep stale doctrine-version citations. Driven by a chat
brief whose current-state premises turned out to be **substantially stale** — so the headline
of this session is the verify-first correction, captured here and in memory-archive [§G28](../references/memory-archive.md).

## What landed (one PR; no doctrine edit; no tag)

1. **New `references/smartsheet-structure.md` (v1, canonical)** — the live-verified `ITS –– Safety
   Portal` workspace structure, **ID-free** (names + `shared/sheet_ids.py` constants only, per repo
   `CLAUDE.md`'s "no Customer-0 sheet IDs in the blueprint" rule). Verified via the Smartsheet MCP
   against exec `21bd909`.
2. **Doctrine-citation currency sweep** — 27 present-tense `Op Stds → v18` / `Handover → v9`
   citations across 10 blueprint docs, provenance preserved.
3. **memory-archive `§G28`** (append-only) — the corrected reconciliation record.

## The brief was stale — what verify-first caught

Grounded with `brief-validator` + `doc-reconciliation-auditor` + a live Smartsheet MCP browse.

| Brief premise | Ground truth | Action |
|---|---|---|
| "All demo Smartsheet architecture is abandoned; only `194283417429892` matters" | `WORKSPACE_DEMO = 4129485730670468` is **live in exec `sheet_ids.py:22` ("customer-facing")** with the Bradley/Brimfield/Huntley/Rockford project folders under it; Op Stds §24 documents it. | **Re-scoped** (operator) to a portal-only structure doc. Demo content NOT touched — abandoning it blueprint-only would manufacture blueprint↔exec drift. It's a cross-repo (exec + doctrine §24) decision. |
| Sweep "old wrong workspace ID `4021545954764676`" → `194283417429892` | `4021545954764676` exists **nowhere** — not in either repo, not in the live workspace list. `194283417429892` was already in the blueprint (6 files). | Phantom; nothing swept. |
| Abandoned: Template Master `3333320395253636` + Demo Seed `685696395569028` | Both are **live OWNER Smartsheet workspaces**, but in **no code**. | Not abandoned; noted. |
| "Permissions v5" | It's **v6** (`references/permissions.md`). | Noted. |
| `ITS_Active_Jobs` spec/unbuilt; WSR/WPR; safety-portal "to build" | All already correct (built 2026-06-03; WSR reconciled in §G27 + handoff v8; safety-portal already v3.1 as-built). | No-ops. |

## Decisions / non-obvious "why"

**D1 — Re-scope to a portal-only structure doc (operator-approved).** The doc documents the
`ITS –– Safety Portal` workspace only; the other workspaces (System, Human Review, demo/template
portfolios) stay covered by `smartsheet-handoff.md` and are explicitly **not** retired here.

**D2 — ID-free (operator-approved).** Per repo `CLAUDE.md` ("specific Smartsheet sheet IDs … belong
in the `its` repo"), the new reference names objects by `sheet_ids.py` constant + live name and points
to `~/its/shared/sheet_ids.py` for the numbers. (The existing `system-hr-handoff.md` carries raw IDs;
that's a legacy exception we did not extend.)

**D3 — Live structure resolved a code/brief discrepancy in the brief's favor.** Live browse shows a
**separate `00_Form Catalog` folder** holding `ITS_Forms_Catalog` (not co-located with `ITS_Active_Jobs`
+ `WSR_human_review` in `00_Safety Portal`). The exec `sheet_ids.py` `FOLDER_SAFETY_PORTAL` comment
("holds all three") is **stale** — flagged for an exec comment refresh.

**D4 — Citation sweep preserved provenance.** Swept only **present-tense** currency cites. Left
untouched: "What Changed"/changelog blocks, "new in v8"/"revised in v8"/"introduced in vN" origin-pins,
the `daemon-health` build-rationale §-cites (only its `Authority:` line updated), and the `:128`
"acknowledged in Op Stds v17" origin-pin. **`email-triage/{mission,brief}.md` left whole** — it's a
coherent, self-documented v8/v13 snapshot (its own 2026-05-28 sweep note explains the baseline);
half-updating it would break that coherence. Recommend a dedicated email-triage currency touch.

**D5 — FM/V&R/Excellence: "don't churn," with one coherence exception.** The brief said FM/V&R/Excellence
are already current — don't churn. Honored, **except** `project-organization.md`'s canonical-doc-set
enumeration (lines 56–64), which I refreshed fully (FM v11 / Op Stds v18 / V&R v9 / Handover v9 /
Excellence v4) because a literal "current canonical doc set" list must be internally coherent. A handful
of stale `FM v4`/`v8` inheritance-boilerplate cites remain elsewhere — **flagged** for a follow-up.

**D6 — No frontmatter `last_verified` bump on citation-only touches.** A version-cite refresh is not a
re-verification of the doc's claims, so bumping `last_verified` / `last_verified_against` would overstate.
The sweep is recorded in §G28 + this log instead. (The new `smartsheet-structure.md` gets a fresh stamp —
it *is* newly authored + live-verified against `21bd909`.)

## Out of scope / flagged for follow-up
- **Demo-abandonment** as a cross-repo exec (`sheet_ids.py` `WORKSPACE_DEMO`) + doctrine (Op Stds §24) decision.
- **Exec `sheet_ids.py` `FOLDER_SAFETY_PORTAL` comment refresh** (Form Catalog split).
- **Residual stale `FM v4/v8` inheritance-boilerplate cites** (PO/subcontracts/ai-employee/extended-workstreams).
- **email-triage currency touch** (v8/v13 → current, with its sweep note).
- **`Forfront IL portfolio` workspace `2228567565199236`** — live (ADMIN), in no code, purpose unknown.
- Contacts roster stays **exec-only** (`cutover_checklist.md`); not added to the blueprint (Customer-0 data).

## Verification
`brief-validator` + `doc-reconciliation-auditor` (both read-only/propose-only) + live Smartsheet MCP browse.
`scripts/lint_frontmatter.py` + `scripts/lint_crossrefs.py` clean. Landed via PR (blueprint CI = those two
lints only; there is no test suite, so a "four-part verify" reduces to lint-CI-green + merged).
