# Module 6 · Lesson 26: Batch processing for scale and cost

> **Course:** Claude Certified Architect: Foundations, a self-paced course
> **Module 6:** Context management & reliability: keep long-running systems correct, affordable, and honest
> **Speaker:** Andrew Brown, ExamPro
> **Source:** Reconstructed from the CCA-F course by Andrew Brown (ExamPro) · [full transcript](../../transcripts/cca-f-full-course.txt)
> **Estimated time:** 30 to 45 minutes (read plus lab)

---

## In one sentence

When you have many prompts to run and you do not need the answers this second, the **Message Batches API** lets you submit them all at once — each tagged with your own `custom_id` — then poll for completion and match every result back to its request by that id, for roughly **half the cost** of running them one by one.

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone
> Project** where you batch-process a queue of Atlas Support tickets and
> reconcile the results back to each ticket by `custom_id`. Everything before the
> Capstone teaches the three moves — submit, check, retrieve — and the one rule
> that makes them reliable (key by id, never by order). If you want to see the
> finish line first, jump to the **"Capstone Project"** section, then come back.

## A few plain-language basics first

This lesson uses a few terms. In plain words:

- **Token:** the unit a model reads and writes in, about ¾ of a word; you are billed per token.
- **Synchronous (real-time) request:** you send one prompt and wait for the answer right then. Every earlier lesson worked this way.
- **Asynchronous (batch) request:** you hand over a pile of prompts, walk away, and collect the answers later. You are not waiting at the keyboard.
- **Batch:** one submitted job containing many requests, processed together in the background.
- **`custom_id`:** a label *you* attach to each request in the batch (for example `ticket-42`) so that when the answers come back — possibly in a different order — you can tell which answer belongs to which request.
- **Poll:** to check on something repeatedly ("is it done yet?") until it is ready, rather than being notified.
- **SLA (service-level agreement):** a promise about how fast something will finish. Batches have **no guaranteed SLA** — they usually finish quickly but may take up to 24 hours.
- **`tool_choice`:** the setting forcing how the model uses tools — `auto`, `any`, a specific `tool`, or `none`.
- **Structured output:** making the model return machine-readable data (usually JSON) by giving it a tool with a JSON input schema.

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

Every request so far has been synchronous: you ask, you wait, you get an answer. That is the right shape for a chat or an agent a person is watching. But a lot of real work is not like that — you have a thousand tickets to classify overnight, a backlog of documents to summarise, a dataset to label. Running those one at a time is slow and, worse, you pay full price for every token.

The Message Batches API is Andrew's answer, and he frames it plainly: "In this video, I just want to show you how batch processing works. And it's not that complicated." The payoff is money. As he puts it, "for the exam, I just want you to know that exists and you can save money with it," and after seeing it run: "if you don't need things right away, apparently *extremely extremely* good savings." That saving is the load-bearing exam fact of this lesson, and it is exactly 50%.

## Learning objectives

By the end of this lesson you will be able to:

1. Explain when to reach for batch processing instead of a synchronous call, and name the trade-off you are accepting.
2. State the cost saving of the Message Batches API (an **EXAM TIP**) and its timing guarantee.
3. Submit a batch of requests, each carrying a `custom_id`.
4. Poll a batch for completion and retrieve its results.
5. Reconcile results back to their requests by `custom_id` — and explain why you must never rely on order.

## Prerequisites

- **Module 1** — a working synchronous Claude call in Python and an Anthropic API key.
- **Module 2 · structured output** — you will reuse a tool with a JSON input schema to force clean, machine-readable answers.
- **Module 6 · Lesson 25 (Reliability II — validation retries and large context)** — batching is the next reliability-and-scale tool after retries.

---

## Part 1: Synchronous vs. batch — and the one thing you give up

A synchronous request is a phone call: you dial, someone picks up, you talk, you hang up with your answer. A batch is a mail-in form: you drop off a stack, and the results come back "later." The whole reason to use the mailbox is that it is cheaper — but you have to be willing to wait.

Andrew is honest about the wait up front. He does not even want to run the batch live at first: "I don't want to run this because uh batch processing isn't something that will happen instantly. I think it takes time for it to come back because yeah, it can take up to **24 hours to process with no guaranteed SLA**."

So the trade is simple and worth memorising:

| | Synchronous request | Batch request |
|---|---|---|
| **You wait** | Yes — answer comes back in seconds | No — collect it later |
| **Timing** | Immediate | Usually under an hour; **up to 24 hours**, no guaranteed SLA |
| **Cost** | Full price | **50% of full price** |
| **Good for** | Chat, agents, anything a human is watching | Overnight jobs, backlogs, bulk labelling |

