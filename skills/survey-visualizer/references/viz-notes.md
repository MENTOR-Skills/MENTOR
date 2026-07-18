# 可视化说明

- 唯一数据源：工作区根目录 `references.json`。
- 统计面板：年份、venue、`access_status`、全文覆盖；可选 `meta.audit`。
- 关系图：读取 `papers[].relations`；`basis: fact` 实线，`basis: inferred` 虚线。
- `target_id` 不在当前 `papers` 中 → 跳过，不发明节点。
- 无 relations → 仍生成页面，关系区提示「未发明边」。

## 后续方向（审美加强）

仓库级后续见 `docs/开发进度-F2F4.md`：**可视化审美加强**——版式/配色/图例可读性；确保页脚或面板同步展示已有 `meta.audit`；推断边与事实边保持一眼可辨。不改变「只读库、不编造边」硬规则。
