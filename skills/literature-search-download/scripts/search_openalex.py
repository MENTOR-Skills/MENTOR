#!/usr/bin/env python3
"""Search OpenAlex and write normalized papers JSONL. Stdlib only. No API key.

Adapted from dsebastien/ai-skill-scholar (simplified for demo).
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

API_BASE = "https://api.openalex.org"
USER_AGENT = "literature-survey-demo/1.0"
SELECT = (
    "id,title,publication_year,cited_by_count,authorships,ids,doi,"
    "open_access,primary_location,abstract_inverted_index,type"
)
_ARXIV_DOI_RE = re.compile(r"10\.48550/arxiv\.(\S+?)(?:v\d+)?$", re.I)
_ARXIV_URL_RE = re.compile(r"arxiv\.org/(?:abs|pdf)/([^\s?#/]+)", re.I)


def reconstruct_abstract(inv_idx: dict | None) -> str:
    if not inv_idx:
        return ""
    slots: list[tuple[int, str]] = []
    for word, positions in inv_idx.items():
        for p in positions:
            slots.append((p, word))
    slots.sort()
    return " ".join(w for _, w in slots)


def extract_arxiv_id(work: dict) -> str | None:
    doi = (work.get("doi") or "").lower().replace("https://doi.org/", "")
    m = _ARXIV_DOI_RE.search(doi) if doi else None
    if m:
        return m.group(1)
    pl = work.get("primary_location") or {}
    source = pl.get("source") or {}
    landing = pl.get("landing_page_url") or ""
    if "arxiv" in (source.get("display_name") or "").lower() or "arxiv.org" in landing:
        m = _ARXIV_URL_RE.search(landing)
        if m:
            return m.group(1).replace(".pdf", "")
    ids = work.get("ids") or {}
    for key in ("openalex",):
        pass
    if ids.get("arxiv"):
        return str(ids["arxiv"]).replace("https://arxiv.org/abs/", "")
    return None


def normalize(work: dict) -> dict:
    pl = work.get("primary_location") or {}
    source = pl.get("source") or {}
    oa = work.get("open_access") or {}
    doi = work.get("doi")
    if doi:
        doi = doi.replace("https://doi.org/", "")
    venue = source.get("display_name") or ""
    pdf_url = oa.get("oa_url") or pl.get("pdf_url")
    arxiv_id = extract_arxiv_id(work)
    if not pdf_url and arxiv_id:
        pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    peer = None
    vtype = (source.get("type") or "").lower()
    if vtype in ("journal", "conference"):
        peer = True
    elif "arxiv" in venue.lower():
        peer = False
    return {
        "id": (work.get("id") or "").replace("https://openalex.org/", "") or None,
        "title": work.get("title") or "",
        "authors": [
            (a.get("author") or {}).get("display_name", "")
            for a in (work.get("authorships") or [])
        ],
        "year": work.get("publication_year"),
        "venue": venue,
        "doi": doi,
        "arxiv_id": arxiv_id,
        "abstract": reconstruct_abstract(work.get("abstract_inverted_index")),
        "pdf_url": pdf_url,
        "pdf_path": None,
        "landing_url": pl.get("landing_page_url"),
        "access_status": "pending",
        "peer_reviewed": peer,
        "cited_by_count": work.get("cited_by_count"),
        "source": "openalex",
    }


def http_get_json(url: str) -> dict:
    email = os.environ.get("OPENALEX_EMAIL")
    ua = f"{USER_AGENT} (mailto:{email})" if email else USER_AGENT
    req = urllib.request.Request(url, headers={"User-Agent": ua, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=45) as resp:
        return json.loads(resp.read().decode("utf-8", errors="replace"))


def search(query: str, limit: int, year: str | None, venue: str | None, min_citations: int | None) -> list[dict]:
    filters: list[str] = []
    if year:
        if "-" in year:
            y0, y1 = year.split("-", 1)
            filters.append(f"from_publication_date:{y0.strip()}-01-01")
            filters.append(f"to_publication_date:{y1.strip()}-12-31")
        else:
            y = year.strip()
            filters.append(f"from_publication_date:{y}-01-01")
            filters.append(f"to_publication_date:{y}-12-31")
    if venue:
        filters.append(f"primary_location.source.display_name.search:{venue}")
    if min_citations is not None:
        filters.append(f"cited_by_count:>{min_citations - 1}")
    params: dict[str, str] = {
        "search": query,
        "per_page": str(min(limit, 50)),
        "select": SELECT,
    }
    # Relevance ranking by default; only sort by citations when user asks via min filter alone
    if min_citations is not None and not query.strip():
        params["sort"] = "cited_by_count:desc"
    if filters:
        params["filter"] = ",".join(filters)
    if os.environ.get("OPENALEX_EMAIL"):
        params["mailto"] = os.environ["OPENALEX_EMAIL"]
    url = f"{API_BASE}/works?" + urllib.parse.urlencode(params)
    data = http_get_json(url)
    return [normalize(w) for w in (data.get("results") or [])][:limit]


def _parse_venues(venue: str | None, venues: str | None) -> list[str | None]:
    """Return list of venue filters; [None] means one unfiltered search."""
    items: list[str] = []
    if venue:
        items.append(venue.strip())
    if venues:
        items.extend(v.strip() for v in venues.split(",") if v.strip())
    return items or [None]


def main() -> int:
    p = argparse.ArgumentParser(description="OpenAlex literature search → JSONL")
    p.add_argument("query")
    p.add_argument("--limit", type=int, default=25)
    p.add_argument("--year", default=None, help="e.g. 2022-2026")
    p.add_argument("--venue", default=None, help="Single venue filter (user-provided)")
    p.add_argument("--venues", default=None, help="Comma-separated venues (user-provided)")
    p.add_argument("--min-citations", type=int, default=None)
    p.add_argument("--out", required=True, help="Output JSONL path")
    args = p.parse_args()
    venue_list = _parse_venues(args.venue, args.venues)
    per_venue_limit = max(5, args.limit // max(1, len([v for v in venue_list if v])) if any(venue_list) else args.limit)
    results: list[dict] = []
    seen: set[str] = set()
    try:
        for v in venue_list:
            lim = per_venue_limit if v else args.limit
            batch = search(args.query, lim, args.year, v, args.min_citations)
            for row in batch:
                key = (row.get("doi") or row.get("arxiv_id") or row.get("id") or row.get("title") or "").lower()
                if key and key not in seen:
                    seen.add(key)
                    results.append(row)
            time.sleep(0.25)
    except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError) as e:
        print(f"ERROR: OpenAlex request failed: {e}", file=sys.stderr)
        return 1
    results = results[: args.limit]
    out_path = args.out
    os.makedirs(os.path.dirname(os.path.abspath(out_path)) or ".", exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        for row in results:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"Wrote {len(results)} papers → {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
