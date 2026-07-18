# f4-sample-run

## 案例是什么

F4 **本地阶段总结**夹具：伪造最小课题目录（脚本 + 一次 run 日志/指标），演示 `progress-digest` 的四份交付形态与证据挂接。  
**不是**真实实验结果；`train.py` 不会真正训练。

## 涉及哪些 skills

| 技能 | 本例角色 |
|------|----------|
| `progress-digest` | 主技能：索引材料并写阶段报告 |
| （未跑）`academic-writing` | 下游 F5；可读本例 `expected/` 四文件（见 `examples/f5-sample-writeup/`） |

## 交付物是什么

| 路径 | 说明 |
|------|------|
| `project/` | 假装用户课题（授权扫描根） |
| `expected/artifact-index.md` | 材料索引样例 |
| `expected/progress-report.md` | 阶段报告样例 |
| `expected/result-summary.md` | 结果摘要样例 |
| `expected/blockers.md` | 阻塞清单样例 |

## 如何复现

### 脚本冒烟（推荐）

在 `MENTOR/` 根目录：

```powershell
python tests/scripts/run_f4_script_smoke.py
```

产物写入 `tests/runs/f4-script-smoke/`（含 `_work/recent-files.jsonl` 与对 `expected/` 的路径校验）。

### Agent 盲测话术

> 工作区请使用 `tests/runs/f4-blind-test/`（先建好 `_work/`）。  
> 允许扫描路径：`examples/f4-sample-run/project`（含 `train.py` 与 `runs`）。  
> 按 F4 `progress-digest`：确认范围 → 列近期文件 → 材料索引 → 阶段报告 / 结果摘要 / 阻塞清单。  
> 不要因为有 `train.py` 就写「训练已成功」；数字必须来自日志或 metrics。

负例：不给扫描路径 → 应出现 `_work/WAITING_scan_scope.md`，不得扫整个用户主目录。
