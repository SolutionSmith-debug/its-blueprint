---
type: audit
status: canonical
last_verified: 2026-05-24
last_verified_against: 79eec73
workstream: null
tags: [secret-exposure, gitleaks, security-baseline, public-repo]
---

# 2026-05-24 — Secret-Exposure Audit (SolutionSmith-debug/its)

Forensic audit conducted during the 2026-05-24 security-hardening cluster. Read-only — no settings changed, no tokens touched, no remediation in scope. Establishes the baseline for the public-repo stay-public decision.

## Summary

| Metric | Count |
|---|---|
| Secrets in CI (repo + env + Dependabot) | 0 |
| Gitleaks findings (current tree) | 0 |
| Gitleaks findings (full history, all refs) | 0 |
| Files matching env/secret patterns (current tree) | 0 |
| Files matching env/secret patterns (anywhere in git history) | 0 |
| Active secret-scanning alerts | N/A (feature was disabled at audit time; enabled post-audit per audit-gap closure) |
| Active Dependabot alerts | N/A (feature was disabled at audit time; enabled post-audit) |
| Active code-scanning alerts | N/A (no analysis ever configured at audit time; CodeQL default setup enabled post-audit) |
| Workflow files referencing secrets.* | 0 |
| Outside collaborators | 0 (solo owner) |
| Repo deploy keys | 0 |

**Headline:** the repo is clean. No tokens needed rotation; no exposure exists to remediate. Stay-public decision validated.

## Methodology

- **Tools used:** gitleaks 8.30.1 (installed via `brew install gitleaks` for this audit), `gh api`, `grep`/`find` over the working tree and git log.
- **Scope:** full git history (`--log-opts="--all"`), all refs, all branches reachable.
- **Mode:** read-only. No `--fix` flags, no settings PATCH/PUT, no token operations.
- **Verification of architectural claim:** the ITS doctrine that "all secrets live in macOS Keychain" was verified empirically by the absence of env-file patterns and the absence of any committed credential material.

## Findings (per category)

### 1. Repo-level GitHub Secrets

API response empty. Zero secrets configured at the repo level.

### 2. Environment-scoped secrets

Zero environments configured. Therefore zero environment-scoped secrets.

### 3. Dependabot secrets

API response empty. Zero Dependabot secrets.

### 4. Deploy keys + fine-grained PATs

Zero deploy keys. Fine-grained PATs not enumerable via API; verified operator-side in GitHub UI: zero fine-grained PATs configured at audit time. Zero classic PATs.

### 5. Secret-scanning alerts

Feature was disabled at audit time (HTTP 404: "Secret scanning is disabled on this repository"). Surfaced as audit gap #1 — closed post-audit by enabling secret scanning + push protection.

### 6. Code scanning + Dependabot alerts

- Code scanning: HTTP 404 ("no analysis found") — never configured. Surfaced as audit gap #3 — closed post-audit by enabling CodeQL default setup.
- Dependabot alerts: HTTP 403 ("Dependabot alerts are disabled for this repository"). Surfaced as audit gap #2 — closed post-audit by enabling Dependabot alerts.

### 7. Gitleaks scans

Current-tree scan: 112 commits scanned, ~2.45 MB, 304ms. **No leaks found.**

Full-history all-refs scan: 112 commits scanned, ~2.45 MB, 217ms. **No leaks found.**

Both scans returned the same commit count because all merged feature branches were deleted on remote + pruned locally during the session prior to audit.

### 8. env / secret / credential file scan

- Current tree (excluding `.venv/` and `.git/`): no matches for `.env*`, `secrets.json`, `credentials.json`, `*.pem`, `*.key`.
- Git history (files ever added at any commit): no matches.

Zero files matching secret-pattern shapes have ever been committed.

### 9. .gitignore coverage

Solid baseline at audit time: `.env`, `.env.*`, `*_secret*`, `*credentials*.json`, `*.token`. CLAUDE.md doctrine "All secrets live in macOS Keychain" referenced in the file.

Gap surfaced: no explicit coverage for `*.pem` or `*.key`. Currently moot (none exist), but flagged as audit gap #5. Closed post-audit by PR #83 (added `*.pem` and `*.key` to `.gitignore` for defense-in-depth).

### 10. Workflow files — secret echo / log leak patterns

- Echo of `${{ secrets.* }}`: zero matches.
- Any `secrets.*` reference at all: zero matches.

The only workflow file at audit time was `.github/workflows/ci.yml` (1143 bytes). Used `GITHUB_TOKEN` implicitly via `actions/checkout`; no other secrets referenced. Zero surface area for workflow-side leak.

### 11. Fork-PR / workflow permissions

- `default_workflow_permissions=read` — `GITHUB_TOKEN` starts read-only.
- `can_approve_pull_request_reviews=false`.
- Fork-PR approval policy at audit time: `first_time_contributors` (default for public repos). Tightened to `all_external_contributors` (strongest) post-audit per stay-public security-minded direction.

