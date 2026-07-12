---
type: mission
version: 5
status: canonical
last_verified: 2026-07-12
last_verified_against: e242074
supersedes: workstreams/subcontracts/mission.md@v4
workstream: subcontracts
tags: [workstream-mission, deterministic, no-ai, po-mirror, external-send-gate, section-50-legal-gate, section-51-subcontractor-sync, section-46-approval, editable-docx-output, code-actuation-gate, generation-built, send-half-unbuilt]
---

# ITS — Subcontracts Mission v5 (as-built)

**2026-07-12 — v5: as-built reconciliation to the DETERMINISTIC (NO-AI) subcontract-generation pipeline (exec HEAD `e242074`, documentation-reconciliation pass; ADR-0003, PO-mirror; SC-S1 foundation `3413b14` / SC-S3 render + poll pipeline; Exhibit A #538).** v5 supersedes v4's central premise. **v4 was wrong about the core mechanic:** it described *"field-fill of Exhibit A from Smartsheet job data + scope library + **AI-drafted scope-specific language**"* — a Claude-API scope-language generator held for legal review. The as-built has **NO AI in the generation path** (operator directive, 2026-07-10, matching the retirement of the Anthropic narrative core from `weekly_generate`). The generation half is **built + enrolled in the External Send Gate**; the **send half (SC-S4) is NOT built** — a remaining build dependency tracked as cutover **CL-38**, escalate-to-Seth. The full v4 text is retained verbatim under [Superseded design (v4)](#superseded-design-v4).

## 1. Mission

Generate Evergreen's subcontract **packages deterministically** from a structured subcontract record — no LLM step. A package (ADR-0003) is a **27-article fixed Subcontract Agreement body** + an **operator-authored, trade-templated Exhibit A (Scope of Work)** + an **Annex C Schedule of Values** + a **fixed Annex kit (C–K)** copied in verbatim. ITS does the deterministic ~95%: the header/party fields, the §2.1 Contract-Price WORDS derived from integer cents, the SOV, the governing-law clause derived from the job-site state, package assembly, and the correctness gates. The high-effort variable — **Article II "The Work"** inside Exhibit A — is **operator-authored from a versioned per-trade scope template** (the operator picks a trade → gets that trade's standard Article II as an editable starting point → edits it). AI-assisted Article II drafting is an **explicitly-parked future capability we do not lean on**.

The value ITS adds over the manual corpus: (a) the §2.1 price **words are derived from the same integer-cents figure** so words always equal figures — the corpus shipped a real "nine cents / $…00" mismatch; (b) **SOV-sums-to-price** + **price-words-equal-figure** correctness gates (re-derived at render time and re-asserted server-side against the signed price); (c) canonical entity strings kill the "BG Wing, LLC, LLC" / multi-form Prime-Contractor drift; (d) governing law **derived from the job-site state** rather than hard-coded Virginia. Every gate failure **fences the subcontract to the Review Queue — a wrong contract is never filed**.

## 2. Product Context

ITS is built with Evergreen Renewables as Customer 0 — the first deployment and design partner, receiving the system at no cost during validation. Solution Smith owns all IP and retains the right to fork the blueprint for additional construction and renewables customers; the blueprint is the reusable artifact, not a multi-tenant SaaS product. This workstream is the deterministic PO-mirror cousin of Purchase Orders & Materials — a bigger, wet-signature document with a per-state jurisdiction dimension.

## 3. Foundation Invariants Inherited

Per [Foundation Mission v11](../../doctrine/foundation-mission.md). The doctrine wins on any conflict.

### Invariant 1 — External Send Gate

Two-process, permanent. **Generation** (`subcontract_generate.py` — module header literally *"NO AI (operator directive)"*) performs zero external transmission and no LLM step; it is enrolled in `GATED_SCRIPTS` in `tests/test_capability_gating.py` (alongside `subcontract_docx.py` and the `subcontract_poll.py` daemon). **Send** (`subcontract_send.py`, SC-S4) will have zero AI step and belong to `SEND_SCRIPTS` — but **it does not yet exist**: only a commented stub remains in `tests/test_capability_gating.py` (`# ("subcontracts/subcontract_send.py", ["anthropic_client", "anthropic"])`). There is no automated external send in this workstream today; the generation pipeline **ships dark** (all `subcontract_poll` passes are `ITS_Config`-gated OFF by default).

