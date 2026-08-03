# Module 3 · Lesson 15: Prompt chaining vs adaptive decomposition

> **Course:** Claude Certified Architect: Foundations, a self-paced course
> **Module 3:** Orchestration: multi-agent architectures: how coordinators route, delegate, gate, and combine the work of many agents
> **Speaker:** Andrew Brown, ExamPro
> **Source:** Reconstructed from the CCA-F course by Andrew Brown (ExamPro) · [full transcript](../../transcripts/cca-f-full-course.txt)
> **Estimated time:** 45 to 60 minutes (read plus lab)

---

## In one sentence

When you coordinate several agents, you choose between a **prompt chain** — a fixed, predictable pipeline where the shape of the work never changes — and **adaptive decomposition**, where each finding reshapes what you do next; and whichever you pick, you must keep every finding attached to its source instead of melting them into one anonymous blob.

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone
> Project** where you give **Atlas Support** an *adaptive investigation mode*
> that follows the evidence and returns structured findings, each one still
> carrying the source it came from. Everything before the Capstone teaches the
> two coordination shapes and the provenance rule you will use there. If you want
> to see the finish line first, jump to the **"Capstone Project"** section, then
> come back.

## First-principles companion

> 💡 **The durable idea behind this lesson.** The SDKs will change, but the
> distinction between a *fixed workflow* and an *agent that decides its own next
> step* is stable and worth reading from the source:
>
> - **[Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)** (Anthropic, engineering post). It names **prompt chaining** as one of the core *workflow* patterns — predictable, fixed steps — and contrasts workflows with **agents** that direct their own process. This lesson is that contrast, made concrete, plus one hard rule about provenance.

## A few plain-language basics first

This lesson uses a handful of terms. Here they are in plain words:

- **Agent:** an AI that takes a *series* of actions on its own toward a goal, rather than answering in one shot.
- **Sub-agent:** an agent spawned by another agent, usually with its own isolated context. You call it, it does a slice of work, it reports back.
- **Coordinator (hub-and-spoke):** one agent that owns routing and combining. It decides who does what, hands slices to sub-agents ("spokes"), and assembles the results. You built this in earlier Module 3 lessons.
- **Pipeline:** a line of steps where the output of one step is the input to the next, like a factory conveyor belt.
- **Findings:** the pieces of information agents dig up during research — a claim, a fact, a recommendation.
- **Provenance:** where something came from and how it got to you. Andrew borrows the antiques word: "let's say you buy a very old antique and you want to make sure that it comes from a particular place, then we use the word provenance." For findings, provenance is *which source, which page, which document*.
- **Structured output:** making the model return machine-readable data (usually JSON) with named fields, instead of free-flowing prose.

You do not need to memorize these. Each is explained again the first time it matters.

## Why this lesson matters

Up to now in Module 3 you have built a coordinator, spun up sub-agents, run them in parallel, and gated their handoffs. This lesson answers the question that sits *above* all of that: **what shape should the work take?** Some jobs are the same every time — you can hard-wire the steps. Other jobs are investigations where you genuinely do not know how deep or wide you will need to go, and forcing them into a fixed pipeline makes them worse. Knowing which is which is a core exam skill in Domain 1.

Then comes the trap that quietly ruins multi-agent research: you gather great findings, mash them together for a final summary, and lose track of who said what. As Andrew puts it, "by the time the final output is written, the provenance is gone." A recommendation you cannot trace back to a source is a recommendation you cannot trust. This lesson teaches you to keep the source glued to the finding from the very first step — the discipline that makes Atlas Support's answers defensible.

## Learning objectives

By the end of this lesson you will be able to:

1. Define **prompt chaining** and name three jobs it fits (fixed-shape work).
2. Define **dynamic adaptive decomposition** and name three jobs it fits (open-ended investigation).
3. Choose between the two for a given task by asking, "Is the shape of the work fixed regardless of the content?"
4. Write an **adaptive investigation** coordinator prompt that turns each finding into the next round of subtasks.
5. Explain the **raw-findings dilemma** and why blob synthesis destroys provenance.
6. Design a **structured findings-with-sources** format so content and its metadata travel together.

## Prerequisites

- **Module 3 · Lesson 14 · "Gates, hooks, and handoff protocols"** — you will reuse programmatic gates here to make an adaptive plan safe.
- Earlier Module 3 lessons on the **coordinator / hub-and-spoke** pattern and **sub-agents** (you will orchestrate several agents).
- Comfort reading small Python and JSON. The **Claude Agent SDK** (the higher-level library for building agents) is assumed installed from Module 0.

