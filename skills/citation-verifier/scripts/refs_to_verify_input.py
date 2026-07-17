#!/usr/bin/env python3
"""Extract verify input list from references.json."""
from __future__ import annotations

import argparse
import json
import os


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--references", required=True)
    p.add_argument("--out", required=True)
    args = p.parse_args()
    with open(args.references, encoding="utf-8-sig") as f:
        data = json.load(f)
    papers = data.get("papers") if isinstance(data, dict) else data
    out = [
        {
            "id": x.get("id") or x.get("cite_key"),
            "arxiv_id": x.get("arxiv_id"),
            "doi": x.get("doi"),
            "title": x.get("title"),
        }
        for x in papers
    ]
    os.makedirs(os.path.dirname(os.path.abspath(args.out)) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"Wrote {len(out)} → {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
