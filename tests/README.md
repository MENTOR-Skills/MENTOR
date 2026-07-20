# tests/ — 本地可跑测试工作区

本目录用于 **脚本冒烟** 与 **Cursor 盲测跑场**。  
`examples/` 放只读样例与说明；真正跑起来的产物写到 `tests/runs/<用例名>/`，默认不提交 Git。

```text
tests/
├── README.md                 # 本说明（含 Cursor 前置步骤）
├── scripts/                  # 一键脚本冒烟
│   ├── run_f1_script_smoke.py
│   ├── run_f2_script_smoke.py
│   ├── run_f3_script_smoke.py
│   └── run_f4_script_smoke.py
└── runs/                     # 每次测试的工作区根（可重建）
    └── .gitkeep
```

约定：一次测试 = `tests/runs/<用例名>/`，目录形态对齐 `shared/workspace-layout.md`（等同于正式的 `campus-research-output/<简称>/`，只是根路径改到 `tests/runs` 便于集中清理）。

---

## Cursor 独立测试：前置步骤

按顺序做完再开盲测对话。

### 1. 代码与分支

1. 打开仓库中的 `MENTOR` 文件夹作为 Cursor 工作区根（或打开整仓但对话里约定工作目录为 `MENTOR`）。
2. 确认已拿到含对应技能的分支（F1–F5 现均在 `main`），且存在目录：
   **F1:** `skills/domain-onboarding/`、`skills/domain-resource-search/`
   **F2:** `skills/literature-search-download/`、`skills/literature-reader/`、`skills/literature-landscape-writer/`、`skills/survey-writer/`、`skills/citation-verifier/`、`skills/survey-visualizer/`
   **F3:** `skills/paper-deep-read/`（复用 `skills/literature-reader/`）
   **F4:** `skills/progress-digest/`
   **F5:** `skills/academic-writing/`

### 2. 把技能装进 Cursor（二选一）

**A. 推荐（本仓库联调）**  
在对话中明确：

> 使用本仓库 `MENTOR/skills/` 下的技能，不要用我全局目录里可能过期的同名 skill。

Agent 会按相对路径读 `SKILL.md` 与 `scripts/`。

