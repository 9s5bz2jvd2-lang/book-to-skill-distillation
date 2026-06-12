# Output Template — 稀疏蒸馏 Skill 交付模板

用于把一本书、长资料或方法论蒸馏成可调用 skill 时的最终交付结构。

## 1. Distillation brief

```markdown
# <skill-name> 稀疏蒸馏简报

## Source boundary
- 源材料：
- 授权/版权状态：
- 可公开内容：
- 不可公开内容：

## Shared core
- 核心定义：
- 安全/证据/版权红线：
- 输出原则：

## Routed experts
| Expert | 触发 | 反触发 | 默认预算 | 需要加载更多时 |
|---|---|---|---|---|
| | | | | |

## Missed-case sweep
- [ ] 反触发检查
- [ ] 相邻 skill 检查
- [ ] 证据/来源检查
- [ ] 隐私/版权检查
- [ ] 高风险安全门

## Artifacts
- `SKILL.md`
- `ROUTING.yaml`
- `GRAPH.md`
- `CACHE.md`
- `reference/source-map.md`
- `assets/eval-cases.md`
```

## 2. ROUTING.yaml minimal contract

```yaml
role: routed_expert_or_router
trigger_terms:
  strong: []
  weak: []
anti_triggers: []
neighbors:
  safety: []
  adjacent: []
budget:
  shared_core: "200-800"
  routed_high: "800-3000"
  routed_low: "200-800"
  heavy_reference: "on-demand"
missed_case_sweep:
  required: []
route_log_fields: []
```

## 3. Final answer format to human

```markdown
已完成：<skill-name>

位置：<path>

这次蒸馏把 <source> 转成了：
1. shared core：<一句话>
2. routed experts：<列出 2-5 个>
3. missed-case sweep：<列出关键查漏>
4. budget/cache：<一句话>
5. eval cases：<数量/类型>

注意边界：<版权/隐私/医学/证据红线>

下一步可选：
- 是否发布到共享 skill 库；
- 是否为它写 HTML explainer；
- 是否用一个真实任务自测。
```
