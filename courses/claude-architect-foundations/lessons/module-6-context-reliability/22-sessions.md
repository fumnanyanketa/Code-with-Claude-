# Module 6 · Lesson 22: Sessions — resume, fork, and rewind

> **Course:** Claude Certified Architect: Foundations, a self-paced course
> **Module 6:** Context management & reliability: keep long-running agents correct, cheap, and trustworthy
> **Speaker:** Andrew Brown, ExamPro
> **Source:** Reconstructed from the CCA-F course by Andrew Brown (ExamPro) · [full transcript](../../transcripts/cca-f-full-course.txt)
> **Estimated time:** 40 to 55 minutes (read plus lab)

---

## In one sentence

A **session** is a saved conversation you can pick up later — you **resume** it to keep going, **fork** it to branch off a non-destructive copy and try a different direction without touching the original, and **rewind** it to roll the same conversation back to an earlier point — and you learn all of this by verifying where sessions actually live on disk instead of trusting the docs.

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone
> Project** where you take one Atlas Support session, fork it into two parallel
> branches to try two different fixes at once, then rewind one branch when it
> goes wrong. Everything before the Capstone teaches the four moves — resume,
> fork, rewind, rename — and the judgment call you hit when Python's SDK is
> missing a feature. If you want to see the finish line first, jump to the
> **"Capstone Project"** section, then come back.

## A few plain-language basics first

This lesson leans on a few terms from earlier lessons and adds a couple of new ones. In plain words:

- **Session:** a saved conversation you can resume (keep going) or fork (branch) non-destructively. Every session has its own **session ID** — a unique string that names it.
- **Claude Code:** Anthropic's agentic coding tool (a CLI/harness) that runs the agentic loop over your codebase. When you type `claude`, you start a new session.
- **Anthropic SDK vs Claude Agent SDK:** the *Anthropic SDK* is the lower-level library for calling the model API directly; the *Claude Agent SDK* is the higher-level library for building agents. **The Python Agent SDK sometimes lags the TypeScript one** — which is the whole drama of Part 2.
- **Context window:** how much text (in tokens) the model can hold in mind at once. A **token** is the unit a model reads and writes in, about ¾ of a word; you are billed per token. Session size is measured in tokens, so a bigger session costs more to resume.
- **Fork (branch):** make a copy of a session at its current point and continue in the copy, leaving the original untouched. Borrowed from version control, where "forking" a project means copying it to work on independently.
- **Rewind:** roll a *single* session backward to an earlier message, discarding what came after — like an undo for a conversation.

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

Everything you have built so far assumed a conversation lives for exactly as long as one program run. Real work is not like that. You start something, close the laptop, come back tomorrow, realise you took a wrong turn, and want to go back three steps without losing the good parts — or try two ideas side by side and keep the winner. Sessions are how an agent survives across time and how you explore *cheaply*: forking lets you test two approaches from a shared starting point instead of re-running everything twice. This lesson is also where Andrew hits one of the course's recurring truths head-on. The docs and even Claude's own answers were *wrong* about how to fork a session, and the only way he got to the truth was to build it, port it, and check the files on disk. As he puts it: "what we read and what's generated out is not what is actually true... Don't watch, do and verify yourself."

## Learning objectives

By the end of this lesson you will be able to:

1. Explain what a session is, and the difference between a **web** session and a **local** one.
2. Resume a previous session with `--resume` (or `/resume`) and read its size to gauge cost.
3. Fork a session non-destructively with `--fork-session` (or `/fork`) and explain why the original is untouched.
4. Recognise an **SDK gap** — a feature present in TypeScript but missing in Python — and make the port-to-TypeScript judgment call.
5. Rename a session, and rewind/restore it to an earlier point.
6. Verify where sessions are stored on disk instead of trusting the documentation.

## Prerequisites

- **Module 1 · Lesson 3 (Tools and the stop-reason loop)** and the agentic-loop lessons — a session is that loop's saved history.
- **Module 5 (Claude Code config)** — you should be comfortable launching `claude` and running slash commands.
- Claude Code installed, plus the Claude Agent SDK for both **Python** and **TypeScript** (you will need Node.js for the TypeScript port — Andrew does not teach installing Node here, so have it ready).

