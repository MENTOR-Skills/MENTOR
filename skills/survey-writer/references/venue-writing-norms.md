# 期刊 / venue 书写规范摘要（理工科多学科）

> 本文件是**给 Agent 的压缩规范**，不是官方模板全文。正式投稿以目标 venue 当年作者指南为准。  
> 与 `style-packs.md` 配合：先选写法包，再按本节微调语气与章节名。

## 0. 四写法包与 venue 的对应（速查）

| 写法包 | 常见对标 venue / 文体 | MENTOR 默认交付 |
|--------|----------------------|-----------------|
| 叙事权威综述 | Nature Reviews 系列、*Annual Review of …*、ACS *Chemical Reviews* | `survey.md` |
| 分类框架综述 | ACM Computing Surveys (CSUR)、多数 CS·EE arXiv/IEEE survey | `survey.md`（**默认**） |
| 系统梳理/映射 | PRISMA 系习惯、IEEE Access Topical Review、SEGRESS 映射思路 | `survey.md` + `_work/selection-protocol.md` |
| Related Work | IEEE/ACM 研究论文相关工作节 | `related-work.md` |

---

## 1. 共通写作原则（四包共享）

1. **主题综合**，不是按发表年份的论文清单；也不是「A 说…B 说…」逐篇摘要。
2. **只引用已入库文献**；数值与对比结论须来自 `reading_notes` 或用户本地证据，否则标缺口。
3. **预印本**标 `(preprint)`；**推断**标「推断」；核验交给 `citation-verifier`，正文不自夸「已全部核验」。
4. **检索/纳入细节**默认不进正文一级结构；系统梳理模式例外——过程写 `_work/selection-protocol.md`，正文可摘要。
5. 中文独立综述约 **2500+ 字**；Related Work 更短；默认 Markdown，不出相机 PDF/LaTeX。

---

## 2. 叙事权威综述（Nature Reviews / Annual Reviews / Chemical Reviews）

**结构重心：** 用「问题—机制—证据—未解问题」的**叙事链**组织，taxonomy 可隐含在段落里，不必大段编号分类表。

| 元素 | 常见习惯 |
|------|----------|
| 开篇 | 领域重要性 + 读者为何现在需要这篇 review |
| 主体 | 按科学问题或机制线索展开；代表工作作证据节点，非按年份罗列 |
| 图表 | 机制示意图、时间线（慎用编年体正文）、对比表 |
| 语气 | 权威、综合、面向跨子领域读者；化学/生命科学常强调反应/通路/尺度 |
| 局限 | 明确覆盖边界与争议点 |

**对本技能：** 用 `narrative-review-template.md`；仍禁止库外引用；不必模仿 Nature 的正式 figure 编号。

**参考入口（公开作者页，非全文模板）：**

