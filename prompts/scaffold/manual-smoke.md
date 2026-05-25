---
type: scaffold
name: manual-smoke
version: 1
audience: chat / operator
usage_count: 1
---

# Manual Smoke Procedure

For operator-side verification between CC-reports-complete and
pre-merge. Covers daemon migrations, new module work, and any change
that touches persistent state under `~/its/state/` or has external-API
side effects. Distinct from CI: CI exercises mocks; manual smoke
exercises real APIs against the sandbox tenant.

## When to use

- After CC reports completion of work that writes to `~/its/state/`.
- After CC reports completion of work that calls Smartsheet, Box, or
  Graph against real (sandbox) APIs.
- Before authorizing CC to run `gh pr merge` on a hardening-cluster PR.
- Any time the gap between "CI green" and "I trust this against real
  APIs" matters.

## When NOT to use

- Pure docs PRs (no code path executed).
- Pure scaffold / blueprint repo PRs (no executable code).
- Refactors where the test suite is the authoritative check
  (operator's call; default is to smoke anyway if state files are
  touched).

## zsh paste constraints

The smoke procedure ALWAYS lives within these constraints:

- **Single-line commands only.** Multi-line `python -c "…"` blocks
  inside outer double quotes break on paste — zsh splits at the
  embedded newlines and tries to execute fragments.
- **Use `python3 -c "import …; …; print(…)"` on a single line.** If a
  check needs multi-line logic, write it to a temp file first, then
  invoke. Never embed newlines inside quoted strings.
- **Echo section headers** so the output is parseable when pasted back.
  `echo "--- {check name} ---"` between each command.
- **Capture exit codes** for every script invocation:
  `script_call; echo "exit=$?"`.

## Template (skeleton)

Three batches, each paste-safe independently. Operator pastes each
batch, captures output, pastes back to chat for assessment.

### Batch 1 — Setup + before-snapshot

```bash
cd ~/its

git fetch origin
git checkout {feature-branch}
git log -1 --oneline

ls -la ~/its/state/ | grep -E "{relevant patterns}" || echo "(state dir empty)"

# {Optional: capture content of files about to change}
cat ~/its/state/{file} 2>/dev/null || echo "(missing)"
```

### Batch 2 — Invoke + per-script verification

For EACH daemon or script being smoked, in its own paste batch:

```bash
.venv/bin/python -m {module.path}
echo "exit=$?"

echo "--- {state file} content ---"
cat ~/its/state/{file}

echo "--- {sidecar / lock file} present? ---"
ls -la ~/its/state/{sidecar}

echo "--- {file} valid JSON? ---"
python3 -c "import json,os; json.load(open(os.path.expanduser('~/its/state/{file}'))); print('OK')"

echo "--- {timestamp file} content ---"
cat ~/its/state/{timestamp_file}

echo "--- stray tmp files? ---"
ls ~/its/state/ | grep -F ".tmp." || echo "none (good)"
```

### Batch 3 — Cross-consumer integration + cleanup

If multiple consumers share a state file, run them in sequence and
assert each consumer's key is preserved after the next consumer runs.
This is the F23 no-clobber pattern; reusable for any shared-state
migration.

```bash
.venv/bin/python -m {second module.path}
echo "exit=$?"

echo "--- {shared state} after BOTH consumers ---"
cat ~/its/state/{shared file}

echo "--- no-clobber check (expect ≥N keys) ---"
python3 -c "import json,os; d=json.load(open(os.path.expanduser('~/its/state/{shared file}'))); print('keys:', sorted(d.keys())); print('PASS' if len(d)>={N} else 'CHECK')"

echo "--- final stray tmp files check ---"
ls ~/its/state/ | grep -F ".tmp." || echo "none (good)"

git checkout main
```

## Standard assertion checklist

For each smoked entity:

| # | Assertion | Pass criteria |
|---|-----------|---------------|
| 1 | Script exit | exit=0 |
| 2 | State file present | file exists at expected path |
| 3 | State file valid | JSON parses (or expected non-JSON format) |
| 4 | Sidecar / lock file | present per design |
| 5 | Timestamp file | valid ISO 8601 |
| 6 | No tmp residue | `*.tmp.*` grep returns empty |
| 7 | Cycle log emitted | `error_log` cycle summary line in stdout |

For multi-consumer state files, add:

| 8 | No-clobber | All consumer keys present after sequential cycles |

## Failure handling

A red on any assertion does NOT block merge unconditionally. Common
non-blocking causes:

- **Pre-existing gaps** (e.g., a daemon's ITS_Daemon_Health row not
  seeded). Surfaces as WARN, daemon continues fail-open. Track as
  carryforward operator action, not a PR blocker.
- **Empty cycle paths** (e.g., seen-set file not created when
  fetched=0). Unit tests are the canonical correctness proof; smoke
  just confirms no regression.

A red that DOES block merge:

- Script exits non-zero (real crash).
- State file written but invalid JSON / wrong shape.
- Stray tmp files remaining (atomic-write cleanup broken).
- Sidecar lock pattern broken (file written without lock).
- Consumer A's key clobbered by consumer B (F23 protection failed).

## Why this works

- **zsh-paste-safe by construction.** The first iteration of this
  procedure used multi-line heredocs inside outer quotes and broke
  on paste; the single-line constraint is non-negotiable.
- **Three-batch structure** matches operator workflow: paste, run,
  paste output back; chat assesses; next batch.
- **Before/after capture** gives delta visibility — "what changed
  during the cycle" rather than just "what's there now."
- **Explicit pass criteria per assertion** prevents the
  "everything looks fine, ship it" failure mode where a real
  regression hides in a wall of output.

## Cross-references

- First use: `its` PR #88 smoke (2026-05-25), captured in
  `its/docs/session_logs/2026-05-25_state-io-atomic-write.md`.
- Four-part PR-landed verify: `prompts/scaffold/pr-merge-verify.md`.
- Tooling gotcha: `gh run view --json url` not `htmlUrl` (per
  `its/docs/operations/pr_merge_discipline.md` "Tooling gotchas").
