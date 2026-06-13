# Multi-Book Same-Domain Distillation

Sheng-Wanwu note: this module is the source-pack / unified-graph foundation layer for 生万物 (Sheng-Wanwu) harnesses; it does not itself generate or validate hypotheses.

Use this module when the goal is to distill **multiple books or source systems in the same domain** into one callable agent skill or skill family. This is not a license to merge all books into one giant `SKILL.md`. The correct shape is a **domain parent router** over a set of **source packs**, with sparse routing, source anchors, conflict handling, and return-to-cache.

## Core rule

> Many books may share one domain skill only if each source keeps its own identity. The parent skill routes across sources; it does not erase source boundaries.

A same-domain multi-book skill should let an agent answer: which source(s) were consulted, why those sources were selected, whether sources agree or conflict, and which evidence/source gate ran.

## Vocabulary

| Term | Meaning |
|---|---|
| domain parent skill | The public/callable skill entry point for the field. It holds shared rules, safety/evidence gates, and routing logic. |
| source pack | One book, guideline, database, course, or corpus distilled into a source map plus optional routed experts. |
| source unit | A stable unit inside a source pack: chapter, section, table, formula, recommendation, field, or page range. |
| unified graph index | A lightweight graph that links source units across packs by topic, prerequisite, contradiction, analogy, update lineage, or safety gate. |
| source anchor | The source ID + location + version/edition/date needed to verify a claim. |
| conflict log | A compact record of cross-source disagreement, edition drift, terminology mismatch, or scope boundary. |

## Recommended architecture

```text
multi-book domain request
  -> domain parent skill
  -> source inventory and legal/privacy boundary
  -> per-source source packs
      book_A/source_map
      book_B/source_map
      guideline_C/source_map
  -> unified graph index
  -> shared domain core
  -> top-k source-aware routed experts
  -> source/conflict/safety gates
  -> route log + conflict log + cache update
```

Do not make the parent skill a full anthology. The parent contains only:

- trigger/anti-trigger terms;
- shared domain red lines;
- source-pack catalog;
- routing policy;
- evidence/conflict gates;
- stable cross-source signatures;
- route-log and conflict-log templates.

Long source details stay in source packs, private substrate, or on-demand references.

## Construction flow

1. **Inventory sources before merging.** Record each source as a separate `source_id` with title, edition/version/date, license/publishability, domain tags, risk tags, and private substrate path.
2. **Build per-source maps.** For each book/source, map source units to topic signatures, roles, risk tags, publishability, and neighbor edges.
3. **Build a shared domain core.** Put only stable domain-wide rules here: safety, evidence hierarchy, terminology conventions, output contract, and anti-hallucination rules.
4. **Create a source-pack catalog.** The catalog says which source is best for definitions, methods, formulas, examples, recommendations, current guidance, historical context, or edge cases.
5. **Add cross-source graph edges.** Use explicit edge types; do not rely on semantic blending.
6. **Route top-k sources, not all sources.** A task first hits signatures; then the router selects the smallest sufficient source packs and experts.
7. **Run conflict/source gates.** If multiple sources are consulted, mark agreement, conflict, edition drift, and scope differences.
8. **Return to cache.** Repeated cross-source paths become shorter signatures, graph edges, eval cases, or conflict-log examples.

## Multi-book source map fields

Extend the minimum source map with fields that keep sources separable:

```yaml
source_pack_id: stable identifier for one book/source
domain_id: stable identifier for the domain parent skill
source_id: edition/version-specific source identifier
source_title: human-readable title
source_kind: textbook | guideline | database | paper_collection | course | manual | corpus
version_or_edition: edition, year, database version, guideline date
license_status: copyrighted | open | licensed | unknown
publishability: public_abstract | private_only | needs_license_review
unit_id: source-local stable unit id
location: chapter/page/section/table/field/url/path
topic_signature: short trigger words or controlled concepts
role: shared_core | routed_expert | safety_gate | source_anchor | heavy_reference | eval_source
risk_tags: [copyright, medical, stale, unit_conversion, OCR_low_confidence, conflicting_guidance]
source_strength: primary | authoritative | textbook_consensus | illustrative | historical | superseded
cross_source_edges:
  agrees_with: []
  conflicts_with: []
  updates_or_supersedes: []
  same_concept_as: []
  terminology_variant_of: []
  prerequisite_for: []
conflict_status: none | possible | confirmed | resolved | needs_human_review
refresh_policy: static | check_before_publication | check_every_run
```

## Sparse invocation across many books

Use this path:

```text
task signature
  -> seed concepts / fields / recommendations
  -> candidate source packs by catalog role
  -> top-k source units (default 2, max 5)
  -> one-hop cross-source graph expansion
  -> source/conflict/safety/evidence gates
  -> answer or deliberate expansion
  -> route log + conflict log
```

Default behavior is **not** to read every book. Full multi-source scan is justified only for first inventory, audit, release review, source coverage proof, conflict resolution, or high-risk evidence review.

## Conflict gate

When two or more source packs are consulted, run a conflict gate:

1. Do the sources address the same population, condition, timeframe, and definition?
2. Is one source newer, more authoritative, or narrower in scope?
3. Are units/terms/measurement systems equivalent?
4. Is there a direct contradiction, or only a context difference?
5. Does the output need to say “Source A says X, Source B says Y” rather than synthesize?
6. Should a human or domain expert resolve the conflict?

Never collapse conflicting sources into a single unsourced sentence.

## Output contract

A multi-book distilled answer or module should identify:

- selected source packs;
- source anchors used;
- skipped source packs and why they were not needed;
- whether sources agree, conflict, or differ by context;
- any safety/evidence/source-boundary gate that ran;
- what should be cached or logged for next time.

## Anti-patterns

- Giant `SKILL.md` containing summaries of every book.
- Removing edition/version/source identity after merging.
- “Consensus” statements without source anchors.
- Treating older and newer editions as interchangeable.
- Reading all books for every query.
- Letting route logs store long copyrighted excerpts or private source text.
- Using cross-source analogy as evidence without a verification gate.

## Acceptance gate

A same-domain multi-book skill is acceptable only if:

1. every source pack has a stable `source_pack_id` and version/edition;
2. every strong claim can point to at least one source anchor;
3. conflicts are logged instead of smoothed over;
4. routing can select top-k source packs without full traversal;
5. high-risk domains include safety/evidence gates;
6. route logs record cross-source hits compactly;
7. the next invocation can be sparser because of cache/graph updates.
