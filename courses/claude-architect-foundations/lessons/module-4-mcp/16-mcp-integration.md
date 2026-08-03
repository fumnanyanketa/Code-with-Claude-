# Module 4 · Lesson 16: MCP — discovery, resources, and building a server

> **Course:** Claude Certified Architect: Foundations, a self-paced course
> **Module 4:** Tools & MCP integration: the protocol Anthropic most wants you to know
> **Speaker:** Andrew Brown, ExamPro
> **Source:** Reconstructed from the CCA-F course by Andrew Brown (ExamPro) · [full transcript](../../transcripts/cca-f-full-course.txt)
> **Estimated time:** 45 to 60 minutes (read plus lab)

---

## In one sentence

MCP is the open standard Anthropic created for plugging external tools and data into an agent: you point your agent at one or more MCP servers, their capabilities are *discovered* at connect time into a single flat tool list, and each server can expose three kinds of thing — **tools** (actions), **resources** (read-only data mapped to a schema), and **prompts** (templates almost nobody uses) — a distinction the exam loves to test.

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone
> Project** where you build a small custom MCP server that gives **Atlas
> Support** a real tool *and* a read-only resource, backed by a local SQLite
> database. Everything before the Capstone teaches the pieces you will wire
> together there. If you want to see the finish line first, jump to the
> **"Capstone Project"** section, then come back.

## A few plain-language basics first

This lesson uses some terms that show up everywhere in the MCP domain. Here they are in plain words:

- **MCP (Model Context Protocol):** an open standard, *created by Anthropic*, for connecting agents to external tools, data, and prompts. Because Anthropic invented it, the exam wants you to know it cold.
- **MCP server:** a small program that exposes some capabilities (tools, resources, prompts) in the MCP format. Your agent is the *client* that connects to it. A server can wrap a database, an API, the filesystem — anything.
- **Tool / tool call / tool result:** a function the model can choose to run. When it decides to use one, that is a *tool call*; what comes back is the *tool result*. Tools are for *actions* (including actions that write or change data).
- **Resource:** an MCP capability that exposes **read-only** data described by a *schema* (a description of the shape and types of the data). Think "here is what my data looks like, read it directly."
- **Prompt (MCP prompt template):** a reusable prompt a server can offer. As you will see, these are rarely used in practice.
- **Schema:** a machine-readable description of data — its fields, their types, what is required. A resource carries one so the agent knows the shape of what it is reading.
- **SQLite:** a tiny database that lives in a single file on disk. No server to run, no setup — perfect for a lab.
- **CRUD:** the four basic data operations — **C**reate, **R**ead, **U**pdate, **D**elete.

You do not need to memorize these. Each is explained again the first time it matters.

## Why this lesson matters

MCP is the heart of Domain 2, and Anthropic weights it heavily precisely because they built it. As Andrew puts it, "within MCP there is more than just tools. There's also resources and prompts. Nobody uses prompt templates as they're not useful. But resources are, and they don't get talked about enough, and you definitely need to know them for the exam." Most people who use MCP only ever wire up tools and never touch resources — which is exactly why the resources-vs-tools distinction is a favorite exam trap. By the end of this lesson you will not only know the difference, you will have built a server that exposes both, so the distinction is muscle memory rather than a fact you half-remember.

## Learning objectives

By the end of this lesson you will be able to:

1. Explain what MCP is and what an MCP server exposes.
2. Describe **MCP discovery**: how multiple servers' capabilities load into one *flat* tool list at connection time, and why that flatness is a design consideration.
3. Point to where you register servers in the Agent SDK (the `mcp_servers` option).
4. Distinguish the three MCP primitives — **tools** (actions), **resources** (read-only, schema-mapped data), and **prompts** (mostly unused) — and defend the distinction on an exam.
5. Build a small custom MCP server that exposes tool-based CRUD plus a read-only resource, backed by a local SQLite database.

## Prerequisites

