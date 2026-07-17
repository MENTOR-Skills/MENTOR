#!/usr/bin/env python3
"""Write _work/WAITING_user_pdf.md from shortlist + access info (MENTOR protocol)."""
from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone


PROTOCOL_STATUS = {
    "fulltext",
    "abstract_only",
    "waiting_user_pdf",
    "unknown",
}


def normalize_status(raw: str | None, has_pdf: bool) -> str:
    if has_pdf:
        return "fulltext"
    if not raw:
        return "waiting_user_pdf"
    # legacy demo statuses
    legacy = {
        "oa_pdf": "fulltext",
        "arxiv_pdf": "fulltext",
        "user_pdf": "fulltext",
        "ok": "fulltext",
        "metadata_only": "waiting_user_pdf",
        "failed": "waiting_user_pdf",
        "need_user_pdf": "waiting_user_pdf",
        "pending": "waiting_user_pdf",
    }
    if raw in PROTOCOL_STATUS:
        return raw
    return legacy.get(raw, "waiting_user_pdf")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--shortlist", required=True)
    p.add_argument("--out", required=True)
    args = p.parse_args()
    with open(args.shortlist, encoding="utf-8-sig") as f:
        data = json.load(f)
    items = data.get("items") if isinstance(data, dict) else data

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    lines = [
        "# 等待事项：补充付费墙 / 非 OA 全文 PDF",
        "",
        "- 当前状态：已对 shortlist 尝试 OA / arXiv 自动下载；下列条目仍无可用全文。",
        "- 你需要做：通过学校图书馆、学会会员等渠道获取 PDF，放入 `pdfs/user/`（文件名建议含 doi 或 shortlist id），然后回复「已补充」或继续。",
        "- 完成后我将：运行 `register_user_pdfs.py`，进入 `literature-reader` 精读入库。",
        f"- 创建时间：{now}",
        "",
        "自动通道仅尝试 **OA / arXiv**，不会绕过付费墙。",
        "",
        "| # | Title | Year | Venue | DOI / arXiv | Landing | access_status |",
        "|---|-------|------|-------|-------------|---------|---------------|",
    ]
    need = 0
    for i, x in enumerate(items, 1):
        path = x.get("pdf_path")
        ok = bool(path and os.path.isfile(path))
        status = normalize_status(x.get("access_status"), ok)
        if status != "fulltext":
            need += 1
        lines.append(
            f"| {i} | {x.get('title', '')} | {x.get('year', '')} | {x.get('venue', '')} | "
            f"{x.get('doi') or x.get('arxiv_id') or ''} | "
            f"{x.get('landing_url') or x.get('url') or ''} | {status} |"
        )
    lines += [
        "",
        f"**仍需用户提供或明确允许摘要级：{need} 篇**",
        "",
        "若你同意对缺失全文仅用摘要精读，请明确说明；对应条目将标为 `abstract_only`。",
        "",
        "请同步确认：调度侧应更新 `_work/state.yaml` → `waiting_for: user_pdf`。",
        "",
    ]
    os.makedirs(os.path.dirname(os.path.abspath(args.out)) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Wrote {args.out} (need_user={need})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
