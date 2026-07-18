---
name: campus-research-orchestrator
description: >-
  Main entry point for MENTOR. Receives the student's research need, matches
  it to F1–F5 via semantic understanding, initializes or recovers the workspace,
  manages state across sessions, and invokes child skills. Never generates
  research content itself. Handles ambiguity with exactly one clarifying
  question. Use when a student enters MENTOR with any research-related ask.
  Trigger words: 科研, 论文, 文献, 入门, 总结, 写作, 组会, 读, 写, 找,
  research, paper, survey, write, read, search, literature.
---

# 调度模块（campus-research-orchestrator）

横切用户入口技能：接收需求 → 语义理解匹配 F1–F5 → 初始化/恢复工作区 → 管理状态 → 调用子技能 → 在确认点停下。

遵守 `shared/honesty-checklist.md`。本技能**不生成科研正文**，只做路由与状态管理。深度档现阶段固定「标准」。

## 何时使用 / 何时不使用

**使用：**
- 用户首次进入 MENTOR，有任何科研相关需求时自动触发
- 用户说「帮我做 XX 方向的文献综述」「我不了解 YY 领域」「总结我这周实验」「帮我写组会材料」
- 用户从上次停车点继续（由本技能检测 `_work/WAITING_*.md` 并恢复）
- 用户在多技能间切换（如「文献找好了，现在帮我仔细读这篇」）

**不使用：**
- 纯聊天、非科研任务（「今天天气怎么样」「帮我写封邮件」）
- 开发者对 MENTOR 自身的调试或修改
- 用户明确指定了技能路径（直接路由，不走匹配）

## 前置条件（依赖哪些技能、哪些文件须已存在）

| 依赖 | 说明 |
|------|------|
| `shared/honesty-checklist.md` | 全程生效的基础规程 |
| `shared/effort-contract.md` | 深度档行为上限（现阶段固定标准） |
| `shared/workspace-layout.md` | 工作区目录约定 |
| `skills/research-workspace/` | 工作区初始化与恢复 |
| `skills/academic-honesty/` | 学术诚信规程（被各子技能在成稿前调用） |
| `skills/domain-onboarding/` | F1 子技能 |
| `skills/domain-resource-search/` | F1 内部技能（被 domain-onboarding 调用） |
| `skills/literature-search-download/` | F2 子技能（入口） |
| `skills/paper-deep-read/` | F3 子技能 |
| `skills/progress-digest/` | F4 子技能 |
| `skills/academic-writing/` | F5 子技能 |
| `AGENTS.md` | 功能索引权威来源（本技能引用，不复制全文） |

## 硬规则（禁止项）

1. **不得**猜测用户意图——含混时必须问一个澄清问题，不假设
2. **不得**自行发明新功能或新技能——只路由到已有 F1–F5 技能
3. **不得**生成科研正文——本技能只做路由，不做内容产出
4. **不得**跳过确认关卡——`scope.md` 未确认、材料不足时必须停车
5. **不得**在无匹配时静默——列出五项功能的一句话描述让用户选
6. **不得**覆盖已有 `scope.md` 或 `_work/state.yaml`，除非用户明确确认
7. 含混时**严格只问一个**澄清问题；不问多选题、不过度细化
8. 中文 UTF-8；若写入过程文件，交付前跑 `shared/scripts/check_encoding.py`

## 步骤（有序，可勾选）

### 阶段一：接收与匹配

1. [ ] 加载 `AGENTS.md`、`shared/honesty-checklist.md`、`shared/effort-contract.md`
2. [ ] 接收用户需求，**根据语义理解**匹配 F1–F5（参照 `AGENTS.md` §1 功能索引）

   **匹配策略（无硬编码优先级）：**
   - Agent 根据用户表述的**真实意图**判断需要哪个功能——不依赖关键词覆盖或优先级序号
   - 若用户需求明显涉及多个功能（如「先入门再找论文」），按自然顺序建议串行并请用户确认
   - 若用户需求含混、可合理归入两个功能 → 问一个澄清问题（步骤 3）
   - 若用户需求完全无法匹配 → 列出五项功能让用户选（步骤 4）

