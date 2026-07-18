---
name: domain-onboarding
description: >-
  Onboards a student into an unfamiliar research field. Interviews background
  first, then searches across papers/learning-resources/open-source via
  domain-resource-search, and builds five personalized deliverables FROM
  search results: glossary, learning map, prerequisite gap report, starter
  resources, and a first hands-on practice. Use when the student says they are
  new to a field, need a learning path, or ask "where do I start." Trigger
  words: 入门, 不了解, 完全陌生, 怎么开始, 学什么, 零基础, 新手, new to,
  getting started, beginner, onboarding.
---

# 领域入门（domain-onboarding）

F1 工作流技能：背景访谈 → **先搜索** → 基于搜索结果生成五件套 → 诚信声明。

**核心理念：** 框架建立在搜索结果之上，不凭空生成。每条术语和学习阶段可追溯到具体论文、课程或项目。不猜测学生背景，不伪造资源列表。

遵守 `shared/honesty-checklist.md`。工作区根：`campus-research-output/<课题简称>/`（见 `shared/workspace-layout.md`）。

## 何时使用 / 何时不使用

**使用：**
- 「我对 XX 方向完全不了解，想入门」「XX 方向怎么开始学」「零基础怎么学 XX」
- 「帮我梳理 XX 领域的学习路线」「XX 需要哪些前置知识」

**不使用：**
- 只要找论文、做文献综述 → F2 `literature-search-download`
- 只要精读已指定的论文 → F3 `paper-deep-read`
- 只要总结本地实验进展 → F4 `progress-digest`
- 只要写组会材料 → F5 `academic-writing`

## 前置条件

| 依赖 | 说明 |
|------|------|
| 工作区 | `campus-research-output/<课题简称>/` 已初始化，`scope.md` 已确认 |
| `domain-resource-search` | F1 搜索执行技能（本技能步骤 2 调用） |
| 领域内容包（可选） | `domain-packs/<编号>/` 下有 `pack.yaml` + `curriculum.md` + `glossary.md` 则加载加速；无则纯对话生成 |
| 诚信规程 | `shared/honesty-checklist.md`（全程生效） |

## 硬规则（禁止项）

1. **不得**在搜索前生成术语表或学习地图——框架必须基于步骤 2 的搜索结果
2. **不得**伪造「必读经典」名单——每条推荐可追溯到搜索来源或标注 `model-suggested`
3. **不得**猜测学生背景——背景信息由学生自述
4. **不得**绕过付费墙；自动下载仅限 OA/arXiv
5. 术语表**不得**堆砌——精简为核心术语（≤25 条），每条一句解释
6. 中文交付 UTF-8；文件名仅 ASCII；交付前跑 `shared/scripts/check_encoding.py`

## 步骤（有序，可勾选）

### 阶段一：背景访谈

1. [ ] 加载 `shared/honesty-checklist.md`；读 `scope.md` 确认主题、输出语言。
   按 `references/background-interview.md` 收集：已修课程/知识背景、目标子方向、可用时间。
   学生自述，模型不猜测；信息不足时追问补全。

### 阶段二：先搜索（核心改动）

2. [ ] **调用 `domain-resource-search`**，传入主题关键词 + 学生背景摘要。
   若有匹配 `domain-packs/<领域>/` → 加载其术语列表作为搜索辅助关键词；**无包不停止**，直接搜索。
   等待返回 `_work/f1-search-results.md`。

### 阶段三：基于搜索结果生成五件套

3. [ ] 生成 `glossary.md`（模板：`references/glossary-template.md`）：
   - 从搜索结果中**提取**核心术语（≤25 条），每条一句中文解释 + 英文原名
   - 标注推荐阅读顺序
   - 术语来源标注：`from-search`（出现在搜索到的论文/课程中）/ `from-domain-pack` / `model-supplement`

4. [ ] 生成 `learning-map.md`（模板：`references/learning-map-template.md`）：
   - 基于搜索到的课程大纲、综述论文结构**归纳** 3-5 个学习阶段
   - 每阶段有：目标、核心知识点、建议学时、产出检验方式
   - 起点对齐学生已有背景
   - 阶段来源标注：`derived-from-search` / `model-designed`

5. [ ] 生成 `prerequisite-gap.md`（模板：`references/prerequisite-gap-template.md`）：
   - 学生已有知识 vs 学习地图所需前置，逐项对比
   - 缺口分级：必须补（blocker）/ 建议补 / 可选
   - 每个 blocker 给出补救资源（优先从搜索结果中引用）

6. [ ] 生成 `starter-resources.md`（模板：`references/starter-resources-template.md`）：
   - 按 3 渠道分组（论文 / 学习资源 / 开源与实战），不按「必读/选读」
   - 每条包含：标题、链接、一句话说明、来源标签（`search-verified` / `model-suggested` / `community-curated`）
   - 论文优先列综述，再列经典单篇
   - 末尾追加**来源统计**：「本次共命中 X 条，其中 search-verified: A, model-suggested: B, community-curated: C」

