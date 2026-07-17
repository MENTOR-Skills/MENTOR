---
name: literature-search-download
description: >-
  Cascaded literature search via OpenAlex then limited arXiv, downloads only
  shortlist OA/arXiv PDFs, then pauses for the user to supply paywalled PDFs.
  Use when finding papers or obtaining full texts for a literature survey /
  F2 landscape. Preferred venues must come from the user or scope — never
  hardcode venue names.
---

# 文献检索与下载（literature-search-download）

F2 执行技能：分级检索 → 合并去重 → 提出精读候选 → 仅对候选尝试开放获取下载 → 付费墙停车。

遵守 `shared/honesty-checklist.md`。工作区根：`campus-research-output/<课题简称>/`（见 `shared/workspace-layout.md`）。

## 何时使用 / 何时不使用

**使用：** 用户要找论文、做相关工作梳理、F2 文献全景；或 F1 需要可核对文献列表时调用本技能。

**不使用：** 用户已指定单篇 PDF/链接要深读（进 F3）；只要阶段总结（F4）；只要写组会材料且文献库已齐（F5）。

## 前置条件（依赖哪些技能、哪些文件须已存在）

- 课题工作区已初始化；`scope.md` 已写入主题、年份范围、深度档（现阶段按标准档）。
- 可选：`_work/preferred_venues.txt`（每行一个 venue；空则跳过 Tier-1 venue 过滤）。
- 诚信规程：`shared/honesty-checklist.md`。

## 硬规则（禁止项）

1. **禁止**在本 skill / 脚本默认参数里写死任何会议或期刊名称。优先 venue 只能来自用户当面指定，或 `scope.md` / `_work/preferred_venues.txt` 中用户确认过的列表。
2. **禁止**对检索大池批量下载 PDF。只对精读 shortlist 尝试自动下载。
3. **禁止**绕过付费墙。自动下载仅限 OA 与 arXiv。
4. 检索与自动下载结束后 **必须挂起**，写入 `_work/WAITING_user_pdf.md`，并更新 `_work/state.yaml` 的 `waiting_for: user_pdf`。
5. `access_status` 仅使用协议枚举：`fulltext` / `abstract_only` / `waiting_user_pdf` / `unknown`（来源用 `pdf_path` / `arxiv_id` 表达，不塞进 status）。

## 步骤（有序，可勾选）

1. [ ] 确认主题、年份、是否提供 preferred venues → 写入/更新 `scope.md`。
2. [ ] 分级检索（Cascade）：

| 级别 | 做法 | 何时进入下一级 |
|------|------|----------------|
| **Tier-1** | OpenAlex + 用户首选 venue | 相关命中不足阈值（默认 8） |
| **Tier-2** | OpenAlex 不限 venue（或次选）；`peer_reviewed` 优先 | 仍不足 |
| **Tier-3** | arXiv，默认 max≤10 | 仅补最新/缺口；预印本须标明 |

3. [ ] Agent 在 `_work/papers_all.jsonl` 上筛选 → `_work/shortlist.json`（默认 5–12 篇；标准档请用户确认后再精读）。
4. [ ] 仅对 shortlist 下载到 `pdfs/auto/`。
5. [ ] 运行 `write_wait_gate.py` → `_work/WAITING_user_pdf.md`；更新 `state.yaml`。
6. [ ] **停止**，等待用户将无法自动获取的 PDF 放入 `pdfs/user/`。
7. [ ] 用户确认继续后运行 `register_user_pdfs.py`，再进入 `literature-reader`。

## 必须问人的点（停下条件与如何继续）

| 停下 | 问什么 | 继续条件 |
|------|--------|----------|
| 检索前 | 主题、年份、preferred venues（可不提供） | 写入 scope |
| shortlist 后（标准档） | 候选是否合适、是否增删 | 用户确认 shortlist |
| 自动下载后 | 列出缺全文条目，请补 PDF | 用户放入 `pdfs/user/` 并回复继续；或明确允许摘要级（标 `abstract_only`） |

停车时写入 `_work/WAITING_user_pdf.md`（结构见 `shared/workspace-layout.md`），并追加 `research-log.md`。

## 交付契约（输入 / 输出路径与字段）

**输入：** `scope.md`；可选 `_work/preferred_venues.txt`。

**过程输出（`_work/`）：**

- `papers_all.jsonl` / `shortlist.json` / `access.json`
- `WAITING_user_pdf.md`

**侧写：** `pdfs/auto/*.pdf`；用户补档在 `pdfs/user/`。

**shortlist 条目建议字段：** `id`, `title`, `authors`, `year`, `venue`, `doi`, `arxiv_id`, `url`, `pdf_path`, `access_status`（协议枚举）, `peer_reviewed`（可选）。

## 脚本调用（若有，给命令模板）

```bash
# 工作目录 = campus-research-output/<课题简称>/
python skills/literature-search-download/scripts/tiered_search.py \
  --query "user topic" \
  --year 2024-2026 \
  --venues-file _work/preferred_venues.txt \
  --tier1-min 8 \
  --arxiv-max 10 \
  --out-dir _work/

python skills/literature-search-download/scripts/shortlist_to_jsonl.py \
  --in _work/shortlist.json --out _work/shortlist.jsonl

python skills/literature-search-download/scripts/download_pdf.py \
  --jsonl _work/shortlist.jsonl \
  --output-dir pdfs/auto \
  --access-out _work/access.json \
  --max-downloads 12

python skills/literature-search-download/scripts/write_wait_gate.py \
  --shortlist _work/shortlist.json \
  --out _work/WAITING_user_pdf.md

# 用户补 PDF 后
python skills/literature-search-download/scripts/register_user_pdfs.py \
  --shortlist _work/shortlist.json \
  --user-dir pdfs/user \
  --pdf-dir pdfs/user \
  --out _work/shortlist.json
```

也可分步：`search_openalex.py` / `search_arxiv.py` / `merge_papers.py`。

## 失败与回流

| 失败 | 处理 |
|------|------|
| OpenAlex/arXiv 超时或空结果 | 放宽 query / 请用户改主题词；记录于 `research-log.md`；不得伪造命中 |
| 下载失败 | `access_status: waiting_user_pdf`，进 WAITING，不假装已有全文 |
| 用户拒绝补 PDF | 对缺失篇目标 `abstract_only`，后续精读保持摘要级 |

## 参考（链接 references/）

- `references/query-tips.md`
- `references/venues-from-user.md`
- 下游：`literature-reader` → `literature-landscape-writer` → `citation-verifier` → `survey-visualizer`
- 编码：`shared/encoding-utf8.md`；校验：`python shared/scripts/check_encoding.py <路径>`
