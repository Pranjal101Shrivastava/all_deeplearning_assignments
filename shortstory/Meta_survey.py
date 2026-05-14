"""Meta-survey: re-derive the taxonomy from Tang et al. 2025 (arXiv:2510.17491)
on a fresh batch of recent LLM-agent papers pulled from arXiv.

The original survey proposes a 5-level capability maturity model (L1-L5) and
three technology pillars (Memory, Planning, Tool Use), plus five application
domains. We fetch the most recent papers in cs.CL / cs.AI matching "LLM agent"
and apply a transparent keyword-based classifier per pillar and per domain.

Run:  python meta_survey.py --max-papers 200 --out results/
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from dataclasses import dataclass, asdict
from pathlib import Path


ARXIV_API = "http://export.arxiv.org/api/query"
ATOM_NS = {"a": "http://www.w3.org/2005/Atom"}


# ---------------------------------------------------------------------------
# Taxonomy from the paper (Fig. 1 and Fig. 2 of arXiv:2510.17491)
# ---------------------------------------------------------------------------

MEMORY_LEVELS = {
    "L1_contextual":         ["context window", "chain of thought", "in-context", "working memory", "scratchpad"],
    "L2_passive_retrieval":  ["retrieval-augmented", "rag ", "vector store", "embedding retriev", "knowledge base"],
    "L3_active_learning":    ["reflection", "self-reflect", "experience replay", "lifelong", "self-improv", "memory writ"],
    "L4_distributed_shared": ["shared memory", "multi-agent memory", "blackboard", "team memory", "global memory"],
    "L5_evolutionary":       ["evolutionary memory", "generational", "population memory", "cultural", "intergenerational"],
}

PLANNING_LEVELS = {
    "L1_linear":              ["chain-of-thought", "step-by-step", "linear plan"],
    "L2_reactive":            ["react ", "reactive", "react agent", "act-observe", "tool-use loop"],
    "L3_global":              ["tree of thought", "tree-of-thought", "world model", "monte carlo tree", "look-ahead", "global plan"],
    "L4_collaborative":       ["multi-agent plan", "collaborative plan", "role-based", "agent team", "task allocation"],
    "L5_autonomous_goal":     ["open-ended goal", "self-directed", "goal generation", "autonomous goal", "intrinsic motivation"],
}

TOOL_LEVELS = {
    "L1_instruction_driven":  ["program-aided", "pal ", "code interpreter", "call this function"],
    "L2_goal_driven":         ["toolformer", "tool learning", "api call", "function calling", "webgpt", "webshop"],
    "L3_dynamic_orch":        ["tool selection", "tool routing", "tool orchestrat", "toolnet", "toolchain"],
    "L4_distributed_mgmt":    ["tool marketplace", "tool sharing", "agent-as-tool", "tool federation"],
    "L5_tool_creation":       ["tool creation", "auto-generated tool", "self-made tool", "creator agent", "synthesise tool"],
}

DOMAINS = {
    "process_execution":        ["text-to-sql", "nl-to-fl", "form filling", "document extraction", "layoutlm", "structured extraction"],
    "interactive_problem":      ["copilot", "decision support", "ui agent", "gui agent", "interactive assistant"],
    "digital_engineering":      ["code agent", "software engineering", "autodev", "swe-bench", "pentest", "devops"],
    "scientific_discovery":     ["scientific discovery", "ai scientist", "drug discovery", "chemistry agent", "biology agent", "materials"],
    "embodied_intelligence":    ["embodied", "robot", "manipulation", "navigation agent", "minecraft", "vln"],
    "business_execution":       ["finance agent", "trading agent", "supply chain", "marketing", "customer service"],
    "system_simulation":        ["agent-based simulation", "social simulation", "citysim", "urban planner", "society of agents"],
}


# ---------------------------------------------------------------------------
# arXiv fetcher
# ---------------------------------------------------------------------------

@dataclass
class Paper:
    arxiv_id: str
    title: str
    abstract: str
    published: str
    categories: str
    url: str


def fetch_arxiv(query: str, max_results: int = 200, batch: int = 50) -> list[Paper]:
    """Query the arXiv Atom API in batches and return parsed Paper objects."""
    papers: list[Paper] = []
    for start in range(0, max_results, batch):
        params = {
            "search_query": query,
            "start": start,
            "max_results": min(batch, max_results - start),
            "sortBy": "submittedDate",
            "sortOrder": "descending",
        }
        url = f"{ARXIV_API}?{urllib.parse.urlencode(params)}"
        with urllib.request.urlopen(url, timeout=30) as resp:
            body = resp.read()
        root = ET.fromstring(body)
        entries = root.findall("a:entry", ATOM_NS)
        if not entries:
            break
        for e in entries:
            arxiv_id = e.find("a:id", ATOM_NS).text.rsplit("/", 1)[-1]
            papers.append(Paper(
                arxiv_id=arxiv_id,
                title=" ".join(e.find("a:title", ATOM_NS).text.split()),
                abstract=" ".join(e.find("a:summary", ATOM_NS).text.split()),
                published=e.find("a:published", ATOM_NS).text[:10],
                categories=",".join(c.attrib["term"] for c in e.findall("a:category", ATOM_NS)),
                url=e.find("a:id", ATOM_NS).text,
            ))
        time.sleep(3)  # be nice to arXiv
    return papers


# ---------------------------------------------------------------------------
# Classifier (transparent keyword match against title + abstract)
# ---------------------------------------------------------------------------

def _score(text: str, keywords: list[str]) -> int:
    t = text.lower()
    return sum(1 for kw in keywords if kw.lower() in t)


def classify_levels(text: str, levels: dict[str, list[str]]) -> str | None:
    """Return the highest-scoring level, or None if no keyword matched."""
    scored = {label: _score(text, kws) for label, kws in levels.items()}
    best = max(scored.items(), key=lambda x: x[1])
    return best[0] if best[1] > 0 else None


def classify_domains(text: str) -> list[str]:
    """A paper can hit multiple application domains."""
    return [d for d, kws in DOMAINS.items() if _score(text, kws) > 0]


def classify_paper(p: Paper) -> dict:
    blob = f"{p.title}\n{p.abstract}"
    return {
        "arxiv_id": p.arxiv_id,
        "title": p.title,
        "published": p.published,
        "url": p.url,
        "memory_level": classify_levels(blob, MEMORY_LEVELS),
        "planning_level": classify_levels(blob, PLANNING_LEVELS),
        "tool_level": classify_levels(blob, TOOL_LEVELS),
        "domains": classify_domains(blob),
    }


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def write_outputs(rows: list[dict], outdir: Path) -> None:
    outdir.mkdir(parents=True, exist_ok=True)

    with (outdir / "classified.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["arxiv_id", "published", "title",
                    "memory_level", "planning_level", "tool_level",
                    "domains", "url"])
        for r in rows:
            w.writerow([r["arxiv_id"], r["published"], r["title"],
                        r["memory_level"] or "", r["planning_level"] or "",
                        r["tool_level"] or "", "|".join(r["domains"]), r["url"]])

    with (outdir / "classified.jsonl").open("w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")

    mem = Counter(r["memory_level"] or "unclassified" for r in rows)
    plan = Counter(r["planning_level"] or "unclassified" for r in rows)
    tool = Counter(r["tool_level"] or "unclassified" for r in rows)
    dom = Counter(d for r in rows for d in r["domains"]) or Counter({"unclassified": len(rows)})

    summary = {
        "n_papers": len(rows),
        "memory_distribution": dict(mem.most_common()),
        "planning_distribution": dict(plan.most_common()),
        "tool_distribution": dict(tool.most_common()),
        "domain_distribution": dict(dom.most_common()),
    }
    (outdir / "summary.json").write_text(json.dumps(summary, indent=2))

    md = ["# Meta-survey results", "",
          f"Classified **{len(rows)}** recent arXiv papers against the taxonomy "
          "from arXiv:2510.17491.", ""]
    for name, counter in [("Memory pillar", mem), ("Planning pillar", plan),
                          ("Tool-Use pillar", tool), ("Application domain", dom)]:
        md.append(f"## {name}")
        md.append("| level | count |")
        md.append("|---|---|")
        for k, v in counter.most_common():
            md.append(f"| {k} | {v} |")
        md.append("")

    md.append("## Sample papers per memory level")
    by_mem = defaultdict(list)
    for r in rows:
        by_mem[r["memory_level"] or "unclassified"].append(r)
    for level, items in by_mem.items():
        md.append(f"### {level} (n={len(items)})")
        for r in items[:3]:
            md.append(f"- [{r['arxiv_id']}]({r['url']}) — {r['title']}")
        md.append("")
    (outdir / "report.md").write_text("\n".join(md))


# ---------------------------------------------------------------------------

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--query",
                    default='abs:"LLM agent" OR abs:"language model agent" OR ti:"LLM agent"')
    ap.add_argument("--max-papers", type=int, default=200)
    ap.add_argument("--out", default="results")
    args = ap.parse_args()

    print(f"Querying arXiv: {args.query!r}  (max {args.max_papers})")
    papers = fetch_arxiv(args.query, max_results=args.max_papers)
    print(f"Fetched {len(papers)} papers")

    rows = [classify_paper(p) for p in papers]
    write_outputs(rows, Path(args.out))
    print(f"Wrote results to {args.out}/")


if __name__ == "__main__":
    main()
