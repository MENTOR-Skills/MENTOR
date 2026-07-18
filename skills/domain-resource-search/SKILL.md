---
name: domain-resource-search
description: >-
  Searches across papers, learning resources, and open-source projects for
  F1 domain onboarding. Called by domain-onboarding after background interview;
  not invoked directly by end users. Returns structured, source-tagged resource
  lists that domain-onboarding uses to build glossary, learning map, and
  starter resources. Trigger words: none (internal skill).
---

# 领域资源搜索（domain-resource-search）

F1 内部搜索执行技能：接收主题 + 学生背景 → 3 渠道并行搜索 → 返回带来源标签的结构化资源列表。

遵守 `shared/honesty-checklist.md`。**不直接面向用户**——由 `domain-onboarding` 在背景访谈后调用。

## 何时使用 / 何时不使用

**使用：** `domain-onboarding` 完成背景访谈后调用，获取用于构建知识框架和起步材料的原始资源。

**不使用：**
- 用户直接要求（应通过 orchestrator 进入 `domain-onboarding`）
- 专题文献全景 → F2 `literature-search-download`
- 只要单篇论文 → F3 `paper-deep-read`
- 已有足够的本地或内容包材料，不需要搜索

## 前置条件

| 依赖 | 说明 |
|------|------|
| 调用方 | `domain-onboarding` 提供：主题关键词、学生背景摘要、可选领域内容包术语列表 |
| F2 检索脚本（可选） | `skills/literature-search-download/scripts/search_arxiv.py`、`search_openalex.py`；可用则跑，不可用则 Agent 搜索降级 |
| `shared/honesty-checklist.md` | 全程生效 |
| 工作区 | 由调用方 `domain-onboarding` 确保已初始化 |

## 硬规则（禁止项）

1. **不得**编造论文标题、课程名、GitHub 仓库名——每条资源必须可追溯到搜索结果
2. **不得**绕过付费墙；论文自动下载仅限 OA/arXiv
3. **不得**在搜索前让学生做渠道选择题——3 渠道默认全跑
4. 每条资源必须标注来源标签：`search-verified` / `model-suggested` / `community-curated`
5. 论文优先列综述（survey/review），再列经典单篇
6. 中文 UTF-8；若写入过程文件，交付前跑 `shared/scripts/check_encoding.py`

## 步骤（有序，可勾选）

### 阶段一：接收与准备

1. [ ] 从 `domain-onboarding` 接收：主题关键词、学生背景摘要、输出语言、可选领域内容包术语列表

### 阶段二：3 渠道并行搜索

2. [ ] **渠道 1 — 论文**（标签：`search-verified`）：
   - 若 F2 脚本可用 → 跑 `search_arxiv.py` + `search_openalex.py`，各取 5–8 篇
   - 若脚本不可用 → Agent 搜索 arXiv/OpenAlex/Semantic Scholar
   - 优先取综述（survey/review/tutorial），其次高引经典单篇
   - 输出：标题、作者、年份、链接、一句话说明

3. [ ] **渠道 2 — 学习资源**（标签：`model-suggested`）：
   - Agent 搜索公开课程（MIT OCW / Coursera / edX / 国内 MOOC）、教材、知名教程
   - 输出：资源名、平台/来源、链接、一句话说明、适合初学者/进阶

4. [ ] **渠道 3 — 开源与实战**（标签：`community-curated`）：
   - Agent 搜索 GitHub topic / awesome-list、数据集/基准（Papers with Code / Hugging Face / Kaggle）
   - 输出：仓库名/数据集名、链接、一句话说明、活跃度（最近更新/star 大致量级）

5. [ ] 合并三个渠道的结果，按渠道分组写入 `_work/f1-search-results.md`（过程文件，供 `domain-onboarding` 步骤 3–6 消费）

### 阶段三：返回

6. [ ] 向 `domain-onboarding` 返回：搜索结果摘要（各渠道命中数）+ `_work/f1-search-results.md` 路径

## 必须问人的点

本技能**不直接与用户交互**。若搜索全部渠道返回空，将空结果返回给 `domain-onboarding`，由它决定是否停车。

## 交付契约（输入 / 输出）

**输入（由 `domain-onboarding` 传入）：**
- 主题关键词（英文，用于搜索 query）
- 学生背景摘要（用于过滤难度不匹配的资源）
- 可选：领域内容包术语列表（用于优化搜索 query）

**输出（过程文件，供 `domain-onboarding` 读取）：**

| 文件 | 内容 |
|------|------|
| `_work/f1-search-results.md` | 3 渠道分组资源列表，每条标注来源标签 |

**不产生终稿文件。** 终稿（glossary.md 等）由 `domain-onboarding` 基于本技能结果生成。

## 脚本调用

```bash
# 渠道 1：论文（工作目录 = campus-research-output/<课题简称>/）
python skills/literature-search-download/scripts/search_openalex.py \
  --query "<topic keywords>" --year 2021-2026 --limit 8 --out _work/f1_openalex.jsonl

python skills/literature-search-download/scripts/search_arxiv.py \
  --query "<topic keywords>" --max 5 --out _work/f1_arxiv.jsonl

# 编码检查（仅过程文件）
python shared/scripts/check_encoding.py _work/f1-search-results.md
```

渠道 2、3 由 Agent 通过 WebSearch/WebFetch 完成；无专用脚本。

## 失败与回流

| 失败 | 处理 |
|------|------|
| OpenAlex/arXiv 超时或空结果 | 放宽 query 重试一次；仍空则 Agent 搜索降级；标注「论文渠道命中少」 |
| 三个渠道全部无结果 | 返回空结果给 `domain-onboarding`；由它决定：纯模型生成并标注、还是停车 |
| 学习资源/开源渠道命中极少（<3 条） | 正常返回，标注命中数；不编造补足 |
| F2 脚本路径不可用 | 静默降级为 Agent 搜索；不影响技能执行 |

## 参考

- 上游：`domain-onboarding`（唯一调用方）
- F2 脚本：`skills/literature-search-download/scripts/search_arxiv.py`、`search_openalex.py`
- 诚信：`shared/honesty-checklist.md`
- 编码：`shared/scripts/check_encoding.py`
