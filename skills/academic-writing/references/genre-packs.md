# 文体包对照（人话）

进 F5 = 打开 `academic-writing`，选下表**一个** id。组会不再另开技能。

## 怎么选

| 你想要… | 选 | 得到什么文件 |
|---------|-----|--------------|
| 导师一眼能看完的进展 | `meeting-one-pager` | `meeting-one-pager.md` |
| 预演会被问什么 | `meeting-qna` | `qna-prep.md` |
| 照着念的口播 | `meeting-talk` | `meeting-talk.md` |
| 写进周报/阶段说明的技术段落 | `stage-writeup` | `stage-writeup.md` |
| PPT：先大纲，有 LaTeX 再 Beamer | `meeting-slides` | `meeting-slides-outline.md`（± `.tex`） |
| README / 用法说明类 | `tech-doc` | `tech-doc.md` |
| 已有底稿，改某一节 | `paper-section` | `paper-section-<slug>.md` |
| 已有底稿，按某刊语气润色 | `polish` | `polish-<slug>.md` |

## 批次

- **核心（首版必会）：** 主张—证据 + `meeting-one-pager` / `meeting-qna` / `meeting-talk` / `stage-writeup`
- **第二批（薄模板可用）：** `meeting-slides` / `tech-doc` / `paper-section` / `polish`

## 别进错门

| 需求 | 正确去向 |
|------|----------|
| 从零写 Related Work / 长综述 | F2 `survey-writer`，**不是**本技能 |
| 扫代码日志出阶段四文件 | F4 `progress-digest` |
| 找论文 / 全景 | F2 主链 |

## 共同规矩（所有包）

1. 先写 `_work/claims-evidence.md`
2. 文件名只用 ASCII
3. 勾选 `shared/honesty-checklist.md`
4. 无证据 → 标缺口或删主张，不编造
