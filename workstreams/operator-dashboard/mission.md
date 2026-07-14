---
type: mission
version: 1
status: canonical
last_verified: 2026-07-12
last_verified_against: e242074 (documentation-reconciliation pass)
workstream: operator_dashboard
tags: [workstream-mission, ws2, operator-visibility, localhost-only, tailscale, pin-gated, config-editor, secret-rotation, internal-sor-write, code-actuation-gate, fail-closed, ships-dark]
---

# ITS — Operator Dashboard (WS2) — Mission v1

**2026-07-12 — v1 (as-built stub): the WS2 Operator Dashboard as it exists in code (exec `operator_dashboard/`, PRs #516 / #519 / #523).** A localhost-only operator control surface reconciled to the as-built system; a short stub pending a full mission pass.

## 1. Purpose

Give the operator **one screen** of ITS runtime health — and a **tightly-gated** surface to flip runtime config — without exposing anything to the public internet. It is a **local-first FastAPI app** (`python -m operator_dashboard`, bound to **`127.0.0.1:8484`**, reached from other devices only over **Tailscale**). It **observes the live `~/its` daemon tree** through the owning `shared/` modules and, on its one mutation route, **writes only `ITS_Config`**.

## 2. Two tiers (as-built)

- **Tier 1 — loginless READ (D1-1, PR #516).** Read-only observability panels: launchd status (`launchctl list`), watchdog Check-C markers, circuit breaker, daemon liveness heartbeats, state locks (passive non-mutating `fcntl` probe), recent log tail, and TTL-cached `ITS_Errors` / `ITS_Review_Queue`. Every panel route is **GET and fail-soft** — a missing file / dead read / failed import degrades that one card to "unavailable," the page never crashes. Every displayed value is redacted (`shared.redact`) + HTML-escaped.
- **Tier 2 — PIN-gated ACT surface (D1-2 PR #519, D1-3 PR #523).** Three privileged routes over a **fixed `(Setting, Workstream)` registry**:
  - **Class A** — `POST /act/config`: plain-PIN `ITS_Config` editor over the registry (per-key typed validators; non-editable rows refused: `external_send_gate`, `system.state`, `config_actuator`, `*.poll_interval_seconds`).
  - **Class B** — `POST /act/config/elevated`: **elevated-confirm** ceremony (re-enter PIN **and** type the exact target name) for identity / trust / send-poller-activation edits.
  - **Class C** — `POST /act/secret/rotate` (+ `POST /act/pin/change`, the operator-PIN change): **write-only** credential rotation, registry-bound (`registry.SECRETS`) — never reads a secret back, never logs a value; Box refresh token is guided-only; the operator-PIN change requires the CURRENT PIN + the new PIN entered twice, and a LOST PIN recovers only from the terminal.
  Every applied edit + escalation writes a `config_audit` row to `ITS_Errors`.

**Class C is Developer-Operator-only** (§44 *Developer-Operator credential self-service* rider, 2026-07-14): the "Tier 2" heading above names the app's ACT *layer*, not the §44 maintenance role — Class-A pause/tune is §44-Tier-2-eligible, but Class-C credential rotation is scoped to the **Developer-Operator** (gated by proof of the current credential; a Successor-Operator does not hold or rotate secrets). Later routes (D1-3b interval edit, Block-3 daemon control / breaker clear) are Class-B; see the exec runbook for the full route set.

## 3. Auth posture (as-built)

- **Operator PIN** from Keychain `ITS_OPERATOR_PIN`, compared **constant-time** (SHA-256 both sides → `hmac.compare_digest`), **FAIL-CLOSED** — a missing/locked keychain **denies**. Brute-force throttled: **5 fails / 60 s lockout → CRITICAL** (Class-A and elevated share one guess budget).
- **Origin/Referer allowlist** (`ITS_DASH_ALLOWED_ORIGINS` + localhost) is CSRF defense-in-depth on top of the PIN.

## 4. §50 relationship — writes `ITS_Config` only, never actuates code

The dashboard's only mutation is an **internal system-of-record write to `ITS_Config`** (§51), effective on the daemon's next cycle. It **never deploys or enqueues code** — the §50 privileged **code-actuation gate is the session-authed SPA's job**, applied by the `config_actuator` daemon on the Mac. The External Send Gate stays with the daemons (no `anthropic` / `graph_client.send_mail` / `resend` here).

## 5. Status & follow-ups (as-built)

- **Ships DARK.** The ACT surface is fail-closed until `ITS_OPERATOR_PIN` is provisioned; until then every write is denied.
- **Read-auth hardening** (a login rate-limit on the loginless read tier) is a **tracked follow-up**.
- **No launchd plist yet (D1-3b remaining)** — the dashboard is run manually; making it a daemon (plist install + interval-key edits) is the open work.

§43 runbooks: `docs/runbooks/operator_dashboard_config_editor.md`, `docs/runbooks/operator_dashboard_sensitive_tier.md`.
