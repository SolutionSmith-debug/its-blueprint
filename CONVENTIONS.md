# ITS Blueprint — Doc Conventions

Canonical structure for every `.md` file in this repo. Mirrors the
execution-layer `docs/operations/doc_conventions.md` with planning-side
extensions (doctrine, mission, brief types).

## Frontmatter

REQUIRED on every doc EXCEPT `README.md`, `CONVENTIONS.md`, and
`CLAUDE.md` (this file's exempt list mirrors the execution-layer
linter).

```yaml
---
type: doctrine | mission | brief | reference | audit | session_log | overlay | scaffold | snippet
version: 8                          # monotonic integer; canonical state tagged in git
status: canonical | draft | superseded | archived
last_verified: 2026-05-24           # ISO date; lint warns if stale beyond N days
last_verified_against: bee6f46      # git SHA of its repo, or blueprint commit SHA
supersedes: doctrine/foundation-mission.md@v7   # optional
workstream: safety_reports | safety_portal | email_triage | purchase_orders |
            subcontracts | ai_employee_capabilities | null
tags: [external-send-gate, invariant]   # optional
---
```

### Field semantics

| Field | Required | Notes |
|---|---|---|
| `type` | yes | Discriminator. Must be in canonical set. |
| `version` | yes for doctrine/mission/brief | Monotonic int. Filename is stable; this carries the version. |
| `status` | yes | `canonical` = currently in force. `draft` = work in progress. `superseded` = retired by a successor. `archived` = retired, no successor. |
| `last_verified` | yes for status=canonical | ISO date the doc was last checked against reality. |
| `last_verified_against` | yes for status=canonical | Git SHA (in `its` repo or here) that the verification was against. |
| `supersedes` | optional | When v8 supersedes v7, point at the prior doc with `@vN`. |
| `workstream` | yes | Closed set. `null` valid for cross-cutting. |
| `tags` | optional | Free-form supplementary. |

### Canonical sets

- **types**: `doctrine`, `mission`, `brief`, `reference`, `audit`, `session_log`, `overlay`, `scaffold`, `snippet`
- **status**: `canonical`, `draft`, `superseded`, `archived`
- **workstream**: `safety_reports`, `safety_portal`, `email_triage`, `purchase_orders`, `subcontracts`, `ai_employee_capabilities`, `null`

Adding a workstream = small PR editing `scripts/lint_frontmatter.py`
and this file. Don't ad-hoc.

## Prompt Scaffolds

The `prompts/` directory holds orchestration scaffolds (meta-prompts
for chat-to-CC or operator-to-CC direction) and reusable snippets.
Distinct from `its/prompts/` (execution repo), which holds runtime
prompts called by Python at API time.

### Scaffold frontmatter

```yaml
---
type: scaffold
name: <slug matching filename without .md>
version: 1                    # monotonic int; bump on substantive revision
audience: chat | cc | operator | (combination, e.g., "chat | cc")
usage_count: 0                # monotonic; bump on substantive revision (not every use)
---
```

### Snippet frontmatter

Same shape as scaffolds, with `type: snippet`. Snippets get extracted
when a fragment is used by ≥2 scaffolds.

### Filename convention

- Scaffolds: `prompts/scaffold/<slug>.md` — slug kebab-case.
- Snippets: `prompts/snippets/<slug>.md` — slug kebab-case.

### When to add a scaffold

When the same orchestration pattern has been used ≥3 times in chat or
by operator and is worth capturing. Don't speculatively scaffold.

### When to extract a snippet

When a fragment appears verbatim in ≥2 scaffolds. Move to `snippets/`,
reference from each scaffold.

## Filename convention

Stable. NO version suffixes (the version lives in frontmatter; git tags
mark canonical commits).

- **Doctrine**: `doctrine/<topic>.md`. E.g., `doctrine/foundation-mission.md`.
- **Workstreams**: `workstreams/<slug>/{mission,brief}.md`. Slug uses
  kebab-case. E.g., `workstreams/safety-reports/mission.md`.
- **References**: `references/<topic>.md`.
- **Audits**: `audits/YYYY-MM-DD_<topic>.md` (time-bound, date-prefixed).
- **Session logs**: `session-logs/YYYY-MM-DD_<topic>.md`.

The lint script flags filename mismatches per type.

## Cross-references

Use markdown links to stable filenames + anchors. Never link to a
versioned filename. Examples:

```text
[External Send Gate](../doctrine/foundation-mission.md#invariant-1--external-send-gate-unchanged-from-v7)
[picklist sync runbook](https://github.com/SolutionSmith-debug/its/blob/main/docs/references/picklist_sync.md)
```

Anchors are GitHub-style autogen: lowercase, hyphens for spaces, strip
punctuation. The cross-ref linter validates every link resolves.

## Versioning workflow

1. Doc starts at `version: 1, status: draft`.
2. When ready, flip to `status: canonical`. Tag the commit
   `<topic>-v1` (e.g., `foundation-mission-v8`).
3. On substantive change: bump `version` to N+1 in same file (don't
   create a copy); flip prior tag's content to archived in-place via
   the supersession chain.
4. Filename never changes.

## Lazy retrofit

Same policy as the execution repo: existing docs grandfathered;
new docs MUST conform; when any doc is touched for unrelated reasons,
retrofit it. The lint script runs warn-only during the retrofit window
(no end date yet — set after this initial big-bang migration is fully
absorbed).

## Tooling

- `scripts/lint_frontmatter.py` — validates frontmatter shape +
  canonical sets + filename match per type.
- `scripts/lint_crossrefs.py` — walks every `[text](path)` link in
  every `.md` and verifies the target exists and the anchor (if
  any) is generated by the target file's headings.
- `scripts/render_handoff_packet.py` — pandoc `.md → .docx` for
  customer/external delivery. Run only at handoff boundaries; the
  rendered `.docx` is NOT committed (output goes to `handoff/` which
  is gitignored).

## Owner

Seth Smith. Convention changes require a small PR; the lint scripts
are codified against the spec above.
