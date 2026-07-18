---
name: adversarial-lite
description: >-
  Optional F5 internal review that stress-tests a draft with mentor-style
  questions and weakness notes. Writes only _work/adversarial-notes.md; never
  edits the final deliverable. Use when the user asks for rehearsal of advisor
  pushback or adversarial review. Not enabled by default in standard effort.
  Never invent counter-evidence papers or fake metrics.
---

# 挑刺审阅（adversarial-lite）

F5 **可选**内部技能：对已有成稿做导师向追问与薄弱点标注。

**只输出** `_work/adversarial-notes.md`（或等价过程文件）；**不改**终稿（`meeting-one-pager.md` 等）。

**标准档默认不启用。** 仅当用户明确说「预演导师追问」「挑刺」「adversarial」等时调用。

遵守 `shared/honesty-checklist.md`。

## 何时使用 / 何时不使用

**使用：** 用户已有 F5 成稿（或等价草稿），并明确要求预演追问 / 找茬。

**不使用：**

- 标准档默认流程（不要主动插入）；
- 代替 `academic-writing` 写一页纸；
- 用户要求「帮我改掉所有漏洞」且期望本技能直接改终稿 → 意见写在 notes，改稿仍走 `academic-writing`；
- 无成稿可读。

## 前置条件

| 依赖 | 说明 |
|------|------|
| 成稿 | 至少一份 F5 交付或用户指定 ASCII 路径草稿 |
| 主张表（强烈建议） | `_work/claims-evidence.md` |
| 上游材料 | F4 四文件和/或 `references.json`（用于核对，不用于编造反证） |

## 硬规则（禁止项）

1. **不得修改**终稿文件；只写 `_work/adversarial-notes.md`。
2. **不得捏造**反证文献、DOI、实验数字或「某篇论文已推翻」。
3. 质疑须指向：证据缺口、过度声称、逻辑跳步、与 F4/文献库不一致——有依据才写。
4. 可建议「若导师问 X，诚实回答是…」；不可编造更漂亮的答词数字。
5. 中文 UTF-8；交付前对 notes 跑编码检查。

## 步骤（有序，可勾选）

1. [ ] 确认用户明确要求挑刺；标准档未要求则跳过本技能。
2. [ ] 读成稿 + `_work/claims-evidence.md` + 相关 F4/文献材料。
3. [ ] 按 `references/adversarial-notes-template.md` 写出追问、薄弱点、建议降级措辞。
4. [ ] 自检：每条意见可回溯材料或「逻辑/清晰度」类问题；无伪造文献。
5. [ ] `check_encoding.py`；更新 `research-log.md`（注明未改终稿）。

## 必须问人的点（停下条件与如何继续）

| 停下 | 问什么 | 继续条件 |
|------|--------|----------|
| 未明确要求挑刺 | 是否启用本技能？（默认否） | 用户说「要」 |
| 无成稿 | 先跑哪个文体包？ | 用户完成 `academic-writing` |
| 意见是否并入终稿 | 是否回流 `academic-writing` 按 notes 改稿？ | 用户选择 |

## 交付契约（输入 / 输出）

**输入：** 成稿路径 + 建议的主张—证据表。

**输出（仅过程文件）：**

| 文件 | 说明 |
|------|------|
| `_work/adversarial-notes.md` | 挑刺意见；非完成标准中的「终稿」 |

## 脚本调用

```bash
python shared/scripts/check_encoding.py _work/adversarial-notes.md
```

## 失败与回流

| 失败 | 处理 |
|------|------|
| 想「发明」反证论文 | 停止该条；改为「材料未覆盖，属证据缺口」 |
| 用户要直接改终稿 | 说明本技能只出 notes；改稿用 `academic-writing` |
| 成稿与主张表严重冲突 | 在 notes 列出冲突，建议回流写作技能 |

## 参考（链接 references/）

- `references/adversarial-notes-template.md`
- 上游：`academic-writing` 成稿
- 诚信：`shared/honesty-checklist.md`
