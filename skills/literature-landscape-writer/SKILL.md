---
name: literature-landscape-writer
description: >-
  Writes literature-landscape.md and reading-shortlist.md from references.json
  only. Use after F2 reading notes are stored; produces a landscape overview
  and a 3–5 paper shortlist. For a long survey.md or Related Work draft, use
  survey-writer. Mark inferred relations explicitly.
---

# 文献全景撰写（literature-landscape-writer）

F2 执行技能：基于文献库写出主线、分类、关系说明与精读清单。

**完成标准：** `literature-landscape.md` + `reading-shortlist.md`。  
长篇 `survey.md` / Related Work 由可选扩展技能 `survey-writer` 产出。

遵守 `shared/honesty-checklist.md`。

## 何时使用 / 何时不使用

**使用：** `references.json` 已含精读字段，用户需要专题全景、相关工作梳理、精读建议。

**不使用：** 文献库尚未入库；只要检索候选（停在 `literature-search-download`）；只要单篇深读报告（F3）；用户明确要求长篇综述或 Related Work → 改调 **`survey-writer`**（可先完成本技能再扩展）。

## 前置条件（依赖哪些技能、哪些文件须已存在）

- `references.json` 存在且 `papers` 非空；目标篇目已有 `reading_notes`（至少四字段），或用户明确允许摘要级综合（须在文中声明局限）。
- `scope.md` 已确认主题与时间范围。
- 上游：`literature-reader`（及此前的检索/PDF 门控）。

## 硬规则（禁止项）

1. **只引用** `references.json` 中的条目；不得编造未入库文献。
2. 关系若由模型推断，必须标注「推断」或 `basis: inferred`；不得写成既成事实。
3. 预印本须标明（如 venue 或文中标注 preprint）。
4. 声称须能回溯到对应 `reading_notes` 或摘要级依据；无证据则标缺口。
5. 不要把检索协议、漏斗数字表作为全景正文一级结构。
6. 中文 UTF-8；写完用 `shared/scripts/check_encoding.py` 校验。

## 步骤（有序，可勾选）

1. [ ] 读取 `scope.md` 与 `references.json`；确认可写范围。
2. [ ] 归纳 2–4 条问题主线 / 方法族（综合叙述，非「A 说 B 说」堆砌）。
3. [ ] 写出代表工作与关系；同步可回写 `papers[].relations`（推断标 `inferred`）。
4. [ ] 写出可见缺口（标明「据当前短名单，可能遗漏」）。
5. [ ] 生成 `literature-landscape.md`（结构见模板）。
6. [ ] 生成 `reading-shortlist.md`：3–5 篇，区分已入库精读与建议下一步 F3 深读。
7. [ ] 编码校验；建议接着跑 `citation-verifier`，再跑 `survey-visualizer`。
8. [ ] 若用户还要长篇综述 / Related Work → 调用 `survey-writer`。
9. [ ] 更新 `state.yaml` / `research-log.md`。

## 必须问人的点（停下条件与如何继续）

| 停下 | 问什么 | 继续条件 |
|------|--------|----------|
| 库内精读不足 | 先补精读还是以摘要级出全景并声明局限？ | 用户选择 |
| 关系图边争议大 | 哪些边保留为推断、哪些删除？ | 用户确认后改稿 |

## 交付契约（输入 / 输出路径与字段）

**输入：** `references.json`、`scope.md`

**输出（工作区根）：**

| 文件 | 内容 |
|------|------|
| `literature-landscape.md` | 全景说明（见 `references/landscape-template.md`） |
| `reading-shortlist.md` | 精读清单（见 `references/reading-shortlist-template.md`） |

可选回写：`references.json` 中 `relations` 字段。

## 脚本调用（若有，给命令模板）

本技能以 Agent 撰稿为主；无强制脚本。

```bash
python shared/scripts/check_encoding.py literature-landscape.md
python shared/scripts/check_encoding.py reading-shortlist.md
```

## 失败与回流

| 失败 | 处理 |
|------|------|
| `references.json` 缺失或空 | 回流 `literature-reader`，不得空写 |
| 引用核对失败 | 改 landscape / shortlist 或标未核实后重跑 verifier |
| 编码校验失败 | 删除坏文件并重新 UTF-8 生成，禁止 replace/cp1252「修复」 |

## 参考（链接 references/）

- `references/landscape-template.md`
- `references/reading-shortlist-template.md`
- `references/legacy-survey-template.md`（重定向至 `survey-writer`）
- 下游：`citation-verifier` → `survey-visualizer`；可选 `survey-writer`
