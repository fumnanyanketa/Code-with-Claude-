# Module 3 · Lesson 14: Gates, hooks, and handoff protocols

> **Course:** Claude Certified Architect: Foundations, a self-paced course
> **Module 3:** Orchestration: multi-agent architectures: coordinators, parallelism, and the guardrails that keep them honest
> **Speaker:** Andrew Brown, ExamPro
> **Source:** Reconstructed from the CCA-F course by Andrew Brown (ExamPro) · [full transcript](../../transcripts/cca-f-full-course.txt)
> **Estimated time:** 45 to 60 minutes (read plus lab)

---

## In one sentence

When a prompt alone cannot be trusted to make an agent do the right thing in the right order, you enforce it in code — with **gates** that block an action until its prerequisites are met, **hooks** that fire logic before and after every tool call, and a structured **handoff protocol** that hands a stuck situation to a human with everything they need.

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone
> Project** where you add a pre-tool *gate* and a structured *human handoff* to
> **Atlas Support**, the multi-agent system this course builds end to end. That
> handoff is not throwaway practice — it is the exact piece the Module 7 capstone
> (a support agent that escalates to a human) will stand on. Everything before
> the Capstone teaches the skills you will use there. If you want to see the
> finish line first, jump to the **"Capstone Project"** section, then come back.

## First-principles companion

