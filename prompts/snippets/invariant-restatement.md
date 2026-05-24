---
type: snippet
name: invariant-restatement
version: 1
audience: cc
usage_count: 0
---

# Invariant Restatement (snippet)

Paste this verbatim into any prompt or doc that touches code or data
flows involving external-bound output OR external content ingestion.
Fill in the `{workstream-specific}` placeholders.

## Used by

- `scaffold/cc-implementation.md` — when the implementation touches
  external send paths or external content ingestion
- `scaffold/new-workstream.md` — every workstream's mission +
  brief inherits both invariants

## Snippet content (paste this into the target doc)

```markdown
## Foundation invariants

Per `doctrine/foundation-mission.md` (its-blueprint repo). Both
invariants are non-negotiable; every workstream inherits both.

### Invariant 1 — External Send Gate

No external transmission without explicit human approval. Permanent,
not time-bounded.

- **Workstream-specific application**: {how this workstream's
  customer-facing output is gated. Reference the workstream's
  `<Workstream>_Pending_Review` Smartsheet with the standard columns
  (Approved for Send, Approved By, Approved At, Sent At, Send Status).}
- **Two-process model**: {how generation and send are separated in
  this workstream. Name the specific script files. Generation script
  cannot import any send capability; send script cannot import any
  AI capability. Both are registered in
  `tests/test_capability_gating.py`.}

### Invariant 2 — Adversarial Input Handling

All content originating outside the operating customer tenant is
untrusted data. Six-layer defense.

- **Workstream-specific application**: {which of the six layers are
  load-bearing for this workstream. Common pattern: Layer 1 (sender
  allowlist via ITS_Trusted_Contacts sheet + scope enforcement +
  header-forgery detection); Layer 2 (untrusted-content tagging via
  `shared.untrusted_content.wrap()`); Layer 5 (anomaly logging via
  `shared.anomaly_logger.check()`); plus Layer 6 attachment screening
  for any workstream with attachment intake.}
- **Untrusted-content tagging**: every Anthropic API call processing
  external content uses `shared.untrusted_content.wrap()` and the
  canonical system-prompt boilerplate.
- **Anomaly logging**: every extraction output passes through
  `shared.anomaly_logger.check()` before being trusted.
```

## Why this snippet exists

Restating invariants inline in every brief is defense in depth. The
operator and CC both need the reminder; doctrine living in a separate
file means it can be missed. Pulling the restatement into a snippet
means doctrine changes propagate automatically to every brief that
includes the snippet, rather than each brief drifting independently.

When this snippet's `version` bumps (e.g., FM v9 introduces a seventh
defense layer), every consumer scaffold should be reviewed in the
same PR to absorb the change. The cross-ref linter doesn't catch
this drift automatically — it's a manual review item at v-bump time.
