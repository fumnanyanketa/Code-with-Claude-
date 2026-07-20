# Module 6 · Lesson 23: Managing the context window

> **Course:** Claude Certified Architect: Foundations, a self-paced course
> **Module 6:** Context management & reliability: keep sessions cheap, honest, and trustworthy
> **Speaker:** Andrew Brown, ExamPro
> **Source:** Reconstructed from the CCA-F course by Andrew Brown (ExamPro) · [full transcript](../../transcripts/cca-f-full-course.txt)
> **Estimated time:** 30 to 45 minutes (read plus lab)

---

## In one sentence

Every session has a fixed token budget called the context window; `/context` shows you exactly how that budget is being spent (including a ~22% slice Claude Code holds back for auto-compaction), and `/compact` and `/clear` are the two deliberate tools you use to reclaim that space — one summarizes, one wipes.

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone
> Project** where you instrument Atlas Support: you fill up a session's context
> on purpose, read the `/context` breakdown to see where the tokens went,
> `/compact` to reclaim space, and measure exactly how much you got back.
> Everything before the Capstone teaches you to read that budget and spend it on
> purpose. If you want to see the finish line first, jump to the **"Capstone
> Project"** section, then come back.

## A few plain-language basics first

This lesson uses a handful of terms. Here they are in plain words:

- **Token:** the unit a model reads and writes in, roughly ¾ of a word; you are billed per token, so every token in the conversation costs something.
- **Context window:** how much text (in tokens) the model can hold in mind at once. Think of it as the desk the model works on — finite surface area, and once it is full, something has to come off.
- **Session:** a saved conversation you can resume or fork (branch) non-destructively — the thing whose context you are managing here.
- **Compaction:** replacing a long conversation history with a shorter *summary* of it, to free up room while keeping the gist.
- **Auto-compaction:** Claude Code doing that summarizing *for you* automatically when the window gets close to full.
- **Auto-compact buffer:** a reserved slice of the context window (~22%) that Claude Code keeps empty so it always has room to write that summary.

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

Two lessons ago you learned that a runaway loop burns tokens — "the text could be a misleader ... iterations could be a misleader." The context window is the same cost story from a different angle: as a conversation grows, it consumes more tokens, and as Andrew puts it, "larger conversations ... consume more tokens, that equals greater cost with your API usage, or you're going to run out of your subscription usage — that five-hour window — a lot sooner than you think." A long session is not free just because you are on a subscription; it eats your rate limit. This lesson gives you the instrument to *see* that spend (`/context`) and the two levers to control it (`/compact`, `/clear`) — so you stop guessing and start managing the budget on purpose. Andrew flags that this pays off later: "later in the course you'll see me use it a lot more as I start to think, okay, how much usage do we have?"

## Learning objectives

By the end of this lesson you will be able to:

1. Read the `/context` command's token breakdown and name what each category (system prompt, skills, messages) is consuming.
2. Explain the ~22% auto-compact buffer and why Claude Code reserves it.
3. Describe what auto-compaction does and when Claude Code triggers it on its own.
4. Choose deliberately between `/compact` (summarize to reclaim space) and `/clear` (wipe the conversation) — and know the cautions on `/clear`.
5. Measure how much context you reclaimed by comparing `/context` before and after.

## Prerequisites

- **Module 6 · Lesson 22, "Sessions — resume, fork, and rewind"** — you need to be comfortable starting, resuming, and switching between sessions; `/context` reports on *whichever session you are in*.
- A working Claude Code install (Module 5 set this up) and a project you can open it in.
- The cost intuition from **Module 1 · Lesson 4** ("loop antipatterns") — that tokens are money.

---

## Part 1: The context window is a budget, and `/context` is the receipt

Start with the mental model. The model can only hold so much text in mind at once — that ceiling is the **context window**, measured in tokens. Everything in your session shares that one budget: the hidden system prompt, any skills that got loaded, and every message you and Claude have exchanged. When it fills, you are out of room.

