# Prompts

Orchestration scaffolds — meta-prompts used by chat or operator to direct
Claude Code. Different from the execution-repo `its/prompts/` directory:
those are runtime prompts called by Python at API-call time. These are
patterns for chat/operator-to-CC direction.

## Layout

- `scaffold/` — full prompt templates. One file per pattern. Copy and fill
  in the placeholders.
- `snippets/` — reusable fragments that get embedded in larger prompts.
  Snippets get extracted when used by 2+ scaffolds, not invented upfront.

## Convention

Each scaffold has frontmatter (per CONVENTIONS.md "Prompt Scaffolds" section):

```yaml
---
type: scaffold | snippet
name: <slug matching filename>
version: 1
audience: chat | cc | operator | (combination)
usage_count: 0
---
```

`usage_count` is monotonic and bumped on substantive revision (not on
every use). It surfaces which scaffolds are load-bearing vs. dormant.

## When to add a new scaffold

When the same orchestration pattern has been used in chat (or by operator)
≥3 times and is worth capturing for future re-use. Don't speculatively
add scaffolds for hypothetical workflows.

## When to extract a snippet

When a fragment of prose (e.g., the foundation-invariant restatement, the
four-part PR verify block) appears verbatim in ≥2 scaffolds. Move it to
`snippets/` and reference from each scaffold.

## Index

| Scaffold | Audience | Purpose |
|---|---|---|
| `_example.md` | n/a | Copy-this template |
| `cc-implementation.md` | chat | Writing CC implementation prompts |
| `session-orientation.md` | chat | Fresh-session loading order |
| `forensic-audit.md` | chat | Repo audit pattern |
| `pr-merge-verify.md` | cc | Four-part PR landing check |
| `doctrine-revision.md` | chat | Updating a doctrine doc safely |
| `session-log.md` | chat / cc | Writing a session log |
| `new-workstream.md` | chat | Bootstrapping a new workstream |

| Snippet | Used by |
|---|---|
| `invariant-restatement.md` | `cc-implementation.md`, `new-workstream.md` |
