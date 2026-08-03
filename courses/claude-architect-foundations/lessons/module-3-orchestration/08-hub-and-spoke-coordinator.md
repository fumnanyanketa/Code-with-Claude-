# Module 3 · Lesson 8: Hub-and-spoke: your first coordinator

> **Course:** Claude Certified Architect: Foundations, a self-paced course
> **Module 3:** Orchestration: multi-agent architectures — turn one agent into a reliable coordinated system
> **Speaker:** Andrew Brown, ExamPro
> **Source:** Reconstructed from the CCA-F course by Andrew Brown (ExamPro) · [full transcript](../../transcripts/cca-f-full-course.txt)
> **Estimated time:** 45 to 60 minutes (read plus lab)

---

## In one sentence

A **hub-and-spoke** system puts one **coordinator** agent at the centre that owns three jobs — routing, context, and aggregation — and treats every other agent as just a tool it can call, so you build one screening coordinator that dispatches to a few single-purpose "spoke" agents and merges their answers into a single verdict.

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone
> Project** where you build Atlas Support's first coordinator: an intake
> screener that delegates to two or three spoke agents-as-tools and aggregates
> their results into one decision. Everything before the Capstone teaches the
> three jobs a coordinator owns and why spokes are "just tools." If you want to
> see the finish line first, jump to the **"Capstone Project"** section, then
> come back.

## First-principles companion

> 💡 **The durable idea behind this lesson.** Coordinator agents are new;
> the pattern underneath them is decades old.
>
> - **[The Actor Model](https://en.wikipedia.org/wiki/Actor_model)** (Carl
>   Hewitt, 1973). Independent "actors" that never share memory and only
>   communicate by passing messages. A coordinator with spokes that "never have
>   direct lines to each other" is exactly this: isolated workers that talk only
>   through messages routed by a hub.
> - **[Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)**
>   (Anthropic, 2024), the *orchestrator-workers* pattern. A central LLM
>   dynamically breaks a task down, delegates to worker LLMs, and synthesises
>   their results — the same three jobs you will build here.

## A few plain-language basics first

This lesson uses some terms from earlier lessons and a few new ones. In plain words:

- **Agent:** an AI that takes a series of actions on its own toward a goal, rather than answering in one shot.
- **Tool / tool call / tool result:** a function the model can choose to run; when it decides to run one, that is a *tool call*, and what comes back is the *tool result*.
- **`stop_reason`:** the field the API returns saying *why* the model stopped — `tool_use` (it wants to run a tool) or `end_turn` (it is finished). You drive the loop off this, never off the text.
- **Coordinator / hub-and-spoke:** an architecture where one *coordinator* agent (the "hub") owns routing, context, and aggregation, and delegates to *sub-agents* (the "spokes") that are exposed to it as tools.
- **Sub-agent (spoke):** an agent spawned to do one narrow job, usually with its own isolated context. It only knows what the coordinator hands it.
- **Routing:** deciding *which* spoke handles *which* piece of work.
- **Aggregation:** collecting every spoke's output and merging it into one coherent answer.

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

Last lesson you learned when to let the *model* decide versus when to hard-code the decision. A coordinator is where that judgment goes to live: it is a single agent whose whole job is to decide who does what and then pull the pieces back together. As Andrew puts it, "when you think of like Claude Code, I have a feeling that this is at least one of the means... when you're working with sub agents for communication." This is the shape most real multi-agent systems take, and it is the backbone of Atlas Support for the rest of the course. Learn it once here on a small, testable example and every later module (parallelism, hooks, handoff) just adds capability to the same skeleton.

## Learning objectives

By the end of this lesson you will be able to:

1. Draw the hub-and-spoke topology and explain why spokes never talk to each other directly.
2. Name and describe the coordinator's three jobs — routing, context ownership, and aggregation.
3. Explain why a sub-agent is "just a tool" from the coordinator's point of view.
4. Build a working coordinator that dispatches to two or three spoke agents and aggregates their outputs into one decision.
5. Verify a coordinator's behaviour instead of trusting that it did what it claims.

