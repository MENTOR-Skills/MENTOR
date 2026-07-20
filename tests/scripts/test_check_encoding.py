#!/usr/bin/env python3
"""Tests for the shared UTF-8 encoding checker."""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CHECKER = ROOT / "shared" / "scripts" / "check_encoding.py"


class CheckEncodingCliTests(unittest.TestCase):
    def run_checker(self, *targets: Path) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        return subprocess.run(
            [sys.executable, str(CHECKER), *(str(target) for target in targets)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=env,
            check=False,
        )

    def test_explicit_file_is_strictly_decoded_regardless_of_extension(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "invalid.txt"
            target.write_bytes(b"\xff")

            result = self.run_checker(target)

        self.assertEqual(1, result.returncode)
        self.assertIn("FAIL Not UTF-8", result.stdout)

    def test_all_targets_are_checked_and_any_failure_sets_exit_one(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            valid = root / "valid.md"
            invalid = root / "invalid.json"
            valid.write_text("valid", encoding="utf-8")
            invalid.write_bytes(b"\xff")

            result = self.run_checker(valid, invalid)

        self.assertEqual(1, result.returncode)
        self.assertIn(str(invalid), result.stdout)

    def test_directory_recurses_supported_extensions_and_ignores_others(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            nested = root / "nested"
            nested.mkdir()
            (nested / "valid.yaml").write_text("key: value", encoding="utf-8")
            (nested / "ignored.txt").write_bytes(b"\xff")

            result = self.run_checker(root)

        self.assertEqual(0, result.returncode)
        self.assertIn("OK All files are UTF-8.", result.stdout)

    def test_missing_target_fails_even_when_another_target_is_valid(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            valid = root / "valid.md"
            missing = root / "missing"
            valid.write_text("valid", encoding="utf-8")

            result = self.run_checker(valid, missing)

        self.assertEqual(1, result.returncode)
        self.assertIn(f"Path not found: {missing}", result.stdout)

    def test_no_supported_files_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "ignored.txt").write_text("valid", encoding="utf-8")

            result = self.run_checker(root)

        self.assertEqual(1, result.returncode)
        self.assertNotIn("OK All files are UTF-8.", result.stdout)

    def test_utf8_bom_is_reported_as_warning_without_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "bom.md"
            target.write_bytes(b"\xef\xbb\xbfcontent")

            result = self.run_checker(target)

        self.assertEqual(0, result.returncode)
        self.assertIn(f"WARNING UTF-8 with BOM: {target}", result.stdout)


if __name__ == "__main__":
    unittest.main()
