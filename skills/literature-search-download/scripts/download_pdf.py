#!/usr/bin/env python3
"""Download OA / arXiv PDFs only. Never bypass paywalls. Stdlib only."""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.request


def validate_pdf(path: str) -> bool:
    try:
        with open(path, "rb") as f:
            if f.read(5) != b"%PDF-":
                return False
            f.seek(0, 2)
            size = f.tell()
            f.seek(max(0, size - 1024))
            return b"%%EOF" in f.read()
    except OSError:
        return False


def safe_name(paper: dict) -> str:
    base = paper.get("arxiv_id") or paper.get("doi") or paper.get("id") or "paper"
    base = str(base).replace("/", "_").replace("\\", "_").replace(":", "_")
    return base + ("" if base.endswith(".pdf") else ".pdf")


def download(url: str, dest: str, timeout: int = 60) -> bool:
    part = dest + ".part"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "MENTOR-literature-search/1.0 (academic OA fetcher)"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            ctype = resp.headers.get("Content-Type", "")
            if "text/html" in ctype and "pdf" not in ctype.lower():
                return False
            with open(part, "wb") as f:
                while True:
                    chunk = resp.read(8192)
                    if not chunk:
                        break
                    f.write(chunk)
        if not validate_pdf(part):
            os.remove(part)
            return False
        os.replace(part, dest)
        return True
    except Exception as e:
        print(f"  fail {url}: {e}", file=sys.stderr)
        if os.path.exists(part):
            os.remove(part)
        return False


def resolve_url(paper: dict) -> tuple[str | None, str]:
    """Return (url, source_kind). Prefer arxiv then explicit pdf_url.

    source_kind is for access log only. Paper access_status uses protocol enums:
    fulltext | abstract_only | waiting_user_pdf | unknown.
    """
    if paper.get("arxiv_id"):
        aid = str(paper["arxiv_id"]).replace("arxiv:", "")
        return f"https://arxiv.org/pdf/{aid}.pdf", "arxiv"
    url = paper.get("pdf_url")
    if url and ("arxiv.org" in url or url.lower().endswith(".pdf")):
        kind = "arxiv" if "arxiv.org" in url else "oa"
        return url, kind
    return None, "none"


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--jsonl", required=True)
    p.add_argument("--output-dir", required=True)
    p.add_argument("--access-out", required=True)
    p.add_argument("--max-downloads", type=int, default=30)
    p.add_argument("--delay", type=float, default=1.0)
    args = p.parse_args()

    papers = []
    with open(args.jsonl, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                papers.append(json.loads(line))

    os.makedirs(args.output_dir, exist_ok=True)
    access = []
    downloaded = 0
    updated = []

    for paper in papers:
        url, kind = resolve_url(paper)
        entry = {
            "id": paper.get("id"),
            "title": paper.get("title"),
            "doi": paper.get("doi"),
            "arxiv_id": paper.get("arxiv_id"),
            "landing_url": paper.get("landing_url") or paper.get("url"),
            "attempted_url": url,
            "source_kind": kind,
            "status": "waiting_user_pdf",
            "reason": None,
            "hint": "Place institutional PDF in pdfs/user/ if no OA PDF.",
        }
        if not url:
            entry["reason"] = "no_oa_or_arxiv_url"
            paper["access_status"] = "waiting_user_pdf"
            access.append(entry)
            updated.append(paper)
            continue
        if downloaded >= args.max_downloads:
            entry["reason"] = "max_downloads_reached"
            paper["access_status"] = "waiting_user_pdf"
            access.append(entry)
            updated.append(paper)
            continue
        dest = os.path.join(args.output_dir, safe_name(paper))
        if os.path.isfile(dest) and validate_pdf(dest):
            paper["pdf_path"] = dest
            paper["access_status"] = "fulltext"
            entry["status"] = "fulltext"
            entry["path"] = dest
            access.append(entry)
            updated.append(paper)
            continue
        ok = download(url, dest)
        time.sleep(args.delay)
        if ok:
            downloaded += 1
            paper["pdf_path"] = dest
            paper["access_status"] = "fulltext"
            entry["status"] = "fulltext"
            entry["path"] = dest
        else:
            paper["access_status"] = "waiting_user_pdf"
            entry["status"] = "waiting_user_pdf"
            entry["reason"] = "download_or_validate_failed"
        access.append(entry)
        updated.append(paper)

    with open(args.jsonl, "w", encoding="utf-8") as f:
        for row in updated:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    os.makedirs(os.path.dirname(os.path.abspath(args.access_out)) or ".", exist_ok=True)
    with open(args.access_out, "w", encoding="utf-8") as f:
        json.dump({"count": len(access), "records": access}, f, ensure_ascii=False, indent=2)
    print(f"Downloaded {downloaded}; access log → {args.access_out}; updated {args.jsonl}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
