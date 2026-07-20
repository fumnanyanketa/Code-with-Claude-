# Module 3 · Lesson 9: Task decomposition done right

> **Course:** Claude Certified Architect: Foundations, a self-paced course
> **Module 3:** Orchestration: multi-agent architectures — one coordinator, many specialised spokes, working as a system
> **Speaker:** Andrew Brown, ExamPro
> **Source:** Reconstructed from the CCA-F course by Andrew Brown (ExamPro) · [full transcript](../../transcripts/cca-f-full-course.txt)
> **Estimated time:** 45 to 60 minutes (read plus lab)

---

## In one sentence

When a coordinator splits a job for its sub-agents, three things decide whether the result is any good: the split leaves **no gaps** (every part of the ask is covered), the slices **do not overlap** (no two agents redo the same work), and the coordinator runs **only the agents this input actually needs** (so you do not burn tokens on spokes that answer nothing).

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone Project** where you add a *partition planner* and a *dynamic-selection* step to Atlas Support's coordinator, so a messy multi-part customer request gets covered completely, with no slice done twice and no spoke run for nothing. Everything before the Capstone teaches the three moves you will use there. If you want to see the finish line first, jump to the **"Capstone Project"** section, then come back.

## First-principles companion

> 💡 **The durable idea behind this lesson.** Coordinators and sub-agents are new; the idea of splitting a problem into pieces that are *mutually exclusive* (no overlap) and *collectively exhaustive* (no gaps) is decades old. It even has a name.
>
> - **MECE — "Mutually Exclusive, Collectively Exhaustive"** — from Barbara Minto's *The Pyramid Principle* (the structured-thinking method McKinsey teaches). MECE is exactly the two-sided test you will apply to a partition: do the slices overlap, and do they cover everything? Every good decomposition in this lesson is just MECE with tokens attached.

## A few plain-language basics first

This lesson uses some everyday terms. Here they are in plain words:

- **Coordinator (hub-and-spoke):** one agent that owns routing, context, and putting the answers back together. It hands work to smaller agents ("spokes") that are exposed to it as tools. You built one last lesson.
- **Sub-agent / spoke:** an agent spawned by the coordinator, usually with its *own isolated context* — meaning it can only see the little slice of the task it was handed, and nothing else.
- **Task decomposition:** the act of breaking one big request into smaller subtasks to hand out. "Decompose" just means "break apart."
- **Partition:** one non-overlapping slice of the whole job. If you cut a pizza so no two people get the same piece and no piece is left on the tray, you have partitioned it.
- **Gate:** a checkpoint the coordinator must pass through — usually a tool it is forced to call — that verifies something (like "did you cover everything?") before it is allowed to continue.
- **Dynamic selection / routing:** deciding *on the fly*, from the actual input, which spokes to run — instead of always running all of them.
- **Token:** the unit a model reads and writes in, about ¾ of a word; you are billed per token. Running a spoke that answers nothing still costs tokens.

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

Last lesson you got a coordinator *working*. This lesson is about getting its decomposition *right*, which is a different and harder thing. Here is the trap, in Andrew's words: **"when Claude decomposes a task, it can only delegate what it thinks to ask for."** A spoke cannot rescue a bad split, because — as Andrew stresses — **"each sub-agent only sees its own isolated context. None of them can flag what's missing."** If the coordinator forgets a subtopic, that subtopic simply never gets researched, and no one downstream will ever notice. Meanwhile, if the coordinator plays it safe and runs *every* spoke on *every* request, you pay for a pile of answers to questions nobody asked. This lesson gives you the three moves that fix both failures — and the honesty to know whether they actually helped.

## Learning objectives

By the end of this lesson you will be able to:

1. Diagnose a **narrow decomposition** — spot when a split has silently dropped whole subtopics, and explain why the spokes cannot catch it themselves.
2. Enforce **coverage** with a gate — a tool the coordinator must call before delegating, and/or a check at the aggregate step, that verifies nothing was missed.
3. Write a **partition planner** step that emits non-overlapping slices as structured JSON (agent, scope, exclusions), so no two spokes redo the same work.
4. Add **dynamic selection** so the coordinator runs only the spokes a given input needs, and understand where the routing rule should live once you also have a planner.
5. Judge whether any of it actually improved the result, instead of trusting that output means success.

