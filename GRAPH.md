# GRAPH.md — 稀疏蒸馏 Skill Graph 关系图

本文件说明“稀疏蒸馏 | Book-to-Skill Sparse Distillation”与相邻 skill / 工作流的关系。它不是运行时强制 API，而是给 agent 和未来路由器看的图谱说明。

## 1. 上游输入

本 skill 通常从以下来源进入：

- **归一**：一次复杂任务完成后，判断经验值得写成 skill。
- **textbook-distillation**：已有教材/图书学习轨道，需要升级为可调用 skill 或大型 skill library。
- **Anthropic / Perplexity Skills 结构讨论**：folder + progressive disclosure + scripts/assets/references 的基础。
- **DeepSeek / MoE 稀疏激活启发**：不是模型专家，而是 skill runtime/design 层面的 sparse activation。
- **临床营养工作流**：先抓最可能问题，再做红旗/禁忌/特殊人群/证据查漏。

## 2. 下游输出

本 skill 的输出可流向：

- 新建 `.library/custom/<skill-name>/`；
- 发布到 `.library_shared/<skill-name>/`（须经人类确认）；
- 形成 GitHub issue / discussion / PR 的结构化 proposal；
- 形成 Orange Book / 技术文章 / 方法论文档；
- 形成 eval cases 与 route-log 回流计划。

## 3. 邻近 skill

| 邻居 | 关系 | 何时联用 |
|---|---|---|
| 归一 | 上游蒸馏方法 | 需要从一次任务经验炼成通用 skill |
| skills-manual | 元规范 | 创建/验证/发布 skill 前必须读 |
| textbook-distillation | 内容蒸馏 | 源材料是书、教材、课程、长文档 |
| anti-hallucination-academic-writing | 证据门 | 学术/论文/引用相关材料 |
| nutrition-history-anti-hallucination | 历史文献门 | 食疗史、古籍、营养史 |
| food-agent-methodology | 营养 agent 红线 | 营养/医学 agent 口径、边界、评测 |
| nutrition-ai-productization | 产品化 | 把 skill library 变成 AI 产品路线 |
| lingtai-issue-report | 外部反馈 | 要向上游提交 issue/PR/discussion |
| html-report | 人类交付 | 需要把蒸馏结果做成可读 HTML |

## 4. 互斥 / 反触发

不要把本 skill 用作：

- 普通摘要器；
- 盗版/规避版权工具；
- 私有事实存储；
- “把所有资料塞进一个巨大 SKILL.md”的压缩器；
- 只追求低 token、但没有安全查漏的路由器。

## 5. 安全门关系

高风险领域必须联动安全门：

```text
user task
  -> sparse-book-to-skill-distillation
  -> safety/evidence gate
  -> routed expert(s)
  -> missed-case sweep
  -> output
```

营养/医学类至少扫：

- 是否替代诊断/治疗；
- 是否涉及特殊人群；
- 是否有药物、疾病、妊娠、儿童、进食障碍等风险；
- 是否伪造或夸大证据；
- 是否使用羞耻化语言。

## 6. 关键词种子与点对点扩展

稀疏调用不是“只读一个节点然后冒险作答”，也不是“遍历所有书籍内容”。它应是：

```text
关键词 / 任务签名
  -> 命中 seed nodes
  -> 打开最相关专家节点
  -> 沿 graph edges 点对点扩展
  -> safety/evidence/red-flag gates
  -> missed-case sweep
  -> 输出并回流
```

扩展之边应有理由：

| 边类型 | 何时打开 | 例 |
|---|---|---|
| semantic neighbor | 同一主题的邻接概念会影响答案 | 膳食纤维 -> 胃肠耐受 |
| prerequisite | 当前节点需前置定义/分类 | BMI -> 儿童生长曲线/风险分类 |
| downstream action | 输出会落到具体干预/模板 | 儿童肥胖 -> 家庭饮食行为 |
| safety/evidence | 涉及高风险或强结论 | 儿童肥胖 -> 儿科安全门/指南锚点 |
| contradiction check | 两节点可能给出冲突建议 | 高纤维建议 -> 肠胃疾病禁忌 |
| source anchor | 需要可核证出处 | 营养建议 -> 指南/教材 source map |

