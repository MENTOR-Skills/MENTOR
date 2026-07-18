---
name: academic-writing
description: >-
  Writes academic drafts from verifiable local or literature materials via
  genre packs (meeting one-pager, Q&A, talk script, slides outline, stage
  writeup, tech doc, paper-section rewrite, polish). Always builds
  _work/claims-evidence.md before drafting. Use when the user asks to write,
  prepare a group meeting, PPT, polish, or tech docs. Never invent evidence;
  never write Related Work or long surveys from scratch (route to survey-writer).
---

# 学术写作（academic-writing）

F5 **唯一**写作工作流：选定**文体包** → 先写主张—证据表 → 再按模板成稿。

**记法：** 进 F5 = 打开本技能，选一个文体包。组会材料不再另开 `meeting-brief`。

遵守 `shared/honesty-checklist.md`。无材料不编造；不代替 F2/F4；不保证过审或相机就绪。

## 何时使用 / 何时不使用

**使用：** 「写组会一页纸」「预期问答」「口播稿」「阶段技术说明」「PPT 大纲」「润色」「技术文档 / README」「按大纲改写论文某一节」。

**不使用：**

- 从零写 Related Work / 长综述 → F2 `survey-writer`；
- 检索、全景、引用核对 → F2；单篇深读 → F3；扫代码/日志写阶段报告 → F4；
- 用户拒绝提供可核对材料且不愿标缺口；
- 要求伪造指标、引用或「实验已成功」。

## 前置条件（依赖哪些技能、哪些文件须已存在）

| 依赖 | 说明 |
|------|------|
| 材料来源（至少一类） | F4 四文件（`artifact-index.md` / `progress-report.md` / `result-summary.md` / `blockers.md`）；和/或 `references.json`（及可选 `literature-landscape.md` / `related-work.md` / `survey.md`）；和/或用户给出的 **ASCII** 路径底稿 |
| `scope.md` | 建议已有主题、语言、深度档；口头确认亦可写入 |
| 文体包选择 | 步骤 1 与用户确认（见「文体包」） |
| `paper-section` / `polish`（Related Work 类） | **须已有** F2 产物或用户底稿路径；禁止从零写 |

## 硬规则（禁止项）

1. **任何成稿前**必须先有 `_work/claims-evidence.md`；每条关键主张挂证据路径或显式缺口。
2. 强制加载并勾选 `shared/honesty-checklist.md`；不得编造引用、DOI、实验数值、下载状态。
3. **禁止**在本技能从零撰写 Related Work 或长综述；须导向 F2 `survey-writer` 或要求用户提供底稿。
4. 交付**文件名 / slug / 目录名仅 ASCII**（小写、数字、连字符）；正文可为中文 UTF-8。禁止 `paper-section-方法.md` 等中文文件名。
5. 推断须标明「推断」；未核实不得写成事实；不保证过审。
6. PPT：无 LaTeX **只**交 `meeting-slides-outline.md`；有 Beamer 才交 `meeting-slides.tex`；图表不得编造数据。
7. 未授权不得扫盘；不绕付费墙；交付不含密钥 / `.env`。
8. 成稿前跑 `shared/scripts/check_encoding.py`。

## 文体包（选一个）

| 文体包 id | 用户话术举例 | 主交付（ASCII） | 批次 |
|-----------|--------------|-----------------|------|
| `meeting-one-pager` | 组会一页纸 | `meeting-one-pager.md` | **核心** |
| `meeting-qna` | 预期问答 | `qna-prep.md` | **核心** |
| `meeting-talk` | 口播 / 汇报稿 | `meeting-talk.md` | **核心** |
| `stage-writeup` | 阶段技术说明 | `stage-writeup.md` | **核心** |
| `meeting-slides` | 组会 PPT | 有 LaTeX → `meeting-slides.tex`；否则仅 `meeting-slides-outline.md` | 第二批 |
| `tech-doc` | 技术文档 / README 类 | `tech-doc.md`（或用户指定的 ASCII basename） | 第二批 |
| `paper-section` | 论文某一节（改写） | `paper-section-<slug>.md` | 第二批 |
| `polish` | 按某刊润色 | `polish-<slug>.md` | 第二批 |

对照与选型话术见 `references/genre-packs.md`。

**分期：** 核心批 = 主张—证据 + 一页纸 / 问答 / 口播 / 阶段说明。第二批 = PPT / 技术文档 / 论文节改写 / 润色（薄模板可用；Related Work 仍禁止从零）。

## 步骤（有序，可勾选）

