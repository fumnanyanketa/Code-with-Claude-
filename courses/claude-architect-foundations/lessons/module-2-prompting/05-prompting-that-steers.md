# Module 2 · Lesson 5: Prompting that steers the model

> **Course:** Claude Certified Architect: Foundations, a self-paced course
> **Module 2:** Prompting & structured output: steer the model before orchestrating many
> **Speaker:** Andrew Brown, ExamPro
> **Source:** Reconstructed from the CCA-F course by Andrew Brown (ExamPro) · [full transcript](../../transcripts/cca-f-full-course.txt)
> **Estimated time:** 45 to 60 minutes (read plus lab)

---

## In one sentence

You steer a model far more reliably by *showing it examples* and *describing the goal and quality bar* than by handing it a rigid list of steps — and by writing prompts specific enough that the model can't wander off doing the wrong thing.

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone Project** where you take one weak, vague prompt for an Atlas Support sub-task and rewrite it into a criteria-driven, few-shot prompt — then compare the two outputs side by side. Everything before the Capstone teaches the three moves you will use there: few-shot examples, goal-and-criteria prompting, and specificity. If you want to see the finish line first, jump to the **"Capstone Project"** section, then come back.

## A few plain-language basics first

This lesson uses a handful of terms. Here they are in plain words:

- **LLM:** the kind of AI that reads and writes text; "Claude" is one.
- **Model:** one specific version of that AI (e.g., Opus, Sonnet, Haiku) differing in strength, speed, and price.
- **Token:** the unit a model reads and writes in, roughly three-quarters of a word; you are billed per token, so wasted work costs real money.
- **Prompt:** the instructions and context you send the model to tell it what you want.
- **Hallucination:** when the model confidently makes something up — invents a fact, a format, or a field that was never real.
- **Few-shot prompting:** giving the model a few worked examples (good ones, bad ones, even scored ones) inside the prompt so it copies the pattern instead of guessing.
- **Coordinator:** in a multi-agent system, the one agent that owns routing and decides what "done" looks like. You will meet it fully in a later module; here it is just "the agent you are prompting."
- **False positive:** the model reports work or findings that look like a result but are actually the wrong thing — because it never knew precisely what you wanted.

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

Before you orchestrate many agents, you have to be able to steer *one*. A model that drifts, hallucinates a format, or "does many many things" on a vague instruction will only drift faster once you wire several together. This lesson is where you learn to put your hands firmly on the wheel. As Andrew frames the vague-prompt trap: "it'll start working on the wrong files or looking at the wrong things because it just doesn't know what it's supposed to be doing." The fix is three concrete prompting moves that cost you a few extra sentences and save you compute, time, and re-runs. Get these right and every later lesson — structured output, tools, coordinators — sits on solid ground.

## Learning objectives

By the end of this lesson you will be able to:

1. Write a few-shot prompt that includes good, bad, and *scored* examples to cut hallucination and lock in a format.
2. Replace a rigid step-by-step prompt with a goal-and-quality-criteria prompt that survives when a step breaks or the task doesn't fit the script.
3. Spot a vague prompt that will produce false positives, and rewrite it to be specific enough to save compute and get realistic results.

## Prerequisites

- **Module 1 · Lesson 4, "Loop antipatterns and ending the loop correctly."** You should already know that an agent runs a loop and stops on a signal, not on you parsing its text. This lesson is about what you *put into* that loop.
- A working way to call a model (the Anthropic SDK or Claude Code from Module 1 is plenty). No new tools required.

---

## Part 1: Few-shot — show, don't just tell

Start with the simplest, highest-leverage move. Suppose you want to pull the measurement out of each ingredient line. A user writes "roughly three teaspoons of olive oil" and you want it in one exact shape. You could describe the shape in words. But as Andrew puts it, "to make sure that we get it the way that we want, we're going to provide examples."

That is few-shot prompting: you include a few worked examples right in the prompt so the model copies the pattern instead of inventing one. Andrew's reasoning is blunt and worth memorising: "it's going to provide consistent results and it's going to reduce hallucinations. And this works extremely well."

Why does showing beat telling? A description leaves gaps, and a model fills gaps by guessing — that guess is the hallucination. An example leaves no gap: the model can see the exact field names, the exact casing, the exact way you want a fuzzy input ("roughly three") turned into a clean output.

> 🔑 **Examples remove the gaps a model would otherwise fill by hallucinating. Show the exact output you want, don't just describe it.**

### Go further: bad examples and scored examples

Good examples steer toward the target. Andrew adds two upgrades that steer *away* from the ditch:

- **Bad examples.** Show the model what a wrong answer looks like, not just a right one. Andrew does this for a Japanese language-learning app: "I will provide really good ones and bad ones."
- **Scored examples.** Attach a quality score to each example. "And in fact, I will even score them and that will help them a lot more." A score teaches the model the *gradient* between great and poor, not just a binary.

