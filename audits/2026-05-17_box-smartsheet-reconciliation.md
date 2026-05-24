---
type: audit
status: archived
last_verified: 2026-05-24
last_verified_against: 3b7d56d
workstream: null
tags: [forensic, schema-reconciliation]
---

ITS — Box ↔ Smartsheet Reconciliation v1

**ITS — Box ↔ Smartsheet Reconciliation v1**

*Generated 2026-05-17  •  New artifact  •  Companion to Handoff v3  •  Inputs: parse_job_v3.py + 10 active production Box projects (2026-05-16 corpus)*

# Purpose

Reconcile the current Smartsheet 12-sheet flat model (built for Customer 0 / Forefront-Luminace) against the structural reality of production Box folder trees as captured in parse_job_v3.py. This doc preserves the architectural findings and the 4 deferred questions so they can be addressed cleanly before Customer 2 onboarding.

*Status: ***deferred**. No structural changes to the Smartsheet model are recommended during the Forefront/Luminace migration. Resolve the architectural questions in this doc before applying ITS to a second customer.

# 1. What parse_job_v3 knows

parse_job_v3.py (alongside v1+v2) classifies Box folder trees into 8 schemas. The 4 active-side schemas — the ones that matter for ITS today — were derived from a 2026-05-16 deep-dive of 10 active production projects.

| **Schema** | **Example project** | **Top-level pattern** |
| --- | --- | --- |
| ACTIVE_PORTFOLIO_MODERN | KSI 4 IL, Forefront/Luminace, Steger & Roxbury, Kendall CSP 5, Keystone & Coast, Almon | 'N. Portfolio <Subject>' grid (12 canonical subjects) + sub-jobs at root |
| ACTIVE_MODERN | Oregon — Kendall (2023.126) | Same 12 canonical subjects, pre-Portfolio naming (e.g. '1. EPC' not '1. Portfolio Client Docs') |
| ACTIVE_DEVELOPMENT | Dolphin and Shoestring — Kendall | 8 dev-phase subjects (Corp Gov / GIS / Interconnection / Permit&Env / Prod&Offtake / Real Estate / Regulatory / Eng.) — NO EPC, NO Closeout |
| ACTIVE_SINGLE_PROJECT | Bonacci 1&2 (Generate) | Just 'A. Office' + 'B. Field' at root — no portfolio layer at all |

*Also recognized: 5 sub-job ID formats (*YYYY.NNN.X / NNN.X / YYYY-NNNN / a.lowercase / A1.upper+digit*), the R./S. dated-loose-file convention, and chaos patterns (pre-canonical 0., sub-decimal 1.5., z. ARCHIVE, **'** - Copy**'** suffix).*

# 2. Production corpus (10 projects, 2026-05-16)

Source: live Box top-level folder listings for the 10 active projects below. Folder structure files preserved as user uploads on 2026-05-17.

| **#** | **Project** | **Schema (detected)** |
| --- | --- | --- |
| P1 | 2025.201 KSI 4 IL | ACTIVE_PORTFOLIO_MODERN + chaos (0., A1.) |
| P2 | 2024.335 Forefront / Luminace  (Customer 0) | ACTIVE_PORTFOLIO_MODERN-hybrid (NNN.X sub-jobs) |
| P3 | 2023.126 Oregon — Kendall | ACTIVE_MODERN (pre-Portfolio) |
| P4 | 2025.358 Keystone & Coast | ACTIVE_PORTFOLIO_MODERN + chaos (0., 1.5.) |
| P5 | 2025.108 Bonacci 1&2 (Generate) | ACTIVE_SINGLE_PROJECT |
| P6 | 2025.364 Steger & Roxbury | ACTIVE_PORTFOLIO_MODERN + chaos (' - Copy') |
| P7 | 20171–20176 OR Portfolio (SPI) | ACTIVE_PORTFOLIO_MODERN (legacy YYYY-NNNN sub-jobs) |
| P12 | 2024.112 Almon / Lomaside / Perrydale / Hawthorne | ACTIVE_PORTFOLIO_MODERN-partial (lowercase sub-jobs) |
| P13 | 2025.112 Kendall CSP Portfolio 5 | ACTIVE_PORTFOLIO_MODERN + z. ARCHIVE chaos |
| P15 | 2025.127 Dolphin and Shoestring — Kendall | ACTIVE_DEVELOPMENT (8 dev-phase subjects) |

# 3. Canonical-subject prevalence across the 10 projects

Normalized presence of each canonical subject (✓ present at top level, · absent). 'Bonacci' (P5) is intentionally sparse — its ACTIVE_SINGLE_PROJECT schema has no portfolio subjects at all.

