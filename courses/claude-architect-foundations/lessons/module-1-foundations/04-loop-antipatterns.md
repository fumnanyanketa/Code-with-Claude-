# Module 1 · Lesson 4: Loop antipatterns and ending the loop correctly

> **Course:** Claude Certified Architect: Foundations, a self-paced course
> **Module 1:** Foundations: how Claude agents work
> **Speaker:** Andrew Brown, ExamPro
> **Source:** Reconstructed from the CCA-F course by Andrew Brown (ExamPro) · [full transcript](../../transcripts/cca-f-full-course.txt)
> **Estimated time:** 30 to 45 minutes (read plus lab)

---

## In one sentence

You end an agent's loop by watching one structured field — `stop_reason` — not by reading the model's prose for words like "done," and you protect yourself from a loop that never ends by adding a maximum-iteration cap with a clean break.

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone
> Project** where you take last lesson's working loop and *harden* it: add a
> max-iteration guard and prove the loop terminates on both a normal finish
> (`end_turn`) and the safety cap. Everything before the Capstone teaches the
> two habits you need there. If you want to see the finish line first, jump to
> the **"Capstone Project"** section, then come back.

> 📝 **This is an EXAM TIP lesson.** As Andrew puts it, "let's look at some
> antipatterns that Anthropic wants you to know about." These are the exact
> loop mistakes the CCA-F exam probes, phrased the way the exam phrases them.
> If you remember only one thing: **use `stop_reason` `end_turn`** to decide
> when to stop — never the text, never the iteration count alone.

## A few plain-language basics first

This lesson uses a handful of terms. Here they are in plain words:

