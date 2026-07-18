# 写法包对照表（survey-writer）

> 四个写法包共用同一技能 `survey-writer`；差别在结构重心、过程文件与对标习惯。  
> 正式投稿仍以目标 venue 当年作者指南为准。

## 快速选型

| 用户怎么说 | 推荐写法包 | 主交付 |
|------------|------------|--------|
| 「像 Nature Reviews / Annual Reviews 那样讲清楚脉络」 | 叙事权威综述 | `survey.md` |
| 「按 taxonomy / 分类写 CS survey」（默认） | 分类框架综述 | `survey.md` |
| 「系统梳理 / PRISMA / 映射表 / 选文过程要可追溯」 | 系统梳理/映射 | `survey.md` + `_work/selection-protocol.md` |
| 「论文 Related Work / 相关工作章节」 | Related Work | `related-work.md` |

## 四写法包对照

| 维度 | 叙事权威 | 分类框架（默认） | 系统梳理/映射 | Related Work |
|------|----------|------------------|---------------|--------------|
| 对标 | Nature Reviews、Annual Reviews、ACS *Chemical Reviews* | ACM CSUR、IEEE/ACM CS·EE survey | PRISMA-lite、IEEE Access Topical Review、SEGRESS | 会议/期刊论文章节 |
| 结构重心 | 问题—机制—证据链叙事；少显式 taxonomy 标题 | 显式分类体系 + 主题节 + 比较表 | 范围 + 映射/对比 + 过程可追溯 | 主题小节 + positioning |
| 过程文件 | 可选 `_work/survey-outline.md` | 可选 outline | **必填** `_work/selection-protocol.md` | 建议 `_work/contribution.md` |
| 建议篇数 | ≥ 8 有 `reading_notes` | ≥ 8 | ≥ 8（映射表行可少于篇数） | ≥ 5 + 用户贡献 |
| 默认篇幅 | 中文 2500+ 字 | 中文 2500+ 字 | 中文 2500+ 字（过程另文件） | 更短 |
| 检索协议进正文 | 否（放 `_work/`） | 否 | 摘要进正文；细节在 protocol | 否 |
| 模板 | `narrative-review-template.md` | `survey-template.md` | `systematic-mapping-template.md` | `related-work-template.md` |

## 共通点（四包都遵守）

- 只引用 `references.json`；主题综合，非编年流水账
- 预印本标 `(preprint)`；推断标「推断」
- 成稿跑 `citation-verifier` + `check_encoding.py`
- 语料不足：声明局限或回流检索/精读，不编造引用

## 与 venue-writing-norms 的关系

- **venue-writing-norms.md** 解释各学科「为什么这样写」
- **本表** 解释 Agent「选哪种包、交哪些文件」
- 用户指定 venue 时：先选写法包，再按 norms 微调语气与章节名
