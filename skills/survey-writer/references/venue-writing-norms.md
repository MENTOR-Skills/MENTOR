# 期刊 / 会议书写规范摘要（CS 综述与 Related Work）

> 本文件是**给 Agent 的压缩规范**，不是官方模板全文。正式投稿以目标 venue 当年模板为准。  
> 下列习惯综合自公开作者指南与开源写作技能中的常见约定。

## 1. 独立 Survey / Review（本技能默认）

常见结构（与 ACM Computing Surveys 类、arXiv CS survey 草稿习惯相近）：

1. Abstract / 摘要  
2. Introduction（动机、范围、贡献式「本文组织了哪些主题」）  
3. **按主题/分类体系**展开的若干节（taxonomy / thematic synthesis）  
4. Comparison / Discussion（常含对比表）  
5. Open problems / Future directions  
6. Conclusion  
7. References  

**写作原则：**

- 主题综合，而非编年体论文清单（多家 survey skill 与 IEEE Related Work 指南一致强调 thematic organization）。
- 比较表注明指标与设定是否可比；不可比则写明。
- 方法学细节（检索式、PRISMA 漏斗）放附录或过程文件，除非用户明确要求 systematic review 文体。

## 2. IEEE 习惯（会议/期刊论文，含 Related Work）

参考：[IEEE Author Center](https://journals.ieeeauthorcenter.ieee.org/)

| 项 | 常见约定 |
|----|----------|
| 摘要 | 约 150–250 词；先写最后改 |
| 正文组织 | Introduction → Related Work → Method → Experiments → Conclusion（研究论文）；Survey 则主题节替代 Method/Experiments |
| 引用 | 方括号数字序 `[1]`，文末 References |
| 图表 | 表题在表上方；对比表突出最优结果时需有依据，禁止伪造数值 |

对本技能：Markdown 阶段用 `[1]` 或「作者年份」皆可，**须在文内统一**，并与参考文献列表一致。

## 3. ACM 习惯

参考：[ACM Primary Article Templates](https://www.acm.org/publications/proceedings-template)、[CCS](https://dl.acm.org/ccs)

| 项 | 常见约定 |
|----|----------|
| 摘要后 | CCS Concepts + Keywords（正式稿）；Markdown 草稿可用「关键词」代替 |
| Related Work | 常与 Background 合并或紧随 Introduction；**按主题分小节** |
| 讨论 | 正式研究论文常含 Threats to Validity；独立 survey 可改为「局限与覆盖缺口」 |
| 引用 | 视模板为数字序或 author-year |

对本技能：不强制输出 CCS 编号；用户若指定 ACM 投稿，再补 Keywords/CCS 占位节。

## 4. 开源技能中可借鉴、但未照搬的做法

| 来源 | 借鉴 | 未采用 |
|------|------|--------|
| [wentorai/research-plugins](https://github.com/wentorai/research-plugins) research-paper-writer | IEEE/ACM 章节骨架、Related Work 按主题、摘要四句式 | 不生成完整 Method/Experiments 论文壳 |
| [AI4Scientist/nano-scientist](https://github.com/AI4Scientist/nano-scientist) research-survey | 大纲→分节扩展、taxonomy 优先于编年 | 不引入重型多阶段 pipeline |
| [ShaishavMaisuria/… draft-survey](https://github.com/ShaishavMaisuria/research-paper-lifecycle-skills) | 主题综合 + 强制引用可核验 | 不默认两栏 LaTeX |
| demo `survey-writer` | 禁止开篇堆检索协议；中文 2500+ 字默认 | — |

## 5. 与 MENTOR 诚信规则的交叠

- 凡数值、对比结论，必须来自 `reading_notes` 或用户提供的本地结果；否则标缺口。
- 引用存在性交给 `citation-verifier`；正文不自我背书「已全部核验」。