7. [ ] 生成 `first-practice.md`（模板：`references/first-practice-template.md`）：
   - 一个具体可执行的小任务（不是「读三篇论文」）
   - 包含：任务描述、预计耗时、检验标准
   - 与学生当前水平匹配——不应要求尚未掌握的前置知识

### 阶段四：收尾

8. [ ] **诚信声明与交付**：
   - 勾选 `shared/honesty-checklist.md` A–E 五类
   - 在 `starter-resources.md` 末尾显式声明：「model-suggested 的资源未经独立验证，请在使用前自行评估」
   - 跑 `shared/scripts/check_encoding.py` 检查全部 5 个交付文件
   - 更新 `_work/state.yaml` + 追加 `research-log.md`
   - 结尾建议：带着 first-practice.md 中的任务进入 F2 文献全景

## 必须问人的点（停下条件与如何继续）

| 停下 | 问什么 | 继续条件 |
|------|--------|----------|
| 背景信息不足（步骤 1） | 请告诉我：已修课程？目标方向？每周可用时间？ | 至少给出「已修课程 + 目标方向」两项 |
| 搜索结果全部为空（步骤 2 返回空） | 未搜到相关资源。是否降级为「纯模型生成」（会标注全部内容需自行核实）？ | 用户确认降级或更换主题词 |
| 付费论文无法获取（步骤 2 论文渠道） | 以下论文为付费内容：<列表>。请放入 `pdfs/user/` 或接受标注 `abstract_only` | 用户补 PDF 或确认降级 |
| 学习地图争议（步骤 4 后） | 该学习路径是否合理？是否需要调整？ | 用户确认或给出修改 |

停车时写入 `_work/WAITING_<描述>.md`，更新 `_work/state.yaml`。

## 交付契约（输入 / 输出路径与字段）

**输入：**
- `scope.md`（已确认的研究范围）
- 学生背景自述（口头对话中收集）
- `_work/f1-search-results.md`（由 `domain-resource-search` 产出）
- 可选：`domain-packs/<编号>/`

**输出（工作区根，文件名冻结自协议 §3）：**

| 文件 | 内容 | 模板 |
|------|------|------|
| `glossary.md` | 核心术语（≤25 条），来源可追溯 | `references/glossary-template.md` |
| `learning-map.md` | 分阶段学习路径（3–5 阶段），基于搜索结果归纳 | `references/learning-map-template.md` |
| `prerequisite-gap.md` | 已有 vs 所需知识对比，缺口分级 | `references/prerequisite-gap-template.md` |
| `starter-resources.md` | 按 3 渠道分组的起步资源，标注来源标签 | `references/starter-resources-template.md` |
| `first-practice.md` | 一个具体可执行的动手任务 | `references/first-practice-template.md` |

## 脚本调用

```bash
# 交付前编码检查
python shared/scripts/check_encoding.py \
  glossary.md learning-map.md prerequisite-gap.md \
  starter-resources.md first-practice.md
```

论文搜索由 `domain-resource-search` 内部调用 F2 脚本；本技能不直接调搜索脚本。

## 失败与回流

| 失败 | 处理 |
|------|------|
| `domain-resource-search` 全部渠道空结果 | 停车问用户是否降级为纯模型生成；确认后所有内容标注 `model-knowledge, MUST verify` |
| 学生背景信息反复不足（≥3 次追问） | 使用默认假设（「无相关前置知识」）并显式标注 |
| 无匹配领域内容包 | **不停止**；直接走搜索+对话生成路径，在交付中注明「无匹配领域内容包」 |
| 编码校验失败 | UTF-8 重写；禁止 cp1252「修复」 |
| 学生中途要切换到 F2/F5 | 保存当前进度，告知已生成文件位置 |

## 推进节奏控制

1. **先搜索，再框架**——步骤 2 完成前不产出任何教学材料
2. 术语表先出（步骤 3），让学生确认核心概念理解无误后再给学习地图
3. 首次练习（步骤 7）必须具体可执行
4. 深度档现阶段固定「标准」

## 参考

- `references/background-interview.md` — 背景访谈提纲
- `references/glossary-template.md` — 术语表模板
- `references/learning-map-template.md` — 学习地图模板
- `references/prerequisite-gap-template.md` — 知识缺口模板
- `references/starter-resources-template.md` — 起步材料模板
- `references/first-practice-template.md` — 首次练习模板
- `shared/honesty-checklist.md` — 学术诚信清单（A–E）
- `shared/workspace-layout.md` — 工作区目录约定
- 上游：`research-workspace`（工作区初始化）；`domain-resource-search`（搜索执行）
- 下游：F2 `literature-landscape-writer`（建议学生带着 first-practice 进入）
- 样例：`examples/f1-sample-run/`
