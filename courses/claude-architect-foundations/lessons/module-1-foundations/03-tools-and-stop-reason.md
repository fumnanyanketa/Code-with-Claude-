# Module 1 · Lesson 3: Tools and the stop-reason loop

> **Course:** Claude Certified Architect: Foundations, a self-paced course
> **Module 1:** Foundations: how Claude agents work — the exam map plus the agentic loop, tools, and stop-reason loop everything else is built on.
> **Speaker:** Andrew Brown, ExamPro
> **Source:** Reconstructed from the CCA-F course by Andrew Brown (ExamPro) · [full transcript](../../transcripts/cca-f-full-course.txt)
> **Estimated time:** 45 to 60 minutes (read plus lab)

---

## In one sentence

An agent gets things done by calling **tools** — plain code functions it can choose to run — and you drive that behaviour yourself by making one API call, reading the `stop_reason` field it hands back, running any tool it asked for, appending the result to the conversation, and calling the API again, looping until `stop_reason` says `end_turn`.

> 🎯 **Where this lesson is heading.** This is the first real hands-on lesson. It builds to a **Capstone Project** where you write a minimal single-tool agent loop from scratch — no framework, just the API and a `while` loop. That tiny program is the seed the whole north-star project, **Atlas Support**, will grow from. Everything before the Capstone teaches the four moves the loop is made of. If you want to see the finish line first, jump to the **"Capstone Project"** section, then come back.

## First-principles companion

