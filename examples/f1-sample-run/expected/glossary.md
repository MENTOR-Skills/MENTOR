# 具身智能核心术语

> **来源：** from-search（论文+课程搜索结果）+ from-domain-pack: embodied-ai
> **生成方式：** 先从 `_work/f1-search-results.md` 中提取高频术语，再以 domain-pack 术语表补全
> **生成时间：** 2026-07-19T15:30:00

## 阅读建议

先掌握标注「★ 先修」的术语（共 6 条），再按顺序阅读其余。
若有不清楚的概念，回到本表查阅。

---

## 术语列表

| # | 术语 | 英文 | 一句话解释 | 先修关系 |
|---|------|------|-----------|---------|
| 1 | 具身智能 | Embodied AI | 智能体在物理或仿真环境中通过感知和行动与环境交互、完成任务的智能形式 | ★ 先修 |
| 2 | 感知-规划-控制 | Sense-Plan-Act | 经典机器人框架：先感知环境 → 规划行动序列 → 执行控制，三者串行 | ★ 先修 |
| 3 | 端到端学习 | End-to-End Learning | 从原始传感器输入直接输出控制信号，不经过显式规划模块 | 依赖 #2 |
| 4 | 仿真环境 | Simulation Environment | 用计算机模拟物理世界，供 agent 训练和测试（如 Habitat, Isaac Sim） | ★ 先修 |
| 5 | 视觉导航 | Visual Navigation | 仅用视觉输入（RGB/深度）引导 agent 移动到目标位置 | 依赖 #2 |
| 6 | 物体操纵 | Object Manipulation | 控制机械臂或其他执行器与物体交互（抓取、推动、放置等） | 依赖 #2 |
| 7 | 模仿学习 | Imitation Learning (Behavioral Cloning) | 从人类示教数据中学习策略，模仿示教者的行为 | 依赖 #3 |
| 8 | Sim-to-Real Transfer | Sim-to-Real | 在仿真中训练的策略迁移到真实物理世界的技术 | 依赖 #4 |
| 9 | VLN | Vision-and-Language Navigation | 根据自然语言指令在视觉环境中导航的任务 | 依赖 #5 |
| 10 | PPO | Proximal Policy Optimization | 一种广泛用于 embodied 训练的强化学习算法 | 依赖 #3 |
| 11 | 部分可观测 | Partial Observability (POMDP) | agent 只能看到环境的一部分（如第一视角 RGB），不知道全局状态 | 依赖 #2 |
| 12 | 语义地图 | Semantic Map | 不仅包含几何信息、还标注物体类别和功能的地图表示 | 依赖 #5 |
| 13 | 交互式感知 | Interactive Perception | 通过主动与环境交互来改善感知（如推一下物体看它是否会动） | 依赖 #1 |
| 14 | 任务与动作空间 | Task and Action Space | 任务空间=agent 能完成什么任务；动作空间=agent 能执行什么动作 | ★ 先修 |
| 15 | 本体感受 | Proprioception | agent 感知自身状态（关节角度、末端位置、受力等） | ★ 先修 |
| 16 | 具身基础模型 | Foundation Model for Embodied AI | 在大规模 embodied 数据上预训练的通用模型（如 RT-2, Octo） | 依赖 #3, #4 |
| 17 | 可供性 | Affordance | 物体提供的行为可能性（如门把手"可供"抓握和旋转） | 依赖 #6 |
| 18 | 稀疏奖励 | Sparse Reward | RL 中只在任务完成时给奖励信号——embodied 常见难点 | 依赖 #3 |

---

## 阅读顺序建议

```
#1 具身智能 ─┬→ #2 Sense-Plan-Act ─┬→ #4 仿真环境
             │                      │        ↓
             │                      │   #8 Sim-to-Real
             │                      │
             │                      ├→ #3 端到端学习 ─┬→ #7 模仿学习
             │                      │                  ├→ #10 PPO
             │                      │                  ├→ #16 具身基础模型
             │                      │                  └→ #18 稀疏奖励
             │                      │
             │                      ├→ #11 部分可观测
             │                      │
             │                      ├→ #5 视觉导航 → #9 VLN → #12 语义地图
             │                      │
             │                      └→ #6 物体操纵 → #17 可供性
             │
             ├→ #14 任务与动作空间
             └→ #15 本体感受
```

## 使用说明

1. **本术语表聚焦入门：** 不包括具身智能的全部术语，只覆盖看懂学习地图和 starter-resources 所需的核心概念
2. **解释追求可理解：** 目标读者为本科生，不用公式，用直觉性描述
3. **来源可追溯：** 术语定义优先从搜索到的论文综述和课程大纲中提取；domain-pack 作为补充验证
4. **可反馈修改：** 如发现解释不准确或缺少关键术语，告诉 Agent 补充
