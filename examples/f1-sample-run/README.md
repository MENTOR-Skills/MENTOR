# F1 完整演示：具身智能入门

## 案例是什么

大三学生小张学过 ML 入门课、线性代数、Python，但对「具身智能」完全陌生，想入门。
Agent 先做背景访谈，然后调用 `domain-resource-search` 在 3 个渠道并行搜索，
再基于搜索结果生成个性化五件套。

## 涉及哪些 Skills

| 技能 | 作用 |
|------|------|
| `research-workspace` | 初始化 `campus-research-output/embodied-ai/` 工作区 |
| `domain-onboarding` | F1 主流程：背景访谈 → 触发搜索 → 基于搜索结果生成五件套 |
| `domain-resource-search` | F1 内部：3 渠道并行搜索（论文/学习资源/开源实践）→ `_work/f1-search-results.md` |
| `academic-honesty` | 成稿前诚信勾选（由 domain-onboarding 步骤 8 调用） |

## 流程（新版：先搜索，再框架）

```
步骤 1  背景访谈（确认学过 ML+Python、未学 3D 视觉和 RL、希望偏操纵方向）
步骤 2  调用 domain-resource-search，3 渠道并行搜索
           ├─ 论文：arXiv + OpenAlex → 综述 + 经典单篇
           ├─ 学习资源：公开课程 + 教材 + 教程
           └─ 开源实践：GitHub + 数据集
           → 写入 _work/f1-search-results.md
步骤 3  从搜索结果中提取术语 → glossary.md
步骤 4  基于搜到的课程大纲和综述结构归纳学习阶段 → learning-map.md
步骤 5  对比学生背景 vs 学习地图 → prerequisite-gap.md
步骤 6  聚合搜索结果按 3 渠道分组 → starter-resources.md
步骤 7  设计对齐学习地图的动手任务 → first-practice.md
步骤 8  诚信声明 + 编码检查 + 收尾
```

## 交付物是什么

位于 `examples/f1-sample-run/expected/`：

| 文件 | 说明 | 来源 |
|------|------|------|
| `glossary.md` | 18 条核心术语，标注阅读顺序 | 从搜索结果提取（含 domain-pack 补充） |
| `learning-map.md` | 4 阶段学习路径，对齐学生已有 ML + 编程背景 | 基于搜到的课程大纲和综述结构归纳 |
| `prerequisite-gap.md` | 3 项 blocker（3D 视觉、RL、仿真环境）、2 项建议补 | 对比学生背景 vs 学习地图 |
| `starter-resources.md` | 按 3 渠道分组：12 篇论文 + 5 项学习资源 + 5 个开源项目 | 来自 3 渠道搜索结果，标注来源标签 |
| `first-practice.md` | 用预训练模型在 Habitat 中跑 PointNav 并分析失败案例 | 对齐 learning-map 阶段 2 |

## 新旧流程对比

| 维度 | 旧版 | 新版 |
|------|------|------|
| 技能数 | 1 个 | **2 个**（domain-onboarding + domain-resource-search） |
| 搜索时机 | 框架生成之后 | **框架生成之前** |
| 搜索渠道 | 8 个（用户勾选） | **3 个**（直接并行，无 UI） |
| 术语来源 | `from-domain-pack` / `model-knowledge` | **`from-search`**（可追溯到搜索结果） |
| 学习阶段来源 | `from-domain-pack` / `model-designed` | **`derived-from-search`** |
| 内容包无匹配 | 停车确认 | **不停止**，直接搜索 |

## 如何复现

1. 确保工作区已初始化（`research-workspace` 已运行）
2. 对 Agent 说：「我对具身智能完全不了解，学过 ML 入门和 Python，每周约 10 小时，想系统入门」
3. Agent 进入 F1 `domain-onboarding`，先做背景访谈（确认 3D 视觉未学过、希望偏操纵方向）
4. Agent 自动调用 `domain-resource-search`（3 渠道并行，无需用户勾选）
5. Agent 基于搜索结果生成五件套（对应 `expected/` 下的文件）
6. 交付后跑 `python shared/scripts/check_encoding.py glossary.md learning-map.md prerequisite-gap.md starter-resources.md first-practice.md`

> **注意：** `starter-resources.md` 中的 URL 和论文因时间推移可能失效。
> 本样例中论文标题和 URL 标注为演示值（标题后加 `[demo]`），
> 实际运行时 `domain-resource-search` 实时搜索获取真实结果。