> 💡 **The durable idea behind this lesson.** SDK names and endpoints change, but the shape of a tool definition does not. A tool's `input_schema` is written in **JSON Schema** — a small, tool-agnostic standard for describing the shape of JSON data (types, which fields are required, allowed values).
>
> - **[JSON Schema — "Getting Started"](https://json-schema.org/learn/getting-started-step-by-step)** (official docs). The timeless account of the `type` / `properties` / `required` structure you will type into every tool you ever define, for any model or provider.

## A few plain-language basics first

This lesson uses some everyday terms. Here they are in plain words:

- **LLM:** the kind of AI that reads and writes text; "Claude" is one. On its own it can only produce text.
- **Model:** one specific version of Claude — e.g. Opus, Sonnet, Haiku — differing in strength, speed, and price. Sonnet is the balanced default.
- **API:** a way for your own program to send a request to Claude over the internet and get a reply back, instead of typing into a chat box.
- **SDK:** a ready-made code library (here, the **Anthropic SDK** for Python) that wraps the API so you call a function instead of building web requests by hand.
- **Agent:** an AI that takes a series of actions on its own toward a goal, rather than answering in one shot.
- **Agentic loop:** the repeating cycle an agent runs — gather context, take action, verify — until the task is done.
- **JSON:** a plain-text way of writing structured data (lists, and `name: value` pairs). It is how your program and Claude pass structured information back and forth.
- **API key:** a secret password string that identifies your account so the API knows who to bill. You keep it out of your code, usually in an environment variable.

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

In the last lesson you learned that the agentic loop is *gather context → take action → verify*, and that Claude Code runs that loop for you. This lesson is where you pull the curtain back and run the loop **yourself**, by hand, in about thirty lines of Python. As Andrew puts it, "we are learning by doing it manually. It helps us see what's going on." Once you have watched a single tool call flow out of Claude, run in your code, and flow back in, every framework you meet later — the Claude Agent SDK, hub-and-spoke coordinators, MCP — stops being magic. It is all this same four-step loop underneath.

There is a second reason, and it is on the exam. The CCA-F guide names `stop_reason` in Domain 1, so, in Andrew's words, "that's why we're talking about stop reason." Knowing that you steer an agent off a structured field — never by reading its prose — is a load-bearing idea you will lean on for the rest of the course.

## Learning objectives

By the end of this lesson you will be able to:

1. Explain what a tool is (a code function the model can choose to run) and give examples of tools used in each phase of the agentic loop.
2. Define `stop_reason` and its two values, `tool_use` and `end_turn`, and say what each one tells your program to do next.
3. Define a single tool for the Anthropic API with a name, a description, and a JSON-Schema `input_schema`.
4. Write the core loop by hand: make the API call, branch on `stop_reason`, run the requested tool, append a `tool_result`, and repeat until `end_turn`.
5. Recognise and fix the classic runaway loop caused by never re-calling the API inside the loop.

## Prerequisites

- **Module 1 · Lesson 2 ("The agentic loop and Claude Code")** — you should be comfortable with *gather context → take action → verify* and with the idea that Claude picks a model (opus/sonnet/haiku) per run.
- **Module 0** (optional on-ramp) — Python installed, the `anthropic` package available, and an API key. If you skipped it: you need Python, `pip install anthropic`, and a small amount of credit loaded on your Anthropic account. As Andrew warns, "there's no free tier for the API usage" — five or ten dollars is plenty for this whole course.

---

## Part 1: What a tool actually is

Start with the plainest possible definition, straight from Andrew: "tools are code functions that an agent is aware of and can invoke to complete their tasks. And when I say they're code functions, I literally mean it's just a code function."

That is the whole idea. A **tool** is an ordinary function in your program — `get_weather(city)`, `read_file(path)` — that you have told the model about. When the model decides to use one, that is a **tool call**; whatever your function returns is the **tool result**.

Why does an LLM need this at all? Because, as Andrew says, "the LM is in its own little box... it can just produce text. And so it needs some way of interacting with external programs." The model cannot read your files, hit a database, or check today's weather. It can only write text. A tool is the model's hands: it writes out *"I want to call `get_weather` with `city=Winnipeg`"*, your code actually runs the function, and you feed the answer back.

> 🔑 **A tool is just a normal function you have described to the model. The model never runs it — it only *asks* you to. Your code does the running.**

### Tools show up in every phase of the loop

Remember the three phases from Lesson 2. Every one of them reaches for tools. Andrew walks the example of fixing a failing Python unit test:

| Loop phase | What the tool does there | Example tools |
|---|---|---|
| **Gather context** | Pull in information the model doesn't have | read a file, search an API, query a database, scan the codebase (this is RAG — retrieval-augmented generation), check system state |
| **Take action** | Change something in the world | edit code, run a command, write a file, call an API, execute a script |
| **Verify results** | Confirm the action worked | run the test (`pytest`), compile the code, read the output, check logs, compare results |

Andrew's note on the "gather context" row is worth keeping: reaching out to a database to enrich the model's context "is a rag" — retrieval-augmented generation — but with agents "it just kind of seamlessly happens... we don't even think about it." You do not need a separate RAG framework; a tool that fetches data *is* your retrieval step.

Claude Code ships with built-in tools in roughly five categories: file operations, search-and-find, execution (run commands), web search, and code intelligence. When you asked "can Claude Code make its own tools?" — yes, and you will build custom ones later (skills, MCP). For now the point is smaller: **without tools, "no code would be changed... it would just be talking to you."**

## Part 2: `stop_reason` — the field you steer by

Here is the single most important field in this lesson. When you make an API call, the JSON that comes back includes a field called `stop_reason`. In Andrew's words, "stop reason is the reason why the claude agent has stopped executing its loop."

For our purposes it takes one of two values:

- **`tool_use`** — "this is when the agent stops with the intention to call an external function." Claude has decided it needs a tool and is telling you which one, with what inputs. It is now *your* move.
- **`end_turn`** — "this is when the agent has decided to return you a result because it's done." No tool wanted; the text reply is the final answer.

Picture Andrew's weather example. You ask, "what is the weather in Winnipeg?" Claude replies with something like *"Let me check the weather for you,"* and alongside that text it emits a **tool_use** block naming the tool `get_weather` with input `Winnipeg` — the city it extracted from your question. The top-level `stop_reason` on that response is `tool_use`. Claude has not answered the weather question; it has asked *you* to go get the data.

> 🔑 **You drive the loop off `stop_reason`, never off reading Claude's text.** `tool_use` means "run something and come back"; `end_turn` means "we're done." This one branch is the engine of every agent you will build.

> ❌ **The trap this closes:** trying to figure out whether Claude is finished by scanning its prose for phrases like "here is your answer." That is fragile and wrong. The API already tells you, in a structured field. Read the field.

## Part 3: The four-move loop — how a tool call flows out and back

A tool call is a round trip. Claude asks; you answer; Claude continues. The mechanic that makes this work is **appending** — you keep adding to the running list of messages. Andrew's framing: "whatever the result is, we're appending it to our message conversation."

One subtlety he flags: `stop_reason` lives on the *response*, not inside your message list. "What's in the messages is not the same of what is being outputted." So you will see `stop_reason` when you inspect each API response, but it never becomes part of the conversation history you send back. The history carries the tool *request* and the tool *result*; the `stop_reason` is just your signal for what to do between calls.

Here is the whole cycle as four moves:

```text
   your message: "Will I be a billionaire on Mars in 2026?"
            │
            ▼
   (1) call the API  ──────────────►  response, stop_reason = ?
            │
            ├── end_turn  ──►  print the text.  DONE.
            │
            └── tool_use  ──►  (2) read the tool_use block: which tool? what input?
                                   (3) run that function in your code
                                       append the assistant's tool_use turn
                                       append a tool_result turn (with the tool_use_id)
                                   (4) loop back to (1) with the longer message list
```

Move 1 is one API call. Move 2 reads what Claude asked for. Move 3 runs it and writes the answer back into the conversation. Move 4 goes around again. You keep going until move 1 comes back `end_turn`. That is the entire lesson — four moves in a `while` loop.

> ✅ **What to do about it:** every time around the loop you must (a) make a *fresh* API call with the updated messages, and (b) check the new response's `stop_reason`. Skipping either one is how the loop breaks — as you are about to see.

---

## Key takeaways

1. **A tool is just a function you described to the model.** The model asks to call it; your code runs it and returns the result. The LLM can only produce text on its own.
2. **Tools appear in all three loop phases.** Gather context (read/search/query), take action (edit/run/write), verify (test/compile/compare).
3. **`stop_reason` is how you steer.** `tool_use` = run a tool and come back; `end_turn` = finished. Branch on this field, never on the model's prose.
4. **A tool call is a round trip you append.** Assistant's `tool_use` in, your `tool_result` back, then loop. The `tool_use_id` ties a result to its request.
5. **The loop ends when `stop_reason` stops being `tool_use`.** You must re-call the API inside the loop or it never updates — and never ends.

## Common pitfalls

- ❌ **Never re-calling the API inside the loop.** Andrew's own loop "looped forever" for exactly this reason: "you never update the response inside the loop." If `response` never changes, `stop_reason` is `tool_use` forever. Fix: assign `response = client.messages.create(...)` *inside* the `while`.
- ❌ **Picking a tool the model can do on its own.** Andrew first tried an "add two numbers" tool, then realised "this is obviously something that the agent would be capable of doing... so it might make it hard for it to know" whether to call it. Choose a tool for something the model *can't* just do in its head — a lookup, a live value, a deterministic action.
- ❌ **A vague tool description.** The description is how Claude decides *when* to reach for the tool. Andrew is deliberate: "use this tool to add two numbers together... I'm being prescriptive... that way it helps it to know how to select the correct tool." Write the description as an instruction, not a label.
- ❌ **Forgetting to append the assistant's `tool_use` turn before the `tool_result`.** The API needs both halves in order. If you append only the result, the `tool_use_id` it refers to isn't in the history and the call is rejected.
- ❌ **Reading `response.content[0]` and assuming it's text.** When `stop_reason` is `tool_use`, the content is a list of *blocks*; you have to iterate to find the `tool_use` one. "You do kind of have to iterate to get to the correct one."

---

## 🛠️ Capstone Project: the seed of Atlas Support — a single-tool agent loop

> This is the main hands-on project for the lesson. You will hand-write the smallest possible agent: one tool, one loop, driven entirely by `stop_reason`. It is deliberately tiny — and it is the exact skeleton every later Atlas Support component bolts onto. "We are going to reap the benefits of this code going forward."

### What you will build

A short Python program, `main.py`, that:

- defines **one** tool with a name, a prescriptive description, and a JSON-Schema `input_schema`;
- sends a user question plus that tool to the API in a `while` loop;
- reads `stop_reason`, and when it is `tool_use`, finds the tool block, **runs the real function**, and appends a `tool_result`;
- keeps looping until `stop_reason` is `end_turn`, then prints Claude's final text.

Because Atlas Support will be a *support* agent, use a support-flavoured tool the model genuinely cannot answer on its own — say `lookup_order_status(order_id)` that returns a canned status string. (If you'd rather mirror the transcript exactly, use Andrew's `magic_eightball(question)` that returns a random yes/no verdict. Either works; the point is the loop.)

Here is an illustrative reconstruction of the whole thing. Read it, then build it move by move via the milestones below.

```python
import anthropic

client = anthropic.Anthropic()      # reads ANTHROPIC_API_KEY from your environment
MODEL = "claude-sonnet-4-5"         # use a current Sonnet id — the cost/quality "goldilocks"

# --- the one tool: a lookup the model cannot do on its own ---
tools = [
    {
        "name": "lookup_order_status",
        "description": "Use this tool to look up the status of a customer's order by its order id.",
        "input_schema": {
            "type": "object",
            "properties": {
                "order_id": {"type": "string", "description": "The customer's order id, e.g. A-1042"}
            },
            "required": ["order_id"],
        },
    }
]

def lookup_order_status(order_id):
    # a real tool would hit a database; we fake it deterministically
    return f"Order {order_id}: shipped, arriving Tuesday."

# --- the running conversation ---
messages = [
    {"role": "user", "content": "Where is my order A-1042?"}
]

while True:
    # MOVE 1: one API call, with the tool available
    response = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        tools=tools,
        tool_choice={"type": "auto"},   # let Claude decide; we'll force tools in a later lesson
        messages=messages,
    )
    print("stop_reason:", response.stop_reason)

    if response.stop_reason != "tool_use":
        break                           # end_turn — Claude is done

    # record Claude's turn (it holds the tool_use block) before we answer it
    messages.append({"role": "assistant", "content": response.content})

    # MOVE 2 + 3: find each tool block, run it, collect the results
    tool_results = []
    for block in response.content:
        if block.type == "tool_use":
            print("Claude wants:", block.name, block.input)   # move 2
            result = lookup_order_status(**block.input)        # move 3: run the real function
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": block.id,      # ties this result to Claude's request
                "content": result,
            })

    # append the results as the next user turn, then MOVE 4: loop back to MOVE 1
    messages.append({"role": "user", "content": tool_results})

# the loop only exits on end_turn — print the final answer
print(response.content[0].text)
```

### Why this is the perfect practice

| Lesson idea | Where you use it in the Capstone |
|---|---|
| A tool is a described function | The `tools` list + the real `lookup_order_status` function |
| JSON-Schema `input_schema` | `type` / `properties` / `required` on the tool |
| Branch on `stop_reason` | `if response.stop_reason != "tool_use": break` |
| Round-trip by appending | Append the `assistant` turn, then the `tool_result` turn |
| Re-call the API each pass | `response = client.messages.create(...)` *inside* the `while` |

### Milestones (build them in order, each one works on its own)

1. **One call, one tool.** Write the tool definition and make a *single* API call (no loop yet) with `tools=tools` and a question that should trigger it. Print the whole response. Success = you see `stop_reason: tool_use` and a `tool_use` block in the content. (Tip from Andrew: pretty-print with `print(response.model_dump_json(indent=2))` so the structure is readable.)
2. **Detect and announce the call.** Iterate `response.content`, find the block whose `type == "tool_use"`, and print its `name` and `input`. Success = your program prints exactly which tool Claude wants and with what arguments — without you having run anything yet.
3. **Run it and append the result.** Call the real function with `**block.input`, then append two turns to `messages`: the assistant's `response.content`, and a `user` turn holding a `tool_result` block (with the matching `tool_use_id`). Make one more API call by hand and confirm the new `stop_reason` is `end_turn`. Success = a second, final response comes back done.
4. **Close the loop.** Wrap it all in `while True`, `break` on anything that isn't `tool_use`, and re-assign `response` on every pass. Success = you run the file once and it drives itself to completion, printing the final text answer.
5. **Stretch goals.** Ask a question that needs *no* tool ("Hi, are you there?") and confirm you get `end_turn` on the first pass. Add a second tool and a question that should pick the *other* one. Swap in `magic_eightball` to match the transcript. Add a max-iteration counter — a preview of the very next lesson.

### How you will know you are done

- ✅ Running `python main.py` prints at least one `stop_reason: tool_use`, then a final `stop_reason: end_turn`, then a sensible text answer that used your tool's result.
- ✅ Your `while` loop terminates on its own — it does not run forever.
- ✅ You can point to the exact line that (a) branches on `stop_reason`, (b) runs the tool, and (c) appends the `tool_result` with its `tool_use_id`.
- ✅ If you delete the `response = client.messages.create(...)` line from inside the loop, you can explain why it now loops forever.

> 💡 **Keep yourself honest:** before you write the loop, run just milestone 1 and read the raw JSON. Andrew's whole method is "validate all these things actually work as expected, and the only way to do that is to do it." Seeing the real `tool_use` block once is worth more than any diagram.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice on one idea. Optional and independent; the Capstone already touches all of them, so feel free to skip straight to it.

### Exercise 1: Read a real response (foundational)
Make a single tool-triggering call and pretty-print the response as JSON. In the output, point to: the top-level `stop_reason`, the `tool_use` block, its `id`, its `name`, and the `input` Claude extracted. No loop, no execution — just learn to read the shape.

### Exercise 2: Description-driven selection (intermediate)
Define two tools, `lookup_order_status` and `open_support_ticket`, and send three different questions. Confirm Claude picks the right tool each time based purely on your descriptions. Then weaken one description to a bare label (e.g. `"orders"`) and watch selection get worse. This is why Andrew is "prescriptive" with descriptions.

### Exercise 3: Break it on purpose (advanced)
Take your finished loop and comment out the `response = client.messages.create(...)` line inside the `while`. Run it, watch it loop forever, then stop it. Write one sentence explaining the cause ("`response` never updates, so `stop_reason` is `tool_use` forever"). Fixing a bug you created cements the lesson better than avoiding it.

---

## Cheat sheet

```text
TOOL  = a code function you describe to the model. The model asks; your code runs it.
        Choose tools for things the model CAN'T do itself (lookups, live data, actions).
        Description = an instruction ("Use this tool to..."), it drives selection.

TOOL DEFINITION (Anthropic API):
  name          short id, e.g. "lookup_order_status"
  description   prescriptive: when to use it
  input_schema  JSON Schema: { type:"object", properties:{...}, required:[...] }

stop_reason  (on the RESPONSE, not in your messages) — how you steer:
  "tool_use"  -> Claude wants a tool. YOUR move: run it, append result, loop.
  "end_turn"  -> Claude is done. Print the text. Stop.

THE FOUR-MOVE LOOP:
  1. response = client.messages.create(model, tools, tool_choice, messages)
  2. if stop_reason != "tool_use": break        # find the tool_use block(s)
  3. run function(**block.input)
     append assistant turn (response.content)
     append user turn: {type:"tool_result", tool_use_id:block.id, content:result}
  4. loop back to 1 with the longer messages list

#1 BUG: re-assign `response` INSIDE the loop, every pass. Forget it -> infinite loop.
tool_choice="auto" for now (Claude decides). Forcing tools comes in a later lesson.
```

## How this connects to the rest of the course

- **Earlier, Module 1 · Lesson 2 ("The agentic loop and Claude Code"):** you learned the *gather context → take action → verify* loop conceptually and saw Claude Code run it. This lesson is that same loop, but you are the one running it — tools are how the phases touch the world, and `stop_reason` is the signal that decides each pass.
- **Next, Module 1 · Lesson 4 ("Loop antipatterns and ending the loop correctly"):** you will harden this exact loop — always driving control flow off `stop_reason` (never by parsing text) and capping runaway loops with a max-iteration break, turning the "stretch goal" counter into a proper safety net.
- **Later, Module 2 · Lesson 6 ("Forcing structured output"):** the `tool_choice: auto` you set here becomes a deliberate choice (`auto` / `any` / `tool` / `none`), and the `input_schema` you wrote becomes the way you force clean JSON out of the model.
- **Much later, Module 3 onward:** this single-tool loop grows into Atlas Support — a hub-and-spoke coordinator whose sub-agents are exposed to it *as tools*. The round trip you just built is the atom every one of those agents is made of.

---

*Source: reconstructed from the CCA-F course by Andrew Brown (ExamPro). Code snippets and diagrams are illustrative reconstructions of the patterns described in the course. Model ids and SDK details change — adapt them to the current Anthropic SDK.*