## Prerequisites

- **Module 3 · Lesson 8 ("Hub-and-spoke: your first coordinator")** — you need a working coordinator that delegates to spoke tools. This lesson modifies that coordinator.
- Comfort reading a coordinator's system prompt and running it from `main.py` (Modules 1–2).
- A rough feel for JSON (types, arrays, required fields) from the structured-output lesson.

---

## Part 1: Narrow decomposition — the gap you cannot see

Start with the failure. Andrew gives a research coordinator this brief:

> *"Give me a comprehensive analysis of the EV market."*

The coordinator breaks it into subtasks and delegates:

- Research EV sales figures
- Research EV battery technology
- Research major EV manufacturers

Looks reasonable. Now look at what never got researched, because no one asked for it:

- Charging infrastructure
- Government policies and subsidies
- The second-hand EV market
- Consumer sentiment and adoption barriers
- Supply chains (lithium, cobalt)
- Grid-capacity implications

Six whole topics, gone. And here is the part that makes it dangerous rather than merely incomplete: **nobody in the system can tell.** The sales-figures spoke only sees "research sales figures." The battery spoke only sees "research battery tech." As Andrew puts it, **"each sub-agent only sees its own isolated context. None of them can flag what's missing."** The coordinator moves on, aggregates three tidy answers, and hands you a confident report with a hole in the middle.

> 🔑 **A narrow split is invisible from the inside. The coordinator can only delegate what it thought to ask for, and the spokes can only answer what they were handed — so a dropped subtopic leaves no trace anywhere.** The fix has to live at the coordinator, before or after delegation, never in the spokes.

### Why "just write a better prompt" is not enough

The obvious reflex is to write a more specific brief. That helps, and you should do it — but a prompt can still miss things, and you get no warning when it does. Andrew's point is that a good architecture does not *rely* on the brief being perfect. It adds a checkpoint that catches a weak split even when the prompt let one through. That checkpoint is the subject of Part 2.

## Part 2: Coverage gates — force the system to check its own work

Andrew describes **two** places you can bolt on a coverage check. You can use either or both.

**Gate 1 — before delegating (a tool gate).** Make the coordinator submit its subtask breakdown *for review* before it is allowed to hand anything out. In Andrew's words: *"when the agent goes and does a task it's going to say, 'oh, did you submit a subtask breakdown for review for delegating?' Well, then trigger this tool"* — and the tool checks the breakdown against what a complete answer needs. Because the check is a separate tool, it is decoupled from the brief: even if your carefully worded coordinator prompt fails, the gate still fires. *"This gives you a guarantee,"* as he puts it.

**Gate 2 — after aggregating (an aggregate check).** The second safeguard runs at the other end. After the spokes report back and the coordinator is about to write the final answer, it checks: *"hey, did you make sure, before writing the answer, that you met these things?"* If a required dimension is missing, it goes back and fills it instead of shipping the hole.

Together these give you, in Andrew's summary, **"two different safeguards for improving over narrow task decomposition"** — one at the entrance, one at the exit.

> ✅ **What to do about it:** bake the coverage question *into the coordinator prompt itself* as a required step. Andrew's "better coordinator" does exactly this. Instead of listing fixed subtasks, it says: *"generate an initial list of screening angles. Ask yourself what perspectives, stakeholders, or dimensions are missing. Add screening angles to cover those gaps only. Then begin delegating."* The instruction "ask yourself what is missing, add angles to cover the gaps, **then** delegate" is a soft gate written in prose; the tool gates above are the hard version for when prose is not enough.

Here is that pattern as an illustrative coordinator prompt (reconstructed — adapt to your SDK):

```text
You are a screening coordinator.

STEP 1 — Plan coverage (do NOT delegate yet):
  - Generate an initial list of screening angles.
  - Ask yourself: what perspectives, stakeholders, or dimensions
    are MISSING from that list?
  - Add angles ONLY to cover those gaps.

STEP 2 — Gate: call check_coverage(angles) before delegating.
  If it returns "gaps: [...]", go back to STEP 1.

STEP 3 — Delegate one screening-agent call per angle.

STEP 4 — Before writing the final report, confirm every angle
  was answered. If not, delegate the missing ones.
```

