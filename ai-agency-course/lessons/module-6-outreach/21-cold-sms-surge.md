# Module 6 · Lesson 21: Cold SMS Surge

> **Course:** The AI Agency Blueprint, a self-paced course
> **Module 6:** Outreach: getting your first appointments with cold SMS and cold calling
> **Speaker:** Owen Rensland, founder, AI Agency / SMMA course
> **Source talk:** [AI Agency Full Course (Owen Rensland)](https://www.youtube.com) · [full transcript](../../transcripts/ai-agency-full-course.txt)
> **Estimated time:** 55 to 70 minutes (read plus exercises)

---

## In one sentence

Cold SMS is a no-ad-budget appointment machine — you scrape a list of local businesses, validate the numbers, drip a three-message Hook / Pitch / Follow-up sequence out of your CRM, and call the moment someone replies — but it only works if you first make it legally compliant, because texting strangers is heavily regulated and getting it wrong carries real financial and legal risk.

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone Project** where you stand up the whole cold-SMS system end to end AND write a compliance checklist for your own country/state, then prove it works with one compliant test send to your own phone that triggers the call-and-book flow. Everything before the Capstone teaches the skills you will use there. If you want to see the finish line first, jump to the **"Capstone Project"** section, then come back.

## First-principles companion

> 💡 **The durable idea behind this lesson.** The tools (GoHighLevel, Clear Out Phone) will change; the underlying idea — *permission-based outreach that identifies the sender and offers an easy opt-out* — is law, not a trend. For the timeless, tool-agnostic version:
>
> - **[FCC rules on the TCPA and text messaging](https://www.fcc.gov/consumers/guides/stop-unwanted-robocalls-and-texts)** (US regulator). The plain-English account of why consent, sender identification, and honoring "STOP" are not optional when you text a phone you do not have a prior relationship with.
> - **[CTIA Messaging Principles and Best Practices](https://www.ctia.org/)** (the trade body carriers follow). The rulebook the phone carriers actually enforce through A2P 10DLC registration.

## A few plain-language basics first

This lesson uses some everyday terms. Here they are in plain words:

- **Cold SMS:** a text message you send to a business or person who has **not** asked to hear from you and has no prior relationship with you. "Cold" means no prior contact.
- **Lead:** a business you might want as a client — here, usually a name, a phone number, and a company name.
- **Scraping:** collecting public business info (names, phones) from a source like Google Maps or the Better Business Bureau into a spreadsheet.
- **CRM:** "customer relationship management" software — the database that stores your leads and sends the texts. Owen uses GoHighLevel (GHL).
- **Drip campaign:** an automation that sends messages on a timed schedule (e.g. 5 texts every 5 minutes) instead of all at once.
- **A2P 10DLC:** "Application-to-Person, 10-Digit Long Code" — the mandatory US registration that tells phone carriers who you are before they let your business software send texts from a normal phone number. Covered in Module 4.
- **TCPA:** the US **Telephone Consumer Protection Act**, the federal law that governs unsolicited calls and texts to consumers.
- **Opt-out:** the recipient's right to stop your messages, usually by replying "STOP." You must honor it instantly and forever.
- **DNC / do-not-contact:** a list of numbers you are forbidden to contact. Scrubbing means removing those numbers from your list before you send.

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

If you have zero ad budget, cold SMS is the single fastest way to fill your calendar — Owen says flatly, *"this system alone... took me to 20K a month. No paid ads. Only this system."* But that upside comes attached to the most legally dangerous tactic in the whole course. Sending one text to a stranger is trivial; sending it *compliantly* is the actual skill. This lesson teaches both, and it puts the compliance first on purpose — because the difference between "free appointment machine" and "expensive legal problem" is entirely in the setup you do before the first text goes out.

## Learning objectives

By the end of this lesson you will be able to:

1. State the compliance requirements for cold SMS in your own jurisdiction and decide whether you can legally run it at all.
2. Register/confirm your A2P 10DLC campaign, add sender identification and a STOP opt-out, and scrub your list against do-not-contact numbers.
3. Scrape a list of local-business leads and organise them in a master lead list.
4. Validate phone numbers to drop landlines so you only text real mobiles.
5. Write a Hook / Pitch / Follow-up (HPF) three-message sequence.
6. Import leads into a CRM and run a timed drip (about 5 texts every 5 minutes) with a sane daily cap.
7. Call within 5 minutes of a positive reply and book the appointment live, on the phone.

## Prerequisites

- **Lesson 20** (the previous outreach lesson) — you should already understand why outreach volume drives your whole business.
- **Module 4 (Infrastructure)** — your CRM/GoHighLevel sub-account is set up and, critically, your **A2P 10DLC registration** is done. Do not send a single cold text until this is complete.

---

## Part 1: Compliance first — "do this compliantly, or don't do it"

Before any tactics, the non-negotiable part. Cold, unsolicited SMS is one of the most heavily regulated things in this entire course, and the rules are not a formality — they carry real financial and legal exposure.

> 🔑 **Cold SMS is not "send texts and see who bites." It is "prove you are allowed to text this person, identify yourself, give them an easy way out — and only then send."**

Here is the landscape, by region. **You must check your own before you send.**

| Region | The rules in short | Reality |
|---|---|---|
| **United States** | **TCPA** (federal) + carrier **A2P 10DLC** registration are required. Messages need clear sender identification and a working opt-out (STOP). | Texting consumers without consent carries real legal exposure — TCPA statutory damages run **$500–$1,500 per message**. Class actions happen. |
| **UK / EU** | **PECR** and **GDPR**. Marketing texts generally require **prior consent**; unsolicited B2C marketing SMS is effectively **prohibited**. | Often flatly not allowed for consumers. Regulators (ICO in the UK) fine for it. |
| **Canada** | **CASL** — one of the strictest anti-spam laws in the world. | Commercial electronic messages generally need consent; penalties are severe. Cold SMS is usually a no-go. |

Even in the US, where this can be done, "can" means "after you do the setup." Your compliance checklist, every time:

> ✅ **What to do about it — the pre-send checklist:**
> 1. **Register your A2P 10DLC campaign** (Module 4) so carriers know who you are. Unregistered traffic gets filtered or blocked anyway.
> 2. **Identify yourself** in the message — your name and/or business — so it never reads as anonymous spam.
> 3. **Honor STOP / opt-outs instantly and permanently.** GHL and most CRMs auto-handle "STOP," but confirm it is on and never re-add an opt-out.
> 4. **Scrub against do-not-contact lists.** Remove any number on a DNC list or any number that ever opted out.
> 5. **Check your jurisdiction BEFORE sending a single text.** If you are in the UK/EU/Canada, assume you cannot cold-SMS consumers and use another channel (e.g. cold calling, next lesson) instead.

> ⚠️ **Reality check.** Owen's course frames cold SMS as "so simple, don't overcomplicate it." The *sending* is simple. The *legality* is not, and he does not dwell on it. Treat the compliance checklist above as the price of admission. If you cannot tick every box for your location, the correct move is to not run cold SMS — do cold calling (Lesson 22) or paid ads (Module 5) instead. This is a "do it compliantly or don't do it" tactic.

## Part 2: The system at a glance

Owen's promise is that the flow is genuinely simple. Once compliance is handled, the whole machine is six steps:

```text
  ┌──────────────────────────────────────────────────────────────┐
  │  1. SCRAPE leads      (Google Maps / BBB, or buy a list)       │
  │  2. VALIDATE numbers  (drop landlines → keep mobiles only)      │
  │  3. IMPORT to CRM      (master lead list → CSV → GHL contacts)  │
  │  4. DRIP the HPF       (Hook → Pitch → Follow-up; 5 SMS / 5 min)│
  │  5. CALL on reply      (within 5 min of a positive response)    │
  │  6. BOOK live          (book the appointment while on the call) │
  └──────────────────────────────────────────────────────────────┘
```

> 🔑 **The engine is a drip automation plus a fast human. The software sends texts all day in the background; your only real job is to call the instant someone replies and book them there and then.**

Owen's plug-and-play version imports a GHL "snapshot" that creates a pipeline (Cold SMS lead → Pitched → Booked → No-show) and two automations: a **Queue/Pitch SMS** workflow (sends the hook, waits, sends the pitch on a positive reply, follows up) and an **SMS notification** that pings you the moment a lead replies positively.

> 💡 **Tool alternatives.** Owen builds everything on **GoHighLevel** (CRM + pipeline + SMS + automations bundled). You are not locked in. Alternatives: **HubSpot, Keap, Close, Vendasta**, or a stack you wire together yourself — **Cal.com/Calendly** (booking) + **Zapier or Make** (automation) + **Brevo/Mailchimp** (email) + **Twilio/Telnyx** (SMS) + **Stripe** (payments). GHL bundles it; a stack is cheaper and more flexible but you assemble it. Whatever you use, it must support A2P 10DLC-registered sending and automatic STOP handling.

## Part 3: Fuel for the fire — getting leads and the master lead list

You cannot text anyone until you have numbers. Owen's favourite sources are **Google Maps** and the **Better Business Bureau (BBB)** for niches that live there; otherwise you can **buy a list** (e.g. off Fiverr) or use any other method.

> 💡 **Owen's own warning:** *"Don't spend too much time scraping leads... it's pretty low leverage and there's a lot of methods out there."* Scraping is grunt work — do it fast or delegate it, don't perfect it.

He organises everything into a **master lead list** — one spreadsheet, a tab per US state, with columns for website/BBB link, company name, phone, email, and full name. Two handy formatting tricks he calls out:

- BBB and scrapers often return company names like `Owen Roofing LLC`. The sheet reformats it to just `Owen Roofing`, so when you text "is this Owen Roofing?" it reads human, not robotic.
- Full names like `Owen Jangle Rensland` get split into first/last automatically for a clean CRM import.

> 💡 **A note on "leads are infinite."** Owen argues you can re-text the *same* list months later and people forget they were ever contacted. Be careful here: re-texting people who never responded — or worse, who opted out — is exactly what compliance rules exist to stop. Re-use a list only for numbers that never opted out, and never for anyone who replied STOP.

## Part 4: Validate the numbers (drop the landlines)

You do not want to text landlines — they can't receive SMS, you waste sends, and you look careless. Owen uses **Clear Out Phone** to validate:

1. Take your scraped phone numbers into a Google Sheet. **Label the top row `phone numbers`** — the validator needs to know which column holds them.
2. Run them through Clear Out Phone (cheap, pay-as-you-go credits).
3. It returns each number tagged **mobile / fixed line / toll-free**. Sort A→Z on that column, **delete every fixed line**, keep the mobiles.
4. Copy the clean mobiles back into the right state tab of your master lead list. Duplicates highlight red so you can spot them.

> ✅ **What to do about it:** never send to an unvalidated list. Validation both saves money and quietly improves compliance — it stops you texting numbers that were never going to be legitimate mobile recipients.

> 💡 **Tool alternatives.** Instead of **Clear Out Phone**, you can use **Twilio Lookup** (line-type intelligence via API), **NumVerify** (simple validation API), or **Clearout**. All do the same core job: tell you which numbers are real, textable mobiles.

## Part 5: The HPF script — Hook, Pitch, Follow-up

Owen uses exactly **three** messages, on purpose: *"SMS costs money... if you have like 20 follow-ups and you send 5,000, that will end up spending a lot."* Three messages keeps cost and annoyance down. HPF = **H**ook, **P**itch, **F**ollow-up.

> ⚠️ **All scripts below are illustrative examples to adapt, not gospel — and every one of them must carry your sender identification and respect opt-outs to be compliant.** Wording, pricing, and offers are reconstructions of what Owen describes.

| Message | Job | Illustrative example (adapt + add identification) |
|---|---|---|
| **Hook** | Qualify / engage. A short question that gets a reply. | *"Hi, is this [Owner/Company]? Do you guys do roof replacements? — [Your name]"* |
| **Pitch** | Sent only after a positive reply. Convey the offer simply — a "dumbed-down" version, not your full formal offer. | *"Nice — this is [Your name]. Saw you on Google with some solid reviews. I've got about 5–8 people in [area] who need a roof replacement — open to a quick chat about sending them your way?"* |
| **Follow-up** | For people who replied to the Hook but went quiet on the Pitch. One gentle nudge. | *"Hi [Company] — still open to chatting about this? No worries either way. — [Your name]"* |

> 🔑 **The Hook's only job is to get a reply. The Pitch's only job is to earn a phone call. Keep both short, human, and identified — nobody books off a wall of text.**

Note the sequence logic in the automation: send Hook → wait → if positive reply, send Pitch and mark them **Pitched** in the pipeline → if no reply to the Pitch, send the single Follow-up → if they reply, they become a new lead and you get a notification to call.

## Part 6: Import and drip — 5 every 5 minutes, ~500/day

With a clean CSV of validated, compliant leads:

1. **CRM → Contacts → Import.** Upload the CSV. Map columns (formatted company name → company, phone → phone), and tell it **not** to import unmatched columns. Name the import by count + date (e.g. `34 - 06-18-25`) so you can find it later. The CRM auto-drops duplicate phone numbers on import.
2. **Select all → Add to automation → the Queue/Pitch SMS workflow → Drip mode.**
3. Set it to send **5 SMS every 5 minutes**, starting a few minutes out.

That pace means the system trickles texts out all day in the background. Owen's routine: *"every morning... setting it up at 8 and setting like 500 leads to go, and basically the entire day it'll just send SMS."* Roughly **500 sends a day** is his working volume.

> 💡 **Why the slow drip matters (beyond what Owen says).** Blasting hundreds of identical texts at once is exactly the pattern carriers flag as spam and block. A metered drip is both gentler on deliverability and easier to keep compliant. Your CRM will also **ramp** your sending limit over time (Owen mentions it climbing 100 → 150 → 250 → 350 → 500 as you build sending reputation) — don't try to outrun it.

> 💡 **Testing discipline (Owen's own rule):** *"Don't make script changes after 50 messages are sent."* Because you can send ~500/day, you can genuinely A/B a new script daily. The number he looks for before judging a script is about **300 sends**. Change one thing at a time.

## Part 7: Call within 5 minutes and book live

This is where the money is made, and it is a human job. When a lead replies positively, your notification fires — *"New lead, call within 5 minutes"* — with a link straight to the conversation.

> 🔑 **Speed is the whole game. The value of a positive reply decays by the minute. Call within 5 minutes, every time.**

On the call, two framing reminders from Owen:

- **Reset the frame.** They engaged first, so the frame is already half-set — but re-establish that *they* are evaluating *your* service, not the other way around. *"We don't need them as clients, but they need our services."*
- **Build urgency.** No urgency, no show-up. All the reminder automations in the world won't make someone attend a call they see no value in.

**Book them live, on the call.** Don't tell them "I'll send a link." Because the CRM keys contacts off phone number, you just open `yourdomain.com/strategycall`, fill in their info **using the same number you're calling from** (so it merges to the right contact and auto-marks them Interested), and book them then and there. Since they never see your booking/confirmation page themselves, walk them through those steps while you're still on the phone. Show-up automations (confirmation text, a reminder call ~2 hours before) then do the rest.

---

## Key takeaways

1. **Compliance is the first feature, not the fine print.** A2P registration, sender ID, honored opt-outs, DNC scrubbing, and a jurisdiction check come *before* the first text. In the UK/EU/Canada, assume you can't cold-SMS at all.
2. **The flow is six steps:** scrape → validate → import → drip HPF → call on reply → book live.
3. **Validate to drop landlines.** Text mobiles only; it saves money and reduces junk.
4. **HPF = three messages, no more.** Hook engages, Pitch (post-reply) conveys a simple offer, Follow-up nudges the quiet ones.
5. **Drip ~5 every 5 minutes, ~500/day.** Slow and metered beats a spammy blast for both deliverability and compliance.
6. **Call within 5 minutes and book on the call.** Speed and live booking are what turn replies into appointments.

## Common pitfalls

- ❌ **Sending before A2P registration / a jurisdiction check.** This is the expensive one — carrier blocks at best, TCPA exposure ($500–$1,500/message) at worst. Do the compliance checklist first, always.
- ❌ **No sender identification or no working STOP.** An anonymous, un-opt-out-able text is both spam and a violation. Put your name in the message; confirm STOP is honored.
- ❌ **Re-texting opt-outs or a stale list.** "Leads are infinite" does not mean "opt-outs are re-contactable." Never re-text anyone who replied STOP or never engaged.
- ❌ **Texting unvalidated numbers.** Landlines waste sends and make you look careless. Validate every list.
- ❌ **Sitting on a positive reply.** A reply left for an hour is a dead lead. Call within 5 minutes.
- ❌ **Rewriting the script after 20 messages.** Judge a script at ~300 sends, not 20. Change one variable at a time.

---

## 🛠️ Capstone Project: Your compliant cold-SMS surge system

> This is the main hands-on project for the lesson. You will build the entire cold-SMS machine AND the compliance layer that makes it legal to run — then prove it works with a single test send to your own phone. Keep it small: one niche, a handful of leads, one clean end-to-end run.

### What you will build

A working cold-SMS system for your agency plus a written compliance checklist for your jurisdiction. The pieces, each mapped to a lesson idea:

- A **jurisdiction compliance checklist** (Part 1) — the gate everything else passes through.
- A **master lead list** with a small batch of scraped leads (Part 3).
- A **validated** subset with landlines removed (Part 4).
- An **HPF script** with sender identification baked in (Part 5).
- A **drip automation** in your CRM (Part 6).
- A **call-and-book flow** wired to a reply notification (Part 7).

### Why this is the perfect practice

| Lesson idea | Where you use it in the Capstone |
|---|---|
| Compliance first | Writing your jurisdiction checklist and confirming A2P + STOP before anything sends |
| Scrape + master list | Collecting a small lead batch into the state-organised sheet |
| Number validation | Running the batch through a validator and dropping landlines |
| HPF script | Writing Hook, Pitch, Follow-up with your name in them |
| Drip cadence | Setting 5-every-5-minutes in the automation |
| Call + book live | Triggering the notification and rehearsing the live booking |

### Milestones (build them in order, each one works on its own)

1. **Write your compliance checklist.** In writing, for your country/state: Is cold SMS to businesses legal here? Is A2P 10DLC registered (US)? Where's my sender identification? Is STOP auto-honored? What's my DNC-scrub step? If you can't answer all of these "yes/handled," **stop and switch to cold calling** — that's a valid, complete outcome for this milestone.
2. **Build the master lead list.** Copy the state-tab spreadsheet, scrape (or buy) 10–20 leads in one niche, paste them in cleanly.
3. **Validate the numbers.** Run the phones through Clear Out Phone (or Twilio Lookup / NumVerify), sort, delete fixed lines, keep mobiles.
4. **Write your HPF.** One Hook, one Pitch, one Follow-up — each carrying your name/business. Mark them as your v1 to test later.
5. **Wire the drip.** Import the validated CSV to your CRM, add to the Queue/Pitch automation in drip mode, set 5 every 5 minutes.
6. **Prove it end to end — the done-criteria test.** Add **your own number** to the list, send one compliant test, confirm you receive the Hook, reply positively, and confirm the reply fires your "call within 5 minutes" notification and you can open the booking flow.
7. **Stretch goals.** Add a Slack channel for reply notifications; draft the 2-hours-before reminder call script; write an SOP so you never re-read this lesson; A/B a second Hook after 300 real sends.

### How you will know you are done

- ✅ You have a written, jurisdiction-specific compliance checklist and every box is either ticked or you've consciously chosen cold calling instead.
- ✅ A **compliant test send to your own number arrives**, correctly identifies you, and would honor STOP.
- ✅ Replying to that test **triggers the call/booking flow** (notification fires; you can open the booking calendar).
- ✅ Your HPF messages each contain sender identification.

> 💡 **Keep yourself honest:** the test send must go to *your own* phone. Do not send to real strangers until your compliance checklist is fully green — that is the entire point of building the checklist first.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice on one idea. Optional and independent; the Capstone already touches all of them, so feel free to skip straight to it.

### Exercise 1: Jurisdiction one-pager (foundational)
Write a half-page answering: In my location, can I legally send cold marketing SMS to businesses? Cite the governing law (TCPA / PECR+GDPR / CASL / other). End with a one-line verdict: "Cold SMS OK with these steps" or "Use cold calling instead."

### Exercise 2: Three HPF variants (intermediate)
Write three different Hooks for one niche, each under 160 characters and each identifying you. Predict which gets the highest reply rate and why. (You'll validate with real data at ~300 sends.)

### Exercise 3: Deliverability + compliance audit (advanced)
Take your drip setup and list every point where a compliance or deliverability failure could occur (unregistered sender, no STOP handling, unvalidated numbers, too-fast send rate, re-texting opt-outs). For each, write the one control that prevents it.

---

## Cheat sheet

```text
COLD SMS SURGE — one-page recap

RULE ZERO: Do it compliantly or don't do it.
  Pre-send checklist (US):
    [ ] A2P 10DLC campaign registered (Module 4)
    [ ] Sender identification in every message (your name/business)
    [ ] STOP / opt-out honored instantly + forever
    [ ] List scrubbed against do-not-contact / prior opt-outs
    [ ] Jurisdiction checked BEFORE sending
  UK/EU (PECR+GDPR) & Canada (CASL): usually NOT allowed to consumers → cold call instead.
  US risk if you skip it: TCPA $500–$1,500 PER message.

THE FLOW (6 steps):
  scrape → validate → import → drip HPF → call on reply → book live

LEADS: Google Maps / BBB / buy a list. Organise in master lead list (tab per state).
VALIDATE: Clear Out Phone (or Twilio Lookup / NumVerify) → drop FIXED LINES, keep MOBILES.

HPF SCRIPT (3 msgs only — SMS costs money):
  HOOK      = short question, qualify/engage  ("is this [Company]? do you do X?")
  PITCH     = post-reply, simple offer         (only after a positive reply)
  FOLLOW-UP = one nudge for the quiet ones
  → every message carries YOUR NAME. Illustrative only — adapt.

DRIP: import CSV → automation → 5 SMS every 5 min → ~500/day.
  Sending limit ramps: 100→150→250→350→500. Don't outrun it.
  Test a script at ~300 sends, not 20. Change one thing at a time.

ON A POSITIVE REPLY:
  CALL WITHIN 5 MINUTES. Reset frame (they need you). Build urgency.
  BOOK LIVE on the call — same phone number so CRM merges the contact.
  Walk them through the booking steps; show-up automations handle reminders.

TOOL ALTERNATIVES:
  GoHighLevel → HubSpot / Keap / Close, or Cal.com+Zapier+Brevo+Twilio+Stripe
  Clear Out Phone → Twilio Lookup / NumVerify / Clearout
  Send Blue (blue-bubble) → standard SMS via Twilio (iMessage-for-business = grey area)
```

## How this connects to the rest of the course

- **Earlier, Module 4 · Infrastructure:** you set up your CRM sub-account and registered A2P 10DLC — the exact prerequisite that makes compliant cold SMS possible here.
- **Earlier, Lesson 20:** established why outreach volume, not cleverness, drives your first clients — cold SMS is how you generate that volume with no budget.
- **Next, Lesson 22 · Cold Calling Catalyst:** the other outreach channel — and your fallback if your jurisdiction rules out cold SMS. Many of the framing and urgency skills carry straight over.
- **Later, Module 7 · Sales: setting:** the appointments you book here feed directly into the setting and closing process — cold SMS fills the calendar; sales converts it.

---

*Source: "Cold SMS Surge" by Owen Rensland, AI Agency Full Course. Scripts, prices, KPI numbers, and configuration steps are illustrative reconstructions of the patterns described in the talk. Adapt them to your current tools — and to the law in your jurisdiction, which is your responsibility to verify.*