---

## Part 1: Prompt chaining — the fixed, predictable pipeline

Start with the simplest coordination shape. **Prompt chaining** — you can also call it a **sequential pipeline** — is when you run a series of calls or agents one after another, feeding each result into the next. As Andrew describes it: "we have our input, we run it, we put that out there, we run it, we put that out there." Step, step, step. Same order, every time.

```text
input ──▶ [ step 1 ] ──▶ [ step 2 ] ──▶ [ step 3 ] ──▶ output
         identify bugs   propose fixes   apply fixes
```

The defining trait: **the shape of the work is fixed regardless of the content.** It does not matter *what* the input is — a Ruby file, a legal document, a product description — the pipeline always runs the same steps in the same order. That predictability is the whole point.

This makes prompt chaining a great fit for:

- **Document processing** — extract, then classify, then summarize.
- **Content transformation** — draft, then edit, then format.
- **ETL pipelines** ("extract, transform, load" — the classic move data from A to B, reshaping it on the way).
- **Any task where the steps never depend on what you find.**

Andrew is careful to point out this is not some new invention. "Prompt chaining is not a new concept. It's very old." Before agents ran in loops, "when we were really starting with LLMs and everything was very short and fixed, the only way we could work with LLMs was to prompt chain." An **LLM** (large language model) is the kind of AI that reads and writes text; Claude is one. Chaining was how people got real work out of early ones.

### The bug-fixing chain (the lab)

In the course lab, Andrew asks Claude to demonstrate prompt chaining and it produces a three-step pipeline on its own: **identify bugs → propose fixes → apply fixes**. He feeds it a file of ten deliberately broken Ruby functions (generated over in ChatGPT so he does not burn Claude credits on busywork), runs `python main.py`, and the pipeline marches through: "identify bugs, propose fixes, apply fixes." It finds and fixes "most of the bugs." Notice the structure of the code Claude wrote — "await run step, await run step" — literally one fixed step after another.

> 💡 **A build-and-verify moment.** The first run did nothing, because Andrew had
> not saved the file. "Is it just working on a blank file?" Once saved, "now it's
> taking longer because there's actually something to process." The pipeline was
> fine; the input was empty. Always confirm the thing you are feeding the pipeline
> is actually there before you conclude the pipeline is broken.

> 🔑 **Use a prompt chain when the steps are the same every time. If the content
> never changes *which* steps run or in *what order*, a fixed pipeline is the
> right — and cheapest, most predictable — tool.**

## Part 2: Dynamic adaptive decomposition — follow the evidence

Now the opposite shape. **Dynamic adaptive decomposition** is when, in Andrew's words, "intermediate findings should change what you do next: which agents to call, how many times, and in what order." The plan is not fixed. It grows and bends as results come back.

*Decomposition* just means breaking a big task into smaller subtasks. *Adaptive* means the breakdown is not decided up front — it is re-decided after every result. Where a chain is a straight conveyor belt, adaptive decomposition is a coordinator standing at a whiteboard, redrawing the plan each time a sub-agent reports in.

This fits the jobs a fixed pipeline cannot handle:

- **Open-ended research.**
- **Investigation tasks.**
- **Anything where you do not know upfront how deep or how wide the work needs to go.**

The heart of it is the coordinator's prompt. Andrew's example says it plainly:

> "You're a research coordinator. After each step, assess what you found and decide what to do next. You may need more research, a different angle, or you may have enough to synthesize. **Do not follow a fixed sequence. Follow the evidence.**"

That last line is the whole pattern. "Follow the evidence" is the opposite of "run step 1, then step 2, then step 3." The coordinator keeps the authority to call another sub-agent, switch angles, or stop.

| | Prompt chaining | Adaptive decomposition |
|---|---|---|
| **Plan** | Fixed up front | Re-decided after each finding |
| **Steps** | Same order every time | Chosen by the coordinator at runtime |
| **How many calls** | Known in advance | Unknown — "as deep or wide as needed" |
| **Best for** | Fixed-shape work (ETL, document processing) | Open-ended research and investigation |
| **Risk** | Too rigid for messy work | Cost and scope can run away |

### The "agent dungeon" lab — a cautionary tale

