#!/usr/bin/env python3
"""Check files and supported files under directories for UTF-8 encoding.

Usage:
    python shared/scripts/check_encoding.py <文件或目录> [<文件或目录> ...]

Exit code 0 = all files UTF-8 (BOM flagged as warning); 1 = any file not UTF-8.
See shared/encoding-utf8.md for the full rules.
"""
import sys
from pathlib import Path


EXTENSIONS = {'.md', '.json', '.yaml', '.yml', '.html', '.htm'}


def collect_files(paths):
    files = []
    all_ok = True
    for raw_path in paths:
        path = Path(raw_path)
        if not path.exists():
            print(f"Path not found: {raw_path}")
            all_ok = False
        elif path.is_file():
            files.append(path)
        elif path.is_dir():
            files.extend(
                file
                for file in sorted(path.rglob('*'))
                if file.is_file() and file.suffix.lower() in EXTENSIONS
            )
    return files, all_ok


def check_encoding(paths):
    files, all_ok = collect_files(paths)
    if not files:
        print("FAIL No files to check.")
        all_ok = False

    for f in files:
        try:
            text = f.read_text(encoding='utf-8')
            if text.startswith('\ufeff'):
                print(f"WARNING UTF-8 with BOM: {f}")
        except UnicodeDecodeError:
            print(f"FAIL Not UTF-8: {f}")
            all_ok = False
        except Exception as e:
            print(f"FAIL Error reading: {f} ({e})")
            all_ok = False

    if all_ok:
        print("OK All files are UTF-8.")
    return all_ok


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python check_encoding.py <file-or-directory> [<file-or-directory> ...]")
        sys.exit(1)
    ok = check_encoding(sys.argv[1:])
    sys.exit(0 if ok else 1)
