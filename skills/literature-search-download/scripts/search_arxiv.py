#!/usr/bin/env python3
"""Search arXiv Atom API → JSONL. Stdlib only.

Adapted from dsebastien/ai-skill-arxiv (simplified for demo).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime

ATOM_NS = {
    "a": "http://www.w3.org/2005/Atom",
    "arxiv": "http://arxiv.org/schemas/atom",
}
USER_AGENT = "literature-survey-demo/1.0"
API_URL = "http://export.arxiv.org/api/query"


def build_query(terms: str, category: str | None) -> str:
    # Prefer phrase search for multi-word queries (avoids stopword traps like all:all).
    cleaned = terms.strip()
    parts: list[str] = []
    if cleaned:
        if " " in cleaned:
            phrase = cleaned.replace('"', "")
            parts.append(f'all:%22{urllib.parse.quote(phrase)}%22')
        else:
            parts.append(f"all:{urllib.parse.quote(cleaned)}")
    if category:
        parts.append(f"cat:{category}")
    return "+AND+".join(parts) if parts else "all:*"


def parse(xml_text: str) -> list[dict]:
    root = ET.fromstring(xml_text)
    results = []
    for entry in root.findall("a:entry", ATOM_NS):
        abs_url = _text(entry, "a:id") or ""
        arxiv_id = abs_url.rsplit("/abs/", 1)[-1] if "/abs/" in abs_url else abs_url
        pdf_url = ""
        for link in entry.findall("a:link", ATOM_NS):
            if link.get("title") == "pdf":
                pdf_url = link.get("href", "")
                break
        if not pdf_url and arxiv_id:
            pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
        published = _text(entry, "a:published") or ""
        year = None
        if published:
            try:
                year = datetime.fromisoformat(published.replace("Z", "+00:00")).year
            except ValueError:
                year = int(published[:4]) if published[:4].isdigit() else None
        journal = _text(entry, "arxiv:journal_ref")
        doi = _text(entry, "arxiv:doi")
        results.append({
            "id": f"arxiv:{arxiv_id}",
            "title": _clean(_text(entry, "a:title")),
            "authors": [_text(a, "a:name") or "" for a in entry.findall("a:author", ATOM_NS)],
            "year": year,
            "venue": journal or "arXiv",
            "doi": doi,
            "arxiv_id": arxiv_id,
            "abstract": _clean(_text(entry, "a:summary")),
            "pdf_url": pdf_url,
            "pdf_path": None,
            "landing_url": abs_url,
            "access_status": "pending",
            "peer_reviewed": bool(journal),
            "cited_by_count": None,
            "source": "arxiv",
        })
    return results


def _text(parent, path: str) -> str | None:
    el = parent.find(path, ATOM_NS)
    return el.text if el is not None and el.text else None


def _clean(s: str | None) -> str:
    if not s:
        return ""
    return " ".join(s.split())


def main() -> int:
    p = argparse.ArgumentParser(description="arXiv search → JSONL")
    p.add_argument("query")
    p.add_argument("--max", type=int, default=20)
    p.add_argument("--category", default=None, help="e.g. cs.LG")
    p.add_argument("--out", required=True)
    args = p.parse_args()
    q = build_query(args.query, args.category)
    # search_query already contains encoded phrases; append other params encoded.
    rest = urllib.parse.urlencode({
        "start": 0,
        "max_results": args.max,
        "sortBy": "relevance",
        "sortOrder": "descending",
    })
    url = f"{API_URL}?search_query={q}&{rest}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            xml_text = resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        print(f"ERROR: arXiv request failed: {e}", file=sys.stderr)
        return 1
    rows = parse(xml_text)
    os.makedirs(os.path.dirname(os.path.abspath(args.out)) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"Wrote {len(rows)} papers → {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