---

## Part 1: What a session actually is

Andrew's definition is refreshingly plain: "a Claude Code session is functionally a conversation to the Claude Code agent. And resuming a session is the same as resuming a previous conversation."

That is the whole idea. A session is a saved conversation — the full back-and-forth of prompts, tool calls, and results — stored so you can come back to it. Every time you type `claude`, "you are starting a new session." Each session carries its own **session ID**, a unique string that names it on disk.

There are **two types** of session, and which one you get depends only on *where the conversation started*:

| Type | Where it starts | Andrew's note |
|---|---|---|
| **Local** | The terminal or your IDE, running on your machine | Scoped to the specific project you are in |
| **Web** | Claude Code for web, or remote control | Shows up more broadly, across projects |

"If you start it via remote control or via Claude Code for web then it will be a web session." The interesting wrinkle: in the VS Code extension you can **resume a web conversation into a local one**. That makes sense once you see the point of remote control — "the idea is to trigger it over web to then run your machine." Where the session *originated* is recorded, even if you continue it somewhere else.

> 🔑 **A session is just a saved conversation with a unique ID. "Resuming a
> session is the same as resuming a previous conversation." Web vs local only
> tells you where it started.**

## Part 2: The SDK gap — fork_session exists in TypeScript, not Python

Now the hard-won lesson. **Forking** a session means branching a single conversation at some point into separate sessions that "explore those things independently at the same time." Andrew lays out the properties:

- Each branch gets its **own session history and its own UUID** (a session ID).
- Each branch's state is **saved**, so you can resume it later.
- Branches **run in parallel**, so results come back quicker.
- Branches are **isolated** — they do not share knowledge with each other.

In the Claude Agent SDK this is a function called `fork_session`. Here is the catch, in Andrew's words: it is "only available... in TypeScript at this time. It's not available in Python. I have no idea why the Python one is so far behind."

This is exactly the recurring theme of the course, and it played out live. Andrew asked Claude for a Python code example using `fork_session` and "literally was arguing with it for like 15 minutes and it just refuses to make a code example." Claude kept insisting on an `options` object with a `fork_session` *option* rather than the real function — because, in Python, that is genuinely all there is. The AI's confident answer was not the truth. Only when Andrew pushed did the real story surface: "if you wanted to use the Agent SDK session system... TypeScript has the `fork_session` session ID which branches a session at its current point, but that isn't in the Python one."

### The judgment call: recognise the gap, then port

This is the skill worth naming. When a feature you need lives in the TypeScript SDK but not the Python one, you have a decision to make — and the right move here was **port the code to TypeScript**. Andrew's instruction was simply: "Port my code to TypeScript and let's use that feature." Claude kept the `main.py` around and produced a `main.ts` that imports `fork_session` from the Claude Agent SDK and runs on Haiku ("Which model is being used? Haiku. Good. Because I want to save money").

```text
Illustrative shape of the TypeScript fork (reconstructed):

  import { query, forkSession } from "@anthropic-ai/claude-agent-sdk";

  // 1. Build ONE baseline conversation (the shared starting point)
  const baseline = await query({ prompt: "Analyze the EV market briefly.",
                                 options: { model: "claude-haiku-..." } });

  // 2. Fork it into isolated branches, each with its own session/UUID
  const branches = [
    "Most optimistic 5-year adoption scenario?",
    "Most pessimistic scenario?",
    "How could regulation reshape it?",
  ];
  await Promise.all(branches.map(q =>
      forkSession(baseline.sessionId, q)   // branches at the baseline point
  ));                                        // run in parallel, isolated
```

The payoff, once it ran: "forking into three isolated branches concurrently... it's holding three separate sessions," each able to be picked up later by its own UUID. Andrew's honest read on *why* you would do this over the hub-and-spoke research pattern from Module 3: "parallelization obviously is going to give us a huge advantage in terms of getting results quicker. We're going to burn through more credits."

> ❌ **The trap:** trusting Claude's (or the docs') answer that a Python `options:
> { fork_session }` is the feature. It is not the same as the TypeScript
> `fork_session` function. When the SDKs disagree, the SDK — not the chatbot — is
> the source of truth.

