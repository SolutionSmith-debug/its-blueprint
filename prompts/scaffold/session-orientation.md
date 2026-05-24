---
type: scaffold
name: session-orientation
version: 1
audience: chat
usage_count: 0
---

# Session Orientation

What chat loads at the start of a fresh session to come up to speed on
ITS without burning tokens on stale or irrelevant context.

## When to use

- First message of a new chat session
- After memory compaction
- When the operator references "the project" without recent context loaded

## Load order

1. **Memory** — auto-loaded by Claude. Carries the 30 entries codifying
   doctrine pointers, invariants, conventions.
2. **Top-level orientation** — `README.md` and `CLAUDE.md` from
   its-blueprint (in project knowledge). Establishes the two-layer
   model.
3. **Doctrine** — load in this order: `foundation-mission.md`,
   `operational-standards.md`, `vision-and-roadmap.md`. The
   non-negotiables and the current operational rules and the phasing
   context.
4. **Status snapshot** — `references/foundation-scaffold.md`. What's
   done in the execution repo.
5. **Then** load anything specific the operator's first message implies.

## What NOT to pre-load

- Workstream missions/briefs unless the operator names a workstream
- Memory archive unless restoration is needed
- Audits unless investigating drift
- Session logs unless asked about prior decisions
- Doctrine docs beyond the three foundational ones

Pre-loading too much burns context budget that's better spent on the
actual task.

## Template (chat's first response shape)

```
{Optional one-line acknowledgment of session start}

{Direct answer to the operator's question, with cross-references to
doctrine docs by stable anchor path}
```

Don't announce "Loaded canonical state from..." — it's preamble that
operator doesn't need. Just answer with awareness of current canonical
state.

## Why this works

Anchors the session in current canonical doctrine before answering.
Avoids the "Claude responds from stale memory" failure mode. The
"don't pre-load" list is as important as the load order — premature
loading burns context budget.
