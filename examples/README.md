# examples/ — 只读样例索引

每个子目录是一个**可对照的案例说明**（不是跑场）。  
真正执行请写入 `tests/runs/<用例名>/`（见 `tests/README.md`）。

## 每个 example 的 README 必须包含

| 小节 | 内容 |
|------|------|
| **案例是什么** | 测什么、适用谁 |
| **涉及哪些 skills** | 技能目录名列表 |
| **交付物是什么** | 预期文件路径 |
| **如何复现** | 命令或 Cursor 话术 |

大体积 PDF 默认忽略；勿提交付费全文。

## 目录一览

| 目录 | 一句话 |
|------|--------|
| [`sample-topic/`](./sample-topic/) | F2 字段联调夹具：三篇经典文 + 全景 + 精读清单 + 关系图 |
| [`f2-script-smoke/`](./f2-script-smoke/) | 纯脚本冒烟说明（产物生成在 `tests/runs/f2-script-smoke/`） |
| [`f2-survey-extension/`](./f2-survey-extension/) | 长篇 `survey.md` 扩展样例（基于同一文献库） |
| [`f4-sample-run/`](./f4-sample-run/) | F4 阶段总结夹具：假项目 + `expected/` 四份交付样例 |