> ✅ **What to do about it:** when a feature is missing in Python, check whether
> TypeScript has it, and if the feature matters, port. "Hopefully you're
> comfortable moving between languages." A small language detour beats
> hand-rolling a feature the SDK already ships.

## Part 3: Resuming — pick a conversation back up

Resuming is the everyday move, and it is "very straightforward." Two ways in:

- **In the terminal:** run `claude --resume` (Andrew always types `resume`, never `continue`, though "continue, resume, it's the same thing"). Inside a session you can use the `/resume` slash command.
- **In the IDE:** the VS Code extension shows a **Conversations** list — "conversations, which is the same thing as sessions" — split into local and web. Click one to teleport back in.

When you kill a session in the terminal, Claude Code prints a `--resume` line with a session ID so you can jump straight back. (Andrew notes an honest gap: "I have no idea how you get the session IDs or list them" from the CLI — most people just use the interactive picker.)

The resume picker is genuinely useful because **it shows the size of each session**. "Notice that it shows you the size of it. So you have an idea of how much of the... conversation is at that given point." Session size is measured in tokens, and tokens are what you pay for, so size is a rough cost-and-context gauge before you even reopen the thing. A few keys inside the picker:

```text
In the resume picker:
  Ctrl+A   show ALL projects (not just the current folder)
  Ctrl+B   toggle branch
  Ctrl+V   preview a session
  (also)   rename right from the list
```

> 💡 **A habit worth copying:** right after resuming, run `/context` (next lesson)
> to see how big the conversation is. "When you're using the resume... flag to
> continue a previous session, then often you'll run the context here to see the
> size of it."

> 🔑 **Resume = keep going in the same conversation. The picker shows each
> session's size in tokens, which is your quick read on cost and context.**

## Part 4: Forking — a non-destructive branch

Forking is resuming's careful cousin. Andrew's definition: forking "allows you to resume a previous session **without affecting the original session**." When you fork, "it's going to basically branch off as a new conversation with its own session ID." The original sits there, untouched, exactly as you left it.

Two ways to fork:

- **In the terminal:** `claude --fork-session` (with `--resume` to pick which session to branch).
- **Inside a session:** the `/fork` slash command. Andrew almost missed it — "I'm not sure if they have a fork command here. Do they have a fork command? They do." — and it was not in his own slides, another reminder to check the tool, not the notes.

In his lab, Andrew had Claude "code me Flappy Bird in a new folder using JavaScript," let it finish, then ran `/fork`. "Now it's forked that conversation. And we can see there's the original one here." In the fork he asked, "can you check the Flappy Bird game for bugs?" — and now there were clearly **two conversations**: the original "code Flappy Bird" one and the new bug-checking branch, side by side. "We could probably rename it so we can distinguish it if we were working on another fork. But really that's all it takes to fork something."

```text
                 code Flappy Bird
                 (original session, UNTOUCHED)
                        │
                     /fork            ← branch at this point
                        │
                        ▼
                 check Flappy Bird for bugs
                 (new session, own ID — a copy that diverges)
```

Why this matters for cost and safety: you explore a risky idea in the fork. If it works, keep it; if it does not, throw the fork away and your original is still pristine. That is the "non-destructive" promise, and it is why forking pairs so well with parallel exploration — one shared starting point, several cheap branches.

> 🔑 **Fork = branch a copy at the current point, with its own ID, leaving the
> original untouched. Resume changes a conversation; fork protects it.**

## Part 5: Rename and rewind — label it, or roll it back

Two smaller commands round out session control.

**`/rename`** simply renames the current session. Andrew is candid that this is a discipline he needs to build: "I do find it very hard to distinguish those conversations." Unnamed sessions all look alike in the resume picker; a name ("maths", "atlas-refund-fix") is the difference between finding the right one and guessing. He also flags a housekeeping fact to plan around: **sessions are kept for about 30 days**, and backing them up beyond that is something to look into if it matters to you.

**`/rewind`** "will restore a session to an older point in time." Unlike a fork (which makes a *new* branch), rewind stays in the *same* session and rolls it *backward* — "literally you are clearing out to that point and continuing on from that point." When you rewind, Claude offers a choice: **restore the conversation** or **summarize from here**.

