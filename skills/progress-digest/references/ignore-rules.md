# F4 扫描忽略规则

与 `shared/workspace-layout.md`「忽略规则（F4 扫描时自动跳过）」一致。`list_recent_files.py` 与 Agent 手工索引均须遵守。

## 目录名（路径任一段匹配即跳过）

- `node_modules`
- `venv` / `.venv`
- `__pycache__`
- `.git` / `.svn`

## 文件名 / 扩展名

| 类别 | 模式 |
|------|------|
| 模型权重 | `*.pth`、`*.ckpt`、`*.safetensors`；`*.bin` 且 >10MB |
| 数据集本体 | `*.tfrecord`、`*.hdf5`、`*.arrow` |
| 密钥与配置 | `.env`、`*.key`、`*.pem`、`secrets.*`、`credentials.*` |
| 二进制与媒体 | `*.exe`、`*.dll`、`*.so`、`*.mp4` |

## Agent 额外注意

- 即使脚本漏过滤，Agent 也不得打开疑似密钥文件写入交付。
- 超大日志可只记入索引元数据，精读时截取头尾与含 `loss`/`acc`/`error` 的行。