Andrew's adaptive lab is an **agent dungeon**: a text dungeon-crawler where the world is *generated as you explore*, so "static replanning is impossible." When the player walks into an unvisited room, a coordinator ("the orchestrator") decides which sub-agents to fire — a room builder, a code writer, a lore agent — because you cannot know in advance how deep into "the necromancer's tower" a player will go. That is genuine adaptive decomposition: the work appears only as the player moves.

Two lessons matter more than whether the game worked (it mostly did not):

- **Cost runs away fast.** Generating a large TypeScript codebase from scratch, adaptively, "consumed a lot of credits" — Andrew was "halfway through" his daily usage from a single task. His takeaway: pull from a boilerplate you already trust, use a cheap **model** like **Haiku** (models differ in strength, speed, and price), and "restrict how Claude is working." Adaptive freedom without a budget is a wallet leak.
- **Adaptive needs guardrails.** The spec claimed the AI would "fire once per unvisited room, never touches again," but "we don't have any guarantees that it'll do that." Andrew ties it straight back to Lesson 14: "remember earlier we talked about programmatic gates to enforce things... that's not a guarantee. We need to have programmatic guarantees." An adaptive coordinator decides freely *inside* limits you enforce in code — not on the honor system.

> ❌ **Do not confuse "adaptive" with "unbounded."** The coordinator chooses the
> next step; your code still enforces the ceiling — max turns, which model,
> when the AI is allowed to fire at all. Freedom in planning, hard walls in code.

> 🔑 **Use adaptive decomposition when you cannot know the steps in advance —
> and fence it with a budget and programmatic gates so "follow the evidence"
> never becomes "follow the evidence off a cliff."**

## Part 3: The adaptive investigation plan — each finding drives the next subtasks

Adaptive decomposition needs a concrete engine, and here it is. An **adaptive investigation plan** "treats each finding as input to the next decision — not just data to collect, but a signal that reshapes what needs to be done next."

Contrast it with a **fixed plan**: "we need to do these three things," and the findings never change the plan after it starts. Fine when the shape is known — but useless for a real investigation, where what you learn in step one should decide step two.

The mechanism is a set of questions the coordinator asks itself *after every finding*. From Andrew's prompt:

> "You're an investigative researcher coordinator. After each finding, ask:
> - **What does this raise that I don't know yet?**
> - **What would change my conclusion if it turned out differently?**
> - **What claim here needs verification?**
> Generate targeted subtasks from those questions."

Then those subtasks become the next round of research, and the cycle repeats. That is the loop:

```text
     ┌─────────────────────────────────────────────┐
     ▼                                             │
 finding ──▶ ask: what's now unknown?              │
             what would flip the conclusion?       │
             what needs verifying?                 │
                     │                             │
                     ▼                             │
          generate targeted subtasks ──▶ research ─┘
                     │
                     ▼   (when nothing important is left open)
                synthesize
```

Notice how different this is from a chain. A chain never asks a question — it just runs the next fixed step. The investigation plan makes *questions* the thing that generates the next subtasks, so the plan is literally built out of what you do not yet know.

> ✅ **What to do about it:** put the three questions verbatim into your
> coordinator's system prompt. They are the difference between an agent that
> collects a fixed list and one that actually investigates.

## Part 4: The raw-findings dilemma — how blob synthesis destroys provenance

Here is the failure that spoils multi-agent research even when everything else works. Andrew calls it the **raw-findings dilemma**: "this is when you pass raw findings between agents as a single blob of text and attributions get lost."

Picture several sub-agents each returning a paragraph of prose. The coordinator concatenates them into one big text and hands it to a synthesis agent. That synthesis agent "can't tell which claim came from which source, and by the time the final output is written, the provenance is gone." **Provenance** — Andrew's antiques word — is the record of where each claim came from. Lose it, and you have facts you cannot stand behind.

His example blob:

```text
EV adoption grew 40% in 2024. Battery costs have fallen. The IEA report on
page 14 says charging infrastructure is the main barrier. Reuters also
reported that BYD overtook Tesla in Q3.
```

Read it and try to answer the obvious questions: **Which source? What page? What document?** For the 40% figure, there is no answer — the attribution is "just gone." The blob reads confidently and cites nothing you can check.

This is not a cosmetic problem. In the movie-research lab later, the findings come back beautifully structured — confidence, claim, type, name, author, published date, accessed date — and yet, Andrew notes, "the only thing we don't have is like where did it get that data?" Even a good structure fails if it forgets the one field that makes a finding checkable: the source.

