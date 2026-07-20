# Module 0 · Lesson 0: Set up your architect's workbench

> **Course:** Claude Certified Architect: Foundations, a self-paced course
> **Module 0:** Pre-flight: set up your workbench: an optional on-ramp so every later lab just runs
> **Speaker:** Self-guided (no talk) — reconstructed from Andrew Brown, ExamPro
> **Source:** Reconstructed from the CCA-F course by Andrew Brown (ExamPro) · [full transcript](../../transcripts/cca-f-full-course.txt)
> **Estimated time:** 45 to 60 minutes (read plus lab)

---

## In one sentence

You install and verify the five tools this whole course runs on — Python, the Anthropic SDK, the Claude Agent SDK, Claude Code, and an API key you store safely — make one real call to Claude, and build a tiny reusable helper (`sdk_parser`) that turns Claude's noisy output into something readable and logs every run, so every later lab starts from a workbench that just works.

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone Project** where you *prove your workbench works*: install everything, make one successful API call, build the `sdk_parser` helper, and commit it to a git repo. Everything before the Capstone teaches the pieces you will assemble there. If you want to see the finish line first, jump to the **"Capstone Project"** section, then come back.

## A few plain-language basics first

This lesson uses some everyday terms. Here they are in plain words:

- **Terminal (or shell):** the text window where you type commands instead of clicking buttons. On Windows this course assumes **WSL 2** (Windows Subsystem for Linux — a real Linux running inside Windows), which is what Andrew uses; on macOS or Linux it is just your normal terminal.
- **CLI:** a *command-line interface* — a program you run by typing its name and options in the terminal (for example `python`, `git`, or `claude`).
- **Package / `pip`:** a *package* is reusable code someone else published. `pip` is Python's tool for downloading and installing packages (`pip install <name>`).
- **`requirements.txt`:** a plain text file listing the packages your project needs, one per line, so anyone can install them all at once with `pip install -r requirements.txt`.
- **Environment variable:** a named value your operating system hands to programs (for example `ANTHROPIC_API_KEY`). It lets you keep a secret *outside* your code.
- **Repo (repository):** a folder tracked by **git**, the tool that records the history of your changes and lets you push them to GitHub.
- **API key:** a secret password-like string that proves to Anthropic's servers that a request is really from your account (and who to bill).

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

Every other lesson in this course is a *lab* — you read a concept, then you build it and run it. That only works if your machine is ready. Andrew keeps a single rule for this whole course, and he says it plainly: **the only way to know the truth about these tools is to do it for real.** As he puts it, "often the docs were wrong, the exam guide was wrong, the AI was wrong. And so only by doing it, by going through the process, did we find out the real truth of these tools." You cannot verify anything if your tools are not installed. This on-ramp gets you to a first successful run, so from Lesson 1 onward you are spending your time *learning*, not fighting setup.

It is also honest about a gap the rest of the course quietly assumes: that you can open a terminal, run Python, and have money loaded to call the API. If any of that is not true for you yet, this is the lesson that fixes it. If it is all already true, skim the Capstone, tick it off, and move on — this module is optional on purpose.

## Learning objectives

By the end of this lesson you will be able to:

1. Install and verify Claude Code, and confirm you are logged in.
2. Install the Anthropic SDK and the Claude Agent SDK into a Python 3 environment, and explain the difference between them.
3. Create an Anthropic API key, load a little credit, and store the key as an environment variable that is never committed to git.
4. Make one successful call to Claude and read the response back.
5. Build a small reusable library (`sdk_parser`) that formats Claude's raw output for humans and writes a timestamped log file per run.
6. Put it all in a git repo and commit it — the workbench every later lab stands on.

## Prerequisites

