# 具身智能知识缺口分析

> **学生背景：** 大三，学过 ML 入门课（Coursera ML） + 线性代数 + 概率论 + Python 熟练，未学过 3D 视觉和 RL，对 ROS 无了解，希望偏机器人操纵方向
> **目标学习地图：** `learning-map.md`（基于搜索结果归纳）
> **生成时间：** 2026-07-19T15:30:00
> **缺口补救资源：** 优先引用 `domain-resource-search` 搜索到的资源；不足时标注 `model-suggested`

---

## 学生已有基础

| 知识/技能 | 掌握程度 | 来源 |
|-----------|---------|------|
| Python 编程 | 熟练（写过课程项目） | 学生自述 |
| 线性代数 | 学过但有点生疏 | 学生自述 |
| 概率论 | 学过基础 | 学生自述 |
| 机器学习入门 | 上过 Coursera ML，了解监督/无监督/过拟合 | 学生自述 |
| PyTorch | 会用但不算熟练 | 学生自述 |
| 3D 视觉/点云/深度 | 未学过 | 学生自述 |
| 强化学习 | 未学过 | 学生自述 |
| ROS | 听说过但没用过 | 学生自述 |
| 机器人学 | 无 | 学生自述 |

---

## 缺口分析

### 🔴 必须补（blocker）——不补无法进入核心阶段

| 缺口 | 对应学习地图阶段 | 为什么是 blocker | 补救建议 | 来源 |
|------|-----------------|-----------------|---------|------|
| 3D 视觉基础（深度估计、点云、坐标系变换） | 阶段 2 | 不看深度图/点云就没法理解 visual navigation | 见 starter-resources.md §学习资源 #1（MIT 6.4210 Lecture 2–5）| `model-suggested, MUST verify` |
| 强化学习基础（MDP、Q-learning、Policy Gradient） | 阶段 3 | BC 和 PPO 都需要 RL 基础概念 | 见 starter-resources.md §学习资源 #2（CS224R 前 4 讲）+ §论文检索 #7（RL 入门综述）| `search-verified` |
| 仿真环境使用（Habitat） | 阶段 1 | 贯穿整个学习过程，所有动手实践都依赖 | 见 starter-resources.md §开源与实战 #1 | `community-curated` |

### 🟡 建议补（更顺畅）——不补也能学，但会吃力

| 缺口 | 对应学习地图阶段 | 为什么建议补 | 补救建议 | 来源 |
|------|-----------------|-------------|---------|------|
| 线性代数复习（矩阵分解、SVD、优化视角） | 阶段 2–3 | 3D 变换和 RL 中大量用到 | 见 starter-resources.md §学习资源（可在线速览 3–4h）| `model-suggested, MUST verify` |
| ROS 基础概念 | 阶段 4 | mini-project 如果涉及真实机器人需要 | 见 starter-resources.md §学习资源 | `model-suggested, MUST verify` |

### 🟢 可选补（锦上添花）——有余力再看

| 缺口 | 对应学习地图阶段 | 为什么可选 | 补救建议 | 来源 |
|------|-----------------|-----------|---------|------|
| 控制理论入门（PID、动力学基础） | 阶段 3 | 偏操纵方向时可以加深理解，但 BC/RL 训练不需要 | 见 starter-resources.md §学习资源 | `model-suggested, MUST verify` |
| 多模态学习基础 | 阶段 4 | Foundation model for embodied 涉及 vision-language-action | 见 starter-resources.md §论文检索 #11 | `search-verified` |

---

## 建议的补课顺序

```
第 1 步：仿真环境上手（blocker，约 6h）
  ↓
第 2 步：线性代数快速复习（建议补，约 3–4h）
  ↓
第 3 步：3D 视觉基础（blocker，约 8h）  ← 从这步开始进入阶段 2
  ↓
第 4 步：RL 基础（blocker，约 8h）        ← 为阶段 3 做准备
  ↓
然后按 learning-map.md 阶段 1–4 推进
```