> ❌ **The trap:** synthesizing many sub-agent results into one paragraph *feels*
> like the finish line. It is actually where trust dies — a fluent summary whose
> claims can no longer be traced to anything.

> 🔑 **The moment you flatten findings into one blob of prose, you throw away
> provenance. And a claim you cannot trace is a claim you cannot defend.**

## Part 5: Structured findings-with-sources — keep content and metadata together

The fix is a shape, not a scolding. As Andrew says: "we want structured formats to keep content and metadata traveling together." Instead of passing prose, every agent passes a **structured finding** — the claim *and* everything needed to trace it, glued into one record that never comes apart as it moves between agents.

A finding is a small object, not a sentence:

```json
{
  "claim": "EV adoption grew 40% in 2024.",
  "confidence": "high",
  "source": {
    "type": "report",
    "name": "IEA Global EV Outlook 2025",
    "page": 14,
    "url": "https://www.iea.org/reports/...",
    "accessed": "2026-07-20"
  }
}
```

Now the synthesis agent physically cannot lose the source, because the source rides *inside* the same object as the claim. When it writes the final answer, "40% growth" can carry "(IEA Global EV Outlook 2025, p.14)" with it — automatically.

Two implementation notes from the lab, both worth stealing:

- **Enforce the shape, don't beg for it.** In the movie lab Andrew reaches for **Pydantic** (a Python library that validates data against a declared model) so the findings *must* match the structure — "so it's forcing that structure." A prompt asking nicely for JSON is fragile; a schema the data is validated against is not. (This is the **structured output** idea from the prompting module, applied to findings.)
- **Persist the findings.** "Are we saving the findings to a file so we can see what they are at some given point?" The lab prints each finding and then saves the set to a `results.json`. Findings you can open, re-read, and audit later are worth far more than findings that vanish when the run ends.

### The movie-recommender lab

The whole thing comes together in a delightfully specific job: find late-1970s/early-1980s films similar to the 1981 Japanese film *Schools in the Crosshairs* — "99% wholesome and 1% Japanese weird," as Andrew describes it. A film-researcher sub-agent runs across several "similarity axes" (psychic school films, mind-control cults, coming-of-age, visionary directors), and each recommendation comes back as a structured finding — confidence, claim, type, name, author, dates — saved to `results.json`.

It took real fiddling. Claude kept defaulting to the lower-level **Anthropic SDK** instead of the **Claude Agent SDK** and its proper `AgentDefinition`, and at one point "destroyed the entire use case" by rewriting the prompt and dropping the findings structure — a live reminder that "every time they say it's better," you still review the diff. And the finished findings still lacked the single most important field: the URL. As Andrew signs off, "that's great that you have this information, but where did it come from?" That gap *is* the lesson — which is exactly the field your capstone will require.

> ✅ **What to do about it:** make the source a **required** field on every
> finding, validated by a schema. If an agent cannot supply where a claim came
> from, the finding does not pass — no exceptions.

---

## Key takeaways

1. **Prompt chaining = fixed pipeline.** Same steps, same order, regardless of content. Perfect for document processing, content transformation, and ETL. Old, boring, reliable.
2. **Adaptive decomposition = follow the evidence.** Each finding re-decides which agents to call, how many times, in what order. For open-ended research where you cannot know the shape up front.
3. **Choose by one question:** "Is the shape of the work fixed regardless of the content?" Yes → chain. No → adapt.
4. **Adaptive is not unbounded.** Give it a budget, a cheap model where you can, and *programmatic gates* — the coordinator plans freely only inside walls your code enforces.
5. **The adaptive engine is three questions per finding:** what's now unknown, what would flip the conclusion, what needs verifying — and subtasks are generated from the answers.
6. **Blob synthesis destroys provenance.** Flatten findings into one paragraph and you can no longer say which source made which claim.
7. **Keep content and metadata together.** Every finding is a structured record with its source attached, schema-enforced and saved to a file.

## Common pitfalls

