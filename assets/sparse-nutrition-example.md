# Worked Example — nutrition skill sparse invocation

This example captures the intended mechanism for a nutrition-domain skill distilled with this workflow.

Scenario:

> A nutrition agent has a skill distilled from several nutrition books/guidelines. A user asks about a topic such as childhood obesity, protein needs, gestational diabetes nutrition, or dietary fiber. The agent should not traverse every book-derived module by default. It should seed by keywords, expand along the knowledge graph point-to-point, and run a missed-case sweep to avoid omissions.

## Desired invocation pattern

```text
user keywords
  → seed nodes in skill index / ROUTING / source map
  → top matching expert nodes
  → one-hop graph neighbors
  → safety/evidence/red-flag gates
  → answer or expand further
  → route log and cache update
```

This is **not** global traversal. It is targeted expansion.

## Example 1 — childhood obesity

Input:

> 孩子 BMI 超标，家长问怎么调整饮食。

Sparse seed hits:

- `childhood_obesity`
- `BMI`
- `family_meal_pattern`
- `screen_time_or_activity`

Initial files/nodes:

- shared nutrition core;
- childhood-obesity expert;
- family intervention / behavior expert.

Point-to-point expansion:

| From | Edge reason | To |
|---|---|---|
| childhood_obesity | special population | pediatric safety gate |
| BMI | risk classification | referral / clinical boundary |
| family_meal_pattern | intervention context | stigma-free counseling language |
| diet adjustment | evidence needed | guideline/source anchor |

Missed-case sweep:

- child growth and development;
- eating-disorder / weight-shame language;
- medical referral red flags;
- caregiver role and home food environment;
- evidence source and date;
- avoid self-diagnosis or treatment promises.

Expansion rule:

- Do not traverse the whole nutrition library.
- Expand to adjacent nodes only when keyword seed or sweep requires it.
- If the question becomes clinical, expand to evidence/source anchors and professional boundary.

## Example 2 — dietary fiber

Input:

> 高纤维饮食是不是适合所有人？

Sparse seed hits:

- `dietary_fiber`
- `gastrointestinal_tolerance`
- `chronic_disease_prevention`

Point-to-point expansion:

| From | Edge reason | To |
|---|---|---|
| dietary_fiber | contraindication check | GI disease / post-surgery caution |
| dietary_fiber | population check | children / elderly / pregnancy if mentioned |
| chronic_disease_prevention | evidence boundary | guideline/source anchor |
| increase fiber | behavior advice | hydration / gradual increase |

Missed-case sweep:

- absolute claim check: not “everyone must eat high fiber”; 
- condition-specific caution;
- medication/supplement interaction if mentioned;
- evidence freshness.

## What to test

A good sparse nutrition skill should:

1. find the right seed node by keyword;
2. avoid loading all book chapters;
3. expand one hop to relevant neighboring risks;
4. run a safety/evidence sweep;
5. know when to escalate to full source review;
6. log any missing route so future calls are cheaper.

Failure modes:

- linear traversal of all nutrition modules;
- answer from one keyword node without neighbor safety sweep;
- generic medical advice without source boundary;
- no route log after discovering a missing node;
- treating sparse mode as a ban on full review when clinical safety requires full evidence checking.