Andrew's lab makes it concrete. He started a session, renamed it "maths" straight away, then set low effort on Haiku and ran a string of `1 + 1`, `2 + 2`, ... prompts. He checked `/context` (822 tokens), ran `/rewind`, chose an earlier point (`2 + 2`), picked **restore conversation**, and checked context again — "the token count is much... well, it's not that much smaller, but is smaller." The warning that comes with the power: "if you cannot afford to lose that other stuff, you know, just don't go too far back." Rewind *discards* what came after the point you land on.

| Command | What it does | New session? | Destructive? |
|---|---|---|---|
| `--resume` / `/resume` | Continue an existing conversation | No | No |
| `--fork-session` / `/fork` | Branch a copy at the current point | **Yes** (new ID) | No (original safe) |
| `/rename` | Label the current session | No | No |
| `/rewind` | Roll the current session back to an earlier point | No | **Yes** (loses what came after) |

> 🔑 **Fork branches sideways into a new session; rewind moves backward inside
> the same one and drops what came after. Choose fork when you want to keep both
> paths, rewind when you want to abandon a path.**

## Part 6: Verify where sessions live — don't take the docs' word

The thread tying this lesson together is verification, and Andrew models it literally. Testing whether the Agent SDK (not just Claude Code) even *has* resume and fork, he built a small project, ran a session that fixed some buggy Ruby, then resumed it by session ID, then forked it — and asked the one question that settles arguments: "What I'm going to be interested in is where is it storing this information? That's what I want to know."

So he went looking on disk. He found a sessions folder with "three sessions here. I don't think that we would have had three sessions before." Then the decisive move: "I'm just going to delete these files out and run it again, because if they generate in here, then we know **absolutely** that that is what is going on." Delete, re-run, watch the files reappear — proof, not a claim from a doc.

This is the same discipline that cracked the `fork_session` mystery. The documentation was incomplete, Claude's answer was wrong, but the *files on disk* and the *SDK source* do not lie.

> ✅ **What to do about it:** when you want to know how a session behaves, find
> where it is stored, delete the files, re-run, and watch what regenerates. "Just
> because it said it did, it does not mean it did." The disk is the truth.

---

## Key takeaways

1. **A session is a saved conversation with a unique ID.** "Resuming a session is the same as resuming a previous conversation." New `claude` = new session.
2. **Web vs local only marks where a session started.** You can resume a web session into a local one in the IDE.
3. **Resume keeps going; fork branches non-destructively.** `--fork-session` / `/fork` makes a new session with its own ID and leaves the original untouched.
4. **`fork_session` is a TypeScript-only Agent SDK feature.** Python lags. When the feature matters, recognise the SDK gap and **port to TypeScript** — don't trust Claude's "Python `options.fork_session`" answer.
5. **Rewind is an undo for a single session.** It rolls the same conversation back and *discards* what came after — don't rewind past something you can't afford to lose.
6. **Rename your sessions.** Unnamed conversations are indistinguishable in the picker; sessions live ~30 days.
7. **The resume picker shows session size in tokens** — a quick read on cost and context before you reopen it.
8. **Verify on disk.** Delete the session files, re-run, watch them regenerate. The docs and the AI can be wrong; the files aren't.

## Common pitfalls

- ❌ **Believing the docs or Claude over the SDK.** Andrew argued with Claude for 15 minutes; it kept giving a Python `fork_session` that isn't the real function. Check the SDK and the disk.
- ❌ **Confusing fork with rewind.** Fork = new sideways branch, original safe. Rewind = same session, moves backward, *loses* everything after the landing point.
- ❌ **Rewinding too far.** "If you cannot afford to lose that other stuff... just don't go too far back." There is no undo for the undo.
- ❌ **Never naming sessions.** A pile of unnamed conversations is unusable. Rename right when you start, like Andrew's "maths."
- ❌ **Forking or resuming from the wrong folder.** Andrew repeatedly had to "be really careful and pay attention to where we are" — the picker is scoped to your current directory unless you hit `Ctrl+A` for all projects.
- ❌ **Assuming parallel forks are free.** They finish faster but "we're going to burn through more credits." Speed costs tokens.

