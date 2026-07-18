# 具身智能首次练习

> **任务来源：** model-designed, 建议调整难度（基于 learning-map.md 阶段 2 的产出检验标准设计）
> **预计耗时：** 6–8 小时
> **适合阶段：** 完成 `learning-map.md` 阶段 2 后
> **生成时间：** 2026-07-19T15:30:00

---

## 任务描述

### 你要做什么

在 Habitat 仿真环境中，用预训练的 PointNav 模型跑 10 个导航场景，记录每一步的成功/失败情况，分析 3 个失败案例，写出 500 字的分析。然后尝试将一个场景的起点/终点调换（反向导航），观察模型是否仍能成功，思考为什么。

**一句话：** 跑通一个 SOTA 模型 → 看它在什么情况下失败 → 分析为什么。

---

### 我需要准备什么

- [x] Habitat Lab 已安装（见 starter-resources.md §开源与实战 #1）
- [x] 下载了 Gibson 或 Matterport3D 的一个测试场景
- [x] Python 3.8+, PyTorch 1.12+
- [x] 有一块 GPU（CPU 也可以但要等更久）

---

### 步骤

1. **下载预训练模型**（5 分钟）
   ```bash
   python -m habitat_baselines.run \
     --config-name pointnav/pointnav_habitat_test.yaml \
     habitat_baselines.evaluate=True \
     habitat_baselines.checkpoint_folder=data/checkpoints \
     habitat_baselines.eval_ckpt_path_dir=data/checkpoints/latest.pth
   ```
   如没有现成 checkpoint，用 `habitat_baselines` 的默认配置跑 eval 模式（它自带下载）。

2. **跑 10 条导航 episode**（1–2 小时，取决于 GPU）
   ```bash
   python -m habitat_baselines.run \
     --config-name pointnav/pointnav_rgbd.yaml \
     habitat_baselines.num_environments=1 \
     habitat_baselines.total_num_steps=1000 \
     habitat_baselines.eval.video_option=["disk"]
   ```
   记下每次运行的 `success` / `spl` / `distance_to_goal`。

3. **收集失败案例**（30 分钟）
   - 筛选出 `success=False` 的 episodes
   - 重放这些 episodes 的 RGB 视频，观察 agent 在哪个位置卡住

4. **分析 3 个失败案例**（1–2 小时）
   对每个失败案例回答：
   - agent 卡在了哪里？（走廊尽头？家具旁？起点不动？）
   - 为什么卡住？（看不到目标点？深度图噪声？训练分布外？）
   - 如果是你（人类），你会怎么走？

5. **反向导航实验**（1 小时）
   - 选一个成功的 episode，将起点和目标点互换
   - 用同一模型跑，看成功率是否下降
   - 思考：PointNav 策略是否对称？为什么（不）？

6. **写分析**（1 小时）
   - 500 字中文分析
   - 结构：做了什么 → 观察到了什么 → 为什么 → 对我的启发

---

## 检验标准

### 你怎么知道做对了？

- [x] 成功跑通 10 条 navigation episodes，输出 `success` 和 `spl` 指标
- [x] 至少分析了 3 个失败案例，每个都有场景描述 + 原因推测
- [x] 完成了反向导航实验，记下成功率对比
- [x] 产出一段 500 字的分析（不是流水账，是有 why 的分析）
- [x] 代码和日志可以复现（保留你的命令和输出）

### 常见坑

| 可能遇到的问题 | 如何解决 |
|---------------|---------|
| Habitat 安装失败（CUDA 版本不匹配） | 先装 CPU 版 `conda install habitat-sim -c conda-forge -c aihabitat` |
| 场景数据下载慢 | 只下载 1 个场景测试，不用全下（Gibson 的 `Allensville` 场景足够） |
| GPU OOM | 把 `num_environments` 改为 1，减小 resolution |
| 预训练模型不提供 | 用 Habitat Challenge 2022 的公开 checkpoint，或降低目标：只跑 random agent 基线 |

---

## 做完后

### 下一步建议

- 如果顺利完成 → 进入 `learning-map.md` 阶段 3（决策与 RL），尝试用 BC 训练你自己的 PointNav 策略
- 如果遇到困难 → 回顾 `prerequisite-gap.md`，检查 3D 视觉和仿真环境使用是否真的掌握了
- 如果觉得太简单 → 试试 ObjectNav（不只导航到坐标，而是导航到「椅子」「桌子」这类语义目标）

### 带着问题进入 F2

在做这个练习的过程中，记录以下具体问题：

- 为什么 PointNav 在某些场景表现好、另一些场景差？
- 现有导航方法是否对场景布局过拟合？
- RL 训练的导航策略和经典规划（如 A* + 地图）相比优劣在哪？

带着这些问题进入 F2 文献全景——你会比泛泛搜索「embodied navigation」高效得多。
