---
type: scaffold
name: pr-merge-verify
version: 1
audience: cc
usage_count: 0
---

# PR Merge Verification

Codifies the four-part landed-verify discipline from
`docs/operations/pr_merge_discipline.md` in the `its` repo. Run after
EVERY PR squash-merge. Until all four parts pass, the PR is "merged but
not landed."

## When to use

- Every PR. Without exception.
- Even hotfix PRs. Especially hotfix PRs.

## Template (executable as-is, replace <N>)

```bash
# After: gh pr merge <N> --squash --delete-branch

# 1. PR-state triplet
gh pr view <N> --json mergedAt,mergeCommit,state
# Assert manually: state=MERGED, mergedAt non-null, mergeCommit.oid present

# 2. Capture merge SHA into shell variable
MERGE_SHA=$(gh pr view <N> --json mergeCommit --jq '.mergeCommit.oid')
echo "Merge SHA: $MERGE_SHA"

# 3. Wait for push: main run on the merge commit to complete
until gh run list --branch main --commit "$MERGE_SHA" \
    --json status --jq '[.[].status] | all(. == "completed")' | grep -q true; do
  echo "Waiting for main-branch CI on $MERGE_SHA..."
  sleep 30
done

# 4. Verify all main-branch runs concluded as success
gh run list --branch main --commit "$MERGE_SHA" \
    --json conclusion --jq '[.[].conclusion] | all(. == "success")' | grep -q true \
  || { echo "ERROR: post-merge main CI failed on $MERGE_SHA"; \
       gh run list --branch main --commit "$MERGE_SHA" --json databaseId,name,conclusion; \
       exit 1; }

echo "PR #<N> four-part verify: clean"
```

## Session log line

Every session log that records a merged PR includes the four-part
result:

```
- pytest: <N> passed / <M> skipped / <D> deselected
- mypy: <E> errors / <F> source files
- ruff: clean
- main-branch CI on merge commit: SUCCESS
```

If the fourth line is anything other than SUCCESS, the session log
records the PR as "merged but not landed" and the next action is the
CI fix, not the next deliverable.

## When step 4 fails

The PR is NOT landed even if state=MERGED. Two valid resolutions:

- Revert this PR until `main` is restored, OR
- Land a CI-fix PR first, then re-land this PR's changes

"Inherit and propagate red main" is NOT acceptable. PR #68 through
PR #73 landed under that framing historically; PR #74 codified this
discipline to prevent recurrence.

## Why this works

PR #34 ghost (closed-not-merged in branch cleanup, claimed landed in
memory) and the PR #68→#73 red-main propagation are the two failure
cases this discipline retires. Step 1 catches ghosts; steps 3+4 catch
propagation. All four are necessary.
