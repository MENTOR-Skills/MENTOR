---
name: survey-writer
description: >-
  Writes standalone literature surveys (survey.md) or Related Work
  (related-work.md) from references.json only. One skill, four style packs:
  narrative review, taxonomic survey (default), systematic mapping, and
  related-work section. STEM-oriented; always run citation-verifier and
  check_encoding before treating output as finished.
---

# 综述撰写（survey-writer）

F2 **可选扩展**技能：文献库与（建议）全景说明就绪后，按用户选的**写法包**产出 `survey.md` 或 `related-work.md`。

**一个技能、多种写法。** 理工科不同方向共用本技能；差别在写法包与模板，不在另建技能目录。

基本版 F2 完成标准仍是全景 + 精读清单 + 关系图；本技能在用户明确要求「写综述 / Related Work / 投稿向草稿」时启用。

遵守 `shared/honesty-checklist.md`。

## 何时使用 / 何时不使用

**使用：**

- 用户明确要求长篇综述、survey 草稿、系统梳理稿，或论文 Related Work 章节；
- `references.json` 已有足够 `reading_notes`，且用户确认进入「综述扩展」模式；
- 全景主链（检索 → 入库 → 全景）已完成或用户接受跳过全景、直接写综述。

**不使用：**

- 只要专题全景与精读建议 → 用 `literature-landscape-writer`；
- 文献库空、或大量 `abstract_only` 且用户未声明接受摘要级局限；
- 代替用户向期刊正式投稿排版（本技能出 Markdown，不出 PDF/LaTeX 相机稿）；
- 用户尚未提供 Related Work 所需的「本文贡献 / 定位」说明。

## 前置条件（依赖哪些技能、哪些文件须已存在）

| 依赖 | 说明 |
|------|------|
| `references.json` | `papers` 非空；目标篇目有完整 `reading_notes`（至少 problem / method / results / limitations） |
| `scope.md` | 已确认主题、时间范围、输出语言 |
| `literature-landscape.md` | **建议已有**（便于主题分节与缺口对齐）；无全景亦可，须先与用户确认大纲 |
| 写法包选择 | 用户或 Agent 在步骤 1 确认（见「写法家族」） |
| Related Work 额外输入 | 用户给出本文贡献、方法要点或 positioning 草稿（可写入 `scope.md` 或 `_work/contribution.md`） |
| 系统梳理额外过程 | 选「系统梳理/映射」时，须能写 `_work/selection-protocol.md`（模板见 references） |

**建议门槛（未达须声明局限或回流，不硬凑篇幅）：**

| 模式 | 建议下限 |
|------|----------|
| 独立综述 / 叙事 / 分类 / 系统梳理 | ≥ **8** 篇有 `reading_notes` |
| Related Work | ≥ **5** 篇 + 用户贡献说明 |

## 硬规则（禁止项）

1. **只引用** `references.json` 中的条目；不得编造未入库文献、DOI 或实验数字。
2. 按**主题 / 方法族 / 问题设定**综合叙述，禁止终稿主结构为编年流水账或「A 说…B 说…」逐篇摘要。
3. 预印本正文或参考文献中标 `(preprint)`；推断性关系或判断标注「推断」。
4. 主张须能回溯到 `reading_notes` 或明确摘要级依据；无证据标缺口，不静默升级语气。
5. **分类框架 / 叙事权威**默认不把检索协议、纳入排除表、漏斗统计作为正文一级结构（可放 `_work/` 或附录）。
6. **系统梳理/映射**例外：选文过程须写 `_work/selection-protocol.md`；正文可摘要过程，但不得伪造 PRISMA 数字。
7. **不要**在正文写「已全部核验」；核验结果进 `_work/CITATION_AUDIT.*`。
8. 中文 UTF-8；交付前跑 `shared/scripts/check_encoding.py`。
9. 中文独立综述约 **2500+ 字**（或等价英文）；Related Work 更短；演示夹具可更短但须标明「演示级」。

## 写法家族（选一个，步骤 1 确认）

| 写法包 | 对标习惯 | 主交付 | 模板 |
|--------|----------|--------|------|
| **叙事权威综述** | Nature Reviews、Annual Reviews、ACS *Chemical Reviews* | `survey.md` | `references/narrative-review-template.md` |
| **分类框架综述** | ACM CSUR、多数 CS·EE survey（**默认**） | `survey.md` | `references/survey-template.md` |
| **系统梳理/映射** | PRISMA-lite、IEEE Access Topical Review、SEGRESS 思路 | `survey.md` + `_work/selection-protocol.md` | `references/systematic-mapping-template.md` + `selection-protocol-template.md` |
| **Related Work** | 论文章节 | `related-work.md` | `references/related-work-template.md` |

对照表与选型话术见 `references/style-packs.md`；Venue 细节见 `references/venue-writing-norms.md`；成稿自检见 `references/quality-gate.md`。

## 步骤（有序，可勾选）

