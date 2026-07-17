# 阶段报告（progress-report）

> 时间窗：最近 30 天  
> 授权扫描路径：`examples/f4-sample-run/project`  
> 深度档：标准

## 目标回顾

按 `examples/f4-sample-run/project/README.md`：跑通 baseline 训练循环并记录 val_acc；本阶段不做消融。

## 已完成（须挂证据）

1. 写了最小训练入口 — 证据：`examples/f4-sample-run/project/train.py`
2. 完成一次名为 exp001 的记录运行，日志显示 3 个 epoch 结束 — 证据：`examples/f4-sample-run/project/runs/exp001/train.log`
3. 留下可核对的 metrics 表 — 证据：`examples/f4-sample-run/project/runs/exp001/metrics.csv`

## 进行中

（无）

## 未做 / 延期

1. 消融实验（README 已声明尚未做）
2. 与外部基线的系统对比

## 后续动作

1. 若组会需要，用 F5 基于本报告与 blockers 清单写一页纸
2. 补一次对照实验前先固定随机种子与数据划分说明

## 风险

1. 训练入口脚本仅为占位，真实训练逻辑未在仓库中；指标仅来自预写日志，未经本环境复现

## 诚信声明

- [x] 未将「有代码」写成「实验已成功」
- [x] 每条「已完成」均有路径
- [x] 不确定处已标明未独立复现