Here is the pattern in one illustrative prompt:

```text
Extract the measurement from each ingredient. Output exactly: {"amount": <number>, "unit": "<unit>"}

Example (score 10/10 — ideal):
  Input:  "roughly three teaspoons of olive oil"
  Output: {"amount": 3, "unit": "tsp"}

Example (score 2/10 — bad, do NOT do this):
  Input:  "roughly three teaspoons of olive oil"
  Output: {"amount": "three teaspoons", "unit": "olive oil"}   # kept the fuzzy word, put the food in "unit"

Now extract from:
  Input:  "a couple pinches of sea salt"
  Output:
```

The bad example with a one-line note ("kept the fuzzy word, put the food in `unit`") is doing real teaching: it names the exact mistake so the model steers clear of it.

> 💡 **It is not a complicated concept.** In Andrew's words: "Add in examples, or examples of the results, and you'll get better results." Two or three examples usually move the needle more than another paragraph of instructions.

## Part 2: Goals and quality criteria, not rigid step lists

The instinct when you want control is to write a procedure: do this, then this, then this. Andrew warns that this backfires: "if you have procedural prompts that make the coordinator rigid — if a step breaks or the task doesn't fit the script, it will break."

Here is the rigid prompt he shows, the kind to avoid:

```text
You are a coordinator. Follow these steps exactly:
  1. Call this.
  2. Call that.
  3. Do this, do that.
  4. Return the reviewed output.
Always follow these exact sequences.
```

The problem: real tasks don't fit one fixed script. When something fails partway, "you know the thing is done" — it stalls, because the script has no room to adapt. You have described the *path* instead of the *destination*, so the model can't recover when the path is blocked.

The better move is to describe the destination and the bar for reaching it:

```text
You are a research coordinator.

GOAL: Produce a response that fully addresses the user's request with
accurate, well-supported findings.

QUALITY CRITERIA (a finding is high quality only when ALL are met):
  - Every claim is backed by a cited source.
  - The final output covers all five similarity axes.
  - At least 15 distinct items are returned.

GUIDANCE (use only if helpful): you may work in phases; stop when the
criteria above are met.
```

Notice what carries the weight. As Andrew says, "the major thing we're looking at is this quality criteria." The goal tells the model *what success is*; the criteria tell it *how to check its own work*; the guidance is optional scaffolding, not a cage. He even sharpens the criteria with concrete numbers — "produces a curated source back list of at least 15 distinct films" — because "that's being very clear as to how much."

> ✅ **What to do about it:** lead with a `GOAL` line and a `QUALITY CRITERIA` checklist the model can grade itself against. Demote step-by-step instructions to optional `GUIDANCE`. Let the model find the path; you own the destination and the bar.

### A judgment note on phases

Working "in phases" is not automatically bad — Andrew is explicit: "this thing is going through phases, which is not necessarily a bad thing. We can do that." The trap is *only* having phases with no criteria, so the model can't tell whether the work is actually good. Phases are fine as guidance; criteria are what make the output trustworthy. And notice Andrew's honesty about a real gap in his own criteria version: "I don't see how it would loop back, though" — describing the goal well doesn't automatically tell the model when to *retry*, so name that in your criteria too if you need it.

> 💡 **The recurring lesson of this course:** don't trust that a prompt works because it reads well — Andrew keeps saying "I won't know until we run it." Write the criteria version, run it, and check the output against your own criteria. Build it and verify.

## Part 3: Be specific — vague prompts cause false positives and waste compute

The third move is the one Andrew calls "probably the most obvious but the most important prompting technique": be specific.

Here is the failure mode. You give a vague instruction and, because the model "just doesn't know what it's supposed to be doing," it starts "broadly doing many many things." Andrew's example: you say "go review the codebase for issues." *What* issues? The model doesn't know, so "it'll come back with all sorts of stuff, eat up your compute, eat up your time" — and maybe none of it is the specific thing you actually cared about.

That is a **false positive**: the model produces confident-looking work on the wrong target. It looks like a result; it isn't the result you needed.

Compare the specific version: "audit only the single one, and that's going to save you time and compute and get realistic results." Same model, same task family — but now it hits the target instead of spraying effort across the whole surface.

The classic vague prompt is "fix the login bug." Andrew unpacks why it stalls: "fix it how? Use what email at what address? Is there more than one app in here?" With that missing, the agent "is going to waste a lot of time looking around for stuff." Fill those blanks in and, in his words, "more information is going to have the agent SDK or Claude Code perform a lot better."

> 🔑 **Vague in, unpredictable out. Specificity is not politeness — it is how you stop the model burning tokens on the wrong thing.**