**B. 安装到用户技能目录**  
将上述技能目录复制到 Cursor skills 目录（Windows 常见为 `%USERPROFILE%\.cursor\skills\`）。  
复制后若全局与仓库各有一份，**以仓库版为准**，避免测到旧 demo。

### 3. Python 与网络

- 系统可用 `python` / `python3`（3.10+ 即可；脚本以标准库为主）。
- 检索与引用核验需要能访问外网：`export.arxiv.org`、OpenAlex、CrossRef。
- 不必配置 API Key（当前脚本未强制 Semantic Scholar Key）。

### 4. 准备跑场目录

```powershell
cd MENTOR
New-Item -ItemType Directory -Force -Path tests/runs/my-blind-test/_work, tests/runs/my-blind-test/pdfs/user, tests/runs/my-blind-test/pdfs/auto
```

在 `tests/runs/my-blind-test/scope.md` 写好主题、年份、深度档（标准）、禁止事项。

### 5. 诚信与协议（开跑前扫一眼）

- `shared/honesty-checklist.md`
- `docs/接口与协议.md` §3 / §6（交付文件名与 `references.json` 字段）
- `AGENTS.md` 全局禁令（不伪造引用、不绕付费墙）

### 6. 发起盲测对话（F2 示例话术）

> 工作区请使用 `tests/runs/my-blind-test/`。  
> 帮我梳理「你的真实主题」（年份范围），给出精读建议和关系图。  
> 按 F2：确认范围 → 检索 → 遇付费墙停下 → 入库 → 全景与精读清单 → 引用核对 → 关系图。  
> 若你还想要长综述，再说一声再写 `survey.md`。

### 7. 你要盯的门控

| 检查点 | 期望 |
|--------|------|
| 付费/无 OA | 出现 `_work/WAITING_user_pdf.md`，流程暂停 |
| 交付 | 工作区根有四件基本交付；可选 `survey.md` |
| 关系图 | `viz/index.html` 边来自 `references.json`，推断为虚线 |
| 编码 | `python shared/scripts/check_encoding.py tests/runs/my-blind-test` |

### 8. 仅测脚本、不测 Agent 文笔时

```powershell
cd MENTOR
python tests/scripts/run_f1_script_smoke.py
python tests/scripts/run_f2_script_smoke.py
python tests/scripts/run_f3_script_smoke.py
python tests/scripts/run_f4_script_smoke.py
```

产物分别写入 `tests/runs/f1-script-smoke/`、`tests/runs/f2-script-smoke/`、`tests/runs/f4-script-smoke/`。  
F3 只使用临时目录验证安全写回，并检查 `examples/f3-sample-run/` 恰好包含 `references.json`、阅读报告 Markdown 和同名 PDF。  
F1 说明见 `examples/f1-sample-run/README.md`；F2 说明见 `examples/f2-script-smoke/README.md`；F3 成品见 `examples/f3-sample-run/`；F4 说明见 `examples/f4-sample-run/README.md`。

### F1 盲测话术（新增）

> **前置准备：** 
> 1. 确认已拿到含 F1 技能的分支（`main`），且存在目录：
>    - `skills/domain-onboarding/`
>    - `skills/domain-resource-search/`
> 2. 可选：`domain-packs/embodied-ai/` 存在（无内容包时 F1 仍可运行，直接走搜索+对话生成）
> 3. 准备跑场目录：
> ```powershell
> cd MENTOR
> New-Item -ItemType Directory -Force -Path tests/runs/f1-blind-test/_work, tests/runs/f1-blind-test/pdfs/user, tests/runs/f1-blind-test/pdfs/auto
> ```
> 4. 在 `tests/runs/f1-blind-test/scope.md` 写入主题、学生背景、深度档。

**话术（具身智能场景）：**

> 工作区请使用 `tests/runs/f1-blind-test/`。  
> 我对具身智能完全不了解，学过 ML 入门和 Python，每周约 10 小时，想系统入门，偏机器人操纵方向。  
> 按 F1：背景访谈 → 先搜索 → 基于搜索结果生成五件套 → 诚信声明。

**话术（通用场景，不含领域内容包）：**

> 工作区请使用 `tests/runs/f1-blind-test/`。  
> 我想入门 <你的主题>，学过 <背景>，每周约 <N> 小时。  
> 按 F1 流程帮我生成个性化入门材料。

**检查点：**

| 检查点 | 期望 |
|--------|------|
| 背景信息不足 | Agent 追问课程/方向/时间，至少收集 2 项后才继续 |
| 搜索先于框架 | 在生成 glossary 之前，Agent 先做 3 渠道搜索；`_work/f1-search-results.md` 先于五件套出现 |
| 全部渠道空结果 | Agent 停下问「是否降级为纯模型生成」；不可静默跳过 |
| 术语表质量 | `glossary.md` ≤25 条，每条有来源标注；标注阅读顺序 |
| 学习地图起点 | `learning-map.md` 对齐学生已有背景（不教已会的 ML 和 Python） |
| 缺口分级 | `prerequisite-gap.md` 有 🔴 blocker / 🟡 建议补 / 🟢 可选 三级 |
| 来源标签 | `starter-resources.md` 每条资源有 `search-verified` / `community-curated` / `model-suggested` 标签 |
| 诚信声明 | `starter-resources.md` 末尾有来源统计 + 诚信勾选清单 |
| 首次练习 | `first-practice.md` 有具体步骤 + 检验标准 + 常见坑，不是「读三篇论文」 |
| 领域内容包匹配 | 若 `embodied-ai` 存在 → 术语表引用 `from-domain-pack`；若不存在 → 不停止，直接搜索+对话生成 |
| 编码 | `python shared/scripts/check_encoding.py tests/runs/f1-blind-test` |

### F4 盲测话术（补充）

> 工作区请使用 `tests/runs/f4-blind-test/`。  
> 允许扫描：`examples/f4-sample-run/project`。  
> 按 F4：确认范围 → 列文件 → 材料索引 → 阶段报告 / 结果摘要 / 阻塞清单。

| 检查点 | 期望 |
|--------|------|
| 无授权路径 | `_work/WAITING_scan_scope.md`，不扫主目录 |
| 交付 | 工作区根有四件：`artifact-index.md` 等 |
| 诚信 | 不得仅凭 `train.py` 写「训练已成功」 |
| 编码 | `python shared/scripts/check_encoding.py tests/runs/f4-blind-test` |

---

## 与 examples/ 的分工

| 路径 | 角色 |
|------|------|
| `examples/<名>/` | 只读样例；通常附 README。F3 成品例外，只保留已冻结的三项样例交付 |
| `tests/runs/<名>/` | 可写跑场；可随时删 |

不要把大体积 PDF 提交进仓库（见根目录 `.gitignore`）。
