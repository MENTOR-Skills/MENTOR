#!/usr/bin/env python3
"""Merge multiple papers JSONL files; dedupe by arxiv_id / doi / normalized title."""
from __future__ import annotations

import argparse
import json
import os
import re
import sys


def norm_title(t: str) -> str:
    t = (t or "").lower()
    t = re.sub(r"[^a-z0-9\s]", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def load_jsonl(path: str) -> list[dict]:
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def key_of(p: dict) -> str:
    if p.get("arxiv_id"):
        return "arxiv:" + str(p["arxiv_id"]).lower().split("v")[0]
    if p.get("doi"):
        return "doi:" + str(p["doi"]).lower().replace("https://doi.org/", "")
    return "title:" + norm_title(p.get("title") or "")


def merge_prefer(a: dict, b: dict) -> dict:
    """Prefer peer-reviewed / richer metadata."""
    out = dict(a)
    for k, v in b.items():
        if out.get(k) in (None, "", [], "pending") and v not in (None, "", []):
            out[k] = v
    if b.get("peer_reviewed") and not a.get("peer_reviewed"):
        out["venue"] = b.get("venue") or out.get("venue")
        out["peer_reviewed"] = True
    if (b.get("cited_by_count") or 0) > (a.get("cited_by_count") or 0):
        out["cited_by_count"] = b["cited_by_count"]
    sources = {a.get("source"), b.get("source")} - {None}
    out["source"] = "merge" if len(sources) > 1 else (a.get("source") or b.get("source"))
    return out


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("inputs", nargs="+")
    p.add_argument("--out", required=True)
    args = p.parse_args()
    merged: dict[str, dict] = {}
    order: list[str] = []
    for path in args.inputs:
        if not os.path.isfile(path):
            print(f"WARN: missing {path}", file=sys.stderr)
            continue
        for row in load_jsonl(path):
            k = key_of(row)
            if not k or k == "title:":
                continue
            if k not in merged:
                merged[k] = row
                order.append(k)
            else:
                merged[k] = merge_prefer(merged[k], row)
    os.makedirs(os.path.dirname(os.path.abspath(args.out)) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        for k in order:
            f.write(json.dumps(merged[k], ensure_ascii=False) + "\n")
    print(f"Merged {len(order)} unique papers → {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
