# Module 6 · Lesson 24: Reliability I — human review, confidence, and synthesis

> **Course:** Claude Certified Architect: Foundations, a self-paced course
> **Module 6:** Context management & reliability: keep long-running agents honest, focused, and checkable
> **Speaker:** Andrew Brown, ExamPro
> **Source:** Reconstructed from the CCA-F course by Andrew Brown (ExamPro) · [full transcript](../../transcripts/cca-f-full-course.txt)
> **Estimated time:** 45 to 60 minutes (read plus lab)

---

## In one sentence

Three techniques make an agent's output trustworthy instead of merely confident-sounding: attach a **confidence score** to every field and send only the shaky ones to a human (**stratified review**, so no category hides inside a good-looking average); when you **synthesise** several sources, carry each claim's **source** all the way through and flag where sources disagree; and let a **fresh-context reviewer** grade the work, because a model that just produced something is biased toward saying it did a great job.

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone
> Project** where you bolt three reliability layers onto Atlas Support's
> outputs: field-level confidence with a human-review queue, a synthesis step
> that preserves provenance, and an independent peer-review pass. Everything
> before the Capstone teaches those three techniques. If you want to see the
> finish line first, jump to the **"Capstone Project"** section, then come back.

## A few plain-language basics first

This lesson leans on a few earlier terms and adds some new ones. In plain words:

- **Agent:** an AI that takes a series of actions on its own toward a goal, rather than answering in one shot.
- **Sub-agent:** an agent spawned by another agent, usually with its own isolated context (its own separate "memory" of the conversation).
- **Structured output:** making the model return machine-readable data (usually JSON) rather than free prose.
- **Confidence score:** a number the model attaches to a piece of its own output saying how sure it is — e.g. "99% sure on the date, 40% sure on the total." It is the model's self-estimate, not a guarantee.
- **Calibration:** how well those self-estimates match reality. If everything the model marks "90% sure" is right about 90% of the time, it is *well calibrated*. The gap between claimed confidence and actual accuracy is the **calibration gap**.
- **Stratified sampling:** instead of spot-checking at random, you deliberately pull samples from *each* category (each document type, each field), so a weak category can't hide inside a strong overall average.
- **Provenance:** the record of *where a claim came from* — which source said it. Preserving provenance means every fact stays attached to its origin.
- **Claim–source mapping:** the concrete data structure that holds provenance: a list pairing each claim with the source it came from.
- **Synthesis:** combining findings from several sources into one coherent answer.
- **Scratchpad:** a small file a sub-agent writes its findings into, instead of dumping everything back into the conversation. The coordinator reads the scratchpad later.
- **Peer review (here):** having a *different* agent — one with no memory of writing the work — check it. The opposite is **self-review**, where the same agent grades its own output.
- **Human-in-the-loop:** a design where a person reviews or approves some of the agent's outputs before they count as final.

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

So far you have made Atlas Support *do* things. This lesson is about making its output *trustworthy*. Andrew opens the section bluntly: "when you work with data, how do you ensure that the data is actually accurate and a human's able to easily review it." That is the whole game once real people depend on your agent. A single headline number like "90% accurate" feels reassuring and is often a lie of omission — "when it's a single metric like this, it can be hiding information." And a model asked to grade its own work will happily tell you it nailed it. The three techniques here — confidence-driven human review, provenance-preserving synthesis, and independent peer review — are how architects turn an impressive demo into something you can actually ship. They also set up the recurring lesson of this whole course, which lands hard in this section: **the AI's own account of what it did is not evidence. You have to build it and verify.**

## Learning objectives

By the end of this lesson you will be able to:

1. Explain why one aggregate accuracy number hides information, and use **stratified sampling** to expose per-category accuracy instead.
2. Attach **field-level confidence scores** to structured output and route only low-confidence fields to a human-review queue.
3. Describe **calibration** and the calibration gap, and why a confident model can still be wrong.
4. Build a synthesis step that **preserves provenance** — a claim–source mapping — and **annotates conflicts** between sources instead of silently averaging them.
5. Explain why self-review is biased, and run an **independent, fresh-context peer review** to check an agent's work.
6. Verify all of the above by reading the actual output, not by trusting the model's summary of it.

