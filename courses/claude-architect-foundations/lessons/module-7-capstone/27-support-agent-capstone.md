# Module 7 · Lesson 27: Build a support agent with progressive escalation

> **Course:** Claude Certified Architect: Foundations, a self-paced course
> **Module 7:** Capstone: put it all together — combine the whole course into one production-shaped agent
> **Speaker:** Andrew Brown, ExamPro
> **Source:** Reconstructed from the CCA-F course by Andrew Brown (ExamPro) · [full transcript](../../transcripts/cca-f-full-course.txt)
> **Estimated time:** 50 to 60 minutes (read plus lab)

---

## In one sentence

A production support agent is a **state machine**: it starts in a "bot handling" state where it resolves the common requests it is allowed to resolve, and on an explicit trigger — a legal threat, a policy gap, a customer who asks for a person, or too many failed attempts — it flips to an "escalate" state and hands the ticket to a human with a **structured handoff package**, logging every step along the way.

> 🎯 **Where this lesson is heading.** This is the **course capstone**. It builds
> to the complete **Atlas Support** agent — the north-star project every lesson
> before this one contributed a piece to. You will assemble the tool loop
> (Module 1), structured output (Module 2), the hub-and-spoke coordinator and the
> structured handoff (Module 3), MCP-shaped tools (Module 4), permissions
> (Module 5), and reliability, confidence, and escalation (Module 6) into one
> agent that resolves what it can and escalates the rest. If you want to see the
> finish line first, jump to the **"Capstone Project"** section, then come back.

## First-principles companion