> 💡 **A note on when this pattern earns its keep.** Andrew is honest that on his own hiring example — three fixed checks (keywords, deep evaluator, red-flag detector) fed one resume — the gap-hunting did not add much: *"it's just like there's these three things... it's not conducting research."* The narrow-decomposition problem bites hardest when the coordinator is **ingesting more than one source** or **doing open-ended research**, where the space of "what to look at" is genuinely large. Reach for coverage gates when the ask is broad, not when it is three known boxes to tick.

## Part 3: Dynamic selection — run only the spokes this input needs

Coverage pushes toward *more*: do not miss anything. Dynamic selection pulls the other way: do not run anything you do not need.

The waste is easy to picture. If your coordinator *"runs the entire pipeline for every single possible spoke in a sequence,"* Andrew notes, *"you are consuming as much as you can"* — every spoke fires on every request, whether or not it has anything to contribute. A simple, factual request that one spoke could answer instead pays for five.

The fix is to tell the coordinator to *route*: **"think about what kind of pathing it needs or what kind of routing it should have,"** and give it concrete conditions under which each path applies. Andrew's routing guidance, from the run that worked, reads like this:

```text
Routing guidance — adapt to what you observe; do not apply mechanically.

- Simple factual match?  -> skip the keyword scan, go straight to the
                            decision agent.
- Non-traditional background? -> run the transferable-skills angle.
- ...

Never invoke a screening agent unless it answers a REAL question.
```

That last line is the whole idea in one sentence: **never run a spoke that answers nothing.** When it worked, Andrew's reaction was simply, *"we wasted no tokens. There's no reason we can't do that. We don't have to prompt everything."*

> 🔑 **Coverage and selection are two ends of the same dial. Coverage says "leave no gap"; selection says "spend nothing on non-answers." A good coordinator turns both knobs: it asks what is missing, and it refuses to run what is pointless.**

And, exactly as with coverage, you can back the prompt with a **tool gate**: *"you could set up a tool that says, 'hey, did you do a good job here?'"* — a checkpoint that inspects the routing decision the same way the coverage gate inspects the subtask list.

## Part 4: Partitioning — non-overlapping slices, planned as JSON

Parallel research has a third, distinct failure. As Andrew puts it: *"if you give three research agents the same brief, you get three overlapping answers and wasted tokens."* Three agents told "research the EV market" will each research *the EV market* — you pay triple for one report.

The fix is partitioning: **"carve up the scope so each agent owns a distinct slice."** And rather than carve by hand, you have the model emit the partition as **structured JSON** in a dedicated planning step, so the slices are explicit, printable, and checkable. Andrew's screening-partition planner:

```text
You are a screening-partitioning planner.
Given a job posting and a resume, output a JSON array of
NON-OVERLAPPING screening partitions.

Each partition object must have:
  - agent:   which spoke runs it
  - scope:   what this partition covers
  - excludes/rules: what it must NOT touch (that is another partition's job)

Design partitions so that TOGETHER they cover all relevant
hiring questions. No two partitions may share the same aspect.
Include ONLY partitions genuinely needed for this candidate.
```

Read the last two lines carefully — they are MECE in disguise. *"Together they cover all relevant questions"* is collective exhaustiveness (no gaps). *"No two partitions may share the same aspect"* is mutual exclusivity (no overlap). *"Only partitions genuinely needed"* folds dynamic selection into the plan.

Two practical touches Andrew insists on:

- **Print the structure.** Emit the JSON plan to the console *"so the human can see it on the run of the coordinator."* A partition you can read is a partition you can audit. If two slices look like twins, you caught it before spending a single spoke's tokens.
- **Make the coordinator downstream "dumb" on purpose.** Once the plan exists, the coordinator's job shrinks to obedience: *"invoke exactly one screening-agent call per partition — no more, no less. Do not invent additional screening angles beyond the partitions provided. They were designed to cover all relevant dimensions without overlap."*

### Where does routing live once you have a planner?

This is the subtle bit, and Andrew works through it on camera. Once you have *both* a partition planner *and* dynamic-selection routing, they can end up fighting: *"you create a conflict of two places fighting over what gets evaluated."* If the planner decides which slices exist **and** the coordinator re-decides which to run, they contradict each other.

