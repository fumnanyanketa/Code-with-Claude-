# Module 3 · Lesson 13: Running agents in parallel

> **Course:** Claude Certified Architect: Foundations, a self-paced course
> **Module 3:** Orchestration: multi-agent architectures: turn one agent into a reliable coordinated system
> **Speaker:** Andrew Brown, ExamPro
> **Source:** Reconstructed from the CCA-F course by Andrew Brown (ExamPro) · [full transcript](../../transcripts/cca-f-full-course.txt)
> **Estimated time:** 45 to 60 minutes (read plus lab)

---

## In one sentence

When several pieces of work do not depend on each other, you can make your coordinator fire all of its sub-agents at once instead of one after another — but you have to *ask* for that in the prompt, each parallel agent runs its own private loop you cannot easily watch, so per-run logs become the only window you have.

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone
> Project** where you fan **Atlas Support** out across several sub-agents that
> each research an independent slice of a customer problem *at the same time*,
> then aggregate their findings — with one log file per agent per run so you can
> see what is happening. Everything before the Capstone teaches the skills you
> will use there. If you want to see the finish line first, jump to the
> **"Capstone Project"** section, then come back.

## First-principles companion

> 💡 **The durable idea behind this lesson.** SDKs and model names change, but
> "split independent work, run it concurrently, then recombine" is one of the
> oldest ideas in computing.
>
> - **[MapReduce: Simplified Data Processing on Large Clusters](https://research.google/pubs/pub62/)** (Dean & Ghemawat, 2004). The canonical *fan-out / fan-in* (also called *scatter-gather*) pattern: partition a job into independent pieces, process them in parallel, then merge. A parallel coordinator is the same shape — the sub-agents are the "map," the coordinator's dedupe-and-rank step is the "reduce."
> - **[Amdahl's Law](https://en.wikipedia.org/wiki/Amdahl%27s_law)** — the timeless reminder that parallelism only speeds up the part of the work that is actually independent, and coordination is never free.

## A few plain-language basics first

This lesson uses some everyday terms. Here they are in plain words:

- **Agent:** an AI that takes a series of actions on its own toward a goal, rather than answering in one shot.
- **Agentic loop:** the repeating cycle an agent runs — gather context, take action, verify — until the task is done.
- **Coordinator (hub-and-spoke):** one agent that owns routing, context, and aggregation, and delegates to *sub-agents* ("spokes") that are exposed to it as tools.
- **Sub-agent:** an agent spawned by another agent, usually with its own isolated context and its own loop.
- **Claude Agent SDK vs Anthropic SDK:** the *Agent SDK* is the higher-level library for building agents (decorator tools, sub-agents, hooks); the *Anthropic SDK* is the lower-level library for calling the model API directly. The Python Agent SDK sometimes lags the TypeScript one.
- **Agent (task) tool:** the built-in tool the Agent SDK gives your coordinator so it can spawn a named sub-agent. (The docs call it the *task* tool; in the SDK it is the *agent* tool — a naming quirk you met last lesson.)
- **Parallel vs sequential:** *sequential* means do one thing, wait for it to finish, then do the next; *parallel* means start several at once and let them run together.
- **Partition:** a slice of the work that does not overlap with the other slices — one axis of research, one region, one document set.
- **Aggregate:** collect the separate results back into one combined answer (here: merge, de-duplicate, and rank).
- **`stdout` / `tail`:** `stdout` is the stream a program prints to; `tail -f <file>` follows a file live, printing new lines as they are written — how you "watch" a log.

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

Last lesson you ported your coordinator to the Agent SDK and used the Agent tool to spawn isolated sub-agents. But it called them **one at a time**. If five sub-agents each do independent research, running them sequentially means the user waits for all five to finish *in a row*. Running them together can cut that wait dramatically — and this is exactly the kind of orchestration the exam's Domain 1 wants you to reason about. The catch, and the real lesson, is what Andrew hits repeatedly here: the moment several agents run at once, "I have no output or logging and so I have no sense of ... if the agents are stuck in a loop or if they are going to finish soon or what they're even doing." Speed you get almost for free; **visibility you have to build.**

## Learning objectives

By the end of this lesson you will be able to:

1. Explain why the Agent tool does **not** run sub-agents in parallel automatically, and prompt a coordinator to fan out versus stay sequential.
2. Decide, per task, whether the sub-agents' work is independent enough to run at once.
3. Describe what "each agent runs its own loop" means and why that makes sub-agents hard to observe.
4. Add per-run, per-sub-agent log files so you can `tail` a fleet of parallel agents and know something is happening.
5. Recognise that a lost or empty result is usually a **formatting/aggregation** bug, not a parallelism bug — and keep the two separate when you debug.

## Prerequisites

- **Module 3 · Lesson 12** (the Agent SDK and the Agent/task tool) — you need a working coordinator with at least one named sub-agent definition.
- **Module 3 · Lesson 8** (hub-and-spoke) and **Lesson 9** (non-overlapping partitions) — parallelism only works when the partitions do not depend on each other.
- Python, the Claude Agent SDK installed, and an API key (Module 0).

---

## Part 1: A quick reminder that the docs can be wrong

Before the parallelism work, Andrew is still poking at agent-definition fields from last lesson, and he runs into the theme that runs through this whole course. He asks Claude for *all* the fields on an agent definition in Python, gets a short list, and does not trust it. He checks the TypeScript SDK and finds more: "the type set has significantly more fields [than] the Python. If you need these capabilities, you need to use the [TypeScript SDK]. Wow, isn't that interesting?"

His takeaway is the one to carry into everything below:

> "It's good that we know, right? So if I had not checked that, then I would have thought that's all there was."

> 🔑 **Verify by building, not by reading.** The docs "weren't built for humans,"
> as Andrew puts it, and the Python SDK lags the TypeScript one. Whenever this
> lesson tells you the SDK "can" or "can't" do something, the honest answer is
> "at the time of recording, and only until you check." Treat every capability
> claim as a hypothesis you confirm by running code.

## Part 2: The Agent tool is not automatically parallel — you ask for it

Here is the single most surprising fact of the lesson. You might assume that if a coordinator has five independent sub-agents to call, the SDK is smart enough to run them together. It is not. By default the coordinator "calls research agent sequentially one at a time."

So how do you get parallelism? As Andrew says, "the way you do that when you're using the Agent SDK is you just simply tell it that you want to do it." You **prompt** for it. The coordinator's prompt is where you say: these calls are independent, so make them all in a single response instead of waiting between them.

He shows the two halves of a good prompt — not just "you *may* run in parallel" but *when* to and *when not* to:

- Give **examples of tasks that can be run in parallel** (independent research on five different axes), and
- Give the case where you would run **sequentially** instead (when one step's input depends on a previous step's output).

> "It's up to the coordinator to decide if they want to do them all at the same time or not."

That is the mental model: you are not flipping a `parallel=true` switch. You are giving the coordinator a decision rule, and it chooses per task. The reconstructed prompt language that flips the behaviour looks like this:

```text
# Illustrative — the key lines in the coordinator prompt

In a SINGLE response, call the research_agent tool simultaneously for ALL
five axes. The axes are independent — no axis depends on another's result —
so DO NOT wait between calls. Delegate to all of them at once, then call
record_findings on the combined results.

(Run sub-agents SEQUENTIALLY only when a later agent needs an earlier
agent's output as its input.)
```

The phrases doing the work are "in a single response," "simultaneously," and "do not wait between calls." As Andrew narrates while reading the generated code: "in a single response call research agent simultaneously [for] all axes ... we're telling it to do this. Do not wait but delegate to all of them. That's the key thing that we were asking it to do."

> 🔑 **Parallelism is a prompt, not a flag.** The Agent tool runs sub-agents one
> at a time unless the coordinator's prompt tells it to issue all the calls in a
> single response. No prompt, no parallelism.

> ✅ **What to do about it:** in your coordinator prompt, name the independent
> tasks explicitly, say "call them in a single response, simultaneously, do not
> wait," and add the sequential exception so the model does not parallelise work
> that actually has a dependency.

### How do you *know* it parallelised?

Honestly? At first, you barely can. Andrew asks the exact right question — "How do we know that's being parallelised?" — and the best signal he has is the coordinator announcing "all in [a single] turn" and "the agent is saying it's starting them all simultaneously." He is candid: "The only thing that will be hard here is to really observe that they're running all at the same time ... I'm not sure exactly how we would monitor that." That discomfort is not a mistake on his part — it is the problem the rest of the lesson exists to solve.

## Part 3: Each agent runs its own loop (which is why you can't see it)

Recall the agentic loop: gather context → take action → verify, repeated until done. When your coordinator spawns a sub-agent through the Agent tool, that sub-agent does **not** borrow the coordinator's loop. It runs its **own**.

> "Each agent tool runs in [its] own loop ... each agent is running at the same
> time — or can, if you specify it — obviously in parallel, and we might not be
> able to see what the internal loop is doing."

Picture five sub-agents firing at once. Each is independently deciding to search, read a result, maybe search again, and eventually report back:

```text
                 ┌─────────────── coordinator ───────────────┐
                 │  one prompt, one response, five tool calls │
                 └───┬───────┬───────┬───────┬───────┬────────┘
                     │       │       │       │       │      (all issued at once)
                 ┌───▼──┐┌───▼──┐┌───▼──┐┌───▼──┐┌───▼──┐
   sub-agent →   │axis 1││axis 2││axis 3││axis 4││axis 5│   each with its OWN loop:
   own loop      │ g→a→v││ g→a→v││ g→a→v││ g→a→v││ g→a→v│   gather→act→verify…
                 └───┬──┘└───┬──┘└───┬──┘└───┬──┘└───┬──┘
                     └───────┴───┬───┴───────┴───────┘
                          ┌──────▼───────┐
                          │  aggregate:  │  merge → de-duplicate → rank
                          │  coordinator │
                          └──────────────┘
```

The isolation is a feature — each sub-agent gets its own clean context so they do not pollute one another. But it is also the source of the pain. Andrew wanted plain internal logging of what each loop was doing "or at least track my spend or help re-rou[te] it if it's going off tracks, but you can't ... that is just a limitation of how it works right now." He suspects, without being sure, that "sub-agents you have to enable streaming, where the parents ... already stream the information to you and sub-agents don't."

> 🔑 **Isolation cuts both ways.** A sub-agent's own loop keeps its context clean
> *and* keeps its work invisible. With one agent you watch the stream; with five
> parallel agents you get silence until they report back.

> 💡 **A judgment note, not a gotcha.** Andrew is careful to say he has *not*
> verified the streaming claim — "I don't know if this is true or not, we'd have
> to verify it." Hold SDK limitations loosely: they are true at the time of
> recording and may already be fixed. If you truly need per-step visibility for
> production, he floats the escape hatch used throughout this course: "roll your
> own using the ... lower-level Anthropic client."

## Part 4: The fix — one log file per agent, per run

If the SDK will not hand you a live view, you build a modest one. Andrew's approach is exactly what you would reach for: have each sub-agent write to its **own log file, scoped to this run**, so you can follow all of them at once.

The naming scheme he dictates:

```text
logs/run-<ISO-timestamp>-<sub-agent-name>.log
```

One directory of logs per pipeline run; inside it, one file per sub-agent that was spun up, each line time-stamped. His instruction, in his words: "dump logs to each agent run — each run of our coordinator — and then in there have individual logs for each sub-agent that is spun up ... e.g. `logs/run/<ISO timestamp>/<sub-agent name>.log`."

Once the files exist, watching a whole fleet is one command. Because every file for this run starts with `run-`, you follow them all with a wildcard:

```bash
# Illustrative — follow every sub-agent's log for the current run, live
tail -f logs/run-*.log
```

Andrew's live reaction when it finally works: "there they go. There we go ... now what I can do is `tail -f logs run asterisk.log`. And so now it will show us all the logs ... if there are any changes that are happening here, they'll get propagated." He splits his terminal, refreshes, and can finally *see* the agents fire up: "now we can see all the agents are starting ... that's a lot more useful."

It is not perfect — he still can't see the reasoning *inside* each loop, and wishes the files "were named a little bit better." But it clears the bar he actually needed: proof that something is happening and that the run is not wedged.

> ✅ **What to do about it:** give every sub-agent a logger that writes to
> `logs/run-<ISO-timestamp>-<agent-name>.log` and echoes to `stdout`. Then
> `tail -f logs/run-*.log` in a split pane. You are not aiming for perfect
> tracing — you are aiming for "I can tell it's alive."

> 💡 **Why per-*run* and per-*agent* both matter.** Per-run keeps today's logs
> from mixing with yesterday's, so you can diff or delete a whole run cleanly.
> Per-agent keeps five concurrent streams from interleaving into one unreadable
> file. Together they turn "five silent boxes" into five followable timelines.

## Part 5: Parallelism speed vs coordination cost — and a debugging trap

The reason to do any of this is speed. Andrew never instrumented a stopwatch, but the expectation is plain: "I would suspect that it would be faster than what we did before." Five independent researches that used to happen back-to-back now overlap, so the wall-clock wait shrinks toward the length of the *slowest single* agent instead of the *sum* of all five. That is the win.

The cost shows up immediately, and it is worth studying because it is a trap. After switching to parallel agents, his `results.json` came back **empty**: "Why is our JSON empty? What the heck? ... where's my findings?" The natural suspicion is that parallelism broke it: "do you think when we ... changed it to run multiple agents at the same time, this is where we lost the findings JSON data?"

It was **not** the parallelism. Digging in, the real cause was a **format mismatch** in the aggregation step: the `record_findings` / de-dupe tool expected a structured (Pydantic-validated) object, "but the coordinator passes a plain list." A field expecting a string got a list and iterated it character by character, and the failure was **silent** — nothing logged, results just vanished. The fix was defensive aggregation: "add error logging so the failures aren't silent [and] handle the coordinator's natural output format as a fallback."

> 🔑 **Separate the two failure modes.** "It ran fast but the answer is empty" is
> almost always an **aggregation/formatting** bug at the fan-in step, not a
> parallelism bug at the fan-out step. Parallelism changes *when* results
> arrive; your merge/validate/rank code decides whether they survive.

There is a second, deeper coordination cost he names: silent sub-agent failures. Because the sub-agents run their own loops out of view, an error inside one can disappear without a trace unless your fan-in step logs it. His summing-up:

> "There is an issue with sub-agents, at least with the SDK at this time ... it's an internal loop and we do not know what it's doing until it reports back, and that's not great from a user's perspective. If we're going to build something for production and we need to track stuff, we're going to have to roll this stuff ourselves using the lower-level Anthropic client."

> ❌ **The trap in one line:** blaming parallelism for a missing result. Check
> your aggregation/validation first — add error logging there before you touch
> the fan-out.

### One more improvement he folds in

While debugging, Andrew notices the findings themselves are thin — a bare URL with no provenance. He enriches each finding to carry the **source URL, document name, and page number**: "now we have better source information. We really should have done that prior." Keep this in your pocket; provenance becomes a first-class concern later in the course, and it is nearly free to add while you are already in the aggregation code.

---

## Key takeaways

1. **Parallelism is prompted, not automatic.** The Agent tool calls sub-agents sequentially unless the coordinator's prompt says to issue all the calls in a single response ("simultaneously, do not wait").
2. **Give the coordinator a decision rule, not a switch.** Show it independent tasks (parallel) *and* dependent tasks (sequential) so it chooses correctly per job.
3. **Each sub-agent runs its own loop.** That isolation keeps contexts clean but makes the internal work invisible while it runs.
4. **You must build observability.** Per-run, per-agent log files (`logs/run-<ISO>-<agent>.log`) plus `tail -f logs/run-*.log` are the minimum that lets you see a fleet is alive.
5. **Empty results ≠ broken parallelism.** A vanished result is almost always a fan-in formatting/validation bug; log failures at the aggregation step so they are never silent.
6. **The speed win is real; the coordination cost is observability.** Weigh both before you fan out.

## Common pitfalls

- ❌ **Assuming the SDK parallelises for you.** It does not. Without an explicit "single response, simultaneously, do not wait" instruction, five independent agents still run one at a time.
- ❌ **Parallelising dependent work.** If agent B needs agent A's output, firing them together produces garbage. Only fan out non-overlapping partitions.
- ❌ **Running many agents with no logging.** You will stare at a frozen screen with no idea whether anything is happening, exactly as Andrew did — build the per-agent logs *first*.
- ❌ **One shared log file for all sub-agents.** Concurrent writes interleave into an unreadable mess. One file per agent per run.
- ❌ **Blaming parallelism for an empty `results.json`.** Check the aggregation/validation step and its (probably silent) errors first.
- ❌ **Leaving `bypass permissions` on because a generated script added it.** Andrew removes it every time he sees it: "we did not request it to do that." Turn it off unless you deliberately want it.

---

## 🛠️ Capstone Project: fan Atlas Support out to parallel researchers

> This is the main hands-on project for the lesson. You will feel the difference
> between "wait for five agents in a row" and "watch five agents run at once" —
> and, just as importantly, feel why the logs you build are the only reason the
> second one is bearable. Keep it small on purpose.

### What you will build

Take your Agent SDK coordinator from Lesson 12 and give **Atlas Support** a parallel research stage. When a customer problem arrives, the coordinator splits it into several **independent partitions** (for example: the product docs, past support tickets, the changelog/known-issues, the billing/account system, and community/forum posts), spawns one research sub-agent per partition **at the same time**, then aggregates their findings into a single de-duplicated, ranked list — with one log file per agent per run so you can watch it work.

Its pieces, each mapped to a lesson idea:

- A **coordinator prompt** that names the independent partitions and says "call them in a single response, simultaneously, do not wait" → Part 2.
- **Five research sub-agents**, each with its own loop and its own partition → Part 3.
- A **per-run logging** helper writing `logs/run-<ISO>-<agent>.log` → Part 4.
- An **aggregation step** (a dedupe/rank agent or tool) that merges results and **logs its own failures** → Part 5.
- Findings enriched with **source URL, document name, page number** → Part 5.

### Why this is the perfect practice

| Lesson idea | Where you use it in Atlas Support |
|---|---|
| Prompt for parallel vs sequential | The coordinator prompt that fans out to all five partitions in one response |
| Independent partitions only | Choosing five research slices that genuinely don't depend on each other |
| Each agent runs its own loop | Five sub-agents researching concurrently, isolated from each other |
| Per-run, per-agent logs | `logs/run-<ISO>-<agent>.log` + `tail -f logs/run-*.log` |
| Fan-in bug ≠ fan-out bug | Making the dedupe/rank step log failures instead of silently dropping findings |

### Milestones (build them in order, each one works on its own)

1. **Sequential baseline.** With your Lesson 12 coordinator, have it call the research sub-agents **one at a time** across the five partitions and print a combined result. Note roughly how long it takes. *This alone is a working deliverable.*
2. **Flip to parallel.** Edit only the coordinator prompt: name the five partitions, state they are independent, and instruct "in a single response, call them simultaneously, do not wait between calls." Add the sequential exception in one sentence. Run it. Confirm the coordinator announces it is starting them all at once.
3. **Per-agent, per-run logs.** Give each sub-agent a logger that writes to `logs/run-<ISO-timestamp>-<agent-name>.log` and also echoes to `stdout`. Run again, and in a second pane run `tail -f logs/run-*.log`. You should see multiple agents' lines appear together. *You can stop here and have proven observability.*
4. **Harden the fan-in.** Make the aggregation step (dedupe + rank) log any error instead of failing silently, and accept the coordinator's "natural" plain-list output as a fallback, not only the strict validated shape. Deliberately feed it a slightly wrong shape and confirm you now get a logged error, not an empty `results.json`.
5. **Enrich provenance.** Extend each finding to carry `source_url`, `document_name`, and `page_number`, and make sure they survive aggregation into the final ranked list.
6. **Compare and reflect.** Write two or three sentences: was parallel faster than your Milestone 1 baseline, and what did the logs let you see that the sequential run didn't need?
7. **Stretch goals.** (a) Add a sixth partition and confirm the fan-out scales with only a prompt change. (b) Make the coordinator choose sequential automatically for a *dependent* task (e.g. "summarise, then translate the summary") to prove your decision rule works both ways. (c) Prototype the "roll your own with the Anthropic client" escape hatch for one sub-agent so you get true per-step tracing, and compare the effort.

### How you will know you are done

- ✅ Running the pipeline once produces a `logs/` directory with **one file per sub-agent** for that run, each with time-stamped lines.
- ✅ `tail -f logs/run-*.log` shows **multiple agents' output interleaving live**, proving they run concurrently.
- ✅ The final `results.json` is **non-empty**, de-duplicated, ranked, and every finding carries a URL, document name, and page number.
- ✅ Feeding the aggregation step a malformed input yields a **logged error**, not a silent empty result.
- ✅ You can state, in one sentence each, why you chose parallel for these partitions and what a genuinely *sequential* task would look like instead.

> 💡 **Keep yourself honest:** before you blame parallelism for any missing data,
> open the aggregation logs first. If they're empty, that silence *is* the bug —
> Atlas Support should never drop a finding without saying so.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice
> on one idea. Optional and independent; the Capstone already touches all of
> them, so feel free to skip straight to it.

### Exercise 1: Spot the switch (foundational)
Take a coordinator prompt that runs sub-agents sequentially. Rewrite only the delegation paragraph so the agents run in parallel. Underline the exact words ("single response," "simultaneously," "do not wait") that do the work. No code — just the prompt.

### Exercise 2: The silent drop (intermediate)
Write a tiny `aggregate(findings)` function that expects a list of objects but is sometimes handed a plain string. First reproduce the character-by-character iteration bug and an empty result. Then add (a) a logged error and (b) a fallback that coerces the string into the expected shape. Confirm nothing is ever dropped silently.

### Exercise 3: Watch the fleet (advanced)
Spawn three trivial sub-agents (each just sleeps a random 1–5 seconds and logs "start"/"done") in parallel, each writing to `logs/run-<ISO>-<name>.log`. Use `tail -f logs/run-*.log` to watch them. Then make one agent's work *depend* on another's output and rewrite the coordinator so those two go sequential while the third stays parallel.

---

## Cheat sheet

```text
RUNNING AGENTS IN PARALLEL — quick recap

THE BIG SURPRISE
  The Agent (task) tool runs sub-agents SEQUENTIALLY by default.
  Parallelism is a PROMPT, not a flag. You must ask for it.

PROMPT THAT FANS OUT (put in the coordinator prompt)
  "In a SINGLE response, call <agent> simultaneously for ALL <partitions>.
   They are independent — DO NOT wait between calls. Delegate to all at once."
  Then add the exception:
  "Run SEQUENTIALLY only when a later agent needs an earlier one's output."

MENTAL MODEL
  coordinator --(one response, N tool calls)--> N sub-agents at once
  each sub-agent runs its OWN loop (gather→act→verify), context isolated
  coordinator then AGGREGATES: merge → de-duplicate → rank   (fan-in)

WHY IT'S HARD TO WATCH
  Sub-agents run their own loops out of view. No built-in per-step logging.
  (Streaming for sub-agents = unverified SDK claim; may change. Verify it.)

BUILD OBSERVABILITY YOURSELF
  Each sub-agent -> logs/run-<ISO-timestamp>-<agent-name>.log  (+echo stdout)
  Watch the whole fleet:   tail -f logs/run-*.log

WIN vs COST
  Win : wall-clock ≈ slowest single agent, not the SUM of all agents.
  Cost: visibility. Amdahl's Law — only independent work speeds up.

DEBUGGING RULE
  Empty result ≠ broken parallelism.
  It's almost always a FAN-IN formatting/validation bug. Log those failures.
  (Andrew's case: tool wanted a validated object, coordinator sent a plain list.)

DON'T FORGET
  - Only fan out NON-OVERLAPPING partitions.
  - Enrich findings: source URL + document name + page number.
  - Remove `bypass permissions` you didn't ask for.
  - Verify SDK limits by building; the docs & Python SDK lag.
```

## How this connects to the rest of the course

- **Earlier, Module 3 · Lesson 12 (the Agent SDK and the Agent/task tool):** you built the isolated sub-agents this lesson runs concurrently — and met the same "docs and Python SDK lag" reality that reappears here.
- **Earlier, Module 3 · Lesson 9 (task decomposition):** the non-overlapping partitions you learned to define are precisely what makes parallel fan-out safe.
- **Earlier, Module 3 · Lesson 10 (refinement loops and observability):** the logging instinct you started there becomes non-negotiable once many agents run at once.
- **Next, Module 3 · Lesson 14 (gates, hooks, and handoff protocols):** hooks give you a cleaner, SDK-native place to hang the logging and checks you hand-rolled here — and a structured way to hand off when an agent gets stuck.
- **Later, Module 6 (context management and reliability):** provenance-preserving findings, silent-failure logging, and the "roll your own with the Anthropic client for real observability" escape hatch all mature into first-class reliability practices for Atlas Support.

---

*Source: the CCA-F course by Andrew Brown, ExamPro. Code snippets and diagrams are illustrative reconstructions of the patterns described in the course. Adapt them to the current SDK — and, as Andrew insists, verify every capability claim by building it.*
