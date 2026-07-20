# Module 5 · Lesson 20: Built-in tools, status, and debug

> **Course:** Claude Certified Architect: Foundations, a self-paced course
> **Module 5:** Claude Code configuration & workflows: making the harness behave the way you need
> **Speaker:** Andrew Brown, ExamPro
> **Source:** Reconstructed from the CCA-F course by Andrew Brown (ExamPro) · [full transcript](../../transcripts/cca-f-full-course.txt)
> **Estimated time:** 40 to 55 minutes (read plus lab)

---

## In one sentence

Claude Code ships with a fixed catalog of **built-in tools** — where a `*` marks the ones that need your permission before they run — and it gives you two diagnostic commands, `/status` (which tells you *which account and auth method you are on*) and `/debug` (which writes a verbose log to a file you can open), so you can always answer "what can this agent do, who am I billed as, and what went wrong?"

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone
> Project** where you *audit* Atlas Support's environment: list every tool in
> play, run `/status` to confirm which account you are on, and run `/debug` to
> capture a real diagnostic log. Everything before the Capstone teaches the
> three things you will use there — the tool catalog, `status`, and `debug`. If
> you want to see the finish line first, jump to the **"Capstone Project"**
> section, then come back.

> 📝 **This lesson carries an EXAM-relevant reference.** The built-in tool list —
> and specifically **which tools are marked with a `*` because they require
> permission** — is the kind of recall the CCA-F exam probes. Andrew flags it
> directly: "ones that are marked with an asterisk are permissions required."
> Learn the *rule* (asterisk = needs permission, and those are the tools that
> can change your codebase), not just the list.

## A few plain-language basics first

This lesson uses a handful of terms. Here they are in plain words:

- **Claude Code:** Anthropic's agentic coding tool — a command-line program (a "harness") that runs an AI agent over your codebase, deciding which tools to call to get a job done.
- **Built-in tool:** a capability that ships *inside* Claude Code (or the Agent SDK) out of the box — reading a file, running a shell command, searching text — as opposed to a tool you add yourself.
- **Permission rule:** an allow / ask / deny rule that controls what Claude Code may do. Precedence is deny → ask → allow. Tools marked `*` are the ones Claude Code will *ask* about by default the first time it uses them.
- **Read-only tool:** a tool that only *looks* at things (reads a file, searches text) and cannot change your files or your machine.
- **Auth method:** *how* you are logged in — a subscription, your own API key, or a cloud provider like Amazon Bedrock. This decides who gets billed and at what rate.
- **Agent SDK (Claude Agent SDK):** the higher-level library for *building your own* agents in code. It ships with its own small set of built-in tools. (The lower-level **Anthropic SDK** just calls the model API directly.)
- **Verbose logging:** the mode where a program writes out far more detail than usual — every connection, every tool decision — into a file you can inspect afterward.

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

By now you have built agents and set permissions, but you have been trusting that you *know* what Claude Code can do and *who* it is acting as. Andrew learned the hard way that neither is obvious: "we discovered that there actually are a lot more tools than I thought that they were. I don't know how I missed this earlier." When you cannot see the full tool catalog, you cannot reason about what an agent might do; when you cannot see your auth method, you can burn expensive API credits thinking you are on a flat subscription; and when something breaks, you are guessing. This lesson gives you the three moves that end the guessing: read the tool list (and its `*` markers), run `/status`, and run `/debug`. These are small commands, but they are how you keep an agent's behaviour *legible* — a habit that matters more, not less, as Atlas Support grows into a multi-agent system.

## Learning objectives

By the end of this lesson you will be able to:

1. Recall the built-in tools of Claude Code and explain what the `*` marker means (permission required).
2. Predict which tools will ask for permission by default and which will not, using the read-only heuristic.
3. Name the core built-in tools of the Agent SDK — `read`, `grep`, `glob`, `edit`, `bash` — and say what each does.
4. Run `/status` and read off your auth method (first-party subscription vs API key vs Bedrock, and "logged in false" when you are not).
5. Run `/debug`, describe a problem, and locate and read the verbose log file it produces.

## Prerequisites

- **Module 5 · Lesson 19 ("Sandboxing and dangerous permissions")** — you should already understand permission rules (allow / ask / deny) and the sandbox; this lesson builds on the permission idea.
- Claude Code installed and working, launched at least once (Module 0 set this up).
- Comfort opening a file from the terminal (e.g., `cat somefile`).