### 12. Visibility + settings

- visibility: public, archived: false, disabled: false, is_template: false
- has_issues: true, has_wiki: false, has_pages: false, default_branch: main

### 13. Collaborators

Solo owner. Zero outside collaborators. Zero unexpected access.

## Per-finding rotation analysis

No findings. Specifically:

- No gitleaks hit at any commit → nothing to evaluate for reachability.
- No env-file or credential-file pattern in current tree or any commit ever added.
- No workflow `secrets.*` reference.
- No repo / environment / Dependabot secret of any kind exists in GitHub.
- No deploy keys or unexpected collaborators.

**Token rotation required: NONE.**

The architectural choice that all secrets live in macOS Keychain (per `shared/keychain.py` + `.gitignore` + CLAUDE.md), enforced consistently since the repo's earliest commits, means there are no exposed tokens to rotate — regardless of whether the repo stays public or goes private.

## Audit gaps surfaced (all closed post-audit)

These are NOT rotation-class findings — they're observability/hygiene gaps that the audit identified as worth closing:

| # | Gap | Closure |
|---|---|---|
| 1 | Secret scanning disabled | Enabled post-audit (+ push protection) |
| 2 | Dependabot alerts disabled | Enabled post-audit (alerts only; automated-security-fixes deliberately not enabled) |
| 3 | Code scanning never configured | CodeQL default setup enabled (Python + Actions, weekly) |
| 4 | Fine-grained PAT inventory not API-enumerable | Verified operator-side in GitHub UI: zero PATs |
| 5 | `.gitignore` doesn't cover `*.pem` / `*.key` | PR #83 added explicit coverage |

## CodeQL initial-scan findings (post-audit)

The CodeQL default setup landed during audit-gap closure ran its initial scan and produced 8 alerts. Triage results captured here for the audit trail:

| # | Path | Rule | Final | Reason |
|---|---|---|---|---|
| 1 | `.github/workflows/ci.yml:10` | `actions/missing-workflow-permissions` | fixed (auto) | PR #85 added explicit `permissions: contents: read` |
| 2 | `scripts/migrations/build_its_trusted_contacts_sheet.py:133` | `py/clear-text-logging-sensitive-data` | dismissed (FP) | Sheet name + status + sheet-ID; file-path heuristic flagged a no-PII line |
| 3 | `scripts/migrations/seed_its_trusted_contacts.py:207` | same | dismissed (FP) | Sheet-ID routing constant; live-write PII path remediated in PR #84 |
| 4 | `scripts/migrations/seed_its_trusted_contacts.py:215` | same | dismissed (FP) | Integer count (legacy entries scanned) |
| 5 | `scripts/migrations/seed_its_trusted_contacts.py:216` | same | dismissed (FP) | Integer count (rows planned/added) |
| 6 | `scripts/migrations/seed_its_trusted_contacts.py:217` | same | dismissed (FP) | Integer count (rows skipped) |
| 7 | `scripts/setup_box_oauth.py:239` | same | dismissed (FP) | OAuth auth URL — only public client_id + single-use CSRF state token |
| 8 | `scripts/smoke_test_box.py:55` | same | dismissed (FP) | Keychain service-name constants, not secret values |

Independently surfaced and remediated via PR #84: the inner-function PII logging in `seed_its_trusted_contacts.py` (lines 130–131, 141, 167, 172) which CodeQL had NOT flagged but which the verify-before-fix gate-check identified as the real concern under the file-path heuristic's flagged summary lines. Dry-run path preserved; live-write path stripped.

## Known-FP patterns for future CodeQL scans

Three FP patterns surfaced today that future scans may re-trigger:

1. Logging Keychain service-name constants (`ITS_BOX_CLIENT_ID`, etc.) — the names contain SECRET/TOKEN/KEY substrings but are documented constants, not values.
2. OAuth 2.0 authorize URL containing public `client_id` + single-use CSRF state token — public by design.
3. Any `print()` in modules with `trusted_contacts` in the path — filename heuristic over-triggers regardless of content.

When new alerts match these patterns, dismiss-as-FP is the default unless the content shows actual secret/PII value being logged.

## Re-audit guidance

Re-run gitleaks periodically — specifically after:

- New `shared/*` SDK wrapper merges (these handle external-system tokens)
- Any addition of new credentialed surfaces beyond Smartsheet / Box / Graph / Sentry / Resend
- Suspicion of a leak (e.g., GitHub secret-scanning alert fires)

Re-audit cadence: opportunistic, triggered by surface-area changes. Not on a fixed schedule.

## Authority

Secret-Exposure Audit, 2026-05-24. Forensic snapshot against `SolutionSmith-debug/its` commit `79eec73`. Future audits in this category extend the audits/ directory with new dated files (this doc never gets versioned/superseded; new audits are new files).

Cross-reference: [Op Stds v12 §39](../doctrine/operational-standards.md#39-new-per-customer-fork-security-setup) for the security-baseline doctrine this audit verified the fork against.