- ❌ **Forcing an investigation into a fixed chain.** If findings should change the next step, a rigid pipeline gives shallow, wrong-shaped results. Adapt instead.
- ❌ **Letting an adaptive coordinator run unbounded.** No max turns, no budget, no gates — and it burns your whole daily usage on one task, as the dungeon lab showed.
- ❌ **Trusting "fire once per room, never again" because the prompt says so.** Words are not guarantees; enforce it in code.
- ❌ **Synthesizing findings into one blob of prose.** It reads great and cites nothing. Provenance is gone the moment you flatten it.
- ❌ **Asking for JSON in the prompt and hoping.** Enforce the finding shape with a schema (e.g., Pydantic) so a malformed or source-less finding is rejected, not silently accepted.
- ❌ **Not saving findings.** If they only live in memory during the run, you cannot audit what the agent actually based its answer on.

---

## 🛠️ Capstone Project: Atlas Support's adaptive investigation mode

> This is the main hands-on project for the lesson. You will give **Atlas
> Support** — the multi-agent support system this course builds end to end — an
> *investigation mode* that follows the evidence and returns findings that never
> lose their source. Keep it small; the point is the two patterns working
> together, not a huge codebase.

### What you will build

A small coordinator that, given a support question it cannot answer from one lookup (say, "Why are EU customers seeing checkout failures since Tuesday?"), runs an **adaptive investigation**: it calls research sub-agents, and after each finding it decides what to investigate next. Every finding comes back as a **structured record with its source attached**, and the whole set is saved to a file the human escalation reviewer can audit.

Its pieces, each mapped to a lesson idea:

- A **fixed intake chain** that normalizes the incoming ticket (Part 1).
- An **adaptive coordinator** whose prompt says "follow the evidence" (Part 2).
- The **three investigation questions** driving each round of subtasks (Part 3).
- A **`Finding` schema** with a required `source` field (Parts 4–5).
- A **`findings.json`** the run writes out (Part 5).
- A **programmatic gate** capping total sub-agent calls (Lesson 14 + Part 2).

### Why this is the perfect practice

| Lesson idea | Where you use it in Atlas Support |
|---|---|
| Prompt chaining (fixed shape) | The 2-step intake chain: normalize ticket → classify |
| Adaptive decomposition | The coordinator re-plans after each finding |
| "Follow the evidence" prompt | The coordinator's system prompt, verbatim |
| Three investigation questions | Turned into the next round of subtasks |
| Raw-findings dilemma | Why you refuse to pass prose blobs between agents |
| Findings-with-sources | The `Finding` schema with a required `source` |
| Programmatic gates | A hard cap on sub-agent calls, enforced in code |

### Milestones (build them in order, each one works on its own)

1. **Fixed intake chain.** Write a two-step prompt chain: step 1 normalizes the raw ticket text, step 2 classifies it (billing / outage / how-to). Prove the shape is fixed — it runs identically for any ticket. Smallest version: two sequential calls, printing each step's output.
2. **The `Finding` schema.** Define a `Finding` with `claim`, `confidence`, and a **required** `source` (type, name, url, accessed). Use Pydantic (or any validator) so a finding with no source is rejected. Smallest version: construct one valid finding and one invalid one; confirm the invalid one raises.
3. **One research sub-agent.** Give the coordinator a single sub-agent that answers one focused question and returns a `Finding` (not prose). Run it once end to end.
4. **Adaptive coordinator.** Add the coordinator whose system prompt says "assess what you found and decide what to do next... do not follow a fixed sequence, follow the evidence," and which asks the three questions after each finding to generate the next subtasks. Smallest version: it runs two rounds where round two's question is chosen from round one's finding.
5. **The gate.** Add a programmatic cap (e.g., at most 6 sub-agent calls, or a max-turns limit) enforced in your code — not in the prompt. Prove it stops even if the model "wants" to keep going.
6. **Persist and cite.** Write all findings to `findings.json`. Then have the final answer quote at least one claim *with its source inline* — e.g., "checkout fails for EU cards (from: PaymentsService logs, 2026-07-20)." Confirm you can trace every claim in the answer back to a finding in the file.
7. **Stretch goals.** Add a `confidence` gate that escalates to a human when no high-confidence finding answers the question; add a second sub-agent so the coordinator must *choose* which to call; make the coordinator stop early when the three questions raise nothing new.

### How you will know you are done

- ✅ The intake chain runs the same two steps for any ticket (fixed shape).
- ✅ A `Finding` with a missing `source` is **rejected** by the schema, not saved.
- ✅ The coordinator's round-two subtask is visibly derived from a round-one finding (it adapted).
- ✅ A hard cap on sub-agent calls stops the run even when the model would continue.
- ✅ `findings.json` exists, and every claim in the final answer can be traced to a source in it.

