#!/usr/bin/env python3
"""Deterministic F3 smoke: sample shape, safe upsert, encoding, and PDF presence."""

from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SAMPLE = ROOT / "examples" / "f3-sample-run"
UPSERT = ROOT / "skills" / "literature-reader" / "scripts" / "upsert_reference.py"
ENCODING = ROOT / "shared" / "scripts" / "check_encoding.py"


def run(command: list[str]) -> None:
    result = subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if result.returncode:
        raise RuntimeError(result.stdout + result.stderr)


def main() -> int:
    expected = {
        "references.json",
        "reading-reports/1810.04805.md",
        "reading-reports/1810.04805.pdf",
    }
    actual = {path.relative_to(SAMPLE).as_posix() for path in SAMPLE.rglob("*") if path.is_file()}
    if actual != expected:
        raise AssertionError(f"unexpected F3 sample files: {sorted(actual ^ expected)}")

    sample_library = json.loads((SAMPLE / "references.json").read_text(encoding="utf-8"))
    bert = next(paper for paper in sample_library["papers"] if paper["id"] == "1810.04805")
    with tempfile.TemporaryDirectory(prefix="mentor-f3-smoke-") as temp_dir:
        temp_root = Path(temp_dir)
        library_path = temp_root / "references.json"
        incoming_path = temp_root / "paper.json"
        base = copy.deepcopy(sample_library)
        base_bert = next(paper for paper in base["papers"] if paper["id"] == "1810.04805")
        base_bert["custom"] = {"human_checked": True}
        incoming = copy.deepcopy(bert)
        incoming["title"] = ""
        incoming["access_status"] = "abstract_only"
        library_path.write_text(json.dumps(base, ensure_ascii=False), encoding="utf-8")
        incoming_path.write_text(json.dumps(incoming, ensure_ascii=False), encoding="utf-8")

        run([sys.executable, str(UPSERT), str(library_path), str(incoming_path)])
        merged = json.loads(library_path.read_text(encoding="utf-8"))
        merged_bert = next(paper for paper in merged["papers"] if paper["id"] == "1810.04805")
        assert merged_bert["access_status"] == "fulltext"
        assert merged_bert["custom"]["human_checked"] is True
        assert merged_bert["reading_notes"]["problem"]

    run([
        sys.executable,
        str(ENCODING),
        str(SAMPLE / "references.json"),
        str(SAMPLE / "reading-reports" / "1810.04805.md"),
        str(ROOT / "skills" / "paper-deep-read"),
    ])
    pdf = SAMPLE / "reading-reports" / "1810.04805.pdf"
    if pdf.stat().st_size <= 10_000 or pdf.read_bytes()[:4] != b"%PDF":
        raise AssertionError("sample PDF is missing or invalid")

    print("F3 script smoke OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
