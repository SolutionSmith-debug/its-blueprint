---
type: reference
version: 1
status: canonical
last_verified: 2026-05-24
last_verified_against: 79eec73
workstream: null
tags: [customer-fork, security-hardening, operational-checklist]
---

# Customer Fork Setup Checklist

Operational artifact derived from [Op Stds §39](../doctrine/operational-standards.md#39-new-per-customer-fork-security-setup). Apply when standing up a new ITS customer fork (Customer 2+, or any new repo that inherits ITS doctrine).

Order matters: execute steps in sequence. Each step is independently verifiable; do not proceed past a failed verification without operator review.

## Prerequisites

- `gh` CLI installed and authenticated as the fork owner
- Repository exists and at least one commit landed on `main` (branch protection requires existing branch)
- CI workflow committed (otherwise required-status-checks contexts will reference a job that never runs)

## Step 1 — Branch Protection on main

```bash
gh api -X PUT repos/<OWNER>/<REPO>/branches/main/protection --input - <<EOF
{
  "required_status_checks": {
    "strict": true,
    "contexts": ["test"]
  },
  "enforce_admins": false,
  "required_pull_request_reviews": null,
  "restrictions": null,
  "required_linear_history": true,
  "allow_force_pushes": false,
  "allow_deletions": false,
  "required_conversation_resolution": true,
  "lock_branch": false,
  "allow_fork_syncing": false
}
EOF
```

Substitute `<OWNER>/<REPO>` with the actual repo. The `contexts` array must match actual CI job names — derive via:

```bash
gh run list --branch main --limit 1 --json databaseId
gh run view <RUN_ID> --json jobs --jq '.jobs[].name'
```

Verify:

```bash
gh api repos/<OWNER>/<REPO>/branches/main/protection --jq '{strict: .required_status_checks.strict, contexts: .required_status_checks.contexts, linear: .required_linear_history.enabled, force: .allow_force_pushes.enabled, deletions: .allow_deletions.enabled}'
```

Expected: `strict=true`, contexts populated, `linear=true`, `force=false`, `deletions=false`.

## Step 2 — Fork-PR Approval Policy (public repos only)

For private repos, fork PRs are not possible — skip this step.

For public repos:

```bash
gh api -X PATCH repos/<OWNER>/<REPO>/actions/permissions/fork-pr-contributor-approval \
  -f approval_policy=all_external_contributors
```

Verify:

```bash
gh api repos/<OWNER>/<REPO>/actions/permissions/fork-pr-contributor-approval --jq '.approval_policy'
```

Expected: `all_external_contributors`.

## Step 3 — Secret Scanning + Push Protection

```bash
gh api -X PATCH repos/<OWNER>/<REPO> \
  -f 'security_and_analysis[secret_scanning][status]=enabled' \
  -f 'security_and_analysis[secret_scanning_push_protection][status]=enabled'
```

Verify:

```bash
gh api repos/<OWNER>/<REPO> --jq '.security_and_analysis'
```

Expected: both `secret_scanning.status` and `secret_scanning_push_protection.status` equal `enabled`.

## Step 4 — Dependabot Alerts (NOT auto-fixes)

```bash
gh api -X PUT repos/<OWNER>/<REPO>/vulnerability-alerts
```

(Returns HTTP 204 on success.)

Verify alerts are ON and automated-security-fixes are OFF:

```bash
gh api repos/<OWNER>/<REPO>/vulnerability-alerts -i 2>&1 | head -3   # expect HTTP 204
gh api repos/<OWNER>/<REPO>/automated-security-fixes 2>&1            # expect 404 OR body with "enabled":false
```

Auto-fixes deliberately stay off — auto-opened dependency-bump PRs conflict with the four-part-verify + manual-merge workflow.

## Step 5 — CodeQL Default Setup

```bash
gh api -X PATCH repos/<OWNER>/<REPO>/code-scanning/default-setup \
  -f state=configured \
  -f query_suite=default
```

(Note: the endpoint uses PATCH, not PUT.)

Verify:

```bash
gh api repos/<OWNER>/<REPO>/code-scanning/default-setup --jq '{state, query_suite, languages, schedule}'
```

Expected: `state=configured`, languages include the appropriate set for the fork (typically `python` + `actions` for ITS forks), `schedule=weekly`.

Initial scan kicks off asynchronously — don't wait for it to complete in this step.

## Step 6 — Operator-Only PAT Audit

Not API-automatable. Operator inspects in GitHub UI:

1. Navigate to `github.com → click profile avatar → Settings → Developer settings → Personal access tokens`.
2. **Fine-grained tokens** tab: verify each token's scope is per-repo (not "All repositories"), expiration is set, and the token is in use. Revoke unused or over-scoped tokens.
3. **Tokens (classic)** tab: same review. Classic tokens are the more likely place to find forgotten tokens from `gh auth login` or one-off scripts.

If any token is revoked, any tooling that depended on it will need a new narrower token issued.

## Step 7 — Architectural Verification (gitleaks)

Install gitleaks (one-time):

```bash
brew install gitleaks
```

Run against full git history:

```bash
cd <REPO> && gitleaks detect --source . --log-opts="--all" --no-banner --redact -v
```

Expected: zero findings. The ITS doctrine of "all secrets in macOS Keychain" combined with `.gitignore` coverage of secret-pattern files means a clean fork should have nothing to find. Any finding requires immediate token rotation regardless of repo visibility.

## Step 8 — Final Verification Summary

Capture the final state for the audit trail. Recommended: write to `audits/<YYYY-MM-DD>_<repo>-fork-setup.md` in this blueprint repo or in the customer fork's session log.

Minimum captured state:

```bash
gh api repos/<OWNER>/<REPO>/branches/main/protection > /tmp/branch_protection.json
gh api repos/<OWNER>/<REPO>/actions/permissions/fork-pr-contributor-approval > /tmp/fork_pr_policy.json
gh api repos/<OWNER>/<REPO> --jq '.security_and_analysis' > /tmp/security_analysis.json
gh api repos/<OWNER>/<REPO>/code-scanning/default-setup > /tmp/codeql_setup.json
```

## Authority

Customer Fork Setup Checklist v1, 2026-05-24. Derived from [Op Stds v12 §39](../doctrine/operational-standards.md#39-new-per-customer-fork-security-setup). Update this checklist when §39 changes (`last_verified` bump only for clarifications; version bump for substantive changes).

Canonical reference for: any Customer 2+ onboarding; any new ITS repo (sandbox, experiment, fork-of-fork); any retroactive hardening of an existing ITS repo to current baseline.