- **Module 3 · Lesson 15, "Prompt chaining vs adaptive decomposition"** — you should be comfortable with an agent taking a series of tool-driven steps.
- Earlier tool lessons in this module: you know what a tool call and tool result are.
- A working Agent SDK environment (from Module 0). This course does not re-cover installing the SDK.
- Comfort reading a little Python. The code here is illustrative — you will adapt it.

---

## Part 1: What MCP is, and why Anthropic cares so much

**MCP** — the Model Context Protocol — is an open standard Anthropic created so that any agent can talk to any external tool or data source through one common format. Instead of hand-writing a bespoke integration for every API and every database, you run (or connect to) an **MCP server** that speaks the protocol, and your agent — the *client* — connects to it.

The payoff is reuse. A well-built MCP server for, say, GitHub or a SQL database can be dropped into any MCP-aware agent. That is why the ecosystem matters, and why Anthropic pushes it: MCP is how Claude agents reach the outside world in a standard way.

Keep one framing in mind for the whole lesson: an MCP server can expose **three** kinds of capability — **tools**, **resources**, and **prompts**. Most tutorials only ever show you tools. Parts 3 and 4 are where the exam points hide.

> 🔑 **MCP is Anthropic's open standard for connecting agents to external tools and data via MCP servers. Because Anthropic created it, it is heavily weighted on the exam.**

## Part 2: MCP discovery — many servers, one flat tool list

Here is the mechanic the exam wants you to know. When you configure **multiple** MCP servers, Andrew explains, "all their tools are discovered and loaded at the connection time. And so the agent will treat it like a flat list with no awareness of which server comes from where."

Read that twice. Two ideas are packed in:

1. **Discovery happens at connect time.** When your agent connects to its servers, it asks each one "what can you do?" and loads every capability then and there. You do not enumerate tools by hand; the servers advertise them.
2. **The result is *flat*.** All the tools from all the servers land in one undifferentiated list. The agent does not know (and does not care) that `create_todo` came from your todo server while `search_issues` came from a GitHub server. There is no folder-per-server structure the model sees — just one big list of tools.

Where do you register the servers? In the Agent SDK, there is an **`mcp_servers`** option. Andrew is careful to flag that the snippet he shows is "just kind of a pseudo code" for the shape of it, not exact SDK syntax — but the idea is real: you specify the servers (and their launch commands or locations), the SDK installs/starts them individually, and "all these will just be available to the agent."

Illustrative shape (reconstruction — adapt to the current SDK):

```python
# Illustrative pseudo-code for the shape, not exact SDK syntax.
options = AgentOptions(
    mcp_servers={
        "todos":  {"command": "python", "args": ["todo_server.py"]},
        "github": {"command": "npx",    "args": ["-y", "@modelcontextprotocol/server-github"]},
    },
    allowed_tools=["mcp__todos__*", "mcp__github__*"],  # which discovered tools to allow
)
# At connect time, every tool from every server is discovered
# and flattened into ONE tool list the agent sees.
```

### The consideration the exam is fishing for

Flatness is convenient, but Andrew flags the catch: "you can see where this could run into an issue because now you have a bunch of different tools here." Wire up five chatty servers and the model suddenly faces dozens of similarly named tools with no grouping. That bloats the context, raises the odds of the model picking the wrong tool, and is exactly the kind of trade-off an exam question will probe. The fix in practice is to be selective — only allow the tools an agent actually needs (note the `allowed_tools` filter above) rather than dumping every server's full surface into the loop.

> 💡 **Discovery is automatic and eager.** You do not list tools one by one; you list *servers*, and their tools appear at connect time. Your control point is which servers you attach and which of their tools you allow — not hand-registering each function.

> 🔑 **Multiple MCP servers → all capabilities discovered at connect time → one flat tool list with no server awareness. More servers means more tools competing in one list, which is a real design consideration.**

## Part 3: The three primitives — tools, resources, prompts

Now the core exam content. An MCP server can expose three things, and Andrew is blunt about their relative importance:

| Primitive | What it is | Read/write | Used in practice? |
|---|---|---|---|
| **Tools** | Functions the agent calls to *do* something | Actions (read **or** write) | Constantly — this is what everyone uses |
| **Resources** | Read-only data mapped to a **schema**, read directly | **Read-only** | Underused, but exam-critical |
| **Prompts** | Reusable prompt templates the server offers | — | "Nobody uses prompt templates as they're not useful" |