> 🔑 **Batch = trade *latency* for *cost*. You give up "right now" and get back
> half-price. If a human is waiting on the answer, do not batch it.**

### Do not make the user wait at a spinner

There is a subtle design lesson buried in Andrew's build. His first version *submitted the batch and then blocked* — the program just sat there waiting for the batch to finish, which defeats the point. He catches it: "for batch processing the user has to wait. Is there a way we can uh make it so we can run it and then just check on it ourselves at another time... maybe you don't care and you just come back and you check, but like having to wait there would take forever."

That instinct is the whole ergonomic of batching, and it is why the finished tool has **three separate commands** — you will build exactly these in Part 3.

## Part 2: `custom_id` — the label that makes results usable

Here is the problem batching creates. You submit a hundred requests. The answers come back — but **not necessarily in the order you sent them**, and with no memory of which prompt was which. If you just line the answers up against your original list, you will silently pair ticket #12's answer with ticket #37's ticket. That is a data-corruption bug that no error message will warn you about.

The fix is a label you control. Andrew describes it precisely: "we have a **custom ID on each request** when submitting. And then when you call **batch results, every result comes back as a custom ID**." You name each request; the name rides along; you match on the name.

```text
SUBMIT                          RETRIEVE (order may differ!)
  custom_id="ticket-1"  ─┐        custom_id="ticket-3"  → result C
  custom_id="ticket-2"  ─┼──▶     custom_id="ticket-1"  → result A
  custom_id="ticket-3"  ─┘        custom_id="ticket-2"  → result B

  You reconcile by matching custom_id, NOT by position.
  results = {r.custom_id: r for r in batch_results}
```

> 🔑 **`custom_id` is the join key between what you sent and what you got back.
> Results arrive in any order — match on `custom_id`, never on position.**

### Force one clean answer per request

One more wrinkle that trips people up on the exam. Inside a batch you cannot have a back-and-forth with the model — Andrew again: "if I forget, you can't do interactive round trips. So instead of using tool use, uh, it's going to force a single tool call and the tool input is going to block. Okay? And then you just extract it directly."

In plain terms: a batch request should be *one shot*. If you are using a tool to get structured output (a JSON answer), set `tool_choice` to force that single tool call so the model must fill in your schema and stop — "instead, tool choice `any` forces a single tool call." Then you read the tool input straight out of the result. No loop, no round trips, one clean structured answer per `custom_id`.

> ✅ **What to do about it:** design each batch request to need exactly one
> response. Force the tool call (`tool_choice`) so every result is a single,
> parseable structured output you can pull out by `custom_id`.

## Part 3: The three moves — submit, check, retrieve

Andrew's finished tool lands on three commands, and they map one-to-one onto the API. This is the skeleton to remember.

```text
1. SUBMIT   client.messages.batches.create(requests=[...])
            -> fires the batch, returns a batch id
            -> save that id somewhere (Andrew writes it to a state file)

2. CHECK    client.messages.batches.retrieve(batch_id)
            -> read .processing_status; loop until it == "ended"
            -> this is just "hitting an API endpoint... using ID"

3. RETRIEVE client.messages.batches.results(batch_id)
            -> stream results, each carrying .custom_id and .result
            -> build {custom_id: result} and reconcile
```

Andrew narrates the split as he builds it: "we have submit, check, and run... So here it says submitted to the batch. **Fires the batch. Saves the batch ID to the batch state file**... And so now whenever we want to check it, we can just go and check it. And it's showing if it's succeeded or not... it's calling that **retrieve**... And so it is hitting an API endpoint and we're just using ID."

Why save the batch id to a file? Because the whole point is that you can close your program, come back tomorrow, and still know which batch to check on. The id is your claim ticket.

Here is the shape in code — an illustrative reconstruction; adapt names to the current SDK:

```python
# 1. SUBMIT — each request carries YOUR custom_id
batch = client.messages.batches.create(
    requests=[
        {"custom_id": f"ticket-{t['id']}",
         "params": {"model": "claude-opus-4-8", "max_tokens": 512,
                    "tools": [triage_tool], "tool_choice": {"type": "tool", "name": "triage"},
                    "messages": [{"role": "user", "content": t["body"]}]}}
        for t in tickets
    ]
)
save_batch_id(batch.id)          # your claim ticket — write it down

# 2. CHECK — poll until the batch has ended (come back whenever)
b = client.messages.batches.retrieve(load_batch_id())
if b.processing_status != "ended":
    print("still processing — check back later"); return

# 3. RETRIEVE — reconcile by custom_id, never by order
by_id = {}
for r in client.messages.batches.results(b.id):
    if r.result.type == "succeeded":
        by_id[r.custom_id] = r.result.message   # match on the label
# now by_id["ticket-42"] is exactly ticket 42's answer
```

