---
name: academic-honesty
description: >-
  Enforces the global academic honesty checklist before any F1–F5 skill
  produces a deliverable. Checks fabrication, paywall bypass, unauthorized
  scanning, evidence claims, and UTF-8 encoding. Invoked as a mandatory gate
  by every output-producing skill; not called directly by end users. Use when
  a skill is about to finalize a report, draft, or structured data file.
  Trigger words: honesty, integrity, checklist, 诚信, 核查.
---

# 学术诚信（academic-honesty）

横切规程技能：在 F1–F5 任意技能成稿前强制加载并逐条核对诚信清单；产出 CLEAR 或 BLOCKED 信号。

遵守 `shared/honesty-checklist.md`。本技能本身**不生成科研正文**，只做检查与停车。

## 何时使用 / 何时不使用

**使用：**
- 任何 F1–F5 产出型技能在写入终稿前（由调用方在步骤中显式加载）
- 用户明确要求核查已有交付的学术诚信

**不使用：**
- 作为独立技能被用户直接调用（它是内部门控，由其他技能触发）
- 检查纯过程文件（`_work/state.yaml`、`research-log.md` 等无主张内容的文件）
- 代替各技能自身步骤中的确认关卡（诚信检查是**成稿前最后一道**，不代替中间确认）

## 前置条件（依赖哪些技能、哪些文件须已存在）

- `shared/honesty-checklist.md` 存在于仓库中（本技能加载并逐条执行）
- 调用方技能已准备好待交付内容（草稿已完成，主张—证据表已填写）
- 无上游技能依赖（基础规程）

## 硬规则（禁止项）

1. **不得**静默通过——每条勾选结果必须可追溯（写入 `research-log.md` 或嵌入交付文件）
2. **不得**修改终稿文件——本技能只检查并给出 CLEAR/BLOCKED，改稿由调用方技能负责
3. **不得**跳过 A–E 任一类别——即使某类不适用，也必须显式标注 N/A 及原因
4. **不得**复制 `shared/honesty-checklist.md` 内容——本技能只引用并执行，不重复写入
5. 中文 UTF-8；若本技能写入任何过程文件，交付前跑 `shared/scripts/check_encoding.py`

## 步骤（有序，可勾选）

1. [ ] 加载 `shared/honesty-checklist.md`；确认调用方技能身份（F1–F5 中哪一项）
2. [ ] 识别待交付文件列表与类型（报告 / 结构化数据 / 术语表 / 写作稿等）
3. [ ] 逐类核对（按 `shared/honesty-checklist.md` 五类顺序）：
   - **A 文献与引用** — 每一条引用是否真实存在、DOI/标题/作者匹配；推断关系是否已标注
   - **B 实验与数据** — 数值是否有日志/CSV 可核验；是否因「有代码」错误断定「实验成功」
   - **C 下载与获取** — 是否绕过付费墙；是否假装已获取全文
   - **D 隐私与授权** — 是否扫描了未授权路径；交付中是否含密钥/`.env`
   - **E 明确声明** — 不确定处是否已标注「待验证」「推断」或「未核实」
4. [ ] 对每条「否」按 `references/violation-protocol.md` 处理：删主张 / 标缺口 / 停车等用户
5. [ ] 汇总结果：全部通过或缺口已显式声明 → **CLEAR**；仍有未解决违规 → **BLOCKED**
6. [ ] 将勾选结果写入 `research-log.md`（至少记录：时间、调用方技能、交付文件列表、各类通过/失败/N/A、CLEAR/BLOCKED）
7. [ ] 若 BLOCKED → 写 `_work/WAITING_honesty_<简述>.md`，更新 `_work/state.yaml`（`waiting_for: honesty_blocked`）
8. [ ] 若 CLEAR → 信号返回调用方技能，调用方继续成稿

## 必须问人的点（停下条件与如何继续）

| 停下 | 问什么 | 继续条件 |
|------|--------|----------|
| 发现疑似伪造引用 | 该引用无法核实。删除该主张、标为「未核实」，还是你提供核实方式？ | 用户选择处理方式 |
| 检测到付费墙绕过 | 该论文为付费内容，当前未获取全文。请将 PDF 放入 `pdfs/user/` 或接受 `abstract_only` 标注 | 用户补 PDF 或接受降级 |
| 未授权路径被读取 | 路径 X 不在 `scope.md` 授权扫描范围内。是否将该路径加入授权？ | 用户确认加入或拒绝 |
| 关键主张无证据且用户拒标缺口 | 该主张无法保留。删除后继续成稿，还是你提供证据？ | 用户提供证据或同意删除 |
| 编码校验失败 | 文件编码非 UTF-8。删除坏文件并用 UTF-8 重新生成？ | 用户确认（禁止 cp1252「修复」） |

停车时写入 `_work/WAITING_honesty_<简述>.md`，更新 `_work/state.yaml`。

## 交付契约（输入 / 输出路径与字段）

**输入：** 调用方技能的待交付内容 + 主张—证据表（如有）+ 上游材料路径。

**输出（无独立终稿文件）：**

| 产出 | 路径 | 说明 |
|------|------|------|
| 勾选结果 | `research-log.md`（追加） | 时间、调用方、文件列表、各类结果、CLEAR/BLOCKED |
| 阻塞说明 | `_work/WAITING_honesty_*.md` | 仅当 BLOCKED 时写入 |

**信号：** 返回 CLEAR（可成稿）或 BLOCKED（停车等待）给调用方技能。

## 脚本调用（若有，给命令模板）

本技能以 Agent 逐条核对为主；无专用脚本。

```bash
# 若写入过程文件，交付前跑编码检查
python shared/scripts/check_encoding.py _work/WAITING_honesty_*.md
```

## 失败与回流

| 失败 | 处理 |
|------|------|
| 核实引用时无网络（无法查 DOI） | 标为「未核实」并在交付中声明；不静默通过 |
| 调用方技能拒绝配合修改 | 不 CLEAR；保留 WAITING 文件；不进入下游技能 |
| 诚信清单文件缺失 | 停止所有产出型技能；报告「`shared/honesty-checklist.md` not found」 |
| 用户要求跳过诚信检查 | **拒绝**——诚信清单不可跳过；若用户坚持，结束当前任务并记录 |
| 编码校验失败 | 删除坏文件并重新 UTF-8 生成，禁止 replace/cp1252「修复」 |

## 参考（链接 references/）

- `references/violation-protocol.md` — 违规处理协议
- `references/pre-delivery-checklist.md` — 按功能细化的补充检查项
- `shared/honesty-checklist.md` — 权威诚信清单（五类 A–E）
- `shared/encoding-utf8.md` — 编码规范
- 被引用方：F1–F5 全部产出型技能（在各自「硬规则」和成稿前步骤中加载本技能）