- **Agent:** an AI that takes a series of actions on its own toward a goal, rather than answering in one shot.
- **Agentic loop:** the repeating cycle an agent runs — gather context, take action, verify — until the task is done.
- **Tool / tool call / tool result:** a function the model can choose to run; when it decides to use one that is a *tool call*, and what comes back is the *tool result*.
- **`stop_reason`:** the field the API returns saying *why* the model stopped — `tool_use` (it wants to run a tool) or `end_turn` (it's finished). You drive the loop off this, never off parsing the text.
- **Token:** the unit a model reads and writes in, roughly ¾ of a word; you are billed per token, so every extra loop pass costs real money.
- **Antipattern:** a common "solution" that looks reasonable but reliably causes trouble — worth learning so you can recognise and avoid it.

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

In the previous lesson you built a tool-using loop that runs by hand: call the model, read `stop_reason`, run the tool it asked for, feed the result back, repeat. That loop *worked* — but Andrew was honest that it was rough: "the only part of the code that I think is probably not great is this `while True` loop." A `while True` with no ceiling can run forever, and it is tempting to "fix" it in ways that quietly make things worse. This lesson names the three tempting-but-wrong ways to end a loop, shows why each fails, and gives you the one reliable pattern the exam wants. Getting this right is the difference between an agent that stops cleanly and one that burns your API credits in an infinite loop while you are away from the keyboard.

## Learning objectives

By the end of this lesson you will be able to:

1. Explain why parsing the model's natural-language text to decide "is it done?" is fragile, and name at least two ways it fails.
2. Drive loop termination off `stop_reason` `end_turn` instead of the text or the iteration count.
3. Add a max-iteration cap as a *safety net* (not the primary stop signal) and break out cleanly.
4. Prove a loop terminates on both a normal finish and the safety cap.

## Prerequisites

- **Module 1 · Lesson 3, "Tools and the stop-reason loop"** — you need the working hand-rolled loop from that lesson; this lesson hardens it.
- A Python environment with the Anthropic SDK and an API key (Module 0 set this up).
- Comfort reading a `while` loop and an `if` statement.

---

## Part 1: Don't read the tea leaves — the "parse the text" antipattern

The first temptation is the most natural one. The model finishes talking, and its final message says something like "All done — I've placed the order." So you write code that scans that text for a phrase like "done" or "task complete," and when you see it, you stop the loop.

Andrew's warning is blunt: "when you are going to decide that the loop is over, you do *not* want to just parse natural language ... looking for an indicator from the text that it is complete. What you want to do is check on the `stop_reason` for `end_turn`."

Why is reading the text so fragile? Two reasons.

- **The words can appear by accident.** As Andrew puts it, "maybe these words 'task complete' have something to do not with it being complete, but just in general in the text." Imagine the model writes: "I have not marked this task complete because inventory is low." Your `"task complete" in text` check fires — and you stop the loop right when the model was telling you it is *not* finished.
- **The text is unbounded and unpredictable.** "The output for the text could be anything." The model might say "done," "finished," "all set," "✅," or nothing at all. You cannot enumerate every phrasing, in every language, forever. "There's a lot of points of failure that can happen with parsing natural text specifically for stopping the loop."

Contrast that with `stop_reason`. It is not prose — it is a small, fixed field the API sets to one of a known set of values. "They have a very specific structure like `stop_reason`, and so that's going to be a lot more reliable and give you a better indicator and not be thrown off by the text content."

> 🔑 **To decide *whether the loop is over*, read the structured `stop_reason`, never the free-text answer. Text is for humans; `stop_reason` is for control flow.**

### A nuance, so you don't over-correct

This does *not* mean text is useless. Andrew is careful here: "that doesn't mean that you cannot use text and use regular expressions and `includes` to make decisions on information — though those are brittle." You might read the text to extract a number, a name, or a decision. That is fine (if a little brittle). The rule is narrower and absolute: **for the single job of stopping the loop, use `stop_reason`.**

```python
# Illustrative reconstruction — do NOT do this.
# Antipattern: ending the loop by reading the model's prose.
if "task complete" in response_text.lower():   # fragile: fires on the wrong sentence
    break
```

```python
# Illustrative reconstruction — do this instead.
# Drive control flow off the structured field.
if response.stop_reason == "end_turn":
    break
```

## Part 2: The iteration cap — necessary, but not the stop signal

The second temptation is smarter, and it is half right. You look at your `while True` loop and think: "if it never hits a `false`, it could go forever. So let me put a limit on it — stop after, say, 10 passes."

Adding a ceiling is genuinely good. It is your seatbelt: if everything else fails, the loop cannot run forever and cannot bankrupt you. But — and this is the exam's subtle point — **the cap is a safety net, not the way you normally stop.** Andrew: "you might think, well, let's put an iteration on that, and that would *partially* help the problem. But what if it needed to stop sooner? Because now you're consuming 10 iterations as opposed to if it only needed one or two or three."

If the iteration cap were your *only* stop condition, a task that finishes in 2 passes would still grind through all 10 — eight wasted round-trips, eight tokens bills, for nothing. The cap should almost never be the reason you exit. It should fire only when something has gone wrong.

So the correct design uses **both** signals together:

- **`stop_reason` `end_turn`** is the *primary* exit — you stop the moment the model is actually finished.
- **A max-iteration cap** is the *backstop* — it catches runaway loops the primary exit somehow missed.

As Andrew sums it: "we can still use the max iteration, but we are also going to use that `stop_reason`, and then we're going to provide it that `break` to break out of that loop ... a combination method." And he names the refrain you should hear echoing through this whole module: "you're probably noticing a pattern here, which is use `stop_reason` `end_turn`."

> ✅ **What to do about it:** keep a counter, set an external `MAX_ITERATIONS`
> (e.g., 10), and break when you hit it — *but* make `stop_reason == "end_turn"`
> the exit you expect to fire almost every time. The cap is there for the day it
> doesn't.

## Part 3: "It sent text, so it must be done" — the third antipattern

The last trap looks like a shortcut. You reason: "if I get text back, then surely it must be done — it's not calling tools." So you treat *any* text response as the end of the loop.

Andrew shuts this down too: "that is not necessarily the case, because that structure can return back text in *both* cases" — a message that also contains a tool call still has text in it, and a finished message may or may not have text. Presence of text tells you nothing reliable about whether the model wants to keep going.

Stack the three antipatterns together and the moral is one line. In Andrew's words: "the text could be a misleader, using natural language could be a misleader, using iterations could be a misleader ... we just want to make sure we do `stop_reason` `end_turn`."

Here is the whole decision, as a small diagram:

```text
   call the model  ─────────────┐
        │                       │
        ▼                       │
  read response.stop_reason     │
        │                       │
   ┌────┴─────────────┐         │
   │                  │         │
"tool_use"        "end_turn"    │
   │                  │         │
 run the tool     break ✔ (normal, expected exit)
 append result        │
   │                  │
 iterations += 1      │
   │                  │
 if iterations ≥ MAX ─┴─► break ✔ (backstop, should rarely fire)
   │
   └──────────────────────────► loop again
```

> 🔑 **Three misleaders, one truth: the text can lie, "got text = done" can lie,
> and the iteration count can lie. `stop_reason == "end_turn"` is the signal you
> trust.**

---

## Key takeaways

1. **Stop on the field, not the prose.** Decide the loop is over by reading `stop_reason == "end_turn"`, never by searching the answer text for "done" or "complete."
2. **Text can still inform, just not terminate.** Using regex/`includes` to pull data out of a response is acceptable (if brittle); using it to *end the loop* is the antipattern.
3. **The iteration cap is a seatbelt, not the steering wheel.** A max-iteration break prevents infinite loops and runaway cost, but it should rarely be the reason you exit — `end_turn` should be.
4. **Use both signals together.** `end_turn` for the normal finish, `MAX_ITERATIONS` for the emergency stop, and a clean `break` for each.
5. **"Got text back" proves nothing.** A response can carry text whether or not the model is done, so never treat the mere presence of text as completion.

## Common pitfalls

- ❌ **Ending on a keyword like `"complete" in text`.** It fires on sentences that contain the word for the wrong reason ("I did *not* mark this complete"). Read `stop_reason` instead.
- ❌ **Using the iteration cap as your only exit.** A 2-pass task then burns all 10 passes. Make `end_turn` the primary exit and the cap the backstop.
- ❌ **Hard-coding the cap deep in the loop.** Set it as one clearly named variable at the top (`MAX_ITERATIONS = 10`) so it is easy to find and tune.
- ❌ **Assuming a text response means "finished."** Text can accompany a tool call, too. Only `stop_reason` tells you the model's intent.
- ❌ **Forgetting to increment the counter, or incrementing it on the wrong branch.** If the counter never advances, the cap never trips and you are back to `while True`.

---

## 🛠️ Capstone Project: Harden Atlas Support's loop

> This is the main hands-on project for the lesson. You will take the working —
> but rough — loop from last lesson and make it *safe to leave running*. Keep it
> small: the whole change is a counter, a cap, and a second `break`.

Atlas Support, our north-star project, is still just a single tool-using loop at this stage. Before it grows into a coordinator with many sub-agents, its core loop has to be trustworthy — it must always stop, for the right reason, without wasting tokens. This capstone is the piece Atlas Support will stand on: a loop that provably terminates.

### What you will build

Starting from `model-driven.py` (or your decision-making loop) from Lesson 3, you will create a new `end-loop/main.py` that:

- keeps the `stop_reason == "end_turn"` check as the **primary** exit, with a `break`;
- adds an **external** `MAX_ITERATIONS = 10` variable and a step counter;
- adds a **second** `break` when the counter reaches the cap — the backstop;
- prints each pass's `stop_reason` so you can *watch* the loop decide.

Each piece maps to a lesson idea: the `end_turn` break is Part 1's "stop on the field," the cap is Part 2's "seatbelt," and the second break is Part 3's "both signals, cleanly."

Andrew builds exactly this on camera — he copies the earlier loop, then prompts: "we use a `while` loop, but I would like to have a max iteration of 10, so we set an external var." That is your target.

### Why this is the perfect practice

| Lesson idea | Where you use it in Atlas Support's loop |
|---|---|
| Stop on `stop_reason`, not text (Part 1) | The primary `if response.stop_reason == "end_turn": break` |
| Iteration cap is a backstop (Part 2) | `MAX_ITERATIONS = 10` + `if steps >= MAX_ITERATIONS: break` |
| Both signals, cleanly (Part 3) | Two distinct `break`s, a counter incremented once per pass |
| Proving termination | Running it and watching the loop exit both ways |

### Milestones (build them in order, each one works on its own)

1. **Copy the loop.** Make a new `end-loop/` folder and copy your Lesson 3 loop into `main.py`. Run it once, unchanged, to confirm it still works. As Andrew notes, "notice how much we are reusing our code."
2. **Add the counter and the cap.** At the top of the file, add `MAX_ITERATIONS = 10`. Inside the loop, add `steps += 1` on the tool-use branch. Nothing changes in behaviour yet — you have just wired up the odometer.
3. **Add the backstop break.** After incrementing, add `if steps >= MAX_ITERATIONS: break`. Keep the existing `end_turn` break as the primary exit. You now have two exits.
4. **Prove the normal exit.** Give it a task that finishes in a few tool calls. Confirm the printed `stop_reason` reads `tool_use ... tool_use ... end_turn`, and that the loop exits on `end_turn` *before* hitting the cap. This is the path that should almost always fire.
5. **Prove the backstop.** Temporarily set `MAX_ITERATIONS = 2` (or give it a task it cannot finish) and confirm the loop stops at the cap instead of running forever. Then set it back to 10.
6. **Stretch goals.** (a) When the cap trips, print a distinct message like `"Hit MAX_ITERATIONS — stopping as a safety net"` so the two exits are distinguishable in the logs. (b) Ask yourself Andrew's lingering question — "is there still a little edge case?" — and note what happens if the model returns neither `tool_use` nor `end_turn`. (c) Move the model to Haiku to keep lab costs low, as Andrew keeps reminding himself to do.

### How you will know you are done

- ✅ Your loop has **two** `break`s: one on `stop_reason == "end_turn"`, one on the iteration cap.
- ✅ `MAX_ITERATIONS` is a single named variable at the top of the file, not a magic number buried in the loop.
- ✅ You have run it once and watched it exit on `end_turn` (the normal case) *before* reaching the cap.
- ✅ You have run it once with a tiny cap and watched it exit on the cap instead of looping forever.
- ✅ Nowhere in the loop do you parse the answer text to decide whether to stop.

> 💡 **Keep yourself honest:** the `end_turn` break should be the one that fires
> in normal runs. If your loop routinely exits because it hit the cap, something
> upstream is wrong — the cap is catching a bug, not doing its real job.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice
> on one idea. Optional and independent; the Capstone already touches all of
> them, so feel free to skip straight to it.

### Exercise 1: Spot the misleader (foundational)
Write down three different final messages a model might send — one that says "done" but isn't, one that finishes without any "done"-like word, and one that finishes with text *and* would have called a tool if allowed. For each, state what `stop_reason` you'd expect and why the text alone would mislead you.

### Exercise 2: Two exits, two messages (intermediate)
Extend your capstone so that each exit prints a clearly different line: `"Finished: model returned end_turn"` versus `"Aborted: hit max iterations"`. Run the loop both ways and paste the two outputs side by side to confirm you can tell them apart.

### Exercise 3: Find the edge case (advanced)
Andrew wonders aloud whether "there's still a little edge case" where the loop might not end. Investigate: what does your code do if `stop_reason` comes back as something you didn't handle (e.g., `max_tokens` or `pause_turn`)? Add an explicit branch that logs the unexpected reason and breaks, so an unknown `stop_reason` can never trap you in the loop.

---

## Cheat sheet

```text
ENDING AN AGENTIC LOOP — THE RULES
==================================

THE ONE TRUTH
  Stop the loop on  stop_reason == "end_turn"  — always.

THREE ANTIPATTERNS (the exam's favourites)
  1. Parse the text for "done"/"complete"      -> words appear by accident;
                                                  text is unbounded. FRAGILE.
  2. Iteration cap as the ONLY stop signal     -> wastes passes; a 2-step task
                                                  still runs all 10. BACKSTOP ONLY.
  3. "Got text back, so it's done"             -> text comes back either way.
                                                  Proves nothing.

  Refrain: text can lie · "got text" can lie · iterations can lie.
           stop_reason end_turn is the signal you trust.

THE CORRECT LOOP (both signals)
  MAX_ITERATIONS = 10          # named, external, easy to tune
  steps = 0
  while True:
      resp = call_model(...)
      print(resp.stop_reason)                 # watch it decide
      if resp.stop_reason == "end_turn":
          break                               # PRIMARY exit (expected)
      # ... run the tool, append tool_result ...
      steps += 1
      if steps >= MAX_ITERATIONS:
          break                               # BACKSTOP (should rarely fire)

TEXT IS OK FOR DATA, NEVER FOR STOPPING
  regex / includes to extract a value -> fine (brittle)
  regex / includes to end the loop    -> antipattern
```

## How this connects to the rest of the course

- **Earlier, Module 1 · Lesson 3 ("Tools and the stop-reason loop"):** you built the hand-rolled loop and first met `stop_reason`. This lesson fixes that loop's one weakness — its `while True` had no ceiling.
- **Next, Module 2 ("Prompting that steers the model"):** with a loop that reliably starts and stops, you turn to controlling *what* the model does inside it — few-shot examples and goal-based prompting.
- **Later, Module 3 ("Refinement loops and observability"):** the same max-iteration discipline scales up — a coordinator that re-delegates gaps needs exactly this cap so its refinement loop can't spin forever. And in Module 2 · Lesson 6 you'll meet a *related* infinite-loop trap: forcing `tool_choice: "tool"` and never letting the model reach `end_turn`.

---

*Source: "Claude Certified Architect: Foundations" by Andrew Brown, ExamPro. Code snippets and diagrams are illustrative reconstructions of the patterns described in the course. Adapt them to the current SDK.*
