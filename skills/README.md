# skills/

每个子目录是一个可安装技能，标准形态：

```text
<skill-name>/
├── SKILL.md
├── references/     # 可选
└── scripts/        # 可选
```

## 横切能力

| 技能 | 目录 | 说明 |
|------|------|------|
| 调度模块 | `campus-research-orchestrator/` | 用户入口：识别 F1–F5 意图、含混时只问一个澄清问题、初始化/恢复工作区、管理状态与确认关卡 |
| 工作区约定 | `research-workspace/` | 规程：初始化课题目录、写入 scope.md/state.yaml、跨次会话恢复 |
| 学术诚信 | `academic-honesty/` | 规程：成稿前强制核对 A–E 五类诚信清单；被 F1–F5 技能引用 |

## F1 陌生领域入门

| 技能 | 目录 | 说明 |
|------|------|------|
| 领域入门 | `domain-onboarding/` | 工作流：背景访谈 → 调用 `domain-resource-search` → 基于搜索结果生成五件套（术语表/学习地图/知识缺口/起步材料/首次练习）→ 诚信声明 |
| 领域资源搜索 | `domain-resource-search/` | 内部执行：3 渠道并行搜索（论文/学习资源/开源实践），不直接面向用户 |

领域内容包（`domain-packs/`）提供可选的标准知识框架加速，无包时不停止直接搜索生成。

## F2 文献全景（本周）

| 技能 | 目录 | 说明 |
|------|------|------|
| 文献检索下载 | `literature-search-download/` | 分级检索、shortlist、OA 下载、付费墙停车 |
| 文献精读入库 | `literature-reader/` | 写入 `references.json`（F3 可复用） |
| 文献全景撰写 | `literature-landscape-writer/` | `literature-landscape.md` + `reading-shortlist.md` |
| 综述撰写（扩展） | `survey-writer/` | 四写法包：叙事 / 分类（默认）/ 系统梳理 / Related Work → `survey.md` 或 `related-work.md` |
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

## F5 学术写作（写作中枢）

| 技能 | 目录 | 说明 |
|------|------|------|
| 学术写作 | `academic-writing/` | **唯一**写作工作流：选文体包 → `_work/claims-evidence.md` → 成稿 |
| 挑刺审阅 | `adversarial-lite/` | 可选；只写 `_work/adversarial-notes.md`；标准档不默认开 |

**不单独落地** `meeting-brief`：组会话术走 `academic-writing` 文体包（`meeting-one-pager` / `meeting-qna` / `meeting-talk` 等）。

核心文体：一页纸、问答、口播、阶段说明。第二批薄模板：PPT 大纲、技术文档、论文节改写、润色。  
Related Work / 长综述从零写 → F2 `survey-writer`，不进 F5。

典型顺序：确认材料（F4 四文件和/或文献库）→ 选文体包 → 主张—证据 → 成稿 →（可选）挑刺。

样例总览：`examples/`（含 `f5-sample-writeup/`）；可跑测试工作区：`tests/runs/`。