3. [ ] **含混处理（只在匹配不确定时执行）**：严格只问一个澄清问题，如：
   - 「你想先了解这个领域的基础（入门路径），还是直接找相关论文？」
   - 「你是想总结本地实验进展，还是写组会要用的材料？」
   - 不问「你想做 A 还是 B 还是 C 还是 D 还是 E？」
   - 不问「请你详细描述你的需求」——太模糊等于没问

4. [ ] **无匹配处理**：列出五项功能的一句话描述：
   ```markdown
   MENTOR 目前可以做这些：

   1. **入门陌生领域** — 生成学习地图、术语表、起步材料、首次练习
   2. **文献检索与全景** — 找论文、写综述、画关系图
   3. **单篇深度阅读** — 逐段读懂一篇论文、产出阅读报告
   4. **本地阶段总结** — 扫描你的实验日志和代码，生成进展报告
   5. **学术写作** — 组会一页纸、PPT 大纲、阶段技术说明、润色

   你想做哪一项？（说编号或直接描述即可）
   ```

### 阶段二：工作区管理

5. [ ] 检查工作区状态：
   - `campus-research-output/` 下无课题目录 → 进入「初始化工作区」
   - 已有课题目录但 `scope.md` 缺失或未确认 → 补完或确认
   - 已有完整工作区，`_work/WAITING_*.md` 存在 → 进入「恢复工作区」
   - 已有完整工作区，状态正常 → 直接读取 `scope.md` + `state.yaml`，继续

6. [ ] **初始化工作区**（调用 `research-workspace` 流程）：
   - 询问课题简称（ASCII slug）
   - 创建 `campus-research-output/<简称>/` 目录树
   - 访谈并写入 `scope.md`（按 `research-workspace/references/scope-template.md`）
   - 写入 `_work/state.yaml` 初始状态
   - 写入 `research-log.md` 首条记录
   - scope.md 未确认 → **停车**（`waiting_for: scope_confirm`）

7. [ ] **恢复工作区**（调用 `research-workspace` 恢复流程）：
   - 按 `research-workspace/references/recovery-flow.md` 决策树执行
   - 处理 `_work/WAITING_*.md`（优先最早的一个）
   - 向用户展示上次状态并确认继续或调整

### 阶段三：调用与收尾

8. [ ] 调用对应子技能（传递当前 `scope.md` 和 `state.yaml` 上下文）：
   - F1 → `domain-onboarding`
   - F2 → `literature-search-download`（F2 入口；后续由文献链技能串联）
   - F3 → `paper-deep-read`
   - F4 → `progress-digest`
   - F5 → `academic-writing`

9. [ ] 子技能返回后：
   - 更新 `_work/state.yaml`（`last_updated`、`current_function`、`current_skill`、`step` 重置为 1）
   - 追加 `research-log.md`（记录：时间、调用技能、交付文件列表、停车原因（如有））
   - 若有卡点（子技能返回 BLOCKED 或 WAITING）→ 写入 `_work/WAITING_<描述>.md`

10. [ ] 向用户汇报：做了什么 → 产出了什么 → 下一步建议 → 如有卡点说明等什么

## 必须问人的点（停下条件与如何继续）