1. [ ] 加载 `shared/honesty-checklist.md`；读 `references.json`、`scope.md`；建议读 `literature-landscape.md`。
2. [ ] 向用户确认**写法包**（上表四选一）、语言、引用风格（数字序 `[1]` 或作者—年份）；Related Work 须收集**本文贡献**。
3. [ ] 对照建议门槛：篇数 / 笔记是否够；不足 → 声明局限或回流 `literature-search-download` / `literature-reader`（见「失败与回流」）。
4. [ ] 若选**系统梳理/映射** → 先写 `_work/selection-protocol.md`（检索来源、纳入/排除、漏斗或映射表），再写正文。
5. [ ] 基于库内文献拟定 **3+ 主题节**大纲，写入 `_work/survey-outline.md`（可选）；标准档建议请用户点头。
6. [ ] 按写法包模板撰写 `survey.md` 或 `related-work.md`；比较表 / 开放问题 / positioning 须挂库内条目。
7. [ ] 自检 `references/quality-gate.md` 勾选项。
8. [ ] 运行 `citation-verifier`；失败则改稿或标未核实，不得删引用充数。
9. [ ] 跑 `check_encoding.py`；更新 `research-log.md` / `_work/state.yaml`（`current_skill: survey-writer`）。

## 必须问人的点（停下条件与如何继续）

| 停下 | 问什么 | 继续条件 |
|------|--------|----------|
| 启用前 | 四写法包选哪个？语言与引用风格？ | 用户确认 |
| Related Work | 本文贡献、与现有工作的差异点？ | 用户给出 positioning 要点 |
| 语料不足 | 继续写「局限声明版」还是回流补文献？ | 用户选择 |
| 大纲后 | 主题分节是否合适？ | 用户确认或修改大纲 |
| 系统梳理 | 纳入/排除标准是否与 `scope.md` 一致？ | 用户确认 protocol |
| 核验失败 | 删主张 / 标未核实 / 补库字段？ | 用户选择后改稿 |

## 交付契约（输入 / 输出路径与字段）

**输入：** `references.json`、`scope.md`；建议 `literature-landscape.md`；Related Work 需用户贡献说明；系统梳理需可写的选文过程信息。

**输出（工作区根，按模式）：**

| 文件 | 何时 |
|------|------|
| `survey.md` | 叙事 / 分类 / 系统梳理三种独立综述 |
| `related-work.md` | Related Work 写法包 |
| `_work/selection-protocol.md` | **仅**系统梳理/映射（必填过程文件） |
| `_work/survey-outline.md` | 可选大纲 |
| `_work/contribution.md` | 可选：用户贡献要点归档 |

## 脚本调用（若有，给命令模板）

在研究工作区根执行（路径按实际调整）：

```bash
# 1. 引用核对（见 citation-verifier 技能）
python skills/citation-verifier/scripts/refs_to_verify_input.py \
  --references references.json \
  --out _work/candidates_for_verify.json

python skills/citation-verifier/scripts/verify_citations.py \
  --input _work/candidates_for_verify.json \
  --output _work/CITATION_AUDIT.json \
  --md _work/CITATION_AUDIT.md

# 2. 编码检查（survey 与 related-work 二选一或都跑）
python shared/scripts/check_encoding.py survey.md
python shared/scripts/check_encoding.py related-work.md
python shared/scripts/check_encoding.py _work/selection-protocol.md
```

## 失败与回流

| 失败 | 处理 |
|------|------|
| 库为空或 `reading_notes` 不足 | 回流 `literature-reader`；或写短稿并显式声明「语料局限」，不冒充标准档 |
| 缺全文、仅摘要 | 降级表述；提示用户补 PDF 或扩大 OA 检索（`literature-search-download`） |
| Related Work 无贡献说明 | 写 `_work/WAITING_contribution.md` 并停止 |
| 引用核验失败 | 改稿或改库字段；不得静默删引用 |
| 用户要投稿 PDF/LaTeX | 说明本技能止于 Markdown；排版交给用户或后续工具链 |
| 编年体 / 逐篇摘要倾向 | 回到大纲，按主题重写 |

## 参考（链接 references/）

- `references/style-packs.md` — 四写法包对照与选型
- `references/venue-writing-norms.md` — 理工科多学科书写规范摘要
- `references/quality-gate.md` — 成稿自检清单
- `references/survey-template.md` — 分类框架综述（默认）
- `references/narrative-review-template.md` — 叙事权威综述
- `references/systematic-mapping-template.md` — 系统梳理正文
- `references/selection-protocol-template.md` — 选文过程（系统梳理专用）
- `references/related-work-template.md` — Related Work
- 上游：`literature-landscape-writer` / `literature-reader` / `literature-search-download`
- 下游：`citation-verifier`（成稿必跑）；可视化仍读 `references.json`，不依赖 survey 正文
- 样例：`examples/f2-survey-extension/`