营养学示例：若用户问儿童 BMI 超标，不应遍历整套营养学书籍；应先命中 `childhood_obesity / BMI / family_meal_pattern`，再点对点扩展到儿科安全门、去羞耻语言、转诊边界、指南证据锚点。详见 `assets/sparse-nutrition-example.md`。

## 7. Skill 作为“微型 LLM”的边界类比

存储了大量判断、触发、流程、案例、脚本和 reference 的 skill，在某种意义上可以看作一个**外置的、可编辑的、微型任务模型**：

| LLM/MoE 概念 | Skill Graph 对应物 |
|---|---|
| 参数记忆 | SKILL.md / reference / assets 中沉淀的流程与判断 |
| tokenizer / input interface | skill 的触发词、输入契约、反触发 |
| gate | ROUTING signature 与邻接关系 |
| expert | 具体 workflow、脚本、案例、证据门、模板 |
| shared layers | shared core：版权、隐私、安全、证据边界 |
| eval | assets/eval-cases.md 与验收门 |
| fine-tuning / continual learning | route log 与使用反馈回流 |

但边界也要写清：skill **不是**真正的神经网络参数模型；它不会自动泛化，也不会自己训练。它更像“把一小块专家能力外置成可读、可改、可验证的模型接口”。因此它要靠：短入口、轻 gate、重资料按需、eval 回流，才能像微型 LLM 一样被调用，而不是退化成一堆长文档。

## 8. 从 LingTai #177 吸收的循环流形思想

LingTai #177 被吸收的方式很克制：它没有变成 runtime 机制，也没有宣称真正实现数学流形；而是被黄泽森转译为文档中的**设计隐喻**：Tree 负责分化，Graph 负责连接，Cyclic Manifold 负责回返、连续性、粗粒度沉淀与身份不变。

迁移到本 skill，得到一个原则：

> **Skill Graph 的分支不算完成，直到它回到可复用的压缩结构。**

对应关系：

| #177 循环流形语言 | 稀疏蒸馏 skill 语言 |
|---|---|
| outward trajectory | 一次任务调用、一次专家展开、一次查漏分支 |
| coarse-graining | 把长过程压成 signature / checklist / gotcha / eval / reference brief |
| durable center | SKILL.md shared core、ROUTING.yaml、CACHE.md、GRAPH.md |
| return map | 输出后回流：更新触发词、邻接边、验收门、重料索引 |
| continuity invariant | skill 的用途、红线、输出契约不随每次调用漂移 |
| low-power intuition | 下一次少读历史、少重推流程、少加载重料 |

因此，本 skill 的“球/环”不是装饰，而是验收门：每个非平凡调用结束时必须问：

1. 这次命中的入口能否压成更短 signature？
2. 这次查漏是否暴露了新的交叉边？
3. 哪些长解释可沉淀为 brief，哪些仍应留在 heavy reference？
4. 哪个 gotcha / eval 应该补进来，避免下次重犯？
5. 哪些细节只是噪声，应该被剪掉而不是带入下一轮？

一句话：**网给 skill 以通达，环给 skill 以低功耗；分支出去，回流成丹。**

## 9. 回流关系

每次使用后，将经验回流到：

- `ROUTING.yaml`：新增触发词、反触发词、邻居；
- `assets/eval-cases.md`：新增正例、反例、查漏例；
- `CACHE.md`：修正哪些内容应稳定常驻、哪些应后置；
- `reference/source-map.md`：补来源结构；
- 上游 issue/PR：若发现 runtime 能力缺口。

一句话：**Graph 不是为了复杂，而是为了让“省 token”不等于“少看风险”。**