> 💡 **The durable idea behind this lesson.** "Support bot" is a product; the
> shape underneath it is a **finite-state machine**, one of the oldest ideas in
> computing.
>
> - **[Finite-state machine](https://en.wikipedia.org/wiki/Finite-state_machine)**
>   — a system that is always in exactly one of a fixed set of *states*, and moves
>   between them only on defined *transitions*. Your agent is in `bot_handling` or
>   `human_active`, never "sort of both," and it changes state only when a named
>   trigger fires. That is what makes its behaviour reviewable.
> - **[Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)**
>   (Anthropic, 2024). The "orchestrator" and "human-in-the-loop" patterns: an
>   agent handles the routine path and routes the ambiguous or high-stakes path to
>   a person. Progressive escalation is that pattern made explicit.

## A few plain-language basics first

This lesson pulls terms from the whole course. In plain words:

- **Agent:** an AI that takes a series of actions on its own toward a goal, rather than answering in one shot.
- **Agentic loop / tool loop:** the repeating cycle — the model asks to run a tool, you run it, you feed the result back, repeat — driven off `stop_reason` (`tool_use` means it wants a tool; `end_turn` means it is done).
- **Tool / tool call / tool result:** a function the model can choose to run; the choice is a *tool call*, and what comes back is the *tool result*.
- **Structured output:** making the model return machine-readable data (usually JSON) by giving it a tool with a typed input schema.
- **Anthropic SDK vs Claude Agent SDK:** the *Anthropic SDK* calls the model API directly; the *Claude Agent SDK* is the higher-level library for building agents (decorator tools, sessions, the loop handled for you).
- **State machine:** a system that is always in exactly one named *state* and moves to another only on a defined *trigger*. Here: `bot_handling → escalation_triggered → human_queue → human_active → resolved`.
- **Escalation:** handing a request off to a human because the agent should not, or cannot, resolve it.
- **Handoff package:** the structured bundle the human receives when a ticket escalates — who the customer is, what they want, what has been tried, and why it escalated.
- **Session context:** the small piece of state the agent carries across turns — the turn count, the current state, the escalation reason.

You do not need to memorise these. Each is re-explained the first time it matters.

## Why this lesson matters

Every lesson so far taught one moving part on a small toy. This is where the parts become a machine. As Andrew opens the lab: "we are going to be building a support bot because we want to take a look at how to handle escalation, as that is something that the exam wants us to know." The scenario is deliberately real — "Exam Pro Training Inc," a tech-education platform whose support today is, as Andrew jokes, "100% humans." The exercise is to build the agent that could take the first pass: resolve refunds, course swaps, and confirmation-email requests on its own, and escalate anything legal, ambiguous, or angry to a person — *cleanly*, with everything the human needs to pick up where the bot left off. If you can build this, you can build the real thing.

There is also a design ethic here worth naming. A support agent that traps frustrated customers in a loop is a bad agent. Andrew is blunt about it: "if you can keep them in that system, it's going to save humans time. I'm not saying it's good — I obviously don't like that — but I'm just saying, if we're engineering based on what they are saying here." Progressive escalation is the humane version: try your best, but let people reach a human the moment they need one.

## Learning objectives

By the end of this lesson you will be able to:

1. Model a support agent as a **state machine** and list its states and transitions.
2. Distinguish the two escalation modes — **escalate immediately** vs **offer to resolve first** — and code the difference.
3. Write **explicit, few-shot escalation criteria** instead of relying on the model's mood-reading.
4. Produce a **structured handoff package** so a human can take over without re-interrogating the customer.
5. Explain **why sentiment and self-reported confidence are unreliable escalation triggers**, and what to use instead.
6. Assemble the full **Atlas Support** agent, tracing each piece back to the lesson that built it.

## Prerequisites

- **Module 1 · Lessons 2–4 (the agentic loop, tools, and `stop_reason`):** the engine underneath everything here.
- **Module 2 · Lesson 6 (structured output):** the handoff package is structured output.
- **Module 3 · Lesson 8 (hub-and-spoke coordinator)** and **Lesson 14 (the structured handoff / gates):** escalation is a gated handoff.
- **Module 4 (MCP tools):** the support actions (`issue_refund`, `swap_course`, …) are the tools an MCP server would expose.
- **Module 5 (permissions and sandboxing):** issuing a refund is a destructive action — it belongs behind a gate.
- **Module 6 (reliability, confidence, escalation):** the judgment about *when* to escalate.
- Python, an Anthropic API key, and the `.env` / `dotenv` setup from Module 0.

---

## Part 1: A support agent is a state machine, not a chatbot

Andrew's first cut of the agent was just a polite chatbot with tools. It worked for a clean refund — it asked for the email, the order number, whether the course had been used, then processed it. Then he typed one sentence that broke it: *"Can I talk to a human?"* The agent replied, "Unfortunately, I don't have a direct transfer function available in my current system."

That is the whole problem in one exchange. A support agent needs somewhere to *go* when it hits its own limits. And you do not want it flipping to a human on any stray complaint. As Andrew puts it: "with these systems you generally want them to follow some kind of structure before there's an escalation." The structure is a **state machine** — the agent is always in exactly one named state, and moves between states only when a defined trigger fires.

Andrew reasoned his way straight to it: "is there a state machine, a simple state machine? What we could do is tell the prompt what the state machine is and then have it update it. That'd probably be the easiest way to do it." Here is the machine his build settled on:

```text
        ┌──────────────┐
        │ bot_handling │◄── start here. Resolve what you're allowed to.
        └──────┬───────┘
               │  a trigger fires (see Part 2)
               ▼
     ┌─────────────────────┐
     │ escalation_triggered│  call escalate_to_human(handoff_package)
     └──────────┬──────────┘
                ▼
          ┌───────────┐
          │ human_queue│  ticket waiting for a person
          └─────┬──────┘
                ▼
         ┌────────────┐
         │ human_active│  a human has taken over
         └─────┬───────┘
               ▼
          ┌──────────┐
          │ resolved │
          └──────────┘
```

You do not build a heavyweight state engine for this. Two cheap pieces carry it:

- **The prompt describes the machine** — the states, and the exact conditions that move the agent out of `bot_handling`.
- **A small session context tracks where you are** — Andrew's carried "how many turns, the reason, the messaging, and its current state." That is it.

> 🔑 **The agent is always in exactly one state, and only a named trigger moves it.
> That is what turns "a bot that sometimes gets a human" into a system you can
> review, log, and trust.**

## Part 2: Two escalation modes, and the triggers that fire them

Not every escalation is the same, and the exam guide (which Andrew reads on screen) draws the line sharply. There are **two modes**, and confusing them is the classic mistake.

| Mode | When | What the agent does |
|---|---|---|
| **Escalate immediately** | The customer *explicitly* asks for a human; or the request is legal/fraud/dispute; or policy is silent/ambiguous | Stop trying. Call `escalate_to_human` right away. Do not "first investigate." |
| **Offer to resolve first** | The customer is frustrated but has *not* asked for a person, and the issue is inside the agent's capabilities | Acknowledge the frustration, offer a fix, and only escalate if the fix fails |

The triggers Andrew wrote into the prompt were: the customer explicitly asked to speak to a human; the issue involves a legal threat, fraud claim, or dispute; the customer expresses extreme frustration; the agent cannot resolve after two to three attempts; or a request outright fails. Certain categories — GDPR and other legal requests — **auto-escalate** regardless.

There is a genuine judgment call buried here, and Andrew wrestles with it live. He briefly removed the "honor explicit human requests immediately" rule because he wanted the bot to try its best first — "if you can try to not bother the humans unless really absolutely needing to." But the exam is firm the other way: honor an explicit request for a human *immediately, without first attempting investigation*. Andrew concedes the point, with a dig: "obviously there are some systems that are evil that want to push this off." The lesson: **respecting an explicit human request is a hard rule, not a suggestion.** Trap-the-customer is an anti-pattern even when it "saves time."

One more rule from the exam that Andrew calls "actually smart": when a tool returns **multiple matching records**, do not guess. "If a tool returns multiple matching records, do not guess or pick — ask the customer for additional information." (Example: "I found two orders on your account — could you tell me which one?") Guessing on a refund is how you refund the wrong purchase.

> ✅ **What to do about it:** write the triggers as an explicit list in the prompt,
> with **few-shot examples** for the fuzzy cases (a frustrated-but-resolvable
> customer, an explicit human request, a policy gap like a competitor price-match).
> The exam's exact phrasing is "adding explicit escalation criteria with few-shot
> examples" — examples beat adjectives.

## Part 3: The structured handoff — escalation is only as good as what you hand over

An escalation that dumps a raw chat log on a human is barely better than no escalation. The payoff of Lesson 14's **structured handoff** shows up here: when the agent escalates, it does not just flip a flag — it builds a **handoff package**, a structured bundle the human can act on without re-interrogating the customer.

When Andrew provoked an escalation (a rude customer demanding an immediate refund), the agent produced exactly this: a summary reading, in effect, *"customer extremely frustrated, demanding immediate refund for the CLF-C02 course; customer has provided email; …"* That is the shape you want — reason, customer identifiers, request, and what has been tried, all in one place.

```text
HANDOFF PACKAGE  (structured output — Module 2)
{
  "escalation_reason": "explicit_human_request | legal | policy_gap |
                        failed_attempts | extreme_frustration",
  "customer":   { "email": "andrew@example.com", "account_id": "…" },
  "request":    "Refund for CLF-C02",
  "attempted":  ["verified email", "asked for order number (not provided)"],
  "state":      "escalation_triggered",
  "turn_count": 4,
  "transcript_summary": "Customer frustrated; wants refund; only email given."
}
```

Two things make this a *structured* handoff and not a paragraph:

1. **It is a tool with a schema** (Module 2). The `escalate_to_human` tool takes typed fields, so the model must fill in every required one. The `escalation_reason` is an **enum** — a fixed set of allowed values — which is what makes escalations countable and auditable later.
2. **It is built from the session context you were already tracking** (Part 1). The turn count, the state, the reason — you kept those anyway; the handoff just serialises them.

> 🔑 **Escalation = the gate; the handoff package = the thing that passes through
> it. A human should be able to resume from the package alone, without re-asking
> the customer a single thing.**

### Log everything

The third job — beside resolve and escalate — is **log**. Every resolved refund, every state transition, every handoff is a record. This is the choke-point observability idea from the coordinator lesson (Module 3): because escalation is a single, named event with a structured payload, you can log it once, count reasons, and later ask "what fraction of tickets did the bot resolve, and why did the rest escalate?"

## Part 4: Why sentiment and self-reported confidence are the weak spot

This is the subtlest point in the whole course, and — true to the course's ethic — Andrew is honestly unsure about it on camera, which makes it a better lesson than a clean answer would. The exam guide states: **sentiment-based escalation and self-reported confidence scores are unreliable proxies for actual complexity.** Andrew pushes back in real time: "sentiment-based escalation means, like, are they mad? Why wouldn't that work? It obviously worked right there." And at the end he admits the gap: "the only thing that doesn't really help is that sentiment information."

Here is the reconciliation, taught as judgment, not gospel:

- **Sentiment is not complexity.** A customer can be furious about a one-click refund (easy) and perfectly calm about a GDPR data-takedown across three systems (hard). Routing on *mood* escalates the wrong tickets — it sends easy-but-angry to humans and keeps hard-but-polite in the bot. Mood is real signal for *tone*, but a poor proxy for *"is this beyond the agent?"*
- **Self-reported confidence is self-graded.** When a model says "I'm 90% confident," that number is produced by the same model that might be wrong; a confidently wrong answer reports high confidence. You cannot trust a system's own grade of itself as your escalation gate.
- **So what do you use?** The **explicit, checkable criteria** from Part 2: an explicit human request, a legal/fraud flag, a policy gap, a *tool failure*, or *N failed attempts*. These are observable facts, not vibes or self-assessment. Sentiment and confidence can be *inputs* to a human's later review, but they should not be the trigger.

This is also a live instance of the course's running theme: **the docs, the model, and even the exam guide can be unclear — you get to the truth by building it and watching.** Andrew's honest "it's not exactly clear, but I think…" is the correct posture. Don't memorise the exam's sentence; understand *why* an observable criterion beats a felt one.

> 💡 **Nuance:** "unreliable proxy" does not mean "useless signal." Extreme,
> sustained frustration is a legitimate *explicit* trigger (Part 2 lists it). The
> warning is against making a sentiment score or a self-confidence number your
> *primary* routing logic. Gate on facts; annotate with feelings.

## Part 5: Assembling Atlas Support — the whole course in one file

Step back and look at what the finished agent is made of. Every module shows up:

```text
ATLAS SUPPORT  =  one agent, built from the whole course

  Module 1  tool loop ............ the engine: call model, run tool,
                                    feed result back, drive off stop_reason
  Module 2  structured output .... the escalate_to_human schema +
                                    the handoff package (typed, enum reason)
  Module 3  coordinator + handoff. the state machine + the gated,
                                    structured handoff to a human (Lesson 14)
  Module 4  MCP tools ............ issue_refund, swap_course, resend_email,
                                    create_bug_ticket, process_gdpr … as an
                                    MCP server would expose them
  Module 5  permissions .......... issue_refund is destructive → gate it;
                                    ask/deny before money moves
  Module 6  reliability .......... explicit escalation criteria, confidence
                                    done right, retries, verify-don't-trust
```

Andrew's build choices echo the course, too. He deliberately uses the **Claude Agent SDK, not the low-level Anthropic SDK** ("implement an agent using Anthropic's Agent SDK, not the low-level SDK"). He mocks the support actions as tool calls, noting they "probably would live in an MCP server that goes to Exam Pro endpoints" — the Module 4 shape. And he runs on **Sonnet to keep costs down**, hitting exactly the trade-off Module 6 warned about: with Sonnet the loop first threw an "unexpected tool handler" because the model invented a tool. "We're using Sonnet, right? We're trying to keep our costs down. If we used Opus, it probably would work" — a real reliability-vs-cost decision, not a hypothetical.

And the course's loudest lesson lands one more time. Andrew tells the model to add human escalation, it says it will, and he checks: "did it add human intervention? I don't think it did." It hadn't. **Just because it said it did, it does not mean it did.** He also caught the classic setup bug — the agent kept dropping the `.env` load because the hello-world example he copied from never had it: "I've been complaining this entire time… it's just not in the example we're pulling from. I'm the problem, folks." Verify the boring things too.

> 🔑 **The finale is not a new idea — it is every earlier idea, wired together.
> If any piece feels shaky, that is your signal for which earlier lesson to
> revisit before you build.**

---

## Key takeaways

1. **Model the agent as a state machine.** One current state at a time; transitions only on named triggers. Describe it in the prompt, track it in a tiny session context.
2. **Two escalation modes.** Escalate *immediately* on an explicit human request, legal/fraud, or a policy gap; *offer to resolve first* when the customer is merely frustrated and the issue is in scope.
3. **Explicit criteria with few-shot examples beat adjectives.** List the triggers; show examples for the fuzzy cases.
4. **The handoff package is structured output.** A typed tool with an enum `reason`, built from the context you were already tracking — so a human can resume without re-asking anything.
5. **Log every resolution and every escalation.** Escalation is a single named event with a structured payload; that is your observability.
6. **Sentiment and self-reported confidence are unreliable proxies for complexity.** Gate on observable facts (explicit request, legal flag, policy gap, failed attempts); use mood and confidence only as annotations.
7. **Verify the boring things.** The `.env`, whether the tool was actually added, whether the model really escalated. "Just because it said it did, it does not mean it did."

## Common pitfalls

- ❌ **Trapping the customer.** Ignoring or deferring an explicit "I want a human." The exam and basic decency both say: honor it immediately, no investigation first.
- ❌ **Routing on mood.** Escalating because the model senses anger. An easy request from an angry customer is still easy; a hard request from a polite one is still hard.
- ❌ **Trusting the model's own confidence score as the gate.** It is self-graded; a confidently wrong answer reports high confidence.
- ❌ **Guessing when a tool returns multiple matches.** Refunding the wrong order is worse than asking one more question. "Do not guess or pick — ask the customer."
- ❌ **A handoff that is just the raw transcript.** Without a structured summary, reason, and identifiers, the human re-interrogates the customer and the escalation saved nobody time.
- ❌ **Forgetting the setup plumbing.** The dropped `.env`, the uncapped loop, the invented tool on a cheaper model. Verify each before you trust the run.
- ❌ **Leaving `issue_refund` ungated.** A destructive, money-moving action with no permission check is a Module 5 failure hiding in a Module 7 build.

---

## 🛠️ Capstone Project: Atlas Support — resolve, escalate, log

> This is the **course capstone** — the whole of Atlas Support, assembled. It is
> intentionally small enough to finish, and intentionally wired from every module
> so that finishing it proves you learned the course, not just this lesson.

### What you will build

A single support agent for "Exam Pro Training Inc." that: (1) **resolves** the common requests it is allowed to, using mocked tools; (2) **escalates** everything legal, ambiguous, or explicitly human-requested to a person, via a structured handoff package; and (3) **logs** every resolution and escalation. Its pieces map straight to the course:

- **A tool loop** driven off `stop_reason` — the engine. *(Module 1)*
- **Mocked support tools** — `issue_refund`, `swap_course`, `resend_confirmation_email`, `create_bug_ticket`, `create_content_issue_ticket`, `route_business_development`, `process_gdpr_request` — MCP-shaped. *(Module 4)*
- **A state machine** in the prompt + a session context tracking state, turn count, and reason. *(this lesson, Module 3)*
- **An `escalate_to_human` tool** whose input *is* the structured handoff package. *(Module 2 + Lesson 14)*
- **A permission gate** on `issue_refund` and other destructive actions. *(Module 5)*
- **Explicit escalation criteria with few-shot examples**, and confidence handled honestly. *(Module 6)*

### Why this is the perfect practice

Each milestone below is one earlier lesson, cashed in.

| Capstone milestone | The lesson it uses |
|---|---|
| M1 — Tool loop that runs one support tool | Module 1 · Lessons 2–4 (agentic loop, tools, `stop_reason`) |
| M2 — The seven mocked support tools | Module 4 (MCP tools; "as an MCP server would expose them") |
| M3 — Interactive loop you can talk to | Module 1 · Lesson 4 (loop done right, capped) |
| M4 — State machine + session context | Module 3 · Lesson 8 (coordinator state) + this lesson |
| M5 — `escalate_to_human` structured handoff | Module 2 · Lesson 6 + Module 3 · Lesson 14 (structured handoff) |
| M6 — Explicit triggers + few-shot examples | Module 6 (reliability, escalation, confidence) |
| M7 — Gate the refund; log everything | Module 5 (permissions) + Module 3 (choke-point logging) |

### Milestones (build them in order, each one works on its own)

1. **One tool, one loop.** Build a minimal agent (Claude Agent SDK, with a real `.env` load — check it) that has exactly one tool, `resend_confirmation_email(email)`, mocked to return success. Run the tool loop until `end_turn`. Ask it to resend a confirmation email and watch the tool fire. This alone is a working agent.
2. **The full toolbelt.** Add the rest of the mocked tools: `issue_refund`, `swap_course`, `create_bug_ticket`, `create_content_issue_ticket`, `route_business_development`, `process_gdpr_request`. Each just returns a canned success/record. Confirm the agent picks the right tool per request (refund vs swap vs bug). If it invents a tool that isn't there, that's your Sonnet-vs-Opus reliability moment — tighten the prompt or bump the model.
3. **Make it interactive.** Turn the hardcoded single message into a real read-eval loop you can talk to turn by turn (Andrew: "make the agent a real loop I can talk to when I run it"). Have a genuine back-and-forth: refund request → agent asks for email and order number → you answer → refund processes.
4. **Add the state machine.** Put the five states (`bot_handling → escalation_triggered → human_queue → human_active → resolved`) into the prompt, and add a session context that tracks `current_state`, `turn_count`, and `escalation_reason`. The agent starts in `bot_handling`. Nothing escalates yet — just confirm the state is tracked and updated.
5. **Add escalation with a structured handoff.** Add the `escalate_to_human` tool. Its input schema *is* the handoff package: `escalation_reason` (enum), `customer`, `request`, `attempted`, `state`, `turn_count`, `transcript_summary`. Write the explicit triggers into the prompt (explicit human request; legal/fraud/dispute; extreme frustration; 2–3 failed attempts; GDPR auto-escalate). Test the two modes: a calm "can I talk to a human?" escalates immediately; a frustrated-but-resolvable refund gets an offer to fix first. Verify the tool actually got added — don't take the model's word for it.
6. **Add few-shot examples + the multi-match rule.** From the exam's to-do list, add few-shot examples for the fuzzy cases (explicit human request with no frustration → escalate at once; competitor price-match / merge-two-accounts → policy gap → escalate rather than improvise; frustration with an in-scope issue → offer resolution). Add the rule: if a tool returns multiple matching records, ask the customer to disambiguate instead of guessing.
7. **Gate the destructive tools and log everything.** Put a permission check in front of `issue_refund` (and any tool that moves money or data) — ask/confirm before it runs (Module 5). Log every resolved request and every escalation, writing the handoff package to your log on escalation. You now have resolve + escalate + log.
8. **Stretch goals.** (a) **Add sentiment** as an *annotation* on the handoff package — and prove to yourself it is a poor *trigger* by finding one angry-but-easy and one calm-but-hard ticket. (b) **Batch the ticket queue**: feed a list of tickets through the agent in a batch run (Module 6's batch lesson), collecting resolutions and escalations. (c) **Add confidence scoring** done honestly — have the agent emit a confidence, but gate escalation on the explicit criteria, using confidence only to sort the human's queue.

### How you will know you are done

- ✅ A clean refund runs end-to-end: the agent gathers email + order number, and calls `issue_refund` — **behind a permission gate** — without you touching the code.
- ✅ Typing "I want to speak to a human" escalates **immediately**, with no investigation first.
- ✅ A frustrated-but-in-scope request gets an **offer to resolve** before any escalation.
- ✅ A GDPR / legal request **auto-escalates** regardless of tone.
- ✅ On escalation, a **structured handoff package** is produced with a valid enum `reason` and enough context that a human could resume **without re-asking the customer anything**.
- ✅ When a tool returns multiple matches, the agent **asks to disambiguate** instead of guessing.
- ✅ Your log contains one record per resolution and one handoff package per escalation.
- ✅ You can point at each part of the agent and name the module it came from.
- ✅ You **read the run trace** and saw each of the above happen — you did not trust the model's summary of itself.

> 💡 **Keep yourself honest:** the model will tell you it added the escalation
> tool, loaded the `.env`, and gated the refund. None of that is evidence. Your
> done-criteria are things you *watched the agent do* in the trace — the course's
> first rule, one last time: "just because it said it did, it does not mean it did."

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice
> on one idea. Optional and independent; the Capstone already touches all of them,
> so feel free to skip straight to it.

### Exercise 1: Draw the machine (foundational)
On paper, draw the five states and label every transition with the trigger that causes it. Then mark which transitions are "escalate immediately" and which are "offer first." Any transition you can't label with a *checkable* trigger is a design bug.

### Exercise 2: Classify ten tickets (intermediate)
Write ten sample tickets — some easy-and-angry, some hard-and-calm, some explicit human requests, some legal. For each, decide: resolve, offer-then-maybe-escalate, or escalate-now. Notice how *mood* and *difficulty* pull in different directions. That contrast is Part 4 in your own words.

### Exercise 3: Write the enum, break the handoff (advanced)
Define the `escalation_reason` enum, then deliberately hand a human a *raw transcript* instead of the structured package. Time (or imagine) how long it takes them to reconstruct the customer's identity and request. Now swap in the structured package. The gap you feel is why Lesson 14 exists.

---

## Cheat sheet

```text
ATLAS SUPPORT — progressive-escalation support agent (one-page recap)

THE SHAPE: a STATE MACHINE (one state at a time; move only on a trigger)
  bot_handling -> escalation_triggered -> human_queue -> human_active -> resolved
  Prompt describes the machine. Session context tracks: state, turn_count, reason.

THREE JOBS
  RESOLVE   run a support tool for a common request
  ESCALATE  hand off to a human on a defined trigger
  LOG       one record per resolution; the handoff package per escalation

TWO ESCALATION MODES
  ESCALATE NOW      explicit human request | legal/fraud/dispute | policy gap
                    (do NOT investigate first — honor it immediately)
  OFFER FIRST       frustrated + in-scope -> acknowledge, offer a fix,
                    escalate only if the fix fails
  AUTO-ESCALATE     GDPR / legal categories, regardless of tone

TRIGGERS (explicit, checkable — use few-shot examples for fuzzy cases)
  asked for a human · legal/fraud/dispute · extreme frustration ·
  2–3 failed attempts · a request/tool failed
  MULTI-MATCH: never guess — ask the customer to disambiguate

HANDOFF PACKAGE (structured output, typed, enum reason)
  { escalation_reason, customer, request, attempted, state,
    turn_count, transcript_summary }
  Goal: a human resumes from the package alone, re-asking nothing.

WEAK PROXIES (do NOT gate on these)
  SENTIMENT           mood != complexity (angry+easy, calm+hard)
  SELF-CONFIDENCE     self-graded; confidently-wrong reports high
  -> gate on FACTS; use mood/confidence only to annotate & sort

BUILT FROM THE WHOLE COURSE
  M1 tool loop · M2 structured output · M3 coordinator + handoff (L14) ·
  M4 MCP tools · M5 gate the refund · M6 escalation/confidence/batch

THE RULE (one last time)
  "Just because it said it did, it does not mean it did."
  Check the .env. Check the tool was added. Read the trace.
```

## How this connects to the rest of the course

- **Earlier, Module 1 · Lessons 2–4:** the tool loop and `stop_reason` are the engine Atlas Support runs on — you drive escalation off tool calls, never off parsing text.
- **Earlier, Module 2 · Lesson 6:** structured output is exactly what the `escalate_to_human` handoff package is — a typed tool with an enum reason.
- **Earlier, Module 3 · Lesson 8 and Lesson 14:** the coordinator gave you state and a choke point; Lesson 14's structured handoff is the gate the escalation passes through.
- **Earlier, Module 4:** the seven support actions are MCP-shaped tools — "an MCP server that goes to Exam Pro endpoints."
- **Earlier, Module 5:** issuing a refund is destructive, so it sits behind a permission gate. This capstone is where that discipline stops being theoretical.
- **Earlier, Module 6:** reliability, confidence, and escalation — including the previous lesson, **"Batch processing for scale and cost,"** which the stretch goal cashes in when you run the ticket queue as a batch.
- **Next:** nothing — this is the finish line. You have taken Atlas Support from a single API call all the way to an agent that resolves what it can and escalates the rest with a clean handoff. That is the whole course, standing in one file.

---

*Source: reconstructed from the CCA-F course by Andrew Brown (ExamPro). Code
snippets and diagrams are illustrative reconstructions of the patterns described
in the course. Adapt them to the current SDK.*
