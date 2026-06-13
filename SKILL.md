---
name: book-to-skill-distillation
description: |
  End-to-end workflow for rewriting a book, long PDF, EPUB, manual, course, guideline library, same-domain multi-book source pack, large database, or methodology into an agent-native LingTai / Agent Skill structure. Use when the task is not a summary, but a reusable skill/knowledge system: source triage, scanned/image-only PDF OCR, source/schema maps, shared-core extraction, top-k routed experts, sparse activation, missed-case sweep, budgeted references, daemon fan-out, copyright-safe transformation, validation, cyclic return-to-cache, and publishing.
version: 0.5.1
tags: [workflow, meta-skill, distillation, ocr, daemons, progressive-disclosure, sparse-routing, missed-case-sweep, agent-native-rewrite, multi-book, source-pack, sheng-wanwu]
---

# book-to-skill-distillation

Convert a linear human text into a branching **agent-native** skill. Distillation here is not a summary and not a compressed copy: it is a rewrite into the forms an agent can call while working — routers, decision trees, checklists, schemas, prompts, scripts, validation gates, worked examples, and reference modules.

Version 0.5.1 promotes same-domain multi-book distillation to a first-class shape on top of the v0.5 sparse overlay for large books, guideline collections, and databases: **shared core + top-k routed experts + missed-case sweep + budgeted references + cache-friendly layout + cyclic return-to-cache feedback loop**. The old OCR / daemon / copyright / publishing workflow remains; the new rule is that a distilled skill should make partial, routed reading possible by default, while still allowing full reading/audit when the task genuinely requires it. For large sources, a source map or schema map is the bridge between raw material and routed experts; for many books in one domain, a domain parent skill routes over separate source packs rather than erasing source identity.

Keep `SKILL.md` as the stable router; use `reference/source-map-and-database-distillation.md` for book/database source maps; use `reference/multi-book-domain-distillation.md` for same-domain source packs; use `RUNBOOK.md` for execution discipline, `skill-manifest.yaml` and `ROUTING.yaml` for machine-readable routing, `scripts/route_plan.py` for first-pass reading plans, `GRAPH.md` for point-to-point expansion, `CACHE.md` for return-to-cache, `reference/` for depth, `assets/` for templates/evals, and project-private extraction substrate under `work/book-distill/<slug>/`.

## Core model

| Layer | Purpose | Artifact examples |
|---|---|---|
| Source substrate | legally and privately inspect the source | `work/book-distill/<slug>/`, OCR, TOC map, source/schema map, source-pack catalog |
| Shared core | tiny always-on kernel for this skill | trigger, exclusions, red lines, output contract, safety sweep |
| Routed experts | task-shaped modules, not chapter-shaped summaries | `reference/<expert>.md`, decision tables, checklists, scripts |
| Sparse activation | keyword/task seed, then load the smallest sufficient expert set | `ROUTING.yaml`, `skill-manifest.yaml`, `scripts/route_plan.py` |
| Graph expansion + missed-case sweep | point-to-point neighbor expansion to avoid omissions without brute-force traversal | `GRAPH.md`, safety gates, neighbor checks, anti-triggers, eval cases |
| Return-to-cache | invocation lessons flow back into shorter reusable structures | `CACHE.md`, `GRAPH.md`, route log, validation updates |

One-line test: **network gives the skill reachability; the cycle gives it continuity. Branch out, then return to a usable state.**

## Lifecycle

`Set boundary → Scout source → Recover structure → Extract/OCR substrate → Build source map → Design shared core → Split into routed experts → Rewrite in parallel → Reconcile → Missed-case sweep → Return to cache/graph → Validate & publish`

## Router

| Situation | Read next |
|---|---|
| understand the core transformation | `reference/agent-native-rewrite.md` |
| run a demand-sensitive sparse invocation | `RUNBOOK.md`, `scripts/route_plan.py`, `skill-manifest.yaml`, `ROUTING.yaml` |
| use the sparse-distillation overlay | `reference/sparse-distillation-methodology.md`, `ROUTING.yaml` |
| keyword seed + point-to-point graph expansion | `GRAPH.md`, `assets/sparse-nutrition-example.md` |
| classify PDF/EPUB/database/source | `reference/source-triage.md` |
| scanned PDF / blank pdftotext / full OCR | `reference/scanned-pdf-recipe.md` |
| recover table of contents | `reference/toc-recovery.md` |
| map book/database source units to skill tree | `reference/source-map-and-database-distillation.md`, `reference/outline-design.md` |
| distill many books in one domain | `reference/multi-book-domain-distillation.md`, `reference/source-map-and-database-distillation.md`, `GRAPH.md`, `CACHE.md` |
| add cyclic return / low-power / trajectory discipline | `reference/cyclic-low-power-distillation.md`, `CACHE.md` |
| use daemons in parallel | `reference/daemon-orchestration.md`, `assets/daemon-task-template.md` |
| copyright concern | `reference/copyright-discipline.md` |
| validate/publish | `reference/validation-checklist.md`, `reference/publishing.md`, `assets/eval-cases.md`, `assets/route-log-examples.md` |
| calibrate on this run | `reference/worked-example-legal-dd.md` |
| understand graph / cache / evolution surfaces | `GRAPH.md`, `CACHE.md`, `docs/self-evolution-loop.md` |