---

## Part 1: The built-in tool catalog, and what the `*` means

Claude Code does not have unlimited, mysterious powers. It has a **fixed list of built-in tools**, and Andrew's whole point in this segment is that you should actually go read it: "what we'll do is go review all the built-in tools that can get the job done for you."

The list is presented **alphabetically**, and the single most important detail is a small mark next to some entries. In Andrew's words: "ones that are marked with an asterisk are permissions required."

So what does the asterisk actually control? Andrew reasons it through carefully, and it is worth keeping his nuance:

- A tool **with** a `*` requires permission. "In default mode, there is a tool that when it['s the] first time you use it, it's going to ask you whether it's allowed to use it."
- A tool **without** a `*` probably will *not* ask you in default mode: "for tools that do not have the asterisk, it probably will not ask you in the default mode."
- But — and this is the subtlety — the absence of a `*` does **not** mean you are powerless over it. "It doesn't mean that you cannot set permissions to deny it ... we can still explicitly deny them, allow, or ask them."

And there is a clean heuristic for *why* a tool has a `*`: "generally if they don't have the asterisk, they're probably just read-only tools ... or things that wouldn't impact your codebase." Flip that around and you have the rule the exam wants: **the tools that can change your files or your machine are the ones that ask permission.**

> 🔑 **The `*` marks tools that need permission — and those are exactly the
> "can change something" tools (bash, edit, write, notebook edit). No `*`
> usually means read-only. You can still add your own allow/ask/deny rule to
> *any* tool regardless of the marker.**

### The tools, in Andrew's tour order (alphabetical)

Andrew walks the list top to bottom. Here it is as a reference table. Treat the `*` column as "asks for permission by default, because it can affect your environment." (The exact on-screen markers are what the list itself shows; the pattern to remember is *mutating tools carry the `*`*.)

| Tool | What it does | `*` needs permission? |
|---|---|---|
| `agent` | "Spawns a sub-agent with its own context window to handle a task." | |
| `ask user questions` | "Ask multiple-choice questions to gather requirements or clarify ambiguity." | |
| `bash` | "Execute shell commands in your environment." Andrew: "make note of the asterisk as it obviously is going to be doing heavy lifting." | `*` |
| `cron create` | "Schedule a recurring or one-shot prompt within the current session." | |
| `cron delete` | Delete a scheduled task "based on a task ID." | |
| `cron list` | List the cron jobs. | |
| `edit` | Edit "a very specific file." | `*` |
| `enter plan mode` | "Switch to plan mode to design an approach." | |
| `enter worktree` | "Look at an isolated git worktree." | |
| `exit plan mode` | Leave plan mode. | |
| `exit worktree` | Leave the worktree. | |
| `glob` | Discover files by name pattern. | |
| `grep` | "A pattern for searching across files" (contents). | |
| `list MCP resource tools` | List the MCP resource tools available. | |
| `LSP` | "Code intelligence tool ... Language Server Protocol" — understand a language. | |
| `notebook edit` | Edit a Jupyter notebook. Andrew: "notice the asterisk there as it's editing something." | `*` |
| `read` | Read a file. | |
| `read MCP resource` | Read an MCP resource. | |
| `skill` | "Execute a skill." | |
| `task create / get / list / output / stop / update` | Create and manage background tasks (some take "a task ID or something" as a parameter). | |
| `todo write` | "Manage the session task checklist." | |
| `tool search` | Search the available tools. | |
| `web fetch` | "Fetch something from a URL." | |
| `web search` | "Perform searches." | |
| `write` | Write a file. | `*` |

Andrew's honest summary: "there's obviously more tools there and any of those can be applied. They might even have some parameters ... but there you go." The catalog evolves, so the durable skill is not memorising every row — it is knowing *how to read the list* and what the `*` means.

> 💡 **A judgment note in the spirit of this course.** Andrew openly admits he
> "missed this earlier" and thought there were fewer tools. The lesson: don't
> trust your memory of what a harness can do — open the actual tool list and
> read it. The truth is in the tool, not in your recollection.

## Part 2: `status` — which account and auth method am I actually on?

Now the first diagnostic command. `status` answers a question you should ask *before* you start spending: who am I logged in as, and how?

