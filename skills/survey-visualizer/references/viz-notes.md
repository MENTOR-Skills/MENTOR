# 可视化说明

- 唯一数据源：工作区根目录 `references.json`。
- 统计面板：年份、venue、`access_status`、全文覆盖；可选 `meta.audit`。
- 关系图：读取 `papers[].relations`；`basis: fact` 实线，`basis: inferred` 虚线。
- `target_id` 不在当前 `papers` 中 → 跳过，不发明节点。
- 无 relations → 仍生成页面，关系区提示「未发明边」。
