# Module 2 · Lesson 3 — The Prompting Playbook

> **Course:** Building with Claude — A Self-Paced Course
> **Module 2:** Core skills — working with the model
> **Speaker:** Margo van Laar, Applied AI Engineer, Anthropic (London)
> **Source talk:** [The prompting playbook](https://www.youtube.com/watch?v=G2B0YWuJUgI) · [full transcript](../../transcripts/code-with-claude-2026-london-2026/05_the-prompting-playbook.txt)
> **Estimated time:** 45–60 min (read + exercises)

---

## In one sentence

Prompting is a debugging discipline, not a writing exercise: you make changes **one at a time against an eval suite**, apply general "hygiene" first, and reach for the *right* fix — structure, a tool, a better model, or a multi-step loop — instead of piling on more instructions.

## Why this lesson matters

Prompting is "arguably the first skill we had to learn as engineers working with LLMs, and it continues to be one of the most critical." Most of the time you are **not** writing a prompt from scratch — you're maintaining one that several people have edited, that mixes policy, tone, and old model-specific patches, and that suddenly performs worse after a model migration. This lesson gives you a repeatable method for exactly that situation, then shows how to start a brand-new agent the right way.

## Learning objectives

By the end of this lesson you will be able to:

1. Build a minimal **eval suite** with the three case types every prompt needs (control, edge, capability/handoff).
2. Apply **prompt hygiene** — structure, removing cruft, output contracts — before chasing specific failures.
3. Diagnose *why* a prompt fails and choose the correct fix: rewrite an instruction, give the model a **tool**, change the **model/effort**, or split into a **multi-prompt loop**.
4. Recognize and avoid the core anti-pattern: **overfitted instructions** ("ban lists" and one-sided rules) inherited from older models.

## Prerequisites

- Module 2 · Lesson 1 (*The Prompting Playbook* assumes the basics of sending messages to Claude).
- Helpful: Module 3 (*Evals for taste*) — this lesson leans heavily on evals; you can take them in either order.

---

## Part 1 — The setup: a prompt in trouble

Picture a customer-support bot for a fictional telco, **Meridian Mobile**. The prompt has "no clear owner," covers "policy, tone, processes," and carries "patches for previous models all mixed together." After migrating to a new model, several test cases regress.

> 🔑 **Key idea — you can't fix what you can't measure.** When a prompt regresses after a model change, there are two possible causes, and you must tell them apart:
> 1. The new model is **capable but behaves differently** → you can fix it with prompting.
> 2. The new model is **less capable** at this task → no amount of prompting will fix it.
> An eval suite is what lets you distinguish these and prove a change actually helped.

### The three case types every eval needs

The demo uses just **five** test cases (yours will have far more), but they cover three essential categories:

| Case type | What it checks | Meridian example |
|---|---|---|
| **Control** | A case that should *always* pass — unambiguous, well-handled | "What's the data limit on the basic plan?" |
| **Edge** | A case where the model has failed before; the prompt should prevent regression | Proration math; not withholding info the model has |
| **Capability / handoff** | Does the model know the limits of its job — when to escalate or refuse? | Escalate billing errors to a human |

> 💡 The capability/handoff case is the one teams most often forget. A model that confidently answers something it should have escalated is worse than one that fails loudly.

### The method

```
1. Run the eval on v0 of the prompt        → see the failure modes
2. Apply general hygiene (clean up first)  → often a free uplift
3. Target failure modes ONE AT A TIME      → isolate cause and effect
4. Re-run the eval after every change       → keep what helps, revert what doesn't
```

After the first run, the control case passes but the bot "performs pretty poorly in the other areas." Before zooming in on specific failures, clean up.

---

## Part 2 — Prompt hygiene (do this first, every time)

The original prompt has tell-tale problems: it claims the bot is a human ("which just isn't true"), and it contains text **copied straight from a website** — "the key giveaway is a reference to a hero image" and "references to cookies at the bottom." Everything is jammed "into one big paragraph" with "no real way of unpacking policy from guidelines from tone."

### Fix 2.1 — Add structure with XML tags

A messy, undifferentiated prompt looks like this:

```text
You are a friendly human support rep for Meridian Mobile. Our hero image
shows... [website cruft] ... Always be polite. Never give wrong plan
details, point them to the URL. Plans: basic 10GB... Calculate prorations
correctly. We use cookies to... Always calculate prorated amounts correctly.
```

Restructure it so each kind of information is separated:

```text
<role>
You are a customer support assistant for Meridian Mobile, a mobile network operator.
</role>

<guidelines>
- Be concise, warm, and conversational.
- Answer using the customer's account data as the source of truth.
</guidelines>

<policy>
- Plan data allowances are listed in <plan_data>.
- Customers on grandfathered/legacy plans may have different allowances —
  these are captured in the customer's account context.
</policy>

<tone>
Friendly and professional. Avoid jargon.
</tone>

<plan_data>
...
</plan_data>
```

Re-running the eval after *only* this change already improves performance.

> 🔑 **Rule of thumb (quote):** *"If you're reading a prompt and you can't tell guidelines from policy from data, most likely the model isn't able to either."* — Margo van Laar

### Fix 2.2 — Add an output contract (and enforce it in the harness)

If output format is inconsistent, define it explicitly **and** back it up in the API call rather than relying on the prompt alone:

```text
<output_format>
Respond with your message wrapped in <response>...</response> tags.
</output_format>
```

```python
# Enforce the contract in the harness, not just the prompt.
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    system=system_prompt,
    messages=messages,
    stop_sequences=["</response>"],   # stop generating at the closing tag
)
```

> 💡 For complex schemas (e.g. nested JSON), prefer **structured outputs** to guarantee shape programmatically. The prompt "is not always the most effective way of handling issues" — change the harness too.

After hygiene, two cases pass consistently. Three failures remain: **hotspot**, **proration**, **billing error**. Now target them one at a time.

---

## Part 3 — Targeting failures one at a time

### Failure 3.1 — The model withholds information it has (hotspot)

**Question:** "How much hotspot data is on my unlimited plan?"
**Customer reality:** They're on a *grandfathered* plan and their account data says **5 GB**.
**Bug:** The bot answers with the generic "4 GB" and tells the customer to "go check this out yourself" — deflecting to a URL instead of giving the answer it already has.

The culprit instruction:

```text
We changed our plans recently. The policy doc shows current plan data, and
customers on grandfathered plans have different rates. NEVER give a customer
the wrong plan details — instead, point them to the URL.
```

That "never give wrong details → point to URL" line is an old **patch** for a weaker model. Newer models follow instructions more literally, so the patch is now **overfitted**: the bot suppresses correct info to avoid being "wrong." The fix is to state the balanced truth:

```text
Customers on grandfathered plans may have different allowances. The customer's
account context is the accurate source of truth — use it to answer directly.
```

> 🔑 **Lesson:** We worry about hallucination (inventing facts), but the **opposite** also happens — the model **withholds** information it actually has, usually because of a defensive patch.
> ✅ **Best practice:** **Version-control your defensive changes.** Whenever you add a patch, record *why*. Later models may make it counterproductive, and you'll want to find and remove it.

### Failure 3.2 — Mental math (proration)

**Question:** "What if I upgrade to the 30 GB plan? What will my next bill be?"
**Bug:** The model "reasons through it, does a little mental math," but never returns a concrete, trustworthy number.

The culprit instruction just *exhorts* the model:

```text
Don't ever give a customer a vague answer. CRITICAL: always calculate any
prorated amounts correctly.
```

> 🔑 **Lesson (quote):** *"Instructions don't add capability. Telling the model it's critical to do a calculation right doesn't make it better at mental maths."*

The correct fix is to **give it a tool** so it executes the math reliably. Three steps:

```text
# 1. In the prompt — tell it when to use the tool
Whenever a calculation is required, use the calculate_proration tool. Do not
do arithmetic yourself.
```

```python
# 2. Define the tool schema so the model knows what it does and when to call it
calculate_proration_tool = {
    "name": "calculate_proration",
    "description": "Calculate a prorated charge when a customer changes plan "
                   "partway through a billing cycle. Use this for ANY billing math.",
    "input_schema": {
        "type": "object",
        "properties": {
            "old_plan_price": {"type": "number"},
            "new_plan_price": {"type": "number"},
            "days_remaining":  {"type": "integer"},
            "days_in_cycle":   {"type": "integer"},
        },
        "required": ["old_plan_price", "new_plan_price",
                     "days_remaining", "days_in_cycle"],
    },
}

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    system=system_prompt,
    tools=[calculate_proration_tool],
    messages=messages,
)
```

```python
# 3. Implement the actual maths behind the tool
def calculate_proration(old_plan_price, new_plan_price, days_remaining, days_in_cycle):
    daily_old = old_plan_price / days_in_cycle
    daily_new = new_plan_price / days_in_cycle
    credit  = daily_old * days_remaining          # unused portion of old plan
    charge  = daily_new * days_remaining           # new plan for remaining days
    return round(charge - credit, 2)
```

With the tool wired in, the eval passes — the model does the maths "using the tool in the background and returns the correct response."

### Failure 3.3 — One-sided trade-offs (billing escalation)

**Scenario:** A genuine billing conflict that should be **escalated to a human**.
**Bug:** The bot tries to diagnose and explain the problem itself instead of escalating.

The culprit instruction tells only one side of the story:

```text
Avoid escalating or transferring to a care specialist unless absolutely
necessary, as it costs ~$8 and counts against our fast-resolution contract.
```

With only the *cost* of escalating stated, the model overfits to never escalating. State **both** sides:

```text
Escalating to a care specialist costs ~$8 and counts against our fast-resolution
target — so don't escalate trivially. BUT if you get a billing error wrong, it
can cost a refund AND the customer's trust. When there is a genuine billing
conflict, escalate.
```

> 🔑 **Lesson:** The model "optimizes for a goal." If you give it only one side of a trade-off, it will overfit to that side.
> As models get smarter they make trade-offs *themselves* — so **state both sides** and let them weigh it. (This is the same failure shape as the hotspot patch.)

All five cases now pass. ✅

---

## Part 4 — Building a new agent from scratch

The second scenario: an agent that builds a **week-long retail staff schedule** for 8 employees against hard constraints (head-count per shift, availability, etc.). Building from zero means choosing three things, not one: **prompt + model + harness**.

Because the rules are hard constraints, you don't need an LLM judge — you can grade with a **deterministic Python function** that counts violations:

```python
def count_violations(schedule, employees, requirements):
    """Return the number of hard-constraint violations in a generated schedule."""
    violations = 0
    for shift in requirements:
        assigned = schedule.get(shift.id, [])
        if len(assigned) < shift.required_headcount:
            violations += 1
        for emp_id in assigned:
            if not employees[emp_id].is_available(shift):
                violations += 1
    return violations
```

The talk then walks a **hill-climb** across approaches. Watch how the lever changes at each step:

| # | Approach | Result | Cost / latency |
|--:|---|---|---|
| 1 | **Sonnet 4.6**, simple prompt | All 5 fail; burns tokens, doesn't check its work | baseline |
| 2 | **Opus 4.7**, same prompt | Still fails, but **far fewer violations** — more reasoning helps | similar |
| 3 | **Opus 4.7 + adaptive thinking** (API change only) | **Reliably passes** | ~3× tokens, ~3× latency (~100s) |
| 4 | **Sonnet 4.6 + better prompt** ("check your work before output") | Passes 2/5; failures are now *output-limit* truncations, not rule violations | even more tokens if you raise max_tokens |
| 5 | **Agentic generate→evaluate→repair loop** (3 small prompts) | **All 5 pass** | **lower** tokens & latency than #4 |

Approach 3 needs only an API change:

```python
# Same prompt — just let Opus decide how much to think.
response = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=4096,
    thinking={"type": "adaptive"},   # model chooses its own reasoning depth
    system=system_prompt,
    messages=messages,
)
```

Approach 5 splits one big prompt into **three small, independent prompts**:

```python
def schedule_agent(problem, max_rounds=3):
    schedule = generate(problem)                 # 1. draft a schedule
    for _ in range(max_rounds):
        violations = evaluate(schedule, problem) # 2. LLM lists specific violations + evidence
        if not violations:
            break
        schedule = repair(schedule, violations)  # 3. make targeted fixes
    return schedule
```

> 🔑 **Two viable winners:** *Opus 4.7 + adaptive thinking* **or** the *generate→evaluate→repair loop*. The loop has a bonus: you can inject **soft constraints at runtime** in the evaluate step without touching the deterministic grader — e.g. *"Harry doesn't like working with Sally, separate them where possible"* or *"add a third shift on Wednesday."*

> 💡 **Design principle:** When steps are "easy and repeatable to separate out," isolate them into their own prompts instead of asking one mega-prompt to do everything.

---

## Key takeaways

1. **Evals first.** They're the only way to know whether a prompt change is a real improvement or noise. Cover control, edge, and capability/handoff cases.
2. **Hygiene before heroics.** Structure with XML tags, delete copied-in cruft, and add an output contract — often a free uplift.
3. **Change one thing at a time.** Isolate each failure mode so cause and effect are clear.
4. **Instructions don't add capability.** If the model can't do the task, give it a **tool**, a **bigger model**, more **thinking**, or a **multi-step loop** — don't just tell it to "be careful."
5. **Beware overfitted patches & one-sided rules.** Old defensive instructions ("never...", "always...", ban-lists) can make smarter models *withhold* info or refuse to act. State both sides of trade-offs and let the model decide.
6. **Version-control defensive changes** so you can find and remove them when a new model makes them harmful.

## Common pitfalls

- ❌ Telling the model to "do better" instead of giving it the capability to do better.
- ❌ Long ban-lists / "never do X" stacks that the next model over-optimizes for.
- ❌ One-sided cost statements (mentioning the cost of an action but not the cost of inaction).
- ❌ Leaving website/boilerplate cruft (hero images, cookie notices) in a prompt.
- ❌ Changing several things at once, so you can't tell what helped.
- ❌ Relying on the prompt alone for output format when `stop_sequences` / structured outputs would be more reliable.

---

## 🛠️ Practice project — build **PromptLab**

> This is the main event: the best way to make this lesson stick is to **build the very tool Margo used in the talk** — a small eval workbench — and then use it to harden a real agent end-to-end. *"I five-coded this web app so that we can iterate on the prompt together... I can run my evals on all five test cases and inspect the results."* You're going to build your own. **We'll build this out together** — start as small as a CLI, grow it as far as you like.

### What you'll build

**PromptLab** — an eval-driven prompt workbench, plus the support agent you develop inside it. It has two halves that map exactly to the two halves of this lesson:

1. **The harness** — define test cases, run a prompt against all of them, and see a green/red results grid (like Margo's web app).
2. **The agent** — a support assistant for a fictional company that you take from a broken v0 to all-green by applying every technique in this lesson.

> 🎯 **Pick your domain.** Reuse **Meridian Mobile** (telco) for continuity, or swap in something you find fun — a **gym chain**, a **streaming service**, a **co-working space**. The shape you need: tiered *plans*, a *mid-cycle upgrade* (→ proration math), a *grandfathered/legacy* edge case, and a *dispute* that must be escalated to a human. That single domain naturally exercises every skill below.

### Why this is the perfect practice

| Lesson skill | Where you'll use it in PromptLab |
|---|---|
| Eval suite (control / edge / capability) | Milestone 1 — you can't proceed without it |
| Prompt hygiene (XML, output contract) | Milestone 3 — measure the free uplift |
| Fix overfitted patches | Milestone 4a — the "withheld info" bug |
| Tools > instructions | Milestone 4b — the proration tool |
| State both sides of a trade-off | Milestone 4c — the escalation bug |
| Model / effort selection | Milestone 5 — the from-scratch capability |
| generate → evaluate → repair loop | Milestone 5 — constraint solving |

### Milestones (build incrementally — each one is shippable)

- **M0 · Scaffold.** Project + Anthropic SDK + a `cases.json` (or `.yaml`) with 5 test cases: 1 control, 2 edge, 1 capability/handoff, 1 of your choice. *(Smallest version: a Python script. Bigger: a tiny web UI with a results grid.)*
- **M1 · Eval runner.** A function that runs the current prompt against every case and prints a **pass/fail grid**. This is your instrument panel for everything that follows.
- **M2 · The broken v0.** Write a deliberately messy prompt (one big paragraph, copied-in cruft, an old "never give wrong info → send them to the URL" patch). Run evals → establish a red baseline.
- **M3 · Hygiene pass.** Restructure with `<role>/<guidelines>/<policy>/<tone>`, delete cruft, add an output contract + `stop_sequences`. Re-run → record the uplift.
- **M4 · Target failures one at a time.**
  - **(a)** Fix the withheld-info bug by removing the overfitted patch and trusting the account data.
  - **(b)** Add a `calculate_proration` tool (schema + implementation) so the model stops doing mental math.
  - **(c)** Fix the escalation bug by stating **both sides** of the cost/benefit trade-off.
- **M5 · A from-scratch capability.** Add a second skill to the agent — a **weekly staff scheduler** under hard constraints. Write a deterministic `count_violations` grader, then hill-climb: simple prompt → bigger model → adaptive thinking → **generate→evaluate→repair loop**. Plot violations vs. tokens vs. latency.
- **M6 · Stretch.** Version every prompt and show a **leaderboard** of versions; add an **LLM-judge** grader for tone; allow **soft constraints at runtime** ("keep Harry and Sally on different shifts") without touching the deterministic grader.

### Definition of done

- ✅ All eval cases pass **consistently** (run each a few times — beware variance).
- ✅ You can point to **each change** and show, from the grid, the failure it fixed.
- ✅ At least one case is fixed by a **tool**, and one by **stating both sides of a trade-off** — proving you didn't just "add more instructions."
- ✅ The scheduler passes via the **loop** at lower cost/latency than brute-forcing one mega-prompt.

> 💡 **Keep it honest:** change **one thing at a time** and re-run. If you can't attribute an improvement to a specific change, you've changed too much at once.

---

## Exercises (warm-up drills)

> Smaller drills to do before or alongside the capstone. Work these against a tiny eval harness — even a notebook with 5 test cases and a pass/fail print is enough. Reuse the Meridian scenario or invent your own.

### Exercise 1 — Build the eval first (Foundational)
Write a 5-case eval for a support bot in a domain you know (e.g. a SaaS billing assistant). Make sure you include **one control case, two edge cases, and one capability/handoff case** (where the bot must escalate or refuse). Write down the *expected* answer for each before you write any prompt.

### Exercise 2 — Hygiene pass (Foundational)
Take this deliberately messy prompt and restructure it with `<role>`, `<guidelines>`, `<policy>`, and `<output_format>` tags; remove anything that doesn't belong:

```text
You are a helpful human agent. Our homepage hero banner says "Switch & Save!".
Be nice. Never quote a wrong price, send them to /pricing instead. We accept
cookies. Plans: Lite $10/10GB, Pro $30/50GB. Always get the math right.
```
Run your eval before and after. What changed, and why?

### Exercise 3 — Tool vs. instruction (Intermediate)
Your bot keeps doing arithmetic in its head and getting it slightly wrong. Without changing the model:
(a) write the prompt instruction that points it to a tool, (b) define the tool schema, and (c) implement the tool. Confirm the eval flips from fail → pass. *Reflection:* why couldn't a stronger instruction alone fix this?

### Exercise 4 — Fix a one-sided rule (Intermediate)
Find a "never / always / avoid unless absolutely necessary" line in one of your real prompts. Rewrite it to state **both sides of the trade-off**. Predict how a smarter model would behave under the old vs. new wording, then test it.

### Exercise 5 — Hill-climb a from-scratch agent (Advanced)
Pick a constraint-satisfaction task (scheduling, seating chart, packing). Build a deterministic grader, then climb the ladder yourself: simple prompt → bigger model → adaptive thinking → **generate→evaluate→repair loop**. Plot violations vs. tokens vs. latency for each. Which approach is best for *your* cost/latency budget? Then add a **soft constraint at runtime** in the evaluate step and confirm you didn't have to touch the grader.

---

## Cheat sheet

```
WHEN A PROMPT REGRESSES
  1. Do you have an eval? If not, build one (control + edge + capability).
  2. Hygiene: structure (XML), delete cruft, output contract (+ stop_sequences).
  3. Target ONE failure at a time; re-run after each change.

CHOOSE THE RIGHT FIX (not "more instructions")
  Wrong/withheld facts ...... fix overfitted patch; trust the data source
  Bad math / unreliable step . give a TOOL
  Won't act / over-cautious .. state BOTH sides of the trade-off
  Not smart enough ........... bigger model OR adaptive thinking
  One prompt doing too much .. split into generate → evaluate → repair

REMEMBER
  • Instructions don't add capability.
  • Version-control defensive patches.
  • Smarter models make their own trade-offs — give them both sides.
```

## Connections to the rest of the course

- **← Module 2 · Lesson 4 (Picking the right model):** the "bigger model vs. adaptive thinking" choices here are made rigorously with evals there.
- **← Module 2 · Lesson 5 (The thinking lever):** deep dive on adaptive thinking / effort, the lever used in Part 4.
- **→ Module 3 (Evals for taste):** formalizes the eval suite this lesson depends on (code-based vs. LLM-judge graders).
- **→ Module 5 (Claude Managed Agents):** the generate→evaluate→repair pattern scales into multi-agent orchestration and "outcomes."

---

*Source: "The prompting playbook" by Margo van Laar (Anthropic), Code with Claude 2026, London. Code snippets are illustrative reconstructions of the approaches demonstrated in the talk; adapt model IDs and APIs to the current SDK.*
