# Source Map and Database Distillation

Use this module when the source is not a single linear book but a textbook set, guideline collection, database export, table corpus, evidence library, wiki, or other large source system. The goal is not to copy the source into a skill. The goal is to build a **callable source map** and then distill only the operational routes an agent needs.

## Core rule

> A large source becomes a skill only after it has a source map. A source map is the bridge between raw material and routed experts.

The source map records where knowledge lives, what role it plays, what risk it carries, and whether it can be published. It is not a long summary and not a replacement for the source.

## Supported source shapes

| Source shape | First map | Typical experts | Extra risk gate |
|---|---|---|---|
| single book / textbook | chapter -> concept -> task role | routed chapter-to-task experts | copyright |
| multi-book library | source -> topic -> overlap/conflict | topic experts + source-anchor experts | conflict / edition drift |
| guideline collection | guideline -> recommendation -> population -> date | evidence and recommendation experts | freshness / authority |
| database / table corpus | table -> field -> entity -> unit -> provenance | query, normalization, interpretation experts | schema drift / unit errors |
| OCR corpus | page -> region -> confidence -> topic | OCR cleanup and source-anchor experts | OCR uncertainty |
| wiki / living docs | page -> owner -> update date -> dependency | route + refresh experts | staleness / unreviewed edits |

## Minimum source map fields

Use a table, YAML, JSON, SQLite index, or CSV. The format may vary, but the fields must be recoverable:

```yaml
unit_id: stable local identifier
source_id: book/database/guideline/table name
location: page/chapter/table/row/range/url/path
topic_signature: short trigger words or concepts
role: shared_core | routed_expert | safety_gate | source_anchor | heavy_reference | eval_source
risk_tags: [copyright, privacy, medical, stale, unit_conversion, OCR_low_confidence]
publishability: public_abstract | private_only | needs_license_review
neighbor_edges:
  prerequisite: []
  semantic_neighbor: []
  downstream_action: []
  safety_evidence: []
  contradiction_check: []
refresh_policy: static | check_before_publication | check_every_run
```

## Construction flow

```text
raw sources
  -> inventory and legal/privacy boundary
  -> source map / schema map
  -> shared core and safety gates
  -> seed-node signatures
  -> routed experts
  -> point-to-point graph edges
  -> evals and route-log examples
  -> validation / publication review
```

Do not start by writing expert prose. Start by mapping source units and their roles.

## Database-specific rules

When distilling a database or table-heavy corpus:

1. Record schema before interpretation: table names, fields, data types, units, missing-value codes, provenance, and update date.
2. Keep raw rows private unless the license explicitly permits redistribution.
3. Distill query/interpretation procedures, not the dataset itself.
4. Put unit conversion, normalization, outlier, and missing-data checks into safety gates.
5. Treat field descriptions and column names as source anchors; do not silently rename them without a mapping table.
6. If the database is living, add a refresh gate and version pin.
7. Build eval cases from synthetic or licensed examples, not from private user records.

## Keyword seed -> point-to-point expansion

For large source systems, sparse invocation should use this path:

```text
task keywords / field names / concept signature
  -> source-map seed units
  -> top-k routed experts
  -> one-hop graph neighbors
  -> safety/evidence/source-anchor gates
  -> answer or deliberate expansion
  -> route log and cache update
```

Each opened node needs a reason. If there is no source-map field or graph edge explaining why a module is opened, skip it until the missed-case sweep demands it.

## When full reading or full scan is correct

Full reading/scanning is correct for:

- first-time source inventory;
- schema recovery;
- audit of coverage;
- release review;
- migration from old source version to new source version;
- resolving contradictory recommendations;
- safety/evidence review in high-risk domains.

Full reading is not a failure. The failure is doing full reading and leaving no shorter map for next time.

## Return-to-cache after a large-source run

After each serious run, update at least one return surface:

- `source_map` or schema map: new unit, corrected location, better role;
- `ROUTING.yaml`: new trigger or anti-trigger;
- `GRAPH.md`: new neighbor edge or contradiction edge;
- `CACHE.md`: new stable signature or gotcha;
- `assets/eval-cases.md`: new route/anti-route/safety example;
- `assets/route-log-examples.md`: compact precedent for future calls.

## Acceptance gate

A book/database-derived skill is not complete until an agent can answer:

1. Which source-map seed did this task hit?
2. Which routed experts were opened and why?
3. Which relevant neighbors were checked without global traversal?
4. Which safety/evidence/source-anchor gates ran?
5. When would this task require full source review?
6. What was returned to the map/cache/evals for next time?
