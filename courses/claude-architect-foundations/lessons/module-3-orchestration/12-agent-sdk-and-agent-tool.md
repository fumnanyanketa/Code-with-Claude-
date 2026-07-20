# Module 3 · Lesson 12: The Claude Agent SDK and the Agent (task) tool

> **Course:** Claude Certified Architect: Foundations, a self-paced course
> **Module 3:** Orchestration: multi-agent architectures — turn one agent into a reliable coordinated system
> **Speaker:** Andrew Brown, ExamPro
> **Source:** Reconstructed from the CCA-F course by Andrew Brown (ExamPro) · [full transcript](../../transcripts/cca-f-full-course.txt)
> **Estimated time:** 45 to 60 minutes (read plus lab)

---

## In one sentence

You will lift your hand-built coordinator off the low-level Anthropic SDK and onto the higher-level **Claude Agent SDK**, where tools become one-line decorators, your tools ship as an *internal* MCP server, and one built-in **Agent tool** spins up an isolated sub-agent from a small "agent definition" — while learning, the hard way, that the docs and the model both lie about the details, so an architect trusts only what they build and test.

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone Project** where you port Atlas Support's coordinator to the Claude Agent SDK using decorator tools, then add one sub-agent through the Agent tool — and you write down every place the SDK's real behaviour did not match its docs. Everything before the Capstone teaches the skills you will use there. If you want to see the finish line first, jump to the **"Capstone Project"** section, then come back.

## A few plain-language basics first

This lesson uses some everyday terms. Here they are in plain words:

- **LLM:** the kind of AI that reads and writes text; "Claude" is one.
- **Model:** one specific version of that AI (e.g., Opus, Sonnet, Haiku), differing in strength, speed, and price.
- **Agent:** an AI that takes a series of actions on its own toward a goal, rather than answering in one shot.
- **Tool / tool call / tool result:** a function the model can choose to run; when it decides to use one, that is a *tool call*, and what comes back is the *tool result*.
- **Anthropic SDK vs Claude Agent SDK:** the *Anthropic SDK* is the lower-level library for calling the model API directly; the *Claude Agent SDK* is the higher-level library for building agents (decorator tools, sub-agents, hooks). The Python Agent SDK sometimes lags the TypeScript one.
- **Coordinator / hub-and-spoke:** an architecture where one *coordinator* agent owns routing, context, and aggregation, and delegates to *sub-agents* ("spokes") exposed to it as tools.
- **Sub-agent:** an agent spawned by another agent, usually with its own isolated context (its own memory of the conversation).
- **MCP (Model Context Protocol):** an open standard (created by Anthropic) for connecting agents to external tools, data, and prompts via *MCP servers*.
- **Decorator (Python):** a small `@something` line written directly above a function that wraps it with extra behaviour — here, "this function is a tool."
- **Context window:** how much text (in tokens, ~¾ of a word each) the model can hold in mind at once.

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

For the last few lessons you built the coordinator *by hand* on the Anthropic SDK: you wrote the tool JSON schemas yourself, read `stop_reason`, and appended each tool result to keep the loop going. That taught you how the machinery works — and now you get to trade it in. The Claude Agent SDK does the loop for you, turns each tool into a one-line decorator, and hands you a built-in way to spawn sub-agents. As Andrew puts it after the port, *"the key takeaway here is the fact that the tool-use call got easier and it's setting up an MCP server."* But the deeper lesson is an architect's discipline: on this exact feature Andrew discovers the "task tool" is really the "agent" tool, and that the Python SDK is quietly missing fields the TypeScript SDK has. *"We always confirm and we don't just go based on this stuff,"* he says. *"You have to go out and test them and then draw a line back to your information."*

## Learning objectives

By the end of this lesson you will be able to:

1. Explain the difference between the **Anthropic SDK** and the **Claude Agent SDK**, and say which one you reach for and why.
2. Port a hand-built coordinator to the Agent SDK using **decorator tools** and an **internal (in-process) MCP server**.
3. Use the built-in **Agent tool** to spawn an isolated sub-agent, and explain why spawning one is *not* automatically parallel.
4. Read and write an **agent definition** — its `name`, `description`, `prompt`, and `tools` fields — and name the fields the Python SDK still lacks versus TypeScript.
5. Apply "verify-everything" judgment: treat the docs and the model's answers as unverified until your own test confirms them.

## Prerequisites