**Prompts** you can almost set aside. In Andrew's words, "nobody uses prompt templates as they're not useful." Know they exist as the third primitive; do not expect to build with them.

**Tools** you have already met. They are "basically functions that are called," and often a tool "handles a domain of an API" — it acts as a buffer in front of some external system. Andrew's example: a tool that answers "what tables exist in the database." The tool "will call a function, which will make a database call, an SQL query, and return back those results." Crucially, tools can *do* things — including write, update, and delete. They are for **actions**.

**Resources** are the ones "that don't get talked about enough." Picture a plain API endpoint or a database that "is just going to return back data." Wrapping every such read behind a full tool call can feel heavy. So instead, Andrew explains, "resources has this schema that maps what the data looks like from your data source, and the idea is that it'll just read it directly, and so you'll get faster results. There'll be less back and forth." A resource says: *here is the shape of my data (the schema), read it.*

### The honest nuance Andrew hits live

Watch the build-and-verify theme land here. Andrew admits that when the AI generated the server, he learned something about his own mental model: "I always thought that it was a direct call and I never knew it was a function inside of this, because I don't really implement resources. I usually just implement tools." Under the hood a resource is *still backed by a function* — "it's still basically like a function, it's calling it" — "but I guess the difference is that it only expects read-only information," and it "follows this schema format."

So the clean mental model is not "tool = function, resource = magic direct pipe." Both run code. The real, testable difference is **intent and contract**:

- A **tool** is for **actions**. It can change state. The model calls it to *do* something.
- A **resource** is for **read-only data**, described by a **schema**, meant to be read directly for speed and less back-and-forth. As Andrew sums it up: "treat one as read-only, one as actions."

> 💡 **"Obviously you could put anything you want in here."** Nothing physically stops you from writing to a database inside a resource handler — but that breaks the contract. Resources are a *promise* of read-only. On the exam and in real design, honor it.

> 🔑 **EXAM TIP — resources vs tools vs prompts.** This is the MCP distinction most likely to appear on the exam:
> - **Tools = actions.** Functions the agent calls to *do* things; can read **or** write/change state.
> - **Resources = read-only data.** Backed by a function too, but they map your data to a **schema** and are read directly — faster, less back-and-forth. Never used to change state.
> - **Prompts = reusable templates.** The third primitive, but "nobody uses" them — knowing they exist is enough.
>
> If a question describes read-only, schema-mapped data pulled straight from a source, the answer is **resource**, not tool. Because most people only ever build tools, this is a favorite trap.

## Part 4: Building a custom MCP server (the todo server)

Time to build. Andrew's lab is a **custom MCP server that reads a local SQLite database** in a folder called `todos`, and it deliberately exposes *both* primitives:

- **Tools** for the write/action side — "create, update, edit, destroy to-dos" (that is CRUD).
- **A resource** for the read-only side — "an MCP resource to list out to-dos."

That split is the whole point: the *listing* is read-only data, so it belongs in a **resource**; *creating* and *deleting* change state, so they belong in **tools**. Building it this way makes the Part 3 distinction concrete instead of abstract.

Andrew's prompt to the AI, roughly: load a custom MCP server that can read a local SQLite3 database in a folder called `todos`; give it tool use to create, update, edit, and destroy todos; and give it an MCP **resource** to list out the todos.

### The build-and-verify lesson baked into this lab

This lab is also the course's core stance in miniature — *don't trust generated code, verify it*. The AI's first attempt worried Andrew: it reached for `anthropic` / `AsyncAnthropic` directly instead of the Agent SDK, and it went off "reading the whole darn thing" trying to find reference material. As he says, "it really just comes down to like, you know, is what you're looking at correct? Because you can see it can generate out variations of code that might work, but that doesn't mean it's good code."

