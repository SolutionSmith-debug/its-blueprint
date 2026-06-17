---
type: brief
version: 1
status: draft
last_verified: 2026-06-16
last_verified_against: SolutionSmith-debug/its@fb15881
workstream: urs_marine_portal
tags: [workstream-brief, cc-brief, urs-marine, adapter-seam, hmac, pull-transport, host-agnostic, two-process]
---

# CC Brief B3 — Name the adapter seam + host-agnostic transport skeleton (in `its-portal-template`)

> **You start with no context.** DIRECTION + INCLUSION below. Pinned to `its@fb15881`; **run
> `brief-validator` first** — re-confirm the internal-endpoint surface and the canonical HMAC
> payload against current HEAD before writing. This brief touches the outbound path and inbound
> ingestion, so **paste `prompts/snippets/invariant-restatement.md` into the brief's output and the
> module docstrings.**

## Cold-start context

**Where you are.** A session in `~/its-portal-template` (created by B1). The Worker is already
**adapter-unaware** — it exposes only the bearer-gated `/api/internal/*` contract; it never imports
a PM-tool client. Your job is to *name* that boundary and add a host-agnostic skeleton that
consumes it. `~/its` (the Evergreen source of the proven Python pull pattern) and `~/its-blueprint`
are siblings.

**DIRECTION.**
- `~/its-portal-template/worker/index.ts` — the three internal endpoints (re-read; do not assume
  shapes): `GET /api/internal/pending` (drain), `POST /api/internal/mark-filed` (receipt), `POST
  /api/internal/sync` (job-set replace). Bearer-gated.
- The proven host pattern to port (read, then re-implement minimally — do not copy Evergreen's full
  pipeline): `~/its/safety_reports/portal_poll.py` (60s launchd, fresh-process-per-cycle),
  `~/its/shared/portal_hmac.py` (constant-time verify), `~/its/shared/portal_client.py` (endpoint
  client shapes), `~/its/scripts/launchd/` (plist templates).
- `~/its-blueprint/doctrine/foundation-mission.md` §Invariant 1 (the outbound push is a "send") +
  §Invariant 2 (the inbound job-set is untrusted).

**INCLUSION — engagement decisions.**
- **Canonical HMAC payload (do not alter):** `submission_uuid \n job_id \n form_code \n work_date \n
  payload_json`. The host recomputes + verifies (constant-time) **before** the adapter touches a
  row; a row whose HMAC does not verify is rejected + one-shot-flagged, **never filed, never
  mark-filed** (downgrade defense).
- **Host-agnostic by design (decision #4):** the transport (pull + HMAC) and the adapter interface
  carry **no host assumption** — the same modules run under launchd (Mac mini / Solution-Smith-
  hosted) *or* a GitHub Actions step. Do not bake in a host.
- **Scope = the SEAM, not a real adapter.** Ship the named protocol + the transport client + a
  pluggable `Adapter` interface + a **no-op reference adapter**. The Smartsheet adapter stays in
  Evergreen; the **Monday adapter is a URS-fork follow-on** (B6). The template must run end-to-end
  against the no-op adapter (D1 is the SoR — nothing downstream is required for the portal to work).
- **Language ⟫OVERRIDE:** Python, in a small self-contained `adapter_host/` package (B1 dropped
  Evergreen's `shared/` + `pyproject.toml`; this re-introduces a minimal, dependency-light host —
  reusing the proven constant-time `portal_hmac` + the fresh-process launchd pattern, structured so
  a GH Actions runner can import the same modules). (Alternative: a TS Worker-side cron — rejected
  for now; it would put transmission back at the edge, outside the two-process boundary.)

## Goal

A named, documented PM-adapter seam that makes Monday a drop-in sibling of Smartsheet, with a
host-agnostic transport skeleton and a runnable no-op adapter.

## PR-1 — The named protocol (doc) + the transport client

- `docs/pm-adapter-protocol.md`: specify the three-endpoint contract as the **PM Adapter Protocol** —
  request/response shapes, the bearer-token gate, the canonical HMAC payload + constant-time verify,
  the receipt fields (`box_verified`/`filed_at`/`box_link`/`box_file_id`), and the **two-process
  boundary** (the host files deterministically; no AI/reasoning step in the drain-and-file path —
  any future AI enrichment is a separate process, per Invariant 1).
- `adapter_host/transport.py`: a pure transport client — `pull_pending()`, `mark_filed(receipt)`,
  `sync(job_set)` — plus `verify_hmac(row)` (constant-time; port from `portal_hmac.py`). No PM-tool
  knowledge, no host assumption.

## PR-2 — The pluggable `Adapter` interface + no-op reference adapter

- `adapter_host/adapter.py`: define `class Adapter(Protocol)` with the method set —
  `file_submission(submission) -> Receipt` (deterministic; returns the receipt fields) and
  `sync_jobs(jobs) -> None` (optional; for PM tools that source the job set). Document that
  `file_submission` must be side-effect-deterministic and AI-free.
- `adapter_host/noop_adapter.py`: a reference `NoopAdapter` that satisfies the interface (logs the
  submission, returns a synthetic receipt) so the seam is runnable with no PM tool.

## PR-3 — The host runner skeleton (host-agnostic)

- `adapter_host/run_once.py`: one cycle — `verify_hmac` each pending row → on pass hand to the
  configured `Adapter.file_submission` → `mark_filed`; bad-HMAC rows are one-shot-flagged, never
  filed. Optionally call `Adapter.sync_jobs` → `transport.sync`. The runner reads which adapter +
  the Worker base URL + the bearer token from config/Keychain (no hardcoded host).
- `scripts/launchd/portal-adapter.plist.template`: fresh-process-per-cycle (port the Evergreen
  pattern). Add a one-paragraph note in `docs/pm-adapter-protocol.md` that the same `run_once.py`
  is the entrypoint a GitHub Actions scheduled job would invoke — **the host is interchangeable.**

> **Reconciliation note for the fork (record, don't implement here):** in Evergreen, `/api/internal/
> sync` PULLS jobs from Smartsheet *into* D1 (D1 mirrors). In URS, **D1 is the jobs SoR** (fed from
> contracts), so `sync` is likely unused for jobs there — URS writes jobs directly. The seam keeps
> `sync` generic; whether URS uses it is a B4 decision.

## PR-4 — Tests

`test/` (Python): constant-time HMAC verify; tamper → reject + flag (never filed, never mark-filed);
the drain loop hands each verified row to the adapter exactly once; `mark_filed` posted on success;
the `NoopAdapter` satisfies the `Adapter` Protocol. Reviewed by `portal-worker-security-reviewer`
(the HMAC/bearer boundary + the two-process discipline) + `ops-stds-enforcer` (Send Gate,
preservation).

## Definition of done

- The three endpoints are documented as a named protocol; a no-op adapter runs the full
  drain→file→receipt loop against local D1; HMAC failure is fail-closed + flagged.
- No host assumption baked into transport or adapter; the launchd plist is a template, and the GH
  Actions path is documented as a drop-in.
- Monday is now an "implement this interface" task, not a core change.
- **§43 note** (symptom: submissions stuck in the queue; low-class repair: re-run `run_once.py`,
  check the bearer token / Worker base URL config; escalate-to-Seth: any HMAC/transport *code* edit
  is high-class).
- Squash; linear; propose-only.