The `/context` command is how you read that budget. In Andrew's words, "context shows tokens consumed in the current session and available tokens broken down by category." Two words there matter. *Current session* — it reports on wherever you are right now, not globally. And *broken down by category* — it does not just give you one number, it itemizes where the tokens went.

Run it in a brand-new session and there is almost nothing to see: "when we have a new session ... basically all the space is available. In fact, the only thing that's taking up any room is the skills being loaded into here" — plus the auto-compact buffer (Part 2). A fresh desk is empty except for the tools you laid out on it.

Run it in an older, worked-in session and you get the real picture — "a breakdown of information in terms of what it's utilizing." Andrew reads it off:

| Category | What it is | Typical size early on |
|---|---|---|
| **System prompt** | The hidden instructions Claude Code always sends | Fixed, modest |
| **Skills** | Any skills loaded into the session | "really small here" |
| **Messages** | Your actual back-and-forth conversation | Grows as you work |
| **Auto-compact buffer** | Reserved headroom (see Part 2) | ~22%, held back |

> 🔑 **`/context` is a receipt, not a setting. It tells you where your token
> budget is being spent right now, itemized — so you can decide whether you need
> to reclaim space before you run out.**

### It is per-session — so it changes when you switch

A detail Andrew verifies live: the breakdown "absolutely does change with your session. So if you switch over to a previous session, you're going to get different information." If you resume or switch sessions and re-run `/context`, the numbers move, because you are now looking at a different conversation's budget. This is exactly why he pairs it with resume: "a really great way ... when you're using the resume flag to continue a previous session, then often you'll run the context here to see the size of it."

> 💡 **The CLI shows a nicer breakdown than the IDE.** Andrew notes the same
> command "in the CLI" gives the clean stacked breakdown, while the IDE version
> "is not as nice — it says how much we have here, but it's not as nice as the
> one in the CLI." If your `/context` output looks thin, try it in the terminal.

## Part 2: The ~22% auto-compact buffer — headroom Claude keeps for itself

Look closely at a `/context` readout and you will see a chunk labelled for auto-compaction, even in a brand-new session. That is the **auto-compact buffer**, and it is not wasted space — it is deliberate insurance.

Andrew's definition: "auto-compact buffer is Claude Code reserving a portion of the context window — so 22% of it — that ensures there's enough headroom to summarize conversation history when the limits are approached. So very, very useful feature."

Here is why it has to exist. Summarizing a long conversation is itself a piece of work the model has to do, and doing work takes room. If Claude let the window fill to 100% and *then* tried to write a summary, there would be no space left to write it in — like trying to tidy a desk that is already buried under paper with nowhere to set the tidy pile. So Claude Code fences off ~22% up front and never lets your conversation spill into it. When you approach the limit, that reserved slice is the workspace it uses to compact.

```text
CONTEXT WINDOW (one session's total budget)
┌───────────────────────────────────────────────────────────┐
│ system │ skills │ messages ....................... │ ~22% │
│ prompt │        │ (grows as you work)              │ AUTO │
│        │        │                                  │COMPACT│
│        │        │                                  │BUFFER │
└───────────────────────────────────────────────────────────┘
                                                     └──┬───┘
                          reserved headroom Claude keeps empty so it
                          always has room to write a summary when full
```

> 🔑 **The 22% buffer is not room you lost — it is room Claude saved so it can
> rescue you. It is the reason auto-compaction can happen at all.**

## Part 3: Auto-compaction, `/compact`, and `/clear` — three ways to reclaim space

When a conversation gets big, something has to give. You have three levers, from most automatic to most destructive.

### Auto-compaction (Claude does it for you)

Left alone, "Claude Code is going to do auto-compaction. So technically it will take care of itself at those larger sizes." When the messages approach the limit, Claude uses that reserved buffer to summarize the history down to a shorter form and keeps going. You do not have to do anything. This is the default safety net.

### `/compact` (you trigger the summary early)

Sometimes you do not want to wait for the automatic trigger — you want to reclaim room *now*, while staying in the same conversation. That is `/compact`. It does the same thing auto-compaction does, on demand: replaces the long history with a summary. After it runs you will see a note like "conversation compacted" (Andrew: "control-O for history" shows what was rolled up). Re-run `/context` and, as he observes, "it is much, much smaller." You keep the thread of what you were doing; you just shed the token weight of every verbatim exchange.

