# 跨次会话恢复流程

> 被 `research-workspace` 在检测到已有工作区时调用。
> 目标：从磁盘文件恢复上下文，避免依赖聊天记忆。

## 决策流程

```
检测到 campus-research-output/<简称>/ 已存在
  │
  ├─ _work/state.yaml 可读？
  │   ├─ 是 → 读取所有字段
  │   └─ 否 → 尝试从 research-log.md 重建
  │            ├─ 可重建 → 写入新 state.yaml，标注「reconstructed」
  │            └─ 不可重建 → 视为新课题（保留已有文件，不覆盖）
  │
  ├─ _work/ 下存在 WAITING_*.md？
  │   ├─ 是 → 按创建时间排序，优先处理最早的一个
  │   │       读取 WAITING 内容 → 向用户说明当前卡点
  │   └─ 否 → 直接进入状态恢复
  │
  ├─ 读取 research-log.md 最近 3 条记录
  │
  └─ 向用户确认：「上次我们做到了 [state.current_skill] 第 [state.step] 步，
      现在继续还是调整？」
      ├─ 继续 → 更新 state.yaml（last_updated，清除 waiting_for）
      │         通知 orchestrator 路由到 state.current_function
      └─ 调整 → 询问用户想做什么
                 orchestrator 重新路由
```

## 恢复向用户展示的信息模板

```markdown
## 恢复会话：<课题简称>

**上次状态：**
- 功能：<F1–F5>
- 技能：<skill-name>
- 进度：第 <step> 步 / 共 N 步
- 时间：<last_updated>

**卡点：** <waiting_for 的中文说明；无则写「无卡点」>

**最近记录：**
1. <research-log.md 最近第 1 条>
2. <research-log.md 最近第 2 条>
3. <research-log.md 最近第 3 条>

继续还是调整？
```

## 边界情况处理

| 情况 | 处理 |
|------|------|
| 多个 WAITING 文件 | 按文件修改时间排序，先处理最早的；一次只处理一个卡点 |
| state.yaml 中 `waiting_for` 与 WAITING 文件不一致 | 以 WAITING 文件为准；更新 state.yaml 的 waiting_for |
| research-log.md 为空或不存在 | 只展示 state.yaml 信息；标注「无历史记录」 |
| 工作区目录存在但 _work/ 为空 | 视为损坏的工作区；询问用户是否重建 |
| 用户换了电脑/路径 | 如果 `scope.md` 中的绝对路径不可访问，提醒用户更新路径 |
