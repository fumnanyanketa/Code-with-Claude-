# Module 2 · Lesson 6: Forcing structured output

> **Course:** Claude Certified Architect: Foundations, a self-paced course
> **Module 2:** Prompting & structured output: steer the model reliably before you orchestrate many of them.
> **Speaker:** Andrew Brown, ExamPro
> **Source:** Reconstructed from the CCA-F course by Andrew Brown (ExamPro) · [full transcript](../../transcripts/cca-f-full-course.txt)
> **Estimated time:** 45 to 60 minutes (read plus lab)

---

## In one sentence

You force Claude to hand back clean, machine-readable JSON by giving it a *tool* whose input schema (types, enums, required fields) describes exactly the shape you want, then using `tool_choice` to make the model fill that shape — while sidestepping the trap where forcing a specific `tool` on every request loops forever.

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone
> Project** where you build the **Atlas Support triage classifier**: feed it a
> raw, messy support ticket and force it to emit a strict JSON verdict — a
> category from a fixed list, a priority, and a short reason — then validate that
> verdict in code. Everything before the Capstone teaches the pieces you will use
> there. If you want to see the finish line first, jump to the
> **"Capstone Project"** section, then come back.

## First-principles companion

> 💡 **The durable idea behind this lesson.** SDKs and model names change, but the
> way you describe a data shape to a machine does not. For the timeless,
> tool-agnostic version:
>
> - **[JSON Schema](https://json-schema.org/)** (the specification). JSON Schema
>   is *the* declarative language for saying "valid data looks like this" — types,
>   allowed values (enums), which fields are required, nested objects, arrays. A
>   tool's `input_schema` is just JSON Schema, and frontier models are trained to
>   read it. Learn the vocabulary once and it transfers to every provider and
>   every validator you will ever touch.

## A few plain-language basics first

This lesson uses some everyday terms. Here they are in plain words:

- **Structured output:** making the model return machine-readable data (usually
  JSON) instead of free-flowing prose, by giving it a tool with a JSON input
  schema (types, enums, required fields). "Machine-readable" means your code can
  parse it and act on it without guessing.
- **JSON:** a simple text format for data — objects with named fields, e.g.
  `{"category": "billing", "priority": "high"}`. It is how programs pass
  structured data around.
- **Tool / tool call / tool result:** a function the model can choose to run.
  When it decides to use one, that is a *tool call*; what comes back is the *tool
  result*. Here we use a tool not to *do* something, but purely to make the model
  produce data in the tool's declared input shape.
- **JSON Schema:** a declarative language for describing and validating the
  structure, data types, and constraints of a JSON document.
- **Enum:** short for *enumeration* — a fixed list of allowed values for a field
  (e.g. a `unit` field that may only be `"celsius"` or `"fahrenheit"`).
- **`tool_choice`:** the setting that forces *how* the model uses tools —
  `auto`, `any`, a specific `tool`, or `none`. It lives in the low-level
  **Anthropic SDK**.
- **`stop_reason`:** the field the API returns saying *why* the model stopped —
  `tool_use` (it wants to run a tool) or `end_turn` (it is finished). You drive
  the loop off this, never off parsing the text. (From Module 1.)
- **Pydantic:** a popular Python library where you describe data shapes as
  classes; it emits JSON Schema and validates data against it.

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

In the last lesson you learned to *steer* the model with prompts. But a good
prompt still returns prose, and prose is a nightmare to build software on top of —
you end up writing brittle string parsing that breaks the moment Claude phrases
something differently. The fix is to stop parsing text at all. As Andrew shows,
you hand Claude a tool whose input schema *is* the data shape you need, and Claude
"is going to read that input schema because it's schema JSON, and then it will
know what to generate out." This is the difference between an agent that *chats*
and an agent that *feeds a system*. Atlas Support cannot route a ticket on a
paragraph of English; it needs `{"category": "billing", "priority": "high"}`. This
lesson is how you get that, reliably — and how to avoid the infinite loop that bit
Andrew live on camera.

## Learning objectives

By the end of this lesson you will be able to:

1. Explain the four `tool_choice` modes (`auto`, `any`, `tool`, `none`) and what each guarantees.
2. Write a tool `input_schema` in JSON Schema using types, arrays, **enums**, and **required** fields to constrain what Claude returns.
3. Force clean structured JSON from a single API call and read the payload off the tool-use block.
4. Diagnose and avoid the force-`tool` infinite loop by understanding how `tool_choice` interacts with `stop_reason`.
5. Add a validation layer (by hand, or with Pydantic) to catch semantic errors the schema cannot.

## Prerequisites

- **Module 1 · Lesson 3 (Tools and the stop-reason loop)** and **Lesson 4 (ending the loop correctly)** — you must already know that you drive control flow off `stop_reason`, not off the text. This lesson is where that pays off.
- **Module 2 · Lesson 5 (Prompting that steers the model)** — few-shot examples and specific prompts; we reuse the "give the model the structure" idea.
- A working Anthropic SDK setup and an API key (Module 0). Python is assumed.

---

## Part 1: Why structured output, and how a tool schema shapes it

The core move is counterintuitive at first: you use a **tool** even though you do
not care what the tool *does*. You care about the *shape of data the model must
produce to call it*. A tool declares an `input_schema` — a JSON Schema document —
and the model reads that schema to decide exactly what JSON to generate.

Andrew's canonical example is a weather tool with a `unit` field:

```python
# Illustrative reconstruction — a tool whose INPUT is the data shape we want.
weather_tool = {
    "name": "record_weather",
    "description": "Record a weather reading.",
    "input_schema": {
        "type": "object",
        "properties": {
            "location": {"type": "string"},
            "unit": {
                "type": "string",
                "enum": ["celsius", "fahrenheit"],   # <-- fixed set of choices
            },
        },
        "required": ["location", "unit"],            # <-- both must be present
    },
}
```

The schema vocabulary you need is small. As Andrew puts it, "the thing that I want
you to pay attention to is the different types of properties":

| JSON Schema piece | What it does |
|---|---|
| `"type": "string" / "integer" / "number" / "boolean"` | The primitive type of a field. |
| `"type": "array", "items": {…}` | A list, with a schema for each element. |
| `"type": "object", "properties": {…}` | A nested object with its own fields. |
| `"enum": [ … ]` | Restricts a field to a fixed set of allowed values. |
| `"required": [ … ]` | Names the fields that must be present (not optional). |

> 🔑 **The tool's `input_schema` is your contract.** Claude reads it as JSON
> Schema and generates output that fits it. Design the schema and you have
> designed the output.

## Part 2: Enums and required — the two levers (EXAM TIP)

Two schema features do almost all the work of making output *clean* rather than
merely *JSON-shaped*, and they are exactly what the exam probes.

**Enums** turn an open-ended field into a decision. A `unit` field typed as a
plain string could come back as `"C"`, `"Centigrade"`, `"metric"` — anything.
Add `"enum": ["celsius", "fahrenheit"]` and, as Andrew says, "now the AI can
determine, well, which one should I input." You have converted a
generate-any-text problem into a pick-one-of-these problem, which the model does
far more reliably. For Atlas Support, an enum is how you guarantee a ticket's
`category` is always one of *your* routable categories and never a surprise
string your router has no branch for.

**Required** stops the model from quietly omitting a field. With
`"required": ["location", "unit"]`, "it expects both location [and] unit to be
supplied. They're not optional." Miss this and you will hit runtime errors like
the `field name required` / `field ... required` failures Andrew ran into when
Claude left a field out.

> 🔑 **EXAM TIP — enums + required are the levers.** When a question asks how to
> make structured output reliable, the answer centres on the tool's input schema:
> **enums** constrain *which* values are allowed, **required** constrains *which
> fields must appear*. Types alone are not enough.

> 💡 **Schema stops syntax errors, not meaning errors.** As Andrew notes, "strict
> JSON schemas via tool use limit syntax errors but do not prevent semantic
> errors." The schema guarantees the JSON is well-formed and the enum value is
> from the list — it cannot guarantee the model picked the *correct* enum value
> for this ticket. That gap is what Part 5 (validation) and human review (Module
> 6) exist to close.

## Part 3: The four `tool_choice` modes

`tool_choice` is the setting that controls *whether and how* the model reaches for
a tool. Andrew is emphatic about one thing up front: "notice that we're using the
Anthropic SDK because you have to use that. It's not available in the Agent SDK,
which I thought it was, but it isn't."

The four modes:

| Mode | Meaning | Can it return plain text / `end_turn`? |
|---|---|---|
| `auto` | Claude decides whether to use a tool at all. | Yes — it may just answer in text. |
| `any` | Must use *some* tool from the list; Claude picks which. | Not on that call — it is forced to call a tool. |
| `tool` (with a `name`) | Must use *this specific* named tool. | No — forced every time. |
| `none` | Claude cannot use any tool. | Yes — text only. |

```python
# Illustrative — forcing one specific tool. Note BOTH type and name are required.
resp = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=1024,
    tools=[triage_tool],
    tool_choice={"type": "tool", "name": "submit_triage"},  # force this tool
    messages=[{"role": "user", "content": raw_ticket}],
)
```

A few hard-won details from Andrew's session, each a small verify-everything lesson:

- **`auto` is the risky one for structured output.** "If you want structured JSON
  output and a tool is going to return that... if it doesn't use that tool, then
  it might just return back text, and so that is an edge case where things might
  break." For guaranteed output you want `any` or `tool`, not `auto`.
- **The value is `tool`, not `force`.** Andrew's own slide said `force` — and the
  API rejected it: `tool choice force bad, using type does not match auto, any,
  tool, or none`. He corrected it live: "I have the word wrong. So it's
  technically `tool`... that obviously is bad and out of date." A clean reminder
  that even the instructor's slides (and the exam guide) can be wrong — the API is
  the source of truth.
- **`type: "tool"` needs a `name`.** `tool_choice: {"type": "tool"}` alone errors
  with `name ... required`; you must say *which* tool: `{"type": "tool", "name":
  "submit_triage"}`.

> ✅ **What to do about it:** for one-shot structured output, force the tool
> (`{"type": "tool", "name": ...}`) so the model cannot wander off into prose.
> Just do not wrap that forced call in a naive loop — which is exactly the trap
> Part 4 is about.

### The Agent SDK does not expose it

Andrew spends a long stretch trying to make `tool_choice` work in the higher-level
**Claude Agent SDK** and cannot. The SDK reports: "tool choice is not a parameter
of the Claude agent options. It doesn't exist [in] the agent SDK... [it] controls
tool permissions but does not expose the underlying tool choice flag." He even
checks whether it is a Python-vs-TypeScript gap (some features lag in Python) and
confirms it is not: the answer is that the Agent SDK wraps the Claude CLI and
simply does not surface `tool_choice`. **So: `tool_choice` is Anthropic (low-level)
SDK only.** When you need it, drop to the lower-level SDK.

## Part 4: The force-`tool` infinite loop (the real trap)

This is the part the exam skill names explicitly, and it is worth slowing down for
because it ties directly to Module 1's `stop_reason` lesson.

Andrew forces the tool (`tool_choice: {"type": "tool", ...}`), wraps the call in a
`while True:` loop, and it runs forever. "For whatever reason it's looping... it
clearly doesn't have a way to stop." He digs in and finds the mechanism:

> "The bug forces a tool call in every API request... after that tool runs, the
> results are appended in the loop and [it] continues, which forces another tool
> call." — Andrew

Here is why that is fatal. Remember from Module 1 that you end the loop when
`stop_reason == "end_turn"`. But when you force a tool (`tool` **or** `any`) on
*every* request, the model is *obligated* to emit a tool call, so `stop_reason` is
always `tool_use` and **never** `end_turn`. The exit condition can never fire.
Andrew's diagnosis lands with an audible "OH": the loop was set to keep forcing a
tool, and there was no `break`.

There are two independent fixes, and you generally want both:

1. **Do not force a tool on the turn where the model should be allowed to
   finish.** Switch from a fixed `tool` to `any` (or `auto`) so a later turn can
   come back with `end_turn`. As Andrew realises: "OH, AND THAT'S why we want to
   have any" — with `any`, "it actually comes back with an end turn."
2. **Add the missing `break`.** For one-shot structured extraction you do not need
   a loop at all — call once, read the tool input, stop. If you do loop, cap it
   (a `max_iterations` break, per Module 1's antipattern lesson) so a forced-tool
   configuration can never run away.

```python
# Illustrative — the SAFE one-shot pattern: no loop, no runaway.
resp = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=1024,
    tools=[triage_tool],
    tool_choice={"type": "tool", "name": "submit_triage"},
    messages=[{"role": "user", "content": raw_ticket}],
)
# Pull the structured payload straight off the tool-use block — done.
verdict = next(b.input for b in resp.content if b.type == "tool_use")
print(verdict)   # {"category": "billing", "priority": "high", "reason": "..."}
```

> ❌ **The trap:** forcing a specific `tool` inside a `while True:` loop. Every
> iteration is obligated to call the tool, so `stop_reason` is never `end_turn`
> and the loop never exits. Andrew watched it spin until he killed it.

> 🔑 **The rule:** `tool` and `any` **force** a tool call, so `stop_reason` stays
> `tool_use`. Only `auto` (or `none`) lets the model reach `end_turn`. If you
> force, you must provide your own exit — a single non-looping call, or a capped
> `break`.

## Part 5: Validation — because well-formed is not the same as correct

The schema makes the JSON *valid*. It does not make it *right*. The model can
still choose the wrong enum value or a nonsensical priority. This is where
**Pydantic** comes in — a "very popular" Python library where, as Andrew
describes, "you define data structure models... and then you can pass your data
into it and then it validates it, and if it doesn't match, then it can say, hey,
you need to go fix it, or fail early."

Pydantic does two useful things:

1. **Validate the returned payload.** Define the shape once as a class; feed
   Claude's JSON in; get a clear error if a field is missing or an enum value is
   out of range. That error can drive a retry (you will formalise this
   validation-retry loop in Module 6).
2. **Emit the schema.** Pydantic models "in the end... just going to output JSON
   Schema format," which "most if not all the frontier models understand." So you
   can generate your tool's `input_schema` from the same class you validate with —
   one source of truth. You can even inject that schema into the prompt (recall
   **few-shot prompting** from Lesson 5) to nudge better output before the tool is
   even called.

```python
# Illustrative — one definition, used to both DESCRIBE and VALIDATE the output.
from enum import Enum
from pydantic import BaseModel

class Category(str, Enum):
    billing = "billing"; technical = "technical"; account = "account"; other = "other"

class Priority(str, Enum):
    low = "low"; medium = "medium"; high = "high"; urgent = "urgent"

class Triage(BaseModel):
    category: Category
    priority: Priority
    reason: str

schema = Triage.model_json_schema()   # -> feed as the tool's input_schema
verdict = Triage.model_validate(claude_json)   # -> raises if invalid; catches semantic drift
```

Andrew is candid that he skips Pydantic in the lab only because "they're not
asking for it" on the (2025-dated) exam guide — "but in practice, you know, I
would absolutely be using Pydantic. This is not enough for me for structured JSON
output." Treat the raw schema as the exam-minimum and Pydantic as the
professional standard.

> 💡 **How would you ever know it is reliable?** Andrew's honest answer:
> "the only way you'd know that is if we did a batch processing and we ran it like
> a hundred times." A single green run proves it *can* work, not that it *always*
> will. You will do exactly this batch check in Module 6.

---

## Key takeaways

1. **Use a tool as a data mold.** Structured output means giving Claude a tool whose `input_schema` is the JSON shape you want; Claude reads the schema and fills it.
2. **Enums + required are the levers (EXAM).** Enums restrict *which values* are allowed; required restricts *which fields must appear*. Types alone do not make output clean.
3. **Know the four modes.** `auto` (may skip the tool), `any` (must use some tool), `tool` (must use this named tool), `none` (no tools). It is Anthropic-SDK-only — the Agent SDK does not expose it.
4. **Forcing a tool blocks `end_turn`.** With `tool` or `any`, `stop_reason` stays `tool_use` forever. Force only in a single non-looping call, or add a capped `break`.
5. **The value is `tool`, not `force`.** And `type: "tool"` needs a `name`. Verify against the API, not against slides or the exam guide.
6. **Validate beyond the schema.** Well-formed ≠ correct. Pydantic validates payloads and can emit the same schema you enforce — use it in practice.

## Common pitfalls

- ❌ **Wrapping a forced-`tool` call in `while True:`.** It can never return `end_turn`, so it loops forever. Use a single call, switch to `any`/`auto` for the finishing turn, and always cap iterations.
- ❌ **Using `auto` when you need guaranteed JSON.** `auto` may return plain prose and break your parser. Force the tool for one-shot extraction.
- ❌ **Reaching for `tool_choice` in the Claude Agent SDK.** It is not there. Drop to the low-level Anthropic SDK.
- ❌ **Writing `"force"` as the mode, or `{"type":"tool"}` with no `name`.** The API rejects both. Valid modes are `auto`, `any`, `tool`, `none`; `tool` needs a `name`.
- ❌ **Typing a category as a plain string.** Without an enum you will get values your code has no branch for. Constrain it.
- ❌ **Trusting one successful run.** Well-formed output on one ticket is not proof; batch-test before you trust it in production.

---

## 🛠️ Capstone Project: the Atlas Support triage classifier

> This is the main hands-on project for the lesson. You will feel the moment prose
> becomes data: a messy human ticket goes in, and a strict JSON verdict your code
> can route on comes out. Keep it small on purpose.

### What you will build

A single Python script that takes a raw, unstructured support ticket (one big blob
of text) and forces Claude to return a strict JSON **triage verdict** — a
`category` from a fixed list, a `priority` from a fixed list, and a short `reason`
— then validates that verdict in code. This is the first component of **Atlas
Support** that produces machine-readable output; every later module (routing,
escalation, batch) will consume verdicts shaped exactly like this.

Its pieces, each mapped to a lesson idea:

- A `submit_triage` **tool** whose `input_schema` is the verdict shape (Part 1).
- **Enums** on `category` and `priority`, plus a **required** list (Part 2).
- A **forced** `tool_choice` call, single-shot, no loop (Parts 3–4).
- A **validation** step that rejects a bad verdict (Part 5).

### Why this is the perfect practice

| Lesson idea | Where you use it in the triage classifier |
|---|---|
| Tool as a data mold | The `submit_triage` `input_schema` defines the verdict |
| Enums + required | `category`/`priority` enums; `required: [category, priority, reason]` |
| `tool_choice` modes | Force `{"type":"tool","name":"submit_triage"}` |
| Force-`tool` infinite loop | Single call (no `while True:`), then observe the loop if you add one |
| Validation | Check enum membership and required fields; optionally Pydantic |

### Milestones (build them in order, each one works on its own)

1. **Define the tool schema.** Write `submit_triage` with an `input_schema`: `category` (enum: `billing`, `technical`, `account`, `other`), `priority` (enum: `low`, `medium`, `high`, `urgent`), `reason` (string), and `required: ["category", "priority", "reason"]`. Print the schema to confirm it is valid JSON.
2. **Force one clean call.** Send a raw ticket with `tool_choice={"type":"tool","name":"submit_triage"}`, `model="claude-haiku-4-5"`, no loop. Read the verdict off the `tool_use` block's `.input` and print it. Smallest win: one ticket in, one JSON object out.
3. **Print what was passed to the tool.** Add a line that shows the exact payload Claude generated (Andrew's `print` trick). This is your window into *why* a field is ever missing.
4. **Validate the verdict.** In plain Python, assert `category` and `priority` are in their allowed sets and all required keys are present; raise a clear error otherwise. Confirm a hand-edited bad value gets rejected.
5. **Tour the modes.** Run the same ticket under `tool` and `any` and note that both force a tool call; switch to `auto` and observe it *can* return plain text (breaking your parser). Write one sentence on why `auto` is unsafe here.
6. **Reproduce and fix the infinite loop.** Deliberately wrap the forced call in `while True:` with the results appended each pass; watch it never reach `end_turn`; then fix it two ways — switch to `any` so a turn can end, and add a `max_iterations` `break`.
7. **Stretch goals.** (a) Redefine the schema with **Pydantic** and validate with `model_validate`, generating the tool schema from `model_json_schema()`. (b) Run 20–100 tickets and count how often the verdict is well-formed *and* sensible — your first taste of the batch reliability check from Module 6.

### How you will know you are done

- ✅ A single forced call returns a JSON object with exactly `category`, `priority`, `reason` — no prose, no loop.
- ✅ Both `category` and `priority` are always one of your declared enum values.
- ✅ Your validator rejects a verdict with a missing field or an out-of-enum value.
- ✅ You can explain, in one sentence each, why `tool`/`any` never hit `end_turn` and why `auto` is unsafe for guaranteed output.
- ✅ Your loop version cannot run away — it either does one call or breaks after a capped number of iterations.

> 💡 **Keep yourself honest:** a green run on one ticket proves the pipeline
> *can* work, not that it *always* will. As Andrew says, the only way to trust it
> is to "run it like a hundred times" — note that as the Module 6 follow-up rather
> than declaring victory now.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice on
> one idea. Optional and independent; the Capstone already touches all of them, so
> feel free to skip straight to it.

### Exercise 1: Enum swap (foundational)
Take the `submit_triage` tool and remove the `enum` from `category`, leaving it a
plain string. Run five varied tickets and record the category strings you get
back. Then restore the enum and rerun. Write down what changed — this is the enum
lesson in one experiment.

### Exercise 2: Break the required contract (intermediate)
Drop `reason` from the `required` list and rerun a few ambiguous tickets. Note
whether Claude sometimes omits it. Then add it back and confirm it always appears.
You are proving that `required` is doing real work.

### Exercise 3: Validation-retry stub (advanced)
Wrap the call so that if validation fails (missing field or bad enum), you re-send
the ticket *with the error message appended to the prompt* ("your last output was
invalid because ...") — capped at three attempts. This is a preview of the
validation-retry loop you will build properly in Module 6.

---

## Cheat sheet

```text
STRUCTURED OUTPUT = give Claude a TOOL whose input_schema is the JSON you want.
  Claude reads the schema (it's JSON Schema) and generates output to fit it.

JSON SCHEMA PIECES
  type: string | integer | number | boolean
  array  -> {"type":"array","items":{...}}
  object -> {"type":"object","properties":{...}}
  enum   -> fixed set of allowed VALUES         <-- lever 1 (EXAM)
  required -> list of fields that MUST appear   <-- lever 2 (EXAM)
  (schema stops SYNTAX errors, not SEMANTIC errors)

tool_choice  (ANTHROPIC low-level SDK ONLY — not in the Agent SDK)
  auto  -> may use a tool OR return text        (unsafe for guaranteed JSON)
  any   -> must use SOME tool; Claude picks      (forces a tool call)
  tool  -> must use THIS tool: {"type":"tool","name":"..."}   (forces it)
  none  -> no tools; text only
  NOTE: the value is "tool", NOT "force". type:"tool" REQUIRES a name.

THE INFINITE-LOOP TRAP
  Forcing a tool (tool OR any) => stop_reason stays "tool_use", never "end_turn".
  while True + forced tool + no break  ==> loops forever.
  FIX 1: don't loop — one call, read tool_use .input, done.
  FIX 2: use "any"/"auto" so a turn can end + always cap with a break.

VALIDATE beyond the schema  ->  Pydantic
  model_json_schema()  -> emit the tool's input_schema (one source of truth)
  model_validate(json) -> catch missing/out-of-enum fields; drive a retry
  Reliability proof = run it in BATCH (100x), not one green run.
```

## How this connects to the rest of the course

- **Earlier, Module 1 · Lessons 3–4 (the stop-reason loop):** you learned to end the loop on `end_turn` and cap runaways. That is *exactly* why forcing a tool loops forever — `stop_reason` never reaches `end_turn`. This lesson is that rule biting in practice.
- **Earlier, Module 2 · Lesson 5 (prompting that steers):** few-shot and specific prompts. Injecting a Pydantic-emitted schema into the prompt is few-shot applied to structured output.
- **Next, Module 3 (Code-driven vs model-driven decisions):** a clean JSON verdict is what lets *code* make deterministic routing decisions instead of the model — the whole reason you forced structure here.
- **Later, Module 6 (Reliability):** you will feed schema-validation errors back for capped retries and batch-run the classifier to measure how often it is actually right — the honesty check this lesson keeps pointing at.

---

*Source: the CCA-F course by Andrew Brown (ExamPro). Code snippets and diagrams are
illustrative reconstructions of the patterns described in the course. Adapt them to
the current SDK.*
