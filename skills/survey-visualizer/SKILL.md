---
name: survey-visualizer
description: >-
  Builds a single-file HTML dashboard and relation graph from references.json
  only. Use after F2 literature library exists; never invent chart data or
  edges. Inferred relations render as dashed lines.
---

# 关系可视化（survey-visualizer）

F2 执行技能：只根据文献库生成 `viz/index.html`（统计面板 + 关系图）。

## 何时使用 / 何时不使用

**使用：** `references.json` 已存在，需要关系图或文献库概览网页（F2 标准交付）。

**不使用：** 文献库为空；想用训练记忆补边（禁止）；尚未完成检索/入库。

## 前置条件（依赖哪些技能、哪些文件须已存在）

- 工作区根：`references.json`，`papers` 非空。
- 建议在 `literature-landscape-writer` 与（可选）`citation-verifier` 之后运行。

## 硬规则（禁止项）

1. **只读** `references.json`；不得编造论文节点或关系边。
2. 无 `relations` → 仍可出统计看板，并明确「无关系边、未发明边」。
3. `basis: inferred` 必须用虚线（或图例）与 `fact` 区分。
4. 目标边的 `target_id` 不在库内 → 跳过该边，不画悬空节点。

## 步骤（有序，可勾选）

1. [ ] 确认 `references.json` 可读且含 papers。
2. [ ] 运行 `build_viz.py` → `viz/index.html`。
3. [ ] 目视检查：节点数与库一致；推断边为虚线。
4. [ ] 编码校验（HTML UTF-8）。

## 必须问人的点（停下条件与如何继续）

通常无需问人。若用户要求「补全领域关系网」但库中无边：说明只能基于现有 `relations`，请先回 `literature-landscape-writer` / reader 补标注。

## 交付契约（输入 / 输出路径与字段）

**输入：** `references.json`（可选 `papers[].relations[]`：`target_id`, `kind`, `basis`）

**输出：** `viz/index.html`

## 脚本调用（若有，给命令模板）

```bash
# 工作目录 = campus-research-output/<课题简称>/
python skills/survey-visualizer/scripts/build_viz.py \
  --out viz/index.html \
  --references references.json \
  --title "Literature Landscape"
```

无 `references.json` 或 `papers` 为空 → 非零退出，不写假图。

## 失败与回流

| 失败 | 处理 |
|------|------|
| 退出码非 0 | 先修文献库，再重跑 |
| 边过多难读 | 不删数据；可在 landscape 文中说明，或请用户筛选展示子集（须改库而非脚本瞎编） |

## 参考（链接 references/）

- `references/viz-notes.md`
- 上游：`literature-landscape-writer`、`citation-verifier`