## Prerequisites

- **Module 1 · Lesson 3 (Tools and the stop-reason loop)** and **Lesson 4 (ending the loop correctly)** — the coordinator *is* a stop-reason loop with a max-iteration cap.
- **Module 3 · Lesson 7 (Code-driven vs model-driven decisions)** — routing is the model-driven decision you now put a structure around.
- Python, an Anthropic API key, and the response-parser helper from Module 0.

---

## Part 1: What hub-and-spoke actually is

Andrew states the pattern in one line: "hub and spoke architecture is a pattern where one coordinator agent sits at the center and all sub agents talk to the coordinator."

The picture is a wheel. The coordinator is the hub in the middle. Each spoke is a sub-agent doing one narrow job. The rule that makes it hub-and-spoke — and not just "a pile of agents" — is this: **spokes never have direct lines to each other.**

```text
                 ┌─────────────┐
        ┌────────┤ COORDINATOR ├────────┐
        │        │   (hub)     │        │
        │        └──────┬──────┘        │
        ▼               ▼               ▼
   ┌─────────┐    ┌───────────┐   ┌──────────┐
   │ spoke A │    │  spoke B  │   │ spoke C  │
   └─────────┘    └───────────┘   └──────────┘

   Spokes never talk to each other. Every message
   goes through the hub.
```

As Andrew says: "if you have like a research agent over here, it cannot directly talk to the reviewer agent. It has to go through the coordinator." A spoke does not even know the other spokes exist "unless the coordinator passes that information along and it gets injected."

Why force everything through one point? Because a single choke point is a gift for control and observability. "That would make it really good for observability because now everything's passing through there and we have a choke point where we can check and collect information." Every decision, every hand-off, every error passes through one place you can log, inspect, and guard.

> 🔑 **Hub-and-spoke = one coordinator in the middle, isolated spokes on the
> outside, and every message routed through the hub. The isolation is the
> feature, not a limitation.**

## Part 2: The coordinator's three jobs

Strip away the details and a coordinator owns exactly three responsibilities. Hold onto these three words — routing, context, aggregation — and the rest of the module is variations on them.

| Job | What the coordinator does | Andrew's words |
|---|---|---|
| **Routing** | Decide *which* spoke handles *which* subtask, based on the task | "the coordinator is going to own the routing. So it's going to decide how to route things" |
| **Context ownership** | Decide *what* each spoke is allowed to see; spokes are isolated by default | "the research agent is not going to be aware of what everyone's doing unless the coordinator passes that information along" |
| **Aggregation** | Collect every spoke's output and merge it into one coherent answer | "you've gotten all the outputs from multiple agents, combine them into a single coherent response, resolve any conflicts, and make the data pretty" |

Andrew frames the full task life cycle as: **task decomposition** (break the task into subtasks), **task delegation** (decide who works on each), **result aggregation** (bring it all back together), and choosing "which sub-agents to invoke based on query complexity."

### Routing is a decision, not a fixed wiring

The interesting part is that routing does not have to be static. You can *describe* how to route in the coordinator's prompt and let it judge. Andrew's routing instruction reads roughly: "Simple factual questions use a single agent. Multi-step tasks delegate out sequentially, passing the results forward. Independent subtasks delegate in parallel." That is "not just static routing — you route based on the use case." You will hard-code some routing and let the model decide the rest; Lesson 7 was about choosing which.

### Context ownership is what keeps spokes honest

Because each spoke "only sees its own isolated context," a spoke cannot leak assumptions from another spoke's work. That is *why* the coordinator owns context: isolation keeps each worker focused and its output independent — which matters enormously when you aggregate (a spoke cannot just echo another's answer).

> 🔑 **Routing, context, aggregation. If you can name those three jobs and say
> which one a line of code belongs to, you understand coordinators.**

## Part 3: A spoke is just a tool

Here is the mental jump that makes the code simple. From the coordinator's point of view, **a sub-agent is a tool.** Nothing more exotic.

