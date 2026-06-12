#!/usr/bin/env python3
"""Generate a demand-sensitive sparse reading plan for book-to-skill-distillation.

This helper is intentionally dependency-free. It does not replace agent judgment;
it makes the first reading decision explicit so ordinary calls start sparse, while
audit/refactor/safety tasks can deliberately expand to broad or full reading.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
from dataclasses import dataclass, asdict
from typing import Iterable

ROOT = pathlib.Path(__file__).resolve().parents[1]

CORE_FILES = ["SKILL.md", "ROUTING.yaml"]
RUNBOOK_FILES = ["RUNBOOK.md"]
GRAPH_CACHE_FILES = ["GRAPH.md", "CACHE.md"]
SAFETY_FILES = [
    "reference/copyright-discipline.md",
    "reference/validation-checklist.md",
]

EXPERTS = {
    "source-triage": {
        "file": "reference/source-triage.md",
        "terms": ["source", "pdf", "epub", "manual", "book", "triage", "inspect", "material", "材料", "来源", "格式"],
    },
    "scanned-pdf": {
        "file": "reference/scanned-pdf-recipe.md",
        "terms": ["scan", "scanned", "ocr", "image", "blank", "render", "扫描", "图片", "识别"],
    },
    "toc-recovery": {
        "file": "reference/toc-recovery.md",
        "terms": ["toc", "bookmark", "outline", "heading", "目录", "章节", "结构"],
    },
    "outline-design": {
        "file": "reference/outline-design.md",
        "terms": ["outline", "tree", "module", "expert", "split", "route", "map", "graph", "拆分", "路由", "模块", "结构"],
    },
    "agent-native-rewrite": {
        "file": "reference/agent-native-rewrite.md",
        "terms": ["rewrite", "agent-native", "workflow", "checklist", "skill", "转写", "工作流", "清单"],
    },
    "sparse-methodology": {
        "file": "reference/sparse-distillation-methodology.md",
        "terms": ["sparse", "top-k", "moe", "routing", "cache", "稀疏", "低功耗", "按需", "全量", "回流"],
    },
    "cyclic-low-power": {
        "file": "reference/cyclic-low-power-distillation.md",
        "terms": ["cycle", "return", "cache", "low-power", "回流", "成圆", "低功耗", "闭环"],
    },
    "daemon-orchestration": {
        "file": "reference/daemon-orchestration.md",
        "terms": ["daemon", "parallel", "fanout", "分神", "并行", "多代理"],
    },
    "copyright": {
        "file": "reference/copyright-discipline.md",
        "terms": ["copyright", "license", "publish", "quote", "reproduce", "版权", "发布", "引用", "复刻"],
    },
    "validation": {
        "file": "reference/validation-checklist.md",
        "terms": ["validate", "quality", "test", "eval", "acceptance", "验收", "测试", "质量"],
    },
    "publishing": {
        "file": "reference/publishing.md",
        "terms": ["publish", "release", "repo", "github", "公开", "发布", "仓库"],
    },
}

HIGH_RISK_TERMS = [
    "medical", "medicine", "nutrition", "legal", "finance", "clinical", "patient", "children",
    "医学", "医疗", "营养", "法律", "金融", "临床", "儿童", "投稿", "公开发布",
]
AUDIT_TERMS = [
    "audit", "full", "entire", "whole", "migration", "migrate", "refactor", "redesign", "quality investigation",
    "repo-wide", "coverage", "release review", "审计", "全量", "全部", "迁移", "重构", "整改", "质量排查", "发布前",
]
GRAPH_EXPANSION_TERMS = [
    "graph", "network", "neighbor", "point-to-point", "seed node", "keyword", "关键词", "网状", "网络", "点对点", "节点", "邻接", "非遍历", "无遗漏",
]
NUTRITION_TERMS = ["nutrition", "diet", "dietary", "obesity", "BMI", "营养", "膳食", "肥胖", "儿童肥胖", "食养"]
ANTI_TRIGGER_TERMS = [
    "summary only", "book report", "copy the book", "verbatim", "bypass copyright", "只要摘要", "读后感", "复制原文", "绕过版权",
]


@dataclass
class RoutePlan:
    task: str
    mode: str
    confidence: str
    should_full_read: bool
    selected_files: list[str]
    optional_expansion_files: list[str]
    skipped_by_default: list[str]
    missed_case_sweep: list[str]
    escalation_triggers: list[str]
    return_to_cache: list[str]
    notes: list[str]


def norm(text: str) -> str:
    return text.lower()


def has_any(text: str, terms: Iterable[str]) -> bool:
    t = norm(text)
    return any(term.lower() in t for term in terms)


def score_experts(task: str) -> list[tuple[int, str, str]]:
    t = norm(task)
    scores: list[tuple[int, str, str]] = []
    for name, meta in EXPERTS.items():
        score = 0
        hits = []
        for term in meta["terms"]:
            if term.lower() in t:
                score += 2 if len(term) > 3 else 1
                hits.append(term)
        if score:
            scores.append((score, name, meta["file"]))
    scores.sort(reverse=True)
    return scores


def infer_mode(task: str, requested_mode: str | None) -> str:
    if requested_mode:
        return requested_mode
    if has_any(task, AUDIT_TERMS):
        return "audit"
    if has_any(task, HIGH_RISK_TERMS):
        return "high-risk"
    if any(w in norm(task) for w in ["cross", "integrate", "synthesis", "跨", "综合"]):
        return "cross-topic"
    if any(w in norm(task) for w in ["quick", "lookup", "where", "哪个", "哪里", "查一下"]):
        return "quick"
    return "normal"


def plan(task: str, mode: str | None = None, top_k: int | None = None) -> RoutePlan:
    task = task.strip()
    if not task:
        raise SystemExit("--task is required")

    inferred = infer_mode(task, mode)
    anti = has_any(task, ANTI_TRIGGER_TERMS)
    high_risk = inferred == "high-risk" or has_any(task, HIGH_RISK_TERMS)
    audit = inferred in {"audit", "migration", "refactor", "full", "redesign"} or has_any(task, AUDIT_TERMS)
    graph_expansion = has_any(task, GRAPH_EXPANSION_TERMS)
    nutrition = has_any(task, NUTRITION_TERMS)

    scores = score_experts(task)
    default_top_k = 1 if inferred == "quick" else 3 if inferred in {"normal", "cross-topic"} else 4
    if top_k is None:
        top_k = default_top_k
    top_k = max(1, min(top_k, 8))

    selected = list(CORE_FILES)
    if inferred != "quick" or audit:
        selected += RUNBOOK_FILES
    selected += [file for _, _, file in scores[:top_k]]

    if not scores and not audit:
        selected += ["reference/agent-native-rewrite.md", "reference/sparse-distillation-methodology.md"]

    if high_risk:
        for f in SAFETY_FILES:
            if f not in selected:
                selected.append(f)

    if graph_expansion:
        if "GRAPH.md" not in selected:
            selected.append("GRAPH.md")
    if nutrition:
        if "assets/sparse-nutrition-example.md" not in selected:
            selected.append("assets/sparse-nutrition-example.md")

    if inferred in {"cross-topic", "audit", "migration", "refactor", "full", "redesign"} or audit:
        for f in GRAPH_CACHE_FILES:
            if f not in selected:
                selected.append(f)

    if audit:
        # Broad reading is intentional. List all repo guidance files that exist.
        broad = [
            "README.md", "RUNBOOK.md", "ROUTING.yaml", "GRAPH.md", "CACHE.md", "RULES.md",
            "assets/eval-cases.md", "assets/output-template.md", "assets/route-log-template.md",
            "reference/agent-native-rewrite.md", "reference/sparse-distillation-methodology.md",
            "reference/source-triage.md", "reference/outline-design.md", "reference/validation-checklist.md",
            "reference/copyright-discipline.md", "reference/publishing.md",
        ]
        selected = list(dict.fromkeys(CORE_FILES + broad))

    optional = []
    for _, _, f in scores[top_k:top_k + 5]:
        if f not in selected:
            optional.append(f)
    if "GRAPH.md" not in selected:
        optional.append("GRAPH.md")
    if "CACHE.md" not in selected:
        optional.append("CACHE.md")
    optional = list(dict.fromkeys(optional))

    all_files = [meta["file"] for meta in EXPERTS.values()] + ["GRAPH.md", "CACHE.md", "assets/eval-cases.md"]
    skipped = [f for f in all_files if f not in selected and f not in optional]

    sweep = [
        "copyright_and_source_boundary",
        "private_information_boundary",
        "anti_trigger_check",
        "adjacent_skill_check",
        "output_contract_check",
    ]
    if high_risk:
        sweep += ["safety_or_evidence_gate", "citation_verifiability", "professional_boundary"]
    if audit:
        sweep += ["whole_repo_consistency", "stale_route_check", "coverage_vs_budget_check"]

    escalation = [
        "selected modules conflict",
        "answer cannot pass acceptance checks",
        "source/evidence boundary is unclear",
        "missed-case sweep finds a red flag",
    ]
    if graph_expansion:
        escalation.append("one-hop graph expansion still leaves an uncovered neighbor or red flag")
    if not audit:
        escalation.append("user asks for audit/migration/refactor/release review/full coverage")

    return_to_cache = [
        "append route log using assets/route-log-template.md",
        "promote repeated expansion into ROUTING.yaml or GRAPH.md",
        "add gotcha/eval case when a route fails",
        "compress broad/full reading into CACHE.md before next invocation",
    ]

    notes = []
    if anti:
        notes.append("Anti-trigger likely matched: consider refusing, redirecting, or asking for a transformation goal.")
    if audit:
        notes.append("Broad/full reading is justified for this task; do not treat full reading as sparse failure.")
    elif high_risk:
        notes.append("High-risk task: include safety/evidence gate even if not top semantic match.")
    else:
        notes.append("Start sparse; expand only if a listed escalation trigger fires.")
    if graph_expansion:
        notes.append("Use keyword seed nodes, then point-to-point graph expansion; do not traverse the whole graph by default.")
    if nutrition:
        notes.append("Nutrition example: include population/safety/evidence/stigma/referral sweep before answering.")

    confidence = "medium" if scores else "low"
    if audit or high_risk or len(scores) >= 2:
        confidence = "high"

    return RoutePlan(
        task=task,
        mode=inferred,
        confidence=confidence,
        should_full_read=bool(audit),
        selected_files=list(dict.fromkeys(selected)),
        optional_expansion_files=optional,
        skipped_by_default=skipped,
        missed_case_sweep=list(dict.fromkeys(sweep)),
        escalation_triggers=escalation,
        return_to_cache=return_to_cache,
        notes=notes,
    )


def render_markdown(p: RoutePlan) -> str:
    def bullets(xs: list[str]) -> str:
        return "\n".join(f"- `{x}`" if re.search(r"[./]", x) else f"- {x}" for x in xs) or "- none"

    return f"""# Route Plan

**Task:** {p.task}

- mode: `{p.mode}`
- confidence: `{p.confidence}`
- full reading now: `{str(p.should_full_read).lower()}`

## Read first

{bullets(p.selected_files)}

## Optional expansion

{bullets(p.optional_expansion_files)}

## Skip by default

{bullets(p.skipped_by_default)}

## Missed-case sweep

{bullets(p.missed_case_sweep)}

## Escalate when

{bullets(p.escalation_triggers)}

## Return to cache

{bullets(p.return_to_cache)}

## Notes

{bullets(p.notes)}
"""


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Generate a sparse/demand-sensitive reading plan.")
    ap.add_argument("--task", required=True, help="User task or invocation summary")
    ap.add_argument("--mode", choices=["quick", "normal", "cross-topic", "high-risk", "audit", "migration", "refactor", "full", "redesign"], help="Override inferred mode")
    ap.add_argument("--top-k", type=int, help="Number of routed experts to select before expansion")
    ap.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown")
    args = ap.parse_args(argv)

    p = plan(args.task, args.mode, args.top_k)
    if args.json:
        print(json.dumps(asdict(p), ensure_ascii=False, indent=2))
    else:
        print(render_markdown(p))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