> 💡 **The durable idea behind this lesson.** SDKs get renamed and hook APIs
> change, but the concept underneath is decades old. A gate is a *precondition*
> and a post-tool check is a *postcondition* — the timeless account is:
>
> - **[Design by Contract](https://www.eiffel.com/values/design-by-contract/introduction/)**
>   (Bertrand Meyer, *Object-Oriented Software Construction*). A routine may run
>   only if its **precondition** holds, and it promises a **postcondition** when
>   it finishes. Swap "routine" for "tool call" and you have exactly the gate-and-hook
>   model in this lesson: enforce the contract in code, not in a hopeful comment.

## A few plain-language basics first

This lesson uses some terms that show up throughout. Here they are in plain words:

- **Agent:** an AI that takes a *series* of actions on its own toward a goal, rather than answering in one shot.
- **Agentic loop:** the repeating cycle an agent runs — gather context, take action, verify — until the task is done.
- **Tool / tool call / tool result:** a function the model can choose to run; when it decides to use one that is a *tool call*, and what comes back is the *tool result*.
- **Coordinator (hub-and-spoke):** an architecture where one *coordinator* agent owns routing and delegates to *sub-agents* ("spokes") exposed to it as tools. This is the shape Atlas Support already has from earlier lessons.
- **Sub-agent:** an agent spawned by another agent, usually with its own isolated context (here: a *research* agent and a *synthesis* agent).
- **Gate:** a check that blocks an action until its prerequisites are met. "Don't let this run until that is done."
- **Hook:** a function that fires *automatically* before or after a tool call — the place you put a gate's logic so it runs every time, without you remembering to call it.
- **Handoff protocol:** a structured package an agent assembles before escalating a problem to a human, so the human has everything they need without digging through the chat.
- **Anthropic SDK vs Claude Agent SDK:** the *Anthropic SDK* is the lower-level library for calling the model API directly; the *Claude Agent SDK* is the higher-level library for building agents, and it has hooks built in. The Python Agent SDK sometimes lags the TypeScript one.
- **Lambda:** a tiny, unnamed function you can pass around like a value. Andrew uses these to hold each gate's rule so the loop stays clean.

You do not need to memorize these. Each is explained again the first time it matters.

## Why this lesson matters

You have spent the last few lessons making a coordinator delegate work to sub-agents — including running them in parallel. But delegation only helps if the sub-agents run in the *right order* and only when they *should*. You might write in the prompt, "always research before synthesizing, and never call synthesis before research has completed." Will the agent obey? As Andrew warns, it might not: "when Claude has long conversations or unusual inputs or it's just having an off day, it will just not listen and will do something else." A prompt is guidance, not a guarantee. This lesson is where your architecture grows a spine — you stop *hoping* and start *enforcing*, and you give the agent a dignified way to quit and call a human when it truly cannot proceed.

## Learning objectives

By the end of this lesson you will be able to:

1. Explain why prompt guidance alone cannot guarantee ordering or prerequisites, and when to reach for code enforcement instead.
2. Write a **prerequisite gate** that makes an out-of-order or unauthorized tool call structurally impossible.
3. Attach **pre-tool and post-tool hooks** so a gate's logic fires automatically around every tool call.
4. Contrast a **roll-your-own** hook system with the **Agent SDK's native** pre/post tool-use hooks, and say why the native one is cleaner and how per-tool matching works.
5. Assemble a **structured handoff package** that escalates to a human with full context.

## Prerequisites

- **Module 3 · Lesson 13 "Running agents in parallel"** and the earlier coordinator lessons — you need a working hub-and-spoke Atlas Support with at least a couple of sub-agent tools to gate.
- Comfort with the coordinator's agentic loop: reading `stop_reason`, seeing a `tool_use`, running the tool, feeding the result back. Gates and hooks slot *into* that loop.
- A little Python. The examples are short; every term is defined.

---

## Part 1: Why a prompt is not enforcement

Here is the situation Andrew sets up. Your coordinator is about to route work. You want a hard rule: **research must finish before synthesis runs.** The natural move is to write it into the prompt:

> "Always research before synthesizing, and never call the synthesis agent before the research agent has completed."

Then you sit back and ask, in Andrew's words, "Okay, well, I wrote that in there. Is it going to do that?" The honest answer is: maybe. The model treats your instruction as strong *guidance*, but under long conversations, weird inputs, or just an "off day," it can quietly ignore it and do something else. For a demo that is annoying; for a support agent that issues refunds, it is a real hazard.

So the question becomes: "How can we get enforcement through some programming stuff?" The answer is to stop relying on the model's goodwill and add a **prerequisite gate** — something that "has to happen or has to be met before it can proceed forward," and which "makes it structurally impossible for them to skip."

> 🔑 **A prompt is a request; a gate is a rule. Anything that must never happen out of order has to be enforced in code, not asked for in the prompt.**

## Part 2: The prerequisite gate

The simplest gate lives right inside your routing logic. Imagine the coordinator's `route` function deciding who to delegate to. You add a check: if we are about to run synthesis but research has not happened yet, don't — send it to research first.

```python
# Illustrative reconstruction — a gate baked into the route function.
def route(context):
    # GATE: synthesis has a prerequisite — research must be done first.
    if context.wants("synthesis") and not context.has("research"):
        # "Hey, you didn't do this first" — force research instead.
        return delegate("research")
    return delegate(context.next_step())
```

That is a real gate: the coordinator *cannot* reach synthesis with empty research, no matter what the model "decided," because the code reroutes it. As Andrew puts it, "you must go run the synthesis agent down here... we are enforcing it that way."

This works, but notice the smell: the enforcement is tangled into the routing. Every new rule means another `if` in the middle of `route`. There is a cleaner home for this logic.

> 💡 **A gate is just a precondition check.** "The prerequisite gate is: don't let
> this run until it is done." Same idea as `assert research_done` before you are
> allowed into the synthesis step.

## Part 3: Hooks — where gate logic belongs

A **hook** is "a function that fires automatically before or after a tool call, which is where you put your logic gate." Instead of scattering `if`s through `route`, you register two functions on the loop:

- a **pre-tool hook** that runs *just before* any tool call, and
- a **post-tool hook** that runs *just after* it returns.

Now the gate lives in the pre-tool hook: "before you do `delegate_synthesis`, if your context is research-not-done, block it." The routing code goes back to being about routing; the *rules* live in hooks that fire on their own.

```text
        coordinator wants to call a tool
                     │
             ┌───────▼────────┐
             │  PRE-TOOL HOOK │  ← gate runs here; may BLOCK the call
             └───────┬────────┘
                     │ (allowed)
                run the tool
                     │
             ┌───────▼────────┐
             │ POST-TOOL HOOK │  ← check/clean up the result here
             └───────┬────────┘
                     │
              feed tool_result back
```

When Andrew asked Claude to build this from scratch (the "roll-your-own" version), it produced a `gate.py` with an `EnforcementGate` object you attach pre- and post-hooks to, plus "four built-in factories" of ready-made rules — things like a **max-hook-calls** limit and a **no-duplicate-arguments** check. When a pre-hook decides a call is illegal, it raises an error and the call never happens. Andrew liked the shape: "It creates a gate, then we can add a hook and a pre-hook. That's kind of cool."

### The refactor that makes it clean: hold each rule in a lambda

The first draft buried each rule inside `if/else` branches in the loop. Andrew pushed back — that "doesn't really seem like a hook architecture." The fix is to store each rule as a **lambda** (a tiny unnamed function passed around like a value; Andrew jokingly calls it a "llama" or "proc"). The loop then just *fires* whatever rules are registered, rather than hard-coding them:

```python
# Illustrative reconstruction — rules as lambdas, fired by the gate.
gate = EnforcementGate()

# Register a rule as a small function (a "lambda"): synthesis needs research.
gate.add_pre_hook(
    "delegate_synthesis",
    lambda ctx: ctx.has("research")   # returns False -> the call is blocked
)

# The loop stays dumb: it just asks the gate to run whatever is registered.
# "The gates fire pre-hooks and they block, then they fire post-hooks, all internally."
```

Now, as Andrew describes the redesign, "the gates fire pre-hooks and they block, and then they fire post-hooks all internally." The loop no longer knows the rules; it just calls `gate.check_pre(...)` and `gate.check_post(...)`. Adding a rule is one more `add_pre_hook`, not surgery on the loop.

> 🔑 **Put rules in hooks, not in the loop. A hook fires every time automatically,
> so a rule you register once can never be forgotten — and holding each rule in a
> lambda keeps the loop clean and the rules easy to add.**

> 💡 **Andrew's honest aside:** he built this in the Python Anthropic SDK and was
> not thrilled with how it read — "I don't really like this in Python... this
> would be a lot better in TypeScript." That is a real judgment worth absorbing:
> rolling your own hook system is fiddly. Which is exactly why Part 5 exists.

## Part 4: The handoff protocol — quitting well

Some situations an agent simply should not resolve alone: a refund above a threshold, a suspected-fraud flag, an ambiguous account. The mature move is to **escalate to a human** — but escalate *well*.

Andrew's definition is the whole idea: "A handoff protocol is a structured package that the agent assembles before escalating. It ensures whoever receives the escalation has everything they need without having to dig through conversation history."

That last clause is the point. A bad handoff is "customer is upset, please help" — now a human has to reread the entire transcript. A good handoff is a **structured package**: the agent synthesizes the conversation into fields a human can act on immediately.

```text
HANDOFF PACKAGE  (what the agent assembles before escalating)
-------------------------------------------------------------
customer_id .......... who this is
issue_summary ........ one-paragraph plain statement of the problem
steps_taken .......... tools the agent already ran (lookup_order, attempt_refund, ...)
current_state ........ e.g. "fraud flag set; refund blocked pending review"
why_escalating ....... the rule that tripped (amount over limit / fraud / ambiguity)
requested_action ..... exactly what the human needs to decide or do
raw_context .......... link/pointer to full transcript, if they want it
```

In the build, the coordinator has support tools — `lookup_order`, `attempt_refund`, `clear_fraud_flag`, `simulate_backend`. When the loop hits a case it must not handle, it calls a `build_handoff` step: the agent is asked "to synthesize a structured handoff package for the conversation," and then it **escalates** — stages that package for a person. On screen, "it attempts it and then it has to escalate to the customer." The agent did not fail silently or guess; it packaged the problem and handed it up.

> ✅ **What to do about it:** decide your escalation *triggers* explicitly (amount
> over X, fraud flag, low confidence), and for each one have the agent emit the
> full structured package — never a bare "help." The human should be able to act
> from the package alone.

## Part 5: The SDK-native hooks (why you usually shouldn't roll your own)

Here is the payoff, and it comes with a build-and-verify lesson attached.

The **Claude Agent SDK** has pre-tool-use and post-tool-use hooks built in. You register them on the agent, "so that you can go and intersect them" around your tools. No `gate.py`, no factories, no lambda plumbing — the machinery you hand-built in Part 3 is already there.

Two things make the native version better than roll-your-own:

- **Per-tool matching.** The default matches on *all* tools, but "if you wanted to, you could tell it to match on a very specific tool." So you can set "exactly what the pre and post tool hook is for each individual allowed tool" — a fraud check only around `attempt_refund`, say, instead of one big handler branching on tool name.
- **It is just cleaner.** After wiring it up, Andrew's verdict on the roll-your-own version: "we created like this whole hook system and it was so complicated. But why not just use this because it's right here." The native hooks are "obviously better than rolling your own if you're using the Agent SDK."

Now the judgment lesson — the recurring theme of this whole course. When Andrew first asked, the Python SDK reported it "does not have built-in pre-post hooks," and even he second-guessed himself: "I don't know why I thought there was pre-post hooks." He pushed back — "Are these not part of the SDK? Is this another limitation of the Python SDK?" — and on re-checking, the truth surfaced: **pre and post hooks *are* built into the Agent SDK; they are just not the same thing as the Claude Code CLI's hooks feature.** The first answer was wrong. Only by challenging it and verifying did the real picture appear.

> 🔑 **If you are on the Claude Agent SDK, use its native pre/post tool-use hooks
> and per-tool matching — do not hand-roll a gate system. But confirm what the SDK
> actually supports by running it: the first answer you get (from the AI, the docs,
> or your own memory) may be wrong.**

> 💡 **Don't confuse the two "hooks."** Claude Code (the CLI) has its own hooks
> feature; the Agent SDK has *tool-use* hooks for agents you build. Same word,
> different mechanism. The confusion above came from exactly this overlap.

---

## Key takeaways

1. **A prompt is guidance, not enforcement.** Under long context or an "off day," the model can ignore ordering rules. Anything that must never happen out of order goes in code.
2. **A gate blocks until prerequisites are met** — "don't let this run until it is done" — making a skipped step structurally impossible.
3. **Hooks are where gate logic belongs:** a pre-tool hook (runs before, can block) and a post-tool hook (runs after). Register rules as lambdas so the loop stays clean.
4. **The handoff protocol is a structured package**, not a plea. It gives a human summary, steps taken, current state, escalation reason, and requested action — no transcript-digging required.
5. **Prefer the Agent SDK's native pre/post tool-use hooks** over rolling your own; they support per-tool matching and are far cleaner. Verify what the SDK really supports by running it — the first answer can be wrong.

## Common pitfalls

- ❌ **Writing the rule only in the prompt.** "Always research first" is a wish. If skipping it can cause harm, gate it in code.
- ❌ **Burying gate logic in the routing `if/else`.** It tangles routing with rules and is easy to forget on the next tool. Move it into hooks; hold each rule in a lambda.
- ❌ **Rolling your own hook system when the SDK already has one.** You will rebuild `gate.py` and factories that ship for free. Use native hooks if you are on the Agent SDK.
- ❌ **A vague escalation.** "Customer is upset, please help" forces the human to reread everything. Emit the full structured package instead.
- ❌ **Trusting the first answer about SDK support.** The Python SDK first "said" no built-in hooks; it was wrong. Push back and run it.
- ❌ **Confusing Claude Code CLI hooks with Agent SDK tool-use hooks.** Same word, different feature — pick the one that matches what you are building.

---

## 🛠️ Capstone Project: A pre-tool gate and human handoff for Atlas Support

> This is the main hands-on project for the lesson. You will make Atlas Support
> *refuse* to do a dangerous thing without a prerequisite, and *escalate well*
> when it must stop — the two habits that separate a toy agent from one you would
> let near a real customer. Keep it small: one gate, one handoff.

### What you will build

Two guardrails bolted onto the Atlas Support coordinator you already have:

- **A pre-tool gate** on the `attempt_refund` tool: the refund may not run unless a prerequisite is met (the order was looked up *and* no fraud flag is set). If the prerequisite fails, the pre-tool hook blocks the call.
- **A structured human handoff:** when a case trips an escalation trigger (refund over a threshold, or a fraud flag), the agent assembles a structured handoff package and escalates to a human instead of acting.

Each piece maps to a lesson idea:

- Gate → Part 2 (prerequisite gate) fired from a Part 3 pre-tool hook.
- Handoff package → Part 4 (the structured escalation).
- Optional native rewrite → Part 5 (Agent SDK pre/post tool-use hooks).

### Why this is the perfect practice

| Lesson idea | Where you use it in Atlas Support |
|---|---|
| Prompt is not enforcement (Part 1) | You *stop trusting* the prompt for the refund rule and gate it |
| Prerequisite gate (Part 2) | `attempt_refund` blocked until order-looked-up + no-fraud |
| Pre/post hooks + lambdas (Part 3) | The gate fires from a registered pre-tool hook, rule held in a lambda |
| Handoff protocol (Part 4) | A structured package the agent emits before escalating |
| Native SDK hooks + per-tool match (Part 5) | Optional: rewrite the gate as an Agent SDK pre-tool hook matched to `attempt_refund` |

### Milestones (build them in order, each one works on its own)

1. **Add a pre-tool hook that logs.** Before any tool call in the coordinator loop, print the tool name and arguments. Smallest working version: it just prints — you have proven the hook fires.
2. **Turn it into a gate on `attempt_refund`.** In the pre-tool hook, if the tool is `attempt_refund` and the prerequisite is unmet (no prior `lookup_order`, or a fraud flag is set), *block* the call and return a clear reason. Verify by trying to refund before looking up an order — it must be refused.
3. **Hold the rule in a lambda.** Move the prerequisite check into a lambda registered against `attempt_refund`, so the loop just fires registered rules. Adding a second rule should be one more registration, not a new `if` in the loop.
4. **Define your escalation triggers.** Pick two: refund amount over a threshold, and fraud flag set. Decide, in code, that these must escalate rather than act.
5. **Build the handoff package.** When a trigger fires, have the agent synthesize a structured package (customer_id, issue_summary, steps_taken, current_state, why_escalating, requested_action) and stage it for a human. Verify the loop escalates instead of calling `attempt_refund`.
6. **Prove both paths.** Run one clean case that passes the gate and refunds, and one case that trips a trigger and produces a handoff package. Confirm the human-readable package is complete enough to act on without the transcript.
7. **Stretch goals.** Rewrite the gate as an **Agent SDK native pre-tool hook** matched specifically to `attempt_refund` (Part 5), and add a **post-tool hook** that records every completed tool call to an audit log. Compare the native version's cleanliness to your roll-your-own.

### How you will know you are done

- ✅ Calling `attempt_refund` before `lookup_order`, or with a fraud flag set, is **blocked by the pre-tool hook** — not merely discouraged in the prompt.
- ✅ The prerequisite rule lives in a registered lambda/hook, not inline in the loop; adding a rule does not touch the loop body.
- ✅ A triggering case produces a **structured handoff package** with all required fields and escalates to a human instead of acting.
- ✅ A human could act on the package alone, without reading the conversation.
- ✅ (Stretch) The gate also runs as an Agent SDK native pre-tool hook matched only to `attempt_refund`.

> 💡 **Keep yourself honest:** a gate only counts if you *watched it block* a bad
> call, and a handoff only counts if a teammate (or future you) could act from the
> package without opening the transcript. Run both paths; don't just read the code.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice
> on one idea. Optional and independent; the Capstone already touches all of
> them, so feel free to skip straight to it.

### Exercise 1: Break it with a prompt, fix it with a gate (foundational)
Tell your coordinator in the prompt "never refund before looking up the order," then deliberately prompt it into refunding first until it slips. Now add the pre-tool gate and watch the same attempt get blocked. Feel the difference between asking and enforcing.

### Exercise 2: Rules as lambdas (intermediate)
Refactor a gate written as inline `if/else` into a lambda registered on the gate. Then add a *second* rule (e.g., block `clear_fraud_flag` unless a manager_id is present) purely by registering another lambda — with zero changes to the loop body.

### Exercise 3: Native per-tool hooks (advanced)
Using the Agent SDK, attach a pre-tool hook matched to *only* `attempt_refund` and a post-tool hook matched to *all* tools. Verify (by running it) that the refund hook does not fire for other tools. Note where the SDK's real behavior differed from your first assumption.

---

## Cheat sheet

```text
GATES, HOOKS & HANDOFF — enforcing agent behavior in code
---------------------------------------------------------
WHY            A prompt is guidance, not a guarantee. Under long context /
               odd inputs / "an off day," the model may ignore ordering rules.
               Enforce the must-nots in CODE.

GATE           A prerequisite check that BLOCKS an action until met.
               "Don't let this run until that is done."  (= a precondition)

HOOK           A function that fires AUTOMATICALLY around a tool call:
                 pre-tool  -> runs BEFORE; can BLOCK the call  <- put the gate here
                 post-tool -> runs AFTER;  check / clean up / audit
               Hold each rule in a LAMBDA; the loop just fires registered rules.

ROLL-YOUR-OWN  gate.py + EnforcementGate + factories (max-calls, no-dupe-args).
               Works, but fiddly ("complicated," nicer in TypeScript).

SDK-NATIVE     Claude Agent SDK has pre/post TOOL-USE hooks built in.
  (preferred)  - PER-TOOL MATCHING: match all tools, or one specific tool.
               - Cleaner: "why not just use this, it's right here."
               - NOT the same as Claude Code CLI hooks. Verify by RUNNING it.

HANDOFF        Structured package the agent assembles BEFORE escalating,
  PROTOCOL     so a human needs no transcript-digging:
                 customer_id · issue_summary · steps_taken · current_state
                 · why_escalating · requested_action
               Triggers: amount over limit / fraud flag / low confidence.

RULE OF THUMB  Must-never-happen -> gate it. Cannot-resolve -> hand it off.
               On the Agent SDK -> native hooks, not your own.
```

## How this connects to the rest of the course

- **Earlier, Module 3 · Lesson 13 "Running agents in parallel":** you made the coordinator delegate to (and fan out across) sub-agents. This lesson adds the guardrails that keep those delegations in order and safe.
- **Next, Module 3 · "Prompt chaining vs adaptive decomposition":** you will choose between a fixed sequential pipeline and a plan that adapts to intermediate findings — orchestration shapes that these same gates and hooks keep honest.
- **Later, Module 7 (capstone):** the **support agent that escalates to a human** is built directly on the handoff package you assemble here. What you write in this lesson's capstone is the seed of that final build — Atlas Support learns to know its limits and call for help.

---

*Source: reconstructed from the "Claude Certified Architect: Foundations" course by Andrew Brown (ExamPro). Code snippets and diagrams are illustrative reconstructions of the patterns described in the course; adapt them to the current SDK.*
