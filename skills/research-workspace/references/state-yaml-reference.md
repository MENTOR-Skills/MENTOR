# state.yaml 字段参考

> 被 `research-workspace` 和所有 F1–F5 技能在步骤转换时更新。
> 字段名使用英文；值按约定枚举。

## 完整结构

```yaml
session:
  last_updated: "2026-07-18T14:30:00"  # ISO 8601 时间，每次更新必改
  current_function: "F1"               # F1 | F2 | F3 | F4 | F5 | null（未路由时）
  current_skill: "domain-onboarding"   # 当前技能目录名（kebab-case）
  depth: "standard"                    # standard（现阶段固定；lightweight/deep 预留）
  step: 3                              # 当前技能内步骤编号（数字，对应 SKILL.md 步骤序号）
  waiting_for: null                    # null | user_pdf | user_confirm | user_materials | honesty_blocked | scan_scope | ...
  completed_steps: [1, 2]              # 已完成的步骤编号数组
```

## 字段说明

| 字段 | 类型 | 何时更新 | 允许的值 |
|------|------|----------|----------|
| `last_updated` | ISO 8601 字符串 | 每次写入 state.yaml 时 | 当前时间 |
| `current_function` | 字符串或 null | orchestrator 路由后 | `F1`–`F5`；未路由时为 `null` |
| `current_skill` | 字符串 | 进入新技能时 | 技能目录名（如 `domain-onboarding`） |
| `depth` | 字符串 | 初始化时写入，现阶段不改 | 固定 `standard` |
| `step` | 整数 | 每完成一个步骤后 | 对应 SKILL.md 中 `[ ]` 步骤序号 |
| `waiting_for` | 字符串或 null | 停车时设为具体原因；恢复后清为 `null` | 见下表 |
| `completed_steps` | 整数数组 | 每完成一步追加 | 如 `[1, 2, 3]` |

## `waiting_for` 常用值

| 值 | 含义 | 对应 WAITING 文件 |
|----|------|-------------------|
| `null` | 无卡点，正常运行中 | — |
| `user_pdf` | 等用户补充付费论文 PDF | `_work/WAITING_user_pdf.md` |
| `user_confirm` | 等用户确认某个选择或草稿 | `_work/WAITING_<topic>.md` |
| `user_materials` | 等用户提供材料（如 F4 扫描路径、F5 底稿） | `_work/WAITING_materials.md` |
| `honesty_blocked` | 诚信检查 BLOCKED，等用户处理 | `_work/WAITING_honesty_*.md` |
| `scan_scope` | 等用户确认 F4 扫描范围 | `_work/WAITING_scan_scope.md` |
| `scope_confirm` | 等用户确认 scope.md | `_work/WAITING_scope_confirm.md` |

## 更新规则

1. **每步必更新** `last_updated` 和 `step`
2. **停车必更新** `waiting_for`；恢复后必清为 `null`
3. **切换技能必更新** `current_skill` 和重置 `step` 为 1
4. **切换功能必更新** `current_function`
5. `completed_steps` 只增不减（表示历史完成记录）
