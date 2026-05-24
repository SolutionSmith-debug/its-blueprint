---
type: scaffold
name: forensic-audit
version: 1
audience: chat
usage_count: 1
---

# Forensic Audit

Walking the repo to verify documented state against actual state.
Used at major milestones (pre-handoff, post-cascade, suspected drift,
operator-requested validation).

## When to use

- Pre-handoff (Phase 1.5 California cutover, Customer 2 fork)
- After a large cascade event to verify absorption was complete
- When a doctrine doc's `last_verified` is more than 60 days stale
- Operator requests "audit" or "validate" or "verify what's actually there"

## Procedure

1. Clone the relevant repo(s) to a tmp path; read the actual code/docs
   (don't rely on memory or project knowledge alone — those go stale).
2. For each canonical claim in doctrine, find the corresponding evidence
   in the repo: test file, module, config row, PR, or commit SHA.
3. Note any drift: stale version references in code comments, dead
   code paths, broken cross-references, missing tests, undocumented
   behavior.
4. Categorize findings into three buckets:
   - **Blockers** — must fix before whatever motivated the audit
   - **Open with trigger** — track in tech_debt with a revisit condition
   - **Cosmetic** — note but don't queue work
5. Cross-check against lint baselines: frontmatter clean, cross-refs
   clean, mypy = 0, ruff clean, pytest green.
6. Produce a written summary with one-sentence headline verdict, a
   findings table, then ranked findings each with concrete file paths.

## Output format

```markdown
## Headline verdict

{One sentence: pass / pass with notes / fail with specifics}

## Dimensions

| Dimension | Result |
|---|---|
| {area} | {one-line summary} |
| {area} | {one-line summary} |

## Findings (ranked by impact)

### Blockers

1. {finding with file path and line numbers}

### Open with trigger

1. {finding} — revisit when {condition}

### Cosmetic

1. {finding}
```

## Anti-patterns

- DO NOT skip the actual clone-and-read step. "I think the repo has X"
  is worth nothing if X isn't actually there.
- DO NOT only report problems. Surface what's good too — it's the only
  way to calibrate the bar for next time.
- DO NOT mix blockers with cosmetic in the same list. Rank explicitly.
- DO NOT report findings without file paths. "There's drift somewhere
  in shared/" is unactionable.

## Why this works

The forensic discipline is the antidote to verify-before-fix drift.
Memory entry 5 (verify-before-fix discipline) extends to audit
authorship: don't write findings against memory state; write against
verified live state. The ranked output format forces explicit
priority calls and prevents the audit-fatigue trap of "many minor
things look like one big problem."
