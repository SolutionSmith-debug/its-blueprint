# Archive — Retirement Registry

This directory is empty by design. It records what existed in the prior
.docx forest (Claude.ai project file attachments) before the 2026-05-24
big-bang migration to markdown, and what (if anything) superseded each
file.

## Why retired vs migrated

The big-bang migration kept docs that carried unique canonical content:
doctrine, missions/briefs, references, forensic audits. Everything else
fell into one of three buckets and is **not** in the new repo:

1. **Cascade Unification Updates (CUUs)** — meta-docs whose only job was
   reconciling drift between binary .docx versions. With version-controlled
   markdown + frontmatter + git log, CUUs serve no purpose: `git log
   doctrine/` IS the cascade narrative.
2. **Comprehensive Session Updates / Chat Syntheses** — end-of-session
   wrap-up docs whose content either (a) belongs in a session log, or
   (b) duplicates what's in the execution-repo's `docs/session_logs/`.
3. **Implementation Checklists, Errata, Resolution Batches** — point-in-time
   coordination docs. The work landed; the docs are stale by design.

Each entry below records the retirement decision so a future maintainer
can find the original if needed (Claude.ai project knowledge retains the
.docx attachments indefinitely).

## Retirement registry

### Cascade Unification Updates (5)

| File | Date | Retired because | Replaced by |
|---|---|---|---|
| `ITS_Cascade_Unification_Update_2026-05-19.docx` | 2026-05-19 | Reconciled v9.1 + v6.1 + others; absorbed | git log on `doctrine/` |
| `ITS_Cascade_Unification_Update_2026-05-20_ManagedAgents.docx` | 2026-05-20 | Managed-agents framing absorbed into FM v8 + Op Stds v11 + V&R v7.2 | `doctrine/foundation-mission.md`, `doctrine/operational-standards.md`, `doctrine/vision-and-roadmap.md` |
| `ITS_Cascade_Unification_Update_2026-05-20_Box_OAuth_Pivot.docx` | 2026-05-20 | Box OAuth pivot landed in PR #39; doc is point-in-time | execution repo PR #39 + `docs/session_logs/` |
| `ITS_Cascade_Unification_Update_2026-05-20_Alert_Dedupe_Ship.docx` | 2026-05-20 | Alert dedupe shipped PRs #42-#44; absorbed into Op Stds v11 §3 | `doctrine/operational-standards.md` |
| `ITS_Cascade_Unification_Update_2026-05-21_Picklist_Sync_Ship.docx` | 2026-05-21 | Picklist sync shipped PRs #45-#51; absorbed into Op Stds v11 §30 | `doctrine/operational-standards.md` |
| `ITS_Cascade_Unification_Update_2026-05-22_Security_Hardening.docx` | 2026-05-22 | Security hardening absorbed into FM v8 + Op Stds v11 §33/§34 | `doctrine/foundation-mission.md`, `doctrine/operational-standards.md` |

### Errata + Audit revisions (2)

| File | Date | Retired because | Replaced by |
|---|---|---|---|
| `ITS_Cascade_Audit_Errata_2026-05-19.docx` | 2026-05-19 | Errata on prior cascade; absorbed | git log |
| `ITS_Cascade_Audit_Errata_2026-05-22.docx` | 2026-05-22 | Errata on 05-22 cascade; absorbed | git log |

### Implementation checklists (2)

| File | Date | Retired because | Replaced by |
|---|---|---|---|
| `ITS_Cascade_Implementation_Checklist_v2_2026-05-19.docx` | 2026-05-19 | Implementation completed | execution repo history |
| `ITS_Cascade_Implementation_Checklist_2026-05-20.docx` | 2026-05-20 | Implementation completed | execution repo history |

### Session updates + comprehensive syntheses (5)

| File | Date | Retired because | Replaced by |
|---|---|---|---|
| `ITS_Session_Update_2026-05-19_20.docx` | 2026-05-19/20 | Session wrap; content in execution repo session logs | execution repo `docs/session_logs/` |
| `ITS_Session_Update_2026-05-20.docx` | 2026-05-20 | Session wrap | execution repo `docs/session_logs/` |
| `ITS_Comprehensive_Session_Update_2026-05-18_19.docx` | 2026-05-18/19 | Session wrap | execution repo `docs/session_logs/` |
| `ITS_Comprehensive_Session_Update_2026-05-21_EOD.docx` | 2026-05-21 | Session wrap; content absorbed into Memory Archive §G5 | `references/memory-archive.md` |
| `ITS_Comprehensive_Session_Update_2026-05-22_to_2026-05-24_EOC.docx` | 2026-05-22/24 | Session wrap | execution repo `docs/session_logs/` |
| `ITS_Comprehensive_Chat_Synthesis_2026-05-24.docx` | 2026-05-24 | Pre-migration synthesis; THIS migration is the response | this repo |

### Operational point-in-time docs (3)

| File | Date | Retired because | Replaced by |
|---|---|---|---|
| `ITS_Q4-Q8_Resolution_2026-05-21.docx` | 2026-05-21 | Q4-Q8 decisions absorbed into Op Stds v10.1 → v11 | `doctrine/operational-standards.md` |
| `ITS_Bradley1_DFR_Backfill_2026-05-21.docx` | 2026-05-21 | Bradley 1 demo seeding; operational task complete | Memory Archive §G4 |
| `ITS_Workstream_Mission_Brief_Pointer_Update_Batch_2026-05-17.docx` | 2026-05-17 | Pointer refresh; absorbed via missions/briefs migration | `workstreams/*/` |

### Already-markdown artifacts (1)

| File | Date | Disposition |
|---|---|---|
| `cluster_wrap_2026-05-23.md` | 2026-05-23 | Phase 1 cluster wrap; relevant content absorbed into Memory Archive + FSU v6.5. Not migrated as standalone. |

## Recovery path

If a retired doc's content turns out to be load-bearing for some future
question:

1. Find the original in Claude.ai project knowledge (file attachments
   retain indefinitely).
2. Extract the needed section.
3. Add it to the appropriate canonical doc here as a clarifying
   amendment, with a session log noting the recovery.

The retirement is not a deletion — the original .docx files persist in
the Claude.ai project. This registry just documents what's NOT in the
canonical markdown corpus.