- [Nature Reviews author guidelines](https://www.nature.com/nature-reviews/for-authors)
- [Annual Reviews contributor information](https://www.annualreviews.org/page/authors/generalinformation)
- [ACS Chemical Reviews author guidelines](https://pubs.acs.org/page/4authors/submission/cc_review.html)

---

## 3. 分类框架综述（ACM CSUR / CS·EE survey，默认包）

**结构重心：** 显式 **taxonomy**（分类维度）+ 按主题分节 + 比较表 + open problems。

常见结构：

1. Abstract / 摘要  
2. Introduction（动机、范围、本文组织哪些主题）  
3. **Background / Preliminaries**（可选，术语与问题形式化）  
4. **Taxonomy 或 Thematic sections**（≥ 3 主题节）  
5. Comparison / Discussion（常含对比表）  
6. Open problems / Future directions  
7. Conclusion  
8. References  

**写作原则：**

- 比较表注明指标与设定是否可比；不可比则写明。
- CCS Keywords 等正式稿元素：用户指定 ACM 投稿时再补占位节。

**参考入口：**

- [ACM Computing Surveys](https://dl.acm.org/journal/csur)
- [ACM Primary Article Templates](https://www.acm.org/publications/proceedings-template)

**对本技能：** 用 `survey-template.md`；IEEE 数字序 `[1]` 与作者—年份二选一，全文统一。

---

## 4. 系统梳理 / 映射（PRISMA-lite / IEEE Access Topical / SEGRESS）

**结构重心：** 范围与方法**可追溯** + 映射表或主题矩阵 + 综合讨论。  
正文可摘要选文过程；**完整纳入/排除、检索来源、漏斗或映射表**写 `_work/selection-protocol.md`（见 `selection-protocol-template.md`）。

| 元素 | 常见习惯 |
|------|----------|
| PRISMA 系 | 检索库、检索式、纳入排除标准、筛选阶段计数（**不得伪造数字**） |
| IEEE Access Topical Review | 明确 topical scope + 结构化小节 + 面向实践者的总结 |
| SEGRESS 思路 | 软件工程等领域强调 evidence type、quality 与 mapping 维度 |

**对本技能：**

- 用 `systematic-mapping-template.md` + 必填 `selection-protocol.md`
- 若实际未做系统检索，不得冒充 PRISMA；应改选「分类框架」或声明「非系统综述」

**参考入口：**

- [PRISMA statement](https://www.prisma-statement.org/)
- [IEEE Access author guidelines](https://ieeeaccess.ieee.org/guide-for-authors/)

---

## 5. Related Work（IEEE / ACM 论文）

**结构重心：** 按**主题**分小节；每节：该线工作 → 局限 → **与本稿差异**；结尾 **positioning**。

| 项 | 常见约定 |
|----|----------|
| 位置 | Introduction 后或 Method 前（视 venue） |
| 组织 | 主题分节，非编年流水账 |
| 篇幅 | 短于独立 survey；seminal + 近期 + 最近邻 |
| 引用 | IEEE 常 `[1]` 数字序；ACM 视模板 |

**对本技能：** 用 `related-work-template.md`；**必须**有用户提供的「本文贡献」才能写 positioning。

**参考入口：**

- [IEEE Author Center](https://journals.ieeeauthorcenter.ieee.org/)

---

## 6. 写法包差异 vs 共通点（小结）

|  | 共通 | 叙事权威 | 分类框架 | 系统梳理 | Related Work |
|--|------|----------|----------|----------|--------------|
| 只引 `references.json` | ✓ | ✓ | ✓ | ✓ | ✓ |
| 主题综合 | ✓ | ✓（叙事链） | ✓（taxonomy） | ✓（映射+综合） | ✓ |
| 过程文件 protocol | — | 可选 outline | 可选 outline | **必填** | 建议 contribution |
| 检索协议进正文 | 默认否 | 否 | 否 | 摘要可，细节 protocol | 否 |
| 主交付 | — | `survey.md` | `survey.md` | `survey.md` | `related-work.md` |

---

## 7. 开源 GitHub 技能：借鉴与不采用

| 来源 | 借鉴 | **不采用** |
|------|------|------------|
| [wentorai/research-plugins](https://github.com/wentorai/research-plugins) research-paper-writer | IEEE/ACM 章节骨架、Related Work 按主题 | 不生成完整 Method/Experiments 论文壳 |
| [AI4Scientist/nano-scientist](https://github.com/AI4Scientist/nano-scientist) research-survey | 大纲→分节扩展、taxonomy 优先于编年 | 不引入重型多阶段 pipeline |
| [ShaishavMaisuria/… draft-survey](https://github.com/ShaishavMaisuria/research-paper-lifecycle-skills) | 主题综合 + 强制引用可核验 | 不默认两栏 LaTeX |
| 各类 PRISMA bot / systematic review 模板 | selection protocol 字段清单 | 不伪造漏斗计数；不做未执行检索的「假系统综述」 |
| MENTOR `survey-writer` | 四写法包合一技能、质量门 + citation-verifier | 不出投稿 PDF；不搬入 `literature-survey-orchestrator` |

---

## 8. 与 MENTOR 诚信规则的交叠

- 凡数值、对比结论，必须来自 `reading_notes` 或用户提供的本地结果；否则标缺口。
- 引用存在性交给 `citation-verifier`；正文不自我背书「已全部核验」。
- 成稿前跑 `references/quality-gate.md` 自检清单。
