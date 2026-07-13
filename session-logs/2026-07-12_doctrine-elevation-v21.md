---
type: session_log
status: archived
workstream: null
tags: [doctrine, operational-standards-v21, section-55, verification-discipline, truthful-reporting, anti-hallucination, reconstruction, lost-v10-sections, data-fidelity, handover-v10, foundation-mission-invariant-1, vision-1.4.3, send-gate, cutover-posture, operator-directed]
---

# 2026-07-12→13 — Operational Standards v21: quality-discipline elevation + reconstruction of the lost v10 sections

## Purpose

The follow-up to the 2026-07-12 documentation-reconciliation (see §G63 + exec session log
`2026-07-12_documentation-reconciliation.md`). The operator answered four scope decisions and then
directed an **operational-standards elevation** — "update our operational standards to a better level of
quality practice, ensuring that future sessions don't lie or hallucinate and actually validate the work" —
and "add it to our corpus of markdown files and commit and merge everything." This session did that:
authored a new §55, reconstructed two lost carry-forward stubs, and landed the whole doctrine bundle across
both repos.

## Operator decisions (ratified this session)

- **Q1 — SC-S4 subcontract SEND** is a **best-effort Aug-7 target, NOT a cutover blocker**: subcontract
  *generation* ships regardless; send defers gracefully if SC-S4 doesn't land. (exec #551 softened CL-38 + D18.)
- **Q2 — amend all three** companion doctrine docs (FM Invariant 1, Vision §1.4.3, Handover).
- **Q3 — reconstruct the lost §§4-22 / §25-30** (see the discovery below); do NOT restore "verbatim v10"
  (it doesn't exist). Elevate the quality discipline into doctrine.
- **Q4 — `po-send` stays launchd-UNLOADED at cutover** (the send-gate-strict alternative); VC-02 gains
  `DARK_UNLOADED_LABELS`. (exec #551; docs 15→14 loaded.)

## The load-bearing discovery (Q3)

The `# §§4-22 — Carry Forward From v10` and `# §25-§30 — Carry Forward From v10` lines were **stubs from the
very first commit** ("Initial migration from .docx corpus"). The full section bodies were **never committed to
git** — the migration brought only the deltas + the two carry-forward pointers — and the operator does not
have the v10 `.docx`. So the content was **genuinely unrecoverable**, not merely stubbed. Per the operator's
directive it was **reconstructed** from the surviving execution-layer paraphrases + `§N` code citations (a
6-agent workflow), each section marked `> *Reconstructed…*` (honesty, not verbatim).

**§4 was mislabeled.** The stub index named §4 "reviewer chain" (duplicating §15) — but 6+ live code
citations (`seed_its_active_jobs.py "§4 — Address sourced from live data ONLY"`, tech_debt, session logs,
info-gap, memory-archive) resolve §4 as **Data Fidelity / No-Invented-Field-Data**; the reviewer chain is
**§15**. The index has carried this mislabel since v11. §4 is thus itself an anti-hallucination doctrine —
dovetailing with the new §55.

## What landed

**Blueprint doctrine v21 — `#66` (`1e24574`, lint-clean):**
- **NEW §55 — Verification & Truthful-Reporting Discipline**: §55.1 verify-before-asserting (anti-hallucination) ·
  §55.2 prove-the-control-bites · §55.3 the four-part landing verify · §55.4 faithful reporting — elevating the
  execution-layer reflexes (`docs/HOUSE_REFLEXES.md`) to canonical doctrine.
- **§§4-22 + §25-30 reconstructed** (25 sections, replacing the two dead stubs; §4 relabeled Data-Fidelity).
- **Riders** §31 (`intake_poll` retired), §32 (+progress_reports/field_ops), §36 (~215 / split file).
- **Companions**: FM Invariant 1 "customer-facing" → "external recipient" (covers PO→vendors, subk→subcontractors);
  Vision §1.4.3 rescope (email-attachment screening = Email-Triage DoD, does NOT gate Aug-7 — portal photos
  satisfy §34); **Handover → v10** (Check C = 12 jobs not 4, Friday-catch-up closed via Check I, 7-workstream roster).

**Exec-side (kept the cross-repo consistent + CI green):**
- `#551` — Q4 po-send-unloaded (VC-02 `DARK_UNLOADED_LABELS`, +2 prove-it-bites tests) + Q1 SC-S4 framing.
- `#553` — `doctrine_manifest.yaml` (op_stds 20→21, `max_section` 54→55, handover 9→10) + CLAUDE.md/README/
  agent version refs → v21, so the M1/M7 drift gate stays green.
- `#555` — README reconciled to as-built (all 8 packages + 15 daemons — a gap the reconciliation had missed).

## The transformation practiced §55

The 105 KB → 155 KB `operational-standards.md` rewrite went through an **assert-heavy Python transformer,
dry-run-verified before writing** (§55.2), and the exec sync was **proven against the `check_doctrine_drift`
oracle** rather than assumed (§55.2 again). The reconstructed sections wear their `Reconstructed` markers
rather than posing as verbatim (§55.4).

## Verify

- Blueprint `#66`: `lint_frontmatter` + `lint_crossrefs` clean (96 files); state=MERGED · mergeCommit `1e24574`.
- Exec `#551`/`#553`/`#555`: ruff clean · mypy 360 files clean · pytest pass · `check_doctrine_drift --strict`
  no blocking drift (M1/M4/M7) · all four-part-verified (state=MERGED · mergedAt · mergeCommit · main-CI green).

## Open (operator)

- **Skim the 25 reconstructed sections** — canonical now but marked reconstructed-from-paraphrases; 5 carry a
  `thin-evidence` flag. Correct any and drop its marker.
- **CL-23** — `main` still UNPROTECTED (server-side; top of the cutover punch-list).
- SC-S4 subcontract send remains an unbuilt best-effort target (separate engineering brief).
