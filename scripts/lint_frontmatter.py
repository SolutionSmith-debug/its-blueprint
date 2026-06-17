"""Lint ITS Blueprint markdown frontmatter.

Mirrors the execution-layer doc-conventions linter with planning-side
extensions (doctrine, mission, brief, overlay types). See CONVENTIONS.md
for the spec.

Checks each doc for:
  1. Frontmatter present (required for all docs except exempt list)
  2. Required fields present
  3. type / status / workstream in canonical sets
  4. Filename matches naming convention for the type
  5. last_verified not stale beyond N days for status=canonical

CLI:
    python scripts/lint_frontmatter.py
    python scripts/lint_frontmatter.py --strict
    python scripts/lint_frontmatter.py --stale-days 60
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent

CANONICAL_TYPES = frozenset({
    "doctrine",
    "mission",
    "brief",
    "reference",
    "audit",
    "session_log",
    "overlay",
    "scaffold",
    "snippet",
})

CANONICAL_STATUS = frozenset({
    "canonical",
    "draft",
    "superseded",
    "archived",
})

CANONICAL_WORKSTREAMS = frozenset({
    "safety_reports",
    "safety_portal",
    "email_triage",
    "purchase_orders",
    "subcontracts",
    "ai_employee_capabilities",
    "urs_marine_portal",
})  # None / null also valid

VERSION_REQUIRED_TYPES = frozenset({"doctrine", "mission", "brief"})
DATE_PREFIXED_TYPES = frozenset({"audit", "session_log"})
# Scaffolds and snippets require: name, version, audience, usage_count
SCAFFOLD_TYPES = frozenset({"scaffold", "snippet"})

EXEMPT_FILES = frozenset({
    "README.md",
    "CLAUDE.md",
    "CONVENTIONS.md",
})


@dataclass(frozen=True)
class Violation:
    path: Path
    rule: str
    severity: str
    message: str


def _parse_frontmatter(text: str) -> tuple[dict[str, Any] | None, str | None]:
    if not text.startswith("---\n") and not text.startswith("---\r\n"):
        return None, "missing frontmatter delimiter at file start"
    match = re.search(r"^---\s*$", text[4:], flags=re.MULTILINE)
    if match is None:
        return None, "missing closing frontmatter delimiter"
    yaml_block = text[4 : 4 + match.start()]
    try:
        parsed = yaml.safe_load(yaml_block)
    except yaml.YAMLError as exc:
        return None, f"YAML parse error: {exc!r}"
    if not isinstance(parsed, dict):
        return None, "frontmatter is not a YAML mapping"
    return parsed, None


def _is_exempt(rel_path: Path) -> bool:
    return rel_path.name in EXEMPT_FILES or rel_path.name == "README.md"


def _check_filename(rel_path: Path, doc_type: str | None) -> Violation | None:
    name = rel_path.name
    date_prefix = re.match(r"^(\d{4}-\d{2}-\d{2})_", name)

    if doc_type in DATE_PREFIXED_TYPES and date_prefix is None:
        return Violation(
            rel_path, "filename-date-prefix", "warn",
            f"type={doc_type!r} expects YYYY-MM-DD_topic-slug.md filename",
        )
    if doc_type not in DATE_PREFIXED_TYPES and date_prefix is not None:
        return Violation(
            rel_path, "filename-no-date-prefix", "warn",
            f"type={doc_type!r} expects stable filename (no date prefix)",
        )

    stem = name.rsplit(".", 1)[0]
    slug = stem[11:] if date_prefix else stem
    if "__" in slug:
        return Violation(
            rel_path, "filename-slug-double-underscore", "warn",
            "double-underscore in slug; use single",
        )
    return None


def lint_file(rel_path: Path, stale_days: int) -> list[Violation]:
    if _is_exempt(rel_path):
        return []

    abs_path = REPO_ROOT / rel_path
    text = abs_path.read_text()
    fm, parse_error = _parse_frontmatter(text)

    violations: list[Violation] = []

    if fm is None:
        violations.append(Violation(
            rel_path, "frontmatter-required", "error",
            parse_error or "frontmatter missing",
        ))
        return violations

    doc_type = fm.get("type")
    if not isinstance(doc_type, str) or doc_type not in CANONICAL_TYPES:
        violations.append(Violation(
            rel_path, "type-canonical", "error",
            f"type={doc_type!r} not in {sorted(CANONICAL_TYPES)}",
        ))

    status = fm.get("status")
    if doc_type not in SCAFFOLD_TYPES:
        if not isinstance(status, str) or status not in CANONICAL_STATUS:
            violations.append(Violation(
                rel_path, "status-canonical", "error",
                f"status={status!r} not in {sorted(CANONICAL_STATUS)}",
            ))

    if doc_type not in SCAFFOLD_TYPES:
        workstream = fm.get("workstream", "MISSING")
        if workstream == "MISSING":
            violations.append(Violation(
                rel_path, "workstream-required", "error",
                "missing field 'workstream' (use null for cross-cutting)",
            ))
        elif workstream is not None and (
            not isinstance(workstream, str) or workstream not in CANONICAL_WORKSTREAMS
        ):
            violations.append(Violation(
                rel_path, "workstream-canonical", "error",
                f"workstream={workstream!r} not in {sorted(CANONICAL_WORKSTREAMS)} or null",
            ))

    if doc_type in VERSION_REQUIRED_TYPES or doc_type in SCAFFOLD_TYPES:
        version = fm.get("version")
        if not isinstance(version, int) or version < 1:
            violations.append(Violation(
                rel_path, "version-required", "error",
                f"type={doc_type!r} requires integer version >= 1",
            ))

    if doc_type in SCAFFOLD_TYPES:
        name = fm.get("name")
        if not isinstance(name, str):
            violations.append(Violation(
                rel_path, "scaffold-name-required", "error",
                "scaffold/snippet requires string 'name' field",
            ))
        audience = fm.get("audience")
        if not isinstance(audience, str):
            violations.append(Violation(
                rel_path, "scaffold-audience-required", "error",
                "scaffold/snippet requires string 'audience' field",
            ))
        usage_count = fm.get("usage_count")
        if not isinstance(usage_count, int) or usage_count < 0:
            violations.append(Violation(
                rel_path, "scaffold-usage-count-required", "error",
                "scaffold/snippet requires integer 'usage_count' >= 0",
            ))

    if status == "canonical":
        last_verified = fm.get("last_verified")
        if last_verified is None:
            violations.append(Violation(
                rel_path, "last-verified-required", "error",
                "status=canonical requires 'last_verified' (YYYY-MM-DD)",
            ))
        elif isinstance(last_verified, date):
            age = (date.today() - last_verified).days
            if age > stale_days:
                violations.append(Violation(
                    rel_path, "last-verified-stale", "warn",
                    f"last_verified is {age}d old (threshold {stale_days}d)",
                ))

    fn_violation = _check_filename(rel_path, doc_type if isinstance(doc_type, str) else None)
    if fn_violation:
        violations.append(fn_violation)

    return violations


def walk_docs() -> list[Path]:
    md: list[Path] = []
    for path in REPO_ROOT.rglob("*.md"):
        if any(part.startswith(".") for part in path.parts):
            continue
        if path.parts[0] == "archive":
            # archive/ entries are retirement registry; only README required to lint
            if path.name != "README.md":
                continue
        md.append(path.relative_to(REPO_ROOT))
    return md


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="lint_frontmatter")
    parser.add_argument("--strict", action="store_true",
                        help="exit non-zero on any violation")
    parser.add_argument("--stale-days", type=int, default=60,
                        help="warn threshold for last_verified age (default 60)")
    args = parser.parse_args(argv)

    md_files = walk_docs()
    all_v: list[Violation] = []
    for rel in sorted(md_files):
        all_v.extend(lint_file(rel, args.stale_days))

    if not all_v:
        print(f"Frontmatter lint: clean ({len(md_files)} files).")
        return 0

    errors = [v for v in all_v if v.severity == "error"]
    warns = [v for v in all_v if v.severity == "warn"]

    print(f"Frontmatter lint: {len(errors)} error(s), {len(warns)} warn(s):")
    for v in all_v:
        tag = "[error]" if v.severity == "error" else "[warn]"
        if args.strict and v.severity == "error":
            tag = "[strict-error]"
        print(f"  {tag} {v.path}: {v.rule}: {v.message}")

    if args.strict and errors:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