What fixed it was giving the model the *right* reference — an inline MCP example — so it stopped guessing and produced "way, way better" code that actually used the Agent SDK and correctly set the MCP server via the `mcp_servers` option. The takeaway: generated MCP code often *looks* plausible while quietly using the wrong library or pattern. Read it, and confirm it runs and does what you meant.

### Illustrative shape of the server

A minimal reconstruction of the todo server — the tools do CRUD, the resource is read-only. Adapt to the current SDK; treat this as illustrative:

```python
# todo_server.py — illustrative reconstruction of an MCP server.
# Tools = actions (create/update/delete). Resource = read-only list.
import sqlite3
from mcp.server import Server

server = Server("todos")
db = sqlite3.connect("todos/todos.db")
db.execute("CREATE TABLE IF NOT EXISTS todos(id INTEGER PRIMARY KEY, text TEXT, done INTEGER DEFAULT 0)")

# --- TOOLS: actions that CHANGE state ---
@server.tool()
def create_todo(text: str) -> str:
    db.execute("INSERT INTO todos(text) VALUES (?)", (text,)); db.commit()
    return "created"

@server.tool()
def update_todo(id: int, done: bool) -> str:
    db.execute("UPDATE todos SET done=? WHERE id=?", (int(done), id)); db.commit()
    return "updated"

@server.tool()
def delete_todo(id: int) -> str:
    db.execute("DELETE FROM todos WHERE id=?", (id,)); db.commit()
    return "deleted"

# --- RESOURCE: READ-ONLY data, mapped to a schema, read directly ---
@server.resource("todos://list")
def list_todos() -> list[dict]:
    rows = db.execute("SELECT id, text, done FROM todos").fetchall()
    # Schema-shaped, read-only. No writes here — that is the contract.
    return [{"id": r[0], "text": r[1], "done": bool(r[2])} for r in rows]
```

Notice the asymmetry that *is* the lesson: three **tools** that write to the database, one **resource** that only reads from it. Both are backed by functions; only the tools are allowed to change anything.

### Watching it run

When Andrew ran the finished agent, it exercised exactly the loop you would want to demonstrate the difference: "it's listing it out [resource], and then it will go ahead and create some [tool], and then it's going to do an update [tool], it's going to do another read [resource]... now it's deleting [tool]." Reads go through the resource; changes go through tools. As he concludes, "they're both just functions, but the idea is that these are just read-only actions... treat one as read only, one as actions."

> ✅ **What to do about it:** when you design an MCP server, sort each capability by intent *before* you code it. Does it change state? Tool. Is it a read of schema-shaped data? Resource. That single sort is what the exam is testing and what keeps your servers clean.

## Part 5: How the pieces stack

Put the lesson together end to end:

```text
        YOUR AGENT (the MCP client)
                 │
                 │  attach servers via `mcp_servers` option
                 ▼
   ┌──── DISCOVERY at connect time ────┐
   │  ask each server "what can you do?" │
   └───────────────┬────────────────────┘
                   ▼
        ONE FLAT TOOL LIST  (no server awareness)
                   │
   ┌───────────────┼───────────────────────────┐
   ▼               ▼                            ▼
 TOOLS          RESOURCES                    PROMPTS
 actions        read-only, schema-mapped     templates
 read OR write  read directly, faster        "nobody uses"
   │               │
   └── create_todo └── list_todos  (todo server, SQLite)
       update_todo
       delete_todo
```

You attach *servers*; the agent *discovers* their capabilities into one flat list; each capability is a **tool**, a **resource**, or a **prompt**; and when you build your own server you deliberately put actions in tools and read-only data in resources.

---

## Key takeaways

1. **MCP is Anthropic's open standard** for connecting agents to external tools and data through MCP servers — heavily weighted on the exam because Anthropic created it.
2. **Discovery is eager and flat.** Attach multiple servers via the Agent SDK's `mcp_servers` option; at connect time all their capabilities load into one flat tool list with no server awareness. More servers = more tools competing — a real design consideration.
3. **Three primitives:** tools (actions), resources (read-only, schema-mapped data), prompts (templates almost nobody uses).
4. **Resources vs tools is the exam trap.** Both are backed by functions, but a resource is *read-only* and schema-described for direct, fast reads; a tool is for *actions* and can change state.
5. **Build a server by sorting on intent:** writes → tools, read-only reads → resources. The todo lab (tool CRUD + a resource list over SQLite) makes it concrete.
6. **Verify generated MCP code.** It often looks right while using the wrong library or pattern — "that doesn't mean it's good code."

