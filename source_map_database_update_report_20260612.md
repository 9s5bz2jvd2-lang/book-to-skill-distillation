# Source-map / database distillation update report

Date: 2026-06-12
Repo: `https://github.com/9s5bz2jvd2-lang/book-to-skill-distillation`

## Why this update

After comparing the earlier Anthropic Skills discussion with the current sparse book-to-skill workflow, Runyuan clarified the default future use case: when distilling books or large databases into skills, use the sparse graph method as the construction method, not as an optional afterthought.

## What changed

- Upgraded visible version references to `0.5.0`.
- Added `reference/source-map-and-database-distillation.md`:
  - source/schema map fields;
  - supported source shapes: books, multi-book libraries, guideline collections, databases, OCR corpora, wikis;
  - database-specific rules for schema, units, provenance, missing values, versioning, and synthetic evals;
  - keyword/field signature -> seed node -> one-hop graph expansion -> safety/evidence gate -> route log.
- Added `assets/route-log-examples.md` with compact precedents for:
  - small skill edit;
  - high-risk nutrition invocation;
  - release audit requiring full reading.
- Updated `SKILL.md`, `README.md`, `RUNBOOK.md`, `ROUTING.yaml`, `GRAPH.md`, `CACHE.md`, `assets/eval-cases.md`, `skill-manifest.yaml`, and `scripts/route_plan.py` to treat books, guideline libraries, and databases as first-class distillation sources.
- Strengthened `scripts/quality_check.py` so release checks require the sparse/source-map surfaces.

## Final rule

> Distill large sources by building source maps and routed experts. Invoke sparsely by keyword/field/task signatures. Expand point-to-point through graph edges. Run missed-case sweeps. Allow full reading for audit/migration/release/high-risk review. Return every serious run to routing, graph, cache, evals, or route-log examples.

## Validation to run before push

```bash
python3 scripts/quality_check.py .
python3 scripts/route_plan.py --task 'distill a large food composition database and nutrition guideline library into a skill without traversing the whole database'
python3 scripts/route_plan.py --task 'audit source map coverage before publishing the skill' --mode audit --json
python3 - <<'PY'
import yaml
from pathlib import Path
for fn in ['ROUTING.yaml', 'skill-manifest.yaml']:
    yaml.safe_load(Path(fn).read_text())
print('yaml ok')
PY
```