Andrew: "This is going to allow you to know what method of authentication you're currently using. Basically tells you whether you're logged in or not."

You can run it two ways. Inside the interactive Claude CLI it is `/status`. But Andrew's habit is to check it *first*, from the shell, before he even opens the interactive console: "I normally will use it before I go into the interactive console, because it's more useful to know before you go and start using Claude exactly which one you're utilizing ... so you don't end up using something you don't mean to use."

The output *looks different depending on how you are logged in*, and reading those differences is the whole skill:

| You are logged in as… | What `status` shows | The tell |
|---|---|---|
| **API usage** (Anthropic Console, key made for you) | `Claude first party`, **subscription type: `null`**, **Manage key** | "Subscription type is null — that is indicating that it is using the API because it is null." `Manage key` means Claude Code created the key for you. |
| **A subscription** | `first party`, a **subscription** shown, **no** "Manage key" | "Notice that it doesn't say manage key, just says first party ... and we don't see API key source because we're not using API key source." |
| **Your own custom API key** | `first party`, key source: **`Anthropic API key`** | "It would say first party, but you can see that we're using Anthropic API key as our key source — that's the custom key." |
| **A third-party provider (e.g. Amazon Bedrock)** | shows **third party / Bedrock** | "If we use a third party then we can see that we're using a third party with Bedrock ... set with our AWS credentials the normal way." |
| **Not logged in at all** | `logged in: false`, `method: none`, `API provider: first party` | The plain "you're not authenticated" state. |

Two things Andrew hit in the wild are worth borrowing as warnings:

- **More than one token.** He once had "more than one token in here ... the nice part was it prompted me saying, hey, you have more than one here, so do something about [it]." The fix: "you'd have to log out, check your env-var keys, and then explicitly log back in and fix that issue." An `ANTHROPIC_API_KEY` sitting in your environment can silently override what you expected.
- **The expensive-mode reminder.** With an API token set, Claude Code "actually reminded me ... saying, hey, did you know you have this set and you're doing this? Is this what you want to do?" Andrew explains why that nudge matters: "when you're using the API key, then you're having more direct spend — it's more expensive, or can get more expensive." `status` (and that reminder) is how you avoid billing yourself per-token when you meant to be on a flat plan.

> 🔑 **Run `/status` before you start work. `subscription type: null` = you are
> on the pay-per-token API. A subscription line = flat plan. `Manage key` = the
> key Claude Code made for you; `Anthropic API key` source = a custom key you
> supplied; Bedrock = a third-party provider. `logged in: false` = not
> authenticated.**

## Part 3: `debug` — verbose logging to a file you can open

The second diagnostic command is for when something is *wrong*. Andrew: "it's a mode that will output verbose information to a specific text file, and Claude will also prompt you to describe the problem as it attempts to investigate the issue."

There are two ways to turn it on:

- **Mid-session:** type `debug` (i.e. `/debug`) inside Claude Code. It replies that "debug logging for this session" is enabled and starts "outputting to a very specific directory."
- **From launch:** "there's also a flag to start this up on the start — you can do `--debug`." Andrew shows the guidance Claude itself gives: "if you can't easily reproduce it in the session, you can also restart Claude Code with debug mode enabled from the start with `claude --debug`."

Once enabled, Claude asks you to **describe the problem** — literally, "to help debug the issue, describe the problem you're having." The idea is that you reproduce the issue while it watches, and it captures diagnostics. In the lab Andrew has no real bug, so he invents one ("the code output seems to be containing mistakes") just to see what gets written — a perfectly good way to *observe the tool* even when nothing is actually broken.

What ends up in the log file? Andrew: "it says stuff like what it connects to, what tools are disabled or used, all a bunch of stuff." To read it, you stop the session and open the file directly — "we'll type in `clear` and we'll `cat` this file out." Looking through it, he sees entries like "temp files rewritten, added, original permission file," and concludes honestly: "if there were communication issues or other stuff going on there, I could see that might be helpful."

The intended use is *sharing* that log to get help: "this seems like something that you would provide to Claude to say, hey, I had problems, can you help me debug it?" One practical caution he raises: check the file before you send it — "I don't know if there's any sensitive information in here. I don't see any" — because a diagnostic log can contain paths, connections, and config you might not want to paste in public.

