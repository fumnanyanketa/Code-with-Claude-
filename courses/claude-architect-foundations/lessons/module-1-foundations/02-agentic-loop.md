# Module 1 · Lesson 2: The agentic loop and Claude Code

> **Course:** Claude Certified Architect: Foundations, a self-paced course
> **Module 1:** Foundations: how Claude agents work — the exam map plus the loop, tools, and stop-reason machinery everything else is built on.
> **Speaker:** Andrew Brown, ExamPro
> **Source:** Reconstructed from the CCA-F course by Andrew Brown (ExamPro) · [full transcript](../../transcripts/cca-f-full-course.txt)
> **Estimated time:** 45 to 60 minutes (read plus lab)

---

## In one sentence

Every Claude agent — including Claude Code, Anthropic's command-line coding tool — works by repeating one three-step cycle, **gather context → take action → verify results**, calling small functions called *tools* along the way and running one model of your choosing (Opus, Sonnet, or Haiku) for the whole cycle until it decides the job is done.

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone Project** where you trace a single real task all the way through the loop on paper — narrating each gather/act/verify step, naming the tool each step would call, and picking the right model for the job. No heavy coding: a diagram and a short script stub is all you produce. This is the conceptual foundation that **Atlas Support**, the multi-agent system you build across this course, will run on top of. If you want to see the finish line first, jump to the **"Capstone Project"** section, then come back.

## First-principles companion

> 💡 **The durable idea behind this lesson.** Claude Code and the model names in it will change. The loop underneath will not. For the timeless, tool-agnostic version:
>
> - **[ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)** (Yao et al., 2022, research paper). This is the original account of interleaving *reasoning* (thinking about what to do) with *acting* (calling an external tool and reading the result), which is exactly the "gather context → take action → verify" cycle repackaged as a product. Read it once and you will recognize the loop inside every agent you ever meet, whatever it is branded.

## A few plain-language basics first

This lesson uses some everyday terms. Here they are in plain words:

- **LLM (large language model):** the kind of AI that reads and writes text; "Claude" is one. On its own it can *only* produce text — nothing else.
- **Model:** one specific version of Claude (Opus, Sonnet, Haiku) that differ in strength, speed, and price.
- **Token:** the unit a model reads and writes in, roughly three-quarters of a word; when you use the API you are billed per token.
- **Agent:** an AI that takes a series of actions on its own toward a goal, instead of answering in a single shot.
- **Agentic loop:** the repeating cycle an agent runs — gather context, take action, verify — until the task is done.
- **Tool / tool call / tool result:** a plain code function the model is allowed to run. When the model decides to run one, that is a *tool call*; what the function hands back is the *tool result*.
- **CLI (command-line interface):** a program you drive by typing commands into a terminal, rather than clicking buttons.
- **Terminal:** the black text window where you type commands to your computer.
- **`stop_reason`:** a field the model's reply carries that says *why* it stopped talking. You will only meet the concept here; you wire it up in the next lesson.

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

Every advanced thing in this course — coordinators, parallel agents, MCP tools, escalation — is just the loop in this lesson, repeated, nested, and dressed up. If the loop is solid in your head, the rest of the course is variations on a theme; if it is fuzzy, everything later feels like magic. As Andrew puts it, "if you've learned about agents, you probably already know this, but we'll cover it anyway and specifically in the context of Claude Code." That framing matters for the exam: Domain 1 is built on this exact vocabulary, and the questions assume you can say precisely what "gather context," "tool call," and "stop reason" mean.

## Learning objectives

By the end of this lesson you will be able to:

1. Describe the three phases of the agentic loop — gather context, take action, verify results — and explain why it repeats.
2. Say what Claude Code is, name its surfaces (terminal, IDE, desktop, browser), and explain why it is "just a CLI program" at heart.
3. Explain what a tool is (a code function the agent can invoke) and give an example tool for each loop phase.
4. Choose a model — Opus, Sonnet, Haiku, Sonnet-1M, or opus-plan — for a given job and justify the choice.
5. State the concept of `stop_reason` and its two values, `tool_use` and `end_turn` (implementation comes next lesson).

## Prerequisites

