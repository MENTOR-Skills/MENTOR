#!/usr/bin/env python3
"""Cascaded search: user venues (Tier-1) → open OpenAlex (Tier-2) → limited arXiv (Tier-3).

No hardcoded venue names. Venues come from --venues, --venues-file, or are skipped.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys


def read_venues(path: str | None, cli: str | None) -> list[str]:
    items: list[str] = []
    if cli:
        items.extend(v.strip() for v in cli.split(",") if v.strip())
    if path and os.path.isfile(path):
        with open(path, encoding="utf-8-sig") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    items.append(line)
    # dedupe preserve order
    seen = set()
    out = []
    for v in items:
        k = v.lower()
        if k not in seen:
            seen.add(k)
            out.append(v)
    return out


def run(cmd: list[str]) -> None:
    print("+", " ".join(cmd), flush=True)
    subprocess.check_call(cmd)


def load_jsonl(path: str) -> list[dict]:
    if not os.path.isfile(path):
        return []
    rows = []
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def count_peer(rows: list[dict]) -> int:
    return sum(1 for r in rows if r.get("peer_reviewed") is True)


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    p = argparse.ArgumentParser()
    p.add_argument("--query", required=True)
    p.add_argument("--year", default=None)
    p.add_argument("--venues", default=None, help="Comma-separated user venues")
    p.add_argument("--venues-file", default=None)
    p.add_argument("--secondary-venues-file", default=None)
    p.add_argument("--tier1-min", type=int, default=8)
    p.add_argument("--tier2-min", type=int, default=8)
    p.add_argument("--tier1-limit", type=int, default=30)
    p.add_argument("--tier2-limit", type=int, default=30)
    p.add_argument("--arxiv-max", type=int, default=10)
    p.add_argument("--out-dir", required=True)
    args = p.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)
    oa = os.path.join(here, "search_openalex.py")
    ax = os.path.join(here, "search_arxiv.py")
    merge = os.path.join(here, "merge_papers.py")

    venues = read_venues(args.venues_file, args.venues)
    secondary = read_venues(args.secondary_venues_file, None)
    paths: list[str] = []
    log = {"query": args.query, "year": args.year, "venues_user": venues, "tiers_run": []}

    # Tier-1
    t1 = os.path.join(args.out_dir, "tier1_openalex.jsonl")
    if venues:
        cmd = [sys.executable, oa, args.query, "--limit", str(args.tier1_limit), "--out", t1, "--venues", ",".join(venues)]
        if args.year:
            cmd.extend(["--year", args.year])
        run(cmd)
        paths.append(t1)
        log["tiers_run"].append({"tier": 1, "mode": "user_venues", "count": len(load_jsonl(t1))})
    else:
        log["tiers_run"].append({"tier": 1, "mode": "skipped_no_user_venues", "count": 0})

    n1 = len(load_jsonl(t1)) if venues else 0

    # Tier-2 if needed
    t2 = os.path.join(args.out_dir, "tier2_openalex.jsonl")
    if n1 < args.tier1_min:
        if secondary:
            cmd = [sys.executable, oa, args.query, "--limit", str(args.tier2_limit), "--out", t2, "--venues", ",".join(secondary)]
        else:
            cmd = [sys.executable, oa, args.query, "--limit", str(args.tier2_limit), "--out", t2]
        if args.year:
            cmd.extend(["--year", args.year])
        run(cmd)
        paths.append(t2)
        log["tiers_run"].append({"tier": 2, "mode": "secondary_or_open", "count": len(load_jsonl(t2))})
    else:
        log["tiers_run"].append({"tier": 2, "mode": "skipped_tier1_enough", "count": 0})

    merged_so_far = os.path.join(args.out_dir, "papers_pre_arxiv.jsonl")
    if paths:
        run([sys.executable, merge, *paths, "--out", merged_so_far])
    else:
        # force tier-2 open search if nothing yet
        cmd = [sys.executable, oa, args.query, "--limit", str(args.tier2_limit), "--out", t2]
        if args.year:
            cmd.extend(["--year", args.year])
        run(cmd)
        run([sys.executable, merge, t2, "--out", merged_so_far])
        log["tiers_run"].append({"tier": 2, "mode": "forced_open", "count": len(load_jsonl(t2))})

    pre = load_jsonl(merged_so_far)
    n_peer = count_peer(pre)

    # Tier-3 arXiv if still thin
    t3 = os.path.join(args.out_dir, "tier3_arxiv.jsonl")
    final = os.path.join(args.out_dir, "papers_all.jsonl")
    if len(pre) < args.tier2_min or n_peer < max(3, args.tier1_min // 2):
        run([sys.executable, ax, args.query, "--max", str(args.arxiv_max), "--out", t3])
        run([sys.executable, merge, merged_so_far, t3, "--out", final])
        log["tiers_run"].append({"tier": 3, "mode": "arxiv_limited", "count": len(load_jsonl(t3))})
    else:
        run([sys.executable, merge, merged_so_far, "--out", final])
        log["tiers_run"].append({"tier": 3, "mode": "skipped", "count": 0})

    log["final_count"] = len(load_jsonl(final))
    log_path = os.path.join(args.out_dir, "search_log.json")
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)
    print(f"Done. papers={log['final_count']} log={log_path}")
    print("NOTE: Do NOT bulk-download. Build shortlist first, then download shortlist only.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