- **Module 3 · Lesson 8** (hub-and-spoke coordinator) and **Lesson 11** (failure recovery and the clean coordinator refactor) — you are porting *that* coordinator here.
- **Module 1 · Lesson 3** (tools and the `stop_reason` loop) — so you appreciate what the Agent SDK now does for you.
- **Module 0** toolchain: Python, the Anthropic SDK, and the **Claude Agent SDK** installed, plus either an API key or a logged-in Claude subscription.
- Comfort reading small Python files. All code here is an *illustrative reconstruction* — adapt it to the current SDK.

---

## Part 1: Two SDKs, two jobs — Anthropic SDK vs Claude Agent SDK

Anthropic ships **two** libraries, and the exam expects you to tell them apart.

- The **Anthropic SDK** is the *low-level* one. You call the model API directly: send messages, get back a response, read `stop_reason`, and — if you want a loop — you write that loop yourself. This is what you have been using to build the coordinator by hand.
- The **Claude Agent SDK** (Andrew also calls it the "Claude Code Agent SDK" — *"when I say Claude Code agent SDK I'm talking about the same thing"*) is the *higher-level* one. It is built for *agents*. It runs the agentic loop for you, lets you declare tools with a decorator, spawns sub-agents, and runs hooks. It is, in effect, the engine inside Claude Code, exposed as a library.

