---
type: session_log
status: archived
workstream: safety_portal
tags: [pull-transport, clean-break, wpr-decommission, production-cutover, doctrine-bump, op-stds-v17, sixth-workspace]
---

# 2026-06-05 — Safety Portal transport pull-model + clean-break + Op Stds v17 (blueprint delta)

Chat-side delta on the [Safety Portal blueprint reconciliation](2026-06-05_safety-portal-blueprint-update.md) (earlier same day). Doctrine-authoring only — no execution code. Verified live against exec main before authoring (the repo advanced `0cff5f9` → `753f12f` / PR #171 mid-session — re-pinned to `753f12f`), per the brief's "verify live, don't trust SHAs" instruction.

## Verify-before-fix: what the brief claimed vs what's actually on main

The brief described the pull-model + clean-break as largely settled. Live verification found it **actively landing** (re-checked as the repo advanced to `753f12f`):

- **Landed:** PR #169 (`fc034eb`) — `/api/submit` HMAC-signs; bearer-gated `/api/internal/pending` (queue drain, `timingSafeEqual`, fail-closed 503) + `/api/internal/mark-filed` (receipt); the Python HMAC contract `shared/portal_hmac.py` + test (cross-language validated on `wrangler dev`). PR #168 (`ffad86b`) — `WSR_human_review` sheet + `sheet_ids` constants + PDF merge. **PR #171 (`753f12f`) — `intake_poll.py` retired/tombstoned** (raises `NotImplementedError`; the shared Graph infra explicitly preserved for Email Triage).
- **NOT built (in-flight Python rewire, not on main):** `portal_poll.py`; the `intake.py` portal-marker branch; the `weekly_generate`/`weekly_send` rewire onto `WSR_human_review`. The WPR→WSR decommission is **by-doc only** in code — the `weekly_*` scripts still reference `WPR_Pending_Review` until the rewire lands.

So the brief's "intake_poll removed" became true mid-session (PR #171); "process_message driven by portal_poll" remains in-flight. The blueprint encodes the **ratified decision** at doctrine level and records the **landed/in-flight boundary** precisely (memory-archive §G23.1).

## Deltas captured

1. **Transport = Python PULL model** (decision `decision_phase5-portal-transport`; mirrors exec §G22.3). The v2 email shim is **retired**. Worker = send-free durable D1 queue; Mac-side `portal_poll.py` drains `/api/internal/pending`, verifies the cross-language HMAC (`shared/portal_hmac.py`), files via the `intake.py` portal-marker branch, POSTs `/api/internal/mark-filed`. **Why:** a TS email shim transmits from the edge, *outside* the Python AST capability-gate (`tests/test_capability_gating.py`); the pull model keeps the Worker send-free and puts all transmission on the Python side, **inside** the gate — it closes the trust-boundary gap. And D1-store-then-pull has no silent-loss failure mode. External Send Gate: the Worker is send-free; the only external send is `weekly_send`. → `safety-portal/{mission §1/§4/§7/§9/§10, brief §1/§2/§8/§11/§12/§14/§15}`.

2. **Clean break — portal-only safety intake** (resolves last session's Flag #2). Evergreen cuts over all-at-once, no legacy-system integration. `intake_poll.py` → superseded by `portal_poll.py` for safety; `WPR_Pending_Review` → **decommissioned**, unified on `WSR_human_review`. **Scope boundary:** NOT an email teardown — `graph_client` / `untrusted_content` / `header_forgery` + `intake.py`'s Graph path are **preserved** for the committed Email Triage workstream. → `safety-portal/brief §8.1`; `safety-reports/mission v5.2` + `brief v6.2`; `email-triage/mission` inherited-infra note.

3. **Production-cutover DNS plan** (at cutover, not now). GoDaddy WordPress + Elementor; apex DNS + M365 on GoDaddy; **no Cloudflare account** (created fresh, Evergreen-owned, at cutover). Attach **only** `safety.evergreenrenewables.com` — likely **subdomain NS-delegation** at GoDaddy — leaving the apex + email untouched. Likely path, not locked. → `safety-portal/brief §11`; `info-gap §6`.

4. **DOCTRINE EDIT (operator-approved): Op Stds v16 → v17.** §23/§24 now acknowledge `ITS — Safety Portal` as a 6th, standalone, approval-gated workspace (workspace-membership = approval authority; self-contained; additive exception to the five-workspace audience-separation model, which is otherwise unchanged). Tag `operational-standards-v17`. **Clears the topology doctrine drift** the last-session §23/§24 flag raised — doctrine now matches the 6-workspace reality in the reference tables + `sheet_ids.py`.

## ⚑ Flags handed to the execution layer (out of scope here — exec-repo tasks)

1. **`ops-stds-enforcer` agent is pinned at Op Stds v13.** The v16→v17 bump **widens** that gap; the agent is blind to §23's 6th-workspace acknowledgement (and §43/§44). The agent-file update is an exec-repo task.
2. **`check_doctrine_drift` scan-scope** widening (so the drift check recognizes the topology acknowledgement) is exec-side.

## Version note

Per the operator's explicit "DELTA on mission/brief v2 — touch only the items below" framing, the Safety Portal mission/brief stay at **v2** (in-place refinement of a pre-deployment design; the email-shim was a v2 proposal corrected to the ratified pull model the same day, before anything is deployed). A dated changelog line in each records the transport+clean-break delta. The sibling `safety-reports` docs took status-overlay bumps (v5.1→v5.2, v6.1→v6.2). `doctrine/operational-standards.md` took a proper major bump (v16→v17) — a doctrine content change warrants it and the operator authorized it.

## Close

`scripts/lint_frontmatter.py` + `scripts/lint_crossrefs.py` clean. Committed to `main` and pushed to `origin/main`; tag `operational-standards-v17` pushed.

Cross-references:
- [Safety Portal mission v2](../workstreams/safety-portal/mission.md) · [brief v2](../workstreams/safety-portal/brief.md)
- [memory-archive §G22 (exec PRs) + §G23 (this blueprint delta)](../references/memory-archive.md)
- [Operational Standards v17 §23/§24](../doctrine/operational-standards.md#23-workspace-topology)
- [2026-06-05 Safety Portal blueprint reconciliation (earlier same day)](2026-06-05_safety-portal-blueprint-update.md)
- exec session log: `~/its/docs/session_logs/2026-06-05_safety-portal-phase4-runtime-renderer-phase5-foundation-transport.md`
