# Session Logs (Planning-Side)

Durable narrative records of **chat sessions** in the planning project.
Mirror concept of the execution-repo `docs/session_logs/` but for
decisions made in conversation that didn't (yet) land in a doctrine doc.

The execution-repo session logs cover code-changing cc sessions.
These cover doctrine-changing or roadmap-changing chat sessions.

## When to write one

A planning-side session log is appropriate when:

1. A chat session lands ≥1 change to doctrine, missions, briefs,
   references, or roadmap.
2. A non-obvious decision was made (carveout, deferral, choice between
   valid alternatives) that wouldn't survive in just the doc-diff.

The threshold is roughly the same as the execution repo: if rebuilding
context six months later from just the docs would lose meaningful
"why," write the log.

Pure mechanical doc edits (frontmatter fix, typo, link refresh) don't
need logs.

## Filename + frontmatter

```
session-logs/YYYY-MM-DD_topic-slug.md
```

```yaml
---
type: session_log
status: archived            # session logs are write-once snapshots
workstream: <tag> | null
tags: [doctrine-change, roadmap-update]   # optional
---
```

## What goes here vs. what goes in execution-repo session logs

| Decision class | Lives in |
|---|---|
| Architectural carveout that shapes future work | here (planning) |
| Doctrine v-bump or status change | here (planning) |
| Choice of which of N approaches to ship in code | execution repo |
| Class-of-bug discovery + new test discipline | execution repo |
| Mission/brief revision | here (planning) |
| PR-merge verification result | execution repo |
| Cascade decisions (what supersedes what) | here (planning) |

When in doubt: if the decision changes a doc *here*, the log lives here.
If it changes code *there*, the log lives there.
