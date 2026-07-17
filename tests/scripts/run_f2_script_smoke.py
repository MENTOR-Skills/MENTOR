#!/usr/bin/env python3
"""F2 script smoke: arxiv search → wait gate → viz → citation verify.

Writes into tests/runs/f2-script-smoke/ under the MENTOR repo root.
Does not invent reading notes or survey prose (those need an agent).
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / "tests" / "runs" / "f2-script-smoke"
EXAMPLE_REFS = ROOT / "examples" / "sample-topic" / "references.json"


def run(cmd: list[str]) -> None:
    print("+", " ".join(cmd))
    subprocess.check_call(cmd, cwd=ROOT)


def main() -> int:
    if RUN.exists():
        shutil.rmtree(RUN)
    work = RUN / "_work"
    work.mkdir(parents=True)
    (RUN / "pdfs" / "auto").mkdir(parents=True)
    (RUN / "pdfs" / "user").mkdir(parents=True)
    (RUN / "viz").mkdir(parents=True)

    (RUN / "scope.md").write_text(
        "# 研究范围说明\n"
        "- 主题：transformer attention（脚本冒烟）\n"
        "- 时间范围：不限\n"
        "- 深度档：标准\n"
        "- 用户已确认：冒烟用例\n",
        encoding="utf-8",
    )

    search = ROOT / "skills" / "literature-search-download" / "scripts"
    run(
        [
            sys.executable,
            str(search / "search_arxiv.py"),
            "transformer attention",
            "--max",
            "3",
            "--out",
            str(work / "arxiv.jsonl"),
        ]
    )

    # Minimal shortlist for wait-gate (no PDF yet)
    items = []
    with open(work / "arxiv.jsonl", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                items.append(json.loads(line))
    shortlist = {"items": items[:3]}
    for it in shortlist["items"]:
        it["access_status"] = "waiting_user_pdf"
        it["pdf_path"] = None
    (work / "shortlist.json").write_text(
        json.dumps(shortlist, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    run(
        [
            sys.executable,
            str(search / "write_wait_gate.py"),
            "--shortlist",
            str(work / "shortlist.json"),
            "--out",
            str(work / "WAITING_user_pdf.md"),
        ]
    )

    # Use frozen sample references for viz + citation (stable OA ids)
    refs_dst = RUN / "references.json"
    shutil.copy2(EXAMPLE_REFS, refs_dst)

    viz = ROOT / "skills" / "survey-visualizer" / "scripts" / "build_viz.py"
    run(
        [
            sys.executable,
            str(viz),
            "--references",
            str(refs_dst),
            "--out",
            str(RUN / "viz" / "index.html"),
            "--title",
            "F2 Script Smoke",
        ]
    )

    ver = ROOT / "skills" / "citation-verifier" / "scripts"
    run(
        [
            sys.executable,
            str(ver / "refs_to_verify_input.py"),
            "--references",
            str(refs_dst),
            "--out",
            str(work / "candidates_for_verify.json"),
        ]
    )
    run(
        [
            sys.executable,
            str(ver / "verify_citations.py"),
            "--input",
            str(work / "candidates_for_verify.json"),
            "--output",
            str(work / "CITATION_AUDIT.json"),
            "--md",
            str(work / "CITATION_AUDIT.md"),
        ]
    )

    enc = ROOT / "shared" / "scripts" / "check_encoding.py"
    run([sys.executable, str(enc), str(RUN)])

    print("\nOK smoke →", RUN)
    print("See examples/f2-script-smoke/README.md for expected deliverables.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
