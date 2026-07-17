# 用户提供 venue 列表（可选）

本文件**不是**技能内置刊名表。由用户或 scope 填写；每行一个 OpenAlex venue 检索词。

```text
# preferred_venues.txt 示例格式（请换成你自己的领域，勿照抄）
ExampleConfA
ExampleJournalB
```

- 空文件或缺失 → 跳过 Tier-1 venue 过滤
- 次选 venue 可另存为 `secondary_venues.txt`，供 Tier-2 使用