> 💡 **Keep yourself honest:** open `findings.json` and pick any claim from the
> final answer. If you cannot point to the exact source record it came from, your
> provenance leaked somewhere — fix the shape, not the summary.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice
> on one idea. Optional and independent; the Capstone already touches all of
> them, so feel free to skip straight to it.

### Exercise 1: Classify the job (foundational)
For each task, decide **chain** or **adaptive** and say why in one sentence: (a) convert 500 blog posts from Markdown to HTML; (b) find out why a specific customer's refund failed; (c) generate invoices from a fixed template; (d) research which competitor feature caused a churn spike. The tell is always "is the shape fixed regardless of content?"

### Exercise 2: Spot the lost provenance (intermediate)
Take Andrew's blob — "EV adoption grew 40% in 2024. Battery costs have fallen. The IEA report on page 14 says charging infrastructure is the main barrier. Reuters also reported that BYD overtook Tesla in Q3." — and rewrite it as an array of `Finding` objects. For any claim with no traceable source, mark `source: null` and note that it would be **rejected** by a required-source schema.

### Exercise 3: Write the investigation prompt (advanced)
Write a coordinator system prompt for an open-ended task of your choice. It must (1) say "follow the evidence, do not follow a fixed sequence," (2) ask the three questions after each finding, and (3) require every returned finding to include its source. Then add, in prose, the *programmatic* gate you would enforce in code around it (max calls or max turns).

---

## Cheat sheet

```text
CHAINING vs ADAPTIVE — choosing a coordination shape
----------------------------------------------------
THE ONE QUESTION
  "Is the shape of the work fixed regardless of the content?"
     YES -> prompt chain (fixed pipeline)
     NO  -> adaptive decomposition (follow the evidence)

PROMPT CHAINING (sequential pipeline)  [old, reliable]
  input -> step1 -> step2 -> step3 -> output   (same steps, every time)
  Fits: document processing, content transformation, ETL, fixed-shape work
  Example: identify bugs -> propose fixes -> apply fixes

ADAPTIVE DECOMPOSITION (dynamic)
  Findings re-decide: which agents, how many times, what order
  Prompt: "assess what you found, decide what to do next.
           DO NOT follow a fixed sequence. FOLLOW THE EVIDENCE."
  Fits: open-ended research, investigation, unknown depth/width
  WARNING: cap it. Budget + cheap model (Haiku) + PROGRAMMATIC GATES.
           Adaptive != unbounded. Words are not guarantees.

ADAPTIVE INVESTIGATION ENGINE (ask after EACH finding)
  1. What does this raise that I don't know yet?
  2. What would change my conclusion if it turned out differently?
  3. What claim here needs verification?
  -> generate targeted subtasks -> research -> repeat -> synthesize

RAW-FINDINGS DILEMMA
  Pass findings as one BLOB of prose -> provenance is GONE.
  Synthesis agent can't say which source made which claim.
  "which source? what page? what document?" -> no answer.

FINDINGS-WITH-SOURCES (the fix)
  Content + metadata travel together, as one record:
    { claim, confidence, source:{type,name,page,url,accessed} }
  Enforce shape with a schema (Pydantic). Save to findings.json.
  RULE: source is REQUIRED. No source -> finding rejected.
```

## How this connects to the rest of the course

- **Earlier, Module 3 · Lesson 14 · "Gates, hooks, and handoff protocols":** gave you the programmatic gates you use here to keep an adaptive coordinator from running away. This lesson is where those gates stop being optional.
- **Earlier, Module 3 (coordinator arc):** the hub-and-spoke coordinator and parallel sub-agents you built are the machinery; this capstone lesson decides *how they should be shaped* — and is the arc's payoff.
- **Next, Module 4 · "MCP: discovery, resources, and building a server":** your findings need real sources, and MCP is how agents reach external tools and data (**resources**). You will start pulling findings from MCP servers — where provenance becomes something you can actually cite.
- **Later, across Atlas Support:** the investigation mode you build here becomes how the support agent researches a hard ticket before it escalates to a human — with every claim still traceable to its source.

---

*Source: reconstructed from the "Claude Certified Architect: Foundations" course by Andrew Brown (ExamPro). Code snippets and diagrams are illustrative reconstructions of the patterns described in the course; adapt them to the current SDK.*