| | Anthropic SDK | Claude Agent SDK |
|---|---|---|
| Altitude | Low-level: raw API calls | High-level: build agents |
| The loop | You write it (`stop_reason`) | Runs for you |
| Defining tools | You write JSON schemas | `@tool` decorator |
| Sub-agents | Roll your own coordinator | Built-in **Agent tool** |
| Footprint | More code | Smaller code |
| When to drop down | — | When you need low-level control the Agent SDK hides (e.g., seeing inside a sub-agent's loop) |

Why port at all? Andrew's reason is practical: *"we're going to be getting into specific Agent SDK arguments. And if we want to know how they work, we need to have an example over there."* You do not port because the hand-built version was wrong — you port because the next several features (sub-agents, parallel agents, hooks) *live* in the Agent SDK.

> 🔑 **The Anthropic SDK is for talking to the model; the Claude Agent SDK is for building the agent around it. Same company, two altitudes — know which one a question is about.**

> 💡 **The Agent SDK is not always the ceiling.** Later you will want to watch a sub-agent's internal loop or track spend mid-run. Andrew notes you *can't* do that from the Agent SDK today: *"I believe you'd have to drop down to the Anthropic SDK."* Higher-level means less code *and* less visibility. Keep the low-level SDK in your back pocket.

## Part 2: The port — decorator tools and an internal MCP server

Here is what actually changes when you move the coordinator over. Andrew ports the whole thing in one shot and then reads the diff.

**Before (Anthropic SDK):** every tool needed a hand-written JSON schema — a big block describing the tool's name, description, and each parameter's type. Your loop read `stop_reason`, dispatched the tool call, and appended the result.

**After (Claude Agent SDK):** each tool becomes a *decorated function*. As Andrew narrates while reading the diff, *"instead of handling tools here, we have a decorator … so we have decorators on top of our functions, making this code a lot smaller."*

```python
# Illustrative reconstruction — adapt to the current SDK.
from claude_agent_sdk import tool, create_sdk_mcp_server, query, ClaudeAgentOptions

# 1. Each tool is just a decorated function. The decorator carries the
#    name, the description, and the input schema — no separate JSON file.
@tool("screen_candidate", "Score one candidate against the job criteria",
      {"resume_text": str, "job_id": str})
async def screen_candidate(args):
    result = do_the_screening(args["resume_text"], args["job_id"])
    return {"content": [{"type": "text", "text": result}]}

# 2. Bundle the tools into an in-process ("internal") MCP server.
screening_server = create_sdk_mcp_server(
    name="atlas-screening",
    version="1.0.0",
    tools=[screen_candidate],   # plus your other coordinator tools
)

# 3. Hand the server to the SDK. It runs the loop for you.
options = ClaudeAgentOptions(
    mcp_servers={"screening": screening_server},
    allowed_tools=["mcp__screening__screen_candidate"],
)
```

Two things surprised Andrew, and both are worth internalising:

1. **Your own tools now ride an MCP server — an *internal* one.** You met MCP as a way to reach *external* tools. Here the SDK wraps *your* in-process functions in an MCP server that never leaves your program. As Andrew says: *"we basically have an internal MCP … literally it's an internal MCP server."* He reads it as a signal of intent: *"clearly Anthropic is obviously making that a priority."* MCP is not just for third-party tools — it is becoming the SDK's native way to describe *any* tool.

2. **The decorator captures state through a normal closure.** Andrew wanted his tools to live in a separate `tools/` module instead of inside the coordinator, and worried the decorator's tight coupling forbade it. Claude's explanation: *"tool is a decorator [that] runs at call time not import time. So you can apply it inside the factory function. It captures state via normal closures."* Translation: you *can* define your tools in a `make_coordinator_tools(...)` factory that closes over the coordinator's state, keeping the module layout clean. The port ends with a tidy `coordinator/` (a `make_coordinator_tools` factory plus a separate `coordinator_state`), which is the shape Andrew wanted.

> ✅ **What to do about it:** after the port, actually run it. Andrew's whole confidence check is one line — *"I just want to make sure that it still runs because we've changed a lot of code … to another framework."* It ran clean. A framework port is exactly the kind of large, invisible change where "it compiled" is not "it works."

## Part 3: The Agent tool — one isolated sub-agent, and it is *not* auto-parallel

Now the headline feature. The Claude Agent SDK has a built-in tool that *spins up a sub-agent*.

Here is the trap, and it is the whole spirit of this course. Andrew: *"this is where you are able to basically spin up an agent. It was previously called the **task tool** … then the agent came along and I didn't realize that they're basically — it's just a name change, and so task is just no longer there."* The tool is now called **Agent**. But the old name **task** is still scattered through code, message types, and half-remembered docs — enough that Claude *itself* could not tell Andrew for certain which was which. His conclusion is the exam's favourite theme:

> As Andrew puts it: *"So task is agent, agent is task. Isn't it great? We always confirm and we don't just go based on this stuff. If you were to generate out your lesson plan based on this, you would be in poor trouble … even their docs don't make it clear."*

What the Agent tool actually gives you when you invoke it:

- **Its own isolated context.** The sub-agent does *not* see the parent's conversation. *"If you need your agent to know something, you need to provide it. Otherwise it only knows what you tell it."* This is exactly the coordinator discipline from Lesson 8 — the spokes never inherit the hub's context.
- **Its own system prompt** (its instructions) and **its own set of tools** (which may differ from the parent's — a research sub-agent might have web access the writer does not).
- **A blocking call by default.** This is the part everyone gets wrong. Spawning a sub-agent does *not* mean it runs in parallel. Andrew: *"though you're spinning up a sub-agent, it's not necessarily going to be parallelized … generally it's going to block the parent from doing anything until the single sub-agent is done and then come back."* One Agent-tool call = one sub-agent, run to completion, then control returns. Parallelism is a *separate* thing you must ask for (that is the next lesson).

To use it, you allow the Agent tool and register your sub-agents. Note the naming wrinkle Andrew flags: tool names show up **Title-cased in Python** (`Agent`) and **lowercase-underscored in the TypeScript** examples — another "which SDK am I even reading?" moment.

```python
# Illustrative reconstruction — adapt to the current SDK.
options = ClaudeAgentOptions(
    system_prompt="You are a coordinator that produces a short article on a topic.",
    model="claude-haiku-...",       # Andrew used Haiku for the demo
    allowed_tools=["Agent"],        # the built-in tool that spawns sub-agents
    agents={                        # the sub-agents it may spawn
        "researcher": researcher_def,
        "writer": writer_def,
    },
    # permission_mode="bypassPermissions",  # DO NOT ship this — see below
)

async for message in query(prompt="Write a short article about the James Webb telescope.",
                           options=options):
    print(message)
```

> ❌ **`bypassPermissions` is a "no no."** The generated code came back with `permission_mode="bypassPermissions"`, which, in Andrew's words, *"means that it can just do whatever it wants. And that is a no-no."* He deletes it on sight. Review generated config the way you review generated code — the model will happily hand you the most permissive setting.

> 🔑 **Spawning a sub-agent is one isolated, blocking unit of work. It has no parent context, its own prompt, its own tools — and it runs alone unless you explicitly ask for parallelism.** This is hub-and-spoke, now built into the SDK.

## Part 4: The agent definition — the blueprint, and where Python falls behind

Every sub-agent you register is described by an **agent definition**: *"the blueprint for the sub-agent. It defines what the agent is, what it knows about itself, and what is allowed to do before a single message is sent."*

The core fields:

| Field | What it is | Watch out |
|---|---|---|
| **name** | The sub-agent's identity (e.g., `researcher`) | *Very* sensitive — the name itself can cause the coordinator to trigger it or not. |
| **description** | When to use this agent | *"This is what's going to trigger the agent."* Write it deliberately, like a tool description. |
| **prompt** | Labelled `prompt`, but it is the **system prompt** — the agent's standing instructions | The name is misleading. Read `prompt` as "system prompt." |
| **tools** | The agent's **allowed tools** | Andrew renames it `allowed_tools` in his head for clarity; some APIs did call it that. |
| **disallowedTools** | Tools to explicitly forbid | — |
| **maxTurns** | Cap on the agent's internal loop iterations | **May be missing in Python.** |
| **model** | Which model this agent runs on | **May be missing in Python.** |
| *(also seen: mcpServers, skills)* | Extra capabilities | Availability varies by SDK. |

And here is the part that made Andrew re-record the video *four times*. He could not confirm the field list — not in the docs, not from Claude. When he tested it, *"the fields didn't match. And in fact there were fields that weren't there. Then I found out that there are some fields that are only available in the TypeScript SDK and some that are not available in the Python SDK."* His verdict:

> *"I literally found out that the Python SDK can be behind in features. And not only that, that the TypeScript one can be behind in features. So they don't have one-to-one SDKs … Make sure you test everything and do not trust what Claude generates. Do not trust what the docs say. You've got to go and test these things yourself."*

So the practical rule for the exam and for real work: **the Python and TypeScript Agent SDKs are not one-to-one.** If a field you need (say `maxTurns` or `model` on an agent definition) is missing in Python, the capability may only exist in TypeScript today. Discover this by *testing*, not by trusting a field list — the model hallucinated non-existent fields for Andrew repeatedly, and the docs *"weren't built for humans."*

> 💡 **How to actually find the truth when docs fail.** Andrew's escape hatch, when Claude kept guessing: point it at the *installed SDK source code* — *"I did also have it go and explore the actual codebase to find out the solution."* The library on disk is ground truth; the docs are a lagging description of it. When in doubt, read the code you already installed.

---

## Key takeaways

1. **Two SDKs, two altitudes.** The Anthropic SDK calls the model; the Claude Agent SDK builds the agent (decorators, sub-agents, hooks, and it runs the loop). Know which one a question is about.
2. **Decorator tools shrink the code.** `@tool` replaces hand-written JSON schemas, and your tools ship as an *internal* MCP server the SDK runs in-process. The tool-use call *"got easier."*
3. **Task is Agent, Agent is task.** The "task tool" was renamed the **Agent tool**; the old name lingers in code and message types. Confirm it yourself — even Claude and the docs get this wrong.
4. **A sub-agent is isolated and blocking.** It has no parent context, its own prompt and tools, and it does *not* run in parallel just because you spawned it. Parallelism is a separate, explicit choice (next lesson).
5. **The agent definition is the blueprint:** `name` (trigger-sensitive), `description` (what triggers it), `prompt` (really the system prompt), `tools` (allowed tools), plus `disallowedTools`, `maxTurns`, `model`. **Python lags TypeScript on some of these.**
6. **Trust what you build, not what you read.** Docs, model answers, and even the exam guide can be wrong. The architect's move is to test and draw a line back to verified fact.

## Common pitfalls

- ❌ **Assuming "task tool" and "Agent tool" are two different tools.** They are the same tool under two names. Allowing sub-agent spawning means allowing the Agent tool.
- ❌ **Expecting spawned sub-agents to run in parallel.** By default the parent *blocks* until the single sub-agent finishes. Do not design for concurrency you have not explicitly requested.
- ❌ **Forgetting the sub-agent has no context.** It only knows what you put in its definition and its prompt. Passing nothing and expecting it to "just know" is the classic hub-and-spoke mistake.
- ❌ **Reading `prompt` as a user message.** In an agent definition, `prompt` is the *system prompt* — the agent's standing instructions, not a one-off request.
- ❌ **Trusting a field list from the docs or the model.** Fields hallucinate; Python and TypeScript diverge. If a field is missing in Python, check whether it is TypeScript-only — by testing or reading the SDK source.
- ❌ **Shipping `bypassPermissions`.** The generator loves the most permissive mode. Strip it; grant only what the agent needs.

---

## 🛠️ Capstone Project: port Atlas Support's coordinator to the Claude Agent SDK

> This is the main hands-on project for the lesson. You will feel the code *shrink* as decorators replace schemas, then watch one isolated sub-agent do real work — and, most importantly, catch the SDK lying to you at least once and write it down.

### What you will build

You will take the Atlas Support coordinator you refactored in Lesson 11 and re-platform it onto the Claude Agent SDK, then give it its first *built-in* sub-agent. Atlas Support is the one system this whole course builds — a multi-agent support system that will eventually escalate to a human. This lesson contributes the piece it will stand on for every later feature: **the coordinator, now expressed in the Agent SDK**, so that parallelism (next), hooks, and MCP tools have somewhere to live.

Its pieces, each mapped to a lesson idea:

- A coordinator whose tools are **decorated functions** bundled into an **internal MCP server** (Parts 1–2).
- **One sub-agent** (start with a `researcher`) spawned through the **Agent tool** (Part 3).
- An **agent definition** for that sub-agent with `name`, `description`, `prompt`, and `tools` (Part 4).
- A short **`SDK_NOTES.md`** recording every doc/reality mismatch you hit (Parts 3–4 and the course theme).

### Why this is the perfect practice

| Lesson idea | Where you use it in Atlas Support |
|---|---|
| Anthropic SDK vs Agent SDK | Choosing the Agent SDK for the coordinator, keeping the option to drop down |
| Decorator tools + internal MCP | Milestone 1: re-express the coordinator's tools |
| The Agent tool spawns one isolated sub-agent | Milestone 3: the coordinator delegates to `researcher` |
| Blocking, not parallel | Milestone 4: confirm the parent waits |
| Agent-definition fields | Milestone 3: write and test the `researcher` blueprint |
| Python lags TypeScript / verify everything | Milestone 5: the `SDK_NOTES.md` log |

### Milestones (build them in order, each one works on its own)

1. **Decorate one tool.** Take a *single* coordinator tool, delete its hand-written JSON schema, and re-express it with `@tool(name, description, schema)`. Nothing else. Confirm it still imports.
2. **Stand up the internal MCP server.** Wrap your decorated tool(s) with `create_sdk_mcp_server(...)`, pass it via `ClaudeAgentOptions(mcp_servers=...)`, allow the tool, and run the coordinator end to end on the Agent SDK. Andrew's bar: *"I just want to make sure that it still runs."* This alone is a complete, shippable port of the tool layer.
3. **Add one sub-agent via the Agent tool.** Write an agent definition for a `researcher` (name, a trigger-worthy `description`, a `prompt`/system prompt, and a `tools` list — give it web access if your setup allows). Register it in `agents={...}`, add `"Agent"` to `allowed_tools`, and prompt the coordinator to *use the researcher* for one small task.
4. **Prove it blocks.** Add a print/log right after the Agent-tool call and confirm it only runs *after* the sub-agent returns. Write one sentence in your notes: "spawning is blocking, not parallel."
5. **Keep an `SDK_NOTES.md`.** Log every place reality diverged from the docs or the model: task-vs-Agent naming, any agent-definition field that hallucinated or that Python rejected, Title-case vs lowercase tool names. Note at least one **"Python lags TypeScript"** finding if you hit one.
6. **Strip the dangerous defaults.** Search your generated code for `bypassPermissions` (and any over-broad `allowed_tools`) and remove them. Grant the sub-agent only the tools it needs.
7. **Stretch goals.** Move your tools into a `make_coordinator_tools(state)` factory (closures, per Part 2) so tools live in their own module. *Or* register a second sub-agent (`writer`) with *no* web access and have the coordinator chain researcher → writer. *Or* try to set `maxTurns`/`model` on an agent definition in Python and record whether it works — if not, note it as a TypeScript-only capability.

### How you will know you are done

- ✅ The coordinator runs end to end on the Claude Agent SDK, and its tools are decorators bundled into an internal MCP server (no hand-written JSON schemas left).
- ✅ The coordinator successfully spawns the `researcher` sub-agent through the Agent tool and uses its result.
- ✅ You can state, from your own run, that spawning the sub-agent **blocked** the parent until it finished.
- ✅ Your `SDK_NOTES.md` contains at least one verified doc-vs-reality mismatch, and at least one "Python vs TypeScript" observation.
- ✅ No `bypassPermissions` anywhere; the sub-agent's tool list is minimal.

> 💡 **Keep yourself honest:** for every field and name in this lab, ask *"did I read that, or did I test it?"* If you only read it, you do not yet know it. Draw the line back to a run you watched.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice on one idea. Optional and independent; the Capstone already touches all of them, so feel free to skip straight to it.

### Exercise 1: Two-column SDK sort (foundational)
Write ten one-line capabilities (e.g., "run the agentic loop for me," "send raw messages and read `stop_reason`," "spawn a sub-agent," "define a tool with a JSON schema by hand"). Sort each into **Anthropic SDK** or **Claude Agent SDK**. Then name one job where you would *drop down* from the Agent SDK to the Anthropic SDK, and why.

### Exercise 2: Write a triggering description (intermediate)
For a `researcher` sub-agent, write three candidate `description` fields — one too vague, one too narrow, one just right. Predict which the coordinator will actually route to, then test it by giving the coordinator a borderline task and seeing which agent fires. Record what changed the trigger.

### Exercise 3: Find the SDK gap (advanced)
Pick one agent-definition field beyond the core four (`maxTurns`, `model`, `mcpServers`, or `skills`). Try to use it in the *Python* Agent SDK. If it fails or is ignored, open the installed SDK source (or the TypeScript types) and confirm whether it is TypeScript-only. Write a three-line note: field, Python result, where the truth lives.

---

## Cheat sheet

```text
TWO SDKs
  Anthropic SDK ....... low-level. Call the model. You write the loop (stop_reason).
  Claude Agent SDK .... high-level. Builds agents. Runs the loop. Decorators, sub-agents, hooks.
                        (= "Claude Code Agent SDK", same thing). Drop down for loop visibility/spend.

THE PORT (Agent SDK)
  @tool("name","desc",{schema}) ....... a tool is now a decorated function (no JSON block)
  create_sdk_mcp_server(tools=[...]) ... your tools ride an INTERNAL (in-process) MCP server
  ClaudeAgentOptions(mcp_servers=...) .. hand it over; the SDK runs the loop
  factory + closure ................... tools can live in their own module (runs at call time)
  after porting: RUN IT. "just make sure it still runs."

THE AGENT TOOL  (was: the "task tool" — same tool, renamed. task == Agent)
  - spawns ONE isolated sub-agent: own context, own system prompt, own tools
  - NO parent context: it knows only what you give it
  - BLOCKING by default: parent waits; spawning != parallel (parallelism is separate)
  - allow it: allowed_tools=["Agent"]   (Title-case in Python, lowercase_ in TS examples)

AGENT DEFINITION (the sub-agent blueprint)
  name ............ trigger-sensitive identity
  description ..... what triggers this agent (write it like a tool description)
  prompt .......... it is the SYSTEM prompt, despite the name
  tools ........... allowed tools
  disallowedTools / maxTurns / model / mcpServers / skills
  >>> Python SDK LAGS TypeScript on some fields (e.g. maxTurns/model). Not 1:1.

DANGER
  permission_mode="bypassPermissions" = "do whatever it wants" -> strip it.

ARCHITECT'S RULE
  Docs lie. The model hallucinates fields. SDKs diverge.
  Trust what you BUILD and TEST. Read the installed source when docs fail.
```

## How this connects to the rest of the course

- **Earlier, Module 3 · Lesson 8 & 11:** you hand-built the hub-and-spoke coordinator on the Anthropic SDK and refactored it into clean prompts/tools/lib modules. This lesson re-platforms *that* coordinator onto the Agent SDK — same architecture, less code.
- **Earlier, Module 1 · Lesson 3:** you drove the loop by hand off `stop_reason`. Now you can appreciate exactly what the Agent SDK is doing for you (and what it hides).
- **Next, Module 3 · Lesson 13 (Running agents in parallel):** you just learned the Agent tool is *blocking* by default. Next you make several sub-agents run at once — each in its own loop — by explicitly prompting for parallel tool calls.
- **Later, Module 4 (MCP):** the "internal MCP server" you met here is the same protocol you will use to connect *external* tools and read the flat tool list — the Agent SDK just pointed it inward.
- **Later, Module 6 · Lesson 22 (Sessions):** the "Python lags TypeScript" theme returns — resuming/forking sessions is another place the Python SDK needs a TypeScript detour. The judgment you practised here is the whole point.

---

*Source: the CCA-F course by Andrew Brown (ExamPro). Code snippets and diagrams are illustrative reconstructions of the patterns described in the course. The Claude Agent SDK is evolving and its Python and TypeScript libraries are not one-to-one — verify field names and availability against the SDK you have installed.*
