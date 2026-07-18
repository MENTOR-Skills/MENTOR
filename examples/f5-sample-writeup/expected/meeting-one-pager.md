# 组会一页纸（meeting-one-pager）

> **演示级。** 依据 `examples/f4-sample-run/expected/`；非真实实验结论。

## 本周目标

跑通 baseline 训练循环并记录 val_acc；本阶段不做消融（见 F4 阶段报告目标回顾）。

## 已完成

1. 写了最小训练入口 — 证据：`examples/f4-sample-run/project/train.py`
2. 完成一次名为 exp001 的记录运行（日志显示 3 个 epoch 结束）— 证据：`examples/f4-sample-run/project/runs/exp001/train.log`
3. 留下可核对的 metrics 表 — 证据：`examples/f4-sample-run/project/runs/exp001/metrics.csv`

## 关键结果（若有）

| 指标或观察 | 数值/结论 | 来源 |
|------------|-----------|------|
| best_val_acc（日志） | 0.72 | `examples/f4-sample-run/project/runs/exp001/train.log`（夹具预写，未独立复现） |
| val_acc @ epoch 3 | 0.72 | `examples/f4-sample-run/project/runs/exp001/metrics.csv` |

## 进行中 / 未做

- 消融实验：未做
- 与外部基线的系统对比：未做
- 真实数据管线：未接入（训练入口仍为占位）

## 阻塞与待拍板（≤3）

1. 下一周优先补数据管线，还是先做假数据上的消融骨架？
2. val_acc=0.72 是否达到「可写进组会」的门槛，还是只作冒烟？

## 下周计划（可执行）

1. 按导师拍板结果：补数据管线 **或** 搭消融骨架（二选一，避免并行空转）
2. 补对照实验前先固定随机种子与数据划分说明

## 诚信摘要

- 未将「有代码」写成「实验已成功」；指标来自预写日志，未经本环境复现。
- 主张—证据见同目录 `claims-evidence.md`（运行时应为 `_work/claims-evidence.md`）。