1. [ ] 加载 `shared/honesty-checklist.md`；读 `scope.md`；确认材料来源（F4 四文件 / 文献库 / 用户路径）。
2. [ ] 与用户确认**文体包**、输出语言、是否只要大纲。
3. [ ] 材料不够 → 写 `_work/WAITING_materials.md`（或缺哪类材料）并停止（见「停下条件」）。
4. [ ] 若文体为 `paper-section` / `polish` 且目标含 Related Work / 综述从零 → **停止并路由 F2 `survey-writer`**，不在本技能起草。
5. [ ] 写 `_work/claims-evidence.md`（模板：`references/claims-evidence-template.md`）；关键主张挂路径或缺口。
6. [ ] 按文体包模板成稿到工作区根（或用户指定 ASCII 路径）。
7. [ ] 逐条勾选诚信清单；缺口已在正文或主张表标明。
8. [ ] 跑编码检查；更新 `research-log.md` / `_work/state.yaml`（`current_function: F5`，`current_skill: academic-writing`）。
9. [ ] 若用户明确要求「预演导师追问 / 挑刺」→ 提示调用可选 `adversarial-lite`（**标准档不默认开**）。

## 必须问人的点（停下条件与如何继续）

| 停下 | 问什么 | 继续条件 |
|------|--------|----------|
| 无材料 | 提供 F4 四文件路径、`references.json`，还是粘贴要点并接受缺口标签？ | 用户给出可读材料或接受降级 |
| 文体未定 | 上表选哪个文体包？ | 用户确认 id |
| Related Work 从零 | 是否先走 F2 `survey-writer`，或提供已有底稿 ASCII 路径？ | 用户选 F2 或给出底稿 |
| 证据缺口关键主张 | 删主张 / 标缺口进稿 / 回流 F4 补证据？ | 用户选择 |
| slug / 文件名 | `paper-section` / `polish` 的 ASCII slug？ | 用户给出英文 slug |
| PPT / LaTeX | 是否有 Beamer 环境？无则只交大纲 | 用户确认 |

## 交付契约（输入 / 输出路径与字段）

**输入：** 可核对材料（F4 四文件和/或文献库和/或用户底稿）+ 选定文体包。

**强制中间产物：**

| 文件 | 说明 |
|------|------|
| `_work/claims-evidence.md` | 成稿前必须存在 |

**按文体包输出（工作区根，文件名 ASCII）：**

| 文体包 | 输出 |
|--------|------|
| `meeting-one-pager` | `meeting-one-pager.md` |
| `meeting-qna` | `qna-prep.md` |
| `meeting-talk` | `meeting-talk.md` |
| `stage-writeup` | `stage-writeup.md` |
| `meeting-slides` | `meeting-slides-outline.md`；可选 `meeting-slides.tex` |
| `tech-doc` | `tech-doc.md` 或用户指定 ASCII 名 |
| `paper-section` | `paper-section-<slug>.md` |
| `polish` | `polish-<slug>.md` |

**可选下游：** `_work/adversarial-notes.md`（仅当启用 `adversarial-lite`）。

## 脚本调用（若有，给命令模板）

在研究工作区根执行（路径按实际调整）：

```bash
# 成稿前编码检查（按实际交付文件替换）
python shared/scripts/check_encoding.py \
  _work/claims-evidence.md \
  meeting-one-pager.md \
  qna-prep.md \
  meeting-talk.md \
  stage-writeup.md
```

无本技能专用脚本；不强制 LaTeX 编译。

## 失败与回流

| 失败 | 处理 |
|------|------|
| 材料不足 | `_work/WAITING_*.md`；不编造成稿 |
| 用户要从零 Related Work / 长综述 | 回流 F2 `survey-writer`；本技能不写 |
| 主张无证据且用户拒标缺口 | 删除该主张或停止成稿 |
| F4 数字与正文不一致 | 以 F4 / 本地文件为准改稿，不「圆」数字 |
| 编码校验失败 | UTF-8 重写；禁止 cp1252「修复」 |
| 用户要相机 PDF | 说明本技能止于 Markdown（+ 可选 Beamer 源）；排版由用户负责 |

## 参考（链接 references/）

- `references/genre-packs.md` — 文体包对照（人话）
- `references/claims-evidence-template.md` — 主张—证据（强制）
- `references/meeting-one-pager-template.md` — 组会一页纸
- `references/qna-prep-template.md` — 预期问答
- `references/meeting-talk-template.md` — 口播 / 汇报稿
- `references/stage-writeup-template.md` — 阶段技术说明
- `references/meeting-slides-outline-template.md` — PPT 大纲（第二批）
- `references/tech-doc-template.md` — 技术文档（第二批）
- `references/paper-section-template.md` — 论文节改写（第二批；禁从零 Related Work）
- `references/polish-template.md` — 润色（第二批；禁从零 Related Work）
- 上游：F4 `progress-digest`；F2 文献库 / `survey-writer` 产物
- 可选下游：`adversarial-lite`
- 样例：`examples/f5-sample-writeup/`
