#!/usr/bin/env python3
"""Contract tests for the F3 skill and its checked-in sample."""
from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "skills" / "paper-deep-read" / "SKILL.md"
REPORT_TEMPLATE = ROOT / "skills" / "paper-deep-read" / "references" / "report-template.md"
SAMPLE = ROOT / "examples" / "f3-sample-run"


class F3ContractTests(unittest.TestCase):
    def test_skill_is_a_thin_nine_section_router(self) -> None:
        text = SKILL.read_text(encoding="utf-8")
        required = (
            "## 何时使用 / 何时不使用",
            "## 前置条件（依赖哪些技能、哪些文件须已存在）",
            "## 硬规则（禁止项）",
            "## 步骤（有序，可勾选）",
            "## 必须问人的点（停下条件与如何继续）",
            "## 交付契约（输入 / 输出路径与字段）",
            "## 脚本调用（若有，给命令模板）",
            "## 失败与回流",
            "## 参考（链接 references/）",
        )
        for heading in required:
            self.assertIn(heading, text)
        self.assertLessEqual(len(text.splitlines()), 85)
        self.assertIn("references/report-template.md", text)
        self.assertIn("stage: rough", text)
        self.assertIn("stage: deep", text)
        self.assertIn("waiting_user_pdf", text)
        self.assertNotIn("templates/", text)
        self.assertNotIn("winget install", text)
        self.assertNotIn('```json', text)

    def test_report_template_owns_content_and_evidence_rules(self) -> None:
        text = REPORT_TEMPLATE.read_text(encoding="utf-8")
        for marker in (
            "摘要级概览",
            "stage: rough",
            "stage: deep",
            "粗读判断复核",
            "作者明确陈述",
            "据模型分析",
            "| 主张 | 来源位置 | 证据类型 | 支持状态 | 限制 |",
        ):
            self.assertIn(marker, text)
        self.assertIn("不得进入全文细读", text)

    def test_sample_contains_only_the_three_final_artifacts(self) -> None:
        actual = {
            path.relative_to(SAMPLE).as_posix()
            for path in SAMPLE.rglob("*")
            if path.is_file()
        }
        self.assertEqual(
            {
                "references.json",
                "reading-reports/1810.04805.md",
                "reading-reports/1810.04805.pdf",
            },
            actual,
        )

    def test_sample_library_and_report_are_consistent(self) -> None:
        library = json.loads((SAMPLE / "references.json").read_text(encoding="utf-8"))
        papers = [paper for paper in library["papers"] if paper["id"] == "1810.04805"]
        self.assertEqual(1, len(papers))
        paper = papers[0]
        self.assertEqual("fulltext", paper["access_status"])
        self.assertEqual("read", paper["status"])
        self.assertEqual("reading-reports/1810.04805.md", paper["reading_report"])
        for field in ("problem", "method", "results", "limitations"):
            self.assertTrue(paper["reading_notes"][field])

        report = (SAMPLE / "reading-reports" / "1810.04805.md").read_text(encoding="utf-8")
        self.assertIn("paper_id: '1810.04805'", report)
        self.assertIn("stage: deep", report)
        self.assertIn("来源位置", report)
        self.assertIn("据模型分析", report)

        pdf = SAMPLE / "reading-reports" / "1810.04805.pdf"
        self.assertGreater(pdf.stat().st_size, 10_000)
        self.assertEqual(b"%PDF", pdf.read_bytes()[:4])


if __name__ == "__main__":
    unittest.main()
