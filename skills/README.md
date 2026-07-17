# skills/

每个子目录是一个可安装技能，标准形态：

```text
<skill-name>/
├── SKILL.md
├── references/     # 可选
└── scripts/        # 可选
```

## F2 文献全景（本周）

| 技能 | 目录 | 说明 |
|------|------|------|
| 文献检索下载 | `literature-search-download/` | 分级检索、shortlist、OA 下载、付费墙停车 |
| 文献精读入库 | `literature-reader/` | 写入 `references.json`（F3 可复用） |
| 文献全景撰写 | `literature-landscape-writer/` | `literature-landscape.md` + `reading-shortlist.md` |
| 综述撰写（扩展） | `survey-writer/` | 可选 `survey.md` / `related-work.md` |
| 引用核对 | `citation-verifier/` | arXiv / CrossRef 核验 |
| 关系可视化 | `survey-visualizer/` | `viz/index.html`（含 relations 图） |

典型顺序：检索 → 精读入库 → 全景撰写 →（可选）综述撰写 → 引用核对 → 可视化。  
串联由横切 `campus-research-orchestrator` 负责；不另设 F2 空壳编排技能。

## F4 本地阶段总结

| 技能 | 目录 | 说明 |
|------|------|------|
| 阶段进展整理 | `progress-digest/` | 授权扫描 → `artifact-index.md` + `progress-report.md` + `result-summary.md` + `blockers.md` |

典型顺序：确认扫描范围与时间窗 → `list_recent_files.py` → 材料索引 → 精读证据 → 三份报告 → 路径/编码校验。  
不另设 F4 空壳编排技能；下游组会材料由 F5 读取上述四文件。

样例：`examples/`；可跑测试工作区：`tests/runs/`。