## Prerequisites

- **Module 3 (Orchestration)** — coordinators, sub-agents, and the idea that a sub-agent is "just a tool." The synthesis part reuses an explorer/synthesiser pattern.
- **Module 6 · Lesson 23 (Managing the context window)** — scratchpads and keeping raw data out of the main context; this lesson writes findings to scratchpads for exactly that reason.
- **Structured output** (returning JSON via a tool schema), from Module 2.
- Python, an Anthropic API key, and the response-parser helper from Module 0. (The confidence lab also uses a public dataset from Hugging Face; installing it is part of Milestone 1.)

---

## Part 1: One number hides the truth — stratify and score

Picture an extraction agent that reads invoices and reports it is "90% accurate overall." Sounds good. But, as Andrew warns, "when it's a single metric like this, it can be hiding information." Maybe it is 99% on dates, 95% on vendor names, and 55% on line-item totals. The average looks healthy while the field that actually costs you money is a coin flip. The headline number *averaged the disaster away.*

Two moves fix this.

**Stratified sampling.** Instead of randomly spot-checking a handful of documents, you "deliberately sample from each category" — each document type, each field, each complexity band — so that "categories don't get lost in their average." You force every category to show its own accuracy. Andrew's phrase for it is "stratified random sampling": still random *within* a category, but guaranteed to cover every category.

```text
Aggregate metric (hides the problem):
  overall accuracy = 90%          <- looks fine, ship it

Stratified view (exposes the problem):
  dates          99%  ✓
  vendor names   95%  ✓
  line totals    55%  ✗  <- this is where the money is
  signatures     72%  ⚠
```

**Field-level confidence scores.** Rather than one verdict per document, the model rates each field: "I'm 99% sure on the date, 72% sure on the vendor name, 40% sure on the total line items." Now you have "a lot more detailed information," and — crucially — you have a knob for *where humans should look.*

> 🔑 **An aggregate accuracy number is a comfort blanket. Stratify by category
> and score every field, so the one weak spot can't hide inside a good-looking
> average.**

## Part 2: Route by confidence — don't review everything

Field-level confidence is only useful if you *do* something with it. The thing you do is **stratified human review**: you do not send every output to a person (that defeats the point of automation) and you do not blindly trust every output (that defeats the point of review). You set a threshold and route by confidence band.

```text
        model extracts a field, attaches a confidence score
                              │
             ┌────────────────┼────────────────┐
             ▼                ▼                 ▼
        high (>90%)      medium (70–90%)     low (<70%)
        auto-approve     spot-check          human review queue
                         (sampled)           (attorney reads it)
```

In Andrew's lab this becomes a **law-firm contract-intake pipeline**: contracts come in, Claude "extracts 30 key clauses, routed by confidence — attorney only reviews when [confidence is low]." High-confidence fields flow straight through; low-confidence fields land in a queue where a human confirms, edits, or defers. That human-review step is a small command-line interface (**CLI** — a text-based program you drive by typing): for each flagged extraction it shows the clause, the model's answer, and its confidence, then waits for you to **confirm / edit / defer**. Andrew's run: "confirmed or what does edit let us do?... 73%. There we go." Every human decision also feeds the accuracy tracker, so the system learns how good its own confidence really is.

That last point is **calibration**. A well-calibrated model's "72% sure" is right about 72% of the time. When it is *not* — when things it marks 90% are only right 60% of the time — you have a **calibration gap**, and Andrew's tracker surfaces exactly that gap by comparing claimed confidence against what the human reviewer found. A confident model is not the same as a correct one.

> 💡 **Field-level confidence isn't just AI saying "I think this invoice is
> right."** It is the model saying *which parts* it is unsure about, so you can
> spend scarce human attention only where it is needed.