> ✅ **What to do about it:** when Claude Code misbehaves, run `/debug` (or
> relaunch with `claude --debug`), describe the problem, reproduce it, then
> `cat` the log file it names. Skim it for anything sensitive before you share
> it with Anthropic or a teammate.

## Part 4: The Agent SDK's core built-in tools

Everything above is about **Claude Code**, the ready-made harness. But when you *build your own* agent with the **Claude Agent SDK** (the higher-level library for making agents in code), it too "comes with a bunch of built-in tools." Andrew is upfront that this is a *curated* subset: "there's way more than just this, but these are the main ones that Anthropic is going to want you to know" — again, exam-relevant recall.

There are five to know:

| Agent SDK tool | What it does | Andrew's words |
|---|---|---|
| `read` | Load a file's contents | "It's going to be able to load files ... summarize this file, and then you have that read option so it can read that file." |
| `grep` | Search *inside* files (contents) | "grep will allow you to search file contents." |
| `glob` | Discover files by *name* pattern | "glob will discover files matching on a pattern ... grep can look in the contents of files, whereas glob is really looking at the names or list of files." |
| `edit` | Change a file | "This is when you want to edit files. If you don't have this, you can't edit files." |
| `bash` | Run any shell command | "bash can do basically all this other stuff ... you could have bash just use any kind of bash command." |

Two relationships are worth locking in. First, `grep` vs `glob`: **grep searches contents, glob lists files by name.** That distinction shows up constantly. Second, `bash` is the powerful catch-all — it "can do basically all this other stuff" — which is exactly why it is the one most constrained: "when you're working in a sandbox, normally bash is not allowed, and it has to go outside the sandbox." (Notice the through-line to Part 1: bash is the tool that carries the `*`.)

Andrew's framing of why these five matter: "if you were to build your own coding harness, these are like very basic ones you absolutely want to have." A harness with read + grep + glob + edit + bash can navigate a codebase, find things, change them, and run commands — the minimum viable agent toolkit.

> 🔑 **Agent SDK core five: `read` (load a file), `grep` (search contents),
> `glob` (find files by name), `edit` (change a file), `bash` (run anything).
> grep = inside files; glob = file names. bash is the most powerful and the
> most sandbox-restricted.**

### A quick judgment note

When Andrew ran the built-in-tools lab he expected a longer Agent SDK list and was briefly puzzled: "maybe my confusion is that there's other providers that have a larger list, or maybe there are more and I'm just not seeing them." That is the healthy reflex this course keeps teaching — when the tool doesn't match your memory, don't argue with the screen; note the gap and verify. The five above are the ones Anthropic wants you to know cold.

---

## Key takeaways

1. **The `*` = permission required.** Marked tools ask before running by default; unmarked ones usually don't. The marked ones are the tools that can *change* something (bash, edit, write, notebook edit).
2. **No `*` still means you can rule on it.** You can explicitly allow / ask / deny *any* tool, marked or not — the marker only sets the default behaviour.
3. **Open the real tool list.** Andrew "missed" tools he assumed weren't there. The catalog is the source of truth, not your memory.
4. **`status` before you spend.** It tells you first-party vs API key vs Bedrock, and whether you're logged in. `subscription type: null` means you're on the pay-per-token API.
5. **Watch for stray tokens and the expensive-mode nudge.** A leftover `ANTHROPIC_API_KEY` can silently switch you to metered spend; Claude Code will warn you — heed it.
6. **`debug` writes a verbose log to a file.** Enable it in-session or with `claude --debug`, describe the problem, reproduce it, then `cat` the file. Check for sensitive info before sharing.
7. **Agent SDK core five:** `read`, `grep`, `glob`, `edit`, `bash` — the minimum toolkit for a coding harness.

## Common pitfalls

- ❌ **Assuming "no asterisk" means "I can't control it."** You can still deny an unmarked tool. The `*` only sets the *default* ask/allow behaviour.
- ❌ **Starting work without checking `status`.** You think you're on a subscription but a stray API key means every call is metered. Run `/status` first — Andrew does it from the shell *before* opening the console.
- ❌ **Reading `subscription type: null` as "broken."** `null` is the normal signal that you're using the API (pay-per-token), not that something failed.
- ❌ **Confusing `grep` and `glob`.** grep searches file *contents*; glob matches file *names*. Reaching for the wrong one wastes a step.
- ❌ **Pasting a debug log without reading it.** Logs can contain paths, connections, and config. Skim for sensitive info before you share, exactly as Andrew pauses to do.
- ❌ **Forgetting `bash` is the sandbox flashpoint.** Because bash "can do basically all this other stuff," it's the tool most likely to be blocked in a sandbox and the one carrying the `*`.