You already know how tools work (Lesson 3): you give the model a list of tools with input schemas, it emits a `tool_use`, you run the function, you feed back a `tool_result`, and you loop on `stop_reason`. A spoke fits that exactly. The "function" you run just happens to be *another call to Claude* with its own narrow prompt. The coordinator does not care — it sees `run_keyword_scanner`, `run_deep_evaluator`, `run_red_flag_detector` as tools it may call, and off it goes.

```text
Coordinator's tool list (what the hub "sees"):
  - run_keyword_scanner(job_posting, resume)  → spoke A
  - run_deep_evaluator(job_posting, resume)   → spoke B
  - run_red_flag_detector(resume)             → spoke C

Each tool's implementation = one Claude call with a single-purpose prompt.
```

In Andrew's build these show up as a **dispatch tool** and a **tool schema** — "these are the actual tools deciding whether they should get triggered or not... what the coordinator hub sees." The coordinator "owns calling each spoke with the right input, deciding which spoke to call, collecting and combining their outputs."

### A trap to avoid: don't make decomposition a spoke

Mid-build, Andrew almost let the model invent a *separate* "decomposer" sub-agent and a *separate* "router" sub-agent. He caught it: "in a proper hub and spoke architecture the coordinator is the hub. It owns it. The decomposer isn't a separate sub-agent." Decomposition and routing are the coordinator's *own* responsibilities — jobs it does before it calls anyone. Only the actual *work* (scanning, evaluating, flagging) belongs in spokes.

> ❌ **The common mistake:** spinning up a "planner" or "router" agent as a
> spoke. Routing and decomposition are the hub's jobs. Spokes only do work.

### Verify — don't trust the narration

One line from Andrew is the whole ethos of this course: **"Just because it said it did, it does not mean it did."** When the model announced it had implemented the architecture, he read the code anyway — "this is me looking at going, that doesn't seem right." The docs, the AI's own summary of its work, even a confident "you're right" are not proof. The way to the truth is to run it and read the output. Build that habit into every milestone below.

> ✅ **What to do about it:** after every step, run the coordinator and read the
> actual spoke calls and outputs. Confirm each spoke ran, with the input you
> expected, before you believe the final verdict.

---

## Key takeaways

1. **Hub-and-spoke = one coordinator, isolated spokes, every message through the hub.** Spokes never talk to each other; that isolation is the feature.
2. **The coordinator owns three jobs: routing, context, aggregation.** Everything else is detail.
3. **A spoke is just a tool.** Its implementation is one Claude call with a narrow prompt, but the coordinator sees it as an ordinary tool with an input schema.
4. **Decomposition and routing belong to the hub, not to a spoke.** Spokes only do work.
5. **The choke point is a gift.** One point every message passes through is exactly where you add logging, checks, and error handling later.
6. **Verify, don't trust.** "Just because it said it did, it does not mean it did." Run it and read the output.

## Common pitfalls

- ❌ **Letting spokes call each other.** The moment spoke A calls spoke B directly, you have lost your choke point and your observability. Route everything through the hub.
- ❌ **Making a "router" or "decomposer" a spoke.** Those are the coordinator's own jobs. Spokes only execute work.
- ❌ **Trusting the model's summary of its own build.** It will say "done" and "you're right." Read the code and the run output yourself.
- ❌ **A `while True` loop with no cap.** Andrew keeps flagging this: even with a `break` on `end_turn`, add a max-iteration cap (he uses 10, "double the expected five steps") so a runaway loop can't burn tokens forever.
- ❌ **Fat, vague spoke prompts.** A spoke that "manages tasks in general" is useless. Each spoke does exactly one thing (scan / evaluate / flag) with a literal, specific instruction.

---

## 🛠️ Capstone Project: Atlas Support's first coordinator (an intake screener)

> This is the main hands-on project for the lesson. You will feel the moment a
> pile of separate agents becomes *one* system with a single brain. Keep it
> small on purpose — the point is the pattern, not a perfect screener.

