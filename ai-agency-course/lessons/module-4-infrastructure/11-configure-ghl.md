# Module 4 · Lesson 11: Configure your GHL command center

> **Course:** The AI Agency Blueprint, a self-paced course
> **Module 4:** Infrastructure: the systems that catch, book, and follow up with every lead
> **Speaker:** Owen Rensland (AI Agency / SMMA Full Course)
> **Source talk:** [AI Agency Full Course (Owen Rensland)](https://www.youtube.com) · [full transcript](../../transcripts/ai-agency-full-course.txt)
> **Estimated time:** 55 to 70 minutes (read plus exercises)

---

## In one sentence

You will turn a raw GoHighLevel sub-account into a working command center — branded as your own, wired to a booking calendar, a compliant phone and SMS line, a deliverable email domain, e-signable contracts, and the handful of automations that make sure no lead ever goes cold.

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone
> Project** where you fully configure one client-ready sub-account: white-label
> done, calendar live, a verified phone number forwarding to your phone,
> deliverability set, one agreement uploaded, and reminders switched on.
> Everything before the Capstone teaches one piece of that setup. If you want to
> see the finish line first, jump to the **"Capstone Project"** section, then
> come back.

## First-principles companion

> 💡 **The durable idea behind this lesson.** Tools rename their menus every
> quarter, but the plumbing under a small business does not change: capture,
> book, remind, sign, follow up. For the timeless version of that plumbing:
>
> - **["The CRM Handbook" style fundamentals — see HubSpot's free CRM basics](https://www.hubspot.com/products/crm)** and the messaging-compliance
>   primer at **[The CTIA Messaging Principles & Best Practices](https://www.ctia.org/the-wireless-industry/industry-commitments/messaging-interoperability-sms-mms)**. GHL is one packaging of these ideas; the
>   ideas outlive the packaging.

## A few plain-language basics first

This lesson uses some everyday terms. Here they are in plain words:

- **CRM (Customer Relationship Management):** the software that stores every
  lead and customer and the history of every message, call, and appointment
  with them. GoHighLevel is a CRM that also does calendars, texts, and websites.
- **Sub-account:** one isolated workspace inside GoHighLevel, usually one per
  client (or one for your own agency). It has its own contacts, calendar, and
  phone number.
- **White-label:** hiding the vendor's branding so the software looks like it
  is yours. Your clients log in to *your* domain, not "gohighlevel.com".
- **Custom value:** a saved snippet of text (like your booking link or phone
  number) that you type once and reuse everywhere with a merge tag. Change it in
  one place, it updates everywhere.
- **A2P 10DLC:** "Application-to-Person, 10-Digit Long Code." The US carrier
  registration system that lets a business send texts from a normal local
  number. You must register before you can send SMS reliably.
- **DNS record:** a setting at your domain provider that tells the internet
  where your website and email live, and proves you own the domain.
- **VSL (Video Sales Letter):** a short video on your landing page that explains
  who you are and warms a cold visitor up before they book.

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

In Lesson 10 you created the sub-account. An empty sub-account books nobody. This
lesson is where it becomes a machine: a lead fills a form, lands on your calendar,
gets a text reminder from your own number, and shows up — with zero manual work
from you. Every hour you spend here is repaid by every lead you *don't* lose to a
forgotten follow-up. It is also where you meet your first hard legal
requirement: you cannot legally text strangers until your messaging campaign is
registered and your opt-outs work. Get this right once and you clone it for
every client after.

## Learning objectives

By the end of this lesson you will be able to:

1. White-label a GHL sub-account so clients log in under your own brand.
2. Create and reuse custom values (phone, booking page, privacy/terms, VSL,
   first name) across the account.
3. Build a strategy-call calendar with correct staff, meeting link, availability,
   intervals, duration, and scheduling window.
4. Stand up a compliant phone/SMS line: choose a provider, register A2P 10DLC,
   buy a local number, and forward calls.
5. Set up a dedicated email sending subdomain with the right DNS records.
6. Upload and field an e-signable agreement, replacing DocuSign.
7. Turn on the core automations: reminders, surveys, new-lead alerts, and a
   trust email.

## Prerequisites

- **Lesson 10** (you have a GHL account and a sub-account created).
- A domain you own (from Module 0), and access to its DNS settings.
- A phone you can forward calls to.

---

## Part 1: White-label the login

The first thing a client sees is the login screen. If it says "GoHighLevel," you
look like a reseller of someone else's tool. White-labeling swaps that for your
own domain and logo, so the whole platform reads as *your* software.

In GHL this lives under **Agency Settings → Company / Rebranding**. You point a
subdomain you own — for example `app.youragency.com` — at GHL by adding a CNAME
DNS record, then upload your logo and set your brand colors. Clients now log in
at your URL and never see the vendor.

> 🔑 **White-label is not vanity — it is trust. A branded portal makes a solo
> operator look like an established company, which is exactly the credibility a
> local business owner is buying.**

> 💡 **Alternatives to GoHighLevel.** GHL bundles CRM, funnels, calendar,
> automations, and SMS in one paid product. If you would rather assemble your own
> stack (usually cheaper and more flexible, but you wire it together yourself):
> **HubSpot, Keap, Close, or Vendasta** for the all-in-one route, or a stack of
> **Cal.com / Calendly** (booking) + **Zapier or Make** (automation) +
> **Brevo / Mailchimp** (email) + a form tool + **Stripe** (payments). This
> lesson teaches GHL because that is what the course uses; the concepts port
> directly.

## Part 2: Custom values — write once, reuse everywhere

A **custom value** is a saved snippet you reference by a merge tag instead of
retyping. Set them under **Settings → Custom Values**. The ones worth creating on
day one:

| Custom value | What it holds | Where it gets used |
|---|---|---|
| Phone number | Your business number | Emails, SMS, footers |
| Booking page | Your calendar link | Every "book a call" button |
| Privacy policy URL | Link to your privacy page | Email/SMS compliance footers |
| Terms URL | Link to your terms | Same |
| VSL link | Your video sales letter URL | Nurture emails, funnels |
| First name | The contact's first name | Personalizing every message |

The payoff: when your number or booking link changes, you edit one custom value
and every email, text, and automation updates automatically. No hunting through
templates.

> ✅ **What to do about it:** create the six custom values above *before* you
> build any automation. Then reference them by tag everywhere, never paste the
> raw value. Future-you will thank present-you.

## Part 3: The strategy-call calendar

This is the calendar prospects book to talk to you. Configure it under
**Calendars → Create Calendar**. The settings that actually matter:

- **Staff / team member:** assign yourself (or the closer) so the invite comes
  from a real person and syncs to their Google calendar.
- **Meeting location:** connect **Google Meet or Zoom** so a video link is
  auto-generated on every booking.
- **Availability:** set the days and hours you will actually take calls. Owen's
  point from the ads module applies here — *the more flexible your availability,
  the lower your cost per booking*, because prospects find a slot before they
  cool off.
- **Slot interval: 15 minutes.** Offering 10:15, 10:30, 10:45 gives people far
  more options than hourly slots and lifts your booking rate.
- **Duration: 30 to 45 minutes.** Long enough to run a real strategy call, short
  enough to fit several a day.
- **Scheduling window and minimum notice:** how far ahead people can book (e.g.
  the next 2 to 3 weeks) and the minimum lead time before a slot (e.g. at least
  1 hour out, so nobody books a call for "5 minutes from now" when you are not
  ready).

> 🔑 **A high booking rate is mostly a calendar-settings problem, not a sales
> problem. 15-minute intervals plus generous availability plus an auto-generated
> video link removes the friction that quietly kills bookings.**

> 💡 **Carry the details across.** If your funnel already collected name, phone,
> and email, pass those into the calendar so the prospect does not re-type them.
> Owen: people "should not have to fill out their information twice in order to
> book a call." (You will wire this in the funnel lesson next.)

## Part 4: The phone system — Twilio, A2P, and a local number

GHL can hand you a native number in a click, but Owen recommends running phone
and SMS through **Twilio** instead. The reason is control and deliverability:
Twilio gives you a properly registered number, better SMS throughput, and it
survives if you ever move off GHL. Native numbers are convenient but limited.

### Buy a local number and forward it

Connect Twilio to the sub-account, then **buy a local number** in your client's
area code (a local number gets answered more than a toll-free one). Set **call
forwarding** so any call to that number rings your (or the client's) real phone.
Now the CRM number is the public number, every call is logged, and it still
reaches a human.

### A2P 10DLC — the part you cannot skip

Before you send a single business text from that number, US carriers require you
to register it under **A2P 10DLC** ("Application-to-Person, 10-Digit Long Code").
You submit your business details and a "campaign" describing what you will text
about, and the carriers approve the number for business messaging. Unregistered
numbers get their texts filtered or blocked outright.

> ⚠️ **Reality check — this is compliance, not red tape.** In the US, sending
> marketing or outreach texts without registering your A2P campaign and honoring
> opt-outs implicates the **TCPA** (Telephone Consumer Protection Act) and
> carrier rules. You must: (1) register your 10DLC campaign before sending,
> (2) get consent to text where required, and (3) honor **STOP / opt-out**
> automatically on every message. This matters *again* in the cold-SMS lesson
> (Module 6) — unsolicited SMS is heavily regulated, and other countries (UK
> GDPR/PECR, Canada CASL) are stricter still. Set it up correctly now so you are
> not scrambling later.

> 💡 **Alternatives to Twilio.** **Telnyx, Plivo, Bandwidth, or Vonage** are all
> real substitutes with their own dashboards and 10DLC flows. The A2P
> registration requirement is the *carriers'*, not Twilio's — so it applies no
> matter which provider you pick.

## Part 5: Email deliverability — a dedicated sending subdomain

If your automated emails land in spam, the whole machine is pointless. The fix is
a **dedicated sending subdomain** — a subdomain like `mail.youragency.com` used
only for sending, so its reputation is yours to build and one bad campaign never
poisons your main domain.

You set this up by adding DNS records at your domain provider that authenticate
your mail:

- **SPF** — lists which servers may send email as you.
- **DKIM** — cryptographically signs your mail so receivers know it is really you.
- **DMARC** — tells receivers what to do with mail that fails the above.

GHL generates these records; you paste them into your DNS. Owen uses
**Cloudflare** to manage DNS because its dashboard is fast and free.

> ✅ **What to do about it:** connect your domain in GHL's email settings, copy
> the SPF/DKIM/DMARC records it gives you into Cloudflare (or your registrar's
> DNS), wait for them to verify, then send yourself a test email and confirm it
> lands in the inbox, not spam.

> 💡 **Alternatives to Cloudflare.** Any DNS host works: **your registrar's own
> DNS (Namecheap, Porkbun), Bunny.net, or Fastly.** The records are identical
> wherever you host them.

## Part 6: E-signable agreements — replace DocuSign

GHL has a documents/contracts feature that lets a client sign online, so you do
not need a separate e-signature tool. You **upload your service agreement as a
PDF**, then drag **fillable fields** onto it — a signature box, a date, the
client's name — and send it for signature. When they sign, you get a legally
executed contract back, tracked in the CRM.

> 💡 **DocuSign, and alternatives.** GHL's built-in signing **replaces DocuSign**
> for most agency needs. If you prefer a dedicated tool, **PandaDoc or Dropbox
> Sign (formerly HelloSign)** are strong substitutes.

> ⚠️ **A note on contract clauses.** Some coaches teach aggressive clauses
> ("large charge for a missed exit interview," penalties for "false reporting").
> These can be unenforceable and can wreck your local reputation. Keep your first
> agreement simple, fair, and in your own legal name — a clean contract closes
> more clients than a scary one.

## Part 7: The core automations

Automations are the difference between a CRM and a filing cabinet. Set up these
few under **Automation → Workflows**:

1. **Appointment reminders.** Text and/or email the prospect before the call
   (e.g. 24 hours and 1 hour out). This is the single biggest lever on show rate.
2. **Post-call / survey.** After the appointment, send a short survey or
   feedback request — useful data and a professional touch.
3. **New-lead alert.** The moment a lead comes in, text or email *yourself* so
   you can respond fast. Speed-to-lead is a real edge.
4. **The trust email.** A short, personalized email that goes out after booking,
   introducing you and building credibility before the call — the same "warm
   them up" job the VSL does on the page. Personalize it with the first-name
   custom value.

> 🔑 **Reminders are the highest-ROI automation you will ever build. A prospect
> who forgets is a no-show; a prospect who gets a well-timed reminder shows up.
> Turn reminders on before anything else.**

> ❌ **Pitfall:** building an SMS reminder before your A2P campaign is approved.
> The texts silently fail or get filtered and you never see the reminder fire.
> Register first, *then* switch on SMS reminders.

---

## Key takeaways

1. **White-label first.** A branded login turns a solo operator into a company in
   the client's eyes.
2. **Custom values are the DRY principle for your CRM.** Set six, reference them
   everywhere, edit in one place.
3. **Calendar settings drive booking rate.** 15-minute slots, 30–45 minute
   duration, generous availability, auto video link.
4. **A2P 10DLC is mandatory, not optional.** Register your campaign and honor
   opt-outs before any SMS. This returns in the cold-SMS lesson.
5. **Deliverability lives in DNS.** A dedicated sending subdomain with
   SPF/DKIM/DMARC keeps your mail out of spam.
6. **GHL replaces DocuSign.** Upload a PDF, add fields, get signed contracts in
   the CRM.
7. **Reminders are the money automation.** They directly lift show rate.

## Common pitfalls

- ❌ Sending SMS before A2P registration is approved — texts get filtered or
  blocked. Register first.
- ❌ Never wiring opt-out (STOP) handling — this is a legal violation, not a
  nice-to-have. Honor it automatically.
- ❌ Pasting raw phone numbers and links into templates instead of custom values
  — then having to hunt them all down when something changes.
- ❌ Hourly calendar slots with tight availability — you strangle your own
  booking rate.
- ❌ Skipping the email subdomain and sending from your main domain — one bad
  send hurts your primary reputation.
- ❌ Assuming a native GHL number is "good enough" for volume SMS — Twilio (or a
  Telnyx/Plivo/Bandwidth equivalent) with proper 10DLC is the durable choice.

---

## 🛠️ Capstone Project: A fully configured, client-ready sub-account

> This is the main hands-on project for the lesson. When you finish, you will
> have a real, working command center you can hand to a client — or use for your
> own agency — and prove it works by booking a test appointment and watching the
> reminder fire.

### What you will build

One GHL sub-account configured end to end: white-labeled, with custom values, a
live strategy-call calendar, a verified Twilio number forwarding to your phone, a
deliverability subdomain, one uploaded agreement template, and reminders switched
on. Each piece maps to a Part above.

- White-label login → Part 1
- Six custom values → Part 2
- Strategy-call calendar → Part 3
- Verified Twilio number + A2P → Part 4
- Email sending subdomain → Part 5
- One agreement template → Part 6
- Reminder + new-lead automations → Part 7

### Why this is the perfect practice

| Lesson idea | Where you use it in the sub-account |
|---|---|
| White-label | Branded login at your own subdomain |
| Custom values | Booking link + phone reused in every message |
| Calendar settings | 15-min slots, 30–45 min, video link |
| A2P 10DLC | Registered campaign before SMS reminders |
| DNS deliverability | Test email lands in inbox |
| E-sign agreement | One PDF with signature fields |
| Automations | Reminder fires on your test booking |

### Milestones (build them in order, each one works on its own)

1. **White-label the login.** Point a subdomain at GHL, upload your logo, set
   colors. Done when your login page shows your brand, not GoHighLevel.
2. **Create the six custom values.** Phone, booking page, privacy, terms, VSL,
   first name. Done when each has a merge tag you can drop into a message.
3. **Build the strategy-call calendar.** Staff assigned, Google Meet/Zoom
   connected, availability set, 15-min interval, 30–45 min duration, scheduling
   window and minimum notice set. Done when you can view a bookable link.
4. **Stand up the phone line.** Connect Twilio, submit A2P 10DLC registration,
   buy a local number, set call forwarding to your phone. Done when calling the
   number rings your phone. (SMS goes live once A2P is approved.)
5. **Set the email subdomain.** Add SPF/DKIM/DMARC records in Cloudflare, verify
   in GHL, send a test email. Done when the test lands in the inbox, not spam.
6. **Upload one agreement.** Drop in your service-agreement PDF, add signature,
   date, and name fields. Done when you can send it for signature to yourself.
7. **Turn on the automations.** Appointment reminder (24h + 1h), new-lead alert
   to yourself, and the personalized trust email. Done when a workflow is
   published and active.
8. **Stretch goals.** Add the post-call survey workflow; connect Stripe for
   deposits; clone the whole configured sub-account as a template for the next
   client.

### How you will know you are done

- ✅ Your login page is fully branded (no vendor logo).
- ✅ All six custom values exist and render your real data in a test message.
- ✅ A test call to your number forwards to your phone and is logged in the CRM.
- ✅ Your A2P campaign is submitted (and, once approved, a test SMS sends).
- ✅ A test email lands in the inbox with SPF/DKIM/DMARC passing.
- ✅ One agreement template is uploaded with working fillable fields.
- ✅ **You book a test appointment on your own calendar and confirm the reminder
  fires** (email now; SMS once A2P is approved).

> 💡 **Keep yourself honest:** the capstone is not "done" until you have actually
> booked a real test slot and *received* the reminder. Configuring a workflow and
> confirming it fires are two different things — verify, don't assume.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice
> on one idea. Optional and independent; the Capstone already touches all of
> them, so feel free to skip straight to it.

### Exercise 1: Custom-value swap (foundational)
Create the "booking page" custom value, drop its tag into a draft email, then
change the value to a different URL. Confirm the email now shows the new link
without you editing the email. This is the whole point of custom values in one
rep.

### Exercise 2: Calendar friction test (intermediate)
Build the calendar twice — once with hourly slots and once with 15-minute slots
— and open the booking link for each on your phone. Notice how many more options
the 15-minute version offers. Keep the better one.

### Exercise 3: Deliverability audit (advanced)
After setting your SPF/DKIM/DMARC records, send a test email to a mail-tester
tool (search "email deliverability test") and read the score. Fix any record it
flags until you pass. Bonus: send to a Gmail and a non-Gmail inbox and confirm
both land in the primary inbox.

---

## Cheat sheet

```text
GHL COMMAND CENTER — SETUP ORDER
1. White-label     → subdomain CNAME + logo + colors (Agency Settings)
2. Custom values   → phone, booking, privacy, terms, VSL, first name
3. Calendar        → staff · Meet/Zoom · availability · 15-min · 30-45 min
                     · scheduling window + min notice
4. Phone (Twilio)  → connect · A2P 10DLC REGISTER · buy local # · forward
                     (alts: Telnyx, Plivo, Bandwidth, Vonage)
5. Email           → dedicated subdomain · SPF + DKIM + DMARC in Cloudflare
                     (alts: Namecheap/Porkbun DNS, Bunny, Fastly)
6. Agreement       → upload PDF + fillable fields (replaces DocuSign;
                     alts: PandaDoc, Dropbox Sign)
7. Automations     → reminders (24h+1h) · new-lead alert · trust email · survey

COMPLIANCE (not optional):
  • A2P 10DLC registered BEFORE any SMS
  • Honor STOP / opt-out automatically on every text
  • TCPA (US) applies; UK GDPR/PECR + Canada CASL are stricter
  • Returns in Module 6 (cold SMS)

DONE = book a test appointment → reminder fires.

CALENDAR TARGETS: 15-min slots · 30-45 min duration · generous availability
GHL ALTERNATIVES: HubSpot · Keap · Close · Vendasta · or Cal.com+Zapier+Brevo
```

## How this connects to the rest of the course

- **Earlier, Module 4 · Lesson 10:** you created the sub-account and account
  structure — this lesson filled that empty shell with working systems.
- **Next, Module 4 · Lesson 12:** you build your funnel with Lovable, which feeds
  leads into the calendar and custom values you just set up (and passes contact
  details straight through so nobody types their info twice).
- **Later, Module 6 (Outreach):** the phone number, A2P registration, and
  opt-out handling you configured here become mandatory the moment you send cold
  SMS — the compliance you set up now is what keeps that outreach legal.

---

*Source: "AI Agency Full Course" by Owen Rensland. Prices, settings, KPI numbers,
and any config shown are illustrative reconstructions of the patterns described
in the course. Menu names in GoHighLevel and other tools change often — adapt
these steps to the current interface.*
