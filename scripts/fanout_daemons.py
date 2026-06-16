#!/usr/bin/env python3
"""Generate one LingTai daemon task per reference doc.

Fan-out is how this skill rewrites in parallel: one daemon per topic, each
turning a slice of the source into an operational reference module — not a
chapter summary. This script takes a list of planned reference docs and emits a
concrete daemon task prompt for each, shaped by `assets/daemon-task-template.md`
and the copyright/page-citation rules in `reference/daemon-orchestration.md`.

Input (JSON file via positional arg, or JSON on stdin) — a list of docs:

    [
      {"path": "reference/childhood-overweight.md",
       "scope": "Ch 7, pages 120-138",
       "topic": "childhood overweight management"},
      {"path": "reference/adult-weight.md", "pages": "139-160"}
    ]

A bare list of strings (treated as output paths) also works:

    ["reference/childhood-overweight.md", "reference/adult-weight.md"]

Output: fanout_tasks.json — one daemon task per doc, ready to dispatch.
Dependency-free; Python 3.10+.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

# Standard sections every reference module must contain (see
# assets/reference-doc-template.md / daemon-task-template.md).
REQUIRED_SECTIONS = [
    "scope",
    "when to use",
    "checklist or procedure",
    "pitfalls",
    "cross-references",
    "source notes",
]

# Copyright/citation constraints every daemon inherits.
CONSTRAINTS = [
    "Do not reproduce more than ~2 consecutive source sentences.",
    "Cite only pages you actually opened.",
    "Flag OCR uncertainty and any claim needing current-law/standard verification.",
    "Output operational structures (checklists, decision trees), not chapter prose.",
]


def normalize_doc(raw: object, index: int) -> dict:
    """Accept either a path string or a dict; return a normalized doc record."""
    if isinstance(raw, str):
        return {"path": raw}
    if isinstance(raw, dict):
        if "path" not in raw:
            sys.exit(f"doc #{index} is missing required 'path' field: {raw!r}")
        return dict(raw)
    sys.exit(f"doc #{index} must be a string or object, got {type(raw).__name__}")


def build_task(doc: dict, target_skill: str, book_title: str) -> dict:
    """Build one LingTai daemon task description for a single reference doc."""
    path = doc["path"]
    name = pathlib.Path(path).stem
    topic = doc.get("topic", name.replace("-", " "))
    scope = doc.get("scope") or doc.get("pages") or "<CHAPTERS/PAGES — fill in>"

    prompt = (
        f"You are distilling {scope} of \"{book_title}\" into one reference doc "
        f"for `.library/custom/{target_skill}/`.\n"
        f"Topic: {topic}.\n"
        f"Output path: {path}.\n"
        f"Include these sections: {', '.join(REQUIRED_SECTIONS)}.\n"
        + "\n".join(f"- {c}" for c in CONSTRAINTS)
    )

    return {
        "daemon_id": f"distill-{name}",
        "role": "reference-distillation-daemon",
        "target_skill": target_skill,
        "topic": topic,
        "scope": scope,
        "output_path": path,
        "required_sections": REQUIRED_SECTIONS,
        "constraints": CONSTRAINTS,
        "must_write_file": True,
        "prompt": prompt,
    }


def load_docs(source: str | None) -> list:
    if source:
        text = pathlib.Path(source).read_text(encoding="utf-8")
    else:
        if sys.stdin.isatty():
            sys.exit("No input file given and stdin is empty. See --help.")
        text = sys.stdin.read()
    data = json.loads(text)
    if not isinstance(data, list):
        sys.exit("Input must be a JSON list of docs (strings or objects).")
    return data


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(
        description="Generate one LingTai daemon task per reference doc.",
    )
    ap.add_argument(
        "input", nargs="?",
        help="JSON file listing reference docs (default: read JSON from stdin)",
    )
    ap.add_argument(
        "-o", "--out", type=pathlib.Path, default=pathlib.Path("fanout_tasks.json"),
        help="Output path for the generated tasks (default: fanout_tasks.json)",
    )
    ap.add_argument(
        "--target-skill", default="<TARGET_SKILL>",
        help="Slug of the skill being built (default: <TARGET_SKILL>)",
    )
    ap.add_argument(
        "--book-title", default="<BOOK_TITLE>",
        help="Source book/database title (default: <BOOK_TITLE>)",
    )
    args = ap.parse_args(argv)

    docs = load_docs(args.input)
    tasks = [
        build_task(normalize_doc(raw, i), args.target_skill, args.book_title)
        for i, raw in enumerate(docs)
    ]

    args.out.write_text(
        json.dumps({"tasks": tasks}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Wrote {len(tasks)} daemon task(s) to {args.out}")
    for task in tasks:
        print(f"  - {task['daemon_id']} -> {task['output_path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