### `/clear` (you wipe the conversation entirely)

`/clear` is the blunt instrument. It does not summarize — it "clears the conversation history and free[s] up context," starting over from scratch. After a `/clear`, `/context` shows "basically just one thing." Use it when you are genuinely done with a line of work and want a clean slate, not when you want to keep going.

> ✅ **What to do about it:** reach for `/compact` when you want to *keep working*
> but reclaim space, and `/clear` only when you are *finished* with this
> conversation and want to start fresh. Compact preserves the gist; clear throws
> it away.

| | Auto-compaction | `/compact` | `/clear` |
|---|---|---|---|
| Who triggers it | Claude, automatically | You, on demand | You, on demand |
| What it does | Summarizes history | Summarizes history | Deletes history |
| Keeps the gist? | Yes | Yes | **No** |
| When to use | Always on, background | Reclaim space, keep going | Done — clean slate |

### The cautions on `/clear`

Two warnings Andrew repeats, because "a lot of people get mixed up on" them:

- **`/clear` does not touch your `CLAUDE.md` or auto-memory.** "Clear will not clear out your CLAUDE.md files or your auto-memory." It wipes the *conversation*, not your project's persistent instructions. Those survive.
- **Do not type `clear` out of Linux muscle memory.** In a normal terminal, `clear` (or `cls`) just wipes the *screen*. In Claude Code, "this will literally clear out — like delete — the conversation and start it over from scratch." As Andrew warns mid-lab: "I'm so tempted to type clear, but clear is going to clear the conversation ... you really don't want to type that." One reflexive keystroke can throw away a conversation you cared about.

> ❌ **The classic trap: typing `clear` to tidy your screen and deleting your
> whole conversation instead. In Claude Code, `/clear` is a delete, not a
> screen-wipe.**

There is a reliability angle too. Andrew recounts a session "at the max" where his WSL2 environment "hung and I had to restart it completely." Long, near-full sessions are more fragile; keeping context lean with `/compact` is partly about *not* living permanently at the edge of the budget.

---

## Key takeaways

1. **The context window is a shared, finite budget.** System prompt + skills + messages all draw from one token pool per session; when it fills, you are out of room.
2. **`/context` is your receipt.** It itemizes where tokens went, it is per-session (switch sessions, the numbers change), and the CLI view is cleaner than the IDE view.
3. **The ~22% auto-compact buffer is reserved on purpose.** Claude keeps that headroom empty so it always has room to summarize when the window fills.
4. **Auto-compaction is the default net; `/compact` is you pulling it early.** Both summarize the history to reclaim space while keeping the gist.
5. **`/clear` is a delete, not a summarize.** It wipes the conversation (but not `CLAUDE.md` or auto-memory) — use it only for a clean slate, and never out of Linux screen-clearing habit.
6. **Big sessions cost real money and rate-limit budget** — and are more fragile. Managing context is the same cost discipline as ending a loop cleanly.

## Common pitfalls

- ❌ **Treating a subscription as "free tokens."** A long session still eats your five-hour usage window "a lot sooner than you think." Watch `/context`.
- ❌ **Typing `clear` to clean your screen.** In Claude Code that deletes the conversation. If you only want a tidy screen, that is not the command you want.
- ❌ **Thinking `/clear` erases your project memory.** It does not touch `CLAUDE.md` or auto-memory — only the conversation. (Some people avoid `/clear` for the wrong reason because of this confusion.)
- ❌ **Reaching for `/clear` when you meant `/compact`.** If you still need the thread of what you were doing, compact it — clearing throws the gist away.
- ❌ **Reading `/context` in one session and assuming it applies to another.** The breakdown is per-session; re-run it after you switch or resume.
- ❌ **Waiting until the window is 100% full to act.** Near-max sessions are slower and more prone to environment hangs — compact before you hit the wall.

---

## 🛠️ Capstone Project: Instrument Atlas Support's context

