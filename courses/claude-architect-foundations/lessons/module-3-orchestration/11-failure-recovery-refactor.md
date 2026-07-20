# Module 3 · Lesson 11: Failure recovery and a clean coordinator refactor

> **Course:** Claude Certified Architect: Foundations, a self-paced course
> **Module 3:** Orchestration: multi-agent architectures — turn one agent into a reliable coordinated system
> **Speaker:** Andrew Brown, ExamPro
> **Source:** Reconstructed from the CCA-F course by Andrew Brown (ExamPro) · [full transcript](../../transcripts/cca-f-full-course.txt)
> **Estimated time:** 45 to 60 minutes (read plus lab)

---

## In one sentence

When a sub-agent fails, don't crash the whole system and don't silently swallow the error — catch it as a **typed error**, hand the coordinator **structured error context** so it can recover locally, and once your coordinator works, refactor the one giant file into clean `prompts/`, `tools/`, and `lib/` modules with parseable JSON logs.

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone Project** where you make Atlas Support resilient: you deliberately break one sub-agent, watch the coordinator recover instead of dying, then split the messy single file into readable modules. Everything before the Capstone teaches the two skills you'll use there — failure handling and the refactor. If you want to see the finish line first, jump to the **"Capstone Project"** section, then come back.

## First-principles companion