## Common pitfalls

- ❌ **Thinking MCP means only tools.** It exposes tools, resources, *and* prompts. Missing resources is the single most common exam mistake.
- ❌ **Believing a resource is a "direct pipe" with no code.** It is still backed by a function; the difference is it is *read-only* and schema-mapped, not that it skips code.
- ❌ **Putting a read-only list behind a tool (or writing inside a resource).** It may run, but it breaks the contract the exam tests. Sort by intent.
- ❌ **Attaching every server "just in case."** A bloated flat tool list confuses the model. Allow only the tools an agent needs.
- ❌ **Shipping generated server code unread.** Andrew's own attempt reached for `AsyncAnthropic` instead of the Agent SDK. Read it, run it, confirm it.
- ❌ **Expecting to build with prompt templates.** "Nobody uses" them; know they exist and move on.

---

## 🛠️ Capstone Project: An MCP server that gives Atlas Support a tool and a resource

> This is the main hands-on project for the lesson. You will build the MCP
> component that **Atlas Support** — the multi-agent support system this course
> builds end to end — stands on: a custom server exposing one real **tool**
> (an action) and one read-only **resource**, backed by a local SQLite
> database. Small on purpose; the point is to *feel* the tool-vs-resource split.

### What you will build

A single custom MCP server, `atlas_support_server.py`, that wraps a local SQLite database of support tickets and exposes both primitives, plus a tiny agent that connects to it via the Agent SDK's `mcp_servers` option and exercises both:

- **A SQLite database** (`atlas/tickets.db`) with a `tickets` table (id, subject, status).
- **Tools (actions):** `create_ticket`, `update_ticket_status`, `delete_ticket` — full CRUD on the write side.
- **A resource (read-only):** `list_tickets` — schema-shaped ticket data read directly, never mutating state.
- **A small driver agent** that connects, lists tickets (resource), creates and updates one (tools), then lists again (resource) — proving the read/write split live.

### Why this is the perfect practice

| Lesson idea | Where you use it in the server |
|---|---|
| MCP server exposes capabilities | You author the whole server from scratch |
| Discovery via `mcp_servers` | Your driver agent registers the server there |
| Flat tool list | Your agent sees your tools + resource in one list |
| Tools = actions | `create/update/delete_ticket` change state |
| Resources = read-only, schema-mapped | `list_tickets` reads directly, never writes |
| Sort by intent | You decide which capability is which before coding |
| Build-and-verify | You run it and watch the read/write ordering |

### Milestones (build them in order, each one works on its own)