Each result also carries a status — `succeeded`, `errored`, `expired`, or `canceled` — so you handle failures per item instead of losing the whole batch. Results stay available for 29 days after the batch is created, so "come back later" can be much later.

> 🔑 **Submit → check → retrieve. Save the batch id so "later" actually works,
> and reconcile the results by `custom_id`.**

---

## Key takeaways

1. **Batching trades latency for cost.** You give up "right now"; you get back half price.
2. **EXAM TIP — the Message Batches API costs 50% of standard pricing.** This is *the* fact to remember from this lesson. Timing: usually under an hour, up to 24 hours, **no guaranteed SLA**.
3. **Every request carries a `custom_id` you choose.** Results come back tagged with it.
4. **Results can arrive in any order — reconcile by `custom_id`, never by position.** Matching on order is a silent data-corruption bug.
5. **One shot per request.** No interactive round trips in a batch; force the single tool call so every answer is a clean, parseable structured output.
6. **Three commands: submit, check, retrieve.** Save the batch id so you can walk away and collect results later.

## Common pitfalls

- ❌ **Batching something a human is waiting on.** Batches can take up to 24 hours. If someone is staring at a spinner, use a synchronous call. Batch only work that can wait.
- ❌ **Matching results by list position.** They come back in any order. Zip them against your inputs and you will pair the wrong answer with the wrong request — with no error to warn you. Always key on `custom_id`.
- ❌ **Blocking your program until the batch finishes.** That throws away the whole benefit. Submit, save the id, and *check* later — Andrew's exact realisation.
- ❌ **Forgetting the batch id.** The id is how you find your results. Persist it (a file, a row in a table) the moment you submit.
- ❌ **Designing a multi-turn request.** No round trips inside a batch. Make each request self-contained and force the single tool call.
- ❌ **Assuming a speed guarantee.** There is no SLA. Plan for "up to 24 hours," even though most batches finish far sooner.

---

## 🛠️ Capstone Project: batch-triage Atlas Support's overnight ticket queue

> This is the main hands-on project for the lesson. You will feel the moment a
> pile of prompts becomes one cheap background job whose answers land back
> exactly where they belong. Keep it small on purpose — a handful of tickets is
> enough to prove the pattern.

Atlas Support — the multi-agent system you have built across this course — has a component that does not need to be instant: overnight triage. Tickets pile up while nobody is online; by morning, each should already be categorised and prioritised, ready for the escalation agent you will build next module. That is a perfect batch job: many items, no human waiting, cost that matters at volume.

### What you will build

A small script that takes a queue of support tickets, submits them as one half-price batch, checks on it, and reconciles each answer back to its ticket by `custom_id`. Its pieces map straight to the lesson:

- **A ticket queue** — a list of, say, 5–10 fake tickets, each with an id and a body. *(Part 2)*
- **A triage tool** — a JSON schema (`category`, `priority`, `one_line_summary`) forced with `tool_choice`, so each answer is clean structured output. *(Part 2)*
- **Submit** — one `batches.create` call, each request tagged `ticket-<id>`, batch id saved to a file. *(Part 3)*
- **Check** — a `retrieve` command that reports `processing_status` and stops if not `ended`. *(Part 3)*
- **Retrieve + reconcile** — build `{custom_id: result}` and print each ticket next to its triage. *(Parts 2–3)*

### Why this is the perfect practice

| Lesson idea | Where you use it in the triage job |
|---|---|
| Batch trades latency for cost | Overnight triage has no human waiting — the ideal batch candidate |
| `custom_id` is the join key | `ticket-<id>` ties each answer back to its ticket |
| Reconcile by id, not order | You build a dict keyed on `custom_id` and look tickets up in it |
| One shot per request | Forced `tool_choice` gives one parseable triage per ticket |
| Submit / check / retrieve | The three commands become your three script modes |

### Milestones (build them in order, each one works on its own)

