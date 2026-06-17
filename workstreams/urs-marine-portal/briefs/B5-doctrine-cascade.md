---
type: brief
version: 1
status: draft
last_verified: 2026-06-16
last_verified_against: SolutionSmith-debug/its@fb15881
workstream: urs_marine_portal
tags: [workstream-brief, cc-brief, urs-marine, doctrine-cascade, fork-model, propose-only]
---

# CC Brief B5 — Doctrine cascade: record the portal-template fork-model amendment

> **Small, markdown-only, parallelizable** (runs alongside B1 per the build sequence). This brief
> edits **doctrine**, so it is behind the `block-doctrine-write` guard: a home-rooted or
> non-blueprint session must produce a **proposal/diff only** and hand it to a guarded
> blueprint-rooted session (or the Developer-Operator) to land. Doctrine bumps require the symmetric
> Authority-block + companion cross-ref update (four-lens adversarial diff review; `lint_frontmatter.py`
> does not catch asymmetry).

## Cold-start context

**Where you are.** A blueprint-rooted session in `~/its-blueprint` (for the landing step). The
amendment is decided; this brief only records it in doctrine.

**DIRECTION.**
- `doctrine/excellence-roadmap.md` — the target doc (quality bar + tooling stack + fork model).
- `doctrine/foundation-mission.md` + `doctrine/operational-standards.md` — companion docs whose
  cross-refs may need the symmetric update if the fork-model statement is cited there.
- `workstreams/urs-marine-portal/mission.md` §11 decisions 1–2 — the ratified source of the
  amendment.

**INCLUSION — the amendment (decided in the kickoff engagement).**
- **Fork model amendment:** customers fork from **blueprint + `its-portal-template`** (the platform
  substrate), *not* from a strip of Customer 0's full `its` execution repo. The portal-template is
  the platform fork-source; per-customer execution repos (`its-<customer>`) fork from it. This
  amends any prior "fork the execution repo" framing.
- This is the **only** doctrine change in the URS workstream. The three-tier successor/maintenance
  model and the two invariants are already current doctrine (FM v11) — do **not** re-bump them.

## Goal

`doctrine/excellence-roadmap.md` records the portal-template fork model as the canonical
customer-onboarding path, with the version + Authority block bumped symmetrically and every
companion cross-ref updated in the same PR.

## Steps

1. Add (or extend) the fork-model section of `excellence-roadmap.md`: portal-template = platform
   fork-source; blueprint stays one artifact (no per-customer blueprint forks — already stated in
   the blueprint `CLAUDE.md`); per-customer `its-<customer>` execution repos fork from the template.
2. Bump the doc version + `last_verified` + Authority block; update the doctrine manifest
   (`../its/docs/doctrine_manifest.yaml`) if the version is tracked there.
3. Symmetric companion update: if `foundation-mission.md` / `operational-standards.md` cross-ref the
   fork model, update those references in the same PR (the lint won't catch asymmetry — do the
   four-lens diff review).
4. Run `python scripts/lint_frontmatter.py` + `python scripts/lint_crossrefs.py`; run
   `scripts/check_doctrine_drift.py` / `doc-reconciliation-auditor` if present.

## Definition of done

- The fork model is canonical doctrine; version/Authority/`last_verified` bumped symmetrically;
  companion cross-refs consistent; linters + drift check green.
- Landed by a guarded blueprint session (the `block-doctrine-write` guard fires); a home-rooted
  session stops at the proposal and does not write `doctrine/`.
- Squash; linear.
