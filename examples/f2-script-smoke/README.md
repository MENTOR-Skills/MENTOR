# f2-script-smoke

## 案例是什么

**纯脚本冒烟**：验证检索脚本、付费墙等待文件、可视化、引用核验能否在本机跑通。  
不生成 Agent 撰写的全景正文（那部分见 `sample-topic` 或盲测）。

## 涉及哪些 skills

| 技能 | 脚本 |
|------|------|
| `literature-search-download` | `search_arxiv.py`、`write_wait_gate.py` |
| `survey-visualizer` | `build_viz.py` |
| `citation-verifier` | `refs_to_verify_input.py`、`verify_citations.py` |
| （编码）`shared/scripts/check_encoding.py` | 交付编码检查 |

文献库内容复用 `examples/sample-topic/references.json`（保证核验稳定）。

## 交付物是什么

运行后出现在 **`tests/runs/f2-script-smoke/`**（不在本目录）：

| 路径 | 说明 |
|------|------|
| `scope.md` | 冒烟用范围说明 |
| `_work/arxiv.jsonl` | arXiv 检索结果 |
| `_work/shortlist.json` | 短名单 |
| `_work/WAITING_user_pdf.md` | 付费墙/待补 PDF 门控文件 |
| `references.json` | 自 sample-topic 复制 |
| `viz/index.html` | 关系图 |
| `_work/CITATION_AUDIT.md` | 引用核验报告 |

## 如何复现

```powershell
cd MENTOR
python tests/scripts/run_f2_script_smoke.py
```

成功时终端打印 `OK smoke → .../tests/runs/f2-script-smoke`。  
需要外网访问 arXiv 与 CrossRef。
