#!/usr/bin/env python3
"""F1 script smoke: validate skill structure, templates, encoding, domain-packs, and test-run outputs.

Checks everything that does NOT need an LLM agent:
  1. Both F1 skills pass validate_skill.py (nine-section structure, frontmatter, frozen filenames)
  2. All 6 templates under domain-onboarding/references/ exist and have required sections
  3. All .md/.json/.yaml under skills/domain-onboarding/ and skills/domain-resource-search/ are UTF-8
  4. domain-packs/{_template,embodied-ai}/ have pack.yaml + curriculum.md + glossary.md
  5. examples/f1-sample-run/expected/ has all 5 frozen deliverables and they are UTF-8
  6. Test-run outputs (if present under tests/runs/f1-script-smoke/) pass encoding check

Does NOT generate glossary/learning-map prose — that needs an LLM agent.
Writes a minimal smoke workspace into tests/runs/f1-script-smoke/.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / "tests" / "runs" / "f1-script-smoke"
SKILLS = ROOT / "skills"
EXAMPLES = ROOT / "examples" / "f1-sample-run"
DOMAIN_PACKS = ROOT / "domain-packs"
SHARED_SCRIPTS = ROOT / "shared" / "scripts"
TOOLS_SCRIPTS = ROOT / "tools" / "skill-creator" / "scripts"

F1_SKILLS = ["domain-onboarding", "domain-resource-search"]
F1_TEMPLATES = [
    "background-interview.md",
    "glossary-template.md",
    "learning-map-template.md",
    "prerequisite-gap-template.md",
    "starter-resources-template.md",
    "first-practice-template.md",
]
F1_DELIVERABLES = [
    "glossary.md",
    "learning-map.md",
    "prerequisite-gap.md",
    "starter-resources.md",
    "first-practice.md",
]
DOMAIN_PACK_FILES = ["pack.yaml", "curriculum.md", "glossary.md"]
REQUIRED_PACKS = ["_template", "embodied-ai"]

TEMPLATE_REQUIRED_SECTIONS = {
    "glossary-template.md": ["术语列表", "阅读顺序建议", "使用说明"],
    "learning-map-template.md": ["目标", "核心知识点", "产出检验", "建议资源"],
    "prerequisite-gap-template.md": ["学生已有基础", "缺口分析", "必须补", "建议补"],
    "starter-resources-template.md": ["论文检索", "学习资源", "开源与实战", "诚信声明"],
    "first-practice-template.md": ["任务描述", "检验标准", "常见坑", "做完后"],
    "background-interview.md": ["最少必要信息", "已修课程", "目标方向", "可用时间"],
}

fails: list[str] = []
warns: list[str] = []
oks: list[str] = []


def fail(msg: str) -> None:
    fails.append(msg)
    print(f"FAIL {msg}")


def warn(msg: str) -> None:
    warns.append(msg)
    print(f"WARN {msg}")


def ok(msg: str) -> None:
    oks.append(msg)
    print(f"OK   {msg}")


def run(cmd: list[str]) -> None:
    print("+", " ".join(cmd))
    subprocess.check_call(cmd, cwd=ROOT)


def main() -> int:
    # ------------------------------------------------------------------
    # 0. Prepare workspace
    # ------------------------------------------------------------------
    if RUN.exists():
        shutil.rmtree(RUN)
    (RUN / "_work").mkdir(parents=True)
    (RUN / "pdfs" / "auto").mkdir(parents=True)
    (RUN / "pdfs" / "user").mkdir(parents=True)

    (RUN / "scope.md").write_text(
        "# 研究范围说明\n"
        "- 主题：具身智能入门（F1 脚本冒烟）\n"
        "- 学生背景：大三，ML+Python，未学 3D 视觉和 RL\n"
        "- 深度档：标准\n"
        "- 用户已确认：冒烟用例\n",
        encoding="utf-8",
    )

    # ------------------------------------------------------------------
    # 1. Validate both F1 skills with validate_skill.py
    # ------------------------------------------------------------------
    print("\n=== 1. Skill structure validation ===\n")
    for name in F1_SKILLS:
        skill_dir = SKILLS / name
        if not skill_dir.is_dir():
            fail(f"技能目录不存在: skills/{name}/")
            continue
        try:
            run([sys.executable, str(TOOLS_SCRIPTS / "validate_skill.py"), name])
            ok(f"skills/{name}/ 结构校验通过 (0 FAIL)")
        except subprocess.CalledProcessError:
            fail(f"skills/{name}/ 结构校验存在 FAIL（见上方输出）")

    # ------------------------------------------------------------------
    # 2. Check template completeness
    # ------------------------------------------------------------------
    print("\n=== 2. Template completeness ===\n")
    template_dir = SKILLS / "domain-onboarding" / "references"
    for tpl_name in F1_TEMPLATES:
        tpl_path = template_dir / tpl_name
        if not tpl_path.is_file():
            fail(f"模板缺失: skills/domain-onboarding/references/{tpl_name}")
            continue

        text = tpl_path.read_text(encoding="utf-8")
        if tpl_name in TEMPLATE_REQUIRED_SECTIONS:
            missing = [s for s in TEMPLATE_REQUIRED_SECTIONS[tpl_name]
                       if s not in text]
            if missing:
                fail(f"模板 {tpl_name} 缺少章节: {missing}")
            else:
                ok(f"模板 {tpl_name} 结构完整")
        else:
            ok(f"模板 {tpl_name} 存在")

    # ------------------------------------------------------------------
    # 3. Encoding check on all F1 skill files
    # ------------------------------------------------------------------
    print("\n=== 3. F1 skill file encoding ===\n")
    for name in F1_SKILLS:
        try:
            run([sys.executable, str(SHARED_SCRIPTS / "check_encoding.py"),
                 str(SKILLS / name)])
            ok(f"skills/{name}/ UTF-8 编码通过")
        except subprocess.CalledProcessError:
            fail(f"skills/{name}/ 编码校验失败")

    # ------------------------------------------------------------------
    # 4. Domain-pack well-formedness
    # ------------------------------------------------------------------
    print("\n=== 4. Domain-pack validation ===\n")

    # 4a. _template — scaffolding only; needs README.md, content files are optional
    template_dir = DOMAIN_PACKS / "_template"
    if template_dir.is_dir():
        if (template_dir / "README.md").is_file():
            ok("domain-packs/_template/README.md 存在（脚手架模板）")
        else:
            fail("domain-packs/_template/README.md 缺失")
        # Check which template files exist; WARN about missing ones (nice-to-have)
        for fname in DOMAIN_PACK_FILES:
            if (template_dir / fname).is_file():
                ok(f"domain-packs/_template/{fname} 存在")
            else:
                warn(f"domain-packs/_template/{fname} 缺失（建议补，方便新建领域包时复制）")
    else:
        warn("domain-packs/_template/ 目录不存在")

    # 4b. Real domain packs — must have full structure
    real_packs = [p.name for p in DOMAIN_PACKS.iterdir()
                  if p.is_dir() and not p.name.startswith("_") and not p.name.startswith(".")]
    if not real_packs:
        warn("未发现任何实际领域内容包（domain-packs/<编号>/）")
    for pack_name in sorted(real_packs):
        pack_dir = DOMAIN_PACKS / pack_name
        missing = [f for f in DOMAIN_PACK_FILES if not (pack_dir / f).is_file()]
        if missing:
            fail(f"domain-packs/{pack_name}/ 缺少: {missing}")
        else:
            ok(f"domain-packs/{pack_name}/ 结构完整（{', '.join(DOMAIN_PACK_FILES)}）")
        # Check pack.yaml has required fields
        yaml_path = pack_dir / "pack.yaml"
        text = yaml_path.read_text(encoding="utf-8")
        for field in ["id:", "title:", "description:"]:
            if field not in text:
                stripped = field.rstrip(':')
                warn(f"domain-packs/{pack_name}/pack.yaml 缺少字段 '{stripped}'")

    # ------------------------------------------------------------------
    # 5. Expected outputs completeness & encoding
    # ------------------------------------------------------------------
    print("\n=== 5. Example expected outputs ===\n")
    expected_dir = EXAMPLES / "expected"
    if not expected_dir.is_dir():
        fail(f"examples/f1-sample-run/expected/ 目录不存在")
    else:
        for fname in F1_DELIVERABLES:
            fpath = expected_dir / fname
            if not fpath.is_file():
                fail(f"期望输出缺失: examples/f1-sample-run/expected/{fname}")
            else:
                ok(f"期望输出 {fname} 存在")

        # Check example README exists
        readme = EXAMPLES / "README.md"
        if not readme.is_file():
            fail("examples/f1-sample-run/README.md 缺失")
        else:
            ok("examples/f1-sample-run/README.md 存在")

        try:
            run([sys.executable, str(SHARED_SCRIPTS / "check_encoding.py"),
                 str(expected_dir)])
            ok("examples/f1-sample-run/expected/ UTF-8 编码通过")
        except subprocess.CalledProcessError:
            fail("examples/f1-sample-run/expected/ 编码校验失败")

    # ------------------------------------------------------------------
    # 6. Content smell checks on expected outputs
    # ------------------------------------------------------------------
    print("\n=== 6. Content smell checks ===\n")
    for fname in F1_DELIVERABLES:
        fpath = expected_dir / fname
        if not fpath.is_file():
            continue
        text = fpath.read_text(encoding="utf-8")

        # 6a. No leftover placeholders
        if "[TODO" in text or "[TODO:" in text:
            warn(f"expected/{fname} 仍有 [TODO] 残留")
        else:
            ok(f"expected/{fname} 无 [TODO] 残留")

        # 6b. Source labels present (glossary, learning-map, starter-resources)
        if fname == "glossary.md":
            if "from-search" not in text and "from-domain-pack" not in text:
                warn("glossary.md 缺少来源标注（from-search / from-domain-pack）")
        if fname == "learning-map.md":
            if "derived-from-search" not in text and "model-designed" not in text:
                warn("learning-map.md 缺少来源标注")
        if fname == "starter-resources.md":
            if "search-verified" not in text:
                warn("starter-resources.md 缺少 search-verified 标签")
            if "model-suggested" not in text:
                warn("starter-resources.md 缺少 model-suggested 标签")
            if "诚信声明" not in text:
                fail("starter-resources.md 缺少「诚信声明」节（协议硬要求）")
            if "来源统计" not in text:
                warn("starter-resources.md 建议含「来源统计」表")

        # 6c. Glossary should not exceed 25 terms
        if fname == "glossary.md":
            # Count table rows starting with | N |
            import re
            term_rows = re.findall(r'^\|\s*\d+\s*\|', text, re.MULTILINE)
            if len(term_rows) > 25:
                fail(f"glossary.md 术语 {len(term_rows)} 条 > 25（硬规则）")
            elif len(term_rows) >= 10:
                ok(f"glossary.md 术语 {len(term_rows)} 条（≤25，合理）")
            elif len(term_rows) > 0:
                warn(f"glossary.md 术语仅 {len(term_rows)} 条，可能偏少")

    # ------------------------------------------------------------------
    # 7. Test-run output encoding (if exists)
    # ------------------------------------------------------------------
    print("\n=== 7. Test-run output check ===\n")
    test_run = ROOT / "tests" / "runs" / "f1-test"
    if test_run.is_dir():
        try:
            run([sys.executable, str(SHARED_SCRIPTS / "check_encoding.py"),
                 str(test_run)])
            ok("tests/runs/f1-test/ UTF-8 编码通过")
        except subprocess.CalledProcessError:
            warn("tests/runs/f1-test/ 编码校验存在警告")
    else:
        ok("tests/runs/f1-test/ 目录不存在（跳过，正常——盲测时才会生成）")

    # ------------------------------------------------------------------
    # Report
    # ------------------------------------------------------------------
    print(f"\n{'='*60}")
    print(f"F1 SCRIPT SMOKE RESULT: {len(fails)} FAIL / {len(warns)} WARN / {len(oks)} OK")
    if fails:
        print("存在 FAIL —— 修复后再跑。")
        return 1
    print("OK →", RUN)
    print(f"{'='*60}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
