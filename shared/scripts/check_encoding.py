#!/usr/bin/env python3
"""Check whether all .md/.json/.yaml/.html files under a path are UTF-8 encoded.

Usage:
    python shared/scripts/check_encoding.py <文件或目录>

Exit code 0 = all files UTF-8 (BOM flagged as warning); 1 = any file not UTF-8.
See shared/encoding-utf8.md for the full rules.
"""
import sys
from pathlib import Path


def check_encoding(root_path):
    root = Path(root_path)
    if not root.exists():
        print(f"Path not found: {root_path}")
        return False

    extensions = {'.md', '.json', '.yaml', '.yml', '.html', '.htm'}
    all_ok = True

    for f in sorted(root.rglob('*')):
        if f.suffix not in extensions:
            continue
        try:
            text = f.read_text(encoding='utf-8')
            has_bom = text.startswith('﻿')
            if has_bom:
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
        print("Usage: python check_encoding.py <directory>")
        sys.exit(1)
    ok = check_encoding(sys.argv[1])
    sys.exit(0 if ok else 1)