**Send/execution approval is §46 workspace membership + F22, Mac-side — NOT a portal capability.** Approval authority resolves from the `ITS — Subcontracts`-tier workspace share list (the §46 mechanism the PO and Safety workstreams use), verified F22-style from cell history at send time. There is no portal cap that authorizes a send.

**Layered legal-review gate (§50).** On top of the send gate, the subcontract body renders on a live subcontract **only once its terms version is legally cleared**: `subcontracts/terms.py` loads immutable, sha256-pinned version files and enforces a **Layer-A gate** — a version renders only when `legal_review == "cleared"` (the config-editor "make this version current" path sets it). A **minted-but-un-cleared (`pending`) version RAISES**, the single choke point that fences a subcontract until the operator make-currents its body. This is the workstream's realization of the §50 privileged-actuation posture (the config editor is the actuator; the operator clears legal review).

### Invariant 2 — Adversarial Input Handling

All content outside the operating tenant is untrusted data. The subcontract Worker (`safety_portal/worker/subcontract.ts`) is **send-free** and treats the client as adversarial: it **recomputes all money server-side in integer cents** (`unit_price_cents` required on every SOV line; a client-displayed price is never trusted), asserts **SOV-sums-to-price**, writes the D1 mutation and its audit row as one atomic batch (the "W4" pattern), and **HMAC-signs the queued payload under a domain-separated `"sub:v1"` prefix** (`shared/portal_hmac.py`; distinct from the safety/portal domains). The Mac-side `subcontract_poll.py` **re-verifies the `sub:v1` HMAC** (constant-time) before rendering, and **re-asserts SOV-sums-to-signed-price**; a bad HMAC / SOV mismatch / numbering collision is a **permanent per-item fence** to the Review Queue (one-shot-flagged, no 120 s Review-Queue spam), never filed. The Worker's server-side extended-cents rounding (`Math.round`, half-up) must agree bit-for-bit with `money.py::_js_round` (copied verbatim) or the JS/Python HMAC recompute breaks — the docstring pins this and vitest locks it.

## 4. Architecture (as-built, deterministic PO-mirror)

Two-store data model mirroring Purchase Orders: **D1 authoritative for documents; Smartsheet mirrors.** For the party registry the polarity flips — **Smartsheet `ITS_Subcontractors` is the SoR, D1 caches** (§51). Two-process, ships dark.

