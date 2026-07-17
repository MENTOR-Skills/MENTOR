# f2-survey-extension

## 案例是什么

F2 **长篇综述扩展**样例：在同一文献库上展示 `survey-writer` 产出的 `survey.md` 形态（主题综合、比较表、开放问题、参考文献）。  
篇幅为演示级短综述，不是投稿相机就绪稿。

## 涉及哪些 skills

| 技能 | 本例角色 |
|------|----------|
| `literature-reader` | 上游库字段（复用 sample-topic） |
| `literature-landscape-writer` | 建议先有全景（可对照 sample-topic） |
| `survey-writer` | 本例核心：`survey.md` |
| `citation-verifier` | 成稿后应对库内引用再核一次 |

## 交付物是什么

| 路径 | 说明 |
|------|------|
| `../sample-topic/references.json` | 文献库（不重复拷贝大数据） |
| `survey.md` | 独立综述草稿样例 |
| （可选）`related-work.md` | 本例未单独给出；模板见技能 `references/related-work-template.md` |

## 如何复现

1. 阅读 `skills/survey-writer/SKILL.md` 与 `references/venue-writing-norms.md`。
2. 对照本目录 `survey.md` 与 `examples/sample-topic/references.json`：是否只引用库内文献。
3. Cursor 话术（写入跑场时）：

> 工作区用 `tests/runs/my-survey/`，文献库先从 `examples/sample-topic/references.json` 复制。  
> 调用 `survey-writer`，文体选独立综述，中文，数字序引用，产出 `survey.md`，然后跑 citation-verifier。