---

## 🛠️ Capstone Project: Audit Atlas Support's environment

> This is the main hands-on project for the lesson. You will produce a short
> written **environment audit** of Atlas Support — the tools in play, the
> account you're on, and a captured debug log. Keep it small: this is a
> reconnaissance exercise, not a build. Each milestone stands on its own, so a
> stuck learner still ships something useful.

Atlas Support, our north-star project, is growing into a multi-agent system, and the more moving parts it has, the more you need to be able to answer three questions on demand: *what can it do, who is it billed as, and what does the log say when it breaks?* This capstone is the diagnostic muscle Atlas Support will lean on every time something goes wrong later.

### What you will build

A single `audit/ENVIRONMENT.md` file (plus one captured log) that records:

- **The tool inventory** — the Claude Code built-in tools relevant to Atlas Support, each labelled read-only or permission-required (`*`), and the Agent SDK core five if you're building with the SDK.
- **The auth snapshot** — the output of `/status`, interpreted: first-party subscription, API key, or Bedrock, and whether you're logged in.
- **A debug log** — a real verbose log file captured with `/debug`, with a note on what's inside it.

Each piece maps to a lesson idea: the inventory is Part 1 + Part 4, the auth snapshot is Part 2, the log is Part 3.

### Why this is the perfect practice

| Lesson idea | Where you use it in the audit |
|---|---|
| `*` = permission required (Part 1) | Labelling each tool read-only vs permission-required |
| Agent SDK core five (Part 4) | Listing `read`/`grep`/`glob`/`edit`/`bash` if using the SDK |
| Reading `status` (Part 2) | Recording and interpreting your auth method |
| `debug` writes a file (Part 3) | Capturing and skimming a real log |

### Milestones (build them in order, each one works on its own)

1. **Create the audit file.** Make an `audit/` folder and an `ENVIRONMENT.md` inside it with three headings: `Tools`, `Auth`, `Debug`. That's a complete, working deliverable on its own.
2. **Inventory the tools.** Under `Tools`, list the Claude Code built-in tools that matter for Atlas Support (at minimum `bash`, `edit`, `write`, `read`, `grep`, `glob`, `agent`). Mark each read-only or `*` permission-required, and write one sentence explaining the rule: "the `*` tools are the ones that can change something." Andrew's line — "ones marked with an asterisk are permissions required" — is your test.
3. **Snapshot your auth.** Run `/status` (from the shell first, as Andrew recommends). Paste the key facts into `Auth` and interpret them in one line: are you first-party subscription, `subscription type: null` API, a custom `Anthropic API key`, or Bedrock? Note whether `logged in` is true.
4. **Capture a debug log.** Turn on `/debug` (or relaunch with `claude --debug`). When it asks you to describe the problem, invent a small one — exactly as Andrew does — reproduce a step, then stop and `cat` the log file it named. Save a copy into `audit/`.
5. **Read the log.** In the `Debug` section, write two or three lines on what the log actually contains (what it connects to, which tools were used or disabled) and confirm you checked it for sensitive info before deciding whether it's safe to share.
6. **Stretch goals.** (a) If you're building with the Agent SDK, add a short `agent_sdk_tools` list documenting the core five with a one-line "grep = contents, glob = names" reminder. (b) Add an `ANTHROPIC_API_KEY` to your environment, re-run `/status`, and record how the output changes and whether Claude Code warns you about the stray token. (c) Note which of your listed tools would be blocked inside a sandbox (hint: `bash`).

### How you will know you are done

- ✅ `audit/ENVIRONMENT.md` exists with all three sections filled in.
- ✅ Every tool in your inventory is labelled read-only or `*` permission-required, and you can state the rule for *why*.
- ✅ Your `Auth` section names your exact auth method and cites the tell you used (e.g., "`subscription type: null` → API").
- ✅ A real debug log file is saved in `audit/`, and you've written what's in it.
- ✅ You checked the log for sensitive information before treating it as shareable.

