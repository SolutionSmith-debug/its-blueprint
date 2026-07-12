---
type: mission
version: 5
status: canonical
last_verified: 2026-07-12
last_verified_against: e242074
workstream: purchase_orders
tags: [workstream-mission, deterministic-no-ai, external-send-gate, integer-cents-money-path, worker-parity-recompute, pull-transport, fieldops-sync-multipass, workspace-membership-approval, code-actuation-gate, vendor-sor, ships-dark]
---

# ITS — Purchase Orders & Materials Mission v5 (as-built)

**2026-07-12 — v5: as-built reconciliation. The workstream that shipped is the *opposite* of v4's RFQ framing.** WS1 of the Aug-7 delivery program landed as **`po_materials`** — a **deterministic, direct Purchase-Order-to-vendor** pipeline with **zero AI in any path** (every `anthropic` string in these modules is an AST-forbidden capability-gating *negation*, not a call). v4's entire subject — *drafting RFQs*, `rfq_generate.py` / `rfq_send.py`, Anthropic-based supplier-response extraction, and "Status: not started" — describes a design that was **never built** and is **deferred post-delivery**; it is retained verbatim under [Superseded design (v4)](#superseded-design-v4). The as-built pipeline is: `po_generate.py` (deterministic render + integer-cents assertion) → `po_poll.py` (the 90s multi-pass Mac daemon) → `po_send.py` / `po_send_poll.py` (the F22-gated send half) → `config_actuator.py` / `config_apply.py` (the §50 privileged config editor). Verified against exec HEAD **`e242074`** (documentation-reconciliation pass). Slices **S0–S8 COMPLETE + LIVE**; ships **dark** (every per-pass `polling_enabled` gate shipped `false`). Companion: the the Aug-7 delivery program (`~/its/docs/2026-07-09_aug7_delivery_program.md`) (PO slices S0–S8), ADR-0002 (the code-actuation actuator mirrors the Safety Portal's `publish_daemon`), and the blueprint info-gap doc / [memory-archive §G59](../../references/memory-archive.md) (RFQ deferral).

# 1. Purpose

Automate the generation, gated send, filing, and tracking of **finalized Purchase Orders to vendors** for Evergreen project materials — deterministically, from operator-authored line items and vendor-config artifacts, with **no model call anywhere in the pipeline**. A PO is a legal document with money on it; the design goal is that a wrong number is *structurally impossible to file silently* — the Mac re-derives every total on integer-cent basis and refuses (fences to the Review Queue) on any mismatch, rather than trusting the number that arrived.

This is a clean inversion of the v4 mission's framing. v4 assumed ITS would draft **RFQs** (request-for-quotes, multi-supplier, no pricing) and that awarded POs came back from suppliers "outside ITS." The as-built system does the opposite: **ITS generates the priced Purchase Order itself**, and the RFQ/supplier-quote surface is deferred.

# 2. Package and shape

The workstream lives in **`po_materials/`** (mirroring the `safety_reports/` shape). Its modules:

- **`po_generate.py`** — the DETERMINISTIC PO renderer + the Worker-matching integer-cents assertion. `totals_mismatches()` recomputes `lineExtendedCents` / `computeTotals` to **mirror `safety_portal/worker/po.ts` EXACTLY** (Python imports the same integer math the Worker runs at build time), diffs the recomputed totals against the **HMAC-signed D1 row**, and returns machine-readable **integer-only mismatch strings** — `[]` when clean. It **never raises**: a totals-basis failure (unknown tax mode, malformed field) is *returned* as a `totals_basis:` mismatch so the caller fences to the Review Queue rather than crashing. `render_po_pdf()` renders only rows that already passed `totals_mismatches`.
- **`po_poll.py`** — the 90s multi-pass Mac daemon (below).
- **`po_send.py`** + **`po_send_poll.py`** — the send half (below).
- **`config_actuator.py`** + **`config_apply.py`** — the §50 privileged config editor (below).
- Supporting modules: `numbering.py` (PO numbering), `po_naming.py` (filed-artifact names), `po_log.py` (`PO_Log` write), `po_review.py` (Review-Queue fences), `vendors.py` (`ITS_Vendors` upsert), `terms.py` (terms/purchaser resolution), and the config artifacts `config/purchaser.json`, `config/tax.json`, `terms/manifest.json` (+ per-vendor terms bodies).

# 3. Foundation Invariants Inherited

Per [Foundation Mission v11](../../doctrine/foundation-mission.md). This workstream touches **both** external-bound send (the PO email to the vendor) **and** external-content ingestion (every `/pending` row pulled from the Worker), so it inherits both invariants; doctrine wins on any conflict.

## Invariant 1 — External Send Gate (two-process, code-verified)

Generation and send are **separate, capability-gated modules**, verified at import by `tests/test_capability_gating.py`:

- **Generation / actuation (zero send capability):** `GATED_SCRIPTS` enrolls **`po_materials/po_poll.py`**, **`po_materials/po_generate.py`**, and **`po_materials/config_actuator.py`**. None may import `graph_client.send_mail`, Resend, `smtplib`, or `email.mime`. `po_poll` is customer-send-free (it renders, files, and mirrors state); `po_generate` is a pure deterministic renderer; `config_actuator` actuates *code* (commit/deploy) but performs zero external customer transmission.
- **Send (zero AI step):** `SEND_SCRIPTS` enrolls **`po_materials/po_send.py`** and **`po_materials/po_send_poll.py`**. Both are `anthropic` / `anthropic_client` AST-forbidden — the PO instantiation of the shared send engine. A successful prompt injection cannot cause an external send because there is no AI in the send process.

The kill switch and per-pass config gates are operator-convenience controls, **not** the security boundary — the two-process split is (FM Invariant 1; Op Stds v20 §1).

## Invariant 2 — Adversarial Input Handling

A Worker `/pending` row is **untrusted until proven**:

- **HMAC verify.** `po_poll` recomputes the canonical per-row HMAC (`shared.portal_hmac.verify_po`, constant-time) before any use; a bad-HMAC row is **one-shot-flagged** (CRITICAL + Review-Queue), never rendered, never `mark-filed`.
- **Money re-derived, never taken on faith.** The integer-cents recompute + diff (`totals_mismatches`, §2) is the Invariant-2 defense on the *number that appears on the legal document*: the Worker-side total is re-derived on the Mac and asserted; a mismatch is a **permanent per-row fence** to the Review Queue.
- **Integer-basis-point money path.** `config_apply` **rejects both `float` and `bool`** in the tax table (`rates_bp[state]` must be an `int` basis point in `0..MAX_BP`; a `9.0` is not an `int`) — no floats anywhere in the money path, matching the Worker's integer arithmetic.

# 4. Pipeline (as-built)

## 4.1 `po_poll.py` — the multi-pass Mac daemon

A single launchd daemon (**`org.solutionsmith.its.po-poll`**, `StartInterval` 90s, `RunAtLoad`), one host / one lock / one heartbeat, on the **`fieldops_sync` multi-pass model** — four passes, each behind its own `ITS_Config` gate, **all shipped `false`**:

1. **① Drafts pass** (`po_materials.po_poll.polling_enabled`): `GET /pending` → constant-time HMAC verify → `totals_mismatches` cents-assert → `po_generate` render → Box filing → `PO_Log` write → `POST mark-filed` receipt. A bad-HMAC or totals-mismatch row is one-shot-flagged (CRITICAL + Review-Queue) and skipped every subsequent cycle (no 90s spam).
2. **② Vendor down-sync pass** (`.vendors_sync_enabled`, §51): full `ITS_Vendors` projection → `POST vendors/sync` **full-replace** into the D1 vendor dropdown (the Worker's dirty-row fence protects it).
3. **③ Vendor up-sync pass** (same gate, §51): `GET vendors/pending` → per vendor, bridge-key find-or-create **into the `ITS_Vendors` SoR** (`vendors.upsert_vendor`, column-scoped).
4. **④ Status pass** (`.status_sync_enabled`): read `PO_Pending_Review` approve/SENT state → `POST status-sync` (approved-before-sent guard). D1 status is a **display cache only** — this pass *reports*, it does not authorize; F22 approval verification stays with the S5 send poller.

The **§51 vendor sync (passes ②③) ships dark.** Missing base URL / bearer / HMAC secret → **fail-closed**: no pass runs, CRITICAL fires. Per-item fences (bad HMAC, totals mismatch, collision, unknown vendor, `TermsError`, picklist, HTTP-400 validation) are permanent Review-Queue rows, never infinite re-pull.

## 4.2 `po_send.py` + `po_send_poll.py` — the send half

`po_send_poll.py` (15-min launchd **`org.solutionsmith.its.po-send`**) runs the **F22 approval-attestation gate on the driving checkbox** via `shared.approval_verification`, resolving the authorized-approver set from **membership of the `ITS — Purchase Orders` workspace** (`f22_workspace_id = sheet_ids.WORKSPACE_PURCHASE_ORDERS`; §46 — membership = PO approval authority, decision **D11** — never the Safety Portal's or Progress Reporting's workspace). It stamps the verified approver, then dispatches each approved row to `po_send.send_one_row`, which resolves recipients only from `ITS_Vendors` and calls the bound sender. The gate is **fail-CLOSED**:

- a circuit-open / auth error reading the approver set **propagates → the cycle aborts with zero sends**;
- an empty resolved set → `EMPTY_ALLOWLIST` → **all sends blocked** (the §46 share list of `ITS — Purchase Orders` must include the approvers);
- a disabled `po_materials.po_send.polling_enabled` short-circuits the cycle (operator pause).

The poller has zero send capability of its own; `po_send` has zero AI step (both AST-enforced, §3).

## 4.3 `config_actuator.py` + `config_apply.py` — the §50 privileged config editor

The **sole privileged config actuator** for PO config. The cloud Worker can only *validate + enqueue* a config-edit request (send-free AND code-free); the Mac **`config_actuator.py`** launchd daemon is the *only* process that **commits + deploys** the config — because the Worker imports `purchaser.json` / `tax.json` / `terms/manifest.json` at build time, a config change requires a full commit → CI → merge → local `wrangler` deploy → fast-forward the live `~/its` tree → post-deploy health check → stamp. It **performs zero external customer transmission and no LLM step** (in `GATED_SCRIPTS`). `config_apply.py` is the pure filesystem transform it wraps: it re-validates against live git HEAD and writes the config file(s), raising `ConfigApplyError` on any validation failure (no network, no Smartsheet, no git/deploy of its own). The editor is **generic over workstreams** (`worker/config.ts` `CONFIG_REGISTRY`) — terms / purchaser / tax today, subcontracts and beyond by registry entry. This is the Op Stds v20 **§50 privileged code-actuation gate**, ratified doctrine (v19, 2026-06-29); ADR-0002 records the pattern (mirroring the Safety Portal's `publish_daemon`).

The v4 open questions on **legal entity / ship-from** and **tax rate by job-site state** are resolved as-built into these config artifacts: `config/purchaser.json` (purchaser entity) and `config/tax.json` (integer-basis-point rate table), edited through the §50 path. PO numbering is owned by `numbering.py`.

# 5. Scope

**In (as-built):**

- Operator-authored PO line items pulled from the send-free Worker D1 queue (Python PULL transport).
- Deterministic priced-PO render with integer-cents Worker-parity assertion.
- Config-driven purchaser entity, per-state tax table, and per-vendor terms (the §50 editor).
- Gated send to the vendor via `PO_Pending_Review` (F22 = `ITS — Purchase Orders` workspace membership).
- Box filing of issued POs + `PO_Log` tracking.
- `ITS_Vendors` as the vendor system of record, with bidirectional D1↔Smartsheet sync (§51; ships dark).

**Out (deferred / not built):**

- **RFQ drafting** (multi-supplier, no-pricing request generation) — the entire v4 subject; deferred post-delivery.
- **Supplier-response / awarded-PO extraction** — the Anthropic-based inbound-quote parsing v4 described; deferred (no AI is in the shipped pipeline at all).
- Vendor invoice matching / full AP processing.
- Customer-side billing or pay applications.

# 6. Decisions Locked (as-built)

| Decision | Resolution (v5, as-built) |
|---|---|
| Package + framing | **`po_materials`**, a deterministic direct-PO pipeline. Supersedes v4's RFQ framing (`rfq_*` never built). |
| AI in the pipeline | **None, anywhere.** Every `anthropic` reference in these modules is an AST-forbidden capability-gating negation. |
| Money path | **Integer basis points only.** `config_apply` rejects `float` *and* `bool`; `po_generate.totals_mismatches` recomputes to mirror `safety_portal/worker/po.ts` exactly and fences on mismatch (never raises). |
| Transport | **Python PULL** (send-free Worker D1 queue → Mac `po_poll` drains `/pending`, HMAC-verifies, files, `mark-filed` receipt) — the same shape as the Safety Portal. |
| Daemon model | **`fieldops_sync` multi-pass** in one 90s `po-poll` daemon (drafts / vendor down-sync / vendor up-sync / status). All per-pass `polling_enabled` gates ship **`false`** (dark). |
| Send gate | **Two-process, F22 fail-CLOSED.** `po_send` / `po_send_poll` (15-min `po-send`); approver set = membership of the **`ITS — Purchase Orders`** workspace (§46, D11); `EMPTY_ALLOWLIST` blocks all; auth/circuit error → cycle aborts, zero sends. |
| Vendor SoR | **`ITS_Vendors`** (Smartsheet), synced to/from D1 (§51). Ships dark. |
| Config editing | **§50 sole privileged actuator** (`config_actuator` + `config_apply`): commit → CI → merge → local `wrangler` deploy; zero send, no LLM. Generic over workstreams (`CONFIG_REGISTRY`). |
| Approval-authority decision id | **D11** (workspace membership = approval authority). The terms model is **D6**. There is **no in-repo "decision D3"** governing RFQ deferral — the RFQ deferral is recorded only in the blueprint info-gap doc / memory-archive §G59. |

# 7. Phase status (as-built)

| Slice | Scope | Status |
|---|---|---|
| S0–S3 | Foundation: schemas, numbering, naming, `PO_Log`, terms/purchaser/tax config artifacts, Worker `po.ts` integer-cents math | **Landed + LIVE** |
| S4 | `po_generate` (deterministic render + `totals_mismatches` Worker-parity assertion) + `po_poll` (multi-pass Mac daemon, `org.solutionsmith.its.po-poll`) | **Landed + LIVE** — ships dark (per-pass gates `false`) |
| S5 | `po_send` + `po_send_poll` (F22 fail-CLOSED against `ITS — Purchase Orders`, `org.solutionsmith.its.po-send`) | **Landed + LIVE** — send-gated, dark |
| §50 config editor | `config_actuator` + `config_apply`; purchaser/tax/terms editing; fully-automatic C12=A actuation | **Landed + LIVE** (ADR-0002) |
| §51 vendor sync | `ITS_Vendors` ↔ D1 down/up-sync passes in `po_poll` | **Landed** — ships dark |
| S6–S8 | Deploy activation, live PO pipeline, pentest + stress, cutover enrollment | **COMPLETE** (see the Aug-7 delivery program) |

Activation is a visible per-pass `ITS_Config` cell-flip (each gate row is seeded `false`), gated behind the Evergreen production cutover.

# 8. Success criteria (as-built)

- **Zero PO sent without explicit human approval** (F22 fail-CLOSED; `EMPTY_ALLOWLIST` blocks all).
- **Zero PO filed or sent with a wrong total** — every PO's money is re-derived on the Mac on integer-cent basis and fenced to the Review Queue on any Worker-parity mismatch.
- **Zero AI in any PO path** (import-verified by `tests/test_capability_gating.py`).
- Issued POs filed at canonical Box paths + tracked in `PO_Log` without manual data entry.
- Config (purchaser / tax / terms) editable end-to-end through the §50 actuator with a fail-closed CI gate and no silent deploy.

# 9. Cross-workstream relationships

- **Safety Portal** — the source of the Python PULL transport pattern, the `publish_daemon` code-actuation pattern (ADR-0002 mirrors it), and the `worker/po.ts`↔Python integer-cents parity discipline. `po_poll` reuses the shared Box mirror-tree root owned by `safety_reports`.
- **Subcontracts** — the sibling deterministic document-generation workstream (ADR-0003) that slots into the same `CONFIG_REGISTRY` and reuses the PO scaffolding.
- **Email Triage** — the eventual home for any RFQ / supplier-response ingestion, *if* that deferred scope is ever built.

---

## Superseded design (v4)

> **Retained for provenance only. This describes a design that was NOT built.** v4 assumed the workstream would draft **RFQs** and call the Anthropic API to extract inbound supplier responses. The as-built system (§1–§8 above) is the opposite: a deterministic, zero-AI, direct-**Purchase-Order** pipeline. The RFQ + supplier-extraction scope is **deferred post-delivery** (recorded in the blueprint info-gap doc / memory-archive §G59; there is **no in-repo "decision D3"** governing it). Do not treat anything below as current.

**v4 Mission (superseded).** Automate the drafting of RFQs (request-for-quotes) to suppliers for Evergreen project materials. The output was framed as the request that initiates procurement — an RFQ sent to multiple suppliers — not a finalized or awarded PO. Awarded POs were assumed to come back from suppliers, filed and tracked but *not generated* by ITS. (As-built reality: ITS **generates the priced PO itself**; there is no RFQ stage.)

**v4 two-process architecture (superseded).** `rfq_generate.py` (calls the Anthropic API for scope language / free-form fields; writes drafts to an `RFQ_Pending_Review` sheet with `Approved for Send` unchecked) and `rfq_send.py` (no AI; reads approved rows and sends to the supplier list via Graph). Neither module exists; the as-built two-process split is `po_generate`/`po_poll` (generation, AST-forbidden send) vs `po_send`/`po_send_poll` (send, AST-forbidden AI), and the approval sheet is `PO_Pending_Review`.

**v4 adversarial-input framing (superseded).** Inbound supplier responses (quotes, awarded POs) were to be treated as untrusted content, wrapped in `<untrusted_content>` tags before **Anthropic API extraction**, with anomaly logging on extracted fields. The as-built pipeline makes **no model call at all**; its Invariant-2 surface is the HMAC-verified `/pending` row + the integer-cents re-derivation, not an LLM extraction.

**v4 open questions (superseded / partially resolved by config).** Materials-request intake mechanism; supplier database existence; RFQ template design; RFQ numbering line; tax/ship-to logic; vendor-specific T&C addenda; **legal entity + ship-from address** (E.S.S. LLC vs Evergreen Renewables LLC; STE 1030 vs STE 570 — v4 marked this a HARD BLOCK before any RFQ send). As-built, the legal-entity and per-state-tax questions are resolved into the §50 config artifacts (`config/purchaser.json`, `config/tax.json`); the RFQ-specific questions are moot until/unless the deferred RFQ scope is revived.

**v4 material classes + corpus notes (superseded, informational).** Two classes were identified — *standard POs* (`04_Purchase_Orders`) and *racking/module POs* (`06_Racking_Module_POs`, high-dollar, vendor-specific) — informed by `Purchase_Order_2019.docx` and the 14-page `ESS_Field_Purchase_Order_Terms_and_Conditions.docx`. The observed numbering convention was `YYYY.NNN.S.SEQ` (year.project.site.sequence), with a vendor-issued `IL-004` exception. These corpus observations informed the as-built `numbering.py` + terms artifacts but are no longer the governing design.

---

## Authority & Versioning

This is the canonical mission for the Purchase Orders & Materials sub-project — **v5 (as-built), 2026-07-12**, verified against exec HEAD **`e242074`**. It supersedes v4 (2026-05-13), whose entire RFQ-drafting + Anthropic-extraction design was never built and is folded above under [Superseded design (v4)](#superseded-design-v4). Where v4 conflicts with the as-built facts here, **the code wins**; where this mission and the planning-layer doctrine conflict, **the doctrine wins** ([Foundation Mission v11](../../doctrine/foundation-mission.md), [Operational Standards v20](../../doctrine/operational-standards.md)) — flag the inconsistency.

Cross-references:
- [Foundation Mission v11](../../doctrine/foundation-mission.md) — Invariants 1 & 2 (§3).
- [Operational Standards v20](../../doctrine/operational-standards.md) — §46 (workspace-membership approval), §50 (privileged code-actuation gate), §51 (ITS-owned structured-SoR write-back).
- the Aug-7 delivery program (`~/its/docs/2026-07-09_aug7_delivery_program.md`) — PO slices S0–S8.
- ADR-0002 (`../../../its/docs/adr/`) — the PO config actuator mirrors the Safety Portal `publish_daemon` code-actuation pattern.
- [Safety Portal mission](../safety-portal/mission.md) — the PULL-transport / code-actuation / integer-cents-parity source patterns.
- Blueprint info-gap doc + [memory-archive §G59](../../references/memory-archive.md) — the RFQ / supplier-extraction deferral.

v6 trigger: substantive scope change — a **revival of the deferred RFQ / supplier-quote-extraction scope** (would reintroduce an AI step and a new `<Workstream>_Pending_Review` surface), an authentication/transport swap away from the Python PULL model, activation of the §51 vendor sync as a governing (non-dark) behavior with a schema change, or doctrine movement on §50/§51 that reframes §4.3. Status-overlay updates absorb activation/deploy progress (per-pass gate flips) without a version bump.
