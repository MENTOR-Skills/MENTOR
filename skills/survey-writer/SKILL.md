---
name: survey-writer
description: >-
  Writes a standalone literature-survey article (survey.md) or a short Related
  Work section from references.json only. Use when the user explicitly wants a
  long survey / related-work draft after the literature library exists. Follows
  CS survey norms inspired by IEEE/ACM thematic organization; always run
  citation-verifier before treating the draft as finished.
---

# 综述撰写（survey-writer）

F2 **可选扩展**技能：在文献库与（建议）全景说明已就绪后，产出长篇 `survey.md`，或论文用短 `related-work.md`。

基本版 F2 完成标准仍是全景 + 精读清单 + 关系图；本技能在用户明确要求「写综述 / Related Work / 投稿向草稿」时启用。

遵守 `shared/honesty-checklist.md`。

## 何时使用 / 何时不使用

**使用：**

- 用户明确要求长篇综述、survey paper 草稿、或论文 Related Work 章节；
- `references.json` 已含足够精读笔记，且用户确认要进入「综述扩展」模式。

**不使用：**

- 只要专题全景与精读建议 → 用 `literature-landscape-writer`；
- 文献库未入库或大量 `abstract_only` 且用户未声明接受摘要级局限；
- 代替用户向期刊正式投稿排版（本技能出 Markdown 文稿，不保证相机就绪 LaTeX）。

## 前置条件（依赖哪些技能、哪些文件须已存在）

- `references.json` 存在，`papers` 非空；目标篇目有 `reading_notes`（至少四字段）。
- 建议已有 `literature-landscape.md`（便于主题分节与缺口对齐）；无全景亦可，但须先与用户确认大纲。
- `scope.md` 已确认主题、时间范围、输出语言。
- 成稿前后应调用 `citation-verifier`。

## 硬规则（禁止项）

1. **只引用** `references.json` 中的条目；不得编造未入库文献或 DOI。
2. 按**主题/方法族**综合叙述，禁止终稿主结构为「A 说…B 说…」逐篇摘要。
3. 预印本标明 `(preprint)`；推断性关系/判断标注「推断」。
4. 声称须能回溯到 `reading_notes` 或明确摘要级依据；无证据标缺口。
5. **不要**把检索协议、纳入排除表、漏斗统计作为正文开篇一级结构（可放附录或 `_work/`）。
6. **不要**在正文写「已全部核验」；核验结果进 `_work/CITATION_AUDIT.*`。
7. 中文 UTF-8；写完用 `shared/scripts/check_encoding.py` 校验。

## 步骤（有序，可勾选）

1. [ ] 向用户确认文体：`survey`（独立综述）或 `related-work`（论文章节）。
2. [ ] 确认篇幅目标（默认中文约 2500+ 字或等价英文；Related Work 更短）与引用风格偏好（见 `references/venue-writing-norms.md`：数字序 [1] 或作者—年份）。
3. [ ] 基于库内文献与全景，拟定 **3+ 主题节**大纲，请用户点头（标准档建议确认）。
4. [ ] 按模板撰写 `survey.md` 或 `related-work.md`。
5. [ ] 比较表 / 开放问题须挂库内条目；不可比处显式说明。
6. [ ] 运行 `citation-verifier`；失败则改稿或标未核实后重跑。
7. [ ] 编码校验；更新 `research-log.md` / `state.yaml`。

## 必须问人的点（停下条件与如何继续）

| 停下 | 问什么 | 继续条件 |
|------|--------|----------|
| 启用前 | 要独立综述还是 Related Work？篇幅与语言？ | 用户确认 |
| 大纲后 | 主题分节是否合适？ | 用户确认或修改大纲 |
| 核验失败 | 删主张 / 标未核实 / 补正确元数据？ | 用户选择后改稿 |

## 交付契约（输入 / 输出路径与字段）

**输入：** `references.json`、`scope.md`；建议 `literature-landscape.md`。

**输出（工作区根，按模式二选一或并存）：**

| 文件 | 何时 |
|------|------|
| `survey.md` | 独立综述模式 |
| `related-work.md` | Related Work 模式 |

过程文件可放 `_work/survey-outline.md`。

## 脚本调用（若有，给命令模板）

```bash
python shared/scripts/check_encoding.py survey.md
# 然后按 citation-verifier 技能命令跑审计
```

## 失败与回流

| 失败 | 处理 |
|------|------|
| 库为空或笔记不足 | 回流 `literature-reader`，不空写 |
| 引用核验失败 | 改 `survey.md` / 库字段，不得静默删引用充数 |
| 用户要「投稿相机就绪 PDF」 | 说明本技能止于 Markdown；LaTeX/模板交给用户或后续工具链 |

## 参考（链接 references/）

- `references/survey-template.md` — 独立综述结构
- `references/related-work-template.md` — 论文 Related Work
- `references/venue-writing-norms.md` — IEEE/ACM/CS 综述书写规范摘要与来源
- 上游：`literature-landscape-writer` / `literature-reader`
- 下游：`citation-verifier`（强烈建议）；可视化仍读 `references.json`，不依赖 survey 正文