Atlas Support needs a front door. Before a ticket reaches a human, something has to look it over, decide which checks apply, run them, and produce one recommendation. That is a coordinator. We will build it in Andrew's own worked example — a **job-application screener** — because it is easy to validate, then note how the identical skeleton becomes Atlas Support's ticket intake.

### What you will build

A coordinator agent that takes a **job posting** plus one **résumé** and returns a single hire / no-hire recommendation, by dispatching to three isolated spoke agents and aggregating their outputs. Its pieces map straight to the lesson:

- **The coordinator (hub)** — owns routing, context, aggregation. *(Parts 1–2)*
- **Three spokes, each a tool** — keyword scanner, deep evaluator, red-flag detector. *(Part 3)*
- **A dispatch tool + tool schema** — how the hub "sees" the spokes. *(Part 3)*
- **A stop-reason loop with a max-iteration cap** — the engine. *(Prerequisites, Lesson 4)*
- **An aggregation step** — one coherent verdict with conflicts resolved. *(Part 2)*

### Why this is the perfect practice

| Lesson idea | Where you use it in the screener |
|---|---|
| Hub owns routing | Coordinator prompt: "orchestrate three independent screening agents... run in order, do not skip any" |
| Hub owns context | Each spoke gets only the job posting and/or résumé it needs, nothing about the others |
| Hub owns aggregation | Spoke aggregator merges keyword match + evaluation + red flags into one decision |
| Spoke = tool | `run_keyword_scanner` / `run_deep_evaluator` / `run_red_flag_detector` as tools with schemas |
| Verify, don't trust | You read the actual spoke calls in the output before believing the verdict |

### Milestones (build them in order, each one works on its own)

