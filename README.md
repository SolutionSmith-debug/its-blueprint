# ITS Blueprint

Planning layer for ITS — Integrated Technical System. This repo holds the
canonical doctrine, workstream missions/briefs, references, and audits
that drive the **execution-layer** implementation in
[`SolutionSmith-debug/its`](https://github.com/SolutionSmith-debug/its).

This is a **white-glove custom-development practice**. Each customer
receives a fork of the execution-layer repo; the blueprint here is the
reusable artifact, not a multi-tenant product. Evergreen Renewables is
Customer 0.

## Two-layer architecture

| Layer | Repo | Contains |
|-------|------|----------|
| **Planning** | this repo (`its-blueprint`) | Doctrine, missions, briefs, references, audits. Markdown, version-controlled, lint-enforced. |
| **Execution** | `SolutionSmith-debug/its` | Customer-0-specific Python implementation. Reads decisions made here. |

If a doc here contradicts the execution-layer code, this repo wins.
Flag the inconsistency in the relevant doc's frontmatter (`status:
draft`) until reconciled.

## Directory layout

- [`doctrine/`](doctrine/) — non-negotiable invariants. Foundation
  Mission, Operational Standards, Vision & Roadmap, Handover Plan,
  Excellence Roadmap.
- [`workstreams/`](workstreams/) — per-workstream mission + brief pairs.
  One subdirectory per workstream.
- [`references/`](references/) — evergreen explanatory docs (memory
  archive, project organization, schema specs, handoff packets).
- [`audits/`](audits/) — time-bound forensic snapshots against a closed
  scope.
- [`session-logs/`](session-logs/) — chat-side session logs (the
  execution repo has its own `docs/session_logs/`).
- [`archive/`](archive/) — retired-doc registry. Retired docs are NOT
  in-tree; `archive/README.md` lists what existed pre-migration and
  what superseded each.
- [`scripts/`](scripts/) — linters for frontmatter, cross-references,
  workstream taxonomy.
- [`.github/workflows/`](.github/workflows/) — CI: lint on every push.

## Conventions

Every doc has YAML frontmatter. Filenames are stable (no version
suffixes); version lives in frontmatter; git tags mark canonical
states. Cross-references use markdown links to stable anchors, never
to versioned filenames. See [`CONVENTIONS.md`](CONVENTIONS.md) for the
full spec.

## Quickstart

```bash
git clone https://github.com/SolutionSmith-debug/its-blueprint.git
cd its-blueprint
python3 -m venv .venv && source .venv/bin/activate
pip install pyyaml

# Lint
python scripts/lint_frontmatter.py
python scripts/lint_crossrefs.py

# Render handoff packet (.md → .docx for external delivery)
python scripts/render_handoff_packet.py --out handoff/
```

## Relationship to Claude.ai project knowledge

The `.md` files here are also uploaded to the Claude.ai project for
chat ergonomics — chat sessions read from project knowledge, which
mirrors this repo. The repo is canonical; project knowledge is a
read-only convenience copy. When a doc changes:

1. Edit the `.md` here.
2. Commit + push.
3. Re-upload the changed file(s) to the Claude.ai project.

Step 3 is the only manual sync. (At Phase 2+ this could be automated
via the Claude.ai API.)

## Migration provenance

This repo was initialized 2026-05-24 by big-bang migrating ~30 .docx
files from the prior Claude.ai project knowledge corpus. The .docx
files lived in the project's file attachments and accumulated
cross-reference drift through v-bumps; the .md migration eliminates
that tax. See [`archive/README.md`](archive/README.md) for the full
retirement registry.
