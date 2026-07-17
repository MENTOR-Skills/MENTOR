#!/usr/bin/env python3
"""Convert shortlist.json to JSONL for download_pdf.py."""
from __future__ import annotations

import argparse
import json
import os


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--in", dest="inp", required=True)
    p.add_argument("--out", required=True)
    args = p.parse_args()
    with open(args.inp, encoding="utf-8-sig") as f:
        data = json.load(f)
    items = data.get("items") if isinstance(data, dict) else data
    if not isinstance(items, list):
        raise SystemExit("shortlist must be list or {items: [...]}")
    os.makedirs(os.path.dirname(os.path.abspath(args.out)) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        for row in items:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"Wrote {len(items)} → {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