---

## 🛠️ Capstone Project: Atlas Support — fork a session to try two fixes, then rewind

> This is the main hands-on project for the lesson. You will feel the difference
> between branching sideways (fork) and stepping backward (rewind) on one real
> conversation. Keep it small on purpose — the point is the session moves, not a
> perfect fix.

Atlas Support, the multi-agent system you are building across this course, has a small bug in its ticket-intake script. You are not sure whether the better fix is approach A or approach B, and you do not want to re-run the whole investigation twice. This is exactly what forking is for: branch the same starting point into two isolated sessions, try one fix in each, keep the winner — and if a branch goes wrong, rewind it instead of starting over.

### What you will build

A single Claude Code session that you deliberately branch and roll back. Its pieces map straight to the lesson:

- **A baseline session** — one investigation of the bug, shared by both branches. *(Part 1)*
- **Two forks** — approach A and approach B, isolated, non-destructive. *(Part 4)*
- **A rewind** — undo a wrong turn inside one branch. *(Part 5)*
- **Named sessions** — so you can tell the branches apart. *(Part 5)*
- **A disk check** — proof the forks are real, separate sessions. *(Part 6)*

### Why this is the perfect practice

| Lesson idea | Where you use it in the Capstone |
|---|---|
| Session = saved conversation | The baseline you build once and branch from |
| Fork is non-destructive | Approach A and B branch from baseline; baseline stays clean |
| Resume shows size | You read each branch's token size before reopening it |
| Rename for clarity | You label the two branches "fix-A" and "fix-B" |
| Rewind rolls back | You undo a bad step inside one branch |
| Verify on disk | You delete session files and watch them regenerate |

### Milestones (build them in order, each one works on its own)