The resolution: **the routing rule belongs to the planner; the coordinator stays dumb.** The planner is where "only create a partition if the rules say this candidate needs it" lives. The coordinator downstream, in Andrew's words, *"is correct to be dumb selection, because the decision was already made upstream."* Selection happens once, when the plan is built — not again when the plan is executed.

```text
        ┌────────────────────┐
input → │ Partition planner  │  ← routing + coverage rules live HERE
        │  (emits JSON plan)  │     "include only needed, non-overlapping
        └─────────┬──────────┘      slices that together cover everything"
                  │  prints plan for the human
                  ▼
        ┌────────────────────┐
        │ Coordinator (dumb) │  ← one call per partition, invents nothing
        └─────────┬──────────┘
                  ▼
         spoke · spoke · spoke   (each owns one distinct slice)
                  ▼
             aggregate → optional coverage gate → answer
```

> 🔑 **Decide once, execute plainly. Put the "what to run and why" logic in one place — the planner — and let the coordinator that executes the plan be gloriously stupid. Two brains arguing over the same decision is worse than one.**

## Part 5: The move that ties them together — build it, then verify it

Andrew repeats one warning through this entire stretch, and it is the real lesson: **producing output is not the same as producing a good decomposition.** *"Just because it will produce something doesn't mean that it's useful."* The coordinator will always hand you a confident answer. Whether the split behind it was sound is a separate question that the answer itself cannot tell you.

So how do you actually know? You test it against reality. *"To test this you'd actually have to create sample data, run it, and then adjust — say, 'hey, this is not how I would have judged it.'"* Dump every spoke's output, save the final report, and compare the narrow run against the partitioned run on the *same* input. Andrew's own instinct, repeated: *"we should be dumping all these logs out and then comparing them."* Without that, you have a system that runs, not a system you trust.

> 💡 **The judgment quote to keep.** *"If you are doing this for real, write these things by hand yourself. Use your brain... Garbage in means garbage out. Just because this thing works doesn't mean that it's well designed."* The techniques in this lesson are scaffolding for thinking, not a substitute for it. And there are no rules — Andrew is explicit that a **hybrid** (some logic in the coordinator prompt, some in plain code) is completely fine: *"there's nothing wrong with it. There's no rules here, folks."*

---

## Key takeaways

1. **A narrow split is invisible from the inside.** The coordinator can only delegate what it thought to ask for; spokes only answer what they were handed. Dropped subtopics leave no trace — so the fix must live at the coordinator.
2. **Gate coverage in two places.** Before delegating (a tool that reviews the subtask breakdown) and after aggregating (a check that every dimension was answered). Prose-level "ask what's missing, then delegate" is the soft version; a forced tool call is the hard guarantee.
3. **Select dynamically to stop the bleed.** Give the coordinator routing conditions and one rule above all: *never invoke a spoke that answers no real question.* That is where the token savings come from.
4. **Partition as printed JSON.** Each slice names its agent, scope, and exclusions; together they cover everything, no two overlap, only needed ones exist. Print it so a human can audit the split before it costs anything. This is MECE.
5. **Decide once, execute plainly.** With both a planner and routing, the routing rule belongs to the planner and the executing coordinator stays dumb — two brains over one decision only fight.
6. **Output ≠ good.** The only way to know a decomposition helped is to run narrow vs. improved on the same sample data and compare the dumped logs. Build it, then verify it.

## Common pitfalls

- ❌ **Trusting a confident report.** The system always produces *something*. If you never diff a narrow run against an improved one on identical input, you are guessing. Dump logs and compare.
- ❌ **Trying to fix a narrow split inside the spokes.** They cannot see past their own slice. Coverage lives at the coordinator — before or after delegation — never in the spoke.
- ❌ **Running every spoke on every request "to be safe."** That is the token bleed dynamic selection exists to stop. Route; do not fan out blindly.
- ❌ **Putting routing logic in two places.** If the planner picks the slices *and* the coordinator re-picks which to run, they conflict. Choose once, upstream; keep the executor dumb.
- ❌ **Reaching for coverage gates on a three-box task.** The gap-hunting pattern shines on broad, multi-source, research-style asks. On "run these three fixed checks," it mostly adds tokens — Andrew watched it add nothing on his own hiring example.
- ❌ **Hand-editing overlapping partitions and never printing them.** If you cannot see the plan, you cannot catch the twins. Emit the JSON to the console every run.

