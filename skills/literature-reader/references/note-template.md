# references.json 单篇字段说明（F2/F3 共用）

## 必填（协议 §6）

| 字段 | 说明 |
|------|------|
| `id` | 稳定编号（优先 arXiv / 开放库 id） |
| `title` | 标题 |
| `authors` | 字符串数组 |
| `year` | 发表年；未知写 `null` |
| `venue` | 期刊/会议/预印本平台；未知写 `""` |
| `access_status` | `fulltext` / `abstract_only` / `waiting_user_pdf` / `unknown` |

入库或深读后必填 `reading_notes`：

| 子字段 | 说明 |
|--------|------|
| `problem` | 研究问题（短句） |
| `method` | 方法（短句） |
| `results` | 主要结果或结论（短句） |
| `limitations` | 局限（短句） |

## 建议

- `url` / `doi` / `arxiv_id` / `pdf_path` / `abstract`

## 可选扩展

- `data_metrics`、`quotable_claims`、`source_spans`（证据位置：Abstract / §x / Table y）
- `peer_reviewed`、`topics`、`status`（to_read / reading / read）
- `relations[]`：`{ "target_id", "kind", "basis": "fact"|"inferred" }`

## 不要做

- 不要把 `cite_key` 当作入库失败原因（需要时由程序生成）
- 不要为 F2 强制创建逐篇 `notes/*.md`（F3 用人读报告 `reading-reports/<id>.md`）
