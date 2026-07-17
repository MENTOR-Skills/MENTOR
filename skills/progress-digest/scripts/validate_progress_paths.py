#!/usr/bin/env python3
"""Validate that backtick paths and markdown links in F4 deliverables exist.

Extracts `relative/path` and markdown links [text](path). Skips http(s) URLs
and anchors. Exit non-zero if any local path is missing.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

BACKTICK_RE = re.compile(r"`([^`\n]+)`")
MD_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")

SKIP_PREFIXES = ("http://", "https://", "mailto:", "#")
# Paths that are documentation placeholders, not real evidence
SKIP_EXACT = {
    "path/to/file",
    "path/one",
    "path/two",
    "relative/or/absolute/path",
    "runs/.../metrics.csv",
    "runs/.../loss.png",
}


def looks_like_path(s: str) -> bool:
    s = s.strip()
    if not s or s in SKIP_EXACT:
        return False
    if s.startswith(SKIP_PREFIXES):
        return False
    # Evidence paths must include a directory separator (bare `train.py` is prose).
    if "/" in s or "\\" in s:
        return True
    return False


def extract_candidates(text: str) -> list[str]:
    found: list[str] = []
    for m in BACKTICK_RE.finditer(text):
        found.append(m.group(1).strip())
    for m in MD_LINK_RE.finditer(text):
        target = m.group(1).strip()
        # strip optional title: path "title"
        if " " in target:
            target = target.split(" ", 1)[0].strip('"')
        found.append(target)
    return found


def resolve(workspace: Path, raw: str) -> Path | None:
    raw = raw.strip().strip('"').strip("'")
    if not looks_like_path(raw):
        return None
    # Drop line/column suffixes like file.py:12
    raw = re.sub(r":\d+(-\d+)?$", "", raw)
    p = Path(raw)
    if p.is_absolute():
        return p
    return (workspace / p).resolve()


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate evidence paths in F4 markdown.")
    parser.add_argument(
        "--workspace",
        type=Path,
        default=Path("."),
        help="Workspace root for resolving relative paths",
    )
    parser.add_argument(
        "files",
        nargs="+",
        type=Path,
        help="Markdown files to scan (artifact-index, progress-report, ...)",
    )
    args = parser.parse_args()
    workspace = args.workspace.resolve()

    missing: list[tuple[str, str]] = []
    checked = 0
    for md in args.files:
        path = md if md.is_absolute() else workspace / md
        if not path.is_file():
            print(f"error: deliverable missing: {path}", file=sys.stderr)
            return 2
        text = path.read_text(encoding="utf-8")
        for raw in extract_candidates(text):
            resolved = resolve(workspace, raw)
            if resolved is None:
                continue
            checked += 1
            if not resolved.exists():
                missing.append((str(path), raw))

    if missing:
        print(f"checked {checked} path-like refs; {len(missing)} missing:", file=sys.stderr)
        for src, raw in missing:
            print(f"  {src}: {raw}", file=sys.stderr)
        return 1

    print(f"ok: {checked} path-like refs exist under {workspace}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