---

## 🛠️ Capstone Project: Atlas Support's partition-planner + dynamic-selection coordinator

> This is the main hands-on project for the lesson. You will make Atlas Support's coordinator handle a messy, multi-part customer message correctly: every part addressed, nothing done twice, and no spoke run for nothing. Keep it small — the point is to *feel* the three moves, not to build a call centre.

### What you will build

**Atlas Support** is the multi-agent support system this course builds across every module. Its coordinator routes a customer message to specialist spokes — say **billing**, **technical/auth**, and **account/plans**. Real customers send tangled requests like:

> *"I was double-charged last month, my API key suddenly stopped working, and while you're at it I want to upgrade to the Team plan."*

That is three genuinely different jobs. A narrow split drops one; a naive coordinator runs all spokes on every message even when someone just asks "how do I reset my password." You will add a **partition planner** (non-overlapping slices as printed JSON), a **coverage gate**, and **dynamic selection** (only the needed spokes), then prove it with two contrasting inputs.

Its pieces, each mapped to a lesson idea:

- A **partition planner** step that emits JSON slices — Part 4.
- A **coverage gate** so no part of the request is dropped — Part 2.
- **Dynamic-selection rules** in the planner so single-issue messages run one spoke — Parts 3 & 4.
- A **dumb coordinator** that runs exactly one call per partition — Part 4.
- A **narrow-vs-improved comparison** on the same message — Part 5.

### Why this is the perfect practice

| Lesson idea | Where you use it in Atlas Support |
|---|---|
| Narrow split is invisible (Part 1) | Milestone 1: watch a subtopic get silently dropped |
| Coverage gate (Part 2) | Milestone 2: a tool that rejects an incomplete plan |
| Dynamic selection (Part 3) | Milestone 4: a single-issue message runs one spoke |
| Partition as JSON (Part 4) | Milestone 3: printed, auditable, non-overlapping slices |
| Decide once, execute dumb (Part 4) | Milestone 5: coordinator obeys the plan, invents nothing |
| Output ≠ good (Part 5) | Milestone 6: diff narrow vs. improved on one input |

### Milestones (build them in order, each one works on its own)

1. **Reproduce the gap.** Copy your Lesson 8 coordinator into a new `atlas_decomposition/main.py`. Feed it the three-part message above with a *narrow* prompt that lists only "billing" and "technical." Run it and confirm the upgrade request is silently never handled. Smallest win: you have seen a dropped subtopic with your own eyes.
2. **Add a coverage gate.** Add a `check_coverage(parts)` tool the coordinator must call *before* delegating; have it return any request-parts not matched to a spoke. Make the prompt loop back if `check_coverage` reports gaps. Smallest win: the same three-part message now refuses to proceed until all three parts are assigned.
3. **Add a partition planner.** Insert a planning step whose whole job is to emit a JSON array of partitions — each with `agent`, `scope`, and `excludes` — that together cover the message with no two slices overlapping. **Print the JSON** on every run. Smallest win: you can read the slices and confirm billing, auth, and upgrade are three clean, non-overlapping partitions.
4. **Add dynamic selection.** Put routing rules *in the planner*: it emits a partition only for issues the message actually raises, and it never emits one that answers no real question. Feed it a *single*-issue message ("how do I reset my password") and confirm the plan contains exactly one partition. Smallest win: one input yields three slices, another yields one — from the same code.
5. **Make the coordinator dumb.** Change the coordinator that runs the plan to "invoke exactly one spoke call per partition; invent no angles beyond the plan." Confirm routing decisions now live only in the planner. Smallest win: removing all routing prose from the coordinator changes nothing, because the decision already happened upstream.
6. **Verify by diffing.** Run the narrow (Milestone 1) and improved (Milestones 3–5) versions on the *same* three-part message. Dump every spoke's output and both final replies to files. Read them side by side and write two sentences on whether the improved version is genuinely better. Smallest win: a judgment backed by logs, not vibes.
7. **Stretch goals.** Add an aggregate-level gate that re-checks coverage *after* the spokes reply. Add a partition-overlap tool that flags two slices sharing an aspect before delegation. Try a **hybrid**: compute the obvious partitions in plain Python and let the planner only fill the ambiguous ones.

