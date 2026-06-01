---
type: session_log
status: archived
workstream: null
tags: [doctrine, tier-1-self-heal, check-h-naming-artifact, check-c-marker-floor, status-absorption, provenance-preserved, uptimerobot-f16]
---

# 2026-06-01 — Correct Tier-1 self-heal characterization (Check-H → Check C marker-file floor)

Part A of the Tier-1 self-heal brief. Landed as PR #34 (merge `275e664`).
Companion to exec `its`#133 (Part B — the watchdog Check I catch-up that
implements the one residual this correction names).

## Purpose

The doctrine described Tier-1 self-heal as a separate, **unimplemented "Check
H" heartbeat-staleness** watchdog check (reading ITS_Daemon_Health, 2 ×
Interval) with "2 of 3 daemons heartbeat-pending / only `intake_poll` writes a
heartbeat." Verified against exec `585823d`, that framing is **inaccurate on
both axes** and is corrected here. This was a co-resolved status correction (the
brief carried Seth's decision); CC implemented.

## Pre-flight findings (the verified-true model)

A 9-agent validation workflow checked every code-shape claim against live exec
HEAD before editing:

1. **"Check H" was never built — it is a naming artifact.** The implemented
   staleness floor is the marker-file **Check C** (`scripts/watchdog.py`):
   `TRACKED_JOBS` already covers ALL FOUR daemons (`safety_intake`,
   `safety_weekly_send_poll`, `safety_weekly_generate`, `safety_picklist_audit`)
   with per-job freshness windows. The "2-of-3 heartbeat-pending" gap is closed.
2. **The external dead-man's-switch ping (audit F16) is live** in
   `watchdog.main()`. Vendor is **UptimeRobot** (F16's title) — the brief said
   "Healthchecks.io", which appears nowhere in the blueprint; corrected.
3. **Lone honest residual:** `weekly_generate` runs on `StartCalendarInterval`
   (Friday 14:00), so a *crashed* Friday cycle is detected by Check C but not
   auto-recovered by launchd until next Friday. The exec follow-on (Check I,
   `its`#133) closes it — after which V&R Pre-Cutover Condition 4 is MET.
4. **The "every Enabled daemon emits a heartbeat" gate criterion was
   mis-specified** — the watchdog is deliberately NOT self-tracked (a daemon
   can't detect its own death); its liveness is the F16 ping, by design.
   Corrected the gate's wording.

## Code/doc changes

Five doctrine files + one reference + one workstream brief:
- `doctrine/{foundation-mission,operational-standards,vision-and-roadmap,handover-plan,excellence-roadmap}.md`
- `references/worktree-discipline.md` (Check-H cross-ref)
- `workstreams/safety-reports/brief.md` (risk row; + stale `Op Stds v11 §2` → `v16 §2`)

The gate **scope** is unchanged everywhere — Tier-1 self-heal stays a real
pre-cutover gate; only the stale *status text* is corrected.

## Decisions made during execution

1. **Bump level — all STATUS-absorbing, no major bump, no new tags.** This is a
   status correction of an unchanged mechanism, not a framing/principle change.
   Per each doc's own forward trigger:
   - FM v11.x (trigger: "v11.x absorbs … Tier-1 self-heal completion")
   - Op Stds v16.x (trigger: "v16.x absorbs further status updates")
   - V&R v9.x (trigger: "v9.x absorbs further status updates")
   - Handover v8.x (trigger: status updates absorbed w/o major bump)
   - Excellence Roadmap in-place at v4 (G7: no minor overlay; frontmatter/title stay equal)

   Frontmatter `version` integers unchanged; the correction is body text + a
   provenance note in each authority/changelog block.
2. **Provenance preserved, not blind-deleted.** Each doc's authority block
   records the prior "Check H" framing as corrected (per the brief's discipline,
   matching the de-1b cascade). `session-logs/` and `audits/` left untouched
   (historical — correctly recorded state-at-the-time).
3. **references/ scope.** Included the trivial, clearly-stale
   `worktree-discipline.md` cross-ref (same correction); **deferred**
   `references/daemon-health-schema.md:174-175` ("retrofit to write heartbeat"
   for watchdog/picklist_sync) to a separate references-pass — safely editing a
   schema-roster doc needs its full context. Flagged in the PR.

## Verification

- lint_frontmatter: clean (72 files)
- lint_crossrefs: clean (72 files)
- ruff / mypy / pytest: N/A (markdown-only repo)
- main-branch CI on merge commit: SUCCESS (lint)

## Out-of-scope notes

- `references/daemon-health-schema.md:174-175` references-pass (above).
- Exec-side `CLAUDE.md` carried the same stale "Check H" maintenance-model
  line (via #132) — reconciled in the exec Part B PR (`its`#133), not here.

## Sequencing context

Part-A-first ordering honored: this doctrine correction merged (#34, 18:52Z)
before the exec Part B (#133, 18:57Z), so the doctrine was accurate before the
code that implements its residual landed.

## Merge verification quartet output

```
state:        MERGED
mergedAt:     2026-06-01T18:52:30Z
mergeCommit:  275e664815c45a4a851cb8c4fa2a149097fed888
main-CI:      SUCCESS (lint on 275e664)
```
