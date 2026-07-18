# f5-sample-writeup

## 案例是什么

F5 **学术写作**夹具：基于 `examples/f4-sample-run/expected/` 四份阶段材料，演示 `academic-writing` 核心文体（主张—证据 → 组会一页纸 → 预期问答）的**期望形态**。

**演示级**：不是真实实验室产出；证据路径挂到 f4 夹具，勿当作真实实验结果。

可选对照：`examples/sample-topic/`（文献侧）本例未强依赖。

## 涉及哪些 skills

| 技能 | 本例角色 |
|------|----------|
| `academic-writing` | 主技能：文体包 `meeting-one-pager` + `meeting-qna` |
| （上游只读）`progress-digest` | 材料来自 `examples/f4-sample-run/expected/` |
| （未跑）`adversarial-lite` | 可选；标准档不默认 |

## 交付物是什么

| 路径 | 说明 |
|------|------|
| `expected/claims-evidence.md` | 主张—证据样例（运行时对应 `_work/claims-evidence.md`） |
| `expected/meeting-one-pager.md` | 组会一页纸样例 |
| `expected/qna-prep.md` | 预期问答样例 |

说明：夹具把主张表放在 `expected/` 便于对照；真实工作区应写在 `_work/claims-evidence.md`。

## 如何复现

### 对照阅读（推荐）

1. 先读 `examples/f4-sample-run/expected/` 四文件。
2. 再对照本目录 `expected/` 三文件：主张如何挂路径、一页纸如何压缩、问答如何预演 blockers。

### Agent 话术

> 请按 F5 `academic-writing`：文体包先用 `meeting-one-pager`，再写 `meeting-qna`。  
> 材料只读：`examples/f4-sample-run/expected/` 下四文件。  
> 成稿前必须先写主张—证据表；数字只能来自该 expected 中的日志/metrics 路径。  
> 不要因为有 `train.py` 就写「训练已在真实数据上成功」。  
> 交付文件名用 ASCII。不要从零写 Related Work。

产物可写入 `tests/runs/f5-blind-test/`（先建 `_work/`）；本目录 `expected/` 仅作形态对照。
