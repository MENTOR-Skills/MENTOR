# 中文编码规范：UTF-8 与 Windows 防乱码

> 依据设计方案 §4.2
> 适用范围：所有中文交付文件、脚本输出、工作区 Markdown 报告。

---

## 规则

1. **所有中文交付文件必须使用 UTF-8 编码（无 BOM）保存。**
2. **在 Windows 上，正式交付前运行编码检查。**
3. **脚本路径使用相对路径，禁止写死绝对路径。**

---

## 写给技能的指令

### 写入文件时

- Python：`open(path, 'w', encoding='utf-8')`
- PowerShell 7+：`Out-File -Encoding utf8NoBOM`（PS 7 起 `utf8` 默认即无 BOM）
- ⚠️ Windows PowerShell 5.1：`Out-File -Encoding utf8` / `Set-Content -Encoding utf8` **会写入 BOM**，与「无 BOM」规则冲突。改用：
  ```powershell
  [System.IO.File]::WriteAllText($path, $text, [System.Text.UTF8Encoding]::new($false))
  ```
- 不用系统默认编码（Windows 上通常是 GBK）

### 读取文件时

- Python：`open(path, 'r', encoding='utf-8')`
- 遇到 `UnicodeDecodeError` → 尝试 `encoding='gbk'` 读取，然后转为 UTF-8 重写

### 运行编码检查

```bash
python shared/scripts/check_encoding.py <文件或目录>
```

检查逻辑：
1. 遍历指定路径下所有 `.md`、`.json`、`.yaml`、`.html` 文件
2. 尝试以 UTF-8 读取每个文件
3. 失败的报告为「非 UTF-8」，成功的检查是否有 BOM 头
4. 输出检查清单：✅ / ❌ / ⚠️（UTF-8 with BOM）

---

## 给 Windows 用户的说明

如果你发现打开 `.md` 文件后中文显示为乱码：

1. **不要用记事本打开。** Windows 记事本对 UTF-8 支持差。
2. 推荐使用 VS Code、Cursor、Notepad++ 等编辑器。
3. 如果用 VS Code，右下角可以看到当前编码，点击可切换为 UTF-8。

如果你用 Excel 打开 CSV/TSV 文件乱码：
- 用「数据 → 从文本/CSV 导入」，选择 UTF-8 编码导入。

---

## 检查脚本

脚本实体已落位：**`shared/scripts/check_encoding.py`**，供所有技能在交付中文文件前调用。用法见上文「运行编码检查」；实现逻辑（遍历 → UTF-8 试读 → BOM 警告 → 退出码）直接读脚本源码即可，本文不再内嵌副本，避免两处漂移。
