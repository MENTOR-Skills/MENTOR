# sample-topic

## 案例是什么

F2 **字段与交付形态联调夹具**：用 3 篇广为人知的 OA/arXiv 文献，演示协议 §6 的 `references.json`（含 `fact` / `inferred` 关系、`fulltext` / `abstract_only`），以及全景、精读清单、关系图。  
**不是**对某一新课题的真实端到端调研结果。

## 涉及哪些 skills

| 技能 | 本例角色 |
|------|----------|
| `literature-reader` | 字段形态参考（笔记已写入 JSON） |
| `literature-landscape-writer` | 样例 `literature-landscape.md` / `reading-shortlist.md` |
| `survey-visualizer` | 生成 / 重建 `viz/index.html` |
| `citation-verifier` | 可对 `references.json` 做存在性核验 |
| （未跑）`literature-search-download` | 真实检索请另开 `tests/runs/` 盲测 |
| （未跑）`survey-writer` | 见 `examples/f2-survey-extension/`（`survey.md` + `related-work.md`） |

## 交付物是什么

| 路径 | 说明 |
|------|------|
| `references.json` | 3 篇；2 条 relations |
| `literature-landscape.md` | 全景说明样例 |
| `reading-shortlist.md` | 精读清单样例 |
| `viz/index.html` | 关系图（可重建） |

## 如何复现

在 `MENTOR/` 根目录：

```powershell
python skills/survey-visualizer/scripts/build_viz.py `
  --references examples/sample-topic/references.json `
  --out examples/sample-topic/viz/index.html `
  --title "Sample Literature Landscape"
```

引用核验（产物建议写到 `tests/runs/`，勿污染本目录）：

```powershell
New-Item -ItemType Directory -Force -Path tests/runs/sample-verify/_work
python skills/citation-verifier/scripts/refs_to_verify_input.py `
  --references examples/sample-topic/references.json `
  --out tests/runs/sample-verify/_work/candidates_for_verify.json
python skills/citation-verifier/scripts/verify_citations.py `
  --input tests/runs/sample-verify/_work/candidates_for_verify.json `
  --output tests/runs/sample-verify/_work/CITATION_AUDIT.json `
  --md tests/runs/sample-verify/_work/CITATION_AUDIT.md
```

### Cursor 演示话术

> 打开 `examples/sample-topic/references.json`，按 F2 检查字段是否符合协议，并说明关系图里哪条是推断。
