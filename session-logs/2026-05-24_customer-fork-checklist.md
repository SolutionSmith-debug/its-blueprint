---
type: session_log
status: archived
workstream: null
tags: [customer-fork, downstream-cascade, operational-checklist]
---

# 2026-05-24 — Customer Fork Setup Checklist (downstream cascade from Op Stds v12 §39)

## Purpose

Create the operational artifact derived from Op Stds v12 §39 (landed in prior PR `74ee6f8`). The checklist gives any operator the verbatim `gh api` commands and UI steps needed to harden a fresh customer fork to the §39 baseline.

## Pre-flight findings

Op Stds v12 §39 establishes the doctrine (what the baseline IS). Without the operational checklist, applying the baseline to Customer 2+ would require the operator to reconstruct the commands from doctrine prose. That reconstruction is error-prone and slow. The checklist makes the work mechanical.

Verified pre-flight:

- PR 1 landed on main at commit `74ee6f8` with tag `operational-standards-v12` pushed.
- `python3 scripts/lint_frontmatter.py` → clean (49 files, baseline for this PR).
- `python3 scripts/lint_crossrefs.py` → clean (49 files). Initial draft used a double-hyphen anchor (`#39-new--per-customer-fork-security-setup`) per the brief's spec; the actual GitHub-style slugify in `scripts/lint_crossrefs.py` collapses `\s+` to a single hyphen, so the correct anchor is `#39-new-per-customer-fork-security-setup` (single hyphen between "new" and "per"). Caught at PR-2 lint; fixed before push.

## Decisions made

- **Decision**: Verbatim `gh api` commands in the checklist, not abstract descriptions.
  - **Alternative considered**: Describe the configuration goals; let the operator write the commands.
  - **Rationale**: The point of the checklist is to remove discretion from a security-baseline application. Verbatim commands match the "defense by architecture" pattern — make the secure path the obvious path.

- **Decision**: Step 6 (PAT audit) explicitly flagged as operator-only.
  - **Alternative considered**: Skip the PAT audit since it's not API-automatable.
  - **Rationale**: The PAT audit is part of the §39 baseline. Documenting it as operator-only (with UI navigation steps) keeps the checklist complete and prevents "oh I forgot that part" gaps.

- **Decision**: Step 7 (gitleaks) included even though gitleaks isn't part of §39 configuration.
  - **Alternative considered**: Leave gitleaks for an audits/* artifact only.
  - **Rationale**: Gitleaks IS the verification step for §39's architectural defense claim ("all secrets in Keychain"). Without running it, the checklist completes "successfully" while leaving the architectural claim unverified. Step 7 makes the verification mandatory.

- **Decision**: Anchor cross-reference uses `[Op Stds §39](../doctrine/operational-standards.md#39-new--per-customer-fork-security-setup)` — a plain (non-backticked) markdown link that the cross-ref linter actively validates.
  - **Alternative considered**: Backtick-wrap the doctrine path the way forward references in PR 1 did.
  - **Rationale**: This PR lands AFTER §39 exists. A real validated link is preferable to a backticked path — the linter then catches any future rename of §39's heading.

## Doc changes (this PR)

- Created `references/customer-fork-setup-checklist.md` (new reference doc, derived from Op Stds v12 §39).
- Created `session-logs/2026-05-24_customer-fork-checklist.md` (this file).

## Verification

- `python3 scripts/lint_frontmatter.py` → expect clean (51 files; 49 baseline + this PR's reference doc + this session log).
- `python3 scripts/lint_crossrefs.py` → expect clean (51 files); confirms forward reference from this checklist to Op Stds §39's anchor resolves correctly.

## Out of scope

- Did NOT create the audit doc — that's PR 3.
- Did NOT append §G7 — that's PR 3.
- Did NOT modify Op Stds v12 — that landed in PR 1.

## Sequencing context

This PR is the downstream cascade from PR 1 (Op Stds v11→v12). After this lands, the doctrine + operational artifacts pair is complete for the per-customer-fork security setup concern.

PR 3 follows next (audit + memory archive §G7).

## Cross-references

- Predecessor PR: PR 1 (Op Stds v11 → v12), merge commit `74ee6f8`
- Successor PR: PR 3 (audit + memory archive §G7)
- Doctrine: [Op Stds v12 §39](../doctrine/operational-standards.md#39-new-per-customer-fork-security-setup)
- Future use: Customer 2+ onboarding (V&R v7.2 Phase 1.6 territory)