- **None** — this is the first lesson and the course's on-ramp. It assumes only that you have a computer you can install software on.
- Comfort opening a terminal helps. If you are on Windows, install **WSL 2** first (search "install WSL" — Microsoft's one-line installer sets it up); this course's commands assume a Linux-style shell.
- A payment method for a small amount of API credit (Andrew suggests loading five or ten dollars — more on this in Part 4).

---

## Part 1: The five tools, and why each one is here

Before you install anything, it helps to know what you are installing and why. Here is the whole workbench in one table. Do not worry if some terms are new — the later parts install and explain each one.

| Tool | What it is | Why the course needs it |
|---|---|---|
| **Python 3** | A programming language. | Every lab in this course is written in Python. |
| **Anthropic SDK** | A Python *package* (`anthropic`) for calling Claude's API directly. | The lower-level way to send a message to a **model** and get a reply. |
| **Claude Agent SDK** | A Python *package* (`claude-agent-sdk`) for building *agents*. | The higher-level way to build things that take actions in a loop. |
| **Claude Code** | Anthropic's agentic coding tool — a **CLI** you run in your terminal. | You will use it to help write and debug the labs. |
| **API key + credit** | A secret string plus a small balance on your account. | Direct API calls are billed per token; the key authorises them. |

A few of these terms are worth pinning down now, because they recur in every lesson:

- **LLM** (large language model): the kind of AI that reads and writes text. "Claude" is one.
- **Model:** one specific version of Claude — Opus, Sonnet, or Haiku — differing in strength, speed, and price. You pick one per call.
- **Token:** the unit a model reads and writes in, roughly three-quarters of a word. You are billed per token, which is why cost comes up so often.
- **Agent:** an AI that takes a *series* of actions on its own toward a goal, rather than answering in one shot.

> 🔑 **The Anthropic SDK calls the model; the Claude Agent SDK builds agents.** Same company, two libraries, two jobs. You install both because this course uses both.

### The one distinction people trip on

The two SDKs sound alike and are easy to confuse. Keep them straight this way:

- The **Anthropic SDK** (package name `anthropic`) is the *lower-level* library. You give it a model, a message, and a token limit; it returns Claude's reply. This is what you use when you want to drive the raw API yourself.
- The **Claude Agent SDK** (package name `claude-agent-sdk`) is the *higher-level* library for building agents — things that use tools, run in a loop, and can act on your files. It is Claude Code packaged as a library you call from Python.

Andrew hit this confusion live, because the Agent SDK was *renamed*. As he found in the docs: "the Claude Code SDK was renamed Claude Agent SDK." So older material, and even the AI itself, sometimes calls it by the wrong name. This is your first taste of the course's recurring theme — **names and docs drift; you confirm the truth by checking and running it.**

## Part 2: Install and verify Claude Code

Claude Code is a CLI — a program you run by typing `claude` in your terminal. Install it the way Anthropic recommends for your system.

There are usually three install methods: a **native install**, Homebrew, and (on Windows) winget. Andrew's guidance, and the general recommendation, is to **prefer the native install**: it pulls the latest version straight from the source. The package-manager builds "might be old, and so you might run into an issue where you're having weird API issues because they're old."

On WSL 2 or Linux, the native install is a one-line command from Anthropic's install page. Run it, then **verify** — this is the habit the whole course is built on. Never assume an install worked; check it:

```bash
# Illustrative — get the exact current command from Anthropic's install page.
claude --version     # should print a version, e.g. 2.1.x
```

If `claude --version` prints a version number, Claude Code is installed. Now confirm you are logged in. Launch it and check status:

```bash
claude               # launches Claude Code
# inside Claude Code, type:
/status              # tells you whether you are logged in
/login               # starts the login flow if you are not
```

The `/login` flow opens a browser, you authorise, copy the code back, and you are in. As Andrew notes, logging in with your **subscription** is "probably one of the best ways that you can use Claude, because it's the most cost-effective way right now for learning" — the subscription covers your Claude Code usage.

Then prove it actually works with a trivial task. Andrew's check is to ask it to create an empty file:

> Ask Claude Code: *"Can you create me a `README.md` file that is completely empty in this folder."*

If the file appears, Claude Code is installed, logged in, and working. That is Part 1 of the workbench done.

> ✅ **What to do about it:** after any install in this course, run the tool's version or status command before moving on. A green check now saves an hour of confusion later.

## Part 3: Install the two SDKs into Python

Claude Code is for *helping you write* the labs. The labs themselves are Python programs that import the SDKs. Install both.

First confirm you have Python 3:

```bash
python3 --version    # should print Python 3.x
```

Then install the two packages. Andrew keeps it simple — no isolated virtual environment per tiny lab, just the system Python 3 on WSL ("we're just installing that one thing, and I don't want to be doing that all day every day"). If you prefer a virtual environment, that is fine too; nothing in the course depends on the choice.

```bash
pip install anthropic          # the Anthropic SDK (calls the model API)
pip install claude-agent-sdk   # the Claude Agent SDK (builds agents)
```

> 💡 **Watch the package names.** The *Anthropic SDK*'s package is `anthropic`. The *Claude Agent SDK*'s package is `claude-agent-sdk` (this is the one that was renamed from the old "Claude Code SDK"). If a tool or an AI tells you to `pip install agent-sdk` or drops `anthropic` into a `requirements.txt` for an agent lab, pause and check — Andrew caught exactly this mistake happening live. The fix is to confirm the real name in the docs, not to trust the first suggestion.

A clean habit: record what a lab needs in a `requirements.txt` so anyone (including future-you) can reinstall in one step. For a lab that uses the Anthropic SDK, that file is just:

```text
anthropic
```

Then `pip install -r requirements.txt` installs everything listed. You will make one of these per lab.

### About the API key vs. the subscription

Here is a subtle point Andrew tested by doing it. The **Claude Agent SDK** *can* pick up your Claude Code login (your subscription) if you are logged in via the CLI. But when you call the **Anthropic SDK** directly — the raw model API — you use an **API key**, and that draws on **API credit**, not your subscription. As Andrew reasons: "normally you'd be using this in a production environment, so it would never be tied to a subscription." So the next part sets up the key.

## Part 4: Create an API key and store it safely

To call the model API directly you need an **API key** and a little **credit**. There is no free tier for API usage, so you load a small balance. Andrew's advice: "load up five or ten bucks and see what mileage you get, because it'll give you an idea of how fast the consumption is." That small amount is plenty for this course's labs if you pick cheap models (more below).

Steps:

1. Sign in at the Anthropic console (`console.anthropic.com`).
2. Create an **API key**. Copy it once — you usually cannot see it again.
3. Add a small amount of credit (five to ten dollars is a sensible start).

Now the part that matters for safety. **The key is a secret. It must never end up in your code or your git history.** Anyone who has it can spend your money. The standard fix is an **environment variable** — a value your operating system hands to programs, kept outside your source files. The Anthropic SDK automatically looks for one named `ANTHROPIC_API_KEY`.

Set it in your shell:

```bash
# For the current terminal session only:
export ANTHROPIC_API_KEY="sk-ant-...your key..."

# To make it permanent, add that same line to your shell startup file
# (~/.bashrc on WSL/Linux, ~/.zshrc on macOS), then restart the terminal.
```

Because the SDK reads that variable on its own, your code never contains the key:

```python
import anthropic

# No key in the code — the SDK reads ANTHROPIC_API_KEY from the environment.
client = anthropic.Anthropic()
```

> ❌ **The mistake that leaks keys:** pasting the key straight into a `.py` file, or committing a file that contains it. If a key ever lands in a commit, it is compromised even after you delete it, because git keeps history. Protect yourself before your first commit: add a `.gitignore` that excludes secret files, and keep the key in the environment variable only.

A minimal `.gitignore` for these labs:

```text
# .gitignore — keep secrets and noise out of git
.env
*.log
logs/
__pycache__/
```

> 🔑 **Store the key once, in the environment, and never in a file git can see.** Everything else in Part 4 follows from that one rule.

## Part 5: Your first successful call ("hello, Claude")

Now make one real call. This is the moment your key, your credit, and the Anthropic SDK all prove themselves together. Keep it tiny to spend almost nothing.

Pick a **cheap model** for warm-up and testing. Andrew's guidance throughout the course is to "try to use one that's cost-effective, since we will be testing out a lot of stuff." The **Haiku** family is the fast, inexpensive tier — ideal here.

```python
# main.py — illustrative first call. Adapt the model id to the current Haiku model.
import anthropic

client = anthropic.Anthropic()   # reads ANTHROPIC_API_KEY from the environment

message = client.messages.create(
    model="claude-haiku-4-5",     # a cheap, fast model for warm-up and testing
    max_tokens=100,
    messages=[
        {"role": "user", "content": "Say hello in one short sentence."}
    ],
)

# The reply is a list of content blocks; the text lives in the first one.
print(message.content[0].text)
```

Run it:

```bash
python3 main.py
```

If a friendly sentence prints, **your workbench is real**. You installed the SDK, your key authorised the request, your credit paid for a handful of tokens, and Claude answered. That single successful line is the whole point of this on-ramp.

> 💡 **If it errors instead of printing:** the message usually tells you what is wrong. An authentication error means `ANTHROPIC_API_KEY` is not set in *this* terminal (re-run the `export`, or restart after editing your startup file). A "model not found" error means the model id has moved on — model names change over time; check Anthropic's current model list and swap in the right Haiku id. This is, again, the course's theme: you find the truth by running it and reading the actual error.

## Part 6: Build the reusable helper — `sdk_parser`

Here is the one piece of code you will actually reuse in every later lab, so it is worth building carefully now.

When you print Claude's raw response, it is a wall of nested Python objects — hard for a human to read. Andrew's move is to build a small library once and reuse it everywhere. In his words: "Can we create our own Python library for parsing it? ... I plan to use this library in multiple projects, so maybe it should live in a `lib` directory at the top of the project." The goal is two small functions:

1. `format_message(message)` — turn a raw response into a clean, human-readable string.
2. `log_message(message, project_dir)` — write that formatted output to a **timestamped log file**, one new file per run, in a `logs/` folder next to the project that is running.

Why the logging half matters: once each run is saved to a file, you can feed that file straight back to Claude Code when something breaks. As Andrew puts it, "if that file has not changed, we can now feed it back into it ... that's going to make it really, really useful for debugging." A timestamp on each log lets you tell runs apart and hand the exact one to the debugger.

Put the library at the top of the repo so any lab can import it:

```text
your-repo/
├── lib/
│   ├── __init__.py
│   └── sdk_parser.py        # format_message() + log_message()
├── hello_world/
│   └── main.py              # a lab that imports the parser
└── logs/                    # created at runtime, git-ignored
```

An illustrative `lib/sdk_parser.py`. The exact shape of a response object varies between the Anthropic SDK and the Claude Agent SDK, so treat this as the pattern, not a copy-paste-forever artefact:

```python
# lib/sdk_parser.py — illustrative reconstruction of Andrew's reusable helper.
from datetime import datetime
from pathlib import Path


def format_message(message) -> str:
    """Turn a raw Claude response into a clean, human-readable string."""
    lines = []
    # stop_reason tells you WHY the model stopped — you will lean on this heavily later.
    stop_reason = getattr(message, "stop_reason", None)
    if stop_reason:
        lines.append(f"stop_reason: {stop_reason}")
    for block in getattr(message, "content", []) or []:
        block_type = getattr(block, "type", "text")
        if block_type == "text":
            lines.append(f"[text] {getattr(block, 'text', '')}")
        else:
            # tool calls and other block types print their type + payload
            lines.append(f"[{block_type}] {block!r}")
    return "\n".join(lines)


def log_message(message, project_dir: str) -> Path:
    """Write the formatted output to a timestamped log file, one per run.

    Logs land in <project_dir>/logs/, relative to the lab that is running.
    """
    logs_dir = Path(project_dir) / "logs"
    logs_dir.mkdir(exist_ok=True)
    stamp = datetime.now().isoformat(timespec="seconds").replace(":", "-")
    log_path = logs_dir / f"{stamp}.log"
    log_path.write_text(format_message(message))
    return log_path
```

Notice `format_message` already surfaces `stop_reason`. You do not need it yet — but it is the single most important field in the whole API (it tells you *why* the model stopped: it wants to run a tool, or it is finished), and Lesson 3 is built entirely on it. Printing it from day one means your logs already show it.

Using the helper from a lab:

```python
# hello_world/main.py — illustrative
import anthropic
from lib.sdk_parser import format_message, log_message

client = anthropic.Anthropic()
message = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=100,
    messages=[{"role": "user", "content": "Say hello in one short sentence."}],
)

print(format_message(message))          # readable output on screen
path = log_message(message, ".")        # saved to ./logs/<timestamp>.log
print(f"logged to {path}")
```

> 🔑 **Build the helper once, reuse it forever.** A readable formatter plus a timestamped log turns every future lab from "a wall of objects I can't read" into "clean output on screen and a file I can feed back to Claude when it breaks."

> 💡 **A small documentation habit from Andrew:** when a folder has notes for the AI to read, he renames the `README.md` to `CLAUDE.md`, "as that's what it prefers to look for." You will see `CLAUDE.md` files throughout the course — that is why.

## Part 7: How the pieces stack

Here is the whole workbench as one picture. Each layer depends only on the ones below it — which is exactly why we installed them in this order.

```text
                 ┌─────────────────────────────────────────┐
   You run  ───▶ │  git repo (history + commits)            │
                 │   ├── lib/sdk_parser.py  (reused by all) │
                 │   └── hello_world/main.py                │
                 └───────────────┬─────────────────────────┘
                                 │ imports
                                 ▼
   Claude Agent SDK  ┐   ┌──  Anthropic SDK  ──▶  Claude's model API
   (build agents)    │   │    (call the model)         ▲
                     │   │                             │ authorised by
   Claude Code ──────┘   └─────────────────────────────┤ ANTHROPIC_API_KEY
   (helps you write)                                    │ (env var + credit)
                                                        │
                          Python 3  ──────────  the ground everything runs on
```

Read it bottom-up: Python 3 is the ground. The Anthropic SDK calls the model, authorised by your key. Claude Code helps you write the code. Your reusable `lib/` sits at the top and every lab imports it. Wrap the whole thing in a git repo and you have a workbench that any later lesson can build on.

---

## Key takeaways

1. **Verify every install.** `claude --version`, `/status`, `python3 --version`, and one real API call. Never assume — the course's whole method is "do it and confirm."
2. **Two SDKs, two jobs.** The *Anthropic SDK* (`anthropic`) calls the model; the *Claude Agent SDK* (`claude-agent-sdk`) builds agents. The Agent SDK was renamed, so its name is a common point of confusion.
3. **The key lives in the environment, never in code.** Set `ANTHROPIC_API_KEY`, add a `.gitignore`, and load a small amount of credit. There is no free API tier.
4. **Build `sdk_parser` once.** A `format_message` + `log_message` helper in a top-level `lib/` gives you readable output and a timestamped log per run — reused by every later lab and perfect for feeding failures back to Claude.
5. **Names and docs drift; running it is the truth.** This is the theme of the entire course, and it starts here.

## Common pitfalls

- ❌ **Pasting the API key into a `.py` file or committing it.** Once it is in git history it is compromised. Use the `ANTHROPIC_API_KEY` environment variable and a `.gitignore` from the start.
- ❌ **Installing `anthropic` for an agent lab (or `agent-sdk` for a model lab).** Match the package to the job: `anthropic` for direct model calls, `claude-agent-sdk` for agents. Andrew watched an AI get this exactly wrong.
- ❌ **Skipping verification.** An install that "seemed to work" but silently failed costs far more time later. Run the version/status check every time.
- ❌ **Expecting the subscription to pay for direct API calls.** Your Claude Code subscription covers Claude Code; the Anthropic SDK's direct API calls draw on API credit. Load a few dollars.
- ❌ **Forgetting the key is per-terminal.** `export` only sets it for the current session. Add it to your shell startup file (`~/.bashrc` / `~/.zshrc`) to make it stick, then restart the terminal.
- ❌ **Copying a model id and expecting it to work forever.** Model names change. If you get a "model not found" error, check the current model list and swap in the right (cheap) one.

---

## 🛠️ Capstone Project: Prove your workbench works

> This is the main hands-on project for the lesson. When you finish it you will *know* — not hope — that every later lab can run, because you will have installed everything, made one paid call to Claude, and committed the helper you will reuse for the rest of the course.

### What you will build

A single git repo containing: a working install of all five tools, one Python program that makes a successful call to Claude, and a reusable `lib/sdk_parser.py` (formatter + logger) — committed with a `.gitignore` that keeps your key and logs out of history. This is the north-star system's foundation: the course builds one growing multi-agent system called **Atlas Support** across every lesson, and this repo is the ground it stands on. Nothing here is throwaway — the `sdk_parser` you build now is used in every Atlas Support lab that follows.

Its pieces, each mapped to a lesson idea:

- **A verified toolchain** (Part 2, Part 3) — Claude Code, both SDKs, Python 3.
- **A safely stored key** (Part 4) — env var + `.gitignore`, plus a little credit.
- **One successful call** (Part 5) — the proof that the API path works end to end.
- **The `sdk_parser` helper** (Part 6) — readable output + timestamped logs, in a top-level `lib/`.
- **A committed repo** (Part 7) — the workbench, under git.

### Why this is the perfect practice

| Lesson idea | Where you use it in the Capstone |
|---|---|
| Verify every install | Milestones 1–3: version/status checks before moving on |
| Two SDKs, two jobs | Milestone 3: install and tell apart `anthropic` and `claude-agent-sdk` |
| Key in the environment, never in code | Milestone 4: `export` + `.gitignore`, no key in any file |
| One real call | Milestone 5: `python3 main.py` prints Claude's reply |
| Build `sdk_parser` once | Milestone 6: `format_message` + `log_message` in `lib/` |
| Everything under git | Milestone 7: commit the whole workbench |

### Milestones (build them in order, each one works on its own)

1. **Claude Code installed and working.** Run the native install, then `claude --version`. Launch `claude`, run `/status`, and `/login` if needed. Ask it to create an empty `README.md`. *Done when the file appears.*
2. **Python 3 present.** `python3 --version` prints a 3.x version. *Done when it does.*
3. **Both SDKs installed.** `pip install anthropic` and `pip install claude-agent-sdk`. *Done when both install without error and you can say, in one sentence each, what they are for.*
4. **Key stored safely + credit loaded.** Create an API key in the console, add a few dollars of credit, `export ANTHROPIC_API_KEY=...`, and add a `.gitignore` that excludes `.env`, `*.log`, `logs/`. *Done when the key is set in your shell and appears in no tracked file.*
5. **One successful call.** Write `main.py` that calls a cheap (Haiku) model and prints the reply. `python3 main.py`. *Done when a sentence from Claude prints.*
6. **The `sdk_parser` helper.** Create `lib/sdk_parser.py` with `format_message` and `log_message`. Wire `main.py` to print via `format_message` and save via `log_message`. Run it. *Done when you see readable output on screen and a new file under `logs/`.*
7. **Commit the workbench.** `git init`, then `git add`, then `git commit -m "init: workbench setup"`. *Done when `git log` shows your commit and `git status` is clean.*
8. **Stretch goals.** (a) Confirm the Claude Agent SDK picks up your Claude Code login by writing a tiny agent-SDK hello-world. (b) Feed a saved log file back to Claude Code and ask it to explain what happened. (c) Add a `CLAUDE.md` to `lib/` documenting how to import the parser.

### How you will know you are done

- ✅ `claude --version` prints a version and `/status` shows you logged in.
- ✅ `python3 -c "import anthropic, claude_agent_sdk"` runs with no error.
- ✅ `echo $ANTHROPIC_API_KEY` prints your key, and `git grep` (or a search) finds it in **no** tracked file.
- ✅ `python3 main.py` prints a real sentence from Claude.
- ✅ A new timestamped file appears under `logs/` after each run.
- ✅ `git log` shows one commit containing `lib/sdk_parser.py`, `main.py`, and `.gitignore` — and `git status` is clean.

> 💡 **Keep yourself honest:** before you commit, actually run `git status` and confirm no `.env`, no `*.log`, and no key-bearing file is staged. The single most expensive mistake in this whole lesson is committing a secret — check for it *before* the commit, not after.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice on one idea. Optional and independent; the Capstone already touches all of them, so feel free to skip straight to it.

### Exercise 1: The verification drill (foundational)
Without looking back, write down the one command you would run to verify each of: Claude Code is installed, you are logged in, Python 3 is present, and the API works. Then run all four. If any fails, fix it — that is the whole point of the drill.

### Exercise 2: Prove the `.gitignore` works (intermediate)
Create a fake `secret.env` file containing a dummy key, make sure your `.gitignore` excludes it, then run `git status`. Confirm the file does **not** appear as something git wants to track. Now you have tested your safety net with a fake secret instead of your real one.

### Exercise 3: Debug from a log (advanced)
Deliberately break `main.py` (for example, mistype the model id), run it, and capture the error in a log. Then open Claude Code, hand it the log file, and ask it to diagnose the problem. Fix it based on the answer. This rehearses the read-the-log-then-feed-it-back loop you will use constantly.

---

## Cheat sheet

```text
THE FIVE TOOLS
  Python 3            python3 --version
  Anthropic SDK       pip install anthropic          # calls the MODEL API
  Claude Agent SDK    pip install claude-agent-sdk    # builds AGENTS (was "Claude Code SDK")
  Claude Code         claude --version ; claude ; /status ; /login
  API key + credit    console.anthropic.com  → key + a few $ (no free API tier)

VERIFY EVERYTHING (the course's method)
  claude --version              # Claude Code installed?
  /status                       # logged in?
  python3 --version             # Python 3 present?
  python3 main.py               # does one real call work?

KEY SAFETY (never commit a secret)
  export ANTHROPIC_API_KEY="sk-ant-..."   # env var, per session
  add to ~/.bashrc / ~/.zshrc             # make it stick
  .gitignore:  .env  *.log  logs/  __pycache__/
  client = anthropic.Anthropic()          # reads the env var; no key in code

REUSABLE HELPER (lib/sdk_parser.py)
  format_message(msg) -> readable string (includes stop_reason)
  log_message(msg, project_dir) -> ./logs/<timestamp>.log  (one per run)

CAPSTONE = prove it works
  install all 5  →  one successful call  →  build sdk_parser  →  git commit

MODELS: use a cheap one (Haiku) for warm-up/testing. Names change — check the list.
```

## How this connects to the rest of the course

- **This is the first lesson**, so it sets up everything. There is nothing earlier — this module *is* the ground floor.
- **Next, Module 1 · Lesson 0 ("What the CCA-F exam is and how to pass it"):** now that your tools run, you will learn the shape of the exam, its five domains, the scoring, and the hands-on, verify-everything study plan this course follows.
- **Soon, Module 1 · Lesson 3 ("Tools and the stop-reason loop"):** the `stop_reason` field your `format_message` already prints becomes the engine of the whole agentic loop — you will drive control flow off it, not off parsing text.
- **Throughout — the north-star project, "Atlas Support":** the repo and the `sdk_parser` helper you commit here are the foundation the entire multi-agent system is built on. Every later capstone adds one component; this is the piece all of them stand on.

---

*Source: Reconstructed from the CCA-F course by Andrew Brown (ExamPro). Code snippets and diagrams are illustrative reconstructions of the patterns described in the course. Tool names, package names, and model ids change over time — adapt them to the current SDKs and Anthropic docs, and confirm by running them.*
