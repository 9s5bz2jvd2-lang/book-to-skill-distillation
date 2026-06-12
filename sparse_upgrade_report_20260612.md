# Sparse-methodology upgrade report — book-to-skill-distillation

Date: 2026-06-12
Repo: `https://github.com/9s5bz2jvd2-lang/book-to-skill-distillation`
Local path: `.lingtai/mimo-2-5-pro/projects/repo_attribution_fix_20260605/book-to-skill-distillation`
Status: local changes only; not committed or pushed.

## Goal

Use the methodology from `sparse-book-to-skill-distillation` to upgrade the older `book-to-skill-distillation` skill, without losing the older OCR / daemon / copyright / publishing workflow.

After Runyuan's refinement, the core rule is now:

> Start sparse by keyword/task seed nodes; expand point-to-point along the skill graph; do not traverse everything by default; allow broad/full reading when the task requires audit, migration, refactor, safety/evidence review, release review, or failed acceptance checks; after broad/full reading, compress findings back into routing/cache/evals/logs.

## What changed locally

### Updated

- `SKILL.md`
  - upgraded from `version: 0.3.0` to `version: 0.4.0`;
  - changed the entry from a linear book-to-skill router into a sparse-enabled router;
  - added execution routes for `RUNBOOK.md`, `skill-manifest.yaml`, and `scripts/route_plan.py`;
  - changed the sparse rule from "do not load everything" to demand-sensitive: sparse by default, broad/full reading when justified;
  - added graph expansion language: keyword/task seed → point-to-point expansion → missed-case sweep → return-to-cache;
  - preserved older routes: source triage, scanned PDF OCR, TOC recovery, outline design, daemon orchestration, copyright discipline, validation, publishing.

- `README.md`
  - documented `RUNBOOK.md`, `skill-manifest.yaml`, `scripts/route_plan.py`, `assets/route-log-template.md`, and `assets/sparse-nutrition-example.md`;
  - added route-plan invocation examples;
  - retained the older OCR/daemon/publishing workflow.

- `ROUTING.yaml`
  - added `seed_strategy: keyword/task signature -> seed nodes -> point-to-point graph expansion -> missed-case sweep`;
  - made full reading an explicit escalation path for audit/migration/refactor/safety/release/quality work;
  - added rule to compress broad/full reading back into routing/graph/cache/evals/route logs.

- `GRAPH.md`
  - added a section on keyword seed nodes and point-to-point expansion;
  - added edge types: semantic neighbor, prerequisite, downstream action, safety/evidence, contradiction check, source anchor;
  - included the nutrition example: child BMI / childhood obesity should expand to pediatric safety, stigma-free language, referral boundary, and guideline anchors rather than traversing all nutrition chapters.

- `reference/sparse-distillation-methodology.md`
  - changed runtime path to `user task -> shared core -> route candidates -> top-k experts -> main workflow -> escalate if needed`;
  - clarified that sparse-first is not a ban on full reading.

- `assets/eval-cases.md`
  - added a nutrition-domain eval for keyword sparse search, non-traversal, graph point-to-point expansion, and missed-case sweep.

### Added

- `RUNBOOK.md` — demand-sensitive execution manual: reading modes, when to stay sparse, when to expand, when full reading is correct, missed-case sweep, return-to-cache ritual.
- `skill-manifest.yaml` — machine-readable invocation surface: modes, modules, triggers, escalation rules, return surfaces.
- `scripts/route_plan.py` — dependency-free helper that turns a task into a reading plan; supports normal sparse plans and audit/full-reading plans.
- `assets/route-log-template.md` — after-action route log for recording files read/skipped, graph expansion, missed-case sweep, and cache proposals.
- `assets/sparse-nutrition-example.md` — worked example of nutrition-domain invocation: keyword seed nodes, point-to-point graph expansion, safety/evidence sweep.
- Earlier sparse overlay additions retained: `CACHE.md`, `RULES.md`, `assets/output-template.md`, `docs/self-evolution-loop.md`, `docs/structure-diagram.md`, `reference/sparse-distillation-methodology.md`.

## Validation run

Commands run locally:

```bash
cd projects/repo_attribution_fix_20260605/book-to-skill-distillation
chmod +x scripts/route_plan.py
python3 scripts/quality_check.py .
python3 scripts/route_plan.py --task '若营养学用此 skill 蒸馏，调用时根据关键词稀疏式寻找书籍内容，非遍历，网状点对点扩展，以求无遗漏'
python3 scripts/route_plan.py --task 'audit whether this repo really implements sparse invocation' --mode audit --json
python3 - <<'PY'
import yaml, json
from pathlib import Path
for fn in ['ROUTING.yaml','skill-manifest.yaml']:
    yaml.safe_load(Path(fn).read_text())
print('ok')
PY
```

Results:

- `quality_check: ok`
- `ROUTING.yaml` parses successfully.
- `skill-manifest.yaml` parses successfully.
- Nutrition sparse invocation route plan now selects:
  - `SKILL.md`
  - `ROUTING.yaml`
  - `RUNBOOK.md`
  - `reference/agent-native-rewrite.md`
  - `reference/sparse-distillation-methodology.md`
  - `reference/copyright-discipline.md`
  - `reference/validation-checklist.md`
  - `GRAPH.md`
  - `assets/sparse-nutrition-example.md`
- The same nutrition route plan does **not** full-read by default; it records graph expansion and high-risk safety/evidence sweep.
- Audit-mode route plan returns `should_full_read: true`, proving full reading remains available when justified.

## Current git state

Changed / added locally, not yet committed or pushed.

```text
 M README.md
 M SKILL.md
?? CACHE.md
?? GRAPH.md
?? ROUTING.yaml
?? RULES.md
?? RUNBOOK.md
?? assets/eval-cases.md
?? assets/output-template.md
?? assets/route-log-template.md
?? assets/sparse-nutrition-example.md
?? docs/
?? reference/sparse-distillation-methodology.md
?? scripts/route_plan.py
?? skill-manifest.yaml
?? sparse_upgrade_report_20260612.md
```

## Recommended next step

If Runyuan confirms, commit and push under account `9s5bz2jvd2-lang`:

```bash
gh api user --jq .login   # must be 9s5bz2jvd2-lang before pushing

git add SKILL.md README.md RUNBOOK.md skill-manifest.yaml ROUTING.yaml GRAPH.md CACHE.md RULES.md \
  assets/eval-cases.md assets/output-template.md assets/route-log-template.md assets/sparse-nutrition-example.md \
  docs/ reference/sparse-distillation-methodology.md scripts/route_plan.py sparse_upgrade_report_20260612.md

git commit -m "Upgrade book-to-skill distillation with sparse routing"
git push origin main
```

Do not push if the active GitHub account cannot be verified as `9s5bz2jvd2-lang`.
