#!/usr/bin/env python3
"""List candidate files under authorized roots within a time window.

Stdlib only. Lists metadata only — does not read file contents.
Respects F4 ignore rules from shared/workspace-layout.md.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

SKIP_DIR_NAMES = {
    "node_modules",
    "venv",
    ".venv",
    "__pycache__",
    ".git",
    ".svn",
}

WEIGHT_SUFFIXES = {".pth", ".ckpt", ".safetensors"}
DATASET_SUFFIXES = {".tfrecord", ".hdf5", ".arrow", ".h5"}
BINARY_SUFFIXES = {".exe", ".dll", ".so", ".mp4"}
SECRET_NAMES = {".env"}
SECRET_SUFFIXES = {".key", ".pem"}
SECRET_PREFIXES = ("secrets.", "credentials.")

KIND_BY_SUFFIX = {
    ".py": "code",
    ".sh": "code",
    ".ps1": "code",
    ".yaml": "code",
    ".yml": "code",
    ".toml": "code",
    ".json": "result",
    ".csv": "result",
    ".tsv": "result",
    ".log": "log",
    ".md": "doc",
    ".txt": "doc",
    ".png": "result",
    ".jpg": "result",
    ".jpeg": "result",
    ".svg": "result",
    ".pdf": "doc",
}


def parse_since(value: str) -> datetime:
    """Parse ISO date YYYY-MM-DD or relative Nd (e.g. 7d)."""
    value = value.strip()
    m = re.fullmatch(r"(\d+)\s*d", value, flags=re.IGNORECASE)
    now = datetime.now(timezone.utc)
    if m:
        return now - timedelta(days=int(m.group(1)))
    try:
        dt = datetime.strptime(value, "%Y-%m-%d")
        return dt.replace(tzinfo=timezone.utc)
    except ValueError as e:
        raise argparse.ArgumentTypeError(
            f"--since must be YYYY-MM-DD or Nd (e.g. 7d), got {value!r}"
        ) from e


def is_secret_name(name: str) -> bool:
    lower = name.lower()
    if lower in SECRET_NAMES:
        return True
    if any(lower.startswith(p) for p in SECRET_PREFIXES):
        return True
    suffix = Path(name).suffix.lower()
    return suffix in SECRET_SUFFIXES


def should_skip_file(path: Path) -> bool:
    name = path.name
    if is_secret_name(name):
        return True
    suffix = path.suffix.lower()
    if suffix in WEIGHT_SUFFIXES or suffix in DATASET_SUFFIXES or suffix in BINARY_SUFFIXES:
        return True
    if suffix == ".bin":
        try:
            if path.stat().st_size > 10 * 1024 * 1024:
                return True
        except OSError:
            return True
    return False


def guess_kind(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in KIND_BY_SUFFIX:
        return KIND_BY_SUFFIX[suffix]
    name = path.name.lower()
    if "log" in name:
        return "log"
    if name.startswith("metric") or name.startswith("result"):
        return "result"
    return "doc"


def iter_candidate_files(root: Path):
    root = root.resolve()
    if not root.exists():
        return
    if root.is_file():
        yield root
        return
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIR_NAMES]
        for name in filenames:
            yield Path(dirpath) / name


def collect(roots: list[Path], since: datetime, max_files: int) -> list[dict]:
    rows: list[dict] = []
    since_ts = since.timestamp()
    for root in roots:
        root = root.resolve()
        if not root.exists():
            print(f"warning: root does not exist: {root}", file=sys.stderr)
            continue
        for path in iter_candidate_files(root):
            if any(part in SKIP_DIR_NAMES for part in path.parts):
                continue
            if should_skip_file(path):
                continue
            try:
                st = path.stat()
            except OSError:
                continue
            if st.st_mtime < since_ts:
                continue
            mtime = datetime.fromtimestamp(st.st_mtime, tz=timezone.utc)
            rows.append(
                {
                    "path": str(path),
                    "mtime": mtime.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "size": st.st_size,
                    "kind_guess": guess_kind(path),
                }
            )

    rows.sort(key=lambda r: r["mtime"], reverse=True)
    if max_files > 0:
        rows = rows[:max_files]
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description="List recent files under authorized roots.")
    parser.add_argument(
        "--roots",
        nargs="+",
        required=True,
        help="Authorized root paths (files or directories)",
    )
    parser.add_argument(
        "--since",
        type=parse_since,
        required=True,
        help="ISO date YYYY-MM-DD or relative Nd (e.g. 7d)",
    )
    parser.add_argument(
        "--out",
        type=Path,
        required=True,
        help="Output JSONL path",
    )
    parser.add_argument(
        "--max-files",
        type=int,
        default=500,
        help="Max rows to write (default 500; 0 = no limit)",
    )
    args = parser.parse_args()

    roots = [Path(p) for p in args.roots]
    rows = collect(roots, args.since, args.max_files)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"wrote {len(rows)} rows -> {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
