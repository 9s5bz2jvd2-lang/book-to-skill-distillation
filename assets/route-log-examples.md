# Route Log Examples

These examples show how to keep route logs short. They record decisions that make the next invocation cheaper; they do not preserve long reasoning or source text.

## Example A — small skill edit, no heavy routing

```yaml
task_signature: add anti-trigger terms to a sparse skill
mode: quick
files_read: [SKILL.md, ROUTING.yaml]
files_skipped:
  GRAPH.md: no neighbor logic changed
  reference/*: no deep method needed
selected_experts: []
missed_case_sweep: [anti_trigger_check, output_contract_check]
full_reading: false
return_to_cache:
  ROUTING.yaml: added three anti-trigger phrases
outcome: ok
```

## Example B — nutrition book skill invocation

```yaml
task_signature: child BMI above reference, parent asks diet adjustment
mode: high_risk_sparse
seed_nodes: [childhood_obesity, BMI, family_meal_pattern]
selected_experts: [childhood_obesity, family_intervention]
point_to_point_edges:
  childhood_obesity -> pediatric_safety_gate: special population
  BMI -> referral_boundary: risk classification
  family_meal_pattern -> stigma_free_language: counseling risk
  diet_adjustment -> guideline_source_anchor: evidence requirement
sweep_items_checked:
  - eating_disorder_or_weight_shame
  - medical_referral_red_flags
  - guideline_date_and_authority
full_reading: false
return_to_cache:
  GRAPH.md: if repeated, add BMI -> eating_disorder_language edge
outcome: bounded parent-facing guidance
```

## Example C — release audit, full reading justified

```yaml
task_signature: verify repo implements sparse invocation before public push
mode: audit
files_read: [README.md, SKILL.md, RUNBOOK.md, ROUTING.yaml, GRAPH.md, CACHE.md, assets/eval-cases.md, scripts/route_plan.py]
full_reading: true
why_full_reading: public release review and structural consistency check
findings:
  - SKILL.md version lagged manifest
  - database source-map path missing
  - eval lacked large-database case
return_to_cache:
  SKILL.md: version and router updated
  reference/source-map-and-database-distillation.md: added
  assets/eval-cases.md: added database cases
  scripts/quality_check.py: added required file checks
outcome: ready after validation
```

## Example D — same-domain multi-book source-pack route

```yaml
task_signature: compare fiber recommendations across nutrition textbooks and guidelines
mode: multi_book_sparse
seed_nodes: [dietary_fiber, adult_recommendation, tolerance_boundary]
source_packs_selected: [textbook_A_2022, guideline_B_2024]
source_packs_skipped:
  textbook_C_2010: older edition; only open if conflict persists
source_anchor_units:
  - textbook_A_2022:chapter_8:fiber
  - guideline_B_2024:recommendation_3.2
point_to_point_edges:
  dietary_fiber -> guideline_source_anchor: evidence requirement
  guideline_B_2024 -> textbook_C_2010: updates_or_supersedes
conflict_log_entries:
  - possible difference between textbook explanatory range and guideline population-specific recommendation
sweep_items_checked:
  - source_anchor_gate
  - edition_or_version_gate
  - medical_or_nutrition_scope
full_reading: false
return_to_cache:
  GRAPH.md: add dietary_fiber -> tolerance_boundary edge if repeated
  ROUTING.yaml: add fiber/recommendation as multi-book seed signature
outcome: bounded answer with source-specific distinctions
```
