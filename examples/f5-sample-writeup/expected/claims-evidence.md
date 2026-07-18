# 主张—证据对照（claims-evidence）

> **演示级。** 运行时路径应为 `_work/claims-evidence.md`。  
> 证据挂到 `examples/f4-sample-run/expected/` 与 `examples/f4-sample-run/project/`。

## 材料来源

| 类型 | 路径 |
|------|------|
| F4 四文件 | `examples/f4-sample-run/expected/artifact-index.md`、`progress-report.md`、`result-summary.md`、`blockers.md` |
| 本地项目（索引所指） | `examples/f4-sample-run/project/` |

## 主张表

| # | 主张（写进成稿的句子） | 证据路径或字段 | 状态 | 备注 |
|---|------------------------|----------------|------|------|
| 1 | 本阶段目标是跑通 baseline 训练循环并记录 val_acc，不做消融 | `examples/f4-sample-run/expected/progress-report.md`（目标回顾）；`examples/f4-sample-run/project/README.md` | 已挂证据 | |
| 2 | 已有最小训练入口脚本 | `examples/f4-sample-run/project/train.py` | 已挂证据 | 占位脚本，非完整训练逻辑 |
| 3 | exp001 日志显示 3 个 epoch 结束，best_val_acc=0.72 | `examples/f4-sample-run/project/runs/exp001/train.log`；`metrics.csv`；`expected/result-summary.md` | 已挂证据 | 夹具预写，未独立复现 |
| 4 | 消融与系统基线对比尚未做 | `examples/f4-sample-run/expected/progress-report.md`（未做） | 已挂证据 | |
| 5 | 真实数据管线尚未接入，训练入口仅为占位 | `examples/f4-sample-run/expected/blockers.md`；`project/train.py` | 已挂证据 | |
| 6 | 「训练已在真实数据上成功」 | — | **缺口** | **不写进成稿** |

## 明确不写进成稿的内容

| 内容 | 原因 |
|------|------|
| 训练已在真实数据上成功 | 无真实数据路径；脚本为占位 |
| 方法显著优于外部基线 | 未做系统对比 |

## 诚信勾选（摘要）

对照 `shared/honesty-checklist.md`：

- [x] A 文献与引用 — N/A（本稿无文献主张）
- [x] B 实验与数据 — 数字来自夹具日志/metrics；标明未独立复现
- [x] C 下载与获取 — N/A
- [x] D 隐私与授权 — 仅用 examples 路径
- [x] E 不确定处已声明

## 下游文体包

本表支撑：`meeting-one-pager`、`meeting-qna`
