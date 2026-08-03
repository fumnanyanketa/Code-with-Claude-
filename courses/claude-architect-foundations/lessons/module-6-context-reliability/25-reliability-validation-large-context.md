# Module 6 · Lesson 25: Reliability II — validation retries and large context

> **Course:** Claude Certified Architect: Foundations, a self-paced course
> **Module 6:** Context management & reliability: keep an agent correct and stable as work gets big
> **Speaker:** Andrew Brown, ExamPro
> **Source:** Reconstructed from the CCA-F course by Andrew Brown (ExamPro) · [full transcript](../../transcripts/cca-f-full-course.txt)
> **Estimated time:** 45 to 60 minutes (read plus lab)

---

## In one sentence

When a model's structured output fails a check, you do not throw it away — you **feed the specific errors back into the loop and let it retry, up to a hard cap**; and when a job gets too big for the context window, you stop cramming everything in and instead keep a **findings file as external memory**, **filter bulky tool output down to what matters**, and run a **crash-recoverable explorer** whose progress lives in a resumable manifest.

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone
> Project** where you make Atlas Support survive a large job: it writes findings
> to external memory, filters a huge tool result down to a few fields, and
> resumes cleanly after a simulated crash. Everything before the Capstone teaches
> the two skills you will use there — validation-retry loops and the large-context
> fixes. If you want to see the finish line first, jump to the **"Capstone
> Project"** section, then come back.

## First-principles companion

