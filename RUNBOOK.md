# RUNBOOK — demand-sensitive sparse reading

This runbook turns the sparse-distillation method into an execution habit. Use it when invoking this skill, upgrading another skill, or auditing whether a distilled skill is truly sparse-callable.

Core rule:

> Start sparse. Expand on demand. Full reading is allowed when the task requires it. After broad/full reading, compress what you learned back into routing, graph, cache, evals, or a route log.

## 0. Before you read

Answer these first:

1. What is the task type?
   - quick lookup
   - normal distillation
   - cross-topic synthesis
   - high-risk safety/evidence work
   - audit / migration / refactor / quality investigation
   - full redesign
2. Is the source legally readable and publishable?
3. Is the user asking for operational transformation, not reproduction?
4. What would make sparse reading insufficient?
5. What must be recorded for return-to-cache?

If uncertain, produce a route plan before opening deep references:

```bash
python3 scripts/route_plan.py --task "<task>"
python3 scripts/route_plan.py --task "<task>" --mode audit --json
```

## 1. Reading modes

| Mode | Read first | Expand when | Stop when | Return artifact |
|---|---|---|---|---|
| quick lookup | `SKILL.md`, `ROUTING.yaml`, one expert | answer lacks boundary/evidence | answer is bounded and cites loaded module | short route log optional |
| normal distillation | `SKILL.md`, `RUNBOOK.md`, `ROUTING.yaml`, top 2–3 experts | source map incomplete, module conflict, high-risk content | target skill has router/core/experts/checks | route log + cache proposals |
| cross-topic synthesis | shared core + selected experts + `GRAPH.md` | two branches disagree or hidden neighbor appears | synthesis passes missed-case sweep | graph/cache update proposal |
| high-risk work | shared core + safety/evidence/copyright gates | claims need source verification | every strong claim has source boundary | safety route log |
| audit / migration / refactor | broad or full repo reading | any file may affect structure | findings compressed into actionable diffs | required route log |
| full redesign | full source/repo reading | always | new sparse structure validated | route log + eval updates |

Sparse is an economy default, not a prohibition. If the task is to audit the whole skill, find stale routing, migrate structure, or prove coverage, full reading is correct.

## 2. Standard sparse invocation

1. Read `SKILL.md`.
2. Read `ROUTING.yaml`.
3. Classify task:
   - anti-trigger? stop or redirect.
   - low-risk? top 1 expert.
   - normal? top 2–3 experts.
   - high-risk? add safety/evidence/copyright gate.
   - audit/refactor? broad/full read.
4. Seed by keywords or task signature. Find the first matching nodes; do **not** traverse the whole skill graph by default.
5. Read only selected seed modules first.
6. Expand point-to-point along graph edges:
   - semantic neighbor;
   - prerequisite/background node;
   - downstream output node;
   - safety/evidence/red-flag node;
   - source-anchor node.
7. Run the missed-case sweep.
8. If the sweep finds gaps, expand deliberately:
   - one more expert;
   - `GRAPH.md` for neighbor/return relations;
   - `CACHE.md` for prior gotchas;
   - source map/private substrate if legally needed;
   - full reading if the task demands whole-system assurance.
9. Produce the deliverable.
10. Write a route log for serious runs.

## 3. When to stay sparse

Stay sparse when:

- the question targets one clearly routed capability;
- `SKILL.md` and one expert are sufficient;
- the answer is low-risk and does not require exact source quotation;
- no anti-trigger or neighbor conflict fires;
- the user asks for operational next steps, not exhaustive audit.

Examples:

- “How do I turn a scanned PDF into source substrate?” → `reference/scanned-pdf-recipe.md`.
- “How should I split chapters into agent-native modules?” → `reference/outline-design.md` + sparse methodology.
- “What are the copyright boundaries?” → `reference/copyright-discipline.md`.

## 4. When to expand

Expand when:

- selected modules disagree;
- source map is missing;
- answer would make a medical/nutrition/legal/finance claim;
- user asks for submission, publication, or public release;
- the task spans multiple routed experts;
- the route plan has low confidence;
- missed-case sweep finds a neighbor skill or anti-trigger.

Expansion is staged: add the next most relevant module before opening everything.

## 5. When full reading is correct

Full or broad reading is correct when the task is:

- audit: “does this repo really implement sparse calling?”
- migration: “upgrade old skill to sparse methodology.”
- refactor: “rename/split/reorganize the whole skill.”
- quality investigation: “find stale, contradictory, or overbroad rules.”
- release review: “is this safe to publish?”
- benchmark: “compare sparse plan against full coverage.”

Full reading must end with compression. Do not leave the next invocation needing full reading again for the same reason.

## 6. Keyword → graph expansion pattern

For a domain skill such as nutrition, use this pattern:

```text
keyword hit → seed node → one-hop neighbors → safety/evidence gates → answer or expand → route log
```

Example: a childhood-obesity question should seed `childhood_obesity / BMI / family meal pattern`, then expand point-to-point to pediatric safety, stigma-free language, referral boundary, and guideline source anchors. It should not traverse every nutrition chapter. See `assets/sparse-nutrition-example.md`.

The graph expansion is for coverage without brute force: each opened node needs a reason. If no edge explains why a file is opened, skip it until the sweep demands it.

## 7. Missed-case sweep

Before final answer, check:

- copyright and source boundary;
- privacy/secrets/local paths;
- anti-trigger match;
- adjacent skill better suited;
- high-risk domain gate;
- missing evidence / stale source;
- overbroad promise;
- whether full reading was actually needed.

## 8. Return-to-cache ritual

For every serious run, append a route log using `assets/route-log-template.md` or JSON fields from `ROUTING.yaml`:

- task summary;
- mode used;
- files read;
- files skipped;
- why sparse was enough or why full reading was needed;
- missed-case hits;
- output artifacts;
- proposed updates to `ROUTING.yaml`, `GRAPH.md`, `CACHE.md`, evals, or RUNBOOK.

If the same expansion happens twice, promote it into routing or cache.

## 9. Acceptance gate

A run is complete only if you can state:

1. why these modules were read;
2. why other modules were skipped or why full reading was justified;
3. what risk sweep was performed;
4. what should be easier next time.
