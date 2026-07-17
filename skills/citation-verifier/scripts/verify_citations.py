#!/usr/bin/env python3
"""Verify paper existence: arXiv → CrossRef DOI → CrossRef title fallback.

Inspired by ARIS pre-search verification / K-Dense DOI checks. Stdlib only.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

UA = "literature-survey-demo-verify/1.0"
ATOM_NS = {"a": "http://www.w3.org/2005/Atom"}


def user_agent() -> str:
    mail = os.environ.get("CROSSREF_MAILTO") or os.environ.get("OPENALEX_EMAIL")
    return f"{UA} (mailto:{mail})" if mail else UA


def http_get(url: str, accept: str = "*/*") -> tuple[int, bytes]:
    req = urllib.request.Request(url, headers={"User-Agent": user_agent(), "Accept": accept})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read() if e.fp else b""
    except Exception:
        return 0, b""


def verify_arxiv(arxiv_id: str) -> tuple[str, str]:
    aid = arxiv_id.strip().replace("arxiv:", "")
    aid = re.sub(r"v\d+$", "", aid)
    url = f"http://export.arxiv.org/api/query?id_list={urllib.parse.quote(aid)}"
    code, body = http_get(url)
    if code != 200:
        return "pending", "arxiv_http_error"
    root = ET.fromstring(body.decode("utf-8", errors="replace"))
    entries = root.findall("a:entry", ATOM_NS)
    # arXiv returns an entry even for bad ids sometimes with error; check title
    if not entries:
        return "unverified", "arxiv_no_entry"
    title = ""
    for el in entries[0].findall("a:title", ATOM_NS):
        title = (el.text or "").strip()
    if not title or title.lower().startswith("error"):
        return "unverified", "arxiv_missing"
    return "verified", "arxiv"


def verify_doi(doi: str) -> tuple[str, str, dict]:
    doi = doi.strip().replace("https://doi.org/", "")
    url = "https://api.crossref.org/works/" + urllib.parse.quote(doi)
    code, body = http_get(url, accept="application/json")
    if code == 404:
        return "unverified", "crossref_not_found", {}
    if code != 200:
        return "pending", "crossref_http_error", {}
    try:
        msg = json.loads(body.decode("utf-8", errors="replace")).get("message") or {}
    except json.JSONDecodeError:
        return "pending", "crossref_bad_json", {}
    return "verified", "crossref", {
        "title": " ".join(msg.get("title") or []),
        "year": (msg.get("published-print") or msg.get("published-online") or {}).get("date-parts", [[None]])[0][0],
    }


def verify_title(title: str) -> tuple[str, str, dict]:
    if not title or len(title) < 8:
        return "error", "no_identifier", {}
    q = urllib.parse.urlencode({"query.bibliographic": title, "rows": 3})
    url = f"https://api.crossref.org/works?{q}"
    code, body = http_get(url, accept="application/json")
    if code != 200:
        return "pending", "crossref_title_http_error", {}
    try:
        items = (json.loads(body.decode("utf-8", errors="replace")).get("message") or {}).get("items") or []
    except json.JSONDecodeError:
        return "pending", "crossref_bad_json", {}
    nt = re.sub(r"\s+", " ", title.lower())
    for it in items:
        cand = " ".join(it.get("title") or []).lower()
        cand = re.sub(r"\s+", " ", cand)
        # rough overlap
        tw = set(nt.split())
        cw = set(cand.split())
        if not tw or not cw:
            continue
        overlap = len(tw & cw) / max(len(tw), len(cw))
        if overlap >= 0.6:
            return "verified", "title", {"title": " ".join(it.get("title") or []), "doi": it.get("DOI")}
    return "unverified", "title_no_match", {}


def verify_one(p: dict) -> dict:
    out = {
        "id": p.get("id"),
        "title": p.get("title"),
        "doi": p.get("doi"),
        "arxiv_id": p.get("arxiv_id"),
        "status": "error",
        "method": "none",
        "notes": "",
        "meta": {},
    }
    if p.get("arxiv_id"):
        status, method = verify_arxiv(str(p["arxiv_id"]))
        out["status"], out["method"] = status, method if status == "verified" else method
        out["notes"] = method
        if status == "verified":
            return out
        time.sleep(0.3)
    if p.get("doi"):
        status, method, meta = verify_doi(str(p["doi"]))
        out["status"], out["method"], out["meta"] = status, method, meta
        out["notes"] = method
        if status == "verified":
            return out
        time.sleep(0.3)
    if p.get("title"):
        status, method, meta = verify_title(str(p["title"]))
        out["status"], out["method"], out["meta"] = status, method, meta
        out["notes"] = method
        return out
    out["status"] = "error"
    out["notes"] = "no_arxiv_doi_title"
    return out


def verdict_of(papers: list[dict]) -> str:
    terminal = [x for x in papers if x["status"] in ("verified", "unverified")]
    if not papers:
        return "ERROR"
    if any(x["status"] == "pending" for x in papers):
        return "WARN"
    if not terminal:
        return "ERROR"
    unver = sum(1 for x in terminal if x["status"] == "unverified")
    rate = unver / len(terminal)
    if rate > 0.2:
        return "WARN"
    if unver:
        return "WARN"
    return "PASS"


def to_md(report: dict) -> str:
    lines = [
        f"# Citation Audit",
        "",
        f"- verdict: **{report['verdict']}**",
        f"- summary: {report['summary']}",
        "",
        "| id | status | method | title |",
        "|----|--------|--------|-------|",
    ]
    for p in report["papers"]:
        title = (p.get("title") or "").replace("|", "/")
        lines.append(f"| {p.get('id')} | {p.get('status')} | {p.get('method')} | {title} |")
    lines += [
        "",
        "## Claim-support (agent-filled)",
        "",
        "List any survey sentences whose cited paper does not support the claim.",
        "",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="JSON list of papers")
    ap.add_argument("--output", required=True, help="CITATION_AUDIT.json")
    ap.add_argument("--md", default=None, help="CITATION_AUDIT.md")
    args = ap.parse_args()

    with open(args.input, encoding="utf-8-sig") as f:
        data = json.load(f)
    if isinstance(data, dict) and "papers" in data:
        papers_in = data["papers"]
    elif isinstance(data, list):
        papers_in = data
    else:
        print("ERROR: input must be a list or {papers: [...]}", file=sys.stderr)
        return 1

    results = []
    for p in papers_in:
        results.append(verify_one(p))
        time.sleep(0.2)

    report = {
        "verdict": verdict_of(results),
        "summary": f"{sum(1 for x in results if x['status']=='verified')} verified / {len(results)} total",
        "papers": results,
    }
    os.makedirs(os.path.dirname(os.path.abspath(args.output)) or ".", exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    md_path = args.md or os.path.splitext(args.output)[0] + ".md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(to_md(report))
    print(f"verdict={report['verdict']} → {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