> 💡 **The durable ideas behind this lesson.** The tools are new; the problems
> are not.
>
> - **[Lost in the Middle: How Language Models Use Long Contexts](https://arxiv.org/abs/2307.03172)**
>   (Liu et al., 2023). The paper that named the effect Andrew describes: models
>   attend well to the *start* and *end* of a long input and reliably miss what
>   sits in the *middle*. It is why "just make the context bigger" is not a fix.
> - **[JSON Schema](https://json-schema.org/)** — the timeless account of what a
>   "valid" object *is* (types, enums, required fields). A validation-retry loop
>   is just: check the object against a contract, and if it breaks the contract,
>   hand the breakage back in words the model can act on.

## A few plain-language basics first

This lesson leans on terms from earlier lessons and adds a few new ones. In plain words:

- **Token:** the unit a model reads and writes in, about ¾ of a word; you are billed per token, and the context window is measured in them.
- **Context window:** how much text (in tokens) the model can hold in mind at once. When a job needs more than fits, something has to give.
- **Structured output:** making the model return machine-readable data (usually JSON) by giving it a tool with a JSON input schema — types, enums, required fields.
- **Agentic loop:** the repeating cycle an agent runs — call the model, run any tool it asks for, feed the result back — until it is done. You drive it off `stop_reason`, never off parsing the text.
- **Schema (syntax) error:** the returned object is the wrong *shape* — a missing required field, a number where a string belongs, a value not in the enum. Tool schemas catch most of these for you.
- **Validation (semantic) error:** the object has the right shape but the *data is wrong* — a tag that should be snake_case isn't, a total that doesn't add up, a field that violates a business rule. The schema can't catch these; you write the check.
- **External memory:** important facts written to a file *outside* the conversation, then re-injected into the prompt each turn, so they survive summarization and never rot.
- **Manifest:** a small state file (JSON) that records what work exists and the status of each piece (`pending`, `running`, `done`, `failed`) — so a job can be resumed after a crash.
- **Sub-agent:** an agent spawned by another agent, with its own isolated context. It does the noisy work so the parent's context stays clean.

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

Last lesson (Reliability I) you learned to keep a *human* in the loop — confidence gates, review, synthesis. This lesson keeps the *machine* honest under two everyday stresses: bad output and big jobs. Both are guaranteed to happen. Models return data that fails your rules, and real tasks — reading a 50-page document, exploring a large codebase — overflow the context window. As Andrew puts it, when structured JSON "comes back with either syntax errors or there's just something absolutely wrong... we want to have a way for it to correct." And on scale: once the context "gets too large... it forgets things on the tail end or when it summarizes it, it loses key information." The fixes are cheap, mechanical, and turn a fragile demo into something that survives a real workload. This is exactly what Atlas Support needs before it can run at scale in the next module.

## Learning objectives

By the end of this lesson you will be able to:

1. Build a validation-retry loop that appends specific errors back into the conversation and retries with a hard attempt cap.
2. Tell a schema (syntax) error from a validation (semantic) error, and decide which retries are even worth attempting.
3. Name the four large-context failure modes — progressive-summarization loss, lost-in-the-middle, bulky tool output, and history compaction — and the fix for each.
4. Use a findings file as external memory: extract key facts, store them outside the conversation, and re-inject them each turn.
5. Filter a large tool result down to the few fields the model actually needs.
6. Design a crash-recoverable explorer: a coordinator, an isolated sub-agent, and a resumable manifest that lets the job pick up where it left off.

## Prerequisites

- **Module 4 (Structured output & tool schemas)** — a validation-retry loop starts from structured output, so you need a tool with a JSON schema.
- **Module 1 · Lessons 3–4 (the stop-reason loop and its max-iteration cap)** — retry-with-a-cap and the explorer loop are both that same capped loop.
- **Module 3 · Lesson 8 (hub-and-spoke coordinator)** and sub-agents — the explorer is a coordinator delegating to an isolated sub-agent.
- **Reliability I** (previous lesson) — this continues the reliability theme.
- Python, an Anthropic API key, and Claude Code installed (the codebase-explorer lab uses it).

---

## Part 1: Validation-retry loops (remediate, don't discard)

You already make the model return structured JSON by giving it a tool with a schema. The schema handles *shape*. But two things still go wrong: the object can come back malformed, or — more often — it comes back well-formed but **the data is wrong**. Andrew's word for the fix is one he thinks the course *should* have used: **remediate**.

The move is simple and worth memorising: **when output fails a check, append the specific errors back into the conversation and let the model try again — up to a cap.**

```text
                 ┌─────────────────────────────┐
                 ▼                             │
   call model → get structured output          │  (retry, attempt++ )
                 │                             │
                 ▼                             │
   run your validation checks                  │
                 │                             │
        pass? ───┴─── fail? → append the exact │
         │                    error strings ───┘
         ▼                    ("Tags must use snake_case")
       done                          │
                                     ▼
                       attempts >= MAX_ATTEMPTS? → give up, quit out
```

Andrew builds this on the triage example from the structured-output section. The validator runs "four business rule checks and return[s] specific error strings." On failure, "the tool result is returned and is `error: true`, pinpointed to the error," and the loop **continues with no break** — it feeds the problem back in: *"validation failed, fix all the issues."* As he narrates the run: *"validation failed on attempt one — tags must use snake case. And then it's calling a second time, and now it passed."* One targeted error string, one retry, fixed.

> 🔑 **Remediate = check the output, and on failure hand the *specific* error
> back to the model as a tool result, then loop. Vague "that was wrong" teaches
> it nothing; "Tags must use snake_case" gets fixed on the next attempt.**

### Schema errors vs validation errors

Two different failures, and it is worth being able to name them:

| | Schema (syntax) error | Validation (semantic) error |
|---|---|---|
| What's wrong | The *shape* is wrong | The *data* is wrong |
| Example | Missing required field; number where a string goes; value not in the enum | Tag not snake_case; totals don't sum; a field breaks a business rule |
| Who catches it | Mostly **eliminated by tool use** — the schema enforces shape | **You** write the check; the schema can't see it |
| Andrew's words | "does it meet the JSON requirements" | "is the data actually correct?" |

Andrew's summary: *"validation errors is like the quality of the data that's coming through... [schema] errors is like does it meet the JSON requirements."* Tool schemas take a big bite out of the first column for free. The retry loop is mostly there for the second.

### Cap the retries — and know when not to retry at all

Two limits matter. First, **always cap the attempts.** The loop has "max attempts... it can try and it will quit out if it meets those." This is the same discipline as the loop's max-iteration cap from Module 1: even a self-correcting loop must be unable to run forever.

Second — and subtler — some failures are *never* worth retrying. Andrew flags it directly: retries are "infected when the required information is simply absent from the source document." If a ticket doesn't contain a phone number, no amount of retrying will conjure one. A mature loop can "make a use case where if you find that it's never going to meet the requirements, you should quit out" early instead of burning all its attempts on the impossible.

> ✅ **What to do about it:** append the *exact* validation error as the tool
> result, cap attempts (Andrew uses a small `max_attempts`), and — where you can
> tell — bail out early on failures that are unfixable rather than merely wrong.

> 💡 **A judgment note, in the course's spirit.** Andrew wonders aloud whether a
> library like Pydantic or Instructor could "take care of some of this." It can
> handle a lot of the *schema* side. But the semantic checks — your business
> rules — are yours to write, and the append-and-retry loop is the same shape no
> matter which library sits underneath. Learn the loop; swap the library later.

## Part 2: What goes wrong when context gets large

Structured retries fix *bad* output. The second half of reliability is *big* jobs. When "your context gets too large — you have too much information you're passing through the model," specific, predictable failures appear. Andrew names four.

**1. Progressive-summarization loss.** When a model condenses information over several steps, it doesn't know which details are load-bearing. "There's going to be information in there that's very important — like dates, percentages, numbers, or key information... as you summarize that information, it doesn't know that that's important, and it's going to literally make it generic. And you're going to lose that information." Each summary of a summary sands off the precise facts.

**2. Lost-in-the-middle.** Give a model a lot of data — "let's say 50 pages" — and "it's going to look at the first few pages and the last, and it's going to miss the middle information. This is just how the model works." (This is the Liu et al. effect from the companion above.) A bigger context window does not save you; the *middle* is where attention thins out.

**3. Bulky tool output.** External tools and APIs "often return back data, usually JSON, but you might not need all that JSON data — maybe just the order number or key information." Andrew's example is a flight-search MCP tool (Tavily / a travel API) that "returns a lot of information. You're not going to want to ingest all that." Every unfiltered token of tool output is context you're spending — and noise the model has to see past.

**4. History compaction.** This one you've already lived through without noticing. In a long chat — Claude Code, ChatGPT — "you can have a conversation that goes on forever. What's happening behind the scenes is that they're summarizing the information." An agent "needs the whole conversation history" to act, and "each time you prompt it, you're feeding back... all the things you said. But at some point you're going to run out of memory," so parts get summarized — which quietly reintroduces failure mode #1.

```text
LARGE-CONTEXT FAILURE MODES → FIX
  1. Progressive-summarization loss  → extract key facts to EXTERNAL MEMORY,
                                        re-inject them verbatim each turn
  2. Lost-in-the-middle              → process in SECTIONS/CHUNKS; put the
                                        most important info at start or end
  3. Bulky tool output               → FILTER the result to the few fields
                                        you need (optionally via a small agent)
  4. History compaction              → same fix as #1: keep facts outside the
                                        conversation so summarizing can't lose them
```

> 🔑 **The root cause is one thing wearing four hats: important, precise
> information gets diluted or dropped as context grows. Every fix below is a way
> to keep the precise facts *out of harm's way* — outside the conversation, or
> trimmed before they ever enter it.**

## Part 3: The three fixes

Andrew skips chunking in the lab ("chunking sections seems pretty easy") and builds the three fixes that carry the most weight: external memory, tool-output filtering, and a crash-recoverable explorer.

### Fix 1 — External memory (a findings file / case facts)

The solution to summarization loss is to *not rely on the conversation to remember*. "Extract that information out, store it somewhere, and then always inject it back into the next prompt... the exact information, so it knows what is the most important information and we're not losing that out."

In the text-adventure lab this is a **case-facts file**. Key player facts are saved to disk (`save_case_facts`), then "loaded into context every time" through the system prompt: *"You are a narrator of a text adventure game. Here's the case facts..."* The facts live in a file, not in the drifting chat history, so summarization can't touch them. That is the whole idea of external memory: the conversation can compact freely, because the facts that matter are re-read from a file each turn.

### Fix 2 — Filter big tool output

When a tool returns a wall of JSON, don't hand the model the wall. Return only the fields it needs. In the same lab, a `get_world_state` tool returns "the full world state simulating a bloated API response" — thousands of tokens of "irrelevant bulk data." The fix: "filter the massive world state down to only what's needed. So instead of injecting thousands of tokens, we'll inject 50 tokens of the fact." Concretely, the tool "individually select[s] that data and returns it back to the model" — just the current room, not the whole world.

You do **not** need an LLM to filter — often plain code selecting fields is enough. But when the trimming needs judgment, "you can make an additional step to a smaller agent or model to do that, to reduce the amount of information. You're not going to want to pass back the entire API request."

> ✅ **What to do about it:** treat every tool result as untrusted *volume*. Trim
> it to the handful of fields the model needs before it ever hits the context —
> in code where you can, with a small helper model where you must.

### Fix 3 — A crash-recoverable explorer (the Doom lab)

The biggest fix combines everything, on a real problem: exploring a large codebase (Andrew clones the **Doom** source) to answer questions like *"how does a player take damage?"* A large codebase overwhelms context — as it ingests more, "it forgets things on the tail end, or when it summarizes it, it loses key information." Four design choices solve it:

1. **External memory as a findings file.** Key discoveries are appended to a `findings.md` (Andrew ends up making it a `findings/` folder of scratchpad artifacts). The coordinator "can continuously reference that information" instead of holding it all in context.

2. **A sub-agent absorbs the noise.** If the main agent (the coordinator / Claude Code runtime) reads all the raw source itself, "there's a lot of busy information that's going to eat up the coordinator's context, and it's not going to be able to coordinate effectively. So we need a sub-agent that can handle the noise." The coordinator "never performs raw code exploration itself — keep context clean." Verified afterward: *"parent context state clean, zero Doom-source reads in the conversation. All explorations happened inside the isolated sub-agents."*

3. **A resumable manifest for crash recovery.** "For whatever reason our computer shuts down, or there's an error, or we run out of credits, and we want to pick up where we last left off" — so task state lives in a `manifest.json`. Each task carries a status; a `resume_from` field lets a sub-agent continue an interrupted task by *appending* to its scratchpad. Because scratchpads are "append only by convention... partial work will survive." The acceptance test says it plainly: *"killing and restarting the parent mid-task resumes without losing findings."*

4. **A synthesizer + a skill to invoke it.** A second sub-agent, the **synthesizer**, "merges per-task scratchpads into one coherent answer" — the "report a human actually reads," versus the raw per-task files. And the whole coordinator is wired to fire via a **skill** (invoked by its description) plus a light pointer in `CLAUDE.md`, rather than a fat procedure pasted into the config.

```text
DOOM EXPLORER — the shape of a crash-recoverable, context-safe job

   ┌──────────────┐   reads/writes    ┌──────────────┐
   │ COORDINATOR  │◄─────────────────►│ manifest.json│  task status:
   │ (stays clean)│                   │ (resumable)  │  pending/running/
   └──────┬───────┘                   └──────────────┘  done/failed + resume_from
          │ dispatch one question
          ▼
   ┌──────────────┐   append only     ┌──────────────┐
   │  EXPLORER    │──────────────────►│  findings/   │  external memory:
   │ (sub-agent,  │   never rewrites   │  scratchpads │  survives crashes &
   │  reads Doom) │                   └──────┬───────┘  summarization
   └──────────────┘                          │
                                             ▼
                                    ┌──────────────┐
                                    │ SYNTHESIZER  │→ one narrative answer
                                    │ (never reads │   (the human-readable report)
                                    │  Doom source)│
                                    └──────────────┘
   Coordinator NEVER reads raw source. Explorer NEVER edits code.
   Synthesizer NEVER reads source — only merges scratchpads.
```

Notice how the earlier lessons stack here: the coordinator is the hub-and-spoke pattern (Module 3), the isolation keeps context clean (this module), and the manifest is just a capped, resumable version of the agentic loop's state.

> 💡 **A real gotcha Andrew hit — verify, don't trust.** Claude Code "didn't
> register our project-level agent definitions as sub-agent types; only built-in
> agent types are exposed." The runtime worked around it by invoking the
> general-purpose agent under the Doom Explorer contract. The lesson the course
> repeats: the docs and even the tool's own behaviour surprise you — you find the
> truth by running it and reading the output, not by trusting the setup worked.

---

## Key takeaways

1. **Remediate, don't discard.** On a failed check, append the *specific* error as a tool result and retry — the model fixes a precise complaint ("tags must be snake_case") in one more turn.
2. **Two error kinds.** Schema/syntax errors (wrong shape) are mostly eliminated by tool use; validation/semantic errors (wrong data) are yours to check with business rules.
3. **Cap the retries, and skip the impossible.** Always bound attempts, and bail early on failures that can't be fixed (required info absent from the source) instead of wasting the budget.
4. **Four large-context failures, one cause.** Progressive-summarization loss, lost-in-the-middle, bulky tool output, and history compaction all dilute precise information as context grows.
5. **External memory beats a bigger window.** Extract key facts to a file and re-inject them each turn; the conversation can compact freely without losing them.
6. **Filter tool output at the door.** Return only the fields the model needs — in code where you can, via a small helper model where judgment is required.
7. **Design for the crash.** A coordinator + isolated sub-agent + resumable manifest + append-only findings means killing the job mid-task loses nothing.

## Common pitfalls

- ❌ **Handing back a vague error.** "That was wrong" teaches the model nothing. Return the exact, pinpointed string it can act on.
- ❌ **A retry loop with no cap.** Self-correction that can loop forever is just a slower runaway. Bound `max_attempts` every time.
- ❌ **Retrying the unfixable.** If the source doesn't contain the data, retrying can't invent it — detect that case and quit out.
- ❌ **Assuming a bigger context window fixes recall.** It doesn't; the middle still gets lost. Keep precise facts in external memory and process in sections.
- ❌ **Dumping raw tool JSON into context.** Every unfiltered token is spend *and* noise. Trim before it enters.
- ❌ **Letting the coordinator read the raw source itself.** That pollutes the very context it needs to coordinate. Isolate exploration in a sub-agent.
- ❌ **Rewriting scratchpads instead of appending.** Append-only is what makes a job resumable after a crash. Overwriting throws away partial work.
- ❌ **Trusting "done."** Claude Code silently didn't expose the project sub-agent types. Read the manifest and the findings yourself.

---

## 🛠️ Capstone Project: make Atlas Support survive a large job

> This is the main hands-on project for the lesson. You will feel the difference
> between an agent that falls over on a big input and one that keeps precise
> facts safe, trims what it ingests, and survives being killed mid-run. Keep it
> small on purpose — one findings file, one filtered tool, one simulated crash.

Atlas Support is about to run at scale (next module is batch processing). Before it can, it needs to survive a *large* job without silently losing facts or dying halfway. In this capstone you give it that survivability: a validation-retry loop for correctness, external memory for durability, tool-output filtering for cost, and a resumable manifest for crash recovery.

### What you will build

A small Atlas Support "large-job" runner that ingests a big ticket bundle (or a bulky external API result), extracts the facts that matter, and answers a question about it — surviving a mid-run crash. Its pieces map straight to the lesson:

- **A validation-retry loop** — the triage tool's output is checked against business rules; on failure the exact error is fed back and retried with a cap. *(Part 1)*
- **A findings/case-facts file** — key facts (ticket IDs, customer tier, SLA deadlines) extracted to disk and re-injected each turn. *(Part 3, Fix 1)*
- **A filtered tool** — a `get_ticket_bundle` tool that returns a huge JSON blob, trimmed to the few fields the model needs. *(Part 3, Fix 2)*
- **A manifest + resume** — task status in `manifest.json`, so a killed run picks up where it left off. *(Part 3, Fix 3)*

### Why this is the perfect practice

| Lesson idea | Where you use it in the runner |
|---|---|
| Remediate (append error, retry, cap) | Triage output fails a snake_case tag rule → error string fed back → passes on attempt two |
| Schema vs validation error | Tool schema catches the missing field; your check catches the malformed tag |
| External memory | Case facts written to `findings.md`, re-injected in the system prompt each turn |
| Tool-output filtering | `get_ticket_bundle` returns 3,000 tokens; you inject ~50 |
| Resumable manifest | Kill the process mid-run; restart resumes from the manifest without losing findings |
| Verify, don't trust | You read the manifest and findings file yourself to confirm resume worked |

### Milestones (build them in order, each one works on its own)

1. **A validation-retry loop.** Take your Module 4 structured triage tool. Add a validator that runs a few business-rule checks and returns specific error strings (e.g. *"Tags must use snake_case"*, *"priority must be one of low/medium/high"*). On failure, append that string as the tool result and loop; on pass, break. Cap it with `max_attempts` (start with 3). Run it against an input you know is malformed and watch it fail on attempt one, then pass on attempt two. This alone is a complete, testable unit.
2. **Add the early bail-out.** Extend the loop so that if a required fact is *absent* from the source (not just wrong), it stops and reports "unfixable — missing data" instead of burning all its attempts. Prove it by feeding a ticket with no order number when the schema needs one.
3. **External memory (case facts).** Write a `findings.md` (or `case_facts.json`). Have the runner extract key facts — ticket IDs, customer tier, SLA deadline — and `save` them to that file, then load them back into the system prompt each turn: *"Here are the case facts: ..."*. Confirm the facts appear verbatim in the prompt on every iteration, not paraphrased.
4. **Filter a bulky tool.** Write a `get_ticket_bundle` tool that returns a deliberately huge JSON blob (simulate a bloated API response — pad it to a few thousand tokens). Then filter it: return only the current ticket's key fields. Count tokens before and after; confirm you're injecting tens of tokens, not thousands.
5. **A manifest.** Create `manifest.json` listing each ticket to process with a status (`pending`/`running`/`done`/`failed`). As the runner processes each ticket, update its row. After a full clean run, confirm every row is `done`.
6. **Simulate a crash and resume.** Kill the runner mid-job (Ctrl-C after two of five tickets, or `sys.exit()` on ticket three). Restart it. It should read the manifest, skip the `done` rows, and continue from the first non-done one — appending to `findings.md`, never rewriting it. Verify by reading the manifest and findings file yourself: no ticket processed twice, no findings lost. *"Killing and restarting the parent mid-task resumes without losing findings."*
7. **Stretch goals.** (a) Split exploration into an **isolated sub-agent** so the coordinator never ingests the raw bundle, and confirm the coordinator's context stays clean. (b) Add a **synthesizer** pass that merges per-ticket findings into one summary report. (c) Wire the coordinator to fire from a **skill** plus a one-line pointer in `CLAUDE.md`, instead of a fat pasted procedure. (d) Route the tool-filtering through a small/cheap model when the trimming needs judgment.

### How you will know you are done

- ✅ The retry loop feeds back a *specific* error and fixes it within the cap; you have watched it fail then pass.
- ✅ Unfixable inputs bail out early instead of exhausting `max_attempts`.
- ✅ Case facts appear verbatim in the prompt every turn, read from an external file.
- ✅ The filtered tool injects a small fraction of the raw blob — you have counted the tokens.
- ✅ After a mid-run kill, a restart resumes from the manifest: no ticket done twice, no findings lost — and you confirmed it by reading the files, not by trusting the log.

> 💡 **Keep yourself honest:** the proof of crash recovery is not that the program
> printed "resumed." It is that you opened `manifest.json` and `findings.md` after
> the restart and saw exactly the right state. Read the files.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice
> on one idea. Optional and independent; the Capstone already touches all of
> them, so feel free to skip straight to it.

### Exercise 1: Classify the error (foundational)
Take ten things that could be wrong with a triage output. For each, label it **schema/syntax** (wrong shape — caught by the tool schema) or **validation/semantic** (wrong data — you must check). Then, for the semantic ones, write the exact error string you'd feed back.

### Exercise 2: Trim the blob (intermediate)
Grab any real bulky JSON (a weather API, a flight search, a GitHub API response). Write a plain-code filter that returns only the three fields an agent would need. Count tokens before and after. Now write one sentence on when you'd reach for a small helper model instead of plain code.

### Exercise 3: Break it, then survive it (advanced)
Take your Capstone runner. Inject a crash on a random ticket each run (`if random.random() < 0.3: sys.exit()`). Run it repeatedly until the whole job completes across several restarts. Confirm from the manifest and findings file that the final result is identical to an uninterrupted run — same tickets, same facts, none duplicated.

---

## Cheat sheet

```text
RELIABILITY II — VALIDATION RETRIES & LARGE CONTEXT — one-page recap

VALIDATION-RETRY LOOP (remediate)
  call model -> get structured output
  run YOUR checks -> pass? done
                  -> fail? append the EXACT error as tool_result, loop
  ALWAYS cap attempts (max_attempts).
  BAIL EARLY on unfixable failures (required data absent from source).

  SCHEMA (syntax) error  = wrong shape  -> mostly killed by tool use
  VALIDATION (semantic)  = wrong data   -> you write the check
    "does it meet JSON requirements" vs "is the data actually correct?"

LARGE-CONTEXT FAILURES -> FIX
  1. progressive-summarization loss -> EXTERNAL MEMORY (findings file),
                                       re-inject facts verbatim each turn
  2. lost-in-the-middle             -> chunk/sections; important info at
                                       start or end (bigger window won't help)
  3. bulky tool output              -> FILTER to needed fields (code, or a
                                       small helper model)
  4. history compaction             -> same as #1: keep facts outside the chat

CRASH-RECOVERABLE EXPLORER (the Doom pattern)
  COORDINATOR   stays clean; never reads raw source
  SUB-AGENT     isolated; absorbs the noise; APPEND-ONLY findings
  MANIFEST.json task status + resume_from  -> kill & restart loses nothing
  SYNTHESIZER   merges scratchpads -> the one report a human reads
  wire it via a SKILL (+ light CLAUDE.md pointer), not a pasted procedure

THE RULE
  "Just because it said it did, it does not mean it did."
  Read the manifest and findings files. Don't trust "resumed."
```

## How this connects to the rest of the course

- **Earlier, Module 4 (structured output & tool schemas):** the schema that gives you shape for free is where the validation-retry loop starts; you added the semantic checks on top.
- **Earlier, Module 1 · Lessons 3–4 (the capped stop-reason loop):** both the retry cap and the resumable manifest are that same "loop, but it can't run forever" discipline.
- **Earlier, Module 3 · Lesson 8 (hub-and-spoke) and sub-agents:** the crash-recoverable explorer *is* a coordinator delegating to an isolated sub-agent — you just added external memory and a resumable manifest.
- **Previous, Reliability I:** kept a human in the loop (confidence, review, synthesis); this kept the machine honest under bad output and big jobs. Together they are Module 6's reliability core.
- **Next, Batch processing for scale and cost:** now that a single large job survives, you make *many* jobs run cheaply and in bulk — the external-memory and filtering habits here are what keep batch runs affordable.

---

*Source: reconstructed from the CCA-F course by Andrew Brown (ExamPro). Code
snippets and diagrams are illustrative reconstructions of the patterns described
in the course. Adapt them to the current SDK.*
