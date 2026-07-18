---
name: research-workspace
description: >-
  Initializes and maintains the per-topic workspace under
  campus-research-output/, writes scope.md and _work/state.yaml, and
  handles cross-session recovery. Use when starting a new research topic,
  resuming from a prior session, or any F1–F5 skill needs to verify
  workspace integrity. Trigger words: workspace, setup, initialize, resume,
  continue, 工作区, 初始化, 继续, 新建课题.
---

# 工作区约定（research-workspace）

横切规程技能：初始化用户课题工作区目录、写入 `scope.md` 与 `_work/state.yaml`、处理跨次会话恢复。

遵守 `shared/honesty-checklist.md`。本技能不生成科研正文，只负责目录与状态文件的创建和维护。目录结构以 `shared/workspace-layout.md` 为准。

## 何时使用 / 何时不使用

**使用：**
- 用户首次进入 MENTOR、开始一个新课题
- `campus-research-orchestrator` 检测到工作区不存在或 `scope.md` 缺失
- 用户说「继续」「接着上次」「初始化工作区」「新建课题」
- 跨次会话恢复：检测到 `_work/WAITING_*.md` 或需从 `state.yaml` 恢复上下文

**不使用：**
- 工作区已完整且状态匹配当前任务（技能直接读取即可，不重新初始化）
- 用户只想聊天、了解功能，尚未确定课题
- 纯开发/调试 MENTOR 自身（不创建用户工作区）

## 前置条件（依赖哪些技能、哪些文件须已存在）

- 用户提供课题简称（ASCII slug，小写英文+数字+连字符，最长 40 字符）
- 可选：用户指定非默认输出根路径（默认 `campus-research-output/`）
- 必须加载：`shared/workspace-layout.md`（目录结构权威来源）、`shared/effort-contract.md`（深度档规则）
- 无上游技能依赖（基础规程，被 orchestrator 调用）

## 硬规则（禁止项）

1. **不得**在 `campus-research-output/` 之外创建工作区，除非用户明确指定其他根路径并写入 `scope.md`
2. **不得**覆盖已有 `scope.md` 或 `_work/state.yaml`，除非用户明确确认（先展示差异）
3. 课题简称**仅 ASCII**（小写字母、数字、连字符），禁止中文或空格
4. `scope.md` 必须经用户确认（口头或显式同意）后，才允许后续 F1–F5 技能开始产出
5. `_work/state.yaml` 必须在每次步骤转换和每次停车时更新
6. 所有文件名和目录名仅 ASCII；中文正文 UTF-8

## 步骤（有序，可勾选）

### 新建工作区

1. [ ] 询问课题简称（ASCII slug）；若用户不确定，根据主题建议一个英文简称并请用户确认
2. [ ] 检查 `campus-research-output/<简称>/` 是否已存在
   - 若存在 → 转入「恢复工作区」流程
   - 若不存在 → 继续步骤 3
3. [ ] 创建目录树：`<简称>/`、`<简称>/_work/`、`<简称>/pdfs/auto/`、`<简称>/pdfs/user/`、`<简称>/reading-reports/`、`<简称>/viz/`
4. [ ] 访谈用户，收集 `scope.md` 必填信息（按 `references/scope-template.md`）：
   - 主题描述、时间范围、深度档（现阶段固定「标准」）、输出语言
   - 期刊/会议偏好（可选）、允许 F4 扫描的本地路径（可选，可后续补）
   - 领域内容包编号（可选）、禁止事项
5. [ ] 写入 `scope.md`，展示给用户确认；未确认 → 回到步骤 4 修改
6. [ ] 写入 `_work/state.yaml` 初始状态：
   ```yaml
   session:
     last_updated: "<ISO时间>"
     current_function: null
     current_skill: research-workspace
     depth: standard
     step: 6
     waiting_for: null
     completed_steps: [1,2,3,4,5]
   ```
7. [ ] 写入 `research-log.md` 首条记录（时间、课题简称、scope.md 已确认）
8. [ ] 通知 orchestrator：工作区就绪，可路由到 F1–F5

### 恢复工作区（跨次会话）

