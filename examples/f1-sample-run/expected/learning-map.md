# 具身智能学习地图

> **来源：** derived-from-search + from-domain-pack: embodied-ai（基于搜索结果中的课程大纲和综述结构归纳阶段，domain-pack 补充调整）
> **目标学生背景：** 大三，学过 ML 入门课 + 线性代数 + Python，未学过 3D 视觉和 RL，希望偏机器人操纵方向
> **预计总学时：** 80–120 小时（每周 10 小时，约 8–12 周）
> **生成时间：** 2026-07-19T15:30:00

## 总体说明

你的 ML 和编程基础可以直接跳过「什么是机器学习」「怎么用 PyTorch」这类入门内容。
但需要补 3D 视觉基础（你没学过）和 RL 入门（你没学过）作为 blocker。
本学习地图 4 个阶段：先打工具和概念基础 → 补 3D 视觉 → 学决策 → 做项目。

---

## 阶段 1：基础工具与概念（15–20h）

### 目标
- 理解具身智能的核心问题：感知、规划、控制三者如何耦合
- 能用至少一种仿真环境跑 Hello World

### 核心知识点
| 知识点 | 对应术语 | 重要程度 | 建议学时 |
|--------|---------|---------|---------|
| 具身智能定义与范围 | glossary.md #1 | 必须掌握 | 2h |
| Sense-Plan-Act 经典框架 | glossary.md #2 | 必须掌握 | 3h |
| 端到端 vs 模块化 trade-off | glossary.md #3 | 理解即可 | 2h |
| 仿真环境上手（Habitat） | glossary.md #4 | 必须掌握 | 6h |
| 任务与动作空间 | glossary.md #14 | 理解即可 | 2h |

### 产出检验
- [ ] 用一段话解释「具身智能与传统 CV/NLP 有什么本质不同」
- [ ] 在 Habitat 中跑通 `python examples/example.py` 并截图

### 建议资源
- 论文：见 starter-resources.md §论文检索 #1, #2（综述）
- 课程：见 starter-resources.md §学习资源 #1（MIT 6.4210 前 5 讲）
- 开源：见 starter-resources.md §开源与实战 #1（Habitat Lab）

---

## 阶段 2：视觉感知与场景理解（20–25h）

### 目标
- 理解 embodied agent 如何从视觉输入理解 3D 环境
- 掌握 PointNav 和 ObjectNav 的基本范式

### 核心知识点
| 知识点 | 对应术语 | 重要程度 | 建议学时 |
|--------|---------|---------|---------|
| 3D 视觉基础（深度、点云） | — | 必须掌握 | 8h |
| 视觉导航（Visual Navigation） | glossary.md #5 | 必须掌握 | 8h |
| 语义地图 | glossary.md #12 | 理解即可 | 3h |
| VLN（语言引导导航） | glossary.md #9 | 了解概念 | 3h |

### 产出检验
- [ ] 用预训练模型在 Habitat 中完成一次 PointNav 最短路径导航
- [ ] 解释为什么 ImageNet 预训练特征在 embodied 场景中不够用

### 建议资源
- 论文：见 starter-resources.md §论文检索 #3–#6
- 开源：见 starter-resources.md §开源与实战 #3（Habitat Challenge baseline）
- 视频：见 starter-resources.md §学习资源 #1

---

## 阶段 3：决策、规划与控制（20–25h）

### 目标
- 理解 agent 如何从感知到行动
- 能用模仿学习训练一个简单策略

### 核心知识点
| 知识点 | 对应术语 | 重要程度 | 建议学时 |
|--------|---------|---------|---------|
| 强化学习基础（PPO, SAC） | glossary.md #10 | 必须掌握 | 8h |
| 模仿学习（BC, Dagger） | glossary.md #7 | 必须掌握 | 6h |
| 部分可观测问题 | glossary.md #11 | 理解即可 | 2h |
| 稀疏奖励与 reward shaping | glossary.md #18 | 理解即可 | 2h |
| 分层规划（HRL 概念） | — | 了解概念 | 3h |

### 产出检验
- [ ] 用 BC 在 Habitat 中训练一个 pick-and-place 的简单策略
- [ ] 解释 RL 在 embodied 场景中 sample efficiency 为什么是瓶颈

### 建议资源
- 论文：见 starter-resources.md §论文检索 #7–#9（决策与 RL）
- 课程：见 starter-resources.md §学习资源 #2（CS224R 前 8 讲）
- 开源：见 starter-resources.md §开源与实战 #2（Isaac Lab）

---

## 阶段 4：前沿主题与 mini-project（20–30h）

### 目标
- 了解当前研究热点
- 完成一个完整的 mini-project

### 核心知识点
| 知识点 | 对应术语 | 重要程度 | 建议学时 |
|--------|---------|---------|---------|
| 物体操纵基础 | glossary.md #6 | 了解概念 | 4h |
| 可供性（Affordance） | glossary.md #17 | 了解概念 | 2h |
| Foundation Model for Embodied AI | glossary.md #16 | 了解概念 | 3h |
| Sim-to-Real 基本思路 | glossary.md #8 | 了解概念 | 2h |
| mini-project | — | 必须掌握 | 12h+ |

### 产出检验
- [ ] 完成一个自选 mini-project（建议方向见 first-practice.md）
- [ ] 列出该方向的 3–5 篇里程碑论文并说出它们之间的关系
- [ ] 写一段 1000 字的研究计划草稿（带着它进 F2）

### 建议资源
- 论文：见 starter-resources.md §论文检索 #10–#12（前沿与 foundation model）
- 社区：见 starter-resources.md §学习资源 #1, #2（学习路线参考）
- 课程：见 starter-resources.md §学习资源 #3

---

## 学习路径总览

```
阶段 1 (基础) ──→ 阶段 2 (感知) ──→ 阶段 3 (决策) ──→ 阶段 4 (前沿 + 项目)
  15–20h           20–25h           20–25h           20–30h
```
