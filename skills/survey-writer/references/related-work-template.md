# Related Work 模板（论文章节 · 写法包四）

按**主题**组织（IEEE/ACM Related Work 常见做法），不要按发表年份流水账。  
**必须**有用户提供的「本文贡献 / 定位」才能写 positioning。详见 `venue-writing-norms.md` §5。

```markdown
## Related Work

> 用户贡献摘要（写作依据，可来自 `scope.md` 或 `_work/contribution.md`）：  
> 「本文 …（方法/问题/数据/结论）…」

### <Theme 1：问题线或方法线 A>
概括该线如何定义问题与主流做法，引用 2–4 篇库内代表作（含近期/经典）。
**局限：** …  
**与本稿差异：** …

### <Theme 2：…>
…

### <Theme 3（可选）：最近邻工作>
紧贴本稿设定的工作；差异要具体（数据、指标、假设、训练方式等）。

### Positioning
一段话说明本稿落在哪条线、补哪个缺口；避免「我们也做了 X」清单。
须与用户贡献一致；无贡献说明则不要写本节，停下问用户。
```

### 注意

- Related Work ≠ 完整 Survey；控制在 seminal + 近期代表 + 最近邻。
- 只引用 `references.json` 内条目；预印本标 `(preprint)`。
- 交付文件名：`related-work.md`（工作区根）。
- 建议 ≥ **5** 篇有 `reading_notes` + 用户贡献；演示夹具可更少但须标注演示级。

### 篇幅

- 明显短于独立 `survey.md`（无需 2500 字门槛，但仍须主题综合、非流水账）。