## Quick start

1. **Set boundary first.** Confirm the source is legally readable, the goal is transformation not reproduction, and the output may be shared only if copyright/privacy permits.
2. For invocation or upgrade work, generate/read a route plan first: `python3 scripts/route_plan.py --task "<task>"`; if it recommends audit/full reading, broaden deliberately and record why.
3. Create `work/book-distill/<slug>/` and keep source-derived OCR/transcripts there, not inside the published skill.
4. Run `scripts/scout.sh <source.pdf> work/book-distill/<slug>` or equivalent inspection; decide whether the source has a text layer.
5. Recover the source structure: TOC, headings, page offsets, chapter boundaries, appendices, and repeated schemas.
6. Build a **source/schema map**: unit/table/field → source location → topic signature → role → risk → publishability → neighbor edges → refresh policy. If the task has multiple books in one domain, first build per-source **source packs**, then a domain parent router and unified graph index; do not blend sources into one anonymous summary.
7. Design the target skill before rewriting: trigger, exclusions, shared core, routed experts, assets, scripts, caveats, and validation plan.
8. Split by **agent-native units** (tasks/decisions/risks), not by mechanical chapters. Each unit should become a routed expert or reference module.
9. Fan out daemons: each daemon rewrites one topic or coherent topic group into operational structures, **not** into a chapter summary.
10. Parent reconciles, removes duplication, cross-links experts, labels evidence boundaries, and enforces copyright-safe abstraction.
11. Run a missed-case sweep: anti-triggers, adjacent skills, red flags, high-risk domain gates, missing evidence, and overbroad promises.
12. Return lessons to hub: update `ROUTING.yaml`, `GRAPH.md`, `CACHE.md`, eval cases, route-log examples, gotchas, and validation checklist if the run revealed new patterns.
13. Validate, refresh, and smoke-test realistic prompts before publishing.

## Sparse activation rule of thumb

| Task shape | Load budget |
|---|---|
| simple low-risk lookup inside the skill | `SKILL.md` + one routed expert |
| normal cross-topic distillation | shared core + top 2–3 experts |
| high-risk medical/nutrition/legal/finance source | main experts + safety/copyright/evidence gate |
| large integrated deliverable | staged batches; expand module coverage as needed |
| audit, migration, refactor, or quality investigation | deliberately read broadly or fully, then compress findings back into routes/cache |

Completeness comes from **source maps, missed-case sweeps, evals, and demand-sensitive escalation**. Sparse is the default economy mode, not a ban on full reading.

## Output test

A good distilled skill lets an agent answer: “What do I do next on this task?” without rereading the book. If the output mostly says what the book said in the same order, it is not yet agent-native. If the output requires loading every module for every task, it is not yet sparse-native.

## Red lines

Multi-book red line: many sources may share one domain skill only if source identity, edition/version, source anchors, and conflict status survive the merge. Never turn conflicting books into a single unsourced “consensus” sentence.


- Do not reproduce copyrighted text, tables, examples, or images beyond tiny necessary snippets.
- Do not put OCR substrate, private chats, customer data, secrets, or local-only paths into a public skill.
- Do not hide uncertainty: OCR errors, stale law, current API behavior, medical/nutrition claims, and financial/legal advice require evidence labels and refresh gates.
- Do not skip the missed-case sweep just because sparse activation saved tokens.
- Do not let daemon branches disappear: every branch returns a short record of goal, sources, outputs, uncertainty, and next action.

## Acceptance checks

Before calling a distillation complete, verify:

1. `SKILL.md` has a clear trigger, exclusions, router, red lines, output test, and acceptance gates.
2. The published skill contains transformed operational artifacts, not source-prose copies.
3. The source map and OCR/transcript substrate remain private or are legally publishable.
4. `ROUTING.yaml` identifies triggers, anti-triggers, neighbors, budget tiers, and missed-case sweep items.
5. `GRAPH.md` explains upstream inputs, downstream outputs, adjacent skills, safety gates, and return relationships.
6. `CACHE.md` separates stable prefix from variable suffix and says what gets updated after a run.
7. At least a small eval set covers positive triggers, anti-triggers, neighbor risks, budget behavior, and failure cases.
8. `scripts/quality_check.py .` and any runtime skill validator pass.

<!-- Maintainer update: Runyuan Wang (9s5bz2jvd2-lang). Sparse methodology graft: 2026-06-12. -->
