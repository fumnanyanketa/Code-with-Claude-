# Module 3 · Lesson 10: Refinement loops and observability

> **Course:** Claude Certified Architect: Foundations, a self-paced course
> **Module 3:** Orchestration: multi-agent architectures — one coordinator, many spokes, working as a system
> **Speaker:** Andrew Brown, ExamPro
> **Source:** Reconstructed from the CCA-F course by Andrew Brown (ExamPro) · [full transcript](../../transcripts/cca-f-full-course.txt)
> **Estimated time:** 45 to 60 minutes (read plus lab)

---

## In one sentence

You will teach a coordinator to grade its own work and try again — add an
evaluation step that measures how well the sub-agents covered the task,
re-delegates only the gaps, and stops after a hard cap — and then wire in the
logging and message capture you need to actually *see* what every agent did.

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone
> Project** where you add a refinement loop and JSON logging to **Atlas
> Support's** coordinator, so you can watch it detect a coverage gap, send one
> more round of work to close it, and stop cleanly. Everything before the
> Capstone teaches the two skills you will use there: the evaluate-then-redelegate
> loop, and coordinator observability. If you want to see the finish line first,
> jump to the **"Capstone Project"** section, then come back.

## A few plain-language basics first

This lesson uses some everyday terms. Here they are in plain words:

- **Agent:** an AI that takes a series of actions on its own toward a goal,
  rather than answering in one shot.
- **Coordinator / hub-and-spoke:** an architecture where one *coordinator* agent
  owns routing, context, and aggregation, and delegates to *sub-agents*
  ("spokes") that it calls as tools.
- **Sub-agent (spoke):** an agent spawned by the coordinator, usually with its
  own isolated context, that does one narrow job and reports back.
- **Tool / tool call / tool result:** a function the model can choose to run;
  when it decides to use one that is a *tool call*, and what comes back is the
  *tool result*.
- **One-shot:** the agent runs once, produces an answer, and stops — no second
  look, no retry.
- **Refinement loop:** the new idea in this lesson — after the first answer, the
  system grades itself, and if it is not good enough, it does another round to
  improve, up to a fixed limit.
- **Coverage:** how much of the task actually got addressed. If you asked five
  questions and only three were answered, coverage is partial.
- **Observability:** your ability to look at a running system and understand what
  it did and why — which agent got asked what, what it replied, what failed.
- **Structured logging:** writing out events as consistent records (each with a
  timestamp, a level like INFO or ERROR, and the data) instead of scattered
  `print` statements, so you can search and compare them later.

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

Up to now, your multi-agent system has been **one-shot**. As Andrew frames it:
"everything's been one shot. It goes through it, it produces an evaluation, and
then it's over. But what if we could feed it back in the loop and refine it until
we are happy with it?" That is the whole idea — a system that notices its own
gaps and closes them. But there is a catch that runs through this entire lesson,
and Andrew says it out loud more than once: **doing it is not the same as it
being good.** "Just because we're doing it doesn't mean it's great." When he
actually ran his refinement loop, the coverage score went *down* over two
iterations. The only way to know whether any of this helps is to be able to
*see* what happened — which is exactly why refinement and observability belong in
the same lesson. You cannot improve a system you cannot watch.

## Learning objectives

By the end of this lesson you will be able to:

1. Explain why a one-shot coordinator leaves coverage gaps, and what a refinement
   loop adds.
2. Add an **evaluation step** (a `evaluate_coverage` tool) that scores how well
   the sub-agents covered the task and names the gaps.
3. Make the coordinator **re-delegate only the gaps** and stop after a hard
   iteration cap, so the loop can never run forever.
4. Audit a coordinator for **observability** across four dimensions: message
   capture, error handling, context control, and spoke isolation.
5. Instrument a coordinator with **structured JSON logging** so every delegation,
   response, and decision is recorded and inspectable.

## Prerequisites

- **Module 3 · Lesson 9 ("Task decomposition done right")** — you have a
  coordinator that splits a job into partitions and delegates each to a spoke.
  This lesson builds directly on that code.
- **Module 3's loop-antipatterns lesson** — you already know that any agent loop
  needs a hard stop. We reuse that rule here as the iteration cap.
- You can call Claude through the Anthropic SDK from Python and define a tool with
  a JSON input schema (Modules 1–2). We are still on the plain Anthropic SDK here,
  not the Agent SDK — as Andrew notes, "the agent SDK is awesome, but we will just
  continue on here."

---

## Part 1: The one-shot problem

