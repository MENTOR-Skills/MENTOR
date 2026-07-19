---
name: literature-reader
description: >-
  Two-pass screening and structured reading notes stored inside references.json
  (no per-paper markdown notes for F2). Use after the user PDF gate clears and
  shortlist exists; also reused by F3 to write back the same literature library.
---

# 文献精读入库（literature-reader）

F2+F3 执行技能：把已读论文写入结构化文献库 `references.json`。

遵守 `shared/honesty-checklist.md`。F2 入库用结构化字段；F3 另产 `reading-reports/<id>.md` 并回写同一库。

## 何时使用 / 何时不使用

**使用：** shortlist 与 PDF 门控已完成，需要精读入库；或 F3 深读后必须回写文献库。

**不使用：** 尚未检索/未确认 shortlist；仅写全景文稿（用 `literature-landscape-writer`）；仅画关系图（用 `survey-visualizer`）。

## 前置条件（依赖哪些技能、哪些文件须已存在）

- `_work/shortlist.json` 已存在（通常由 `literature-search-download` 产出）。
- 用户 PDF 门控已完成：该补的 PDF 已放入 `pdfs/user/` 并登记，或用户明确同意对缺失全文仅用摘要（`access_status: abstract_only`）。
- 工作区：`campus-research-output/<课题简称>/`。

## 硬规则（禁止项）

1. 精读笔记写入交付物 **`references.json`**，**不要**为 F2 强制写逐篇 `notes/*.md`。
2. 未读全文 → `access_status: abstract_only`，不得详述方法细节与实验数字。
3. **禁止**用训练记忆冒充该文内容；数字与结论须能指出证据位置（可选 `source_spans`）。
4. **禁止**伪造 `access_status` / `pdf_path` / 已读状态。
5. `cite_key` **不是**入库必填（需要导出时由程序生成）。
6. `access_status` 仅用：`fulltext` / `abstract_only` / `waiting_user_pdf` / `unknown`。

## 步骤（有序，可勾选）

1. [ ] **Pass A（若尚未做）**：在 `_work/papers_all.jsonl` 上筛选并写入 `_work/shortlist.json`；优先用户 preferred venues / `peer_reviewed`。
2. [ ] **Pass B**：对 shortlist 每篇阅读后写入工作区根目录 `references.json`。
3. [ ] 必填字段对齐协议 §6：`id`, `title`, `authors`, `year`, `venue`, `access_status`；入库后填 `reading_notes`（至少四字段）。
4. [ ] 可选：从明确引用/文本得到关系时写入 `relations`（`basis: fact`）；不确定则留给 `literature-landscape-writer` 标注推断。
5. [ ] UTF-8 写入（`ensure_ascii=False`）；用 `shared/scripts/check_encoding.py` 校验。
6. [ ] 更新 `_work/state.yaml`：`current_skill: literature-reader`，清除已完成的 `waiting_for`（若适用）。

## 必须问人的点（停下条件与如何继续）

| 停下 | 问什么 | 继续条件 |
|------|--------|----------|
| 仍有 `waiting_user_pdf` | 补 PDF 还是允许摘要级精读？ | 登记 PDF 或用户书面同意 `abstract_only` |
| 标准档精读前 | shortlist 是否定稿？ | 用户确认 |

## 交付契约（输入 / 输出路径与字段）

**输入：** `_work/shortlist.json`；`pdfs/auto/` 与/或 `pdfs/user/`。

**输出：** `references.json`（工作区根），形态：

```json
{
  "meta": {
    "topic": "",
    "created": "",
    "search": { "note": "optional; not for landscape body" },
    "audit": null
  },
  "papers": [
    {
      "id": "",
      "title": "",
      "authors": [],
      "year": 2024,
      "venue": "",
      "url": "",
      "doi": null,
      "arxiv_id": null,
      "pdf_path": null,
      "access_status": "fulltext",
      "abstract": "",
      "peer_reviewed": true,
      "reading_notes": {
        "problem": "",
        "method": "",
        "results": "",
        "limitations": "",
        "data_metrics": "",
        "quotable_claims": [],
        "source_spans": ["Abstract", "§3"]
      },
      "relations": [
        { "target_id": "", "kind": "方法继承", "basis": "fact" }
      ]
    }
  ]
}
```

- `reading_notes` 最小必填：`problem` / `method` / `results` / `limitations`。
- `relations` 可选；`basis` 为 `inferred` 的不得写成事实。
- `cite_key` 不入库必填。

## 脚本调用（若有，给命令模板）

F3 单篇写回先把该论文条目写成临时 JSON，再安全合并到同一文献库；脚本保留已有扩展字段并拒绝标识冲突：

```bash
python skills/literature-reader/scripts/upsert_reference.py references.json _work/f3-paper.json
python shared/scripts/check_encoding.py references.json
```

## 失败与回流

| 失败 | 处理 |
|------|------|
| PDF 不可读 | 标 `abstract_only` 或请用户换文件；不得编造全文笔记 |
| 字段缺失 | 补齐必填后再进入 `literature-landscape-writer` |
| 与 F3 报告冲突 | 以最新精读为准回写 `references.json`，并在 `research-log.md` 注明 |

## 参考（链接 references/）

- `references/note-template.md`
- `shared/workspace-layout.md`、`docs/接口与协议.md` §6
- 上游：`literature-search-download`；下游：`literature-landscape-writer` / F3 `paper-deep-read`
