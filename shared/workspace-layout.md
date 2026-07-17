# 工作区目录约定

> 依据设计方案 §2.5
> 本文件定义用户课题工作区的标准目录结构和各文件用途。所有技能读写文件时遵守此约定。

---

## 目录结构

默认路径：`campus-research-output/<课题简称>/`（允许用户指定根路径）

```text
campus-research-output/<课题简称>/
├── scope.md                 # 主题、时间范围、深度档、用户确认事项、禁止事项
├── findings.md              # 当前认知摘要（可跨周更新）
├── research-log.md          # 追加式工作记录（做了什么、为何停下）
├── _work/                   # 过程文件（可重建，技能升级不覆盖）
│   ├── WAITING_*.md         # 正在等待用户完成的事项说明
│   ├── shortlist.json       # 精读候选清单
│   ├── claims-evidence.md   # 主张与证据对照表
│   └── state.yaml           # 当前功能、步骤、确认关卡状态
├── pdfs/
│   ├── auto/                # 自动下载的开放获取全文（可重建）
│   └── user/                # 用户自行补充的全文（不可自动删除）
├── references.json          # 结构化文献库（后续技能以此为准，JSON 格式）
├── reading-reports/         # F3 单篇阅读报告（给人读的 Markdown）
├── learning-map.md          # F1 交付：学习地图
├── prerequisite-gap.md      # F1 交付：知识缺口说明
├── glossary.md              # F1 交付：术语表
├── starter-resources.md     # F1 交付：起步材料
├── first-practice.md        # F1 交付：首次练习
├── literature-landscape.md  # F2 交付：文献全景说明
├── reading-shortlist.md     # F2 交付：精读清单
├── survey.md                # F2 可选扩展：长篇综述（survey-writer）
├── related-work.md          # F2 可选扩展：论文 Related Work
├── progress-report.md       # F4 交付：阶段报告
├── artifact-index.md        # F4 交付：材料索引
├── result-summary.md        # F4 交付：结果摘要
├── blockers.md              # F4 交付：阻塞清单
├── stage-writeup.md         # F5 交付：阶段技术说明
├── meeting-one-pager.md     # F5 交付：组会一页纸
├── qna-prep.md              # F5 交付：预期问答
└── viz/                     # F2 交付：关系图网页
    └── index.html
```

---

## 各文件类型约定

| 类型 | 格式 | 读者 | 规则 |
|------|------|------|------|
| `*.md` | Markdown | 人 | 给人阅读的说明与报告；UTF-8 编码 |
| `*.json` | JSON | 技能（程序读取） | 结构化数据，后续技能以此为准；字段名用英文 |
| `*.html` | HTML | 人（浏览器） | 仅浏览用，数据来自 JSON，不得编造 |
| `*.yaml` | YAML | 技能 + 人 | 状态文件，字段名用英文 |

---

## 核心文件详细约定

### `scope.md`

每次研究任务的起点。必须包含：

```markdown
# 研究范围说明
- 主题：
- 时间范围：
- 深度档：轻量 / 标准 / 深入
- 输出语言：
- 期刊/会议偏好（如有）：
- 允许扫描的本地路径（F4 专用）：
- 选用的领域内容包编号（如有）：
- 禁止事项：
- 用户已确认：[是/否]
```

### `references.json`

结构化文献库，是所有文献相关技能的共享数据源。字段口径以 `docs/接口与协议.md` §6 为准。

> **可演化约定：** 以下为最小字段集，不是最终形态。后续开发中可按需添加扩展字段（如 `topics`、`status`、`reading_report`），或在团队内协商后调整结构使其更合理；任何调整须同步更新本节与协议 §6，并通知乙丙丁三方，避免读写口径漂移。

```json
{
  "papers": [
    {
      "id": "稳定编号（优先 arXiv id / 开放库 id，否则团队手编且全程不变）",
      "title": "论文标题",
      "authors": ["作者1", "作者2"],
      "year": 2024,
      "venue": "期刊 / 会议 / 预印本平台名称；未知写空字符串",
      "url": "可访问链接（建议）",
      "doi": "10.xxxx/xxxxx（有则填）",
      "arxiv_id": "2401.xxxxx（有则填）",
      "pdf_path": "pdfs/auto/xxx.pdf 或 pdfs/user/xxx.pdf；尚无全文可空",
      "access_status": "fulltext | abstract_only | waiting_user_pdf | unknown",
      "abstract": "摘要（建议）",
      "reading_notes": {
        "problem": "研究问题（短句）",
        "method": "方法（短句）",
        "results": "主要结果或结论（短句）",
        "limitations": "局限（短句）"
      },
      "relations": [
        { "target_id": "另一篇的 id", "kind": "引用 | 方法继承 | 观点冲突 等", "basis": "fact | inferred" }
      ]
    }
  ]
}
```

- 必填：`id`、`title`、`authors`、`year`、`venue`、`access_status`；`reading_notes` 在深读或入库后必填。
- `relations` 可选（F2 用）；`basis` 为 `inferred` 的关系不得写成事实。
- `cite_key` 不入库：需要导出文献列表 / BibTeX 时由程序按「第一作者姓 + 年份」自动生成（见协议 §6）。
- 可选扩展示例：`topics`、`status`（to_read / reading / read）、`reading_report`（指向 `reading-reports/<id>.md`）等，团队约定后使用。

### `_work/state.yaml`

记录当前任务状态，供跨次会话续跑：

```yaml
session:
  last_updated: "2026-07-15T14:30:00"
  current_function: "F2"       # F1-F5
  current_skill: "literature-search-download"
  depth: "standard"             # lightweight | standard | deep
  step: 2                       # 当前技能内的步骤编号
  waiting_for: null             # 如有卡点，写 "user_pdf" / "user_confirm" 等
  completed_steps: [1]
```

### `_work/WAITING_*.md`

当流程停在确认关卡等用户时写入。文件名描述等待内容。结构：

```markdown
# 等待事项：[一句话标题]
- 当前状态：
- 你需要做：
- 完成后我将：
- 创建时间：
```

---

## 忽略规则（F4 扫描时自动跳过）

以下目录和文件在阶段总结扫描时自动忽略，不得读取或索引：

- 依赖目录：`node_modules/`、`venv/`、`.venv/`、`__pycache__/`
- 版本库内部：`.git/`、`.svn/`
- 模型权重：`*.pth`、`*.ckpt`、`*.safetensors`、`*.bin`（>10MB）
- 数据集本体：`*.tfrecord`、`*.hdf5`、`*.arrow`
- 密钥与配置：`.env`、`*.key`、`*.pem`、`secrets.*`、`credentials.*`
- 二进制与媒体：`*.exe`、`*.dll`、`*.so`、`*.mp4`