1. **One spoke, standing alone.** Write the keyword-scanner spoke as a plain function that calls Claude once with a tight prompt — Andrew's is a good model: *"You are a resume keyword scanner. Check whether required skills from the job posting appear explicitly in the resume. For each required skill, output one line. Be literal. Do not infer or extrapolate. Report only what is explicitly stated."* Feed it a job posting and a résumé; confirm it lists each skill as present or absent. This alone is a working, testable unit.
2. **Two more spokes.** Add a **deep evaluator** (judges overall fit and seniority) and a **red-flag detector** (scans the résumé for problems). Each is one Claude call with its own narrow prompt and its own isolated input. Run each by hand; confirm each does one job well.
3. **Expose the spokes as tools.** Write a tool schema for each spoke (`run_keyword_scanner`, `run_deep_evaluator`, `run_red_flag_detector`) and a dispatch function that maps a tool call to the right spoke. Now the hub can "see" them.
4. **The coordinator loop.** Give the coordinator its prompt — *"You are a job application screening coordinator. Your job is to orchestrate three independent screening agents and then aggregate the results. Run all three in order. Do not skip any of them."* — plus the three tools. Run the stop-reason loop: call the API, on `tool_use` dispatch the spoke and feed back the `tool_result`, break on `end_turn`. **Cap it at 10 iterations** so it can't run away.
5. **Aggregate into one verdict.** Have the coordinator combine the three spoke outputs into a single recommendation — hire / no-hire with a short reason — resolving any conflict (e.g. strong skills but a red flag). Andrew's run produced: *"six out of seven strong, no red flags, all core required skills present, seven years experience → hire."*
6. **Verify the run.** Read the trace. Confirm you see "coordinator routes to keyword scanner," then deep evaluator, then red-flag detector, then a final aggregated recommendation — each spoke actually called, with the input you expected. Do not accept the verdict until you have seen the spokes run. *"Just because it said it did, it does not mean it did."*
7. **Stretch goals.** (a) Reframe it as **Atlas Support intake**: same skeleton, spokes become *category classifier*, *urgency scorer*, *duplicate-ticket checker*; the aggregate is a routing decision. (b) Add a second résumé and confirm each screen runs independently per candidate. (c) Sketch (don't build yet) how you would log every hub decision at the choke point — you will do this for real in Lesson 10.

### How you will know you are done

- ✅ Each spoke runs correctly on its own before the coordinator exists.
- ✅ The coordinator calls all three spokes, in order, each with the right input — and you have *read* that in the output, not assumed it.
- ✅ The final result is a single coherent recommendation, not three separate answers stapled together.
- ✅ No spoke calls another spoke; every message goes through the hub.
- ✅ The loop has a max-iteration cap and breaks on `end_turn`.

> 💡 **Keep yourself honest:** the model will say "done" and "you're right."
> Neither is evidence. Your done-criteria are things you *saw the code do*, not
> things it told you it did.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice
> on one idea. Optional and independent; the Capstone already touches all of
> them, so feel free to skip straight to it.

### Exercise 1: Draw the wheel (foundational)
On paper, draw a coordinator with three spokes. Label every arrow. Now try to draw a spoke-to-spoke arrow and write one sentence on what breaks (observability, isolation) when you allow it.

### Exercise 2: Classify the line (intermediate)
Take your Capstone code and, for ten lines you pick, label each as **routing**, **context**, **aggregation**, or **spoke work**. Any line you cannot label cleanly is probably muddled responsibility — a hint to refactor.

### Exercise 3: Break the isolation, then fix it (advanced)
Deliberately pass one spoke's output into another spoke's input. Observe how the second spoke's answer stops being independent. Then remove it and route that information through the coordinator's aggregation step instead — where it belongs.

---

## Cheat sheet

```text
HUB-AND-SPOKE COORDINATOR — one-page recap

TOPOLOGY
  Coordinator (hub) in the middle; spokes on the outside.
  Spokes NEVER talk to each other. Every message goes through the hub.
  The single choke point = free observability + control.

THE COORDINATOR'S THREE JOBS
  1. ROUTING       decide which spoke handles which subtask (can be
                   model-driven: "simple -> one agent; multi-step ->
                   sequential; independent -> parallel")
  2. CONTEXT       decide what each spoke sees; spokes are isolated by
                   default and only know what the hub injects
  3. AGGREGATION   collect all spoke outputs -> one coherent answer,
                   resolve conflicts

TASK LIFE CYCLE (all owned by the hub)
  decompose -> delegate -> aggregate   (+ choose spokes by complexity)

A SPOKE IS JUST A TOOL
  tool schema the hub sees:  run_<spoke>(inputs) -> result
  implementation:            one Claude call + one narrow prompt
  DON'T make "router"/"decomposer" a spoke — those are the hub's jobs.

THE ENGINE
  stop-reason loop: call API -> on tool_use run spoke, feed tool_result
                    -> break on end_turn
  ALWAYS cap iterations (e.g. 10) even with a break.

THE RULE
  "Just because it said it did, it does not mean it did."
  Run it, read the spoke calls, THEN believe the verdict.
```

## How this connects to the rest of the course

- **Earlier, Module 1 · Lessons 3–4:** the stop-reason loop and the max-iteration cap. The coordinator *is* that loop, now driving other agents.
- **Earlier, Module 3 · Lesson 7 (Code-driven vs model-driven decisions):** routing is the model-driven decision you just wrapped a structure around.
- **Next, Module 3 · Lesson 9 (Task decomposition done right):** you saw the hub *decompose* work here; next you make sure the decomposition covers everything (non-overlapping partitions, enforced coverage) so entire subtasks don't get silently dropped.
- **Later, Module 3:** you will make spokes run in parallel (Lesson 13), instrument the choke point with logging and observability (Lesson 10), add failure recovery (Lesson 11), and finally port this exact coordinator to the Claude Agent SDK, where — as Andrew notes — "this would be greatly simplified" (Lesson 12). Every one of those builds on the hub you built today.

---

*Source: reconstructed from the CCA-F course by Andrew Brown (ExamPro). Code
snippets and diagrams are illustrative reconstructions of the patterns described
in the course. Adapt them to the current SDK.*