A useful tell: if *you* can't say exactly what a correct answer would look like, the model can't either. When you're stuck, Andrew notes you "can even use plan mode or some other things to extract out better tasks" before you run the expensive work — a way to sharpen the target first. This connects straight back to Part 1 and Part 2: a scored example *is* a form of specificity (it pins down what good looks like), and quality criteria *are* specificity about the finish line.

### How the three moves stack

```text
Vague prompt
  └─ model guesses format        → hallucination
  └─ model guesses the target    → false positives, wasted compute
  └─ rigid steps, no bar         → stalls when a step breaks

Steered prompt
  ├─ FEW-SHOT examples (good + bad + scored)   → locks the format, cuts hallucination
  ├─ GOAL + QUALITY CRITERIA (not rigid steps) → survives surprises, self-checks
  └─ SPECIFICITY (name the exact target)       → hits the right thing, saves compute
                                   ↓
                    consistent, realistic, cheaper output
```

---

## Key takeaways

1. **Show, don't just tell.** Few-shot examples remove the gaps a model would fill by hallucinating. Include good, bad, and *scored* examples for the strongest steer.
2. **Prompt the destination, not the path.** Lead with a goal and a quality-criteria checklist; demote step lists to optional guidance so the prompt survives when a step breaks.
3. **Specificity is a cost control.** Vague prompts cause false positives — confident work on the wrong target — and burn compute. Name the exact thing you want.
4. **Verify, don't assume.** A prompt that reads well can still be wrong. "I won't know until we run it" — run it and grade the output against your own criteria.

## Common pitfalls

- ❌ **Describing the output format in prose instead of showing it.** The model fills the unspecified details by guessing. Paste one or two exact example outputs.
- ❌ **Only giving good examples.** Add a bad example with a one-line note on *why* it's bad; the contrast teaches more than another good one.
- ❌ **Writing "follow these steps exactly."** The first failed step strands the model. Give a goal and criteria; let it find the path.
- ❌ **Vague scope like "review the codebase" or "fix the login bug."** You'll get sprawling false positives and a big bill. State the single specific target and what "fixed" means.
- ❌ **Trusting the prompt because it reads well.** Run it and check the output against your criteria before you rely on it.

---

## 🛠️ Capstone Project: Steer one Atlas Support sub-task

> This is the main hands-on project for the lesson. You will feel, directly, the difference between a prompt that hopes and a prompt that steers — on a real piece of the system this course builds.

Across this course you are building **Atlas Support**, a multi-agent support system that will eventually escalate hard tickets to a human. Long before it has many agents, it has to steer *one* well. Your job here is to take a single Atlas Support sub-task — **classify an incoming support ticket** — and turn a weak prompt into a steered one, then prove the upgrade with output.

### What you will build

A tiny before/after harness: one weak prompt, one rewritten prompt, and a short write-up of how the outputs differ. The rewritten prompt uses all three moves from this lesson:

- **Few-shot examples** (good + bad + scored) — from Part 1.
- **A goal and quality-criteria block** instead of rigid steps — from Part 2.
- **A specific target** so the model can't produce a false positive — from Part 3.

### Why this is the perfect practice

| Lesson idea | Where you use it in the capstone |
|---|---|
| Few-shot (good/bad/scored) | The three example tickets you paste into the rewritten prompt |
| Goal + quality criteria | The `GOAL`/`QUALITY CRITERIA` block replacing "follow these steps" |
| Specificity kills false positives | Naming the exact label set and required fields, not "categorise this" |
| Build and verify | Running both prompts and comparing the actual outputs |

### The starting point (a weak prompt)

```text
Look at this support ticket and tell me what it's about and how urgent it is.

Ticket: "Hi, I was charged twice for my May subscription and the second
charge put my account into overdraft. I need this refunded today."
```

This is vague on every axis: no fixed categories, no output shape, no urgency scale, no definition of "done." As Andrew warns, the model will "broadly do many many things" and you'll get an unpredictable blob you can't route on — a false positive dressed up as an answer.

### The target (a steered prompt — illustrative)

```text
You are the Atlas Support triage classifier.

GOAL: Turn one raw support ticket into a routing decision the coordinator
can act on without re-reading the ticket.

QUALITY CRITERIA (output is acceptable only when ALL are met):
  - "category" is exactly one of: billing | technical | account | other
  - "urgency" is exactly one of: low | medium | high
  - "needs_human" is true only if the ticket involves money movement,
    legal risk, or an explicit demand for a person
  - Output is valid JSON with exactly these three fields, nothing else

Example (score 10/10 — ideal):
  Ticket: "The app crashes every time I open the reports tab."
  Output: {"category": "technical", "urgency": "medium", "needs_human": false}

Example (score 2/10 — bad, do NOT do this):
  Ticket: "The app crashes every time I open the reports tab."
  Output: "This looks like a technical problem, probably medium urgency."
  # prose instead of JSON; missing needs_human; not machine-routable

Now classify:
  Ticket: "Hi, I was charged twice for my May subscription and the second
  charge put my account into overdraft. I need this refunded today."
  Output:
```