### How you will know you are done

- ✅ The three-part message is fully addressed — billing, auth, **and** upgrade — with no part dropped.
- ✅ The printed partition JSON shows non-overlapping slices, and the single-issue message produces exactly one partition.
- ✅ Removing routing prose from the executing coordinator does not change behaviour (the decision lives in the planner).
- ✅ You have saved logs from a narrow run and an improved run on the same input, and a written two-sentence verdict comparing them.

> 💡 **Keep yourself honest:** do not declare victory because it "ran." Andrew's rule applies directly — *"just because this thing works doesn't mean that it's well designed."* Milestone 6 (the diff) is the one that actually proves anything; do not skip it.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice on one idea. Optional and independent; the Capstone already touches all of them, so feel free to skip straight to it.

### Exercise 1: Find the missing topics (foundational)
Take the brief *"give me a comprehensive analysis of remote-work policy."* Write the three subtasks a narrow coordinator would produce, then list five subtopics it would silently drop. This is Part 1 with a fresh topic — practise seeing the invisible gap.

### Exercise 2: Write the gate (intermediate)
Draft the JSON input schema for a `check_coverage` tool: it takes a list of subtasks and a list of required dimensions, and returns the dimensions not covered. Then write the one prompt line that forces the coordinator to call it before delegating.

### Exercise 3: Resolve the two-brain conflict (advanced)
You have a partition planner *and* a coordinator, and both contain routing rules — so they disagree on one run. Rewrite the pair so the routing rule lives in exactly one place. Justify in two sentences why the executor should be the dumb one, quoting the "decision was already made upstream" idea.

---

## Cheat sheet

```text
TASK DECOMPOSITION DONE RIGHT — the three moves

THE FAILURE (narrow split)
  "Claude can only delegate what it thinks to ask for."
  Spokes see only their own slice -> a dropped subtopic
  leaves NO trace. Fix lives at the coordinator, not the spoke.

MOVE 1 — COVERAGE (leave no gap)
  Gate A (before delegating): tool reviews the subtask list.
  Gate B (after aggregating): "did I cover every dimension?"
  Prompt form: "list angles -> ask what's MISSING -> add to fill
  gaps -> THEN delegate."  Best on broad/multi-source asks.

MOVE 2 — DYNAMIC SELECTION (spend nothing on non-answers)
  Give routing conditions. One rule above all:
  "Never invoke a spoke unless it answers a REAL question."
  = the token savings.  Back it with a tool gate if needed.

MOVE 3 — PARTITION (no two slices overlap)
  Planner emits JSON: {agent, scope, excludes} per slice.
  Together = cover everything (no gaps).
  No two share an aspect (no overlap).  Only needed ones exist.
  PRINT the JSON so a human can audit it.
  = MECE (Mutually Exclusive, Collectively Exhaustive).

WHERE ROUTING LIVES (planner + coordinator together)
  Routing rule -> PLANNER (decide once, upstream).
  Coordinator  -> DUMB: one call per partition, invent nothing.
  Two brains over one decision = conflict.

THE DISCIPLINE
  Output != good.  Run narrow vs. improved on the SAME input,
  dump the logs, compare.  Hybrid (prompt + code) is fine.
  "Garbage in means garbage out."
```

## How this connects to the rest of the course

- **Earlier, Module 3 · Lesson 8 ("Hub-and-spoke: your first coordinator"):** gave you a coordinator that delegates to spokes. This lesson made that delegation *correct* — complete, non-overlapping, and selective.
- **Next, Module 3 · Lesson 10 ("Refinement loops and observability"):** the partition plan and coverage gate become the things a refinement loop iterates on — run, evaluate coverage, fill only the gaps, repeat up to a max. The coverage check you built here is exactly what tells the loop when to stop.
- **Later, in the reliability and escalation modules:** the "build it, then verify it" discipline from Part 5 grows into real reliability checks, and a coordinator that knows what it did *not* cover is the one that knows when to escalate to a human.

---

*Source: reconstructed from the CCA-F course by Andrew Brown (ExamPro). Code snippets and diagrams are illustrative reconstructions of the patterns described in the course. Adapt them to the current SDK.*
