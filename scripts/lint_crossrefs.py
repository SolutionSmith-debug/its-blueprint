"""Lint ITS Blueprint cross-references.

Walks every `[text](path)` markdown link in every `.md` file and
verifies the target file exists. If the link includes an `#anchor`,
verifies the anchor matches a heading in the target file (GitHub-style
autogen: lowercase, hyphens for spaces, strip punctuation).

External links (http://, https://) are skipped.

CLI:
    python scripts/lint_crossrefs.py
    python scripts/lint_crossrefs.py --strict
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Match [text](target) markdown links. Capture target.
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")

# Match heading lines (skip code blocks via state machine in caller)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")


@dataclass(frozen=True)
class LinkViolation:
    source: Path
    target_raw: str
    rule: str
    message: str


def _slugify(heading_text: str) -> str:
    """GitHub-style anchor autogeneration."""
    text = heading_text.lower()
    # Strip backticks, asterisks, underscores, em-dashes, etc.
    text = re.sub(r"[`*_]", "", text)
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"\s+", "-", text)
    return text.strip("-")


def _extract_anchors(path: Path) -> set[str]:
    """Return all GitHub-autogen anchors from a file's headings."""
    if not path.exists():
        return set()
    anchors: set[str] = set()
    in_code = False
    for line in path.read_text().splitlines():
        # Toggle code-block state on ``` lines
        if line.lstrip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        m = HEADING_RE.match(line)
        if m:
            anchors.add(_slugify(m.group(2)))
    return anchors


def _extract_links(path: Path) -> list[tuple[str, str]]:
    """Return [(text, target_raw)] for every markdown link in the file.

    Skips links inside fenced code blocks AND inside inline backtick spans.
    """
    links: list[tuple[str, str]] = []
    in_code = False
    in_frontmatter = False
    line_count = 0
    for line in path.read_text().splitlines():
        line_count += 1
        # Skip YAML frontmatter
        if line_count == 1 and line.startswith("---"):
            in_frontmatter = True
            continue
        if in_frontmatter:
            if line.startswith("---"):
                in_frontmatter = False
            continue
        if line.lstrip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        # Strip inline backtick spans before matching links
        stripped = re.sub(r"`[^`]*`", "", line)
        for m in LINK_RE.finditer(stripped):
            links.append((m.group(1), m.group(2)))
    return links


def lint_file(rel_path: Path) -> list[LinkViolation]:
    abs_path = REPO_ROOT / rel_path
    violations: list[LinkViolation] = []

    for _text, target_raw in _extract_links(abs_path):
        # Skip external links
        if target_raw.startswith(("http://", "https://", "mailto:")):
            continue
        # Skip pure-anchor links (#section) — resolve against same file
        if target_raw.startswith("#"):
            anchor = target_raw.lstrip("#")
            anchors = _extract_anchors(abs_path)
            if anchor not in anchors:
                violations.append(LinkViolation(
                    rel_path, target_raw, "anchor-not-found",
                    f"anchor {anchor!r} not found in {rel_path.name}",
                ))
            continue

        # Split target into path + anchor
        if "#" in target_raw:
            path_part, anchor = target_raw.split("#", 1)
        else:
            path_part, anchor = target_raw, None

        # Resolve relative path
        target_abs = (abs_path.parent / path_part).resolve()
        try:
            target_abs.relative_to(REPO_ROOT)
        except ValueError:
            violations.append(LinkViolation(
                rel_path, target_raw, "path-outside-repo",
                f"resolved path escapes repo root",
            ))
            continue

        if not target_abs.exists():
            violations.append(LinkViolation(
                rel_path, target_raw, "target-missing",
                f"target file not found: {target_abs.relative_to(REPO_ROOT)}",
            ))
            continue

        if anchor and target_abs.suffix == ".md":
            anchors = _extract_anchors(target_abs)
            if anchor not in anchors:
                violations.append(LinkViolation(
                    rel_path, target_raw, "anchor-not-found",
                    f"anchor {anchor!r} not in {target_abs.relative_to(REPO_ROOT)}",
                ))

    return violations


def walk_docs() -> list[Path]:
    md: list[Path] = []
    for path in REPO_ROOT.rglob("*.md"):
        if any(part.startswith(".") for part in path.parts):
            continue
        md.append(path.relative_to(REPO_ROOT))
    return md


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="lint_crossrefs")
    parser.add_argument("--strict", action="store_true",
                        help="exit non-zero on any violation")
    args = parser.parse_args(argv)

    md_files = walk_docs()
    all_v: list[LinkViolation] = []
    for rel in sorted(md_files):
        all_v.extend(lint_file(rel))

    if not all_v:
        print(f"Cross-ref lint: clean ({len(md_files)} files).")
        return 0

    print(f"Cross-ref lint: {len(all_v)} violation(s):")
    for v in all_v:
        tag = "[strict-error]" if args.strict else "[warn]"
        print(f"  {tag} {v.source}: {v.rule}: {v.target_raw!r} — {v.message}")

    if args.strict:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
