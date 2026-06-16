#!/usr/bin/env python3
"""Bootstrap a book-to-skill distillation workspace from a PDF.

Given a PDF, this script sets up the private extraction substrate an agent then
distills from: it recovers the TOC, dumps full text with page markers, and seeds
the source catalog plus empty node/edge stores. It does *not* do the distillation
itself — that is the agent's job, following SKILL.md.

The workspace lives under `work/book-distill/<slug>/`, which `.gitignore` keeps
out of the published skill (the OCR/text substrate must stay private). See
`reference/source-map-and-database-distillation.md` for what the catalog/node/edge
stores become as the agent routes the source into experts.

Dependency-light by design: only PyMuPDF (`pip install pymupdf`). Python 3.10+.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

try:
    import fitz  # PyMuPDF
except ImportError:  # pragma: no cover - environment guidance
    sys.exit(
        "PyMuPDF is required. Install it with:\n"
        "    pip install pymupdf\n"
        "Then re-run: python scripts/setup_distill.py <input.pdf>"
    )

# Average adult silent reading speed; used only for a rough reading-time estimate.
WORDS_PER_MINUTE = 230


def slugify(text: str) -> str:
    """Turn a title or filename into a stable, filesystem-safe slug."""
    text = text.strip().lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text or "book"


def extract_toc(doc: "fitz.Document") -> list[dict]:
    """Recover TOC/bookmarks as a list of {level, title, page} entries.

    Page numbers are normalized to 1-based PDF pages (PyMuPDF already returns
    1-based pages from get_toc()). Structure recovery from text/rendered TOC,
    when bookmarks are absent, is the agent's job — see reference/toc-recovery.md.
    """
    toc = []
    for level, title, page in doc.get_toc(simple=True):
        toc.append({"level": level, "title": title.strip(), "page": page})
    return toc


def extract_fulltext(doc: "fitz.Document") -> tuple[str, int]:
    """Return full text with per-page markers, plus a total word count."""
    parts = []
    word_count = 0
    for index, page in enumerate(doc):
        text = page.get_text("text")
        word_count += len(text.split())
        # 1-based page marker so citations match the source map convention.
        parts.append(f"\n\n===== PAGE {index + 1} =====\n\n{text}")
    return "".join(parts).lstrip("\n"), word_count


def write_jsonl(path: pathlib.Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def build_catalog_entry(slug: str, title: str, pdf_name: str, page_count: int,
                        toc_entries: int, word_count: int) -> dict:
    """Seed source_catalog.jsonl with one whole-book entry.

    This mirrors the minimum source-map fields in
    reference/source-map-and-database-distillation.md. The agent splits this
    single entry into per-topic units as it routes the book into experts.
    """
    return {
        "unit_id": f"{slug}:whole-book",
        "source_id": title,
        "location": f"{pdf_name} pages 1-{page_count}",
        "topic_signature": [],
        "role": "source_anchor",
        "risk_tags": ["copyright"],
        "publishability": "needs_license_review",
        "neighbor_edges": {
            "prerequisite": [],
            "semantic_neighbor": [],
            "downstream_action": [],
            "safety_evidence": [],
            "contradiction_check": [],
        },
        "refresh_policy": "check_before_publication",
        "stats": {
            "page_count": page_count,
            "toc_entries": toc_entries,
            "word_count": word_count,
        },
    }


def setup(pdf_path: pathlib.Path, title: str | None, slug: str | None,
          root: pathlib.Path) -> dict:
    if not pdf_path.exists():
        sys.exit(f"PDF not found: {pdf_path}")

    doc = fitz.open(pdf_path)
    try:
        resolved_title = title or pdf_path.stem
        resolved_slug = slugify(slug or resolved_title)

        workspace = root / "work" / "book-distill" / resolved_slug
        workspace.mkdir(parents=True, exist_ok=True)

        toc = extract_toc(doc)
        fulltext, word_count = extract_fulltext(doc)
        page_count = doc.page_count
    finally:
        doc.close()

    (workspace / "source_toc.json").write_text(
        json.dumps(
            {"title": resolved_title, "slug": resolved_slug,
             "source_pdf": pdf_path.name, "page_count": page_count, "toc": toc},
            ensure_ascii=False, indent=2,
        ),
        encoding="utf-8",
    )

    (workspace / "fulltext.txt").write_text(fulltext, encoding="utf-8")

    catalog = build_catalog_entry(
        resolved_slug, resolved_title, pdf_path.name,
        page_count, len(toc), word_count,
    )
    write_jsonl(workspace / "source_catalog.jsonl", [catalog])

    # Empty stores the agent fills while distilling.
    write_jsonl(workspace / "node_store.jsonl", [])
    write_jsonl(workspace / "graph_edges.jsonl", [])

    return {
        "title": resolved_title,
        "slug": resolved_slug,
        "workspace": workspace,
        "page_count": page_count,
        "toc_entries": len(toc),
        "word_count": word_count,
    }


def print_summary(result: dict) -> None:
    minutes = result["word_count"] / WORDS_PER_MINUTE if result["word_count"] else 0
    if minutes >= 60:
        reading_time = f"{minutes / 60:.1f} h"
    else:
        reading_time = f"{minutes:.0f} min"

    print("Distillation workspace ready.")
    print()
    print(f"  title          : {result['title']}")
    print(f"  slug           : {result['slug']}")
    print(f"  workspace      : {result['workspace']}")
    print(f"  pages          : {result['page_count']}")
    print(f"  TOC entries    : {result['toc_entries']}")
    print(f"  words          : {result['word_count']:,}")
    print(f"  est. read time : {reading_time}")
    print()
    print("  Wrote: source_toc.json, fulltext.txt, source_catalog.jsonl,")
    print("         node_store.jsonl, graph_edges.jsonl")
    if result["toc_entries"] == 0:
        print()
        print("  Note: no bookmarks found. The source may be scanned or lack a TOC —")
        print("        see reference/toc-recovery.md and reference/scanned-pdf-recipe.md.")
    print()
    print("OK. Agent should now follow SKILL.md to begin distillation.")


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(
        description="Bootstrap a book-to-skill distillation workspace from a PDF.",
    )
    ap.add_argument("pdf", type=pathlib.Path, help="Path to the source PDF")
    ap.add_argument("--title", help="Book title (default: PDF filename)")
    ap.add_argument("--slug", help="Workspace slug (default: derived from title)")
    ap.add_argument(
        "--root", type=pathlib.Path, default=pathlib.Path.cwd(),
        help="Repo root under which work/book-distill/<slug>/ is created (default: cwd)",
    )
    args = ap.parse_args(argv)

    result = setup(args.pdf, args.title, args.slug, args.root)
    print_summary(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
