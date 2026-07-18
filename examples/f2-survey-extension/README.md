# f2-survey-extension

## 案例是什么

F2 **综述撰写扩展**样例：在 `examples/sample-topic/references.json`（三篇经典文）上展示 `survey-writer` 的多种交付形态。

| 文件 | 写法包 | 说明 |
|------|--------|------|
| `survey.md` | 分类框架综述（默认） | 主题综合 + 比较表 + 开放问题；**演示级**，低于标准档 8 篇门槛 |
| `related-work.md` | Related Work | 假设用户要做「高效自注意力变体」时的章节样例；**演示级**，低于 5 篇门槛 |

正式课题请扩大文献库后再按 `skills/survey-writer/references/quality-gate.md` 自检。

## 涉及哪些 skills

| 技能 | 本例角色 |
|------|----------|
| `literature-reader` | 上游库字段（复用 sample-topic） |
| `literature-landscape-writer` | 建议先有全景（可对照 sample-topic） |
| `survey-writer` | 本例核心：`survey.md` / `related-work.md` |
| `citation-verifier` | 成稿后应对库内引用再核一次 |

## 四种用法话术（Cursor / Agent）

工作区建议：`tests/runs/my-survey/`，先将 `examples/sample-topic/references.json` 复制到工作区根。

### 1. 分类框架综述（默认）

> 调用 `survey-writer`，写法包选**分类框架综述**，中文，数字序引用，产出 `survey.md`，然后跑 citation-verifier 和 check_encoding。

### 2. 叙事权威综述

> 调用 `survey-writer`，写法包选**叙事权威综述**（Nature Reviews 式叙事），中文，基于当前 `references.json` 写 `survey.md`，先给大纲确认。

### 3. 系统梳理 / 映射

> 调用 `survey-writer`，写法包选**系统梳理/映射**：先写 `_work/selection-protocol.md`（检索与纳入标准与 scope 一致），再写 `survey.md`；勿伪造 PRISMA 数字。

### 4. Related Work

> 调用 `survey-writer`，写法包选 **Related Work**。本文贡献是：「提出一种面向长序列的稀疏自注意力训练框架，在相同 FLOPs 下提升下游理解任务」。产出 `related-work.md`。

## 如何复现

1. 阅读 `skills/survey-writer/SKILL.md`、`references/style-packs.md`、`references/venue-writing-norms.md`。
2. 对照本目录 `survey.md`、`related-work.md` 与 `../sample-topic/references.json`：是否只引用库内文献、推断是否标注。
3. 任选上表话术在跑场工作区试写；成稿跑 `citation-verifier` + `shared/scripts/check_encoding.py`。

## 交付物

| 路径 | 说明 |
|------|------|
| `../sample-topic/references.json` | 文献库（不重复拷贝） |
| `survey.md` | 分类框架综述演示稿 |
| `related-work.md` | Related Work 演示稿 |