1. **Make a baseline session.** In a small Atlas Support folder, start `claude`, and have it investigate a deliberately buggy intake script (ask Claude to "generate Ruby/Python code with deliberate bugs to test my bug-fixing agent," paste it in). Stop once Claude has *described* the bug but not yet fixed it. Run `/rename` and call it `atlas-intake-baseline`. This shared starting point is a working unit on its own.
2. **Fork into approach A.** From the baseline, run `/fork` (or relaunch with `claude --resume --fork-session`). In the new branch, tell Claude to fix the bug one way (e.g. "guard the nil case"). Rename this branch `fix-A`. Confirm the baseline conversation is *unchanged* — that is the non-destructive promise.
3. **Fork into approach B.** Fork the baseline *again* into a second branch, `fix-B`, and try a different fix (e.g. "validate the input upstream instead"). You now have three sessions from one investigation: baseline plus two isolated branches.
4. **Prove they are separate on disk.** Find the sessions folder, list it, and confirm you see distinct session files with distinct IDs. Delete a throwaway test session's file, re-run, and watch it regenerate — "then we know absolutely that that is what is going on." This is the verify-everything move.
5. **Rewind a branch that went wrong.** In `fix-B`, deliberately take a bad step (ask for a change you'll regret). Then `/rewind` to the point just before it, choose **restore conversation**, and check `/context` — confirm the token count dropped and the bad step is gone. Notice this changed `fix-B` in place; it did *not* create a new session the way a fork would.
6. **Compare sizes and pick a winner.** Run `claude --resume` and read the size of `fix-A` vs `fix-B` in the picker. Reopen the better fix, keep it, and abandon the other branch. The baseline is still there if you want a fresh third attempt.
7. **Stretch goals.** (a) Rebuild the parallel-fork step in the **Claude Agent SDK** — start in Python, hit the missing `fork_session`, and port `main.py` to a `main.ts` that imports `fork_session` and runs three branches concurrently on Haiku. (b) Add a `.gitignore` for `node_modules` before you commit the TypeScript version (Andrew keeps forgetting this — don't). (c) Write one sentence on when you would choose fork vs rewind for a real Atlas Support incident.

### How you will know you are done

- ✅ You have three sessions from one baseline — `atlas-intake-baseline`, `fix-A`, `fix-B` — each with its own ID.
- ✅ The baseline is provably unchanged after both forks (you re-opened it and checked).
- ✅ You located the session files on disk and confirmed a deleted one regenerates on re-run.
- ✅ You rewound `fix-B` and saw `/context` shrink, with the bad step removed from the *same* session.
- ✅ You can state, in one line each, why fork is non-destructive and why rewind is not.

> 💡 **Keep yourself honest:** the difference between fork and rewind is not a
> definition to memorise — it is something you *saw happen*. Fork left the
> baseline alone; rewind deleted part of `fix-B`. If you didn't watch both, you
> don't know it yet.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice
> on one idea. Optional and independent; the Capstone already touches all of
> them, so feel free to skip straight to it.

### Exercise 1: Resume and read the size (foundational)
Open two old sessions with `claude --resume`. Before reopening either, write down each one's size from the picker, then run `/context` after opening to confirm your read of "which conversation is bigger." Get a feel for size as a cost signal.

### Exercise 2: Fork vs rewind, side by side (intermediate)
Take one session. Fork it once and note that the original is untouched. In a *copy*, rewind past a few messages and note that content is gone for good. Write two sentences: what each command did to the *original* conversation.

### Exercise 3: Reproduce the SDK gap (advanced)
In the Claude Agent SDK, try to fork a session in **Python**. When you can't find `fork_session`, confirm it exists in **TypeScript**, and port a minimal script over. Do not stop at "Claude said it's an option" — read the SDK exports yourself and prove which is real.

---

## Cheat sheet

```text
SESSIONS — resume, fork, rewind, rename — one-page recap

WHAT A SESSION IS
  A saved conversation with a unique session ID.
  `claude` = new session.  Resume = continue a previous conversation.
  Two types: WEB (started via web / remote control) and LOCAL (terminal / IDE).
  You can resume a web session into a local one in the IDE.

THE FOUR MOVES
  --resume / /resume        continue an existing conversation (same session)
  --fork-session / /fork    branch a COPY at the current point (NEW id;
                            original untouched — non-destructive)
  /rename                   label the current session (do it — ~30-day retention)
  /rewind                   roll the SAME session back to an earlier point
                            (DESTRUCTIVE — loses everything after; restore or
                            summarize)

FORK vs REWIND
  fork   -> sideways, new session, both paths kept, original safe
  rewind -> backward, same session, later messages discarded

RESUME PICKER KEYS
  Ctrl+A  all projects   Ctrl+B  toggle branch   Ctrl+V  preview
  Picker shows SESSION SIZE (tokens) = quick cost/context read.

THE SDK GAP (judgment call)
  fork_session  ->  TypeScript Agent SDK: YES     Python Agent SDK: NO
  Don't trust Python `options.fork_session` — it's not the real function.
  If the feature matters: PORT main.py -> main.ts, import fork_session.
  Forks run in PARALLEL (faster) but burn MORE credits.

THE RULE
  "What we read and what's generated out is not what is actually true."
  Verify on disk: find the session files, delete one, re-run, watch it
  regenerate. The disk and the SDK source are the truth, not the docs.
```

## How this connects to the rest of the course

- **Earlier, Module 1 · Lesson 3 (the stop-reason loop):** a session is simply that loop's history, saved so you can resume or branch it.
- **Earlier, Module 3 (hub-and-spoke and parallel agents):** forking is the *lightweight* way to run several explorations from one starting point — compare it to the coordinator pattern, where you defined every angle up front. Forking lets the same baseline fan out into isolated branches instead.
- **Earlier, Module 5 (Claude Code config):** the slash commands and CLI flags you practised there are exactly how you drive `/resume`, `/fork`, `/rename`, and `/rewind`.
- **Next, Module 6 (Managing the context window):** the `/context` command you kept reaching for here gets its own lesson — how to read the token breakdown, and how compaction and clearing keep a long-running Atlas Support session cheap and within its window.
- **Later, Module 6:** reliability. Sessions plus context discipline are what let an Atlas Support agent run for a long time, recover from a wrong turn, and still be trustworthy when it finally escalates to a human.

---

*Source: reconstructed from the CCA-F course by Andrew Brown (ExamPro). Code
snippets and diagrams are illustrative reconstructions of the patterns described
in the course. Adapt them to the current SDK.*
