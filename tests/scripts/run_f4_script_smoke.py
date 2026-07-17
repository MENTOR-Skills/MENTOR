#!/usr/bin/env python3
"""F4 script smoke: list_recent_files → validate_progress_paths on fixture.

Writes into tests/runs/f4-script-smoke/ under the MENTOR repo root.
Does not invent progress prose (that needs an agent); validates expected/*.md paths.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / "tests" / "runs" / "f4-script-smoke"
PROJECT = ROOT / "examples" / "f4-sample-run" / "project"
EXPECTED = ROOT / "examples" / "f4-sample-run" / "expected"
SCRIPTS = ROOT / "skills" / "progress-digest" / "scripts"


def run(cmd: list[str]) -> None:
    print("+", " ".join(cmd))
    subprocess.check_call(cmd, cwd=ROOT)


def main() -> int:
    if RUN.exists():
        shutil.rmtree(RUN)
    work = RUN / "_work"
    work.mkdir(parents=True)

    (RUN / "scope.md").write_text(
        "# 研究范围说明\n"
        "- 主题：F4 脚本冒烟（toy-train 夹具）\n"
        "- 时间范围：最近 30 天\n"
        "- 深度档：标准\n"
        "- 允许扫描的本地路径（F4 专用）：\n"
        f"  - {PROJECT.as_posix()}\n"
        "- 用户已确认：冒烟用例\n",
        encoding="utf-8",
    )

    out_jsonl = work / "recent-files.jsonl"
    run(
        [
            sys.executable,
            str(SCRIPTS / "list_recent_files.py"),
            "--roots",
            str(PROJECT),
            "--since",
            "30d",
            "--out",
            str(out_jsonl),
        ]
    )

    if not out_jsonl.is_file() or out_jsonl.stat().st_size == 0:
        print("error: recent-files.jsonl empty or missing", file=sys.stderr)
        return 1

    text = out_jsonl.read_text(encoding="utf-8")
    if "train.py" not in text and "metrics.csv" not in text:
        print("error: expected project files not listed", file=sys.stderr)
        return 1

    # Copy expected deliverables into run dir for encoding check + local validate option
    for name in (
        "artifact-index.md",
        "progress-report.md",
        "result-summary.md",
        "blockers.md",
    ):
        shutil.copy2(EXPECTED / name, RUN / name)

    # Paths inside expected/*.md are relative to MENTOR root
    run(
        [
            sys.executable,
            str(SCRIPTS / "validate_progress_paths.py"),
            "--workspace",
            str(ROOT),
            str(EXPECTED / "artifact-index.md"),
            str(EXPECTED / "progress-report.md"),
            str(EXPECTED / "result-summary.md"),
            str(EXPECTED / "blockers.md"),
        ]
    )

    run(
        [
            sys.executable,
            str(ROOT / "shared" / "scripts" / "check_encoding.py"),
            str(RUN),
        ]
    )

    print("F4 script smoke OK ->", RUN)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
