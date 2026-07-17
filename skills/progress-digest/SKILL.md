---
name: progress-digest
description: >-
  Audits authorized local code, logs, and results into artifact-index.md,
  progress-report.md, result-summary.md, and blockers.md. Use when the user
  asks for stage progress, weekly update, experiment summary, or meeting prep
  from local materials. Never scan the home directory without explicit paths.
---

# 阶段进展整理（progress-digest）

F4 工作流技能：在用户授权的本地路径内审计代码、日志与结果，形成可核对的阶段报告。

**完成标准：** `artifact-index.md` + `progress-report.md` + `result-summary.md` + `blockers.md`。

遵守 `shared/honesty-checklist.md`。本质是**阶段总结 + 证据审计**，不是扫盘后生成空泛概述，也不是自动跑实验。

## 何时使用 / 何时不使用

**使用：** 「总结这周进展」「看我 `./runs`」「阶段报告」「实验日志梳理」；为 F5 组会准备本地证据。

**不使用：** 只要找/读论文（F2/F3）；只要写 Related Work/综述（`survey-writer`）；用户拒绝给扫描路径且不愿粘贴要点；要求自动改代码刷指标（超出 MENTOR 边界）。

## 前置条件（依赖哪些技能、哪些文件须已存在）

- 工作区已有或可创建 `scope.md`，且须含「允许扫描的本地路径」与时间窗（或用户在对话中明确给出并写入）。
- 用户课题材料在本机授权路径内可读；**不要求** `references.json`（文献可选补充）。
- 遵守 `shared/workspace-layout.md` 的 F4 忽略规则（详见 `references/ignore-rules.md`）。

## 硬规则（禁止项）

1. 未获授权 **不得**扫描用户主目录或 `scope.md` 列出的路径之外。
2. **不得**因「有训练脚本 / 有 checkpoint」断定「实验已成功」。
3. 每条「已完成」须挂本地路径、commit、日志片段，或显式标签「口头进展（无产物）」。
4. 扫描时跳过依赖目录、`.git/`、大权重、数据集本体、密钥与 `.env`、大二进制（见忽略规则）。
5. 交付中不得粘贴密钥、token、完整 `.env`；日志摘录须脱敏。
6. 不编造指标曲线/消融；未见数值文件则写「未在授权材料中找到可核对数字」。
7. 中文 UTF-8；交付前跑 `shared/scripts/check_encoding.py`。

## 步骤（有序，可勾选）

1. [ ] 加载 `shared/honesty-checklist.md`；读/建 `scope.md`；确认根路径列表 + 时间窗。
2. [ ] 若无授权路径 → 写 `_work/WAITING_scan_scope.md` 并停止（见「必须问人的点」）。
3. [ ] 运行 `list_recent_files.py`，生成 `_work/recent-files.jsonl`（候选，非终稿）。
4. [ ] 筛候选 → 写 `artifact-index.md`（路径 / 一句话用途 / 是否已读 / 类型：code|log|result|doc）。
5. [ ] 按索引精读：README、近期改动说明、`*.log` / `metrics*.csv` / `results*.json`、图表说明；大文件只读头尾与关键行。
6. [ ] 写 `progress-report.md`：目标回顾 | 已完成（证据）| 进行中 | 未做 | 后续动作 | 风险。
7. [ ] 写 `result-summary.md`：仅基于已读结果文件；无结果则明确「本阶段无数值产物」。
8. [ ] 写 `blockers.md`：阻塞、所需决策（建议 ≤3 条留给导师）、证据缺口。
9. [ ] 跑 `validate_progress_paths.py` + 编码检查；更新 `_work/state.yaml`（`current_function: F4`）与 `research-log.md`。
10. [ ] 若用户要组会材料 → 提示调用 F5（本技能不代写一页纸）。

## 必须问人的点（停下条件与如何继续）

| 停下 | 问什么 | 继续条件 |
|------|--------|----------|
| 无扫描路径 | 请给出相对/绝对路径列表，或改为粘贴要点降级？ | 用户给出路径并写入 `scope.md`，或提供粘贴要点 |
| 路径过大/含数据集 | 是否收窄到 `runs/`、脚本、笔记并排除数据目录？ | 用户确认收窄后的路径 |
| 时间窗不清 | 自何时起？建议「最近 7 天」 | 用户确认时间窗 |
| 口头进展无文件 | 是否允许标「口头进展」？哪些主张必须补证据才可写入「已完成」？ | 用户选择 |

## 交付契约（输入 / 输出路径与字段）

**输入：** `scope.md`（扫描路径 + 时间窗）；授权路径下的本地材料。可选：`references.json`（仅当报告需挂文献结论时）。

**输出（工作区根）：**

| 文件 | 内容 |
|------|------|
| `artifact-index.md` | 材料索引（见 `references/artifact-index-template.md`） |
| `progress-report.md` | 阶段报告（见 `references/progress-report-template.md`） |
| `result-summary.md` | 结果摘要（见 `references/result-summary-template.md`） |
| `blockers.md` | 阻塞清单（见 `references/blockers-template.md`） |

**中间产物（`_work/`，非完成标准）：** `recent-files.jsonl`、`WAITING_scan_scope.md`。

## 脚本调用（若有，给命令模板）

在 MENTOR 仓库根或当前研究工作区根执行（按实际相对路径调整）：

```bash
python skills/progress-digest/scripts/list_recent_files.py \
  --roots path1 path2 --since 7d \
  --out _work/recent-files.jsonl

python skills/progress-digest/scripts/validate_progress_paths.py \
  --workspace . \
  artifact-index.md progress-report.md result-summary.md blockers.md
# 仅校验含目录分隔符的反引号路径 / Markdown 链接（裸文件名不算证据路径）

python shared/scripts/check_encoding.py \
  artifact-index.md progress-report.md result-summary.md blockers.md
```

`--since` 可写 ISO 日期（`2026-07-10`）或相对天数（`7d`）。

## 失败与回流

| 失败 | 处理 |
|------|------|
| 用户拒绝扫描且不粘贴 | 结束；不生成假报告 |
| 脚本列不出文件 | 请用户确认路径/时间窗；可手列索引后继续 |
| 路径校验失败 | 修正断链或删掉无证据主张后重跑 validate |
| 误读密钥文件 | 立即停止；从交付删除敏感内容；记入 `research-log.md` |
| 编码校验失败 | 删除坏文件并重新 UTF-8 生成，禁止 replace/cp1252「修复」 |

## 参考（链接 references/）

- `references/artifact-index-template.md`
- `references/progress-report-template.md`
- `references/result-summary-template.md`
- `references/blockers-template.md`
- `references/ignore-rules.md`
- 上游：用户本地材料 + `scope.md`；下游：F5 `meeting-brief` / `academic-writing`（读本技能四文件）
