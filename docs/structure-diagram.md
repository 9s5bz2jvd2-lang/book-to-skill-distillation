# book-to-skill-distillation sparse overlay — Structure Diagram

This diagram shows how a long source such as a book, textbook, course, or project methodology is distilled into a sparse, callable Skill system.

```mermaid
flowchart TD
    A[Book / Textbook / Long Methodology<br/>书籍·教材·课程·长资料] --> B[Distillation Pass<br/>提炼：核心判断 / 场景 / 红线 / 输出]

    B --> C[Shared Core<br/>常驻核心]
    B --> D[Skill Experts<br/>局部专家群]
    B --> E[References & Assets<br/>重资料 / 模板 / 案例]

    C --> C1[Evidence / Safety / Copyright<br/>证据边界·安全红线·版权边界]
    C --> C2[Output Contract<br/>交付格式·验收标准]

    D --> D1[Expert A<br/>章节 / 方法 / 场景 A]
    D --> D2[Expert B<br/>章节 / 方法 / 场景 B]
    D --> D3[Expert C<br/>章节 / 方法 / 场景 C]

    E --> E1[reference/<br/>按需深读]
    E --> E2[scripts/<br/>可执行工具]
    E --> E3[assets/<br/>模板·评测·案例]

    U[User / Agent Task<br/>当前任务] --> G[Lightweight Gate<br/>ROUTING.yaml<br/>轻门控：触发 / 反触发 / 预算]

    G -->|top-k hit| D1
    G -->|top-k hit| D2
    G -->|if needed| R[Missed-case Sweep<br/>低预算查漏]

    R --> X1[Red Flags<br/>红旗 / 禁忌]
    R --> X2[Neighbor Skills<br/>邻近主题]
    R --> X3[Special Populations<br/>特殊人群 / 边界条件]

    D1 --> O[Task Output<br/>产出]
    D2 --> O
    X1 --> O
    X2 --> O
    X3 --> O
    C1 --> O
    C2 --> O

    O --> V[Validation / Evals<br/>验收与自检]
    V --> L[Route Log / Gotchas<br/>路径记录·踩坑·误触发]
    L --> K[Cache & Graph Update<br/>回流：更短签名 / 更准邻接 / 更好缓存]
    K --> G

    classDef core fill:#fff4cc,stroke:#d6a700,color:#222;
    classDef gate fill:#e8f0ff,stroke:#4b6fd6,color:#111;
    classDef expert fill:#edf8ed,stroke:#3b8f45,color:#111;
    classDef risk fill:#ffecec,stroke:#d95c5c,color:#111;
    classDef loop fill:#f2eaff,stroke:#8a5bd6,color:#111;

    class C,C1,C2 core;
    class G gate;
    class D,D1,D2,D3 expert;
    class R,X1,X2,X3 risk;
    class V,L,K loop;
```

## One-line model

```text
Book
  -> shared core + routed experts + heavy references
  -> lightweight gate
  -> top-k activation + missed-case sweep
  -> output + validation
  -> route log / gotcha / eval feedback
  -> better cache hit next time
```

## Chinese shorthand

> 先炼核心，再分专家；先中主脉，再扫旁枝；预算分层，重料后置；路由留痕，越用越准。

> 网给 Skill 以通达，环给 Skill 以低功耗；分支出去，回流成丹。


## Proposal-based self-evolution

The feedback loop is intentionally not a hidden auto-mutation loop. Route logs, gotchas, and missed cases should become **reviewable patches** to `ROUTING.yaml`, `GRAPH.md`, `CACHE.md`, and eval cases. See [`self-evolution-loop.md`](self-evolution-loop.md).
