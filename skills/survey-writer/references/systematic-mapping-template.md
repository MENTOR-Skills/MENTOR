# systematic-mapping 模板（系统梳理 / 映射正文）

对标 PRISMA-lite、IEEE Access Topical Review、SEGRESS 映射思路：**范围可追溯 + 映射/矩阵 + 综合**。  
**必填过程文件：** `_work/selection-protocol.md`（模板见 `selection-protocol-template.md`）。  
详见 `venue-writing-norms.md` §4。

```markdown
# <题目>

## 摘要
150–300 字：研究问题、范围、映射/main finding、局限（含检索/库覆盖）。

## 关键词
3–6 个。

## 1. 引言
- 动机与 review 问题（可写成 PICO/PEO 式一句，视学科习惯）
- 与 ad hoc 综述的区别：本文强调**可追溯选文**（细节见 selection protocol）
- 结构导航

## 2. 范围与方法（正文摘要版）
- 文献来源与时间窗（与 `scope.md` 一致）
- 纳入 / 排除标准（要点列表）
- 筛选流程一句话 + 「完整漏斗/映射表见 `_work/selection-protocol.md`」
- **不得伪造** PRISMA 各阶段计数；未执行的步骤不要写

## 3. 映射维度与编码说明
说明映射表列（如：方法族、数据模态、证据类型、是否开源等）。
维度须能对应到 `reading_notes` 或库字段。

## 4. 映射结果概览
表格或矩阵：行=库内文献（或聚类），列=映射维度。
附 1–2 段文字解读模式（非逐篇摘要）。

## 5. 主题综合（按映射维度展开）
≥ 3 个小节，按维度或聚类综合叙述。
仍禁止编年流水账。

## 6. 讨论
- 模式、缺口、矛盾结果
- 与 protocol 范围外的文献类型说明
- Threats to validity / 局限（检索库、语言偏倚、摘要级阅读等）

## 7. 结论与建议
面向读者或实践的可操作总结。

## 参考文献
仅 `references.json`；预印本标 `(preprint)`。
```

### 过程文件（必填）

| 文件 | 内容 |
|------|------|
| `_work/selection-protocol.md` | 检索库、检索式、纳入排除、筛选阶段、映射表原始说明 |

正文与 protocol **范围须一致**；修改范围时同步改 protocol。

### 篇幅与语料

- 中文 survey 正文约 **2500+ 字**（protocol 另计）。
- 建议 ≥ **8** 篇有 `reading_notes`；映射表可一行一篇。

### 何时不要选本包

- 实际未做结构化检索与筛选 → 改选「分类框架」或在引言声明「非系统综述」。