> 💡 **Keep yourself honest:** don't fill the tool table from memory — open the
> actual list in Claude Code and copy what's really there, `*` markers and all.
> Andrew "missed" tools he assumed weren't present; the audit is only worth
> anything if it reflects the tool, not your recollection.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice
> on one idea. Optional and independent; the Capstone already touches all of
> them, so feel free to skip straight to it.

### Exercise 1: Mark the movers (foundational)
From memory, write down five Claude Code built-in tools and predict which carry a `*`. Then open the real list and check. For every one you got wrong, write the one-line reason it does or doesn't change your codebase.

### Exercise 2: Read three status outputs (intermediate)
Write out (or reconstruct from Part 2) what `/status` shows in three cases: a flat subscription, the pay-per-token API with a Claude-Code-managed key, and Bedrock. For each, circle the single field that tells them apart (subscription line, `subscription type: null` + `Manage key`, and third-party/Bedrock respectively).

### Exercise 3: A debug log you'd actually send (advanced)
Trigger `/debug`, capture the log, then redact it: produce a shareable version with any paths, keys, or private config removed, and a note listing what you took out. This is the discipline behind Andrew's "I don't know if there's any sensitive information in here" pause.

---

## Cheat sheet

```text
BUILT-IN TOOLS, STATUS & DEBUG — QUICK REFERENCE
================================================

THE ASTERISK RULE (exam)
  *  = permission required, asks by default
  no * = usually read-only, no prompt by default
  EITHER way you can still add allow / ask / deny yourself.
  The * tools are the ones that CHANGE something: bash*, edit*, write*, notebook-edit*

CLAUDE CODE BUILT-INS (alphabetical, abbreviated)
  agent · ask-user-questions · bash* · cron create/delete/list · edit*
  enter/exit plan mode · enter/exit worktree · glob · grep
  list-mcp-resource-tools · LSP · notebook-edit* · read · read-mcp-resource
  skill · task create/get/list/output/stop/update · todo-write
  tool-search · web-fetch · web-search · write*
  (grep = searches CONTENTS · glob = matches NAMES)

AGENT SDK CORE FIVE (the ones to know)
  read  -> load a file
  grep  -> search file CONTENTS
  glob  -> find files by NAME pattern
  edit  -> change a file
  bash  -> run any shell command (most powerful, most sandbox-restricted)

/status  — WHO AM I / HOW AM I BILLED  (run it BEFORE you start)
  first party + subscription line          -> flat subscription
  first party + subscription type: null
             + "Manage key"                -> pay-per-token API (key CC made)
  first party + key source: Anthropic API key -> your own custom key
  third party / Bedrock                    -> AWS creds + provider flag
  logged in: false, method: none           -> not authenticated
  ! stray ANTHROPIC_API_KEY can flip you to metered spend — CC warns you

/debug  — VERBOSE LOG TO A FILE
  turn on:  /debug   (or launch:  claude --debug)
  it asks you to DESCRIBE THE PROBLEM, then reproduce it
  writes: what it connects to, which tools used/disabled, etc.
  read it:  clear ; cat <the file it named>
  CHECK FOR SENSITIVE INFO before sharing with Anthropic
```

## How this connects to the rest of the course

- **Earlier, Module 5 · Lesson 19 ("Sandboxing and dangerous permissions"):** you learned allow/ask/deny and the sandbox. The `*` marker here is the *other half* of that story — it tells you which built-in tools trigger those permission prompts in the first place, and why `bash` is the one the sandbox fights hardest.
- **Next, Module 5 ("Automating with Claude Code GitHub Actions"):** when you hand Atlas Support to an automated GitHub Action, you can no longer sit and answer permission prompts — so knowing *which* tools ask, and being able to check `status` and `debug` from logs, becomes essential.
- **Later:** as Atlas Support gains MCP tools, sub-agents, and reliability checks, this audit habit — list the tools, confirm the account, read the log — is the routine you'll run every time behaviour surprises you.

---

*Source: "Claude Certified Architect: Foundations" by Andrew Brown, ExamPro. Code snippets, tables, and diagrams are illustrative reconstructions of the patterns described in the course. The built-in tool catalog evolves — always confirm against the live list in your version of Claude Code and the Agent SDK.*
