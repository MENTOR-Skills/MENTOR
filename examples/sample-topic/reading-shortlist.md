# 精读清单：Attention / Transformer（样例）

> 依据当前 `references.json` 与全景说明；非穷尽推荐。

## 已入库精读

| id | 标题 | 年份 | 为何保留 | 阅读重点（挂 notes） |
|----|------|------|----------|----------------------|
| 1706.03762 | Attention Is All You Need | 2017 | 架构原点 | problem/method：自注意力替代 RNN |
| 2005.14165 | Language Models are Few-Shot Learners | 2020 | 规模与少样本 | results/limitations：成本与幻觉 |
| 1810.04805 | BERT… | 2019 | 双向预训练 | 摘要级；`abstract_only` |

## 建议下一步深读（可进 F3）

### 1. `1706.03762` — Attention Is All You Need

- **为何优先：** 后续两条主线的共同骨架。
- **建议阅读重点：** 多头注意力、位置编码、复杂度讨论。
- **依据：** reading_notes + 全文可 OA。
- **access_status：** fulltext

### 2. `1810.04805` — BERT

- **为何优先：** 理解双向预训练与微调范式。
- **建议阅读重点：** MLM / NSP 设定与任务迁移。
- **依据：** 当前为摘要级；建议补全文后再做数字级结论。
- **access_status：** abstract_only

### 3. `2005.14165` — Language Models are Few-Shot Learners

- **为何优先：** 对照「架构创新」与「规模效应」叙事。
- **建议阅读重点：** few-shot 设定与局限。
- **依据：** reading_notes。
- **access_status：** fulltext