1. **A synchronous triage of one ticket.** Before any batching, write a normal Claude call that triages a *single* ticket with your forced triage tool and prints the JSON. This proves your schema and `tool_choice` work. It is a complete, testable unit on its own.
2. **A queue and a submit command.** Make a list of 5–10 tickets. Build the `requests` list, tagging each with `custom_id="ticket-<id>"`, and call `batches.create`. Print and **save the batch id to a file**. Confirm the submit returns without waiting for answers.
3. **A check command.** Read the saved batch id, call `retrieve`, and print `processing_status`. Run it repeatedly; watch it move from `in_progress` to `ended`. This alone is your "come back later" tool.
4. **A retrieve-and-reconcile command.** Once the status is `ended`, stream `batches.results`, build `{custom_id: message}`, and print each ticket body next to its triage. **Verify** that `ticket-7`'s output really is ticket 7's — spot-check one by hand.
5. **Break the order on purpose.** Shuffle your results list before reconciling, then confirm the id-keyed lookup still pairs everything correctly. Now try (deliberately) matching by position instead and watch it mis-pair — feel the bug the `custom_id` prevents.
6. **Handle a failure.** Add one deliberately malformed request (or just branch on `r.result.type`). Confirm one `errored` item does not sink the rest — you still get triage for every ticket that succeeded.
7. **Stretch goals.** (a) Add prompt caching for a shared system prompt across all requests and note the extra saving. (b) Estimate the cost: multiply your token counts by full price, then halve it, to see the batch discount in dollars. (c) Wire the reconciled output into a file the Module 7 escalation agent could read.

### How you will know you are done

- ✅ Submitting returns a batch id immediately — your program does **not** hang waiting for answers.
- ✅ The batch id is written to a file, and a fresh run of your check command finds it.
- ✅ Every ticket's triage is matched to the correct ticket by `custom_id`, and you have verified one by hand.
- ✅ Shuffling the results changes nothing — the id-keyed lookup is order-independent.
- ✅ A single failed request does not lose the whole batch.

> 💡 **Keep yourself honest:** the danger in batching is the *silent* mis-pair.
> Do not trust that answer #3 is ticket #3 — prove it by reading the `custom_id`.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice
> on one idea. Optional and independent; the Capstone already touches all of
> them, so feel free to skip straight to it.

### Exercise 1: Say when to batch (foundational)
Write down five real jobs (e.g. "live chat reply," "label 50,000 reviews overnight," "summarise a document a user just uploaded"). For each, decide batch or synchronous and give the one-line reason (is a human waiting?). This drills the core trade.

### Exercise 2: The reconciliation dictionary (intermediate)
Given a list of results in scrambled order, write the three lines that turn them into a `{custom_id: result}` dictionary and look one up. Then write the *wrong* version (zip by position) and describe, in one sentence, the bug it produces.

### Exercise 3: Two-command tool (advanced)
Refactor a blocking "submit-and-wait" script into two separate commands — `submit` (saves the id and exits) and `check` (reads the id, reports status, retrieves if ended). Confirm you can quit the program entirely between the two.

---

## Cheat sheet

```text
BATCH PROCESSING — one-page recap

WHEN
  Many prompts + no human waiting -> BATCH.
  Human waiting -> synchronous.

THE TRADE
  Give up: "right now" (up to 24h, NO guaranteed SLA; usually < 1h)
  Get:     50% of standard cost        <-- EXAM TIP

THE THREE MOVES
  1. SUBMIT    batches.create(requests=[{custom_id, params}, ...])
               -> returns batch id ; SAVE IT (state file)
  2. CHECK     batches.retrieve(id) ; loop until processing_status == "ended"
  3. RETRIEVE  batches.results(id)  ; each result has .custom_id + .result

THE RULE
  Results arrive in ANY ORDER.
  Reconcile by custom_id, NEVER by position:
      by_id = {r.custom_id: r.result.message for r in results
               if r.result.type == "succeeded"}

ONE SHOT PER REQUEST
  No interactive round trips in a batch.
  Force the single tool call (tool_choice) -> one clean structured output.

PER-ITEM STATUS
  succeeded | errored | expired | canceled  -> one failure != whole batch lost
  Results available ~29 days after creation.
```

## How this connects to the rest of the course

- **Earlier, Module 2 (structured output):** the JSON-schema tool and `tool_choice` you used to force clean answers are exactly what makes each batch request a single, parseable result.
- **Earlier, Module 6 · Lesson 25 (Reliability II):** validation retries kept individual calls correct; batching is the next lever — running *many* calls correctly and cheaply.
- **Next, Module 7 (capstone — build a support agent with progressive escalation):** the triaged, `custom_id`-keyed tickets you produce here are exactly the queue a support agent draws from before deciding what to escalate to a human. This lesson is the cheap, scalable intake that feeds the course's final build.

---

*Source: reconstructed from the CCA-F course by Andrew Brown (ExamPro). Code
snippets and diagrams are illustrative reconstructions of the patterns described
in the course. Adapt them to the current SDK.*