> This is the main hands-on project for the lesson. You will treat one Atlas
> Support session like an instrument panel: fill it up, read the gauges, compact,
> and measure exactly what you reclaimed. Keep it small — the point is the
> measurement discipline, not the task you run.

Atlas Support, our north-star support system, will eventually run long, multi-step sessions — reading tickets, calling tools, escalating to a human. Long sessions are exactly where context management stops being optional. This capstone is the piece Atlas Support will stand on: the habit of *reading the budget before it bites you*. You are not building a feature here; you are building the instinct to instrument.

### What you will build

Working inside one Claude Code session on your Atlas Support project, you will:

- record a **baseline** `/context` reading on a fresh session, and locate the ~22% auto-compact buffer in it;
- **fill the context on purpose** by giving Claude a big, sprawling task (Andrew's trick: "I want you to port the app over to Rust ... I just want to fill up the context");
- read the **filled** `/context` breakdown and name what grew (it will be the *messages* category);
- run `/compact`, then re-read `/context` and **measure the reclaim** (before minus after);
- run `/clear` on a throwaway copy of the session and confirm `/context` drops to "basically just one thing."

Each piece maps to a lesson idea: the baseline reading is Part 1, spotting the buffer is Part 2, and compact-then-measure-then-clear is Part 3.

### Why this is the perfect practice

| Lesson idea | Where you use it in Atlas Support |
|---|---|
| Read the `/context` breakdown (Part 1) | Baseline and filled readings; naming which category grew |
| The ~22% auto-compact buffer (Part 2) | Locating the reserved slice in the readout |
| `/compact` reclaims space (Part 3) | The before/after measurement of tokens freed |
| `/clear` wipes to a clean slate (Part 3) | Confirming context drops to ~one item |
| Big sessions cost money (Why it matters) | Noting your session usage % climb as you fill it |

### Milestones (build them in order, each one works on its own)

1. **Baseline reading.** Start a fresh session in your Atlas Support project and run `/context`. Note the numbers: near-empty except skills and the auto-compact buffer. Write down the total used. *This milestone stands alone — you have already learned to read the receipt.*
2. **Find the 22%.** In that same readout, point to the auto-compact buffer slice. Confirm it is there even though you have barely used the session, and note roughly what fraction of the window it is. *Stands alone — you can now spot the reserved headroom.*
3. **Fill it on purpose.** Give Claude a deliberately large task that generates a lot of conversation — Andrew ports a whole app to another language just to bulk up the history. Anything sprawling works; you are "not actually trying to make this work," only to grow the context. Let it run. *Stands alone — you have produced a big session.*
4. **Read the filled breakdown.** Run `/context` again. Identify which category grew (it will be *messages*) and by how much versus your baseline. While you are here, check your session usage % — Andrew notes he was "at 28% for the session." *Stands alone — you have measured a full budget.*
5. **Compact and measure the reclaim.** Run `/compact`, wait for "conversation compacted," then run `/context` once more. Compare to Milestone 4: Andrew's verdict is "it is much, much smaller." Write down `before − after` — that number is what you reclaimed. *Stands alone — this is the core skill.*
6. **Clear on a throwaway.** On a session you do *not* need to keep, run `/clear`, then `/context`. Confirm it collapses to "basically just one thing," and confirm your `CLAUDE.md` / auto-memory is untouched. *Stands alone — you have seen the blunt instrument safely.*
7. **Stretch goals.** (a) Keep a tiny log — `baseline / filled / compacted` token totals — so you can see the shape of the spend. (b) Resume an *older* session, run `/context`, and confirm the breakdown differs from your current one (proving it is per-session). (c) Deliberately let a session grow until auto-compaction fires on its own, and compare that to your manual `/compact`.

### How you will know you are done

- ✅ You have a **before and after** `/context` reading around a `/compact`, and you can state the token difference you reclaimed.
- ✅ You can point to the auto-compact buffer in a readout and say roughly what % it is (~22%).
- ✅ You correctly named which category (*messages*) grew when you filled the context.
- ✅ You ran `/clear` on a throwaway session and watched `/context` drop to ~one item.
- ✅ You did **not** accidentally `/clear` a session you wanted to keep, and you can explain why `/clear` did not erase your `CLAUDE.md`.

> 💡 **Keep yourself honest:** the whole exercise is worthless if you do not
> record the *numbers*. "Compacted and it felt smaller" is a vibe; "18,400 → 4,100
> tokens" is a measurement. Write both readings down before you move on.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice
> on one idea. Optional and independent; the Capstone already touches all of
> them, so feel free to skip straight to it.

### Exercise 1: Read the receipt (foundational)
Open any project in Claude Code, run `/context`, and write out each category you see (system prompt, skills, messages, auto-compact buffer) with its size. In one sentence, say which one you expect to grow as you work — and why.

### Exercise 2: Compact vs. clear, decided out loud (intermediate)
Write three short scenarios: (a) you are mid-debug and running low on room, (b) you just finished a task and want to start something unrelated, (c) you want a tidy screen. For each, say whether you would use `/compact`, `/clear`, or neither, and justify it in one line. (Answer key: compact, clear, neither — `/clear` is *not* a screen-wipe.)

### Exercise 3: Prove it is per-session (advanced)
Fill up one session, note its `/context` total, then resume a different, older session and run `/context` there. Confirm the numbers differ. Then switch back and confirm the first session's numbers are unchanged. Write one sentence explaining why `/context` is a per-session receipt, not a global one.

---

## Cheat sheet

```text
MANAGING THE CONTEXT WINDOW
===========================

THE MODEL
  Context window = one finite token budget per session.
  Shared by:  system prompt + skills + messages.
  Full window = out of room = auto-compaction kicks in.

/context  — READ THE BUDGET (do this often)
  Shows tokens used + available, BROKEN DOWN by category.
  Categories:  system prompt | skills | messages | auto-compact buffer
  PER SESSION — switch/resume a session, the numbers change.
  CLI view is cleaner than the IDE view.

AUTO-COMPACT BUFFER  (~22%)
  Reserved headroom Claude keeps EMPTY.
  Why: it needs room to WRITE the summary when the window fills.
  Not wasted space — it's the reason auto-compaction can happen.

RECLAIMING SPACE — three levers
  auto-compaction   Claude does it for you near the limit   (summarize)
  /compact          you trigger the summary early            (summarize, KEEP gist)
  /clear            you wipe the conversation                 (DELETE, clean slate)

  after /compact  -> /context is "much, much smaller"
  after /clear    -> /context is "basically just one thing"

/clear CAUTIONS
  - Does NOT delete CLAUDE.md or auto-memory (only the conversation).
  - NOT a screen-wipe. In Linux `clear` tidies the screen;
    here it DELETES the conversation. Don't type it out of habit.

MEASURE, DON'T GUESS
  reclaimed = /context(before) - /context(after)
  Big sessions cost tokens = money + eat your 5-hour usage window.
```

## How this connects to the rest of the course

- **Earlier, Module 6 · Lesson 22 ("Sessions — resume, fork, and rewind"):** you learned to move between sessions; this lesson gives you the gauge (`/context`) for reading each one's budget, which is why Andrew pairs `/context` with `resume`.
- **Earlier, Module 1 · Lesson 4 ("Loop antipatterns"):** the same cost theme — tokens are money, a runaway loop or a bloated session both burn them. Context discipline is loop discipline at the session scale.
- **Next, Module 6 · Lesson 24 ("Reliability I — human review, confidence, and synthesis"):** with sessions you can measure and keep lean, you turn to trusting their *output* — checking Claude's work, its confidence, and how it synthesizes results.
- **Later, in the multi-agent build:** coordinators and sub-agents each carry their own context. Knowing how to read and reclaim one session's budget is what lets Atlas Support run long, escalating support flows without going broke or hitting the wall.

---

*Source: "Claude Certified Architect: Foundations" by Andrew Brown, ExamPro. Code snippets and diagrams are illustrative reconstructions of the patterns described in the course. Adapt them to the current SDK.*
