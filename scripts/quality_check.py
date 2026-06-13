#!/usr/bin/env python3
"""Lightweight release checks for the book-to-skill-distillation repo."""
from __future__ import annotations

import pathlib
import sys

root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '.')
errs: list[str] = []

required = [
    'SKILL.md',
    'RUNBOOK.md',
    'ROUTING.yaml',
    'GRAPH.md',
    'CACHE.md',
    'skill-manifest.yaml',
    'assets/eval-cases.md',
    'assets/route-log-template.md',
    'assets/route-log-examples.md',
    'reference/sparse-distillation-methodology.md',
    'reference/source-map-and-database-distillation.md',
    'reference/multi-book-domain-distillation.md',
    'scripts/route_plan.py',
]

for rel in required:
    if not (root / rel).exists():
        errs.append(f'missing required file: {rel}')

for p in root.rglob('*.md'):
    txt = p.read_text(encoding='utf-8', errors='ignore')
    if '[PLACEHOLDER]' in txt:
        errs.append(f'placeholder: {p.relative_to(root)}')
    if p.name == 'SKILL.md' and len(txt) > 12000:
        errs.append(f'SKILL.md too long for a thin router: {len(txt)} chars')

skill = root / 'SKILL.md'
if skill.exists():
    txt = skill.read_text(encoding='utf-8', errors='ignore')
    for needle in ['ROUTING.yaml', 'GRAPH.md', 'CACHE.md', 'missed-case', 'source map', 'multi-book', 'source pack']:
        if needle not in txt:
            errs.append(f'SKILL.md missing expected sparse/source-map term: {needle}')

multibook = root / 'reference/multi-book-domain-distillation.md'
if multibook.exists():
    txt = multibook.read_text(encoding='utf-8', errors='ignore')
    for needle in ['source_pack_id', 'source anchor', 'conflict log', 'domain parent', 'Sheng-Wanwu']:
        if needle not in txt:
            errs.append(f'multi-book reference missing required term: {needle}')

routing = root / 'ROUTING.yaml'
if routing.exists():
    txt = routing.read_text(encoding='utf-8', errors='ignore')
    for needle in ['source_pack_catalog', 'conflict_or_edition_drift_check', 'multi_book']:
        if needle not in txt:
            errs.append(f'ROUTING.yaml missing multi-book gate: {needle}')

print('\n'.join(errs) if errs else 'quality_check: ok')
sys.exit(1 if errs else 0)
