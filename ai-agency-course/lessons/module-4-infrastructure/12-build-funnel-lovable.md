# Module 4 · Lesson 12: Build your funnel with Lovable

> **Course:** The AI Agency Blueprint, a self-paced course
> **Module 4:** Infrastructure: the systems that turn ad clicks into booked appointments
> **Speaker:** Owen Rensland, founder of a local-business ad agency
> **Source talk:** [AI Agency Full Course (Owen Rensland)](https://www.youtube.com) · [full transcript](../../transcripts/ai-agency-full-course.txt)
> **Estimated time:** 50 to 65 minutes (read plus exercises)

---

## In one sentence

A funnel is the mobile-first page your ad clicks land on, and this lesson shows you how to build one — headline, proof, survey, booking calendar — in Lovable, wired to your CRM so a submission becomes a real lead and a booking lands on a calendar.

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone
> Project** where you build one working funnel for your niche and prove it end to
> end: a survey submission creates a lead in your CRM, and a booking shows up on
> the calendar. Everything before the Capstone teaches the ideas you will use
> there — funnel vs. lead form, friction theory, ad congruency, and the webhook
> wiring. If you want to see the finish line first, jump to the **"Capstone
> Project"** section, then come back.

## First-principles companion

> 💡 **The durable idea behind this lesson.** The tools (Lovable, GoHighLevel)
> will change; the psychology of a conversion page will not. For the timeless
> version:
>
> - **[$100M Leads](https://www.acquisition.com/books) by Alex Hormozi** (book).
>   The source of "more / better / new" and of value = dream outcome × likelihood
>   ÷ time × effort. A funnel is just that equation rendered as a web page.
> - **Eugene Schwartz, *Breakthrough Advertising*** (book). The "market awareness"
>   ladder — meeting a visitor where their thinking already is — is why ad-to-page
>   congruency matters at all.

## A few plain-language basics first

This lesson uses some everyday terms. Here they are in plain words:

- **Funnel:** a single web page (or short sequence) whose only job is to turn an
  ad click into a booked appointment. No menu, no blog, no distractions.
- **Lead form:** Meta's built-in mini-form that opens *inside* Facebook or
  Instagram when someone taps your ad. Lowest effort to fill out; you never leave
  the app.
- **Friction:** anything that makes a visitor do more work — extra questions,
  extra clicks, a slow page. More friction means fewer but higher-quality leads.
- **Congruency (or alignment):** the page looks and reads like the ad that sent
  the visitor there — same promise, same visuals — so they don't bounce.
- **VSL (Video Sales Letter):** a short video on the page that explains the offer
  and builds trust.
- **Survey / qualification:** a few questions that filter out people who aren't a
  real fit before they reach the calendar.
- **Booking calendar:** the embedded scheduler where a qualified visitor picks a
  time. Here it comes from your CRM (GoHighLevel).
- **CRM:** "Customer Relationship Manager" — the software that stores contacts,
  runs your calendar, and fires automations. This course uses GoHighLevel (GHL).
- **Webhook:** a one-way message from one app to another. When someone submits
  your funnel, Lovable *pings* GHL with the data, and GHL creates a lead.
- **Custom field:** a slot you create in your CRM to store an answer that isn't
  standard (e.g. "deck age"), so the survey answers arrive labelled, not lost.

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

You can have the best ad in your city, but "it won't matter how good your ads are
[if] they will never convert into anything" — Owen. The funnel is where the money
is made or lost. A clunky page throws away clicks you paid for; a clean, congruent,
fast one turns them into appointments your client will pay you for month after
month. And because AI builders like Lovable exist, you can now build a
high-converting funnel in an afternoon instead of hiring a developer.

## Learning objectives

By the end of this lesson you will be able to:

1. Explain when to use a funnel versus Meta's native lead form, and why.
2. Apply friction theory: start minimal to confirm it converts, then add friction to raise lead quality.
3. Name the five funnel components and the six common funnel mistakes.
4. Build a mobile-first ("iPhone first") funnel in Lovable with a conditional survey and embedded booking calendar.
5. Wire a funnel submission to your CRM via an inbound webhook with mapped custom fields, and test it end to end.

## Prerequisites

- **Lesson 11** (your infrastructure / CRM sub-account set up in GoHighLevel).
- A Lovable account (or an alternative builder — see the callout in Part 4).
- A niche and a rough offer chosen in Module 2 — you'll write it into the headline.

---

## Part 1: Funnel vs. lead form — pick your destination

Every ad has four parts: an **offer**, a **creative** (the image/video), the
**copy**, and a **destination** — "where you send the traffic to convert them
from cold to leads, appointments, clients." This lesson is about the destination.

You have two real choices, and Owen is blunt about the trade-off:

| | **Lead form** (Meta native) | **Funnel** (a landing page) |
|---|---|---|
| Where it lives | Inside Facebook/Instagram | Your own web page |
| Friction | Lowest possible | You control it |
| Lead quality | Low — "everybody just seems to fill them out without much thought" | Higher — visitors chose to leave the app |
| Tracking / pixel data | Thin, less accurate | Rich, accurate |
| Flexibility | Fixed | Full — headline, proof, friction, all testable |
| Best when | You have little budget | Almost always |

> 🔑 **Owen's verdict: "I wouldn't recommend using [lead forms]… I would
> recommend using landing pages."** Lead forms are the lowest-friction, lowest-
> quality option; funnels give you flexibility, better data, and better leads.

Lead forms aren't useless — Owen says he "spent around $20,000 on this single lead
form" successfully, using two qualifying questions with conditional logic to add
"a little bit of friction." Use them when budget is tight. Otherwise, build a
funnel. The rest of this lesson builds a funnel.

## Part 2: Friction theory — the drop of water

Here is the single most useful mental model in the lesson. Picture your traffic
as water dripping through a pipe. Every qualifying question you add is another
bend in the pipe. Owen: "as you add more questions and more friction… people who
aren't as interested, they won't even bother with it. So we'll just naturally get
a higher quality lead, but we'll get less leads."

That gives you a dial you can turn on purpose:

```text
  LOW friction                              HIGH friction
  ├────────────────────────────────────────────────────┤
  many leads                                few leads
  lower quality                             higher quality
  (start here)                              (move here only if needed)
```

The order matters, and beginners get it backwards. Owen's rule:

> ✅ **What to do about it:** *"Start with minimal friction, make sure the
> process is actually working and getting conversions. Then only if you have too
> many leads and appointments coming through and your quality isn't good enough,
> then you would add friction."* Prove it converts first. Raise quality second.

There's one honest exception: for a **bigger client with a large addressable
market** who is paying you well and only wants qualified leads, Owen sometimes
launches with heavier friction on purpose — "I usually wouldn't start a campaign
with this much friction… the only reason I'm okay with this is because this is a
bigger company and I know they need qualified leads." That's a deliberate choice
tied to market size, not the default. When in doubt, start light.

## Part 3: The five funnel components and the six mistakes

A funnel, Owen says, "typically consists of a couple of things." Here they are,
each tied to a job:

| Component | What it is | Job |
|---|---|---|
| **Call-out** | Who it's for ("Home improvement contractors") | Grab the right person |
| **Headline** | The offer, mirroring the winning ad | Confirm they're in the right place |
| **VSL / proof** | Short video, reviews, past jobs, ratings | Build belief |
| **Survey / qualification** | A few conditional questions | Filter and capture the lead |
| **Booking calendar** | Embedded scheduler | Turn a lead into an appointment |

Below the survey sits a **booking calendar**, and after booking, a **thank-you /
pre-call page** with proof and instructions.

Now the traps. Owen's six common funnel mistakes:

- ❌ **No congruency.** The funnel headline and visuals don't mirror the ad, so
  people "click on the ad and go to the page and just click off because they
  don't think it's the same thing."
- ❌ **Slow load time.** A page that lags loses people before it renders.
- ❌ **Not mobile-first.** "This looks great on computer but has a look on the
  phone." Almost all your traffic is on a phone.
- ❌ **Too many / unnecessary questions.** Every needless question is friction you
  didn't choose.
- ❌ **Inconsistent visuals** — jargon, clutter, off-brand design that erodes trust.
- ❌ **Off-ramps.** Tabs to "my product," "about us," "proof" — "all this BS that
  takes people out of the closed funnel." A funnel has no exits but the calendar.

> 🔑 **A funnel is a closed hallway with one door at the end: the booking
> calendar.** Every mistake above is a hole punched in the wall.

## Part 4: Build it in Lovable — iPhone first

**Lovable** is an AI website builder: you describe the page in plain English (or
paste a screenshot), and it generates it. Owen's whole approach is to point it at
a proven page and say "recreate this."

> 💡 **Alternatives to Lovable.** You are not locked in. Other AI/site builders
> that build the same funnel: **Framer, Webflow, Carrd, v0 by Vercel,
> Bolt.new**, or dedicated landing-page tools **Unbounce, Instapage, Leadpages**.
> The components and the webhook wiring are identical everywhere — only the editor
> changes. Pick one and stick with it for the Capstone.

Here is the build order Owen follows for a real client (a decking company),
rewritten as steps you can copy. The prompt text below is **illustrative** — adapt
the wording, offer, and questions to your niche.

**1. Set the frame: mobile-first.** From the first message, tell it the priority.
Owen: *"it's going to be iPhone first"* and later, *"notice how I'm building all
this on a mobile. Mobile first."* Preview on a phone-width screen the whole time.

*Example opening prompt:* "Build a mobile-first landing page for a decking
company. Headline mirrors this offer: 'Brand-new deck starting at $9.5K.' Keep it
simple, high-converting, minimal friction."

**2. Borrow only the brand, not the layout.** He gives Lovable the client's current
site for colour only: *"Don't take any inspiration other than some slight colour
inspiration just so it looks on brand."* Upload the logo too.

**3. Add social proof — but keep it clean.** *"Display the social proof as a
carousel that cycles"* (e.g. "Class A contractor," BBB-accredited, manufacturer-
certified). Embed the Google rating and reviews. Owen makes the Google rating
redirect to the real reviews page and keeps proof high on the page: "I do want
reviews to be higher up… that's probably the best thing."

**4. Cut the clutter — reduce friction.** The first draft is always too busy.
Owen's reaction: "this is way, way, way too much going on… you don't know where to
call, you don't know where to click. So we'll reduce all the friction. Remove
everything that doesn't need to be there." Kill the "takes 60 seconds" badges,
duplicate CTAs, and any stray call buttons.

**5. Build the conditional survey.** Ask only what qualifies the lead, and branch.
For the deck company: *Do you already have a deck? → How big is it? (branch:
under 180 sq ft is disqualified) → How old is it? → What size do you want? →
Timeline? → Name, email, phone, address.* Conditional logic means later questions
depend on earlier answers, so nobody answers irrelevant ones.

> 💡 **Capture contact info in the survey, then forward to the calendar.** Owen:
> *"add a question in the form with the contact information — name, email, phone,
> address — and then forward that to the booking calendar at the end, so there's
> minimal friction."* The visitor types their details once; the calendar
> autofills. (In his test, email and address autofilled but full name didn't — so
> test yours and fix what doesn't carry over.)

**6. Embed the booking calendar from your CRM.** In GoHighLevel, open the calendar,
choose **share → embed code**, and paste that into Lovable at the end of the
survey. Now the survey ends on a real, connected scheduler — book a time and it
lands on the client's calendar.

**7. Add a thank-you page.** Make it `/thank-you`, congruent with the funnel (not
a generic template). Owen: "make it look like it belongs in the funnel. Add social
proof, everything they need to get confidence in the company." Embed the Google
Business profile and a few real job photos here.

## Part 5: Wire the funnel to your CRM with an inbound webhook

The page is built. Now a submission needs to *become a lead* in GoHighLevel. That
link is an **inbound webhook** — a message Lovable sends to GHL the instant someone
submits. All the field mapping below is an **illustrative example**; your fields
will match your own survey.

Owen's actual method is almost embarrassingly simple. In Lovable:

> *"All I did is say: make it so a survey submission is a new lead inside of GHL
> with an inbound webhook."* — Owen

Then the flow:

```text
  Visitor submits funnel (Lovable)
        │  inbound webhook (a URL)
        ▼
  GoHighLevel automation: "New Lead"
        │  create contact + map fields
        ▼
  Contact created · client notified · booking on calendar
```

**Step by step:**

1. **In GHL, open (or create) the "New Lead" automation** and add an **Inbound
   Webhook** trigger. GHL gives you a **webhook URL**.
2. **Paste that URL into Lovable.** Owen: "it's going to ask for the URL, which we
   just got here. So you copy that… drop the URL."
3. **Send a test submission** so a real payload arrives. In GHL, "check new
   requests" to see the incoming data. If it doesn't appear, ask Lovable for a
   **payload reference** (a screenshot / list of the field names it's sending) and
   attach it as a mapping reference.
4. **Create the contact and map the standard fields:** first name, last name,
   email, phone, address.
5. **Create custom fields for the survey answers.** In GHL: *Settings → Custom
   Fields → create single-line contact field.* For the deck example Owen creates:
   `project type`, `has existing deck`, `current deck size`, `deck age`,
   `desired deck size`, `timeline`.
6. **Map each survey answer to its custom field** back in the automation.
7. **(Optional) Update the internal notification** so the email your client gets
   about a new lead includes those custom fields — project type, timeline, size,
   etc.

> 🔑 **The webhook is the whole game.** Without it, a "submission" is just text on
> a page that vanishes. With it, every submission is a labelled contact your CRM
> can nurture, notify, and book.

> 💡 **Alternatives to GoHighLevel.** GHL bundles CRM + funnels + calendar + SMS +
> automation in one. If you'd rather assemble a cheaper, more flexible stack:
> **Cal.com or Calendly** (booking) + **Zapier or Make** (catch the webhook,
> create the contact) + **Brevo or Mailchimp** (email) + a form tool + **Stripe**.
> All-in-one substitutes: **HubSpot, Keap, Close, Vendasta.** The idea is the same
> everywhere — a submission fires a webhook that creates a contact and books a
> time. You just wire it yourself.

## Part 6: Test it end to end (and mind the details)

Owen tests every stage live, and so should you. Fill the funnel out yourself:

- Does the survey **branch** correctly and **autofill** the calendar? (He caught
  that "full name" didn't autofill and fixed it.)
- Does a submission **create a contact** in GHL with all custom fields populated?
- Does a booking **land on the calendar** and fire the client notification?

When his first test showed empty custom fields, he diagnosed it out loud: "It's
looking like none of this actually showed up… I'm assuming that means the webhook
didn't fire properly." That's the exact failure you're testing for. If contact
data lands but the notification email looks bad, that's a separate email-
deliverability fix (set up a dedicated sending domain in GHL) — don't confuse the
two.

> ⚠️ **Reality check on proof and reviews.** It's fine to showcase a client's
> *real* Google rating and *their own* completed-job photos — Owen does. It is
> **not** fine to borrow another company's testimonials, invent reviews, or imply
> results that didn't happen. In the US the FTC requires endorsements to be
> truthful and substantiated. Use only proof that belongs to the business you're
> building the funnel for.

> 💡 **One congruency detail Owen fixes at launch:** his page said "free instant
> decking quote" while the ad said "best deck prices." He rewrote the headline to
> match the ad — "we just want it to be aligned, that's the biggest thing." Do the
> ad and the page a favour and make the promise word-for-word the same.

---

## Key takeaways

1. **Funnel beats lead form for almost everyone.** More flexibility, better data,
   higher-quality leads. Lead forms are the budget option.
2. **Friction is a dial, not an accident.** Start minimal to prove it converts,
   then add questions only to raise quality once volume is there.
3. **Congruency is survival.** The page must mirror the ad's promise and look, or
   paid clicks bounce.
4. **Mobile-first, always.** Build and preview on a phone from message one.
5. **The webhook makes it real.** A submission only matters if it becomes a mapped
   contact in your CRM and a booking on the calendar.

## Common pitfalls

- ❌ **Building on desktop and checking mobile last.** Reverse it — iPhone first.
- ❌ **Starting with a heavy survey to "get quality."** You'll get near-zero data
  and won't know if the page even works. Start light, add friction later.
- ❌ **Leaving off-ramps in the funnel** (nav menus, "about" tabs). Every exit is a
  lost lead. One door only: the calendar.
- ❌ **Trusting the webhook without testing.** Submit a real test lead and confirm
  the contact and every custom field arrive. Empty fields = webhook or mapping bug.
- ❌ **Headline that doesn't match the ad.** Different wording quietly tanks
  conversion. Copy the winning ad's promise onto the page.

---

## 🛠️ Capstone Project: one working funnel for your niche

> This is the main hands-on project for the lesson. You'll feel the moment it
> "clicks" when your own test submission pops up as a real lead in your CRM and a
> booking appears on the calendar. Keep it small: one page, one niche.

### What you will build

A single mobile-first funnel in Lovable (or an alternative) for the niche you
chose in Module 2, wired to your GoHighLevel sub-account so that a survey
submission creates a lead and a booking lands on the calendar. Its pieces, each
mapped to a lesson idea:

- **Call-out + headline** mirroring your offer (congruency, Part 3).
- **Social proof** — reviews or a rating, kept clean (Part 4).
- **A short conditional survey** capturing name/email/phone (friction theory, Part 2).
- **An embedded GHL booking calendar** (Part 4).
- **An inbound webhook → New Lead automation** with mapped custom fields (Part 5).

### Why this is the perfect practice

| Lesson idea | Where you use it in the funnel |
|---|---|
| Funnel vs. lead form | Choosing to build a page, not a native form |
| Friction theory | Keeping the survey short to start |
| The five components | Call-out, headline, proof, survey, calendar |
| The six mistakes | Your QA checklist before launch |
| Mobile-first | Building and previewing on phone width |
| Webhook + custom fields | Making the submission a real CRM lead |

### Milestones (build them in order, each one works on its own)

1. **Pick a proven reference.** Find a competitor funnel in the Facebook Ads
   Library that's been running a while, and screenshot it (or write a clear brief).
2. **Generate the page in Lovable, iPhone-first.** Feed it the screenshot/brief,
   your offer as the headline, and your brand colours + logo. Preview on phone.
3. **Cut the clutter.** Remove every off-ramp, duplicate CTA, and needless badge
   until there is one obvious next action.
4. **Add a short conditional survey** (3–5 questions max) that captures name,
   email, phone, and forwards to the calendar.
5. **Embed your GHL booking calendar** via its embed code at the end of the survey.
6. **Wire the webhook.** Tell Lovable to send submissions to GHL via inbound
   webhook; create the New Lead trigger; create and map your custom fields.
7. **Test end to end** with a fake submission and a fake booking; confirm the
   contact, the fields, and the calendar entry all appear.
8. **Stretch goals.** Add a congruent `/thank-you` page with proof; connect a
   custom domain; add the Meta pixel (`ask it: "add pixel to this"`).

### How you will know you are done

- ✅ The funnel loads fast and looks right on an actual phone.
- ✅ The headline's promise matches the ad/offer word-for-word.
- ✅ Submitting the survey creates a **new contact in GoHighLevel** with every
  custom field populated (not blank).
- ✅ Picking a time creates a **booking on the calendar** and fires the client
  notification.
- ✅ There is no way to leave the funnel except by booking.

> 💡 **Keep yourself honest:** you are not done when the page *looks* built — you
> are done when your own test lead and test booking have actually landed in the
> CRM. If a custom field is empty, the job isn't finished.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice on
> one idea. Optional and independent; the Capstone already touches all of them.

### Exercise 1: Friction dial (foundational)
Write two versions of your survey: a **3-question** minimal version and a
**6-question** high-friction version. Note which you'd launch with, and the one
condition (big client, large market) under which you'd start with the heavier one.

### Exercise 2: Congruency audit (intermediate)
Take any funnel in the Facebook Ads Library. List every way its landing page does
or doesn't match the ad that leads to it (headline, colours, image, promise).
Score it against the six common mistakes.

### Exercise 3: Webhook without the CRM bundle (advanced)
Rebuild the wiring using a stack instead of GHL: point the Lovable webhook at a
**Make or Zapier** scenario that creates a contact in a spreadsheet or **HubSpot**
and books via **Cal.com**. Prove one test submission flows all the way through.

---

## Cheat sheet

```text
FUNNEL vs LEAD FORM
  Lead form  = Meta-native, lowest friction, lowest quality, thin data → budget only
  Funnel     = your page, flexible, better data + leads → use this (Owen's pick)

FRICTION THEORY (the drop of water)
  More questions → fewer, higher-quality leads
  RULE: start minimal (prove it converts) → add friction later (raise quality)
  Exception: big client + large market may start heavier, on purpose

FUNNEL COMPONENTS
  1 Call-out  2 Headline (mirror the ad)  3 VSL/proof
  4 Survey/qualification (conditional)    5 Booking calendar
  + congruent /thank-you page

SIX MISTAKES
  no congruency · slow load · not mobile-first ·
  too many questions · inconsistent visuals · off-ramps

BUILD IN LOVABLE (iPhone first)
  screenshot a winner → "recreate this" → borrow brand colour only →
  cut clutter → conditional survey (capture name/email/phone) →
  embed GHL calendar → /thank-you page

WIRE TO CRM
  Lovable: "make a survey submission a new lead in GHL via inbound webhook"
  GHL: New Lead automation → inbound webhook trigger → copy URL into Lovable
  test submission → check payload → map: first/last name, email, phone, address
  Custom fields (Settings → Custom Fields) for each survey answer → map them
  TEST: contact created + fields filled + booking on calendar = done

ALTERNATIVES
  Builder: Framer · Webflow · Carrd · v0 · Bolt.new · Unbounce/Instapage/Leadpages
  CRM:     HubSpot · Keap · Close  OR  Cal.com+Zapier/Make+Brevo+Stripe
```

## How this connects to the rest of the course

- **Earlier, Module 4 · Lesson 11:** set up your GoHighLevel sub-account, calendar,
  and automations — the CRM this funnel plugs into.
- **Next, Module 4 · Lesson 13 "Your VSL & Facebook page warm-up":** you'll create
  the proof video that lives on this funnel and warm the ad account that will drive
  traffic to it.
- **Later, Module 5 (Meta Ads Mastery):** you'll build the ad campaign that points
  at this funnel — and congruency between ad and page becomes the thing you tune.

---

*Source: "AI Agency Full Course" by Owen Rensland. Prompt text, field mappings,
prices, and configuration are illustrative reconstructions of the patterns
described in the talk. Adapt them to your niche and the current versions of the
tools.*
