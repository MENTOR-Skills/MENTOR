# MENTOR 技能一览（SKILLS_CATALOG）

> 给人读的技能看板；智能体冷启动路由请见 `AGENTS.md`。
> 状态口径：**未开始 / 骨架 / 开发中 / 可演示 / 可用**。
> 负责人与分支约定见 `docs/分工说明.md`；交付文件名见 `docs/接口与协议.md` §3。

---

## 技能总表

| # | 技能 | 目录 | 功能 | 类型 | 负责人 | 建议分支 | 状态 |
|---|------|------|------|------|--------|----------|------|
| 1 | 调度模块 | `skills/campus-research-orchestrator/` | 横切 | 用户入口 | 丁 | `feat/crosscut-writing` | 未开始 |
| 2 | 工作区约定 | `skills/research-workspace/` | 横切 | 规程 | 丁 | `feat/crosscut-writing` | 未开始 |
| 3 | 学术诚信 | `skills/academic-honesty/` | 横切 | 规程 | 丁 | `feat/crosscut-writing` | 未开始 |
| 4 | 领域入门 | `skills/domain-onboarding/` | F1 | 工作流 | 甲 | `feat/f1-onboarding` | 未开始 |
| 5 | 文献检索下载 | `skills/literature-search-download/` | F2 | 执行 | 乙 | `feat/f2-landscape` | 可演示 |
| 6 | 文献精读入库 | `skills/literature-reader/` | F2+F3 | 执行 | 乙（丙复用） | `feat/f2-landscape` | 可演示 |
| 7 | 文献全景撰写 | `skills/literature-landscape-writer/` | F2 | 执行 | 乙 | `feat/f2-landscape` | 可演示 |
| 8 | 引用核对 | `skills/citation-verifier/` | F2 | 自动程序 | 乙 | `feat/f2-landscape` | 可演示 |
| 9 | 关系可视化 | `skills/survey-visualizer/` | F2 | 执行 | 乙 | `feat/f2-landscape` | 可演示 |
| 9b | 综述撰写（扩展） | `skills/survey-writer/` | F2 扩展 | 执行 | 乙 | `feat/f2-landscape` | 可演示（扩展） |
| 10 | 单篇深读 | `skills/paper-deep-read/` | F3 | 工作流 | 丙 | `feat/f3-deep-read` | 未开始 |
| 11 | 阶段进展整理 | `skills/progress-digest/` | F4 | 工作流 | 乙 | `feat/f4-progress-digest` | 可演示 |
| 12 | 学术写作 | `skills/academic-writing/` | F5 | 工作流 | 丁 | `feat/crosscut-writing` | 可演示（薄） |
| 13 | 组会材料包 | （不单独落地） | F5 | — | 丁 | — | **取消独立技能**：组会话术路由到 #12 文体包 |
| 14 | 挑刺审阅 | `skills/adversarial-lite/` | F5 | 内部 | 丁（可选） | `feat/crosscut-writing` | 骨架（标准档不默认开） |

---

## 公用文档与路由

| 文件 | 用途 | 状态 |
|------|------|------|
| `AGENTS.md` | 智能体冷启动路由索引 | 草稿已审 |
| `shared/honesty-checklist.md` | 成稿前诚信勾选清单（F1–F5 强制引用） | 草稿已审 |
| `shared/effort-contract.md` | 深度档行为上限（现阶段仅标准档生效） | 草稿已审 |
| `shared/encoding-utf8.md` | 中文编码规范 | 草稿已审 |
| `shared/workspace-layout.md` | 工作区目录与 `references.json` 字段约定 | 草稿已审（已对齐协议 §6） |
| `shared/platform-notes.md` | 宿主平台安装与差异 | 草稿已审（部分配置待实测） |
| `shared/scripts/check_encoding.py` | 交付前编码机械检查 | 可用 |
| `docs/接口与协议.md` | 协作协议（冻结项以此为准） | 已确认 |
| `docs/分工说明.md` | 第一周并行分工 + F2/F4/F5 开发进度 | 已确认（进度节随 PR 更新） |
| `docs/开发进度-F2F4.md` | 周报短索引（含 F5 薄落地） | 随 PR 更新 |
| `docs/F5设计提纲-扩大版.md` | F5 写作中枢扩大版设计与审批记录 | 已批；技能已薄落地 |
| `docs/分支约定.md` | 分支与 PR 规则 | 已确认 |

---

## 维护规则

1. **状态变更**由负责人在对应 PR 中一并更新本表。
2. **新技能立项**：先在本表登记（状态 = 骨架），再建目录；技能名用小写英文 + 连字符。
3. **F4（progress-digest）** 已落地：演示话术与夹具见 `examples/f4-sample-run/`；脚本冒烟见 `tests/scripts/run_f4_script_smoke.py`。
4. **F5（academic-writing）** 核心已落地：一体多文体包；夹具见 `examples/f5-sample-writeup/`；`adversarial-lite` 为可选骨架；不建 `meeting-brief`。
5. 本表与 `AGENTS.md` §7 的技能清单保持同步；新增 / 删除技能时两处一起改。
