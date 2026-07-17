---
name: citation-verifier
description: >-
  Verifies papers in references.json via arXiv and CrossRef. Use before
  finalizing F2 landscape or shortlist deliverables; write audit into _work
  or references.json meta. Never claim "all verified" in the prose body.
---

# 引用核对（citation-verifier）

F2 自动程序：核对 `references.json` 中文献是否真实存在、关键字段是否完整。

遵守 `shared/honesty-checklist.md` 与 `references/three-axis.md`（存在性 / 元数据 / 声称支持）。

## 何时使用 / 何时不使用

**使用：** `literature-landscape.md` / `reading-shortlist.md` 成稿前后；任何准备对外展示的文献主张。

**不使用：** 尚未写入 `references.json`；仅做检索尚未精读（可对 shortlist 预检，但终检以文献库为准）。

## 前置条件（依赖哪些技能、哪些文件须已存在）

- 工作区根已有 `references.json`，且 `papers` 非空。
- 建议在 `literature-landscape-writer` 产出初稿后、或定稿前运行。

## 硬规则（禁止项）

1. 不得伪造核验结果；失败项必须进入审计文件，不得静默删除引用。
2. **不要**在 `literature-landscape.md` / `reading-shortlist.md` 正文写「已全部核验」。
3. 核验失败 → 回流改文稿或标记未核实，不得假装通过。

## 步骤（有序，可勾选）

1. [ ] 从 `references.json` 抽出候选。
2. [ ] 运行 `verify_citations.py`（arXiv → CrossRef → 标题兜底）。
3. [ ] 将审计写入 `_work/CITATION_AUDIT.json` 与 `_work/CITATION_AUDIT.md`。
4. [ ] 可选：摘要写入 `references.json` → `meta.audit`。
5. [ ] **声称支持轴**：对照各篇 `reading_notes.quotable_claims`（若有），由 Agent 完成；无则跳过并在审计中注明。
6. [ ] 失败项回流：改 landscape / shortlist / 库字段后重跑。

## 必须问人的点（停下条件与如何继续）

| 停下 | 问什么 | 继续条件 |
|------|--------|----------|
| 关键引用无法核实 | 删除该主张、改为「未核实」、还是用户提供正确 DOI/链接？ | 用户选择后改稿再核 |

## 交付契约（输入 / 输出路径与字段）

**输入：** `references.json`

**输出：**

- `_work/candidates_for_verify.json`
- `_work/CITATION_AUDIT.json` / `_work/CITATION_AUDIT.md`
- 可选：`references.json.meta.audit`

## 脚本调用（若有，给命令模板）

```bash
# 工作目录 = campus-research-output/<课题简称>/
python skills/citation-verifier/scripts/refs_to_verify_input.py \
  --references references.json \
  --out _work/candidates_for_verify.json

python skills/citation-verifier/scripts/verify_citations.py \
  --input _work/candidates_for_verify.json \
  --output _work/CITATION_AUDIT.json \
  --md _work/CITATION_AUDIT.md
```

## 失败与回流

| 失败 | 处理 |
|------|------|
| 网络不可用 | 记录于 `research-log.md`；标记待核验，不伪造通过 |
| 元数据不匹配 | 修正 `references.json` 或在 landscape 中降级表述 |
| 声称无 `reading_notes` 支撑 | 删主张或标缺口 |

## 参考（链接 references/）

- `references/three-axis.md`
- 上游：`literature-landscape-writer`；并行/后续：`survey-visualizer`