Picture the system you built last lesson. A coordinator reads a candidate's
resume, splits the screening into partitions ("core stack proficiency," "REST API
capabilities," "senior-level experience"), sends one spoke per partition, collects
the answers, and issues a recommendation. Then it stops.

That is **one-shot**: one pass, one answer, done. It works, but it has no way to
notice when it did a mediocre job. In Andrew's run the spokes came back with
"partials" — a *maybe* recommendation with uneven coverage across the partitions.
Some angles were answered well; others were thin. A one-shot system ships that
mediocre result anyway, because it has no step that asks *"is this actually good
enough?"*

The fix is to add exactly that step, and then act on its answer:

```text
ONE-SHOT (before)
  decompose → delegate to spokes → collect → recommend → STOP

REFINEMENT LOOP (after)
  decompose → delegate to spokes → collect
      → EVALUATE coverage
          → good enough?  ── yes ──▶ submit final → STOP
          → gaps found?   ── no  ──▶ re-delegate only the gaps ──┐
                                          ▲                        │
                                          └──── (up to N times) ◀──┘
```

> 🔑 **A refinement loop turns "produce one answer and stop" into "grade the
> answer, fix the gaps, repeat until good enough or out of tries."**

## Part 2: The evaluation agent — score the coverage, name the gaps

The heart of the loop is a new step whose only job is to judge the work so far.
Andrew adds it as a tool the coordinator must call: `evaluate_coverage`. After all
the initial spokes have reported, the coordinator calls this tool with the
findings, and it returns a **coverage score** plus a list of what is still
missing.

Think of it as a second agent with a narrow brief: *do not do the screening —
just tell me how complete the screening is.* Its output drives the next decision.
In Andrew's run it came back with things like "coverage score, code quality
practices: no evidence" — i.e. it flagged that one dimension had no supporting
evidence yet. That "no evidence" note is the gap the next round will try to fill.

An illustrative shape for the tool:

```python
# Illustrative reconstruction — adapt to the current SDK.
evaluate_coverage = {
    "name": "evaluate_coverage",
    "description": (
        "Judge whether the screening findings are sufficient to make a "
        "confident recommendation. Call this AFTER all partition agents have "
        "reported. Do not perform screening yourself."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "coverage_score": {"type": "number"},   # 0.0 - 1.0
            "sufficient": {"type": "boolean"},       # good enough to stop?
            "gaps": {                                # what still needs work
                "type": "array",
                "items": {"type": "string"},
            },
        },
        "required": ["coverage_score", "sufficient", "gaps"],
    },
}
```

Notice this is **structured output** — you make the model return machine-readable
data (here JSON with a score, a boolean, and a list) by giving it a tool with a
typed schema, instead of hoping to parse a paragraph. The coordinator can then
branch on `sufficient` and read `gaps` directly, with no guessing.

> 💡 **The evaluator is a judge, not a worker.** Its prompt must forbid it from
> doing the screening itself. Its entire value is an *honest, separate* read on
> how complete the real work is.

## Part 3: Re-delegate the gaps — and cap the loop

Once you have a coverage verdict, the coordinator prompt encodes the loop. Andrew
tells it, in plain language, three things:

1. **The phases.** "Phase one: invoke exactly one screening agent per partition.
   Phase two: after all initial partition agents have reported, call
   `evaluate_coverage`."
2. **The refinement rule.** "If `evaluate_coverage` returns sufficient = false,
   invoke screening agents to fill *only* the identified gaps" — not the whole
   thing again, just the missing pieces.
3. **The exit gate.** "Do not call `submit_final` before evaluation." The final
   recommendation is only allowed *after* the evaluator has spoken, so the system
   can never ship an ungraded answer.

And the load-bearing safety rule: **a maximum number of iterations.** Andrew caps
it at four: "we can have up to maximum four refinement iterations." This is the
same discipline you met in the loop-antipatterns lesson — every agent loop needs
a hard stop so a self-improving system can never become a self-*looping* one. The
evaluator might keep finding gaps; the cap guarantees the loop ends regardless.

```text
COORDINATOR PROMPT — refinement contract
  MAX_ITERATIONS = 4
  Phase 1  invoke exactly one screening agent per partition
  Phase 2  after all report → call evaluate_coverage (plain findings)
  Phase 3  if not sufficient AND iterations < MAX_ITERATIONS:
               re-delegate ONLY the named gaps → back to Phase 2
           else:
               call submit_final   (never allowed before an evaluation)
```

> ❌ **The trap: a loop with no cap.** "Refine until happy" with no ceiling can
> run forever, burn tokens, and stall. The cap is not optional polish — it is the
> thing that makes the loop safe to ship.

### An honest note: refining is not automatically improving

When Andrew ran his loop, something instructive happened: "the coverage score is
going down now. Interesting... it did two iterations and their score went down."
More refinement made the *measured* result worse, not better. His verdict is the
theme of this whole course: "Is that good? I don't know. It takes a lot of work
to evaluate this stuff... There's no magic here folks. We can code these out very
quickly, but to make sure they actually work good is a different story."

Take this seriously. The loop is a *mechanism*, not a guarantee. Whether it helps
depends on your evaluator's quality, your data, and your prompts — and the only
way to find out is to run it on real examples and compare. As Andrew muses, the
honest test would be "let's say 100 applicants and you ran it through, to see if
it just skewed it to one side or not." Which is exactly why you need to be able to
*see* the runs — Part 4.

## Part 4: Observability — you must be able to see what happened

Andrew's next move is to ask a blunt question of his own coordinator: **is it
actually behaving like a coordinator?** He puts Claude in **plan mode** (a
read-only mode that produces a plan without changing code) and asks it to audit
four things:

- **Message capture** — are we storing "all messages that are being sent to our
  spokes" and everything they send back?
- **Context control** — is the coordinator "controlling context and what is
  passed to my spokes"?
- **Spoke isolation** — do "only those sub-agents talk to the coordinator," and
  not to each other?
- **Error handling / tracing** — can we "capture any errors"?

The audit was unflattering, and worth reading because your first coordinator will
have the same holes:

| Dimension | What the audit found | Why it hurts |
|---|---|---|
| Observability | "Only print statements." No API-level tracing — no token counts, no latency, no request IDs. No persistent audit trail (ephemeral stdout). | You cannot debug, cost, or replay a run. |
| Message capture | Questions *to* spokes get printed, but "spoke responses are never stored — they go straight into the tool results and are lost." No log of the coordinator's own reasoning between tool calls. | You can't see *why* it decided anything. |
| Context control | "Every spoke receives the full job posting" regardless of its partition. Scope is "only advisory... not enforced at the spoke level." | Spokes can wander outside their assigned partition. |
| Spoke isolation | One-directional (spokes are stateless functions, no cross-spoke chatter) — good — but "spokes have no awareness of their assigned partition; they can't reject out-of-scope questions." | Isolation is real but unenforced. |

The summary: "Can't debug or audit the run. Silent crashes on failures. Can't
replay or inspect what's wrong. Coordinator doesn't know if all dimensions are
covered mid-run." A coordinator that cannot be observed is not really acting as a
coordinator — it is a black box that happens to call other agents.

> 🔑 **A coordinator's job is not only to route and aggregate — it is to be the
> observable layer.** If you cannot see what it delegated, what came back, and
> what it decided, you cannot trust or improve the system.

### The fixes: structured logging and message capture

The recommended fixes are small and concrete, and they are what you will build in
the Capstone:

- **Structured logging** — log events "with timestamps and levels" (INFO,
  ERROR), scoped to each partition and agent name, instead of bare `print`s. Now
  you can search, filter, and compare runs.
- **Error handling** — "wrap the JSON loads" and other fragile spots so a bad
  response is a logged error, not a silent crash.
- **Persist spoke inputs and outputs** — store what each spoke was asked *and*
  what it answered, so responses are no longer "lost after the coordinator."
- **Add the coverage gate** — the `evaluate_coverage` tool and the "force the
  coordinator to call `submit_final`" rule from Parts 2–3 are themselves
  observability: they make the *decision to stop* explicit and inspectable.

> ✅ **What to do about it:** replace every `print` with a structured log record
> (timestamp, level, agent, event, payload), and write both the question sent and
> the response received for every spoke call. That single change is the
> difference between guessing and knowing.

### A practical trick and an honest limit

Two asides from Andrew worth keeping. First, when a change has many steps, he asks
Claude to "create this plan in a README with a task checklist and check off the
tasks as you complete them" — a lightweight way to keep a long edit on track.
Second, he is candid that his instrumented file became "a mess... not how you
should have your codebase." Logging bolted onto one big file works for learning;
the *next* lesson refactors it into something clean. And he notes what he skipped:
real tests that "pollute the context between agents" to prove a spoke rejects
out-of-scope questions. Observability is the foundation those tests would stand
on — you have to capture the messages before you can assert anything about them.

---

## Key takeaways

1. **One-shot ships mediocre.** A single pass has no step that asks "is this good
   enough?" A refinement loop adds one.
2. **The evaluator is a separate judge.** `evaluate_coverage` scores coverage and
   names gaps as structured output; it must not do the work itself.
3. **Re-delegate only the gaps.** Fill what's missing, not the whole task again.
4. **Always cap the loop.** Max iterations (Andrew uses 4) is the safety rule
   from the loop-antipatterns lesson — non-negotiable.
5. **Refining ≠ improving.** Andrew's score went *down*. The loop is a mechanism;
   only real evaluation tells you if it helps.
6. **A coordinator must be observable.** Capture messages, handle errors, control
   context, enforce isolation — and log it all with structure, or you are flying
   blind.

## Common pitfalls

- ❌ **A refinement loop with no iteration cap.** "Refine until happy" can loop
  forever. Set `MAX_ITERATIONS` and enforce it.
- ❌ **Re-running everything each round.** Re-delegate only the named gaps, or you
  waste tokens and may overwrite good findings.
- ❌ **Letting `submit_final` fire before evaluation.** The exit gate exists so
  you never ship an ungraded answer — enforce it in the prompt.
- ❌ **Logging with `print` and calling it observability.** Stdout is ephemeral
  and unsearchable. Use structured records with timestamps and levels.
- ❌ **Dropping spoke responses into tool results and moving on.** If you don't
  persist them, they're gone — and you can't debug or replay the run.
- ❌ **Assuming the loop made it better.** Measure. A lower coverage score after
  refinement is a real outcome you must be able to detect.

---

## 🛠️ Capstone Project: a self-refining, observable Atlas Support coordinator

> This is the main hands-on project for the lesson. You will feel the moment your
> coordinator catches its own gap, sends one more round to close it, stops at the
> cap — and, for the first time, lets you *read the whole story* in the logs.
> Keep it small on purpose.

Atlas Support is the one system this course builds across every lesson — a
multi-agent support system that grows from a single API call into a coordinator
that escalates to a human. Last lesson you gave its coordinator task
decomposition. This lesson you give it two things every serious coordinator needs:
the ability to grade and retry its own work, and the ability to be watched.

### What you will build

Take your Atlas Support coordinator from Lesson 9 (it decomposes an incoming
support ticket into partitions and delegates each to a spoke). Add:

- An **`evaluate_coverage` tool** the coordinator calls after the first round —
  returns `coverage_score`, `sufficient`, and a list of `gaps`.
- A **refinement loop** with `MAX_ITERATIONS = 4`: if not sufficient, re-delegate
  only the gaps, then re-evaluate; stop at the cap or when sufficient.
- An **exit gate**: `submit_final` may only be called after an evaluation.
- **Structured JSON logging**: every delegation, every spoke response, every
  evaluation, and the final decision written as JSON records with a timestamp,
  level, iteration number, and agent name.

### Why this is the perfect practice

| Lesson idea | Where you use it in Atlas Support |
|---|---|
| Evaluation step (Part 2) | The `evaluate_coverage` tool that scores the ticket's answer |
| Re-delegate only the gaps (Part 3) | Round 2 asks only about the `gaps` list |
| Hard iteration cap (Part 3) | `MAX_ITERATIONS = 4` guard around the loop |
| Exit gate (Part 3) | `submit_final` blocked until evaluation has run |
| Message capture (Part 4) | Log the question *and* response for every spoke |
| Structured logging (Part 4) | JSON records replacing every `print` |

### Milestones (build them in order, each one works on its own)

1. **JSON logging first.** Before touching the loop, replace your coordinator's
   `print`s with a tiny logger that emits one JSON object per event:
   `{"ts": ..., "level": "INFO", "iteration": 0, "agent": "coordinator",
   "event": "delegate", "payload": {...}}`. Run the existing one-shot flow and
   confirm you can read the full run from the log lines alone. *This milestone is
   valuable by itself — you now have observability even without the loop.*
2. **Capture spoke responses.** Log the response of every spoke, not just the
   question you sent it. Verify no spoke reply is lost after its tool result.
3. **Add the evaluator tool.** Define `evaluate_coverage` (score, `sufficient`,
   `gaps`) and have the coordinator call it once after the first round. Log its
   output. Don't loop yet — just see the verdict.
4. **Close one gap.** If `sufficient` is false, re-delegate *only* the `gaps` and
   re-evaluate. Log each round with its `iteration` number so you can watch the
   score change.
5. **Cap and gate.** Enforce `MAX_ITERATIONS = 4` and forbid `submit_final`
   before an evaluation has run. Confirm from the logs that the loop always ends —
   either "sufficient" or "hit cap."
6. **Read your own run.** Pipe the JSON logs to a file and answer, using only the
   log: how many iterations ran? Did the coverage score go up or down? Which gaps
   were re-delegated? If you can answer all three from the log, you have real
   observability.
7. **Stretch goals.** Add token counts and latency per spoke call to each log
   record. Add error handling that wraps `json.loads` so a malformed spoke reply
   becomes a logged ERROR, not a crash. Run the loop on 5–10 real tickets and
   compare final scores — did refinement help, hurt, or wash out?

### How you will know you are done

- ✅ Every delegation, spoke response, evaluation, and final decision appears as a
  structured JSON log record with a timestamp and iteration number.
- ✅ The coordinator calls `evaluate_coverage` before it ever calls `submit_final`.
- ✅ When coverage is insufficient, only the named gaps are re-delegated.
- ✅ The loop always terminates — you can point to either a "sufficient" record or
  a "hit MAX_ITERATIONS" record.
- ✅ From the log alone, you can state how many iterations ran and whether the
  score rose or fell.

> 💡 **Keep yourself honest:** run it on more than one ticket and actually read
> the scores across iterations. As Andrew's own run showed, the score can go
> *down* — the whole point of the logging is that you would *see* that instead of
> assuming the loop helped.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice on
> one idea. Optional and independent; the Capstone already touches all of them, so
> feel free to skip straight to it.

### Exercise 1: The one-line logger (foundational)
Write a single helper `log(level, event, **fields)` that prints one JSON object
per call with a timestamp. Replace three `print`s in any script with it and
confirm the output is valid JSON, one object per line.

### Exercise 2: The evaluator's schema (intermediate)
Write the `input_schema` for `evaluate_coverage` on your own: `coverage_score`
(0–1 number), `sufficient` (boolean), `gaps` (array of strings), all required.
Then write a coordinator prompt that forbids the evaluator from doing the
screening itself.

### Exercise 3: Prove the cap holds (advanced)
Force a "never sufficient" evaluator (always returns `sufficient: false`) and run
the loop. Confirm from the logs that it stops at exactly `MAX_ITERATIONS` and then
calls `submit_final`. This proves your cap, not your evaluator, is what ends the
loop.

---

## Cheat sheet

```text
REFINEMENT LOOP + OBSERVABILITY — the recap

REFINEMENT LOOP
  Phase 1  decompose → invoke exactly one spoke per partition
  Phase 2  after all report → call evaluate_coverage(findings)
             returns { coverage_score, sufficient, gaps }
  Phase 3  if not sufficient AND iterations < MAX_ITERATIONS:
               re-delegate ONLY the gaps → back to Phase 2
           else:
               submit_final   (NEVER allowed before an evaluation)
  SAFETY   MAX_ITERATIONS (Andrew uses 4) — a loop with no cap can run forever
  TRUTH    refining is not automatically improving — MEASURE (score can drop)

THE EVALUATOR
  A separate judge. Scores coverage, names gaps. Does NOT do the work.
  Structured output (typed JSON tool) so the coordinator can branch on it.

OBSERVABILITY — audit 4 dimensions
  message capture  store BOTH question sent and response received (not lost)
  context control  what each spoke is given (and whether scope is enforced)
  spoke isolation  spokes talk only to coordinator, never each other
  error handling   wrap json.loads etc.; a bad reply = logged ERROR, not crash

STRUCTURED LOGGING (replaces print)
  { ts, level (INFO/ERROR), iteration, agent, event, payload }
  → searchable, comparable, replayable, persistent
  print to stdout = ephemeral = NOT observability

DONE = from the log alone you can say: how many iterations,
       score up or down, which gaps re-delegated.
```

## How this connects to the rest of the course

- **Earlier, Module 3 · Lesson 9 ("Task decomposition done right"):** gave your
  coordinator the ability to split a task into partitions and delegate them. This
  lesson grades and retries that work, and makes it observable.
- **Earlier, Module 3 (loop antipatterns):** taught that every agent loop needs a
  hard stop. The `MAX_ITERATIONS` cap here is that rule applied to refinement.
- **Next, Module 3 · Lesson 11 ("Failure recovery and a clean coordinator
  refactor"):** the logging you add here is the foundation for handling spoke
  failures gracefully — and it cleans up the "one big dumb file" this lesson
  admits it left behind.
- **Later in the course:** the same observability discipline underpins Atlas
  Support's reliability checks and its final ability to escalate to a human — you
  can only hand off safely what you can fully see.

---

*Source: "Claude Certified Architect: Foundations" by Andrew Brown, ExamPro. Code
snippets and diagrams are illustrative reconstructions of the patterns described
in the course. Adapt them to the current SDK.*
