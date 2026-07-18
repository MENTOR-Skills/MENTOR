# 成稿质量门（survey-writer）

成稿交付前逐项勾选；任一项不通过须改稿或显式写入「局限声明」，不得假装达标。

## A. 语料与诚实

- [ ] 正文引用**全部**来自 `references.json`，无库外文献
- [ ] 独立/系统模式：≥ 8 篇有 `reading_notes`，或已在摘要/引言声明「语料局限」
- [ ] Related Work：≥ 5 篇 + 用户贡献已反映于 positioning
- [ ] 预印本已标 `(preprint)`；推断已标「推断」
- [ ] 无「已全部核验」类自背书；审计在 `_work/CITATION_AUDIT.*`

## B. 结构与写法

- [ ] 主结构为**主题综合**，非按年份或逐篇摘要流水账
- [ ] 独立综述：≥ 3 个主题节（或叙事包中的等价叙事段）
- [ ] 含比较/讨论（表或段）且注明不可比之处
- [ ] 开放问题/展望关联已引用工作，区分「库内可见」与全域断言
- [ ] Related Work 含 positioning，说明与本文贡献差异
- [ ] 系统梳理：`_work/selection-protocol.md` 已写且与正文范围一致

## C. 篇幅与格式

- [ ] 中文独立综述约 **2500+ 字**（演示样例可 shorter 但须标注演示级）
- [ ] Related Work 篇幅短于独立综述
- [ ] 引用风格全文统一（`[1]` 或作者—年份）
- [ ] UTF-8；`check_encoding.py` 通过

## D. 程序校验

- [ ] 已跑 `citation-verifier`；失败项已处理或标未核实
- [ ] `research-log.md` / `state.yaml` 已更新（如适用）

## 不通过时的默认动作

| 问题 | 动作 |
|------|------|
| 篇数不足 | 回流 `literature-search-download` / `literature-reader`，或写局限声明短稿 |
| 编年/逐篇体 | 重写大纲，按主题合并段落 |
| 缺 selection-protocol | 补写 `_work/selection-protocol.md` 再交付 survey |
| 缺贡献说明（RW） | 停下，写 `_work/WAITING_contribution.md` |