- **Module 1 · Lesson 1** ("What the CCA-F exam is and how to pass it"), for the exam shape and the verify-everything mindset.
- Optional: **Module 0** if you still need Python, an API key, and Claude Code installed. Nothing in *this* lesson requires running code — it is conceptual — but the capstone is nicer if your tools are ready.

---

## Part 1: What Claude Code is

Andrew opens with the plain definition: "Claude Code is an agentic coding tool and it reads your codebase, edits files, runs commands and integrates with your development tools." You find it at **code.claude.com**.

The first thing to internalise is that Claude Code shows up in more than one place. As Andrew lists them, "it's available in your terminal, IDE, desktop app, browser, and more" — these are its **surfaces**. A *surface* is just a place you can drive Claude Code from. It "looks a bit different and works a bit different depending on where you use it," but it is the same engine underneath.

| Surface | What it is | When you reach for it |
|---|---|---|
| **Terminal (CLI)** | Typing commands in your text terminal | The most common and, as Andrew says, "probably the most natural way to use it because it is a CLI tool" |
| **IDE** | Inside your code editor (e.g., VS Code) | Editing while you see the diffs in your editor |
| **Desktop app** | A standalone application | A dedicated window, away from the terminal |
| **Browser** | On the web | Working "from anywhere," no local install |

Its use cases, from Andrew's list: "automating your workflow you keep putting off, build features and fix bugs, create commits and pull requests, connect your tools with MCP, customize with instructions, skills and hooks, run agent teams and build custom agents, pipe scripts, automate with the CLI and work from anywhere." The one people get most excited about is **agent teams** — "a bunch of agents working together in a team to accomplish a task" — which this course covers in depth later (that is the whole of Module 3).

But strip the excitement away and hold onto Andrew's grounding line:

> 🔑 **"The main thing is that Claude Code is a CLI program. It's a code harness. It's an agentic coding tool, but at the end of it, it's just a CLI program."** A *harness* is the surrounding program that runs the model in a loop and connects it to your files and terminal. Claude Code is specialised for code, but "it can also write docs, run builds, search files, research topics, and more."

And the sentence that sets up the entire rest of the lesson: Claude Code "uses an agentic loop, multiple models — specifically the Claude Code models — [and] tool calls to achieve your desired goal." Loop, models, tools. That is the whole lesson in one line.

## Part 2: The agentic loop

Here is the heart of it. You invoke Claude Code and ask it to do something. As Andrew describes it, "you're going to ask it to do something and that's going to start the loop." From that point the agent runs three phases over and over:

1. **Gather context** — find out what it needs to know.
2. **Take action** — change something in the world.
3. **Verify results** — check whether the change worked.

Then it loops back to the top. "It's going to continuously do this until it achieves its goal."

```text
        ┌─────────────────────────────────────────┐
        │                                         │
        ▼                                         │
  ┌───────────────┐   ┌──────────────┐   ┌────────────────┐
  │ GATHER        │──▶│ TAKE         │──▶│ VERIFY         │
  │ CONTEXT       │   │ ACTION       │   │ RESULTS        │
  │ read, search  │   │ edit, run    │   │ test, compare  │
  └───────────────┘   └──────────────┘   └────────────────┘
        │                   │                   │
        └──── each phase may call a TOOL ───────┘

  loop until: goal met  ·  needs your feedback  ·  stops to save money
```

Two details make this real rather than hand-wavy.

**The model lives in a box.** As Andrew puts it, "the LLM is in its own little box... it would have to call out to a function in order to interact with your developer environment." The model itself can only produce text. Anything that touches your files, your terminal, or the internet happens through a **tool** — a function it is allowed to call. That is why every phase in the diagram has an arrow pointing at "call a tool": the loop is how the model *does things*, and tools are the only way it reaches outside the box.

**You are still in charge.** "At any time you can interrupt this loop and give it corrections," Andrew notes, "and then eventually it will decide that it has met the goal or needs more feedback or it doesn't want to run anymore to not waste your money." So the loop ends for one of three reasons: the goal is met, the agent needs your input, or it stops to avoid burning tokens. You are never locked out — you can jump in mid-loop and steer.

