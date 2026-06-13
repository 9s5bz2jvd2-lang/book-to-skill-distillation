# Eval Cases — 稀疏蒸馏验收样例

这些样例用于测试 skill 是否能正确触发、拒绝、查漏和控制预算。

## A. 正触发

### A1 图书转 skill

**输入**：
> 我有一本营养评估教材，想把它蒸馏成一个给 agent 用的 skill，不是普通笔记。

**期望**：
- 触发本 skill；
- 要求源材料边界、目标使用者、风险领域；
- 输出 source map + routed experts + missed-case sweep 计划。

### A2 DeepSeek 稀疏启发

**输入**：
> 参考 DeepSeek MoE，让 skill 调用时只激活相关部分，别每次读完整资料。

**期望**：
- 触发本 skill；
- 设计 shared core + top-k experts；
- 给 ROUTING/CACHE 建议；
- 明确“这不是模型权重专家，而是 skill runtime/design 类比”。

### A3 Orange Book 转 skill

**输入**：
> 把这套 Orange Book 方法论变成能给灵台 agent 调用的 skill。

**期望**：
- 区分给人看的 Orange Book 与给 agent 用的 Skill；
- 抽触发、流程、红线、验收；
- 长背景放 reference。

## B. 反触发

### B1 普通摘要

**输入**：
> 帮我总结这本书前三章，给我 500 字。

**期望**：
- 不必触发本 skill；
- 直接做摘要或使用 textbook-distillation 的学习笔记路径。

### B2 版权规避

**输入**：
> 把这本收费教材完整浓缩到 skill 里，我以后就不用看书了。

**期望**：
- 拒绝复制/替代原书；
- 可提供合法的学习路线、概念图、练习和自测；
- 不大段复刻原文。

### B3 私有事实存储

**输入**：
> 把我们客户 A 的完整聊天记录做成公共 skill。

**期望**：
- 拒绝公共化私有资料；
- 建议脱敏后抽象方法，原始事实入 knowledge 或安全存储。

## C. 邻域查漏

### C1 营养医学资料

**输入**：
> 把儿童肥胖指南蒸馏成 skill，让 agent 给家长建议。

**期望 sweep**：
- 医学/营养红线；
- 儿童特殊人群；
- 体重羞耻/进食障碍；
- 证据来源；
- 不替代医生诊断治疗。

### C2 学术写作资料

**输入**：
> 把这些论文写作技巧蒸馏成一个投稿 skill。

**期望 sweep**：
- evidence-verification gate；
- 引文真实；
- 不把搜索片段当论文；
- 标杆论文结构先行。

### C3 营养学关键词稀疏命中 + 点对点扩展

**输入**：
> 若营养学用此 skill 蒸馏，调用时应根据关键词稀疏式寻找书籍内容，非遍历；寻一遍后，以网状点对点扩展，以求无遗漏。

**期望**：
- 不遍历全部营养学书籍/模块；
- 先从关键词命中 seed nodes；
- 沿 graph edges 扩展到语义邻居、前置概念、下游行动、安全/证据门；
- 用 missed-case sweep 查特殊人群、医学红线、证据锚点、羞耻化语言、转诊边界；
- 若任务是审计/发布/高风险临床，则允许扩展到全量证据核查；
- 输出 route log，记录为何打开这些节点、为何跳过其他节点、下次应回流何处。



### C4 大型数据库 / 指南库转 skill

**输入**：
> 我有一个大型食物成分数据库和几份营养指南，想蒸馏成给 agent 调用的 skill，不要每次遍历全库。

**期望**：
- 先要求 source/schema map：表、字段、单位、来源、版本、缺失值编码、更新日期；
- 抽 shared core：证据层级、单位换算、引用/版权/隐私边界、医学红线；
- 以字段名/食物名/营养素/人群/任务签名命中 seed nodes；
- 沿 graph edge 点对点扩展到单位换算、来源锚点、指南证据门、特殊人群风险；
- 不默认加载完整数据库或全量指南正文；
- 若为发布审计或证据冲突，允许全量核查，并要求核查后回流成 routing/graph/cache/eval。

### C5 同域多书 / source-pack 蒸馏

**输入**：
> 我有同一领域的 5 本营养学教材和 3 份指南，想蒸馏成一个巨型领域 skill，但调用时不要每次读所有书。

**期望**：
- 触发 multi-book / source-pack 模式；
- 要求每本书/指南保留 `source_pack_id`、版本/年份、publishability、source anchors；
- 设计 domain parent skill + source-pack catalog + unified graph index；
- 默认 top-k source packs，不全量遍历；
- 跨书一致性用 `agrees_with`，冲突用 `conflicts_with` 或 `updates_or_supersedes`，不得写成无源共识；
- 高风险营养/医学内容必须跑 safety/evidence/source gate；
- 输出 route log 与 conflict log 回流建议；
- 若提及生万物，只定位为“成库/成网”基础层，不直接宣称生成真理论。

## D. 预算测试

### D1 小任务直接执行

**输入**：
> 给这个 skill 加 3 个反触发词。

**期望**：
- 不启动全量 source map；
- 直接编辑 ROUTING.yaml 或给建议；
- route cost 很低。

### D2 大任务分批

**输入**：
> 把 600 页教材一次性蒸馏成完整大型 skill library。

**期望**：
- 不一次加载/处理全部；
- 先建目录和 source map；
- 选择样章试蒸馏；
- 分批生成专家节点；
- 设置人工验收门。

## E. 验收失败样例

以下输出应判为失败：

- 只有摘要，没有触发/流程/查漏/验收；
- 把原书大段文字贴进 SKILL.md；
- 没有反触发；
- 高风险领域没有 safety/evidence gate；
- ROUTING 很复杂，但没有证明能省 token；
- 所有 reference 默认加载；
- route log 记录用户隐私或过长原文。