### A judgment note: confidence scores are a lever, not a truth

The model's self-reported confidence is still just a number *it* produced. It can be overconfident. That is *why* you keep humans reviewing the low band and *why* you track the calibration gap — you are measuring whether the confidence can be trusted, not assuming it. Andrew is candid that the demo isn't proof of accuracy: "I'm not saying it's accurate... but the plumbing and how it works is really, really good." The plumbing is the skill. (In production Andrew would also validate the structured output with **Pydantic**, a Python library that checks data against a schema and rejects it if it doesn't fit — "this is not in the exam guide because they're not asking for it... but in practice I would absolutely be using Pydantic." You will meet retry-on-validation next lesson.)

> ✅ **What to do about it:** pick a confidence threshold, auto-approve above it,
> queue below it for a human, and *record every human correction* so you can see
> your calibration gap. Adjust the threshold from real data, not from a guess.

## Part 3: Synthesis that keeps its receipts

Now the second technique. When an agent gathers findings from several sources and merges them into one answer, something quietly breaks: "source attribution is lost during summarization steps when findings are compressed without preservation of claim–source mappings." In plain terms — you squeeze five sources into one tidy paragraph, and now nobody can tell which source said what. The receipts are gone.

Andrew's fix has two requirements, and they are the heart of this part:

1. **Preserve the claim–source mapping.** Every claim in the synthesis stays paired with the source it came from. Sub-agents are *required* "to output structured claim–source mappings" — not prose, a structure: `{claim, source, confidence}`. The synthesiser merges those without throwing the `source` away.
2. **Annotate conflicts instead of averaging them.** When two credible sources disagree — "conflicting statistics from credible sources" — you do not silently pick one or split the difference. You keep both and label them: *Source A says X (2023); Source B says Y (2024).* Conflicts get "annotated with source attributions," often with dates, so a human can adjudicate.

The lab reuses the explorer/synthesiser shape from an earlier project: an **explorer** sub-agent goes and gathers, writing each finding to a **scratchpad** file (`{content, confidence, source, tags}`); a **synthesiser** sub-agent reads only the scratchpads and produces a structured synthesis with a claim map, a retained-conflicts table, and temporal notes. Keeping raw text in scratchpads rather than the main conversation is the context-discipline habit from Lesson 23 — the synthesiser "never holds raw data, task-ID scratchpads only."

```text
explorer agents ──▶ scratchpad files            synthesiser ──▶ synthesis
                    each finding =                reads scratchpads,
                    { content,                    PRESERVES source,
                      confidence,                 emits:
                      source,        ───────▶       - claim → source map
                      tags }                        - conflicts table (A vs B)
                                                     - temporal notes
```

### The most honest ten minutes in the course

Andrew's synthesis run *did not work*, and he leaves the failure in — it teaches more than a clean demo. The synthesised file "didn't preserve the original source... I feel like this failed." He pushed on it, and then made the discovery that reframes everything: the underlying research agent "never used tools." It had been *hallucinating* the films it "found" — inventing sources rather than fetching them. "See how easy it is to miss stuff?"

This is the course's spine, made vivid. The agent *reported* sources. The report was fiction. Provenance is not a formatting nicety you can bolt on at the end — if the pipeline doesn't genuinely fetch and carry the source at every hop, a confident synthesis is just laundered hallucination. The only way Andrew found out was by reading the actual output and asking "where are the sources?" — not by trusting the summary.

> 🔑 **Preserve provenance end-to-end or don't claim it.** If a claim can't name
> the source it came from, treat it as unsourced — no matter how confident or
> polished the synthesis looks.

## Part 4: Peer review — a fresh reviewer beats self-review

The third technique attacks a specific, sneaky failure. Ask a model to review work it just produced and it is biased: "because it already has that history prior, it's going to take bias to its work and think that it's done a really, really good job." It is "anchored to its own reasoning, prior choices," and if it made a mistake it may "double down on it."

The fix is structural, not a better prompt: **have a separate agent, model, or step review the work — one with no memory of producing it.** Andrew's contrast is exact:

| | **Self-review** | **Peer review** |
|---|---|---|
| Context | Continues the *same* conversation | A **brand-new request, no prior messages** |
| What the reviewer knows | Full memory of having generated the work | "The model has no knowledge" of who wrote it |
| Bias | Anchored to its own reasoning; may double down | No stake in the answer; judges it fresh |
| Good for | Quick, cheap sanity pass | Real quality control |

The lab generates **JLPT N5 Japanese vocabulary practice questions** (JLPT = the standard Japanese-Language Proficiency Test; N5 is the beginner level) two ways. In self-review the generator keeps the conversation and — predictably — "they're all correct." In peer review "a brand-new request with no prior messages... the model has no knowledge" of the source and scores each question on its own merits. Andrew's rule is worth memorising verbatim: **"For any AI-generated content that requires quality control, always use a separate context... never ask the generator to grade its own input in the same conversation."**

The cheapest way to get a fresh context is a fresh message thread — a new API call with no history. A sub-agent (its own isolated context) does the same job. The point is only that the reviewer must not carry the generator's memory.

> 🔑 **The generator is the worst judge of its own output.** Quality control
> means a reviewer with a clean context — one generates, a *different* one
> reviews.

---

## Key takeaways

1. **One aggregate accuracy number hides the weak category.** Stratify by document type and field so each category shows its own accuracy.
2. **Score every field, then route by confidence.** Auto-approve the high band, queue the low band for a human. Don't review everything; don't trust everything.
3. **Confident ≠ correct.** Track the calibration gap by recording human corrections; the model's self-confidence is a lever to be measured, not a truth.
4. **Preserve provenance end-to-end.** Keep a claim→source mapping through every synthesis step; if a claim can't name its source, it's unsourced.
5. **Annotate conflicts, don't average them.** Keep both disagreeing sources, labelled (often with dates), for a human to adjudicate.
6. **A generator can't grade itself.** Use an independent, fresh-context peer reviewer for real quality control.
7. **The AI's account of its work is not evidence.** Andrew's agent *claimed* sources it had hallucinated. Read the output; verify.

## Common pitfalls

- ❌ **Reporting a single accuracy number.** It averages your worst field into invisibility. Always stratify.
- ❌ **Reviewing every output by hand.** That throws away the automation. Route by confidence band instead.
- ❌ **Trusting the confidence score as ground truth.** It's the model's self-estimate. Measure it against human corrections (the calibration gap).
- ❌ **Compressing findings and losing the source.** The moment you summarise without carrying `source`, provenance is gone and can't be reconstructed.
- ❌ **Silently resolving conflicts.** Picking one of two disagreeing sources, or averaging them, destroys information a human needed. Keep both, annotated.
- ❌ **Letting the generator review itself in the same conversation.** It's anchored to its own reasoning and will pass its own work. Use a fresh context.
- ❌ **Believing "I found these sources."** Andrew's agent never used tools and invented them. Confirm the fetch actually happened.

---

## 🛠️ Capstone Project: Reliability layers for Atlas Support

> This is the main hands-on project for the lesson. You will feel the shift from
> "the agent produced an answer" to "the agent produced an answer I can *trust,
> route, and defend*." Keep each layer small — the point is the pattern.

### What you will build

Take Atlas Support's ticket-triage output (category, urgency, suggested response, and any extracted facts) and wrap it in the three reliability layers from this lesson. Each layer is a standalone milestone that works on its own:

- **Field-level confidence + a human-review queue** — the model scores each field; low-confidence fields go to a review CLI. *(Parts 1–2)*
- **Stratified accuracy tracking** — accuracy broken down by field and ticket type, plus a calibration gap. *(Parts 1–2)*
- **Provenance-preserving synthesis** — when a ticket pulls facts from several sources (knowledge-base articles, past tickets), keep a claim→source map and flag conflicts. *(Part 3)*
- **An independent peer-review pass** — a fresh-context reviewer grades the suggested response before it's sent. *(Part 4)*

### Why this is the perfect practice

| Lesson idea | Where you use it in Atlas Support |
|---|---|
| Stratified sampling | Accuracy tracked per field and per ticket type, never one blended number |
| Field-level confidence | Each triage field carries its own score |
| Route by confidence | Low-confidence fields land in a human-review CLI (confirm/edit/defer) |
| Calibration gap | Every human correction is logged and compared to claimed confidence |
| Preserve provenance | Facts pulled from sources keep a claim→source mapping through synthesis |
| Annotate conflicts | Disagreeing sources are kept and labelled, not averaged |
| Peer review | A fresh-context agent grades the drafted reply before it goes out |
| Verify, don't trust | You read the queue, the map, and the review — you don't assume they worked |

### Milestones (build them in order, each one works on its own)

1. **Get a dataset and print it.** You need realistic multi-field extractions to score. Grab a public one from **Hugging Face** the way Andrew did — `pip install datasets`, then `from datasets import load_dataset` and load the **CUAD** contract dataset (`load_dataset("theatticusproject/cuad", ...)`). Just print a few rows first. *(Heads-up, straight from Andrew's run: the loader may complain about `trust_remote_code` or a size-mismatch — "remove the trust remote code, this is a standard parquet dataset, no script loading needed." Adjust and re-run. Getting the data to print is the milestone.)* Prefer Atlas Support's own tickets? Use those instead; the dataset is only stand-in structured data.
2. **Field-level confidence.** Have Claude extract several fields per record (for CUAD: clause types; for Atlas: category, urgency, extracted facts) and return, for each field, `{value, confidence}` as JSON. Print them. Confirm you see *different* confidences per field, not one blanket number.
3. **The human-review queue (a CLI).** Set a threshold (say 0.85). Auto-approve fields above it; for each field below it, print the field, the model's value, and its confidence, then read a keypress: **c**onfirm / **e**dit / **d**efer. This is your human-in-the-loop. Run it on ~5 records — you should only be asked about the genuinely uncertain fields.
4. **Stratified accuracy tracking.** As the human confirms/edits, record accuracy **per field and per ticket type** — never one aggregate. Print the breakdown, and print the **calibration gap**: for fields the model marked ">90%," how often did the human actually change them? That gap is your headline reliability signal.
5. **Provenance-preserving synthesis.** Now the second technique. When a ticket needs facts from multiple sources (2–3 short mock KB articles + a past ticket), have an explorer step write each finding to a **scratchpad** as `{claim, source, confidence}`, and a synthesiser step read the scratchpads and emit a synthesis that (a) keeps a claim→source map and (b) lists any conflicts as "Source A says X; Source B says Y." Verify by opening the synthesis and checking every claim names a source — Andrew's failure was exactly here.
6. **Independent peer review.** Take the suggested customer reply and send it to a **brand-new API call with no prior messages** — a reviewer that never saw it written. Prompt it to score accuracy, tone, and completeness and flag problems. Compare against a self-review (same conversation) and note how much softer the self-review is. Ship only replies the *fresh* reviewer passes.
7. **Stretch goals.** (a) Feed the calibration gap back: raise the review threshold for fields the model is overconfident about. (b) Validate the extraction JSON with **Pydantic** and reject malformed output before it reaches the queue (bridges into next lesson). (c) Have the peer reviewer output structured `{pass, issues[]}` so a failing review can auto-route back for a rewrite.

### How you will know you are done

- ✅ Every extracted field carries its own confidence score — you can point to a high one and a low one.
- ✅ Only sub-threshold fields reach the human queue; high-confidence fields are auto-approved.
- ✅ Accuracy is reported per field and per ticket type, plus an explicit calibration gap — never a single blended number.
- ✅ Every claim in the synthesis names its source, and any conflict is shown with both sources, not averaged away.
- ✅ The peer reviewer runs in a fresh context with no memory of the draft, and you can show it catching something self-review missed.
- ✅ You verified each of the above by *reading the actual output*, not by trusting the model's summary.

> 💡 **Keep yourself honest:** the two mistakes this lesson is built to catch are
> (1) trusting a confident number and (2) trusting a synthesis whose sources were
> never really fetched. For each, open the raw output and prove it. "See how easy
> it is to miss stuff?"

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice
> on one idea. Optional and independent; the Capstone already touches all of
> them, so feel free to skip straight to it.

### Exercise 1: Un-hide the average (foundational)
Given four fields with accuracies 99%, 95%, 55%, 72% and equal weight, compute the aggregate. Then write one sentence on which field the aggregate hides and why a human reviewer needs the stratified view.

### Exercise 2: Route the queue (intermediate)
Take ten mock extractions with confidence scores. Pick a threshold, split them into auto-approve / review / defer, and justify your threshold. Then move the threshold and describe the trade-off (more human work vs. more errors slipping through).

### Exercise 3: Break provenance, then peer-review it (advanced)
Write a synthesiser that summarises three sources into a paragraph *without* carrying the source — observe that the claims are now unattributable. Fix it with a claim→source map. Then hand the two versions to a fresh-context reviewer and have it flag which one it can and cannot verify.

---

## Cheat sheet

```text
RELIABILITY I — human review, confidence, synthesis, peer review

1) FIELD-LEVEL CONFIDENCE + STRATIFIED HUMAN REVIEW
   - One aggregate number HIDES the weak category. Stratify:
       report accuracy PER field and PER document/ticket type.
   - Score every field: { value, confidence }  (e.g. date 99%, total 40%)
   - Route by band:  high -> auto-approve
                     low  -> human-review queue (confirm / edit / defer)
   - CALIBRATION GAP = claimed confidence vs. actual accuracy.
       Log every human correction; measure the gap. Confident != correct.
   - (prod) validate structured output with Pydantic.

2) MULTI-SOURCE SYNTHESIS — KEEP THE RECEIPTS
   - Provenance is lost when findings are compressed without the source.
   - Require sub-agents to emit CLAIM -> SOURCE mappings (a structure):
       { claim, source, confidence }
   - Synthesiser reads scratchpads, PRESERVES source, and
       ANNOTATES conflicts:  "Source A says X (2023); Source B says Y (2024)"
       -> keep both, don't average.
   - If a claim can't name its source, treat it as UNSOURCED.

3) PEER REVIEW — FRESH CONTEXT BEATS SELF-REVIEW
   - Self-review = same conversation -> biased, "it's all correct."
   - Peer review = brand-new request, NO prior messages -> judges fresh.
   - RULE: "never ask the generator to grade its own input in the
            same conversation." Use a separate context for QC.

THE SPINE OF THE COURSE
   The AI's account of what it did is NOT evidence.
   Andrew's agent CLAIMED sources it had hallucinated (never used tools).
   Read the output. Verify. "See how easy it is to miss stuff?"
```

## How this connects to the rest of the course

- **Earlier, Module 3 (Orchestration):** the explorer/synthesiser pattern here is a coordinator with sub-agents — provenance is what you add so aggregation doesn't destroy information.
- **Earlier, Module 6 · Lesson 23 (Managing the context window):** scratchpads keep raw source text out of the main context; this lesson uses them so synthesis stays lean *and* sourced.
- **Next, Module 6 · Lesson 25 (Reliability II — validation retries and large context):** confidence tells you *where* the output is weak; next you make the loop *fix* invalid output automatically — append the validation error and retry, with a max-attempt cap. Pydantic, mentioned here, becomes central there.
- **Later:** these reliability checks are what let Atlas Support safely run in batch and, at the end, escalate to a human — the human-review queue you build here is that escalation path in miniature.

---

*Source: reconstructed from the CCA-F course by Andrew Brown (ExamPro). Code
snippets and diagrams are illustrative reconstructions of the patterns described
in the course. Adapt them to the current SDK.*