| 停下 | 问什么 | 继续条件 |
|------|--------|----------|
| 意图含混（步骤 3） | 一个澄清问题（如「入门还是找论文？」） | 用户选择其中一个方向 |
| 无匹配（步骤 4） | 列出五项功能，你想做哪一项？ | 用户选择（说编号或描述） |
| 课题简称未定（步骤 6） | 请给出一个英文简称（如 `embodied-ai`） | 用户给出合法 ASCII slug |
| scope.md 未确认（步骤 6） | 以上范围说明是否正确？有需补充的吗？ | 用户确认 |
| 恢复时有 WAITING 文件（步骤 7） | 上次我们在等「X」。解决了吗？ | 用户确认已解决或提供输入 |
| 子技能返回 BLOCKED | 子技能因「X」暂停。你想怎么处理？ | 用户选择（解决 / 跳过 / 换方向） |
| 用户想跨功能切换 | 当前进度会保存。确认切换到「X」功能？ | 用户确认 |
| 无法继续（三次停车） | 当前任务已暂停三次。你想跳过、换方式，还是今天先到这里？ | 用户选择 |

停车时写入 `_work/WAITING_<描述>.md`，更新 `_work/state.yaml` 的 `waiting_for` 字段。

## 交付契约（输入 / 输出路径与字段）

**输入：** 用户的自然语言科研需求（一句话即可，不要求结构化）。

**输出（本技能不产生终稿文件）：**

| 产出 | 路径 | 说明 |
|------|------|------|
| 工作区初始化 | `campus-research-output/<简称>/` | 目录树 + `scope.md` + `_work/state.yaml` + `research-log.md` |
| 状态更新 | `_work/state.yaml` | 每次路由和步骤转换后更新 |
| 停车说明 | `_work/WAITING_<描述>.md` | 流程暂停时写入 |
| 日志追加 | `research-log.md` | 每次技能调用后追加 |

**本技能不负责**子技能的具体交付文件（如 `learning-map.md`、`survey.md` 等）——这些由各子技能按其交付契约生成。

## 脚本调用（若有，给命令模板）

本技能以 Agent 匹配与路由为主；无专用脚本。

```bash
# 若需检查工作区完整性（可选）
ls campus-research-output/<简称>/scope.md
ls campus-research-output/<简称>/_work/state.yaml

# 编码检查（仅本技能写入的过程文件）
python shared/scripts/check_encoding.py research-log.md
```

## 失败与回流

| 失败 | 处理 |
|------|------|
| 无法识别意图（路由失败） | 列出五项功能；不猜测、不随机路由 |
| 用户说了一句但匹配到两个功能 | 问一个澄清问题；不同时启动两个技能 |
| 工作区初始化失败（权限不足等） | 报告错误，建议用户检查权限或更换输出根路径 |
| scope.md 用户多次拒绝（≥3 次） | 保留草稿为 `_work/scope-draft.md`；建议用户自行编辑 |
| 子技能不存在或未实现 | 诚实告知「该功能尚未完成」；不假装执行 |
| 子技能执行失败 | 读取 state.yaml 确认当前步骤；询问用户是否重试、回退或跳过 |
| 恢复时 state.yaml 损坏 | 按 `research-workspace/references/recovery-flow.md` 决策树处理；无法恢复则视为新课题 |
| 用户要求同时做多项（如「先入门再找论文」） | 建议串行：先 F1 打基础，再 F2 搜索——因为 F1 产出的知识框架能让 F2 检索更精准 |
| 用户在子技能中途直接找 orchestrator 说话 | 保存子技能当前进度（更新 state.yaml），处理新需求，之后再恢复 |

## 参考（链接 references/）

- `references/routing-table.md` — F1–F5 功能匹配参考（触发词、边界案例；无硬编码优先级）
- `AGENTS.md` — 智能体冷启动功能索引（权威来源）
- `shared/honesty-checklist.md` — 学术诚信清单
- `shared/effort-contract.md` — 深度档行为上限
- `shared/workspace-layout.md` — 工作区目录约定
- `docs/接口与协议.md` — 协作协议权威来源
- 下游全部技能：`research-workspace`、`academic-honesty`、`domain-onboarding` (F1)、F2 文献链、`paper-deep-read` (F3)、`progress-digest` (F4)、`academic-writing` (F5)
