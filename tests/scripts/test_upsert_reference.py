#!/usr/bin/env python3
"""CLI tests for safe single-paper updates to references.json."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "skills" / "literature-reader" / "scripts" / "upsert_reference.py"


class UpsertReferenceTests(unittest.TestCase):
    def run_upsert(self, library: Path, incoming: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(library), str(incoming)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

    def write_json(self, path: Path, data: object) -> None:
        path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    def test_merge_preserves_human_fields_and_fulltext_status(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            library = root / "references.json"
            incoming = root / "paper.json"
            self.write_json(library, {"meta": {"topic": "x"}, "papers": [{
                "id": "p1", "title": "Old", "access_status": "fulltext",
                "custom": {"human_checked": True},
                "relations": [{"target_id": "p2"}],
                "reading_notes": {"problem": "old", "method": "keep"},
            }]})
            self.write_json(incoming, {
                "id": "p1", "title": "", "access_status": "abstract_only",
                "reading_notes": {"problem": "new", "method": ""},
            })

            result = self.run_upsert(library, incoming)

            self.assertEqual(0, result.returncode, result.stderr)
            paper = json.loads(library.read_text(encoding="utf-8"))["papers"][0]
            self.assertEqual("Old", paper["title"])
            self.assertEqual("fulltext", paper["access_status"])
            self.assertEqual({"problem": "new", "method": "keep"}, paper["reading_notes"])
            self.assertTrue(paper["custom"]["human_checked"])
            self.assertEqual([{"target_id": "p2"}], paper["relations"])

    def test_identifier_conflict_fails_without_changing_library(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            library = root / "references.json"
            incoming = root / "paper.json"
            self.write_json(library, {"meta": {}, "papers": [{
                "id": "p1", "title": "One", "arxiv_id": "1810.04805"
            }]})
            self.write_json(incoming, {"id": "p2", "title": "Two", "arxiv_id": "1810.04805"})
            original = library.read_bytes()

            result = self.run_upsert(library, incoming)

            self.assertNotEqual(0, result.returncode)
            self.assertIn("identifier conflict", result.stderr)
            self.assertEqual(original, library.read_bytes())

    def test_invalid_library_is_not_rewritten(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            library = root / "references.json"
            incoming = root / "paper.json"
            library.write_text("{broken", encoding="utf-8")
            self.write_json(incoming, {"id": "p1"})
            original = library.read_bytes()

            result = self.run_upsert(library, incoming)

            self.assertNotEqual(0, result.returncode)
            self.assertEqual(original, library.read_bytes())

    def test_creates_new_library_for_complete_paper(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            library = root / "references.json"
            incoming = root / "paper.json"
            self.write_json(incoming, {
                "id": "p1", "title": "Paper", "authors": ["A"], "year": 2026,
                "venue": "Test", "access_status": "fulltext",
            })

            result = self.run_upsert(library, incoming)

            self.assertEqual(0, result.returncode, result.stderr)
            data = json.loads(library.read_text(encoding="utf-8"))
            self.assertEqual("p1", data["papers"][0]["id"])


if __name__ == "__main__":
    unittest.main()
