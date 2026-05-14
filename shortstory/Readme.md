# LLM-Driven Industry Agents — Short Story, Medium Article & Meta-Survey

A coursework project for **CMPE 297 (San José State University, Spring 2026)**
that turns the October 2025 survey

> Tang et al., *Empowering Real-World: A Survey on the Technology, Practice,
> and Evaluation of LLM-driven Industry Agents.*
> [arXiv:2510.17491](https://arxiv.org/abs/2510.17491)

into three complementary deliverables:

1. A **Medium article** that walks a general technical reader through the
   paper's argument.
2. A **slide deck / short story** version for a 15-minute talk.
3. A small **autoresearch-style reproduction** — a meta-survey that
   re-derives the paper's taxonomy on a fresh batch of arXiv papers.

---


## TL;DR of the paper (in my own words)

LLM-based agents have moved from research demos toward genuine tools used
inside companies, but the path from "an LLM that can call functions" to "an
agent that pays for itself in a real business workflow" is unevenly mapped in
the literature. Tang and co-authors try to draw that map. They argue that
industry agents — autonomous or semi-autonomous systems deployed in concrete
business contexts — face harder problems than general agents do: they live
under real time constraints (finance), real authority constraints (healthcare),
and real physical constraints (manufacturing).

The survey's central contribution is a **five-level capability maturity model**
that lines up agent sophistication with the technologies that make each level
possible:

| Level | System type | What it can do |
|---|---|---|
| **L1** | Process Execution | Translate natural language to a structured action; extract information |
| **L2** | Interactive Problem-Solving | Augment a human in the loop, support decisions |
| **L3** | End-to-End Autonomous | Close the loop in engineering, science, or embodied tasks |
| **L4** | Collaborative Intelligent | Run business processes across multi-agent teams or simulate complex systems |
| **L5** | Adaptive Social | Generate its own goals and evolve across "generations" of interactions |

The authors then track three technology pillars — **Memory**, **Planning**,
and **Tool Use** — through the same five rungs, showing that each rung of the
maturity model is gated by a corresponding upgrade in each pillar. Memory
goes from a transient context window (L1) to retrieval over external knowledge
(L2), to active reflection (L3), to multi-agent shared memory (L4), to
evolutionary memory that carries forward across populations of agents (L5).
Planning travels from chain-of-thought, through ReAct loops, to global tree
search, to multi-agent role allocation, to self-directed goal generation.
Tool Use moves from a fixed instruction-bound call, to learned API
invocation, to dynamic orchestration, to distributed tool marketplaces, to
agents that *create* their own tools.

The evaluation chapter is split between **fundamental** benchmarks
(per pillar — Memory, Planning, Tool Use) and **industry-specific** benchmarks
(general agent benchmarks vs. domain-specific ones), and the authors are
explicit that current benchmarks under-test the things industry actually cares
about: long-horizon reliability, safety under adversarial users, regulatory
compliance, and authenticity of the evaluation environment.

The paper closes on bottlenecks: long-context forgetting and noisy memory are
the hard part of Memory; brittleness under real-world dynamism is the hard
part of Planning; selecting and recovering from tools is the hard part of
Tool Use. Above the technology layer, governance, capability boundaries, and
the cost of bringing deep domain expertise into an agent are the open
questions for the next generation of industry deployments.

---

## The Medium article

**Title:** *From Lab Demos to Production Lines: A Field Guide to LLM-Driven
Industry Agents*

**Subtitle:** *A walk-through of the October 2025 survey by Tang et al. — and
what it tells us about why most agent demos never become products.*

**Length:** ~3,500 words, ~12 minutes of reading.

**Sources:**
Medium_Article : https://medium.com/@pranjal.shrivastava_9505/from-lab-demos-to-production-lines-647a11c14f52?postPublishedType=initial)

**Structure of the article:**

1. **TL;DR** — an industry agent is not a model; it is a workflow built on
   three pillars and measured by maturity, not accuracy.
2. **Why I picked this paper** — most agent surveys are written for
   researchers; this one is written for the people who actually have to ship.
3. **The central question** — how do we translate LLM reasoning into
   *industrial* productivity?
4. **The gap nobody talks about** — what research optimises for vs. what
   deployments actually need.
5. **The capability maturity framework** — the L1→L5 ladder, with a key
   observation: L5 is not always the goal.
6. **The three pillars** — Memory, Planning, Tool Use, with production
   notes on each.
7. **Where industry agents are actually landing** — five domains (digital
   engineering, scientific discovery, embodied intelligence, collaborative
   business, system simulation) with two spotlights.
8. **Evaluation: beyond accuracy** — why a single leaderboard is not enough,
   and why the field is heading for a "metric crisis."
9. **Open challenges** — authenticity, safety, long-horizon memory, cost &
   latency, multi-agent coordination, domain adaptation.
10. **My critical take** — strengths and where the survey could go deeper.
11. **Five things to remember** — a one-screen recap.

The article includes my own commentary and a "my take" block at the end of
each major section — these are explicitly mine, not paraphrases of the
survey.

---

## The slide deck (short story)

**Title:** *From Lab Demos to Production Lines — LLM-Driven Industry Agents*

**Format:** 15 slides, designed for a ~15-minute course presentation.

**Sources:**
https://docs.google.com/presentation/d/1WL0jHZvAl510cy_rAOQMtxQXHOR2WPct/edit?usp=drive_link&ouid=110036436129950097450&rtpof=true&sd=true

**Slide map:**

| # | Slide | Purpose |
|---|---|---|
| 1 | Title | Set up the framing — "demos vs. production lines." |
| 2 | Why this paper | Industry framing vs. research framing. |
| 3 | The gap | Side-by-side: research priorities vs. deployment priorities. |
| 4 | Maturity framework | The L1→L5 ladder. |
| 5 | L1–L2 in practice | Process execution and reactive assistants. |
| 6 | L3 in practice | End-to-end autonomous workers — the current frontier. |
| 7 | L4–L5 in practice | Multi-agent and adaptive ecosystems. |
| 8 | Pillar 1: Memory | Working / episodic / semantic / procedural. |
| 9 | Pillar 2: Planning | CoT, ReAct, tree search, reflection. |
| 10 | Pillar 3: Tool Use | The canonical loop and three production lessons. |
| 11 | Application domains | Five domains with two spotlights. |
| 12 | Evaluation | The three-layer model: capabilities, benchmarks, impact. |
| 13 | Open challenges | Six bottlenecks blocking L3 → L4. |
| 14 | My critical take | Strengths and limits. |
| 15 | Takeaways + references | Five ideas to remember. |

The deck reuses the figures in [`figures/`](figures/), which were redrawn from
Figure 1 (framework), Figure 2 (taxonomy), Figure 3 (memory evolution), and
the planning / tool-use diagrams in the paper.

---

## The meta-survey reproduction

A small Python project under [`meta_survey/`](meta_survey/) that puts the
survey's taxonomy to a quick empirical test.

**What it does**

1. Pulls the most recent ~150 arXiv papers matching `"LLM agent"` /
   `"language model agent"` from the arXiv Atom API.
2. Scores each paper's title and abstract against a keyword dictionary built
   from Fig. 1 and Fig. 2 of the survey.
3. Assigns each paper the best-fit level for each pillar (Memory, Planning,
   Tool Use) plus any matching application domains.
4. Aggregates into a distribution that mirrors the paper's taxonomy.

**Why this counts as a reproduction.** The survey itself runs no experiments
— it is a synthesis paper. The natural thing to "reproduce" is its central
claim: that the field can be cleanly bucketed into the L1–L5 / Memory /
Planning / Tool-Use grid. This project re-derives that grid on papers
published *after* the survey was written, and reports whether the grid still
fits.

**Headline finding from the 150-paper run**

- About 85% of recent papers fall outside the survey's strict keyword
  vocabulary — i.e. the survey's terminology is largely *retrospective*.
  Authors of new papers do not yet self-describe as building "evolutionary
  memory" or "dynamic tool orchestration," even when the underlying ideas are
  present.
- Among classified papers, **Memory L1/L3** and **Tool Use L2 (function
  calling)** dominate — matching the survey's prediction that L3 is the
  current frontier and tool creation (L5) is still essentially absent.
- **Embodied intelligence** and **digital engineering** lead the domain axis;
  L5 ("adaptive social system") does not appear in the sample at all, again
  consistent with the survey.

**Run it yourself**

```bash
cd meta_survey
python3 meta_survey.py --max-papers 200 --out results/
```

No third-party dependencies. Python 3.10+ standard library only. The script
uses `urllib` against the public arXiv API and respects the 3-second batch
rate limit.

---

## How the three pieces fit together

| Deliverable | Audience | Length | Purpose |
|---|---|---|---|
| Medium article | General technical reader | ~12 min | Argue the survey's framing in plain English |
| Slide deck | Classmates / instructor | ~15 min | Compress the argument into a talk |
| Meta-survey code | Reviewer / future self | small | Put the taxonomy on a fresh batch of papers and report what fits |

The article and deck are interpretive; the meta-survey is empirical. Together
they form a small autoresearch-style writeup of the paper.

---

## Citing the original work

> Tang, Y., Chen, K., Yue, L., Fan, J., Zhou, C., Li, X., Zhang, Y., Zhao, M.,
> Kai, S., Guo, K., Zeng, X., Cun, W., Shang, L., & Zhang, M. (2025).
> *Empowering Real-World: A Survey on the Technology, Practice, and
> Evaluation of LLM-driven Industry Agents.*
> arXiv preprint [arXiv:2510.17491](https://arxiv.org/abs/2510.17491).

## Author

**Pranjal Shrivastava** — M.S. student, San José State University.
