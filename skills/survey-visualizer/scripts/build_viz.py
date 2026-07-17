#!/usr/bin/env python3
"""Build single-file HTML from references.json. Stdlib only.

Includes year/venue/access charts and an optional relation graph.
Never invents papers or edges not present in references.json.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys
from collections import Counter
from html import escape


def load_refs(path: str) -> dict:
    with open(path, encoding="utf-8-sig") as f:
        return json.load(f)


def bar_rows(counter: Counter, max_n: int = 12) -> str:
    if not counter:
        return "<p class='muted'>No data</p>"
    items = counter.most_common(max_n)
    m = max(v for _, v in items) or 1
    parts = []
    for k, v in items:
        pct = 100.0 * v / m
        parts.append(
            f"<div class='bar'><span class='lab'>{escape(str(k))}</span>"
            f"<span class='track'><span class='fill' style='width:{pct:.1f}%'></span></span>"
            f"<span class='n'>{v}</span></div>"
        )
    return "\n".join(parts)


def short_label(paper: dict, max_len: int = 28) -> str:
    title = str(paper.get("title") or paper.get("id") or "?")
    year = paper.get("year")
    prefix = f"{year} · " if year else ""
    s = prefix + title
    if len(s) > max_len:
        return s[: max_len - 1] + "…"
    return s


def collect_edges(papers: list) -> list[dict]:
    id_set = {str(p.get("id")) for p in papers if p.get("id")}
    edges = []
    for p in papers:
        src = p.get("id")
        if not src:
            continue
        for rel in p.get("relations") or []:
            if not isinstance(rel, dict):
                continue
            tgt = rel.get("target_id")
            if not tgt or str(tgt) not in id_set:
                continue
            basis = rel.get("basis") or "inferred"
            if basis not in ("fact", "inferred"):
                basis = "inferred"
            edges.append(
                {
                    "source": str(src),
                    "target": str(tgt),
                    "kind": str(rel.get("kind") or "related"),
                    "basis": basis,
                }
            )
    return edges


def layout_nodes(papers: list, width: int = 720, height: int = 420) -> dict[str, tuple[float, float]]:
    """Simple circular layout; deterministic, no external deps."""
    ids = [str(p.get("id")) for p in papers if p.get("id")]
    n = len(ids)
    cx, cy = width / 2, height / 2
    r = min(width, height) * 0.38
    pos: dict[str, tuple[float, float]] = {}
    if n == 0:
        return pos
    if n == 1:
        pos[ids[0]] = (cx, cy)
        return pos
    for i, pid in enumerate(ids):
        ang = 2 * math.pi * i / n - math.pi / 2
        pos[pid] = (cx + r * math.cos(ang), cy + r * math.sin(ang))
    return pos


def relation_svg(papers: list, edges: list[dict]) -> str:
    if not papers:
        return "<p class='muted'>No papers</p>"
    width, height = 720, 420
    pos = layout_nodes(papers, width, height)
    id_to_paper = {str(p.get("id")): p for p in papers if p.get("id")}

    parts = [
        f'<svg viewBox="0 0 {width} {height}" width="100%" role="img" '
        f'aria-label="Paper relation graph">'
        '<defs>'
        '<marker id="arrow-fact" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">'
        '<path d="M0,0 L6,3 L0,6 Z" fill="#0f766e"/></marker>'
        '<marker id="arrow-inf" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">'
        '<path d="M0,0 L6,3 L0,6 Z" fill="#a8a29e"/></marker>'
        "</defs>"
    ]

    if not edges:
        parts.append(
            '<text x="24" y="32" class="svg-muted">No relations in references.json '
            "(statistics only; edges are not invented).</text>"
        )
    else:
        for e in edges:
            if e["source"] not in pos or e["target"] not in pos:
                continue
            x1, y1 = pos[e["source"]]
            x2, y2 = pos[e["target"]]
            # shorten toward target so arrowhead clears the node
            dx, dy = x2 - x1, y2 - y1
            dist = math.hypot(dx, dy) or 1
            shrink = 18
            x2s = x2 - shrink * dx / dist
            y2s = y2 - shrink * dy / dist
            x1s = x1 + shrink * dx / dist
            y1s = y1 + shrink * dy / dist
            inferred = e["basis"] == "inferred"
            stroke = "#a8a29e" if inferred else "#0f766e"
            dash = ' stroke-dasharray="6 4"' if inferred else ""
            marker = "arrow-inf" if inferred else "arrow-fact"
            title = escape(f"{e['kind']} ({e['basis']})")
            parts.append(
                f'<line x1="{x1s:.1f}" y1="{y1s:.1f}" x2="{x2s:.1f}" y2="{y2s:.1f}" '
                f'stroke="{stroke}" stroke-width="2"{dash} marker-end="url(#{marker})">'
                f"<title>{title}</title></line>"
            )

    for pid, (x, y) in pos.items():
        p = id_to_paper.get(pid, {})
        label = escape(short_label(p))
        parts.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="14" fill="#fff" stroke="#0f766e" stroke-width="2">'
            f"<title>{escape(str(p.get('title') or pid))}</title></circle>"
            f'<text x="{x:.1f}" y="{y + 32:.1f}" text-anchor="middle" class="svg-lab">{label}</text>'
        )

    parts.append("</svg>")
    legend = (
        '<div class="legend">'
        '<span><i class="sw solid"></i> fact</span>'
        '<span><i class="sw dash"></i> inferred</span>'
        f'<span class="muted">{len(edges)} edge(s)</span>'
        "</div>"
    )
    return legend + "\n".join(parts)


def access_bucket(paper: dict) -> str:
    status = paper.get("access_status")
    if status in ("fulltext", "abstract_only", "waiting_user_pdf", "unknown"):
        return str(status)
    # legacy demo values
    legacy = {
        "oa_pdf": "fulltext",
        "arxiv_pdf": "fulltext",
        "user_pdf": "fulltext",
        "metadata_only": "waiting_user_pdf",
        "failed": "waiting_user_pdf",
    }
    if status in legacy:
        return legacy[status]
    if paper.get("pdf_path"):
        return "fulltext"
    if paper.get("fulltext") is True:
        return "fulltext"
    if paper.get("fulltext") is False:
        return "abstract_only"
    return str(status or "unknown")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--references", required=True)
    ap.add_argument("--title", default="Literature Landscape")
    args = ap.parse_args()

    if not os.path.isfile(args.references):
        print("ERROR: references.json missing; refusing to invent charts", file=sys.stderr)
        return 1
    data = load_refs(args.references)
    papers = data.get("papers") if isinstance(data, dict) else data
    if not papers:
        print("ERROR: no papers in references.json", file=sys.stderr)
        return 1

    years = Counter(str(p.get("year") or "unknown") for p in papers)
    venues = Counter(str(p.get("venue") or "unknown")[:40] for p in papers)
    access = Counter(access_bucket(p) for p in papers)
    fulltext = Counter(
        "fulltext" if access_bucket(p) == "fulltext" else "not_fulltext" for p in papers
    )
    edges = collect_edges(papers)
    rel_html = relation_svg(papers, edges)

    rows = []
    for p in papers:
        rows.append(
            "<tr>"
            f"<td>{escape(str(p.get('year') or ''))}</td>"
            f"<td>{escape(str(p.get('venue') or ''))}</td>"
            f"<td>{escape(str(p.get('title') or ''))}</td>"
            f"<td>{escape(access_bucket(p))}</td>"
            f"<td>{escape(str(p.get('doi') or p.get('arxiv_id') or p.get('id') or ''))}</td>"
            "</tr>"
        )

    audit = (data.get("meta") or {}).get("audit") if isinstance(data, dict) else None
    audit_html = "<p class='muted'>No audit in meta</p>"
    if isinstance(audit, dict):
        audit_html = (
            f"<p><strong>verdict:</strong> {escape(str(audit.get('verdict')))} — "
            f"{escape(str(audit.get('summary') or ''))}</p>"
        )

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{escape(args.title)}</title>
<style>
:root {{ --bg:#f7f4ef; --ink:#1c1917; --accent:#0f766e; --card:#fff; --muted:#78716c; }}
body {{ margin:0; font-family:"Segoe UI","PingFang SC","Noto Sans SC",sans-serif;
  background:linear-gradient(160deg,#f7f4ef,#e7eef0 50%,#f0ebe3); color:var(--ink); }}
header {{ padding:2.5rem 1.5rem 1rem; max-width:960px; margin:0 auto; }}
h1 {{ font-size:1.75rem; margin:0 0 .5rem; }}
.sub {{ color:var(--muted); }}
main {{ max-width:960px; margin:0 auto; padding:0 1.5rem 3rem; display:grid; gap:1rem; }}
section {{ background:var(--card); border-radius:12px; padding:1.25rem 1.5rem; box-shadow:0 1px 0 rgba(28,25,23,.06); }}
h2 {{ font-size:1.05rem; margin:0 0 1rem; color:var(--accent); }}
.bar {{ display:grid; grid-template-columns:140px 1fr 2rem; gap:.5rem; align-items:center; margin:.35rem 0; }}
.lab {{ font-size:.8rem; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }}
.track {{ background:#e7e5e4; border-radius:999px; height:10px; overflow:hidden; }}
.fill {{ display:block; height:100%; background:var(--accent); border-radius:999px; }}
.n {{ font-size:.8rem; text-align:right; }}
table {{ width:100%; border-collapse:collapse; font-size:.85rem; }}
th,td {{ border-bottom:1px solid #e7e5e4; padding:.45rem .35rem; text-align:left; vertical-align:top; }}
th {{ color:var(--muted); font-weight:600; }}
.muted {{ color:var(--muted); }}
.legend {{ display:flex; gap:1.25rem; flex-wrap:wrap; font-size:.85rem; margin-bottom:.75rem; align-items:center; }}
.legend .sw {{ display:inline-block; width:28px; height:0; border-top:3px solid #0f766e; vertical-align:middle; margin-right:.35rem; }}
.legend .sw.dash {{ border-top-style:dashed; border-top-color:#a8a29e; }}
svg .svg-lab {{ font-size:11px; fill:var(--ink); }}
svg .svg-muted {{ font-size:13px; fill:var(--muted); }}
footer {{ max-width:960px; margin:0 auto; padding:0 1.5rem 2rem; font-size:.75rem; color:var(--muted); }}
</style>
</head>
<body>
<header>
  <h1>{escape(args.title)}</h1>
  <p class="sub">From references.json · {len(papers)} papers · relations not invented</p>
</header>
<main>
  <section><h2>关系图</h2>{rel_html}</section>
  <section><h2>年份</h2>{bar_rows(years)}</section>
  <section><h2>Venue</h2>{bar_rows(venues)}</section>
  <section><h2>获取方式 (access_status)</h2>{bar_rows(access)}</section>
  <section><h2>全文覆盖</h2>{bar_rows(fulltext)}</section>
  <section><h2>核验摘要</h2>{audit_html}</section>
  <section>
    <h2>文献表</h2>
    <table>
      <thead><tr><th>Year</th><th>Venue</th><th>Title</th><th>Access</th><th>ID</th></tr></thead>
      <tbody>{''.join(rows)}</tbody>
    </table>
  </section>
</main>
<footer>MENTOR · survey-visualizer · data from references.json only</footer>
</body>
</html>
"""
    os.makedirs(os.path.dirname(os.path.abspath(args.out)) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Wrote {args.out} (papers={len(papers)}, edges={len(edges)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
