# Module 3 · Lesson 7: Code-driven vs model-driven decisions

> **Course:** Claude Certified Architect: Foundations, a self-paced course
> **Module 3:** Orchestration: multi-agent architectures: turn one agent into a reliable coordinated system
> **Speaker:** Andrew Brown, ExamPro
> **Source:** Reconstructed from the CCA-F course by Andrew Brown (ExamPro) · [full transcript](../../transcripts/cca-f-full-course.txt)
> **Estimated time:** 45 to 60 minutes (read plus lab)

---

## In one sentence

Every branch point in an agent system is a choice between letting **your code**
decide what happens next (fast, cheap, predictable) and letting **the model**
decide at runtime (flexible, but slower, pricier, and less certain) — and knowing
which to pick, and why, is the first real orchestration skill.

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone
> Project** where you implement the *same* Atlas Support intake decision two ways
> — once as a hard-coded classifier, once as model-driven tool routing — and
> compare them side by side. Everything before the Capstone teaches the judgment
> you will use there. If you want to see the finish line first, jump to the
> **"Capstone Project"** section, then come back.

## First-principles companion

> 💡 **The durable idea behind this lesson.** The tools and model names will
> change; the distinction will not. For the timeless, vendor-neutral version:
>
> - **[Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)**
>   (Anthropic engineering, Dec 2024). It draws exactly this line: *workflows*,
>   where LLM steps are orchestrated through predefined code paths, versus
>   *agents*, where the model directs its own process and tool use. This lesson
>   is that essay made concrete.
> - **[Finite-state machine](https://en.wikipedia.org/wiki/Finite-state_machine)**
>   (computer science). The "hard-code the control flow" half of this lesson is a
>   direct application of a 70-year-old idea: a fixed set of states and the rules
>   for moving between them.

## A few plain-language basics first

This lesson uses some everyday terms. Here they are in plain words:

- **LLM:** the kind of AI that reads and writes text; "Claude" is one.
- **Model:** one specific version of that AI (Opus, Sonnet, Haiku) differing in
  strength, speed, and price.
- **Token:** the unit a model reads and writes in, about ¾ of a word; you are
  billed per token, so every model call costs money.
- **Agent:** an AI that takes a series of actions on its own toward a goal,
  rather than answering in one shot.
- **Agentic loop:** the repeating cycle an agent runs — gather context, take
  action, verify — until the task is done.
- **Tool / tool call / tool result:** a function you let the model choose to run;
  when it decides to use one, that decision is a *tool call*, and what the
  function returns is the *tool result*.
- **`stop_reason`:** the field the API returns saying *why* the model stopped —
  `tool_use` (it wants to run a tool) or `end_turn` (it is finished). You drive
  the loop off this, never off reading the text.
- **Control flow:** the order in which the steps of a program run — which branch
  is taken, what happens next. "Who owns the control flow" is the whole question
  of this lesson: your code, or the model.
- **State machine:** a program written as a fixed set of *states* with rules for
  moving between them ("from *awaiting-payment* you can go to *paid* or
  *cancelled*"). A structured way to hard-code control flow.
- **Coordinator / hub-and-spoke:** an architecture where one *coordinator* agent
  sits at the center, owns routing, and delegates to *sub-agents* ("spokes")
  around it. This lesson is the on-ramp to it.

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

Up to now you have built *one* agent that runs *one* loop. The moment you have
more than one thing an agent could do next — send this ticket to billing or to
tech support, check inventory or place an order — you face a design decision that
shapes cost, speed, and reliability for the whole system. As Andrew puts it,
"both options are valid and useful. It's just depending on what you're doing."
The exam leans model-driven — "Anthropic wants you to be model driven, right?
Because that's what they're trying to sell you on" — but Andrew is blunt that a
good architect keeps both tools on the belt. This lesson gives you the judgment
to reach for the right one instead of defaulting.

## Learning objectives

By the end of this lesson you will be able to:

1. Define **code-driven** (preconfigured) and **model-driven** decision-making
   and say exactly which one owns the control flow in each.
2. Explain why a state machine is "not really agentic," and why that is sometimes
   the point.
3. List the trade-offs — determinism, cost, latency, reliability vs. flexibility
   — and pick the right approach for a given branch point.
4. Implement the *same* routing decision two ways: a hard-coded classifier and
   model-driven tool routing.
5. Recognise how model-driven routing becomes the coordinator in a hub-and-spoke
   architecture (your next lesson).

## Prerequisites

- **Module 1 · Lesson 3 (Tools and the stop-reason loop)** — you will reuse the
  call-the-API, read `stop_reason`, run-the-tool loop here.
- **Module 1 · Lesson 4 (Ending the loop correctly)** — model-driven routing runs
  inside a loop; you already know to break on `stop_reason`.
- **Module 2 · Lesson 6 (Forcing structured output)** — the code-driven classifier
  leans on getting a clean, single-word category back.
- A Python environment with the Anthropic SDK and an API key (Module 0).

---

## Part 1: Two ways to decide "what happens next"

Every agent system is a series of decisions. At each one, someone has to choose
the next step. There are only two candidates for who that "someone" is: **your
code** or **the model**. That is the whole lesson.

**Code-driven** (Andrew's transcript calls it *preconfigured*, and grumbles that
"code-driven" is the better word — "I swear to goodness the marketing material is
being done by an agent"). Here **you hardcode the logic and the code decides what
happens next.** The simplest form is an `if/else`. Andrew: "A very simple one
would be an if/else statement. So if this then do that." The more structured form
is a **state machine** — "where it's saying what the initial state is and you can
transition to other states." You may also hear Anthropic say **tool sequence**;
that is just their name for "a state machine or a series of steps."

**Model-driven** (an actual agentic system). Here "you hand Claude a set of tools
and a goal and Claude figures out the sequence itself at runtime based on context.
You don't tell it what to call or when." The model reads the situation and picks
the next action every turn.

> 🔑 **The one question that decides everything: who owns the control flow?** If
> the *code* chooses the branch, it is code-driven. If the *model* chooses, it is
> model-driven. Everything else — cost, reliability, flexibility — follows from
> that one fact.

## Part 2: Why a state machine is "not really agentic"

Here is a piece of history worth keeping. When people first tried to figure out
what an agent even was, "they would implement state machines, because that was the
way they would set up the complex logic." It worked — but Andrew is precise about
why we no longer call it agentic:

> "Something that's agentic is that it goes through an agentic loop where each
> time the decision is being made by the agent itself and not by the code. So if
> the code is making the decision then it's not exactly agentic now is it? But if
> the agent is deciding then it actually is agentic." — Andrew

That is the whole definition in two sentences. Agentic is not about using an LLM
somewhere in the system — a state machine can call Claude on every step. It is
about *who decides the next move*. A state machine that calls the model to fill in
a blank, then follows a fixed transition you wrote, is still code-driven: the
model was a worker, not the decider.

> 💡 **"Not agentic" is not an insult.** A state machine being non-agentic is
> exactly why you would reach for it: you *want* the branch to be certain, not
> reasoned about. The label describes where the decision lives, not which design
> is "better."

## Part 3: The trade-offs — determinism vs. flexibility

Both approaches are valid. You pick based on what the branch point needs. Here is
the trade-off laid out.

| Dimension | Code-driven (if/else, state machine) | Model-driven (tools + goal) |
|---|---|---|
| **Who decides** | Your code | The model, at runtime |
| **Determinism** | High — same input, same path, every time | Lower — the model may route differently across runs |
| **Cost (tokens)** | Low — code branches are free; you pay only for the model calls you *choose* to make | Higher — every routing decision is a model call, and the loop may take several |
| **Latency** | Fast — a branch is instant | Slower — each decision is a round-trip to the API |
| **Reliability** | Predictable; no hallucinated branch | Can pick a wrong or surprising tool |
| **Flexibility** | Rigid — it only handles cases you foresaw | Adapts to inputs you never wrote a branch for |
| **Observability** | Trivial — the path is in your code | Needs instrumentation to see why it chose what it chose |

Andrew's own example for **when code-driven wins**: a multi-user dungeon (a text
adventure game). "You have very specific logic that you want to play out, but you
want to have some flexibility. This is where you can get a trade-off where you
have this logical structure that keeps the game working in a very particular way
where you're not worried about things hallucinating and you're not consuming lots
of tokens." The code owns the rules of the world; the model only handles the
open-ended bits (say, describing a room). You get certainty *and* cheapness where
it matters.

> ✅ **What to do about it:** reach for **code-driven** when the branches are
> known, must be certain, must be cheap, or must be fast — routing by a fixed
> rule, enforcing a required order of steps, guarding game or business logic.
> Reach for **model-driven** when the space of situations is open-ended and you
> want the system to adapt to inputs you did not enumerate. Most real systems mix
> both.

## Part 4: A quiet truth about model-driven tools and the system prompt

When you built the stop-reason loop in Module 1, you handed Claude a list of tools
in the API request — but notice you *never* wrote "here are your available tools"
into the system prompt. That is deliberate, and it trips up people coming from
older frameworks.

> "You'll notice that when we did the stop reason video, we never put in the
> system prompt that these were the tools that were available... The models got
> smart enough that you didn't have to do this anymore. Or maybe there's something
> in their API, they're doing some abstraction for us... When we're using the
> Claude API, we just literally specify these are the tools we have. We don't have
> to literally tell it what tools are available." — Andrew

In other words: the `tools` array you pass to the Messages API *is* how the model
learns its options. The tool `name` and `description` you write there get picked
up and reasoned over — "that's how it would reason." You do not, and should not,
re-list them in prose. In the lab, Andrew adds a tool list to the system prompt
only "as a demonstration of where it used to go," then notes the model works fine
without it. This is a recurring theme of the course: **build it and verify** —
the old habit (spell out tools in the prompt) turns out to be unnecessary once you
actually try it.

> 🔑 **For model-driven routing you give the model two things: the `tools`
> (each with a clear `name` and `description`) and a `goal` in the system prompt.
> The descriptions *are* the routing instructions. Write them well and the model
> routes well.**

## Part 5: Where this is heading — the coordinator

Model-driven routing is not just a party trick; it is the engine of the
architecture the rest of this module is about. Andrew introduces it here:

> "Something we're going to hear a lot about is the hub and spoke architecture for
> setting up a coordinator agent. This is where you will have a single agent
> sitting at the center and it's going to talk out to other sub agents around it,
> and it's going to intercept all communication between it." — Andrew

A **coordinator** is one agent that sits at the hub. Its "spokes" are sub-agents,
each exposed to it as a tool. The coordinator owns the routing (which spoke gets
the work), the context sharing (a spoke only knows what the coordinator passes
it), and the error handling and observability (everything flows through one
choke point). Sub-agents "never have direct lines to each other" — they always go
through the hub.

Look closely and the coordinator is just Part 1's model-driven routing scaled up:
give one agent a goal and a set of tools *that happen to be other agents*, and let
it decide, at runtime, which to call. That is why this lesson comes first. Build
the judgment here on a two-tool intake router, and next lesson the same pattern
becomes your first real coordinator.

```text
        code-driven                         model-driven
   (this lesson, Part 1)              (this lesson, Parts 4-5)
                                                │
   input → [if/else] → branch        input → ( model + tools + goal )
           you wrote                          │  model picks the tool
                                              ▼
                                    ──►  grows into  ──►  HUB-AND-SPOKE
                                              coordinator = model-driven
                                              router whose tools are agents
                                                   (Lesson 8)
```

---

## Key takeaways

1. **One question decides it: who owns the control flow — your code or the
   model?** Code-driven = your `if/else` or state machine chooses. Model-driven =
   Claude chooses at runtime from tools + a goal.
2. **A state machine is "not really agentic," and that can be exactly why you
   want it.** Non-agentic means the decision is certain and lives in your code —
   perfect when you cannot afford a hallucinated branch.
3. **The trade-off is determinism/cost/speed/reliability vs. flexibility.**
   Code-driven is cheap, fast, and predictable but only handles cases you
   foresaw; model-driven adapts but costs a call per decision and can surprise you.
4. **For model-driven routing, the `tools` array is the routing brain.** The model
   learns its options from tool `name` + `description`; you do not re-list them in
   the prompt.
5. **Model-driven routing scales up into the hub-and-spoke coordinator** — same
   pattern, where the tools are sub-agents.

## Common pitfalls

- ❌ **Thinking "uses an LLM" means "agentic."** A state machine can call Claude
  on every step and still be code-driven. Agentic is about *who decides the next
  move*, not whether a model is involved anywhere.
- ❌ **Reaching for model-driven by default because the exam prefers it.** You pay
  a model call for every decision. For a fixed 3-way route that must be cheap and
  certain, a classifier + `if/else` is the better engineering choice. Andrew:
  "both are useful."
- ❌ **Re-listing your tools in the system prompt.** Unnecessary with the modern
  API — the `tools` array already teaches the model its options. Spend that effort
  on writing sharp tool descriptions instead.
- ❌ **Vague tool descriptions in a model-driven router.** The descriptions *are*
  the routing rules. "handle_billing: charges, refunds, invoices, payment
  problems" routes far better than "handle_billing: billing stuff."
- ❌ **Running model-driven routing in a `while True:` with no exit.** The loop
  must break on `stop_reason == "end_turn"` and carry a max-iteration cap (Module
  1 · Lesson 4), or a wrong turn burns tokens forever.

---

## 🛠️ Capstone Project: the Atlas Support intake router, built both ways

> This is the main hands-on project for the lesson. You will build the *same*
> decision — "where does this incoming support message go?" — twice, once
> code-driven and once model-driven, and feel the trade-off in your own hands.
> Keep it small on purpose.

### What you will build

**Atlas Support** (the north-star system you build across this whole course) needs
an **intake router**: the very first step that reads a customer message and sends
it to the right place — billing, technical, or general. This is the piece Atlas
Support's future coordinator will stand on. You will implement it two ways against
the same three test messages, then compare.

Its pieces, each mapped to a lesson idea:

- A **code-driven classifier** — model classifies into one category, your code
  routes (Parts 1–3).
- A **model-driven router** — Claude is given route tools + a goal and picks
  (Parts 4–5).
- A **comparison** — same inputs, both approaches, side by side (Part 3's
  trade-off table, made real).

### Why this is the perfect practice

| Lesson idea | Where you use it in the intake router |
|---|---|
| Code owns the control flow (Part 1) | The classifier's `if/else` picks the branch |
| State machine / non-agentic on purpose (Part 2) | The code-driven route is certain and free |
| Determinism vs. cost vs. flexibility (Part 3) | You compare the two runs directly |
| `tools` array is the routing brain (Part 4) | The model-driven router's tool descriptions |
| Routing grows into a coordinator (Part 5) | This router becomes Lesson 8's hub |

### Milestones (build them in order, each one works on its own)

1. **Set up three fixtures.** Create a folder `decision-making/` and a list of
   three real support messages — one per category — so both builds share input:

   ```text
   "I was charged this twice this month. Can you help?"      → billing
   "My app keeps crashing after the latest update."         → technical
   "What are your business hours?"                          → general
   ```

2. **Build the code-driven classifier (`code_driven.py`).** Ask the model to do
   one narrow job and nothing else, then let *your code* route. Illustrative
   reconstruction:

   ```python
   # illustrative — adapt to the current SDK
   SYSTEM = (
       "You are a customer-support classifier. Classify the user message into "
       "exactly one of these categories: billing, technical, or general. "
       "Respond with only the category name and nothing else."
   )

   def classify(message: str) -> str:
       resp = client.messages.create(
           model="claude-haiku-4-5",          # cheap model for a tiny job
           max_tokens=10,
           system=SYSTEM,
           messages=[{"role": "user", "content": message}],
       )
       return resp.content[0].text.strip().lower()

   def route(message: str) -> str:
       category = classify(message)           # the model answers...
       if category == "billing":              # ...your CODE decides.
           return handle_billing(message)
       elif category == "technical":
           return handle_technical(message)
       else:
           return handle_general(message)
   ```

   Each `handle_*` can just print what it would do ("Routing to the billing team.
   Pull account record and check payment status."). Run it over all three
   fixtures. **You now have a working router that costs exactly one model call per
   message and always takes a branch you wrote.**

3. **Build the model-driven router (`model_driven.py`).** Now hand the model
   *tools* — one per destination — plus a goal, and let it choose. Reuse your
   stop-reason loop from Module 1:

   ```python
   # illustrative — adapt to the current SDK
   tools = [
       {"name": "route_billing",
        "description": "Route to the billing team. Use for charges, refunds, "
                       "invoices, double-charges, and payment problems.",
        "input_schema": {"type": "object",
                         "properties": {"reason": {"type": "string"}},
                         "required": ["reason"]}},
       {"name": "route_technical",
        "description": "Route to technical support. Use for crashes, bugs, "
                       "errors, and things not working after an update.",
        "input_schema": {"type": "object",
                         "properties": {"reason": {"type": "string"}},
                         "required": ["reason"]}},
       {"name": "route_general",
        "description": "Route to general support. Use for hours, policies, "
                       "and anything not billing or technical.",
        "input_schema": {"type": "object",
                         "properties": {"reason": {"type": "string"}},
                         "required": ["reason"]}},
   ]

   SYSTEM = "You are Atlas Support intake. Read the customer message and route it "
            "to the correct team by calling exactly one tool."

   MAX_STEPS = 10                              # cap the loop (Lesson 4)
   # loop: create → if stop_reason == "tool_use", that tool IS the route;
   #       append the tool_result, continue; break on "end_turn" or the cap.
   ```

   Note what you did *not* do: you never listed the tools in the prose of the
   prompt. The `description` fields carry the routing logic. Run it over the same
   three fixtures.

4. **Compare.** Put the two runs side by side and answer, in a short note:
   - Did both send all three messages to the same teams?
   - How many model calls did each make per message? (Classifier: one. Router:
     one or more, since it runs a loop.)
   - Which would you trust for a fixed 3-way route in production, and why?

5. **Stress the difference.** Add a fourth, ambiguous message — e.g. *"I was
   charged for a plan but the upgrade button is broken."* Run both. Watch the
   code-driven classifier force it into one bucket, and see whether the
   model-driven router reasons about it differently. This is the flexibility
   trade-off, live.

6. **Stretch goals.** (a) Make the classifier fall back to `general` on any
   unexpected category string, so a surprise output can never crash routing.
   (b) Log each routing decision as one JSON line (`message`, `route`, `approach`,
   `model_calls`) — you will thank yourself when this becomes a coordinator.
   (c) Add a fourth team and feel how much cheaper it is to extend the
   model-driven router (add a tool) than to re-plan the classifier's categories.

### How you will know you are done

- ✅ `code_driven.py` routes all three fixtures with **exactly one** model call
  each, and the branch is chosen by your `if/else`.
- ✅ `model_driven.py` routes the same fixtures by **calling a tool**, with the
  loop breaking on `end_turn` and a max-iteration cap in place.
- ✅ No tool list appears in the model-driven system prompt — routing rides on the
  tool `description`s.
- ✅ You can state, in one sentence each, when you would choose each approach for
  Atlas Support.

> 💡 **Keep yourself honest:** count the model calls. If your "cheap" code-driven
> path is quietly making more calls than the model-driven one, you have built the
> worst of both worlds — go find the extra call.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice on
> one idea. Optional and independent; the Capstone already touches all of them, so
> feel free to skip straight to it.

### Exercise 1: Name the owner (foundational)
For each system, say who owns the control flow — code or model — and why: (a) a
thermostat that turns on heat below 68°F; (b) an agent given a `search`, a `read`,
and an `email` tool and told "find and summarise today's news"; (c) a checkout
flow that calls the model to extract an address, then follows a fixed
validate → charge → confirm sequence. (Answers: code; model; code — the model is
a worker inside a state machine.)

### Exercise 2: Sharpen a description (intermediate)
Take your model-driven router and rewrite each tool `description` to be as vague
as possible ("handle billing things"). Re-run the fixtures. Then rewrite them to
be crisp and specific. Note how routing accuracy tracks the description quality —
proof that the `tools` array is the routing brain.

### Exercise 3: Convert one into the other (advanced)
Take a small state machine you have (or the classifier from the Capstone) and
convert it to model-driven — one tool per transition, a goal in the system prompt,
no hard-coded branches. Then argue in three sentences whether the conversion was a
good idea for *this* problem. The skill is not "always convert"; it is knowing
when not to.

---

## Cheat sheet

```text
CODE-DRIVEN vs MODEL-DRIVEN — who owns the control flow?

CODE-DRIVEN (a.k.a. "preconfigured", "tool sequence")
  - You hardcode the logic; the CODE decides what's next.
  - Forms: if/else  →  state machine (states + transitions).
  - NOT agentic (the code decides) — and that's often the point.
  - Pros: deterministic, cheap (no call to branch), fast, reliable.
  - Cons: rigid — only handles cases you foresaw.
  - Use when: known branches, must be certain / cheap / fast.
  - Ex: dungeon-game rules, required step order, fixed N-way route.

MODEL-DRIVEN (an actual agentic system)
  - Give the model TOOLS + a GOAL; the MODEL decides at runtime.
  - You do NOT say what to call or when.
  - The `tools` array IS the routing brain — name + description
    carry the logic. Do NOT re-list tools in the prompt.
  - Pros: flexible, adapts to inputs you never enumerated.
  - Cons: a model call per decision (cost + latency), can surprise.
  - Runs in a loop → break on stop_reason == "end_turn" + max-iter cap.
  - Use when: open-ended situations, want adaptation.

THE ONE QUESTION:  code decides → code-driven.  model decides → model-driven.
BOTH ARE VALID. Pick per branch point. Most real systems MIX them.

WHERE IT GOES NEXT:
  model-driven routing, scaled up, = the HUB-AND-SPOKE COORDINATOR
  (one agent at the hub; its tools are sub-agents / "spokes").
```

## How this connects to the rest of the course

- **Earlier, Module 1 · Lessons 3–4:** you built the stop-reason loop and learned
  to end it correctly. The model-driven router here *is* that loop, now used to
  route instead of to do one task.
- **Earlier, Module 2 · Lesson 6:** forcing structured output. The code-driven
  classifier depends on getting one clean category back — the same discipline.
- **Next, Module 3 · Lesson 8 (Hub-and-spoke: your first coordinator):** you take
  the model-driven router and make its tools into sub-agents. Same pattern, one
  step up — the coordinator is a model-driven router whose choices are other
  agents.
- **Later, Module 3 · Lessons 9–15:** task decomposition, refinement loops,
  parallelism, and handoff all live *inside* the coordinator you are about to
  build — every one of them is another "who decides?" call you now know how to
  make.

---

*Source: the CCA-F course by Andrew Brown, ExamPro. Code snippets and diagrams are
illustrative reconstructions of the patterns described in the course. Adapt them to
the current SDK.*
