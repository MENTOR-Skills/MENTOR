---
name: paper-deep-read
description: >-
  Reads one AI/ML paper for a beginner researcher, first as a rough map and then,
  after confirmation, as an evidence-checked deep reading. Use for 粗读、精读、
  细读、论文笔记、分析论文 or 复现准备 from a PDF, reliable link, title, or
  references.json id. Produces reading-reports/<id>.md and updates the same
  references.json.
---

# 单篇论文深度阅读（F3）

当前只使用全局标准档；`rough` 与 `deep` 是阅读阶段，不是深度档。报告内容以 `references/report-template.md` 为唯一模板。

## 何时使用 / 何时不使用

- **使用：** 用户要读懂一篇指定论文，或为该论文准备复现条件。
- **不使用：** 主题检索与文献全景走 F2；把多篇材料写成学术成稿走 F5；只有标题且无可靠正文时不得假装读过。

## 前置条件（依赖哪些技能、哪些文件须已存在）

- 输入之一：本地 PDF、开放全文链接、论文标题或 `references.json` 中的 `id`。
- 使用用户指定工作区；未指定时使用已初始化的 `campus-research-output/<课题简称>/`。
- 开始写作前读取 `shared/honesty-checklist.md`；字段口径遵循 `docs/接口与协议.md` §6。

## 硬规则（禁止项）

1. 论文 `id`、报告文件名和文献库条目必须一致；只更新同一份 `references.json`。
2. 未取得全文时先进入 `waiting_user_pdf`；仅在用户明确同意后生成 `abstract_only` 概览。
3. `abstract_only` 只写摘要直接支持的内容，不得进入全文细读、补公式或补实验数字。
4. 关键主张必须标来源位置；作者陈述与“据模型分析”分开；不得伪造引用、数值、页码或已读状态。
5. 中文 Markdown / JSON 使用 UTF-8 无 BOM。

## 步骤（有序，可勾选）

1. [ ] 确认工作区、论文 `<id>`、输入来源和已有文献库条目。
2. [ ] 获取并检查全文文字层；失败则按下节停车。用户接受摘要级分析时，只填写模板的“摘要级概览”。
3. [ ] 按模板完成 `stage: rough`，写 `reading-reports/<id>.md`，回写简版 `reading_notes`，再询问是否进入细读及重点。
4. [ ] 用户确认后，在同一报告完成 `stage: deep`：复核粗读判断，展开方法与实验，审查证据和局限，再回写完整笔记与 `status: read`。
5. [ ] 用户明确要求复现准备时，另写冻结交付 `reproduction-checklist.md`；不得声称已运行实验。
6. [ ] 校验编码；用户需要时把 Markdown 渲染为同名 PDF。

## 必须问人的点（停下条件与如何继续）

| 停下条件 | 必须动作 | 继续条件 |
|---|---|---|
| 全文不可得 | 写 `_work/WAITING_user_pdf.md`，更新 `_work/state.yaml` 与 `research-log.md` | 用户补 PDF，或明确接受 `abstract_only` |
| rough 完成 | 写 `waiting_for: user_confirm_deep_read` 并询问细读范围 | 用户确认后进入 `stage: deep` |
| 生成复现清单 | 先说明只做条件审计、不运行实验 | 用户明确要求 |

## 交付契约（输入 / 输出路径与字段）

- 主交付：`reading-reports/<id>.md`、回写后的工作区根 `references.json`。
- 可选派生物：`reading-reports/<id>.pdf`；复现准备另交 `reproduction-checklist.md`。
- 报告结构与证据表见模板；文献库最小字段见 `docs/接口与协议.md` §6，不在本文件复制。

## 脚本调用（若有，给命令模板）

```bash
python skills/literature-reader/scripts/upsert_reference.py references.json _work/f3-paper.json
python shared/scripts/check_encoding.py reading-reports/<id>.md references.json
python skills/paper-deep-read/scripts/render_pdf.py reading-reports/<id>.md
```

## 失败与回流

- PDF 不可读或证据不足：停车请用户补文件；若用户接受摘要级概览，明确标 `abstract_only`。
- 文献库损坏或标识冲突：停止写回并保留原文件，先修复冲突。
- PDF 渲染失败：保留 Markdown 和既有 PDF，报告脚本给出的重试信息，不把排版失败当成阅读失败。

## 参考（链接 references/）

- `references/report-template.md`：报告结构、语言与证据纪律（唯一权威模板）。
- `shared/honesty-checklist.md`、`docs/接口与协议.md` §3/§6、`shared/workspace-layout.md`。
