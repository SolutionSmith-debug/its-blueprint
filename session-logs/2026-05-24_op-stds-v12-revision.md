---
type: session_log
status: archived
workstream: null
tags: [doctrine-revision, op-stds, cc-tooling, fork-security, pii-logging, actions-discipline]
---

# 2026-05-24 — Operational Standards v11 → v12 revision

## Purpose

Codify the doctrine implications of the 2026-05-24 execution-repo work cluster (PRs #79–85 in `SolutionSmith-debug/its` + server-side branch protection + audit-gap closures). Five new sections (§§37–41) capture conventions that apply to all current and future ITS customer forks.

## Pre-flight findings

The execution-repo work cluster generated substantive doctrine implications that the chat-side workflow had not yet cascaded back to blueprint. Pattern: chat directs CC for execution-repo work; the work succeeds; the planning-side absorption step is at risk of being skipped if not deliberately triggered.

This session is the deliberate cascade step. The cluster wrap (`cluster_wrap_2026-05-24.md`, uploaded to project knowledge) captures the narrative; this PR captures the doctrine.

Verified at pre-flight:

- Repo state: clean main, last commit `1163075` (memory-consolidation PR #3).
- `python3 scripts/lint_frontmatter.py` → clean (48 files; required `pip3 install pyyaml` as one-time dev setup on this machine — pyyaml is the linter's only external dep).
- `python3 scripts/lint_crossrefs.py` → clean (48 files).
- `gh api repos/SolutionSmith-debug/its-blueprint/branches/main/protection` → **HTTP 403 "Upgrade to GitHub Pro or make this repository public to enable this feature"**. The blueprint is private on a free GitHub plan, and branch protection on private repos is a paid feature. Logged for awareness — the planning repo has no server-side enforcement of the merge-discipline that the execution repo enforces. Mitigation today: solo + CC operation means the operator-side merge discipline (squash + four-part-equivalent verify + linter gates) is sufficient. Re-evaluate if the planning repo ever gets multi-contributor.

## Decisions made

- **Decision**: Five separate sections rather than one combined section.
  - **Alternative considered**: Single combined section "§37 CC tooling + fork security" with subsections.
  - **Rationale**: Existing Op Stds pattern (§31–§35 in v11 are similarly related but kept separate). Separate sections are easier to cross-reference from workstream briefs and reference docs. The five sections cover genuinely distinct concerns (skills convention, hook convention, fork-setup baseline, PII asymmetry, actions discipline).

- **Decision**: §37 lists installed skills explicitly by name.
  - **Alternative considered**: Reference the install command and let the install determine the list.
  - **Rationale**: The default install set is the doctrine-level commitment. Listing skills explicitly makes the doctrine a verifiable reference and surfaces drift if upstream `mattpocock/skills` ever changes its default set. Skill list updates are doctrine extensions (`last_verified` bump), not v-bumps.

- **Decision**: §39 references the customer-fork-setup-checklist by name as a forward reference.
  - **Alternative considered**: Embed all `gh api` commands inline in §39.
  - **Rationale**: §39 is doctrine (what the baseline IS); the checklist is operational (how to apply it). Mixing the two makes both harder to maintain. Forward references between doctrine and reference docs are valid per CONVENTIONS.md. The forward reference to `references/customer-fork-setup-checklist.md` is backtick-wrapped in both §39 and the Authority section, so the cross-ref linter's "skip backticked paths" behavior keeps this PR lint-clean even though the checklist file doesn't yet exist (it lands in PR 2).

- **Decision**: §40 explicitly says dry-run preserves PII while live-write strips it.
  - **Alternative considered**: Strip PII from both paths uniformly.
  - **Rationale**: Dry-run is review material — the operator needs PII visibility to verify what WILL be added before confirming. Stripping defeats the purpose. The asymmetry rule matches the threat model: dry-run output is ephemeral operator-confirmation; live-write output persists in scrollback/screen-shares/shell-history.

- **Decision**: §41 codifies the verify-before-bump pattern with PR #81 as canonical example.
  - **Alternative considered**: Leave as a general "verify-before-fix" instance under §14.
  - **Rationale**: GitHub Actions version bumps are common enough and have specific failure modes (Node.js runtime version, breaking input changes) that warrant dedicated doctrine. §41 references back to verify-before-fix as the parent principle.

- **Decision**: No downstream cascade in this PR — separate PR follows for `customer-fork-setup-checklist.md`.
  - **Alternative considered**: Bundle the checklist into this PR for atomicity.
  - **Rationale**: `prompts/scaffold/doctrine-revision.md` explicitly prohibits bundling doctrine bump with cascade. Land doctrine first, validate clean absorption, then sweep downstream in PR 2.

## Doc changes (this PR)

- Edited `doctrine/operational-standards.md`:
  - Frontmatter: version 11 → 12; `last_verified_against` 3b7d56d → 79eec73; supersedes pointer updated to v11; tags extended with `cc-tooling`, `fork-security`, `pii-logging`, `actions-version-discipline`.
  - Subtitle and version-line updated (v11 → v12, new date, new "Cluster Absorb" subtitle).
  - "What Changed in v12" section added between "What Changed in v11" and `# §1 — Kill Switch`.
  - §§37–41 added between §36 (In-Repo Tech Debt Log) and Authority section.
  - Cross-references added: §3.1 ↔ §38 + §39; §14 ↔ §37; §30 ↔ §37 (all called out in the "What Changed in v12" section).
  - Authority section updated.

- Created `session-logs/2026-05-24_op-stds-v12-revision.md` (this file).

## Verification

- `python3 scripts/lint_frontmatter.py` → expect clean (49 files after this PR; 48 was the baseline).
- `python3 scripts/lint_crossrefs.py` → expect clean (49 files).
- Doctrine tag will be pushed post-merge: `git tag operational-standards-v12 && git push --tags`.

## Out of scope

- Did NOT create `references/customer-fork-setup-checklist.md` — that's PR 2 (downstream cascade per doctrine-revision discipline).
- Did NOT create `audits/2026-05-24-secret-exposure-audit.md` — that's PR 3 (independent artifact).
- Did NOT append §G7 to `references/memory-archive.md` — that's PR 3 (independent artifact).
- Did NOT modify any workstream mission/brief — workstreams cross-reference Op Stds by stable anchor; no v-pointer updates needed.

## Sequencing context

This PR is the first of three planning-side PRs absorbing the 2026-05-24 execution-repo work cluster. PR 2 follows immediately (downstream cascade from §39). PR 3 follows after that (audit + memory archive §G7).

After all three land, the planning-layer absorption of the 2026-05-24 work cluster is complete and the cluster wrap can be considered fully cascaded.

## Cross-references

- Execution-repo PRs absorbed by this doctrine bump: #79 (skills), #80 (hooks), #81 (actions bump), #84 (PII asymmetry), #85 (workflow permissions). All at https://github.com/SolutionSmith-debug/its/pulls
- Cluster wrap: `cluster_wrap_2026-05-24.md` (uploaded to Claude.ai project knowledge, not committed to this repo per precedent set by `cluster_wrap_2026-05-23.md`)
- Related PRs in this repo: PR 2 (customer-fork-setup-checklist), PR 3 (audit + memory archive §G7) — both follow this PR
