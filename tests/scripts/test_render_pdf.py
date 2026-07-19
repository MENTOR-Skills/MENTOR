#!/usr/bin/env python3
"""Failure-path tests for the F3 PDF renderer."""
from __future__ import annotations

import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "skills" / "paper-deep-read" / "scripts" / "render_pdf.py"
SPEC = importlib.util.spec_from_file_location("f3_render_pdf", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class RenderPdfTests(unittest.TestCase):
    def make_note(self, root: Path) -> Path:
        note = root / "paper.md"
        note.write_text("---\ntitle: test\n---\n\n## Body\n", encoding="utf-8")
        return note

    def test_renderer_uses_assets_not_references_for_latex_resources(self) -> None:
        self.assertEqual("assets", MODULE.TEMPLATE.parent.name)
        self.assertEqual("assets", MODULE.METADATA.parent.name)

    def test_rejects_output_equal_to_markdown_input(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            note = self.make_note(Path(temp_dir))
            original = note.read_bytes()
            self.assertEqual(2, MODULE.render(note, note))
            self.assertEqual(original, note.read_bytes())

    def test_rejects_non_pdf_output(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            note = self.make_note(root)
            self.assertEqual(2, MODULE.render(note, root / "paper.txt"))
            self.assertFalse((root / "paper.txt").exists())

    def test_missing_dependency_leaves_no_build_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            note = self.make_note(root)
            with patch.object(MODULE, "find_executable", return_value=None):
                self.assertEqual(3, MODULE.render(note))
            self.assertFalse((root / "build").exists())

    def test_failed_render_preserves_old_pdf_and_cleans_temp_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            note = self.make_note(root)
            output = note.with_suffix(".pdf")
            output.write_bytes(b"old-pdf")
            failed = subprocess.CompletedProcess([], 1, "", "failed")
            with patch.object(MODULE, "find_executable", side_effect=lambda name: f"C:/{name}.exe"), patch.object(
                MODULE.subprocess, "run", return_value=failed
            ):
                self.assertEqual(1, MODULE.render(note))
            self.assertEqual(b"old-pdf", output.read_bytes())
            self.assertFalse((root / "build").exists())
            self.assertEqual([], list(root.glob("*.tmp.pdf")))

    def test_success_atomically_replaces_pdf_and_cleans_temp_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            note = self.make_note(root)
            output = note.with_suffix(".pdf")
            output.write_bytes(b"old-pdf")

            def fake_run(command: list[str], **_: object) -> subprocess.CompletedProcess[str]:
                temp_pdf = Path(command[command.index("-o") + 1])
                temp_pdf.write_bytes(b"%PDF-new")
                return subprocess.CompletedProcess(command, 0, "", "")

            with patch.object(MODULE, "find_executable", side_effect=lambda name: f"C:/{name}.exe"), patch.object(
                MODULE.subprocess, "run", side_effect=fake_run
            ):
                self.assertEqual(0, MODULE.render(note))

            self.assertEqual(b"%PDF-new", output.read_bytes())
            self.assertEqual([], list(root.glob(".paper-deep-read-*")))


if __name__ == "__main__":
    unittest.main()