- **Render core — `subcontracts/subcontract_generate.py`** (NO AI, capability-gated). The record → filled-body-text transform, in order: shape-validate the record → `money.sov_mismatches` **SOV-sums-to-price guard** (integer cents; §2.1 words + figure both derived from the *same* cents via `cents_to_words` / `format_figure`) → load Contractor identity config → load the body text via `terms.py` (sha-verified + the §50 Layer-A legal gate; a `pending` body RAISES) → build the body tokens including the num2words price clause and `governing_law.resolve(...)` (jurisdiction **derived from the job-site state** — 50 states + DC + the four commonwealths render "the Commonwealth of …"; an unknown state **fails closed / raises**, and Virginia keeps Evergreen's home Fairfax County venue per the corpus) → **strict** token substitution (an unfilled contract blank RAISES).
- **Document render — `subcontracts/subcontract_docx.py`** (NO AI, NO send). Emits **EDITABLE Office files, NOT flat PDF** (operator decision 2026-07-11 — the operator adjusts specific clauses / line values in Word before wet signature). `render_package()` returns **three files** keyed by filename: **`Subcontract.docx`** (the 27-article body, python-docx), **`Exhibit A.docx`** (the sha-pinned skeleton with the operator's / trade-fallback Article II filled in), and **`Annex C - Schedule of Values.xlsx`** (openpyxl). Byte-determinism is guaranteed by **`_normalize_ooxml_clock`**, which pins BOTH wall-clock sources in every OOXML zip (each member's local-header `date_time` and `docProps/core.xml`'s `<dcterms:created>`/`<dcterms:modified>`) to the agreement date, so a re-render of the same record is byte-identical (analogous to the PO PDF's reportlab CreationDate pin).
- **Exhibit A — `subcontracts/exhibit.py`** (#538). A git-versioned, sha256-pinned FIXED skeleton (`exhibit/manifest.json` → `skeleton.md`: Article I General + a `{{article_ii}}` marker + Articles III/IV/V/VI) plus a set of **per-trade Article II "The Work" bodies** (`art2/<key>.md`, each hash-verified on load). A subcontract's trade maps through `trade_map` to a template key (the three electrical trades share one `electrical` scope); the renderer fills `{{article_ii}}` with **the operator-authored body when present, else the trade fallback**. A wording change is a NEW file + manifest bump, never an edit.
- **Worker half — `safety_portal/worker/subcontract.ts`** (send-free). Draft / supersede / cancel + internal routes under a **new `requireSubToken` bearer tier** (`PORTAL_SUB_API_TOKEN` / Keychain `ITS_PORTAL_SUB_TOKEN`). Validates + recomputes money server-side (integer cents), writes the D1 mutation + audit row atomically, queues the subcontract **send-free in D1**, and HMAC-signs under `"sub:v1"`. The Mac daemon drains it.
- **Consumer — `subcontracts/subcontract_poll.py`** (launchd `org.solutionsmith.its.subcontract-poll`, **StartInterval 120 s** — staggered off `po_poll` 90 s / `portal_poll` 60 s; **every pass `ITS_Config`-gated OFF by default**). Four passes per cycle:
  1. **Drafts pass** (`subcontracts.subcontract_poll.polling_enabled`): `GET` pending → HMAC-verify (`sub:v1`) → **SOV re-assert vs signed price** → `Subcontract_Log` numbering-collision double-check → `ITS_Subcontractors` SoR snapshot → render the **three files** → **Box: three uploads** (§45 find-or-create ROOT→job→"Subcontracts"; §47 version-on-conflict) → `Subcontract_Log` append + `Subcontract_Pending_Review` row (+ best-effort inline attach of all three files) → **`mark-filed` receipt WITH `box_file_id` last** (idempotent; version-on-conflict + dedupe by key).
  2. **Subcontractor down-sync** (`.subcontractors_sync_enabled`): full `ITS_Subcontractors` → D1 mirror (§51).
  3. **Subcontractor up-sync** (same gate): D1 `subcontractors/pending` → Smartsheet (§51).
  4. **Status pass** (`.status_sync_enabled`): read `Subcontract_Pending_Review` approve/SENT state → `POST` status-sync (approved before sent, per the Worker's guarded batch) → mirror the stamps into `Subcontract_Log` (incl. an operator-set **`executed`** wet-signature flip mirrored into the D1 display state).
- **Registry grouping — group by STATE, not region** (§51; migration 0052). Subcontracts are jurisdiction-specific (governing law + lien-waiver annexes are per-state), so the subcontractor registry's grouping/filter dimension is the 2-letter USPS `state` (matching `governing_law_state`), replacing the coarse West/Midwest/East/National `region` the `po_vendors` cache uses. The §51 bidirectional sync carries `state` both ways.
- **Review surface — `subcontracts/subcontract_review.py`** is a **WSR schema twin** (a thin re-export of `safety_reports.wsr_review`): `Subcontract_Pending_Review`'s column titles + types are identical to `WSR_human_review`, so a future SC-S4 `SendConfig` binds the shared `weekly_send` + `send_poll_core` engine with no engine surgery (three protocol-titled slots carry subcontract semantics — "Job ID" ← Sub Key, "Week Of" ← agreement date, "Compiled PDF" ← the `Subcontract.docx` Box link). §42-documented as a re-export, not a clone.

**Migrations 0049–0052 are deploy-order-critical** (`0049_subcontractors`, `0050_subcontracts` + `sov_lines`, `0051_subcontracts_capability`, `0052_subcontractors_state`). `git pull ~/its` to latest main BEFORE any `wrangler d1 migrations apply`.

## 5. Decisions Locked (as-built)

Non-negotiable for the current phase unless explicitly revisited. Supersedes the v4 open-question set.

| Decision | Resolution (v5) |
|---|---|
| Scope-language generation | **Fully deterministic — NO AI.** (Operator directive 2026-07-10.) Article II "The Work" is operator-authored from a **versioned per-trade scope template**; AI-assisted drafting is explicitly parked. Supersedes v4's "AI-drafted scope-specific language." |
| Output format | **EDITABLE `.docx` / `.xlsx`, NOT flat PDF** (operator decision 2026-07-11) — the operator edits clauses / line values in Word before wet signature. `render_package` emits three files, byte-deterministic (`_normalize_ooxml_clock`). |
| Package composition | 27-article Subcontract body + Exhibit A (skeleton + operator/trade Article II) + Annex C SOV `.xlsx` + a **fixed Annex kit (C–K) copied in verbatim** (not re-authored per sub). Only two documents are authored. |
| Money model | **Integer cents, no floats, no tax/shipping.** §2.1 price words **derived from the cents figure** (words == figures). SOV-sums-to-price + price-words-equal-figure gates, re-derived at render + re-asserted vs signed price server-side. `_js_round` copied verbatim for JS/Py HMAC parity. |
| Legal-review gate | **§50 Layer-A gate in `terms.py`:** a subcontract body renders only when its sha-pinned terms version is `legal_review == "cleared"`; a `pending` version RAISES (fences to Review). Cleared via the config-editor make-current path. |
| Governing law | **Derived from the job-site state** (`governing_law.py`): 50 + DC + 4 commonwealths; Virginia keeps the corpus Fairfax County venue; a per-subcontract override wins; an unknown state **fails closed**. |
| Transport | **Send-free Worker D1 queue → Mac pull.** `safety_portal/worker/subcontract.ts` validates / recomputes money / signs (`sub:v1` HMAC) / queues under `requireSubToken`; `subcontract_poll.py` drains, re-verifies, renders, files. |
| Data model | PO-mirror two-store: **D1 authoritative for documents, Smartsheet mirrors**; party registry flips — **`ITS_Subcontractors` is SoR, D1 caches** (§51 bidirectional sync). |
| Registry grouping | **By STATE, not region** (migration 0052) — jurisdiction-specific. |
| Send/execution approval | **§46 workspace membership + F22, Mac-side.** No portal cap authorizes a send. Wet-signature `executed` state added after `sent`. |
| Send half | **SC-S4 NOT built** (`subcontract_send.py` absent; commented stub only). Generation is built + `GATED_SCRIPTS`-enrolled. Tracked as cutover **CL-38**, escalate-to-Seth. |

## 6. Scope

**In**
- Deterministic subcontract-package generation (Subcontract body + operator-authored/trade-templated Exhibit A + Annex C SOV), rendered as editable Office files.
- The §2.1 price-words derivation, SOV-sums-to-price + words-equal-figure correctness gates, canonical entity strings.
- Governing-law derivation from job-site state.
- The §50 Layer-A legal-review gate (sha-pinned terms versions).
- §51 bidirectional `ITS_Subcontractors` ↔ D1 subcontractor sync; status sync incl. wet-signature `executed`.
- Box filing (§45 find-or-create, §47 version-on-conflict), `Subcontract_Log`, `Subcontract_Pending_Review` staging.
- **Planned (SC-S4, not yet built):** `subcontract_send.py` + F22 verification + executed-countersign handling + the send-poller plist. §46 workspace membership = approval authority.

**Out**
- **AI-drafted scope language** — explicitly parked (operator directive); not a current capability.
- Annexes D/F/K/etc. re-authoring — the Annex kit is copied in verbatim.
- Subcontractor performance management, payment/AP processing, pre-qualification/vetting — separate or downstream.
- E-signature of the executed contract — out of scope (wet signature; the operator sets `executed`).

## 7. Build status (as-built)

| Slice | Scope | Status |
|---|---|---|
| SC-S1 — foundation | Migrations 0049–0051, the `subcontracts/` module frame, 4 Smartsheet builders, ADR-0003 | **Merged, ships dark** (#529, `3413b14`) |
| SC-S2 — config artifacts + actuator | Terms/scope-template config artifacts + a **workstream-aware** config actuator (high-capability-class) | Foundation landed; config wiring per the config-editor program |
| SC-S3a — render core | `subcontract_generate.py` (shape/SOV/§50-gate/governing-law/strict-fill) + `money.py` + `terms.py` + `governing_law.py` | **Built + `GATED_SCRIPTS`-enrolled, dark** |
| SC-S3b — document render | `subcontract_docx.py` (3 editable files, `_normalize_ooxml_clock`) + `exhibit.py` (#538 skeleton + per-trade Article II) | **Built, dark** |
| SC-S3c — Worker + daemon | `worker/subcontract.ts` (send-free, `sub:v1` HMAC, server-side money) + `subcontract_poll.py` (4 passes, 120 s launchd, all `ITS_Config`-gated OFF) + migration 0052 (state) | **Built, dark** |
| **SC-S4 — review + SEND** | `subcontract_send.py` + F22 + executed-countersign + send-poller plist; binds the shared `weekly_send` engine via the `subcontract_review` WSR-twin `SendConfig` | **NOT built** — commented stub only; **cutover CL-38, escalate-to-Seth** |

## 8. Current state and operator scope

The **generation half is built and enrolled in the External Send Gate**, ships **dark** (all `subcontract_poll` passes `ITS_Config`-gated OFF). The **send half (SC-S4) is unbuilt** — there is no `subcontract_send.py`, only a commented stub in `tests/test_capability_gating.py`.

**Operator scope decision (2026-07-12):** subcontracts is **FULLY IN the Aug-7 delivery scope, including SEND.** Because the generation half was completed pre-Aug-7 (ADR-0003 / SC-S1..S3) but the send half was not, **SC-S4 is now a remaining build dependency** — `subcontract_send.py` + F22 + executed-countersign + the send-poller plist — tracked as cutover item **CL-38** and **escalated to Seth as a separate SC-S4 build** (send is a high-capability-class category). Subcontract SEND enters the Aug-7 *send* scope only once SC-S4 ships + live-smokes. The Exhibit-A gap and any residual items are in `docs/tech_debt.md` (e.g. SC3c-3: the SOV `.xlsx` Box file id is discarded — forward-looking for SC-S4's dual-attach).

## 9. Cross-Workstream Impact

- **Purchase Orders & Materials.** Subcontracts is the deliberate **PO-mirror** (ADR-0003): reuses `form_pdf.merge_pdfs`, the parameterized `weekly_send` engine, `_js_round` / integer-cents, the `form_pdf` brand primitives, and the config-editor queue; parameterizes `numbering.py`, `vendors.py`→`subcontractors.py` (§51), `po_log.py`, and the `terms.py` loader. The one real "zero-route-changes" gap is making the Mac config actuator **workstream-aware** (SC-S2, high-capability-class).
- **Safety Portal / safety_reports.** Reuses the send-free-Worker-queue + Mac-pull transport shape, `shared/portal_hmac.py` (domain-separated `sub:v1`), and the `WSR_human_review` schema (via the `subcontract_review` twin binding the shared send engine at SC-S4).
- **Config editor (§50).** The subcontract terms library + scope templates are versioned config artifacts; "make current" clears the §50 Layer-A legal-review gate that `terms.py` enforces.
- **§46 / workspaces.** Send/execution approval = `ITS — Subcontracts`-tier workspace membership (a §23/§24 standalone-exception workspace), F22-verified Mac-side.

## 10. Success Criteria

- Every generated subcontract passes the SOV-sums-to-price + price-words-equal-figure gates; a failure fences to Review, never files a wrong contract.
- Zero subcontract rendered from an un-cleared (`pending`) terms version — the §50 Layer-A gate raises.
- Governing-law clause always resolves to a real jurisdiction (fail-closed on unknown state).
- Byte-deterministic re-render of the same record (OOXML clock pinned).
- **SC-S4 send criterion (pending build):** zero subcontract sent without both F22 approval (§46 workspace membership) and the send gate; wet-signature `executed` state tracked post-send.

## 11. Cross-references

- ADR-0003 — Subcontract generation workflow (deterministic, PO-mirror) — the canonical decision record (`~/its/docs/adr/0003-subcontract-generation-workflow.md`).
- [Foundation Mission v11](../../doctrine/foundation-mission.md) — Invariants 1 & 2 (two-process send gate, adversarial input).
- [Operational Standards](../../doctrine/operational-standards.md) — §14 preservation-over-refactor, §45/§47 Box filing, §46 workspace-membership approval, §50 code-actuation gate, §51 structured-SoR sync.
- [Purchase Orders & Materials](../purchase-orders/mission.md) — the mirrored workstream.
- [Safety Portal](../safety-portal/mission.md) — the send-free-Worker + Mac-pull transport pattern.

## Authority

ITS — Subcontracts Mission v5, 2026-07-12 canonical (documentation-reconciliation pass). Supersedes v4 (2026-05-13). Verified against exec HEAD **`e242074`** — every code-shape claim (`subcontract_generate.py` NO-AI header, `money.sov_mismatches` + `_js_round`, the `terms.py` §50 Layer-A `legal_review=='cleared'` gate, `governing_law.py` state derivation, `subcontract_docx.render_package`'s three editable files + `_normalize_ooxml_clock`, `exhibit.py` #538 skeleton + per-trade Article II, `worker/subcontract.ts` `requireSubToken` + `sub:v1` HMAC, `subcontract_poll.py`'s 120 s launchd + four gated passes, migration 0052 group-by-state, the `subcontract_review` WSR twin, `GATED_SCRIPTS` enrollment, and the **absent** `subcontract_send.py` with its commented stub) checked against live code. Both Foundation invariants inherited from [Foundation Mission v11](../../doctrine/foundation-mission.md).

**v6 trigger:** SC-S4 send half ships (would move the send half from "unbuilt / CL-38" to as-built and add `subcontract_send.py` to `SEND_SCRIPTS`); adoption of AI-assisted Article II drafting (currently parked); or a change to the deterministic / PO-mirror / §50-gate / §51-sync model.

---

## Superseded design (v4)

> **Retained for provenance only — NOT current.** The v4 body below described an **AI-drafted scope-language** generator and an RFQ-adjacent quote-drafting flow. Both are superseded: the as-built generation path has **NO AI** (operator directive 2026-07-10; §1, §5), and the six "Open Questions / Blockers" (editable source files, SOV format stability, template source-of-truth, etc.) are resolved by the ADR-0003 deterministic build (git-versioned sha-pinned templates, integer-cents SOV, `.docx`/`.xlsx` output). Do not treat anything below as a current decision.

*v4 | Productization framing + Foundation invariants applied | 2026-05-13*

### Mission (v4)

Automate Evergreen's subcontract drafting from project metadata and standard scope language. The high-effort, automation-eligible portion of every subcontract package is Exhibit A — Scope of Work, which is heavily project- and trade-specific. Boilerplate annexes (D, F, K) and the Subcontract Agreement body are static and attached verbatim. The mission is field-fill of Exhibit A from Smartsheet job data + scope library + AI-drafted scope-specific language.

This workstream also covers subcontractor quote drafting (when a sub needs a quote prepared), per the original project description — though no quote templates have yet been uploaded to the project.

### Foundation Invariants Inherited (v4)

**External Send Gate — implementation:** Subcontract_Pending_Review Smartsheet with Approved for Send (checkbox), Approved By, Approved At, Sent At, Send Status, Legal Review Status columns. Two-process model: subcontract_generate.py writes drafts (no send); subcontract_send.py reads approved rows (no AI). Subcontract send also requires Legal Review Status = APPROVED — belt-and-suspenders gating layered on top of External Send Gate.

**Adversarial Input Handling — implementation:** inbound executed-contract returns from subs (post-signature) treated as untrusted external content. Sender allowlist enforced. Untrusted-content tagging on any Anthropic extraction. Anomaly logging on extracted fields.

### Document structure identified (v4)

Each subcontract package consists of: Subcontract Agreement (boilerplate legal body, lightly parameterized); Exhibit A — Scope of Work (heavily project- and trade-specific; primary automation target); Annex C — Schedule of Values (simple price/scope breakdown); Annex D — Insurance Requirements ("CLEAN_9_30_24", static); Annex F — Lien Waivers (static, sub-filled at invoice time); Annex K — Exhibit K-1 Testing Protocols (static); and other annexes referenced but not all uploaded (B Schedule, G Sub-tier Vendors, H OSHA Competent Personnel, J Delivery Notice, L Commissioning Forms).

### Fillable fields identified for Exhibit A (v4)

Project full name; project short name; project address + coordinates; Owner LLC; subcontractor legal name; scope category; execution date; contract price; application-for-payment cutoff; pier refusal pricing line items.

### File-naming convention (v4)

`[year]_[job#]_[ProjectName]__[folder]__[document].pdf` — signal that Box filing structure can be predicted programmatically.

### Scope (v4)

**In:** Exhibit A generation from Smartsheet job data + scope library + AI-drafted scope language; Subcontract Agreement field-fill; annex assembly (D/F/K verbatim, C from SOV); subcontractor quote drafting; gated send via Subcontract_Pending_Review with both External Send Gate approval AND Legal Review Status; insurance certificate tracking (later phase); Box filing per naming convention.

**Out:** Annexes D/F/K unmodified; subcontractor performance management; payment processing; pre-qualification/vetting; Subcontractor Assignment / Owner-Lender Consent forms (open question).

### Open Questions / Blockers — LEFT INTACT (v4)

1. **Source-of-truth templates** — confirm the 99_Templates "TBD Project" masters are canonical. 2. **Editable source files** — only PDFs uploaded; need Word/Docx originals for python-docx field-filling (HARD BLOCKER). 3. **SOV (.xlsx) format stability** — only one Excel example; confirm column consistency. 4. **Quote workflow** — no quote templates present. 5. **Legal-language version** — is CLEAN_9_30_24 still current, and who owns updates? 6. **Subcontractor Assignment / Owner-Lender Consent** — in scope for drafting automation or handled separately?

*(All six are resolved / superseded by the ADR-0003 deterministic build; see the v5 body above.)*

### Architecture (v4)

Two-process model with extra gate: **Generation** — subcontract_generate.py produces draft package; writes to Subcontract_Pending_Review with Approved for Send = unchecked AND Legal Review Status = NOT_REVIEWED. **Legal review** — human counsel flips Legal Review Status to APPROVED or REJECTED. **Send** — subcontract_send.py only acts on rows with BOTH Approved for Send = checked AND Legal Review Status = APPROVED.

### Operating Principles (v4)

Every subcontract goes through legal review before signing (hard gate layered on External Send Gate); insurance gate is hard; AI-drafted scope language is reviewed in every case; static annexes attached verbatim; inbound executed-contract returns are untrusted content.

### What Changed in v4

Version bumped to reflect the 2026-05-13 cascade: two new Foundation invariants (External Send Gate, Adversarial Input Handling), product-framing correction (productized partnership with Evergreen as Customer 0), reliability language updated to production-quality framing, Takeoffs workstream removed.