> 💡 **The durable ideas behind this lesson.** The SDKs are new; the engineering ideas are decades old.
>
> - **[On the Criteria To Be Used in Decomposing Systems into Modules](https://www.cs.umd.edu/class/spring2003/cmsc838p/Design/criteria.pdf)** (David Parnas, 1972). The classic argument that you split a system into modules by *hiding decisions that are likely to change*, not by copying the flowchart. This is exactly why the refactor moves prompts, tools, and logging into their own files.
> - **[Erlang/OTP supervision trees](https://www.erlang.org/doc/design_principles/sup_princ.html)** (Ericsson). A whole industry ran phone switches on the idea that a worker may fail, report *what* failed in a structured way, and let a supervisor decide whether to recover — rather than one failure taking the system down. Your coordinator is a supervisor; your sub-agents are workers.

## A few plain-language basics first

This lesson uses some everyday terms. Here they are in plain words:

- **Agent:** an AI that takes a series of actions on its own toward a goal, rather than answering in one shot.
- **Sub-agent:** an agent spawned by another agent, usually with its own isolated context (its own private conversation, unaware of the other agents).
- **Coordinator / hub-and-spoke:** an architecture where one *coordinator* agent owns routing, context, and aggregation, and delegates to *sub-agents* ("spokes") exposed to it as tools.
- **Tool / tool call / tool result:** a function the model can choose to run; when it decides to use one that is a *tool call*, and what comes back is the *tool result*.
- **Structured output:** making the model (or your code) return machine-readable data — usually JSON — instead of free-form prose.
- **Exception:** in Python, the object your code raises when something goes wrong. Uncaught, it stops the program ("crashes"). You can *catch* it with `try/except` and decide what to do.
- **JSON / JSONL:** JSON is a text format for structured data (`{"key": "value"}`). JSONL is "JSON Lines" — one JSON object per line in a file, so each log entry is a record you can parse later.
- **Refactor:** changing how code is *organized* without changing what it *does* — to make it readable and maintainable.
- **Stateless class:** a class used only as a labelled bucket of functions (static methods) that hold no data of their own — every input comes in as an argument and every result comes out as a return value. More on this in Part 5.

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

Up to now you have built a coordinator that delegates to sub-agents and *works when everything goes right*. Production is not that. A sub-agent will hit a permission wall, get an empty result, or throw an exception — and the two obvious reactions are both wrong. As Andrew frames the exam guide's point: "silently suppressing errors or terminating entire workflows on single failures are both antipatterns for obvious reasons." Swallow the error and you ship a lie; crash the workflow and one flaky tool takes down the whole job. The professional middle path is **typed, structured error context** that lets the coordinator recover.

And there's a second, quieter lesson here about craft. Andrew's coordinator grew into "one big dumb file," and he is blunt about it: "if you are not a programmer, you might not know that this is not good code... just because the agent can make sense of it and summarize it, that's not good enough. We need to make it so that it is more human readable." Refactoring for *technical ownership* — so you, a human, know exactly what your code does — is part of being an architect, not an afterthought.

## Learning objectives

By the end of this lesson you will be able to:

1. Raise and catch **typed errors** so a sub-agent failure never crashes the coordinator.
2. Return **structured error context** (failure type, what was attempted, partial results) instead of a generic error string.
3. Distinguish an **access/permission failure** from an **invalid/empty request**, and implement **local recovery** for transient failures inside the sub-agent.
4. Make a failure **bubble up** as parseable data the coordinator can act on and summarise.
5. Refactor a monolithic coordinator into `prompts/`, `tools/`, and `lib/` modules with **stateless classes** and **JSON logs**.

## Prerequisites

- **Module 3 · Lesson 8 (Hub-and-spoke: your first coordinator)** and **Lesson 10 (Refinement loops and observability)** — you should already have a coordinator that delegates to sub-agents and logs what it does.
- Comfort running a Python script and reading a `try/except` block.
- An Anthropic API key set in a `.env` file (from Module 0).

---

## Part 1: The two antipatterns — crash and silence

Picture Atlas Support's coordinator delegating to three sub-agents: an **inventory agent**, an **order agent**, and a **notification agent**. The notification agent tries to ping the executive team and gets denied — a permission error. What happens next defines whether your system is production-grade.

There are two tempting, wrong answers:

| Antipattern | What it looks like | Why it's bad |
|---|---|---|
| **Crash the workflow** | The exception propagates; the whole coordinator dies on one sub-agent's failure | One flaky tool call throws away all the work the other agents already did |
| **Silence the error** | `try/except: pass` — swallow it and return as if nothing happened | The coordinator reports success on a lie; nobody learns the notification never sent |

Andrew reads the exam guide's wording almost verbatim and agrees with it: "silently suppressing errors or terminating entire workflows on single failures are both antipatterns for obvious reasons because that would be bad."

> 🔑 **A single sub-agent failure should neither crash the system nor disappear. It should become *information* the coordinator can act on.**

The right answer is a third path: the sub-agent catches its own failure, packages *what went wrong* as structured data, and returns it. The coordinator reads that data and decides — retry, route around it, or report a partial result honestly. That third path is the whole rest of this lesson.

## Part 2: Typed errors — give every failure a name

The first building block is the **typed error**. Instead of a bare string like `"something broke"`, every failure carries a *type* that says what *kind* of failure it was. In Andrew's build, "every error is typed" — there's a small helper (`make_error`) that stamps each failure with a category.

Why type them? Because the coordinator's recovery decision depends on the *kind* of failure:

- An **access failure** (a permission was denied) might be recovered by trying a different, permitted path.
- An **invalid or empty request** (you asked for zero units, or a product that doesn't exist) is not going to succeed on retry — retrying is pointless.
- A **transient failure** (a momentary network blip) is exactly the kind you *should* retry.

If all three come back as the string `"error"`, the coordinator can't tell them apart. Give them types and it can.

```python
# Illustrative reconstruction — adapt to your SDK.
class FailureType:
    ACCESS_DENIED   = "access_denied"    # a permission wall
    INVALID_REQUEST = "invalid_request"  # empty / malformed / impossible
    TRANSIENT       = "transient"        # momentary; safe to retry
    UNKNOWN         = "unknown"

def make_error(failure_type: str, message: str, attempted: str) -> dict:
    """Every failure in the system is minted through this one helper."""
    return {
        "status":       "failed",
        "failure_type": failure_type,   # the *type* — the load-bearing field
        "message":      message,
        "attempted":    attempted,      # what the sub-agent actually tried
    }
```

> 💡 **The type is the load-bearing field.** The human-readable `message` is for your logs; the `failure_type` is what your code branches on. Andrew notes the exam guide asks you to "distinguish between access failures, invalid/empty requests" — and observes the *type already tells you that*, so you don't need a separate flag. The type is the distinction.

## Part 3: Structured error context — return data, not a sentence

A type alone isn't enough. When a sub-agent fails, the coordinator needs enough *context* to make a good decision and to report honestly. So every sub-agent — success or failure — returns **one JSON object** in the same shape. Andrew's report format carries "status, sub-agent, summary, attempts, failures" and more.

```python
# Illustrative reconstruction of a sub-agent's structured report.
{
    "status":    "completed",        # or "failed" / "recovered"
    "sub_agent": "inventory",        # who is reporting
    "summary":   "Reserved 5 units of Widget A.",
    "attempts":  2,                  # how many tries it took
    "failures":  [                   # the typed errors it hit along the way
        {
            "failure_type": "transient",
            "message":      "Inventory service timed out.",
            "attempted":    "check_inventory(widget_a)"
        }
    ],
    "partial_results": {"reserved": 5}   # what it *did* manage to do
}
```

Three things make this "structured error context" rather than just an error message:

1. **Failure type** — from Part 2, so the coordinator can branch.
2. **What was attempted and when** — `attempted` and `attempts` show the sub-agent's effort, so the coordinator (and you) can see the story.
3. **Partial results** — if the agent got *some* of the way, say so. Half a result reported honestly beats a total crash.

> 🔑 **Every sub-agent returns the same JSON shape whether it succeeds or fails. Success and failure are just different values of `status` in one predictable structure — never a return in one case and an exception in another.**

Because the shape is identical, the coordinator has exactly one thing to parse. It never has to guess whether it's holding a result or a crash — it reads `status` and goes.

## Part 4: Local recovery — let the sub-agent try to save itself first

Not every failure needs to reach the coordinator. The exam guide (and Andrew's build) call for a sub-agent to "implement local recovery for transient failures" — meaning the sub-agent tries to fix things *itself* before reporting up.

The clearest example in the build is the **notification agent**. It tries a direct executive-team notification and gets denied: "direct executive team notification denied." Instead of failing outright, it *recovers locally* — it routes the message a different, permitted way and reports back a `"recovered"` status. The coordinator sees that the notification ultimately went out, just via a fallback path.

```python
# Illustrative reconstruction of local recovery inside a sub-agent.
def notify(target, message):
    try:
        return send_direct(target, message)          # preferred path
    except AccessDenied as e:
        # Recover locally instead of bubbling a hard failure up:
        result = send_via_queue(target, message)     # permitted fallback
        return {
            "status":    "recovered",
            "sub_agent": "notification",
            "summary":   f"Direct notify to {target} denied; delivered via queue.",
            "attempts":  2,
            "failures":  [make_error(FailureType.ACCESS_DENIED,
                                     str(e), f"send_direct({target})")],
        }
```

The rule of thumb: **recover as low as you can.**

- A **transient** failure? The sub-agent retries locally — the coordinator shouldn't even hear about a blip that fixed itself.
- An **access** failure with a known fallback? Recover locally and report `"recovered"`.
- A failure the sub-agent genuinely can't handle? *Now* it bubbles up — as structured context, so the coordinator can decide.

> ✅ **What to do about it:** give each sub-agent a short, explicit set of recovery rules in its own prompt ("if the direct channel is denied, use the queue; if inventory times out, retry twice"). Andrew's inventory agent, he notes, "has its detailed rules on how it should recover." Local recovery is a *prompt* instruction backed by a *code* fallback.

## Part 5: Scoped tools and isolated sub-agents (why this stays clean)

Two design choices make the failure handling above actually hold together, and both are worth naming because the exam leans on them.

**Scoped tool sets.** "Each sub-agent only sees its own tools." The inventory agent gets `check_inventory`; the order agent gets `place_order`; the notification agent gets `notification`. Andrew: "they each only get one tool, which is fine." A sub-agent can't cause a failure with a tool it was never handed — scoping shrinks the blast radius.

**Isolation.** Each sub-agent runs as a real sub-agent with "their own context and are unaware of any other agent... independently running." A registry maps a name to a sub-agent, and a `run_sub_agent` function spins one up on demand. Because they're isolated, one sub-agent's failure can't corrupt another's context — it can only return a report.

### A note on the Agent SDK (a judgment call, not a rule)

Andrew stops to ask the honest question: since he *hand-rolled* this coordination, should he just use the **Claude Agent SDK** instead? (The Agent SDK is the higher-level library for building agents — it has a built-in *agent definition* that gives you isolation, tool restriction, and specialized instructions for free.) He checks the docs and reasons it through:

- The Agent SDK's sub-agents give you concurrency, a built-in filesystem, session resume — "the Agent SDK shines when you want filesystem, shell, sub-agents; that's what it's built for."
- But this coordinator is **sequential** and **domain-specific**, and the whole point of the exercise is to *teach the mechanics*. Wrapping them in an abstraction would "hide the exact mechanics we're teaching."

His verdict: "for this use case, sequential is fine — stick with the manual pattern." That is the lesson's recurring theme in miniature: **don't reach for the heavier tool by reflex; verify it fits your case first.** (You *will* port this to the Agent SDK — that's the very next lesson. Here, hand-rolled wins because it teaches.)

> 🔑 **Scope each sub-agent to only the tools it needs, isolate its context, and pick your framework by whether it fits the job — not by what's fanciest.**

## Part 6: The refactor — one big file becomes clean modules

Your coordinator now handles failure well. But look at the source: it's all in one `main.py`. Andrew is unsparing: "you shouldn't have one big dumb file like this... it works for this point that we've been able to hold this all into memory. But if we came back later, we wouldn't be able to really make sense of it. And just because the agent can make sense of it and summarize it, that's not good enough."

The refactor is driven by a written `refactor.md` task list — Andrew makes his complaints concrete, one file structure at a time. Here is the target layout:

```text
coordinator/
├── main.py                 # thin entry point — wires things together, little logic
├── prompts/                # every prompt as its own .md file
│   ├── coordinator.md
│   ├── inventory_agent.md
│   └── notification_agent.md
├── tools/                  # each tool split out
│   ├── check_inventory.py  # the tool's *code*
│   ├── place_order.py
│   └── tools.json          # the JSON schema that gets passed to the API
├── lib/                    # reusable internals
│   ├── coordinator.py      # the coordinator class
│   ├── partitions.py       # partition/decomposition logic
│   ├── coverage_report.py  # coverage reporting
│   ├── logger.py           # one consistent logging helper
│   └── templates.py        # loads templates and injects variables
├── data/                   # data artifacts (no more hardcoded blobs)
├── logs/                   # JSON/JSONL log output
└── reports/                # timestamped human-readable reports
```

The moves, and the *reason* for each (this is Parnas's rule from the companion — separate the things that change independently):

| Move | Why |
|---|---|
| Prompts → `prompts/*.md` | Prompts change constantly and are content, not logic. Editing a prompt shouldn't mean touching code. |
| Tools → `tools/*.py` + `tools.json` | Each tool's code lives on its own; the JSON schema that's "passed to `create`" lives beside it. No more one wieldy tools blob. |
| Partition + coverage logic → `lib/` | Reusable internals belong together, out of `main.py`. |
| Hardcoded data → `data/` | "Make a data folder and store data artifacts and load them into the app." Data is not code. |
| Message content templates → `prompts/` | Those inline strings with variable slots are really prompts too — "prompts for content." Template them and load them. |

> 💡 **The refactor is iterative and honest.** Andrew doesn't get it in one shot — he refactors, re-reads, finds `main.py` "still yick, it's really really long," and writes *more* tasks. That's normal. As he puts it, "I usually just have a sense of like, is this readable?" Trust that sense and keep going until a stranger could read it.

## Part 7: Stateless classes and JSON logs — the two finishing touches

Two specific preferences give the refactored code its final shape, and both pay off when you later write tests or parse logs.

### Stateless classes

Andrew's strong preference: "I would probably prefer stateless classes... that makes it really easy to track inputs and outputs of stuff." A **stateless class**, in his words, is "a class with static methods" — it holds no data of its own; it's a *labelled home* for related functions so you always know where a function lives and who owns it.

He dislikes "loose functions where we don't know where they're coming from and who owns them." So `partitions.py` becomes a `Partitions` class of static methods; the coordinator becomes a `Coordinator` class. And the giant `run_coordinator` function gets broken into many small functions where "the functions basically act as documentation" — the contents of an `if` block become a named function call, so the code reads like a description of itself.

```python
# Illustrative reconstruction — a stateless class = a class of static methods.
class Partitions:
    @staticmethod
    def generate(request: str) -> list[dict]: ...
    @staticmethod
    def validate_overlap(partitions: list[dict]) -> None: ...
    @staticmethod
    def index_by_agent(partitions: list[dict]) -> dict: ...
```

Why bother? Testing. Andrew: "if you want to write test code for this, then you have an input and an output and you know exactly what to mock going in there and out of there." Small, stateless functions with dumb inputs and outputs are trivial to test — that's the payoff.

> 🔑 **Small functions and stateless classes turn your code into its own documentation and make it testable: every piece has a clear input and a clear output you can mock.**

### JSON logs

The final touch is *how* you log. Plain-text lines like `coordinator: delegate` read fine but you can't do anything with them later. Andrew: "I'd probably prefer to log out JSON structure because then we could parse that information... if you're data-driven, you have JSONL data as logs, it's super super useful."

So instead of prose, each log entry is a JSON object written one-per-line to a `logs/` folder:

```text
{"event": "delegate", "sub_agent": "inventory", "attempts": 1, "status": "completed"}
{"event": "recovery", "sub_agent": "notification", "failure_type": "access_denied", "status": "recovered"}
{"event": "final", "summary": "5 units reserved; exec notified via queue."}
```

Now your logs are *data*. You can grep them, count failures by type, feed them into another tool. A consistent `lib/logger.py` with helper functions (`log.event(...)`, `log.warn(...)`) that stamp each entry keeps every line in the same shape — no more "inconsistent" logging.

---

## Key takeaways

1. **Two antipatterns to avoid.** Never crash the whole workflow on one sub-agent's failure, and never silently swallow the error. Take the third path: structured recovery.
2. **Type every error.** A `failure_type` (access / invalid / transient) is the field your coordinator branches on. A bare error string can't be recovered from intelligently.
3. **Return structured error context, not a sentence.** Same JSON shape for success and failure — `status`, `failure_type`, `attempted`, `attempts`, `partial_results`.
4. **Recover as low as you can.** Sub-agents fix transient blips and known-fallback failures themselves; only genuinely unhandleable failures bubble up.
5. **Scope tools and isolate sub-agents.** Each sub-agent sees only its own tools and its own context — smaller blast radius, no cross-contamination.
6. **Refactor for humans, not just the AI.** Split into `prompts/`, `tools/`, `lib/`; use stateless classes and small self-documenting functions; log as JSON. You're buying *technical ownership*.

## Common pitfalls

- ❌ **`try/except: pass`.** The most dangerous line in agent code. It reports success on a failure. Always return a typed, structured failure instead.
- ❌ **Retrying an invalid request.** Retrying an `invalid_request` (zero units, nonexistent product) just wastes tokens and time — it will fail identically. Only `transient` failures deserve a retry.
- ❌ **Different return shapes for success and failure.** If success returns a dict but failure raises an exception, the coordinator needs two code paths. Return the *same* shape; branch on `status`.
- ❌ **Refactoring by moving, not by thinking.** Andrew catches the AI shoving functions into `partitions.py` without asking whether they *belong* there. Moving code isn't refactoring unless each piece lands where its responsibility lives.
- ❌ **Trusting "the AI understood it."** Readable-to-Claude is not readable-to-you. If you couldn't return in a month and explain the file, it isn't done.
- ❌ **Prose logs you can't parse.** `print("done")` feels fine until you need to count failures by type across 500 runs. Log JSON from the start.

---

## 🛠️ Capstone Project: Make Atlas Support resilient, then refactor it clean

> This is the main hands-on project for the lesson. You'll feel the difference between an agent that *dies* on a bad input and one that *reports honestly and recovers* — and then experience the relief of a codebase you can actually read. Keep it small on purpose.

### What you will build

Take your Lesson 10 coordinator (the one with logging) and do two things to it. First, harden it: give its sub-agents typed errors, structured reports, and local recovery, then deliberately break one and confirm the coordinator recovers instead of crashing. Second, refactor the single file into clean modules with JSON logs. The two halves are independent — each is a complete win on its own.

Its pieces, each mapped to a lesson idea:

- Three scoped sub-agents (inventory, order, notification) — *Part 5*
- A `make_error` helper and `FailureType` categories — *Part 2*
- A single structured report shape returned by every sub-agent — *Part 3*
- Local recovery in the notification agent — *Part 4*
- A `prompts/ tools/ lib/` layout with stateless classes — *Parts 6 & 7*
- JSON/JSONL logs in a `logs/` folder — *Part 7*

### Why this is the perfect practice

| Lesson idea | Where you use it in Atlas Support |
|---|---|
| Two antipatterns | You *watch* the crash, then fix it into a recovery |
| Typed errors | `FailureType` + `make_error` (Milestone 2) |
| Structured error context | The one report shape every sub-agent returns (Milestone 3) |
| Local recovery | Notification agent's denied → queue fallback (Milestone 4) |
| Bubbling up | Set inventory to zero and watch the failure surface as data (Milestone 5) |
| Clean modules | The `prompts/ tools/ lib/` refactor (Milestone 6) |
| JSON logs | JSONL entries in `logs/` (Milestone 7) |

### Milestones (build them in order, each one works on its own)

1. **Reproduce the happy path.** Copy your Lesson 10 coordinator into a new `coordinator_failure_handling/` folder. Confirm it delegates to three sub-agents and returns a final summary. This is your baseline.
2. **Add typed errors.** Write `FailureType` (access / invalid / transient / unknown) and a `make_error(failure_type, message, attempted)` helper. Nothing uses it yet — just get the shape right.
3. **Make every sub-agent return one report shape.** Give each sub-agent a return of `{status, sub_agent, summary, attempts, failures, partial_results}` — the same keys whether it succeeds or fails. The coordinator now parses exactly one structure.
4. **Add local recovery to the notification agent.** Have it try a direct executive-team notify, catch the denial, fall back to a permitted channel, and return `status: "recovered"` with the access failure recorded in `failures`. Run it; confirm the coordinator sees a recovery, not a crash.
5. **Break it on purpose and watch it bubble up.** As Andrew does — "let's make it so that it absolutely does break" — set the requested inventory to **zero**. Run it. Confirm you get a clean `status: failed` report with the failure type, *not* a Python traceback, and that the coordinator still finishes and summarises.
6. **Refactor into modules.** Write a `refactor.md` task list, then split `main.py`: prompts to `prompts/*.md`, tools to `tools/*.py` + `tools.json`, partition/coverage/coordinator logic to `lib/`, hardcoded data to `data/`. Make `partitions.py` and the coordinator **stateless classes** (classes of static methods). Re-read `main.py` — is it short and obvious now?
7. **Switch to JSON logs.** Add `lib/logger.py` with helper functions that write one JSON object per line to `logs/coordinator.jsonl`. Run the whole thing and open the log — every line should be parseable JSON.
8. **Stretch goals.** (a) Dump the coverage report as a timestamped, human-readable file in a `reports/` folder. (b) Add a second recovery path (e.g. retry a `transient` inventory timeout twice before giving up). (c) Write one unit test for a stateless static method — feel how easy the mocking is now.

### How you will know you are done

- ✅ Setting inventory to zero produces a structured failure report and a normal coordinator summary — **no uncaught exception, no crash**.
- ✅ The notification agent logs a denial and still delivers via fallback, reporting `status: "recovered"`.
- ✅ Every sub-agent returns the identical set of JSON keys for both success and failure.
- ✅ `main.py` is short; prompts, tools, and lib each live in their own files; `partitions.py` is a class of static methods.
- ✅ `logs/coordinator.jsonl` contains one valid JSON object per line.

> 💡 **Keep yourself honest:** after the refactor, close the file, wait, reopen it, and try to explain `main.py` out loud in two sentences. If you can't, it isn't refactored yet — that's the "would I know what I'm looking at in a month" test Andrew keeps applying.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice on one idea. Optional and independent; the Capstone already touches all of them, so feel free to skip straight to it.

### Exercise 1: Name three failures (foundational)
For each of these, write the `failure_type` and say whether the sub-agent should retry, recover locally, or bubble up: (a) inventory service times out once; (b) user asks for −3 units; (c) the notification tool is denied but a queue is available.

### Exercise 2: One shape to rule them all (intermediate)
Take a sub-agent that currently returns a plain string on success and raises an exception on failure. Rewrite it so both paths return the same `{status, ...}` dict. Then write the three lines of coordinator code that branch on `status`.

### Exercise 3: Turn a monolith into modules (advanced)
Take any single-file script you have (doesn't have to be this one). Write a `refactor.md` listing five specific things you dislike about it, then move prompts/data/logic into separate files and convert one loose group of functions into a stateless class. Re-read the entry point and confirm it got shorter.

---

## Cheat sheet

```text
FAILURE RECOVERY — THE THIRD PATH
  Antipattern 1: crash the workflow on one sub-agent failure   ❌
  Antipattern 2: silently swallow the error (try/except: pass) ❌
  Right answer:  typed error → structured context → recover    ✅

TYPED ERRORS (branch on the type)
  access_denied    → try a permitted fallback (recover locally)
  invalid_request  → do NOT retry (will fail identically)
  transient        → retry locally, don't even tell coordinator
  unknown          → bubble up as structured data

STRUCTURED REPORT (same shape for success AND failure)
  { status, sub_agent, summary, attempts, failures[], partial_results }
  status: completed | failed | recovered

LOCAL RECOVERY: fix it as LOW as you can; bubble up only what you can't.

SCOPE & ISOLATE: each sub-agent sees only its own tools + its own context.
FRAMEWORK CHOICE: sequential/domain-specific → hand-rolled is fine;
  Agent SDK shines for filesystem/shell/concurrent sub-agents. Verify fit.

REFACTOR LAYOUT
  main.py            thin wiring, little logic
  prompts/*.md       every prompt (and content template) as a file
  tools/*.py + .json code per tool + the schema passed to create
  lib/               coordinator.py, partitions.py, coverage_report.py,
                     logger.py, templates.py   (stateless classes!)
  data/  logs/  reports/

STATELESS CLASS = class of @staticmethod functions, holds no state.
  Small functions = self-documenting + trivial to test (clear in/out).

JSON LOGS: one JSON object per line (.jsonl) → parseable, greppable, ingestable.

THE TEST: could a stranger (or you in a month) read main.py and get it?
```

## How this connects to the rest of the course

- **Earlier, Module 3 · Lesson 8 (Hub-and-spoke):** gave you the coordinator and sub-agents-as-tools that you now make *resilient*.
- **Earlier, Module 3 · Lesson 10 (Refinement loops and observability):** gave you the logging you now upgrade to structured JSON logs.
- **Next, Module 3 · Lesson 12 (The Claude Agent SDK and the Agent tool):** you port this exact refactored coordinator to the Agent SDK — the clean module layout is what makes that port sane, and you'll finally use the built-in agent isolation you hand-rolled here.
- **Later, Module 6 (Context management and reliability):** typed failures and structured context are the foundation for validation retries and human review — and the whole idea returns in the **Module 7 capstone**, where Atlas Support escalates to a human with a structured handoff package.

---

*Source: Reconstructed from the CCA-F course by Andrew Brown (ExamPro). Code snippets and diagrams are illustrative reconstructions of the patterns described in the course. Adapt them to the current SDK.*