### Milestones (build them in order, each one works on its own)

1. **Run the weak prompt.** Send the starting prompt to your model and save the raw output. Notice you cannot reliably route on it. This is your baseline.
2. **Add specificity.** Rewrite it to name the exact label sets (`category`, `urgency`) and the required JSON fields. Run it. Already better, still improvable.
3. **Add the goal and criteria block.** Replace any leftover "do this then that" with the `GOAL` and `QUALITY CRITERIA` shown above. Run it.
4. **Add few-shot with a scored bad example.** Paste the good (10/10) and bad (2/10) examples, each with a one-line note. Run it. This is your finished steered prompt.
5. **Compare and write it up.** In three or four sentences, state how the outputs differ: format consistency, correct urgency, correct `needs_human`, and whether the result is now machine-routable.
6. **Stretch goals.** Feed five different tickets through both prompts and count how many the weak prompt gets into clean JSON versus the steered one. Then try deliberately breaking the steered prompt (remove the bad example) and see whether hallucinations creep back — verify the claim yourself.

### How you will know you are done

- ✅ The steered prompt returns valid JSON with exactly the three fields, on every test ticket.
- ✅ The overdraft ticket comes back as `billing`, `high`, `needs_human: true` — and you can explain which part of the prompt made each field correct.
- ✅ You can point to at least one concrete difference between the weak and steered outputs (format, accuracy, or routability).
- ✅ Your write-up names *which* of the three moves fixed *which* problem.

> 💡 **Keep yourself honest:** don't judge the rewrite by how good it reads — run both prompts on the same tickets and compare the actual outputs. As Andrew keeps saying, "I won't know until we run it."

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice on one idea. Optional and independent; the Capstone already touches all of them, so feel free to skip straight to it.

### Exercise 1: Add a scored bad example (foundational)
Take any prompt where you already give one good example. Add one *bad* example of the same input with a one-line note on why it's wrong, and score both. Run before and after; note any change in consistency.

### Exercise 2: De-rigidify a prompt (intermediate)
Find or write a prompt that says "follow these steps." Rewrite it as a `GOAL` plus a `QUALITY CRITERIA` checklist with at least one concrete number in it (like "at least 15"). Run both on a task that *doesn't* fit the original steps and see which one copes.

### Exercise 3: Hunt a false positive (advanced)
Write a deliberately vague instruction ("review this for issues"). Run it and log how much output and how many tokens it produces. Now rewrite it to name one specific thing to check. Compare the token counts and whether the specific version actually found the thing you cared about.

---

## Cheat sheet

```text
PROMPTING PLAYBOOK — three moves to steer one model

1) FEW-SHOT: show, don't tell
   - Paste exact example outputs, not a prose description of them
   - Good + BAD + SCORED examples steer hardest
   - Why: examples remove the gaps a model fills by hallucinating

2) GOAL + QUALITY CRITERIA (not rigid steps)
   - Rigid "follow these steps exactly" breaks when a step breaks
   - Instead: GOAL (what success is) + CRITERIA (self-check checklist)
   - Put concrete numbers in criteria ("at least 15")
   - Steps are optional GUIDANCE, not a cage; phases are OK, criteria matter
   - Criteria don't auto-tell it when to retry — say so if you need loop-back

3) BE SPECIFIC (kills false positives, saves compute)
   - Vague -> model "broadly does many many things" -> wrong target, big bill
   - False positive = confident work on the wrong thing
   - Name the exact target + what "done" looks like
   - Tell: if you can't say what a correct answer looks like, neither can it
   - Sharpen tasks first with plan mode when stuck

ALWAYS: build and verify. A prompt that reads well can still be wrong.
        "I won't know until we run it." Run it, grade the output.
```

## How this connects to the rest of the course

- **Earlier, Module 1 · Lesson 4 ("Loop antipatterns and ending the loop correctly"):** you learned to end the agentic loop on a real signal, not by parsing text. This lesson fills that loop with prompts the model can actually follow.
- **Next, Module 2 ("Forcing structured output"):** the bad example in your few-shot was "prose instead of JSON." Next you make JSON non-negotiable by giving the model a tool with a schema — turning a *prompted* format into an *enforced* one.
- **Later, in the coordinator and multi-agent modules:** goal-and-criteria prompting is exactly how you'll brief a coordinator that delegates to sub-agents. Steering one model well is the prerequisite for orchestrating many.

---

*Source: Reconstructed from the "Claude Certified Architect: Foundations" course by Andrew Brown (ExamPro). Code snippets and diagrams are illustrative reconstructions of the patterns described in the course. Adapt them to the current SDK.*