| **Canonical subject** | **P1** | **P2** | **P3** | **P4** | **P5** | **P6** | **P7** | **P12** | **P13** | **P15** | **N/10** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1. Client / EPC docs | ✓ | ✓ | ✓ | ✓ | · | ✓ | · | ✓ | ✓ | · | 8 |
| 2. Buyout | ✓ | ✓ | ✓ | ✓ | · | ✓ | ✓ | ✓ | ✓ | ✓ | 9 |
| 3. Schedules | ✓ | ✓ | ✓ | ✓ | · | ✓ | ✓ | ✓ | ✓ | ✓ | 9 |
| 4. Dev Docs | ✓ | · | ✓ | ✓ | · | ✓ | ✓ | ✓ | ✓ | ✓ | 8 |
| 5. Engineering Gen | ✓ | ✓ | ✓ | ✓ | · | ✓ | ✓ | ✓ | ✓ | · | 8 |
| 6. Correspondence | ✓ | ✓ | ✓ | ✓ | · | ✓ | ✓ | · | ✓ | ✓ | 8 |
| 7. Financials | ✓ | ✓ | ✓ | ✓ | · | ✓ | · | · | ✓ | ✓ | 7 |
| 8. Change Management | ✓ | ✓ | ✓ | ✓ | · | ✓ | ✓ | · | ✓ | ✓ | 8 |
| 9. Utility-Docs-Tracking | ✓ | ✓ | ✓ | ✓ | · | ✓ | ✓ | · | ✓ | · | 7 |
| 10. Submittal(s) Log(s) | ✓ | ✓ | ✓ | ✓ | · | ✓ | ✓ | · | · | · | 6 |
| 11. De-Comm Bonds | ✓ | · | · | ✓ | · | ✓ | · | · | ✓ | · | 4 |
| 12. Closeout (Portfolio) | ✓ | ✓ | ✓ | ✓ | · | ✓ | ✓ | ✓ | ✓ | · | 8 |
| Permitting (floating pos) | · | ✓ | ✓ | · | · | · | · | · | ✓ | · | 3 |
| Dev-only 8-subject set | · | · | · | · | · | · | · | · | · | ✓ | 1 |
| Bonacci A./B. only | · | · | · | · | ✓ | · | · | · | · | · | 1 |