1. [ ] 列出 `campus-research-output/` 下已有课题；让用户选择或确认当前课题
2. [ ] 检查 `_work/` 下是否存在 `WAITING_*.md` → 如有，读取并按优先级处理（创建时间最早的优先）
3. [ ] 读取 `_work/state.yaml` 恢复上下文 
4. [ ] 读取 `research-log.md` 最近 3 条记录
5. [ ] 向用户确认：「上次我们做到了 X，现在继续还是调整？」
6. [ ] 用户确认后更新 `state.yaml`（`last_updated`、清除 `waiting_for`），通知 orchestrator

## 必须问人的点（停下条件与如何继续）

| 停下 | 问什么 | 继续条件 |
|------|--------|----------|
| 课题简称未定 | 请给出一个英文简称（如 `embodied-ai`、`gnn-survey`）| 用户给出合法 ASCII slug |
| 目录已存在 | `campus-research-output/<简称>/` 已存在。继续使用现有工作区，还是新建？ | 用户选择继续或另起名 |
| scope.md 未确认 | 以上范围说明是否正确？有需要补充或修改的吗？ | 用户确认或给出修改 |
| 恢复时有 WAITING 文件 | 上次我们在等「X」。这个问题解决了吗？ | 用户确认已解决或提供所需输入 |
| 多个工作区存在 | 检测到 N 个已有课题。你要继续哪个？ | 用户选择 |
| state.yaml 损坏或缺失 | 工作区目录存在但状态文件不可读。是否重建状态（可能丢失上次进度），还是手动检查？ | 用户选择重建或手动修复 |

停车时写入 `_work/WAITING_<描述>.md`，更新 `_work/state.yaml` 的 `waiting_for` 字段。

## 交付契约（输入 / 输出路径与字段）

**输入：** 用户课题简称（ASCII）+ scope.md 各字段信息（口头或已有材料）。

**输出（工作区根 `campus-research-output/<简称>/`）：**

| 文件 | 内容 | 模板 |
|------|------|------|
| `scope.md` | 已确认的研究范围说明 | `references/scope-template.md` |
| `_work/state.yaml` | 会话状态（字段说明见 `references/state-yaml-reference.md`） | — |
| `research-log.md` | 初始化记录或恢复记录（追加） | — |

**中间产物（`_work/`）：** `WAITING_*.md`（停车时写入）。

## 脚本调用（若有，给命令模板）

本技能以 Agent 创建目录和文件为主；无专用脚本。

```bash
# 若需批量创建目录（Agent 可逐条 mkdir，此处为备选）
mkdir -p campus-research-output/<简称>/_work
mkdir -p campus-research-output/<简称>/pdfs/auto
mkdir -p campus-research-output/<简称>/pdfs/user
mkdir -p campus-research-output/<简称>/reading-reports
mkdir -p campus-research-output/<简称>/viz

# 成稿前编码检查
python shared/scripts/check_encoding.py scope.md _work/state.yaml
```

## 失败与回流

| 失败 | 处理 |
|------|------|
| 课题简称不合法（含中文/空格/特殊字符） | 拒绝，请用户给出 ASCII slug；自动建议（如将中文转拼音）并请用户确认 |
| 目录创建权限不足 | 报告错误，建议用户检查文件系统权限或更换输出根路径 |
| scope.md 用户多次拒绝（≥3 次） | 保留当前草稿为 `_work/scope-draft.md`；建议用户自行编辑后继续 |
| 恢复时 state.yaml 损坏且 research-log.md 为空 | 视为新课题；询问用户是否重建 |
| 无 Python 环境（无法跑编码检查） | 按 `shared/encoding-utf8.md` 规则手动确保 UTF-8；在 `research-log.md` 中注明「未跑自动编码检查」 |

## 参考（链接 references/）

- `references/scope-template.md` — scope.md 填写模板
- `references/state-yaml-reference.md` — state.yaml 字段说明
- `references/recovery-flow.md` — 跨次会话恢复决策流程
- `shared/workspace-layout.md` — 工作区目录结构权威来源
- `shared/effort-contract.md` — 深度档行为上限
- `shared/encoding-utf8.md` — 编码规范
- 上游：无（基础规程）；下游：`campus-research-orchestrator` 及全部 F1–F5 技能
