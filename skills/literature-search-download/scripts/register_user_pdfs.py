#!/usr/bin/env python3
"""Register user-supplied PDFs into shortlist after the pause gate."""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", (s or "").lower())


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--shortlist", required=True)
    p.add_argument("--user-dir", required=True, help="Directory where user dropped PDFs")
    p.add_argument("--pdf-dir", required=True, help="Canonical pdfs/ directory")
    p.add_argument("--out", required=True)
    args = p.parse_args()

    with open(args.shortlist, encoding="utf-8-sig") as f:
        data = json.load(f)
    items = data.get("items") if isinstance(data, dict) else data
    if not isinstance(items, list):
        raise SystemExit("bad shortlist")

    os.makedirs(args.pdf_dir, exist_ok=True)
    user_files = []
    if os.path.isdir(args.user_dir):
        user_files = [
            os.path.join(args.user_dir, n)
            for n in os.listdir(args.user_dir)
            if n.lower().endswith(".pdf")
        ]

    matched = 0
    for paper in items:
        if paper.get("pdf_path") and os.path.isfile(paper["pdf_path"]):
            paper["access_status"] = "fulltext"
            continue
        keys = [
            norm(str(paper.get("id") or "")),
            norm(str(paper.get("doi") or "")),
            norm(str(paper.get("arxiv_id") or "")),
            norm(str(paper.get("title") or "")[:40]),
        ]
        hit = None
        for uf in user_files:
            base = norm(os.path.splitext(os.path.basename(uf))[0])
            if any(k and k in base for k in keys if k):
                hit = uf
                break
        if hit:
            dest = os.path.join(args.pdf_dir, os.path.basename(hit))
            if os.path.abspath(hit) != os.path.abspath(dest):
                shutil.copy2(hit, dest)
            paper["pdf_path"] = dest
            paper["access_status"] = "fulltext"
            matched += 1

    out_obj = data if isinstance(data, dict) else {"items": items}
    if isinstance(out_obj, dict):
        out_obj["items"] = items
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(out_obj, f, ensure_ascii=False, indent=2)

    missing = [x for x in items if not (x.get("pdf_path") and os.path.isfile(x["pdf_path"]))]
    print(f"Registered {matched} user PDFs; still missing {len(missing)}")
    for m in missing:
        print(f"  MISSING: {m.get('title')} | {m.get('doi') or m.get('arxiv_id')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