*Read: subjects 2/3/5 are nearly universal in active-portfolio schemas; 4/6/7/8/12 are very common; Submittals + De-Comm Bonds are spottier; Permitting position drifts (sometimes #10, sometimes #11, sometimes embedded under Dev Docs).*

# 4. Smartsheet 12-sheet model ↔ Box canonical mapping

| **Smartsheet sheet** | **Box subject (when present)** | **Mapping** |
| --- | --- | --- |
| Schedule | N. (Portfolio) Schedules | 1:1 clean |
| Buyout — Subs | inside N. (Portfolio) Buyout (Subs subfolder) | 1:many — Smartsheet splits one Box folder into 3 sheets |
| Buyout — Materials | inside N. (Portfolio) Buyout | (same) |
| Buyout — Equipment | inside N. (Portfolio) Buyout | (same) |
| Financial Ledger | N. (Portfolio) Financials | 1:1 clean |
| Change Orders (PCO Log) | N. (Portfolio) Change Management | 1:1 clean |
| Closeout — Exhibit K-1 | inside N. PORTFOLIO CLOSEOUT (one exhibit among many) | many:1 — Smartsheet tracks just one exhibit |
| Submittal Log | N. Submittal(s) (Logs) | 1:1 clean |
| Permits & Inspections Log | N. Permitting OR inside Dev Docs | Floating position — sometimes #10/#11/inside #4 |
| Punchlist | (none) | Smartsheet-only workflow tracker |
| RFI Log | (none) | Smartsheet-only workflow tracker |
| Drawing Revisions Index | buried under 5. Engineering Gen/<various> | Floating depth — Box has it deep, not at top |

# 5. Gaps — Box subjects with NO Smartsheet representation

| **Box subject** | **Frequency** | **Worth a sheet?** |
| --- | --- | --- |
| 1. Client / EPC documents | 8/10 | Probably not — Box doc store, not a tracker |
| 4. Developer Documents / Dev Docs | 8/10 | Probably not — Box doc store |
| 5. Engineering Gen (parent) | 8/10 | Drawings sub-aspect already covered |
| 6. Correspondence | 8/10 | Maybe — a correspondence log would land emails + R./S. items |
| 9. Utility-Documents-Tracking | 7/10 | Probably yes — name says 'Tracking', looks like a tracker missing a sheet |
| 11. De-Comm Bonds | 4/10 (newer) | Maybe — financial obligation tracker |

# 6. Strategic finding

The current Smartsheet 12-sheet model is biased toward EPC-phase active construction trackers. It fits Forefront/Luminace (which IS an active EPC portfolio). It will need to flex for:

- **Development-phase customers (ACTIVE_DEVELOPMENT, e.g. Dolphin/Shoestring): **current Closeout K-1, Punchlist, Submittals, Permits, RFI, Drawings sheets would all be empty.

- **Single-project customers (ACTIVE_SINGLE_PROJECT, e.g. Bonacci): **no portfolio layer at all. The 12-sheet-per-project model doesn't map cleanly.

- **Pre-Portfolio legacy customers (ACTIVE_MODERN, e.g. Oregon-Kendall): **same sheets, different Box subject naming.

parse_job_v3 was built to detect these schemas. The Smartsheet structure currently has no awareness of schema. That's the core misalignment.

# 7. Architectural questions (4 — deferred)

## Q-A — Sheet set as fixed vs schema-aware

- **(a) Fixed 12 sheets per project. **Some sit empty for non-EPC projects. Simple, but ugly.

- **(b) Per-schema sheet sets. **12 for ACTIVE_PORTFOLIO_MODERN / ACTIVE_MODERN; 8-sheet dev set for ACTIVE_DEVELOPMENT; 2 sheets (Office/Field) for ACTIVE_SINGLE_PROJECT. parse_job_v3 already classifies.

- **(c) Defer. **Onboard Customer 2 first and diverge only if needed.

*Claude**'**s read: ***(c) for this session, (b) before Customer 2 onboarding.**

## Q-B — Three gap-fillers worth a real look

- **Utility-Documents-Tracking sheet **— name strongly suggests a tracker. 7/10 projects.

- **Correspondence Log sheet **— would give ITS automation a place to land emails and dated R./S. items (parse_job's parse_date_prefix() detects these).

- **De-Comm Bonds sheet **— financial obligation tracker. Newer projects only (4/10).

Add to the 12-sheet model now, defer, or skip entirely?

## Q-C — Subject-name normalization

Box subjects have meaningful name variations: 'Correspondence' / 'Portfolio Owner Correspond' / 'Portfolio Owner Contract and Correspond'. Should ITS internally normalize these to canonical labels (parse_job_v3 has the regex), and use canonical labels in Smartsheet sheet/folder naming for cross-customer consistency? Or preserve customer-specific naming?

## Q-D — Sub-jobs as Smartsheet projects (or as project + parent rollup)

Current pattern: Forefront's '335.1 BRIMFIELD-1' becomes Smartsheet project 'Brimfield 1'. This treats sub-jobs as flat top-level projects. But the parent (Forefront itself) has docs at the parent level ('1. EPC documents', '12. PVsyst Exh Y'). Should there be a PORTFOLIO-PARENT Smartsheet entity above the per-sub-job projects, holding parent-level rollups? Currently 02 — Portfolio Rollups is empty and was destined for Reports — should it also host a parent-level project sheet set?

# 8. Recommended path forward

- **Don****'****t change Smartsheet structure during Forefront migration. **The 12-sheet model works for an ACTIVE_PORTFOLIO_MODERN-hybrid customer.

- **Bank these findings (this doc) as the canonical Box ↔ Smartsheet reconciliation. **Customer 2 onboarding references it.

- **Address Q-A and Q-B explicitly before Customer 2 selection. **Q-A is structural; Q-B is incremental.

- **Q-C (name normalization) can be addressed at customer-onboarding time. **parse_job_v3 has the regex; add a normalize_subject_label() helper when needed.

- **Q-D (parent rollups) is contingent on whether Customer 2 has portfolio-parent docs that need tracking. **Forefront's 02 — Portfolio Rollups could prototype this; defer until concrete need.

# 9. Action triggers — when each question becomes urgent

| **Question** | **Becomes urgent when...** |
| --- | --- |
| Q-A — schema-aware sheet sets | A Customer 2 candidate is identified AND their schema is not ACTIVE_PORTFOLIO_MODERN. |
| Q-B — gap-filler sheets | Evergreen PMs request a tracker for Utility Docs, Correspondence, or De-Comm Bonds in the Forefront demo. |
| Q-C — name normalization | Customer 2 onboarding starts AND Customer 2's subject names diverge from Customer 0's. |
| Q-D — parent rollups | Forefront's portfolio-parent docs (e.g. EPC contract) need workflow tracking, or a Customer 2 candidate has a portfolio-parent layer. |

*End of reconciliation v1. To revise: bump version, preserve this doc, copy structure.*

Page  of