> 💡 **A judgment moment from the transcript.** Earlier in the course, Andrew fed Claude Code a bug ("it's supposed to edit a file, it does not, here check the logs and help me") — and Claude reported the edit had actually worked and the file was already correct. Andrew's honest reaction: "Oh, it's fixed. What? Well, whatever... I'm not sure what happened there." The lesson is not that Claude is always right — it is that the *verify* phase (reading the logs, checking the file) is what surfaced the truth. Throughout this course the rule holds: the docs, the AI's own answers, and even the exam guide can be wrong. The way to the truth is to build it and verify.

> 🔑 **The loop is the product.** Gather → act → verify, repeating, calling tools, until a stop condition. Everything else in Claude Code is scaffolding around this cycle.

## Part 3: What tools are

Andrew's definition is refreshingly literal: "tools are code functions that an agent is aware of and can invoke to complete their tasks. And when I say they're code functions, I literally mean it's just a code function."

Why does an LLM need them at all? Because, as Andrew says, "it can only do so much within itself... it can just produce text. And so it needs some way of interacting with external programs" — or with anything "deterministic that you can use code for." (*Deterministic* means the same input always gives the same output — the reliable, predictable behaviour you get from ordinary code, not from a model's guesswork.) The model decides *what* to do; the tool reliably *does* it.

Crucially, the agent already knows its toolbox before it starts: "the agent knows what tools are available to it. It knows the name of the function, what its inputs are, and what it expects back as output." So a tool, from the model's point of view, is a name plus an input shape plus an expected output.

### A tool for each phase

Andrew's worked example: the prompt is "fix a failing Python unit test."

| Loop phase | What the agent does | Example tool call |
|---|---|---|
| **Gather context** | Understand the failing test | Read `test_payment.py` |
| **Take action** | Make the fix | Edit the file (it needs to know *where* and *what change*) |
| **Verify results** | Confirm the fix worked | Run `pytest`, capture and check the output |

Widen the lens and each phase has a family of tools it might reach for:

```text
GATHER CONTEXT   reading files · searching APIs · querying databases ·
                 codebase scanners · system-state queries
                 (grabbing data from a database to enrich context is RAG —
                  retrieval-augmented generation — and it "just seamlessly
                  happens here," so you rarely think about it)

TAKE ACTION      editing code · running a command · writing files ·
                 calling APIs · executing scripts

VERIFY RESULTS   running a test · compiling code · querying output ·
                 checking logs · comparing results
```

Claude Code ships with **built-in tools in five categories**: file operations, search and find, execution/run, web search, and code intelligence. Can you add your own? Here is a genuine moment of humility from Andrew: "Can you make your own tools? I believe so, like in the context of skills you can. I literally can't remember at this point, but if we can it will be covered in the course. If we can't, then you just won't hear me mention it." Note the honesty — he does not fake certainty. (You *can*, and you will build custom tools and even a whole MCP server in Module 4.)

> ✅ **What to do about it:** whenever you watch an agent work, name the phase and the tool out loud — "it's gathering context by reading a file," "it's taking action by running a command." As Andrew says, "without tools, no code would be changed, nothing would be happening — it would just be talking to you." Tools are where the work happens.

## Part 4: Which model for which job

When Claude Code runs, "it's going to use the same model for all phases of the agentic loop" — one model gathers, acts, and verifies for that run — "and so you have that opportunity to change it at that point in time." You pick the model up front; it stays for the whole loop.

Here are the choices Andrew walks through:

| Choice | What it is | Reach for it when |
|---|---|---|
| **Default** | Claude Code's "best guess" at the right model | You do not want to think about it (usually lands on Sonnet) |
| **Sonnet** | "All-around, well-balanced, the Goldilocks of models" | Daily coding tasks — "that's what you're going to be mostly using" |
| **Opus** | "Really slow, really smart, great for difficult tasks" | Complex reasoning |
| **Haiku** | "Really fast, really dumb, great for general tasks" | Simple, high-volume, cheap work |
| **Sonnet-1M** | Sonnet with a **1-million-token context window** | Long sessions that must hold a lot of text in mind at once |
| **opus-plan** | A special mode: **Opus during plan mode, then Sonnet for execution** | You want deep thinking for the plan but cheaper, faster hands for the doing |

Two of these deserve a second look. **Sonnet-1M** is the same Sonnet, just able to "hold in mind" far more text at once — useful for a long, sprawling session. **opus-plan** is a clever split: it "uses Opus during plan mode, then switches to Sonnet for execution," so you pay for the expensive brain only while it is thinking, not while it is typing.

The mental model Andrew leaves you with, boiled down:

- **Opus** — slow, smart, expensive. Hard problems.
- **Sonnet** — balanced. Your default workhorse.
- **Haiku** — fast, cheap, less clever. Bulk and simple tasks.

He is candid about how to actually choose: "to really understand these, you just really have to use them... For the most part I've just been running Sonnet and have been having no issues. But some people say that if you move over to Opus it's extremely good. But again, you need to drive this stuff and figure it out." And a practical billing note: on the **subscription** plan "it's very hard to gauge usage between these three models, whereas if you are using the **API** you're getting token usage information, so you have a better idea of that spend." (He warns the old intelligence-vs-cost graph in the exam materials is "a bit dated" — the model names on it are older than what you have now. The *shape* — Haiku cheap, Opus dear, Sonnet between — still holds.)

> 🔑 **One model runs the whole loop; you pick it by the job.** Match the model to the difficulty and the budget: Haiku for simple and cheap, Sonnet for everyday, Opus for hard — and let the loop do the rest.

## Part 5: A first look at `stop_reason` (concept only)

The loop has to end *somehow*, and the agent has to signal *why* it stopped after each turn. That signal is the **`stop_reason`** — "the reason why the Claude agent has stopped executing its loop." (By "the Claude agent," Andrew means "whatever the thing is that they have on their server that we're not privy to that is running their agent" — you do not need to see inside it; you just read the field it returns.)

There are two values you care about now:

- **`tool_use`** — the agent stopped *because it wants to call a tool*. "This is when the agent stops with the intention to call an external function." The loop is not done; the model is asking you to run a function and hand back the result.
- **`end_turn`** — the agent is *finished*. "This is when the agent has decided to return you a result because it's done."

Andrew's tiny weather example makes it concrete. Ask "what is the weather in Winnipeg?" and the reply comes back with `stop_reason: tool_use`, naming a tool `get_weather` with the input `Winnipeg` "from what it extracted from the user." Your program runs that tool, appends the result to the conversation, and asks again — and this time the model answers in words and stops with `end_turn`.

```text
you: "what is the weather in Winnipeg?"
        │
        ▼
model → stop_reason: tool_use   (wants get_weather("Winnipeg"))
        │   you run the tool, append its result to the messages
        ▼
model → stop_reason: end_turn   (answers in text — done)
```

That append step — "whatever the result is, we're appending it to our message conversation" — is the hinge that turns two separate replies into one continuous loop. But that is the *implementation*, and it is exactly the next lesson.

> 💡 **Why this feels abrupt.** Andrew jumps straight to `stop_reason` "without talking about the Agent SDK and everything around it" because "we are walking the exam guide... Domain 1, they were talking about stop reason. That's why we're talking about stop reason." His promise: "talk about it, then use it, talk about it, then use it... and then that will accumulate and it will make total sense to you." Take the concept now; you wire it up next lesson.

> ✅ **What to do about it:** remember one rule that carries into the next lesson — you drive the loop off `stop_reason`, the structured field, **never** by reading the model's text and guessing whether it wants a tool. `tool_use` means run a tool and loop; `end_turn` means stop.

---

## Key takeaways

1. **The loop is everything.** Gather context → take action → verify results, repeating and calling tools, until the goal is met, the agent needs feedback, or it stops to save money.
2. **Claude Code is a harness, not magic.** "At the end of it, it's just a CLI program" that runs the loop over your codebase, available across terminal, IDE, desktop, and browser surfaces.
3. **The model is in a box; tools are its hands.** An LLM can only produce text — a tool is "just a code function" it calls to read files, run commands, or check results. Without tools, nothing happens.
4. **One model per loop, picked by the job.** Haiku (fast, cheap, simple), Sonnet (balanced default), Opus (slow, smart, hard problems); plus Sonnet-1M for long context and opus-plan for think-in-Opus-execute-in-Sonnet.
5. **`stop_reason` is how the loop signals itself.** `tool_use` = it wants to run a tool; `end_turn` = it is done. You will build the loop off this field next lesson.
6. **Verify, don't trust.** The docs, the AI's own answers, even the exam guide can be wrong. Andrew's "phantom bug" moment proves the point — the verify phase is what tells you the truth.

## Common pitfalls

- ❌ **Thinking Claude Code "does" the file edits itself.** It does not — the model decides, and a *tool* performs the edit. Confusing the decider with the doer makes the whole loop mysterious.
- ❌ **Believing the agent stopped because it "felt done."** It stops for a concrete reason carried in `stop_reason`. Drive your control flow off that field, never off a vibe or the wording of the text.
- ❌ **Defaulting to Opus "to be safe."** Opus is slow and expensive; most everyday coding runs fine on Sonnet. Reach for Opus for genuinely hard reasoning, Haiku for cheap bulk work.
- ❌ **Treating the intelligence-vs-cost chart as gospel.** Andrew flags it as "a bit dated." The ordering is durable; the exact model names and numbers rot. Verify against current docs.
- ❌ **Skipping verify.** An agent that only gathers and acts is a loose cannon. The verify phase — run the test, check the log, compare the output — is what makes the loop trustworthy.

---

## 🛠️ Capstone Project: Trace the loop (the foundation Atlas Support runs on)

> This is the main hands-on project for the lesson, and it is deliberately conceptual — no working code required. You prove you *understand* the loop by narrating a real task through it and choosing the right model, because every later capstone (the tool-using loop, the coordinator, the escalating support agent) is this same loop, repeated. Get it clear here and the rest of **Atlas Support** stands on solid ground.

### What you will build

A one-page **loop trace**: a labelled diagram plus a short, non-runnable script *stub* (function names and comments, no real logic) that walks a single realistic support-style task through gather context → take action → verify results, names the tool each step would call, and states which model you would run and why. Its pieces:

- A **diagram** of the three-phase loop with your task's steps written into each phase — *maps to Parts 2 and 3*.
- A **tool label on every step** (read / edit / run / test …) — *maps to Part 3*.
- A **model choice with a one-sentence justification** — *maps to Part 4*.
- A **stop-condition note**: where would this loop emit `end_turn`? — *maps to Part 5*.

### Why this is the perfect practice

| Lesson idea | Where you use it in the trace |
|---|---|
| The three-phase loop (Part 2) | The three columns of your diagram |
| Tools as functions per phase (Part 3) | The tool label you attach to each step |
| One model per loop, by the job (Part 4) | Your model pick and its justification |
| `stop_reason` concept (Part 5) | Naming where the loop reaches `end_turn` |
| Verify, don't trust (Part 2 callout) | Making sure your task has a real verify step |

### Milestones (build them in order, each one works on its own)

1. **Pick a task.** Choose one small, verifiable job for a future support agent — e.g., "read a customer's error log and confirm whether the reported bug still reproduces." Write it as one sentence. *(This is the seed of Atlas Support: it starts life as a single task through the loop.)*
2. **Draw the loop.** Copy the three-phase diagram from Part 2 and write your task's concrete step into each phase: what does it gather, what does it change, how does it check?
3. **Label the tools.** On each step, write the tool it would call — Read, Edit, Run/Bash, a test command. If a phase has no natural tool, say so and explain why (some tasks are read-only and never "act").
4. **Choose the model.** Pick Opus, Sonnet, Haiku, Sonnet-1M, or opus-plan for this task and write one sentence justifying it against difficulty and cost. A log-reading check is probably a Haiku or Sonnet job — say why.
5. **Write the stub.** In any language, sketch three empty functions — `gather_context()`, `take_action()`, `verify_results()` — with a comment in each naming its tool, and a top comment marking where the loop would return `end_turn`. No real logic; this is a thinking artifact.
6. **Stop-condition sentence.** In one line, state what would make *your* loop stop: goal met, needs the human, or stopped to save money — and which `stop_reason` value corresponds.
7. **Stretch goals.** Add a second task that genuinely needs Opus and explain the difference. Or add a "phantom bug" branch: what does your verify step do if it discovers the bug was *already* fixed (Andrew's real experience)?

### How you will know you are done

- ✅ Every step in your diagram sits in exactly one phase (gather / act / verify) and carries a tool label.
- ✅ Your model choice has a one-sentence justification tied to difficulty *and* cost.
- ✅ Your stub has all three functions and a comment marking the `end_turn` point.
- ✅ You can explain your trace out loud to someone who has not read this lesson, and they follow it.

> 💡 **Keep yourself honest:** if any step in your trace does not touch a tool, ask whether it is really an *action* or just the model thinking. Only tool-touching steps change the world — that is Andrew's whole point about the box.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice on one idea. Optional and independent; the Capstone already touches all of them, so feel free to skip straight to it.

### Exercise 1: Name the phase (foundational)
For each action, write which loop phase it belongs to: (a) running `pytest`, (b) reading `config.yaml`, (c) editing a function, (d) querying a database for a customer record, (e) comparing two output files. Answers should be gather / take / verify.

### Exercise 2: Match the model (intermediate)
For each job, pick a model and justify it in one line: (a) rename a variable across 200 files, (b) design a tricky concurrency fix, (c) summarise a 900,000-token log in one session, (d) reformat a CSV, (e) plan a big refactor then execute it cheaply. (Expect: Haiku/Sonnet, Opus, Sonnet-1M, Haiku, opus-plan.)

### Exercise 3: Predict the `stop_reason` (advanced)
Write a three-turn conversation for a "check the deploy status" agent and, for each turn, predict whether the reply carries `tool_use` or `end_turn` — and say what tool would run on each `tool_use` turn. You will verify your predictions for real in the next lesson.

---

## Cheat sheet

```text
THE AGENTIC LOOP
  gather context → take action → verify results → (repeat)
  each phase may CALL A TOOL (the only way out of the box)
  ends when: goal met · needs your feedback · stops to save money
  you can interrupt and steer at any time

CLAUDE CODE
  = agentic coding tool + code harness = "just a CLI program"
  at code.claude.com · surfaces: terminal · IDE · desktop · browser
  built-in tool categories (5): file ops · search/find · execution ·
                                 web search · code intelligence

TOOLS
  = "just a code function" the agent knows (name + inputs + output)
  gather : read files · search APIs · query DBs · scan codebase (RAG)
  action : edit code · run command · write files · call APIs · run scripts
  verify : run tests · compile · query output · check logs · compare

MODELS (one model runs the WHOLE loop; pick by the job)
  Opus     slow · smart · $$$   → hard reasoning
  Sonnet   balanced · default   → daily coding  (the Goldilocks)
  Haiku    fast · cheap · basic → simple, high-volume
  Sonnet-1M  Sonnet + 1M-token context → long sessions
  opus-plan  Opus to plan, Sonnet to execute
  subscription = usage hard to gauge · API = token counts visible

stop_reason  (concept now, code next lesson)
  tool_use  → agent wants to run a tool → run it, append result, loop
  end_turn  → agent is done
  RULE: drive the loop off stop_reason, never off the text

MINDSET: docs / AI / exam guide can be wrong → build it and verify
```

## How this connects to the rest of the course

- **Earlier, Module 1 · Lesson 1:** set the exam shape and the "verify everything" mindset. This lesson gives that mindset its home — the *verify* phase of the loop.
- **Next, Module 1 · Lesson 3 ("Tools and the stop-reason loop"):** you stop describing the loop and *build* it by hand — call the API, read `stop_reason`, run the tool, append the `tool_result`, and repeat until `end_turn`.
- **Later, Module 3:** the loop goes multi-agent — a coordinator runs its own loop and delegates to sub-agents that each run *their* loop. Same cycle, nested. And in Module 7, Atlas Support becomes a state machine wrapped around exactly this loop, resolving what it can and escalating the rest to a human.

---

*Source: "Claude Certified Architect: Foundations" by Andrew Brown, ExamPro. Code snippets and diagrams are illustrative reconstructions of the patterns described in the talk. Adapt them to the current SDK.*
