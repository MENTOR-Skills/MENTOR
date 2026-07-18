# 预期问答（qna-prep）

> **演示级。** 答案对齐 f4 expected；不编造额外实验。

## 材料范围

只读：`examples/f4-sample-run/expected/` 四文件及其中指向的 `project/` 路径。

## Q&A

### Q1：这周到底做完了什么？

**答：** 有最小训练入口；跑了一次名为 exp001 的记录，日志显示 3 个 epoch；留下 metrics 表。  
**证据：** `examples/f4-sample-run/expected/progress-report.md`；`project/train.py`；`runs/exp001/train.log`；`metrics.csv`  
**若被追问缺口：** 训练逻辑仍是占位，不能说「真实数据上训练成功」。

### Q2：0.72 的 val_acc 可信吗？能不能写进论文？

**答：** 数字与夹具日志/metrics 一致，但**未独立复现**；F4 结果摘要已标明「夹具预写」。目前只适合作为冒烟记录，不宜当作已验证结论写进论文。  
**证据：** `examples/f4-sample-run/expected/result-summary.md`  
**若被追问缺口：** 需要真实数据路径与可复现命令后再谈门槛。

### Q3：为什么还没做消融？

**答：** 本阶段目标明确不做消融；进展报告「未做」已列出。  
**证据：** `examples/f4-sample-run/expected/progress-report.md`  
**若被追问缺口：** 需要导师拍板：先数据管线还是先假数据消融骨架（见 blockers）。

### Q4：最大阻塞是什么？

**答：** 真实可运行训练与数据管线未接入；`train.py` 主要为占位打印。  
**证据：** `examples/f4-sample-run/expected/blockers.md`；`project/train.py`  
**若被追问缺口：** 没有真实数据路径可展示。

### Q5：你希望我这周拍板哪两件事？

**答：**（1）数据管线 vs 消融骨架优先级；（2）0.72 是否达到组会可引用门槛，还是仅冒烟。  
**证据：** `examples/f4-sample-run/expected/blockers.md`  
**若被追问缺口：** 无第三优先项，避免清单膨胀。

## 不建议硬撑的问题

| 问题方向 | 原因 | 建议话术 |
|----------|------|----------|
| 「是否已在真实数据上训成功？」 | 材料明确为缺口 | 「尚未接入真实数据；当前是占位脚本 + 预写日志。」 |
| 「比某某 SOTA 如何？」 | 未做系统对比 | 「本阶段未做外部基线对比，不能回答优劣。」 |

## 诚信摘要

- 答案未编造数值或文献。
- 缺口题已标「不知 / 未核对」。
