# Sparse Distillation Methodology

This reference module grafts Runyuan Wang's sparse-distillation methodology onto the original book-to-skill workflow. Use it after source triage / OCR when designing the target skill tree, or when upgrading an existing distilled skill that has become too linear, too large, or too expensive to invoke.

## What changes from ordinary book-to-skill distillation

The original workflow answered: **How do we rewrite a source into an agent-native skill?**

The sparse overlay adds: **How do we make the resulting skill cheap, routed, cross-linked, miss-case-aware, and able to improve after each invocation?**

The target is no longer just `SKILL.md + reference/`. The target is a small skill graph:

```text
SKILL.md stable router
  ├─ ROUTING.yaml       # trigger, anti-trigger, neighbors, budgets, sweep hints
  ├─ GRAPH.md           # upstream/downstream/adjacent/safety/return relations
  ├─ CACHE.md           # stable prefix, variable suffix, update policy
  ├─ reference/*        # routed experts and deeper modules
  ├─ assets/*           # eval cases, output templates, schemas
  └─ scripts/*          # deterministic helpers
```

## Ten-step sparse distillation

### 1. Set the boundary

Ask before any extraction:

1. Is the source legally readable?
2. Is the goal operational learning/reuse rather than copying the source?
3. Is the output for humans, for agents, or both?
4. Does the source touch medical, nutrition, legal, finance, or other high-risk decisions?
5. What private paths, chats, customer data, secrets, or unpublished material must be stripped?

If copyright or privacy is unstable, keep the result as private notes/knowledge. Do not publish it as a reusable skill.

### 2. Build a source map, not a running summary

Create a table such as:

| Unit | Source location | Theme | Distillation role | Risk | Public-skill eligibility |
|---|---|---|---|---|---|
| Ch1 | pages 1–20 | concepts | shared core | low | abstracted rewrite OK |
| Ch4 | pages 80–110 | cases | worked pattern | medium | anonymize / abstract only |
| Appendix | appendix A | schema | asset/script | low | rewrite as tool |

The source map is navigation and evidence control. It is not a place to copy the source.

### 3. Extract the shared core

The shared core should be short and stable: definitions, red lines, output contract, source/evidence boundaries, and the universal missed-case sweep. Aim for 200–800 tokens when possible.

### 4. Extract routed experts

Do not mechanically mirror chapters. Split by tasks an agent actually routes to:

```text
intake-triage-expert
risk-red-flag-expert
evidence-verification-expert
report-writing-expert
publishing-or-formatting-expert
```

Each expert needs:

```yaml
trigger_terms:
anti_triggers:
budget_default:
minimum_workflow:
load_more_if:
missed_case_items:
```

### 5. Design sparse-first activation

The default runtime path is:

```text
user task → shared core → route candidates → top-k experts → main workflow → escalate if needed
```

Sparse-first does **not** mean never reading everything. It means start from the smallest sufficient set, then expand according to the task: audit, migration, refactor, safety review, quality investigation, or failed acceptance checks may require broad or full reading. The skill should make both paths explicit: cheap partial use for ordinary calls, deliberate full coverage when the need is real.

### 6. Add the missed-case sweep

Sparse routing creates the risk of omission. After the main route, run a low-budget sweep:

- Did a neighbor skill fit better?
- Did an anti-trigger fire?
- Are there high-risk populations, contraindications, legal/medical/financial red flags, or privacy issues?
- Is evidence missing or stale?
- Is the output overclaiming?
- Does the answer need human/professional review?

### 7. Assign budgets

| Tier | Use | Policy |
|---|---|---|
| stable prefix | every invocation | short, rarely changed |
| routed expert | normal work | load top-k only |
| deep reference | complex/high-risk work | load on demand |
| full substrate | audit/rebuild only | private, never default runtime |

### 8. Make the layout cache-friendly

Stable files change rarely (`SKILL.md`, `ROUTING.yaml`, red lines). Variable files change after learning (`CACHE.md`, eval cases, gotchas, route logs). Avoid mixing them.

### 9. Build evals and route logs

Minimum eval set:

- positive trigger examples;
- anti-trigger examples;
- neighbor/misroute examples;
- high-risk missed-case examples;
- budget tests;
- failure cases where the right answer is to refuse, defer, or ask for more information.

A route log should record: task signature, selected experts, files loaded, missed-case findings, output type, and update proposals.

### 10. Return to the graph

After each serious run, ask what should become shorter and more reusable:

- a new trigger term;
- an anti-trigger;
- a neighbor link;
- a checklist item;
- an eval case;
- a gotcha;
- a script;
- a reference split or merge.

Do not mutate public skills automatically. Record proposals and merge them through review.

## Upgrade checklist for an existing distilled skill

1. Read the existing `SKILL.md` and list its current routes.
2. Identify which sections are shared core and which are routed experts.
3. Move long explanatory material out of `SKILL.md` into `reference/`.
4. Add `ROUTING.yaml` with triggers, anti-triggers, neighbors, budget tiers, and sweep fields.
5. Add `GRAPH.md` to show upstream/downstream/neighbor/safety/return relations.
6. Add `CACHE.md` to separate stable prefix, variable suffix, and update policy.
7. Add eval cases for route correctness and missed-case behavior.
8. Run validation and smoke-test at least one small task, one cross-topic task, one anti-trigger, and one high-risk sweep.

## Output contract

A sparse-distilled skill should ship with:

- a thin, stable `SKILL.md` router;
- a source map or instructions for where the private source map lives;
- routed reference modules;
- explicit red lines and missed-case sweep;
- machine-readable routing hints;
- eval cases;
- validation commands;
- a return-to-cache procedure.