1. **Stand up the database.** Create `atlas/tickets.db` with a `tickets` table (id, subject, status). Smallest working version: a script that inserts one ticket and prints it back.
2. **Write the read-only resource first.** Add a `list_tickets` **resource** that returns schema-shaped rows and *only* reads. On its own, this already proves you can expose read-only data.
3. **Add the CRUD tools.** Add `create_ticket`, `update_ticket_status`, and `delete_ticket` as **tools**. Each changes state; each is deliberately *not* a resource.
4. **Register the server with an agent.** In a small driver script, attach the server via the `mcp_servers` option and confirm the tools and resource show up in the flat tool list.
5. **Drive the read/write loop.** Have the agent list tickets (resource), create one (tool), update its status (tool), then list again (resource). Watch reads go through the resource and changes through tools.
6. **Verify, do not trust.** Read the generated/handwritten code: is anything writing inside the resource? Is it actually using the Agent SDK? Run it and confirm the second listing reflects your changes.
7. **Stretch goals.** Add an `escalate_ticket` tool that flags a ticket for a human (foreshadowing Atlas Support's human-escalation finale); add a second read-only resource for a single ticket by id; add `allowed_tools` filtering so the agent only sees the capabilities it needs.

### How you will know you are done

- ✅ `atlas_support_server.py` exposes at least one **resource** (read-only list) and the three CRUD **tools**.
- ✅ A driver agent connects via `mcp_servers` and both the tools and the resource appear in its tool list.
- ✅ Running the driver shows reads served by the resource and state changes served by tools, and the final listing reflects the changes.
- ✅ You can point to each capability and say, without hesitating, "tool because it acts" or "resource because it is read-only."
- ✅ Nothing inside the resource handler writes to the database.

> 💡 **Keep yourself honest:** the moment you are tempted to make `list_tickets` also mark tickets as "seen," stop — that write belongs in a tool. Guarding that boundary *is* the exam skill.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice
> on one idea. Optional and independent; the Capstone already touches all of
> them, so feel free to skip straight to it.

### Exercise 1: Sort the capabilities (foundational)
Take ten realistic MCP capabilities ("list open orders", "refund an order", "get product schema", "cancel a subscription", …) and label each **tool** or **resource**. For every one, write the one-word reason: *action* or *read-only*. Check yourself against the Part 3 exam tip.

### Exercise 2: Two servers, one flat list (intermediate)
Sketch (in pseudo-code) an `mcp_servers` config attaching your todo/ticket server *and* one public MCP server. Predict the flat tool list the agent will see, then name one problem that appears once both servers' tools mix, and one way to reduce it.

### Exercise 3: Break and defend the contract (advanced)
Deliberately add a write to your `list_tickets` resource, run the agent, and observe that it "works." Then write two sentences on why it is still wrong — what promise you broke and how an exam question would score it. Revert the change.

---

## Cheat sheet

```text
MCP — Model Context Protocol (Anthropic's open standard; exam-heavy)
--------------------------------------------------------------------
WHAT   Standard way to connect an agent (client) to MCP servers that
       expose external tools + data.

DISCOVERY
  - Attach SERVERS (not individual tools) via Agent SDK `mcp_servers`.
  - At CONNECT TIME every capability loads into ONE FLAT tool list.
  - Agent has NO awareness of which server a tool came from.
  - More servers = more tools competing = a design consideration.
       -> allow only the tools each agent needs.

THREE PRIMITIVES
  TOOLS      actions; functions the agent calls; can READ or WRITE
  RESOURCES  READ-ONLY data, mapped to a SCHEMA, read directly
             (faster, less back-and-forth). Still backed by a function.
  PROMPTS    reusable templates — "nobody uses" them; just know they exist

EXAM TIP (resources vs tools)  <-- most-tested MCP point
  Read-only, schema-mapped data pulled from a source  -> RESOURCE
  Something the agent DOES / that changes state        -> TOOL
  Both run code; the difference is INTENT + read-only contract.

BUILD A SERVER (todo / ticket lab)
  Tools:     create / update / delete   (CRUD, actions)
  Resource:  list                       (read-only)
  Backed by: local SQLite (single file, no server to run)
  Sort every capability by intent BEFORE coding it.

STANCE
  Generated MCP code often looks right but uses the wrong lib/pattern.
  "That doesn't mean it's good code." -> read it, run it, verify it.
```

## How this connects to the rest of the course

- **Earlier, Module 3 · Lesson 15, "Prompt chaining vs adaptive decomposition":** you learned to sequence an agent's steps. MCP is *where those steps reach the outside world* — the tools and resources the agent acts through.
- **Earlier in this module:** you defined tools by hand; MCP is how you package and share them as reusable servers, and how you add read-only resources alongside them.
- **Next, Module 5 · "Settings scopes and precedence":** you shift from *what* an agent can reach to *how* you configure and constrain it — including which MCP servers and tools are allowed where.
- **Later, across Atlas Support:** the ticket server you build here becomes the data-and-action backbone the support agent uses when it finally escalates to a human. Your resource lists the tickets; your tools act on them.

---

*Source: reconstructed from the "Claude Certified Architect: Foundations" course by Andrew Brown (ExamPro). Code snippets and diagrams are illustrative reconstructions of the patterns described in the course. Adapt them to the current SDK.*
