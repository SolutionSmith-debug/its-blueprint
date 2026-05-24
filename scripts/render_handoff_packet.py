"""Render selected blueprint docs to .docx for external delivery.

Pandoc converts .md to .docx with a clean default style. Used at
handoff boundaries (Phase 1.5 California shipment, Customer 2 fork)
where the recipient expects Word-format artifacts.

Output is written to ./handoff/ (gitignored). Re-runs are idempotent.

CLI:
    python scripts/render_handoff_packet.py --out handoff/
    python scripts/render_handoff_packet.py --include doctrine/ --out handoff/

Defaults render: all of doctrine/, references/, and workstreams/.
Audits and session logs are NOT in the default packet — they're
internal forensic records, not customer-facing.
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

DEFAULT_INCLUDES = ["doctrine", "references", "workstreams"]


def _strip_frontmatter(md_text: str) -> str:
    """Remove YAML frontmatter before pandoc conversion.

    Pandoc handles frontmatter natively but treats it as metadata for
    the .docx, which clutters the output. Strip it ourselves.
    """
    if not md_text.startswith("---\n"):
        return md_text
    end = md_text.find("\n---\n", 4)
    if end == -1:
        return md_text
    return md_text[end + 5 :].lstrip("\n")


def _render_one(src: Path, dst: Path) -> bool:
    """Render src.md to dst.docx. Returns True on success."""
    dst.parent.mkdir(parents=True, exist_ok=True)
    cleaned = _strip_frontmatter(src.read_text())
    try:
        result = subprocess.run(
            ["pandoc", "-f", "markdown", "-t", "docx", "-o", str(dst)],
            input=cleaned, text=True, capture_output=True, check=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"  FAIL {src.relative_to(REPO_ROOT)}: {e.stderr}")
        return False
    except FileNotFoundError:
        print("  pandoc not installed; aborting")
        sys.exit(2)
    if result.returncode == 0:
        print(f"  ok {src.relative_to(REPO_ROOT)} → {dst.relative_to(REPO_ROOT)}")
        return True
    return False


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="render_handoff_packet")
    parser.add_argument("--out", type=Path, default=REPO_ROOT / "handoff",
                        help="Output directory (default: ./handoff/)")
    parser.add_argument("--include", action="append", default=None,
                        help="Subdirectories to include (default: doctrine/, references/, workstreams/)")
    parser.add_argument("--clean", action="store_true",
                        help="Empty output dir before rendering")
    args = parser.parse_args(argv)

    if args.clean and args.out.exists():
        shutil.rmtree(args.out)

    includes = args.include or DEFAULT_INCLUDES
    md_files: list[Path] = []
    for inc in includes:
        inc_path = REPO_ROOT / inc
        if not inc_path.exists():
            continue
        md_files.extend(sorted(inc_path.rglob("*.md")))

    if not md_files:
        print("No markdown files found.")
        return 0

    print(f"Rendering {len(md_files)} files → {args.out}/")
    success = 0
    for src in md_files:
        rel = src.relative_to(REPO_ROOT)
        dst = args.out / rel.with_suffix(".docx")
        if _render_one(src, dst):
            success += 1

    print(f"\nDone: {success}/{len(md_files)} rendered.")
    return 0 if success == len(md_files) else 1


if __name__ == "__main__":
    sys.exit(main())
