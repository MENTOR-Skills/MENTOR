# tests/ — 本地可跑测试工作区

本目录用于 **脚本冒烟** 与 **Cursor 盲测跑场**。  
`examples/` 放只读样例与说明；真正跑起来的产物写到 `tests/runs/<用例名>/`，默认不提交 Git。

```text
tests/
├── README.md                 # 本说明（含 Cursor 前置步骤）
├── scripts/                  # 一键脚本冒烟
│   ├── run_f2_script_smoke.py
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
2. 确认已拿到含 F2 技能的分支（例如 `feat/f2-landscape`），且存在目录：
   - `skills/literature-search-download/`
   - `skills/literature-reader/`
   - `skills/literature-landscape-writer/`
   - `skills/survey-writer/`
   - `skills/citation-verifier/`
   - `skills/survey-visualizer/`

### 2. 把技能装进 Cursor（二选一）

**A. 推荐（本仓库联调）**  
在对话中明确：

> 使用本仓库 `MENTOR/skills/` 下的 F2 技能，不要用我全局目录里可能过期的同名 skill。

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

### 6. 发起盲测对话（示例话术）

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
python tests/scripts/run_f2_script_smoke.py
python tests/scripts/run_f4_script_smoke.py
```

产物分别写入 `tests/runs/f2-script-smoke/`、`tests/runs/f4-script-smoke/`。  
F2 说明见 `examples/f2-script-smoke/README.md`；F4 说明见 `examples/f4-sample-run/README.md`。

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
| `examples/<名>/` | 只读样例 + **必须有 README**（案例 / skills / 交付物） |
| `tests/runs/<名>/` | 可写跑场；可随时删 |

不要把大体积 PDF 提交进仓库（见根目录 `.gitignore`）。
